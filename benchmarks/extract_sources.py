#!/usr/bin/env python3
"""Extract published insulator comparison data; never imported by the solver.

The rows retain exact TeX source cells, source line numbers and file hashes.
Integer lists describe direct cyclic factors, with zero denoting a free factor.
No entry is used as a symmetry input or as a calculated classification.
"""
from pathlib import Path
import argparse
import hashlib
import json
import re


def factors(tex):
    text = re.sub(r"\\color\{[^}]+\}", "", tex)
    text = text.replace(r"\mathbb{Z}", "Z").replace(r"\mathbb Z", "Z")
    result = []
    for match in re.finditer(r"(?:(\d+)\s*)?Z(?:_\{(\d+)\}|_(\d+))?(?:\^\{(\d+)\}|\^(\d+))?", text):
        prefix, braced_order, order, braced_power, power = match.groups()
        cyclic = int(braced_order or order or 0)
        multiplicity = int(braced_power or power or 1)
        # A leading coefficient 2Z is an embedded free charge lattice; it is
        # abstractly Z. A leading 3Z_2 denotes three finite direct factors.
        if cyclic:
            multiplicity *= int(prefix or 1)
        if cyclic != 1:
            result += [cyclic] * multiplicity
    return result


def source(path, arxiv, location):
    return {"arxiv": arxiv, "url": f"https://arxiv.org/abs/{arxiv}",
            "source_file": path.name, "source_sha256": hashlib.sha256(path.read_bytes()).hexdigest(),
            "location": location}


def raw_rows(path, start, end):
    return [(line_no, [x.strip() for x in line.strip().removesuffix(r"\\").split("&")])
            for line_no, line in enumerate(path.read_text().splitlines(), 1)
            if start <= line_no <= end and "&" in line and line.lstrip().startswith("$")]


