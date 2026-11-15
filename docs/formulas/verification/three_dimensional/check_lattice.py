#!/usr/bin/env python3
"""Complete enumeration of the lattice parity counts against the 3+1D formulas.

F move   the parity change of (1234,0134,0123) -> (0124,0234) equals O_4(01234)
P move   the parity change of stacking two states on (0123) equals E_3(0123)

Each move has 24 independent bits, and all 2^24 inputs are checked:

  F: s1(0i) for i=1..4 (4 bits), omega2(0ij) (6), the integer coordinates of
     n1 modulo four at the vertices 1..4 (8), n2(0ij) (6);
  P: s1(0i) for i=1..3 (3), omega2(0ij) (3), the integer coordinates of both
     states modulo four (12), n2(0ij) and n2'(0ij) (6).

The remaining values follow from the lower equations.  For every input the
parity is counted twice, from the transition loops and from the inversions of
the ordered words, and compared with the formula.  Adding four layers to an
edge changes neither count: this is checked by adding 4 and 12 layers to
every edge of 4096 inputs.  With the formulas depending on n1 only through
[n1]_2 and [floor(n1/2)]_2, the enumeration covers every signed integer n1.
Finally the three worked F moves of the 3+1D stacking paper are evaluated.

Usage: check_lattice.py   (a few minutes on 32 cores)
"""
import json
from itertools import combinations
from multiprocessing import Pool
from pathlib import Path

import formulas as F
import lattice
from formulas import C

HERE = Path(__file__).resolve().parent
TOTAL = 1 << 24


def decode(mask, nv, states):
    """Background and states from the independent bits of mask."""
    bits = iter((mask >> j) & 1 for j in range(24))
    t = [0] + [next(bits) for _ in range(nv - 1)]
    s = {e: t[e[0]] ^ t[e[1]] for e in combinations(range(nv), 2)}
    omega = {(0, i, j): next(bits) for i, j in combinations(range(1, nv), 2)}
    for i, j, k in combinations(range(1, nv), 3):
        omega[i, j, k] = omega[0, i, j] ^ omega[0, i, k] ^ omega[0, j, k]
    out = []
    for _ in range(states):
        r = [0] + [next(bits) for _ in range(nv - 1)]
        r = [0] + [r[i] + 2 * next(bits) for i in range(1, nv)]
        x = [0]
        for i in range(1, nv):
            x.append(x[-1] + (r[i] - r[i - 1]) % 4)
        out.append(x)
    states_out = []
    for x in out:
        n1 = {(i, j): (-1) ** t[i] * (x[j] - x[i]) for i, j in s}
        states_out.append(n1)
    n2s = []
    for n1 in states_out:
        n2 = {(0, i, j): next(bits) for i, j in combinations(range(1, nv), 2)}
        for i, j, k in combinations(range(1, nv), 3):
            source = (omega[0, i, j] ^ (s[0, i] & s[i, j])) * (n1[j, k] % 2)
            n2[i, j, k] = (source + n2[0, j, k] + n2[0, i, k] + n2[0, i, j]) % 2
        n2s.append(n2)
    return s, omega, list(zip(states_out, n2s)), out, t


def cochain(values, degree, integer=False):
    return C(degree, values=dict(values), mod=None if integer else 2)


def f_count(mask):
    s, omega, [(n1, n2)], _, _ = decode(mask, 5, 1)
    loop, word = lattice.f_move(n1, n2, omega, s)
    O4 = F.O4(cochain(n1, 1, True), cochain(n2, 2), cochain(omega, 2), cochain(s, 1))
    return loop != O4((0, 1, 2, 3, 4)) % 2, loop != word


def p_count(mask):
    s, omega, [(n1, n2), (m1, m2)], _, _ = decode(mask, 4, 2)
    loop, word = lattice.p_move(n1, n2, m1, m2, omega, s)
    E3 = F.E3(cochain(n1, 1, True), cochain(n2, 2), cochain(m1, 1, True), cochain(m2, 2),
              cochain(s, 1))
    return loop != E3((0, 1, 2, 3)) % 2, loop != word


def run(task):
    move, start, stop = task
    count = f_count if move == 'F' else p_count
    formula = word = 0
    for mask in range(start, stop):
        a, b = count(mask)
        formula += a
        word += b
    return formula, word


