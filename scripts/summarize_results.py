#!/usr/bin/env python3
"""Render saved campaign reports as concise Markdown and CSV comparison tables."""
from collections import Counter
from fractions import Fraction
from math import gcd
from pathlib import Path
import argparse
import csv
import json

ROOT = Path(__file__).resolve().parents[1]
SPINS = ("spinless", "spin_half")
FAMILIES = ("point2", "wallpaper", "point3")


def group_text(record):
    if not isinstance(record, dict) or not all(k in record for k in ("torsion", "freeRank")):
        return "not computed"
    factors = ["Z"] * record["freeRank"] + [f"Z{n}" for n in record["torsion"] if n > 1]
    counts = Counter(factors)
    return " x ".join(f"{factor}^{count}" if count > 1 else factor
                      for factor, count in counts.items()) or "0"


def uniform_multiplicity(classification):
    """Read the actual uniform lift, never infer it from an abstract free rank."""
    if classification.get("uniformIQHIncluded") is not True:
        return "not computed"
    lifts = [w["sheetMultiplicity"] for w in classification.get("witnesses", [])
             if w.get("kind") == "uniform-IQH-lift" and "sheetMultiplicity" in w]
    values = []
    for value in lifts:
        rational = Fraction(str(value))
        if rational.denominator != 1:
            raise ValueError("Nonintegral uniform-IQH multiplicity")
        values.append(abs(rational.numerator))
    if values:
        step = 0
        for value in values:
            step = gcd(step, value)
        return str(step)
    if classification.get("finalSheetFreeRank") == 0 and classification.get("sheetOrders") == []:
        return "0 (forbidden)"
    return "witness unavailable"


def read_json(path, default):
    return json.loads(path.read_text()) if path.exists() else default


def read_reports(directories):
    cases = {}
    for directory in directories:
        results_path = directory / "results.json"
        results = json.loads(results_path.read_text())
        if not isinstance(results, list):
            raise ValueError(f"Expected a result list: {results_path}")
        comparisons = {row["id"]: row for row in read_json(directory / "comparisons.json", [])}
        failures = {row["id"]: row for row in read_json(directory / "failures.json", [])}
        completed = {row["input"]["id"]: row for row in results}
        if len(completed) != len(results):
            raise ValueError(f"Duplicate result IDs in {directory}")
        selected = set(completed) | set(failures)
        for run in read_json(directory / "run_provenance.json", []):
            selected.update(run.get("selection", []))
        for case_id in sorted(selected):
            if case_id in cases:
                raise ValueError(f"Duplicate case across reports: {case_id}; select one authoritative report")
            result = completed.get(case_id)
            if result:
                metadata = result["input"]
                status = result.get("run", {}).get("status", "status unavailable")
                classification = result.get("classification", {})
            else:
                # Geometry labels are not classification results. Missing
                # computations stay explicit even when the catalog knows names.
                metadata = read_json(ROOT / "insulator_catalog/generated" / (case_id + ".json"), {})
                status = failures.get(case_id, {}).get("status", "no result record")
                classification = {}
            family = metadata.get("family", case_id.split("_")[0])
            if family not in FAMILIES:
                raise ValueError(f"Unknown family for {case_id}")
            spin = metadata.get("spin", "spin_half" if case_id.endswith("spin_half") else "spinless")
            cases[case_id] = {"id": case_id, "metadata": metadata, "family": family,
                              "spin": spin, "status": status, "classification": classification,
                              "comparison": comparisons.get(case_id), "report": str(directory)}
    return cases


def comparison_text(comparison, family):
    if comparison is None:
        return "comparison unavailable", "not supplied"
    checks = comparison.get("checks", [])
    labels = {"stacking": "stacking", "finalChargeOrders": "charge", "finalPhaseOrders": "phase",
              "free_charge_embedding": "filling", "stacking_vs_rotation_band_reduction": "rotation control",
              "stacking_mod_named_neutral_E8": "named-E8 quotient"}
    statuses = {"published_source_discrepancy": "printed discrepancy",
                "requires_source_coordinate_map": "normalization unmapped",
                "requires_generator_witness": "witness unavailable",
                "scope_mismatch": "scope differs", "not_computed": "not computed",
                "requires_sector_map": "sector map needed"}
    selected = checks
    if family == "point3":
        projected = [c for c in checks if c.get("quantity") == "stacking_mod_named_neutral_E8"]
        if projected:
            selected = projected
    descriptions = [labels.get(c.get("quantity"), "scope") + ": " +
                    statuses.get(c.get("status"), c.get("status", "status unavailable")) for c in selected]
    matched_layers = {c.get("quantity") for c in selected if c.get("status") == "match"}
    if family == "wallpaper" and {"finalChargeOrders", "finalPhaseOrders", "stacking"} <= matched_layers:
        descriptions = ["charge/phase/stacking: match"] + [text for text in descriptions
                         if not text.startswith(("charge:", "phase:", "stacking:"))]
    reference = next((c["published"] for c in selected if "published" in c), None)
    return "; ".join(descriptions) or "comparison unavailable", group_text(reference) if reference else "not supplied"


