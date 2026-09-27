"""Contrasts between physical conventions are not an oracle comparison."""
import copy
import csv
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import report_physical_conventions as report


def row(n, spin):
    return {'space_group': n, 'crystalline_spin': spin, 'physical_convention': spin,
            'effective_sign': 'w1(V)', 'effective_omega': '0' if spin == 'half' else 'w2+w1^2',
            'layers': {'pip': [0], 'majorana': [], 'complex_fermion': [2], 'bosonic': []},
            'invariants': [0, 2], 'invariant_options': None, 'free_lattice': {'index': 2},
            'marked_witnesses': spin == 'half', 'kind': 'marked' if spin == 'half' else 'abstract',
            'source_id': spin, 'result_sha256': 'a'*64}


class PhysicalConventionReportTests(unittest.TestCase):
    def test_ambiguous_family_is_not_claimed_equal(self):
        a, b = row(1, 'half'), row(1, 'spinless')
        b.update(invariants=None, invariant_options=[[0, 2], [0, 4]])
        result = report.contrast(a, b)
        self.assertEqual(result['full_group_comparison'], 'undetermined-spin-half-group-is-an-option')
        self.assertIn('not-external-validation', result['interpretation'])
        b['invariant_options'] = [[0, 4]]
        self.assertEqual(report.contrast(a, b)['full_group_comparison'], 'all-certified-spinless-options-differ')

    def test_layer_and_free_index_changes_are_separate(self):
        a, b = row(1, 'half'), row(1, 'spinless')
        b['layers']['majorana'] = [2]; b['free_lattice']['index'] = 4
        result = report.contrast(a, b)
        self.assertTrue(result['majorana_changed']); self.assertTrue(result['free_index_changed'])
        self.assertEqual(result['full_group_comparison'], 'same-abstract-group')

    def test_writer_emits_460_labeled_rows_without_promoting_marked_scope(self):
        a = [row(n, 'half') for n in range(1, 231)]
        b = [row(n, 'spinless') for n in range(1, 231)]
        mocked = ({'rows': b, 'all_230_certificates_strictly_valid': True, 'source_ids': ['spinless']}, False)
        # Writer-only fixture: mathematical acceptance is independently tested
        # by the two actual auditor suites, not by these synthetic rows.
        with tempfile.TemporaryDirectory() as directory, patch.object(report, 'half_rows', return_value=a), patch.object(report, 'audit_spinless', return_value=mocked), patch.object(report, 'geometric_overlap', return_value=[]):
            output = Path(directory)/'out'
            report.generate(Path('half'), Path('spinless'), output)
            with (output/'physical_conventions_460.csv').open() as handle:
                rows = list(csv.DictReader(handle))
            self.assertEqual(len(rows), 460)
            self.assertEqual(rows[0]['actual_marked_witnesses'], 'True')
            self.assertEqual(rows[230]['actual_marked_witnesses'], 'False')
            self.assertIn('not an external verification', (output/'README.md').read_text())
            self.assertFalse(json.loads((output/'comparison.json').read_text())['external_reference_answers_read'])


if __name__ == '__main__':
    unittest.main()
