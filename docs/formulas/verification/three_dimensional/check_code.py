#!/usr/bin/env python3
"""The displayed 3+1D bosonic formulas against the phases of the publication code.

The code evaluates its bosonic construction with the complex-fermion argument
n3 + B3, B3 = n2 cup_1 n2, on each state, and with the stacked argument
N3 + B3[N] + dB2.  Its phases (after the representative change documented on
THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md) are stored as term lists in
code_phases/ and in docs/formulas/term_census/three_dimensional.  This script
checks, pointwise on random solutions of the lower equations,

  O5 = O5^code(n3+B3) + d_s1 rho,
  E4 = E4^code(n3+B3, n3'+B3') + 1/2[w2 B2 + B2^2 + dB2 cup_1 B2
       + (N3+B3[N]+dB2) cup_2 dB2] + Delta rho + 1/2 d K,
  rho = 1/2[n3 cup_2 B3 + n3 cup_3 dB3],
  K = n3' cup_3 B3 + (B3+B3') cup_3 E3 + (B3+B3') cup_2 lam + lam cup_2 dlam,

with lam = n2 cup_2 n2' and B2 the two-cochain of the general formula.
Usage: check_code.py [samples]
"""
import json
import random
import sys
from fractions import Fraction
from functools import lru_cache
from multiprocessing import Pool
from pathlib import Path

import formulas as F
from formulas import C, cup
from towers import background, faces, frozen, state

HERE = Path(__file__).resolve().parent


@lru_cache(None)
def code_phase(law, sector):
    if sector in ('GAMMAPSI', 'PSI'):
        return F.manifest(law, sector)
    return F.Manifest(HERE / 'code_phases' / f'{law}_{sector}.json')


def alphabet(x, y, s, w):
    A = F._alphabet(x, y, s, w)
    A['n_3+B_3'] = x['n3'] + cup(x['n2'], x['n2'], 1)
    if y is not None:
        A["n'_3+B'_3"] = y['n3'] + cup(y['n2'], y['n2'], 1)
    return A


def code_O5(x, s, w, f):
    A = alphabet(x, None, s, w)
    return sum(code_phase('O5', k)(A, s, f) for k in ('C', 'CGAMMA', 'CPSI', 'GAMMA',
                                                       'GAMMAPSI', 'PSI')) % 1


def rho(X):
    B = cup(X['n2'], X['n2'], 1)
    return cup(X['n3'], B, 2) + cup(X['n3'], B.d(), 3)


def obstruction(seed):
    rng = random.Random(seed)
    s, w = background(6, rng)
    x = state(6, rng, s, w)
    r = rho(x).d()
    return sum((F.O5(x, s, w, f) - code_O5(x, s, w, f) - Fraction(r(f) % 2, 2)) % 1 != 0
               for f in faces(6, 5))


def product(seed):
    rng = random.Random(seed)
    s, w = background(5, rng)
    x, y = state(5, rng, s, w), state(5, rng, s, w)
    Z = {k: frozen(v, 5) for k, v in F.stack(x, y, s, w).items()}
    A = alphabet(x, y, s, w)
    n2, m2 = x['n2'], y['n2']
    a, a2 = x['n1'].reduce(2), y['n1'].reduce(2)
    h, k = F.digit(x['n1'], 1), F.digit(y['n1'], 1)
    B2 = C(2, fun=lambda v: (
        a(v[:2]) * k(v[1:]) + h(v[:2]) * a2(v[1:]) + h(v[:2]) * k(v[1:]) + n2(v) * m2(v)
        + a(v[:2]) * a2(v[1:]) * (n2(v) + m2(v))
        + s(v[:2]) * (h(v[:2]) * a2(v[1:]) + a(v[:2]) * a2(v[:2]) * (a(v[1:]) + a2(v[1:])))))
    dB2 = B2.d()
    B, Bm, BN = cup(n2, n2, 1), cup(m2, m2, 1), cup(Z['n2'], Z['n2'], 1)
    output = Z['n3'] + BN + dB2
    face_phase = cup(w, B2) + cup(B2, B2) + cup(dB2, B2, 1) + cup(output, dB2, 2)
    lam = cup(n2, m2, 2)
    e3 = Z['n3'] + x['n3'] + y['n3']
    K = (cup(y['n3'], B, 3) + cup(B + Bm, e3, 3) + cup(B + Bm, lam, 2)
         + cup(lam, lam.d(), 2)).d()
    change = face_phase + rho(Z) + rho(x) + rho(y) + K
    bad = 0
    for f in faces(5, 4):
        code = sum(code_phase('E4', k)(A, s, f) for k in ('C', 'CGAMMA', 'CPSI', 'GAMMA',
                                                          'GAMMAPSI', 'PSI'))
        bad += (F.E4(x, y, s, w, f) - code - Fraction(change(f) % 2, 2)) % 1 != 0
    return bad


def main():
    samples = int(sys.argv[1]) if len(sys.argv) > 1 else 60
    with Pool() as pool:
        result = dict(obstruction=sum(pool.map(obstruction, range(6000, 6000 + samples))),
                      product=sum(pool.map(product, range(7000, 7000 + samples))))
    receipt = dict(status='PASS' if not any(result.values()) else 'FAIL', samples=samples,
                   mismatched_faces=result)
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results/code.json').write_text(json.dumps(receipt, indent=1) + '\n')
    print(json.dumps(receipt, indent=1))
    if any(result.values()):
        raise SystemExit(1)


if __name__ == '__main__':
    main()
