"""Direct evaluation of the displayed 4+1D stacking corrections on the five-simplex (012345).

Every function below transcribes a display of the formula pages; the large
sums are read from the published coefficient files. The cochain operations
(cups, MS words, differentials, integer lifts and Bocksteins) are those of the
publication cochain library. Values are exact rationals modulo one.

  general_E5          FOUR_DIMENSIONAL.md, (T4c)-(T4d): E5^c + E5^{c gamma} + E5^{c psi}
                      + E5^gamma (with Theta_5 and the P-move phase) + E5^{gamma psi} + E5^psi
  self_E5             FOUR_DIMENSIONAL_SELF_STACKING.md (upper state = lower state)
  closed_E5           MAJORANA_AND_ENDPOINTS.md, (M3E) with (M3Ec), (M3Ecgamma), (M7)
  diagonal_E5         FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import gzip
import json
import os
import re
import sys

import numpy as np

ROOT = Path(__file__).resolve().parents[4]
DOCS = ROOT / 'docs/formulas'
COEF = DOCS / 'coefficients'
os.environ.setdefault('FULL4_CACHE_PATH', os.devnull)
for p in (ROOT, ROOT / 'formulas/publication_source/reference/d4_input/code',
          ROOT / 'formulas/publication_source/full4', ROOT / 'formulas/publication_source/bosonic'):
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))
from cochains import C, cup, sq, ds, op, background_data  # noqa: E402
from compact import beta_open, integer_inputs  # noqa: E402

TOP = tuple(range(6))


def at(c):
    return c(TOP)


def frac(x, den):
    return Fraction(int(x) % den, den)


def faces(V, q):
    return list(combinations(range(V), q + 1))


def carry(n):
    """[floor(n/2)]_2 of a signed integer cochain."""
    return (n - n.reduce(2).lift()).div(2).reduce(2)


# ---------------------------------------------------------------- lower layers (formula pages)
def zeta22(x, y):
    return op('1231343', x, x, y, y)


def O4(n, w, s):
    a = n.reduce(2)
    return cup(a, a) + cup(w + cup(s, s), a)


def O5_gamma(u, w, s):
    return cup(u, u, 1) + cup(s, cup(u, u, 2)) + cup(w, u)


def O5_gammapsi(u, s):
    du = u.d()
    return cup(du, u, 2) + cup(s, cup(u, du, 3))


def O5_psi(n, w, s):
    a, h = n.reduce(2), carry(n)
    W = w + cup(s, s)
    aa, Wa, W1W = cup(a, a), cup(W, a), cup(W, W, 1)
    return (zeta22(a, a) + cup(h, cup(a, a, 1)) + cup(s, cup(h, a)) + zeta22(W, a)
            + cup(W1W + cup(s, W), h) + cup(cup(W1W, s, 1) + cup(s, cup(s, W, 1)), a)
            + cup(aa, Wa, 3) + cup(s, cup(aa, Wa, 4)))


def O5(n, u, w, s):
    return O5_gamma(u, w, s) + O5_gammapsi(u, s) + O5_psi(n, w, s)


def bracket_E4psi(a, h, s):
    """The polynomial inside the last bracket of E4^psi."""
    t = cup(a, a, 1)
    return cup(cup(s, h, 1), a) + cup(s, cup(t, a, 2)) + op('12131', t, s, a)


def ell3(x, y):
    return C(3, fun=lambda f: (x((f[0], f[2], f[3])) * y(f[:3])
                               * (1 + x((f[0], f[1], f[3])) * y(f[1:]))) % 2)


def E4_parts(n, u, m, v, w, s):
    a, b, h, k = n.reduce(2), m.reduce(2), carry(n), carry(m)
    W = w + cup(s, s)
    E3, r = cup(a, b, 1), cup(a, b, 2)
    g = cup(u, v, 2) + cup(s, cup(u, v, 3))
    gp = cup(u, v.d(), 3) + cup(E3, u + v, 2) + cup(s, cup(u + v, E3, 3))
    z4 = (op('12413423', a, a, a, b) + op('12314132', a, a, b, b) + op('12314324', a, a, b, b)
          + op('12341321', a, a, b, b) + op('12132413', a, b, b, b) + op('12324214', a, b, b, b))
    p = (z4 + cup(cup(W, a + b), E3, 3) + cup(cup(W, a, 2), b + r) + cup(cup(W, b, 2), a)
         + cup(h, k + b) + cup(a, k) + cup(h.d(), k, 1) + cup(h + k, r)
         + cup(cup(s, a), cup(b, b, 1), 2) + cup(a, cup(s, b), 1) + cup(r, cup(s, a + b), 1)
         + cup(s, cup(s, r) + cup(a, k.d(), 2) + cup(r, a + b, 1) + ell3(a, b)) + cup(E3, E3, 2)
         + bracket_E4psi(a + b, h + k + r, s) + bracket_E4psi(a, h, s) + bracket_E4psi(b, k, s))
    return g, gp, p


def B5(u, w, s):
    """Four times B5[u] (FOUR_DIMENSIONAL_MAJORANA_PHASE.md)."""
    import physical
    return physical.B5(u, w, s)


# ---------------------------------------------------------------- coefficient tables
ARGN = {'n_2': 'n', "n'_2": 'm', '\\check n_3': 'u', "\\check n'_3": 'v', '\\omega_2': 'w', 's_1': 's'}


class Table:
    """A published coefficient sum mod 2, evaluated with the operations of the formula pages."""

    def __init__(self, directory):
        directory = Path(directory)
        index = json.loads((directory / 'INDEX.json').read_text())
        factors, terms = [], []
        for entry in index['files']:
            raw = (directory / entry['file']).read_bytes()
            if entry['file'].endswith('.gz'):
                raw = gzip.decompress(raw)
            (factors if entry['kind'] == 'factors' else terms).extend(json.loads(raw))
        self.F = factors
        width = max(len(t) for t in terms)
        M = np.full((len(terms), max(width, 1)), len(factors), dtype=np.int32)
        for i, t in enumerate(terms):
            M[i, :len(t)] = t
        self.M = M

    def value(self, fields):
        val = np.zeros(len(self.F) + 1, dtype=np.uint8)
        val[len(self.F)] = 1
        cache = {}
        for f in self.F:
            kind = f['kind']
            if kind == 'physical_face':
                x = fields[ARGN[f['cochain']]](tuple(f['face']))
                val[f['id']] = (x // (1 << f.get('binary_digit', 0))) % 2
            elif kind.startswith('standard_'):
                key = (f['operation'], f.get('ordinary_differential'), f.get('binary_digit'), f['degree'],
                       tuple((a['cochain'], tuple(a['face']), a['precision_bits'],
                              sum(c * int(all(val[i] for i in ids)) for c, ids in a['terms'])
                              % (1 << a['precision_bits'])) for a in f['arguments']))
                if key not in cache:
                    cache[key] = standard_operation(*key)
                val[f['id']] = cache[key]
            else:
                total = sum(c * int(all(val[i] for i in ids)) for c, ids in f['numerator'])
                val[f['id']] = (total // f['divisor']) % 2
        return int(val[self.M].prod(axis=1, dtype=np.uint8).sum() % 2)


def standard_operation(name, derivative, digit, degree, args):
    arrays = {}
    for field, face, bits, value in args:
        arrays.setdefault(field, {})[face] = value
    w = C(2, values=arrays.get('\\omega_2', {}))
    s = C(1, values=arrays.get('s_1', {}))
    w.closed = s.closed = True
    g = C(3, values=arrays.get('\\check n_3', {}))
    gp = C(3, values=arrays.get("\\check n'_3", {}))
    n = C(2, values=arrays.get('n_2', {}), mod=None)
    m = C(2, values=arrays.get("n'_2", {}), mod=None)
    n.closed = m.closed = True
    top = tuple(range(degree + 1))
    if name in ('B_4', 'B_4^\\psi', '\\beta^\\circ', '\\lambda_3', '\\lambda_3^\\gamma'):
        if name == '\\beta^\\circ':
            o = beta_open(g)
        elif name in ('B_4', 'B_4^\\psi'):
            o = integer_inputs(n, w, s)[1]
            if name == 'B_4':
                o = o + beta_open(g)
        elif name == '\\lambda_3^\\gamma':
            o = cup(g, gp, 3)
        else:
            U = g + gp + cup(n.reduce(2), m.reduce(2), 1)
            o = (U.lift() - g.lift() - gp.lift() + cup(n, m, 1, s=s, twists=(1, 1))).div(2).reduce(2)
        if derivative:
            o = o.d()
        return (o(top) // (1 << digit)) % 2
    assert not derivative
    if name == '\\mathcal E_4^\\gamma':
        o = cup(g, gp, 2) + cup(s, cup(g, gp, 3))
    elif name == '\\mathcal E_4':
        x, y, z = E4_parts(n, g, m, gp, w, s)
        o = x + y + z
    elif name == '\\mathcal O_5^\\gamma':
        o = O5_gamma(g, w, s)
    elif name == '\\check{\\mathcal O}_4':
        o = O4(n, w, s)
    elif name == '\\mathcal O_5^\\psi':
        o = O5_psi(n, w, s)
    else:
        raise ValueError(name)
    return o(top) % 2


# ---------------------------------------------------------------- Majorana contribution (eq. 33)
def _words():
    text = (DOCS / 'FOUR_DIMENSIONAL_MAJORANA_STACKING_WORDS.md').read_text()
    out = []
    for block in text.split('## Block ')[1:]:
        args = re.search(r'```math\n\((.*?)\)\.\n```', block, re.S).group(1)
        args = [x.strip() for x in re.split(r',(?![^\[]*\])', args)]
        for word in re.search(r'```text\n(.*?)\n```', block, re.S).group(1).split():
            out.append((word, args))
    assert len(out) == 455
    return out


WORDS = _words()
LIFTS = json.loads((COEF / 'FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.json').read_text())['rows']
REPHASING = json.loads((COEF / 'FOUR_DIMENSIONAL_MAJORANA_STACKING_REPHASING.json').read_text())['terms']


def b4(u, v, w, s):
    names = {'n_3': u, "n'_3": v, '\\omega_2': w, 's_1': s}

    def value(face):
        total = 0
        for row in REPHASING:
            p = 1
            for x in row:
                p *= names[x['cochain']](tuple(face[i] for i in x['face']))
                if not p:
                    break
            total += p
        return total % 2
    return C(4, fun=value)


def S(x):
    return cup(x, x, 2)


def K5(x, w, s):
    return O5_gamma(x, w, s) + O5_gammapsi(x, s)


def Theta5(u, v, w, s):
    E4g = cup(u, v, 2) + cup(s, cup(u, v, 3))
    L = cup(u, v, 3)
    dL, N = L.d(), u + v
    t = (cup(S(u), S(v), 3) + cup(S(u) + S(v), E4g + cup(u, v.d(), 3) + cup(u, v, 2) + cup(v, u, 2) + dL, 3)
         + cup(K5(u, w, s) + S(u).d(), S(v), 4) + cup(S(u), K5(v, w, s), 4)
         + cup(E4g + cup(u, v.d(), 3), S(N) + dL, 3) + cup(S(N), dL, 3)
         + cup(dL, K5(N, w, s) + S(N).d(), 4) + sq(L, 2) + cup(w, L))
    for x in (N, u, v):
        t = t + cup(s, S(x)) + cup(S(x), K5(x, w, s), 4) + cup(S(x), K5(x, w, s).d(), 5)
    return t


def E5_gamma(u, v, w, s):
    du, dv = u.d(), v.d()
    bu, bv = beta_open(u).reduce(2), beta_open(v).reduce(2)
    f = {"n_3": u, "n'_3": v, "s_1": s, "\\omega_2": w, "[\\beta^-n_3]_2": bu, "[\\beta^-n'_3]_2": bv,
         "[dn_3]_2": du, "[dn'_3]_2": dv, "d[\\beta^-n_3]_2": bu.d(), "d[\\beta^-n'_3]_2": bv.d()}
    I = C(5)
    for word, args in WORDS:
        I = I + op(word, *[f[x] for x in args])
    l3, l4 = cup(u, v, 3), cup(du, dv, 4)
    E4g = cup(u, v, 2) + cup(s, cup(u, v, 3))
    half = (at(I) + at(cup(s, cup(bu + bv, l3, 3))) + l4((1, 2, 3, 4, 5)) * l3((0, 1, 4, 5))
            + l4((0, 1, 2, 3, 5)) * l3((0, 3, 4, 5)) + at(cup(s, E4g)))
    B4, B4p = beta_open(u), beta_open(v)
    lam3, lam4 = l3.lift().scaled(-1), l4.lift().scaled(-1)
    dB4, dB4p = B4.d(), B4p.d()
    q = (cup(B4, B4p, 3) - cup(B4 + B4p, lam3, 2) + cup(lam3, beta_open(u + v), 2) + cup(lam3, lam3, 1)
         + cup(w.lift(), lam3) - cup(dB4 + dB4p, lam3, 3) + cup(lam3, lam4, 2) + cup(dB4, B4p, 4)
         + cup(dB4 + dB4p, lam3.d(), 4) - cup(B4 + B4p + lam3.d(), lam4, 3))
    L = lam4
    quarter = (at(q) - L((0, 1, 2, 3, 5)) * L((0, 1, 3, 4, 5)) + L((0, 2, 3, 4, 5)) * L((0, 1, 2, 4, 5))
               - L((0, 1, 2, 3, 5)) * L((1, 2, 3, 4, 5)) - L((0, 1, 3, 4, 5)) * L((1, 2, 3, 4, 5)))
    g = {'\\overline{d\\check n_3}': du, "\\overline{d\\check n'_3}": dv, '\\check n_3': u, "\\check n'_3": v,
         '\\bar B_4^\\gamma': bu, '\\bar B_4^{\\gamma\\prime}': bv}
    for row in LIFTS:
        x = 0
        for term in row['terms']:
            p = 1
            for y in term:
                p *= g[y['cochain']](tuple(y['face']))
                if not p:
                    break
            x ^= p
        quarter += row['coefficient'] * x
    rephase = b4(u, v, w, s).lift().scaled(2) + cup(u.lift(), v.lift(), 2)
    return (frac(half, 2) + frac(quarter, 4)
            + frac(-at(B5(u + v, w, s)) + at(B5(u, w, s)) + at(B5(v, w, s)), 4)
            + frac(at(Theta5(u, v, w, s)), 2) + frac(at(ds(rephase, s)), 4)) % 1


# ---------------------------------------------------------------- quarter numerators (eqs. 41-43)
def V5_parts(n, u, m, v, w, s):
    a, b, h, k = n.reduce(2), m.reduce(2), carry(n), carry(m)
    W = w + cup(s, s)
    E3 = cup(a, b, 1)
    bg, bgp = beta_open(u).reduce(2), beta_open(v).reduce(2)
    bp, bpp = integer_inputs(n, w, s)[1].reduce(2), integer_inputs(m, w, s)[1].reduce(2)
    lg, lm = cup(u, v, 3), cup(u + v, E3, 3)
    lp = (E3.lift() + cup(n, m, 1, s=s, twists=(1, 1))).div(2).reduce(2)
    ba = cup(b, a)
    _, _, alpha, hw, _ = background_data(w, s)
    Vg = (cup(bg, bgp, 3) + cup(bg.d(), bgp, 4) + cup(bg + bgp, lg.d(), 3) + cup(bg.d() + bgp.d(), lg.d(), 4)
          + sq(lg, 2) + cup(w, lg))
    Vm = (cup(bg, bpp, 3) + cup(bg.d(), bpp, 4) + cup(bp, bgp, 3) + cup(bp.d(), bgp, 4)
          + cup(bg + bgp, (lm + lp).d() + ba, 3) + cup(bg.d() + bgp.d(), (lm + lp).d() + ba, 4)
          + cup(bp + bpp, (lg + lm).d(), 3) + cup(bp.d() + bpp.d(), (lg + lm).d(), 4)
          + sq(lm, 2) + cup(ba, (lg + lm).d(), 3) + cup(w, lm) + cup(v, a) + cup(b, u))
    for x, y in ((lg, lm), (lg, lp), (lm, lp)):
        Vm = Vm + cup(x, y, 2).d() + cup(x.d(), y, 3).d() + cup(x.d(), y.d(), 3)
    Vp = (cup(bp, bpp, 3) + cup(bp.d(), bpp, 4) + cup(bp + bpp, lp.d() + ba, 3) + cup(bp.d() + bpp.d(), lp.d() + ba, 4)
          + sq(lp, 2) + cup(ba, lp.d(), 3) + cup(w, lp) + cup(hw + alpha, cup(a, b, 2))
          + op('1231343', b, b, a, a) + cup(cup(W, b, 1), a) + cup(k, cup(a, a, 1)) + cup(cup(s, b), h)
          + cup(cup(s, cup(b, s, 1)), a))
    return Vg, Vm, Vp


# ---------------------------------------------------------------- general law
class General:
    def __init__(self):
        self.Tgp = Table(COEF / 'FOUR_DIMENSIONAL_STACKING/gamma_psi')
        self.Tp = Table(COEF / 'FOUR_DIMENSIONAL_STACKING/psi')

    def parts(self, n, u, c, m, v, cp, w, s):
        a, b = n.reduce(2), m.reduce(2)
        W = w + cup(s, s)
        E3, ab = cup(a, b, 1), cup(a, b)
        NN, U = n + m, u + v + cup(a, b, 1)
        Eg, Egp, Ep = E4_parts(n, u, m, v, w, s)
        E4 = Eg + Egp + Ep
        N4 = c + cp + E4
        G, Gp, GN = (O5_gamma(x, w, s) + O5_gammapsi(x, s) for x in (u, v, U))
        P, Pp, PN = O5_psi(n, w, s), O5_psi(m, w, s), O5_psi(NN, w, s)
        out = {}
        out['c'] = frac(at(cup(c, cp, 3) + cup(c + cp, E4, 3)), 2)
        out['c_gamma'] = frac(at(cup(G, cp, 4) + cup(N4, GN, 4) + cup(c, G, 4) + cup(cp, Gp, 4)), 2)
        out['c_psi'] = frac(at(cup(P, cp, 4) + cup(N4, PN, 4) + cup(c, P, 4) + cup(cp, Pp, 4)), 2)
        out['gamma'] = E5_gamma(u, v, w, s)
        fields = dict(n=n, m=m, u=u, v=v, w=w, s=s)
        Vg, Vm, Vp = V5_parts(n, u, m, v, w, s)
        h, k = carry(n), carry(m)
        half = (self.Tgp.value(fields) + at(cup(Eg + Egp, ab, 3)) + at(cup(GN, ab, 4))
                + at(cup(a + b, cup(u, v, 3) + cup(u + v, E3, 3)))
                + at(cup(Vg, Vm, 5)) + at(cup(Vg, Vp, 5)) + at(cup(Vm, Vp, 5)) + at(cup(s, Egp)))
        quarter = at(Vm) + at(cup(n, v.lift(), s=s, twists=(1, 0))) + at(cup(m, u.lift(), s=s, twists=(1, 0)))
        out['gamma_psi'] = (frac(half, 2) + frac(quarter, 4)
                            + frac(-at(B5(U, w, s)) + at(B5(u + v, w, s)) + at(B5(E3, w, s)), 4)) % 1
        half = (self.Tp.value(fields) + at(cup(Ep + ab, ab, 3)) + at(cup(PN, ab, 4)) + at(zeta22(a, b))
                + at(cup(a, cup(b, b) + cup(W, b), 1)) + at(cup(h, cup(b, b, 1))) + at(cup(cup(W, a, 1), b))
                + at(cup(s, cup(a, k))) + at(cup(cup(s, cup(a, s, 1)), b)) + at(cup(E3, a + b)) + at(cup(W, E3))
                + at(cup(s, Ep)))
        nq = cup(n, m, 1, s=s, twists=(1, 1))
        quarter = (at(Vp) + at(cup(NN, E3.lift(), s=s, twists=(1, 0)))
                   + at(cup(cup(n, W.lift(), 1, s=s, twists=(1, 1)), m, s=s, twists=(0, 1)))
                   + at(cup(cup(m, W.lift(), 1, s=s, twists=(1, 1)), n, s=s, twists=(0, 1))))
        out['psi'] = (frac(half, 2) + frac(quarter, 4) + frac(at(cup(W.lift(), nq, s=s, twists=(1, 0))), 8)
                      + frac(at(cup(m - n, nq, s=s, twists=(1, 0)) - cup(nq, m - n, s=s, twists=(0, 1))), 3)
                      - frac(at(B5(E3, w, s)), 4)) % 1
        return out

    def E5(self, *fields):
        return sum(self.parts(*fields).values()) % 1


# ---------------------------------------------------------------- self-stacking
SELF = COEF / 'FOUR_DIMENSIONAL_SELF_STACKING'
SELF_WORDS = json.loads((SELF / 'OPEN_GAMMA_DIAGONAL_WORDS.json').read_text())['terms']
SELF_LIFTS = json.loads((SELF / 'OPEN_GAMMA_DIAGONAL_LIFTS.json').read_text())['rows']


def self_gamma(n, u, w, s):
    du, bg = u.d(), beta_open(u).reduce(2)
    f = {'\\check n_3': u, 's_1': s, '\\omega_2': w, '\\overline{d\\check n_3}': du,
         '\\overline{\\beta^\\circ\\check n_3}': bg, 'd\\overline{\\beta^\\circ\\check n_3}': bg.d()}
    I = C(5)
    for t in SELF_WORDS:
        I = I + op(t['word'], *[f[x] for x in t['inputs']])
    E4g = cup(u, u, 2) + cup(s, u)
    half = at(I) + du((1, 2, 3, 4, 5)) * u((0, 1, 4, 5)) + du((0, 1, 2, 3, 5)) * u((0, 3, 4, 5)) + at(cup(u, u, 1)) + at(cup(s, E4g))
    bO4 = O4(n, w, s).lift().d().div(2)
    B4 = beta_open(u)
    q = (cup(B4, B4, 3) + cup(u.lift(), u.lift(), 1) - cup(w.lift(), u.lift()) + cup(u.lift(), du.lift(), 2)
         - cup(bO4, B4, 4))
    quarter = at(q) - du((0, 1, 2, 3, 4)) * du((0, 1, 2, 4, 5)) - du((0, 1, 2, 3, 4)) * du((0, 2, 3, 4, 5))
    g = {'\\overline{d\\check n_3}': du, '\\check n_3': u, '\\bar B_4^\\gamma': bg}
    for row in SELF_LIFTS:
        x = 0
        for term in row['terms']:
            p = 1
            for y in term:
                p *= g[y['cochain']](tuple(y['face']))
                if not p:
                    break
            x ^= p
        quarter += row['coefficient'] * x
    Sx, K = S(u), K5(u, w, s)
    theta = cup(Sx, Sx, 3) + cup(K + Sx.d(), Sx, 4) + cup(Sx, K, 4) + cup(Sx + cup(s, u) + cup(u, du, 3), du, 3) + sq(u, 2) + cup(w, u)
    rephase = b4(u, u, w, s).lift().scaled(2) + cup(u.lift(), u.lift(), 2)
    return (frac(half, 2) + frac(quarter, 4) + frac(at(theta), 2) + frac(at(ds(rephase, s)), 4)) % 1


def self_V5(n, u, w, s):
    a, h = n.reduce(2), carry(n)
    W = w + cup(s, s)
    N3 = cup(a, a, 1)
    bg, bp = beta_open(u).reduce(2), integer_inputs(n, w, s)[1].reduce(2)
    lp = (N3.lift() + cup(n, n, 1, s=s, twists=(1, 1))).div(2).reduce(2)
    du, a2 = u.d(), cup(a, a)
    _, _, alpha, hw, _ = background_data(w, s)
    Vg = sq(bg, 1) + bg.d() + sq(u, 2) + cup(w, u)
    Vm = ((cup(bg, bp, 4) + cup(u, lp, 2) + cup(du, lp, 3) + cup(u, a, 1)).d() + cup(bg.d(), bp.d(), 5)
          + cup(du, lp.d(), 3) + cup(a2, du, 3) + cup(du, a, 1))
    Vp = (sq(bp, 1) + bp.d() + sq(lp, 2) + cup(a2, lp.d(), 3) + cup(w, lp) + cup(hw + alpha, a)
          + op('1231343', a, a, a, a) + cup(cup(W, a, 1), a) + cup(h, N3) + cup(s, cup(a, h))
          + cup(cup(s, cup(a, s, 1)), a))
    return Vg, Vm, Vp


class Self:
    def __init__(self):
        self.Tgp = Table(SELF / 'gamma_psi')
        self.Tp = Table(SELF / 'psi')

    def parts(self, n, u, c, w, s):
        a, h = n.reduce(2), carry(n)
        W = w + cup(s, s)
        N3, a2 = cup(a, a, 1), cup(a, a)
        Eg, Egp, Ep = E4_parts(n, u, n, u, w, s)
        N4 = Eg + Egp + Ep
        _, _, alpha, _, _ = background_data(w, s)
        out = {'c': frac(at(cup(c, c, 3)), 2),
               'c_gamma': frac(at(cup(K5(u, w, s), c, 4) + cup(N4, O5_gamma(N3, w, s), 4)), 2),
               'c_psi': frac(at(cup(O5_psi(n, w, s), c, 4) + cup(N4, cup(alpha, a), 4)), 2),
               'gamma': self_gamma(n, u, w, s)}
        fields = dict(n=n, m=n, u=u, v=u, w=w, s=s)
        Vg, Vm, Vp = self_V5(n, u, w, s)
        half = (self.Tgp.value(fields) + at(cup(Eg + Egp, a2, 3)) + at(cup(O5_gamma(N3, w, s), a2, 4))
                + at(cup(Vg, Vm, 5)) + at(cup(Vg, Vp, 5)) + at(cup(Vm, Vp, 5)) + at(cup(a, u)) + at(cup(s, Egp)))
        out['gamma_psi'] = (frac(half, 2) + frac(at(Vm), 4)) % 1
        half = (self.Tp.value(fields) + at(cup(Ep + a2, a2, 3)) + at(cup(cup(alpha, a), a2, 4))
                + at(op('1231343', a, a, a, a)) + at(cup(a, O4(n, w, s), 1)) + at(cup(h, N3))
                + at(cup(cup(W, a, 1), a)) + at(cup(s, cup(a, h))) + at(cup(cup(s, cup(a, s, 1)), a))
                + at(cup(W, N3)) + at(cup(a, N3)) + at(cup(cup(a, W, 1), a)) + at(cup(s, Ep)))
        nq = cup(n, n, 1, s=s, twists=(1, 1))
        out['psi'] = (frac(half, 2) + frac(at(Vp), 4) + frac(at(cup(W.lift(), nq, s=s, twists=(1, 0))), 8)
                      - frac(at(B5(N3, w, s)), 4)) % 1
        return out

    def E5(self, *fields):
        return sum(self.parts(*fields).values()) % 1


# ---------------------------------------------------------------- closed sector and diagonal
W1 = ('12131432412', '12343213431', '23412342324')
W2 = ('12123434123', '12131412324', '12134131234', '12312412423', '12314324123', '12314342413',
      '13242412314', '13412321341', '13412321413', '13413142134', '13432412314', '31214124324')
W5 = ('12131432412', '12343213431', '12341231213', '12123434123', '12131412324', '12134131234',
      '12312412423', '12314324123', '12314342413', '12343413214', '12314241231', '12314241312',
      '12312134123', '12324314213', '12324234134', '12314342412')


def beta(x):
    return x.lift().d().div(2)


def Sq1(x):
    return beta(x).reduce(2)


def beta_plus(x):
    p = beta(x)
    return (p + p.reduce(2).lift()).div(2)


def z50(x, y):
    t = C(5)
    for v in W1:
        t = t + op(v, x, y, y, y)
    for v in W2:
        t = t + op(v, x, x, y, y)
    xy = x + y
    return (t + op('12413432312', x, x, x, y) + op('12131432412', y, x, x, xy) + op('12131432412', xy, x, x, y)
            + op('12131432412', xy, y, y, x) + op('12134341321', xy, y, y, x) + op('1212312', xy, y, cup(x, y, 3))
            + op('12313123', y, x, cup(x, y, 2)) + op('12131232', Sq1(x), y, y) + op('123131212', cup(y, y, 1), x, xy)
            + op('123131212', cup(xy, xy, 1), y, x) + cup(cup(x, y, 2), y, 2) + cup(Sq1(x) + Sq1(y), cup(x, y, 3), 2)
            + cup(cup(x, y, 3), Sq1(x) + Sq1(y) + cup(y, x, 2), 2) + cup(cup(x, y, 2), cup(x, x, 1) + cup(y, y, 1), 4)
            + cup(y, cup(x, cup(x, y, 2), 2), 3) + cup(Sq1(y), Sq1(x), 3))


def z5_gamma(u, v, w, s):
    N = u + v
    E4 = cup(u, v, 2) + cup(s, cup(u, v, 3))
    u4 = cup(u, v, 3)
    su4 = cup(s, u4)
    bp = (beta_plus(N) - beta_plus(u) - beta_plus(v)).reduce(2)
    return (z50(u, v) + cup(cup(w, N), E4, 4) + cup(cup(u, v, 2).d(), cup(w, N), 5) + cup(cup(v, v, 1), cup(w, u), 5)
            + cup(cup(v, v, 1) + cup(w, v), cup(s, Sq1(u)), 5) + cup(cup(w, s, 1), u4)
            + cup(cup(u, v, 2), cup(s, Sq1(u) + Sq1(v)), 4) + cup(cup(N, N, 1), su4, 4) + cup(cup(u, v, 2), su4, 3)
            + cup(s, E4 + cup(Sq1(u), Sq1(v), 4) + cup(u4, u4, 2) + cup(Sq1(u) + Sq1(v), su4, 4) + cup(su4, u4, 3) + bp))


def closed_E5(u, c, v, cp, w, s):
    """(M3E) = (M3Ec) + (M3Ecgamma) + (M7) on closed n3, n3'."""
    E4 = cup(u, v, 2) + cup(s, cup(u, v, 3))
    N4 = c + cp + E4
    half = cup(c, cp, 3) + cup(c + cp, E4, 3) + cup(c.d(), cp, 4) + cup(N4, N4.d(), 4) + cup(c, c.d(), 4) + cup(cp, cp.d(), 4)
    u4 = cup(u, v, 3).lift()
    q = cup(beta(u), beta(v), 3) - cup(beta(u) + beta(v), u4, 2) - cup(u4, beta(u + v), 2) + cup(u4, u4, 1) - cup(w.lift(), u4)
    return (frac(at(half), 2) + frac(at(z5_gamma(u, v, w, s)), 2) - frac(at(q), 4)) % 1


def z5_self(x, w, s):
    r, sx = Sq1(x), cup(s, x)
    t = C(5)
    for v in W5:
        t = t + op(v, x, x, x, x)
    return (t + op('12313123', x, x, r) + op('12131232', r, x, x) + cup(r, x, 2) + cup(x, r, 2) + cup(x, cup(x, r, 2), 3)
            + cup(r, r, 3) + cup(cup(x, x, 1), cup(w, x), 5) + cup(cup(x, x, 1) + cup(w, x), cup(s, r), 5)
            + cup(cup(w, s, 1), x) + cup(r, sx, 3) + cup(s, cup(s, x) + cup(r, r, 4) + cup(sx, x, 3)))


def diagonal_E5(x, c, w, s):
    half = z5_self(x, w, s) + cup(beta(x).reduce(2), x, 2) + cup(c, c, 3) + cup(c.d(), c, 4)
    q = cup(beta(x), beta(x), 3) + cup(x.lift(), x.lift(), 1) - cup(w.lift(), x.lift())
    return (frac(at(half), 2) - frac(at(q), 4)) % 1
