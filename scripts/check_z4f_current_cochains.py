"""Check the current four-dimensional Z4^f representatives on the full C2 bar complex.

This is a finite cochain calculation, not a classification rerun.  All 64
inhomogeneous six-tuples, including tuples containing the identity, are tested.
The optional C++ engine already supplied with the formulas accelerates only
the fixed y6 polynomial.  Its shared library is built in a temporary directory.
"""
from __future__ import annotations

import argparse
import ast
import ctypes as ct
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import re
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / 'formulas/publication_source/reference/d4_input/code'
sys.path.insert(0, str(CODE))
from cochains import C, cup, op, sq, ds, parity, pure_parity, mc_phase4, zeta1, zeta2
from compact import beta_open, kappa
from explicit_pip import pure_terms16
from polynomial_tables import total_cochain
from ez_homotopy import ez_homotopy


def phase_transport_functions():
    """Reuse the exact public transport verifier; do not define another R5."""
    source = ROOT / 'scripts/verify_majorana_phase_transport.py'
    tree = ast.parse(source.read_text())
    names = {'H5', 'R0', 'R', 'Gamma'}
    functions = [node for node in tree.body
                 if isinstance(node, ast.FunctionDef) and node.name in names]
    assert {node.name for node in functions} == names
    namespace = dict(C=C, cup=cup, op=op, beta_open=beta_open)
    namespace['words'] = json.loads((ROOT /
        'formulas/publication_source/stages/data/mc3_zero_dictionary.json').read_text())['words']
    text = (ROOT / 'docs/formulas/source/pages/FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md').read_text()
    pure = []
    for block in text.split('## Coefficient block ')[1:]:
        args = re.search(r'```math\n\((.*?)\)\.\n```', block, re.S).group(1).split(',')
        if r'd\check n_3' not in args:
            words = re.search(r'```text\n(.*?)\n```', block, re.S).group(1).split()
            pure.extend((word, args) for word in words)
    assert len(pure) == 85
    namespace['pure'] = pure
    exec(compile(ast.Module(body=functions, type_ignores=[]), str(source), 'exec'), namespace)
    return namespace['R'], namespace['Gamma']


class ResidualEngine:
    """Standard-library interface to the unchanged supplied integer engine."""
    def __init__(self, library):
        self.lib = ct.CDLL(str(library))
        i64 = ct.POINTER(ct.c_int64)
        i32 = ct.POINTER(ct.c_int32)
        self.lib.make_engine.argtypes = [ct.c_char_p, ct.c_int, i64, i64, i64]
        self.lib.make_engine.restype = ct.c_void_p
        self.lib.engine_sum.argtypes = [ct.c_void_p, i32, ct.c_int]
        self.lib.engine_sum.restype = ct.c_int
        self.lib.engine_error.restype = ct.c_char_p
        self.lib.delete_engine.argtypes = [ct.c_void_p]
        self.chain = ez_homotopy(6)
        flat = [((a * 7) + b) * 7 + c
                for simplex in self.chain for a, b, c in simplex]
        self.chain_array = (ct.c_int32 * len(flat))(*flat)

    def y6(self, n, w, s):
        nn = (ct.c_int64 * (7 ** 3))()
        ww = (ct.c_int64 * (7 ** 3))()
        ss = (ct.c_int64 * (7 ** 2))()
        for a, b, c in combinations(range(7), 3):
            index = (a * 7 + b) * 7 + c
            nn[index], ww[index] = n((a, b, c)) % 16, w((a, b, c))
        for a, b in combinations(range(7), 2):
            ss[a * 7 + b] = s((a, b))
        pointer = self.lib.make_engine(
            str(CODE / 'word_residual_program.txt').encode(), 7, nn, ww, ss)
        if not pointer:
            raise RuntimeError(self.lib.engine_error().decode())
        try:
            grid = self.lib.engine_sum(pointer, self.chain_array, len(self.chain))
            if grid < 0:
                raise RuntimeError(self.lib.engine_error().decode())
        finally:
            self.lib.delete_engine(pointer)
        aw = total_cochain(n, w, s, 'Y6_word_total.json', 6)(tuple(range(7)))
        return grid ^ aw, grid, aw


