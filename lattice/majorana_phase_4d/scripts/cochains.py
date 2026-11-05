"""Shared cochain data and formulas for the checks of the lattice Majorana phases.

Phases are integer numerators of 1/8.  Simplices are vertex tuples; binary cochains are
dicts {face: 0/1}.  The repository's own formula package (fspt) is used for every cup
product and for the FSPT_AHSS laws.
"""
import os
import random
import sys
from itertools import combinations

import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.normpath(os.path.join(HERE, "..", "..", ".."))
sys.path.insert(0, REPO)

from fspt.formulas import cup, evaluate, field, phase  # noqa: E402
from fspt.majorana_complete import expression  # noqa: E402

DATA = os.path.join(HERE, "..", "data")

# --------------------------------------------------------------- formulas
n3f, n3pf, wf, sf = field("n3", 3), field("n3p", 3), field("w", 2), field("s", 1)
n4f, n4pf = field("n4", 4), field("n4p", 4)

# parity of the Majorana layer and of the stacked layer
Q = lambda x: cup(x, x, 1) + cup(wf, x) + cup(sf, cup(x, x, 2))  # noqa: E731
M4 = cup(n3f, n3pf, 2) + cup(sf, cup(n3f, n3pf, 3))
N4 = n4f + n4pf + M4
_dn, _dnp, _dN = n4f.differential(), n4pf.differential(), N4.differential()

# complex-fermion parts of the lattice construction (P4 root formulas)
EPS_C = cup(M4, N4, 3) + cup(n4f, n4pf, 3) + cup(n4f, _dnp, 4)
EPS_CG = (cup(M4, _dn + _dnp, 4) + cup(_dn, _dnp, 5) + cup(_dN, M4, 4) + cup(M4, M4, 3)
          + M4.differential())
E_COMPLEX = phase((4, EPS_C + EPS_CG))                       # E^c + E^{cg}
D_E_COMPLEX = E_COMPLEX.differential().reduce(8)


def o_complex(x):
    """O^c + O^{cg} = (1/2)[omega2 x + x u2 x + dx u3 x + dx u4 dx]."""
    dx = x.differential()
    return phase((4, cup(wf, x) + cup(x, x, 2) + cup(dx, x, 3) + cup(dx, dx, 4)))


DELTA_O_COMPLEX = (o_complex(N4) - o_complex(n4f) - o_complex(n4pf)).reduce(8)
PARITY_N4 = (_dN - Q(n3f + n3pf)).reduce(2)

# FSPT_AHSS (majorana_complete.py, q = 3, operator coordinate)
AHSS_STACKING = expression("stacking", 3, "operator")
AHSS_GAMMA = expression("obstruction", 3, "ca")      # with c = 0: the pure Majorana source


# --------------------------------------------------------------- data on a simplex
def faces(k, N):
    return list(combinations(range(N + 1), k + 1))


def cone(bits, k, N):
    """Closed binary k-cochain on Delta^N from its values on the faces containing 0."""
    o = {}
    for i, c in enumerate(combinations(range(1, N + 1), k)):
        o[(0,) + c] = (bits >> i) & 1
    for f in faces(k, N):
        if f[0] != 0:
            o[f] = sum(o[(0,) + f[:i] + f[i + 1:]] for i in range(k + 1)) & 1
    return o


def s_from_potential(h, N):
    return {(i, j): (h[i] + h[j]) & 1 for i, j in faces(1, N)}


def solve_n4(data, name, N, rng):
    """A solution of dn4 = Q(n3) on Delta^N plus a random closed shift."""
    src = Q(field(name, 3))
    sol = {f: (0 if f[0] == 0 else evaluate(src, data, (0,) + f) % 2) for f in faces(4, N)}
    c3 = {f: rng.randrange(2) for f in faces(3, N)}
    for f in faces(4, N):
        sol[f] = (sol[f] + sum(c3[f[:i] + f[i + 1:]] for i in range(5))) & 1
    return sol


# --------------------------------------------------------------- table keys
C5 = list(combinations(range(1, 6), 3))   # cone faces of a five-simplex
C6 = list(combinations(range(1, 7), 3))   # cone faces of a six-simplex
C4 = list(combinations(range(1, 5), 3))   # cone faces of a four-simplex


def e5_key(n3, n3p, w, s, f):
    k = 0
    for i, (a, b, c) in enumerate(C5):
        t = (f[0], f[a], f[b], f[c])
        k |= n3[t] << i | n3p[t] << (i + 10)
    return k | w[f[:3]] << 20 | s[(f[0], f[1])] << 21 | s[(f[0], f[2])] << 22


