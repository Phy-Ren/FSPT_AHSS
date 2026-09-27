"""Uncertainty remains explicit in completed computational archives."""
import hashlib
import json
import sys
from pathlib import Path
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))
from background_performance import collect_background_performance
from archive_background_campaign import archive
import test_collect_performance as baseline
save = baseline.save


class BackgroundPerformanceTests(unittest.TestCase):
    def setUp(self):
        baseline.PerformanceTests.setUp(self)
        self.audits = {n: dict(full_group=True, kind='exact-test') for n in (1, 2)}
        p = self.run/'observation.json'
        obs = json.loads(p.read_text()); obs['observed_campaign_seconds'] = 20
        save(p, obs)

    def test_observer_clock_and_single_task_rss(self):
        result = collect_background_performance(self.run, self.tasks, self.audits)
        self.assertTrue(result['complete'])
        self.assertEqual(result['observer']['full_elapsed_seconds'], 20)
        self.assertEqual(result['totals']['gap_total_cpu_seconds'], 4)
        self.assertEqual(result['max_single_task_rss']['maximum_resident_set_size_kib'], 2048)

    def test_complete_finite_family_is_not_relabelled_unique(self):
        p = self.run/'sg2.json'
        data = json.loads(p.read_text()); data['status'] = 'unresolved'; save(p, data)
        original = p.read_bytes()
        self.audits[2] = dict(full_group=False, kind='unresolved-upper-extension-family')
        pobs = self.run/'observation.json'
        obs = json.loads(pobs.read_text()); obs.update(errors=[2], observed_complete=False); save(pobs, obs)
        result = collect_background_performance(self.run, self.tasks, self.audits)
        self.assertTrue(result['complete'])
        self.assertEqual(result['unique_full_groups'], 1)
        self.assertEqual(result['unresolved_upper_families'], [2])
        self.assertEqual(p.read_bytes(), original)

    def test_uncertified_unresolved_result_is_rejected(self):
        p = self.run/'sg2.json'
        data = json.loads(p.read_text()); data['status'] = 'unresolved'; save(p, data)
        with self.assertRaisesRegex(ValueError, 'contradicts audit'):
            collect_background_performance(self.run, self.tasks, self.audits)

    def test_task_queue_provenance_cannot_change(self):
        p = self.tasks/'task2/status.json'
        data = json.loads(p.read_text()); data['queue'] = 'other'; save(p, data)
        with self.assertRaisesRegex(ValueError, 'provenance mismatch'):
            collect_background_performance(self.run, self.tasks, self.audits)

    def test_partial_archive_refuses_before_creating_destination(self):
        output = self.root/'accepted'
        with self.assertRaisesRegex(ValueError, 'all 230'):
            archive(self.run, self.root/'source', self.tasks, output)
        self.assertFalse(output.exists())


if __name__ == '__main__':
    unittest.main()
