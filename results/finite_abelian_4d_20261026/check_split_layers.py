#!/usr/bin/env python3
"""Check proved split layer rules against archived independent results."""
import json
from math import comb, prod
from pathlib import Path
try:
    from .split_layers import invariant_factors, split_layers
except ImportError:
    from split_layers import invariant_factors, split_layers

LAYER_MAP = {
    "pip": "pip",
    "majorana": "majorana",
    "complex_fermion": "complex_fermion",
    "bosonic": "bosonic",
}


def check_archived(evidence_path):
    evidence = json.loads(Path(evidence_path).read_text())
    results = []
    for row in evidence["selected_backgrounds"]:
        if any(row["power_bits"]):
            continue
        predicted = split_layers(row["orders"])
        archived = {
            name: invariant_factors(row["final_layers"][old_name])
            for name, old_name in LAYER_MAP.items()
        }
        results.append({
            "background_id": row["background_id"],
            "orders": row["orders"],
            "predicted": predicted,
            "archived": archived,
            "match": predicted == archived,
            "result_sha256": row["sha256"],
        })
    return results


def check_elementary():
    for rank in range(11):
        result = split_layers([2]*rank)
        expected_rank = 3*comb(rank, 3) + 3*comb(rank, 4) + comb(rank, 5)
        assert result == {"pip": [], "majorana": [], "complex_fermion": [],
                          "bosonic": [2]*expected_rank}


def main(evidence_path=None):
    here = Path(__file__).resolve().parent
    if evidence_path is None:
        evidence_path = here / "data" / "archived_51.json"
    results = check_archived(evidence_path)
    check_elementary()
    report = {
        "proof": "proofs/SPLIT_DECORATION_LAYERS.md",
        "archived_cases": len(results),
        "all_archived_match": all(row["match"] for row in results),
        "archived_layer_checks": results,
        "elementary_formula_checks": "ranks 0 through 10",
    }
    print(json.dumps({
        "archived_cases": len(results),
        "all_archived_match": report["all_archived_match"],
        "mismatches": [row for row in results if not row["match"]],
    }, indent=2))
    assert report["all_archived_match"], "Archived layer mismatch"
    return report


if __name__ == "__main__":
    import sys
    report = main(sys.argv[1] if len(sys.argv) > 1 else None)
    Path(__file__).with_name("SPLIT_LAYER_CHECKS.json").write_text(
        json.dumps(report, indent=2) + "\n")
