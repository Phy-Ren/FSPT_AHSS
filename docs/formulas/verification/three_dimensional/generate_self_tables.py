#!/usr/bin/env python3
"""Regenerate the two face tables of the torsion self-stacking page.

For n1 = s1 the mixed and pure contributions of the general twister with two
equal inputs, minus the explicit terms printed on the page, are half-valued
functions of the 16 face values of s1, omega2 and n2 on faces containing the
vertex 0.  Evaluating them on all 2^16 values and taking the algebraic normal
form gives the face tables.  The script compares them with the tables of
THREE_DIMENSIONAL_SELF_STACKING_FACES_*.md and writes both sets of monomials.

Usage: generate_self_tables.py   (about three minutes on 32 cores)
"""
import json
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path

import formulas as F
import self_stacking as S
from towers import torsion_state, TORSION_VARIABLES

HERE = Path(__file__).resolve().parent
FREE = [v for v in TORSION_VARIABLES if v[0] != 'n_3']
NAMES = {'s_1': 's_1', 'omega_2': r'\omega_2', 'n_2': 'n_2'}


def bits(k):
    values = {v: 0 for v in TORSION_VARIABLES}
    for j, v in enumerate(FREE):
        values[v] = (k >> j) & 1
    s, w, x = torsion_state(values)
    top = tuple(range(5))
    general = F.E4_parts(x, x, s, w, top)
    S.TABLES.update(MIXED=[], PURE=[])
    explicit = S.torsion_branch(x, s, w, top)
    out = []
    for sector in ('gammapsi', 'psi'):
        rest = (general[sector] - explicit[sector]) % 1
        assert rest in (0, Fraction(1, 2)), (k, sector, rest)
        out.append(int(2 * rest))
    return out


def anf(values):
    a = list(values)
    for i in range(len(FREE)):
        step = 1 << i
        for k in range(len(a)):
            if k & step:
                a[k] ^= a[k ^ step]
    return {k for k, v in enumerate(a) if v}


def page_table(kind):
    index = {(NAMES[name], face): j for j, (name, face) in enumerate(FREE)}
    return {sum(1 << index[factor] for factor in row) for row in S.read_table(kind)}


def main():
    with Pool() as pool:
        rows = pool.map(bits, range(1 << len(FREE)), chunksize=256)
    report = {}
    for i, (sector, kind) in enumerate((('gammapsi', 'MIXED'), ('psi', 'PURE'))):
        generated, printed = anf(r[i] for r in rows), page_table(kind)
        report[sector] = dict(generated=len(generated), printed=len(printed),
                              equal=generated == printed,
                              monomials=[[f'{NAMES[FREE[j][0]]}({"".join(map(str, FREE[j][1]))})'
                                          for j in range(len(FREE)) if m >> j & 1]
                                         for m in sorted(generated)])
    ok = all(r['equal'] for r in report.values())
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results/self_tables.json').write_text(json.dumps(
        dict(status='PASS' if ok else 'FAIL', variables=len(FREE), points=1 << len(FREE),
             tables=report), indent=1) + '\n')
    print(json.dumps({k: {x: y for x, y in v.items() if x != 'monomials'}
                      for k, v in report.items()}, indent=1))
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
