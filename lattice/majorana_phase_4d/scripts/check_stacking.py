"""Stacking compatibility of the lattice phases (full phases, general omega2, s1):

    d_s( E^c + E^{cg} + E_5^gamma ) = O_tot[N] - O_tot[n] - O_tot[n']    on Delta^6,
    O_tot = O_6^gamma + O^c + O^{cg}.

Every E_5 row K in [lo, hi) is checked once: the face 012345 of Delta^6 carries row K, the
remaining n3, n3', omega2, s1 data and the solutions n4, n4' are random.

usage: python3 check_stacking.py E5.bin O6.bin [lo hi] [--seed S] [--jobs J]
"""
import argparse
from collections import Counter
from multiprocessing import Pool

import cochains as C

ap = argparse.ArgumentParser()
ap.add_argument("e5"); ap.add_argument("o6")
ap.add_argument("lo", nargs="?", type=int, default=0)
ap.add_argument("hi", nargs="?", type=int, default=1 << 23)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--jobs", type=int, default=8)
args = ap.parse_args()
E5 = C.load(args.e5, 23)
O6 = C.load(args.o6, 25)
INNER = [C.C6.index(c) for c in C.C5]          # cone bits of Delta^6 lying on 012345
OUTER = [i for i in range(20) if i not in INNER]


def check(K, rng):
    nb = sum(((K >> j) & 1) << INNER[j] for j in range(10))
    npb = sum(((K >> (10 + j)) & 1) << INNER[j] for j in range(10))
    for i in OUTER:
        nb |= rng.randrange(2) << i
        npb |= rng.randrange(2) << i
    n3, n3p = C.cone(nb, 3, 6), C.cone(npb, 3, 6)
    h = [0, (K >> 21) & 1, (K >> 22) & 1] + [rng.randrange(2) for _ in range(4)]
    s = C.s_from_potential(h, 6)
    while True:   # omega2 = d c1 with omega2(012) fixed by the row
        c1 = {e: rng.randrange(2) for e in C.faces(1, 6)}
        w = {(a, b, c): (c1[(b, c)] + c1[(a, c)] + c1[(a, b)]) & 1 for a, b, c in C.faces(2, 6)}
        if w[(0, 1, 2)] == (K >> 20) & 1:
            break
    d = {"n3": n3, "n3p": n3p, "w": w, "s": s}
    d["n4"] = C.solve_n4(d, "n3", 6, rng)
    d["n4p"] = C.solve_n4(d, "n3p", 6, rng)
    if C.evaluate(C.PARITY_N4, d):
        raise AssertionError("parity rule of the stacked layer violated")
    N3 = {f: (n3[f] + n3p[f]) & 1 for f in n3}
    dE = 0
    for r, c in enumerate(C.twisted_coefficients(s, 6)):
        f = tuple(v for v in range(7) if v != r)
        dE += c * int(E5[C.e5_key(n3, n3p, w, s, f)])
    full = tuple(range(7))
    dO = sum(sg * int(O6[C.o6_key(x, w, s, full)]) for sg, x in ((1, N3), (-1, n3), (-1, n3p)))
    comp = C.evaluate(C.D_E_COMPLEX, d) - C.evaluate(C.DELTA_O_COMPLEX, d)
    return (dE + comp - dO) % 8


def run(a):
    lo, hi, sd = a
    rng = C.rng_for(sd)
    H, F = Counter(), []
    for K in range(lo, hi):
        r = check(K, rng)
        H[r] += 1
        if r and len(F) < 5:
            F.append(K)
    return H, F


if __name__ == "__main__":
    H, F = Counter(), []
    with Pool(args.jobs) as p:
        for h, f in p.imap_unordered(run, C.chunks(args.lo, args.hi, 2048, args.seed)):
            H.update(h); F += f
    ok = set(H) == {0}
    print(f"rows {args.lo}..{args.hi}: residual histogram {dict(sorted(H.items()))}",
          "PASS" if ok else f"FAIL (first rows {F[:5]})")
    raise SystemExit(0 if ok else 1)
