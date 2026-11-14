#!/usr/bin/env python3
"""Checks of the 3+1D formulas written in the occupations n_3, standard library only.

The publication code evaluates the complex-fermion layer with the argument
x = n_3 + R_3, R_3 = n_2 cup_1 n_2, and returns the product output
N_3 + R_3[N_2] + dB_2.  This script checks, on a six-vertex complex:

1. the obstruction identity for arbitrary binary cochains x, R,
       F[x+R] - F[x] = d(rho) + (terms with R),
   F[x] = 1/2[w_2 x + x cup_1 x + dx cup_2 x],
   rho  = 1/2[x cup_2 R + x cup_3 dR];
2. the stacking identity for arbitrary cochains: the code product in the
   arguments n_3+R_3 plus Delta(rho) equals the displayed c, c gamma and
   complex-fermion/p+ip terms with R_3;
3. on random towers with n_1 = n'_1 = 0, the code product with its face
   reference B_2 equals the closed-sector formulas after the displayed
   coboundary lambda_3;
4. on the same towers, the displayed O_5^{c psi} and E_4^{c psi} vanish;
5. for two identical complete states with n_1 = 0 or n_1 = s_1, the general
   c, c gamma and c psi formulas reduce to the self-stacking formulas.

All half-valued phases are compared as binary cochains (twice the phase).
"""
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import random

NV = 6


@lru_cache(None)
def cup_faces(p, q, k):
    """Index pairs of the Steenrod cup_k product of a p- and a q-cochain."""
    n = p + q - k
    if k < 0 or n < 0:
        return ()
    word = [j % 2 for j in range(k + 2)]
    out = []
    for cuts in combinations_with_replacement(range(n + 1), k + 1):
        ends = (0,) + cuts + (n,)
        parts = [[], []]
        for j, side in enumerate(word):
            parts[side] += range(ends[j], ends[j + 1] + 1)
        if all(len(l) == deg + 1 and all(a < b for a, b in zip(l, l[1:]))
               for l, deg in zip(parts, (p, q))):
            out.append(tuple(map(tuple, parts)))
    return tuple(out)


def simplices(p):
    return list(combinations(range(NV), p + 1))


def cup(a, p, b, q, k=0):
    out = {}
    for v in simplices(p + q - k):
        out[v] = sum(a[tuple(v[i] for i in l)] * b[tuple(v[i] for i in r)]
                     for l, r in cup_faces(p, q, k)) % 2
    return out


def d(a, p):
    return {v: sum(a[v[:j] + v[j + 1:]] for j in range(p + 2)) % 2
            for v in simplices(p + 1)}


def add(*cochains):
    out = {}
    for c in cochains:
        for f, x in c.items():
            out[f] = (out.get(f, 0) + x) % 2
    return out


def rnd(p, rng):
    return {f: rng.randrange(2) for f in simplices(p)}


def is_zero(c):
    return not any(c.values())


def solve_d(rhs, p, rng):
    """A binary p-cochain x with dx = rhs, plus a random coboundary."""
    X, Y = simplices(p), simplices(p + 1)
    idx = {f: i for i, f in enumerate(X)}
    rows = []
    for y in Y:
        mask = 0
        for j in range(p + 2):
            mask ^= 1 << idx[y[:j] + y[j + 1:]]
        rows.append([mask, rhs[y]])
    r, piv = 0, []
    for col in range(len(X)):
        sel = next((k for k in range(r, len(rows)) if rows[k][0] >> col & 1), None)
        if sel is None:
            continue
        rows[r], rows[sel] = rows[sel], rows[r]
        for k in range(len(rows)):
            if k != r and rows[k][0] >> col & 1:
                rows[k][0] ^= rows[r][0]
                rows[k][1] ^= rows[r][1]
        piv.append(col)
        r += 1
    assert not any(rows[k][1] for k in range(r, len(rows))), 'rhs not closed'
    x = {f: 0 for f in X}
    for k, col in enumerate(piv):
        x[X[col]] = rows[k][1]
    return add(x, d(rnd(p - 1, rng), p - 1)) if p else x


# Shorthands for products of a 3-cochain and a 4-cochain (degrees in names).
def c2(u, v): return cup(u, 3, v, 3, 2)          # deg3 cup_2 deg3
def x43(u, v): return cup(u, 4, v, 3, 3)         # deg4 cup_3 deg3
def y34(u, v): return cup(u, 3, v, 4, 3)         # deg3 cup_3 deg4


