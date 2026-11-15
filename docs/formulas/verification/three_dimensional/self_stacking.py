"""The 3+1D self-stacking formulas of THREE_DIMENSIONAL_SELF_STACKING.md.

Both branches are transcribed from the page; the two face tables are read
from THREE_DIMENSIONAL_SELF_STACKING_FACES_*.md.
"""
import re
from fractions import Fraction
from pathlib import Path

import formulas as F
from formulas import C, cup, op, ds, beta_open

DOCS = Path(__file__).resolve().parents[2]


def half(x):
    return Fraction(x % 2, 2)


def read_table(kind):
    """Rows of a face table as tuples of (field, face)."""
    rows = []
    for path in sorted(DOCS.glob(f'THREE_DIMENSIONAL_SELF_STACKING_FACES_{kind}_*.md')):
        for line in path.read_text().splitlines():
            m = re.match(r'\| *\d+ *\| *\$`(.*)`\$ *\|', line)
            if m:
                rows.append(tuple((name, tuple(map(int, f))) for name, f in
                                  re.findall(r'(n_2|\\omega_2|s_1)\((\d+)\)', m.group(1))))
    return rows


TABLES = {}


def table_value(kind, values, f):
    if kind not in TABLES:
        TABLES[kind] = read_table(kind)
    total = 0
    for row in TABLES[kind]:
        total ^= all(values[name](tuple(f[j] for j in face)) for name, face in row)
    return total


def zero_branch(x, s, w, f):
    """Section 4: n1 = 0."""
    n2, n3 = x['n2'], x['n3']
    A = F.O4_gamma(n2, w, s)
    N3 = cup(n2, n2, 1) + cup(n2, n2.d(), 2) + cup(s, n2)
    b = beta_open(n2)
    h = (cup(n3, n3, 2) + cup(A, n3, 3) + cup(cup(w, s, 1), n2) + cup(b.reduce(2), cup(s, n2), 2)
         + cup(s, N3 + n2.d()) + cup(s, cup(cup(s, n2), n2, 2)) + cup(n2, n2))
    q = cup(b, b, 2) + cup(s.lift(), b.reduce(2).lift()) - A.lift()
    return (half(h(f)) + Fraction(q(f), 4)) % 1


def torsion_branch(x, s, w, f):
    """Section 5: n1 = s1.  Returns the six contributions."""
    n1, n2, n3 = x['n1'], x['n2'], x['n3']
    Z = F.stack(x, x, s, w)
    N1, N3 = Z['n1'], Z['n3']
    dn2, dn3, dN3 = n2.d(), n3.d(), N3.d()
    B = cup(n2, n2, 1)
    dB = B.d()
    c = cup(n2, dn2, 2)
    s2 = cup(s, s)
    beta = beta_open(n2)
    b = beta.reduce(2)

    def g(cochain, *i):
        return cochain(tuple(f[j] for j in i))
    out = {'c': half(cup(n3, n3, 2)(f)),
           'cgamma': half((cup(F.O4_majorana(n2, w, s), n3, 3)
                           + cup(N3, F.O4_gamma(s2, w, s), 3))(f))}
    cpsi = (cup(F.O4_psi(n1, w, s), n3, 3) + cup(N3, F.O4_psi(N1, w, s), 3)
            + cup(dB, n3, 3) + cup(n3, dB, 3) + cup(dB, B, 3) + dB
            + cup(N3 + dn2, dn2, 2) + cup(dn2, dN3, 3) + cup(dn2, n2, 1)
            + cup(B, c, 2) + cup(c, B, 2) + cup(c, c, 2))(f)
    cpsi += (dn3 + dB)(f) * (g(n2, 1, 2, 3) * g(dn2, 0, 1, 3, 4) + g(n2, 0, 1, 4) * g(dn2, 1, 2, 3, 4)
                            + g(n2, 2, 3, 4) * g(dn2, 0, 1, 2, 4))
    out['cpsi'] = half(cpsi)
    sn = cup(s, n2)
    gh = (op('123131', n2, n2, B) + cup(B, n2, 1) + cup(n2, B, 1) + cup(n2, cup(n2, B, 1), 2)
          + cup(b, b, 2) + cup(b, n2, 1) + cup(cup(n2, n2), cup(w, n2), 4)
          + cup(cup(n2, n2) + cup(w, n2), cup(s, b), 4) + cup(cup(w, s, 1), n2)
          + cup(B, sn, 2) + cup(s2, n2) + cup(s, cup(b, b, 3)) + cup(s, cup(sn, n2, 2)))(f)
    gh += g(n2, 0, 1, 2) * g(n2, 1, 2, 3) * g(n2, 2, 3, 4) * g(dn2, 0, 1, 3, 4)
    gq = cup(beta, beta, 2).scaled(-1) + cup(n2.lift(), n2.lift()) - cup(w.lift(), n2.lift())
    out['gamma'] = (half(gh) + Fraction(gq(f), 4)) % 1
    W = F.tilde_omega(w, s)
    bW = ds(W.lift(), s).div(2)
    b3psi = cup(W, s).lift() - cup(cup(s, W, 1), s).lift()
    b3 = beta + b3psi
    bWs = cup(bW, s.lift(), s=s, twists=(1, 1))
    values = {'n_2': n2, r'\omega_2': w, 's_1': s}
    mh = table_value('MIXED', values, f) + (
        cup(b3, dn2.lift(), 2) + ds(cup(beta, n2.lift(), 2), s) - cup(beta, n2.lift(), 1)
        + ds((B + c).lift(), s))(f)
    mq = (cup(beta, b3psi, 2).scaled(-1) - cup(b3psi, beta, 2) + cup(beta, bWs, 3)
          + cup(n2.lift() - s2.lift(), n2.lift().d(), 1)
          + cup(n2.lift(), s2.lift()) + cup(s2.lift(), n2.lift())
          + ds(cup(W, s).lift() - B.lift(), s))(f)
    out['gammapsi'] = (half(mh) - Fraction(mq, 4)) % 1
    second = C(3, fun=lambda face: (bW(face) >> 1) & 1)
    ph = table_value('PURE', values, f) + cup(s2, s2)(f)
    pq = (cup(b3psi, b3psi, 2).scaled(-1) + cup(b3psi, bWs, 3) - cup(w, s2).lift()
          - cup(second, s).lift())(f)
    out['psi'] = (half(ph) - Fraction(pq, 4) - Fraction(cup(W, s2).lift()(f), 8)) % 1
    return out
