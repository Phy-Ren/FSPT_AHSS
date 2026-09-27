"""The public stacking CLI must reject noninjective Smith coordinates."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]


class StackResultCliTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.path = Path(self.tmp.name)/'sg1.json'
        hashes = {'gap/run_one.g': 'a'*64}
        self.result = dict(space_group=1, convention='physical-spin-half-det-sign-omega0',
            status='computed', sptset_loaded=False, classification_status='computed',
            pip=dict(status='computed', orders=[], free_rank=0), majorana=[], complex_fermion=[], bosonic=[2],
            source_sha256=hashes,
            source_id=hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest(),
            stacking=dict(status='computed', freePipRank=0, invariants=[2],
                lower=dict(generators=[dict(name='D1')], presentation=[[2]],
                    smithRowTransform=[[1]], smithColumnTransform=[[1]], smithDiagonal=[2],
                    invariants=[2], enumeratedPhaseProducts=0)))

    def run_cli(self, optimized=False):
        self.path.write_text(json.dumps(self.result))
        command = [sys.executable] + (['-O'] if optimized else []) + [str(ROOT/'scripts/stack_result.py'),
                   str(self.path), '--left', '{"D1":1}', '--right', '{"D1":1}']
        return subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def test_valid_certificate_replays(self):
        result = self.run_cli()
        self.assertEqual(result.returncode, 0, result.stderr)
        value = json.loads(result.stdout)
        self.assertEqual(value['left_order'], 2)
        self.assertEqual(value['stacked'], [0])
        self.assertEqual(value['stacked_marked'], {})

    def test_noninjective_smith_transform_rejected(self):
        self.result['stacking']['lower']['smithColumnTransform'] = [[0]]
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('non-unimodular Smith transformation', result.stderr)
        self.assertEqual(result.stdout, '')

    def test_false_smith_identity_with_unimodular_transform_rejected(self):
        self.result['stacking']['lower']['presentation'] = [[4]]
        result = self.run_cli()
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('Smith matrix identity failed', result.stderr)

    def test_python_optimized_mode_refused(self):
        result = self.run_cli(optimized=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('without -O or PYTHONOPTIMIZE', result.stderr)


if __name__ == '__main__':
    unittest.main()
