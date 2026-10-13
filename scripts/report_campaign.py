#!/usr/bin/env python3
"""Collect immutable campaign evidence and compare independent literature data."""
from collections import Counter
from pathlib import Path
import argparse
import hashlib
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
    results, comparisons, failures, provenance = [], [], [], []
    for root in args.runs:
        selection = json.loads((root / "selection.json").read_text())
        source = json.loads((root / "source.json").read_text())
        encoded = json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(encoded).hexdigest() != source["sha256"]:
            raise ValueError("Corrupted source manifest: " + str(root))
        provenance.append({"runDirectory": str(root), "selection": selection, "source": source})
        for case in selection:
            path = root / case / "run.json"
            if not path.exists():
                failures.append({"id": case, "status": "not_started", "runDirectory": str(root)})
                continue
            metadata = json.loads(path.read_text())
            if metadata["status"] != "complete":
                failures.append(metadata)
                continue
            row = json.loads(path.with_name("result.json").read_text())
            input_hash = hashlib.sha256(path.with_name("input.json").read_bytes()).hexdigest()
            if input_hash != metadata["inputSHA256"] or source["sha256"] != metadata["sourceSHA256"]:
                raise ValueError("Result provenance does not match immutable inputs: " + str(path))
            if row["input"] != json.loads(path.with_name("input.json").read_text()):
                raise ValueError("Result contains a different symmetry input: " + str(path))
            results.append(row)
            comparisons.append(compare(row))
    counts = Counter(check["status"] for row in comparisons for check in row["checks"])
    for name, data in (("results", results), ("comparisons", comparisons),
                       ("failures", failures), ("comparison_counts", dict(counts)),
                       ("run_provenance", provenance)):
        (args.output / (name + ".json")).write_text(json.dumps(data, indent=2) + "\n")
    lines = ["# Insulator campaign evidence", "",
             "All groups below were computed from symmetry inputs and exact cochains.",
             "Published tables are read only by the separate comparison step.", "",
             "| Case | Computed group | Compared subgroup | Comparison |",
             "| --- | --- | --- | --- |"]
    for row, comparison in zip(results, comparisons):
        status = "; ".join(check.get("quantity", "scope") + ": " + check["status"]
                           for check in comparison["checks"])
        classification = row["classification"]
        subgroup = classification.get("relativeUniformIQH0")
        compared = ("n0=0: " + group_text(subgroup)) if subgroup else "same computed sector"
        lines.append("| " + row["input"]["id"] + " | " + group_text(classification)
                     + " | " + compared + " | " + status + " |")
    lines.extend(["", "Completed cases: " + str(len(results)) + ". Failed/incomplete cases: "
                  + str(len(failures)) + ".", "",
                  "A scope mismatch is not a numerical agreement or disagreement. The supplied",
                  "formulas cover the CI-generated, charge and group-cohomological phase sector;",
                  "they do not add an independent neutral E8 sector. Uniform IQH results are",
                  "compared using their explicitly computed n0=0 subgroup where available.", ""])
    (args.output / "README.md").write_text("\n".join(lines))
    benchmark_files = [ROOT / "benchmarks/compare.py"] + sorted((ROOT / "benchmarks").glob("*.json"))
    (args.output / "benchmark_provenance.json").write_text(json.dumps(
        {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
         for p in benchmark_files}, indent=2) + "\n")
    print(json.dumps({"complete": len(results), "failed": len(failures), "comparisons": dict(counts)}))


if __name__ == "__main__":
    main()
