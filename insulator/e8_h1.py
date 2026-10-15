"""Exact H^1(G; Z_s) from a finite presentation and a sign character.

Signed words use integers +/-1,...,+/-ngen.  The method computes the saturated
integer kernel of all relator equations and then divides by the ONE principal
crossed-homomorphism column.  No floating-point or mod-two substitution is used.
"""
from __future__ import annotations
from dataclasses import dataclass
from fractions import Fraction
from functools import reduce
from math import gcd
from typing import Sequence


def _bezout(a: int, b: int) -> tuple[int, int, int]:
    old_r, r, old_s, s, old_t, t = abs(a), abs(b), 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
    return old_r, old_s * (-1 if a < 0 else 1), old_t * (-1 if b < 0 else 1)


def relation_row(word: Sequence[int], signs: Sequence[int]) -> list[int]:
    row, prefix = [0] * len(signs), 1
    for letter in word:
        if not isinstance(letter, int) or not 1 <= abs(letter) <= len(signs):
            raise ValueError('A relator letter is outside the generator range.')
        j = abs(letter) - 1
        row[j] += prefix * (1 if letter > 0 else -signs[j])
        prefix *= signs[j]
    if prefix != 1:
        raise ValueError('The proposed sign character does not respect a relator.')
    return row


def saturated_kernel(rows: Sequence[Sequence[int]], n: int) -> list[list[int]]:
    # Columns of basis remain a saturated basis of all equations imposed so far.
    basis = [[int(i == j) for j in range(n)] for i in range(n)]
    width = n
    for row in rows:
        values = [sum(row[i] * basis[i][j] for i in range(n)) for j in range(width)]
        if not any(values):
            continue
        for j in range(1, width):
            a, b = values[0], values[j]
            if b == 0:
                continue
            g, x, y = _bezout(a, b)
            for i in range(n):
                first, second = basis[i][0], basis[i][j]
                basis[i][0] = x * first + y * second
                basis[i][j] = (-b // g) * first + (a // g) * second
            values[0], values[j] = g, 0
        basis = [line[1:] for line in basis]
        width -= 1
    return basis


def _coordinates(basis: list[list[int]], vector: list[int]) -> list[int]:
    n = len(vector); width = len(basis[0]) if n else 0
    matrix = [[Fraction(x) for x in basis[i]] + [Fraction(vector[i])] for i in range(n)]
    pivot_row = 0; pivots = []
    for column in range(width):
        found = next((i for i in range(pivot_row, n) if matrix[i][column]), None)
        if found is None:
            raise ArithmeticError('Kernel basis unexpectedly lost rank.')
        matrix[pivot_row], matrix[found] = matrix[found], matrix[pivot_row]
        a = matrix[pivot_row][column]
        matrix[pivot_row] = [x/a for x in matrix[pivot_row]]
        for i in range(n):
            if i != pivot_row and matrix[i][column]:
                a = matrix[i][column]
                matrix[i] = [x-a*y for x,y in zip(matrix[i], matrix[pivot_row])]
        pivots.append(pivot_row); pivot_row += 1
    if any(all(x == 0 for x in line[:width]) and line[-1] for line in matrix):
        raise ArithmeticError('Principal coboundary is not in the integer kernel.')
    result = [matrix[pivots[j]][-1] for j in range(width)]
    if any(v.denominator != 1 for v in result):
        raise ArithmeticError('Kernel is not saturated.')
    return [int(v) for v in result]


@dataclass(frozen=True)
class H1Result:
    free_rank: int
    torsion: tuple[int, ...]
    relator_matrix: list[list[int]]
    cocycle_basis_columns: list[list[int]]
    coboundary_coordinates: list[int]


def twisted_h1(signs: Sequence[int], relators: Sequence[Sequence[int]]) -> H1Result:
    if any(s not in (-1,1) for s in signs):
        raise ValueError('Generator signs must be +/-1.')
    n = len(signs)
    rows = [relation_row(word, signs) for word in relators]
    basis = saturated_kernel(rows, n)
    principal = [s-1 for s in signs]
    q = _coordinates(basis, principal)
    width = len(q)
    if not any(q):
        free, torsion = width, ()
    else:
        divisor = reduce(gcd, (abs(v) for v in q), 0)
        free, torsion = width-1, (() if divisor == 1 else (divisor,))
    for row in rows:
        assert all(sum(row[i]*basis[i][j] for i in range(n)) == 0 for j in range(width))
    assert all(sum(basis[i][j]*q[j] for j in range(width)) == principal[i] for i in range(n))
    return H1Result(free, torsion, rows, basis, q)
