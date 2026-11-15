#!/usr/bin/env python3
"""Exact checks of the displayed 3+1D formulas.

closure       d_s1 O_5 = 0 on random solutions of the lower equations (Delta^6)
stacking      d_s1 E_4 = O_5[N] - O_5[n] - O_5[n'] (Delta^5)
closed        for n1 = n1' = 0, O_5 and E_4 equal the closed-sector formulas,
              and the c psi, gamma psi and psi contributions vanish
self_zero     self-stacking page, n1 = 0, against E_4 with equal inputs
self_torsion  self-stacking page, n1 = s1, every contribution against E_4 with
              equal inputs (random values of the 20 independent face bits)
Z4fT          roots and squares of the time-reversal example on all bar simplices

All phases are exact rationals modulo one.  Usage: check_formulas.py [samples]
"""
import json
import random
import sys
from fractions import Fraction
from itertools import product
from multiprocessing import Pool
from pathlib import Path

import closed
import formulas as F
import self_stacking as S
from formulas import C, ds
from towers import (background, faces, frozen, phase_difference, state,
                    torsion_state, TORSION_VARIABLES)

HERE = Path(__file__).resolve().parent
SECTORS = ('c', 'cgamma', 'cpsi', 'gamma', 'gammapsi', 'psi')


def closure(seed):
    rng = random.Random(seed)
    s, w = background(6, rng)
    x = state(6, rng, s, w)
    return int(phase_difference(lambda f: F.O5(x, s, w, f), 6, s) != 0)


def stacking(seed):
    rng = random.Random(seed)
    s, w = background(5, rng)
    x, y = state(5, rng, s, w), state(5, rng, s, w)
    Z = {k: frozen(v, 5) for k, v in F.stack(x, y, s, w).items()}
    top = tuple(range(6))
    lhs = phase_difference(lambda f: F.E4(x, y, s, w, f), 5, s)
    rhs = (F.O5(Z, s, w, top) - F.O5(x, s, w, top) - F.O5(y, s, w, top)) % 1
    return int(lhs != rhs)


def closed_sector(seed):
    rng = random.Random(seed)
    bad = dict(O5=0, E4=0, vanishing=0)
    s, w = background(6, rng)
    x = state(6, rng, s, w, pip=False)
    for f in faces(6, 5):
        parts = F.O5_parts(x, s, w, f)
        bad['O5'] += sum(parts.values()) % 1 != closed.O5(x['n2'], x['n3'], w, s, f)
        bad['vanishing'] += any(parts[k] for k in ('cpsi', 'gammapsi', 'psi'))
    s, w = background(5, rng)
    x, y = state(5, rng, s, w, pip=False), state(5, rng, s, w, pip=False)
    for f in faces(5, 4):
        parts = F.E4_parts(x, y, s, w, f)
        bad['E4'] += sum(parts.values()) % 1 != closed.E4(x['n2'], x['n3'], y['n2'], y['n3'], w, s, f)
        bad['vanishing'] += any(parts[k] for k in ('cpsi', 'gammapsi', 'psi'))
    return bad


def self_zero(seed):
    rng = random.Random(seed)
    s, w = background(4, rng)
    x = state(4, rng, s, w, pip=False)
    top = tuple(range(5))
    return int(S.zero_branch(x, s, w, top) != F.E4(x, x, s, w, top))


def self_torsion(seed):
    rng = random.Random(seed)
    s, w, x = torsion_state({v: rng.randrange(2) for v in TORSION_VARIABLES})
    top = tuple(range(5))
    page, general = S.torsion_branch(x, s, w, top), F.E4_parts(x, x, s, w, top)
    return {k: int(page[k] != general[k]) for k in SECTORS}


