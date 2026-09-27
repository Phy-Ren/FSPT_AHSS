#!/usr/bin/env python3
"""Compare targeted finite bar controls to the unmodified 64-model archive."""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def differences(a, b, path=''):
    if type(a) is not type(b):
        return [(path, a, b)]
    if isinstance(a, dict):
        out = [(path+'/'+k, a.get(k, '<missing>'), b.get(k, '<missing>'))
               for k in sorted(a.keys() ^ b.keys())]
        for key in sorted(a.keys() & b.keys()):
            out.extend(differences(a[key], b[key], path+'/'+key))
        return out
    if isinstance(a, list):
        if len(a) != len(b):
            return [(path, a, b)]
        return [d for i, (x, y) in enumerate(zip(a, b))
                for d in differences(x, y, path+'/'+str(i))]
    return [] if a == b else [(path, a, b)]


def reason(path, a, b, lower_only=False):
    if not lower_only:
        if path in ('/cpu_ms', '/total_cpu_ms'):
            return 'Measured CPU time changes when support checks are enabled.'
        if re.fullmatch(r'/stage_timings/\d+/cpu_ms', path):
            return 'Stage CPU timestamp; all stage names and their order remain compared.'
        if path == '/resolution_timings/finiteResolutionCpuMs':
            return 'Measured finite-resolution CPU time.'
    prefix = '' if lower_only else '/stacking/lower'
    if re.fullmatch(re.escape(prefix)+r'/witnesses/\d+/checkedComparisonSupport', path):
        assert a is False and b is True, 'Audit flag must become a demonstrated check.'
        return 'Additional explicit comparison-support verification, false to true only.'
    raise AssertionError('Unexplained numerical/witness difference: '+path)


def compare(formal, controls, tasks):
    campaign = json.loads((formal/'campaign.json').read_bytes())
    spec = json.loads((controls/'controls.json').read_bytes())
    assert campaign['source_id'] == spec['source_id']
    hashes = {str(p.relative_to(controls/'source')): digest(p)
              for p in sorted((controls/'source/gap').glob('*.g'))}
    assert hashes == spec['source_sha256'] == campaign['source_sha256']
    assert hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest() == spec['source_id']
    jobs = []
    for task in spec['tasks']:
        directory = tasks/task['id']
        status = json.loads((directory/'status.json').read_bytes())
        assert status['status'] == 'done' and status['exit_code'] == 0
        assert status['command'] == task['command'] and status['timeout_s'] == task['timeout_s']
        log = directory/'stdout.txt'
        if not log.exists():
            log = directory/'stdout.log'
        jobs.append({'id': task['id'], 'status_sha256': digest(directory/'status.json'),
                     'metrics_sha256': digest(directory/'metrics.txt'), 'stdout_sha256': digest(log)})
    assert len(jobs) == 4
    rows = []
    for number in (10, 20, 22):
        filename = 'spinless_pg%d.raw.json' % number
        left, right = formal/filename, controls/filename
        a, b = json.loads(left.read_bytes()), json.loads(right.read_bytes())
        ignored = [{'path': p, 'original': x, 'control': y, 'reason': reason(p, x, y)}
                   for p, x, y in differences(a, b)]
        rows.append({'point_group_index': number, 'formal_file': filename,
                     'formal_sha256': digest(left), 'control_file': filename,
                     'control_sha256': digest(right), 'unexplained_differences': 0,
                     'ignored_differences': ignored})
    c4file = controls/'c4_bar.json'
    c4 = json.loads(c4file.read_bytes())
    a = json.loads((formal/'spinless_pg10.raw.json').read_bytes())['stacking']['lower']
    b = copy.deepcopy(c4['lower'])
    # Only the full driver renames this legacy provenance field. The custom
    # bar harness deliberately preserves the original exporter spelling.
    certificate = b['finalFiltrationCertificate']
    assert certificate.pop('spaceGroup') == 10 and 'pointGroupIndex' not in certificate
    certificate['pointGroupIndex'] = 10
    ignored = [{'path': p, 'original': x, 'control': y, 'reason': reason(p, x, y, True)}
               for p, x, y in differences(a, b)]
    assert c4['options'] == {'stackAudit': True, 'closedCF': False,
                             'mod2Contraction': False, 'mod2Bar': False,
                             'compiledCA': False, 'backgroundProjectedCup0': False}
    assert all(type(x) is int and x > 0 for x in c4['checks'].values())
    return {'schema': 'point-group-marked-control-comparison-v1', 'source_id': spec['source_id'],
            'formal_campaign_sha256': digest(formal/'campaign.json'),
            'scope': 'All numerical fields and actual native witnesses compared. No reference answer table read. Point22 retains the original upper-carry scope; lower support checks do not complete unknown upper carries.',
            'controls': rows, 'tasks': jobs,
            'c4_full_bar': {'result_sha256': digest(c4file), 'unexplained_differences': 0,
                           'ignored_differences': ignored,
                           'provenance_key_alias': {'spaceGroup': 'pointGroupIndex', 'value': 10},
                           'checks': c4['checks'], 'options': c4['options'],
                           'literal_square_coordinates': c4['literalSquareCoordinates']}}


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--formal', type=Path, required=True)
    ap.add_argument('--controls', type=Path, required=True)
    ap.add_argument('--tasks', type=Path, required=True)
    ap.add_argument('--output', type=Path, required=True)
    args = ap.parse_args()
    if args.output.exists() or args.output.is_symlink():
        ap.error('refuse existing output')
    result = compare(args.formal, args.controls, args.tasks)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+'\n')
    print('PASS 3 marked-driver controls and exhaustive C4 bar control; no unexplained differences')


if __name__ == '__main__':
    main()
