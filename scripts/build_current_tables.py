#!/usr/bin/env python3
"""Build the current insulator catalogue from accepted calculations and references.

One row is one exact crystalline input and response sector. Reference values
never enter a calculation. Historical inputs and outputs are read-only.
"""
from __future__ import annotations

import argparse
from collections import Counter
from copy import deepcopy
import csv
import hashlib
import json
import os
from pathlib import Path

from build_foundation_tables import group_text, signature
from summarize_results import uniform_multiplicity

ROOT = Path(__file__).resolve().parents[1]
SPINS = {"spinless": "Spinless", "spin_half": "Spin-1/2"}
ZERO = {"torsion": [], "freeRank": 0}


def digest(data):
    return hashlib.sha256(data).hexdigest()


def encoded(value):
    return json.dumps(value, ensure_ascii=False, indent=2) + "\n"


class Catalogue:
    def __init__(self, output, expansions=()):
        self.output = output
        self.inputs, self.files, self.index = {}, {}, []
        saved_path = "results/two_dimensional_20261013/results.json"
        fresh_path = "results/four_data_campaign_20261015/results.json"
        e8_path = "results/four_data_campaign_20261015/e8_results.json"
        self.records = {}
        for position, record in enumerate(self.load(saved_path)):
            case = record["input"]["id"]
            assert record["input"]["dimension"] == 2
            self.records[case, "n0_all"] = self.entry(record, record["classification"], saved_path, position)
            self.records[case, "n0_zero"] = self.entry(
                record, record["classification"]["relativeUniformIQH0"], saved_path,
                position, "classification.relativeUniformIQH0")
        for position, record in enumerate(self.load(fresh_path)):
            if record["input"]["dimension"] != 2:
                continue
            sector = "n0_all" if record["run"]["uniformIQHRequested"] else "n0_zero"
            self.records[record["input"]["id"], sector] = self.entry(
                record, record["classification"], fresh_path, position)
        for position, record in enumerate(self.load(e8_path)):
            assert record["input"]["dimension"] == 3
            assert record["classification"]["neutralE8Included"] is True
            self.records[record["input"]["id"], "four_data"] = self.entry(
                record, record["classification"], e8_path, position)
        self.expansions, self.extra, self.audits = [], {}, {}
        for directory in expansions:
            directory = directory.resolve()
            label = self.path_name(directory)
            if label in self.expansions:
                raise ValueError("Duplicate accepted collection directory.")
            summary = self.load(directory / "collection.json")
            if summary.get("accepted") is not True:
                raise ValueError("An expansion collection is not accepted.")
            self.expansions.append(label)
            for collection in summary["collections"]:
                base = directory / collection["path"]
                for name, expected in collection["filesSHA256"].items():
                    if digest((base / name).read_bytes()) != expected:
                        raise ValueError(f"Accepted collection hash changed: {base / name}")
                validation = self.load(base / "validation.json")
                records = self.load(base / "results.json")
                if (validation.get("accepted") is not True or validation["missingOrFailedSelectedCases"]
                        or len(records) != collection["count"] or len(records) != validation["completeResultCount"]
                        or sorted(r["input"]["id"] for r in records) != validation["selectedCases"]):
                    raise ValueError("An accepted expansion has inconsistent coverage.")
                checks = {r["id"]: r for r in validation["checks"] if r["kind"] in ("e8", "four")}
                audit_path = base.parent / "cyclic_root_audit.json"
                audit_cases = {}
                if collection["family"] == "internal_cyclic" and audit_path.exists():
                    audit = self.load(audit_path)
                    if audit.get("status") != "PASS" or audit.get("spatialDimension") != 4:
                        raise ValueError("Cyclic root audit is not a completed 4+1D audit.")
                    provenance = self.load(base / "provenance.json")
                    raw_hashes = {key: value for item in provenance for key, value in item["resultHashes"].items()}
                    audit_cases = {case["order"]: case for case in audit["cases"]}
                    for record in records:
                        case = audit_cases[record["input"]["order"]]
                        if (case["resultSHA256"] != raw_hashes[record["input"]["id"]]
                                or case["sourceSHA256"] != record["run"]["sourceSHA256"]
                                or case["independentBarCheck"]["presentation"] != record["classification"]["presentation"]):
                            raise ValueError("Cyclic root audit does not match the accepted result.")
                    self.audits[self.path_name(audit_path)] = audit
                for position, record in enumerate(records):
                    case = record["input"]["id"]
                    if case in self.extra or record["input"]["family"] != collection["family"]:
                        raise ValueError("Duplicate or mislabelled expansion input.")
                    entry = self.entry(record, record["classification"], self.path_name(base / "results.json"), position)
                    entry["checks"] = checks[case]
                    if audit_cases:
                        entry["provenance"]["independent_root_audit"] = {
                            "path": self.path_name(audit_path), "sha256": self.inputs[self.path_name(audit_path)],
                            "order": record["input"]["order"], "status": "PASS"}
                    if collection["family"] == "point3":
                        self.records[case, "four_data"] = entry
                    else:
                        self.extra[case] = entry

    @staticmethod
    def path_name(path):
        try:
            return str(path.resolve().relative_to(ROOT))
        except ValueError:
            return str(path.resolve())

    def load(self, name):
        path = ROOT / name
        data = path.read_bytes()
        self.inputs[self.path_name(path)] = digest(data)
        return json.loads(data)

    def expansion_table(self, family, spin=None):
        selected = [r for r in self.extra.values() if r["input"]["family"] == family
                    and (spin is None or r["input"]["spin"] == spin)]
        if not selected:
            return
        selected.sort(key=lambda r: r["input"].get("catalog_number", r["input"].get("order")))
        dimension = 3 if family == "spacegroup" else 4
        p = dimension-2
        columns = [{"key": key, "label": text} for key, text in (
            ("e", f"e{p} (E8)"), ("n", f"n{p} (CI)"), ("charge", f"n{p+2} (charge)"),
            ("phase", f"nu{p+3} (phase)"), ("stacking", "Final stacking"))]
        sources = {}
        if family == "spacegroup":
            destination = Path("3p1d") / spin / "space_groups"
            fixture = self.load("benchmarks/spacegroup_e8_1811.06558v1.json")
            references = {r["spaceGroupNumber"]: r for r in fixture["rows"]}
            source = deepcopy(fixture["source"])
            source.update(version="arXiv v1 (2018); PRB 101, 165129 (2020)",
                          location="Table II, fourth column only: neutral H1(G,Z_orientation)")
            sources["SXH_neutral"] = source
            columns += [{"key": "SXH_neutral", "label": "Song–Xiong–Huang 2018v1, neutral E8 only"}]
            title = f"3+1D {SPINS[spin]} space groups"
            scope = ("The full infinite affine group and primitive translations are retained. E8 data use the selected section and signed integer H1. "
                     "The Song–Xiong–Huang column compares only the e1 layer, not the full electronic stacking group. "
                     "The physical CI-kernel identification remains conditional.")
        else:
            destination = Path("4p1d/internal_cyclic")
            title = "4+1D internal cyclic groups: s=rho=omega=0"
            scope = ("Unitary internal U(1)^f x C_N; no crystalline spin convention is assigned. "
                     "The original four-data tower includes e2,n2,n4,nu5 and excludes the deferred intrinsic r0 response. "
                     "Filtration groups are derived from the actual root-relation presentation by saturated integer elimination. "
                     "The physical CI-kernel identification remains conditional.")
        columns += [{"key": "physical_reference", "label": "Full interacting electronic reference"}]
        rows = []
        for selected_record in selected:
            data, c = selected_record["input"], selected_record["classification"]
            if family == "spacegroup":
                ci = c["ciSector"]
                layers = {"e": signature(c["e8H1"]), "n": self.layer(ci, "Sheet"),
                          "charge": self.layer(ci, "Charge"), "phase": self.layer(ci, "Phase")}
                name, hm = data["name"], data["hermann_mauguin"]
                display = f"{data['catalog_number']}. {name}"
            else:
                layers = selected_record["checks"]["finalFiltrationFromPresentation"]
                name, hm, display = f"C{data['order']}", None, f"C{data['order']}"
            cells = {key: self.cell(value) for key, value in layers.items()}
            cells["stacking"] = self.cell(c)
            if family == "spacegroup":
                reference = references[data["catalog_number"]]
                cells["SXH_neutral"] = self.reference({**self.cell(reference["neutralE8"]),
                    "source": "SXH_neutral", "scope": "Neutral E8 layer only; bosonic coefficient-sector reference, not full electronic classification",
                    "source_location": {"line": reference["sourceLine"], "cell": reference["sourceCellTeX"]}}, layers["e"])
            cells["physical_reference"] = {"availability": "unverified", "comparison_status": "not_compared",
                "reason": "No independently verified full interacting electronic reference with this exact symmetry and response scope is included."}
            row = {"id": data["id"], "name": name, "hermann_mauguin": hm, "display_name": display,
                   "family": family, "physical_spin": spin if spin else "not_applicable_internal",
                   "spatial_dimension": dimension, "spacetime_dimension": dimension+1,
                   "n0_scope": "not_applicable", "e0_scope": "not_applicable",
                   "e8_scope": "selected_section_included" if dimension == 3 else "original_four_data_included",
                   "cells": cells, "provenance": deepcopy(selected_record["provenance"])}
            if dimension == 4:
                row["background"] = {"s": 0, "rho": 0, "omega": "0", "intrinsic_r0_included": False}
            rows.append(row)
            self.index.append({**{k: deepcopy(v) for k,v in row.items() if k != "cells"},
                               "table": str(destination.with_suffix(".json")), "stacking": signature(c),
                               "final_filtration": deepcopy(layers)})
        self.render(destination, {"title": title, "scope": scope, "family": family,
                    "spatial_dimension": dimension, "spacetime_dimension": dimension+1,
                    "physical_spin": spin if spin else "not_applicable_internal", "n0_scope": "not_applicable",
                    "e0_scope": "not_applicable", "e8_scope": rows[0]["e8_scope"],
                    "columns": columns, "sources": sources, "rows": rows})

    def entry(self, record, classification, path, position, selector="classification"):
        assert record["run"]["status"] == "complete"
        return {"input": record["input"], "classification": classification,
                "provenance": {"path": path, "array_index": position, "selector": selector,
                               "source_sha256": record["run"]["sourceSHA256"],
                               "input_sha256": record["run"]["inputSHA256"],
                               "started_utc": record["run"].get("startedUTC"),
                               "record_sha256": digest(json.dumps(record, sort_keys=True, separators=(",", ":")).encode())}}

    def put(self, path, text):
        self.files[str(path)] = text

    @staticmethod
    def layer(classification, name):
        return signature({"torsion": classification["final" + name + "Orders"],
                          "freeRank": classification["final" + name + "FreeRank"]})

    @staticmethod
    def cell(group):
        return {"availability": "available", "comparison_status": "not_compared",
                "group": signature(group)}

    @staticmethod
    def reference(cell, actual):
        result = deepcopy(cell)
        if result["availability"] == "available" and "group" in result:
            result["comparison_status"] = "match" if signature(result["group"]) == signature(actual) else "mismatch"
        return result

    def table(self, dimension, spin, family, sector):
        label = SPINS[spin]
        stem = "wallpaper_groups" if family == "wallpaper" else "point_groups"
        if dimension == 2:
            template_path = f"results/foundation_review_20261014/2p1d/{spin}/e0_zero/{sector}/{stem}.json"
            destination = Path("2p1d") / spin / sector / stem
            response = "n0=0, e0=0" if sector == "n0_zero" else "all allowed n0, e0=0"
            scope = ("The uniform E8 response is fixed to e0=0. "
                     + ("The uniform IQH response is fixed to n0=0. " if sector == "n0_zero" else
                        "All symmetry-allowed uniform IQH responses are included. ")
                     + "The four data columns are final filtration groups after incoming identifications; their product need not be the final stacking group.")
            refs = (["Debray_relative", "R2_journal", "R2_arxiv"] if sector == "n0_zero" else
                    ["Debray_e0_zero", "R2_journal", "R2_arxiv"]) if family == "point2" else (
                    ["R2_journal", "R2_arxiv", "MCB_relative", "L2_charge", "L2_phase"] if sector == "n0_zero" else
                    ["R2_journal", "R2_arxiv", "MCB_e0_zero"])
        else:
            template_path = f"results/four_data_campaign_20261015/3p1d/{spin}/with_e8/{stem}.json"
            destination = Path("3p1d") / spin / stem
            response = "four-data model"
            scope = ("The selected E8 section is included through the independently computed H1(G,Z_s). "
                     "The four data columns are final filtration groups; stacking includes their extensions. "
                     "Identification of the computed CI kernel with the complete physical theory remains conditional. "
                     "Reference columns give full interacting classifications, including neutral E8 contributions.")
            refs = ["Debray", "NMLW", "R3_arxiv", "R3_journal"]
        template = self.load(template_path)
        p = dimension - 2
        columns = [{"key": key, "label": text} for key, text in (
            ("e", f"e{p} (E8)"), ("n", f"n{p} (CI)"),
            ("charge", f"n{p+2} (charge)"), ("phase", f"nu{p+3} (phase)"),
            ("stacking", "Final stacking"))]
        labels = {c["key"]: c["label"] for c in template["columns"]}
        columns += [{"key": key, "label": labels[key]} for key in refs]
        rows = []
        for old in template["rows"]:
            record = self.records[old["id"], sector]
            data, classification = record["input"], record["classification"]
            assert (data["dimension"], data["spin"], data["family"], data["name"]) == (dimension, spin, family, old["name"])
            ci = classification if dimension == 2 else classification["ciSector"]
            layers = {"e": ZERO if dimension == 2 else signature(classification["e8H1"]),
                      "n": ZERO if sector == "n0_zero" else self.layer(ci, "Sheet"),
                      "charge": self.layer(ci, "Charge"), "phase": self.layer(ci, "Phase")}
            cells = {key: self.cell(value) for key, value in layers.items()}
            cells["stacking"] = self.cell(classification)
            for key in refs:
                target = layers[key[3:]] if key in ("L2_charge", "L2_phase") else classification
                cells[key] = self.reference(old["cells"][key], target)
            row = {"id": data["id"], "name": data["name"], "hermann_mauguin": old["hermann_mauguin"],
                   "family": family, "physical_spin": spin, "spatial_dimension": dimension,
                   "spacetime_dimension": dimension + 1, "n0_scope": sector if dimension == 2 else "not_applicable",
                   "e0_scope": "e0_zero" if dimension == 2 else "not_applicable",
                   "e8_scope": "fixed_uniform_zero" if dimension == 2 else "selected_section_included",
                   "cells": cells, "provenance": deepcopy(record["provenance"])}
            if sector == "n0_all":
                row["uniform_iqh_image"] = uniform_multiplicity(classification)
            rows.append(row)
            self.index.append({**{k: deepcopy(v) for k, v in row.items() if k != "cells"},
                "table": str(destination.with_suffix(".json")),
                "stacking": signature(classification), "final_filtration": deepcopy(layers)})
        sources = {}
        for reference in refs:
            key = next(key for key in template["sources"]
                       if reference == key or reference.startswith(key + "_"))
            sources.setdefault(key, deepcopy(template["sources"][key]))
        table = {"title": f"{dimension}+1D {label} {family.replace('point2', 'point groups').replace('point3', 'point groups').replace('wallpaper', 'wallpaper groups')}: {response}",
                 "scope": scope, "spatial_dimension": dimension, "spacetime_dimension": dimension+1,
                 "physical_spin": spin, "family": family, "n0_scope": sector if dimension == 2 else "not_applicable",
                 "e0_scope": "e0_zero" if dimension == 2 else "not_applicable",
                 "e8_scope": "fixed_uniform_zero" if dimension == 2 else "selected_section_included",
                 "columns": columns, "sources": sources, "rows": rows}
        self.render(destination, table)

    def render(self, destination, table):
        keys = [c["key"] for c in table["columns"]]
        table["comparison_counts"] = {key: dict(Counter(row["cells"][key]["comparison_status"] for row in table["rows"])) for key in keys}
        table["availability_counts"] = {key: dict(Counter(row["cells"][key]["availability"] for row in table["rows"])) for key in keys}
        self.put(destination.with_suffix(".json"), encoded(table))
        headers = ["Group" if table["family"] == "internal_cyclic" else "Group (HM)"] + [c["label"] for c in table["columns"]]
        def row_name(row):
            return row.get("display_name", f"{row['name']} ({row['hermann_mauguin']})")
        def display(cell, markdown):
            if cell["availability"] != "available":
                return {"unverified": "UNVERIFIED", "not_applicable": "N/A", "not_computed": "NOT COMPUTED"}[cell["availability"]]
            mark = {"match": "✓", "mismatch": "×"}.get(cell["comparison_status"], "")
            prefix = (f"**{mark}** " if markdown else mark + " ") if mark else ""
            return prefix + group_text(cell["group"]) + (" †" if cell.get("proof_audit") else "")
        lines = ["# " + table["title"], "", table["scope"], "",
                 "**✓** same reported classification group; **×** different reported classification group. UNVERIFIED is not a match.", "",
                 "| " + " | ".join(headers) + " |", "| " + " | ".join(["---"]*len(headers)) + " |"]
        for row in table["rows"]:
            lines.append("| " + " | ".join([row_name(row)] + [display(row["cells"][key], True) for key in keys]) + " |")
        audits = {cell["proof_audit"]["path"] for row in table["rows"] for cell in row["cells"].values() if cell.get("proof_audit")}
        for audit in sorted(audits):
            link = os.path.relpath(ROOT / audit, self.output / destination.parent)
            lines += ["", f"† Printed source values are preserved; see the [supporting-proof grading audit]({link})."]
        if table["sources"]:
            lines += ["", "Sources:", ""]
        for key, source in table["sources"].items():
            authors = source.get("authors", source.get("author", ""))
            if isinstance(authors, list):
                authors = ", ".join(authors)
            lines.append(f"- [{authors}, {source.get('version', source.get('year', ''))}]({source['url']}). "
                         + source.get("title", "") + ". " + source.get("location", "") + ". " + source.get("method", "") + ".")
        provenance = os.path.relpath(self.output / "PROVENANCE.md", self.output / destination.parent)
        audit_paths = sorted({row["provenance"]["independent_root_audit"]["path"] for row in table["rows"]
                              if "independent_root_audit" in row["provenance"]})
        for path in audit_paths:
            link = os.path.relpath(ROOT / path, self.output / destination.parent)
            lines += ["", f"[Independent complete-root and native-boundary audit]({link}): explicit bar-cycle roots and canonical gauges reproduce these presentations; this checks the model, not its physical-spectrum identification."]
        lines += ["", f"[Calculation provenance and scope]({provenance}).", ""]
        self.put(destination.with_suffix(".md"), "\n".join(lines))
        import io
        stream = io.StringIO(newline="")
        writer = csv.writer(stream, lineterminator="\n")
        writer.writerow(["id", "physical_spin", "spatial_dimension", "n0_scope", "e0_scope", "e8_scope"] + headers)
        for row in table["rows"]:
            writer.writerow([row[k] for k in ("id", "physical_spin", "spatial_dimension", "n0_scope", "e0_scope", "e8_scope")]
                            + [row_name(row)] + [display(row["cells"][key], False) for key in keys])
        self.put(destination.with_suffix(".csv"), stream.getvalue())

    def build(self):
        for spin in SPINS:
            for sector in ("n0_zero", "n0_all"):
                for family in ("point2", "wallpaper"):
                    self.table(2, spin, family, sector)
            self.table(3, spin, "point3", "four_data")
            self.expansion_table("spacegroup", spin)
        self.expansion_table("internal_cyclic")
        count = len(self.records) + len(self.extra)
        assert len(self.index) == count
        assert len({(x["id"], x["n0_scope"]) for x in self.index}) == count
        backgrounds = len({r["id"] for r in self.index})
        space_count = sum(r["family"] == "spacegroup" for r in self.index)
        cyclic_count = sum(r["family"] == "internal_cyclic" for r in self.index)
        table_count = sum(name.endswith(".json") and "columns" in json.loads(text)
                          for name, text in self.files.items() if name.endswith(".json"))
        self.index.sort(key=lambda r: (r["spatial_dimension"], r["physical_spin"], r["n0_scope"], r["id"]))
        self.put("index.json", encoded(self.index))
        self.put("collections.json", encoded({"accepted_expansion_directories": self.expansions}))
        self.put("README.md", "# Computed U(1)^f insulator examples\n\n"
                 f"The current catalogue contains {backgrounds} distinct backgrounds and {count} response-sector entries. "
                 "It includes all 54 planar/wallpaper backgrounds and all 64 spatial point-group backgrounds. "
                 "Each 2+1D background has separate n0=0 and all-allowed-n0 tables, both with e0=0. "
                 "The 3+1D tables include the computed neutral E8 section.\n\n"
                 "- [2+1D: point groups and wallpaper groups](2p1d/README.md).\n"
                 "- [3+1D: crystalline groups](3p1d/README.md).\n"
                 + (f"- [4+1D: internal cyclic groups](4p1d/README.md), {cyclic_count} completed inputs.\n" if cyclic_count else "")
                 + (f"\nThe 3+1D collection also contains {space_count} completed space-group inputs, counted separately for each physical spin.\n" if space_count else "")
                 + "\n"
                 "Each row gives the four final data layers, final stacking group, and separately cited interacting references. "
                 "Physical spins and response sectors have separate files. **✓** marks the same reported group; **×** marks a different reported group.\n\n"
                 "[Calculation provenance and scope](PROVENANCE.md) · [Machine-readable example index](index.json).\n")
        for d in (2, 3):
            self.put(f"{d}p1d/README.md", f"# {d}+1D insulator examples\n\n"
                     + "\n".join(f"- [{label}]({spin}/README.md)." for spin, label in SPINS.items()) + "\n")
            for spin, label in SPINS.items():
                base = f"{d}p1d/{spin}"
                if d == 2:
                    self.put(base + "/README.md", f"# 2+1D {label}\n\nUniform E8 response: e0=0.\n\n"
                             "- [n0=0](n0_zero/README.md).\n- [All allowed n0](n0_all/README.md).\n")
                    for sector, scope in (("n0_zero", "n0=0"), ("n0_all", "all allowed n0")):
                        self.put(base + f"/{sector}/README.md", f"# 2+1D {label}: {scope}, e0=0\n\n"
                                 "- [Point groups](point_groups.md) · [CSV](point_groups.csv).\n"
                                 "- [Wallpaper groups](wallpaper_groups.md) · [CSV](wallpaper_groups.csv).\n")
                else:
                    self.put(base + "/README.md", f"# 3+1D {label}\n\n"
                             "- [Point groups, with E8 data](point_groups.md) · [CSV](point_groups.csv).\n"
                             + ("- [Space groups, with E8 data](space_groups.md) · [CSV](space_groups.csv).\n"
                                if any(r["family"] == "spacegroup" and r["physical_spin"] == spin for r in self.index) else ""))
        if cyclic_count:
            self.put("4p1d/README.md", "# 4+1D internal insulator examples\n\n"
                     "- [Unitary cyclic groups, s=rho=omega=0](internal_cyclic.md) · [CSV](internal_cyclic.csv).\n\n"
                     "These are internal symmetries without crystalline spin labels. The original four-data tower is included; intrinsic r0 remains outside the scope.\n")
        self.put("PROVENANCE.md", "# Calculation provenance and scope\n\n"
                 "The catalogue selects one accepted calculation per exact input and response sector. It uses the 64 completed E8-inclusive point-group records and 44 completed 2+1D records from the October 15 campaign. "
                 "The remaining 64 2+1D sector entries use the exhaustive October 13 campaign. For an entry without a separate n0=0 rerun, its value is the saved kernel of the actual IQH response homomorphism, not an inferred removal of a free factor. "
                 "Dates, input/source hashes, immutable record locations and exact selectors are retained in [index.json](index.json); consumed file hashes are in [manifest.json](manifest.json).\n\n"
                 "The final filtration columns are e_p, n_p, n_(p+2), nu_(p+3), with p=d−2. They already include the computed incoming identifications. Their direct product is not assumed to equal the final stacking group. "
                 "The 2+1D tables impose e0=0; the 3+1D tables include independently computed H1(G,Z_s) and the selected E8 section. The remaining identification of the CI model with the complete physical kernel is not certified by a matching abstract group. Intrinsic higher-response sectors are outside these tables.\n\n"
                 "Every literature version has its own column. The 3+1D columns use full interacting source groups, without removing E8 factors. The 2+1D references are restricted to the stated n0/e0 sector. Wang–Qi–Fang–Cheng–Gu columns are charge and phase filtration layers, not stacking groups. Unavailable source values remain UNVERIFIED; an inapplicable source is N/A. No free-band classification or band-generated subgroup is used as a complete interacting benchmark.\n\n"
                 "The [source ledger](../../docs/reference_ledger_20261014.md), [foundation review](../../docs/foundations/README.md), and immutable [October 15 campaign](../four_data_campaign_20261015/README.md) retain detailed calibration and validation evidence. "
                 "Printed Debray D2/D6 values remain unchanged, with their specific proof-grading audit linked in the tables. "
                 "Published tables are comparisons, never solver inputs.\n\n"
                 "Additional accepted collections are listed explicitly in [collections.json](collections.json). "
                 "The builder never scans unfinished runs. Each expansion is accepted by `scripts/collect_expansion.py`, which verifies every selected run, exact CI parent artifacts, source/input hashes, native completion records, and independent integer presentations. "
                 "Space-group Song–Xiong–Huang comparisons concern only the neutral E8 coefficient; full electronic references remain unverified. "
                 "4+1D cyclic filtration entries are derived from the actual root-relation matrix by saturated integer elimination, without treating equal layer orders as the stacking answer.\n\n"
                 + "".join(f"- [Independent cyclic complete-root and native-boundary audit]({os.path.relpath(ROOT / path, self.output)}): {len(audit['cases'])} presentations and {audit['nativePhaseBoundaryCheckCount']} native phase boundaries verified. Its result/source hashes are checked against the accepted collection.\n" for path, audit in sorted(self.audits.items()))
                 + ("\n" if self.audits else "")
                 +
                 "Rebuild with `python3 scripts/build_current_tables.py`; verify deterministic output with `python3 scripts/build_current_tables.py --check`. Historical artifacts are read-only.\n")
        self.inputs["scripts/build_current_tables.py"] = digest(Path(__file__).read_bytes())
        self.put("manifest.json", encoded({"input_sha256": self.inputs,
                 "output_sha256": {name: digest(text.encode()) for name, text in sorted(self.files.items())},
                 "background_count": backgrounds, "sector_entry_count": count, "table_count": table_count,
                 "single_dimension_spin_family_and_response_sector_per_table": True}))

    def save(self, check=False):
        previous_manifest = self.output / "manifest.json"
        if previous_manifest.exists():
            previous_files = json.loads(previous_manifest.read_text())["output_sha256"]
            for name in set(previous_files) - set(self.files):
                relative = Path(name)
                if relative.is_absolute() or ".." in relative.parts:
                    raise ValueError("Unsafe generated path in the current manifest.")
                path = self.output / relative
                if path.exists():
                    if check:
                        raise ValueError(f"Obsolete generated output remains: {path}")
                    path.unlink()
        for name, text in self.files.items():
            path = self.output / name
            if check:
                if not path.exists() or path.read_text() != text:
                    raise ValueError(f"Generated output differs: {path}")
            else:
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_text(text)
        counts = json.loads(self.files["manifest.json"])
        print(f"{'Verified' if check else 'Built'} {counts['table_count']} tables, {counts['sector_entry_count']} sector entries, {counts['background_count']} backgrounds.")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=ROOT / "results/current")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--expansion", type=Path, action="append", default=None,
                        help="Accepted collection directory; repeat for separate immutable campaigns.")
    args = parser.parse_args()
    expansions = args.expansion
    if expansions is None:
        config = args.output / "collections.json"
        expansions = [ROOT / name for name in json.loads(config.read_text())["accepted_expansion_directories"]] if config.exists() else []
    builder = Catalogue(args.output.resolve(), expansions)
    builder.build()
    builder.save(args.check)


if __name__ == "__main__":
    main()
