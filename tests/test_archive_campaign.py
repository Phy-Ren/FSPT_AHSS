"""Campaign archives preserve bytes and reject incomplete or mixed evidence."""
import hashlib
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
import archive_campaign as module


def save(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data))


class ArchiveCampaignTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.run, self.source, self.tasks, self.output = (self.root/name for name in
            ('run', 'frozen_source', 'tasks', 'new_parent/archive'))
        (self.source/'gap').mkdir(parents=True)
        (self.source/'gap/run_one.g').write_bytes(b'# test-only frozen source\r\n')
        hashes = {'gap/run_one.g': hashlib.sha256((self.source/'gap/run_one.g').read_bytes()).hexdigest()}
        self.source_id = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
        campaign = dict(mode='full', prepared_only=False, groups=list(range(1, 231)),
                        source_id=self.source_id, source_sha256=hashes, tasks=[])
        for number in range(1, 231):
            task = dict(id='task%d' % number, space_group=number, command=['gap', str(number)],
                        queue='test_queue', created=1000)
            campaign['tasks'].append(task)
            checkpoint = dict(space_group=number, status='computed', source_id=self.source_id,
                convention='physical-spin-half-det-sign-omega0', formula_convention=module.FORMULA_CONVENTION,
                source_snapshot='/original/absolute/source', sptset_loaded=False, cpu_ms=1000,
                pip=dict(status='computed', orders=[], free_rank=0), majorana=[], complex_fermion=[], bosonic=[])
            save(self.run/'classification'/('sg%d.json' % number), checkpoint)
            result = dict(checkpoint, source_sha256=hashes, mode='full', total_cpu_ms=1500,
                wall_seconds=3.25, stage_timings=[dict(stage='classification_end', cpu_ms=1000)],
                stacking=dict(status='computed', invariants=[], lower=dict(invariants=[], presentation=[],
                    smithRowTransform=[], smithColumnTransform=[], smithDiagonal=[], enumeratedPhaseProducts=0)))
            save(self.run/('sg%d.json' % number), result)
            save(self.tasks/task['id']/'status.json', dict(task, hostname='test-node', pbs_job='test-job',
                 status='done', exit_code=0, elapsed_s=3.25, started=1000, finished=1003.25))
            (self.tasks/task['id']/'metrics.txt').write_bytes(
                b'User time (seconds): 2.5\nSystem time (seconds): 0.25\n'
                b'Elapsed (wall clock) time (h:mm:ss or m:ss): 0:03.25\n'
                b'Maximum resident set size (kbytes): 1024\nExit status: 0\n')
            (self.tasks/task['id']/'stdout.log').write_bytes(b'progress\rcompleted\r\n')
        save(self.run/'campaign.json', campaign)
        save(self.run/'observation.json', dict(source_id=self.source_id, submitted_at=1000,
            observed_complete=True, errors=[], polling_interval_seconds=10,
            history=[dict(observed_at=1010, elapsed_seconds=10, classification_checkpoints=230, full_results=229),
                     dict(observed_at=1020, elapsed_seconds=20, classification_checkpoints=230, full_results=230)]))
        (self.run/'sg1.raw.json').write_bytes(b'do not archive raw duplicate')
        (self.run/'sg1.g').write_bytes(b'do not archive generated driver')

    def call(self):
        return module.archive(self.run, self.source, self.tasks, self.output)

    def input_hashes(self):
        return {str(p): hashlib.sha256(p.read_bytes()).hexdigest()
                for root in (self.run, self.source, self.tasks) for p in root.rglob('*') if p.is_file()}

    def test_success_preserves_original_bytes_and_generates_strict_performance(self):
        before = self.input_hashes()
        result = self.call()
        self.assertTrue(result['complete'])
        self.assertEqual(result['source_id'], self.source_id)
        self.assertEqual(self.input_hashes(), before)
        manifest = json.loads((self.output/'archive.json').read_text())
        for relative, entry in manifest['files'].items():
            payload = (self.output/relative).read_bytes()
            self.assertEqual(hashlib.sha256(payload).hexdigest(), entry['sha256'])
            if entry['original_path'] is not None:
                self.assertEqual(payload, Path(entry['original_path']).read_bytes())
        self.assertEqual((self.output/'tasks/task1/stdout.txt').read_bytes(), b'progress\rcompleted\r\n')
        self.assertFalse((self.output/'tasks/task1/stdout.log').exists())
        self.assertFalse((self.output/'sg1.raw.json').exists())
        self.assertFalse((self.output/'sg1.g').exists())
        self.assertEqual(json.loads((self.output/'sg1.json').read_text())['source_snapshot'], '/original/absolute/source')
        performance = json.loads((self.output/'performance.json').read_text())
        self.assertTrue(performance['complete'])
        self.assertEqual(performance['totals']['metrics_records'], 230)
        self.assertEqual(performance['observer']['full_elapsed_seconds'], 20)
        self.assertFalse(manifest['audit_scope']['reference_answers_read'])

    def test_partial_refused_before_creating_destination_or_parent(self):
        (self.run/'sg230.json').unlink()
        with self.assertRaisesRegex(ValueError, 'all 230 result files'):
            self.call()
        self.assertFalse(self.output.parent.exists())

    def test_existing_destination_is_never_modified(self):
        self.output.mkdir(parents=True)
        sentinel = self.output/'sentinel'
        sentinel.write_bytes(b'keep existing directory')
        with self.assertRaisesRegex(ValueError, 'destination already exists'):
            self.call()
        self.assertEqual(list(self.output.iterdir()), [sentinel])
        self.assertEqual(sentinel.read_bytes(), b'keep existing directory')

    def test_actual_frozen_source_extra_file_is_rejected(self):
        (self.source/'gap/extra.g').write_bytes(b'not in campaign source')
        with self.assertRaisesRegex(ValueError, 'actual frozen source files differ'):
            self.call()
        self.assertFalse(self.output.parent.exists())

    def test_missing_performance_evidence_refused_before_copying(self):
        (self.tasks/'task1/metrics.txt').write_bytes(b'incomplete metrics')
        with self.assertRaisesRegex(ValueError, 'incomplete campaign'):
            self.call()
        self.assertFalse(self.output.parent.exists())

    def test_current_formula_and_checkpoint_layer_agreement_are_required(self):
        path = self.run/'classification/sg1.json'
        original = json.loads(path.read_text())
        data = dict(original, formula_convention='obsolete')
        save(path, data)
        with self.assertRaisesRegex(ValueError, 'checkpoint formula convention differs'):
            self.call()
        data = dict(original, bosonic=[2])
        save(path, data)
        with self.assertRaisesRegex(ValueError, 'checkpoint/result bosonic mismatch'):
            self.call()
        self.assertFalse(self.output.parent.exists())

    def test_change_after_performance_collection_is_rejected(self):
        actual_collect = module.collect

        def changing_collect(*args, **kwargs):
            report = actual_collect(*args, **kwargs)
            path = self.tasks/'task1/stdout.log'
            path.write_bytes(path.read_bytes()+b'changed after snapshot')
            return report

        with patch.object(module, 'collect', side_effect=changing_collect):
            with self.assertRaisesRegex(ValueError, 'input changed during audit'):
                self.call()
        self.assertFalse(self.output.parent.exists())


if __name__ == '__main__':
    unittest.main(verbosity=2)
