#!/usr/bin/env python3
"""Transcribe Class A phase-homology tables from pinned arXiv:2102.02941v3.

This reference-only script does not read classification outputs. Formula
transcription is explicit and source hashes prevent silent version changes.
It does not infer an E8 projection from abstract invariant factors.
"""
import argparse
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from benchmarks.compare import group_signature

HASHES = {
    "cyclic.tex": "f7c48f8ac882841a4deff8fa6997b4f0891c43c4a92aa417f0a7e298c75e8d15",
    "spinc_rotation.tex": "9feecd5aef6e761aa06976eba047c91414641d5df471763dff65787a507f9766",
    "dihedral.tex": "5f9c2d2a50a2223a6741a96f5c34cc8b759ebb5ab537d550f412adda9f9341f8",
    "para_n_gonal.tex": "771404e4a3389d1284998cbfb8f3b671ed0224b56d28abf9f91326ffc0fbfa1f",
    "pin_reflection.tex": "8e4470ba32e4ab31a57183b8504a3a54db2966f32cf74a46ed878aaf21a57e65",
    "inversion.tex": "2e80b964f34f0902342fa82d70e1f22929000714aaca59f7718171fe54d198c1",
    "tet_oct_icos_generalities.tex": "2f53ce2fb93f4c8176062b8c6a44fdb8c7ef5aced1f89e140afe6094d54d71df",
}
POINT2 = "C1 C2 Cs C2v C4 C4v C3 C3v C6 C6v".split()
POINT3 = "C1 Ci C2 Cs C2h D2 C2v D2h C4 S4 C4h D4 C4v D2d D4h C3 C3i D3 C3v D3d C6 C3h C6h D6 C6v D3h D6h T Th O Td Oh".split()
SPINS = ("spinless", "spin_half")


