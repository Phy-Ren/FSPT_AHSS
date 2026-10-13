#!/usr/bin/env python3
"""Audit the independent rotation-only interacting reduction and source versions.

This creates comparison evidence only. It is never imported by a calculation.
"""
from pathlib import Path
import argparse
import hashlib
import json


def source(path, arxiv, location):
    return {"arxiv": arxiv, "url": f"https://arxiv.org/abs/{arxiv}",
            "source_file": path.name,
            "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "location": location}


def line_containing(lines, text):
    matches = [(n, line.strip()) for n, line in enumerate(lines, 1) if text in line]
    if len(matches) != 1:
        raise ValueError(f"expected unique source location: {text!r}")
    return {"source_line": matches[0][0], "source_cell": matches[0][1]}


def extract(cache, output):
    path = next(cache.glob("1809.01636_*/Shift.tex"))
    lines = path.read_text().splitlines()
    cells = {}
    for eta in (0, 1):
        for parity in ("even", "odd"):
            prefix = f"{eta} & {parity} &"
            hit = line_containing(lines, prefix)
            cell = hit["source_cell"].split("&")[2].strip()
            expected = r"\Z_{2N} \times \Z_{N/2}" if parity == "even" else r"\Z_{N} \times \Z_{N}"
            if expected not in cell:
                raise ValueError("rotation table changed; audit the new source")
            cells[eta, parity] = {**hit, "source_cell": cell}
    rows = []
    for n in (1, 2, 3, 4, 6):
        for eta, spin in ((0, "spinless"), (1, "spin_half")):
            factors = [n // 2, 2 * n] if n % 2 == 0 else [n, n]
            rows.append({"name": f"C{n}", "physical_spin": spin,
                         "rotation_power_eta": eta,
                         "band_generated_stacking_orders": [x for x in factors if x > 1],
                         "center_presentation": [[0, n], [n, n // 2 if n % 2 == 0 else 0]],
                         **cells[eta, "even" if n % 2 == 0 else "odd"]})
    data = {"source": source(path, "1809.01636v2", "Table VI, class A; Sec V B, TeX ReductionA"),
            "scope": "Rotation only, no translation, no time reversal, general-position adjoining quotiented; interacting reduction of noninteracting phases.",
            "comparison_limit": "Does not claim absence of interaction-only roots. Equality is an independent band-generated-sector control, not a completeness proof.",
            "uniform_IQH": "fixed_n0_zero",
            "rows": rows}
    (output / "point2_rotation_reduction_1809.01636.json").write_text(json.dumps(data, indent=2) + "\n")

    old = cache / "2012.15657v1_source/combine_arXiv.tex"
    new = next(cache.glob("2012.15657_*/combine_sub.tex"))
    versions = []
    for path, version in ((old, "2012.15657v1"), (new, "2012.15657v2")):
        text = path.read_text().splitlines()
        versions.append({"source": source(path, version, "Supplemental point table and D4 example"),
                         "even_rotation": line_containing(text, "$C_{2m}$&"),
                         "even_dihedral": line_containing(text, "$D_{2m}$&"),
                         "D4_spinless": line_containing(text, r"\mathcal{G}_{D_4,0}^{U(1)}=")})
    audit = {"audit_date": "2026-10-13", "versions": versions,
             "conclusion": "The even-cyclic printed answer is unchanged. Spinless even-dihedral answers changed between v1 and v2. No author-confirmed explanation of the remaining cyclic discrepancy was located.",
             "published_supplement": {"url": "https://journals.aps.org/prresearch/supplemental/10.1103/PhysRevResearch.4.033081/supplementarysub.pdf",
                                      "location": "Page 2, Eq (6) and Table I",
                                      "D4_spinless_orders": [4],
                                      "C2m_both_spins_orders": "[2m, 2m]",
                                      "D2m_spinless_orders": "[2m]",
                                      "inspection": "Web PDF text; direct filesystem download returned HTTP 403, so no local PDF hash is claimed."}}
    (output / "point2_source_version_audit.json").write_text(json.dumps(audit, indent=2) + "\n")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path("/home/arxiv"))
    parser.add_argument("--output", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    extract(args.cache, args.output)
