"""The 3+1D formulas of docs/formulas/THREE_DIMENSIONAL.md on an ordered simplex.

Every function takes cochains of the reference engine
(formulas/publication_source/reference/d4_input/code/cochains.py) and returns
a cochain, or a phase modulo one as a Fraction.  The fields are the physical
decorations of the formula page: n1 (integer, Z_s1), n2, n3 (binary), and the
backgrounds s1, omega2.

The complex-fermion and Majorana contributions are transcribed directly from
the page.  The finite word sums and integer terms of the mixed and p+ip
contributions are read from the term manifests in
docs/formulas/term_census/three_dimensional, whose input names are the
expressions printed on the page; the explicit terms that the page adds to
them are written out below.
"""
from __future__ import annotations

import json
import sys
from fractions import Fraction
from functools import lru_cache
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
ENGINE = ROOT / 'formulas/publication_source/reference/d4_input/code'
MANIFESTS = ROOT / 'docs/formulas/term_census/three_dimensional'
for path in (ENGINE, MANIFESTS):
    if str(path) not in sys.path:
        sys.path.insert(0, str(path))

from cochains import C, cup, op, ds  # noqa: E402
from compact import beta_open  # noqa: E402
from verify_manifests import interval_faces  # noqa: E402


def half(cochain, face):
    return Fraction(cochain(face) % 2, 2)


def digit(n, k):
    """Binary digit [floor(n/2^k)]_2 of an integer cochain (mathematical floor)."""
    return C(n.deg, fun=lambda f: (n(f) >> k) & 1)


def tilde_omega(w, s):
    return w + cup(s, s)


# Lower obstructions -------------------------------------------------------

def O3(n1, w, s):
    return cup(tilde_omega(w, s), n1.reduce(2))


def O4_gamma(n2, w, s):
    return cup(n2, n2) + cup(s, cup(n2, n2, 1)) + cup(w, n2)


def O4_gammapsi(n2, s):
    dn2 = n2.d()
    return cup(dn2, n2, 1) + cup(s, cup(n2, dn2, 2))


def O4_psi(n1, w, s):
    W, a, h = tilde_omega(w, s), n1.reduce(2), digit(n1, 1)
    W11 = cup(W, W, 1)
    zeta = C(4, fun=lambda f: W((f[0], f[1], f[2])) * W((f[0], f[2], f[3]))
             * a((f[2], f[3])) * a((f[3], f[4])))
    return (zeta + cup(W11 + cup(s, W), h)
            + cup(cup(W11, s, 1) + cup(s, cup(s, W, 1)), a))


def O4_majorana(n2, w, s):
    """The Majorana and mixed parts, O4^gamma + O4^{gamma psi}."""
    return O4_gamma(n2, w, s) + O4_gammapsi(n2, s)


def O4(n1, n2, w, s):
    return O4_majorana(n2, w, s) + O4_psi(n1, w, s)


# Lower stacking -----------------------------------------------------------

def E2(n1, m1):
    return cup(n1.reduce(2), m1.reduce(2))


def E3(n1, n2, m1, m2, s):
    a, b, h = n1.reduce(2), m1.reduce(2), digit(n1, 1)
    e = E2(n1, m1)
    gamma = cup(n2, m2, 1) + cup(s, cup(n2, m2, 2))
    mixed = cup(n2, m2.d(), 2) + cup(n2 + m2, e, 1) + cup(s, cup(n2 + m2, e, 2))
    psi = cup(cup(a, e, 1), b) + cup(h, cup(b, b)) + cup(s, cup(h, b))
    return gamma + mixed + psi


def stack(x, y, s, w):
    """Output (N1, N2, N3) of the lower stacking laws."""
    N1 = x['n1'] + y['n1']
    N2 = x['n2'] + y['n2'] + E2(x['n1'], y['n1'])
    N3 = x['n3'] + y['n3'] + E3(x['n1'], x['n2'], y['n1'], y['n2'], s)
    return dict(n1=N1, n2=N2, n3=N3)


# Manifest contributions ---------------------------------------------------

