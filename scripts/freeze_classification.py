#!/usr/bin/env python3
"""Freeze independently computed layers before looking at external answers."""
import argparse
import hashlib
import json
from pathlib import Path
import time

from audit_run import check_result


def signature(d):
    return [d['pip']['orders'], d['majorana'], d['complex_fermion'], d['bosonic']]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('output', type=Path)
    ap.add_argument('--run', type=Path, action='append', required=True)
    args = ap.parse_args()
    if args.output.exists():
        ap.error('frozen output already exists')
    selected, candidates = {}, {}
    for run in args.run:
        paths = sorted(run.glob('sg*.json'))+sorted((run/'classification').glob('sg*.json'))
        for path in paths:
            if '.raw.' in path.name:
                continue
            d = json.loads(path.read_text())
            if d.get('classification_status', d['status']) != 'computed':
                continue
            d.pop('stacking', None)
            d['status'] = 'computed'
            if 'source_sha256' not in d:
                source = Path(d['source_snapshot'])
                d['source_sha256'] = {
                    str(p.relative_to(source)):hashlib.sha256(p.read_bytes()).hexdigest()
                    for p in sorted((source/'gap').glob('*.g'))}
            check_result(d)
            sg = d['space_group']
            if sg in selected and signature(d) != signature(selected[sg]):
                raise ValueError('independent classifications disagree for SG%d'%sg)
            origin = dict(path=str(path.resolve()), sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                          source_id=d['source_id'], checkpoint=d.get('checkpoint_stage'))
            candidates.setdefault(sg, []).append(origin)
            selected[sg] = d
            d['classification_origin'] = origin
    missing = sorted(set(range(1, 231))-selected.keys())
    if missing:
        print(json.dumps(dict(computed=len(selected), missing=missing)))
        return 1
    args.output.mkdir(parents=True)
    hashes = {}
    for sg, d in sorted(selected.items()):
        path = args.output/('sg%d.json'%sg)
        path.write_text(json.dumps(d, indent=2, sort_keys=True)+'\n')
        hashes[path.name] = hashlib.sha256(path.read_bytes()).hexdigest()
    manifest = dict(groups=230, frozen_at=time.time(), external_answers_consulted=False,
                    result_sha256=hashes, independent_candidates=candidates,
                    scope='four associated-graded layers; free p+ip rank, not a marked surviving lattice')
    (args.output/'manifest.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
    print('FROZEN independent classification of all 230 space groups:', args.output)
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
