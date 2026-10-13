#!/usr/bin/env python3
"""Collect immutable campaign evidence and compare independent literature data."""
from collections import Counter
from pathlib import Path
import argparse
import json
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmarks.compare import compare


def group_text(row):
    factors = ["Z"] * row["freeRank"] + ["Z" + str(x) for x in row["torsion"]]
    return " x ".join(factors) or "0"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("runs", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=False)
    results, comparisons, failures = [], [], []
    for root in args.runs:
        for path in sorted(root.glob("*/run.json")):
            metadata = json.loads(path.read_text())
            if metadata["status"] != "complete":
                failures.append(metadata)
                continue
            row = json.loads(path.with_name("result.json").read_text())
            results.append(row)
            comparisons.append(compare(row))
    counts = Counter(check["status"] for row in comparisons for check in row["checks"])
    for name, data in (("results", results), ("comparisons", comparisons),
                       ("failures", failures), ("comparison_counts", dict(counts))):
        (args.output / (name + ".json")).write_text(json.dumps(data, indent=2) + "\n")
    lines = ["# Insulator campaign evidence", "",
             "All groups below were computed from symmetry inputs and exact cochains.",
             "Published tables are read only by the separate comparison step.", "",
             "| Case | Computed group | Comparison |", "| --- | --- | --- |"]
    for row, comparison in zip(results, comparisons):
        status = "; ".join(check.get("quantity", "scope") + ": " + check["status"]
                           for check in comparison["checks"])
        lines.append("| " + row["input"]["id"] + " | " + group_text(row["classification"])
                     + " | " + status + " |")
    lines.extend(["", "Completed cases: " + str(len(results)) + ". Failed/incomplete cases: "
                  + str(len(failures)) + ".", "",
                  "A scope mismatch is not a numerical agreement or disagreement. The supplied",
                  "formulas cover the CI-generated, charge and group-cohomological phase sector;",
                  "they do not add an independent neutral E8 sector.", ""])
    (args.output / "README.md").write_text("\n".join(lines))
    print(json.dumps({"complete": len(results), "failed": len(failures), "comparisons": dict(counts)}))


if __name__ == "__main__":
    main()
