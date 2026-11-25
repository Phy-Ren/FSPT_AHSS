"""4+1D formulas in the physical point-fermion occupation n_4.

The complex-fermion layer obeys dn_4 = O_5, with O_5 the complete directed
F-move count. The Majorana argument u is the physical n_3 (du = O_4); the
complex-fermion argument c is n_4. Every function here is written in these
fields; the 3+1D construction keeps its own auxiliary source in source.py.
Binary cochains are F2; phase numerators are integers over the stated
denominator.
"""
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'reference/d4_input/code'))
sys.path.insert(0, str(ROOT/'bosonic'))
from cochains import C, cup, sq, ds, op, background_data, prism_transgression
from compact import beta_open, integer_inputs, kappa, ell
from explicit_pip import cartan_word


def carry(n):
    """Second binary digit [floor(n/2)]_2 of a signed integer cochain."""
    return (n-n.reduce(2).lift()).div(2).reduce(2)


def zeta22(x, y):
    return op('1231343', x, x, y, y)


def pure_parity(n, w, s):
    """O_5^psi: intrinsic zero modes, projective zero modes, and their pairs."""
    a, h = n.reduce(2), carry(n)
    W = w+cup(s, s)
    aa, Wa, W1W = cup(a, a), cup(W, a), cup(W, W, 1)
    return (zeta22(a, a)+cup(h, cup(a, a, 1))+cup(s, cup(h, a))
            + zeta22(W, a)+cup(W1W+cup(s, W), h)+cup(cup(W1W, s, 1)+cup(s, cup(s, W, 1)), a)
            + cup(aa, Wa, 3)+cup(s, cup(aa, Wa, 4)))


def majorana_parity(u, w, s):
    """O_5^gamma + O_5^{gamma psi} for the Majorana decoration u = n_3."""
    du = u.d()
    return (cup(u, u, 1)+cup(s, cup(u, u, 2))+cup(w, u)
            + cup(du, u, 2)+cup(s, cup(u, du, 3)))


def parity(n, u, w, s):
    """The complete F-move parity O_5; dn_4 = O_5."""
    return majorana_parity(u, w, s)+pure_parity(n, w, s)


def ell3(x, y):
    return C(3, fun=lambda f: (x((f[0], f[2], f[3]))*y(f[:3])
                               * (1+x((f[0], f[1], f[3]))*y(f[1:]))) % 2)


def z4psi(x, y):
    return (op('12413423', x, x, x, y)+op('12314132', x, x, y, y)+op('12314324', x, x, y, y)
            + op('12341321', x, x, y, y)+op('12132413', x, y, y, y)+op('12324214', x, y, y, y))


def s1_polynomial(a, h, s):
    """The one-state s_1 polynomial whose polarization enters E_4^psi."""
    t = cup(a, a, 1)
    return cup(cup(s, h, 1), a)+cup(s, cup(t, a, 2))+op('12131', t, s, a)


def lower_product(n, u, m, v, w, s):
    """E_4 = E_4^gamma + E_4^{gamma psi} + E_4^psi; N_4 = n_4 + n'_4 + E_4."""
    a, b, h, k = n.reduce(2), m.reduce(2), carry(n), carry(m)
    W = w+cup(s, s)
    e3, r = cup(a, b, 1), cup(a, b, 2)
    gamma = cup(u, v, 2)+cup(s, cup(u, v, 3))
    mixed = cup(u, v.d(), 3)+cup(e3, u+v, 2)+cup(s, cup(u+v, e3, 3))
    psi = (z4psi(a, b)+cup(cup(W, a+b), e3, 3)+cup(cup(W, a, 2), b+r)+cup(cup(W, b, 2), a)
           + cup(h, k+b)+cup(a, k)+cup(h.d(), k, 1)+cup(h+k, r)
           + cup(cup(s, a), cup(b, b, 1), 2)+cup(a, cup(s, b), 1)+cup(r, cup(s, a+b), 1)
           + cup(s, cup(s, r)+cup(a, k.d(), 2))+cup(s, cup(r, a+b, 1))+cup(s, ell3(a, b))
           + cup(e3, e3, 2))
    # Delta of the s_1 polynomial: stacked digits a+b and h+k+(a cup_2 b).
    psi = (psi+s1_polynomial(a+b, h+k+r, s)
           + s1_polynomial(a, h, s)+s1_polynomial(b, k, s))
    return gamma+mixed+psi