def background(rng):
    t = [rng.randrange(2) for _ in range(NV)]
    s = {(i, j): (t[i] + t[j]) % 2 for i, j in simplices(1)}
    w = add(d(rnd(1, rng), 1), cup(s, 1, s, 1))
    wt = add(w, cup(s, 1, s, 1))
    return s, w, wt


# Lower obstructions (equations 6-9 of the 3+1D page).
def O4_gamma(n2, s, w):
    return add(cup(n2, 2, n2, 2), cup(s, 1, cup(n2, 2, n2, 2, 1), 3), cup(w, 2, n2, 2))


def O4_gammapsi(n2, s):
    dn2 = d(n2, 2)
    return add(cup(dn2, 3, n2, 2, 1), cup(s, 1, cup(n2, 2, dn2, 3, 2), 3))


def O4_psi(a1, h1, s, wt):
    z = {v: wt[v[:3]] * wt[(v[0], v[2], v[3])] * a1[v[2:4]] * a1[v[3:]] % 2
         for v in simplices(4)}
    w11 = cup(wt, 2, wt, 2, 1)
    t1 = cup(add(w11, cup(s, 1, wt, 2)), 3, h1, 1)
    t2 = cup(add(cup(w11, 3, s, 1, 1), cup(s, 1, cup(s, 1, wt, 2, 1), 2)), 3, a1, 1)
    return add(z, t1, t2)