def _alphabet(x, y, s, w):
    """Every input expression of the manifests, by its printed name."""
    W = tilde_omega(w, s)
    bW = ds(W.lift(), s).div(2)
    vW = bW.reduce(2)
    A = {r'\omega_2': w, 's_1': s, r'\widetilde{\omega}_2': W,
         r'[\beta\omega_2]_2': w.lift().d().div(2).reduce(2),
         r'\beta_{s_1}\widetilde{\omega}_2': bW,
         r'[\beta_{s_1}\widetilde{\omega}_2]_2': vW}
    second = C(3, fun=lambda f: (bW(f) >> 1) & 1)

    def layer(X, p):
        n1, n2 = X['n1'], X['n2']
        a, b = n1.reduce(2), beta_open(n2)
        carry = (cup(W, a).lift() + cup(W.lift(), n1, s=s, twists=(1, 1))).div(2)
        return {rf'n{p}_1': n1, rf'n{p}_2': n2, rf'[n{p}_1]_2': a,
                rf'[\lfloor n{p}_1/2\rfloor]_2': digit(n1, 1),
                rf'[\lfloor n{p}_1/4\rfloor]_2': digit(n1, 2),
                rf'\beta^-n{p}_2': b, rf'[\beta^-n{p}_2]_2': b.reduce(2),
                rf'[\widetilde{{\omega}}_2[n{p}_1]_2]_2': cup(W, a),
                rf'[\frac{{[\widetilde{{\omega}}_2[n{p}_1]_2]_2+\widetilde{{\omega}}_2n{p}_1}}{{2}}]_2':
                    carry.reduce(2)}

    A.update(layer(x, ''))
    a, h = x['n1'].reduce(2), digit(x['n1'], 1)
    A[r'[([\beta_{s_1}\widetilde{\omega}_2]_2\cup_2[\beta_{s_1}\widetilde{\omega}_2]_2)[n_1]_2'
      r'+s_1[\beta_{s_1}\widetilde{\omega}_2]_2[\lfloor n_1/2\rfloor]_2'
      r'+s_1(s_1\cup_1[\beta_{s_1}\widetilde{\omega}_2]_2)[n_1]_2]_2'] = (
        cup(cup(vW, vW, 2), a) + cup(cup(s, vW), h) + cup(cup(s, cup(s, vW, 1)), a))
    A[r'[\lfloor\beta_{s_1}\widetilde{\omega}_2/2\rfloor]_2[n_1]_2^2'] = cup(second, cup(a, a))
    if y is not None:
        A.update(layer(y, "'"))
        n2, m2 = x['n2'], y['n2']
        M, ab = n2 + m2, cup(a, y['n1'].reduce(2))
        bM = beta_open(M)
        A[r"\beta^-[n_2+n'_2]_2"] = bM
        A[r"[n_2+n'_2]_2"] = M
        A[r"[n_2\cup_1n'_2]_2"] = cup(n2, m2, 1)
        A[r"[n_1]_2[n'_1]_2"] = ab
        A[r"[n_2+n'_2+[n_1]_2[n'_1]_2]_2"] = M + ab
        A[r"[\lfloor\beta_{s_1}\widetilde{\omega}_2/2\rfloor]_2([n_1]_2\cup_1[n'_1]_2)"] = (
            cup(second, cup(a, y['n1'].reduce(2), 1)))
        bn, bm = beta_open(n2), beta_open(m2)
        num = (bM + bM.reduce(2).lift() - bn - bn.reduce(2).lift() - bm - bm.reduce(2).lift())
        A[r"[\frac{\beta^-[n_2+n'_2]_2+[\beta^-[n_2+n'_2]_2]_2-\beta^-n_2-[\beta^-n_2]_2"
          r"-\beta^-n'_2-[\beta^-n'_2]_2}{2}]_2"] = num.div(2).reduce(2)
    return A


# Integer leaves with Z_s1 coefficients.  In [omega~ [n1]_2] the product is the
# canonical 0/1 lift of a binary cochain, so that cup is untwisted.
TWISTED = {'n_1', "n'_1", r'\beta_{s_1}\widetilde{\omega}_2', r'\widetilde{\omega}_2'}
BINARY_DIGITS = {'[n_1]_2', "[n'_1]_2"}


def _leaf(A, key):
    c = A[key]
    return c if c.mod is None else c.lift()


def _integer(e, A, s):
    if 'physical_expression' in e:
        key = e['physical_expression']
        return _leaf(A, key), int(key in TWISTED)
    operation = e['operation']
    if operation == 'integer_cup':
        keys = {arg.get('physical_expression') for arg in e['arguments']}
        (x, ex), (y, ey) = (_integer(arg, A, s) for arg in e['arguments'])
        if keys & BINARY_DIGITS and r'\widetilde{\omega}_2' in keys:
            return cup(x, y, e['index']), 0
        return cup(x, y, e['index'], s=s, twists=(ex, ey)), (ex + ey) % 2
    if operation == 'integer_differential':
        x, ex = _integer(e['argument'], A, s)
        return x.d(), ex
    if operation == 'twisted_integer_differential':
        x, ex = _integer(e['argument'], A, s)
        return ds(x, s), ex
    raise ValueError(operation)


