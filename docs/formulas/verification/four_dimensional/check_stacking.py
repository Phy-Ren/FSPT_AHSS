#!/usr/bin/env python3
"""Checks of the displayed 4+1D stacking corrections, evaluated directly from the pages.

For random exact solutions of the lower equations (d_s n2 = 0, dn3 = O4, dn4 = O5,
with closed backgrounds, signed integer n2 and open n3):

  general   displayed E5 = stacking correction of the code (runtime product_4_bosonic
            with the transfer Z_5), on one five-simplex;
  cocycle   d_s E5 = O6[N] - O6[n] - O6[n'] on a six-simplex, with E5 the displayed
            formula on its seven five-faces and O6 the obstruction of the code
            (the displayed obstruction);
  self      displayed self-stacking correction = code correction for equal states;
  closed    at n2 = n2' = 0: (M3E) = code correction, and the Majorana contribution
            of the general law = (M7);
  diagonal  at n2 = 0 and equal states: the zero-p+ip self-stacking law = code correction
            = displayed self-stacking correction.

Usage: check_stacking.py [samples] [workers]   (the receipt goes to results/)
"""
import json
import random
import sys
import time
from fractions import Fraction
from multiprocessing import Pool
from pathlib import Path

import stacking as T
from stacking import C, cup, ds, faces

from fspt.full_formula.runtime import Backend

HERE = Path(__file__).resolve().parent
BACKEND = None
GENERAL = None
SELF = None



def fix(c, V):
    return C(c.deg, values={f: c(f) for f in faces(V, c.deg)}, mod=c.mod)


def restrict(c, f):
    return C(c.deg, values={g: c(tuple(f[i] for i in g)) for g in faces(len(f), c.deg)}, mod=c.mod)


def primitive(z, V):
    """Cone primitive on the full simplex: (h z)(f) = z((0,)+f) for 0 not in f."""
    return fix(C(z.deg - 1, fun=lambda f: 0 if 0 in f else z((0,) + tuple(f)), mod=z.mod), V)


def background(V, rng, kind):
    t = {(i,): (rng.randrange(2) if kind in ('s', 'both') else 0) for i in range(V)}
    s = fix(C(0, values=t).d(), V)
    e = {f: (rng.randrange(2) if kind in ('w', 'both') else 0) for f in faces(V, 1)}
    w = fix(C(1, values=e).d(), V)
    w.closed = s.closed = True
    return w, s


def rnd(q, V, rng):
    return C(q, values={f: rng.randrange(2) for f in faces(V, q)})


def tower(V, w, s, rng, zero_n2=False):
    if zero_n2:
        n = C(2, values={f: 0 for f in faces(V, 2)}, mod=None)
    else:
        r = C(1, values={f: rng.randrange(16) - 8 for f in faces(V, 1)}, mod=None)
        n = fix(ds(r, s), V)
    u = fix(primitive(fix(T.O4(n, w, s), V), V) + rnd(2, V, rng).d(), V)
    c = fix(primitive(fix(T.O5(n, u, w, s), V), V) + rnd(3, V, rng).d(), V)
    return n, u, c


def arr(c, V):
    out = [0] * (1 << V)
    for f in faces(V, c.deg):
        out[sum(1 << j for j in f)] = int(c(f))
    return tuple(out)


def code_E5(n, u, c, m, v, cp, w, s, V=6):
    a = lambda x: arr(x, V)
    A, Ap = u + cup(s, T.carry(n)), v + cup(s, T.carry(m))   # runtime API Majorana input
    return BACKEND.product(4, 'bosonic', dict(n=a(n), a=a(A), c=a(c)), dict(n=a(m), a=a(Ap), c=a(cp)),
                           dict(w=a(w), s=a(s)))


def code_O6(n, u, c, w, s, V):
    a = lambda x: arr(x, V)
    return BACKEND.source(4, 'bosonic', dict(n=a(n), a=a(u + cup(s, T.carry(n))), c=a(c), w=a(w), s=a(s)))


def init(tables):
    """Each worker loads only the coefficient tables of its group of checks."""
    global BACKEND, GENERAL, SELF
    BACKEND = Backend()
    if 'general' in tables:
        GENERAL = T.General()
    if 'self' in tables:
        SELF = T.Self()


KINDS = ('zero', 'w', 's', 'both')


