#!/usr/bin/env python3
"""Explicit, separately evidenced deadline extension for our PBS worker.

This is a scheduling tool, not an acceptance/collection tool. It never changes
worker code, task JSON, status JSON, numerical source, or results. ``check`` is
read-only. ``run`` must itself be submitted through the identified worker.

Plan schema 1: root, queue, hostname, pbs_job, created_at, reason,
allocation_deadline, cleanup_margin_s, worker (process_identity result), tasks
[{id, identity, status_sha256, running_sha256, deadline}]. All absolute times
are UNIX UTC seconds. Tasks must cover EVERY existing task on this worker;
the guard's own task is identified separately by its process group. No pending
tasks may remain. Plan preparation can use make_plan(), which is read-only.

A separate watchdog is armed before SIGSTOP of ONLY the worker PID. It sends
SIGCONT if the guard dies, misses heartbeats, or reaches the allocation cutoff.
Original worker outcomes (including timeout with exit_code=0) remain intact.
Polling records an exit-time interval, never a fabricated exact finish time.
Linux /proc and GNU time are required; Python 3.8 is supported. PID identity
checks reduce reuse risk but are not the atomic pidfd guarantee unavailable on
the cluster's older kernel. Simultaneous SIGKILL of guard and watchdog is not
recoverable by this tool; PBS walltime remains the final external bound.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import signal
import socket
import subprocess
import sys
import time


class GuardError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise GuardError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_bytes())


def atomic_json(path, value):
    path = Path(path)
    temp = path.with_name(path.name + '.tmp.%d' % os.getpid())
    with temp.open('x') as stream:
        json.dump(value, stream, sort_keys=True, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    os.replace(str(temp), str(path))


def event(ledger, owner, name, **fields):
    value = dict(event=name, observed_at=time.time(), monotonic=time.monotonic(),
                 pid=os.getpid(), **fields)
    with (Path(ledger)/('events.%s.jsonl' % owner)).open('a') as stream:
        stream.write(json.dumps(value, sort_keys=True) + '\n')
        stream.flush()
        os.fsync(stream.fileno())
    return value


def process_identity(pid):
    """Read only an explicitly identified process owned by this Unix user."""
    pid = int(pid)
    require(pid > 1, 'unsafe process ID')
    proc = Path('/proc')/str(pid)
    require(proc.stat().st_uid == os.getuid(), 'process is not owned by this user')
    raw = (proc/'stat').read_text()
    fields = raw[raw.rfind(')')+2:].split()
    cmdline = (proc/'cmdline').read_bytes().split(b'\0')
    return dict(pid=pid, uid=os.getuid(), state=fields[0], ppid=int(fields[1]),
                pgid=int(fields[2]), sid=int(fields[3]), start_ticks=int(fields[19]),
                cmdline=[os.fsdecode(x) for x in cmdline if x],
                exit_raw=int(fields[49]) if len(fields) > 49 else None)


def same_process(expected, allow_zombie=True):
    actual = process_identity(expected['pid'])
    for key in ('pid', 'uid', 'pgid', 'sid', 'start_ticks'):
        require(actual[key] == expected[key], 'process identity changed: %s' % key)
    if actual['state'] != 'Z' or not allow_zombie:
        require(actual['cmdline'] == expected['cmdline'], 'process command changed')
    return actual


def checked_signal(identity, sig, group=False):
    actual = same_process(identity, allow_zombie=False)
    require(actual['state'] != 'Z', 'refusing to signal a zombie')
    if group:
        require(actual['pgid'] == actual['pid'] == actual['sid'],
                'task is not its own process group/session leader')
        os.killpg(actual['pgid'], sig)
    else:
        os.kill(actual['pid'], sig)


def direct_children(pid):
    path = Path('/proc')/str(pid)/'task'/str(pid)/'children'
    try:
        values = {int(x) for x in path.read_text().split()}
        if values:
            return values
    except FileNotFoundError:
        pass
    # Older cluster kernels may not expose the proc children interface.
    result = subprocess.run(['ps', '-o', 'pid=', '--ppid', str(pid)],
                            stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    require(result.returncode in (0, 1), 'cannot inspect worker direct children')
    return {int(x) for x in result.stdout.split()}


def paths(plan):
    root = Path(plan['root']).resolve()
    queue = plan['queue']
    require(queue and Path(queue).name == queue, 'invalid queue name')
    return root, root/'runs'/queue


def safe_id(value):
    require(value and Path(value).name == value and value not in ('.', '..'),
            'invalid task ID')
    return value


def make_plan(root, queue, deadlines, allocation_deadline, reason,
              cleanup_margin_s=120):
    """Prepare a value for human review without writing files or signaling."""
    root = Path(root).resolve()
    worker = read_json(root/'runs'/queue/'worker.json')
    tasks = []
    for ident, deadline in sorted(deadlines.items()):
        safe_id(ident)
        status_path = root/'runs/tasks'/ident/'status.json'
        running_path = root/'runs'/queue/'running'/(ident+'.json')
        status = read_json(status_path)
        tasks.append(dict(id=ident, identity=process_identity(status['pid']),
                          status_sha256=sha(status_path.read_bytes()),
                          running_sha256=sha(running_path.read_bytes()), deadline=deadline))
    return dict(schema=1, root=str(root), queue=queue,
                hostname=worker['hostname'], pbs_job=worker['pbs_job'],
                created_at=time.time(), reason=reason,
                allocation_deadline=allocation_deadline,
                cleanup_margin_s=cleanup_margin_s,
                worker=process_identity(worker['pid']),
                worker_script_sha256=sha((root/'scripts/worker.py').read_bytes()),
                worker_script_hash_scope='current-on-disk-file-not-proof-of-running-interpreter-loaded-bytes',
                tasks=tasks)


def validate_plan(plan, own_group=None, require_predeadline=True, worker_may_be_stopped=False):
    require(plan.get('schema') == 1, 'unsupported plan schema')
    root, queue = paths(plan)
    now = time.time()
    require(plan.get('reason', '').strip(), 'extension reason is required')
    require(plan['hostname'] == socket.gethostname(), 'wrong host')
    require(plan['pbs_job'] and plan['pbs_job'] == os.environ.get('PBS_JOBID'),
            'wrong or missing PBS allocation identity')
    require(0 < plan['cleanup_margin_s'] < 3600, 'invalid cleanup margin')
    cutoff = plan['allocation_deadline'] - plan['cleanup_margin_s']
    require(now < cutoff, 'allocation cutoff has passed')
    require(plan['created_at'] <= now, 'plan comes from the future')
    worker_record = read_json(queue/'worker.json')
    require(worker_record['pid'] == plan['worker']['pid'], 'worker PID changed')
    require(worker_record['hostname'] == plan['hostname'] and
            worker_record['pbs_job'] == plan['pbs_job'], 'worker allocation mismatch')
    worker = same_process(plan['worker'], allow_zombie=False)
    require(worker['state'] != 'Z', 'worker has exited')
    require(worker_may_be_stopped or worker['state'] not in ('T', 't'),
            'worker was already stopped before this guard')
    require(sha((root/'scripts/worker.py').read_bytes()) == plan['worker_script_sha256'],
            'worker script changed')
    command = worker['cmdline']
    require('--root' in command and Path(command[command.index('--root')+1]).resolve() == root,
            'worker command points to another project')
    worker_queue = command[command.index('--queue')+1] if '--queue' in command else 'queue'
    require(worker_queue == plan['queue'], 'worker command points to another queue')
    cwd = Path(os.readlink('/proc/%d/cwd' % worker['pid']))
    require(any((cwd/part).resolve() == root/'scripts/worker.py' for part in command[1:]),
            'worker command is not the declared worker script')
    require(not list((queue/'pending').glob('*.json')), 'pending tasks must be empty')
    records = {}
    for entry in plan['tasks']:
        ident = safe_id(entry['id'])
        require(ident not in records, 'duplicate task ID')
        status_path = root/'runs/tasks'/ident/'status.json'
        running_path = queue/'running'/(ident+'.json')
        status_bytes, running_bytes = status_path.read_bytes(), running_path.read_bytes()
        require(sha(status_bytes) == entry['status_sha256'], 'task status changed: '+ident)
        require(sha(running_bytes) == entry['running_sha256'], 'running task changed: '+ident)
        status = json.loads(status_bytes)
        require(status['status'] == 'running' and status['id'] == ident, 'task is not running')
        require(status.get('queue', plan['queue']) == plan['queue'] and status['hostname'] == plan['hostname']
                and status['pbs_job'] == plan['pbs_job'], 'task allocation mismatch')
        require(status['pid'] == entry['identity']['pid'], 'task PID mismatch')
        actual = same_process(entry['identity'])
        require(actual['ppid'] == worker['pid'] and actual['pgid'] == actual['pid']
                and actual['sid'] == actual['pid'], 'task is not an isolated worker child')
        require(entry['identity']['cmdline'] == ['/usr/bin/time', '-v', '-o',
                str(root/'runs/tasks'/ident/'metrics.txt')] + status['command'],
                'task wrapper command differs from original task command')
        original_deadline = status['started'] + status['timeout_s']
        require(plan['created_at'] < original_deadline, 'plan declared after original deadline')
        if require_predeadline:
            require(now < original_deadline, 'original deadline has already passed: '+ident)
        require(original_deadline <= entry['deadline'] < cutoff,
                'extension must fit inside allocation cleanup cutoff')
        records[ident] = dict(entry=entry, status=status, identity=actual,
                              original_deadline=original_deadline)
    require(records, 'no tasks to supervise')
    running_ids = {p.stem for p in (queue/'running').glob('*.json')}
    extras = running_ids - records.keys()
    own_id = None
    own_deadline = None
    if own_group is not None:
        for ident in extras:
            status = read_json(root/'runs/tasks'/safe_id(ident)/'status.json')
            if status.get('pid') == own_group:
                require(own_id is None, 'multiple guard task identities')
                own_id = ident
                require(status.get('status') == 'running' and
                        status.get('pbs_job') == plan['pbs_job'] and
                        status.get('queue', plan['queue']) == plan['queue'] and
                        status.get('hostname') == plan['hostname'], 'guard task identity mismatch')
                own = process_identity(own_group)
                require(own['ppid'] == worker['pid'] and own['sid'] == own_group,
                        'guard is not a direct isolated worker task')
                require(status['started'] + status['timeout_s'] >=
                        max(x['deadline'] for x in plan['tasks'])+10,
                        'guard task original timeout does not cover supervision and cleanup')
                own_deadline = status['started'] + status['timeout_s']
        require(own_id is not None, 'run must itself be launched by this worker')
        extras.discard(own_id)
    require(not extras and set(records) <= running_ids, 'unplanned or missing active tasks')
    if own_group is not None:
        children = direct_children(worker['pid'])
        expected = {r['identity']['pid'] for r in records.values()} | {own_group}
        require(children == expected, 'worker child set differs from supervised task set')
    return dict(worker=worker, records=records, own_task_id=own_id,
                guard_original_deadline=own_deadline,
                cutoff=min(cutoff, own_deadline-5) if own_deadline is not None else cutoff)


def snapshot_file(source, destination):
    data = Path(source).read_bytes()
    with Path(destination).open('xb') as stream:
        stream.write(data)
        stream.flush()
        os.fsync(stream.fileno())
    return dict(original_path=str(source), archive_path=str(destination),
                bytes=len(data), sha256=sha(data))


def resume_worker(plan, ledger, owner, reason):
    # Recovery must still signal when disk-full/IO errors prevent evidence writes.
    def log(name, **values):
        try:
            event(ledger, owner, name, **values)
        except OSError:
            pass
    requested_at = time.time()
    try:
        actual = same_process(plan['worker'])
        if actual['state'] != 'Z':
            checked_signal(plan['worker'], signal.SIGCONT)
        # No ledger read/write/fsync may delay the recovery signal itself.
        # In particular a stalled shared filesystem must not keep the worker
        # stopped. Evidence is written only after local /proc confirmation.
        until = time.monotonic() + 3
        while time.monotonic() < until:
            try:
                actual = same_process(plan['worker'])
            except (FileNotFoundError, ProcessLookupError):
                log('resume_signal_sent', requested_at=requested_at, reason=reason)
                log('resumed', worker_exited=True)
                return True
            if actual['state'] not in ('T', 't'):
                log('resume_signal_sent', requested_at=requested_at, reason=reason)
                log('resumed', state=actual['state'])
                return True
            time.sleep(.02)
        log('resume_failed', reason='worker remains stopped')
    except (OSError, GuardError) as exc:
        log('resume_failed', reason=str(exc))
    return False


def watchdog(ledger):
    ledger = Path(ledger)
    plan = read_json(ledger/'plan.json')
    preflight = read_json(ledger/'preflight.json')
    owner = 'watchdog'
    reason = 'watchdog exception'
    def interrupted(signum, frame):
        raise GuardError('watchdog received signal %d' % signum)
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    try:
        require(sha(Path(__file__).read_bytes()) == preflight['tool_sha256'],
                'watchdog source differs from archived guard source')
        require(socket.gethostname() == plan['hostname'] and
                os.environ.get('PBS_JOBID') == plan['pbs_job'], 'watchdog allocation mismatch')
        same_process(plan['worker'], allow_zombie=False)
        same_process(preflight['guard'], allow_zombie=False)
        atomic_json(ledger/'watchdog.json', dict(ready=True, identity=process_identity(os.getpid()),
                                              observed_at=time.time()))
        event(ledger, owner, 'watchdog_ready')
        while True:
            state = read_json(ledger/'guard_state.json')
            if state.get('finished') and state.get('worker_resumed'):
                reason = 'guard finished with worker resumed'
                break
            try:
                guard = same_process(preflight['guard'])
                if guard['state'] == 'Z':
                    reason = 'guard exited'
                    break
            except (FileNotFoundError, ProcessLookupError):
                reason = 'guard disappeared'
                break
            if time.monotonic() - state['heartbeat_monotonic'] > preflight['watchdog_stale_s']:
                reason = 'guard heartbeat expired'
                break
            if time.time() >= preflight['cutoff'] or time.monotonic() >= preflight['cutoff_monotonic']:
                reason = 'allocation cleanup cutoff reached'
                break
            time.sleep(preflight['poll_s'])
    finally:
        resume_worker(plan, ledger, owner, reason)


def exit_evidence(identity, last_alive_at, deadline, task_dir,
                  last_alive_monotonic=None, monotonic_deadline=None):
    actual = same_process(identity)
    require(actual['state'] == 'Z', 'exit observation requires unreaped worker child')
    observed = time.time()
    observed_mono = time.monotonic()
    raw = actual['exit_raw']
    value = dict(completion_observed_at=observed, last_alive_at=last_alive_at,
                 exit_time_interval=[last_alive_at, observed],
                 completion_observed_monotonic=observed_mono,
                 last_alive_monotonic=last_alive_monotonic,
                 completion_observed_before_deadline=observed <= deadline and
                    (monotonic_deadline is None or observed_mono <= monotonic_deadline),
                 kernel_waitstatus_available=raw is not None,
                 exit_raw=raw,
                 exit_code=os.WEXITSTATUS(raw) if raw is not None and os.WIFEXITED(raw) else None,
                 terminating_signal=os.WTERMSIG(raw) if raw is not None and os.WIFSIGNALED(raw) else None,
                 original_worker_reaped_exit_code_required_for_acceptance=True)
    metrics = task_dir/'metrics.txt'
    if metrics.exists():
        data = metrics.read_bytes()
        lines = data.decode('utf-8', 'replace').splitlines()
        exits = [x.split(':', 1)[1].strip() for x in lines if x.strip().startswith('Exit status:')]
        value['metrics'] = dict(path=str(metrics), sha256=sha(data), bytes=len(data),
                                exit_status=int(exits[0]) if len(exits) == 1 else None)
    else:
        value['metrics'] = None
    return value


def run(plan_path, ledger, poll_s=.25, watchdog_stale_s=10):
    """Explicit execute path. Never called by check or make_plan."""
    require(.02 <= poll_s <= 2 and watchdog_stale_s >= 4*poll_s,
            'invalid polling/watchdog interval')
    plan_bytes = Path(plan_path).read_bytes()
    plan = json.loads(plan_bytes)
    ledger = Path(ledger)
    require(not os.path.lexists(str(ledger)), 'ledger destination already exists')
    # A task can start just before worker atomically writes its running status.
    ready_until = time.monotonic() + 5
    while True:
        try:
            checked = validate_plan(plan, own_group=os.getpgrp())
            break
        except (FileNotFoundError, GuardError):
            if time.monotonic() >= ready_until:
                raise
            time.sleep(.05)
    root, queue = paths(plan)
    ledger.mkdir(parents=True, exist_ok=False)
    (ledger/'before').mkdir()
    (ledger/'tool').mkdir()
    (ledger/'plan.json').write_bytes(plan_bytes)
    tool_evidence = snapshot_file(Path(__file__).resolve(), ledger/'tool/deadline_guard.py')
    snapshots = [snapshot_file(queue/'worker.json', ledger/'before/worker.json')]
    for ident in checked['records']:
        snapshots.append(snapshot_file(root/'runs/tasks'/ident/'status.json',
                                       ledger/'before'/(ident+'.status.json')))
        snapshots.append(snapshot_file(queue/'running'/(ident+'.json'),
                                       ledger/'before'/(ident+'.running.json')))
    start_wall, start_mono = time.time(), time.monotonic()
    preflight = dict(schema=1, validated_at=start_wall, plan_sha256=sha(plan_bytes),
                     tool_sha256=tool_evidence['sha256'], tool_evidence=tool_evidence,
                     guard=process_identity(os.getpid()), worker=checked['worker'],
                     guard_task_id=checked['own_task_id'], snapshots=snapshots,
                     guard_original_deadline=checked['guard_original_deadline'],
                     kernel_waitstatus_available=checked['worker']['exit_raw'] is not None,
                     cutoff=checked['cutoff'], cutoff_monotonic=start_mono+checked['cutoff']-start_wall,
                     poll_s=poll_s, watchdog_stale_s=watchdog_stale_s,
                     original_deadlines={k:v['original_deadline'] for k,v in checked['records'].items()})
    atomic_json(ledger/'preflight.json', preflight)
    state = dict(heartbeat_monotonic=time.monotonic(), observed_at=time.time(),
                 finished=False, worker_resumed=False)
    atomic_json(ledger/'guard_state.json', state)
    outcomes, watched, pause_attempted, resumed = {}, None, False, False
    error = None
    def heartbeat():
        state.update(heartbeat_monotonic=time.monotonic(), observed_at=time.time())
        atomic_json(ledger/'guard_state.json', state)
    def interrupted(signum, frame):
        raise GuardError('guard received signal %d' % signum)
    signal.signal(signal.SIGTERM, interrupted)
    signal.signal(signal.SIGINT, interrupted)
    try:
        watched = subprocess.Popen([sys.executable, str(ledger/'tool/deadline_guard.py'),
                                    'watchdog', '--ledger', str(ledger)], start_new_session=True)
        ready_until = time.monotonic()+5
        while not (ledger/'watchdog.json').exists():
            require(watched.poll() is None, 'watchdog exited before readiness')
            require(time.monotonic() < ready_until, 'watchdog readiness timeout')
            heartbeat()
            time.sleep(poll_s)
        watchdog_record = read_json(ledger/'watchdog.json')
        require(watchdog_record.get('ready') and watchdog_record['identity']['pid'] == watched.pid,
                'watchdog readiness identity mismatch')
        same_process(watchdog_record['identity'], allow_zombie=False)
        # Recheck deadlines and ownership after all preparation, BEFORE stopping.
        validate_plan(plan, own_group=os.getpgrp())
        event(ledger, 'guard', 'suspend_intent', worker=plan['worker'],
              watchdog=watchdog_record['identity'])
        pause_attempted = True
        checked_signal(plan['worker'], signal.SIGSTOP)
        stopped_until = time.monotonic()+3
        while same_process(plan['worker'])['state'] not in ('T', 't'):
            require(time.monotonic() < stopped_until, 'worker did not stop')
            heartbeat()
            time.sleep(.02)
        validate_plan(plan, own_group=os.getpgrp(), worker_may_be_stopped=True)
        event(ledger, 'guard', 'suspended')
        pending = dict(checked['records'])
        last_alive = {key:value['status']['started'] for key,value in pending.items()}
        last_alive_mono = {key:None for key in pending}
        mono_deadlines = {key:start_mono+v['entry']['deadline']-start_wall for key,v in pending.items()}
        while pending:
            heartbeat()
            require(watched.poll() is None, 'watchdog has exited; return control to worker')
            require(same_process(plan['worker'])['state'] in ('T', 't'),
                    'worker resumed outside guard; stop supervising')
            require(time.time() < checked['cutoff'] and time.monotonic() < preflight['cutoff_monotonic'],
                    'allocation cleanup cutoff reached')
            for ident, record in list(pending.items()):
                identity, deadline = record['entry']['identity'], record['entry']['deadline']
                before_read, before_read_mono = time.time(), time.monotonic()
                actual = same_process(identity)
                if actual['state'] == 'Z':
                    value = exit_evidence(identity, last_alive[ident], deadline, root/'runs/tasks'/ident,
                                          last_alive_mono[ident], mono_deadlines[ident])
                    value.update(id=ident, original_deadline=record['original_deadline'],
                                 extended_deadline=deadline, termination_signal_sent=False)
                    outcomes[ident] = value
                    event(ledger, 'guard', 'task_exit_observed', **value)
                    del pending[ident]
                elif time.time() >= deadline or time.monotonic() >= mono_deadlines[ident]:
                    # Use the same process-group SIGKILL policy as worker.py.
                    # Never kill the guard's own group or the worker group.
                    require(identity['pgid'] not in (os.getpgrp(), plan['worker']['pgid']),
                            'unsafe timeout target group')
                    event(ledger, 'guard', 'deadline_signal_intent', id=ident, signal='SIGKILL', identity=identity)
                    checked_signal(identity, signal.SIGKILL, group=True)
                    outcomes[ident] = dict(id=ident, original_deadline=record['original_deadline'],
                                          extended_deadline=deadline, termination_signal_sent=True,
                                          deadline_reached_at=time.time(), completion_observed_before_deadline=False)
                    event(ledger, 'guard', 'deadline_signal_sent', **outcomes[ident])
                    del pending[ident]
                else:
                    last_alive[ident] = before_read
                    last_alive_mono[ident] = before_read_mono
            if pending:
                time.sleep(poll_s)
    except BaseException as exc:
        error = '%s: %s' % (type(exc).__name__, exc)
        event(ledger, 'guard', 'guard_error', reason=error)
    finally:
        if pause_attempted:
            resumed = resume_worker(plan, ledger, 'guard', 'normal completion' if error is None else error)
        else:
            # Watchdog may already exist. A verified SIGCONT is harmless and
            # closes a possible stop-intent / local-exception race explicitly.
            resumed = resume_worker(plan, ledger, 'guard', 'pre-suspend exit')
        state.update(finished=True, worker_resumed=resumed)
        heartbeat()
        if watched is not None:
            try:
                watched.wait(timeout=5)
            except subprocess.TimeoutExpired:
                # Do not kill the recovery mechanism. It retains the PBS cutoff.
                event(ledger, 'guard', 'watchdog_still_running')
        summary = dict(schema=1, plan_sha256=sha(plan_bytes), guard_error=error,
                       worker_resumed=resumed, tasks=outcomes,
                       watchdog_pid=watched.pid if watched is not None else None,
                       watchdog_exit_code=watched.poll() if watched is not None else None,
                       watchdog_finished=watched is not None and watched.poll() is not None,
                       completed_at=time.time(), original_status_files_modified=False,
                       acceptance='not-determined-by-scheduling-tool')
        atomic_json(ledger/'summary.json', summary)
    return 0 if error is None and resumed and not any(x.get('termination_signal_sent') for x in outcomes.values()) else 2


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest='action', required=True)
    check = sub.add_parser('check', help='read-only validation, no ledger or signals')
    check.add_argument('--plan', required=True)
    execute = sub.add_parser('run', help='EXPLICITLY supervise and suspend our worker')
    execute.add_argument('--plan', required=True)
    execute.add_argument('--ledger', required=True)
    execute.add_argument('--poll-s', type=float, default=.25)
    execute.add_argument('--watchdog-stale-s', type=float, default=10)
    watch = sub.add_parser('watchdog', help=argparse.SUPPRESS)
    watch.add_argument('--ledger', required=True)
    args = parser.parse_args()
    try:
        if args.action == 'check':
            result = validate_plan(read_json(args.plan))
            print(json.dumps(dict(valid=True, task_ids=sorted(result['records']),
                                  worker=result['worker'], cutoff=result['cutoff']), indent=2))
            return 0
        if args.action == 'watchdog':
            watchdog(args.ledger)
            return 0
        return run(args.plan, args.ledger, args.poll_s, args.watchdog_stale_s)
    except (GuardError, OSError, KeyError, ValueError) as exc:
        print('deadline guard refused: '+str(exc), file=sys.stderr)
        return 2


if __name__ == '__main__':
    sys.exit(main())
