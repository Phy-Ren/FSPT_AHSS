#!/usr/bin/env python3
"""Render versioned, sector-specific reference tables without changing solver data.

Every row is one catalog group and one physical spin. Sources enter only after
the saved calculation is read. All main comparisons use interacting results;
the band-generated interacting reduction is a separate diagnostic artifact.
"""
from __future__ import annotations

import argparse
import collections
import csv
import hashlib
import json
from fractions import Fraction
from math import gcd
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SPINS = {"spinless": "Spinless", "spin_half": "Spin-half"}
ALIASES = {"Cs": "D1", "C2v": "D2", "C3v": "D3", "C4v": "D4", "C6v": "D6"}
WALL_ALIASES = {"pm": "p1m1", "pg": "p1g1", "cm": "c1m1", "pmm": "p2mm", "pmg": "p2mg",
                "pgg": "p2gg", "cmm": "c2mm", "p4m": "p4mm", "p4g": "p4gm", "p6m": "p6mm"}

SOURCES = {
    "R2_journal": {"authors": "Jian-Hao Zhang, Shuo Yang, Yang Qi, Zheng-Cheng Gu", "year": 2022,
        "title": "Real-space construction of crystalline topological superconductors and insulators in 2D interacting fermionic systems",
        "url": "https://doi.org/10.1103/PhysRevResearch.4.033081", "version": "Published 2022-07-29",
        "method": "Interacting real-space block states, bubbles and stacking", "location": "Table III p.4 (wallpaper); Supplement Table I p.2 (points)"},
    "R2_arxiv": {"authors": "Jian-Hao Zhang, Shuo Yang, Yang Qi, Zheng-Cheng Gu", "year": 2023,
        "title": "Real-space construction of crystalline topological superconductors and insulators in 2D interacting fermionic systems",
        "url": "https://arxiv.org/abs/2012.15657v2", "version": "arXiv v2, 2023-06-20",
        "method": "Interacting real-space block states, bubbles and stacking", "location": "Main Table III; Supplemental Table I"},
    "L2": {"authors": "Qing-Rui Wang, Yang Qi, Chen Fang, Meng Cheng, Zheng-Cheng Gu", "year": 2021,
        "title": "Exactly solvable lattice models for interacting electronic insulators in two dimensions",
        "url": "https://arxiv.org/abs/2112.15533v1", "version": "arXiv v1, 2021-12-31; journal PRB108,L121104 (2023), journal tables not separately verified",
        "method": "Interacting charge decoration, super-cocycle equations and commuting-projector construction",
        "location": "Supplement H, Tables II and III p.17; final charge and phase layers"},
    "MCB": {"authors": "Naren Manjunath, Vladimir Calvera, Maissam Barkeshli", "year": 2024,
        "title": "Characterization and classification of interacting (2+1)D topological crystalline insulators with orientation-preserving wallpaper groups",
        "url": "https://doi.org/10.1103/PhysRevB.109.035168", "version": "PRB109,035168 (2024); extraction pinned to arXiv2309.12389v1",
        "method": "Interacting invertible-phase response invariants", "location": "Table I and Sec.III; response-defined subgroups C=c-=0 or k1=0"},
    "R3_arxiv": {"authors": "Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi, Zheng-Cheng Gu", "year": 2024,
        "title": "Construction and classification of crystalline topological superconductor and insulators in three-dimensional interacting fermion systems",
        "url": "https://arxiv.org/abs/2204.13558v2", "version": "arXiv v2, 2024-06-18",
        "method": "Interacting real-space topological crystals, boundary gapping, bubble equivalence and stacking", "location": "Table II and named E8 root lists"},
    "R3_journal": {"authors": "Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi, Zheng-Cheng Gu", "year": 2025,
        "title": "Construction and Classification of Crystalline Topological Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems",
        "url": "https://doi.org/10.1103/PhysRevX.15.031029", "version": "Published 2025-07-28; supplement dated 2025-07-08",
        "method": "Interacting real-space topological crystals, boundary gapping, bubble equivalence and stacking", "location": "Table II p.031029-5 and independently reread named E8 root lists"},
    "B2_diagnostic": {"authors": "Shang Liu, Ashvin Vishwanath, Eslam Khalaf", "year": 2019,
        "title": "Shift Insulators: Rotation-Protected Two-Dimensional Topological Crystalline Insulators",
        "url": "https://doi.org/10.1103/PhysRevX.9.031003", "version": "Journal 2019; arXiv1809.01636v2",
        "method": "Interacting reduction of band-generated phases under adjoining; not a complete interacting classification",
        "location": "Table VI, class A, interacting right-hand result; published Sec.VI B pp.24-25"},
    "Debray": {"authors": "Arun Debray", "year": 2026, "title": "Version-pinned interacting phase-homology reference pending extraction",
        "url": "https://arxiv.org/abs/2102.02941v3", "version": "arXiv v3, 2026-02-03",
        "method": "Interacting phase homology / bordism", "location": "Pending verified fixture"},
}


