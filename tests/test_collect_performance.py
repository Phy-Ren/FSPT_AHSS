"""Resource summaries must preserve clocks, coverage and provenance boundaries."""
import hashlib
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1]/'scripts'))


SPEC = importlib.util.spec_from_file_location('collect_performance',
    Path(__file__).resolve().parents[1]/'scripts/collect_performance.py')
MOD = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(MOD)


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


def metrics(rss, wall='0:03.25'):
    return ('User time (seconds): 2.5\nSystem time (seconds): 0.25\n'
            'Elapsed (wall clock) time (h:mm:ss or m:ss): %s\n'
            'Maximum resident set size (kbytes): %d\nExit status: 0\n') % (wall, rss)


class PerformanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        self.run, self.tasks = self.root/'campaign', self.root/'tasks'
        self.hashes = {'gap/run_one.g': 'a'*64}
        self.source = hashlib.sha256(json.dumps(self.hashes, sort_keys=True).encode()).hexdigest()
        manifest = dict(mode='full', prepared_only=False, groups=[1, 2],
                        source_id=self.source, source_sha256=self.hashes, tasks=[])
        for sg in [1, 2]:
            task = dict(id='task%d' % sg, space_group=sg, command=['gap', str(sg)],
                        queue='queue%d' % sg, created=1000)
            manifest['tasks'].append(task)
            # Deliberately incomparable node clocks; observer still gives 20s.
            status = dict(task, hostname='n%d' % sg, pbs_job='job%d' % sg,
                          status='done', exit_code=0, elapsed_s=4, started=sg*10000,
                          finished=sg*10000+4)
            save(self.tasks/task['id']/'status.json', status)
            (self.tasks/task['id']/'metrics.txt').write_text(metrics(sg*1024))
            checkpoint = dict(space_group=sg, status='computed', source_id=self.source, cpu_ms=sg*1000)
            save(self.run/'classification'/('sg%d.json' % sg), checkpoint)
            result = dict(checkpoint, source_sha256=self.hashes, mode='full', total_cpu_ms=sg*1000+500,
                          wall_seconds=sg+1, stage_timings=[dict(stage='classification_end', cpu_ms=sg*1000),
                                                            dict(stage='stack_lift_C1', cpu_ms=sg*1000+100)])
            save(self.run/('sg%d.json' % sg), result)
        save(self.run/'campaign.json', manifest)
        save(self.run/'observation.json', dict(source_id=self.source, submitted_at=1000,
             observed_complete=True, errors=[], polling_interval_seconds=10, observer_restarts=[],
             history=[dict(observed_at=1010, elapsed_seconds=10, classification_checkpoints=2, full_results=1),
                      dict(observed_at=1020, elapsed_seconds=20, classification_checkpoints=2, full_results=2)]))

    def test_separate_clocks_cpu_and_peak_memory(self):
        d = MOD.collect(self.run, self.tasks)
        self.assertTrue(d['complete'])
        self.assertEqual(d['observer']['classification_elapsed_seconds'], 10)
        self.assertEqual(d['observer']['full_elapsed_seconds'], 20)
        self.assertEqual(d['totals']['gap_total_cpu_seconds'], 4)
        self.assertEqual(d['totals']['gap_classification_cpu_seconds'], 3)
        self.assertEqual(d['totals']['gap_post_classification_cpu_seconds'], 1)
        self.assertEqual(d['totals']['process_cpu_seconds'], 5.5)
        self.assertEqual(d['max_single_task_rss']['maximum_resident_set_size_kib'], 2048)
        self.assertEqual(d['nodes']['n1']['tasks'], 1)
        self.assertEqual(d['nodes']['n2']['gap_total_cpu_seconds'], 2.5)
        self.assertEqual(d['slowest']['result_wall_seconds'][0]['space_group'], 2)
        self.assertEqual(d['group_measurements'][0]['stage_intervals'][-1]['cpu_seconds'], .4)

    def test_missing_metrics_refused_or_explicit_partial(self):
        (self.tasks/'task2/metrics.txt').unlink()
        with self.assertRaises(MOD.ReportError):
            MOD.collect(self.run, self.tasks)
        d = MOD.collect(self.run, self.tasks, allow_partial=True)
        self.assertFalse(d['complete'])
        self.assertEqual(d['missing']['metrics'], [2])
        self.assertEqual(d['totals']['metrics_records'], 1)
        self.assertEqual(d['totals']['process_cpu_seconds'], 2.75)

    def test_source_conflicts_remain_fatal_in_partial_mode(self):
        path = self.run/'sg2.json'
        d = json.loads(path.read_text()); d['source_id'] = 'other'; save(path, d)
        with self.assertRaisesRegex(MOD.ReportError, 'mixed source'):
            MOD.collect(self.run, self.tasks, allow_partial=True)

    def test_unfinished_campaign_lists_coverage(self):
        (self.run/'sg2.json').unlink()
        path = self.tasks/'task2/status.json'
        d = json.loads(path.read_text()); d['status'] = 'running'; d.pop('exit_code'); save(path, d)
        (self.tasks/'task2/metrics.txt').write_text('')
        path = self.run/'observation.json'
        d = json.loads(path.read_text()); d['observed_complete'] = False; d['history'].pop(); save(path, d)
        report = MOD.collect(self.run, self.tasks, allow_partial=True)
        self.assertEqual(report['missing']['results'], [2])
        self.assertEqual(report['totals']['classification_cpu_records'], 2)
        self.assertEqual(report['totals']['full_cpu_records'], 1)
        self.assertIsNone(report['observer']['full_elapsed_seconds'])
        self.assertEqual(report['observer']['classification_elapsed_seconds'], 10)

    def test_gnu_elapsed_hours_and_missing_field(self):
        d = MOD.parse_metrics(metrics(2048, '1:02:03.45').encode())
        self.assertAlmostEqual(d['wall_seconds'], 3723.45)
        self.assertIsNone(MOD.parse_metrics(b'User time (seconds): 1\n'))

    def test_observer_count_regressions_are_fatal_even_for_partial_reports(self):
        path = self.run/'observation.json'
        original = json.loads(path.read_text())
        for field in ('classification_checkpoints', 'full_results'):
            with self.subTest(field=field):
                data = json.loads(json.dumps(original))
                data['history'].append(dict(observed_at=1030, elapsed_seconds=30,
                                           classification_checkpoints=2, full_results=2))
                data['history'][-1][field] = 1
                save(path, data)
                with self.assertRaisesRegex(MOD.ReportError, 'observer count decreased'):
                    MOD.collect(self.run, self.tasks, allow_partial=True)

    def test_observer_cannot_finish_before_classification_or_without_final_count(self):
        path = self.run/'observation.json'
        data = json.loads(path.read_text())
        data['history'][0]['classification_checkpoints'] = 0
        save(path, data)
        with self.assertRaisesRegex(MOD.ReportError, 'precede their classification'):
            MOD.collect(self.run, self.tasks, allow_partial=True)
        data['history'][0]['classification_checkpoints'] = 2
        data['history'].pop()
        save(path, data)
        with self.assertRaisesRegex(MOD.ReportError, 'without final full count'):
            MOD.collect(self.run, self.tasks, allow_partial=True)

    def test_stage_intervals_partition_runtime_and_reject_bad_clocks(self):
        path = self.run/'sg1.json'
        data = json.loads(path.read_text())
        stages = MOD.stage_intervals(data)
        self.assertAlmostEqual(sum(x['cpu_seconds'] for x in stages), data['total_cpu_ms']/1000)
        for bad_time in (900, 1600):
            with self.subTest(cpu_ms=bad_time):
                data['stage_timings'][1]['cpu_ms'] = bad_time
                save(path, data)
                with self.assertRaisesRegex(MOD.ReportError, 'nonmonotone stage timings'):
                    MOD.collect(self.run, self.tasks, allow_partial=True)

    def test_no_memory_measurements_remain_missing_not_zero(self):
        for sg in (1, 2):
            (self.tasks/('task%d' % sg)/'metrics.txt').unlink()
        data = MOD.collect(self.run, self.tasks, allow_partial=True)
        self.assertEqual(data['totals']['metrics_records'], 0)
        self.assertEqual(data['missing']['metrics'], [1, 2])
        self.assertIsNone(data['max_single_task_rss'])


if __name__ == '__main__':
    unittest.main()
