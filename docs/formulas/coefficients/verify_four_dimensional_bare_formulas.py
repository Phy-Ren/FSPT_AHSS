#!/usr/bin/env python3
"""Checks of the 4+1D complex-fermion terms in the occupation n_4, standard library only.

The formula pages write the complex-fermion layer in the physical occupation
n_4, dn_4 = O_5. The transfer construction of the code evaluates its products in
its own complex-fermion coordinate C = n_4 + t, with t = n_3 cup_2 n_3 + P for each
state (P the one-state polynomial of the last bracket of E_4^psi), lower stacking
correction e = E_4 + Delta t + d(n_3 cup_3 n'_3) and stacked coordinate
N_4 + t_N + d(n_3 cup_3 n'_3). For arbitrary cochains mod 2 this script checks

1. the obstruction identity, with F[c] = 1/2[w_2 c + c cup_2 c + dc cup_3 c + dc cup_4 dc],
       F[c+R] - F[c] = d(1/2[c cup_3 R + c cup_4 dR])
                       + 1/2[w_2 R + R cup_2 R + dR cup_3 R + dR cup_4 dc + dR cup_4 dR];
2. the occupation dependence of the stacking correction: the complex-fermion
   products of the transfer construction in C, C', together with the occupation
   change Delta(1/2[c cup_4 dc + s_1 c + c cup_3 t]) (stacked occupation N_4 + d beta)
   and the gauge terms 1/2[N_4 cup_3 d beta + d(t cup_4 n'_4)], differ from the
   displayed E_5^c + E_5^{c gamma} + E_5^{c psi} in n_4 by a cochain that does not
   change when n_4, n'_4 change by cocycles: the displayed complex-fermion
   contributions contain every term that depends on the occupations. The
   remainder is the occupation part of the lower contributions
   (full4/physical.py:occupation_terms).

All half-valued phases are compared as cochains mod 2 (twice the phase).
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


def check_occupation_dependence(trials=20):
    """Transported code products minus the displayed complex-fermion contributions
    are unchanged by n4 -> n4 + dz, n'4 -> n'4 + dz'."""
    K = Complex(7)
    bad = 0
    c3 = lambda a, b: K.cup(a, 4, b, 4, 3)
    c4 = lambda a, b: K.cup(a, 4, b, 5, 4)
    x54 = lambda a, b: K.cup(a, 5, b, 4, 4)
    for seed in range(trials):
        rng = random.Random(3000 + seed)
        w, s = closed_background(K, rng)
        E, t, tp, tN = (K.rnd(4, rng) for _ in range(4))
        beta = K.rnd(3, rng)
        db = K.d(beta, 3)
        Dt = add(tN, t, tp)
        e = add(E, Dt, db)

        def remainder(n, m):
            O, Op = K.d(n, 4), K.d(m, 4)
            N = add(n, m, E)
            ON = K.d(N, 4)
            C, Cp = add(n, t), add(m, tp)
            code = add(c3(C, Cp), x54(K.d(C, 4), Cp), c3(add(C, Cp), e))
            for c, y in ((add(N, db), tN), (n, t), (m, tp)):
                code = add(code, c4(c, K.d(c, 4)), K.cup(s, 1, c, 4), c3(c, y))
            code = add(code, c3(N, db), K.d(K.cup(t, 4, m, 4, 4), 4))
            shown = add(c3(n, m), c3(add(n, m), E), x54(O, m), c4(N, ON), c4(n, O), c4(m, Op))
            return add(code, shown)
        n, m = K.rnd(4, rng), K.rnd(4, rng)
        r0 = remainder(n, m)
        r1 = remainder(add(n, K.d(K.rnd(3, rng), 3)), add(m, K.d(K.rnd(3, rng), 3)))
        bad += sum(r0[f] != r1[f] for f in r0)
    return bad


def main():
    results = {
        'obstruction identity (arbitrary cochains)': check_obstruction_identity(),
        'occupation dependence of the stacking correction (arbitrary cochains)': check_occupation_dependence(),
    }
    for name, bad in results.items():
        print(f'{name}: {"PASS" if bad == 0 else f"FAIL ({bad} mismatches)"}')
    if any(results.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