def blocks(n, u, c, w, s, y):
    """Six-cochain source of O_6 in the occupation c = n_4.

    Returns binary H and integer Q, Pn, Wnn; the phase numerator over 16 is
    8H + 4Q + Pn + 2Wnn. y is the pure completion y_6 of the physical parity.
    """
    a = n.reduce(2)
    b = beta_open(u)
    _, K, _, _ = integer_inputs(n, w, s)
    B = b+K
    Psi = pure_parity(n, w, s)
    S = cup(u, u, 2)
    O5 = parity(n, u, w, s)
    W, _, _, _, P = background_data(w, s)
    H = (sq(c, 2)+cup(w, c)+prism_transgression(u, w, s)+cup(u, ell(w, s))
         + cup(kappa(u, w, s), Psi, 4)+y+cup(b.reduce(2), K.reduce(2), 2)
         + cup(s, cup(b.reduce(2), K.reduce(2), 3))
         + sq(S, 2)+cup(w, S)+cup(O5, S.d(), 4))
    Q = cup(B, B, 2)+cup(B, B.d(), 3)+cup(w.lift(), B)-cartan_word(n, w, s).lift()
    Pn = cup(P, n, s=s, twists=(0, 1))
    Wnn = cup(W.lift(), cup(n, n, s=s, twists=(1, 1)), s=s, twists=(1, 0))
    return H, Q, Pn, Wnn


def B5(u, w, s):
    """Four times the five-cochain B_5[n_3] of the compact Majorana phase convention."""
    import json
    words = json.loads((ROOT/'stages/data/mc3_zero_dictionary.json').read_text())['words']
    bb = beta_open(u).reduce(2)
    bw = beta_open(w).reduce(2)
    half = C(5)
    for word in words:
        half = half+op(word, u, u, u, u)
    half = (half+cup(u, bb, 2)+cup(u, bw, 1)
            + op('131321', u, u, w)+op('1241431232', u, u, u, w)+op('1412432131', u, u, u, w)
            + op('131212', u, bb, s)+op('1312121', bb, bb, s)
            + op('1241312132', u, u, bb, s)+op('1241323132', u, u, bb, s)
            + op('1241323213', u, u, bb, s)+op('1243123231', u, u, bb, s)
            + op('1321', u, w, s))
    return half.lift().scaled(2)+cup(u.lift(), u.lift(), 1)


def convention(n, u, c, w, s):
    """Four times the one-state rephasing to the displayed convention: the
    operator order 1/2 c cup_4 dc, the compact phase -B_5[n_3] - 1/2 s_1 n_4,
    and 1/2[dS cup_5 O_5 + s_1 S] with S = n_3 cup_2 n_3."""
    S = cup(u, u, 2)
    half = cup(c, c.d(), 4)+cup(s, c)+cup(S.d(), parity(n, u, w, s), 5)+cup(s, S)
    return half.lift().scaled(2)-B5(u, w, s)


def source48(n, u, c, w, s, y):
    """O_6 numerator over 48 in the displayed convention (cubic term included)."""
    H, Q, Pn, Wnn = blocks(n, u, c, w, s, y)
    high = H.lift().scaled(8)+Q.scaled(4)+Pn+Wnn.scaled(2)
    cubic = cup(n, cup(n, n, s=s, twists=(1, 1)), s=s, twists=(1, 0))
    return high.scaled(3)+cubic.scaled(4)+ds(convention(n, u, c, w, s), s).scaled(12)


def Phi(n, w, s):
    """Difference of the two completions' parity brackets (n_2 only):
    w x + x cup_2 x + dx cup_3 x + dx cup_4 dx + O_5^psi cup_4 dx."""
    x = s1_polynomial(n.reduce(2), carry(n), s)
    dx = x.d()
    return cup(w, x)+cup(x, x, 2)+cup(dx, x, 3)+cup(dx, dx, 4)+cup(pure_parity(n, w, s), dx, 4)


def completion_change(n, w, s):
    """Binary five-cochain x cup_4 dx + (h_5^(3))^* Phi on the three-factor grid.

    With y_6 the completion of O_5^psi and y_6^aux that of the transfer kernel,
    y_6 = y_6^aux + Phi + d(h^* Phi); the obstruction source of the product's
    transfer construction differs from O_6 by the twisted differential of one
    half of this cochain."""
    from ez_homotopy import ez_homotopy
    def sign(a, b): return (-1)**(s(tuple(sorted((a, b)))) if a != b else 0)
    ng = C(2, fun=lambda f: sign(f[0][0], f[0][1])*n(tuple(v[1] for v in f)), mod=None)
    wg = C(2, fun=lambda f: w(tuple(v[2] for v in f))); wg.closed = True
    sg = C(1, fun=lambda f: s(tuple(v[0] for v in f))); sg.closed = True
    Pg = Phi(ng, wg, sg)
    H = ez_homotopy(5)
    def value(face):
        total = 0
        for simplex in H:
            total = total+Pg(tuple(tuple(face[c] for c in v) for v in simplex))
        return total % 2
    x = s1_polynomial(n.reduce(2), carry(n), s)
    return C(5, fun=value)+cup(x, x.d(), 4)


