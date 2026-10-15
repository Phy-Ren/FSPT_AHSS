#!/usr/bin/env python3
"""Extend completed finite 3+1D CI point-group runs by the selected E8 section.

The output is a separate immutable campaign. It computes signed integer H1
and a combined relation presentation, and never reads literature tables.
It does not certify the remaining physical CI-kernel identification.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import platform
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))

from insulator.e8_pointgroup import MODEL, PHYSICAL_CAVEAT, extend_classification


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write_json(path: Path, value) -> None:
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def source_manifest() -> dict:
    import sympy

    files = ["insulator/e8_pointgroup.py", "insulator/e8_h1.py",
             "scripts/extend_e8_3p1.py", "docs/e8/3p1.md"]
    hashes = {name: digest(ROOT / name) for name in files}
    encoded = json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()
    return {"sha256": hashlib.sha256(encoded).hexdigest(), "files": hashes,
            "pythonVersion": platform.python_version(), "sympyVersion": sympy.__version__,
            "model": MODEL, "physicalScopeCaveat": PHYSICAL_CAVEAT}


def extend_run(path: Path, output: Path, source: dict) -> dict:
    raw = path.read_bytes()
    result = json.loads(raw)
    classification = extend_classification(result)
    case = result["input"]["id"]
    if not isinstance(case, str) or Path(case).name != case or case in ("", ".", ".."):
        raise ValueError("Invalid case identifier.")
    companion = path.parent / "input.json"
    if not companion.is_file():
        raise ValueError("The immutable CI companion input.json is required.")
    input_raw = companion.read_bytes()
    input_hash = hashlib.sha256(input_raw).hexdigest()
    if json.loads(input_raw) != result["input"] or input_hash != result["run"].get("inputSHA256"):
        raise ValueError("The CI input hash or embedded catalog input does not match input.json.")
    result_hash = hashlib.sha256(raw).hexdigest()
    ci_source_hash = result["run"].get("sourceSHA256")
    if not isinstance(ci_source_hash, str) or len(ci_source_hash) != 64:
        raise ValueError("The completed CI run lacks a valid source hash.")
    metadata = {"id": case, "status": "complete", "exitCode": 0,
                "host": platform.node(), "startedUTC": datetime.now(timezone.utc).isoformat(),
                "operation": "exact-selected-section-E8-extension",
                "inputSHA256": input_hash, "sourceSHA256": source["sha256"],
                "ciResultPath": str(path.resolve()), "ciResultSHA256": result_hash,
                "ciSourceSHA256": ci_source_hash, "ciRun": result["run"],
                "physicalClassificationCertified": False}
    directory = output / case
    directory.mkdir()  # An existing accepted result must never be overwritten.
    (directory / "input.json").write_bytes(input_raw)
    # Preserve the exact consumed CI artifact, including all cochain witnesses.
    (directory / "ci_result.json").write_bytes(raw)
    write_json(directory / "run.json", metadata)
    write_json(directory / "result.json", {"input": result["input"],
               "classification": classification, "run": metadata})
    return {"id": case, "spin": result["input"]["spin"], "status": "complete",
            "torsion": classification["torsion"], "freeRank": classification["freeRank"],
            "ciTorsion": result["classification"]["torsion"],
            "ciFreeRank": result["classification"]["freeRank"],
            "e8H1Torsion": classification["e8H1"]["torsion"],
            "e8H1FreeRank": classification["e8H1"]["freeRank"],
            "ciResultSHA256": result_hash, "sourceSHA256": source["sha256"],
            "physicalClassificationCertified": False}


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ci-root", required=True, type=Path,
                        help="A completed classify.py campaign containing case/result.json")
    parser.add_argument("--output", required=True, type=Path,
                        help="A new separate immutable E8-inclusive campaign directory")
    parser.add_argument("--case", action="append", help="Catalog ID; repeat to select cases")
    parser.add_argument("--spin", choices=("spinless", "spin_half"))
    args = parser.parse_args(argv)
    root = args.ci_root.resolve()
    selection_path = root / "selection.json"
    if not selection_path.is_file():
        parser.error("The CI campaign must retain selection.json.")
    selection = json.loads(selection_path.read_text())
    if not isinstance(selection, list) or not selection or len(set(selection)) != len(selection):
        parser.error("The CI campaign selection must contain distinct case IDs.")
    paths = []
    for case in selection:
        if not isinstance(case, str) or Path(case).name != case or case in ("", ".", ".."):
            parser.error("The CI campaign has an invalid case ID.")
        if args.case and case not in args.case:
            continue
        # IDs are validated against embedded input metadata below. Filtering a
        # case by spin never supplies group-theoretic information to the solver.
        if args.spin and not case.endswith("_" + args.spin):
            continue
        path = root / case / "result.json"
        if not path.is_file():
            parser.error(f"Selected CI result is missing or unfinished: {case}")
        result = json.loads(path.read_text())
        if result.get("input", {}).get("id") != case or (
                args.spin and result["input"].get("spin") != args.spin):
            parser.error(f"Selected CI metadata does not match: {case}")
        paths.append(path)
    if not paths or args.case and set(args.case) != {p.parent.name for p in paths}:
        parser.error("Selection includes missing or incompatible cases.")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = source_manifest()
    source["ciSelectionSHA256"] = digest(selection_path)
    write_json(output / "source.json", source)
    write_json(output / "selection.json", [p.parent.name for p in paths])
    summaries = []
    for path in paths:
        row = extend_run(path, output, source)
        summaries.append(row)
        print(row["id"], row["torsion"], "freeRank=" + str(row["freeRank"]), flush=True)
        write_json(output / "summary.json", sorted(summaries, key=lambda item: item["id"]))
    current = source_manifest()
    if current["sha256"] != source["sha256"]:
        raise RuntimeError("Extension source changed during the calculation.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
