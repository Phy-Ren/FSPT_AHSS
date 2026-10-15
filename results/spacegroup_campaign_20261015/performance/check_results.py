#!/usr/bin/env python3
"""Compare complete SG19 calculations without relaxing any nonzero cochain data."""
from __future__ import annotations
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
TIMING_FIELDS = {"resolutionBuildTimings", "formulaWorkerCalls", "pairedGeometryReuse", "formulaCacheStats"}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def compare(candidate_path, reference_path):
    candidate = json.loads(candidate_path.read_text())
    reference = json.loads(reference_path.read_text())
    assert candidate["input"] == reference["input"], "Symmetry inputs differ"
    assert candidate["run"]["status"] == "complete" and candidate["run"]["exitCode"] == 0
    a, b = reference["classification"], candidate["classification"]
    checked, normalizations = [], []
    for key, value in a.items():
        if key in TIMING_FIELDS:
            continue
        if key == "gaugeReductionWitnesses":
            assert len(value) == len(b[key]), "Gauge witness count changed"
            for i, (old, new) in enumerate(zip(value, b[key])):
                assert old.keys() == new.keys(), "Gauge witness fields changed"
                for sub, data in old.items():
                    if sub == "nativeSheetParameter" and not any(data) and not any(new[sub]):
                        if data != new[sub]:
                            normalizations.append({"witness": i, "field": sub, "before": data, "after": new[sub]})
                        continue
                    assert data == new[sub], (key, i, sub)
        else:
            assert value == b[key], key
        checked.append(key)
    assert b["nativeChainIdentitiesVerified"] is True
    assert (b["torsion"], b["freeRank"]) == ([], 1)
    assert b["spaceGroupFilling"]["fillingStep"] == 4
    assert b["spaceGroupFilling"]["allPresentationRelationsHaveZeroFilling"] is True
    old_time, new_time = reference["run"]["elapsedSeconds"], candidate["run"]["elapsedSeconds"]
    return {"id": candidate["input"]["id"], "status": "exact_match",
            "candidateSHA256": digest(candidate_path), "referenceSHA256": digest(reference_path),
            "candidateSourceSHA256": candidate["run"]["sourceSHA256"],
            "referenceSourceSHA256": reference["run"]["sourceSHA256"],
            "exactMatchingFields": checked, "literalZeroGaugeNormalizations": normalizations,
            "referenceElapsedSeconds": old_time, "candidateElapsedSeconds": new_time,
            "sameHost": reference["run"]["host"] == candidate["run"]["host"],
            "observedCaseTimeRatio": round(old_time / new_time, 4) if reference["run"]["host"] == candidate["run"]["host"] else None,
            "candidatePairedSpins": candidate["run"].get("pairedSpins", False),
            "candidateBatchElapsedSeconds": candidate["run"].get("batchElapsedSeconds"),
            "candidateHost": candidate["run"]["host"], "referenceHost": reference["run"]["host"],
            "workerCalls": b["formulaWorkerCalls"], "cacheStats": b.get("formulaCacheStats"),
            "primitiveFilling": 4}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--campaign", type=Path, default=ROOT / "cluster_c")
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    rows = []
    for spin in ("spin_half", "spinless"):
        name = f"spacegroup_019_{spin}"
        rows.append(compare(args.campaign / name / "result.json", ROOT / "reference_a" / name / "result.json"))
    result = {"status": "both_exact_matches", "rows": rows,
              "normalization": "Only omitted versus explicit all-zero sheet-gauge parameters are identified. All final charge/phase vectors and every nonzero parameter agree exactly.",
              "timingLimit": "Ratios are reported only when hosts match. The first paired case interval includes shared startup, while the second benefits from context reuse. Complete batch timing additionally includes worker shutdown and process exit. Background load differs from reference A; these are observed campaign timings, not an isolated microbenchmark."}
    encoded = json.dumps(result, indent=2, sort_keys=True) + "\n"
    if args.output:
        args.output.write_text(encoded)
    print(encoded)


if __name__ == "__main__":
    main()