def signature(group):
    if isinstance(group, dict):
        orders = list(group["torsion"]) + [0] * int(group["freeRank"])
    else:
        orders = [int(x) for x in group]
    if any(n < 0 for n in orders):
        raise ValueError("Negative cyclic order")
    powers = collections.defaultdict(list)
    for n in orders:
        if n <= 1:
            continue
        p = 2
        while p * p <= n:
            e = 0
            while n % p == 0:
                n //= p
                e += 1
            if e:
                powers[p].append(e)
            p += 1
        if n > 1:
            powers[n].append(1)
    width = max((len(v) for v in powers.values()), default=0)
    factors = [1] * width
    for p, exponents in powers.items():
        for i, exponent in enumerate([0] * (width - len(exponents)) + sorted(exponents)):
            factors[i] *= p ** exponent
    return {"torsion": factors, "freeRank": orders.count(0)}


def group_text(group):
    counts = collections.Counter((["Z"] * group["freeRank"]) + [f"Z{n}" for n in group["torsion"]])
    return " x ".join(f"{n}^{k}" if k > 1 else n for n, k in counts.items()) or "0"


def group_cell(group, *, actual=None, source=None, scope=None, location=None, limit=None):
    target = signature(group)
    return {"availability": "available", "group": target,
            "comparison_status": ("abstract_match" if signature(actual) == target else "abstract_difference") if actual is not None else "not_compared",
            "source": source, "scope": scope, "source_location": location, "comparison_limit": limit}


def missing(availability, reason):
    assert availability in ("not_applicable", "unverified", "not_computed")
    return {"availability": availability, "reason": reason, "comparison_status": "not_compared"}


def note(text, status="documented"):
    return {"availability": "available", "text": text, "comparison_status": status}


def show(cell, compact=False):
    labels = {"not_applicable": "N/A", "unverified": "UNVERIFIED", "not_computed": "NOT COMPUTED"}
    if cell["availability"] != "available":
        if compact:
            return cell.get("short_label", labels[cell["availability"]])
        return labels[cell["availability"]] + ": " + cell["reason"]
    if "group" in cell:
        value = group_text(cell["group"])
        suffix = {"abstract_match": " [abstract match]", "abstract_difference": " [DIFF]"}.get(cell["comparison_status"], "")
        if cell.get("proof_audit"):
            suffix += (" [printed; proof grading conflict](../../" + cell["proof_audit"]["path"] + ")") if compact else "; proof audit: " + cell["proof_audit"]["summary"]
        return value + suffix
    return cell["text"]