def run(job):
    test, seed = job
    rng = random.Random(seed)
    kind = KINDS[seed % 4]
    if test in ('general', 'self', 'closed', 'diagonal'):
        V = 6
        w, s = background(V, rng, kind)
        zero = test in ('closed', 'diagonal') or seed % 5 == 4
        n, u, c = tower(V, w, s, rng, zero)
        if test in ('self', 'diagonal'):
            m, v, cp = n, u, c
        else:
            m, v, cp = tower(V, w, s, rng, zero)
        code = code_E5(n, u, c, m, v, cp, w, s)
        if test == 'general':
            return test, seed, kind, zero, GENERAL.E5(n, u, c, m, v, cp, w, s) == code
        if test == 'self':
            return test, seed, kind, zero, SELF.E5(n, u, c, w, s) == code
        if test == 'closed':
            gamma = GENERAL.parts(n, u, c, m, v, cp, w, s)
            m7 = (T.closed_E5(u, c, v, cp, w, s) - gamma['c'] - gamma['c_gamma']) % 1
            ok = T.closed_E5(u, c, v, cp, w, s) == code and gamma['gamma'] == m7 and gamma['c_psi'] == 0 \
                and gamma['gamma_psi'] == 0 and gamma['psi'] == 0
            return test, seed, kind, zero, ok
        diag = T.diagonal_E5(u, c, w, s)
        return test, seed, kind, zero, diag == code and (SELF is None or SELF.E5(n, u, c, w, s) == code)
    # cocycle condition on a six-simplex
    V = 7
    w, s = background(V, rng, kind)
    zero = seed % 5 == 4
    n, u, c = tower(V, w, s, rng, zero)
    m, v, cp = tower(V, w, s, rng, zero)
    a, b = n.reduce(2), m.reduce(2)
    NN, U = fix(n + m, V), fix(u + v + cup(a, b, 1), V)
    N4 = fix(c + cp + sum(T.E4_parts(n, u, m, v, w, s)[1:], T.E4_parts(n, u, m, v, w, s)[0]), V)
    values = []
    for i in range(V):
        f = tuple(j for j in range(V) if j != i)
        r = [restrict(x, f) for x in (n, u, c, m, v, cp, w, s)]
        r[6].closed = r[7].closed = True
        values.append(GENERAL.E5(*r))
    dE = sum((-1) ** i * x for i, x in enumerate(values))
    if s((0, 1)):
        dE -= 2 * values[0]
    dO = code_O6(NN, U, N4, w, s, V) - code_O6(n, u, c, w, s, V) - code_O6(m, v, cp, w, s, V)
    return test, seed, kind, zero, (dE - dO) % 1 == 0


def main():
    samples = int(sys.argv[1]) if len(sys.argv) > 1 else 24
    workers = int(sys.argv[2]) if len(sys.argv) > 2 else 6
    seeds = {'general': 0, 'cocycle': 1000, 'self': 2000, 'closed': 3000, 'diagonal': 4000}
    start = time.time()
    results = []
    for tables, tests in (('general', ('general', 'cocycle', 'closed')), ('self', ('self', 'diagonal'))):
        jobs = [(t, seeds[t] + j) for t in tests for j in range(samples)]
        with Pool(workers, initializer=init, initargs=(tables,)) as pool:
            results += pool.map(run, jobs, chunksize=1)
    report = {}
    for test, seed, kind, zero, ok in results:
        r = report.setdefault(test, {'samples': 0, 'pass': 0, 'zero_n2': 0, 'nonzero_n2': 0, 'failures': []})
        r['samples'] += 1
        r['pass'] += bool(ok)
        r['zero_n2' if zero else 'nonzero_n2'] += 1
        if not ok:
            r['failures'].append(seed)
    status = 'PASS' if all(r['pass'] == r['samples'] for r in report.values()) else 'FAIL'
    out = {'status': status, 'checks': report, 'seconds': round(time.time() - start, 1),
           'domain': 'Random exact lower towers: signed integer n2 with d_s n2 = 0, dn3 = O4, dn4 = O5, '
                     'closed backgrounds in the four sectors (zero, w2 only, s1 only, both).',
           'scope': __doc__.strip().split('\n\n')[1]}
    (HERE / 'results/STACKING_CHECK.json').write_text(json.dumps(out, indent=2) + '\n')
    print(json.dumps(out, indent=2))
    if status != 'PASS':
        raise SystemExit(1)


if __name__ == '__main__':
    main()
