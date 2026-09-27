"""Fast saved-ledger controls; no signals, cluster access or GAP execution."""
import copy
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('deadline_evidence', ROOT/'scripts/deadline_evidence.py')
EVIDENCE = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(EVIDENCE)


class DeadlineEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.ledger = Path(self.temp.name)/'ledger'
        self.ident, self.project = 'sg219-test', '/toy/project'
        self.task = dict(id=self.ident, queue='queue', space_group=219,
                         command=['python3', '/toy/project/scripts/run_group.py', '219'],
                         cwd=self.project, timeout_s=5, created=999)
        self.before = dict(self.task, status='running', pid=101, started=1000,
                           hostname='toy-node', pbs_job='PBS_TEST')
        self.status = dict(self.before, status='timeout', exit_code=0, elapsed_s=8, finished=1008)
        worker = dict(pid=201, uid=1000, state='S', ppid=1, pgid=201, sid=201,
                      start_ticks=123, cmdline=['python3', self.project+'/scripts/worker.py',
                                               '--root', self.project, '--queue', 'queue'], exit_raw=0)
        child = dict(pid=101, uid=1000, state='S', ppid=201, pgid=101, sid=101,
                     start_ticks=200, cmdline=['/usr/bin/time', '-v', '-o',
                     self.project+'/runs/tasks/'+self.ident+'/metrics.txt']+self.task['command'], exit_raw=0)
        guard = dict(pid=301, uid=1000, state='R', ppid=401, pgid=401, sid=401,
                     start_ticks=300, cmdline=['python3', self.project+'/scripts/deadline_guard.py', 'run'], exit_raw=0)
        watchdog = dict(pid=501, uid=1000, state='R', ppid=301, pgid=501, sid=501,
                        start_ticks=400, cmdline=['python3', str(self.ledger/'tool/deadline_guard.py'),
                                                'watchdog', '--ledger', str(self.ledger)], exit_raw=0)
        self.save('before/'+self.ident+'.status.json', self.before)
        self.save('before/'+self.ident+'.running.json', self.task)
        self.save('before/worker.json', dict(pid=201, hostname='toy-node', pbs_job='PBS_TEST',
                                           active=[self.ident, 'guard-task'], started=900, heartbeat=1002))
        self.put('tool/deadline_guard.py', (ROOT/'scripts/deadline_guard.py').read_bytes())
        self.plan = dict(schema=1, root=self.project, queue='queue', hostname='toy-node',
                         pbs_job='PBS_TEST', created_at=1001, reason='Explicit test extension',
                         allocation_deadline=1050, cleanup_margin_s=5, worker=worker,
                         worker_script_sha256='a'*64, tasks=[dict(id=self.ident, identity=child,
                         deadline=1010, status_sha256=self.hash('before/'+self.ident+'.status.json'),
                         running_sha256=self.hash('before/'+self.ident+'.running.json'))])
        self.save('plan.json', self.plan)
        snapshots = []
        for relative in ('before/worker.json', 'before/'+self.ident+'.status.json',
                         'before/'+self.ident+'.running.json'):
            original = self.project+'/runs/queue/worker.json' if relative.endswith('worker.json') else (
                self.project+'/runs/tasks/'+self.ident+'/status.json' if '.status.' in relative else
                self.project+'/runs/queue/running/'+self.ident+'.json')
            snapshots.append(dict(original_path=original, archive_path=str(self.ledger/relative),
                                  sha256=self.hash(relative), bytes=len(self.raw(relative))))
        tool = dict(original_path=self.project+'/scripts/deadline_guard.py',
                    archive_path=str(self.ledger/'tool/deadline_guard.py'),
                    sha256=self.hash('tool/deadline_guard.py'), bytes=len(self.raw('tool/deadline_guard.py')))
        self.preflight = dict(schema=1, validated_at=1002, plan_sha256=self.hash('plan.json'),
                              tool_sha256=tool['sha256'], tool_evidence=tool, guard=guard,
                              worker=copy.deepcopy(worker), guard_task_id='guard-task', snapshots=snapshots,
                              guard_original_deadline=1020, kernel_waitstatus_available=True,
                              cutoff=1015, cutoff_monotonic=515, poll_s=.25, watchdog_stale_s=10,
                              original_deadlines={self.ident:1005})
        self.save('preflight.json', self.preflight)
        self.save('watchdog.json', dict(ready=True, identity=watchdog, observed_at=1002))
        self.save('guard_state.json', dict(heartbeat_monotonic=507.2, observed_at=1007.2,
                                           finished=True, worker_resumed=True))
        self.metrics = (b'User time (seconds): 1.0\nSystem time (seconds): 0.2\n'
                        b'Elapsed (wall clock) time (h:mm:ss or m:ss): 0:07.00\n'
                        b'Maximum resident set size (kbytes): 2048\nExit status: 0\n')
        self.outcome = dict(id=self.ident, original_deadline=1005, extended_deadline=1010,
            completion_observed_at=1007, last_alive_at=1006.8, exit_time_interval=[1006.8, 1007],
            completion_observed_monotonic=507, last_alive_monotonic=506.8,
            completion_observed_before_deadline=True, termination_signal_sent=False,
            kernel_waitstatus_available=True, exit_raw=0, exit_code=0, terminating_signal=None,
            original_worker_reaped_exit_code_required_for_acceptance=True,
            metrics=dict(path=self.project+'/runs/tasks/'+self.ident+'/metrics.txt',
                         sha256=EVIDENCE.digest(self.metrics), bytes=len(self.metrics), exit_status=0))
        self.summary = dict(schema=1, plan_sha256=self.hash('plan.json'), guard_error=None,
                            worker_resumed=True, tasks={self.ident:self.outcome}, watchdog_pid=501,
                            watchdog_exit_code=0, watchdog_finished=True, completed_at=1007.5,
                            original_status_files_modified=False, acceptance='not-determined-by-scheduling-tool')
        self.guard_events = [self.event('suspend_intent', 1002.05, 301, worker=worker, watchdog=watchdog),
                             self.event('suspended', 1002.1, 301),
                             self.event('task_exit_observed', 1007.01, 301, **self.outcome),
                             self.event('resume_signal_sent', 1007.1, 301, requested_at=1007.08, reason='normal completion'),
                             self.event('resumed', 1007.15, 301, state='S')]
        self.watchdog_events = [self.event('watchdog_ready', 1002, 501),
                                self.event('resume_signal_sent', 1007.3, 501, requested_at=1007.29,
                                           reason='guard finished with worker resumed'),
                                self.event('resumed', 1007.35, 501, state='S')]
        self.flush_outcome()

    def raw(self, name):
        return (self.ledger/name).read_bytes()

    def hash(self, name):
        return EVIDENCE.digest(self.raw(name))

    def put(self, name, payload):
        path = self.ledger/name
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(payload)

    def save(self, name, value):
        self.put(name, (json.dumps(value, sort_keys=True)+'\n').encode())

    def event(self, name, wall, pid, **values):
        return dict(event=name, observed_at=wall, monotonic=wall-500, pid=pid, **values)

    def save_events(self):
        for owner, values in (('guard', self.guard_events), ('watchdog', self.watchdog_events)):
            self.put('events.'+owner+'.jsonl', ''.join(json.dumps(x)+'\n' for x in values).encode())

    def flush_outcome(self):
        self.summary['tasks'][self.ident] = copy.deepcopy(self.outcome)
        self.guard_events[2] = self.event('task_exit_observed', 1007.01, 301, **self.outcome)
        self.save('summary.json', self.summary)
        self.save_events()

    def audit(self):
        return EVIDENCE.audit_extension(self.ledger, self.task, self.status, self.metrics, {})

    def test_honest_extension_preserves_original_timeout_and_all_input_bytes(self):
        before = {str(p):p.read_bytes() for p in self.ledger.rglob('*') if p.is_file()}
        original_status = copy.deepcopy(self.status)
        result = self.audit()
        self.assertEqual(result['effective_status'], 'done_with_audited_deadline_extension')
        self.assertEqual(result['original_worker_status'], 'timeout')
        self.assertAlmostEqual(result['task_wall_seconds_interval'][0], 6.8)
        self.assertEqual(result['task_wall_seconds_interval'][1], 7)
        self.assertEqual(self.status, original_status)
        self.assertEqual(before, {str(p):p.read_bytes() for p in self.ledger.rglob('*') if p.is_file()})

    def test_old_kernel_missing_waitstatus_still_requires_original_worker_success(self):
        self.outcome.update(exit_raw=None, exit_code=None, kernel_waitstatus_available=False)
        self.flush_outcome()
        self.assertFalse(self.audit()['kernel_waitstatus_available'])
        self.status['exit_code'] = -9
        with self.assertRaisesRegex(ValueError, 'original worker did not reap successful exit'):
            self.audit()

    def test_after_wall_or_monotonic_deadline_is_rejected_even_if_claimed_success(self):
        for clock in ('wall', 'monotonic'):
            with self.subTest(clock=clock):
                outcome = copy.deepcopy(self.outcome)
                if clock == 'wall':
                    self.outcome.update(completion_observed_at=1011, exit_time_interval=[1006.8, 1011])
                else:
                    self.outcome['completion_observed_monotonic'] = 511
                self.flush_outcome()
                with self.assertRaises(ValueError):
                    self.audit()
                self.outcome = outcome

    def test_signal_or_nonzero_exit_is_rejected(self):
        for change in ({'termination_signal_sent':True}, {'terminating_signal':9},
                       {'exit_raw':256, 'exit_code':1}):
            with self.subTest(change=change):
                original = copy.deepcopy(self.outcome)
                self.outcome.update(change)
                self.flush_outcome()
                with self.assertRaises(ValueError):
                    self.audit()
                self.outcome = original

    def test_missing_metrics_and_metrics_hash_change_are_rejected(self):
        self.outcome['metrics'] = None
        self.flush_outcome()
        with self.assertRaisesRegex(ValueError, 'GNU time'):
            self.audit()
        self.outcome['metrics'] = dict(sha256='0'*64, bytes=len(self.metrics), exit_status=0)
        self.flush_outcome()
        with self.assertRaisesRegex(ValueError, 'GNU time'):
            self.audit()

    def test_actual_metrics_nonzero_cannot_be_overridden_by_success_record(self):
        self.metrics = self.metrics.replace(b'Exit status: 0', b'Exit status: 1')
        self.outcome['metrics'].update(sha256=EVIDENCE.digest(self.metrics), bytes=len(self.metrics))
        self.flush_outcome()
        with self.assertRaises(ValueError):
            self.audit()

    def test_plan_hash_and_original_payload_tampering_are_rejected(self):
        self.plan['reason'] = 'modified declaration'
        self.save('plan.json', self.plan)
        with self.assertRaisesRegex(ValueError, 'plan hash mismatch'):
            self.audit()
        self.plan['reason'] = 'Explicit test extension'
        self.save('plan.json', self.plan)
        self.before['pid'] += 1
        self.save('before/'+self.ident+'.status.json', self.before)
        with self.assertRaisesRegex(ValueError, 'hash mismatch'):
            self.audit()

    def test_plan_process_identity_tampering_is_rejected_despite_consistent_plan_hashes(self):
        self.plan['worker']['start_ticks'] += 1
        self.save('plan.json', self.plan)
        self.preflight['plan_sha256'] = self.summary['plan_sha256'] = self.hash('plan.json')
        self.save('preflight.json', self.preflight)
        self.save('summary.json', self.summary)
        with self.assertRaisesRegex(ValueError, 'worker identity mismatch'):
            self.audit()

    def test_wrong_guard_or_watchdog_event_process_is_rejected(self):
        for events in (self.guard_events, self.watchdog_events):
            previous = events[0]['pid']
            events[0]['pid'] = 9999
            self.save_events()
            with self.assertRaises(ValueError):
                self.audit()
            events[0]['pid'] = previous

    def test_suspension_intent_must_bind_the_same_worker(self):
        self.guard_events[0]['worker'] = dict(self.plan['worker'], start_ticks=9999)
        self.save_events()
        with self.assertRaises(ValueError):
            self.audit()

    def test_index_records_hash_and_resolves_live_relative_ledger(self):
        run = Path(self.temp.name)/'campaign'
        run.mkdir()
        evidence = {}
        self.assertEqual(EVIDENCE.read_index(run, evidence), {})
        self.assertEqual(evidence, {})
        path = run/'deadline_extensions.json'
        path.write_text(json.dumps(dict(schema='fspt-deadline-extension-index-v1',
                                        tasks={self.ident:'../ledger'})))
        self.assertEqual(EVIDENCE.read_index(run, evidence), {self.ident:self.ledger})
        self.assertEqual(evidence[str(path)], EVIDENCE.digest(path.read_bytes()))

    def test_archived_relative_index_uses_original_run_as_its_base(self):
        archive = Path(self.temp.name)/'archive'
        archive.mkdir()
        original_run = Path('/original/runs/campaign')
        relative_ledger = '../guards/extension'
        original_plan = str((original_run/relative_ledger/'plan.json').resolve())
        (archive/'deadline_extensions.json').write_text(json.dumps(dict(
            schema='fspt-deadline-extension-index-v1', tasks={self.ident:relative_ledger})))
        (archive/'archive.json').write_text(json.dumps(dict(
            original_run=str(original_run), files={'deadline_ledgers/extension/plan.json':dict(
                original_path=original_plan, archive_path='deadline_ledgers/extension/plan.json')})))
        self.assertEqual(EVIDENCE.read_index(archive, {}),
                         {self.ident:archive/'deadline_ledgers/extension'})


if __name__ == '__main__':
    unittest.main()
