"""Heptagon phase against FSPT_AHSS:  O_6^gamma = gamma_AHSS[n3] + d_s B_5^gamma  on Delta^6.

gamma_AHSS is majorana_complete.obstruction(n3, 0, omega2, s1) (pure Majorana source,
quarter bracket -1/4); B_5^gamma is data/B5gamma_15bit.bin.  Random closed n3, omega2, s1.

usage: python3 check_o6_formula.py O6.bin [--samples N] [--seed S] [--jobs J]
"""
import argparse
import os
from collections import Counter
from multiprocessing import Pool

import cochains as C

ap = argparse.ArgumentParser()
ap.add_argument("o6")
ap.add_argument("--b5", default=os.path.join(C.DATA, "B5gamma_15bit.bin"))
ap.add_argument("--samples", type=int, default=20000)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--jobs", type=int, default=8)
args = ap.parse_args()
O6 = C.load(args.o6, 25)
B5 = C.load(args.b5, 15)


def one(rng):
    n3 = C.cone(rng.randrange(1 << 20), 3, 6)
    w = C.cone(rng.randrange(1 << 15), 2, 6)
    s = C.s_from_potential([0] + [rng.randrange(2) for _ in range(6)], 6)
    full = tuple(range(7))
    g = C.evaluate(C.AHSS_GAMMA, {"a": n3, "c": {f: 0 for f in C.faces(4, 6)}, "w": w, "s": s})
    db = 0
    for r, c in enumerate(C.twisted_coefficients(s, 6)):
        db += c * int(B5[C.b5_key(n3, w, s, tuple(v for v in range(7) if v != r))])
    return (int(O6[C.o6_key(n3, w, s, full)]) - g - db) % 8


def run(a):
    n, sd = a
    rng = C.rng_for(sd)
    return Counter(one(rng) for _ in range(n))


if __name__ == "__main__":
    H = Counter()
    with Pool(args.jobs) as p:
        for h in p.imap_unordered(run, [(1000, args.seed * 100003 + i) for i in range(args.samples // 1000)]):
            H.update(h)
    ok = set(H) == {0}
    print(f"samples {sum(H.values())}: residual histogram {dict(sorted(H.items()))}", "PASS" if ok else "FAIL")
    raise SystemExit(0 if ok else 1)
