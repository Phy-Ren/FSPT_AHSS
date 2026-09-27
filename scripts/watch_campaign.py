#!/usr/bin/env python3
"""Record campaign completion on one observer clock, including queue delays."""
import argparse
import fcntl
import json
from pathlib import Path
import time


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    ap.add_argument('--interval', type=float, default=10)
    ap.add_argument('--resume', action='store_true', help='Continue an interrupted observation without discarding its history')
    args = ap.parse_args()
    if args.interval < 1:
        ap.error('interval must be at least one second')
    manifest = json.loads((args.run/'campaign.json').read_text())
    expected = set(manifest['groups'])
    submitted = min(t['created'] for t in manifest['tasks'])
    history, prior = [], None
    result_path = args.run/'observation.json'
    lock = (args.run/'observation.lock').open('a')
    try:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except BlockingIOError:
        ap.error('another observer is already running')
    restarts = []
    if result_path.exists():
        if not args.resume:
            ap.error('an observation record already exists; use --resume to retain it')
        old = json.loads(result_path.read_text())
        if old['source_id'] != manifest['source_id'] or old['submitted_at'] != submitted:
            ap.error('saved observation does not belong to this campaign')
        if old['observed_complete']:
            print('Campaign completion was already observed.', flush=True)
            return 0
        history = old['history']
        restarts = old.get('observer_restarts', [])
        restarts.append(dict(resumed_at=time.time(),
                             previous_recorded_observation=history[-1]['observed_at'] if history else None))
    while True:
        now = time.time()
        files = {int(p.stem[2:]):p for p in args.run.glob('sg*.json') if '.raw.' not in p.name}
        checkpoint_count = len(list((args.run/'classification').glob('sg*.json')))
        result_count = len(expected.intersection(files))
        counts = (checkpoint_count, result_count)
        finished = expected <= files.keys()
        errors = []
        if finished:
            for sg in sorted(expected):
                d = json.loads(files[sg].read_text())
                if d['status'] != 'computed' or d['source_id'] != manifest['source_id']:
                    errors.append(sg)
        if counts != prior or finished:
            event = dict(observed_at=now, elapsed_seconds=now-submitted,
                         classification_checkpoints=checkpoint_count, full_results=result_count)
            history.append(event)
            record = dict(source_id=manifest['source_id'], submitted_at=submitted,
                          observed_complete=finished and not errors, errors=errors,
                          history=history, polling_interval_seconds=args.interval,
                          observer_restarts=restarts,
                          timing_scope='single login-node observer clock; includes queue delays; detection can lag by one polling interval while the observer is running; any observer restarts are recorded')
            if finished:
                record['observed_campaign_seconds'] = now-submitted
            temp = result_path.with_suffix('.tmp')
            temp.write_text(json.dumps(record, indent=2)+'\n')
            temp.replace(result_path)
            print(json.dumps(event), flush=True)
            prior = counts
        if finished:
            return bool(errors)
        time.sleep(args.interval)


if __name__ == '__main__':
    raise SystemExit(main())
