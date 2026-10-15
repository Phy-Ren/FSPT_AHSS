#!/usr/bin/env python3
"""Run exact insulator classifications with immutable inputs and complete logs.

The formula engine never reads the separate literature benchmark tables.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import platform
import select
import shutil
import signal
import subprocess
import threading
import time

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_manifest():
    files = []
    for directory, suffixes in (("gap", {".g"}), ("insulator", {".py", ".json", ".cpp", ".h"}),
                                ("scripts", {".py"})):
        files.extend(p for p in (ROOT / directory).rglob("*") if p.suffix in suffixes)
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in sorted(files)}
    encoded = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "files": hashes}


def formula_runtime_manifest():
    """Record the selected VM artifact; individual requests may use exact fallback."""
    library = Path(os.environ.get("U1_DAG_LIBRARY", str(ROOT / "insulator/_compiled/u1_dag_vm.so"))).resolve()
    return {"requestedMode": os.environ.get("U1_DAG_MODE", "auto"),
            "libraryPath": str(library), "libraryPresent": library.is_file(),
            "librarySHA256": digest(library) if library.is_file() else None,
            "fallbackPolicy": "exact Python integer DAG or original U1 formula according to request eligibility"}


def gap_literal(value):
    if value is True:
        return "true"
    if value is False:
        return "false"
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=True)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return "[" + ",".join(map(gap_literal, value)) + "]"
    if isinstance(value, dict):
        if not all(k.replace("_", "").isalnum() and not k[0].isdigit() for k in value):
            raise ValueError("Unsupported GAP record key")
        return "rec(" + ",".join(k + ":=" + gap_literal(v) for k, v in value.items()) + ")"
    raise TypeError("Catalog input must contain only exact JSON values")


def write_json(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def acceleration_options(charge_primary, phase_class, closed_charge_source):
    if charge_primary not in {"bar", "native", "compare"}:
        raise ValueError("Unknown charge primary mode")
    if phase_class not in {"cycles", "native", "compare"}:
        raise ValueError("Unknown phase class mode")
    if closed_charge_source not in {"certified", "reference", "compare"}:
        raise ValueError("Unknown closed charge source mode")
    return ("c.chargePrimaryMode:=" + gap_literal(charge_primary) + ";;\n"
            "c.phaseClassMode:=" + gap_literal(phase_class) + ";;\n"
            "c.closedChargeSourceMode:=" + gap_literal(closed_charge_source) + ";;\n")


def run_case(input_path, output, gap, timeout, memory, source, uniform_iqh=False,
             charge_primary="native", phase_class="cycles", closed_charge_source="certified"):
    data = json.loads(input_path.read_text())
    directory = output / data["id"]
    directory.mkdir()  # Never overwrite accepted results or another running case.
    shutil.copyfile(input_path, directory / "input.json")
    native = directory / "native.json"
    driver = directory / "driver.g"
    driver.write_text(
        "U1_ROOT:=" + gap_literal(str(ROOT)) + ";;\n"
        + ("U1_USE_KOSZUL:=true;;\n" if data["family"] == "spacegroup" else "")
        +
        "Read(Concatenation(U1_ROOT,\"/gap/load.g\"));;\n"
        "U1_INPUT:=" + gap_literal(data) + ";;\n"
        "c:=U1CatalogContext(U1_INPUT,6);;\n"
        + acceleration_options(charge_primary, phase_class, closed_charge_source) +
        "result:=U1Classify(c,U1_INPUT.dimension,rec(uniformIQH:="
        + gap_literal(uniform_iqh) + "));;\n"
        "output:=OutputTextFile(" + gap_literal(str(native)) + ",false);;\n"
        "SetPrintFormattingStatus(output,false);;\n"
        "PrintTo(output,U1JSON(result),\"\\n\");;\n"
        "CloseStream(output);;\nif IsBound(c.worker) then CloseStream(c.worker);fi;\nQUIT;\n"
    )
    command = [gap, "-q", "-b", "--quitonbreak", "-m", "256m", "-K", memory, str(driver)]
    start = time.monotonic()
    metadata = {"id": data["id"], "status": "running", "command": command,
                "host": platform.node(), "startedUTC": datetime.now(timezone.utc).isoformat(),
                "inputSHA256": digest(input_path), "sourceSHA256": source["sha256"],
                "timeoutSeconds": timeout, "uniformIQHRequested": uniform_iqh,
                "chargePrimaryRequested": charge_primary, "phaseClassRequested": phase_class,
                "closedChargeSourceRequested": closed_charge_source}
    write_json(directory / "run.json", metadata)
    with (directory / "stdout.log").open("w") as out, (directory / "stderr.log").open("w") as err:
        process = subprocess.Popen(command, cwd=ROOT, stdout=out, stderr=err,
                                   start_new_session=True)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = process.returncode
            metadata["status"] = "timeout"
    metadata.update(exitCode=code, elapsedSeconds=round(time.monotonic() - start, 3))
    if metadata["status"] != "timeout":
        metadata["status"] = "failed"
        if code == 0 and native.exists():
            try:
                classification = json.loads(native.read_text())
                required = {"torsion", "freeRank", "presentation", "witnesses", "scope"}
                if not required <= classification.keys():
                    raise ValueError("Incomplete classification result")
                metadata["status"] = "complete"
                write_json(directory / "result.json", {"input": data,
                           "classification": classification, "run": metadata})
            except (ValueError, TypeError) as error:
                metadata["error"] = str(error)
    write_json(directory / "run.json", metadata)
    return metadata


def _pump_pair_stdout(stream, log, case_ids, observed, stop, errors, capture):
    """Copy exact bytes and timestamp complete, ordered marker lines on this node.

    A stopped child may leave stdout inherited by another process. After the
    runner has exited, drain available bytes but do not wait forever for that
    inherited descriptor. Normal GAP shutdown supplies EOF before this limit.
    Markers in the same pipe read share one observation timestamp, so a very
    short second interval can legitimately be zero at this timing granularity.
    """
    markers = [("U1_PAIR_CASE_DONE " + case).encode("utf-8") for case in case_ids]
    max_line = max(map(len, markers))
    pending = b""
    next_case = 0
    drain_started = None
    try:
        while True:
            if stop.is_set() and drain_started is None:
                drain_started = time.monotonic()
            ready, _, _ = select.select([stream.fileno()], [], [], 0.05)
            if ready:
                chunk = os.read(stream.fileno(), 65536)
                seen = time.monotonic()  # Before potentially slow shared-filesystem writes.
                if not chunk:
                    capture["eofObserved"] = True
                    break
                parts = chunk.split(b"\n")
                for index, part in enumerate(parts):
                    # Only marker-sized lines need buffering; every byte is logged below.
                    pending += part[:max(0, max_line + 1 - len(pending))]
                    if index < len(parts) - 1:
                        if next_case < len(markers) and pending == markers[next_case]:
                            observed[case_ids[next_case]] = seen
                            next_case += 1
                        pending = b""
                log.write(chunk)
                log.flush()  # Make completion evidence promptly visible to offline recovery.
            if drain_started is not None:
                if not ready:
                    capture["inheritedPipeClosedAfterIdle"] = True
                    break
                if time.monotonic() - drain_started >= 1.0:
                    capture["inheritedPipeDrainLimitReached"] = True
                    break
    except Exception as error:
        errors.append(error)
    finally:
        stream.close()


def run_spin_pair(input_paths, output, gap, timeout, memory, source, uniform_iqh=False,
                  charge_primary="native", phase_class="cycles", closed_charge_source="certified"):
    """One GAP process, separate immutable outputs and independent omega contexts."""
    if len(input_paths) == 1:
        return [run_case(input_paths[0], output, gap, timeout, memory, source, uniform_iqh,
                         charge_primary, phase_class, closed_charge_source)]
    if len(input_paths) != 2:
        raise ValueError("A paired run requires the two physical spins of one geometry")
    inputs = [json.loads(path.read_text()) for path in input_paths]
    if len({(data["family"], data["index"], data["dimension"]) for data in inputs}) != 1 or {
            data["spin"] for data in inputs} != {"spinless", "spin_half"}:
        raise ValueError("Paired inputs must have the same geometry and distinct physical spins")
    directories = [output / data["id"] for data in inputs]
    for directory, path in zip(directories, input_paths):
        directory.mkdir()
        shutil.copyfile(path, directory / "input.json")
    text = "U1_ROOT:=" + gap_literal(str(ROOT)) + ";;\n"
    if inputs[0]["family"] == "spacegroup":
        text += "U1_USE_KOSZUL:=true;;\n"
    text += 'Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n'
    for i, (data, directory) in enumerate(zip(inputs, directories)):
        text += "U1_INPUT:=" + gap_literal(data) + ";;\n"
        if i == 0:
            text += "c:=U1CatalogContext(U1_INPUT,6);;\n"
        else:
            text += "if IsBound(c.classificationStates) then Unbind(c.classificationStates);fi;\n"
            text += "c:=U1SiblingContext(c,U1_INPUT);;\n"
        text += acceleration_options(charge_primary, phase_class, closed_charge_source)
        text += "result:=U1Classify(c,U1_INPUT.dimension,rec(uniformIQH:=" + gap_literal(uniform_iqh) + "));;\n"
        text += "output:=OutputTextFile(" + gap_literal(str(directory / "native.json")) + ",false);;\n"
        text += "SetPrintFormattingStatus(output,false);;\nPrintTo(output,U1JSON(result),\"\\n\");;\nCloseStream(output);;\n"
        text += 'Print("U1_PAIR_CASE_DONE ",U1_INPUT.id,"\\n");;\n'
    text += "if IsBound(c.worker) then CloseStream(c.worker);fi;\nQUIT;\n"
    for directory in directories:
        (directory / "driver.g").write_text(text)
    command = [gap, "-q", "-b", "--quitonbreak", "-m", "256m", "-K", memory,
               str(directories[0] / "driver.g")]
    started = time.time()
    started_monotonic = time.monotonic()
    metadata = []
    for data, path, directory in zip(inputs, input_paths, directories):
        row = {"id": data["id"], "status": "running", "command": command,
               "host": platform.node(), "startedUTC": datetime.fromtimestamp(started, timezone.utc).isoformat(),
               "inputSHA256": digest(path), "sourceSHA256": source["sha256"],
               "timeoutSeconds": timeout, "batchTimeoutSeconds": timeout * len(inputs),
               "timeoutEnforcement": "shared batch budget; individual cases are not killed separately",
               "uniformIQHRequested": uniform_iqh,
               "chargePrimaryRequested": charge_primary, "phaseClassRequested": phase_class,
               "closedChargeSourceRequested": closed_charge_source,
               "pairedSpins": True, "batchCaseIDs": [item["id"] for item in inputs],
               "timingMethod": "ordered-stdout-completion-markers-observed-with-time.monotonic",
               "timingGranularity": "one-observation-timestamp-per-pipe-read",
               "batchTimingMethod": "time.monotonic-including-stdout-drain",
               "startedUTCMethod": "batch-wall-anchor-plus-monotonic-offset",
               "reusePolicy": "same group/resolution/bar and identical character linear algebra; independent omega/source contexts"}
        write_json(directory / "run.json", row)
        metadata.append(row)
    timed_out = False
    observed, pump_errors = {}, []
    capture = {"eofObserved": False, "inheritedPipeClosedAfterIdle": False,
               "inheritedPipeDrainLimitReached": False}
    stop_pump = threading.Event()
    with (directories[0] / "stdout.log").open("wb") as out, (directories[0] / "stderr.log").open("wb") as err:
        process = subprocess.Popen(command, cwd=ROOT, stdout=subprocess.PIPE, stderr=err,
                                   bufsize=0, start_new_session=True)
        pump = threading.Thread(target=_pump_pair_stdout,
                                args=(process.stdout, out, [data["id"] for data in inputs],
                                      observed, stop_pump, pump_errors, capture), daemon=True)
        pump.start()
        try:
            try:
                code = process.wait(timeout=timeout * len(inputs))
            except subprocess.TimeoutExpired:
                timed_out = True
                os.killpg(process.pid, signal.SIGTERM)
                try:
                    process.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    os.killpg(process.pid, signal.SIGKILL)
                    process.wait()
                code = process.returncode
        finally:
            stop_pump.set()
            pump.join()
        if pump_errors:
            raise pump_errors[0]
    ended_monotonic = time.monotonic()
    for directory in directories[1:]:
        for name in ("stdout.log", "stderr.log"):
            shutil.copyfile(directories[0] / name, directory / name)
    previous_completion = started_monotonic
    for data, directory, row in zip(inputs, directories, metadata):
        native = directory / "native.json"
        completed = observed.get(data["id"])
        row.update(completionMarkerObserved=completed is not None,
                   caseStartBoundaryAvailable=previous_completion is not None,
                   caseTimingAvailable=completed is not None and previous_completion is not None,
                   elapsedSeconds=None, stdoutCapture=dict(capture))
        if previous_completion is not None:
            row["startedUTC"] = datetime.fromtimestamp(
                started + previous_completion - started_monotonic, timezone.utc).isoformat()
        else:
            row["startedUTCMethod"] = "batch-wall-anchor; individual-case-start-unavailable"
        if row["caseTimingAvailable"]:
            row["elapsedSeconds"] = round(completed - previous_completion, 3)
        else:
            row["timingUnavailableReason"] = "exact ordered completion marker or previous boundary not observed"
        row.update(status="timeout" if timed_out else "failed", exitCode=code,
                   batchExitCode=code, batchElapsedSeconds=round(ended_monotonic - started_monotonic, 3))
        if native.is_file():
            try:
                classification = json.loads(native.read_text())
                required = {"torsion", "freeRank", "presentation", "witnesses", "scope"}
                if not required <= classification.keys():
                    raise ValueError("Incomplete paired classification result")
                row.update(status="complete", exitCode=0)
                write_json(directory / "result.json", {"input": data, "classification": classification, "run": row})
            except (ValueError, TypeError) as error:
                row["error"] = str(error)
        previous_completion = completed
        write_json(directory / "run.json", row)
    return metadata


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=("point2", "wallpaper", "point3", "spacegroup"))
    parser.add_argument("--case", action="append", help="Catalog ID; repeat to select cases")
    parser.add_argument("--spin", choices=("spinless", "spin_half"))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--gap", default=os.environ.get("GAP", "gap"))
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--pair-spins", action="store_true",
                        help="Reuse exact geometry/linear algebra in one process for the two physical spins")
    parser.add_argument("--largest-first", action="store_true",
                        help="Schedule larger finite holonomy orders first to reduce the campaign tail")
    parser.add_argument("--timeout", type=int, default=7200)
    parser.add_argument("--memory", default="8g", help="GAP workspace limit per process")
    parser.add_argument("--uniform-iqh", action="store_true",
                        help="Include the 2+1D uniform integer Hall layer")
    parser.add_argument("--charge-primary", choices=("bar", "native", "compare"), default="native",
                        help="Primary charge obstruction class: native exact operations, bar reference, or agreement check")
    parser.add_argument("--phase-class", choices=("cycles", "native", "compare"), default="cycles",
                        help="Closed bar phase class: Smith cycle periods, all native cells, or agreement check")
    parser.add_argument("--closed-charge-source", choices=("certified", "reference", "compare"), default="certified",
                        help="Full closed charge source: certified binary expression, original expression, or pointwise agreement check")
    args = parser.parse_args()
    if not args.family and not args.case:
        parser.error("Select --family or --case")
    if args.jobs < 1 or args.timeout < 1:
        parser.error("jobs and timeout must be positive")
    inputs = []
    for path in sorted((ROOT / "insulator_catalog/generated").glob("*.json")):
        if path.name.endswith(".index.json"):
            continue
        record = json.loads(path.read_text())
        if args.case and record["id"] not in args.case:
            continue
        if args.family and record["family"] != args.family:
            continue
        if args.spin and record["spin"] != args.spin:
            continue
        if args.uniform_iqh and record["dimension"] != 2:
            parser.error("--uniform-iqh applies only to spatial dimension two")
        inputs.append(path)
    if not inputs or args.case and set(args.case) != {p.stem for p in inputs}:
        parser.error("Selection includes missing or incompatible catalog cases")
    if args.largest_first:
        inputs.sort(key=lambda path: (-len(json.loads(path.read_text())["multiplication"]), path.stem))
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    source = source_manifest()
    formula_runtime = formula_runtime_manifest()
    write_json(args.output / "source.json", source)
    write_json(args.output / "formula_runtime.json", formula_runtime)
    write_json(args.output / "selection.json", [p.stem for p in inputs])
    rows = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        if args.pair_spins:
            pairs = {}
            for path in inputs:
                data = json.loads(path.read_text())
                pairs.setdefault((data["family"], data["index"]), []).append(path)
            tasks = [pool.submit(run_spin_pair, paths, args.output, args.gap, args.timeout,
                                 args.memory, source, args.uniform_iqh,
                                 args.charge_primary, args.phase_class,
                                 args.closed_charge_source) for paths in pairs.values()]
        else:
            tasks = [pool.submit(run_case, p, args.output, args.gap, args.timeout,
                                 args.memory, source, args.uniform_iqh,
                                 args.charge_primary, args.phase_class,
                                 args.closed_charge_source) for p in inputs]
        for task in as_completed(tasks):
            completed = task.result()
            if isinstance(completed, dict):
                completed = [completed]
            rows.extend(completed)
            for row in completed:
                print(row["id"], row["status"], row["elapsedSeconds"], flush=True)
            write_json(args.output / "summary.json", sorted(rows, key=lambda r: r["id"]))
    if source_manifest() != source:
        raise RuntimeError("Source changed during campaign; results cannot be accepted")
    if formula_runtime_manifest() != formula_runtime:
        raise RuntimeError("Formula VM artifact changed during campaign; results cannot be accepted")
    return 0 if all(r["status"] == "complete" for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
