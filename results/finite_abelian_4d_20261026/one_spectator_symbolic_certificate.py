#!/usr/bin/env python3
"""Symbolic certificate for the arbitrary-exponent one-spectator reduction.

This checks polynomial identities, not a finite sample of group orders.
Completeness of the starting lattice is proved in TWO_FACTOR_GYSIN_PROOF.md.
The integral/localized operations are explained in
ONE_SPECTATOR_SYMBOLIC_SMITH_PROOF.md.
"""
from math import gcd
from sympy import Matrix, Rational, expand, simplify, symbols


def scalar_factors(m, n):
    """The exact mixed Smith factors, omitting trivial factors."""
    if min(m, n) < 2 or m & (m - 1) or n & (n - 1):
        raise ValueError("m and n must be powers of two at least two")
    g = gcd(m, n)
    k = gcd(n // 2, 2 * g)
    return sorted(x for x in (n // 2, gcd(m // 2, n), k, 2 * n * g // k)
                  if x > 1)


def symbolic_certificate():
    m, n, t, q = symbols("m n t q", integer=True)
    v = Matrix([2*t + 1, t*(t + 1)*(2*t + 1)/6,
                q, (q**3 - q)/6, t*(t + 1)*q/2,
                t*q**2 + (q**2 - q)/2])
    difference_a = v.subs(t, t + m) - v
    difference_b = v.subs(q, q + n) - v
    a = m*(m + 1)*(2*m + 1)/6
    b = m*(m + 1)/2
    c = n*(n*n - 1)/6
    d = n*(n - 1)/2
    e = n*(n + 1)/2
    rows_a = [
        Matrix([2*m, a, 0, 0, 0, 0]),
        Matrix([0, m*(m + 2), 0, 0, 0, 0]),
        Matrix([0, 2*m, 0, 0, 0, 0]),
        Matrix([0, 0, 0, 0, b, m]),
        Matrix([0, 0, 0, 0, 0, 2*m]),
        Matrix([0, 0, 0, 0, m, 0]),
    ]
    rows_b = [
        Matrix([0, 0, n, c, 0, d]),
        Matrix([0, 0, 0, 0, n, n*n]),
        Matrix([0, 0, 0, 0, n, 0]),
        Matrix([0, 0, 0, e, 0, n]),
        Matrix([0, 0, 0, n, 0, 0]),
        Matrix([0, 0, 0, 0, 0, 2*n]),
    ]
    monomials = [1, t, t*(t - 1)/2, q, q*(q - 1)/2, t*q]
    zero = Matrix.zeros(6, 1)
    for difference, rows in [(difference_a, rows_a), (difference_b, rows_b)]:
        reconstruction = sum((f*r for f, r in zip(monomials, rows)), zero)
        assert all(expand(x) == 0 for x in difference - reconstruction)
    assert all(simplify(x) == 0
               for x in rows_a[1] - (m + 2)/2*rows_a[2])
    assert all(simplify(x) == 0
               for x in rows_b[1] - rows_b[2] - n/2*rows_b[5])

    # Explicit local row and column identities for the four-generator block.
    a0, b0, c0, z, g, anew = symbols("a0 b0 c0 z g anew")
    rel_a = b*c0 + m*z
    rel_b = n*a0 + c*b0 + d*z
    rel_c = e*b0 + n*z
    u = (n - 1)/3
    assert simplify(c - u*e) == 0
    assert simplify(rel_b - u*rel_c - (n*a0 + n*u*z/2)) == 0
    assert simplify((rel_b - u*rel_c).subs(a0, u*anew)
                    - u*(n*anew + n*z/2)) == 0
    bnew = (n + 1)*b0 + 2*z
    cnew = (m + 1)*c0 + 2*z
    assert simplify(rel_c - n*bnew/2) == 0
    assert simplify(rel_a - m*cnew/2) == 0
    assert simplify(g*cnew - (m + 1)*g*c0 - 2*g*z) == 0
    assert simplify(2*rel_c - n*(n + 1)*b0 - 2*n*z) == 0
    remaining = Matrix([[n, n/2], [0, 2*g]])
    assert simplify(remaining.det() - 2*n*g) == 0
    return {
        "Newton polynomial identities": "proved symbolically",
        "Redundant Newton rows": "proved symbolically",
        "Localized row and column identities": "proved symbolically",
        "Remaining determinant": "2*N*g",
        "Mixed factors": "N/2, gcd(m/2,N), k, 2*N*g/k",
        "Definitions": "g=gcd(m,N); k=gcd(N/2,2*g)",
        "Parameter sampling": "none",
    }


if __name__ == "__main__":
    import json
    print(json.dumps(symbolic_certificate(), indent=2))
