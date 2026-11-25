#!/usr/bin/env python3
"""Checks of the 4+1D change from the code argument to the occupation n_4, standard library only.

The publication code evaluates the complex-fermion layer with the argument
c = n_4 + y, y = n_3 cup_2 n_3 + x, where x is the s_1 polynomial shown in O_6^psi.
The formula pages use n_4 itself, with dn_4 = O_5. For arbitrary binary cochains
this script checks

1. the obstruction identity, with F[c] = 1/2[w_2 c + c cup_2 c + dc cup_3 c + dc cup_4 dc],
       F[c+R] - F[c] = d(1/2[c cup_3 R + c cup_4 dR])
                       + 1/2[w_2 R + R cup_2 R + dR cup_3 R + dR cup_4 dc + dR cup_4 dR];
2. the obstruction conversion: the code obstruction in c, with its compact parities and
   the +1/4 form of the Majorana quarter bracket, minus the displayed obstruction in n_4
   (with the two occupation brackets of O_6^{c psi} and O_6^psi) is the coboundary of the
   displayed occupation change;
3. the stacking identity: the code products in c, transported by that change, by the
   gauge transformation d(n_3 cup_3 n'_3) of N_4 and by the P-move rephasing
   1/2 y cup_4 n'_4, equal the displayed E_5^c, E_5^{c gamma}, E_5^{c psi} with the
   occupation bracket, N_4 = n_4 + n'_4 + E_4.

All half-valued phases are compared as binary cochains (twice the phase).
"""
from functools import lru_cache
from itertools import combinations, combinations_with_replacement
import random


@lru_cache(None)
def cup_faces(p, q, k):
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


class Complex:
    def __init__(self, nv):
        self.nv = nv

    def simplices(self, p):
        return list(combinations(range(self.nv), p + 1))

    def rnd(self, p, rng):
        return {f: rng.randrange(2) for f in self.simplices(p)}

    def cup(self, a, p, b, q, k=0):
        return {v: sum(a[tuple(v[i] for i in l)] * b[tuple(v[i] for i in r)]
                       for l, r in cup_faces(p, q, k)) % 2
                for v in self.simplices(p + q - k)}

    def d(self, a, p):
        return {v: sum(a[v[:j] + v[j + 1:]] for j in range(p + 2)) % 2
                for v in self.simplices(p + 1)}


def add(*cochains):
    out = {}
    for c in cochains:
        for f, x in c.items():
            out[f] = (out.get(f, 0) + x) % 2
    return out


def background(K, rng):
    t = [rng.randrange(2) for _ in range(K.nv)]
    s = {(i, j): (t[i] + t[j]) % 2 for i, j in K.simplices(1)}
    return add(K.d(K.rnd(1, rng), 1), K.cup(s, 1, s, 1))


def check_obstruction_identity(trials=20):
    K = Complex(8)
    bad = 0
    for seed in range(trials):
        rng = random.Random(seed)
        w = background(K, rng)
        x, R = K.rnd(4, rng), K.rnd(4, rng)

        def F(y):
            dy = K.d(y, 4)
            return add(K.cup(w, 2, y, 4), K.cup(y, 4, y, 4, 2),
                       K.cup(dy, 5, y, 4, 3), K.cup(dy, 5, dy, 5, 4))
        dR, dx = K.d(R, 4), K.d(x, 4)
        lhs = add(F(add(x, R)), F(x),
                  K.d(add(K.cup(x, 4, R, 4, 3), K.cup(x, 4, dR, 5, 4)), 5))
        rhs = add(K.cup(w, 2, R, 4), K.cup(R, 4, R, 4, 2), K.cup(dR, 5, R, 4, 3),
                  K.cup(dR, 5, dx, 5, 4), K.cup(dR, 5, dR, 5, 4))
        bad += sum(lhs[f] != rhs[f] for f in lhs)
    return bad


def closed_background(K, rng):
    t = [rng.randrange(2) for _ in range(K.nv)]
    s = {(i, j): (t[i] + t[j]) % 2 for i, j in K.simplices(1)}
    w = add(K.d(K.rnd(1, rng), 1), K.cup(s, 1, s, 1))
    return w, s


def check_obstruction_conversion(trials=20):
    """Code obstruction (argument c = n4 + S + X, compact parities) minus the displayed one is exact.

    Arbitrary binary n4, S = n3 cup_2 n3, X (the s1 polynomial x), b = [beta^- n3]_2 and
    Gamma (the Majorana parity); Psi = dn4 + Gamma, so dn4 = Gamma + Psi = O5.
    """
    K = Complex(8)
    bad = 0
    for seed in range(trials):
        rng = random.Random(2000 + seed)
        w, s = closed_background(K, rng)
        n4, S, X, b = (K.rnd(4, rng) for _ in range(4))
        G = K.rnd(5, rng)
        On = K.d(n4, 4)
        P = add(On, G)
        dS, dX = K.d(S, 4), K.d(X, 4)
        Go, Po = add(G, dS), add(P, dX)
        c = add(n4, S, X)

        def Q(y):
            dy = K.d(y, 4)
            return add(K.cup(w, 2, y, 4), K.cup(y, 4, y, 4, 2), K.cup(dy, 5, y, 4, 3), K.cup(dy, 5, dy, 5, 4))
        code = add(Q(c), K.cup(w, 2, b, 4), K.cup(b, 4, b, 4, 2), K.cup(Go, 5, Po, 5, 4), K.cup(s, 1, Po, 5))
        Rg = add(K.cup(w, 2, add(S, b), 4), K.cup(S, 4, S, 4, 2), K.cup(b, 4, b, 4, 2),
                 K.cup(S, 4, dS, 5, 3), K.cup(dS, 5, G, 5, 4))
        Rp = add(K.cup(w, 2, X, 4), K.cup(X, 4, X, 4, 2), K.cup(X, 4, dX, 5, 3), K.cup(P, 5, dX, 5, 4))
        shown = add(Q(n4), K.cup(G, 5, P, 5, 4), K.cup(s, 1, P, 5), Rg, Rp)
        B = add(S, X)
        Y = add(K.cup(n4, 4, B, 4, 3), K.cup(n4, 4, K.d(B, 4), 5, 4), K.cup(S, 4, X, 4, 3),
                K.cup(S, 4, dX, 5, 4), K.cup(S, 4, dS, 5, 4), K.cup(X, 4, dX, 5, 4),
                K.cup(dX, 5, add(dS, On), 5, 5), K.cup(s, 1, X, 4))
        lhs = add(code, shown, K.d(Y, 5))
        bad += sum(lhs.values())
    return bad


