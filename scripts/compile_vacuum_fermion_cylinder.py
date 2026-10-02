#!/usr/bin/env python3
"""Compile the literal complete 4D vacuum complex-fermion gauge cylinder.

The binary field is C=delta(eta gamma). The phase is the signed normalized
prism of the matched complete source. No looping or descent identity is used.
"""
import argparse
from functools import lru_cache
import hashlib
import json
from pathlib import Path
import sys
import time
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fspt.formulas_pip_compile import Builder
from fspt.full_formula.compiler import atomic_write_bytes, compact_program


def degenerate(vertices):
    return any(a == b for a, b in zip(vertices, vertices[1:]))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--data-dir', type=Path,
                        default=Path(__file__).resolve().parents[1]/'fspt/data/full_formula')
    args = parser.parse_args()
    started = time.monotonic()
    builder = Builder()
    zero = builder.scalar(0)
    source_path = args.data_dir/'high6.json'
    source_bytes = source_path.read_bytes()
    program = json.loads(source_bytes)

    @lru_cache(None)
    def pull(name, vertices):
        base = tuple(v[0] for v in vertices)
        return zero if degenerate(base) else builder.make('field', name, base)

    @lru_cache(None)
    def fermion(vertices):
        if degenerate(vertices):
            return zero
        value = zero
        for i in range(len(vertices)):
            face = vertices[:i] + vertices[i+1:]
            value += (-1)**i * face[0][1] * pull('gamma', face)
        return value % 2

    def field(name, vertices):
        if name in ('n', 'a', 'y'):
            return zero
        if name in ('s', 'w'):
            return pull(name, vertices)
        if name == 'c':
            return fermion(vertices)
        raise ValueError(name)

    @lru_cache(None)
    def source(vertices):
        if degenerate(vertices):
            return zero
        values = []
        for op, *x in program['program']:
            if op == 'const': value = builder.scalar(x[0])
            elif op == 'field': value = field(x[0], tuple(vertices[j] for j in x[1]))
            elif op == 'add': value = values[x[0]] + values[x[1]]
            elif op == 'mul': value = values[x[0]] * values[x[1]]
            elif op == 'mod': value = values[x[0]] % x[1]
            elif op == 'div': value = builder.divide(values[x[0]], x[1])
            elif op == 'floor': value = builder.floor(values[x[0]], x[1])
            elif op == 'bit': value = builder.bit(values[x[0]], x[1])
            else: raise ValueError(op)
            values.append(value)
        high, cubic = (values[i] for i in program['outputs'])
        return (3*high + 4*cubic) % 48

    vertices = tuple((i, 1) for i in range(6))
    value = zero
    for i in range(len(vertices)):
        simplex = tuple((v[0], 0) for v in vertices[:i+1]) + vertices[i:]
        value += (-1)**i * source(simplex)
    name = 'vacuum_cf4_bosonic'
    data = compact_program(builder, [value % 48], dict(
        name=name, top_degree=5, denominator=48,
        coordinate='publication-20260930-native',
        operation='literal-vacuum-complex-fermion-gauge-cylinder',
        inputs=dict(gamma=3, w=2, s=1),
        assumptions='vacuum input; lambda=beta=0; arbitrary gamma3',
        component_sha256={'high6': hashlib.sha256(source_bytes).hexdigest()}))
    raw = (json.dumps(data, separators=(',', ':')) + '\n').encode()
    atomic_write_bytes(args.data_dir/(name+'.json'), raw)
    print(json.dumps(dict(status='compiled', seconds=time.monotonic()-started,
        name=name, raw_nodes=len(builder.nodes), nodes=len(data['program']),
        bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())), flush=True)


if __name__ == '__main__':
    main()