def group_fields(edges):
    vertices = [0]
    for edge in edges:
        vertices.append(vertices[-1] ^ edge)

    def m(degree, modulus=2):
        return C(degree, fun=lambda face: int(all(
            vertices[a] != vertices[b] for a, b in zip(face, face[1:]))), mod=modulus)
    return m


def frac(value):
    value = Fraction(value) % 1
    return f'{value.numerator}/{value.denominator}'


def check(library):
    reader = json.loads((ROOT / 'formulas/SOURCE_COEFFICIENTS.json').read_text())
    coefficients = json.loads((CODE / 'Y6_word_total.json').read_text())
    assert reader['blocks'] == coefficients['blocks']
    R5, previous_gamma = phase_transport_functions()
    relative_rows = json.loads((ROOT /
        'docs/formulas/data/four_dimensional_majorana_relative_words.json').read_text())['terms']
    # Here d(m1^3)=0 and s1=0. Every omitted multilinear word has a zero input.
    relative_closed_rows = [row for row in relative_rows
                            if 'A' not in row['inputs'] and 's' not in row['inputs']]
    engine = ResidualEngine(library)
    top = tuple(range(7))
    configurations = [
        ('p_ip', 1, 0, 0, Fraction(25, 96), Fraction(25, 96)),
        ('Majorana', 0, 1, 0, Fraction(3, 8), Fraction(1, 8)),
        ('complex_fermion', 0, 0, 1, Fraction(1, 4), Fraction(1, 4)),
        ('bosonic', 0, 0, 0, Fraction(1, 2), Fraction(1, 2)),
    ]
    records = {name: {'old_phase_coefficient': frac(old),
                     'current_phase_coefficient': frac(new), 'values': []}
               for name, _, _, _, old, new in configurations}
    y_values = []
    for edges in product((0, 1), repeat=6):
        m = group_fields(edges)
        w, s = m(2), C(1)
        relative_fields = {'u': m(3), 'w': w}
        relative = sum(op(row['word'], *(relative_fields[x] for x in row['inputs']))(top)
                       for row in relative_closed_rows) % 2
        assert relative == 0
        y_value, grid, aw = engine.y6(m(2, None), w, s)
        assert y_value == int(all(edges))
        y_values.append({'tuple': list(edges), 'grid': grid, 'AW': aw, 'y6': y_value})
        for name, has_n, has_u, has_c, old_phase, new_phase in configurations:
            n = m(2, None) if has_n else C(2, mod=None)
            u = m(3) if has_u else C(3)
            c = m(4) if has_c else C(4)
            a = n.reduce(2)
            lower4 = sq(a, 2) + cup(w, a)
            lower5 = parity(n, u, w, s)
            assert n.d()(tuple(range(4))) == 0
            assert (u.d() + lower4)(tuple(range(5))) == 0
            assert (c.d() + lower5)(tuple(range(6))) == 0
            # Every mixed source vanishes on these four separate-layer inputs:
            # d u = 0, kappa(u) = 0, Xi = 0, and either n = 0 or u = 0.
            assert u.d()(tuple(range(5))) == 0
            assert kappa(u, w, s)(tuple(range(6))) == 0
            assert pure_parity(n, w, s)(tuple(range(6))) == 0
            if has_n:
                y = C(6, values={top: y_value})
                pieces = pure_terms16(n, w, s, binary_y=y)
                numerator = sum(term(top) for term in pieces.values())
                current = Fraction(numerator, 16) + Fraction(cup(cup(n, n), n)(top), 12)
                previous = current
            else:
                current = Fraction(mc_phase4(u, c, w, s)(top), 4)
                previous = Fraction(previous_gamma(u, w, s)[0](top), 4)
                previous += Fraction((sq(c, 2) + cup(w, c))(top), 2)
            transport = R5(u, c, w, s)
            transport_derivative = Fraction(ds(transport, s)(top), 4)
            assert (previous - current - transport_derivative) % 1 == 0
            old_nu = m(5, None).scaled(old_phase)
            new_nu = m(5, None).scaled(new_phase)
            residual = (new_nu.d()(top) - current) % 1
            assert residual == 0
            f5 = tuple(range(6))
            assert (new_nu(f5) - old_nu(f5) + Fraction(transport(f5), 4)) % 1 == 0
            records[name]['values'].append({
                'tuple': list(edges), 'source': frac(current),
                'd_nu_current': frac(new_nu.d()(top)),
                'current_residual': frac(residual),
                'old_phase_in_current_source_residual': frac(old_nu.d()(top) - current),
                'source_transport_residual': frac(previous - current - transport_derivative),
            })
    for name, data in records.items():
        data['current_residual_nonzero_count'] = sum(row['current_residual'] != '0/1' for row in data['values'])
        data['old_phase_in_current_source_nonzero_count'] = sum(row['old_phase_in_current_source_residual'] != '0/1' for row in data['values'])
        data['source_coefficient'] = data['values'][-1]['source']
    pinned = [
        'docs/formulas/source/equations/four-dimensional--4-bosonic-obstruction--14.tex',
        'docs/formulas/source/equations/four-dimensional--4-bosonic-obstruction--16.tex',
        'docs/formulas/source/equations/four-dimensional-majorana-phase--phase-change--1.tex',
        'formulas/SOURCE_COEFFICIENTS.json',
        'formulas/publication_source/reference/d4_input/code/word_residual_program.txt',
        'scripts/verify_majorana_phase_transport.py',
    ]
    return {
        'status': 'PASS', 'dimension': '4+1D',
        'symmetry': {'Gf': 'Z4^f', 'Gb': 'C2', 'omega2': 'm1^2', 's1': '0'},
        'phase_convention': 'Current reader coordinate: nu5 = nu5_previous - R5(check_n3,n4).',
        'normalization': 'm1^q(g1,...,gq) = product(gj), with gj in {0,1}; all tuples are included.',
        'six_tuples_checked_per_root': 64,
        'lower_equations': {'d_n2': 'PASS on all 8 triples', 'd_n3': 'PASS on all 16 four-tuples', 'd_n4': 'PASS on all 32 five-tuples'},
        'R5_Majorana_coefficient': '1/4',
        'coefficient_table_matches_reader_source': True,
        'relative_MS_polynomial_checked_on_all_64_tuples': True,
        'relative_MS_words_after_zero_input_removal': len(relative_closed_rows),
        'source_sha256': {name: hashlib.sha256((ROOT / name).read_bytes()).hexdigest() for name in pinned},
        'y6_values': y_values, 'roots': records,
        'scope': 'Exact concrete cochain solutions and paired phase transport. Existing Z16 group is preserved by the invertible transport; its full presentation is not recomputed here.',
    }


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write the complete exact receipt.')
    args = parser.parse_args()
    with tempfile.TemporaryDirectory(prefix='fspt-z4f-') as temporary:
        library = Path(temporary) / 'residual_engine.so'
        subprocess.run(['g++', '-std=c++17', '-O2', '-fPIC', '-shared',
                        str(CODE / 'residual_engine.cpp'), '-o', str(library)], check=True, timeout=60)
        report = check(library)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps({
        'status': report['status'], 'tuples_per_root': 64,
        'phases': {name: data['current_phase_coefficient'] for name, data in report['roots'].items()},
        'sources': {name: data['source_coefficient'] for name, data in report['roots'].items()},
        'current_residuals': {name: data['current_residual_nonzero_count'] for name, data in report['roots'].items()},
    }))


if __name__ == '__main__':
    main()
