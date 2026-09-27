#!/usr/bin/env python3
"""Collect execution/resource facts for one uniformly versioned full campaign.

No mathematical certificate is rechecked and no reference answer is read.
Observer times use one clock; task CPU/RSS come from saved per-task records.
"""
import argparse
from collections import Counter
from datetime import datetime, timezone
import hashlib
import json
import math
from pathlib import Path
import re
import sys

from deadline_evidence import audit_extension, read_index


class ReportError(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise ReportError(message)


def number(value, name):
    require(isinstance(value, (int, float)) and not isinstance(value, bool)
            and math.isfinite(value) and value >= 0, 'invalid ' + name)
    return value


def read_json(path, evidence):
    payload = path.read_bytes()
    evidence[str(path)] = hashlib.sha256(payload).hexdigest()
    return json.loads(payload)


def parse_metrics(payload):
    """GNU time -v under LC_ALL=C; never infer missing fields as zero."""
    text = payload.decode('utf-8')
    fields = {
        'user_cpu_seconds': 'User time (seconds)',
        'system_cpu_seconds': 'System time (seconds)',
        'maximum_resident_set_size_kib': 'Maximum resident set size (kbytes)',
        'exit_status': 'Exit status',
    }
    values = {}
    for key, label in fields.items():
        match = re.search(r'^\s*' + re.escape(label) + r':\s*([0-9.]+)\s*$', text, re.M)
        if not match:
            return None
        values[key] = number(float(match.group(1)), key)
    match = re.search(r'^\s*Elapsed \(wall clock\) time \(h:mm:ss or m:ss\):\s*([0-9:.]+)\s*$', text, re.M)
    if not match:
        return None
    parts = match.group(1).split(':')
    require(len(parts) in (2, 3), 'invalid GNU time elapsed format')
    values['wall_seconds'] = sum(number(float(x), 'time component') * 60 ** i
                                 for i, x in enumerate(reversed(parts)))
    for key in ('maximum_resident_set_size_kib', 'exit_status'):
        require(values[key].is_integer(), 'nonintegral ' + key)
        values[key] = int(values[key])
    values['process_cpu_seconds'] = values['user_cpu_seconds'] + values['system_cpu_seconds']
    return values


def stage_intervals(data):
    total = data['total_cpu_ms']
    events = data.get('stage_timings')
    require(isinstance(events, list) and events, 'missing stage_timings')
    previous = 0
    for event in events:
        require(isinstance(event.get('stage'), str), 'invalid stage name')
        now = number(event.get('cpu_ms'), 'stage cpu_ms')
        require(previous <= now <= total, 'nonmonotone stage timings')
        previous = now
    stages = [dict(stage='startup_and_resolution', cpu_start_ms=0,
                   cpu_end_ms=events[0]['cpu_ms'], cpu_seconds=events[0]['cpu_ms']/1000)]
    for i, event in enumerate(events):
        end = events[i+1]['cpu_ms'] if i+1 < len(events) else total
        stages.append(dict(stage=event['stage'], cpu_start_ms=event['cpu_ms'],
                           cpu_end_ms=end, cpu_seconds=(end-event['cpu_ms'])/1000))
    return stages


def collect(run, tasks_root, allow_partial=False, top=10):
    evidence = {}
    extensions = read_index(run, evidence)
    manifest = read_json(run/'campaign.json', evidence)
    require(manifest.get('mode') == 'full' and not manifest.get('prepared_only'),
            'require a submitted full campaign')
    groups = manifest['groups']
    require(isinstance(groups, list) and groups and len(set(groups)) == len(groups)
            and all(type(g) is int and 1 <= g <= 230 for g in groups), 'invalid campaign groups')
    source = manifest['source_id']
    hashes = manifest['source_sha256']
    require(isinstance(hashes, dict) and hashes and 'gap/run_one.g' in hashes,
            'missing source hash manifest')
    require(hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest() == source,
            'source_id does not hash the saved source manifest')
    tasks = manifest['tasks']
    require(len(tasks) == len(groups) and {t['space_group'] for t in tasks} == set(groups)
            and len({t['id'] for t in tasks}) == len(tasks), 'tasks do not cover groups exactly once')
    require(set(extensions) <= {t['id'] for t in tasks}, 'deadline extension names a task outside this campaign')
    submitted = min(number(t['created'], 'task created') for t in tasks)
    missing = {k: [] for k in ('results', 'classification_checkpoints', 'task_status',
                               'tasks_not_done', 'metrics', 'observer')}
    rows, nodes = [], {}
    for task in sorted(tasks, key=lambda t: t['space_group']):
        sg, ident = task['space_group'], task['id']
        require(Path(ident).name == ident, 'invalid task id')
        row = dict(space_group=sg, task_id=ident, queue=task['queue'])
        checkpoint_path = run/'classification'/('sg%d.json' % sg)
        result_path = run/('sg%d.json' % sg)
        checkpoint = result = None
        for path, kind in [(checkpoint_path, 'classification_checkpoints'), (result_path, 'results')]:
            if not path.exists():
                missing[kind].append(sg)
                continue
            data = read_json(path, evidence)
            require(data.get('space_group') == sg and data.get('status') == 'computed',
                    'wrong group or noncomputed record: ' + str(path))
            require(data.get('source_id') == source, 'mixed source: ' + str(path))
            number(data.get('cpu_ms'), 'classification cpu_ms')
            if kind == 'results':
                require(data.get('source_sha256') == hashes and data.get('mode') == 'full',
                        'result source hashes or mode differ: ' + str(path))
                number(data.get('total_cpu_ms'), 'total_cpu_ms')
                number(data.get('wall_seconds'), 'wall_seconds')
                require(data['total_cpu_ms'] >= data['cpu_ms'], 'negative post-classification CPU')
                result = data
                row.update(gap_total_cpu_seconds=data['total_cpu_ms']/1000,
                           gap_post_classification_cpu_seconds=(data['total_cpu_ms']-data['cpu_ms'])/1000,
                           result_wall_seconds=data['wall_seconds'], stage_intervals=stage_intervals(data))
            else:
                checkpoint = data
        if checkpoint and result:
            require(checkpoint['cpu_ms'] == result['cpu_ms'], 'checkpoint/result CPU mismatch for SG%d' % sg)
        if checkpoint or result:
            row['gap_classification_cpu_seconds'] = (checkpoint or result)['cpu_ms']/1000
        taskdir = tasks_root/ident
        status_path = taskdir/'status.json'
        if not status_path.exists():
            missing['task_status'].append(sg)
            status = None
        else:
            status = read_json(status_path, evidence)
            for key in ('id', 'space_group', 'command', 'queue', 'created'):
                require(status.get(key) == task.get(key), 'task provenance mismatch: %s %s' % (ident, key))
            row['task_status'] = status['status']
            if status.get('hostname'):
                row.update(hostname=status['hostname'], pbs_job=status.get('pbs_job'))
            else:
                missing['task_status'].append(sg)
        metrics_path = taskdir/'metrics.txt'
        metrics = None
        payload = None
        if metrics_path.exists():
            payload = metrics_path.read_bytes()
            evidence[str(metrics_path)] = hashlib.sha256(payload).hexdigest()
            metrics = parse_metrics(payload)
        if metrics is None:
            missing['metrics'].append(sg)
        else:
            require(not status or status.get('status') != 'done' or metrics['exit_status'] == 0,
                    'successful task has nonzero GNU time exit status: ' + ident)
            row['gnu_time'] = metrics
        if ident in extensions:
            require(status is not None and metrics is not None, 'extension needs final status and complete metrics')
            require(metrics['exit_status'] == 0, 'extended task has nonzero GNU time exit status')
            extension = audit_extension(extensions[ident], task, status, payload, evidence)
            row['deadline_extension'] = extension
            row['effective_task_status'] = extension['effective_status']
            row['worker_task_wall_seconds'] = number(status.get('elapsed_s'), 'worker elapsed_s')
        elif status is not None:
            if status['status'] != 'done' or status.get('exit_code') != 0:
                missing['tasks_not_done'].append(dict(space_group=sg, status=status['status'],
                                                     exit_code=status.get('exit_code')))
            else:
                row['worker_task_wall_seconds'] = number(status.get('elapsed_s'), 'worker elapsed_s')
        rows.append(row)
        if 'hostname' in row:
            node = nodes.setdefault(row['hostname'], dict(groups=[], pbs_jobs=set(), states=Counter(), rows=[]))
            node['groups'].append(sg)
            if row.get('pbs_job'):
                node['pbs_jobs'].add(row['pbs_job'])
            node['states'][row.get('task_status', 'unknown')] += 1
            node['rows'].append(row)

    observation_path = run/'observation.json'
    observer = dict(classification_elapsed_seconds=None, full_elapsed_seconds=None)
    if not observation_path.exists():
        missing['observer'].append('observation.json')
    else:
        observation = read_json(observation_path, evidence)
        require(observation.get('source_id') == source and observation.get('submitted_at') == submitted,
                'observer belongs to a different campaign')
        require(not observation.get('errors'), 'observer reports invalid results')
        history = observation.get('history', [])
        require(isinstance(history, list), 'invalid observer history')
        require(type(observation.get('observed_complete')) is bool, 'invalid observer completion flag')
        previous = -1
        previous_counts = {'classification_checkpoints': 0, 'full_results': 0}
        for event in history:
            elapsed = number(event['elapsed_seconds'], 'observer elapsed')
            observed_at = number(event['observed_at'], 'observer observed_at')
            require(elapsed >= previous and abs(observed_at-submitted-elapsed) < 1e-5,
                    'inconsistent observer clock')
            previous = elapsed
            for key, output in [('classification_checkpoints', 'classification_elapsed_seconds'),
                                ('full_results', 'full_elapsed_seconds')]:
                require(type(event[key]) is int and 0 <= event[key] <= len(groups), 'invalid observer count')
                require(event[key] >= previous_counts[key], 'observer count decreased: ' + key)
                previous_counts[key] = event[key]
                if event[key] == len(groups) and observer[output] is None:
                    observer[output] = elapsed
            require(event['full_results'] <= event['classification_checkpoints'],
                    'observer full results precede their classification checkpoints')
        if not observation.get('observed_complete'):
            missing['observer'].append('full completion not observed')
            observer['full_elapsed_seconds'] = None
        else:
            require(history and history[-1]['full_results'] == len(groups),
                    'observer complete without final full count')
        if observer['classification_elapsed_seconds'] is None:
            missing['observer'].append('classification completion not observed')
        observer.update(submitted_at=submitted, latest_event=history[-1] if history else None,
                        polling_interval_seconds=observation.get('polling_interval_seconds'),
                        observer_restarts=observation.get('observer_restarts', []),
                        timing_scope=observation.get('timing_scope'),
                        wall_time_clock='one observer clock; no cross-node timestamp subtraction')

    def totals(items):
        measured = [r['gnu_time'] for r in items if 'gnu_time' in r]
        return dict(tasks=len(items), classification_cpu_records=sum('gap_classification_cpu_seconds' in r for r in items),
                    full_cpu_records=sum('gap_total_cpu_seconds' in r for r in items), metrics_records=len(measured),
                    gap_classification_cpu_seconds=sum(r.get('gap_classification_cpu_seconds', 0) for r in items),
                    gap_classification_cpu_seconds_for_full_results=sum(r.get('gap_classification_cpu_seconds', 0)
                                                                         for r in items if 'gap_total_cpu_seconds' in r),
                    gap_total_cpu_seconds=sum(r.get('gap_total_cpu_seconds', 0) for r in items),
                    gap_post_classification_cpu_seconds=sum(r.get('gap_post_classification_cpu_seconds', 0) for r in items),
                    process_user_cpu_seconds=sum(m['user_cpu_seconds'] for m in measured),
                    process_system_cpu_seconds=sum(m['system_cpu_seconds'] for m in measured),
                    process_cpu_seconds=sum(m['process_cpu_seconds'] for m in measured))

    for node in nodes.values():
        node.update(totals(node.pop('rows')))
        node['pbs_jobs'] = sorted(node['pbs_jobs'])
        node['states'] = dict(node['states'])
    measured_rows = [r for r in rows if 'gnu_time' in r]
    peak = max(measured_rows, key=lambda r:r['gnu_time']['maximum_resident_set_size_kib'], default=None)
    peak_report = None if peak is None else dict(space_group=peak['space_group'], task_id=peak['task_id'],
        hostname=peak.get('hostname'), maximum_resident_set_size_kib=peak['gnu_time']['maximum_resident_set_size_kib'],
        maximum_resident_set_size_gib=peak['gnu_time']['maximum_resident_set_size_kib']/1024**2)
    slowest = {}
    for field in ('result_wall_seconds', 'gap_total_cpu_seconds', 'gap_classification_cpu_seconds',
                  'gap_post_classification_cpu_seconds'):
        slowest[field] = [dict(space_group=r['space_group'], task_id=r['task_id'], seconds=r[field])
                          for r in sorted((r for r in rows if field in r), key=lambda r:r[field], reverse=True)[:top]]
    intervals = [dict(space_group=r['space_group'], **stage) for r in rows for stage in r.get('stage_intervals', [])]
    slowest['stage_intervals'] = sorted(intervals, key=lambda x:x['cpu_seconds'], reverse=True)[:top]
    complete = not any(missing.values())
    report = dict(schema_version=1, collected_at_utc=datetime.now(timezone.utc).isoformat(),
                  campaign=str(run), task_root=str(tasks_root), source_id=source, source_sha256=hashes,
                  groups=sorted(groups), expected_groups=len(groups), complete=complete, missing=missing,
                  deadline_extensions=[dict(task_id=r['task_id'], **r['deadline_extension'])
                                       for r in rows if 'deadline_extension' in r],
                  observer=observer, totals=totals(rows), nodes=nodes, max_single_task_rss=peak_report,
                  slowest=slowest, group_measurements=rows, evidence_sha256=evidence,
                  scope=dict(reference_answers_read=False, mathematical_audit_performed=False,
                      source_check='saved manifest source hash and every available checkpoint/result provenance agree',
                      gap_cpu='GAP Runtime() values; classification includes setup and free-pip classification',
                      post_classification_cpu='total GAP Runtime minus classification Runtime; includes stacking, witness export and surrounding driver work',
                      process_cpu='GNU time user+system CPU for the task command including child processes and Python wrappers; separate from GAP Runtime',
                      stage_intervals='each recorded GAP stage timestamp to the next timestamp, or final Runtime; includes intervening work',
                      rss='largest GNU time maximum resident set size among measured tasks, in Linux KiB; NOT simultaneous memory across processes, tasks or nodes; RSS values are never summed',
                      partial='CPU sums cover only the separately counted available records; unfinished task CPU is not estimated. Classification can cover more groups than full results; classification_for_full_results plus post_classification reconciles to total GAP CPU.',
                      observer='completion detection may lag; recorded observer restarts can add gaps beyond the polling interval'))
    report['scope']['deadline_extensions'] = ('Original worker states are retained. Separately audited predeadline extensions require original worker exit 0, GNU time exit 0 and a completed guard/watchdog ledger. Worker elapsed can include delayed reaping; GNU time and guard observation intervals describe the command runtime. Observer campaign times are unchanged.')
    if not complete and not allow_partial:
        raise ReportError('incomplete campaign; use --allow-partial for development: ' + json.dumps(missing, sort_keys=True))
    return report


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    ap.add_argument('--tasks-root', type=Path, help='Defaults to the sibling runs/tasks directory')
    ap.add_argument('--allow-partial', action='store_true', help='List missing measurements; source conflicts remain fatal')
    ap.add_argument('--top', type=int, default=10)
    ap.add_argument('--output', required=True, type=Path)
    args = ap.parse_args(argv)
    if args.top < 1:
        ap.error('--top must be positive')
    run = args.run.resolve()
    try:
        report = collect(run, (args.tasks_root or run.parent/'tasks').resolve(), args.allow_partial, args.top)
    except (ReportError, KeyError, OSError, ValueError, TypeError) as exc:
        print('Performance report refused: ' + str(exc), file=sys.stderr)
        return 2
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.output.with_suffix(args.output.suffix+'.tmp')
    tmp.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    tmp.replace(args.output)
    print(json.dumps(dict(complete=report['complete'], expected_groups=report['expected_groups'],
                         observer=report['observer'], totals=report['totals'],
                         max_single_task_rss=report['max_single_task_rss']), sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
