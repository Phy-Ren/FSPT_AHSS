"""Exact local CI/charge/E8 model in the order (e_p,n_p,n_{p+2},nu_{p+3}).

Here p = spatial_dimension - 2. These are local signed cochain operations;
neither a finite group nor a finite multiplication table is required. Global
completion, incoming quotients, and physical-spectrum identification are
separate tasks. In particular, this module never assumes a global primitive.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from . import api as ci
from ._engine import e8_4p1 as neutral

Cochain = ci.Cochain
Symmetry = ci.Symmetry


def _typed(cochain: Cochain, degree: int, symmetry: Symmetry,
           *, integral: bool = False) -> None:
    ci._exact(cochain, degree)
    if cochain.N != symmetry.s1.N or cochain.tw != symmetry.s1.tw:
        raise ValueError('The E8/phase cochain has the wrong simplex or coefficient sign.')
    if integral:
        ci._integer(cochain)


def _sheet(e_p: Cochain, symmetry: Symmetry, dimension: int) -> None:
    if dimension not in (2, 3, 4):
        raise ValueError('spatial_dimension must be 2, 3, or 4.')
    _typed(e_p, dimension - 2, symmetry, integral=True)
    ci._uniform_response_domain(symmetry, dimension, e_p, 'E8')
    if e_p.d().maxabs():
        raise ValueError('The signed integer E8 decoration is not closed.')


def source(symmetry: Symmetry, spatial_dimension: int, e_p: Cochain,
           n_p: Cochain, n_p2: Cochain) -> Cochain:
    """The common terminal source, with the E8 input first."""
    _sheet(e_p, symmetry, spatial_dimension)
    phase = ci.source(symmetry, spatial_dimension, n_p, n_p2)
    if spatial_dimension == 4:
        phase = phase + neutral.source(e_p)
    return phase.mod(1)


@dataclass(frozen=True)
class State:
    """A completed local state (e_p,n_p,n_{p+2},nu_{p+3}), E8 first."""
    e_p: Cochain
    n_p: Cochain
    n_p2: Cochain
    nu_p3: Cochain

    def validate(self, symmetry: Symmetry, spatial_dimension: int) -> None:
        expected = source(symmetry, spatial_dimension, self.e_p, self.n_p, self.n_p2)
        _typed(self.nu_p3, spatial_dimension + 1, symmetry)
        if (self.nu_p3.d() - expected).mod(1).maxabs():
            raise ValueError('The common phase does not solve the full source equation.')

    def stack(self, other: 'State', symmetry: Symmetry, spatial_dimension: int) -> 'State':
        self.validate(symmetry, spatial_dimension)
        other.validate(symmetry, spatial_dimension)
        n, charge, phase = ci.product(symmetry, spatial_dimension,
                                      self.n_p, self.n_p2, other.n_p, other.n_p2)
        if spatial_dimension == 4:
            phase = phase + neutral.product(self.e_p, other.e_p)
        result = State(self.e_p + other.e_p, n, charge,
                       (self.nu_p3 + other.nu_p3 + phase).mod(1))
        result.validate(symmetry, spatial_dimension)
        return result

    def gauge(self, symmetry: Symmetry, spatial_dimension: int,
              e_parameter: Optional[Cochain], n_parameter: Optional[Cochain],
              charge_parameter: Cochain, phase_parameter: Optional[Cochain] = None) -> 'State':
        self.validate(symmetry, spatial_dimension)
        if spatial_dimension == 2:
            if e_parameter is not None:
                raise ValueError('There is no degree-minus-one E8 gauge for e0.')
            e_out = self.e_p
        else:
            if e_parameter is None:
                raise ValueError('Supply an E8 gauge cochain, possibly zero.')
            _typed(e_parameter, spatial_dimension - 3, symmetry, integral=True)
            e_out = self.e_p + e_parameter.d()
        n_out, charge_out, correction = ci.gauge(symmetry, spatial_dimension,
                                                 self.n_p, self.n_p2,
                                                 n_parameter, charge_parameter)
        if spatial_dimension == 4:
            correction = correction + neutral.gauge(self.e_p, e_parameter)
        phase = self.nu_p3 + correction
        if phase_parameter is not None:
            _typed(phase_parameter, spatial_dimension, symmetry)
            phase = phase + phase_parameter.d()
        result = State(e_out, n_out, charge_out, phase.mod(1))
        result.validate(symmetry, spatial_dimension)
        return result

    def inverse(self, symmetry: Symmetry, spatial_dimension: int) -> 'State':
        self.validate(symmetry, spatial_dimension)
        n = self.n_p.sc(-1)
        charge = self.n_p2.sc(-1) + ci.integer_product(
            symmetry, spatial_dimension, self.n_p, self.n_p)
        _, _, phase = ci.product(symmetry, spatial_dimension, self.n_p, self.n_p2, n, charge)
        e = self.e_p.sc(-1)
        if spatial_dimension == 4:
            phase = phase + neutral.product(self.e_p, e)
        result = State(e, n, charge, (self.nu_p3.sc(-1) - phase).mod(1))
        result.validate(symmetry, spatial_dimension)
        return result

    def power(self, exponent: int, symmetry: Symmetry, spatial_dimension: int) -> 'State':
        if not isinstance(exponent, int):
            raise TypeError('The exponent must be an integer.')
        self.validate(symmetry, spatial_dimension)
        base = self if exponent >= 0 else self.inverse(symmetry, spatial_dimension)
        result = State(*(c.sc(0) for c in (self.e_p, self.n_p, self.n_p2, self.nu_p3)))
        exponent = abs(exponent)
        while exponent:
            if exponent & 1:
                result = result.stack(base, symmetry, spatial_dimension)
            exponent //= 2
            if exponent:
                base = base.stack(base, symmetry, spatial_dimension)
        return result

    def background_change(self, symmetry: Symmetry, spatial_dimension: int,
                          parameter: Cochain, kind: str) -> tuple[Symmetry, 'State']:
        """Transport the CI background while retaining the neutral coordinate."""
        self.validate(symmetry, spatial_dimension)
        new_symmetry, n, charge, phase = ci.background_change(
            symmetry, spatial_dimension, self.n_p, self.n_p2, parameter, kind)
        result = State(self.e_p, n, charge, (self.nu_p3 + phase).mod(1))
        result.validate(new_symmetry, spatial_dimension)
        return new_symmetry, result


def thermal_sheet(e_p: Cochain, n_p: Cochain) -> Cochain:
    """Return 16 e_p + 2 n_p in p+ip units; not a full parity-state map."""
    ci._exact(e_p)
    ci._exact(n_p, e_p.p)
    ci._integer(e_p)
    ci._integer(n_p)
    if e_p.N != n_p.N or e_p.tw != n_p.tw:
        raise ValueError('The two response coordinates must have the same coefficient type.')
    return e_p.sc(16) + n_p.sc(2)
