"""Literal run comparisons must retain cochains beyond group isomorphism type."""
import copy
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import compare_background_runs as comparison
from test_audit_background_run import example


class LiteralBackgroundComparisonTests(unittest.TestCase):
    def test_free_candidate_diagnostics_are_explicit_new_evidence(self):
        path = Path(__file__).resolve().parents[1]/'results/space_groups/sg84.json'
        old = json.loads(path.read_text()); new = copy.deepcopy(old)
        q = new['pip']['free_lattice']['parityCandidates'][1]
        self.assertTrue(any(q['majorana_adjustment']))
        q['d3_initial_coordinates'] = [0, 1, 0]
        q['d4_projected_coordinates'] = [0]*len(q['d4_target'])
        a, b, _, _, added = comparison.normalize_pair(old, new, 'half')
        self.assertEqual(a, b)
        self.assertEqual(len(added), 2)
        self.assertIn('/pip/free_lattice/parityCandidates/1/d3_initial_coordinates',
                      [row['path'] for row in added])
        self.assertIn('not independently reconstructed', added[0]['reason'])
        q['majorana_adjustment'][0] ^= 1
        a, b, _, _, _ = comparison.normalize_pair(old, new, 'half')
        self.assertTrue(comparison.differences(a, b))
        q['d3_initial_coordinates'][0] = 2
        with self.assertRaises(AssertionError):
            comparison.normalize_pair(old, new, 'half')

    def test_added_zero_half_diagnostics_have_narrow_checks(self):
        root = Path(__file__).resolve().parents[1]
        path = root/'results/space_groups/sg103.json'
        if not path.exists():
            self.skipTest('accepted spin-half fixture unavailable')
        old = json.loads(path.read_text()); new = copy.deepcopy(old)
        q = new['pip']['torsion'][0]
        q['d3_initial_coordinates'] = [0]*6
        q['d4_projected_coordinates'] = [0]*len(q['d4_target'])
        a, b, _, _, added = comparison.normalize_pair(old, new, 'half')
        self.assertEqual(a, b); self.assertEqual(len(added), 2)
        q['d3_initial_coordinates'][0] = 1
        with self.assertRaises(AssertionError):
            comparison.normalize_pair(old, new, 'half')

    def test_only_enumerated_runtime_fields_are_ignored(self):
        old = example('zero'); new = copy.deepcopy(old)
        new['cpu_ms'] += 100
        new['background_even_pip_compiled_calls'] = 12
        a, b, ignored, _, _ = comparison.normalize_pair(old, new)
        self.assertEqual(a, b)
        self.assertTrue(any(x['path'] == '/background_even_pip_compiled_calls' and x['reason'] for x in ignored))
        new['unreviewed_metadata'] = 1
        a, b, _, _, _ = comparison.normalize_pair(old, new)
        self.assertEqual(comparison.differences(a, b)[0]['path'], '/unreviewed_metadata')

    def test_native_witness_change_is_never_ignored(self):
        old = example('native_cf'); new = copy.deepcopy(old)
        gen = next(g for g in new['stacking']['lower']['generators'] if 'nativeCF3Seed' in g)
        gen['nativeCF3Seed'][0] ^= 1
        a, b, _, _, _ = comparison.normalize_pair(old, new)
        self.assertTrue(any('/nativeCF3Seed/0' in x['path'] for x in comparison.differences(a, b)))
        self.assertEqual(old, example('native_cf'))

    def test_new_matrices_are_reported_as_added_evidence(self):
        new = example('zero'); old = copy.deepcopy(new)
        for key in ('nativeDifferential1F2', 'nativeDifferential2F2', 'nativeH2Generators'):
            del old['crystalline_background'][key]
        a, b, _, _, added = comparison.normalize_pair(old, new)
        self.assertEqual(a, b)
        self.assertEqual(len(added), 3)
        self.assertTrue(all('No earlier matrix' in x['reason'] for x in added))

    def test_two_present_matrices_are_compared(self):
        old = example('h0'); new = copy.deepcopy(old)
        new['crystalline_background']['nativeDifferential1F2'][0][0] ^= 1
        a, b, _, _, added = comparison.normalize_pair(old, new)
        self.assertFalse(added)
        self.assertTrue(comparison.differences(a, b))

    def test_invalid_counter_is_rejected(self):
        old = example('zero'); new = copy.deepcopy(old)
        new['background_sign_pip_compiled_calls'] = -1
        with self.assertRaises(AssertionError):
            comparison.normalize_pair(old, new)

    def test_group_input_hashes_and_pending_coverage(self):
        d = example('zero'); sg = d['space_group']
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory); a = root/'a'; b = root/'b'; a.mkdir(); b.mkdir()
            raw = json.dumps(d).encode()
            for path in (a, b):
                (path/('sg%d.json' % sg)).write_bytes(raw)
            report = comparison.compare(a, b, expected_groups=[sg, 230])
            self.assertTrue(report['all_common_groups_literal_equal'])
            self.assertFalse(report['all_expected_groups_compared_and_equal'])
            self.assertEqual(report['pending_expected_candidates'], [230])
            self.assertGreater(report['rows'][0]['compared_scalar_leaves'], 100)
            self.assertEqual((a/('sg%d.json' % sg)).read_bytes(), raw)


if __name__ == '__main__':
    unittest.main()
