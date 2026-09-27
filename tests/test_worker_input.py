"""Validate worker limits without launching any task or PBS process."""
import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('worker', ROOT/'scripts/worker.py')
WORKER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(WORKER)


class EndFirstIdleIteration(Exception):
    pass


class WorkerInputTests(unittest.TestCase):
    def test_invalid_slot_counts_rejected_before_creating_queue(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)/'unused'
            for count in (0, -1, 29):
                result = subprocess.run([sys.executable, str(ROOT/'scripts/worker.py'),
                    '--root', str(root), '--workers', str(count)],
                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
                self.assertEqual(result.returncode, 2)
                self.assertIn('--workers must be in 1..28', result.stderr)
                self.assertFalse(root.exists())

    def test_invalid_config_type_retains_validated_startup_count(self):
        for config in ({'workers': None}, [], {'workers': {}}):
            with self.subTest(config=config), tempfile.TemporaryDirectory() as directory:
                root = Path(directory)
                queue = root/'runs/queue'
                queue.mkdir(parents=True)
                (queue/'config.json').write_text(json.dumps(config))
                with patch.object(sys, 'argv', ['worker.py', '--root', str(root), '--workers', '7']), \
                     patch.object(WORKER.signal, 'signal'), \
                     patch.object(WORKER.time, 'sleep', side_effect=EndFirstIdleIteration):
                    with self.assertRaises(EndFirstIdleIteration):
                        WORKER.main()
                state = json.loads((queue/'worker.json').read_text())
                self.assertEqual(state['slots'], 7)
                self.assertEqual(state['active'], [])


if __name__ == '__main__':
    unittest.main()