def cyclic_torsion(n):
    return [2 * n, n // 2] if n % 2 == 0 else [n, n]


def planar_dihedral_torsion(n, spin):
    if n % 2:
        return [n]
    if spin == "spinless":
        return [2 * n]
    return [n // 2, 2, 2] if n % 4 == 0 else [n, 2]


def pyramidal_torsion(n, spin):
    if n % 2:
        return [8, 2]
    return [2] * 4 if spin == "spinless" else [8, 4, 2]


def rotation_dihedral_torsion(n, spin):
    if spin == "spinless" or n % 2:
        return []
    return [2] * (2 if n % 4 == 0 else 3)


def make_rows():
    rows = []

    def add(d, name, spin, orders, source_file, location, geometry, formula):
        catalog = POINT2 if d == 2 else POINT3
        full = group_signature(orders)
        row = {
            "id": f"point{d}_{catalog.index(name) + 1:02d}_{spin}",
            "family": f"point{d}", "name": name, "physical_spin": spin,
            "spatial_dimension": d, "fullPhysical": full,
            "source_file": source_file, "source_location": location,
            "source_formula": formula, "spatial_action": geometry,
            "sector": "full_interacting_invertible_phase_homology",
        }
        if d == 2:
            # For cyclic rotations the full intrinsic response has rank two.
            # Restriction to the trivial group is onto that response lattice;
            # its finite kernel is precisely the displayed torsion subgroup.
            row["relativeN0E0Zero"] = group_signature(full["torsion"])
            row["allN0WithE0Zero"] = group_signature(full["torsion"] + [0] * (full["freeRank"] // 2))
            row["restriction_argument"] = (
                "For cyclic rotations, forgetting rotation restricts onto the two-integer "
                "intrinsic electronic response lattice; the finite kernel is the torsion "
                "subgroup. Setting e0=0 retains one free response integer. For reflection "
                "groups both uniform responses vanish. These are abstract subgroup types, "
                "not a dictionary for the solver's primitive roots or product convention."
            )
        else:
            proper = name in {"C1", "C2", "C3", "C4", "C6", "D2", "D3", "D4", "D6", "T", "O"}
            row["retainedComparison"] = full if proper else None
            row["retainedComparisonScope"] = (
                "proper_rotation_full_reference; physical dictionary still required" if proper else
                "not_projected: no named E8 embedding extracted from this source"
            )
        rows.append(row)

    for spin in SPINS:
        for n in (1, 2, 3, 4, 6):
            name = f"C{n}"
            formula = "Z^2 + Z_(2n) + Z_(n/2) for even n; Z^2 + Z_n^2 for odd n"
            add(2, name, spin, [0, 0] + cyclic_torsion(n), "cyclic.tex",
                "Table 3, p.33; Sec.4.3.3, Theorem 4.14", "rotation in the plane", formula)
            add(3, name, spin, [], "cyclic.tex", "Table 3, p.33, d=3",
                "rotation about a fixed axis", "0 for every n")
        add(2, "Cs", spin, [], "pin_reflection.tex", "Table 1, p.29, d=2",
            "one planar reflection", "0")
        add(3, "Cs", spin, [8, 2], "pin_reflection.tex", "Table 1, p.29, d=3",
            "one mirror plane", "Z_8 + Z_2")
        add(3, "Ci", spin, [8, 2], "inversion.tex", "Table 2, p.31, d=3",
            "inversion of all three coordinates", "Z_8 + Z_2")
        for n in (2, 3, 4, 6):
            add(2, f"C{n}v", spin, planar_dihedral_torsion(n, spin), "dihedral.tex",
                "Table 4, p.36, d=2; Secs.4.4.3-4.4.4", "planar D_(2n), order 2n",
                "spinless: Z_(2n) for even n, Z_n for odd n; spin-half: Z_(n/2)+Z_2^2 if n=0 mod4, Z_n+Z_2 if n=2 mod4, Z_n for odd n")
            add(3, f"C{n}v", spin, pyramidal_torsion(n, spin), "dihedral.tex",
                "Table 4, p.36, d=3", "planar rotations/reflections with a fixed third coordinate",
                "odd n: Z_8+Z_2; even n spinless: Z_2^4; even n spin-half: Z_8+Z_4+Z_2")
            add(3, f"D{n}", spin, rotation_dihedral_torsion(n, spin), "para_n_gonal.tex",
                "Table 5, p.52; Sec.4.5.4 (spin-half)", "proper dihedral rotations on R^3, order 2n",
                "spinless:0; spin-half:0 for odd n, Z_2^3 if n=2 mod4, Z_2^2 if n=0 mod4")
        sporadic = {"T": [], "Th": [4, 2, 2, 2] if spin == "spinless" else [8, 2, 2, 2],
                    "Td": [2, 2, 2, 2] if spin == "spinless" else [8, 2, 2],
                    "O": [] if spin == "spinless" else [2],
                    "Oh": [4, 2, 2, 2, 2] if spin == "spinless" else [8, 4, 2, 2, 2, 2]}
        for name, orders in sporadic.items():
            add(3, name, spin, orders, "tet_oct_icos_generalities.tex", "Table 6, p.60; Secs.5.1-5.5",
                "standard three-dimensional point-group representation", str(orders))
    assert len(rows) == 60 and len({r["id"] for r in rows}) == 60
    return sorted(rows, key=lambda r: (r["spatial_dimension"], int(r["id"].split("_")[1]), SPINS.index(r["physical_spin"])))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("/home/arxiv/2102.02941v3_verified"))
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    for name, expected in HASHES.items():
        actual = hashlib.sha256((args.source / name).read_bytes()).hexdigest()
        if actual != expected:
            raise ValueError(f"Source version changed: {name}: {actual}")
    data = {
        "source": {"author": "Arun Debray", "title": "Invertible phases for mixed spatial symmetries and the fermionic crystalline equivalence principle",
                   "url": "https://arxiv.org/abs/2102.02941v3", "version": "v3, 2026-02-03", "first_version": "2021-02-05",
                   "source_url": "https://arxiv.org/src/2102.02941v3",
                   "source_archive_sha256": "0e015df95d1b6fb9ac405446ed4edc7f9e843999c551ed81b15a9126412eb9ad",
                   "files_sha256": HASHES, "method": "Spin-c/Pin-c bordism, Adams spectral sequences, Anderson-dual equivariant phase homology",
                   "scope": "Interacting Class A only, under the generalized-homology ansatz. Class D columns are not extracted. Includes independent intrinsic responses and neutral bosonic contributions.",
                   "independence_limit": "Different mathematical method; v3 explicitly acknowledges revisions following comparison with Zhang-Ning-Qi-Gu2025. Not blind independence of the final tables."},
        "limits": ["No full physical-to-solver generator dictionary is asserted.",
                   "No improper 3D E8 quotient is inferred from abstract factor multiplicities.",
                   "Cyclic n=1 is a specialization of the source's general formula.",
                   "A torsion bordism character and a free-response integer arise from different parts of the Anderson-dual universal coefficient sequence; raw bordism groups are not copied as phase groups."],
        "rows": make_rows(),
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2) + "\n")
    print(json.dumps({"source": data["source"]["version"], "planar_cases": 20, "spatial3_cases": 40,
                      "proper3_direct_comparisons": 22, "improper3_unprojected": 18}))


if __name__ == "__main__":
    main()
