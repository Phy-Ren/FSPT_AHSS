#!/usr/bin/env python3
"""Run complete four-data examples for rank-one through rank-four translations."""
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

from insulator.translation4p1 import calculate, verify_certificate


def write_json(path, data):
    path.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")


def manifest():
    files = sorted(path for path in (ROOT / "insulator").rglob("*")
                   if path.suffix in (".py", ".json"))
    files.extend((Path(__file__).resolve(), ROOT / "formulas/v015_provenance.json"))
    hashes = {str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
              for path in files}
    return {"files": hashes, "sha256": hashlib.sha256(
        json.dumps(hashes, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}


def input_record(rank):
    return {"id": "translations_z{}_4p1".format(rank), "dimension": 4,
            "family": "translations", "translationRank": rank, "schema_version": 2, "s": 0, "r": 0, "rho": 0, "omega": "0",
            "referenceTarget": "translations_z{}".format(rank),
            "spatialInterpretation": "full four-dimensional translations" if rank == 4 else "partial translations in four spatial dimensions",
            "physicalSpin": "not_applicable", "spinScope": "Pure translations have no rotation-spin lift distinction.",
            "atomicFillingRetained": True, "orderedFields": ["e_2", "n_2", "n_4", "nu_5"],
            "intrinsicRowIncluded": False}


def uniform_response(free_rank):
    return {"intrinsicFreeRank": 2, "intrinsicBasis": ["I", "J"],
            "fullGroup": {"torsion": [], "freeRank": free_rank + 2},
            "section": "Pull back each symmetry-independent intrinsic root along B(U1f x Z^r) -> BU1f; forgetting translations is a retraction.",
            "splitting": "The physical natural section splits off Z I plus Z J from the zero-uniform kernel.",
            "zeroLowerLift": {"background": "s=r=omega=0", "intrinsicInputs": [[1, 0], [0, 1]],
                              "lowerFields": {"e_2": 0, "n_2": 0, "n_4": 0, "nu_5": 0},
                              "check": "B=0 and all opened-sheet, charge, and terminal terms vanish by direct zero-input substitution.",
                              "evidenceType": "Physical natural section and direct substitution, not an intrinsic formula-runtime execution."},
            "cochainIntrinsicImplemented": False}


def run_case(rank, output, source):
    data = input_record(rank)
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
        classification, evidence = calculate(rank)
        write_json(directory / "simplicial_evidence.json", evidence)
        evidence_record = {"path": "simplicial_evidence.json",
                           "sha256": hashlib.sha256((directory / "simplicial_evidence.json").read_bytes()).hexdigest()}
        write_json(directory / "computed_result.json", {"input": data, "classification": classification,
                   "evidence": evidence_record, "run": dict(run, status="computed")})
        verification = verify_certificate(classification, evidence)
        run.update(status="complete", exitCode=0, elapsedSeconds=round(time.monotonic() - start, 6),
                   completedUTC=datetime.now(timezone.utc).isoformat())
        write_json(directory / "result.json", {"schema": "u1-translation-4p1-complete-v1", "input": data,
                   "classification": classification, "certificateVerification": verification,
                   "physicalComparison": {"status": "independent_target_not_loaded_by_solver",
                                          "universalPhysicalSpectrumCertified": False},
                   "uniformResponse": uniform_response(classification["freeRank"]),
                   "evidence": evidence_record, "run": run})
    except Exception as error:
        run.update(status="failed", exitCode=1, elapsedSeconds=round(time.monotonic() - start, 6),
                   exception=type(error).__name__, error=str(error))
        write_json(directory / "run.json", run)
        raise
    write_json(directory / "run.json", run)
    return run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--rank", action="append", type=int, choices=(1, 2, 3, 4))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    ranks = args.rank or [1, 2, 3, 4]
    if len(set(ranks)) != len(ranks):
        parser.error("Each translation rank may be selected only once")
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = manifest()
    write_json(output / "source.json", source)
    selected = [input_record(rank)["id"] for rank in ranks]
    write_json(output / "selection.json", selected)
    campaign = {"status": "running", "selectedCases": selected, "sourceSHA256": source["sha256"],
                "startedUTC": datetime.now(timezone.utc).isoformat()}
    write_json(output / "campaign.json", campaign)
    summary = []
    for rank in ranks:
        if manifest() != source:
            raise RuntimeError("Source changed during the campaign; evidence remains unaccepted")
        run = run_case(rank, output, source)
        summary.append(run)
        write_json(output / "summary.json", summary)
        print(run["id"], run["status"], run["elapsedSeconds"], flush=True)
    if manifest() != source:
        raise RuntimeError("Source changed during the campaign; evidence remains unaccepted")
    campaign.update(status="complete", completedUTC=datetime.now(timezone.utc).isoformat(),
                    caseCount=len(summary), runs=summary)
    write_json(output / "campaign.json", campaign)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
