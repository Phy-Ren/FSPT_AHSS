"""Exact circle/carry, closed-charge, and relative E8 comparison maps.

This is a comparison interface, not a superconducting classifier. The same
G_f has quotients G=G_f/U(1)^f and G_b=G_f/Z2^f. X1 is the circle section
coordinate on G_b, with sign rho1. All other inputs are pulled back to
that same simplex. The E8 helpers supply the additional mixed correction
relative to a pure-CI map; that universal pure-CI terminal map is still
not supplied here.
"""
from fractions import Fraction

from . import api as ci
from ._engine import e8_4p1 as neutral


def circle_carry(symmetry: ci.Symmetry, X1: ci.Cochain) -> ci.Cochain:
    """Return integer M2=d_rho X1+2 omega_real on the circle quotient."""
    ci._exact(X1, 1)
    if X1.N != symmetry.s1.N or X1.tw != symmetry.omega2_real.tw:
        raise ValueError('The circle coordinate must have sign rho1 on the same simplex.')
    carry = X1.d() + symmetry.omega2_real.sc(2)
    ci._integer(carry)
    return carry


def parity_extension(symmetry: ci.Symmetry, X1: ci.Cochain) -> ci.Cochain:
    """Return M2 modulo two, with the binary coefficient system."""
    return ci.bin0(circle_carry(symmetry, X1))


def _charge_input(symmetry: ci.Symmetry, X1: ci.Cochain,
                  value: ci.Cochain) -> None:
    circle_carry(symmetry, X1)
    ci._exact(value)
    ci._integer(value)
    if value.N != X1.N or value.tw != symmetry.r1.tw:
        raise ValueError('The integer charge input must have sign r1 on the same simplex.')


def charge_phase_correction(symmetry: ci.Symmetry, X1: ci.Cochain,
                            n_p2: ci.Cochain) -> ci.Cochain:
    """R=X1 cup n_(p+2)/2, for the closed-charge comparison only.

For open charge, an additional X1 cup d_r(n_(p+2))/2 remains in the
source equation; silently applying this closed-sector map would lose it.
"""
    _charge_input(symmetry, X1, n_p2)
    if n_p2.d().maxabs():
        raise ValueError('The CF-only map requires closed charge; the CI-open remainder is nonzero.')
    return X1.cup(n_p2).sc(Fraction(1, 2))


def charge_gauge_phase(symmetry: ci.Symmetry, X1: ci.Cochain,
                       charge_parameter: ci.Cochain) -> ci.Cochain:
    """Primitive -X1 cup u/2 for the difference of the two short gauges."""
    _charge_input(symmetry, X1, charge_parameter)
    return X1.cup(charge_parameter).sc(Fraction(-1, 2))


def e8_ci_source_bridge_4p1(e2: ci.Cochain, n2: ci.Cochain) -> ci.Cochain:
    """Relative mixed R5=P(2n2,e2), with E8 first.

    The parity sheet changes from 2n2 to 2n2+16e2. This is the additional
    source rephasing after the pure-CI comparison, not that missing map.
    """
    neutral._closed_pair(e2, n2)
    return neutral.product(n2.sc(2), e2)


def e8_ci_product_bridge_4p1(e2: ci.Cochain, n2: ci.Cochain,
                            e2_prime: ci.Cochain, n2_prime: ci.Cochain) -> ci.Cochain:
    """Relative mixed K4, retaining the middle-factor exchange correction."""
    neutral._closed_pair(e2, n2)
    neutral._closed_pair(e2_prime, n2_prime)
    neutral._closed_pair(e2, e2_prime)
    a, b, e, f = n2.sc(2), n2_prime.sc(2), e2, e2_prime
    return (neutral.commutator(b, e)
            + neutral.associator(a, b, e) - neutral.associator(a, e, b)
            - neutral.associator(a + b, e, f) + neutral.associator(a + e, b, f))


def e8_ci_gauge_bridge_4p1(e2: ci.Cochain, n2: ci.Cochain,
                          e_parameter: ci.Cochain, n_parameter: ci.Cochain) -> ci.Cochain:
    """Relative mixed H4 from the fixed product prism, with E8-first inputs."""
    neutral.gauge(e2, e_parameter)
    neutral.gauge(n2, n_parameter)
    return neutral.pair_gauge(n2.sc(2), e2, n_parameter.sc(2), e_parameter)
