"""Stacking phase against FSPT_AHSS on every E_5 row:

    E_5^gamma + E^c + E^{cg} = E_AHSS + B_5[N] - B_5[n] - B_5[n'] + d_s sigma_4,

E_AHSS = majorana_complete.stacking (operator coordinate).  The five-simplex carries row K;
the remaining omega2 and s1 data and n4, n4' are random.

usage: python3 check_e5_formula.py E5.bin [lo hi] [--sigma4 F] [--seed S] [--jobs J]
"""
import argparse
import os
from collections import Counter
from multiprocessing import Pool

import cochains as C

ap = argparse.ArgumentParser()
ap.add_argument("e5")
ap.add_argument("lo", nargs="?", type=int, default=0)
ap.add_argument("hi", nargs="?", type=int, default=1 << 23)
ap.add_argument("--b5", default=os.path.join(C.DATA, "B5gamma_15bit.bin"))
ap.add_argument("--sigma4", default=os.path.join(C.DATA, "sigma4_13bit.bin"))
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--jobs", type=int, default=8)
args = ap.parse_args()
E5 = C.load(args.e5, 23)
B5 = C.load(args.b5, 15)
S4 = C.load(args.sigma4, 13)


def run(a):
    lo, hi, sd = a
    rng = C.rng_for(sd)
    H, F = Counter(), []
    for K in range(lo, hi):
        d = C.random_five_simplex(rng, K)
        lhs = sum(v * int(S4[k]) for k, v in C.sigma4_equation(d).items())
        r = (C.stacking_residual(E5, B5, d) - lhs) % 8
        H[r] += 1
        if r and len(F) < 5:
            F.append(K)
    return H, F


if __name__ == "__main__":
    H, F = Counter(), []
    with Pool(args.jobs) as p:
        for h, f in p.imap_unordered(run, C.chunks(args.lo, args.hi, 4096, args.seed)):
            H.update(h); F += f
    ok = set(H) == {0}
    print(f"rows {args.lo}..{args.hi}: residual histogram {dict(sorted(H.items()))}",
          "PASS" if ok else f"FAIL (first rows {F[:5]})")
    raise SystemExit(0 if ok else 1)
