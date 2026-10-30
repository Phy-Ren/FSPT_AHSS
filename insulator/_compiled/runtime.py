"""Guarded exact U1 scalar DAGs with optional checked native execution.

Only the generic nonzero-sheet source/product branches in spatial dimension
three are compiled. Decoding and public validation occur before this module.
Native overflow uses arbitrary-precision Python integer evaluation of the same
DAG. Inputs outside the fixed-denominator domain use the original cochains.
"""
from fractions import Fraction
from functools import lru_cache
import ctypes
import hashlib
import json
import os
from pathlib import Path

from .._engine.simplex import C

HERE = Path(__file__).resolve().parent


class Program:
    def __init__(self, data, library=None):
        self.data = data
        self.nodes = data['program']
        self.slots = []
        slot_ids = {}
        flat = []
        codes = dict(const=0, field=1, add=2, mul=3, mod=4, div=5, floor=6)
        for index, row in enumerate(self.nodes):
            op = row[0]
            if op not in codes:
                raise ValueError('Unknown DAG opcode')
            if op in ('add', 'mul') and any(not 0 <= x < index for x in row[1:]):
                raise ValueError('DAG operands must precede their consumers')
            if op in ('mod', 'div', 'floor') and (not 0 <= row[1] < index or row[2] <= 0):
                raise ValueError('Invalid DAG unary operand or divisor')
            if op == 'field':
                key = (row[1], tuple(row[2]))
                if key not in slot_ids:
                    slot_ids[key] = len(self.slots)
                    self.slots.append(key)
                flat.extend((1, slot_ids[key], 0))
            else:
                flat.extend((codes[op], row[1], row[2] if len(row) > 2 else 0))
        if not 0 <= data['output'] < len(self.nodes) or data['denominator'] <= 0:
            raise ValueError('Invalid DAG output')
        self.native = None
        self.native_hits = self.integer_fallbacks = 0
        if library and all(-(1 << 63) <= x < (1 << 63) for x in flat):
            self.library = ctypes.CDLL(str(library))
            self.native = self.library.u1_formula_eval
            pointer = ctypes.POINTER(ctypes.c_int64)
            self.native.argtypes = [pointer, ctypes.c_int64, pointer, ctypes.c_int64,
                                    pointer, ctypes.c_int64, pointer, pointer]
            self.native.restype = ctypes.c_int
            self.flat = (ctypes.c_int64 * len(flat))(*flat)
            self.outputs = (ctypes.c_int64 * 1)(data['output'])

    def inputs(self, fields):
        values = []
        for name, face in self.slots:
            value = fields[name][face[0]] if name in ('s', 'r') else fields[name](face)
            if name == 'omega':
                value *= 2
            if isinstance(value, Fraction):
                if value.denominator != 1:
                    raise ValueError('Noninteger DAG input')
                value = value.numerator
            if not isinstance(value, int):
                raise TypeError('DAG inputs must be exact integers')
            values.append(value)
        return values

    def evaluate(self, fields):
        inputs = self.inputs(fields)
        if self.native is not None and all(-(1 << 63) <= x < (1 << 63) for x in inputs):
            packed = (ctypes.c_int64 * len(inputs))(*inputs)
            result = (ctypes.c_int64 * 1)()
            bad = ctypes.c_int64(-1)
            status = self.native(self.flat, len(self.nodes), packed, len(inputs),
                                 self.outputs, 1, result, ctypes.byref(bad))
            if status == 0:
                self.native_hits += 1
                return Fraction(result[0], self.data['denominator'])
            if status != -2:
                raise ArithmeticError('Native DAG status {} at node {}'.format(status, bad.value))
        self.integer_fallbacks += 1
        lookup = dict(zip(self.slots, inputs))
        values = []
        for row in self.nodes:
            op = row[0]
            if op == 'const':
                value = row[1]
            elif op == 'field':
                value = lookup[(row[1], tuple(row[2]))]
            elif op == 'add':
                value = values[row[1]] + values[row[2]]
            elif op == 'mul':
                value = values[row[1]] * values[row[2]]
            elif op == 'mod':
                value = values[row[1]] % row[2]
            elif op == 'floor':
                value = values[row[1]] // row[2]
            elif op == 'div':
                value, remainder = divmod(values[row[1]], row[2])
                if remainder:
                    raise ArithmeticError('Nonexact DAG division')
            values.append(value)
        return Fraction(values[self.data['output']], self.data['denominator'])


def _matches_sources(data):
    expected = data.get('source_sha256', {})
    if not expected:
        return False
    return all(hashlib.sha256((HERE.parent / name).read_bytes()).hexdigest() == value
               for name, value in expected.items())


@lru_cache(maxsize=8)
def _program(operation, mode, library):
    data = json.loads((HERE / (operation + '3.json')).read_text())
    if not _matches_sources(data):
        return None
    native = None if mode == 'python' else library
    return Program(data, native)


def _integer_field(cochain, N, degree, sign):
    return (isinstance(cochain, C) and cochain.N == N and cochain.p == degree
            and cochain.tw == tuple(sign)
            and all(len(f) == degree + 1 and tuple(sorted(set(f))) == tuple(f)
                    and all(isinstance(i, int) and 0 <= i <= N for i in f) for f in cochain.v)
            and all(isinstance(v, int) or isinstance(v, Fraction) and v.denominator == 1
                    for v in cochain.v.values()))


def phase3(operation, symmetry, sheet, charge, sheet_prime=None, charge_prime=None):
    """Return the exact terminal phase, or None to retain reference evaluation."""
    mode = os.environ.get('U1_DAG_MODE', 'auto')
    if mode == 'reference':
        return None
    if mode not in ('auto', 'python'):
        raise ValueError('U1_DAG_MODE must be auto, python, or reference')
    N = 5 if operation == 'source' else 4
    s, r, omega = symmetry.s1.tw, symmetry.r1.tw, symmetry.omega2_real
    pairs = [(sheet, 1, s), (charge, 3, r)]
    if operation == 'product':
        pairs += [(sheet_prime, 1, s), (charge_prime, 3, r)]
    elif operation != 'source':
        return None
    if omega.N != N or any(not _integer_field(c, N, p, t) for c, p, t in pairs):
        return None
    # Preserve every value-dependent zero-sheet specialization in calibrated.py.
    if not any(sheet.v.values()) and (operation == 'source' or not any(sheet_prime.v.values())):
        return None
    if any(not isinstance(v, (int, Fraction)) or (2 * Fraction(v)).denominator != 1
           for v in omega.v.values()):
        return None
    library = os.environ.get('U1_DAG_LIBRARY', str(HERE / 'u1_dag_vm.so'))
    if not Path(library).is_file():
        library = None
    program = _program(operation, mode, library)
    if program is None:
        return None
    fields = dict(s=s, r=r, omega=omega, sheet=sheet, charge=charge,
                  sheet_prime=sheet_prime, charge_prime=charge_prime)
    value = program.evaluate(fields)
    return C(N, N, {tuple(range(N + 1)): value}, s)
