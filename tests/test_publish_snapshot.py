"""Publication policy controls; no GitHub or numerical computation."""
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest
import uuid
from unittest import mock

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('publish_snapshot', ROOT/'scripts/publish_snapshot.py')
pub = importlib.util.module_from_spec(spec)
spec.loader.exec_module(pub)


class PublicationTests(unittest.TestCase):
    def test_reference_exclusions_and_numerical_inclusions(self):
        for path in ['reference/code.py', 'vendor/private.zip', 'runs/result.json',
                     'internal_notes/PENDING_TWISTERS_AND_FINAL_CALIBRATION_ZH.md',
                     'docs/case_reports/UPPER_CARRY_SCOPE_ZH.md',
                     'results/upper_carry_scope/presentation_audit.json',
                     'results/point_groups/report/CALIBRATION_REPORT.md',
                     'notes/crystalline_spinless_formulas.pdf',
                     'results/external_comparison/inputs/legacy_sg068.txt',
                     'results/external_comparison/inputs/space_group_230_layers.pdf',
                     'results/boss_layers/parsed_reference.json', 'results/boss_layers/current_reference_comparison.csv',
                     'results/external_comparison/comparison.json', 'new_private/data.json']:
            self.assertFalse(pub.allowed(path), path)
        for path in ['gap/stacking.g', 'results/space_groups/sg219.json',
                     'docs/CLUSTER_RUN.md', 'results/point_groups/spinless_pg22.json',
                     'results/space_groups_spinless/sg219.json',
                     'results/pip_diagnostics/crystalline_spinless.json',
                     'results/classification_frozen/manifest.json',
                     'results/external_comparison/inputs/finite_c2_controls.json']:
            self.assertTrue(pub.allowed(path), path)

    def test_internal_note_content_and_names_are_not_exported(self):
        private_path = 'internal_notes/research_plan.md'
        marker = uuid.uuid4().hex.encode()
        source = {'README.md': b'# Public results\n', 'scripts/run_gap.py': b'import argparse\n',
                  private_path: marker,
                  'publication/group_tables/README.md': b'# Group structures\n'}
        with mock.patch.object(pub, 'read_commit', return_value=('a'*40, source, {})), \
             mock.patch.object(pub, 'summaries', return_value={}):
            payload, _, manifest = pub.build(ROOT, 'HEAD')
        self.assertNotIn(private_path, payload)
        self.assertNotIn(private_path, manifest['excluded_source_files'])
        self.assertEqual(payload['results/group_tables/README.md'], b'# Group structures\n')
        self.assertFalse(any(marker in b for b in payload.values()))

    def test_finite_release_mapping_and_internal_tool_exclusion(self):
        markers = [uuid.uuid4().hex.encode() for _ in range(3)]
        source = {'README.md': b'# Public results\n', 'scripts/run_gap.py': b'import argparse\n',
                  'publication/finite_examples/models.json': b'{"models":[]}\n',
                  'publication/finite_examples/results/d3_C2.json': b'{}\n',
                  'gap/finite_stacking_audit.g': markers[0],
                  'gap/run_calibration_low.g': markers[1],
                  'gap/run_finite_3d.g': b'public production frontend',
                  'publication/build_finite_examples.py': markers[2]}
        with mock.patch.object(pub, 'read_commit', return_value=('a'*40, source, {})), \
             mock.patch.object(pub, 'summaries', return_value={}):
            payload, _, manifest = pub.build(ROOT, 'HEAD')
        self.assertIn('results/finite_examples/models.json', payload)
        self.assertIn('results/finite_examples/results/d3_C2.json', payload)
        self.assertIn('gap/run_finite_3d.g', payload)
        for marker in markers:
            self.assertFalse(any(marker in value for value in payload.values()))
        self.assertEqual(manifest['allowlist']['finite_example_sources']['results/finite_examples/models.json'],
                         'publication/finite_examples/models.json')

    def test_unreviewed_finite_binary_payload_rejected(self):
        source = {'README.md': b'# Public results\n', 'scripts/run_gap.py': b'import argparse\n',
                  'publication/finite_examples/private_bundle.zip': b'private'}
        with mock.patch.object(pub, 'read_commit', return_value=('a'*40, source, {})), \
             mock.patch.object(pub, 'summaries', return_value={}):
            with self.assertRaisesRegex(ValueError, 'Unreviewed finite-example'):
                pub.build(ROOT, 'HEAD')

    def test_history_and_uncommitted_source_not_copied(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            subprocess.run(['git', 'init', '-q', str(root)], check=True)
            subprocess.run(['git', '-C', str(root), 'config', 'user.name', 'Test'], check=True)
            subprocess.run(['git', '-C', str(root), 'config', 'user.email', 'test@example.invalid'], check=True)
            (root/'gap').mkdir()
            (root/'gap/runtime.g').write_text('accepted')
            subprocess.run(['git', '-C', str(root), 'add', '.'], check=True)
            subprocess.run(['git', '-C', str(root), 'commit', '-qm', 'accepted'], check=True)
            (root/'gap/runtime.g').write_text('uncommitted')
            (root/'private.pem').write_text('not tracked')
            _, files, _ = pub.read_commit(root, 'HEAD')
            self.assertEqual(files, {'gap/runtime.g': b'accepted'})

    def test_credential_scan_rejects_without_printing_value(self):
        secret = b'ghp_' + b'A'*36
        with self.assertRaises(ValueError) as failure:
            pub.scan_credentials({'config': secret})
        self.assertNotIn(secret.decode(), str(failure.exception))
        self.assertIn('config', str(failure.exception))

    def test_existing_output_requires_explicit_update(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(SystemExit):
                pub.main(['--source', str(ROOT), '--output', directory])
            self.assertEqual(list(Path(directory).iterdir()), [])

    def test_source_output_overlap_rejected(self):
        with self.assertRaises(SystemExit):
            pub.main(['--source', str(ROOT), '--output', str(ROOT/'runs/public')])

    def test_validate_before_output_creation(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory)/'public'
            with mock.patch.object(pub, 'build', side_effect=ValueError('bad source')):
                with self.assertRaises(ValueError):
                    pub.main(['--source', str(ROOT), '--output', str(output)])
            self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
