"""Task IDs must not overwrite provenance from a same-named earlier run."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import time
import unittest


ROOT = Path(__file__).resolve().parents[1]


class SubmitCampaignTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        (self.root/'scripts').mkdir()
        shutil.copy2(ROOT/'scripts/submit_campaign.py', self.root/'scripts/submit_campaign.py')
        (self.root/'gap').mkdir()
        (self.root/'gap/run_one.g').write_text('# A source fixture; GAP is never launched.\n')
        queue = self.root/'runs/new_queue'
        queue.mkdir(parents=True)
        (queue/'worker.json').write_text(json.dumps(dict(heartbeat=time.time(), slots=1)))
        self.output = self.root/'runs/new_parent/reused_name'

    def submit(self, *extra):
        return subprocess.run([sys.executable, str(self.root/'scripts/submit_campaign.py'),
            '--run', str(self.output), '--queues', 'new_queue', '--groups', '1-2'] + list(extra),
            stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)

    def assert_no_queued_tasks(self):
        self.assertEqual(list((self.root/'runs/new_queue').glob('pending/*.json')), [])

    def test_same_basename_done_collision_rejects_entire_batch(self):
        # A previous run has the same basename under a different parent. Its
        # second task must be detected before even the first new task is queued.
        (self.root/'runs/old_parent/reused_name').mkdir(parents=True)
        previous = self.root/'runs/old_queue/done/reused_name-p001-sg002.json'
        previous.parent.mkdir(parents=True)
        previous.write_text('{"old":true}')
        result = self.submit()
        self.assertEqual(result.returncode, 2)
        self.assertIn('task IDs already used', result.stderr)
        self.assertIn(str(previous), result.stderr)
        self.assert_no_queued_tasks()
        self.assertEqual(previous.read_text(), '{"old":true}')

    def test_existing_task_output_directory_rejects_entire_batch(self):
        previous = self.root/'runs/tasks/reused_name-p001-sg002'
        previous.mkdir(parents=True)
        result = self.submit()
        self.assertEqual(result.returncode, 2)
        self.assertIn(str(previous), result.stderr)
        self.assert_no_queued_tasks()

    def test_valid_prepare_only_preserves_plan_without_queueing(self):
        result = self.submit('--prepare-only')
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((self.output/'campaign.json').read_text())
        self.assertEqual(manifest['groups'], [1, 2])
        self.assertEqual(len(manifest['tasks']), 2)
        self.assert_no_queued_tasks()


if __name__ == '__main__':
    unittest.main()