def o6_key(n3, w, s, f):
    k = 0
    for i, (a, b, c) in enumerate(C6):
        k |= n3[(f[0], f[a], f[b], f[c])] << i
    g = lambda *l: w[tuple(f[i] for i in l)]  # noqa: E731
    return (k | g(0, 1, 2) << 20 | g(0, 1, 3) << 21 | g(0, 2, 3) << 22
            | s[(f[0], f[1])] << 23 | s[(f[0], f[2])] << 24)


def b5_key(x3, w, s, f):
    k = 0
    for i, (a, b, c) in enumerate(C5):
        k |= x3[(f[0], f[a], f[b], f[c])] << i
    g = lambda *l: w[tuple(f[i] for i in l)]  # noqa: E731
    return (k | g(0, 1, 2) << 10 | g(0, 1, 3) << 11 | g(0, 2, 3) << 12
            | s[(f[0], f[1])] << 13 | s[(f[0], f[2])] << 14)


def sigma4_key(d, f):
    k = 0
    for sh, (x, (a, b, c)) in enumerate([(x, t) for x in ("n3", "n3p") for t in C4]):
        k |= d[x][(f[0], f[a], f[b], f[c])] << sh
    k |= d["n4"][f] << 8 | d["n4p"][f] << 9
    return k | (d["w"][f[:3]] | d["s"][(f[0], f[1])] << 1 | d["s"][(f[0], f[2])] << 2) << 10


def twisted_coefficients(s, N):
    """Coefficients of the twisted coboundary on Delta^N: face r gets (-1)^r, and the face
    opposite to 0 is acted on by g_0^{-1} g_1, i.e. negated when s1(01) = 1."""
    c = [(-1) ** r for r in range(N + 1)]
    if s[(0, 1)]:
        c[0] = -c[0]
    return c


def load(name, bits):
    a = np.fromfile(name, dtype=np.int8)
    if a.size != 1 << bits:
        raise ValueError(f"{name}: expected 2^{bits} entries, found {a.size}")
    if (a < 0).any():
        raise ValueError(f"{name}: contains vanishing loops")
    return a


def random_five_simplex(rng, key=None):
    """Data on Delta^5.  With key (an E_5 row) the five-simplex carries that row and the
    remaining omega2 cone bits, s1(03),(04),(05), n4 and n4' are random."""
    if key is None:
        key = rng.randrange(1 << 23)
    wb = (rng.randrange(1 << 10) & ~1) | ((key >> 20) & 1)        # cone bit (1,2) = omega2(012)
    h = [0, (key >> 21) & 1, (key >> 22) & 1] + [rng.randrange(2) for _ in range(3)]
    d = {"n3": cone(key & 1023, 3, 5), "n3p": cone((key >> 10) & 1023, 3, 5),
         "w": cone(wb, 2, 5), "s": s_from_potential(h, 5)}
    d["n4"] = solve_n4(d, "n3", 5, rng)
    d["n4p"] = solve_n4(d, "n3p", 5, rng)
    return d


def stacking_residual(E5, B5, d):
    """R = E_phys - E_AHSS - (B5[N] - B5[n] - B5[n']) on the five-simplex 012345."""
    f = tuple(range(6))
    n3, n3p, w, s = d["n3"], d["n3p"], d["w"], d["s"]
    N3 = {k: (n3[k] + n3p[k]) & 1 for k in n3}
    e_phys = int(E5[e5_key(n3, n3p, w, s, f)]) + evaluate(E_COMPLEX, d)
    e_ahss = evaluate(AHSS_STACKING, {"a": n3, "b": n3p, "c": d["n4"], "cp": d["n4p"], "w": w, "s": s})
    db = int(B5[b5_key(N3, w, s, f)]) - int(B5[b5_key(n3, w, s, f)]) - int(B5[b5_key(n3p, w, s, f)])
    return (e_phys - e_ahss - db) % 8


def sigma4_equation(d):
    """Coefficients of d_s sigma_4 on the five-simplex: {sigma4 key: coefficient}."""
    coef = {}
    for r, c in enumerate(twisted_coefficients(d["s"], 5)):
        f = tuple(v for v in range(6) if v != r)
        k = sigma4_key(d, f)
        coef[k] = coef.get(k, 0) + c
    return coef


def chunks(lo, hi, size, seed):
    return [(a, min(a + size, hi), seed * 1000003 + a) for a in range(lo, hi, size)]


def rng_for(seed):
    return random.Random(seed)
