"""Public finite input/result consistency; no private references or GAP needed."""
import csv
import hashlib
import json
from math import prod
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.finite_examples import gap_literal, group_signature, project_result
DATA = ROOT / 'results/finite_examples'
if not DATA.is_dir():
    DATA = ROOT / 'publication/finite_examples'


class FiniteExampleTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.models = json.loads((DATA / 'models.json').read_text())['models']

    def test_exact_symmetry_inputs(self):
        self.assertEqual(len(self.models), 53)
        for model in self.models:
            n, table, sign, omega = (model[k] for k in ('order', 'productTable', 's1', 'omega2'))
            exact = {k: model[k] for k in ('order', 'productTable', 's1', 'omega2')}
            encoded = json.dumps(exact, sort_keys=True, separators=(',', ':')).encode()
            self.assertEqual(hashlib.sha256(encoded).hexdigest(), model['exact_input_sha256'])
            self.assertEqual(table[0], list(range(1, n + 1)))
            for g in range(n):
                self.assertEqual(table[g][0], g + 1)
                self.assertEqual(sorted(table[g]), list(range(1, n + 1)))
                self.assertEqual(omega[0][g], 0)
                self.assertEqual(omega[g][0], 0)
                for h in range(n):
                    gh = table[g][h] - 1
                    self.assertEqual(sign[gh], (sign[g] + sign[h]) % 2)
                    for k in range(n):
                        hk = table[h][k] - 1
                        self.assertEqual(table[gh][k], table[g][hk])
                        self.assertEqual((omega[h][k] + omega[gh][k] + omega[g][hk] + omega[g][h]) % 2, 0)

    def test_results_and_collections(self):
        counts = {3: 0, 4: 0}
        for model in self.models:
            for dimension in model['verified_dimensions']:
                result = json.loads((DATA / 'results' / ('d%d_%s.json' % (dimension, model['id']))).read_text())
                self.assertEqual(result['model_id'], model['id'])
                self.assertEqual(result['status'], 'computed')
                counts[dimension] += 1
                if dimension == 3:
                    stack = result['stacking']
                    self.assertEqual(stack['invariant_options'], [stack['invariants']])
                    self.assertEqual(prod(stack['invariants']), prod(n for layer in result['layers'].values() for n in layer))
        self.assertEqual(counts, {3: 16, 4: 53})
        for name, count in [('finite_16', 32), ('four_dimensional_43', 43), ('pip_controls', 8)]:
            rows = json.loads((DATA / 'collections' / (name + '.json')).read_text())
            self.assertEqual(len(rows), count)
            for row in rows:
                self.assertTrue((DATA / row['result']).is_file())
        for dimension in (3, 4):
            with (DATA / 'tables' / ('classification_%dd.csv' % dimension)).open() as stream:
                rows = list(csv.DictReader(stream))
            self.assertEqual(len(rows), counts[dimension])
            for row in rows:
                saved = json.loads((DATA / 'results' / ('d%d_%s.json' % (dimension, row['model_id']))).read_text())
                for field, value in saved['layers'].items():
                    self.assertEqual(json.loads(row[field]), value)
                if dimension == 3:
                    self.assertEqual(json.loads(row['full_group']), saved['stacking']['invariants'])

    def test_q8_square_certificate(self):
        certificate = json.loads((DATA / 'certificates/Q8_w0_s0_square.json').read_text())
        self.assertEqual(certificate['fullGroupInvariants'], [2, 2])
        self.assertFalse(any(certificate['projectedSquare']))
        self.assertTrue(any(certificate['nativeSquare']))
        self.assertEqual(certificate['filtration']['bosonic'], [])

    def test_calibration_pairings_and_geometric_aggregate(self):
        def load(name):
            return json.loads((DATA / 'calibrations' / (name + '.json')).read_text())['computed']

        q8 = load('q8_d3_detectors')
        self.assertEqual(len(q8['cases']), 6)
        self.assertEqual(q8['all_lower_choices']['all_towers'], 18)
        self.assertTrue(q8['all_lower_choices']['all_passed'])
        for case in q8['cases']:
            phase = case['O4'] if 'O4' in case else case['O5']
            self.assertEqual(sum(phase[i] for i in case['detector_cycle_indices']) % 2, 1)
            self.assertTrue(case['all_Majorana_shift_classes_zero'])
        for name in ('v4_euler', 'd8_reflection_square_d4'):
            data = load(name)
            for choice in data['choices']:
                values = dict(zip(map(tuple, data['words']), choice['phase_values']))
                pairings = [sum(coefficient * values[tuple(word)] for word, coefficient in cycle) % 16
                            for cycle in data['cycles']]
                self.assertEqual(pairings, choice['cycle_pairings_mod16'])
        d8 = load('d8_reflection_square_d4')
        self.assertEqual(d8['target_identification']['rank'], 3)
        self.assertTrue(all(not any(row) for row in d8['CF_shift_pairings_mod16']))
        self.assertTrue(all(row['cycle_pairings_mod16'] == [8, 8, 0, 8, 8, 0] for row in d8['choices']))
        spin = load('spinc_t2_cp2')
        self.assertEqual(len(spin['terms']), 90)
        self.assertEqual(sum(t['coefficient'] * t['phase_mod16'] for t in spin['terms'].values()) % 16, 2)
        for key, value in spin['aggregate_terms_mod16'].items():
            self.assertEqual(sum(t['coefficient'] * t['parts_mod16'][key] for t in spin['terms'].values()) % 16, value)
        self.assertTrue(spin['chain_and_index']['integral_boundary_zero'])
        self.assertEqual(spin['chain_and_index']['Dirac_index'], '0')
        self.assertEqual(spin['normalization_detectors']['period_after_adding_Pi6'], '5/8')
        controls = load('c2_exact_phase')
        self.assertEqual(controls['1']['numerator_mod16'], 0)
        self.assertEqual(controls['2']['numerator_mod16'], 7)
        self.assertEqual(controls['O6_primitive'], '7 x^5/32')

    def test_manifest_and_nonredundant_incoming_certificate(self):
        manifest = json.loads((DATA / 'manifest.json').read_text())
        for category, base in [('payload_files', DATA), ('production_files', ROOT)]:
            for name, evidence in manifest[category].items():
                payload = (base / name).read_bytes()
                self.assertEqual(hashlib.sha256(payload).hexdigest(), evidence['sha256'])
                self.assertEqual(len(payload), evidence['bytes'])
        raw = {'status': 'computed', 'pip': {'orders': [], 'torsion': []},
               'majorana': [2], 'complex_fermion': [], 'bosonic': [2],
               'ranks': {}, 'resolution_dimensions': [],
               'stacking': {'lower': {'invariants': [2, 2]},
                            'lowerBeforeH0Incoming': {'invariants': [2, 2, 2]},
                            'h0IncomingQuotient': {'backgroundQuotient': {
                                'incomingCoordinates': [1, 0, 0],
                                'preQuotientLower': {'finalFiltrationCertificate': {'convention': 'legacy geometry label'}}}}}}
        result = project_result(raw, 3, 'test')
        self.assertEqual(result['stacking']['h0_incoming_quotient'], {'incomingCoordinates': [1, 0, 0]})
        self.assertEqual(result['stacking']['lower_before_h0']['invariants'], [2, 2, 2])

    def test_payloads_have_no_private_research_records(self):
        for path in DATA.rglob('*'):
            if path.is_file():
                text = path.read_text()
                for marker in ('internal_notes/', '/home/user/', '/home/xingyu/',
                               'counterfactualKnownMajoranaLawVariation', 'majoranaBosonicCarryAudit'):
                    self.assertNotIn(marker, text, str(path))
        self.assertEqual(gap_literal({'id': 'C2', 's1': [0, 1]}), 'rec(id:="C2",s1:=[0,1])')


if __name__ == '__main__':
    unittest.main()
