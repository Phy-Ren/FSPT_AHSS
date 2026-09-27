#!/usr/bin/env python3
"""Compare saved mathematical outputs exactly across performance-only changes.

Only the named top-level execution/provenance fields are excluded. All saved
generator fields, primitives, relations, Smith transforms, and free lattices
are compared literally. This does not re-evaluate arbitrary bar simplices.
"""
import argparse
import hashlib
import json
from pathlib import Path

from audit_run import check_complete_witnesses


EXECUTION_FIELDS = {
    'cpu_ms', 'total_cpu_ms', 'free_pip_cpu_ms', 'started', 'finished',
    'wall_seconds', 'stage_timings', 'resolution_timings', 'libraries',
    'source_id', 'source_sha256', 'source_snapshot',
    'generic_pip_compiled', 'generic_pip_compiled_calls',
    'native_mod2_contraction', 'native_mod2_cache_degrees',
    'binary_bar_mod2', 'closed_cf_obstruction',
}


def differences(a, b, path='$', limit=12):
    if type(a) is not type(b):
        return [path + ' (type)']
    if isinstance(a, dict):
        found = []
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                found.append(path + '.' + key + ' (missing)')
            else:
                found.extend(differences(a[key], b[key], path + '.' + key, limit))
            if len(found) >= limit:
                break
        return found[:limit]
    if isinstance(a, list):
        if len(a) != len(b):
            return [path + ' (length)']
        found = []
        for i, (x, y) in enumerate(zip(a, b)):
            found.extend(differences(x, y, '%s[%d]' % (path, i), limit))
            if len(found) >= limit:
                break
        return found[:limit]
    return [] if a == b else [path]


def load(root):
    results = {}
    for sg in range(1, 231):
        path = root / ('sg%d.json' % sg)
        if not path.exists():
            continue
        payload = path.read_bytes()
        value = json.loads(payload)
        if value['space_group'] != sg:
            raise ValueError('filename and group differ: %s' % path)
        check_complete_witnesses(value, 'normalized-pip-aw-edge-transport-v2')
        results[sg] = (value, hashlib.sha256(payload).hexdigest())
    return results


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('baseline', type=Path)
    ap.add_argument('candidate', type=Path)
    ap.add_argument('--allow-partial', action='store_true')
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if not __debug__:
        ap.error('certificate auditing requires Python without -O')
    left, right = load(args.baseline), load(args.candidate)
    compared = sorted(left.keys() & right.keys())
    mismatches, evidence = {}, {}
    for sg in compared:
        a, b = left[sg][0], right[sg][0]
        am = {k:v for k, v in a.items() if k not in EXECUTION_FIELDS}
        bm = {k:v for k, v in b.items() if k not in EXECUTION_FIELDS}
        paths = differences(am, bm)
        if paths:
            mismatches[sg] = paths
        evidence[sg] = dict(baseline_sha256=left[sg][1], candidate_sha256=right[sg][1],
                            baseline_source=a['source_id'], candidate_source=b['source_id'])
    missing_left = sorted(set(range(1, 231)) - left.keys())
    missing_right = sorted(set(range(1, 231)) - right.keys())
    report = dict(baseline=str(args.baseline.resolve()), candidate=str(args.candidate.resolve()),
                  groups_compared=len(compared), groups_equal=len(compared)-len(mismatches),
                  mismatches=mismatches, missing_baseline=missing_left, missing_candidate=missing_right,
                  complete=not missing_left and not missing_right,
                  excluded_top_level_execution_fields=sorted(EXECUTION_FIELDS), evidence=evidence,
                  scope='literal equality of all other saved fields; bar cochain equations are not rerun',
                  external_answers_consulted=False)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    tmp = args.output.with_suffix('.tmp')
    tmp.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    tmp.replace(args.output)
    print(json.dumps({k:report[k] for k in ['groups_compared', 'groups_equal', 'mismatches', 'complete']}, sort_keys=True))
    return bool(mismatches or (not args.allow_partial and not report['complete']))


if __name__ == '__main__':
    raise SystemExit(main())
