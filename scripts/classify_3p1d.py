#!/usr/bin/env python3
"""Classify and accept the E8-inclusive 3+1D four-data model in one command.

The existing exact CI, signed E8-section and collector stages run unchanged.
Only a fully accepted four-data collection makes this workflow complete.
"""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import classify, extend_e8_3p1


def utc():
    return datetime.now(timezone.utc).isoformat()


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def write_workflow(path, record):
    temporary = path.with_name(path.name + '.partial')
    temporary.write_text(json.dumps(record, indent=2, sort_keys=True) + '\n')
    os.replace(temporary, path)


def parser():
    result = argparse.ArgumentParser(description=__doc__)
    result.add_argument('--family', choices=('point3', 'spacegroup'))
    result.add_argument('--case', action='append', help='3D catalogue ID; repeat to select cases')
    result.add_argument('--spin', choices=('spinless', 'spin_half'))
    result.add_argument('--output', required=True, type=Path, help='New workflow root containing ci/, e8/ and accepted/')
    result.add_argument('--gap', default=os.environ.get('GAP', 'gap'))
    result.add_argument('--jobs', type=int, default=1)
    result.add_argument('--pair-spins', action='store_true', help='Reuse geometry for selected spin partners')
    result.add_argument('--largest-first', action='store_true')
    result.add_argument('--timeout', type=int, default=7200,
                        help='Seconds per case; a two-case paired process has twice this total allowance')
    result.add_argument('--memory', default='8g', help='GAP memory per process, e.g. 8g')
    result.add_argument('--charge-primary', choices=('bar', 'native', 'compare'), default='native')
    result.add_argument('--phase-class', choices=('cycles', 'native', 'compare'), default='cycles')
    result.add_argument('--closed-charge-source', choices=('certified', 'reference', 'compare'), default='certified')
    result.add_argument('--vacuum-reduction', choices=('canonical', 'reference'), default='canonical')
    result.add_argument('--formula-mode', choices=('auto', 'python', 'reference'),
                        default=os.environ.get('U1_DAG_MODE', 'auto'), help='Exact formula VM dispatch; preserves Python fallback')
    return result


def preflight(args):
    if not args.family and not args.case:
        raise ValueError('Select --family or --case.')
    if args.jobs < 1 or args.timeout < 1:
        raise ValueError('jobs and timeout must be positive.')
    if not re.fullmatch(r'[1-9][0-9]*[kKmMgG]?', args.memory):
        raise ValueError('memory must be a positive GAP size such as 8g.')
    if args.formula_mode not in ('auto', 'python', 'reference'):
        raise ValueError('U1_DAG_MODE must be auto, python, or reference.')
    if args.case and len(args.case) != len(set(args.case)):
        raise ValueError('Repeated case identifiers are not allowed.')
    if args.output.exists() or args.output.is_symlink():
        raise ValueError('The output directory must be new; resume and overwrite are not supported.')
    args.output = args.output.resolve()
    gap = shutil.which(args.gap)
    if gap is None:
        raise ValueError('GAP executable was not found: ' + args.gap)
    args.gap = str(Path(gap).resolve())
    selected = []
    for path in sorted((ROOT / 'insulator_catalog/generated').glob('*.json')):
        if path.name.endswith('.index.json'):
            continue
        data = read(path)
        if args.case and data.get('id') not in args.case:
            continue
        if args.family and data.get('family') != args.family:
            continue
        if args.spin and data.get('spin') != args.spin:
            continue
        if data.get('dimension') != 3 or data.get('family') not in ('point3', 'spacegroup'):
            raise ValueError('This entrypoint accepts only 3+1D point3/spacegroup inputs.')
        if data.get('id') != path.stem:
            raise ValueError('Catalogue filename and case identity disagree: ' + str(path))
        selected.append(path)
    if not selected or args.case and set(args.case) != {p.stem for p in selected}:
        raise ValueError('Selection includes missing or incompatible catalogue cases.')
    return selected


