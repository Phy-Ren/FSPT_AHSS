#!/usr/bin/env python3
"""Freeze one runtime and distribute independent space groups over PBS workers.

Only prior independent execution times affect scheduling. No result is supplied
to the numerical program, which recomputes classification and stacking together.
"""
import argparse
import hashlib
import heapq
import json
from pathlib import Path
import shutil
import time


def groups(spec):
    selected = set()
    for part in spec.split(','):
        ends = [int(x) for x in part.split('-')]
        if len(ends) == 1:
            selected.add(ends[0])
        elif len(ends) == 2 and ends[0] <= ends[1]:
            selected.update(range(ends[0], ends[1]+1))
        else:
            raise ValueError('invalid group range: '+part)
    if not selected or not selected <= set(range(1, 231)):
        raise ValueError('space groups must be in 1..230')
    return sorted(selected)


def task_id_conflicts(root, tasks):
    """Check the complete batch before writing any queue entry."""
    identifiers = {task['id'] for task in tasks}
    conflicts = []
    for ident in sorted(identifiers):
        path = root/'runs'/'tasks'/ident
        if path.exists() or path.is_symlink():
            conflicts.append(path)
    for state in ('pending', 'running', 'done'):
        for path in (root/'runs').glob('*/%s/*.json' % state):
            if path.stem in identifiers:
                conflicts.append(path)
    return sorted(set(conflicts))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--run', required=True, type=Path, help='New run directory')
    ap.add_argument('--queues', nargs='+', required=True)
    ap.add_argument('--groups', default='1-230')
    ap.add_argument('--mode', choices=['classification', 'full'], default='full')
    ap.add_argument('--crystalline-spin', choices=['half', 'spinless'], default='half')
    ap.add_argument('--timeout', type=int, default=27000,
                    help='Per-group wall-clock budget in seconds, including slow stacking tails; must fit within the allocation (default: 27000)')
    ap.add_argument('--timings', type=Path, help='Prior independent result directory')
    ap.add_argument('--source', type=Path, help='Existing immutable source snapshot')
    ap.add_argument('--prepare-only', action='store_true', help='Save plan without queuing tasks')
    args = ap.parse_args()
    if args.timeout < 1:
        ap.error('timeout must be positive')
    root = Path(__file__).resolve().parents[1]
    run = args.run.resolve()
    if run.exists():
        ap.error('run directory already exists; use a fresh name')
    try:
        selected = groups(args.groups)
    except ValueError as exc:
        ap.error(str(exc))
    if len(set(args.queues)) != len(args.queues):
        ap.error('duplicate queue names')
    slot_heaps = {}
    now = time.time()
    for queue in args.queues:
        if Path(queue).name != queue:
            ap.error('queue must be a single directory name')
        base = root/'runs'/queue
        if (base/'STOP').exists():
            ap.error('worker has a STOP marker: '+queue)
        worker = json.loads((base/'worker.json').read_text())
        if now-worker['heartbeat'] > 120:
            ap.error('worker heartbeat is stale: '+queue)
        slots = worker['slots']
        if not isinstance(slots, int) or slots < 1:
            ap.error('invalid worker slot count: '+queue)
        slot_heaps[queue] = [0.0]*slots
    cost = {}
    if args.timings:
        for path in args.timings.glob('sg*.json'):
            if '.raw.' in path.name:
                continue
            data = json.loads(path.read_text())
            if data['space_group'] in selected:
                milliseconds = data.get('total_cpu_ms', data['cpu_ms']) if args.mode == 'full' else data['cpu_ms']
                cost[data['space_group']] = max(1.0, milliseconds/1000)
    # Unfinished/unknown cases may be the slowest: start them early too.
    unknown_cost = max(cost.values(), default=1.0)
    for sg in selected:
        cost.setdefault(sg, unknown_cost)
    run.mkdir(parents=True)
    source = args.source.resolve() if args.source else run/'source'
    if not args.source:
        shutil.copytree(root/'gap', source/'gap')
    hashes = {str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest()
              for p in sorted((source/'gap').glob('*.g'))}
    if 'gap/run_one.g' not in hashes:
        ap.error('source snapshot has no gap/run_one.g')
    source_id = hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest()
    tasks = []
    for priority, sg in enumerate(sorted(selected, key=lambda x:(-cost[x], x))):
        queue = min(args.queues, key=lambda q:(slot_heaps[q][0], sum(slot_heaps[q]), args.queues.index(q)))
        finish = heapq.heappop(slot_heaps[queue])+cost[sg]
        heapq.heappush(slot_heaps[queue], finish)
        ident = '%s-p%03d-sg%03d' % (run.name, priority, sg)
        task = dict(id=ident, queue=queue, space_group=sg, estimated_seconds=cost[sg],
                    command=['/home/apps/anaconda3/bin/python3', 'scripts/run_group.py', str(sg),
                             '--mode', args.mode, '--crystalline-spin', args.crystalline_spin, '--source', str(source),
                             '--output', str(run/('sg%d.json'%sg))],
                    cwd=str(root), timeout_s=args.timeout, created=now)
        tasks.append(task)
    conflicts = task_id_conflicts(root, tasks)
    if conflicts:
        ap.error('task IDs already used; choose a different run basename: ' +
                 ', '.join(str(path) for path in conflicts))
    manifest = dict(mode=args.mode, crystalline_spin=args.crystalline_spin, groups=selected, source_snapshot=str(source),
                    source_id=source_id, source_sha256=hashes, tasks=tasks,
                    prepared_only=args.prepare_only,
                    scheduling='longest prior runtime first; least predicted slot finish',
                    predicted_empty_worker_seconds=max(max(h) for h in slot_heaps.values()),
                    scheduling_note='Estimate excludes existing worker tasks and is not a measured benchmark.')
    (run/'campaign.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    if not args.prepare_only:
        for task in tasks:
            pending = root/'runs'/task['queue']/'pending'
            pending.mkdir(parents=True, exist_ok=True)
            path = pending/(task['id']+'.json')
            if path.exists():
                raise FileExistsError(path)
            temp = path.with_suffix('.tmp')
            temp.write_text(json.dumps(task, indent=2)+'\n')
            temp.replace(path)
    print(json.dumps(dict(run=str(run), groups=len(tasks), source_id=source_id,
                          prepared_only=args.prepare_only), indent=2))


if __name__ == '__main__':
    main()