def output_gauge(u, v):
    """Four times the output coboundary B_4^out of the Majorana stacking faces."""
    import json
    terms = json.loads((ROOT.parents[1]/'docs/formulas/coefficients/FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.json').read_text())['terms']
    rows = [tuple((x['cochain'] == "\\check n'_3", tuple(x['face'])) for x in t) for t in terms]
    def value(face):
        total = 0
        for row in rows:
            term = 1
            for second, f in row:
                term = term*(v if second else u)(tuple(face[i] for i in f))
            total = total+term
        return total % 2
    half = C(4, fun=value)
    return half.lift().scaled(2)-cup(beta_open(u)+beta_open(v), cup(u, v, 3).lift(), 3)


def thesis_primitive(u, v, w, s):
    """Binary four-cochain b_4: the Eilenberg-Zilber primitive of the binary part
    of the closed-sector difference to the thesis law, as its face polynomial."""
    import json
    data = json.loads((ROOT/'full4/physical_b4.json').read_text())
    names = {'u': u, 'v': v, 'w': w, 's': s}
    variables = [(names[n], tuple(f)) for n, f in data['variables']]
    monomials = [int(m) for m in data['monomials']]
    def value(face):
        bits = [x(tuple(face[i] for i in f)) for x, f in variables]
        total = 0
        for m in monomials:
            term = 1
            k = 0
            while m:
                if m & 1:
                    term = term*bits[k]
                m >>= 1
                k += 1
            total = total+term
        return total % 2
    return C(4, fun=value)


def stacking_rephasing(n, u, m, v, w, s):
    """Four times the P-move rephasing that puts the twister of source48 in the
    thesis form at n_2 = n'_2 = 0."""
    a, b = n.reduce(2), m.reduce(2)
    U = u+v+cup(a, b, 1)
    S, Sp, SN = cup(u, u, 2), cup(v, v, 2), cup(U, U, 2)
    O, Op, ON = parity(n, u, w, s), parity(m, v, w, s), parity(n+m, U, w, s)
    beta = cup(u, v, 3)
    Q = cup(SN, ON, 5)+cup(S, O, 5)+cup(Sp, Op, 5)+cup(beta.d(), SN, 4)
    return ((Q+thesis_primitive(u, v, w, s)).lift().scaled(2)-output_gauge(u, v)
            + cup(u.lift(), v.lift(), 2))


def occupation_change(n, u, c, w, s):
    """Four times the one-state rephasing from the transfer construction of
    the product, whose complex-fermion argument is c + n_3 cup_2 n_3 + x, to the
    displayed convention in c = n_4; x is the s_1 polynomial of E_4^psi."""
    a, h = n.reduce(2), carry(n)
    S = cup(u, u, 2)
    x = s1_polynomial(a, h, s)
    y = S+x
    O5 = parity(n, u, w, s)
    R = cup(c, y, 3)+cup(O5, y, 4)+cup(S, x, 3)+cup(S.d(), x, 4)
    return convention(n, u, c, w, s)+R.lift().scaled(2)


def product48(n, u, c, m, v, cp, w, s):
    """Nonbinary part of E_5 over 48 in the occupations c = n_4, cp = n'_4.

    The binary transfer Z_5 of the runtime is added separately. The transfer
    construction evaluates its complex-fermion products on c + y, cp + y'
    (y = n_3 cup_2 n_3 + x, x the s_1 polynomial of E_4^psi). The twister of
    the obstruction source48 follows by the polarization of occupation_change
    on the stacked state with occupation N_4 + d(n_3 cup_3 n'_3), the gauge
    primitive that removes d(n_3 cup_3 n'_3), the P-move rephasing
    1/2 y cup_4 n'_4, and the polarization of completion_change.
    """
    from product_full import collected_blocks
    a, b = n.reduce(2), m.reduce(2)
    y = cup(u, u, 2)+s1_polynomial(a, carry(n), s)
    yp = cup(v, v, 2)+s1_polynomial(b, carry(m), s)
    D = collected_blocks(n, u, c+y, m, v, cp+yp, w, s)['nonbinary48']
    NN, U = n+m, u+v+cup(a, b, 1)
    N4 = c+cp+lower_product(n, u, m, v, w, s)
    beta = cup(u, v, 3)
    dR = (occupation_change(NN, U, N4+beta.d(), w, s)
          - occupation_change(n, u, c, w, s)-occupation_change(m, v, cp, w, s))
    G = (cup(N4, beta.d(), 3)+cup(beta, beta.d(), 2)+cup(beta, beta, 1)
         + cup(w, beta)+cup(s, beta.d())+cup(y, cp, 4).d())
    Dy = completion_change(NN, w, s)+completion_change(n, w, s)+completion_change(m, w, s)
    P = ds(stacking_rephasing(n, u, m, v, w, s), s)
    return D+dR.scaled(12)+(G+Dy).lift().scaled(24)+P.scaled(12)
