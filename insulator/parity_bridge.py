"""Exact circle/carry and closed-charge comparison maps for U(1)^f states.

This is a comparison interface, not a superconducting classifier. The same
G_f has quotients G=G_f/U(1)^f and G_b=G_f/Z2^f. X1 is the circle section
coordinate on G_b, with sign rho1+s1. All other inputs are pulled back to
that same simplex. Nonzero CI-sheet terminal maps are not supplied here.
"""
from fractions import Fraction

from . import api as ci


def circle_carry(symmetry: ci.Symmetry, X1: ci.Cochain) -> ci.Cochain:
    """Return integer M2=d_(rho+s) X1+2 omega_real on the circle quotient."""
    ci._exact(X1, 1)
    if X1.N != symmetry.s1.N or X1.tw != symmetry.omega2_real.tw:
        raise ValueError('The circle coordinate must have sign rho1+s1 on the same simplex.')
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
    if value.N != X1.N or value.tw != symmetry.rho1.tw:
        raise ValueError('The integer charge input must have sign rho1 on the same simplex.')


def charge_phase_correction(symmetry: ci.Symmetry, X1: ci.Cochain,
                            n_p2: ci.Cochain) -> ci.Cochain:
    """R=X1 cup n_(p+2)/2, for the closed-charge comparison only.

For open charge, an additional X1 cup d_rho(n_(p+2))/2 remains in the
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
