"""Performance provenance for a completed background campaign.

Computational completion and a uniquely determined physical extension are
separate assertions. An audited finite family is never relabeled computed.
"""
from collections import Counter
import hashlib
import json
from pathlib import Path

from collect_performance import number, parse_metrics, stage_intervals


def require(test, message):
    if not test:
        raise ValueError(message)


def collect_background_performance(run, tasks_root, audits):
    run, tasks_root = Path(run), Path(tasks_root)
    evidence = {}

    def read(path, raw=False):
        payload = path.read_bytes()
        evidence[str(path.resolve())] = hashlib.sha256(payload).hexdigest()
        return payload if raw else json.loads(payload)

    manifest = read(run/'campaign.json')
    groups = manifest['groups']
    require(manifest.get('mode') == 'full' and manifest.get('prepared_only') is False,
            'require a submitted full campaign')
    require(isinstance(groups, list) and groups and len(set(groups)) == len(groups)
            and all(type(g) is int and 1 <= g <= 230 for g in groups), 'invalid campaign groups')
    hashes = manifest['source_sha256']
    require(isinstance(hashes, dict) and 'gap/run_one.g' in hashes, 'missing source manifest')
    require(hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest() == manifest['source_id'],
            'source manifest hash does not match source ID')
    require(set(groups) == set(audits) and len(groups) == len(audits), 'audit group coverage mismatch')
    require(len(manifest['tasks']) == len(groups), 'task count mismatch')
    rows, seen = [], set()
    for task in manifest['tasks']:
        sg, ident = task['space_group'], task['id']
        require(sg not in seen and sg in audits, 'duplicate/unaudited task')
        require(Path(ident).name == ident, 'invalid task ID')
        seen.add(sg)
        result = read(run/('sg%d.json' % sg))
        checkpoint = read(run/'classification'/('sg%d.json' % sg))
        status = read(tasks_root/ident/'status.json')
        metrics = parse_metrics(read(tasks_root/ident/'metrics.txt', raw=True))
        for key in ('id', 'space_group', 'command', 'queue', 'created'):
            require(status.get(key) == task.get(key), 'task provenance mismatch: '+key)
        require(status['status'] == 'done' and status['exit_code'] == 0, 'task did not finish successfully')
        require(metrics is not None and metrics['exit_status'] == 0, 'missing/failed GNU time metrics')
        for data in (result, checkpoint):
            require(data['space_group'] == sg and data['source_id'] == manifest['source_id'], 'result source/group mismatch')
            if 'source_sha256' in data:
                require(data['source_sha256'] == hashes, 'checkpoint/result source hash mismatch')
            number(data['cpu_ms'], 'classification CPU')
        require(result['source_sha256'] == manifest['source_sha256'], 'result source hash mismatch')
        require(result['cpu_ms'] == checkpoint['cpu_ms'], 'checkpoint CPU mismatch')
        number(result['total_cpu_ms'], 'total GAP CPU')
        require(result['cpu_ms'] <= result['total_cpu_ms'], 'invalid GAP CPU accounting')
        number(result['wall_seconds'], 'result elapsed time')
        number(status['elapsed_s'], 'task elapsed time')
        unique = bool(audits[sg]['full_group'])
        require(result['status'] == ('computed' if unique else 'unresolved'), 'mathematical status contradicts audit')
        rows.append(dict(space_group=sg, task_id=ident, queue=task['queue'],
            hostname=status['hostname'], pbs_job=status['pbs_job'],
            gap_classification_cpu_seconds=result['cpu_ms']/1000,
            gap_total_cpu_seconds=result['total_cpu_ms']/1000,
            gap_post_classification_cpu_seconds=(result['total_cpu_ms']-result['cpu_ms'])/1000,
            result_wall_seconds=result['wall_seconds'], worker_task_wall_seconds=status['elapsed_s'],
            gnu_time=metrics, stage_intervals=stage_intervals(result),
            unique_full_group=unique, audit_kind=audits[sg]['kind']))
    observation = read(run/'observation.json')
    submitted = min(number(t['created'], 'task created') for t in manifest['tasks'])
    require(observation['source_id'] == manifest['source_id'] and observation['submitted_at'] == submitted,
            'observer provenance mismatch')
    unresolved = sorted(sg for sg in groups if not audits[sg]['full_group'])
    require(sorted(observation['errors']) == unresolved, 'observer result status does not match audited uncertainty')
    require(observation['observed_complete'] == (not unresolved), 'observer uniqueness flag mismatch')
    previous, previous_counts = -1, [0, 0]
    first_full = first_class = None
    for event in observation['history']:
        elapsed = number(event['elapsed_seconds'], 'observer elapsed')
        observed = number(event['observed_at'], 'observer timestamp')
        require(elapsed >= previous and abs(observed-submitted-elapsed) < 1e-5, 'observer clock inconsistency')
        counts = [event['classification_checkpoints'], event['full_results']]
        require(all(type(x) is int for x in counts), 'observer counts must be integers')
        require(all(a <= b <= len(groups) for a, b in zip(previous_counts, counts)), 'observer count inconsistency')
        require(counts[1] <= counts[0], 'result precedes checkpoint')
        if counts[0] == len(groups) and first_class is None: first_class = elapsed
        if counts[1] == len(groups) and first_full is None: first_full = elapsed
        previous, previous_counts = elapsed, counts
    require(first_full is not None, 'computation completion was not observed')
    require(abs(number(observation['observed_campaign_seconds'], 'campaign elapsed')-previous) < 1e-5, 'campaign elapsed inconsistency')
    peak = max(rows, key=lambda r:r['gnu_time']['maximum_resident_set_size_kib'])
    nodes = Counter(r['hostname'] for r in rows)
    return dict(schema='fspt-background-performance-v1', complete=True,
        source_id=manifest['source_id'], groups=sorted(groups), unique_full_groups=len(groups)-len(unresolved),
        groups_with_complete_marked_evidence=sum(bool(a.get('marked_witnesses', False)) for a in audits.values()),
        unresolved_upper_families=unresolved, evidence_sha256=evidence,
        observer=dict(classification_elapsed_seconds=first_class, full_elapsed_seconds=first_full,
            polling_interval_seconds=observation['polling_interval_seconds'],
            timing_scope='single login-node observer, including queue delay; computation completion is separate from uniqueness'),
        totals=dict(tasks=len(rows),
            gap_total_cpu_seconds=sum(r['gap_total_cpu_seconds'] for r in rows),
            gap_classification_cpu_seconds=sum(r['gap_classification_cpu_seconds'] for r in rows),
            process_cpu_seconds=sum(r['gnu_time']['process_cpu_seconds'] for r in rows)),
        nodes=dict(nodes), max_single_task_rss=dict(space_group=peak['space_group'], hostname=peak['hostname'],
            maximum_resident_set_size_kib=peak['gnu_time']['maximum_resident_set_size_kib'],
            maximum_resident_set_size_gib=peak['gnu_time']['maximum_resident_set_size_kib']/1024**2),
        group_measurements=rows,
        scope=dict(classification='For a nonzero background the current checkpoint follows the integrated background stacking routine, including the H0 incoming quotient when present; it is not a standalone classification benchmark.',
            rss='Maximum single-task GNU time RSS, not total concurrent node memory',
            upper='Unique abstract extension and actual marked upper phase witnesses are distinct'))
