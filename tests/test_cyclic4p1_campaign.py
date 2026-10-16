"""Complete cyclic roots, independent physical lattices, and cache isolation."""
from fractions import Fraction as F
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

from insulator import api as ci
from insulator.cyclic4p1 import ExactOperations, calculate, canonical_roots, state_record
from insulator.cyclic_physical import compare_physical, eta_characters, smith_factors
from scripts.audit_cyclic_4p1 import bar_root_relations
from scripts import classify_cyclic_4p1 as runner


class CompleteCyclicTests(unittest.TestCase):
    def test_cached_and_uncached_complete_witnesses_and_existing_audit(self):
        for order in (1, 2, 3):
            reference = calculate(order, cache=False)
            cached = calculate(order, cache=True)
            self.assertEqual(reference[:2], cached[:2])
            self.assertEqual(cached[0]['presentation'], bar_root_relations(order)['presentation'])
            self.assertEqual(cached[0]['actualGroupOrder'], order**4)
            self.assertEqual(cached[0]['nonvacuousRootCompletionChecks'], 4*(order-1)**2)
            self.assertTrue(compare_physical(order, cached[0]['presentation'])['exactRelationLatticeMatch'])
            if order > 1:
                self.assertGreater(sum(cached[2]['hits'].values()), 0)

    def test_actual_operations_match_public_e8state_on_six_simplex(self):
        a, x, zero, symmetry, roots = canonical_roots(3, (1, 2, 1, 2, 1, 1))
        engine = ExactOperations()
        for root in roots:
            root.validate(symmetry, 4)
            for exponent in (-2, 0, 3):
                actual = engine.power(symmetry, root, exponent)
                expected = root.power(exponent, symmetry, 4)
                self.assertEqual(state_record(actual), state_record(expected))
            actual = engine.gauge(symmetry, root, a, a.sc(-1), a.cup(x))
            expected = root.gauge(symmetry, 4, a, a.sc(-1), a.cup(x))
            self.assertEqual(state_record(actual), state_record(expected))
        self.assertEqual(state_record(engine.stack(symmetry, roots[0], roots[1])),
                         state_record(roots[0].stack(roots[1], symmetry, 4)))

    def test_eta_kernel_detects_wrong_physical_dictionary_at_same_smith_group(self):
        presentation = [[3, 0, 0, -1], [0, 3, 0, -2], [0, 0, 3, 0], [0, 0, 0, 3]]
        wrong = [row[:] for row in presentation]
        wrong[1][3] = -1
        self.assertEqual(smith_factors(presentation), smith_factors(wrong))
        self.assertTrue(compare_physical(3, presentation)['exactRelationLatticeMatch'])
        with self.assertRaises(ArithmeticError):
            compare_physical(3, wrong)
        # Exact group-ring eta construction also covers a prime > 3 and a
        # mixed order; no cochain campaign is performed by these arithmetic checks.
        self.assertEqual(len(eta_characters(7)), 8)
        self.assertEqual(len(eta_characters(15)), 16)

    def test_cache_keys_include_background_values_and_return_no_mutable_alias(self):
        a, x, zero, symmetry, roots = canonical_roots(3, (1, 2, 1, 2, 1, 1))
        omega = a.d().sc(F(1, 2))
        other = ci.Symmetry(omega, zero(1), zero(1))
        engine = ExactOperations(capacity=2)
        first = engine.source(symmetry, roots[2])
        original = dict(first.v)
        first.v[tuple(range(7))] = F(7, 11)
        again = engine.source(symmetry, roots[2])
        self.assertEqual(again.v, original)
        self.assertEqual((engine.source(other, roots[2]) -
                          ci.source(other, 4, roots[2].n_p, roots[2].n_p2)).mod(1).maxabs(), 0)
        self.assertEqual(engine.misses['source'], 2)
        engine.source(symmetry, roots[0])
        self.assertEqual(engine.evictions, 1)
        self.assertLessEqual(len(engine.cache), 2)
        bad = ci.Cochain(6, 2, {(0, 1, 2): 0.0})
        with self.assertRaises(TypeError):
            engine.call('bad', (bad,), lambda: bad)

    def test_case_record_keeps_intrinsic_section_separate(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            inputs = runner.input_record(2)
            runner.write_json(directory / 'input.json', inputs)
            import hashlib
            record = {'status': 'running', 'inputSHA256': hashlib.sha256((directory / 'input.json').read_bytes()).hexdigest(),
                      'sourceSHA256': 'fixture', 'startedUTC': 'fixture'}
            runner.write_json(directory / 'run.json', record)
            with patch.object(runner, 'manifest', return_value={'sha256': 'fixture', 'files': {}}):
                runner.case_worker(2, directory, 'fixture', True)
            result = json.loads((directory / 'result.json').read_text())
            self.assertEqual(result['run']['status'], 'complete')
            self.assertEqual(result['classification']['torsion'], [2, 8])
            self.assertEqual(result['classification']['freeRank'], 0)
            self.assertEqual(result['uniformResponse']['fullGroup']['freeRank'], 2)
            self.assertFalse(result['uniformResponse']['cochainIntrinsicImplemented'])
            self.assertEqual(result['physicalComparison']['status'], 'PASS')
            self.assertEqual(result['evidence']['sha256'], hashlib.sha256((directory / 'cycle_evidence.json').read_bytes()).hexdigest())

    def test_failed_physical_comparison_preserves_computed_roots(self):
        with tempfile.TemporaryDirectory() as temporary:
            directory = Path(temporary)
            runner.write_json(directory / 'input.json', runner.input_record(2))
            import hashlib
            runner.write_json(directory / 'run.json', {
                'status': 'running', 'sourceSHA256': 'fixture', 'startedUTC': 'fixture',
                'inputSHA256': hashlib.sha256((directory / 'input.json').read_bytes()).hexdigest()})
            with patch.object(runner, 'manifest', return_value={'sha256': 'fixture', 'files': {}}), \
                    patch.object(runner, 'compare_physical', side_effect=ArithmeticError('deliberate mismatch')):
                run = runner.case_worker(2, directory, 'fixture', True)
            raw = json.loads((directory / 'computed_result.json').read_text())
            result = json.loads((directory / 'result.json').read_text())
            self.assertEqual(raw['classification']['torsion'], [2, 8])
            self.assertEqual(result['physicalComparison']['status'], 'FAIL')
            self.assertEqual(run['status'], 'calibration_failed')
            self.assertEqual(run['exitCode'], 2)

    def test_source_manifest_covers_every_local_runtime_and_comparison_module(self):
        source = runner.manifest()['files']
        for path in ('insulator/cyclic4p1.py', 'insulator/cyclic_physical.py',
                     'insulator/api.py', 'insulator/e8.py', 'insulator/_engine/simplex.py',
                     'insulator/_engine/product4d.py', 'insulator/_engine/gauge4d.py',
                     'insulator/_engine/e8_4p1.py', 'insulator/_engine/cartan32_polarizer.json',
                     'insulator/_engine/r_polarizer.json', 'scripts/classify.py',
                     'scripts/classify_cyclic_4p1.py'):
            self.assertIn(path, source)


if __name__ == '__main__':
    unittest.main()
