"""Later-run auditing must preserve the pre-reference provenance boundary."""
import copy
from contextlib import redirect_stdout
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from compare_boss import CURRENT_FORMULA_CONVENTION, LAYERS, compare_current, load_current
import compare_boss


def complete_record(n):
    hashes = {'gap/test-only-fixture.g': hashlib.sha256(b'test fixture').hexdigest()}
    return dict(space_group=n, convention='physical-spin-half-det-sign-omega0',
                formula_convention=CURRENT_FORMULA_CONVENTION, sptset_loaded=False,
                status='computed', pip=dict(status='computed', orders=[], free_rank=0),
                majorana=[], complex_fermion=[], bosonic=[], source_sha256=hashes,
                source_id=hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest(),
                stacking=dict(status='computed', invariants=[], lower=dict(invariants=[],
                    presentation=[], smithRowTransform=[], smithColumnTransform=[],
                    smithDiagonal=[], enumeratedPhaseProducts=0)))


class CurrentRunTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.root = Path(self.temp.name)

    def tearDown(self):
        self.temp.cleanup()

    def populate(self):
        for n in range(1, 231):
            (self.root / ('sg%d.json' % n)).write_text(json.dumps(complete_record(n)))

    def test_partial_run_rejected_before_loading_any_result(self):
        (self.root / 'sg1.json').write_text('not even a parsed result')
        with self.assertRaisesRegex(ValueError, 'exactly 230 complete results'):
            load_current(self.root)

    def test_complete_run_records_every_hash_and_later_run_role(self):
        self.populate()
        records, provenance = load_current(self.root)
        self.assertEqual(set(records), set(range(1, 231)))
        self.assertEqual(len(provenance['result_sha256']), 230)
        self.assertTrue(provenance['complete_witnesses_passed'])
        self.assertIn('not a pre-reference freeze', provenance['comparison_role'])
        self.assertNotIn('external_answers_consulted_at_freeze', provenance)
        self.assertEqual(provenance['result_sha256']['sg1.json'],
                         hashlib.sha256((self.root / 'sg1.json').read_bytes()).hexdigest())

    def test_classification_only_and_obsolete_convention_are_rejected(self):
        self.populate()
        bad = complete_record(1)
        del bad['stacking']
        (self.root / 'sg1.json').write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, 'full stacking is missing'):
            load_current(self.root)
        bad = complete_record(1)
        bad['formula_convention'] = 'old-coordinate'
        (self.root / 'sg1.json').write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, 'formula convention differs'):
            load_current(self.root)

    def test_abstract_upper_extension_without_phase_is_rejected(self):
        self.populate()
        bad = complete_record(1)
        bad['pip']['orders'] = [2]
        bad['stacking']['invariants'] = [2]
        bad['stacking']['fullUpperPhaseWitness'] = False
        (self.root / 'sg1.json').write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, r'torsion p\+ip phase witness is missing'):
            load_current(self.root)

    def test_free_rank_without_primitive_phase_witness_is_rejected(self):
        self.populate()
        bad = complete_record(1)
        bad['pip']['orders'] = [0]
        bad['pip']['free_rank'] = 1
        bad['stacking']['invariants'] = [0]
        bad['stacking']['freePipRank'] = 1
        (self.root / 'sg1.json').write_text(json.dumps(bad))
        with self.assertRaisesRegex(ValueError, r'primitive free p\+ip phase witnesses are missing'):
            load_current(self.root)

    def test_partial_cli_preserves_existing_report_and_writes_no_new_one(self):
        (self.root / 'sg1.json').write_text('{}')
        output = self.root / 'report'
        output.mkdir()
        original = output / 'reference_comparison.json'
        original.write_bytes(b'preserved historical report\n')
        script = Path(__file__).resolve().parents[1] / 'scripts/compare_boss.py'
        result = subprocess.run([sys.executable, str(script), '--current', str(self.root),
                                 '--output', str(output)], capture_output=True, text=True)
        self.assertEqual(result.returncode, 1)
        self.assertIn('exactly 230 complete results', result.stderr)
        self.assertEqual(original.read_bytes(), b'preserved historical report\n')
        self.assertEqual(list(output.iterdir()), [original])

    def test_complete_cli_writes_separate_reports_and_preserves_original(self):
        self.populate()
        current, _ = load_current(self.root)
        manifest = dict(groups=230, external_answers_consulted=False, frozen_at=123,
                        result_sha256={'sg%d.json' % n: 'frozen-hash-%d' % n for n in current})
        reference = dict(entries={n: dict(name='fixture', pdf_page=7,
            current={layer: {'orders': []} for layer in LAYERS},
            historical_draft={layer: {'orders': []} for layer in LAYERS}) for n in current},
            pages=[], parser='test-only-reference', pymupdf_version='test')
        pdf, text = self.root / 'test.pdf', self.root / 'test.txt'
        pdf.write_bytes(b'test-only PDF placeholder')
        text.write_bytes(b'test-only text placeholder')
        output = self.root / 'output'
        output.mkdir()
        original = output / 'reference_comparison.json'
        original.write_bytes(b'unchanged original comparison\n')
        argv = ['compare_boss.py', '--current', str(self.root), '--output', str(output),
                '--pdf', str(pdf), '--text', str(text)]
        with patch.object(sys, 'argv', argv), \
             patch.object(compare_boss, 'parse_reference', return_value=reference), \
             patch.object(compare_boss, 'load_frozen', return_value=(current, manifest, 'frozen-manifest-hash')), \
             redirect_stdout(io.StringIO()):
            compare_boss.main()
        self.assertEqual(original.read_bytes(), b'unchanged original comparison\n')
        result = json.loads((output / 'current_reference_comparison.json').read_text())
        self.assertEqual(result['frozen']['manifest_sha256'], 'frozen-manifest-hash')
        self.assertEqual(result['frozen']['result_sha256'], manifest['result_sha256'])
        self.assertEqual(result['counts']['current_vs_reference'], {'match': 920})
        self.assertEqual(result['counts']['current_vs_frozen'], {'match': 920})
        self.assertEqual(result['preserved_original_report_sha256']['reference_comparison.json'],
                         hashlib.sha256(original.read_bytes()).hexdigest())
        self.assertTrue((output / 'current_reference_comparison.csv').is_file())
        self.assertTrue((output / 'current_reference_comparison.md').is_file())

    def test_frozen_fields_unchanged_and_differences_counted_separately(self):
        self.populate()
        records, provenance = load_current(self.root)
        frozen = dict(directory='original-freeze', manifest_sha256='original-manifest-hash',
                      frozen_at=123, external_answers_consulted_at_freeze=False,
                      result_sha256={'sg%d.json' % n: 'original-%d' % n for n in range(1, 231)})
        rows = [dict(space_group=n, space_group_name='test', layer=layer,
                     independent_orders=[], independent_group='0', reference_orders=[],
                     reference_group='0', status='match', pdf_page=7,
                     independent_source_id='original-source')
                for n in range(1, 231) for layer in LAYERS]
        original = dict(reference={'pdf_sha256': 'original-pdf'}, frozen=frozen, rows=rows,
                        convention={}, scope='four layers', free_lattice_comparison='unavailable',
                        full_stacking_comparison='unavailable')
        untouched = copy.deepcopy(original)
        records[1]['bosonic'] = [2]
        report = compare_current(original, records, provenance)
        self.assertEqual(original, untouched)
        self.assertEqual(report['frozen'], untouched['frozen'])
        self.assertEqual(report['counts']['current_vs_frozen'], {'match': 919, 'mismatch': 1})
        self.assertEqual(report['counts']['current_vs_reference'], {'match': 919, 'mismatch': 1})
        self.assertEqual(report['counts']['frozen_vs_reference'], {'match': 920})
        self.assertIn('later formula/performance regression run', report['chronology'])


if __name__ == '__main__':
    unittest.main(verbosity=2)