class Manifest:
    def __init__(self, path):
        data = json.loads(Path(path).read_text())
        assert data['phase_convention'].startswith('physical')
        self.data = data
        half_phase = data['half_phase']
        assert tuple(half_phase['phase_coefficient']) == (1, 2)
        self.inputs = [row['physical_expression'] for row in half_phase['input_cochains']]
        degrees = [row['degree'] for row in half_phase['input_cochains']]
        self.words = []
        for row in half_phase['ms_terms']:
            index = tuple(row['input_indices'])
            cuts = interval_faces(tuple(row['word']), tuple(degrees[i] for i in index))
            self.words.append((index, cuts))
        self.faces = data['physical_binary_face_polynomial']

    def __call__(self, A, s, f):
        xs = [A[k] for k in self.inputs]
        bits = 0
        for index, cuts in self.words:
            for cut in cuts:
                if all(xs[i](tuple(f[j] for j in loc)) for i, loc in zip(index, cut)):
                    bits ^= 1
        if self.faces:
            atoms = [A[row['physical_expression']](tuple(f[j] for j in row['face'])) % 2
                     for row in self.faces['factor_alphabet']]
            for monomial in self.faces['monomials']:
                if all(atoms[i] for i in monomial):
                    bits ^= 1
        value = Fraction(bits, 2)
        for term in self.data['other_phase_terms']:
            p, q = term['phase_coefficient']
            value += Fraction(p * _integer(term['expression'], A, s)[0](f), q)
        for term in self.data['signed_integer_face_terms']:
            p, q = term['phase_coefficient']
            sign = term['sign']['exponent_mod2']
            e = A[sign['physical_expression']](tuple(f[j] for j in sign['face'])) % 2
            product = 1
            for factor in term['integer_factors']:
                product *= _leaf(A, factor['physical_expression'])(
                    tuple(f[j] for j in factor['face']))
            value += Fraction(p * (-1) ** e * product, q)
        return value % 1


@lru_cache(None)
def manifest(law, sector):
    return Manifest(MANIFESTS / f'{law}_{sector}_TERMS.json')


# Majorana contributions (displayed formulas) ------------------------------

def _beta_bits(x):
    """beta^- x and its residue [beta^- x]_2 = x cup_1 x + x cup_2 dx."""
    b = beta_open(x)
    return b, b.reduce(2)


def zeta22(x, y):
    return op('1231343', x, x, y, y)


def zeta13(x, y):
    return op('1231434', x, x, y, y)


def X5(x):
    out = op('1213243', x, x, x, x)
    for v in ('1213431', '1232141', '1234321'):
        out = out + op(v, x, x, x, x)
    return out


def O5_gamma(n2, s, w, f):
    beta, b = _beta_bits(n2)
    sq = cup(n2, n2)
    h = (zeta22(w, n2) + X5(n2) + cup(sq, cup(w, n2), 3) + cup(sq, cup(s, b), 3)
         + cup(cup(w, n2), cup(s, b), 3) + zeta13(s, b) + cup(cup(w, s, 1), b) + cup(s, sq))
    q = cup(w.lift(), beta) + cup(beta, beta, 1) + cup(cup(s, s).lift(), beta + b.lift())
    return (half(h, f) + Fraction(q(f), 4)) % 1


def z4_0(x, y):
    out = C(4)
    for v in ('12123434', '12134131', '12314324', '12314342',
              '13242412', '13413142', '13432412'):
        out = out + op(v, x, x, y, y)
    bx, by = _beta_bits(x)[1], _beta_bits(y)[1]
    out = out + op('12123', x + y, y, cup(x, y, 2)) + op('123131', y, x, cup(x, y, 1))
    out = out + cup(cup(x, y, 1), y, 1) + cup(bx + by, cup(x, y, 2), 1)
    out = out + cup(cup(x, y, 2), bx + by + cup(y, x, 1), 1)
    out = out + cup(cup(x, y, 1), cup(x, x) + cup(y, y), 3)
    out = out + cup(y, cup(x, cup(x, y, 1), 1), 2) + cup(by, bx, 2)
    return out


