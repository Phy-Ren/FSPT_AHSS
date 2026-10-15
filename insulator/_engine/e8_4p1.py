"""Neutral E8 cochains in 4+1 dimensions, signed integer convention.

The source sign agrees with the retained parity source at n2_SC = 16 e2.
All divisions are exact rational arithmetic; no mod-two reduction is used.
"""
from __future__ import annotations
from fractions import Fraction
from ..api import Cochain, _exact

THIRD = Fraction(1, 3)


def _integer(cochain: Cochain) -> None:
    _exact(cochain)
    if any(not isinstance(value, (int, Fraction)) or Fraction(value).denominator != 1
           for value in cochain.v.values()):
        raise ValueError('Neutral decorations and gauge parameters must be exact integers.')


def _closed_pair(e2: Cochain, e2_prime: Cochain) -> None:
    _integer(e2); _integer(e2_prime)
    if e2.N != e2_prime.N or e2.p != 2 or e2_prime.p != 2:
        raise ValueError('Both sheets must be degree-two cochains on the same simplex.')
    if e2.tw != e2_prime.tw:
        raise ValueError('Both neutral sheets must have the same s1 coefficient system.')
    if e2.d().maxabs() or e2_prime.d().maxabs():
        raise ValueError('The neutral sheets must be integrally closed.')


def source(e2: Cochain) -> Cochain:
    """O6_E8 = e2 cup e2 cup e2 / 3. Values are not reduced modulo one."""
    _integer(e2)
    if e2.p != 2 or e2.d().maxabs():
        raise ValueError('A closed signed integral two-cochain is required.')
    return e2.cup(e2).cup(e2).sc(THIRD)


def cubic_polarizer(e2: Cochain, e2_prime: Cochain) -> Cochain:
    """Integral C5, with d C5 = Delta(e2^3) - 3(e2^2 e2_prime + e2 e2_prime^2)."""
    _closed_pair(e2, e2_prime)
    higher_cup = e2.cup(e2_prime, 1)
    return (e2.sc(2) + e2_prime).cup(higher_cup) + higher_cup.cup(e2 + e2_prime.sc(2))


def product(e2: Cochain, e2_prime: Cochain) -> Cochain:
    """The cup commutator [e2 cup1 e2_prime, e2-e2_prime]/3.

    Equal to the integral cubic polarizer /3 modulo integers, with a shorter
    rational representative. In particular the self-twister is identically zero.
    """
    _closed_pair(e2, e2_prime)
    higher_cup = e2.cup(e2_prime, 1)
    difference = e2 - e2_prime
    return (higher_cup.cup(difference) - difference.cup(higher_cup)).sc(THIRD)


def gauge(e2: Cochain, v1: Cochain) -> Cochain:
    """G5 for e2 -> e2 + d_s1 v1, with no silent changes of charge."""
    _integer(e2); _integer(v1)
    if e2.p != 2 or e2.d().maxabs():
        raise ValueError('The input sheet must be integrally closed.')
    if v1.p != 1 or v1.N != e2.N or v1.tw != e2.tw:
        raise ValueError('The gauge parameter must be a signed one-cochain of the same type.')
    e2_out = e2 + v1.d()
    return (v1.cup(e2_out).cup(e2_out)
            + e2.cup(v1).cup(e2_out)
            + e2.cup(e2).cup(v1)).sc(THIRD)


def associator(e2: Cochain, e2_prime: Cochain, e2_double_prime: Cochain) -> Cochain:
    """A4: left-associated minus right-associated phase products = d_s1 A4."""
    _closed_pair(e2, e2_prime)
    _closed_pair(e2, e2_double_prime)
    return e2.cup(e2_prime, 1).cup(e2_double_prime, 1).sc(THIRD)


def commutator(e2: Cochain, e2_prime: Cochain) -> Cochain:
    """C4 with E5(e,e') - E5(e',e) = d_s1 C4, modulo one."""
    _closed_pair(e2, e2_prime)
    top_cup = e2.cup(e2_prime, 2)
    difference = e2 - e2_prime
    return (top_cup.cup(difference) - difference.cup(top_cup)).sc(THIRD)


def inverse_phase(e2: Cochain, nu5: Cochain) -> Cochain:
    """Phase of the inverse of a completed neutral state."""
    return nu5.sc(-1) - product(e2, e2.sc(-1))


def hexagon_first(e2: Cochain, e2_prime: Cochain, e2_double_prime: Cochain) -> Cochain:
    """Degree-three witness for C(e,f+g)-C(e,f)-C(e,g)+A(e,f,g)+A(f,g,e)-A(f,e,g)."""
    return (e2.cup(e2_prime,2).cup(e2_double_prime,1)
            + e2.cup(e2_prime.cup(e2_double_prime,1),2)).sc(-THIRD)


def hexagon_second(e2: Cochain, e2_prime: Cochain, e2_double_prime: Cochain) -> Cochain:
    """Degree-three witness for C(e+f,g)-C(e,g)-C(f,g)-A(e,f,g)-A(g,e,f)+A(e,g,f)."""
    return (e2.cup(e2_prime,1).cup(e2_double_prime,2)
            + e2.cup(e2_prime.cup(e2_double_prime,2),1)).sc(-THIRD)


def interval_integral(operation, *sheet_gauge_pairs) -> Cochain:
    """Fixed signed prism sum of a source/product on closed sheet cylinders.

The j-th prism has vertices (v0,0),...,(vj,0),(vj,1),...,(vq,1).
Its sign is (-1)^j. Degenerate base pullbacks vanish, but the derived
cylinder differential is evaluated before discarding any vertical face.
"""
    from itertools import combinations
    N=sheet_gauge_pairs[0][0].N
    out_degree=operation(*(e for e,v in sheet_gauge_pairs)).p-1
    result={}
    for face in combinations(range(N+1),out_degree+1):
        value=0
        for j in range(len(face)):
            vertices=tuple((a,0) for a in face[:j+1])+tuple((a,1) for a in face[j:])
            arguments=[]
            for e2,v1 in sheet_gauge_pairs:
                tw=tuple(e2.tw[a] for a,t in vertices)
                def base_eval(c,indices):
                    projected=tuple(vertices[i][0] for i in indices)
                    return 0 if len(set(projected))!=len(projected) else c(projected)
                e_pull=Cochain(out_degree+1,2,{ii:base_eval(e2,ii) for ii in combinations(range(out_degree+2),3)},tw)
                height_v=Cochain(out_degree+1,1,{ii:vertices[ii[0]][1]*base_eval(v1,ii) for ii in combinations(range(out_degree+2),2)},tw)
                arguments.append(e_pull+height_v.d())
            value+=(-1)**j*operation(*arguments)(tuple(range(out_degree+2)))
        result[face]=value
    return Cochain(N,out_degree,result,sheet_gauge_pairs[0][0].tw)


def pair_gauge(e2: Cochain, e2_prime: Cochain, v1: Cochain, v1_prime: Cochain) -> Cochain:
    """Explicit H4 for compatibility of two simultaneous gauges with stacking."""
    return interval_integral(product,(e2,v1),(e2_prime,v1_prime))


def gauge_composition(e2: Cochain, v1: Cochain, w1: Cochain) -> Cochain:
    """K4 with G(e;v)+G(e+dv;w)-G(e;v+w)=d K4 over rational lifts."""
    gauge(e2, v1)
    gauge(e2, w1)
    intermediate = e2 + v1.d()
    endpoint = intermediate + w1.d()
    return (v1.cup(w1).cup(endpoint)
            + v1.cup(intermediate).cup(w1)
            + e2.cup(v1).cup(w1)).sc(THIRD)
