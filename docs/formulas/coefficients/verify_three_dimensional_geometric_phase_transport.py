#!/usr/bin/env python3
"""Exact finite CF gauge identity; unrestricted x and B2, closed omega2.
Arithmetic is an independent normalized interval-cut implementation.
"""
from dataclasses import dataclass
from functools import lru_cache
from hashlib import sha256
from itertools import combinations, combinations_with_replacement
from pathlib import Path
import json


@dataclass(frozen=True)
class Polynomial:
    terms: frozenset[int]

    @staticmethod
    def value(x):
        if isinstance(x, Polynomial):
            return x
        return Polynomial(frozenset({0}) if x % 2 else frozenset())

    @staticmethod
    def variable(i):
        return Polynomial(frozenset({1 << i}))

    def __add__(self, other):
        return Polynomial(self.terms ^ self.value(other).terms)

    __radd__ = __add__

    def __mul__(self, other):
        terms = set()
        for x in self.terms:
            for y in self.value(other).terms:
                term = x | y
                if term in terms:
                    terms.remove(term)
                else:
                    terms.add(term)
        return Polynomial(frozenset(terms))

    __rmul__ = __mul__


ZERO = Polynomial.value(0)
VERTICES = tuple(range(5))


@lru_cache(None)
def cuts(p, q, higher):
    """Normalized interval cuts for the alternating higher-cup word."""
    degree = p + q - higher
    result = []
    for inner in combinations_with_replacement(range(degree + 1), higher + 1):
        ends = (0,) + inner + (degree,)
        faces = [[], []]
        for j in range(higher + 2):
            faces[j % 2].extend(range(ends[j], ends[j + 1] + 1))
        if all(len(f) == d + 1 and all(a < b for a, b in zip(f, f[1:]))
               for f, d in zip(faces, (p, q))):
            result.append(tuple(map(tuple, faces)))
    return tuple(result)


def cup(left, p, right, q, higher=0):
    return {
        face: sum((left[tuple(face[i] for i in a)]
                   * right[tuple(face[i] for i in b)]
                   for a, b in cuts(p, q, higher)), ZERO)
        for face in combinations(VERTICES, p + q - higher + 1)
    }


def add(*cochains):
    return {face: sum((c[face] for c in cochains), ZERO) for face in cochains[0]}


def differential(cochain, degree):
    return {
        face: sum((cochain[face[:j] + face[j + 1:]]
                   for j in range(degree + 2)), ZERO)
        for face in combinations(VERTICES, degree + 2)
    }


def closed_from_zero_faces(degree, variable, prefix):
    result = {(0,) + f: variable(prefix + ''.join(map(str, f)))
              for f in combinations(VERTICES[1:], degree)}
    for face in combinations(VERTICES[1:], degree + 1):
        result[face] = sum((result[(0,) + face[:j] + face[j + 1:]]
                            for j in range(degree + 1)), ZERO)
    assert all(x == ZERO for x in differential(result, degree).values())
    return result


VERTICES=tuple(range(6))
Z=ZERO;V=VERTICES;names=[]
def free(deg,name):
 out={}
 for f in combinations(V,deg+1):
  out[f]=Polynomial.variable(len(names));names.append((name,f))
 return out
def d(x,p):return differential(x,p)
x=free(3,'x');b=free(2,'B2')
w=closed_from_zero_faces(2,lambda n:(names.append((n,())) or Polynomial.variable(len(names)-1)),'w')
z=d(b,2);dx=d(x,3)
def Q(c):return add(cup(w,2,c,3),cup(c,3,c,3,1),cup(d(c,3),4,c,3,2))
K=add(cup(w,2,b,2),cup(b,2,b,2),cup(z,3,b,2,1),cup(x,3,z,3,2))
r=add(d(K,4),Q(add(x,z)),Q(x))[V]
assert r==Z
wrong=add(d(K,4),Q(add(x,z)),Q(x),d(cup(w,2,b,2),4))[V]
assert wrong!=Z
report={'status':'PASS','free_bits':len(names),'phase_numerator_modulus':2,'residual_monomials':len(r.terms),'negative_control_omitting_omega_B2_monomials':len(wrong.terms),'identity':'d_s(K/2) = O5(x+dB2)-O5(x) modulo one','scope':'No restriction on x or B2. Closed omega2. Arbitrary s1, since half-valued phases have binary sign coefficients.'}
Path(__file__).with_name('three_dimensional_geometric_phase_transport.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report))