def rows_from_cases(cases):
    grouped = {}
    for case in cases.values():
        metadata = case["metadata"]
        index = metadata.get("index", int(case["id"].split("_")[1]))
        key = case["family"], index
        row = grouped.setdefault(key, {"family": case["family"], "index": index,
                                        "name": metadata.get("name", case["id"]),
                                        "hermann_mauguin": metadata.get("hermann_mauguin", "")})
        spin = case["spin"]
        if spin not in SPINS or spin + "_status" in row:
            raise ValueError(f"Duplicate or unsupported spin in {case['id']}")
        classification = case["classification"]
        compared = classification
        if case["family"] in ("point2", "wallpaper"):
            if classification.get("uniformIQHIncluded") is True:
                compared = classification.get("relativeUniformIQH0", {})
            elif classification.get("uniformIQHIncluded") is not False:
                compared = {}
        status, reference = comparison_text(case["comparison"], case["family"])
        row.update({spin + "_status": case["status"], spin + "_group": group_text(compared),
                    spin + "_full_uniform_IQH_group": group_text(classification)
                    if case["family"] != "point3" and classification.get("uniformIQHIncluded") is True else "not computed",
                    spin + "_uniform_IQH_multiplicity": uniform_multiplicity(classification)
                    if case["family"] != "point3" else "not applicable",
                    spin + "_reference_group": reference, spin + "_comparison": status,
                    spin + "_report": case["report"]})
    rows = [row for _, row in sorted(grouped.items(), key=lambda item: (FAMILIES.index(item[0][0]), item[0][1]))]
    for row in rows:
        for spin in SPINS:
            if spin + "_status" not in row:
                row.update({spin + "_status": "not in supplied reports", spin + "_group": "not computed",
                            spin + "_full_uniform_IQH_group": "not computed",
                            spin + "_uniform_IQH_multiplicity": "not computed",
                            spin + "_reference_group": "not supplied", spin + "_comparison": "comparison unavailable",
                            spin + "_report": ""})
    return rows


def markdown(rows, directories):
    lines = ["# Insulator calculation summary", "",
             "Only saved results and saved comparison statuses are displayed. Spin labels are physical crystalline conventions.",
             "Two-dimensional groups are the computed n0=0 subgroup. IQH multiplicity m means the full calculation permits n0 in mZ; 0 means forbidden. The full groups are retained in the CSV.",
             "Three-dimensional groups cover the CI, charge and group-cohomological phase sector. Where available, the displayed reference is the quotient by the source's named neutral E8 root; this is an abstract comparison, not an implemented E8 cochain map.", ""]
    titles = {"point2": "2+1D point groups", "wallpaper": "2+1D wallpaper groups", "point3": "3+1D point groups"}
    for family in FAMILIES:
        subset = [r for r in rows if r["family"] == family]
        if not subset:
            continue
        lines += ["## " + titles[family], ""]
        if family == "point3":
            columns = ["Group", "Spinless", "Spin-half", "Reference, spinless / spin-half", "Comparison, spinless / spin-half"]
        else:
            columns = ["Group", "Spinless, n0=0", "Spin-half, n0=0", "IQH m, spinless / spin-half", "Comparison, spinless / spin-half"]
        lines += ["| " + " | ".join(columns) + " |", "| " + " | ".join(["---"] * len(columns)) + " |"]
        for row in subset:
            groups = [row[s + "_group"] if row[s + "_status"] == "complete" else
                      row[s + "_group"] + " (" + row[s + "_status"] + ")" for s in SPINS]
            extra = " / ".join(row[s + ("_reference_group" if family == "point3" else "_uniform_IQH_multiplicity")] for s in SPINS)
            spin_comparisons = [row[s + "_comparison"] for s in SPINS]
            comparison = ("both: " + spin_comparisons[0]) if len(set(spin_comparisons)) == 1 else " / ".join(spin_comparisons)
            cells = [row["name"], *groups, extra, comparison]
            lines.append("| " + " | ".join(str(c).replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
        lines.append("")
    lines += ["A printed discrepancy remains a discrepancy even when the independent rotation control matches. That control concerns the interacting reduction of band-generated phases and does not prove absence of interaction-only roots.",
              "Filling normalization remains unmapped until the source's decoration coordinates are matched to primitive-cell charge. Missing results and missing comparisons are never converted into agreement.", "",
              "Source reports: " + ", ".join("`" + str(p) + "`" for p in directories) + ".", ""]
    return "\n".join(lines)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("reports", nargs="+", type=Path)
    parser.add_argument("--output", required=True, type=Path, help="Directory for summary.md and summary.csv")
    args = parser.parse_args()
    rows = rows_from_cases(read_reports(args.reports))
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "summary.md").write_text(markdown(rows, args.reports))
    fields = ["family", "index", "name", "hermann_mauguin"] + [spin + "_" + field for spin in SPINS
              for field in ("status", "group", "full_uniform_IQH_group", "uniform_IQH_multiplicity", "reference_group", "comparison", "report")]
    with (args.output / "summary.csv").open("w", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)
    print(json.dumps({"groups": len(rows), "markdown": str(args.output / "summary.md"),
                      "csv": str(args.output / "summary.csv")}))


if __name__ == "__main__":
    main()
