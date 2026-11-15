#!/usr/bin/env python3
"""Checks of the 4+1D change from the code argument n_4 + B_4 to n_4, standard library only.

The publication code evaluates the complex-fermion layer with the argument
x = n_4 + B_4.  The formula pages use n_4 itself; the change of phase is
    rho = 1/2[n_4 cup_3 B_4 + n_4 cup_4 dB_4].
For arbitrary binary cochains this script checks

1. the obstruction identity, with F[x] = 1/2[w_2 x + x cup_2 x + dx cup_3 x + dx cup_4 dx],
       F[x+R] - F[x] = d(1/2[x cup_3 R + x cup_4 dR])
                       + 1/2[w_2 R + R cup_2 R + dR cup_3 R + dR cup_4 dx + dR cup_4 dR];
2. the stacking identity: the code products c, c gamma, c psi in the arguments
   n_4 + B_4, plus Delta(rho), equal the displayed E_5^c, E_5^{c gamma} and E_5^{c psi},
   with N_4 = n_4 + n'_4 + E_4 + Delta B_4.

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


def check_stacking_identity(trials=20):
    K = Complex(7)
    bad = 0

    def c3(a, b): return K.cup(a, 4, b, 4, 3)
    def x54(a, b): return K.cup(a, 5, b, 4, 4)
    def y45(a, b): return K.cup(a, 4, b, 5, 4)
    for seed in range(trials):
        rng = random.Random(1000 + seed)
        n, m, N, R, Rm, RN = (K.rnd(4, rng) for _ in range(6))
        # O_5 = A + P: A the Majorana parts, P the p+ip part
        A, Am, AN, P, Pm, PN = (K.rnd(5, rng) for _ in range(6))
        O, Om, ON = add(A, P), add(Am, Pm), add(AN, PN)
        x, xm, X = add(n, R), add(m, Rm), add(N, RN)
        E4 = add(X, x, xm)                      # N_4 = n_4 + n'_4 + E_4 + Delta B_4
        code = add(c3(x, xm), c3(add(x, xm), E4),
                   x54(A, xm), y45(X, AN), y45(x, A), y45(xm, Am),
                   x54(P, xm), y45(X, PN), y45(x, P), y45(xm, Pm))

        def rho(u, r): return add(c3(u, r), y45(u, K.d(r, 4)))
        lhs = add(code, rho(N, RN), rho(n, R), rho(m, Rm))

        def Delta(f): return add(f(N, RN, ON, AN, PN), f(n, R, O, A, P), f(m, Rm, Om, Am, Pm))
        Ec = add(c3(n, m), c3(add(n, m), E4))
        Ecg = add(x54(A, m), Delta(lambda u, r, o, a, p: y45(u, a)),
                  c3(n, Rm), c3(R, m), c3(R, Rm), c3(add(R, Rm), E4), x54(O, Rm),
                  Delta(lambda u, r, o, a, p: add(y45(r, o), y45(u, K.d(r, 4)), c3(u, r))))
        Ecp = add(x54(P, m), Delta(lambda u, r, o, a, p: y45(u, p)))
        rhs = add(Ec, Ecg, Ecp)
        bad += sum(lhs[f] != rhs[f] for f in lhs)
    return bad


def main():
    results = {
        'obstruction identity (arbitrary cochains)': check_obstruction_identity(),
        'stacking identity (arbitrary cochains)': check_stacking_identity(),
    }
    for name, bad in results.items():
        print(f'{name}: {"PASS" if bad == 0 else f"FAIL ({bad} mismatches)"}')
    if any(results.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
