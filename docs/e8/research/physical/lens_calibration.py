#!/usr/bin/env python3
"""Exact physical calibration, outside the production AHSS implementation.

Run: python lens_calibration.py
Requires SymPy (tested with 1.14.0). No floating point arithmetic is used.
State order everywhere is (e_p, n_p, n_{p+2}, nu_{p+3}), E8 first.
The geometric invariants below are NOT evaluations of the bare nu cochain.
"""

from __future__ import annotations

import json
from fractions import Fraction as Q
from math import gcd
from pathlib import Path

import sympy as sp


def mod1(value: Q) -> Q:
    return value % 1


def record(value: Q) -> dict[str, str]:
    return {"raw_rational": str(value), "mod_Z": str(mod1(value))}


def disk_integrals(order: int, representation_weight: int) -> dict[str, Q]:
    """W=D(O(-N)->CP2), complex orientation; E_s=O(s), boundary flat.

    The standard deck generator is z -> exp(2 pi i/N) z. In the explicit
    quotient (z,v)~(gz,rho_s(g)v), flat parallel transport is rho_s^{-1}.
    Hence holonomy a(g)=+1/N corresponds to s=-1.
    """
    N, s = order, representation_weight
    D = Q(-s**3, N)
    P = Q(-s * (N**2 + 3), N)
    C = (P - D) / 3
    return {
        "E8_X_geom_minus_C": -C,
        "DW_b_D": D,
        "C": C,
        "y_p1": P,
        "signature_APS_density": (4 * D + 2 * P) / 3,
        "spin_Dirac_APS_density": D / 6 - P / 24,
    }


