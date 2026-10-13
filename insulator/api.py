"""Current calibrated Chern-insulator cochains (consolidated reference edition).

All values are exact integers or fractions.Fraction. Public names follow the
reader's notation. The packaged kernels use the sole calibrated sheet-linear convention.
No external checkout or historical formula variant is loaded.

Cochains are local arrays on a single ordered simplex, not a global GAP solver.
Background characters carry their own sign system, as in the supplied backend.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from typing import Optional

from ._engine.simplex import C as Cochain, bin0, char, halves, word, cartan31, cartan32, background, Fopen
from ._engine import calibrated as _cal
from ._engine.product4d import E4d_integer as _E4, lower_gauge as _gauge4


def _exact(cochain: Cochain, degree: Optional[int] = None) -> None:
    if not isinstance(cochain, Cochain):
        raise TypeError('Expected a local simplex Cochain.')
    if degree is not None and cochain.p != degree:
        raise ValueError(f'Expected cochain degree {degree}; received {cochain.p}.')
    if not isinstance(cochain.N, int) or not isinstance(cochain.p, int) or cochain.N < 0 or cochain.p < 0:
        raise ValueError('Simplex dimension and cochain degree must be nonnegative integers.')
    for face in cochain.v:
        if (len(face) != cochain.p + 1 or tuple(sorted(set(face))) != tuple(face)
                or any(not isinstance(j, int) or not 0 <= j <= cochain.N for j in face)):
            raise ValueError('Cochain face indices must be strictly increasing and inside the simplex.')
    if len(cochain.tw) != cochain.N + 1 or any(v not in (0, 1) for v in cochain.tw):
        raise ValueError('The coefficient sign must contain one bit per simplex vertex.')
    if any(not isinstance(v, (int, Fraction)) for v in cochain.v.values()):
        raise TypeError('Cochain values must be exact integers or Fraction, not floats.')


def _integer(cochain: Cochain) -> None:
    if any(Fraction(v).denominator != 1 for v in cochain.v.values()):
        raise ValueError('An integer decoration or integer gauge contains a noninteger value.')


@dataclass(frozen=True)
class Symmetry:
    """The unshifted real extension lift and the two actual symmetry characters."""
    omega2_real: Cochain
    s1: Cochain
    rho1: Cochain

    def __post_init__(self) -> None:
        _exact(self.omega2_real, 2)
        _exact(self.s1, 1)
        _exact(self.rho1, 1)
        if len({self.omega2_real.N, self.s1.N, self.rho1.N}) != 1:
            raise ValueError('All background cochains must be on the same simplex.')
        for character in (self.s1, self.rho1):
            if (character - char(character.N, character.tw)).maxabs():
                raise ValueError('A character must be the bit difference of its vertex signs.')
        extension_sign = tuple(a ^ b for a, b in zip(self.s1.tw, self.rho1.tw))
        if self.omega2_real.tw != extension_sign:
            raise ValueError('omega2_real must have coefficient sign rho1+s1.')
        _integer(self.omega2_real.d())

    @property
    def checked_omega2_real(self) -> Cochain:
        return background(self.omega2_real, self.s1)[0]

    @property
    def B3(self) -> Cochain:
        return background(self.omega2_real, self.s1)[1]


def _state(symmetry: Symmetry, spatial_dimension: int, sheet: Cochain, charge: Cochain) -> None:
    if spatial_dimension not in (2, 3, 4):
        raise ValueError('The public interface covers spatial dimensions 2, 3, and 4.')
    for cochain, degree, sign in ((sheet, spatial_dimension - 2, symmetry.s1.tw),
                                  (charge, spatial_dimension, symmetry.rho1.tw)):
        _exact(cochain, degree)
        _integer(cochain)
        if cochain.N != symmetry.omega2_real.N or cochain.tw != sign:
            raise ValueError('Decoration simplex or coefficient sign does not match the symmetry.')
    if sheet.d().maxabs():
        raise ValueError('The integer CI sheet is not closed in its sign system.')
    if (charge.d() - integer_obstruction(symmetry, spatial_dimension, sheet)).maxabs():
        raise ValueError('The charge completion does not solve the integer obstruction.')


def integer_obstruction(symmetry: Symmetry, spatial_dimension: int, sheet: Cochain) -> Cochain:
    """mathcal O_{d+1}, with sheet n_{d-2}; no source normalization parameter."""
    _exact(sheet, spatial_dimension - 2)
    _integer(sheet)
    if sheet.N != symmetry.omega2_real.N or sheet.tw != symmetry.s1.tw:
        raise ValueError('The CI sheet has the wrong simplex or coefficient action.')
    if spatial_dimension == 2:
        return symmetry.omega2_real.d().cup(sheet).sc(-1)
    if spatial_dimension == 3:
        return symmetry.B3.cup(sheet).sc(-1)
    if spatial_dimension == 4:
        return (symmetry.B3.cup(sheet) + symmetry.rho1.cup(sheet.cup(sheet))).sc(-1)
    raise ValueError('spatial_dimension must be 2, 3, or 4.')


def charge_source(symmetry: Symmetry, charge: Cochain) -> Cochain:
    """The single open charge block, Equation (CF-source)."""
    return (symmetry.omega2_real.cup(charge) + bin0(charge).sq(2).sc(Fraction(1, 2))).ret(symmetry.s1.tw)


def charge_product(symmetry: Symmetry, charge: Cochain, charge_prime: Cochain) -> Cochain:
    return Fopen(charge, charge_prime).ret(symmetry.s1.tw)


def charge_gauge(symmetry: Symmetry, charge: Cochain, parameter: Cochain) -> Cochain:
    """The shorter fixed-sheet charge gauge, Equation (CF-gauge).

    This and the joint source-cylinder gauge are permitted representatives.
    Their values need not agree pointwise, so callers should retain which gauge
    they use when recording complete root relations.
    """
    _exact(charge)
    _exact(parameter, charge.p - 1)
    _integer(charge)
    _integer(parameter)
    if (charge.N != symmetry.omega2_real.N or parameter.N != charge.N
            or charge.tw != symmetry.rho1.tw or parameter.tw != charge.tw):
        raise ValueError('The charge gauge has the wrong simplex or coefficient action.')
    return (symmetry.omega2_real.cup(parameter)
            + bin0(parameter).sq(2).sc(Fraction(1, 2))
            + Fopen(charge, parameter.d())).ret(symmetry.s1.tw).mod(1)


def source(symmetry: Symmetry, spatial_dimension: int, sheet: Cochain, charge: Cochain, *, validate: bool = True) -> Cochain:
    """Adopted hatted source; explicit checks reject invalid lower configurations."""
    if validate:
        _state(symmetry, spatial_dimension, sheet, charge)
    if spatial_dimension not in (2, 3, 4):
        raise ValueError('spatial_dimension must be 2, 3, or 4.')
    if spatial_dimension == 4:
        return _cal.source4(symmetry.omega2_real, sheet, charge, symmetry.s1, symmetry.rho1).mod(1)
    if spatial_dimension == 3:
        return _cal.source3(symmetry.omega2_real, sheet, charge, symmetry.s1, symmetry.rho1).mod(1)
    extension = symmetry.omega2_real
    quadratic = extension.cup(extension) + extension.cup(extension.d(), 1)
    return (charge_source(symmetry, charge) + sheet.cup(quadratic).sc(Fraction(1, 2))).ret(symmetry.s1.tw).mod(1)


def integer_product(symmetry: Symmetry, spatial_dimension: int, sheet: Cochain, sheet_prime: Cochain) -> Cochain:
    if spatial_dimension == 4:
        return _E4(sheet, sheet_prime, symmetry.rho1)
    if spatial_dimension == 3:
        return symmetry.rho1.cup(sheet).cup(sheet_prime).sc(-1)
    if spatial_dimension == 2:
        return Cochain(sheet.N, 2, {}, symmetry.rho1.tw)
    raise ValueError('spatial_dimension must be 2, 3, or 4.')


def product(symmetry: Symmetry, spatial_dimension: int, sheet: Cochain, charge: Cochain,
            sheet_prime: Cochain, charge_prime: Cochain, *, validate: bool = True) -> tuple[Cochain, Cochain, Cochain]:
    """Return (N_{d-2}, N_d, hatted E_{d+1}); input phases are added separately."""
    if validate:
        _state(symmetry, spatial_dimension, sheet, charge)
        _state(symmetry, spatial_dimension, sheet_prime, charge_prime)
    correction = integer_product(symmetry, spatial_dimension, sheet, sheet_prime)
    if spatial_dimension == 4:
        phase = _cal.product4(symmetry.omega2_real, sheet, charge, sheet_prime, charge_prime,
                              symmetry.s1, symmetry.rho1)
    elif spatial_dimension == 3:
        phase = _cal.product3(symmetry.omega2_real, sheet, charge, sheet_prime, charge_prime,
                              symmetry.s1, symmetry.rho1)
    else:
        binary_derivative = bin0(symmetry.omega2_real.d())
        phase = (charge_product(symmetry, charge, charge_prime)
                 + sheet.cup(sheet_prime).cup(binary_derivative).sc(Fraction(1, 4)))
    return sheet + sheet_prime, charge + charge_prime + correction, phase.ret(symmetry.s1.tw).mod(1)


def gauge(symmetry: Symmetry, spatial_dimension: int, sheet: Cochain, charge: Cochain,
          sheet_parameter: Optional[Cochain], charge_parameter: Cochain, *, validate: bool = True) -> tuple[Cochain, Cochain, Cochain]:
    """Return the complete gauge endpoint and hatted phase correction."""
    if validate:
        _state(symmetry, spatial_dimension, sheet, charge)
    _exact(charge_parameter, spatial_dimension - 1)
    _integer(charge_parameter)
    if charge_parameter.tw != symmetry.rho1.tw or charge_parameter.N != sheet.N:
        raise ValueError('The charge gauge has the wrong coefficient sign.')
    if spatial_dimension == 2:
        if sheet_parameter is not None:
            raise ValueError('There is no degree-minus-one sheet gauge at the 2+1D endpoint.')
        correction = charge_gauge(symmetry, charge, charge_parameter)
        return sheet, charge + charge_parameter.d(), correction.mod(1)
    if sheet_parameter is None:
        raise ValueError('Supply a sheet gauge cochain (possibly the zero cochain).')
    _exact(sheet_parameter, spatial_dimension - 3)
    _integer(sheet_parameter)
    if sheet_parameter.tw != symmetry.s1.tw or sheet_parameter.N != sheet.N:
        raise ValueError('The sheet gauge has the wrong coefficient sign.')
    if spatial_dimension == 4:
        sheet_out, charge_out = _gauge4(symmetry.omega2_real, sheet, charge, sheet_parameter,
                                         charge_parameter, symmetry.s1, symmetry.rho1)
        phase = _cal.gauge4(symmetry.omega2_real, sheet, charge, symmetry.s1, symmetry.rho1,
                            sheet_parameter, charge_parameter)
    else:
        sheet_out = sheet + sheet_parameter.d()
        charge_out = charge + symmetry.B3.cup(sheet_parameter) + charge_parameter.d()
        phase = _cal.gauge3(symmetry.omega2_real, sheet, charge, symmetry.s1, symmetry.rho1,
                            sheet_parameter, charge_parameter)
    return sheet_out, charge_out, phase.ret(symmetry.s1.tw).mod(1)


def integral_cartan(x: Cochain, y: Cochain) -> Cochain:
    """The unified zeta^Z_{p,q}; valid degree pairs are explicitly restricted."""
    _exact(x); _exact(y); _integer(x); _integer(y)
    if x.N != y.N or x.d().maxabs() or y.d().maxabs():
        raise ValueError('Integral Cartan inputs must be closed on a common simplex.')
    x_binary, y_binary = bin0(x), bin0(y)
    if (x.p, y.p) == (3, 1):
        native = cartan31(x_binary, y_binary)
    elif (x.p, y.p) == (3, 2):
        native = cartan32(x_binary, y_binary)
    elif (x.p, y.p) == (2, 2):
        native = word((1, 2, 3, 1, 3, 4, 3), x_binary, x_binary, y_binary, y_binary)
    else:
        raise ValueError('Only degree pairs (3,1), (3,2), and (2,2) are defined.')
    first_sign, second_sign = char(x.N, x.tw), char(y.N, y.tw)
    return (native
            + halves(x).cup(y_binary.sq(1), 0, True)
            + first_sign.cup(x_binary, 0, True).cup(halves(y), 0, True)
            + first_sign.cup(x_binary.cup(second_sign, 1, True), 0, True).cup(y_binary, 0, True)).mod(2)


def cubic_polarizer(n2: Cochain, n2_prime: Cochain) -> Cochain:
    """Exactly regrouped ordered cubic polarizer; no graded commutation is used."""
    higher_cup = n2.cup(n2_prime, 1)
    return (n2.sc(2) + n2_prime).cup(higher_cup) + higher_cup.cup(n2 + n2_prime.sc(2))


def background_change(symmetry: Symmetry, spatial_dimension: int, sheet: Cochain,
                      charge: Cochain, parameter: Cochain, kind: str, *,
                      validate: bool = True) -> tuple[Symmetry, Cochain, Cochain, Cochain]:
    """Transport a 3+1D or 4+1D state under an integral lift or real section change.

    This is the parameter-first source-cylinder prescription of Equation
    (background-changes). Derived differentials are evaluated on the cylinder
    before any projection degeneracy is removed. The 2+1D endpoint transport is
    not specified by that equation and is deliberately not installed here.
    """
    from itertools import combinations
    from ._engine.prism import pull_on_path, evalface, interval_paths

    if spatial_dimension not in (3, 4):
        raise NotImplementedError('Background cylinder transport is supplied for dimensions 3 and 4.')
    if kind not in ('lift', 'section'):
        raise ValueError("kind must be 'lift' or 'section'.")
    if validate:
        _state(symmetry, spatial_dimension, sheet, charge)
    _exact(parameter, 2 if kind == 'lift' else 1)
    if parameter.N != sheet.N or parameter.tw != symmetry.omega2_real.tw:
        raise ValueError('The background parameter has the wrong simplex or coefficient action.')
    if kind == 'lift':
        _integer(parameter)
        new_omega = symmetry.omega2_real + parameter
        new_charge = charge - parameter.cup(sheet)
    else:
        new_omega = symmetry.omega2_real + parameter.d()
        new_charge = charge
    new_symmetry = Symmetry(new_omega, symmetry.s1, symmetry.rho1)
    phase_degree = spatial_dimension + 1
    values = {}
    for face in combinations(range(sheet.N + 1), phase_degree + 1):
        total = Fraction(0)
        for local_path, sign in interval_paths(phase_degree):
            path = tuple((height, face[j]) for height, j in local_path)
            a, k, n, s, rho = [pull_on_path(c, path) for c in
                                (symmetry.omega2_real, sheet, charge, symmetry.s1, symmetry.rho1)]
            cylinder_N = len(path) - 1
            parameter_on_cylinder = Cochain(cylinder_N, parameter.p, {
                f: path[f[0]][0] * evalface(parameter, tuple(path[j][1] for j in f))
                for f in combinations(range(cylinder_N + 1), parameter.p + 1)}, a.tw)
            if kind == 'lift':
                a = a + parameter_on_cylinder
                n = n - parameter_on_cylinder.cup(k)
            else:
                a = a + parameter_on_cylinder.d()
            cylinder_symmetry = Symmetry(a, s, rho)
            total += sign * source(cylinder_symmetry, spatial_dimension, k, n,
                                   validate=validate)(tuple(range(cylinder_N + 1)))
        values[face] = total % 1
    return new_symmetry, sheet, new_charge, Cochain(sheet.N, phase_degree, values, symmetry.s1.tw)


def lower_exchange(symmetry: Symmetry, spatial_dimension: int,
                   sheet: Cochain, sheet_prime: Cochain) -> Cochain:
    """Charge gauge from the reversed lower product to the ordered product."""
    if spatial_dimension == 4:
        return (sheet.cup(sheet_prime, 1).ret(symmetry.rho1.tw).sc(-1)
                + symmetry.rho1.cup(sheet.cup(sheet_prime, 2)))
    if spatial_dimension == 3:
        return (sheet.cup(sheet_prime).ret(symmetry.rho1.tw)
                + symmetry.rho1.cup(sheet.cup(sheet_prime, 1)))
    if spatial_dimension == 2:
        return Cochain(sheet.N, 1, {}, symmetry.rho1.tw)
    raise ValueError('spatial_dimension must be 2, 3, or 4.')


def associator_3p1(symmetry: Symmetry, sheets: list[Cochain], charges: list[Cochain]) -> Cochain:
    """The explicit canonical parameter-tetrahedron associator (three inputs)."""
    from ._engine.transgression import A3canonical
    if len(sheets) != 3 or len(charges) != 3:
        raise ValueError('The associator requires exactly three complete lower inputs.')
    for sheet, charge in zip(sheets, charges):
        _state(symmetry, 3, sheet, charge)
    return A3canonical(symmetry.omega2_real, sheets, charges,
                       symmetry.s1, symmetry.rho1).ret(symmetry.s1.tw).mod(1)


@dataclass(frozen=True)
class State:
    """A complete insulator state, including its exact terminal phase completion."""
    sheet: Cochain
    charge: Cochain
    phase: Cochain

    def validate(self, symmetry: Symmetry, spatial_dimension: int) -> None:
        _state(symmetry, spatial_dimension, self.sheet, self.charge)
        _exact(self.phase, spatial_dimension + 1)
        if self.phase.N != self.sheet.N or self.phase.tw != symmetry.s1.tw:
            raise ValueError('The terminal phase has the wrong simplex or coefficient action.')
        if (self.phase.d() - source(symmetry, spatial_dimension, self.sheet, self.charge)).mod(1).maxabs():
            raise ValueError('The terminal phase does not solve its source equation.')

    def stack(self, other: 'State', symmetry: Symmetry, spatial_dimension: int) -> 'State':
        self.validate(symmetry, spatial_dimension)
        other.validate(symmetry, spatial_dimension)
        k, n, e = product(symmetry, spatial_dimension, self.sheet, self.charge,
                          other.sheet, other.charge)
        return State(k, n, (self.phase + other.phase + e).mod(1))

    def inverse(self, symmetry: Symmetry, spatial_dimension: int) -> 'State':
        self.validate(symmetry, spatial_dimension)
        k = self.sheet.sc(-1)
        n = self.charge.sc(-1) + integer_product(symmetry, spatial_dimension, self.sheet, self.sheet)
        _, _, e = product(symmetry, spatial_dimension, self.sheet, self.charge, k, n)
        return State(k, n, (self.phase.sc(-1) - e).mod(1))

    def power(self, exponent: int, symmetry: Symmetry, spatial_dimension: int) -> 'State':
        """Exact arbitrary integer powers, retaining every intermediate phase."""
        if not isinstance(exponent, int):
            raise TypeError('The root exponent must be an integer.')
        self.validate(symmetry, spatial_dimension)
        base = self if exponent >= 0 else self.inverse(symmetry, spatial_dimension)
        result = State(self.sheet.sc(0), self.charge.sc(0), self.phase.sc(0))
        exponent = abs(exponent)
        while exponent:
            if exponent & 1:
                result = result.stack(base, symmetry, spatial_dimension)
            exponent //= 2
            if exponent:
                base = base.stack(base, symmetry, spatial_dimension)
        return result

    def gauge(self, symmetry: Symmetry, spatial_dimension: int,
              sheet_parameter: Optional[Cochain], charge_parameter: Cochain,
              phase_parameter: Optional[Cochain] = None) -> 'State':
        self.validate(symmetry, spatial_dimension)
        k, n, correction = gauge(symmetry, spatial_dimension, self.sheet, self.charge,
                                  sheet_parameter, charge_parameter)
        phase = self.phase + correction
        if phase_parameter is not None:
            _exact(phase_parameter, spatial_dimension)
            if phase_parameter.N != self.sheet.N or phase_parameter.tw != symmetry.s1.tw:
                raise ValueError('The phase gauge has the wrong simplex or coefficient action.')
            phase = phase + phase_parameter.d()
        return State(k, n, phase.mod(1))


# AHSS operations return representatives; the global solver forms their classes
# only after permitted lower adjustments and incoming identifications.
d2 = charge_source
d3 = integer_obstruction
d4 = source

# Dimension-specific entry points expose the physical names used by the note.
def obstruction_2p1(symmetry: Symmetry, n0: Cochain, n2: Cochain) -> Cochain:
    return source(symmetry, 2, n0, n2)

def obstruction_3p1(symmetry: Symmetry, n1: Cochain, n3: Cochain) -> Cochain:
    return source(symmetry, 3, n1, n3)

def obstruction_4p1(symmetry: Symmetry, n2: Cochain, n4: Cochain) -> Cochain:
    return source(symmetry, 4, n2, n4)

def stacking_2p1(symmetry: Symmetry, n0: Cochain, n2: Cochain,
                 n0_prime: Cochain, n2_prime: Cochain) -> tuple[Cochain, Cochain, Cochain]:
    return product(symmetry, 2, n0, n2, n0_prime, n2_prime)

def stacking_3p1(symmetry: Symmetry, n1: Cochain, n3: Cochain,
                 n1_prime: Cochain, n3_prime: Cochain) -> tuple[Cochain, Cochain, Cochain]:
    return product(symmetry, 3, n1, n3, n1_prime, n3_prime)

def stacking_4p1(symmetry: Symmetry, n2: Cochain, n4: Cochain,
                 n2_prime: Cochain, n4_prime: Cochain) -> tuple[Cochain, Cochain, Cochain]:
    return product(symmetry, 4, n2, n4, n2_prime, n4_prime)