def extract(cache, output):
    wq = next(cache.glob("2112.15533_*/U1f.tex"))
    z2 = next(cache.glob("2012.15657_*/combine_sub.tex"))
    z3 = next(cache.glob("2204.13558_*/main.tex"))
    # Section and table markers, rather than fixed offsets, identify the data;
    # recorded line numbers remain useful for auditing the current source.
    wlines = wq.read_text().splitlines()
    wstart = next(i for i, line in enumerate(wlines, 1) if r"\section{H. Examples" in line)
    batches = []
    current = []
    for n, line in enumerate(wlines, 1):
        if n < wstart:
            continue
        if r"\begin{tabularx}" in line:
            current = []
        elif r"\end{tabularx}" in line:
            batches.append(current)
        elif "&" in line and line.strip().startswith("p") or (n > wstart and "&" in line and line.strip().startswith("c")):
            current.append((n, [x.strip() for x in line.strip().removesuffix(r"\\").split("&")]))
    rows = []
    for spin, batch in zip(("spin_half", "spinless"), batches):
        for n, cells in batch:
            phase = cells[2].split(r"\rightarrow")
            rows.append({"name_as_printed": cells[0], "physical_spin": spin,
                         "charge_orders": factors(cells[1]), "phase_before_incoming_orders": factors(phase[0]),
                         "phase_after_incoming_orders": factors(phase[-1]),
                         "source_line": n, "source_cells": cells,
                         "comparison_type": "graded_charge_phase_layers",
                         "uniform_IQH": "fixed_n0_zero", "full_stacking_group_supplied": False})
    (output / "wallpaper_layers_2112.15533.json").write_text(json.dumps({
        "source": source(wq, "2112.15533", "Supplement H, the two wallpaper tables; duplicate TeX label tab:2dwallpaper"),
        "notation": "paper rho1 is circle automorphism = package rho1+s1",
        "rows": rows}, indent=2) + "\n")
    z2lines = z2.read_text().splitlines()
    z2end = next(i for i, line in enumerate(z2lines, 1) if r"\label{insulator U(1)}" in line)
    z2start = max(i for i, line in enumerate(z2lines, 1) if i < z2end and r"\begin{tabular}" in line)
    rows = []
    for n, cells in raw_rows(z2, z2start, z2end):
        if len(cells) != 3 or "G_b" in cells[0]:
            continue
        name = cells[0].replace("$", "").replace("~", "")
        for spin, cell in zip(("spinless", "spin_half"), cells[1:]):
            rows.append({"name": name, "physical_spin": spin, "stacking_orders": factors(cell),
                         "free_charge_step_as_printed": 2 if "2\\mathbb{Z}" in cell else 1,
                         "source_line": n, "source_cell": cell,
                         "comparison_type": "complete_stacking_within_nonchiral_SPT_sector",
                         "uniform_IQH": "fixed_n0_zero"})
    (output / "wallpaper_stacking_2012.15657.json").write_text(json.dumps({
        "source": source(z2, "2012.15657", "Main-text Table III, TeX label insulator U(1)"),
        "rows": rows}, indent=2) + "\n")
    rows = []
    # Supplemental Table point states the following formulas. Retain separately
    # from the accepted onsite C2 control: even cyclic rows conflict with Z4.
    for n in (1, 2, 3, 4, 6):
        for spin in ("spinless", "spin_half"):
            for kind in ("C", "D"):
                if kind == "C":
                    orders = [n, n] if n > 1 else []
                elif n % 2:
                    orders = [n] if n > 1 else []
                elif spin == "spinless":
                    orders = [2 * n]
                elif (n // 2) % 2:
                    orders = [n, 2]
                else:
                    orders = [n // 2, 2, 2]
                rows.append({"name_as_printed": f"{kind}{n}", "physical_spin": spin,
                             "stacking_orders_as_printed": orders, "uniform_IQH": "fixed_n0_zero",
                             "comparison_status": "source_discrepancy_requires_review" if kind == "C" and n % 2 == 0 else "source_statement",
                             "note": "D_n is the planar dihedral group of order 2n."})
    (output / "point2_stacking_2012.15657.json").write_text(json.dumps({
        "source": source(z2, "2012.15657", "Supplemental Table point (following D4 construction), currently lines 3547-3568"),
        "scope": "nonchiral SPT; retain published statements without replacing calculated answers",
        "discrepancy": "Table gives C2=Z2 x Z2; the onsite U(1)^f x C2 charge-decoration control in 2112.15533 gives Z4. No reconciliation assumed.",
        "rows": rows}, indent=2) + "\n")
    z3lines = z3.read_text().splitlines()
    z3end = next(i for i, line in enumerate(z3lines, 1) if r"\label{TI}" in line)
    z3start = max(i for i, line in enumerate(z3lines, 1) if i < z3end and r"\begin{tabular}" in line)
    rows = []
    for n, cells in raw_rows(z3, z3start, z3end):
        if len(cells) != 9:
            continue
        for offset, spin in ((1, "spinless"), (5, "spin_half")):
            rows.append({"name_as_printed": cells[0], "physical_spin": spin,
                         "block2_orders": factors(cells[offset]), "block1_orders": factors(cells[offset+1]),
                         "block0_orders": factors(cells[offset+2]), "stacking_orders": factors(cells[offset+3]),
                         "source_line": n, "source_cells": cells[offset:offset+4],
                         "includes_neutral_E8": True,
                         "comparison_type": "full_physical_result_requires_sector_projection"})
    (output / "point3_full_2204.13558.json").write_text(json.dumps({
        "source": source(z3, "2204.13558", "Table II, TeX label TI; independent E8 specified in introduction and block-state section"),
        "rows": rows}, indent=2) + "\n")
    assert len(rows) == 64


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cache", type=Path, default=Path("/home/arxiv"))
    parser.add_argument("--output", type=Path, default=Path(__file__).parent)
    args = parser.parse_args()
    extract(args.cache, args.output)