def beta_plus(x):
    beta, b = _beta_bits(x)
    return (beta + b.lift()).div(2)


def z4_gamma(n2, m2, s, w):
    e3 = cup(n2, m2, 1) + cup(s, cup(n2, m2, 2))
    M = n2 + m2
    lam = cup(n2, m2, 2)
    bn, bm = _beta_bits(n2)[1], _beta_bits(m2)[1]
    wM = cup(w, M)
    z = (z4_0(n2, m2) + cup(wM, e3, 3) + cup(cup(n2, m2, 1).d(), wM, 4)
         + cup(cup(m2, m2), cup(w, n2), 4) + cup(cup(m2, m2) + cup(w, m2), cup(s, bn), 4)
         + cup(cup(w, s, 1), lam) + cup(cup(n2, m2, 1), cup(s, bn + bm), 3)
         + cup(cup(M, M), cup(s, lam), 3) + cup(cup(n2, m2, 1), cup(s, lam), 2))
    carry = (beta_plus(M) - beta_plus(n2) - beta_plus(m2)).reduce(2)
    inner = (e3 + cup(bn, bm, 3) + cup(lam, lam, 1) + cup(bn + bm, cup(s, lam), 3)
             + cup(cup(s, lam), lam, 2) + carry)
    return z + cup(s, inner)


def E4_gamma(n2, m2, s, w, f):
    lam = cup(n2, m2, 2).lift()
    Bn, Bm, BM = beta_open(n2), beta_open(m2), beta_open(n2 + m2)
    q = (cup(Bn, Bm, 2).scaled(-1) + cup(Bn + Bm, lam, 1) - cup(lam, BM, 1)
         + cup(lam, lam) - cup(w.lift(), lam))
    return (half(z4_gamma(n2, m2, s, w), f) + Fraction(q(f), 4)) % 1


# Bosonic obstruction ------------------------------------------------------

O5_WORDS_W = ('1212313',)
O5_WORDS_S = ('121341431', '241431341', '124214131', '121431341', '142141314', '142141341')


def O5_parts(x, s, w, f):
    n1, n2, n3 = x['n1'], x['n2'], x['n3']
    A, P = O4_majorana(n2, w, s), O4_psi(n1, w, s)
    B = cup(n2, n2, 1)
    dB, dn2 = B.d(), n2.d()
    y = n3.d() + dB
    c = cup(w, n3) + cup(n3, n3, 1) + cup(n3.d(), n3, 2)
    cpsi = cup(A, P, 3) + cup(P, A, 3) + cup(P, P, 3) + cup(dB, B, 2) + cup(dB, y, 3)
    for v in O5_WORDS_W:
        cpsi = cpsi + op(v, y, w, dn2)
    for v in O5_WORDS_S:
        cpsi = cpsi + op(v, y, s, n2, dn2)
    open_ = cup(n2, dn2, 2)
    D = cup(w, open_) + cup(B, open_, 1) + cup(open_, B, 1) + cup(open_, open_, 1)
    alphabet = _alphabet(x, None, s, w)
    return {'c': half(c, f), 'cgamma': half(cup(A, A, 3), f), 'cpsi': half(cpsi, f),
            'gamma': O5_gamma(n2, s, w, f),
            'gammapsi': (manifest('O5', 'GAMMAPSI')(alphabet, s, f) + half(D, f)) % 1,
            'psi': manifest('O5', 'PSI')(alphabet, s, f)}


def O5(x, s, w, f):
    return sum(O5_parts(x, s, w, f).values()) % 1


# Bosonic stacking ---------------------------------------------------------

