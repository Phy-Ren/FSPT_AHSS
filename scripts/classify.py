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
import shutil
import signal
import subprocess
import time

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def source_manifest():
    files = []
    for directory, suffixes in (("gap", {".g"}), ("insulator", {".py", ".json"}),
                                ("scripts", {".py"})):
        files.extend(p for p in (ROOT / directory).rglob("*") if p.suffix in suffixes)
    hashes = {str(p.relative_to(ROOT)): digest(p) for p in sorted(files)}
    encoded = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "files": hashes}


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


def run_case(input_path, output, gap, timeout, memory, source):
    data = json.loads(input_path.read_text())
    directory = output / data["id"]
    directory.mkdir()  # Never overwrite accepted results or another running case.
    shutil.copyfile(input_path, directory / "input.json")
    native = directory / "native.json"
    driver = directory / "driver.g"
    driver.write_text(
        "U1_ROOT:=" + gap_literal(str(ROOT)) + ";;\n"
        "Read(Concatenation(U1_ROOT,\"/gap/load.g\"));;\n"
        "U1_INPUT:=" + gap_literal(data) + ";;\n"
        "c:=U1CatalogContext(U1_INPUT,6);;\n"
        "result:=U1Classify(c,U1_INPUT.dimension);;\n"
        "output:=OutputTextFile(" + gap_literal(str(native)) + ",false);;\n"
        "SetPrintFormattingStatus(output,false);;\n"
        "PrintTo(output,U1JSON(result),\"\\n\");;\n"
        "CloseStream(output);;\nQUIT;\n"
    )
    command = [gap, "-q", "-b", "--quitonbreak", "-m", "256m", "-K", memory, str(driver)]
    start = time.monotonic()
    metadata = {"id": data["id"], "status": "running", "command": command,
                "host": platform.node(), "startedUTC": datetime.now(timezone.utc).isoformat(),
                "inputSHA256": digest(input_path), "sourceSHA256": source["sha256"],
                "timeoutSeconds": timeout}
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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--family", choices=("point2", "wallpaper", "point3"))
    parser.add_argument("--case", action="append", help="Catalog ID; repeat to select cases")
    parser.add_argument("--spin", choices=("spinless", "spin_half"))
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--gap", default=os.environ.get("GAP", "gap"))
    parser.add_argument("--jobs", type=int, default=1)
    parser.add_argument("--timeout", type=int, default=7200)
    parser.add_argument("--memory", default="8g", help="GAP workspace limit per process")
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
        inputs.append(path)
    if not inputs or args.case and set(args.case) != {p.stem for p in inputs}:
        parser.error("Selection includes missing or incompatible catalog cases")
    args.output = args.output.resolve()
    args.output.mkdir(parents=True, exist_ok=False)
    source = source_manifest()
    write_json(args.output / "source.json", source)
    write_json(args.output / "selection.json", [p.stem for p in inputs])
    rows = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        tasks = [pool.submit(run_case, p, args.output, args.gap, args.timeout,
                             args.memory, source) for p in inputs]
        for task in as_completed(tasks):
            row = task.result()
            rows.append(row)
            print(row["id"], row["status"], row["elapsedSeconds"], flush=True)
            write_json(args.output / "summary.json", sorted(rows, key=lambda r: r["id"]))
    if source_manifest() != source:
        raise RuntimeError("Source changed during campaign; results cannot be accepted")
    return 0 if all(r["status"] == "complete" for r in rows) else 1


if __name__ == "__main__":
    raise SystemExit(main())