class Builder:
    def __init__(self, root: Path, out: Path, debray: Path | None, mirror: Path | None):
        self.root, self.out = root, out
        self.inputs = {}
        self.tables = {}
        self.runs2 = self.load("results/two_dimensional_20261013/results.json")
        self.runs3 = self.load("results/three_dimensional_20261013/results.json")
        self.point = self.load("benchmarks/point2_stacking_2012.15657.json")
        self.wall = self.load("benchmarks/wallpaper_stacking_2012.15657.json")
        self.layers = self.load("benchmarks/wallpaper_layers_2112.15533.json")
        self.mcb = self.load("results/calibration_20261014/wallpaper_2024_response_comparison.json")
        self.mcb_by_id = {r["id"]: r for r in self.mcb["rows"]}
        self.full3a = self.load("benchmarks/point3_full_2204.13558.json")
        self.full3j = self.load("benchmarks/point3_full_journal_2025.json")
        self.e8a = self.load("benchmarks/point3_named_e8_quotient_2204.13558.json")
        self.e8j = self.load("benchmarks/point3_named_e8_journal_2025.json")
        self.diagnostic = self.load("benchmarks/point2_rotation_reduction_1809.01636.json")
        self.load("benchmarks/point2_source_version_audit.json")
        self.load("docs/reference_ledger_20261014.md", json_data=False)
        self.debray = None
        if debray:
            self.debray = self.load(debray)
            SOURCES["Debray"].update(self.debray.get("source", {}))
            SOURCES["Debray"]["location"] = "Tables 1–6 and theorems specified separately in each row; extracted Class A phase groups"
            self.load("docs/foundations/debray_d2_grading_audit.md", json_data=False)
        self.debray_rows = {r["id"]: r for r in (self.debray or {}).get("rows", [])}
        self.mirror = self.load(mirror) if mirror else None
        self.mirror_rows = {r["id"]: r for r in (self.mirror or {}).get("rows", [])}
        if self.mirror:
            source = self.mirror["source"]
            SOURCES["NMLW"] = {**source, "authors": ", ".join(source["authors"]),
                "version": "arXiv2105.02682v1, 2021-05-06; PRB104,075111 (2021)",
                "location": "Table II; Sec.III.B.1 Eqs.19-20 pp.12-13; AppendixB.1 Eq.B4 p.31"}

    def load(self, name, json_data=True):
        path = Path(name)
        if not path.is_absolute():
            path = self.root / path
        data = path.read_bytes()
        self.inputs[str(path.relative_to(self.root)) if path.is_relative_to(self.root) else str(path)] = hashlib.sha256(data).hexdigest()
        return json.loads(data) if json_data else data.decode()

    def debray_cell(self, run, sector, actual=None):
        if run["input"]["family"] == "wallpaper":
            return missing("not_applicable", "point-group reference")
        record = self.debray_rows.get(run["input"]["id"])
        if record is None:
            return missing("unverified", "no verified source value extracted for this concrete group/spin")
        assert (record["name"], record["physical_spin"]) == (run["input"]["name"], run["input"]["spin"])
        key = {"relative_n0_e0_zero": "relativeN0E0Zero", "all_n0_e0_zero": "allN0WithE0Zero",
               "retained_model_quotient": "retainedComparison", "full_physical": "fullPhysical"}[sector]
        if record.get(key) is None:
            cell = missing("unverified", record.get("retainedComparisonScope", "matching source sector not extracted") + "; see full-E8 reference table")
            cell["short_label"] = "UNVERIFIED: not projected; see full-E8 table"
            return cell
        cell = group_cell(record[key], actual=actual, source="Debray", scope=sector,
                         location={"source_file": record["source_file"], "location": record["source_location"]},
                         limit=record.get("restriction_argument", record.get("retainedComparisonScope", "Reference only; no physical-to-model generator dictionary")))
        if record["family"] == "point3" and record["name"] in ("D2", "D6") and record["physical_spin"] == "spin_half":
            cell["proof_audit"] = {
                "path": "docs/foundations/debray_d2_grading_audit.md",
                "result_path": "results/foundation_review_20261014/diagnostics/debray_d2_ku_grading_audit.json",
                "summary": "Printed Z2^3 is preserved. Our source-internal audit finds two, not three, degree-four monomials in the cited graded splitting; this is not a published erratum or a general verdict on the reference.",
                "source_location": "Table 5 p.52; Theorem 4.82 proof item (4) p.57 versus Eq.(4.59) p.49",
                "printed_group_unchanged": True,
            }
        return cell

    def mirror_cell(self, run, full=False, actual=None):
        if run["input"]["family"] != "point3" or run["input"]["name"] != "Cs":
            return missing("not_applicable", "source column is the charge-preserving 3D mirror Cs classification")
        record = self.mirror_rows.get(run["input"]["id"])
        if record is None:
            return missing("unverified", "mirror source fixture not loaded")
        cell = group_cell(record["fullPhysical" if full else "namedE8Quotient"], actual=actual,
                          source="NMLW", scope="full physical mirror classification" if full else "source-named independent E8 quotient; not a computed physical projection",
                          location=record["source_location"], limit=record["comparison_limit"])
        cell.update(named_E8_detector=record["namedE8"], retained_detector=record["retained_detector"],
                    spin_convention=record["spin_convention"])
        return cell

    @staticmethod
    def row(run):
        i = run["input"]
        assert i["spin"] in SPINS
        if run["run"]["status"] != "complete":
            raise ValueError(f"Incomplete run {i['id']}")
        return {"id": i["id"], "family": i["family"], "index": i["index"], "name": i["name"],
                "physical_spin": i["spin"], "hermann_mauguin": i.get("hermann_mauguin"),
                "orientation_reversing": any(i["s"]), "cells": {}}

    def r2(self, run, version, actual, applicable=True):
        if not applicable:
            return missing("not_applicable", "source fixes n0=e0=0; all-n0 group not supplied")
        i = run["input"]
        if i["family"] == "point2":
            row = next(r for r in self.point["rows"] if r["name_as_printed"] == ALIASES.get(i["name"], i["name"]) and r["physical_spin"] == i["spin"])
            orders = row["stacking_orders_as_printed"]
            if version == "journal" and i["spin"] == "spinless" and i["name"] in ("C2v", "C4v", "C6v"):
                # Published supplement Table I gives D_(2m)=Z_(2m), whereas
                # arXiv v2 gives Z_(4m). This is a source-version fact.
                orders = [int(i["name"][1:-1])]
            location = "Supplement Table I p.2" if version == "journal" else "Supplement Table I; v2 TeX lines3547-3568"
        else:
            row = next(r for r in self.wall["rows"] if r["name"] == i["name"] and r["physical_spin"] == i["spin"])
            orders = row["stacking_orders"]
            location = "Main Table III p.033081-4" if version == "journal" else f"Main Table III; v2 TeX line{row['source_line']}"
        return group_cell(orders, actual=actual, source="R2_" + version, scope="n0=e0=0", location=location,
                          limit="Abstract stacking only; free wallpaper charge embedding not identified")

    def mcb_cell(self, run, quantity, actual=None):
        record = self.mcb_by_id.get(run["input"]["id"])
        if record is None:
            return missing("not_applicable", "source covers orientation-preserving wallpaper groups")
        return group_cell(record[quantity], actual=actual, source="MCB", scope={
            "referenceC0CentralCharge0": "C=c_minus=0, hence n0=e0=0",
            "referenceK1Zero": "k1=0, hence e0=0 and C=c_minus; all n0",
            "fullPhysicalReference": "independent electric/thermal/filling responses; full E8 included"}[quantity],
            location="Table I and Sec.III response restrictions",
            limit=self.mcb["limit"])

    def emit(self, name, title, scope, columns, rows, source_keys):
        ids = [r["id"] for r in rows]
        if len(ids) != len(set(ids)):
            raise ValueError(f"Duplicate group/spin row in {name}")
        rows.sort(key=lambda r: (r["family"], r["index"], list(SPINS).index(r["physical_spin"])))
        counts = {key: dict(collections.Counter(r["cells"][key]["comparison_status"] for r in rows)) for key, _ in columns}
        availability = {key: dict(collections.Counter(r["cells"][key]["availability"] for r in rows)) for key, _ in columns}
        table = {"title": title, "scope": scope, "row_rule": "One concrete catalog group and one physical spin per row",
                 "columns": [{"key": key, "label": label} for key, label in columns],
                 "sources": {key: SOURCES[key] for key in source_keys}, "comparison_counts": counts,
                 "availability_counts": availability, "rows": rows}
        self.tables[name] = table
        stem = self.out / name
        stem.parent.mkdir(parents=True, exist_ok=True)
        stem.with_suffix(".json").write_text(json.dumps(table, indent=2) + "\n")
        base = ["id", "family", "index", "name", "physical_spin", "hermann_mauguin", "orientation_reversing"]
        suffixes = ["display", "availability", "torsion", "free_rank", "comparison_status", "source", "scope", "source_location", "comparison_limit", "reason", "proof_audit"]
        with stem.with_suffix(".csv").open("w", newline="") as handle:
            writer = csv.DictWriter(handle, fieldnames=base + [f"{key}__{suffix}" for key, _ in columns for suffix in suffixes],
                                    lineterminator="\n")
            writer.writeheader()
            for row in rows:
                flat = {key: row[key] for key in base}
                for key, _ in columns:
                    cell = row["cells"][key]
                    values = {**cell, "display": show(cell), "torsion": json.dumps(cell["group"]["torsion"]) if "group" in cell else "",
                              "free_rank": cell.get("group", {}).get("freeRank", "")}
                    for suffix in suffixes:
                        value = values.get(suffix, "")
                        flat[f"{key}__{suffix}"] = json.dumps(value) if isinstance(value, (dict, list)) else value
                writer.writerow(flat)
        lines = ["# " + title, "", scope, "",
                 "Each row has one group and one physical spin. `0` is the trivial group. `N/A` means this source or quantity does not apply; `UNVERIFIED` means a relevant value or map has not been established; `NOT COMPUTED` means the runtime does not supply that object. An abstract match is not a physical generator-map or completeness certificate.", "",
                 "| Group | Physical spin | " + " | ".join(label for _, label in columns) + " |",
                 "| --- | --- | " + " | ".join("---" for _ in columns) + " |"]
        for row in rows:
            cells = [row["name"], SPINS[row["physical_spin"]]] + [show(row["cells"][key], compact=True) for key, _ in columns]
            lines.append("| " + " | ".join(c.replace("|", "\\|").replace("\n", " ") for c in cells) + " |")
        lines += ["", "Source columns:", ""]
        for key in source_keys:
            s = SOURCES[key]
            lines += [f"- **{key}:** {s['authors']}. [{s['title']}]({s['url']}). {s['version']}. {s['method']}. Location: {s['location']}."]
            if s.get("scope") or s.get("independence_limit"):
                lines[-1] += " " + " ".join(str(s[k]) for k in ("scope", "independence_limit") if s.get(k))
        lines += ["", "Exact cyclic factors, source locations, comparison limitations and unavailable-value reasons are retained in the adjacent JSON and CSV.", ""]
        stem.with_suffix(".md").write_text("\n".join(lines))

    def relative(self):
        for family in ("point2", "wallpaper"):
            rows = []
            for run in self.runs2:
                if run["input"]["family"] != family:
                    continue
                row = self.row(run)
                actual = run["classification"]["relativeUniformIQH0"]
                cells = row["cells"]
                cells["model_stacking"] = group_cell(actual, scope="n0=e0=0 retained model")
                cells["R2_journal"] = self.r2(run, "journal", actual)
                cells["R2_arxiv"] = self.r2(run, "arxiv", actual)
                if family == "point2":
                    cells["Debray_relative"] = self.debray_cell(run, "relative_n0_e0_zero", actual)
                else:
                    cells["MCB_relative"] = self.mcb_cell(run, "referenceC0CentralCharge0", actual)
                    i = run["input"]
                    ref = next(r for r in self.layers["rows"] if r["name_as_printed"] == WALL_ALIASES.get(i["name"], i["name"]) and r["physical_spin"] == i["spin"])
                    for label, model_key, source_key in (("charge", "finalCharge", "charge_orders"), ("phase", "finalPhase", "phase_after_incoming_orders")):
                        group = {"torsion": actual[model_key + "Orders"], "freeRank": actual[model_key + "FreeRank"]}
                        cells["model_" + label] = group_cell(group, scope="final filtration layer")
                        cells["L2_" + label] = group_cell(ref[source_key], actual=group, source="L2", scope="final " + label + " layer; not a stacking group",
                                                       location=f"Supplement H, {'II' if i['spin']=='spin_half' else 'III'}, TeX line{ref['source_line']}")
                    cells["filling_map"] = missing("unverified", "source orbit coordinates to primitive-cell filling map")
                rows.append(row)
            columns = [("model_stacking", "Computed relative model"), ("R2_journal", "Zhang–Yang–Qi–Gu 2022 stacking"), ("R2_arxiv", "Zhang–Yang–Qi–Gu 2023v2 stacking")]
            keys = ["R2_journal", "R2_arxiv"]
            if family == "point2":
                columns += [("Debray_relative", "Debray 2026v3, matching relative sector")]
                keys += ["Debray"]
            else:
                columns += [("MCB_relative", "Manjunath–Calvera–Barkeshli 2024, C=c-=0"), ("model_charge", "Computed charge layer"), ("L2_charge", "Wang–Qi–Fang–Cheng–Gu 2021v1 charge layer"), ("model_phase", "Computed phase layer"), ("L2_phase", "Wang–Qi–Fang–Cheng–Gu 2021v1 final phase layer"), ("filling_map", "Physical filling map")]
                keys += ["MCB", "L2"]
            self.emit("relative_" + family, "2D " + ("point groups" if family == "point2" else "wallpaper groups") + ": n0=e0=0", "Interacting relative stacking subgroup, with zero electric and thermal Hall response. Uniform neutral E8 is excluded explicitly. Phase and charge layers are displayed separately from stacking; their product is not assumed to be the stacking group.", columns, rows, keys)

    def all_n0(self):
        rows = []
        for run in self.runs2:
            row = self.row(run)
            actual = run["classification"]
            c = row["cells"]
            c["model"] = group_cell(actual, scope="all allowed n0 in the supplied model, no independent E8")
            multiplicities = [Fraction(str(w["sheetMultiplicity"])) for w in actual.get("witnesses", []) if w.get("kind") == "uniform-IQH-lift"]
            assert all(value.denominator == 1 for value in multiplicities)
            values = [abs(int(value)) for value in multiplicities]
            step = 0
            for value in values:
                step = gcd(step, value)
            if row["orientation_reversing"]:
                assert not values
                c["n0_image"] = note("{0}; nonzero uniform n0 forbidden")
                c["physical_product"] = note("No nonzero-n0 product exercised; e0 omitted")
            else:
                assert step > 0
                c["n0_image"] = note("Z" if step == 1 else f"{step}Z")
                c["physical_product"] = missing("unverified", "universal physical nonzero-n0 product/response map")
            c["R2_journal"] = self.r2(run, "journal", actual, row["orientation_reversing"])
            c["R2_arxiv"] = self.r2(run, "arxiv", actual, row["orientation_reversing"])
            c["MCB_e0_zero"] = self.mcb_cell(run, "referenceK1Zero", actual)
            c["Debray_e0_zero"] = self.debray_cell(run, "all_n0_e0_zero", actual)
            rows.append(row)
        self.emit("all_n0_retained_model_2d", "2D all-n0 stacking group of the retained model", "All allowed uniform CI coordinates are included together. This is the supplied no-independent-E8 model, not a computed full physical invertible-phase classification. A single fixed nonzero-n0 fiber is a torsor, not the group displayed here. For orientation-reversing cases the allowed n0 is only zero, so the relative reference applies. Where n0 varies, the physical product/response calibration remains unverified even if an abstract source subgroup matches.",
                  [("model", "Computed all-n0 model"), ("n0_image", "Allowed n0"), ("physical_product", "Physical-product limit"), ("R2_journal", "Zhang–Yang–Qi–Gu 2022"), ("R2_arxiv", "Zhang–Yang–Qi–Gu 2023v2"), ("MCB_e0_zero", "Manjunath–Calvera–Barkeshli 2024, k1=0"), ("Debray_e0_zero", "Debray 2026v3, e0=0")], rows, ["R2_journal", "R2_arxiv", "MCB", "Debray"])

    def three_dimensional(self):
        rows, full_rows = [], []
        journal = {r["id"]: r for r in self.full3j["rows"]}
        e8a = {(r["name"], r["physical_spin"]): r for r in self.e8a["rows"]}
        e8j = {r["id"]: r for r in self.e8j["rows"]}
        for run in self.runs3:
            row, full = self.row(run), self.row(run)
            actual = run["classification"]
            row["cells"]["model"] = group_cell(actual, scope="retained CI/charge/group-cohomological phase model")
            j = journal[row["id"]]
            printed = "S6" if row["name"] == "C3i" else row["name"]
            a = next(r for r in self.full3a["rows"] if r["physical_spin"] == row["physical_spin"] and r["name_as_printed"].split("=")[0].translate(str.maketrans("", "", "$_{}")) == printed)
            for version, r in (("arxiv", a), ("journal", j)):
                source = "R3_" + version
                full["cells"][source] = group_cell(r["stacking_orders"], source=source, scope="source full physical interacting group; E8 included where present", location="Table II")
                if row["orientation_reversing"]:
                    evidence = e8a[row["name"], row["physical_spin"]] if version == "arxiv" else e8j[row["id"]]
                    orders = evidence["quotient_by_named_E8_orders"]
                    scope = "source full group / its named independent neutral E8 root"
                    location = evidence.get("source_location", {"table": "II", "source_root_line": evidence["source_root_line"]} if "source_root_line" in evidence else None)
                else:
                    orders, scope, location = r["stacking_orders"], "proper-rotation source full group; leading E8 H1 is zero", "Table II"
                row["cells"][source] = group_cell(orders, actual=actual, source=source, scope=scope, location=location,
                    limit="Reference-side abstract comparison only; no model-to-physical quotient isomorphism established")
            row["cells"]["scope"] = note("Named-E8 quotient; physical map unverified" if row["orientation_reversing"] else "Proper rotations; source full group")
            row["cells"]["Debray_retained"] = self.debray_cell(run, "retained_model_quotient", actual)
            row["cells"]["NMLW_retained"] = self.mirror_cell(run, actual=actual)
            full["cells"]["Debray_full"] = self.debray_cell(run, "full_physical")
            full["cells"]["NMLW_full"] = self.mirror_cell(run, full=True)
            rows.append(row)
            full_rows.append(full)
        self.emit("retained_model_point3", "3D point groups: retained-model comparisons", "The computed column contains the retained CI, charge and group-cohomological phase model. Each real-space source version has its own reference column. For improper groups those columns are explicitly source-side quotients by independently identified neutral E8 roots; equality of invariant factors is not a verified physical quotient map. No missing E8 operation is assigned zero.",
                  [("model", "Computed retained model"), ("scope", "Comparison scope"), ("R3_arxiv", "Zhang–Ning–Qi–Gu 2024v2"), ("R3_journal", "Zhang–Ning–Qi–Gu journal2025"), ("Debray_retained", "Debray 2026v3, explicitly matched sector"), ("NMLW_retained", "Ning–Mao–Li–Wang 2021, named-E8 quotient")], rows, ["R3_arxiv", "R3_journal", "Debray", "NMLW"])
        self.emit("full_E8_reference_point3", "3D point groups: full physical reference groups", "Reference-only table. Independent neutral E8 decorations are retained wherever the cited physical classification includes them. There is no computed full-E8 physical classification column. The values must not be compared directly with the retained-model column in another table without a sector map.",
                  [("R3_arxiv", "Zhang–Ning–Qi–Gu 2024v2, full"), ("R3_journal", "Zhang–Ning–Qi–Gu journal2025, full"), ("Debray_full", "Debray 2026v3, full physical"), ("NMLW_full", "Ning–Mao–Li–Wang 2021, full mirror")], full_rows, ["R3_arxiv", "R3_journal", "Debray", "NMLW"])

    def physical2(self):
        rows = []
        for run in self.runs2:
            row = self.row(run)
            row["cells"]["MCB_full"] = self.mcb_cell(run, "fullPhysicalReference")
            row["cells"]["Debray_full"] = self.debray_cell(run, "full_physical")
            rows.append(row)
        self.emit("full_E8_reference_2d", "2D full physical reference groups, with independent E8", "Reference-only table. The Manjunath–Calvera–Barkeshli column includes independent electric Hall, thermal Hall and filling coordinates for its orientation-preserving wallpaper groups. No full physical E8 classification is calculated by the current runtime. Other sources are filled only after their exact scope is verified; coverage gaps remain explicit.",
                  [("MCB_full", "Manjunath–Calvera–Barkeshli 2024, full"), ("Debray_full", "Debray 2026v3, full physical")], rows, ["MCB", "Debray"])

    def band_diagnostic(self):
        rows = []
        refs = {(r["name"], r["physical_spin"]): r for r in self.diagnostic["rows"]}
        for run in self.runs2:
            i = run["input"]
            if i["family"] != "point2" or (i["name"], i["spin"]) not in refs:
                continue
            row = self.row(run)
            actual = run["classification"]["relativeUniformIQH0"]
            row["cells"]["model"] = group_cell(actual)
            row["cells"]["B2_interacting_reduction"] = group_cell(refs[i["name"], i["spin"]]["band_generated_stacking_orders"], actual=actual, source="B2_diagnostic",
                scope="Interacting reduction of band-generated phases only; not all interacting phases", location="Table VI class A; interacting right-hand result",
                limit="Does not establish absence of intrinsically interacting phases")
            rows.append(row)
        self.emit("diagnostics/point2_band_generated_interacting_reduction", "Diagnostic only: interacting reduction of band-generated rotation phases", "This file is excluded from the main interacting-classification tables. It contains only the interacting reduction stated by Liu, Vishwanath and Khalaf, not their raw free-fermion result. An abstract match does not turn this restricted result into a complete interacting classification benchmark.",
                  [("model", "Computed relative retained model"), ("B2_interacting_reduction", "Liu–Vishwanath–Khalaf 2019, interacting reduction only")], rows, ["B2_diagnostic"])

    def build(self):
        self.relative()
        self.all_n0()
        self.three_dimensional()
        self.physical2()
        self.band_diagnostic()
        expected = {"relative_point2": 20, "relative_wallpaper": 34, "all_n0_retained_model_2d": 54,
                    "retained_model_point3": 64, "full_E8_reference_point3": 64, "full_E8_reference_2d": 54,
                    "diagnostics/point2_band_generated_interacting_reduction": 10}
        for name, count in expected.items():
            table = self.tables[name]
            assert len(table["rows"]) == count
            assert len({(r["family"], r["index"], r["physical_spin"]) for r in table["rows"]}) == count
            assert all(r["physical_spin"] in SPINS for r in table["rows"])
            if not name.startswith("diagnostics/"):
                assert "B2_diagnostic" not in table["sources"]
            if name.startswith("full_E8_"):
                assert all(not col["key"].startswith("model") for col in table["columns"])
                assert all(c["comparison_status"] == "not_compared" for r in table["rows"] for c in r["cells"].values())
        for row in self.tables["retained_model_point3"]["rows"]:
            if row["orientation_reversing"]:
                assert row["cells"]["Debray_retained"]["availability"] != "available"
        summary = {"generator": "scripts/build_foundation_tables.py", "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
                   "inputs_sha256": self.inputs, "row_counts": expected,
                   "single_group_single_spin_rows_verified": True,
                   "band_generated_diagnostic_excluded_from_main_tables": True,
                   "full_E8_tables_have_no_computed_physical_column": True,
                   "debray_improper_3d_not_projected": True,
                   "debray_printed_d2_d6_values_preserved_with_separate_proof_audit": True,
                   "debray_fixture_loaded": self.debray is not None,
                   "mirror_fixture_loaded": self.mirror is not None,
                   "availability_counts": {name: t["availability_counts"] for name, t in self.tables.items()},
                   "comparison_counts": {name: t["comparison_counts"] for name, t in self.tables.items()}}
        (self.out / "table_validation.json").write_text(json.dumps(summary, indent=2) + "\n")
        print(json.dumps({"output": str(self.out), "row_counts": expected, "debray_fixture_loaded": self.debray is not None}, indent=2))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output", type=Path, default=ROOT / "results/foundation_review_20261014")
    parser.add_argument("--debray-reference", type=Path, default=ROOT / "benchmarks/debray_class_a_2102.02941v3.json")
    parser.add_argument("--mirror-reference", type=Path, default=ROOT / "benchmarks/mirror_interacting_2105.02682.json")
    args = parser.parse_args()
    Builder(args.root, args.output, args.debray_reference, args.mirror_reference).build()


if __name__ == "__main__":
    main()
