#!/usr/bin/env python3
"""Extract the version-of-record Table II independently from PDF glyph positions.

This is a reference audit, never a classification input. Requires PyMuPDF.
The hash and layout checks deliberately reject other PDF versions/layouts.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

PDF_SHA256 = "eda983b3c093877d7b6d34da1092ae8c8c5dc272746e6f4eaf28f35a7438c692"
NAMES = "C1 Ci C2 Cs C2h D2 C2v D2h C4 S4 C4h D4 C4v D2d D4h C3 C3i D3 C3v D3d C6 C3h C6h D6 C6v D3h D6h T Th Td O Oh".split()
CATALOG_INDEX = {name: index for index, name in enumerate(NAMES, 1)}
CATALOG_INDEX.update({"O": 30, "Td": 31})  # Table II and the geometry catalog order these oppositely.
FIELDS = ["block2_orders", "block1_orders", "block0_orders", "stacking_orders"]
BOUNDS = [99, 149, 197, 244, 320, 398, 446, 496, 568]


def extract(pdf: Path) -> dict:
    import pymupdf

    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    if digest != PDF_SHA256:
        raise ValueError(f"Unreviewed PDF SHA256: {digest}")
    document = pymupdf.open(pdf)
    page = document[4]
    if len(document) != 56 or "TABLE II." not in page.get_text():
        raise ValueError("Unexpected journal layout")
    lines = [line for block in page.get_text("dict")["blocks"] for line in block.get("lines", [])]
    labels = [line for line in lines if 51 < line["bbox"][0] < 53 and 138 < line["bbox"][1] < 511]
    if len(labels) != 32:
        raise ValueError(f"Expected 32 group rows, found {len(labels)}")
    chars = [char for block in page.get_text("rawdict")["blocks"] for line in block.get("lines", [])
             for span in line["spans"] for char in span["chars"]]
    rows = []
    for index, (name, label) in enumerate(zip(NAMES, labels), 1):
        baseline = label["spans"][0]["origin"][1]
        row_chars = [c for c in chars if baseline - 4 < c["origin"][1] < baseline + 4.5]
        cells = []
        for left, right in zip(BOUNDS, BOUNDS[1:]):
            cc = [c for c in row_chars if left <= c["origin"][0] < right]
            factors = []
            for z in [c for c in cc if c["c"] in ("Z", "ℤ")]:
                digits = [c for c in cc if c["c"].isdigit() and 3 < c["origin"][0] - z["origin"][0] < 10]
                subs = [c for c in digits if c["origin"][1] > z["origin"][1] + 0.5]
                supers = [c for c in digits if c["origin"][1] < z["origin"][1] - 0.5]
                if len(subs) != 1 or len(supers) > 1:
                    raise ValueError(f"Ambiguous factor: {name}, {left}, {digits}")
                order = int(subs[0]["c"])
                multiplicity = int(supers[0]["c"]) if supers else 1
                if order > 1:
                    factors.extend([order] * multiplicity)
            if not any(c["c"] in ("Z", "ℤ") for c in cc):
                raise ValueError(f"Empty cell: {name}, {left}")
            cells.append({"orders": factors, "pdf_bbox_points": [left, baseline - 9, right, baseline + 5]})
        for spin_number, spin in enumerate(("spinless", "spin_half")):
            selected = cells[spin_number * 4:spin_number * 4 + 4]
            rows.append({
                "id": f"point3_{CATALOG_INDEX[name]:02d}_{spin}", "name": name, "physical_spin": spin,
                "name_as_printed": "".join(s["text"] for s in label["spans"]).replace("¼", "="),
                **{key: cell["orders"] for key, cell in zip(FIELDS, selected)},
                "source_cells": {key: cell["pdf_bbox_points"] for key, cell in zip(FIELDS, selected)},
                "source_location": f"Table II, printed p.031029-5, row {index}, {spin} columns",
            })
    return {
        "source": {
            "version": "PRX version of record, published 2025-07-28",
            "authors": ["Jian-Hao Zhang", "Shang-Qiang Ning", "Yang Qi", "Zheng-Cheng Gu"],
            "title": "Construction and Classification of Crystalline Topological Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems",
            "doi": "10.1103/PhysRevX.15.031029",
            "url": "https://journals.aps.org/prx/pdf/10.1103/PhysRevX.15.031029",
            "pdf_sha256": digest, "pdf_pages": 56, "pdf_page_index": 4,
            "method": "Real-space topological crystals, no-open-edge conditions, bubble equivalence and stacking",
        },
        "extraction": "All 64 spin-specific groups and all 256 layer/full cells extracted from subscript/superscript glyph coordinates; table also visually inspected. No calculated classification enters extraction.",
        "rows": rows,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("pdf", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--arxiv-reference", type=Path)
    args = parser.parse_args()
    result = extract(args.pdf)
    if args.arxiv_reference:
        old = json.loads(args.arxiv_reference.read_text())
        if len(old["rows"]) != 64:
            raise ValueError("Expected 64 arXiv comparison rows")
        changes = []
        for current, previous in zip(result["rows"], old["rows"]):
            if current["physical_spin"] != previous["physical_spin"]:
                raise ValueError("Reference row order differs")
            for field in FIELDS:
                if sorted(current[field]) != sorted(previous[field]):
                    changes.append({"id": current["id"], "name": current["name"], "quantity": field,
                                    "arxiv_2024_v2": previous[field], "journal_2025": current[field],
                                    "arxiv_source_line": previous["source_line"],
                                    "journal_pdf_bbox_points": current["source_cells"][field]})
        result["arxiv_comparison"] = {
            "source": {**old["source"], "version": "arXiv:2204.13558v2, 2024-06-18"},
            "changed_full_cells": sum(c["quantity"] == "stacking_orders" for c in changes),
            "changed_layer_cells": sum(c["quantity"] != "stacking_orders" for c in changes),
            "changed_cells": changes,
        }
    args.output.write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"rows": len(result["rows"]), "version_changes": result.get("arxiv_comparison", {}).get("changed_cells", [])}, indent=2))


if __name__ == "__main__":
    main()
