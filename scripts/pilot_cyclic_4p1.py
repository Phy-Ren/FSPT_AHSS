#!/usr/bin/env python3
"""Run an isolated, exact 4+1D four-data cyclic classification pilot.

Inputs are internal unitary C_N with s=rho=0 and omega=0. No crystalline
spin convention or intrinsic r0 coefficient is inferred from the cyclic name.
Each case retains its full cochain-root relation witnesses and source hashes.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.classify import gap_literal, source_manifest, write_json


def run_case(order, output, source, gap, timeout, memory):
    case = "internal_cyclic_{}_4p1".format(order)
    directory = output / case
    directory.mkdir()
    data = {"id": case, "dimension": 4, "family": "internal_cyclic", "order": order,
            "s": 0, "rho": 0, "omega": "0", "orderedFields": ["e_2", "n_2", "n_4", "nu_5"],
            "intrinsicR0Included": False, "crystallineSpinConvention": "not_assumed"}
    write_json(directory / "input.json", data)
    native = directory / "native.json"
    driver = directory / "driver.g"
    driver.write_text(
        "U1_ROOT:=" + gap_literal(str(ROOT)) + ";;\n"
        'Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n'
        'Read(Concatenation(U1_ROOT,"/formulas/examples/cyclic_4p1.g"));;\n'
        "result:=U1CyclicFourData(" + str(order) + ");;\n"
        "out:=OutputTextFile(" + gap_literal(str(native)) + ",false);;\n"
        'SetPrintFormattingStatus(out,false);;WriteLine(out,U1JSON(result));;CloseStream(out);;QUIT_GAP(0);\n')
    command = [gap, "-q", "-b", "--quitonbreak", "-m", "256m", "-K", memory, str(driver)]
    run = {"id": case, "status": "running", "host": platform.node(), "command": command,
           "startedUTC": datetime.now(timezone.utc).isoformat(), "sourceSHA256": source["sha256"],
           "inputSHA256": hashlib.sha256((directory / "input.json").read_bytes()).hexdigest(),
           "timeoutSeconds": timeout}
    write_json(directory / "run.json", run)
    start = time.monotonic()
    with (directory / "stdout.log").open("w") as stdout, (directory / "stderr.log").open("w") as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr, cwd=ROOT, start_new_session=True)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            import os
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = process.returncode
            run["status"] = "timeout"
    run.update(exitCode=code, elapsedSeconds=round(time.monotonic() - start, 3))
    if run["status"] != "timeout":
        run["status"] = "failed"
        if code == 0 and native.is_file():
            classification = json.loads(native.read_text())
            required = {"presentation", "witnesses", "torsion", "expectedOrderFromFiltration", "actualGroupOrder"}
            if not required <= set(classification):
                raise ValueError("Incomplete cyclic classification artifact")
            run["status"] = "complete"
            write_json(directory / "result.json", {"input": data, "classification": classification, "run": run})
    write_json(directory / "run.json", run)
    return run


def manifest():
    source = source_manifest()
    path = "formulas/examples/cyclic_4p1.g"
    source["files"][path] = hashlib.sha256((ROOT / path).read_bytes()).hexdigest()
    source["sha256"] = hashlib.sha256(json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()).hexdigest()
    return source


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--order", action="append", type=int, required=True)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--gap", default="gap")
    parser.add_argument("--timeout", type=int, default=1800)
    parser.add_argument("--memory", default="8g")
    args = parser.parse_args()
    if any(n < 1 for n in args.order) or len(set(args.order)) != len(args.order) or args.timeout < 1:
        parser.error("Use distinct positive cyclic orders and a positive timeout")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = manifest()
    write_json(output / "source.json", source)
    write_json(output / "selection.json", args.order)
    summary = []
    for order in args.order:
        row = run_case(order, output, source, args.gap, args.timeout, args.memory)
        summary.append(row)
        write_json(output / "summary.json", summary)
        print(row["id"], row["status"], row["elapsedSeconds"], flush=True)
    if manifest() != source:
        raise RuntimeError("Source changed during the pilot; preserve this run as unaccepted evidence")
    return 0 if all(row["status"] == "complete" for row in summary) else 1


if __name__ == "__main__":
    raise SystemExit(main())
