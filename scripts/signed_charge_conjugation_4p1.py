#!/usr/bin/env python3
"""Run exact signed C2 four-data examples, retaining complete global witnesses."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from insulator.signed_charge_conjugation_4p1 import CASES, C2FourData


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def manifest():
    # The 4+1D engine uses these Python modules and fixed operation arrays;
    # the 3+1D compiled VM and GAP are not invoked by this calculation.
    files = sorted(path for path in (ROOT / "insulator").rglob("*")
                   if path.suffix in (".py", ".json"))
    files.append(Path(__file__).resolve())
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in files}
    return {"files": hashes, "sha256": hashlib.sha256(
        json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}


def run_case(case, output, source):
    solver = C2FourData(case)
    data = solver.input()
    directory = output / data["id"]
    directory.mkdir()
    write_json(directory / "input.json", data)
    run = {"status": "running", "id": data["id"], "host": platform.node(),
           "pythonVersion": platform.python_version(), "sourceSHA256": source["sha256"],
           "inputSHA256": hashlib.sha256((directory / "input.json").read_bytes()).hexdigest(),
           "startedUTC": datetime.now(timezone.utc).isoformat()}
    write_json(directory / "run.json", run)
    start = time.monotonic()
    try:
        classification = solver.classify()
        run.update(status="complete", exitCode=0, elapsedSeconds=round(time.monotonic() - start, 6))
        write_json(directory / "result.json", {"input": data, "classification": classification,
                   "physicalComparison": {"status": "independent_target_not_loaded_by_solver",
                                          "universalPhysicalSpectrumCertified": False}, "run": run})
    except Exception as error:
        run.update(status="failed", exitCode=1, elapsedSeconds=round(time.monotonic() - start, 6),
                   exception=type(error).__name__, error=str(error))
        write_json(directory / "run.json", run)
        raise
    write_json(directory / "run.json", run)
    return run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--case", action="append", choices=tuple(CASES))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    selected = args.case or list(CASES)
    if len(set(selected)) != len(selected):
        parser.error("Each case may be selected only once")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = manifest()
    write_json(output / "source.json", source)
    write_json(output / "selection.json", selected)
    campaign = {"status": "running", "selectedCases": selected, "sourceSHA256": source["sha256"],
                "startedUTC": datetime.now(timezone.utc).isoformat()}
    write_json(output / "campaign.json", campaign)
    summary = []
    for case in selected:
        run = run_case(case, output, source)
        summary.append(run)
        write_json(output / "summary.json", summary)
        print(run["id"], run["status"], run["elapsedSeconds"], flush=True)
    if manifest() != source:
        raise RuntimeError("Source changed during the run; retain this output as unaccepted evidence")
    campaign.update(status="complete", completedUTC=datetime.now(timezone.utc).isoformat(),
                    caseCount=len(summary), runs=summary)
    write_json(output / "campaign.json", campaign)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
