#!/usr/bin/env python3
"""Assemble immutable runs; later certificates may replace equal earlier answers."""
import argparse
import json
from pathlib import Path
import time


def layers(d):
    return [d['pip']['orders'], d['majorana'], d['complex_fermion'], d['bosonic']]


ap = argparse.ArgumentParser()
ap.add_argument('output')
ap.add_argument('--run', action='append', required=True,
                help='Input run, in increasing certificate preference order')
args = ap.parse_args()
selected, history = {}, {}
for run in args.run:
    for path in sorted(Path(run).resolve().glob('sg*.json')):
        if '.raw.' in path.name:
            continue
        data = json.loads(path.read_text())
        n = data['space_group']
        history.setdefault(n, []).append(str(path))
        if n in selected:
            old, oldpath = selected[n]
            if layers(old) != layers(data):
                raise ValueError('classification changed for SG%d: %s versus %s' % (n, oldpath, path))
            oldfree = old['pip'].get('free_lattice', {})
            newfree = data['pip'].get('free_lattice', {})
            if oldfree and newfree and oldfree['latticeIndex'] != newfree['latticeIndex']:
                raise ValueError('primitive free lattice index changed for SG%d' % n)
            if old.get('stacking', {}).get('status') == 'computed':
                if data.get('stacking', {}).get('status') != 'computed':
                    continue
                if old['stacking']['invariants'] != data['stacking']['invariants']:
                    raise ValueError('stacking changed for SG%d: %s versus %s' % (n, oldpath, path))
                if old['stacking'].get('fullUpperPhaseWitness') is True and data['stacking'].get('fullUpperPhaseWitness') is not True:
                    continue
                if (old['stacking'].get('fullUpperPhaseWitness') == data['stacking'].get('fullUpperPhaseWitness')
                        and oldfree.get('fullFreePhaseWitness') is True
                        and newfree.get('fullFreePhaseWitness') is not True):
                    continue
        selected[n] = data, path

out = Path(args.output).resolve()
if any(out == Path(run).resolve() for run in args.run):
    raise ValueError('output must be separate from immutable input runs')
out.mkdir(parents=True, exist_ok=True)
for n, (data, path) in selected.items():
    target = out/('sg%d.json' % n)
    temp = target.with_suffix('.tmp')
    temp.write_text(json.dumps(data, indent=2, sort_keys=True)+'\n')
    temp.replace(target)
manifest = dict(created=time.time(), input_runs=args.run, groups=len(selected),
                selected={n: str(path) for n, (data, path) in sorted(selected.items())},
                candidate_history=history, missing=sorted(set(range(1, 231))-selected.keys()))
(out/'assembly.json').write_text(json.dumps(manifest, indent=2, sort_keys=True)+'\n')
print('Assembled', len(selected), 'groups; all overlapping answers agree.')