def commands(args, selected):
    ci = [sys.executable, str(ROOT / 'scripts/classify.py'), '--output', str(args.output / 'ci'),
          '--gap', args.gap, '--jobs', str(args.jobs), '--memory', args.memory, '--timeout', str(args.timeout),
          '--charge-primary', args.charge_primary, '--phase-class', args.phase_class,
          '--closed-charge-source', args.closed_charge_source, '--vacuum-reduction', args.vacuum_reduction]
    if args.family:
        ci += ['--family', args.family]
    if args.spin:
        ci += ['--spin', args.spin]
    for option in ('pair_spins', 'largest_first'):
        if getattr(args, option):
            ci.append('--' + option.replace('_', '-'))
    # Pin the resolved selection even when the user selected an entire family.
    for path in selected:
        ci += ['--case', path.stem]
    return [('ci', ci), ('e8', [sys.executable, str(ROOT / 'scripts/extend_e8_3p1.py'),
                               '--ci-root', str(args.output / 'ci'), '--output', str(args.output / 'e8')]),
            ('acceptance', [sys.executable, str(ROOT / 'scripts/collect_expansion.py'),
                            '--ci-root', str(args.output / 'ci'), '--e8-root', str(args.output / 'e8'),
                            '--output', str(args.output / 'accepted')])]


def check_accepted(root, selected):
    """Bind workflow completion to the exact collector outputs and selected IDs."""
    collection = read(root / 'collection.json')
    if collection.get('accepted') is not True or not collection.get('collections'):
        raise ValueError('Collector did not produce an accepted collection.')
    expected = {path.stem: read(path)['family'] for path in selected}
    seen, hashes = set(), {'collection.json': digest(root / 'collection.json')}
    family_paths = {'point3': '3p1d/point_groups', 'spacegroup': '3p1d/space_groups'}
    for item in collection['collections']:
        family = item.get('family')
        if family not in family_paths or item.get('path') != family_paths[family]:
            raise ValueError('Collector returned a collection outside the selected 3+1D domain.')
        folder = root / item['path']
        required = {'results.json', 'ci_results.json', 'validation.json', 'provenance.json'}
        if set(item.get('filesSHA256', {})) != required:
            raise ValueError('Collector output manifest is incomplete.')
        for name, value in item['filesSHA256'].items():
            if digest(folder / name) != value:
                raise ValueError('Accepted output hash mismatch: ' + name)
            hashes[item['path'] + '/' + name] = value
        records = read(folder / 'results.json')
        ids = [record['input']['id'] for record in records]
        validation = read(folder / 'validation.json')
        if (len(ids) != len(set(ids)) or set(ids) & seen or len(ids) != item['count']
                or validation.get('accepted') is not True
                or validation.get('completeResultCount') != len(ids)
                or set(validation.get('selectedCases', [])) != set(ids)
                or validation.get('missingOrFailedSelectedCases') != []
                or any(expected.get(case) != family for case in ids)):
            raise ValueError('Collector did not accept the exact selected cases.')
        for record in records:
            c = record['classification']
            if (c.get('orderedFields') != ['e_1', 'n_1', 'n_3', 'nu_4']
                    or c.get('neutralE8Included') is not True
                    or c.get('physicalClassificationCertified') is not False):
                raise ValueError('Accepted record does not retain the selected four-data scope.')
        seen.update(ids)
    if seen != set(expected):
        raise ValueError('Accepted output omits selected cases.')
    return hashes