def bits(n1):
    return ({e: x % 2 for e, x in n1.items()},
            {e: (x // 2) % 2 for e, x in n1.items()})


def tower(s, w, wt, mode, rng):
    """A complete state n_1, n_2, n_3 with dn_2 = O_3 and dn_3 = O_4."""
    if mode == 'zero':
        n1 = {e: 0 for e in simplices(1)}
    elif mode == 's1':
        n1 = dict(s)
    else:
        h = [rng.randrange(-3, 4) for _ in range(NV)]
        n1 = {(i, j): (-1) ** s[(i, j)] * h[j] - h[i] for i, j in simplices(1)}
    a1, h1 = bits(n1)
    n2 = solve_d(cup(wt, 2, a1, 1), 2, rng)
    A = add(O4_gamma(n2, s, w), O4_gammapsi(n2, s))
    P = O4_psi(a1, h1, s, wt)
    O = add(A, P)
    assert is_zero(d(O, 4)), 'O_4 not closed'
    n3 = solve_d(O, 3, rng)
    return dict(n1=n1, a1=a1, h1=h1, n2=n2, n3=n3, A=A, P=P)


def stack(X, Y, s, w, wt):
    """Lower stacking laws (equations 20-27) and the pair reference B_2."""
    a, a2, h, h2 = X['a1'], Y['a1'], X['h1'], Y['h1']
    n2, m2 = X['n2'], Y['n2']
    N1 = {e: X['n1'][e] + Y['n1'][e] for e in simplices(1)}
    E2 = cup(a, 1, a2, 1)
    N2 = add(n2, m2, E2)
    nm = add(n2, m2)
    E3 = add(cup(n2, 2, m2, 2, 1), cup(s, 1, cup(n2, 2, m2, 2, 2), 2),
             cup(n2, 2, d(m2, 2), 3, 2), cup(nm, 2, E2, 2, 1),
             cup(s, 1, cup(nm, 2, E2, 2, 2), 2),
             cup(cup(a, 1, cup(a, 1, a2, 1), 2, 1), 2, a2, 1),
             cup(h, 1, cup(a2, 1, a2, 1), 2), cup(s, 1, cup(h, 1, a2, 1), 2))
    N3 = add(X['n3'], Y['n3'], E3)
    aN, hN = bits(N1)
    Z = dict(n1=N1, a1=aN, h1=hN, n2=N2, n3=N3,
             A=add(O4_gamma(N2, s, w), O4_gammapsi(N2, s)), P=O4_psi(aN, hN, s, wt))
    assert d(N3, 3) == add(Z['A'], Z['P']), 'output tower'
    B2 = {}
    for v in simplices(2):
        e1, e2 = v[:2], v[1:]
        B2[v] = (a[e1] * h2[e2] + h[e1] * a2[e2] + h[e1] * h2[e2] + n2[v] * m2[v]
                 + a[e1] * a2[e2] * (n2[v] + m2[v])
                 + s[e1] * (h[e1] * a2[e2] + a[e1] * a2[e1] * (a[e2] + a2[e2]))) % 2
    return Z, dict(E2=E2, E3=E3, B2=B2)


def R3(n2):
    return cup(n2, 2, n2, 2, 1)


# Displayed formulas -------------------------------------------------------

def E4_c(X, Y, L):
    n, m = X['n3'], Y['n3']
    return add(c2(n, m), c2(add(n, m), L['E3']))


def E4_cgamma(X, Y, Z):
    return add(x43(X['A'], Y['n3']), y34(Z['n3'], Z['A']),
               y34(X['n3'], X['A']), y34(Y['n3'], Y['A']))


def E4_cpsi(X, Y, Z, L, s, w):
    """Equation 30 of the 3+1D page."""
    n, m, N = X['n3'], Y['n3'], Z['n3']
    n2, m2 = X['n2'], Y['n2']
    R, Rm, RN, Rp = R3(n2), R3(m2), R3(Z['n2']), R3(add(n2, m2))
    dR, dRm, dRN = d(R, 3), d(Rm, 3), d(RN, 3)
    DR = add(RN, R, Rm)
    E3, E2, B2 = L['E3'], L['E2'], L['B2']
    dB2 = d(B2, 2)
    lam = cup(n2, 2, m2, 2, 2)
    dx, dxm, dX = add(d(n, 3), dR), add(d(m, 3), dRm), add(d(N, 3), dRN)
    t = add(
        x43(X['P'], m), y34(N, Z['P']), y34(n, X['P']), y34(m, Y['P']),
        c2(add(n, m), DR), x43(dR, m), c2(n, Rm), c2(R, m),
        c2(add(R, Rm), add(E3, DR)), x43(dx, Rm),
        y34(RN, dX), y34(R, dx), y34(Rm, dxm), c2(N, RN), c2(n, R), c2(m, Rm),
        cup(w, 2, B2, 2), cup(B2, 2, B2, 2), cup(dB2, 3, B2, 2, 1),
        c2(add(E3, DR, dB2), dB2), cup(dB2, 3, dX, 4, 3),
        cup(add(R, Rm), 3, lam, 2, 1), cup(lam, 2, Rp, 3, 1), cup(lam, 2, lam, 2),
        cup(w, 2, lam, 2),
        d(add(cup(lam, 2, lam, 2, 1), cup(lam, 2, d(lam, 2), 3, 2),
              cup(R, 3, add(E3, m), 3, 3), cup(Rm, 3, E3, 3, 3), cup(RN, 3, lam, 2, 2)), 3),
        cup(add(dx, dxm), 4, add(cup(w, 2, E2, 2), cup(s, 1, add(RN, Rp), 3)), 4, 4))
    dn2, dm2 = d(n2, 2), d(m2, 2)
    F = {}
    for v in simplices(4):
        def g(c, *i): return c[tuple(v[j] for j in i)]
        f1 = (g(m2, 0, 1, 2) * g(dn2, 0, 2, 3, 4) + g(n2, 0, 3, 4) * g(dm2, 0, 1, 2, 3)
              + g(m2, 1, 2, 3) * g(dn2, 0, 1, 3, 4) + g(n2, 0, 1, 4) * g(dm2, 1, 2, 3, 4)
              + g(m2, 2, 3, 4) * g(dn2, 0, 1, 2, 4)
              + g(s, 0, 1) * (g(m2, 1, 2, 4) * g(dn2, 1, 2, 3, 4)
                              + (g(n2, 1, 2, 3) + g(m2, 1, 2, 3)) * g(dm2, 1, 2, 3, 4)))
        f2 = (g(m2, 0, 1, 2) * g(dn2, 0, 2, 3, 4) + g(n2, 0, 3, 4) * g(dm2, 0, 1, 2, 3)
              + g(s, 0, 1) * ((g(n2, 1, 2, 3) + g(m2, 1, 2, 4)) * g(dn2, 1, 2, 3, 4)
                              + g(n2, 1, 2, 3) * g(dm2, 1, 2, 3, 4)))
        F[v] = (g(dx, 0, 1, 2, 3, 4) * f1 + g(dxm, 0, 1, 2, 3, 4) * f2) % 2
    return add(t, F)


def O5_cpsi_cups(X):
    """The cup terms of equation 13; its MS terms all carry dn_2."""
    A, P = X['A'], X['P']
    R = R3(X['n2'])
    dR = d(R, 3)
    return add(cup(A, 4, P, 4, 3), cup(P, 4, A, 4, 3), cup(P, 4, P, 4, 3),
               cup(dR, 4, R, 3, 2), cup(dR, 4, add(d(X['n3'], 3), dR), 4, 3))


def self_cpsi(X, Z):
    """Equation 16 of the 3+1D self-stacking page."""
    n, N, n2 = X['n3'], Z['n3'], X['n2']
    dn2, dn, dN = d(n2, 2), d(n, 3), d(N, 3)
    R = R3(n2)
    dR = d(R, 3)
    t = add(x43(X['P'], n), y34(N, Z['P']), y34(R, dn), x43(dn, R), x43(dR, R),
            c2(add(N, dn2), dn2), cup(dn2, 3, dN, 4, 3), c2(dn2, dn2), cup(dn2, 3, n2, 2, 1))
    dx = add(dn, dR)
    F = {}
    for v in simplices(4):
        def g(c, *i): return c[tuple(v[j] for j in i)]
        F[v] = (g(dx, 0, 1, 2, 3, 4) * (g(n2, 1, 2, 3) * g(dn2, 0, 1, 3, 4)
                + g(n2, 0, 1, 4) * g(dn2, 1, 2, 3, 4) + g(n2, 2, 3, 4) * g(dn2, 0, 1, 2, 4))) % 2
    return add(t, F)


# Checks --------------------------------------------------------------------

def check_obstruction_identity(trials=30):
    bad = 0
    for seed in range(trials):
        rng = random.Random(seed)
        s, w, _ = background(rng)
        x, R = rnd(3, rng), rnd(3, rng)

        def F(y):
            dy = d(y, 3)
            return add(cup(w, 2, y, 3), cup(y, 3, y, 3, 1), cup(dy, 4, y, 3, 2), cup(dy, 4, dy, 4, 3))
        lhs = add(F(add(x, R)), F(x), d(cup(x, 3, R, 3, 2), 4), d(cup(x, 3, d(R, 3), 4, 3), 4))
        dR, dx = d(R, 3), d(x, 3)
        rhs = add(cup(w, 2, R, 3), cup(R, 3, R, 3, 1), cup(dR, 4, R, 3, 2),
                  cup(dR, 4, dx, 4, 3), cup(dR, 4, dR, 4, 3))
        bad += sum(lhs[f] != rhs[f] for f in lhs)
    return bad


def check_stacking_identity(trials=20):
    bad = 0
    for seed in range(trials):
        rng = random.Random(1000 + seed)
        n, m, N, R, Rm, RN = (rnd(3, rng) for _ in range(6))
        A, Am, AN, P, Pm, PN = (rnd(4, rng) for _ in range(6))
        x, xm, X = add(n, R), add(m, Rm), add(N, RN)
        dR, dRm, dRN = d(R, 3), d(Rm, 3), d(RN, 3)
        dx, dxm, dX = add(A, P, dR), add(Am, Pm, dRm), add(AN, PN, dRN)
        Ecode = add(X, x, xm)
        At, Atm, AtN = add(A, dR), add(Am, dRm), add(AN, dRN)
        code = add(c2(x, xm), c2(add(x, xm), Ecode),
                   x43(At, xm), y34(X, AtN), y34(x, At), y34(xm, Atm),
                   x43(P, xm), y34(X, PN), y34(x, P), y34(xm, Pm))

        def rho(u, r): return add(c2(u, r), y34(u, d(r, 3)))
        lhs = add(code, rho(N, RN), rho(n, R), rho(m, Rm))
        DR = add(RN, R, Rm)
        E3 = add(Ecode, DR)
        new = add(c2(n, m), c2(add(n, m), E3),
                  x43(A, m), y34(N, AN), y34(n, A), y34(m, Am),
                  x43(P, m), y34(N, PN), y34(n, P), y34(m, Pm),
                  c2(add(n, m), DR), x43(dR, m), c2(n, Rm), c2(R, m), c2(R, Rm),
                  c2(add(R, Rm), add(E3, DR)), x43(dx, Rm),
                  y34(RN, dX), y34(R, dx), y34(Rm, dxm), c2(N, RN), c2(n, R), c2(m, Rm))
        bad += sum(lhs[f] != new[f] for f in lhs)
    return bad


def check_closed_sector(trials=40):
    """Code product with B_2 = lambda_2 at n_1 = 0 versus the closed formulas."""
    bad = 0
    for seed in range(trials):
        rng = random.Random(2000 + seed)
        s, w, wt = background(rng)
        X, Y = tower(s, w, wt, 'zero', rng), tower(s, w, wt, 'zero', rng)
        Z, L = stack(X, Y, s, w, wt)
        n, m, N, E3 = X['n3'], Y['n3'], Z['n3'], L['E3']
        n2, m2 = X['n2'], Y['n2']
        R, Rm, RN = R3(n2), R3(m2), R3(Z['n2'])
        lam = cup(n2, 2, m2, 2, 2)
        assert L['B2'] == lam
        dl = d(lam, 2)
        x, xm, Xc = add(n, R), add(m, Rm), add(N, RN)
        DR = add(RN, R, Rm)
        Ecode = add(E3, DR, dl)
        code = add(c2(x, xm), c2(add(x, xm), add(E3, DR)), cup(w, 2, lam, 2),
                   cup(lam, 2, lam, 2), cup(dl, 3, lam, 2, 1), c2(Ecode, dl),
                   x43(X['A'], xm), y34(Xc, Z['A']), y34(x, X['A']), y34(xm, Y['A']),
                   y34(dl, Z['A']))
        Drho = add(c2(N, RN), c2(n, R), c2(m, Rm))
        closed = add(E4_c(X, Y, L), E4_cgamma(X, Y, Z))
        Q = add(cup(R, 3, Rm, 3, 2), cup(add(R, Rm), 3, lam, 2, 1),
                cup(lam, 2, R3(add(n2, m2)), 3, 1), cup(lam, 2, lam, 2), cup(w, 2, lam, 2))
        G = d(add(cup(lam, 2, lam, 2, 1), cup(lam, 2, dl, 3, 2)), 3)
        lam3 = add(cup(R, 3, add(E3, m), 3, 3), cup(Rm, 3, E3, 3, 3), cup(RN, 3, lam, 2, 2))
        D = add(code, Drho, closed, Q, G, d(lam3, 3))
        bad += sum(D.values())
    return bad


def check_vanishing(trials=60):
    bad = 0
    for seed in range(trials):
        rng = random.Random(3000 + seed)
        s, w, wt = background(rng)
        X, Y = tower(s, w, wt, 'zero', rng), tower(s, w, wt, 'zero', rng)
        assert is_zero(d(X['n2'], 2)) and is_zero(X['P'])
        Z, L = stack(X, Y, s, w, wt)
        bad += sum(O5_cpsi_cups(X).values())
        bad += sum(E4_cpsi(X, Y, Z, L, s, w).values())
    return bad


def check_self_stacking(trials=40):
    bad = 0
    for mode in ('zero', 's1'):
        for seed in range(trials):
            rng = random.Random(4000 + seed)
            s, w, wt = background(rng)
            X = tower(s, w, wt, mode, rng)
            Z, L = stack(X, X, s, w, wt)
            n, N = X['n3'], Z['n3']
            bad += sum(a != b for a, b in zip(E4_c(X, X, L).values(), c2(n, n).values()))
            O4g_N = O4_gamma(Z['n2'], s, w)
            selfcg = add(x43(X['A'], n), y34(N, O4g_N))
            bad += sum(add(E4_cgamma(X, X, Z), selfcg).values())
            selfcp = self_cpsi(X, Z) if mode == 's1' else {}
            bad += sum(add(E4_cpsi(X, X, Z, L, s, w), selfcp).values())
    return bad


def main():
    results = {
        'obstruction identity (arbitrary cochains)': check_obstruction_identity(),
        'stacking identity (arbitrary cochains)': check_stacking_identity(),
        'closed sector with lambda_3 (n_1 = 0 towers)': check_closed_sector(),
        'O_5^{c psi}, E_4^{c psi} vanish (n_1 = 0 towers)': check_vanishing(),
        'self-stacking c, c gamma, c psi (n_1 = 0, s_1)': check_self_stacking(),
    }
    for name, bad in results.items():
        print(f'{name}: {"PASS" if bad == 0 else f"FAIL ({bad} mismatches)"}')
    if any(results.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
