"""Solve  R = d_s sigma_4  for the local four-cochain sigma_4 (Z/8, bin/z8solve), where

    R = E_5^gamma + E^c + E^{cg} - E_AHSS - (B_5[N] - B_5[n] - B_5[n'])    on Delta^5,

E_AHSS = majorana_complete.stacking(n3, n4, n3', n4', omega2, s1), operator coordinate.
sigma_4 is keyed by its four-face: n3, n3' cone bits (4 + 4), n4, n4', omega2(012),
s1(01), s1(02) (13 bits).  Writes the 8192-entry table and verifies it on fresh samples.

usage: python3 fit_sigma4.py E5.bin out_sigma4.bin [--equations N] [--verify N] [--seed S] [--jobs J]
"""
import argparse
import os
import subprocess
from multiprocessing import Pool

import numpy as np

import cochains as C

ap = argparse.ArgumentParser()
ap.add_argument("e5"); ap.add_argument("out")
ap.add_argument("--b5", default=os.path.join(C.DATA, "B5gamma_15bit.bin"))
ap.add_argument("--equations", type=int, default=20000)
ap.add_argument("--verify", type=int, default=20000)
ap.add_argument("--seed", type=int, default=1)
ap.add_argument("--jobs", type=int, default=8)
args = ap.parse_args()
E5 = C.load(args.e5, 23)
B5 = C.load(args.b5, 15)
SOLVER = os.path.join(C.HERE, "..", "bin", "z8solve")


def rows(a):
    n, sd = a
    rng = C.rng_for(sd)
    out = []
    for _ in range(n):
        d = C.random_five_simplex(rng)
        out.append((C.stacking_residual(E5, B5, d), C.sigma4_equation(d)))
    return out


def gather(n, sd, pool):
    per = max(1, n // (4 * args.jobs))
    res = []
    for part in pool.imap_unordered(rows, [(min(per, n - i), sd * 7919 + i) for i in range(0, n, per)]):
        res += part
    return res


if __name__ == "__main__":
    with Pool(args.jobs) as pool:
        eqs = gather(args.equations, args.seed, pool)
        ver = gather(args.verify, args.seed + 1, pool)
    keys = sorted({k for _, c in eqs for k in c})
    col = {k: i for i, k in enumerate(keys)}
    lines = [f"{len(eqs)} {len(keys)}"]
    for R, c in eqs:
        items = [(col[k], v & 7) for k, v in c.items() if v & 7]
        lines.append(" ".join([str(len(items))] + [f"{a} {b}" for a, b in items] + [str(R)]))
    res = subprocess.run([SOLVER], input="\n".join(lines), capture_output=True, text=True).stdout.split()
    print(f"equations {len(eqs)}, unknowns {len(keys)}: {'solved' if res and res[0] == 'OK' else 'NO SOLUTION'}")
    if not res or res[0] != "OK":
        raise SystemExit(1)
    sigma = np.zeros(1 << 13, dtype=np.int8)
    for k in keys:
        sigma[k] = int(res[1 + col[k]])
    bad = sum((sum(v * int(sigma[k]) for k, v in c.items()) - R) % 8 != 0 for R, c in ver)
    print(f"fresh samples {len(ver)}: bad {bad}", "PASS" if bad == 0 else "FAIL")
    sigma.tofile(args.out)
    raise SystemExit(0 if bad == 0 else 1)