def cyclotomic_eta(order: int, weight: int, operator: str) -> Q:
    """Gilkey1984 Lemma2.1 root-of-unity sum in Q[z]/Phi_N(z).

    Signature uses the FULL tangential signature complex and reduced eta.
    For odd N the spin lift is the unique order-N lift; sqrt(z)=z^((N+1)/2).
    The answer must simplify to a rational number, checked rather than assumed.
    """
    N = order
    z = sp.Symbol("z")
    cyclotomic = sp.cyclotomic_poly(N, z)

    def rem(poly):
        return sp.rem(poly, cyclotomic, z)

    total = sp.Integer(0)
    for k in range(1, N):
        eigenvalue = rem(z**k)
        if operator == "signature":
            numerator = rem(z ** ((k * weight) % N) * (eigenvalue + 1) ** 3)
        elif operator == "spin_Dirac":
            assert N % 2 == 1, "This test uses only the unique odd-order spin lift."
            exponent = k * (weight + 3 * (N + 1) // 2)
            numerator = rem(z ** (exponent % N))
        else:
            raise ValueError(operator)
        denominator = rem((eigenvalue - 1) ** 3)
        total = rem(total + numerator * sp.invert(denominator, cyclotomic, z))
    answer = sp.cancel(total / N)
    assert answer.is_Rational, (N, weight, operator, answer)
    return Q(int(answer.p), int(answer.q))


def run_checks() -> dict:
    cyclic = []
    eta_checks = []
    for N in (2, 3, 4, 5, 6, 9, 12):
        geometric = disk_integrals(N, -1)
        E8_lens = geometric["E8_X_geom_minus_C"]
        b_lens = geometric["DW_b_D"]
        # The second background is CP2 x S1, flat holonomy +1/N.
        E8_product, b_product = Q(-1, N), Q(0)
        q_integer = N * (1 - N**2) // 3
        assert 3 * q_integer == N * (1 - N**2)
        q_mod_N = q_integer % N
        for E8_period, b_period in ((E8_lens, b_lens), (E8_product, b_product)):
            assert mod1(N * E8_period - q_mod_N * b_period) == 0
            assert mod1(N * b_period) == 0
        # Each canonical representative has E8 coordinate first, then DW phase.
        detections = {
            (mod1(e * E8_lens + k * b_lens), mod1(e * E8_product + k * b_product))
            for e in range(N)
            for k in range(N)
        }
        assert len(detections) == N * N
        divisor = gcd(N, q_mod_N)
        cyclic.append({
            "N": N,
            "scope": "reduced oriented bosonic E8-decoration plus DW phase subgroup",
            "generator_order": ["E8_X_geom", "DW_b"],
            "E8_X_lens": record(E8_lens),
            "E8_X_CP2_times_S1": record(E8_product),
            "DW_b_lens": record(b_lens),
            "DW_b_CP2_times_S1": record(b_product),
            "relation_N_X_equals_q_b": q_mod_N,
            "presentation_E8_first": [[N, -q_mod_N], [0, N]],
            "invariant_factors": [v for v in (divisor, N * N // divisor) if v != 1],
            "distinct_two_manifold_detections": len(detections),
        })
        for s in (-1, 0, 1):
            geometric_s = disk_integrals(N, s)
            for operator, density in (
                ("signature", "signature_APS_density"),
                *(([("spin_Dirac", "spin_Dirac_APS_density")]) if N % 2 else []),
            ):
                actual = cyclotomic_eta(N, s, operator)
                predicted = geometric_s[density]
                difference = actual - predicted
                assert difference.denominator == 1, (N, s, operator, actual, predicted)
                eta_checks.append({
                    "N": N,
                    "representation_weight_s": s,
                    "parallel_transport_holonomy": str(Q(-s, N) % 1),
                    "operator": operator,
                    "exact_cyclotomic_sum": record(actual),
                    "relative_characteristic_integral": record(predicted),
                    "integer_difference": int(difference),
                    "equal_mod_Z": True,
                })

    c3 = disk_integrals(3, -1)
    X, b = c3["E8_X_geom_minus_C"], c3["DW_b_D"]
    eta_inverse_stz = cyclotomic_eta(3, -1, "signature")
    eta_stz = cyclotomic_eta(3, 1, "signature")
    I = c3["spin_Dirac_APS_density"]
    assert mod1(X) == Q(7, 9)
    assert mod1(b) == Q(1, 3)
    assert eta_stz == Q(-1, 9)
    assert eta_inverse_stz == Q(1, 9)
    assert mod1(3 * X - b) == 0
    assert mod1(eta_inverse_stz - 4 * X) == 0
    assert mod1(eta_inverse_stz - X - b) == 0
    assert mod1(I) == Q(8, 9)
    assert mod1(3 * I - 2 * b) == 0
    assert mod1(3 * (X + I)) == 0

    # An interacting crystalline control from Ning-Mao-Li-Wang2021 SecIII.B.1.
    # Physical roots: neutral E8 first, electronic IQH second, nonchiral root third.
    # Record the invariant arguments in turns, i.e. eta=exp(2 pi i argument).
    def mirror_indicators(e8: int, iqh: int, nonchiral: int):
        return (mod1(Q(e8, 2)), mod1(Q(iqh - 2 * nonchiral, 8)))

    assert mirror_indicators(2, 0, 0) == (0, 0)
    assert mirror_indicators(0, 2, 1) == (0, 0)
    assert mirror_indicators(0, 0, 4) == (0, 0)
    mirror_values = {mirror_indicators(e, n, k) for e in range(2) for n in range(2) for k in range(4)}
    assert len(mirror_values) == 16
    assert mirror_indicators(1, 0, 0) == (Q(1, 2), 0)

    return {
        "status": "all_assertions_passed",
        "state_notation_E8_first": ["e_p", "n_p", "n_{p+2}", "nu_{p+3}"],
        "p": "d-2, with d the spatial dimension",
        "physical_response_warning": "These are differential-character/APS response evaluations, not bare nu cochain periods.",
        "orientation": "W_N=D(O(-N)->CP2) complex orientation; boundary standard quotient orientation",
        "flat_line_convention": "(z,v)~(g z,rho_s(g)v); parallel transport rho_s^{-1}; a(g)=+1/N means s=-1",
        "cyclic_controls": cyclic,
        "eta_comparisons": eta_checks,
        "eta_comparison_count": len(eta_checks),
        "C3_dictionary": {
            "E8_X_geom_minus_C": record(X),
            "E8_X_eta_equal_X_geom_plus_b": record(eta_inverse_stz),
            "charged_I_spin_restriction": record(I),
            "DW_b": record(b),
            "STZ_rho_1_signature_eta": record(eta_stz),
            "generator_change": "x X_eta + k b = x X_geom + (k+x) b",
            "relations": ["3 X_geom = b", "X_eta = 4 X_geom = X_geom+b", "3 I = 2 b", "3 (X_geom+I) = 0"],
            "charged_scope": "spin background, trivial electromagnetic Spin-c determinant, flat C3 line; not a complete charged bordism calibration",
        },
        "electronic_embedding_of_generated_neutral_subgroup": {
            "symmetry": "split U1f x C_N, tangential/background structure Spin-c x BC_N",
            "lens_Spin_c_determinant": "restriction of (3-N)h from the complex disk bundle W_N",
            "CP2_times_S1_Spin_c_determinant": "h, reducing to w2 modulo2",
            "claim": "the same two-manifold periods distinguish all N^2 generated neutral/DW classes after electronic pullback",
            "proof": "eta_dictionary.md section5; neutral responses ignore the chosen electromagnetic determinant connection",
            "limitation": "no quotient declaring electromagnetic or intrinsic invertible responses trivial; no claim to classify all charged phases",
        },
        "mirror_interacting_control": {
            "symmetry": "physical unitary mirror commuting with U1f; mirror-plane U1f x Z2; charge-conserving fermions",
            "state_order": ["neutral_E8", "electronic_IQH", "nonchiral_Z4_root"],
            "detector_order": ["eta_2f_neutral_E8", "eta_1f_other_roots"],
            "distinct_detector_pairs": len(mirror_values),
            "full_interacting_group": [2, 8],
            "neutral_E8_detector_arguments": ["1/2", "0"],
            "source": "Ning, Mao, Li, Wang, arXiv:2105.02682v1 SecIII.B.1 Eqs19-20; PRB104075111(2021)",
            "scope": "independent source relation/detector arithmetic; not a production solver run or an arbitrary space-group completeness proof",
        },
    }


if __name__ == "__main__":
    result = run_checks()
    mirror = result.pop("mirror_interacting_control")
    result["spacetime_dimension"] = "4+1D"
    result["spatial_dimension"] = 4
    result["state_notation"] = ["e_2", "n_2", "n_4", "nu_5"]
    output = Path(__file__).with_name("calibration_4p1.json")
    output.write_text(json.dumps(result, indent=2) + "\n")
    mirror_output = Path(__file__).with_name("mirror_3p1_checks.json")
    mirror_output.write_text(json.dumps({
        "status": "all_source_relation_and_detector_assertions_passed",
        "spacetime_dimension": "3+1D",
        "spatial_dimension": 3,
        "state_notation_E8_first": ["e_1", "n_1", "n_3", "nu_4"],
        "mirror_interacting_control": mirror,
    }, indent=2) + "\n")
    coefficient_output = Path(__file__).with_name("coefficient_2p1_reference.json")
    coefficient_output.write_text(json.dumps({
        "status": "primary_source_coefficient_dictionary",
        "spacetime_dimension": "2+1D",
        "spatial_dimension": 2,
        "state_notation_E8_first": ["e_0", "n_0", "n_2", "nu_3"],
        "coefficient_order_E8_first": ["e_0", "n_0"],
        "neutral_E8": {"chiral_central_charge": 8, "Hall_conductance": 0},
        "electronic_IQH": {"chiral_central_charge": 1, "Hall_conductance": 1},
        "response_dictionary": {"chiral_central_charge": "8 e_0+n_0", "Hall_conductance": "n_0"},
        "inverse_dictionary": {"e_0": "(c-sigma_H)/8", "n_0": "sigma_H"},
        "source": "Ning, Mao, Li, Wang, arXiv:2105.02682v1 SecIII.B.1 roots(i)-(ii), source lines494-502",
        "scope": "uniform charge-conserving invertible coefficient lattice; not a wallpaper classification or a production solver calculation",
    }, indent=2) + "\n")
    print(json.dumps({
        "status": result["status"],
        "exact_eta_comparisons": result["eta_comparison_count"],
        "cyclic_two_manifold_controls": len(result["cyclic_controls"]),
        "C3_E8_X_geom_mod_Z": result["C3_dictionary"]["E8_X_geom_minus_C"]["mod_Z"],
        "C3_E8_X_eta_mod_Z": result["C3_dictionary"]["E8_X_eta_equal_X_geom_plus_b"]["mod_Z"],
        "output_4p1": str(output),
        "output_3p1": str(mirror_output),
        "output_2p1": str(coefficient_output),
    }, indent=2))