def check_stacking_identity(trials=20):
    """Code complex-fermion products, transported to n4 and N4 = n4 + n'4 + E4, give the
    displayed E5^c, E5^{c gamma}, E5^{c psi} plus the explicit occupation bracket."""
    K = Complex(7)
    bad = 0
    c3 = lambda a, b: K.cup(a, 4, b, 4, 3)
    x54 = lambda a, b: K.cup(a, 5, b, 4, 4)
    y45 = lambda a, b: K.cup(a, 4, b, 5, 4)
    for seed in range(trials):
        rng = random.Random(1000 + seed)
        w, s = closed_background(K, rng)
        n, m, E = (K.rnd(4, rng) for _ in range(3))
        S, Sp, SN, X, Xp, XN = (K.rnd(4, rng) for _ in range(6))
        beta = K.rnd(3, rng)
        dbeta = K.d(beta, 3)
        N = add(n, m, E)
        y, yp, yN = add(S, X), add(Sp, Xp), add(SN, XN)
        Dy = add(yN, y, yp)
        O, Op, ON = K.d(n, 4), K.d(m, 4), K.d(N, 4)
        # code products with argument n4 + y and stacked argument N + y_N + d beta
        xc, xpc, Xc = add(n, y), add(m, yp), add(N, yN, dbeta)
        Eold = add(E, Dy, dbeta)
        code = add(c3(xc, xpc), c3(add(xc, xpc), Eold), x54(K.d(xc, 4), xpc), y45(Xc, K.d(Xc, 4)),
                   y45(xc, K.d(xc, 4)), y45(xpc, K.d(xpc, 4)))

        def Yprime(S_, X_, O_):
            dS_, dX_ = K.d(S_, 4), K.d(X_, 4)
            return add(K.cup(S_, 4, X_, 4, 3), K.cup(S_, 4, dX_, 5, 4), K.cup(S_, 4, dS_, 5, 4),
                       K.cup(X_, 4, dX_, 5, 4), K.cup(dX_, 5, add(dS_, O_), 5, 5), K.cup(s, 1, X_, 4))

        def Ytot(u, S_, X_, O_):
            B_ = add(S_, X_)
            return add(c3(u, B_), y45(u, K.d(B_, 4)), Yprime(S_, X_, O_))
        DY = add(Ytot(N, SN, XN, ON), Ytot(n, S, X, O), Ytot(m, Sp, Xp, Op))
        cvar = add(N, yN)
        F45 = add(K.cup(w, 2, beta, 3), K.cup(cvar, 4, dbeta, 4, 3), K.cup(beta, 3, dbeta, 4, 2),
                  K.cup(beta, 3, beta, 3, 1))
        sigma = K.d(K.cup(y, 4, m, 4, 4), 4)
        lhs = add(code, DY, F45, sigma, K.cup(s, 1, Dy, 4))
        P = add(c3(n, m), c3(add(n, m), E), x54(O, m), y45(N, ON), y45(n, O), y45(m, Op))

        def Z1(S_, X_, O_):
            dS_, dX_ = K.d(S_, 4), K.d(X_, 4)
            return add(y45(add(S_, X_), O_), K.cup(S_, 4, X_, 4, 3), y45(X_, dS_),
                       K.cup(dX_, 5, add(O_, dS_), 5, 5), K.cup(s, 1, S_, 4))
        Qb = add(K.cup(w, 2, beta, 3), K.cup(beta, 3, beta, 3, 1), K.cup(beta, 3, dbeta, 4, 2))
        bracket = add(c3(y, yp), c3(add(y, yp), add(E, Dy, dbeta)), c3(E, add(yN, dbeta)),
                      x54(add(O, K.d(y, 4)), yp), y45(y, Op), K.cup(dbeta, 4, add(ON, K.d(yN, 4)), 5, 4),
                      c3(yN, dbeta), Qb, Z1(SN, XN, ON), Z1(S, X, O), Z1(Sp, Xp, Op))
        rhs = add(P, bracket)
        diff = add(lhs, rhs)
        bad += sum(diff.values())
    return bad


def main():
    results = {
        'obstruction identity (arbitrary cochains)': check_obstruction_identity(),
        'obstruction conversion (arbitrary cochains)': check_obstruction_conversion(),
        'stacking identity (arbitrary cochains)': check_stacking_identity(),
    }
    for name, bad in results.items():
        print(f'{name}: {"PASS" if bad == 0 else f"FAIL ({bad} mismatches)"}')
    if any(results.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
