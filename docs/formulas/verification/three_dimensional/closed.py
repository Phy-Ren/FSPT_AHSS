"""Closed-sector 3+1D formulas (n1 = 0), from the Majorana projector calculation.

These are the formulas of docs/formulas/MAJORANA_AND_ENDPOINTS.md (3+1D), the
same as Sec. IV of the 3+1D stacking paper.  They are independent of the
general formulas in formulas.py and serve as the reference for n1 = 0.
"""
from fractions import Fraction

from formulas import C, cup, op


def beta(x):
    """Bockstein of a closed binary cochain, d(lift x)/2."""
    return x.lift().d().div(2)


def beta_plus(x):
    b = beta(x)
    return (b + b.reduce(2).lift()).div(2)


def X5(x):
    out = op('1213243', x, x, x, x)
    for v in ('1213431', '1232141', '1234321'):
        out = out + op(v, x, x, x, x)
    return out


def O5(n2, n3, w, s, f):
    b = beta(n2).reduce(2)
    sq = cup(n2, n2)
    dn3 = n3.d()
    half = (cup(w, n3) + cup(n3, n3, 1) + cup(dn3, n3, 2) + cup(dn3, dn3, 3)
            + op('1231343', w, w, n2, n2) + X5(n2) + cup(sq, cup(w, n2), 3)
            + cup(sq, cup(s, b), 3) + cup(cup(w, n2), cup(s, b), 3)
            + op('1231434', s, s, b, b) + cup(cup(w, s, 1), b) + cup(s, sq))
    B = beta(n2)
    quarter = cup(w.lift(), B) + cup(B, B, 1) + cup(cup(s, s).lift(), B + b.lift())
    return (Fraction(half(f) % 2, 2) + Fraction(quarter(f), 4)) % 1


def z40(x, y):
    out = C(4)
    for v in ('12123434', '12134131', '12314324', '12314342',
              '13242412', '13413142', '13432412'):
        out = out + op(v, x, x, y, y)
    bx, by = beta(x).reduce(2), beta(y).reduce(2)
    out = out + op('12123', x + y, y, cup(x, y, 2)) + op('123131', y, x, cup(x, y, 1))
    out = out + cup(cup(x, y, 1), y, 1) + cup(bx + by, cup(x, y, 2), 1)
    out = out + cup(cup(x, y, 2), bx + by + cup(y, x, 1), 1)
    out = out + cup(cup(x, y, 1), cup(x, x) + cup(y, y), 3)
    out = out + cup(y, cup(x, cup(x, y, 1), 1), 2) + cup(by, bx, 2)
    return out


def E4(n2, n3, m2, m3, w, s, f):
    e3 = cup(n2, m2, 1) + cup(s, cup(n2, m2, 2))
    N3 = n3 + m3 + e3
    N2 = n2 + m2
    lam = cup(n2, m2, 2)
    bn, bm = beta(n2).reduce(2), beta(m2).reduce(2)
    wN = cup(w, N2)
    z = (z40(n2, m2) + cup(wN, e3, 3) + cup(cup(n2, m2, 1).d(), wN, 4)
         + cup(cup(m2, m2), cup(w, n2), 4) + cup(cup(m2, m2) + cup(w, m2), cup(s, bn), 4)
         + cup(cup(w, s, 1), lam) + cup(cup(n2, m2, 1), cup(s, bn + bm), 3)
         + cup(cup(N2, N2), cup(s, lam), 3) + cup(cup(n2, m2, 1), cup(s, lam), 2))
    carry = (beta_plus(N2) - beta_plus(n2) - beta_plus(m2)).reduce(2)
    inner = (e3 + cup(bn, bm, 3) + cup(lam, lam, 1) + cup(bn + bm, cup(s, lam), 3)
             + cup(cup(s, lam), lam, 2) + carry)
    z = z + cup(s, inner)
    fermion = (cup(n3, m3, 2) + cup(n3 + m3, e3, 2) + cup(n3.d(), m3, 3)
               + cup(N3, N3.d(), 3) + cup(n3, n3.d(), 3) + cup(m3, m3.d(), 3))
    t = lam.lift()
    Bn, Bm, BN = beta(n2), beta(m2), beta(N2)
    quarter = (cup(Bn, Bm, 2).scaled(-1) + cup(Bn + Bm, t, 1) - cup(t, BN, 1)
               + cup(t, t) - cup(w.lift(), t))
    return (Fraction((fermion(f) + z(f)) % 2, 2) + Fraction(quarter(f), 4)) % 1