def z4ft():
    """G_b = Z_2, s1 = m1, omega2 = m1^2; m1^q(g_1,...,g_q) = g_1...g_q."""
    def fields(edges):
        v = [0]
        for e in edges:
            v.append(v[-1] ^ e)
        return lambda q, mod=2: C(q, fun=lambda f: int(all(v[a] != v[b] for a, b in zip(f, f[1:]))),
                                  mod=mod)
    roots = {'p+ip': ((1, 0, 0), Fraction(1, 4), (2, 1, 0), Fraction(1, 4)),
             'Majorana': ((0, 1, 0), Fraction(1, 4), (0, 0, 1), Fraction(0)),
             'complex fermion': ((0, 0, 1), Fraction(0), (0, 0, 0), Fraction(1, 2)),
             'bosonic': ((0, 0, 0), Fraction(1, 2), (0, 0, 0), Fraction(0))}
    report = {}
    for name, ((k1, k2, k3), nu, (K1, K2, K3), square) in roots.items():
        bad = dict(lower=0, obstruction=0, square_fields=0, square_phase=0)
        for edges in product((0, 1), repeat=5):
            m = fields(edges)
            s, w = m(1), m(2)
            x = dict(n1=m(1, None).scaled(k1), n2=m(2) if k2 else C(2), n3=m(3) if k3 else C(3))
            bad['lower'] += any((x['n2'].d()(f) - F.O3(x['n1'], w, s)(f)) % 2 for f in faces(5, 3))
            bad['lower'] += any((x['n3'].d()(f) - F.O4(x['n1'], x['n2'], w, s)(f)) % 2
                                for f in faces(5, 4))
            dnu = ds(m(4, None).scaled(nu), s)(tuple(range(6))) % 1
            bad['obstruction'] += dnu != F.O5(x, s, w, tuple(range(6)))
        for edges in product((0, 1), repeat=4):
            m = fields(edges)
            s, w = m(1), m(2)
            x = dict(n1=m(1, None).scaled(k1), n2=m(2) if k2 else C(2), n3=m(3) if k3 else C(3))
            Z = F.stack(x, x, s, w)
            bad['square_fields'] += any(Z['n1'](f) != K1 * m(1, None)(f) for f in faces(4, 1))
            bad['square_fields'] += any(Z['n2'](f) % 2 != K2 * m(2)(f) for f in faces(4, 2))
            bad['square_fields'] += any(Z['n3'](f) % 2 != K3 * m(3)(f) for f in faces(4, 3))
            top = tuple(range(5))
            phase = (2 * nu * m(4)(top) + F.E4(x, x, s, w, top)) % 1
            bad['square_phase'] += phase != square * m(4)(top)
        report[name] = dict(nu4=f'{nu} m1^4', square=f'({K1} m1, {K2} m1^2, {K3} m1^3, {square} m1^4)',
                            failures=bad)
    return report


def main():
    samples = int(sys.argv[1]) if len(sys.argv) > 1 else 100
    with Pool() as pool:
        result = {
            'closure': sum(pool.map(closure, range(1000, 1000 + samples))),
            'stacking': sum(pool.map(stacking, range(2000, 2000 + samples))),
        }
        rows = pool.map(closed_sector, range(3000, 3000 + samples))
        result['closed'] = {k: sum(r[k] for r in rows) for k in rows[0]}
        result['self_zero'] = sum(pool.map(self_zero, range(4000, 4000 + samples)))
        rows = pool.map(self_torsion, range(5000, 5000 + 4 * samples))
        result['self_torsion'] = {k: sum(r[k] for r in rows) for k in SECTORS}
    result['Z4fT'] = z4ft()
    failures = (result['closure'] + result['stacking'] + sum(result['closed'].values())
                + result['self_zero'] + sum(result['self_torsion'].values())
                + sum(v for r in result['Z4fT'].values() for v in r['failures'].values()))
    receipt = dict(status='PASS' if failures == 0 else 'FAIL', samples=samples,
                   torsion_samples=4 * samples, failures=result)
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results/formulas.json').write_text(json.dumps(receipt, indent=1) + '\n')
    print(json.dumps(receipt, indent=1))
    if failures:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
