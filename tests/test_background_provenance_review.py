"""Independent provenance negatives for the background archive collector."""
import json
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from background_performance import collect_background_performance
import test_background_performance as controls


class BackgroundProvenanceReviewTests(unittest.TestCase):
    def setUp(self):
        controls.BackgroundPerformanceTests.setUp(self)

    def change(self, path, update):
        data = json.loads(path.read_text())
        update(data)
        controls.save(path, data)

    def collect(self):
        return collect_background_performance(self.run, self.tasks, self.audits)

    def test_cross_node_clocks_are_not_subtracted(self):
        self.assertEqual(self.collect()['observer']['full_elapsed_seconds'], 20)

    def test_campaign_requires_full_submitted_mode(self):
        self.change(self.run/'campaign.json', lambda d: d.update(mode='classification'))
        with self.assertRaises(ValueError):
            self.collect()

    def test_source_manifest_hash_is_recomputed(self):
        changed = {'gap/run_one.g': 'b'*64}
        self.change(self.run/'campaign.json', lambda d: d.update(source_sha256=changed))
        for sg in (1, 2):
            self.change(self.run/('sg%d.json' % sg), lambda d: d.update(source_sha256=changed))
        with self.assertRaises(ValueError):
            self.collect()

    def test_optional_checkpoint_source_manifest_must_match(self):
        self.change(self.run/'classification/sg2.json',
                    lambda d: d.update(source_sha256={'gap/run_one.g': 'b'*64}))
        with self.assertRaises(ValueError):
            self.collect()

    def test_nonfinite_cpu_or_wall_is_rejected(self):
        path = self.run/'sg2.json'; original = path.read_bytes()
        for field in ('total_cpu_ms', 'wall_seconds'):
            with self.subTest(field=field):
                path.write_bytes(original)
                self.change(path, lambda d: d.update({field: float('inf')}))
                with self.assertRaises(ValueError):
                    self.collect()

    def test_fractional_observer_count_is_rejected(self):
        def change(d):
            d['history'][0]['classification_checkpoints'] = 1.5
        self.change(self.run/'observation.json', change)
        with self.assertRaises(ValueError):
            self.collect()

    def test_raw_timeout_exit_zero_is_not_plain_success(self):
        self.change(self.tasks/'task2/status.json', lambda d: d.update(status='timeout', exit_code=0))
        with self.assertRaises(ValueError):
            self.collect()

    def test_bad_observer_time_is_rejected(self):
        def change(d):
            d['history'][-1]['observed_at'] += 1
        self.change(self.run/'observation.json', change)
        with self.assertRaises(ValueError):
            self.collect()


if __name__ == '__main__':
    unittest.main()
