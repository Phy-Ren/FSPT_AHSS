"""Only local disposable worker/sleeper processes; no cluster access or GAP."""
import copy
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import tempfile
import time
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT/'scripts'))
import deadline_guard as guard


def wait_for(callback, timeout=15):
    until = time.monotonic()+timeout
    while time.monotonic() < until:
        try:
            result = callback()
            if result:
                return result
        except (FileNotFoundError, json.JSONDecodeError):
            pass
        time.sleep(.03)
    raise AssertionError('local toy process did not reach expected condition')


class DeadlineGuardUnitTests(unittest.TestCase):
    def test_old_kernel_zombie_without_exit_raw(self):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)
            (path/'metrics.txt').write_text('Exit status: 0\n')
            with patch.object(guard, 'same_process', return_value=dict(state='Z', exit_raw=None)):
                result = guard.exit_evidence({}, time.time()-1, time.time()+3, path)
            self.assertIsNone(result['exit_code'])
            self.assertFalse(result['kernel_waitstatus_available'])
            self.assertEqual(result['metrics']['exit_status'], 0)
            self.assertTrue(result['original_worker_reaped_exit_code_required_for_acceptance'])

    def test_monotonic_deadline_survives_wallclock_rollback(self):
        with tempfile.TemporaryDirectory() as directory:
            with patch.object(guard, 'same_process', return_value=dict(state='Z', exit_raw=0)):
                result = guard.exit_evidence({}, time.time()-1, time.time()+500,
                                             Path(directory), monotonic_deadline=time.monotonic()-1)
            self.assertFalse(result['completion_observed_before_deadline'])

    def test_resume_not_blocked_by_ledger_io_failure(self):
        identity = dict(state='T')
        with patch.object(guard, 'event', side_effect=OSError('disk full')):
            with patch.object(guard, 'same_process', side_effect=[identity, dict(state='S')]):
                with patch.object(guard, 'checked_signal') as send:
                    self.assertTrue(guard.resume_worker(dict(worker={}), Path('/unused'), 'guard', 'test'))
        send.assert_called_once_with({}, signal.SIGCONT)

    def test_resume_signals_before_any_ledger_io(self):
        calls = []
        with patch.object(guard, 'event', side_effect=lambda *a, **kw:calls.append('log')):
            with patch.object(guard, 'same_process', side_effect=[dict(state='T'), dict(state='S')]):
                with patch.object(guard, 'checked_signal', side_effect=lambda *a, **kw:calls.append('signal')):
                    self.assertTrue(guard.resume_worker(dict(worker={}), Path('/unused'), 'guard', 'test'))
        self.assertEqual(calls[0], 'signal')

    def test_identity_mismatch_prevents_signal(self):
        identity = guard.process_identity(os.getpid())
        identity['start_ticks'] += 1
        with patch.object(guard.os, 'kill') as send:
            with self.assertRaises(guard.GuardError):
                guard.checked_signal(identity, signal.SIGSTOP)
        send.assert_not_called()

    def test_old_kernel_children_ps_fallback(self):
        with patch.object(Path, 'read_text', side_effect=FileNotFoundError):
            with patch.object(guard.subprocess, 'run', return_value=subprocess.CompletedProcess(
                    [], 0, stdout=b' 101\n 102\n', stderr=b'')) as execute:
                self.assertEqual(guard.direct_children(42), {101, 102})
        self.assertEqual(execute.call_args[0][0], ['ps', '-o', 'pid=', '--ppid', '42'])


@unittest.skipUnless(sys.platform.startswith('linux') and shutil.which('/usr/bin/time'),
                     'Linux /proc and GNU time required')
class DeadlineGuardToyWorkerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='fspt-guard-toy-')
        self.root = Path(self.temp.name)
        (self.root/'scripts').mkdir()
        shutil.copyfile(ROOT/'scripts/worker.py', self.root/'scripts/worker.py')
        self.queue = self.root/'runs/queue'
        for name in ('pending', 'running', 'done'):
            (self.queue/name).mkdir(parents=True)
        self.env = dict(os.environ, PBS_JOBID='LOCAL_TOY_GUARD_TEST')
        self.log = (self.root/'worker.txt').open('wb')
        self.worker = subprocess.Popen([sys.executable, str(self.root/'scripts/worker.py'),
                                       '--root', str(self.root), '--workers', '4'],
                                      cwd=self.root, env=self.env, stdout=self.log,
                                      stderr=subprocess.STDOUT, start_new_session=True)
        wait_for(lambda: (self.queue/'worker.json').exists())

    def tearDown(self):
        # Only this test's explicitly recorded child groups, never arbitrary PIDs.
        try:
            os.kill(self.worker.pid, signal.SIGCONT)
        except ProcessLookupError:
            pass
        for path in (self.root/'runs/tasks').glob('*/status.json'):
            value = guard.read_json(path)
            try:
                identity = guard.process_identity(value['pid'])
                if identity['pgid'] == identity['pid'] == identity['sid'] and identity['ppid'] == self.worker.pid:
                    os.killpg(identity['pgid'], signal.SIGKILL)
            except (FileNotFoundError, ProcessLookupError):
                pass
        for path in self.root.glob('ledger/watchdog.json'):
            identity = guard.read_json(path)['identity']
            try:
                if guard.same_process(identity)['state'] != 'Z':
                    os.kill(identity['pid'], signal.SIGTERM)
            except (FileNotFoundError, ProcessLookupError):
                pass
        try:
            self.worker.terminate()
            self.worker.wait(timeout=4)
        except subprocess.TimeoutExpired:
            self.worker.kill()
            self.worker.wait()
        self.log.close()
        self.temp.cleanup()

    def submit(self, ident, command, timeout):
        value = dict(command=command, cwd=str(self.root), timeout_s=timeout, created=time.time())
        guard.atomic_json(self.queue/'pending'/(ident+'.json'), value)

    def status(self, ident):
        return guard.read_json(self.root/'runs/tasks'/ident/'status.json')

    def prepare(self, sleep_s=7, original_timeout=4, extension_after_start=12, two_tasks=False):
        self.submit('sleeper', [sys.executable, '-c', 'import time; time.sleep(%s)' % sleep_s], original_timeout)
        if two_tasks:
            self.submit('sleeper2', [sys.executable, '-c', 'import time; time.sleep(8)'], 5)
        status = wait_for(lambda: self.status('sleeper'))
        deadlines = {'sleeper':status['started']+extension_after_start}
        if two_tasks:
            second = wait_for(lambda: self.status('sleeper2'))
            deadlines['sleeper2'] = second['started']+extension_after_start
        with patch.dict(os.environ, self.env):
            plan = guard.make_plan(self.root, 'queue', deadlines,
                                   time.time()+60, 'explicit local toy test', cleanup_margin_s=5)
            guard.validate_plan(plan)
        self.plan = self.root/'plan.json'
        guard.atomic_json(self.plan, plan)
        self.ledger = self.root/'ledger'
        return plan

    def launch_guard(self):
        self.submit('guard', [sys.executable, str(ROOT/'scripts/deadline_guard.py'), 'run',
                             '--plan', str(self.plan), '--ledger', str(self.ledger),
                             '--poll-s', '.05', '--watchdog-stale-s', '.5'], 50)
        wait_for(lambda: (self.ledger/'events.guard.jsonl').exists() and
                 '"event": "suspended"' in (self.ledger/'events.guard.jsonl').read_text())
        self.assertIn(guard.process_identity(self.worker.pid)['state'], ('T', 't'))

    def test_success_preserves_worker_timeout_and_raw_evidence(self):
        plan = self.prepare(two_tasks=True)
        self.launch_guard()
        wait_for(lambda: (self.ledger/'summary.json').exists(), timeout=15)
        status = wait_for(lambda: (s if (s:=self.status('sleeper'))['status'] != 'running' else None))
        self.assertEqual((status['status'], status['exit_code']), ('timeout', 0))
        result = guard.read_json(self.ledger/'summary.json')
        self.assertIsNone(result['guard_error'])
        self.assertTrue(result['worker_resumed'])
        self.assertTrue(result['watchdog_finished'])
        self.assertEqual(result['watchdog_exit_code'], 0)
        task = result['tasks']['sleeper']
        self.assertEqual(task['exit_code'], 0)
        self.assertEqual(task['metrics']['exit_status'], 0)
        self.assertTrue(task['completion_observed_before_deadline'])
        self.assertFalse(task['termination_signal_sent'])
        self.assertLessEqual(task['last_alive_at'], task['completion_observed_at'])
        self.assertLessEqual(task['completion_observed_at'], status['finished'])
        self.assertLess(task['completion_observed_at'], result['tasks']['sleeper2']['completion_observed_at'])
        self.assertGreater(status['finished']-task['completion_observed_at'], .4)
        before = (self.ledger/'before/sleeper.status.json').read_bytes()
        self.assertEqual(guard.sha(before), plan['tasks'][0]['status_sha256'])
        self.assertEqual(json.loads(before)['status'], 'running')
        self.assertEqual((self.ledger/'tool/deadline_guard.py').read_bytes(), (ROOT/'scripts/deadline_guard.py').read_bytes())

    def test_guard_death_watchdog_resumes_worker(self):
        plan = self.prepare(sleep_s=20, extension_after_start=15)
        self.launch_guard()
        wait_for(lambda: time.time() > plan['tasks'][0]['deadline']-15+4.2)
        identity = guard.read_json(self.ledger/'preflight.json')['guard']
        guard.checked_signal(identity, signal.SIGKILL)
        wait_for(lambda: guard.process_identity(self.worker.pid)['state'] not in ('T', 't'))
        status = wait_for(lambda: (s if (s:=self.status('sleeper'))['status'] != 'running' else None))
        self.assertEqual(status['status'], 'timeout')
        self.assertNotEqual(status['exit_code'], 0)
        events = (self.ledger/'events.watchdog.jsonl').read_text()
        self.assertIn('"event": "resumed"', events)

    def test_extended_deadline_kills_only_toy_task_group(self):
        self.prepare(sleep_s=20, extension_after_start=6)
        self.launch_guard()
        wait_for(lambda: (self.ledger/'summary.json').exists())
        value = guard.read_json(self.ledger/'summary.json')
        self.assertTrue(value['tasks']['sleeper']['termination_signal_sent'])
        self.assertTrue(value['worker_resumed'])
        self.assertFalse(value['tasks']['sleeper']['completion_observed_before_deadline'])
        self.assertIsNone(self.worker.poll())

    def test_rejects_unplanned_task_and_wrong_pbs_without_signals(self):
        plan = self.prepare(sleep_s=20, original_timeout=15, extension_after_start=20)
        wrong = copy.deepcopy(plan)
        wrong['pbs_job'] = 'another-allocation'
        with patch.dict(os.environ, self.env), patch.object(guard, 'checked_signal') as send:
            with self.assertRaises(guard.GuardError):
                guard.validate_plan(wrong)
        send.assert_not_called()
        self.submit('unplanned', [sys.executable, '-c', 'import time; time.sleep(20)'], 15)
        wait_for(lambda: self.status('unplanned'))
        with patch.dict(os.environ, self.env), patch.object(guard, 'checked_signal') as send:
            with self.assertRaises(guard.GuardError):
                guard.validate_plan(plan)
        send.assert_not_called()
        self.assertFalse((self.root/'ledger').exists())

    def test_missing_legacy_queue_field_is_bound_by_parent_and_running_path(self):
        plan = self.prepare(sleep_s=20, original_timeout=15, extension_after_start=20)
        path = self.root/'runs/tasks/sleeper/status.json'
        status = guard.read_json(path)
        del status['queue']
        guard.atomic_json(path, status)
        plan['tasks'][0]['status_sha256'] = guard.sha(path.read_bytes())
        with patch.dict(os.environ, self.env):
            self.assertIn('sleeper', guard.validate_plan(plan)['records'])


if __name__ == '__main__':
    unittest.main()
