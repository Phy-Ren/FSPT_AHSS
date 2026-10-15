#!/usr/bin/env python3
"""Extract only the neutral E8 column of Song-Xiong-Huang Table II.

This is a bosonic coefficient-sector reference, not a full interacting
electronic classification. The classifier never imports this fixture.
"""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import re


def extract(path):
    raw = path.read_bytes()
    text = raw.decode()
    start = text.index(r"\label{table:H1}")
    stop = text.index(r"\caption{List of 58 magnetic", start)
    rows = []
    for line_number, line in enumerate(text.splitlines(), 1):
        if not re.match(r"\s*\d+\s*&", line):
            continue
        offset = sum(len(x) + 1 for x in text.splitlines()[:line_number - 1])
        if not start < offset < stop:
            continue
        cells = line.split("&")
        if len(cells) != 5:
            raise ValueError("Unexpected number of source-table columns")
        number = int(cells[0].strip())
        cell = cells[3].strip()
        normalized = cell.replace(r"\mathbb{Z}", "Z")
        normalized = normalized.replace(r"\times", "*")
        normalized = re.sub(r"[\s${}]", "", normalized)
        allowed = {"": (0, []), "Z": (1, []), "Z^3": (3, []),
                   "Z_2": (0, [2]), "Z_2*Z": (1, [2]),
                   "Z_2*Z^3": (3, [2])}
        if normalized not in allowed:
            raise ValueError("Unrecognized neutral group: " + cell)
        free, torsion = allowed[normalized]
        rows.append({"spaceGroupNumber": number,
                     "symbolTeX": cells[1].strip().strip("$"),
                     "neutralE8": {"freeRank": free, "torsion": torsion},
                     "sourceCellTeX": cell, "sourceLine": line_number})
    if [row["spaceGroupNumber"] for row in rows] != list(range(1, 231)):
        raise ValueError("Expected exactly the ordered 230 space groups")
    return {"source": {
        "authors": ["Hao Song", "Charles Zhaoxi Xiong", "Sheng-Jie Huang"],
        "title": "Bosonic Crystalline Symmetry Protected Topological Phases Beyond the Group Cohomology Proposal",
        "arxiv": "1811.06558v1", "arxiv_date": "2018-11-15",
        "url": "https://arxiv.org/abs/1811.06558v1",
        "journal": "Physical Review B 101, 165129 (2020)",
        "doi": "10.1103/PhysRevB.101.165129",
        "method": "Interacting bosonic cellular E8 construction and signed integral H1; Appendix A signed-H1 theorem and Table II, fourth column.",
        "scope": "Neutral E8 decoration H1(G,Z_orientation) only. Not the full electronic stacking group.",
        "sourceFile": path.name,
        "sourceSHA256": hashlib.sha256(raw).hexdigest()}, "rows": rows}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    data = extract(args.source)
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print("Extracted", len(data["rows"]), "neutral E8 reference entries")


if __name__ == "__main__":
    main()
