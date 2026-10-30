"""Independent exact comparisons for guarded U1 source/product integer DAGs."""
from fractions import Fraction
from itertools import combinations
import json
import os
from pathlib import Path
import random
import shutil
import subprocess
import tempfile
import unittest
from unittest.mock import patch

from insulator import api as U
from insulator.worker import _evaluate
from insulator._compiled import runtime as R
from insulator._compiled.compiler import compile_program

ROOT = Path(__file__).resolve().parents[1]


def field(N, p, sign, rng, scale=1):
    return U.Cochain(N, p, {f: scale * rng.randint(-7, 7)
                           for f in combinations(range(N + 1), p + 1)}, sign)


def wire(cochain):
    return {','.join(map(str, face)): str(value) for face, value in cochain.v.items()}


def request(operation, seed, scale=1, completed=False):
    N = 5 if operation == 'source' else 4
    rng = random.Random(seed)
    s = [rng.randrange(2) for _ in range(N + 1)]
    r = [rng.randrange(2) for _ in range(N + 1)]
    sign = [a ^ b for a, b in zip(s, r)]
    omega = field(N, 1, sign, rng, Fraction(1, 2)).d() + field(N, 2, sign, rng)
    symmetry = U.Symmetry(omega, U.char(N, s).ret(s), U.char(N, r).ret(r))
    fields = {}
    for suffix in ('', '_prime') if operation == 'product' else ('',):
        if completed:
            u = field(N, 0, s, rng, scale)
            sheet = u.d()
            charge = symmetry.B3.cup(u) + field(N, 2, r, rng, scale).d()
        else:
            sheet = field(N, 1, s, rng, scale)
            charge = field(N, 3, r, rng, scale)
        fields['sheet' + suffix] = wire(sheet)
        fields['charge' + suffix] = wire(charge)
    return dict(schema_version=2,op=operation, dimension=3, simplex_dimension=N, s=s, r=r,
                omega=wire(omega), validate=completed, **fields)


class CompiledSource3Tests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        compiler = shutil.which('g++')
        if compiler is None:
            raise unittest.SkipTest('g++ is required to test native checked-overflow execution')
        cls.temporary = tempfile.TemporaryDirectory(prefix='u1-dag-test-')
        cls.library = str(Path(cls.temporary.name) / 'u1_dag_vm.so')
        subprocess.run([compiler, '-std=c++11', '-O3', '-fPIC', '-shared',
                        str(ROOT / 'insulator/_compiled/u1_dag_vm.cpp'), '-o', cls.library], check=True)

    @classmethod
    def tearDownClass(cls):
        cls.temporary.cleanup()

    def evaluate(self, data, mode):
        with patch.dict(os.environ, U1_DAG_MODE=mode, U1_DAG_LIBRARY=self.library):
            try:
                return {'ok': True, 'result': _evaluate(data)}
            except Exception as error:
                return {'ok': False, 'error': type(error).__name__ + ': ' + str(error)}

    def assert_modes(self, data):
        expected = self.evaluate(data, 'reference')
        self.assertEqual(self.evaluate(data, 'python'), expected)
        self.assertEqual(self.evaluate(data, 'auto'), expected)
        return expected

    def test_reproducible_programs(self):
        for operation in ('source', 'product'):
            expected = json.loads((ROOT / ('insulator/_compiled/' + operation + '3.json')).read_text())
            self.assertEqual(json.loads(json.dumps(compile_program(operation))), expected)
            self.assertTrue(R._matches_sources(expected))
            bad = dict(expected, source_sha256={'_engine/simplex.py': '0' * 64})
            self.assertFalse(R._matches_sources(bad))

    def test_independent_signed_negative_and_completed_towers(self):
        for operation in ('source', 'product'):
            for seed in range(12):
                for completed in (False, True):
                    with self.subTest(operation=operation, seed=seed, completed=completed):
                        result = self.assert_modes(request(operation, seed, completed=completed))
                        self.assertTrue(result['ok'], result)
        programs = [R._program(op, 'auto', self.library) for op in ('source', 'product')]
        self.assertTrue(all(p.native_hits > 0 for p in programs))

    def test_overflow_and_out_of_range_inputs(self):
        for operation in ('source', 'product'):
            program = R._program(operation, 'auto', self.library)
            before = program.integer_fallbacks
            for scale in (1 << 50, -(1 << 90)):
                data = request(operation, 12, scale=scale)
                data['omega'] = {k: str(Fraction(v) * (1 << 40)) for k, v in data['omega'].items()}
                result = self.assert_modes(data)
                self.assertTrue(result['ok'], result)
            self.assertGreaterEqual(program.integer_fallbacks - before, 2)

    def test_nonintegral_background_and_zero_sheet_fallback(self):
        for operation in ('source', 'product'):
            data = request(operation, 19)
            N = data['simplex_dimension']
            sign = [a ^ b for a, b in zip(data['s'], data['r'])]
            omega = field(N, 1, sign, random.Random(52), Fraction(1, 3)).d()
            data['omega'] = wire(omega)
            self.assertTrue(self.assert_modes(data)['ok'])
            data = request(operation, 17)
            data['sheet'] = {}
            if operation == 'product':
                data['sheet_prime'] = {}
            self.assertTrue(self.assert_modes(data)['ok'])

    def test_missing_native_library_and_context_isolation(self):
        data = request('source', 23)
        reference = self.evaluate(data, 'reference')
        with patch.dict(os.environ, U1_DAG_MODE='auto', U1_DAG_LIBRARY='/nonexistent/u1_vm.so'):
            self.assertEqual({'ok': True, 'result': _evaluate(data)}, reference)
        for operation in ('source', 'product'):
            states = [request(operation, seed) for seed in (31, 32, 33)]
            expected = [self.evaluate(item, 'reference') for item in states]
            for index in (0, 1, 0, 2, 1, 0):
                self.assertEqual(self.evaluate(states[index], 'auto'), expected[index])

    def test_validation_and_errors_unchanged(self):
        data = request('source', 22)
        variants = [dict(data, dimension=7), dict(data, simplex_dimension=-1),
                    dict(data, s=[0]), dict(data, validate='false'),
                    dict(data, sheet={'0,1': '1/2'}, validate=True),
                    dict(data, omega={'0,1,2': '1/3'}),
                    dict(data, charge={'values': {}, 'degree': 2}),
                    dict(data, sheet={'0,0': 1}), dict(data, validate=True)]
        for item in variants:
            with self.subTest(item=item):
                self.assertFalse(self.assert_modes(item)['ok'])
        # validate=False still uses the reference evaluator for noninteger
        # decorations; it must not silently truncate them to integer VM fields.
        self.assert_modes(dict(data, sheet={'0,1': '1/2'}, validate=False))


if __name__ == '__main__':
    unittest.main()