def periodic(task):
    """Adding 4 or 12 layers to one edge leaves both counts unchanged."""
    move, mask = task
    nv, states = (5, 1) if move == 'F' else (4, 2)
    s, omega, pairs, xs, t = decode(mask, nv, states)
    base = (lattice.f_move(*pairs[0], omega, s) if move == 'F'
            else lattice.p_move(*pairs[0], *pairs[1], omega, s))
    bad = 0
    for g in range(states):
        for edge in range(nv - 1):
            for copies in (4, 12):
                shifted = []
                for h, (n1, n2) in enumerate(pairs):
                    x = [xi + (copies if h == g and i > edge else 0) for i, xi in enumerate(xs[h])]
                    shifted.append(({(i, j): (-1) ** t[i] * (x[j] - x[i]) for i, j in n1}, n2))
                new = (lattice.f_move(*shifted[0], omega, s) if move == 'F'
                       else lattice.p_move(*shifted[0], *shifted[1], omega, s))
                bad += new != (base[0], base[0]) or base[1] != base[0]
    return bad


def full(values, degree, nv=5):
    return {f: values.get(f, 0) for f in combinations(range(nv), degree + 1)}


EXAMPLES = {
    'open chain': dict(
        n1={(0, 3): 1, (1, 3): 1, (2, 3): 1, (3, 4): 1, (0, 4): 2, (1, 4): 2, (2, 4): 2},
        omega={(0, 1, 2): 1, (1, 2, 3): 1, (1, 2, 4): 1}, n2={(1, 2, 3): 1}, s={}, parity=0),
    'four modes': dict(
        n1={(0, 4): 2, (1, 4): 2, (2, 4): 2, (3, 4): 2},
        omega={(0, 1, 2): 1, (0, 2, 3): 1, (1, 2, 4): 1, (2, 3, 4): 1}, n2={}, s={}, parity=1),
    'anti-unitary': dict(
        n1={(0, 2): 1, (0, 3): 1, (2, 4): 1, (0, 4): 2, (1, 2): -1, (1, 3): -1, (3, 4): -1,
            (1, 4): -2},
        omega={(0, 1, 4): 1, (1, 2, 4): 1, (1, 3, 4): 1},
        n2={(0, 1, 2): 1, (0, 1, 3): 1, (0, 3, 4): 1, (2, 3, 4): 1},
        s={(0, 1): 1, (0, 3): 1, (0, 4): 1, (1, 2): 1, (2, 3): 1, (2, 4): 1}, parity=1),
}


def examples():
    out = {}
    for name, data in EXAMPLES.items():
        n1, omega, n2, s = (full(data['n1'], 1), full(data['omega'], 2),
                            full(data['n2'], 2), full(data['s'], 1))
        loop, word = lattice.f_move(n1, n2, omega, s)
        O4 = F.O4(cochain(n1, 1, True), cochain(n2, 2), cochain(omega, 2), cochain(s, 1))
        out[name] = dict(loops=loop, words=word, O4=O4((0, 1, 2, 3, 4)) % 2, paper=data['parity'])
    return out


def main():
    chunk = 1 << 14
    receipt = {}
    with Pool() as pool:
        for move in ('F', 'P'):
            rows = pool.map(run, [(move, a, a + chunk) for a in range(0, TOTAL, chunk)])
            receipt[move] = dict(inputs=TOTAL, formula_mismatches=sum(r[0] for r in rows),
                                 word_mismatches=sum(r[1] for r in rows))
            masks = [(i * 0x9e3779 + 0x42) % TOTAL for i in range(4096)]
            receipt[move]['four_layer_mismatches'] = sum(pool.map(periodic, [(move, m) for m in masks]))
    receipt['worked_examples'] = examples()
    ok = (all(receipt[m][k] == 0 for m in ('F', 'P')
              for k in ('formula_mismatches', 'word_mismatches', 'four_layer_mismatches'))
          and all(r['loops'] == r['words'] == r['O4'] == r['paper']
                  for r in receipt['worked_examples'].values()))
    receipt = dict(status='PASS' if ok else 'FAIL', **receipt)
    (HERE / 'results').mkdir(exist_ok=True)
    (HERE / 'results/lattice.json').write_text(json.dumps(receipt, indent=1) + '\n')
    print(json.dumps(receipt, indent=1))
    if not ok:
        raise SystemExit(1)


if __name__ == '__main__':
    main()
