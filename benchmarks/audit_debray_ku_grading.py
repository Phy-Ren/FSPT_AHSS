#!/usr/bin/env python3
"""Audit one printed bordism derivation using the cited connective-ku splitting.

No AHSS classification output or implementation is read. This checks degree
counts in known direct-sum formulas; it does not prove the cited splitting.
"""
import argparse
import hashlib
import json
from pathlib import Path


def group(free=0, torsion=()):
    return {"freeRank": free, "torsion": sorted(torsion)}


def plus(*groups):
    return group(sum(g["freeRank"] for g in groups),
                 [v for g in groups for v in g["torsion"]])


def reduced_ku_bc2(k):
    return group(torsion=[2 ** ((k + 1) // 2)]) if k > 0 and k % 2 else group()


def monomials(k):
    # Sigma^2 HF2[u,v], |u|=|v|=2: 2+2a+2b=k.
    return [[a, b] for a in range(max(k, 0) + 1)
            for b in range(max(k, 0) + 1) if 2 + 2 * a + 2 * b == k]


def ku_bv4(k):
    if k < 0:
        return group()
    return plus(group(int(k % 2 == 0)), reduced_ku_bc2(k), reduced_ku_bc2(k),
                reduced_ku_bc2(k - 2), group(torsion=[2] * len(monomials(k))))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("/home/arxiv/2102.02941v3_verified"))
    parser.add_argument("--primary", type=Path,
                        default=Path("/home/arxiv/1008.0166_Ossa's_Theorem_via_the_Kunneth_formula/main.tex"))
    parser.add_argument("--output", type=Path,
                        default=Path(__file__).resolve().parents[1] /
                        "results/foundation_review_20261014/diagnostics/debray_d2_ku_grading_audit.json")
    args = parser.parse_args()
    source_names = ["para_n_gonal.tex", "spinc_mixed_dih_2mod4.tex", "sseq_summary.tex"]
    hashes = {n: hashlib.sha256((args.source / n).read_bytes()).hexdigest() for n in source_names}
    assert hashes["para_n_gonal.tex"] == "771404e4a3389d1284998cbfb8f3b671ed0224b56d28abf9f91326ffc0fbfa1f"
    source = (args.source / "spinc_mixed_dih_2mod4.tex").read_text()
    assert r"\abs u = \abs v = 2" in source
    primary = args.primary.read_text()
    assert r"\label{2.12}" in primary and "2a+2i+2j-2" in primary
    printed = [group(1), group(torsion=[2, 2]), group(1, [2]),
               group(torsion=[2, 2, 2, 4, 4]), group(2, [2, 2, 2]),
               group(torsion=[2] * 6 + [4, 8, 8]), group(2, [2] * 6)]
    rows = []
    for k in range(7):
        actual = plus(ku_bv4(k), ku_bv4(k - 4))
        # Independent indexing of Theorem 2.12 at p=2, i,j>0.
        pairs = [[i, j] for i in range(1, k + 2) for j in range(1, k + 2)
                 if 2 * i + 2 * j - 2 == k]
        assert len(pairs) == len(monomials(k))
        rows.append({"degree": k, "em_monomial_exponents": monomials(k),
                     "primary_theorem_positive_index_pairs": pairs,
                     "em_rank": len(pairs),
                     "printed_proof_em_rank": k - 1 if k >= 2 else 0,
                     "ku_BV4": ku_bv4(k), "shifted_ku_for_spinc": ku_bv4(k - 4),
                     "derived_spinc_BV4": actual, "printed_theorem_4_82_n2": printed[k],
                     "equal": actual == printed[k]})
    assert [r["degree"] for r in rows if not r["equal"]] == [3, 4, 5, 6]
    assert rows[4]["derived_spinc_BV4"] == group(2, [2, 2])
    assert rows[5]["derived_spinc_BV4"]["freeRank"] == 0
    out = {
        "audit_date": "2026-10-14",
        "status": "printed_derivation_grading_inconsistency_confirmed",
        "scope": "Specific degree-count audit of Debray v3 Theorem4.82, p57, using Eq4.59, p49 and an independent primary ku theorem. Not a formal erratum or a proof of every physical comparison.",
        "debray": {"url": "https://arxiv.org/abs/2102.02941v3", "files_sha256": hashes,
                   "printed_phase_group": group(torsion=[2, 2, 2])},
        "independent_primary": {"authors": "Robert Bruner, Khairia Mira, Laura Stanley, Victor Snaith",
                                "title": "Ossa's Theorem via the Kunneth formula",
                                "url": "https://arxiv.org/abs/1008.0166", "location": "Theorem2.12, p=2",
                                "tex_sha256": hashlib.sha256(args.primary.read_bytes()).hexdigest()},
        "mathematical_inputs": [
            "Stable splitting BV4_+ = S wedge BC2 wedge BC2 wedge (BC2 smash BC2).",
            "Reduced ku_(2j)(BC2)=0 and reduced ku_(2j+1)(BC2)=Z/(2^(j+1)), j>=0.",
            "ku smash BC2 smash BC2 = (ku smash Sigma^2 BC2) wedge Sigma^2 H(F2[u,v]), |u|=|v|=2.",
            "Low-degree ABP comparison Omega^SpinC_k(X)=ku_k(X)+ku_(k-4)(X), k<=7, at2; BV4 has no odd-primary reduced contribution.",
            "Anderson dual degree5: Ext(Omega4,Z) plus Hom(Omega5,Z); Omega5 is torsion."],
        "derived_3plus1_phase_group": group(torsion=[2, 2]),
        "rows": rows,
        "no_classifier_data_read": True, "no_printed_fixture_changed": True,
    }
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(out, indent=2) + "\n")
    print(json.dumps({"status": out["status"], "degrees_checked": 7,
                      "derived_phase_group": out["derived_3plus1_phase_group"]}))


if __name__ == "__main__":
    main()
