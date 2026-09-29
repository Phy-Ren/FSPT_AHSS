#!/usr/bin/env python3
"""Compile the supplied fixed O5/O6 cochains, without group or result input.

The symbolic replacement of the polynomial evaluator expands its bit tests as
products. Signed integer division and transport retain the source semantics.
The n=0 graph omits the identically zero pure integer block, not lower terms.
"""
import argparse
import hashlib
import importlib
import json
from itertools import combinations
from pathlib import Path
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas_pip_compile import Builder
from compile_pip_o5_straight import compile_gap


def compile_phase(source, p, integer_zero=False):
    # The source represents a finite sum as nested cochain additions.
    sys.setrecursionlimit(20000)
    sys.path.insert(0, str(source))
    cc = importlib.import_module('cochains')
    tables = importlib.import_module('polynomial_tables')
    explicit = importlib.import_module('explicit_pip')
    B = Builder()

    def div(a, k):
        if a.mod is not None:
            raise ValueError('Integer quotient required')
        if a.known_zero:
            return cc.C(a.deg, mod=None)
        out = cc.C(a.deg, fun=lambda f: B.divide(a(f), k), mod=None)
        out.closed = a.closed
        return out

    cc.C.div = div

    def total_cochain(n, w, s, filename, degree, **kwargs):
        data = json.loads((source / filename).read_text())

        def value(face):
            ans = B.scalar(0)
            for block in data['blocks']:
                i, j, k = block['i'], block['j'], block['k']
                assert i + j + k == degree
                prefix = B.scalar(1)
                for t in range(1, i + 1):
                    prefix = prefix * s((face[t - 1], face[t]))
                middle, last = face[i:i + j + 1], face[i + j:]

                def M(f):
                    sign = 1 if face[0] == f[0] else 1 - 2 * s(tuple(sorted((face[0], f[0]))))
                    return sign * n(f)

                if p == 1:
                    ns = [M((middle[t - 1], middle[t])) for t in range(1, j + 1)]
                else:
                    ns = [M((middle[u - 1], middle[u], middle[v])) -
                          M((middle[u - 1], middle[u], middle[v - 1]))
                          for u, v in combinations(range(1, j + 1), 2)]
                ws = [w((last[u - 1], last[u], last[v])) ^
                      w((last[u - 1], last[u], last[v - 1]))
                      for u, v in combinations(range(1, k + 1), 2)]
                for nc, wc in block['terms']:
                    term, nc = prefix, int(nc)
                    for e, m in enumerate(ns):
                        mask = (nc >> (4 * e)) & 15
                        for bit in range(4):
                            if mask & (1 << bit):
                                term = term * B.bit(m, bit)
                    for e, m in enumerate(ws):
                        if wc & (1 << e):
                            term = term * m
                    ans = ans + term
            return ans % 2
        return cc.C(degree, fun=value)

    tables.total_cochain = total_cochain

    def field(name, degree, mod=2):
        return cc.C(degree, fun=lambda f: B.make('field', name, tuple(f)), mod=mod)

    n = cc.C(p, mod=None) if integer_zero else field('n', p, None)
    b, c, w, s = field('b', p + 1), field('c', p + 2), field('w', 2), field('s', 1)
    w.closed = s.closed = True
    if integer_zero:
        terms = explicit.full_terms16(n, b, c, w, s, binary_y=cc.C(p + 4))
        O = explicit.sum_terms(terms, p + 4)
    else:
        O = explicit.O5(n, b, c, w, s) if p == 1 else explicit.O6(n, b, c, w, s)
    output = O(tuple(range(p + 5))) % 16
    active, pending = set(), [output.index]
    while pending:
        i = pending.pop()
        if i in active:
            continue
        active.add(i)
        node = B.nodes[i]
        if node[0] in ('add', 'mul'):
            pending.extend(node[1:3])
        elif node[0] in ('mod', 'div', 'bit', 'floor'):
            pending.append(node[1])
    indices = {old: new for new, old in enumerate(sorted(active))}
    program = []
    for old in sorted(active):
        node = list(B.nodes[old])
        if node[0] in ('add', 'mul'):
            node[1], node[2] = indices[node[1]], indices[node[2]]
        elif node[0] in ('mod', 'div', 'bit', 'floor'):
            node[1] = indices[node[1]]
        program.append(node)
    source_hashes = {f.name: hashlib.sha256(f.read_bytes()).hexdigest()
                     for f in source.iterdir() if f.suffix in ('.py', '.json')}
    return dict(formula='O' + str(p + 4), p=p, integer_zero=integer_zero,
                denominator=16, omega_zero=False, program=program,
                output=indices[output.index], source_hashes=source_hashes)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--source', type=Path, required=True)
    ap.add_argument('--p', type=int, choices=(1, 2), required=True)
    ap.add_argument('--integer-zero', action='store_true')
    ap.add_argument('--out', type=Path, required=True)
    args = ap.parse_args()
    started = time.time()
    data = compile_phase(args.source, args.p, args.integer_zero)
    raw = (json.dumps(data, separators=(',', ':')) + '\n').encode()
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.with_suffix('.json').write_bytes(raw)
    name = 'AFSD4PhaseP{}{}'.format(args.p, 'Zero' if args.integer_zero else 'Full')
    gap = compile_gap(data, hashlib.sha256(raw).hexdigest()).replace('AFSPipO5General', name)
    gap = gap.replace('scripts/compile_pip_o5_straight.py', 'scripts/compile_dimension4_phase.py')
    args.out.with_suffix('.g').write_text(gap)
    print(json.dumps(dict(operations=len(data['program']), seconds=time.time() - started,
                          sha256=hashlib.sha256(raw).hexdigest(), function=name + 'Program')))


if __name__ == '__main__':
    main()
