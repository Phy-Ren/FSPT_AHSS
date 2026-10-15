#!/usr/bin/env python3
"""Render newly computed cases with dimension, spin, and response scopes separate.

References are version-pinned independent fixtures from the foundation audit.
The classifier never reads this report or its literature inputs.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import csv
from fractions import Fraction
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT))
from build_foundation_tables import group_text, signature
from summarize_results import uniform_multiplicity
from insulator.e8_pointgroup import presentation_invariants

BASE = ROOT / "results/foundation_review_20261014"
SPINS = {"spinless": "Spinless", "spin_half": "Spin-1/2"}


def read(path):
    return json.loads(path.read_text())


def write(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def collect(roots):
    records, provenance = {}, []
    for root in roots:
        selection, source = read(root / "selection.json"), read(root / "source.json")
        encoded = json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(encoded).hexdigest() != source["sha256"]:
            raise ValueError(f"Invalid source manifest: {root}")
        for case in selection:
            run = read(root / case / "run.json")
            result_path = root / case / "result.json"
            result = read(result_path)
            if run["status"] != "complete" or result["run"] != run:
                raise ValueError(f"Incomplete or inconsistent run: {root / case}")
            if run["sourceSHA256"] != source["sha256"] or digest(root / case / "input.json") != run["inputSHA256"]:
                raise ValueError(f"Provenance mismatch: {root / case}")
            if result["input"] != read(root / case / "input.json"):
                raise ValueError(f"Input mismatch: {root / case}")
            if result["input"]["id"] != case or run["id"] != case:
                raise ValueError(f"Case ID mismatch: {root / case}")
            key = (case, run["uniformIQHRequested"])
            if key in records:
                raise ValueError(f"Duplicate case and response sector: {key}")
            records[key] = result
        provenance.append({"directory": str(root), "selection": selection, "source": source,
                           "resultHashes": {case: digest(root / case / "result.json") for case in selection}})
    return records, provenance


def cell(group, actual=None, **metadata):
    value = signature(group)
    status = "not_compared" if actual is None else ("match" if value == signature(actual) else "mismatch")
    return {"availability": "available", "group": value, "comparison_status": status, **metadata}


def refresh(old, actual):
    result = deepcopy(old)
    if "group" in result and result.get("comparison_status") != "not_compared":
        result["comparison_status"] = "match" if signature(result["group"]) == signature(actual) else "mismatch"
    return result


def show(value):
    if value["availability"] != "available":
        return {"not_applicable": "N/A", "unverified": "UNVERIFIED", "not_computed": "NOT COMPUTED"}[value["availability"]]
    if "group" not in value:
        return value.get("text", "")
    marker = {"match": "**✓** ", "mismatch": "**×** "}.get(value["comparison_status"], "")
    return marker + group_text(value["group"]) + (" †" if value.get("proof_audit") else "")


def render(path, table):
    keys = [column["key"] for column in table["columns"]]
    table["comparison_counts"] = {
        key: dict(Counter(row["cells"][key]["comparison_status"] for row in table["rows"])) for key in keys
    }
    table["availability_counts"] = {
        key: dict(Counter(row["cells"][key]["availability"] for row in table["rows"])) for key in keys
    }
    write(path.with_suffix(".json"), table)
    header = ["Group (HM)"] + [column["label"] for column in table["columns"]]
    body = [[f'{row["name"]} ({row["hermann_mauguin"]})'] + [show(row["cells"][key]) for key in keys]
            for row in table["rows"]]
    with path.with_suffix(".csv").open("w", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows([[value.replace("**", "") for value in row] for row in body])
    lines = ["# " + table["title"], "", table["scope"], "",
             "**✓** match; **×** mismatch; UNVERIFIED is not a match. These markers compare final group types; a complete physical generator map remains separate.", "",
             "| " + " | ".join(header) + " |", "| " + " | ".join(["---"] * len(header)) + " |"]
    lines += ["| " + " | ".join(row) + " |" for row in body]
    audit_paths = {c["proof_audit"]["path"] for row in table["rows"]
                   for c in row["cells"].values() if c.get("proof_audit")}
    if audit_paths:
        links = ", ".join(f"[grading audit]({os.path.relpath(ROOT / p, path.parent)})" for p in sorted(audit_paths))
        lines += ["", "† Published Debray D2/D6 spin-half values are retained as printed. The " + links +
                  " identifies a conflict in the supporting KU count; the source cell is not silently corrected.", ""]
    else:
        lines += [""]
    for key, source in table["sources"].items():
        authors = source.get("authors", source.get("author", ""))
        if isinstance(authors, list):
            authors = ", ".join(authors)
        lines += [f'- [{key}: {authors}, {source.get("version", source.get("year", ""))}]({source["url"]}). '
                  + source.get("method", "") + ". " + source.get("location", "")]
    path.with_suffix(".md").write_text("\n".join(lines) + "\n")


def full_references():
    arxiv = read(ROOT / "benchmarks/point3_full_2204.13558.json")
    journal = read(ROOT / "benchmarks/point3_full_journal_2025.json")
    debray = read(ROOT / "benchmarks/debray_class_a_2102.02941v3.json")
    mirror = read(ROOT / "benchmarks/mirror_interacting_2105.02682.json")
    def plain(row):
        return row["name_as_printed"].split("=")[0].translate(str.maketrans("", "", "$_{}"))
    return ({(plain(r), r["physical_spin"]): r for r in arxiv["rows"]},
            {r["id"]: r for r in journal["rows"]},
            {r["id"]: r for r in debray["rows"]}, {r["id"]: r for r in mirror["rows"]})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ci-root", type=Path, action="append", required=True)
    parser.add_argument("--e8-root", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    records, provenance = collect(args.ci_root)
    e8 = {}
    extension_provenance = []
    for root in args.e8_root:
        extension_source = read(root / "source.json")
        encoded = json.dumps(extension_source["files"], sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(encoded).hexdigest() != extension_source["sha256"]:
            raise ValueError(f"Invalid extension manifest: {root}")
        for case in read(root / "selection.json"):
            path = root / case / "result.json"
            result = read(path)
            if result["input"]["id"] != case or case in e8 or (case, False) not in records:
                raise ValueError(f"Duplicate E8 result or missing CI parent: {case}")
            if result["input"] != records[(case, False)]["input"] or result["run"]["status"] != "complete":
                raise ValueError(f"Incompatible E8 result: {case}")
            if result["classification"].get("neutralE8Included") is not True:
                raise ValueError(f"Not an E8-inclusive calculation: {case}")
            parent_path = path.parent / "ci_result.json"
            if (read(parent_path) != records[(case, False)]
                    or digest(parent_path) != result["run"]["ciResultSHA256"]
                    or result["run"]["sourceSHA256"] != extension_source["sha256"]):
                raise ValueError(f"E8 extension used a different CI parent or source: {case}")
            e8[case] = result
        extension_provenance.append({"directory": str(root), "source": extension_source,
             "resultHashes": {case: digest(root / case / "result.json") for case in read(root / "selection.json")}})
    args.output.mkdir(parents=True, exist_ok=False)
    write(args.output / "run_provenance.json", provenance)
    write(args.output / "extension_provenance.json", extension_provenance)
    write(args.output / "results.json", list(records.values()))
    write(args.output / "e8_results.json", list(e8.values()))
    computation_checks = []
    for (case, uniform), result in records.items():
        actual = result["classification"]
        independent = presentation_invariants(actual["presentation"], actual["presentationGeneratorCount"])
        if signature(independent) != signature(actual):
            raise ValueError(f"Independent Smith calculation disagrees: {case}, uniform={uniform}")
        check = {"id": case, "uniformIQH": uniform, "independentSmithCheck": True,
                 "nativeChainCertificatePresent": actual.get("nativeChainIdentitiesVerified") is True}
        filling = actual.get("wallpaperFilling")
        if filling:
            values = [Fraction(str(x)) for x in filling["generatorFillings"]]
            if len(values) != actual["presentationGeneratorCount"] or any(
                    sum(a * b for a, b in zip(row, values)) for row in actual["presentation"]):
                raise ValueError(f"A presentation relation changes physical filling: {case}")
            check.update(fillingRelationsChecked=True, primitiveCellFillingStep=filling["fillingStep"])
        if uniform and (case, False) in records:
            relative = actual["relativeUniformIQH0"]
            standalone = records[(case, False)]["classification"]
            if signature(relative) != signature(standalone):
                raise ValueError(f"Independent n0=0 calculation disagrees with the all-n0 kernel: {case}")
            check.update(independentRelativeKernelGroupCheck=True,
                         relativeKernelPresentationIdentical=relative["presentation"] == standalone["presentation"])
        computation_checks.append(check)
    write(args.output / "computation_checks.json", computation_checks)
    previous3 = {r["input"]["id"]: r for r in read(ROOT / "results/three_dimensional_20261013/results.json")}
    tables, changes, consumed, reference_paths = [], [], set(), set()
    reference_paths.update(ROOT / "benchmarks" / name for name in (
        "point3_full_2204.13558.json", "point3_full_journal_2025.json",
        "debray_class_a_2102.02941v3.json", "mirror_interacting_2105.02682.json"))
    arxiv, journal, debray, mirror = full_references()
    for spin, label in SPINS.items():
        for dimension in (2, 3):
            for uniform in ((False, True) if dimension == 2 else (False,)):
                for family in (("point2", "wallpaper") if dimension == 2 else ("point3",)):
                    stem = "wallpaper_groups" if family == "wallpaper" else "point_groups"
                    branch = Path(f"{dimension}p1d") / spin / ("e0_zero" if dimension == 2 else "without_e8")
                    if dimension == 2:
                        branch /= "n0_all" if uniform else "n0_zero"
                    template_path = BASE / branch / (stem + ".json")
                    template = read(template_path)
                    reference_paths.add(template_path)
                    selected = [r for r in template["rows"] if (r["id"], uniform) in records]
                    if not selected:
                        continue
                    table = deepcopy(template)
                    table["title"] += " — fresh four-data campaign"
                    table["scope"] = table["scope"].replace("E8-inclusive comparison is deferred.", "The separately computed E8-inclusive model has its own table.")
                    model_key = "model_stacking" if dimension == 2 and not uniform else "model"
                    table["columns"].insert(1, {"key": "previous", "label": "Previous result"})
                    if dimension == 3:
                        order = ["model", "previous", "scope", "Debray_retained", "NMLW_retained", "R3_arxiv", "R3_journal"]
                        table["columns"].sort(key=lambda column: order.index(column["key"]))
                    elif family == "point2":
                        # Keep the independent bordism source ahead of the two
                        # versions of the real-space table, without changing a value.
                        columns = table["columns"]
                        first_reference = next(i for i, c in enumerate(columns) if c["key"].startswith("R2_"))
                        bordism = [c for c in columns if c["key"].startswith("Debray_")]
                        table["columns"] = [c for c in columns if c not in bordism]
                        table["columns"][first_reference:first_reference] = bordism
                    table["rows"] = []
                    if dimension == 3:
                        table.update(e0_scope="not_applicable_in_3d", e8_scope="excluded")
                    for prior in selected:
                        case = prior["id"]
                        result = records[(case, uniform)]
                        data = result["input"]
                        if (data["dimension"], data["family"], data["spin"], data["name"]) != (
                                dimension, family, spin, prior["name"]):
                            raise ValueError(f"Case metadata disagrees with its comparison template: {case}")
                        consumed.add((case, uniform))
                        actual = result["classification"]
                        row = deepcopy(prior)
                        if dimension == 3:
                            row.update(e0_scope="not_applicable_in_3d", e8_scope="excluded")
                        row["cells"] = {key: refresh(value, actual) for key, value in prior["cells"].items()}
                        old_group = prior["cells"][model_key]["group"]
                        row["cells"][model_key] = cell(actual)
                        row["cells"]["previous"] = cell(old_group, actual)
                        for layer in ("charge", "phase"):
                            key = "model_" + layer
                            if key in row["cells"]:
                                title = layer.title()
                                layer_group = {"torsion": actual["final" + title + "Orders"],
                                               "freeRank": actual["final" + title + "FreeRank"]}
                                row["cells"][key] = cell(layer_group)
                                row["cells"]["L2_" + layer] = refresh(prior["cells"]["L2_" + layer], layer_group)
                        if "n0_image" in row["cells"]:
                            step = uniform_multiplicity(actual)
                            row["cells"]["n0_image"]["text"] = ("Z" if step == "1" else
                                ("0" if step == "0 (forbidden)" else step + "Z" if step.isdigit() else step))
                        same = signature(old_group) == signature(actual)
                        changes.append({"id": case, "uniformIQH": uniform, "sameGroup": same,
                                        "old": signature(old_group), "new": signature(actual),
                                        "identicalClassification": actual == previous3[case]["classification"] if dimension == 3 else None})
                        table["rows"].append(row)
                    render(args.output / branch / stem, table)
                    tables.append(str(branch / (stem + ".md")))
                    if dimension != 3 or not any(r["id"] in e8 for r in selected):
                        continue
                    extended = {**deepcopy(table), "title": f"3+1D {label} point groups: E8-inclusive selected model",
                        "scope": "The neutral H1(G,Z_s) presentation is computed independently from each group and joined to the fresh CI presentation using the specified 3+1D section. This computes the selected four-data model. Identification of its CI kernel with the complete physical theory remains conditional. Reference columns give the full interacting groups, including E8; no factors are deleted to improve agreement.",
                        "e0_scope": "not_applicable_in_3d", "e8_scope": "included", "rows": [],
                        "columns": [{"key": k, "label": v} for k, v in [
                            ("model", "Computed with E8"), ("neutral", "Computed E8 H1"),
                            ("Debray", "Debray 2026v3 (bordism)"), ("NMLW", "Ning–Mao–Li–Wang 2021"),
                            ("R3_arxiv", "Zhang–Ning–Qi–Gu 2024v2"), ("R3_journal", "Zhang–Ning–Qi–Gu 2025")]]}
                    for prior in selected:
                        case = prior["id"]
                        if case not in e8:
                            raise ValueError(f"Incomplete E8 coverage for {case}")
                        result = e8[case]
                        actual = result["classification"]
                        row = {k: deepcopy(v) for k, v in prior.items() if k != "cells"}
                        row.update(e0_scope="not_applicable_in_3d", e8_scope="included")
                        name = "S6" if row["name"] == "C3i" else row["name"]
                        values = {"model": cell(actual),
                                  "neutral": cell(actual["e8H1"]),
                                  "R3_arxiv": cell(arxiv[name, spin]["stacking_orders"], actual, source="R3_arxiv"),
                                  "R3_journal": cell(journal[case]["stacking_orders"], actual, source="R3_journal")}
                        for key, fixture in (("Debray", debray), ("NMLW", mirror)):
                            values[key] = cell(fixture[case]["fullPhysical"], actual, source=key,
                                               source_location=fixture[case]["source_location"]) if case in fixture else {
                                "availability": "not_applicable" if key == "NMLW" else "unverified", "comparison_status": "not_compared",
                                "reason": "No version-pinned full-group fixture extracted for this case."}
                        audit = prior["cells"].get("Debray_retained", {}).get("proof_audit")
                        if audit:
                            values["Debray"]["proof_audit"] = audit
                        row["cells"] = values
                        extended["rows"].append(row)
                    destination = Path("3p1d") / spin / "with_e8" / stem
                    render(args.output / destination, extended)
                    tables.append(str(destination.with_suffix(".md")))
    if consumed != set(records):
        raise ValueError(f"Some input records were not rendered: {set(records) - consumed}")
    write(args.output / "old_new_comparison.json", changes)
    write(args.output / "reference_provenance.json", {
        str(path.relative_to(ROOT)): digest(path) for path in sorted(reference_paths)})
    write(args.output / "validation.json", {"completeCIRuns": len(records), "completeE8Extensions": len(e8),
          "unchangedGroups": sum(r["sameGroup"] for r in changes), "changedGroups": sum(not r["sameGroup"] for r in changes),
          "tables": tables, "sourceInputHashesVerified": True,
          "independentSmithChecks": len(computation_checks),
          "independentRelativeKernelChecks": sum(c.get("independentRelativeKernelGroupCheck", False) for c in computation_checks),
          "fillingRelationChecks": sum(c.get("fillingRelationsChecked", False) for c in computation_checks),
          "nativeChainCertificatesPresent": sum(c["nativeChainCertificatePresent"] for c in computation_checks)})
    # Each index selects the next scope; no combined spin/dimension result table.
    for directory in sorted({(args.output / t).parent for t in tables} | {args.output}, key=lambda p: -len(p.parts)):
        for parent in [directory, *directory.parents]:
            if parent != args.output and args.output not in parent.parents:
                break
            entries = sorted(p for p in parent.iterdir() if p.is_dir())
            direct = sorted(p for p in parent.glob("*.md") if p.name != "README.md")
            links = [f"- [{p.name}]({p.name}/README.md)" for p in entries] + [f"- [{p.stem}]({p.name})" for p in direct]
            (parent / "README.md").write_text("# Fresh four-data campaign\n\nSelect one dimension, spin convention, and response sector.\n\n" + "\n".join(links) + "\n")
    print(json.dumps(read(args.output / "validation.json"), indent=2))


if __name__ == "__main__":
    main()
