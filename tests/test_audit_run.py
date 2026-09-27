"""Exact presentation audits distinguish groups with equal order and rank."""
import copy
import importlib.util
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('audit_run', ROOT/'scripts/audit_run.py')
AUDIT = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(AUDIT)


class ExactGroupAuditTests(unittest.TestCase):
    def setUp(self):
        self.result = json.loads((ROOT/'tests/fixtures/audit_sg101.json').read_text())

    def test_actual_sg101_presentation_passes(self):
        self.assertEqual(AUDIT.check_result(self.result), 'stacking-with-generator-relations')

    def test_same_order_lower_extension_tampering_is_rejected(self):
        # Both groups have order eight; the measured relation matrix is 2 I_3.
        self.result['stacking']['lower']['invariants'] = [2, 4]
        self.result['stacking']['invariants'] = [2, 4]
        with self.assertRaisesRegex(AssertionError, 'lower presentation and reported group differ'):
            AUDIT.check_result(self.result)

    def test_same_order_final_extension_tampering_is_rejected(self):
        self.result['stacking']['invariants'] = [2, 4]
        with self.assertRaisesRegex(AssertionError, r'free p\+ip split and reported group differ'):
            AUDIT.check_result(self.result)

    def test_column_rank_and_negative_smith_factors(self):
        d = self.result
        d['pip'].update(orders=[0], free_rank=1)
        d.update(majorana=[], complex_fermion=[], bosonic=[0, 0, 2])
        s = d['stacking']
        s.update(freePipRank=1, invariants=[0, 0, 0, 2])
        s['lower'].update(invariants=[0, 0, 2], presentation=[[-2, 0, 0], [0, 0, 0]],
                          smithRowTransform=[[1, 0], [0, 1]],
                          smithColumnTransform=[[1, 0, 0], [0, 1, 0], [0, 0, 1]],
                          smithDiagonal=[-2, 0])
        self.assertEqual(AUDIT.check_result(d), 'stacking-with-generator-relations')
        for rank in (0, 2):
            bad = copy.deepcopy(d)
            bad['stacking']['freePipRank'] = rank
            with self.assertRaisesRegex(AssertionError, r'free p\+ip rank differs'):
                AUDIT.check_result(bad)

    def test_legacy_abstract_upper_scope_is_preserved(self):
        self.result['pip']['orders'] = [2]
        self.result['stacking'].update(invariants=[2, 2, 2, 2], fullUpperPhaseWitness=False)
        self.assertEqual(AUDIT.check_result(self.result), 'stacking-upper-abstract-certificate')
        with self.assertRaisesRegex(AssertionError, r'torsion p\+ip phase witness is missing'):
            AUDIT.check_complete_witnesses(self.result)


if __name__ == '__main__':
    unittest.main()
