"""Reports retain physical conventions and never promote abstract witnesses."""
import csv
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
import report_background_results as reporter
from test_audit_background_run import example


class BackgroundReportTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(); self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name); self.run = self.root/'run'; self.run.mkdir()
        self.output = self.root/'report'

    def save(self, data):
        path = self.run/('sg%d.json' % data['space_group'])
        path.write_text(json.dumps(data))
        return path

    def test_full_report_refuses_partial_before_output(self):
        self.save(example('ext'))
        with self.assertRaisesRegex(ValueError, 'audit refused'):
            reporter.generate(self.run, self.output)
        self.assertFalse(self.output.exists())

    def test_bad_present_result_is_fatal_even_for_partial(self):
        d = example('ext'); d['stacking']['fullUpperPhaseWitness'] = True; self.save(d)
        with self.assertRaisesRegex(ValueError, 'audit refused'):
            reporter.generate(self.run, self.output, allow_partial=True)
        self.assertFalse(self.output.exists())

    def test_partial_tables_preserve_abstract_scope_h0_and_hashes(self):
        ext, h0 = example('ext'), example('h0')
        path = self.save(ext); self.save(h0)
        result = reporter.generate(self.run, self.output, allow_partial=True, tex=True)
        self.assertTrue(result['partial'])
        with (self.output/'space_groups.csv').open() as handle:
            rows = list(csv.DictReader(handle))
        self.assertEqual(len(rows), 230)
        row = rows[ext['space_group']-1]
        self.assertEqual(row['actual_marked_witnesses'], 'False')
        self.assertEqual(row['audit_kind'], 'abstract-upper-family-single-group')
        self.assertEqual(row['crystalline_spin'], 'spinless')
        self.assertEqual(row['effective_omega'], 'w2(V)+w1(V)^2')
        self.assertEqual(row['result_sha256'], hashlib.sha256(path.read_bytes()).hexdigest())
        self.assertEqual(rows[h0['space_group']-1]['h0_incoming_order'], str(h0['h0PipIncoming']['order']))
        text = (self.output/'README.md').read_text()
        self.assertIn('Physical crystalline convention: spinless', text)
        self.assertIn('Equivalent internal convention', text)
        self.assertIn('actual marked witnesses complete: `False`', text)
        self.assertIn('Abstract only', (self.output/'space_groups.tex').read_text())
        with self.assertRaisesRegex(ValueError, 'already exists'):
            reporter.generate(self.run, self.output, allow_partial=True)

    def test_mixed_source_reports_are_refused(self):
        d = example('ext'); self.save(d)
        d = example('h0'); d['source_sha256']['gap/run_one.g'] = 'b'*64
        d['source_id'] = hashlib.sha256(json.dumps(d['source_sha256'], sort_keys=True).encode()).hexdigest()
        self.save(d)
        with self.assertRaisesRegex(ValueError, 'uniform source'):
            reporter.generate(self.run, self.output, allow_partial=True)
        self.assertFalse(self.output.exists())

    def test_possible_full_groups_include_free_pip_rank(self):
        d = example('ext_free'); self.save(d)
        reporter.generate(self.run, self.output, allow_partial=True)
        row = json.loads((self.output/'audit.json').read_text())['rows'][0]
        expected = [[0]*d['pip']['free_rank']+option
                    for option in d['stacking']['pipExtensionCertificate']['invariantOptions']]
        self.assertEqual(row['invariant_options'], expected)
        self.assertIn(d['stacking']['invariants'], row['invariant_options'])


if __name__ == '__main__':
    unittest.main()
