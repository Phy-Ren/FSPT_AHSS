"""Read and audit explicit scheduling-extension evidence without changing it.

An extension never converts the worker's original timeout record into ``done``.
The caller retains that record and reports a separate effective completion state.
"""
import hashlib
import json
import math
from pathlib import Path
import re


def require(condition, message):
    if not condition:
        raise ValueError('deadline evidence: ' + message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def finite(value, name):
    require(type(value) in (int, float) and math.isfinite(value) and value >= 0,
            'invalid ' + name)
    return value


def read_index(run, evidence):
    path = run/'deadline_extensions.json'
    if not path.exists():
        return {}
    raw = path.read_bytes()
    evidence[str(path)] = digest(raw)
    data = json.loads(raw)
    require(data.get('schema') == 'fspt-deadline-extension-index-v1', 'unknown index schema')
    mappings = data.get('tasks')
    require(isinstance(mappings, dict) and mappings, 'empty or invalid index')
    result = {}
    archive_map = None
    original_run = run
    archive_path = run/'archive.json'
    if archive_path.exists():
        archive_raw = archive_path.read_bytes()
        evidence[str(archive_path)] = digest(archive_raw)
        archive = json.loads(archive_raw)
        original_run = Path(archive['original_run'])
        archive_map = {v['original_path']: v['archive_path']
                       for v in archive['files'].values()
                       if v.get('original_path') is not None}
    for ident, ledger in mappings.items():
        require(isinstance(ident, str) and Path(ident).name == ident and ident not in ('', '.', '..'),
                'invalid task ID')
        require(isinstance(ledger, str) and ledger, 'invalid ledger path')
        original = (original_run/ledger).resolve()
        if archive_map is not None:
            original_plan = str(original/'plan.json')
            require(original_plan in archive_map, 'archived ledger is not mapped')
            archived_plan = (run/archive_map[original_plan]).resolve()
            require(run.resolve() in archived_plan.parents, 'archived ledger escapes archive')
            result[ident] = archived_plan.parent
        else:
            result[ident] = original
    return result


def audit_extension(ledger, task, status, metrics_payload, evidence):
    """Require predeadline authorization, successful observation and actual reap.

    The original worker must have reaped the command with exit_code=0. GNU time
    and guard evidence must independently agree. Raw kernel waitstatus is optional
    on old Linux; its absence is recorded, never inferred as zero.
    """
    ledger = Path(ledger).resolve()
    files = {}
    for path in sorted(ledger.rglob('*')):
        require(not path.is_symlink(), 'ledger contains a symlink')
        if path.is_file():
            relative = str(path.relative_to(ledger))
            raw = path.read_bytes()
            files[relative] = raw
            evidence[str(path)] = digest(raw)

    def data(name):
        require(name in files, 'missing ' + name)
        return json.loads(files[name])

    def events(owner):
        name = 'events.'+owner+'.jsonl'
        require(name in files, 'missing '+name)
        values = [json.loads(line) for line in files[name].splitlines() if line]
        require(values, 'empty '+name)
        previous = -1
        for value in values:
            now = finite(value['monotonic'], 'event monotonic')
            require(now >= previous, 'event order regressed')
            previous = now
            finite(value['observed_at'], 'event wall time')
        return values

    plan, preflight, summary = data('plan.json'), data('preflight.json'), data('summary.json')
    require(plan.get('schema') == preflight.get('schema') == summary.get('schema') == 1,
            'unsupported ledger schema')
    require(preflight.get('plan_sha256') == summary.get('plan_sha256') == digest(files['plan.json']),
            'plan hash mismatch')
    require('tool/deadline_guard.py' in files and
            digest(files['tool/deadline_guard.py']) == preflight.get('tool_sha256'),
            'frozen guard tool hash mismatch')
    require(summary.get('guard_error') is None and summary.get('worker_resumed') is True
            and summary.get('watchdog_finished') is True and summary.get('watchdog_exit_code') == 0,
            'guard/watchdog did not finish successfully')
    require(summary.get('original_status_files_modified') is False, 'original status was modified')
    final_state, watchdog = data('guard_state.json'), data('watchdog.json')
    require(final_state.get('finished') is True and final_state.get('worker_resumed') is True,
            'guard has not finished')
    require(watchdog.get('ready') is True and
            watchdog['identity']['pid'] == summary['watchdog_pid'], 'watchdog identity mismatch')
    watch_identity = watchdog['identity']
    require(watch_identity['pid'] == watch_identity['pgid'] == watch_identity['sid'] and
            watch_identity['pgid'] not in (preflight['guard']['pgid'], plan['worker']['pgid']),
            'watchdog is not independent')
    for snapshot in preflight['snapshots']:
        relative = 'before/'+Path(snapshot['archive_path']).name
        require(relative in files and digest(files[relative]) == snapshot['sha256'] and
                len(files[relative]) == snapshot['bytes'], 'preflight snapshot hash mismatch')
    worker_before = data('before/worker.json')
    require(worker_before['pid'] == plan['worker']['pid'] and
            worker_before['hostname'] == plan['hostname'] and worker_before['pbs_job'] == plan['pbs_job'],
            'worker snapshot mismatch')
    ident = task['id']
    entries = {x['id']: x for x in plan['tasks']}
    require(len(entries) == len(plan['tasks']) and ident in entries, 'task not uniquely in plan')
    entry = entries[ident]
    before_name, running_name = 'before/'+ident+'.status.json', 'before/'+ident+'.running.json'
    before, running = data(before_name), data(running_name)
    require(digest(files[before_name]) == entry['status_sha256'] and
            digest(files[running_name]) == entry['running_sha256'], 'original task hash mismatch')
    require(before.get('status') == 'running' and before.get('id') == ident, 'not a running task at declaration')
    for key, value in before.items():
        if key not in ('status', 'exit_code', 'elapsed_s', 'finished'):
            require(status.get(key) == value, 'reaped task identity changed: '+key)
    for key in ('id', 'command', 'queue', 'created', 'space_group'):
        require(status.get(key) == task.get(key), 'campaign/task identity mismatch: '+key)
    for key, value in running.items():
        require(before.get(key) == value, 'running payload differs from original status: '+key)
    require(status.get('status') in ('done', 'timeout') and status.get('exit_code') == 0,
            'original worker did not reap successful exit')
    require(plan['hostname'] == status['hostname'] and plan['pbs_job'] == status['pbs_job']
            and plan['queue'] == status.get('queue', plan['queue']), 'allocation mismatch')
    identity = entry['identity']
    require(identity['pid'] == before['pid'] == identity['pgid'] == identity['sid'] and
            identity['ppid'] == plan['worker']['pid'], 'task process identity mismatch')
    require(identity['cmdline'] == ['/usr/bin/time', '-v', '-o',
            str(Path(plan['root'])/'runs/tasks'/ident/'metrics.txt')] + before['command'],
            'task process command mismatch')
    for key in ('pid', 'uid', 'pgid', 'sid', 'start_ticks', 'cmdline'):
        require(plan['worker'][key] == preflight['worker'][key], 'worker identity mismatch: '+key)
    original = finite(before['started'], 'started') + finite(before['timeout_s'], 'original timeout')
    extended = finite(entry['deadline'], 'extended deadline')
    require(preflight['original_deadlines'][ident] == original, 'original deadline mismatch')
    require(plan['created_at'] <= preflight['validated_at'] < original <= extended < preflight['cutoff'],
            'extension not declared and validated before deadline or outside cutoff')
    require(preflight['cutoff'] <= plan['allocation_deadline'] - plan['cleanup_margin_s'] and
            preflight['guard_original_deadline'] >= extended+10, 'extension outside supervised allocation')
    guard_events, watchdog_events = events('guard'), events('watchdog')
    require(all(x['pid'] == preflight['guard']['pid'] for x in guard_events) and
            all(x['pid'] == watch_identity['pid'] for x in watchdog_events), 'event process identity mismatch')
    require(not any(x['event'] in ('guard_error', 'resume_failed', 'watchdog_still_running')
                    for x in guard_events+watchdog_events), 'guard error event present')
    suspension = [x for x in guard_events if x['event'] == 'suspended']
    intent = [x for x in guard_events if x['event'] == 'suspend_intent']
    ready = [x for x in watchdog_events if x['event'] == 'watchdog_ready']
    require(len(intent) == len(ready) == 1 and intent[0]['worker'] == plan['worker'] and
            intent[0]['watchdog'] == watch_identity, 'suspension identity mismatch')
    require(len(suspension) == 1 and preflight['validated_at'] <= suspension[0]['observed_at'] < original,
            'worker not suspended before original deadline')
    require(ready[0]['monotonic'] <= intent[0]['monotonic'] <= suspension[0]['monotonic'],
            'watchdog was not ready before suspension')
    require(any(x['event'] == 'resumed' for x in guard_events) and
            any(x['event'] == 'resumed' for x in watchdog_events) and
            any(x['event'] == 'watchdog_ready' for x in watchdog_events), 'missing recovery/watchdog evidence')
    exits = [x for x in guard_events if x['event'] == 'task_exit_observed' and x.get('id') == ident]
    require(len(exits) == 1, 'task exit was not uniquely observed')
    outcome = summary['tasks'][ident]
    require(all(exits[0].get(k) == v for k, v in outcome.items()), 'summary/exit event mismatch')
    require(outcome.get('termination_signal_sent') is False and
            outcome.get('completion_observed_before_deadline') is True and
            outcome.get('terminating_signal') is None, 'task did not finish within extension')
    require(not any(x['event'].startswith('deadline_signal') and x.get('id') == ident
                    for x in guard_events), 'task was signaled by deadline guard')
    require(outcome['original_deadline'] == original and outcome['extended_deadline'] == extended,
            'outcome deadline mismatch')
    observed = finite(outcome['completion_observed_at'], 'completion observation')
    lower = finite(outcome['last_alive_at'], 'last alive')
    require(before['started'] <= lower <= observed <= extended and
            outcome['exit_time_interval'] == [lower, observed], 'invalid completion interval')
    require(suspension[0]['monotonic'] <= outcome['completion_observed_monotonic'] <=
            preflight['cutoff_monotonic'] - preflight['cutoff'] + extended,
            'completion outside monotonic deadline')
    require(all(x['monotonic'] >= outcome['completion_observed_monotonic']
                for x in guard_events+watchdog_events if x['event'] == 'resumed'),
            'worker resumed before task exit observation')
    require(outcome.get('exit_raw') in (None, 0) and outcome.get('exit_code') in (None, 0),
            'nonzero kernel exit evidence')
    metric_record = outcome.get('metrics')
    require(metric_record and metric_record['sha256'] == digest(metrics_payload) and
            metric_record['bytes'] == len(metrics_payload) and metric_record['exit_status'] == 0,
            'GNU time completion evidence mismatch')
    actual_exits = re.findall(r'^\s*Exit status:\s*(\d+)\s*$', metrics_payload.decode('utf-8'), re.M)
    require(actual_exits == ['0'], 'GNU time payload does not report successful exit')
    require(status['finished'] >= observed and summary['completed_at'] >= observed,
            'completion precedes observation')
    return dict(effective_status='done_with_audited_deadline_extension', ledger=str(ledger),
        original_worker_status=status['status'], original_deadline=original, extended_deadline=extended,
        completion_observed_at=observed, exit_time_interval=[lower, observed],
        task_wall_seconds_interval=[lower-before['started'], observed-before['started']],
        original_worker_reap_at=status['finished'], kernel_waitstatus_available=outcome.get('exit_raw') is not None,
        scope='successful original worker reap plus GNU time and predeadline guard evidence; original status preserved')