def run_workflow(args, selected):
    source = classify.source_manifest()
    e8_source = extend_e8_3p1.source_manifest()
    runtime = classify.formula_runtime_manifest()
    runtime['requestedMode'] = args.formula_mode
    inputs = {path.stem: digest(path) for path in selected}
    env = dict(os.environ, U1_DAG_MODE=args.formula_mode)
    args.output.mkdir(parents=True, exist_ok=False)
    logs = args.output / 'logs'
    logs.mkdir()
    record = {'schema': 'u1-3p1-four-data-workflow-v1', 'status': 'running', 'stage': 'ci',
              'startedUTC': utc(), 'spacetimeDimension': '3+1',
              'orderedFields': ['e_1', 'n_1', 'n_3', 'nu_4'],
              'scope': 'E8-inclusive selected 3+1D four-data model', 'physicalClassificationCertified': False,
              'selectedCases': [p.stem for p in selected], 'inputSHA256': inputs,
              'classifierSource': source, 'e8Source': e8_source, 'formulaRuntime': runtime,
              'workflowSHA256': digest(Path(__file__)), 'pythonVersion': sys.version,
              'cwd': str(ROOT), 'output': str(args.output), 'stages': []}
    path = args.output / 'workflow.json'
    start = time.monotonic()
    write_workflow(path, record)
    current = None
    try:
        for name, command in commands(args, selected):
            record['stage'] = name
            current = {'name': name, 'status': 'running', 'command': command, 'startedUTC': utc(),
                       'stdout': 'logs/' + name + '.stdout.log', 'stderr': 'logs/' + name + '.stderr.log'}
            record['stages'].append(current)
            write_workflow(path, record)
            print(name + ': running', flush=True)
            stage_start = time.monotonic()
            with (args.output / current['stdout']).open('wb') as out, (args.output / current['stderr']).open('wb') as err:
                result = subprocess.run(command, cwd=ROOT, env=env, stdout=out, stderr=err)
            current.update(exitCode=result.returncode, endedUTC=utc(),
                           elapsedSeconds=round(time.monotonic() - stage_start, 6))
            if result.returncode:
                raise RuntimeError(name + ' exited with status ' + str(result.returncode))
            if name in ('ci', 'e8'):
                selection = read(args.output / name / 'selection.json')
                if len(selection) != len(set(selection)) or set(selection) != set(inputs):
                    raise ValueError(name + ' did not retain the exact selection.')
            current['status'] = 'succeeded'
            write_workflow(path, record)
        record['stage'] = 'verify_accepted'
        write_workflow(path, record)
        accepted = check_accepted(args.output / 'accepted', selected)
        runtime_after = classify.formula_runtime_manifest()
        runtime_after['requestedMode'] = args.formula_mode
        if (classify.source_manifest() != source or extend_e8_3p1.source_manifest() != e8_source
                or runtime_after != runtime or any(digest(p) != inputs[p.stem] for p in selected)):
            raise ValueError('Source, runtime or catalogue input changed during the workflow.')
        if read(args.output / 'ci/source.json') != source or read(args.output / 'ci/formula_runtime.json') != runtime:
            raise ValueError('CI runtime/source provenance differs from the workflow snapshot.')
        if any(digest(args.output / 'ci' / case / 'input.json') != value for case, value in inputs.items()):
            raise ValueError('CI input bytes differ from the initial catalogue snapshot.')
        recorded_e8_source = read(args.output / 'e8/source.json')
        if (any(recorded_e8_source.get(key) != value for key, value in e8_source.items())
                or recorded_e8_source.get('ciSelectionSHA256') != digest(args.output / 'ci/selection.json')):
            raise ValueError('E8 provenance differs from the workflow source or CI selection.')
        record.update(status='complete', stage='complete', exitCode=0, acceptedCount=len(inputs),
                      acceptedRoot=str(args.output / 'accepted'), acceptedFilesSHA256=accepted,
                      endedUTC=utc(), elapsedSeconds=round(time.monotonic() - start, 6))
        write_workflow(path, record)
        print('complete: accepted %d E8-inclusive 3+1D cases at %s' % (len(inputs), args.output / 'accepted'), flush=True)
        return 0
    except (Exception, KeyboardInterrupt) as error:
        code = 130 if isinstance(error, KeyboardInterrupt) else 1
        if current is not None and current['status'] == 'running':
            current['status'] = 'failed'
            current.setdefault('exitCode', None)
            current.setdefault('endedUTC', utc())
            current['error'] = {'type': type(error).__name__, 'message': str(error)}
        record.update(status='interrupted' if code == 130 else 'failed', exitCode=code,
                      error={'type': type(error).__name__, 'message': str(error)},
                      endedUTC=utc(), elapsedSeconds=round(time.monotonic() - start, 6))
        write_workflow(path, record)
        print(record['status'] + ' at ' + record['stage'] + ': ' + str(error), file=sys.stderr, flush=True)
        return code


def main(argv=None):
    cli = parser()
    args = cli.parse_args(argv)
    try:
        selected = preflight(args)
    except (ValueError, OSError) as error:
        cli.error(str(error))
    return run_workflow(args, selected)


if __name__ == '__main__':
    raise SystemExit(main())
