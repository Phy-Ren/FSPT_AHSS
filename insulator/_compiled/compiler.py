"""Compile current U1 cochains to a fixed-denominator integer DAG.

The integer builder/VM design is adapted from FSPT_AHSS main0864495,
fspt/formulas_pip_compile.py and fspt/full_formula/native.cpp. Every traced
formula here belongs to this repository's insulator engine. Compilation is
an offline operation: the temporary symbolic cup method is never installed
by the formula worker.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
import math
from pathlib import Path

from .._engine import simplex as S, transgression as T, calibrated as K


class Builder:
    def __init__(self):
        self.nodes = []
        self.indices = {}

    def make(self, op, *args):
        key = (op,) + args
        if key not in self.indices:
            self.indices[key] = len(self.nodes)
            self.nodes.append(key)
        return self.indices[key]

    def const(self, value):
        return self.make('const', int(value))

    def value(self, node):
        row = self.nodes[node]
        return row[1] if row[0] == 'const' else None

    def binary(self, op, a, b):
        av, bv = self.value(a), self.value(b)
        if av is not None and bv is not None:
            return self.const(av + bv if op == 'add' else av * bv)
        if op == 'add':
            if av == 0:
                return b
            if bv == 0:
                return a
        else:
            if av == 0 or bv == 0:
                return self.const(0)
            if av == 1:
                return b
            if bv == 1:
                return a
        # Scalar arithmetic is commutative. Ordered cochain faces have already
        # been selected by trace_cup; their order is never changed here.
        return self.make(op, *sorted((a, b)))

    def unary(self, op, a, divisor):
        value = self.value(a)
        if value is not None:
            if op == 'mod':
                return self.const(value % divisor)
            if op == 'floor':
                return self.const(value // divisor)
            if op == 'div':
                if value % divisor:
                    raise ArithmeticError('Nonexact constant division')
                return self.const(value // divisor)
        if divisor == 1 and op in ('div', 'floor'):
            return a
        if divisor == 1 and op == 'mod':
            return self.const(0)
        if op == 'mod' and self.nodes[a][0] == 'mod' and self.nodes[a][2] == divisor:
            return a
        return self.make(op, a, divisor)

    def scalar(self, value):
        if isinstance(value, Rational):
            if value.builder is not self:
                raise ValueError('Cannot combine two symbolic builders')
            return value
        value = Fraction(value)
        return Rational(self, self.const(value.numerator), value.denominator)

    def field(self, name, face, denominator=1):
        return Rational(self, self.make('field', name, tuple(face)), denominator)


class Rational:
    """An integer expression divided by one fixed positive denominator."""
    __slots__ = ('builder', 'node', 'denominator')

    def __init__(self, builder, node, denominator=1):
        value = builder.value(node)
        if value is not None:
            value = Fraction(value, denominator)
            node, denominator = builder.const(value.numerator), value.denominator
        self.builder, self.node, self.denominator = builder, node, denominator

    def __add__(self, other):
        other = self.builder.scalar(other)
        denominator = self.denominator // math.gcd(self.denominator, other.denominator) * other.denominator
        a = self.builder.binary('mul', self.node, self.builder.const(denominator // self.denominator))
        b = self.builder.binary('mul', other.node, self.builder.const(denominator // other.denominator))
        return Rational(self.builder, self.builder.binary('add', a, b), denominator)

    __radd__ = __add__

    def __mul__(self, other):
        other = self.builder.scalar(other)
        return Rational(self.builder, self.builder.binary('mul', self.node, other.node),
                        self.denominator * other.denominator)

    __rmul__ = __mul__

    def __neg__(self):
        return self * -1

    def __sub__(self, other):
        return self + -self.builder.scalar(other)

    def __rsub__(self, other):
        return self.builder.scalar(other) + -self

    def __mod__(self, modulus):
        if not isinstance(modulus, int) or modulus <= 0:
            raise ValueError('Symbolic modulus must be a positive constant integer')
        return Rational(self.builder, self.builder.unary('mod', self.node, modulus * self.denominator),
                        self.denominator)

    def __floordiv__(self, divisor):
        if not isinstance(divisor, int) or divisor <= 0:
            raise ValueError('Symbolic floor divisor must be a positive constant integer')
        return Rational(self.builder, self.builder.unary('floor', self.node, divisor * self.denominator))

    def __xor__(self, other):
        return (self + other) % 2

    __rxor__ = __xor__

    def __rpow__(self, base):
        if base != -1 or self.denominator != 1:
            raise ValueError('Only integer sign exponents are supported')
        return 1 - 2 * (self % 2)

    def __bool__(self):
        raise TypeError('A symbolic value cannot control a branch')


def _structurally_zero(value):
    if isinstance(value, Rational):
        return value.builder.value(value.node) == 0
    return value == 0


def trace_cup(self, other, i=0, binary=False):
    """The exact reference cup plan, pruning only structural constant zeros."""
    output = {}
    for face, cuts in S._cup_plan(self.N, self.p, other.p, i):
        value = 0
        for left, right, sign in cuts:
            a, b = self(left), other(right)
            if _structurally_zero(a) or _structurally_zero(b):
                continue
            coefficient = 1 if binary else sign * (-1) ** (
                self.tw[face[0]] + self.tw[left[0]] + other.tw[face[0]] + other.tw[right[0]])
            value += coefficient * a * b
        output[face] = value % 2 if binary else value
    return S.C(self.N, self.p + other.p - i, output, [a ^ b for a, b in zip(self.tw, other.tw)])


def source_hashes():
    root = Path(__file__).resolve().parents[1]
    names = ('simplex.py', 'cochains.py', 'transgression.py', 'prism.py', 'calibrated.py')
    return {'_engine/' + name: hashlib.sha256((root / '_engine' / name).read_bytes()).hexdigest()
            for name in names}


def compile_program(operation='source'):
    if operation not in ('source', 'product'):
        raise ValueError('Only source and product have branch-safe dispatch')
    builder = Builder()
    N = 5 if operation == 'source' else 4
    s = [builder.field('s', (j,)) for j in range(N + 1)]
    rho = [builder.field('rho', (j,)) for j in range(N + 1)]
    twist = [a ^ b for a, b in zip(s, rho)]

    def field(name, degree, sign, denominator=1):
        return S.C(N, degree, {face: builder.field(name, face, denominator)
                              for face in combinations(range(N + 1), degree + 1)}, sign)

    omega, sheet, charge = field('omega', 2, twist, 2), field('sheet', 1, s), field('charge', 3, rho)
    ss, rr = S.char(N, s).ret(s), S.char(N, rho).ret(rho)
    original_cup = S.C.cup
    S.C.cup = trace_cup
    try:
        if operation == 'source':
            output = T.O3canonical(omega, sheet, charge, ss, rr) + K.calibration(omega, sheet, ss, rr)
        else:
            output = T.E4canonical(omega, sheet, charge, field('sheet_prime', 1, s),
                                   field('charge_prime', 3, rho), ss, rr)
        result = builder.scalar(output(tuple(range(N + 1))) % 1)
    finally:
        S.C.cup = original_cup
    pending, active = [result.node], set()
    while pending:
        node = pending.pop()
        if node in active:
            continue
        active.add(node)
        row = builder.nodes[node]
        if row[0] in ('add', 'mul'):
            pending.extend(row[1:3])
        elif row[0] in ('mod', 'floor', 'div'):
            pending.append(row[1])
    remap = {old: new for new, old in enumerate(sorted(active))}
    nodes = []
    for node in sorted(active):
        row = list(builder.nodes[node])
        if row[0] in ('add', 'mul'):
            row[1:3] = [remap[x] for x in row[1:3]]
        elif row[0] in ('mod', 'floor', 'div'):
            row[1] = remap[row[1]]
        nodes.append(row)
    return {'op': operation, 'dimension': 3, 'simplex_dimension': N, 'program': nodes,
            'output': remap[result.node], 'denominator': result.denominator,
            'full_uncompacted_nodes': len(builder.nodes), 'source_sha256': source_hashes(),
            'traced': 'Current U1 generic transgression and calibrated source; no SC formula data'}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('operation', choices=('source', 'product'))
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()
    args.out.write_text(json.dumps(compile_program(args.operation), sort_keys=True, separators=(',', ':')) + '\n')


if __name__ == '__main__':
    main()