def E4_parts(x, y, s, w, f):
    n1, n2, n3 = x['n1'], x['n2'], x['n3']
    m1, m2, m3 = y['n1'], y['n2'], y['n3']
    Z = stack(x, y, s, w)
    N1, N2, N3 = Z['n1'], Z['n2'], Z['n3']
    e2, e3 = E2(n1, m1), E3(n1, n2, m1, m2, s)
    A, Am, AN = O4_majorana(n2, w, s), O4_majorana(m2, w, s), O4_majorana(N2, w, s)
    P, Pm, PN = O4_psi(n1, w, s), O4_psi(m1, w, s), O4_psi(N1, w, s)

    c = cup(n3, m3, 2) + cup(n3 + m3, e3, 2)
    cgamma = cup(A, m3, 3) + cup(N3, AN, 3) + cup(n3, A, 3) + cup(m3, Am, 3)

    B, Bm, BN = cup(n2, n2, 1), cup(m2, m2, 1), cup(N2, N2, 1)
    Bp = cup(n2 + m2, n2 + m2, 1)
    b, bm, bp = _beta_bits(n2)[1], _beta_bits(m2)[1], _beta_bits(n2 + m2)[1]
    dB, dBm, dBN = B.d(), Bm.d(), BN.d()
    DB = BN + B + Bm
    a, a2 = n1.reduce(2), m1.reduce(2)
    h, k = digit(n1, 1), digit(m1, 1)
    pair = C(2, fun=lambda v: (
        a(v[:2]) * k(v[1:]) + h(v[:2]) * a2(v[1:]) + h(v[:2]) * k(v[1:]) + n2(v) * m2(v)
        + a(v[:2]) * a2(v[1:]) * (n2(v) + m2(v))
        + s(v[:2]) * (h(v[:2]) * a2(v[1:]) + a(v[:2]) * a2(v[:2]) * (a(v[1:]) + a2(v[1:])))))
    dpair = pair.d()
    lam = cup(n2, m2, 2)
    yx, ym, yN = n3.d() + dB, m3.d() + dBm, N3.d() + dBN
    cpsi = (cup(P, m3, 3) + cup(N3, PN, 3) + cup(n3, P, 3) + cup(m3, Pm, 3)
            + cup(n3 + m3, DB, 2) + cup(dB, m3, 3) + cup(n3, Bm, 2) + cup(B, m3, 2)
            + cup(B + Bm, e3 + DB, 2) + cup(yx, Bm, 3)
            + cup(BN, yN, 3) + cup(B, yx, 3) + cup(Bm, ym, 3)
            + cup(N3, BN, 2) + cup(n3, B, 2) + cup(m3, Bm, 2)
            + cup(w, pair) + cup(pair, pair) + cup(dpair, pair, 1)
            + cup(e3 + DB + dpair, dpair, 2) + cup(dpair, yN, 3)
            + cup(B, Bm, 2) + cup(b, bm, 2)
            + cup(b + bm, lam, 1) + cup(lam, bp, 1) + cup(lam, lam) + cup(w, lam)
            + (cup(m3, B, 3) + cup(B + Bm, e3, 3) + cup(B + Bm, lam, 2)
               + cup(lam, lam, 1)).d()
            + cup(yx + ym, cup(w, e2) + cup(s, BN + Bp), 4))
    dn2, dm2 = n2.d(), m2.d()

    def g(cochain, *i):
        return cochain(tuple(f[j] for j in i))
    face = (g(yx, 0, 1, 2, 3, 4) * (
        g(m2, 0, 1, 2) * g(dn2, 0, 2, 3, 4) + g(n2, 0, 3, 4) * g(dm2, 0, 1, 2, 3)
        + g(m2, 1, 2, 3) * g(dn2, 0, 1, 3, 4) + g(n2, 0, 1, 4) * g(dm2, 1, 2, 3, 4)
        + g(m2, 2, 3, 4) * g(dn2, 0, 1, 2, 4)
        + g(s, 0, 1) * (g(m2, 1, 2, 4) * g(dn2, 1, 2, 3, 4)
                        + (g(n2, 1, 2, 3) + g(m2, 1, 2, 3)) * g(dm2, 1, 2, 3, 4)))
        + g(ym, 0, 1, 2, 3, 4) * (
        g(m2, 0, 1, 2) * g(dn2, 0, 2, 3, 4) + g(n2, 0, 3, 4) * g(dm2, 0, 1, 2, 3)
        + g(s, 0, 1) * ((g(n2, 1, 2, 3) + g(m2, 1, 2, 4)) * g(dn2, 1, 2, 3, 4)
                        + g(n2, 1, 2, 3) * g(dm2, 1, 2, 3, 4))))
    alphabet = _alphabet(x, y, s, w)
    return {'c': half(c, f), 'cgamma': half(cgamma, f),
            'cpsi': Fraction((cpsi(f) + face) % 2, 2),
            'gamma': E4_gamma(n2, m2, s, w, f),
            'gammapsi': (manifest('E4', 'GAMMAPSI')(alphabet, s, f)
                         + half((cup(lam, lam, 1) + cup(lam, lam.d(), 2)).d(), f)) % 1,
            'psi': manifest('E4', 'PSI')(alphabet, s, f)}


def E4(x, y, s, w, f):
    return sum(E4_parts(x, y, s, w, f).values()) % 1
