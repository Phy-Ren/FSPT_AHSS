#!/usr/bin/env python3
"""Compare saved 2D model groups to response-defined subgroups of PRB 109, 035168.

This is an independent reference audit, not a solver input or a cochain map.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmarks.compare import group_signature


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path(
        "/home/arxiv/2309.12389_Characterization_and_classification_of_i/main.tex"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    source = args.source.read_text()
    table = source[source.index("\\begin{tabular}{l|l|l|"):
                   source.index("\\label{tab:Classif_Summary}")]
    factors = {1: [], 2: [4, 4, 4, 2], 3: [3] * 5,
               4: [8, 4, 4, 2], 6: [12, 6, 3]}
    table_rows = {}
    for line in table.splitlines():
        pieces = line.strip().split("&")
        if len(pieces) > 2 and pieces[0].strip().isdigit():
            table_rows[int(pieces[0].strip())] = pieces[2].strip()
    assert set(table_rows) == set(factors)
    expected_cells = {
        1: r"$\Z^3$", 2: r"$\Z^3\times\Z_4^3\times\Z_2$",
        3: r"$\Z^3\times\Z_3^5$",
        4: r"$\Z^3\times\Z_8\times\Z_4^2\times\Z_2$",
        6: r"$\Z^3\times\Z_{12}\times\Z_6\times\Z_3$"}
    assert table_rows == expected_cells, "Primary table changed; audit before reuse"
    saved = ROOT / "results/two_dimensional_20261013/results.json"
    rows = []
    for result in json.loads(saved.read_text()):
        info, classification = result["input"], result["classification"]
        if info["family"] != "wallpaper" or info["name"] not in ("p1", "p2", "p3", "p4", "p6"):
            continue
        order = int(info["name"][1:])
        relative = classification["relativeUniformIQH0"]
        actual_relative = group_signature(relative["torsion"] + [0] * relative["freeRank"])
        actual_full = group_signature(classification["torsion"] + [0] * classification["freeRank"])
        expected_relative = group_signature(factors[order] + [0])
        expected_restricted = group_signature(factors[order] + [0, 0])
        rows.append({"id": info["id"], "name": info["name"], "physicalSpin": info["spin"],
                     "relativeModel": actual_relative,
                     "referenceC0CentralCharge0": expected_relative,
                     "relativeAbstractGroupMatch": actual_relative == expected_relative,
                     "allN0Model": actual_full,
                     "referenceK1Zero": expected_restricted,
                     "allN0AbstractGroupMatch": actual_full == expected_restricted,
                     "fullPhysicalReference": group_signature(factors[order] + [0, 0, 0]),
                     "sourceTableCell": table_rows[order],
                     "physicalCochainProductCalibrated": False})
    assert len(rows) == 10
    assert all(row["relativeAbstractGroupMatch"] and row["allN0AbstractGroupMatch"] for row in rows)
    audit = {"source": {"authors": ["Naren Manjunath", "Vladimir Calvera", "Maissam Barkeshli"],
                        "arxiv": "2309.12389v1", "journal": "Physical Review B 109, 035168 (2024)",
                        "url": "https://doi.org/10.1103/PhysRevB.109.035168",
                        "sourceSHA256": hashlib.sha256(args.source.read_bytes()).hexdigest(),
                        "locations": ["Table I", "Sec. III, common invariants and M=4 classification",
                                      "Source labels eq:FTresult_C1, eq:FTresult_C4, tab:indep_invts"]},
             "savedResultsSHA256": hashlib.sha256(saved.read_bytes()).hexdigest(),
             "responseDictionary": {"C": "n0", "c_minus": "n0 + 8 e0", "k1": "-e0",
                                    "fillingAtZeroFlux": "kappa"},
             "sectorDefinitions": {"relative": "C=c_minus=0, equivalently n0=e0=0",
                                   "currentAllN0Model": "e0=0, equivalently k1=0 and C=c_minus",
                                   "fullPhysicalReference": "independent c_minus,k1,kappa plus torsion"},
             "spinConvention": "The source uses C_M^M=1 and explicitly defines C_M^- = exp(i pi Q/M) C_M^+, whose Mth power is fermion parity. For orientation-preserving pM this charge redefinition identifies abstract symmetry groups; response-coordinate matching still needs this operator choice.",
             "limit": "Only response-defined abstract subgroup types are compared. No map from stored native roots to all source response invariants, nor a universal physical calibration of the nonzero-n0 cochain product, is established by this audit.",
             "rows": rows}
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(audit, indent=2) + "\n")
    print(json.dumps({"cases": len(rows), "relativeGroupMatches": len(rows),
                      "allN0RestrictedGroupMatches": len(rows), "physicalProductCalibration": "pending"}))


if __name__ == "__main__":
    main()
