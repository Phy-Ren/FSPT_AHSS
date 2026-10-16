#!/usr/bin/env python3
"""Compute complete internal cyclic 4+1D roots and independent physical pairing.

Uses the adopted four-data local API. Each case runs in a bounded subprocess
and retains its exact cycle/gauge ledger, independent eta kernel, hashes, and
logs. No crystalline spin or general intrinsic cochain solver is inferred.
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import gzip
import io
import json
import os
from pathlib import Path
import platform
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insulator.cyclic4p1 import calculate
from insulator.cyclic_physical import compare_physical
from scripts.classify import source_manifest, write_json

ORDERS = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 18]


def manifest():
    result = source_manifest()
    for path in sorted((ROOT / 'formulas/v015_reference').rglob('*')):
        if path.is_file() and path.suffix in ('.py', '.json', '.md', '.tex'):
            result['files'][str(path.relative_to(ROOT))] = hashlib.sha256(path.read_bytes()).hexdigest()
    provenance = ROOT / 'formulas/v015_provenance.json'
    if provenance.is_file():
        result['files'][str(provenance.relative_to(ROOT))] = hashlib.sha256(provenance.read_bytes()).hexdigest()
    result['sha256'] = hashlib.sha256(json.dumps(result['files'], sort_keys=True,
                                                separators=(',', ':')).encode()).hexdigest()
    return result


def input_record(order):
    return {'id': 'internal_cyclic_{}_4p1'.format(order), 'dimension': 4,
            'family': 'internal_cyclic', 'order': order, 's': 0, 'rho': 0, 'omega': '0',
            'physicalSpin': 'not_applicable', 'crystallineSpinConvention': 'not_assumed',
            'orderedFields': ['e_2', 'n_2', 'n_4', 'nu_5'],
            'intrinsicRowIncluded': False, 'intrinsicR0Included': False}


def uniform_response(relative_torsion):
    return {
        'intrinsicFreeRank': 2, 'intrinsicBasis': ['I', 'J'],
        'fullGroup': {'torsion': relative_torsion, 'freeRank': 2},
        'section': 'Give each symmetry-independent I or J root the trivial C_N action; equivalently pull back along B(U1f x C_N) -> BU1f.',
        'splitting': 'Forgetting C_N composed with this section is the identity, so the full physical group is canonically the relative kernel plus Z I plus Z J.',
        'zeroLowerLift': {'background': 's=rho=omega=0', 'intrinsicInputs': [[1, 0], [0, 1]],
                         'lowerFields': {'e_2': 0, 'n_2': 0, 'n_4': 0, 'nu_5': 0},
                         'check': 'B=0; all primary, charge, and terminal terms in the reviewed intrinsic formulas vanish on these inputs.',
                         'evidenceType': 'Direct zero-input substitution and the physical natural section, not an intrinsic formula-runtime execution.'},
        'cochainIntrinsicImplemented': False,
        'scope': 'Separate physical natural-section statement for the direct product only; the recorded cochain campaign is the original four-data relative theory.'}


def write_evidence(directory, evidence, evidence_format):
    if evidence_format == 'json':
        path = directory / 'cycle_evidence.json'
        write_json(path, evidence)
    elif evidence_format == 'json-gzip':
        path = directory / 'cycle_evidence.json.gz'
        with path.open('wb') as raw:
            with gzip.GzipFile(filename='', mode='wb', fileobj=raw, mtime=0, compresslevel=6) as compressed:
                with io.TextIOWrapper(compressed, encoding='utf-8') as stream:
                    json.dump(evidence, stream, sort_keys=True, separators=(',', ':'))
                    stream.write('\n')
    else:
        raise ValueError('Unknown evidence format')
    return path


def case_worker(order, directory, expected_source, cache, evidence_format='json'):
    current = manifest()
    if current['sha256'] != expected_source:
        raise RuntimeError('The immutable source snapshot changed before the case')
    inputs = json.loads((directory / 'input.json').read_text())
    if inputs != input_record(order):
        raise RuntimeError('Case input does not match the requested order')
    run = json.loads((directory / 'run.json').read_text())
    if run['sourceSHA256'] != expected_source:
        raise RuntimeError('Run metadata has the wrong source hash')
    start = time.monotonic()
    classification, evidence, stats = calculate(order, cache=cache)
    evidence_path = write_evidence(directory, evidence, evidence_format)
    evidence_hash = hashlib.sha256(evidence_path.read_bytes()).hexdigest()
    evidence_record = {'path': evidence_path.name, 'sha256': evidence_hash,
                       'cycleTerms': classification['cycleTerms'],
                       'scope': 'All normalized periodic-cycle terms with actual complete states, powers and sheet/charge gauges.'}
    # Always retain the computed mathematics before consulting a physical
    # reference. A mismatch must be preserved as evidence, not erase roots.
    write_json(directory / 'computed_result.json', {
        'input': inputs, 'classification': classification, 'evidence': evidence_record,
        'run': dict(run, status='computed', elapsedSeconds=round(time.monotonic()-start, 6), cache=stats)})
    try:
        physical = compare_physical(order, classification['presentation'])
    except ArithmeticError as error:
        physical = {'status': 'FAIL', 'exactRelationLatticeMatch': False, 'error': str(error),
                    'scope': 'Computed root presentation retained; physical comparison failed.'}
    if manifest() != current:
        raise RuntimeError('The source snapshot changed during the case')
    if hashlib.sha256((directory / 'input.json').read_bytes()).hexdigest() != run['inputSHA256']:
        raise RuntimeError('Case input changed during execution')
    passed = physical['status'] == 'PASS'
    run.update(status='complete' if passed else 'calibration_failed', exitCode=0 if passed else 2,
               elapsedSeconds=round(time.monotonic()-start, 6),
               finishedUTC=datetime.now(timezone.utc).isoformat(), cache=stats)
    write_json(directory / 'result.json', {
        'schema': 'u1-cyclic-4p1-complete-roots-v1', 'input': inputs,
        'classification': classification, 'physicalComparison': physical,
        'uniformResponse': uniform_response(classification['torsion']),
        'evidence': evidence_record,
        'run': run})
    write_json(directory / 'run.json', run)
    return run


def launch(order, output, source, timeout, cache, evidence_format='json'):
    inputs = input_record(order)
    directory = output / inputs['id']
    directory.mkdir()
    write_json(directory / 'input.json', inputs)
    command = [sys.executable, str(Path(__file__).resolve()), '--worker-order', str(order),
               '--worker-directory', str(directory), '--worker-source', source['sha256'],
               '--cache', 'on' if cache else 'off', '--evidence-format', evidence_format]
    run = {'id': inputs['id'], 'status': 'running', 'host': platform.node(),
           'python': sys.version, 'command': command,
           'startedUTC': datetime.now(timezone.utc).isoformat(),
           'sourceSHA256': source['sha256'],
           'inputSHA256': hashlib.sha256((directory / 'input.json').read_bytes()).hexdigest(),
           'timeoutSeconds': timeout}
    write_json(directory / 'run.json', run)
    start = time.monotonic()
    with (directory / 'stdout.log').open('w') as stdout, (directory / 'stderr.log').open('w') as stderr:
        try:
            completed = subprocess.run(command, cwd=ROOT, stdout=stdout, stderr=stderr,
                                       timeout=timeout, env=dict(os.environ, PYTHONDONTWRITEBYTECODE='1'))
            code = completed.returncode
        except subprocess.TimeoutExpired:
            code = 124
    if code:
        written = json.loads((directory / 'run.json').read_text())
        if written.get('status') == 'calibration_failed':
            run = written
        run.update(status='timeout' if code == 124 else run['status'] if run['status'] == 'calibration_failed' else 'failed', exitCode=code,
                   elapsedSeconds=round(time.monotonic()-start, 6))
        if (directory / 'result.json').is_file():
            (directory / 'result.json').rename(directory / 'unaccepted_result.json')
        write_json(directory / 'run.json', run)
        return run
    run = json.loads((directory / 'run.json').read_text())
    result = json.loads((directory / 'result.json').read_text())
    if run['status'] != 'complete' or result['physicalComparison']['status'] != 'PASS':
        raise RuntimeError('A successful subprocess did not retain a complete accepted result')
    if hashlib.sha256((directory / result['evidence']['path']).read_bytes()).hexdigest() != result['evidence']['sha256']:
        raise RuntimeError('Case evidence hash mismatch')
    return run


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--order', type=int, action='append', help='Repeat for selected orders; default is the reviewed 14-order campaign')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=600)
    parser.add_argument('--cache', choices=('on', 'off'), default='on')
    parser.add_argument('--evidence-format', choices=('json', 'json-gzip'), default='json',
                        help='Losslessly compress complete cycle witnesses for larger batches')
    parser.add_argument('--worker-order', type=int, help=argparse.SUPPRESS)
    parser.add_argument('--worker-directory', type=Path, help=argparse.SUPPRESS)
    parser.add_argument('--worker-source', help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args.worker_order is not None:
        record = case_worker(args.worker_order, args.worker_directory, args.worker_source, args.cache == 'on', args.evidence_format)
        return record['exitCode']
    orders = args.order or ORDERS
    if not args.output or any(n < 1 for n in orders) or len(orders) != len(set(orders)) or args.jobs < 1 or args.timeout < 1:
        parser.error('Use a new output directory, distinct positive orders, and positive jobs/timeout')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = manifest()
    write_json(output / 'source.json', source)
    write_json(output / 'selection.json', orders)
    rows = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = {pool.submit(launch, n, output, source, args.timeout, args.cache == 'on', args.evidence_format): n
                   for n in sorted(orders, reverse=True)}
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            write_json(output / 'summary.json', sorted(rows, key=lambda r: int(r['id'].split('_')[2])))
            print(row['id'], row['status'], row['elapsedSeconds'], flush=True)
    if manifest() != source:
        raise RuntimeError('Source changed during the campaign; output remains unaccepted')
    complete = len(rows) == len(orders) and all(row['status'] == 'complete' for row in rows)
    write_json(output / 'campaign.json', {'schema': 'u1-cyclic-4p1-campaign-v1',
        'status': 'complete' if complete else 'failed', 'orders': orders, 'completed': len(rows),
        'sourceSHA256': source['sha256'], 'jobs': args.jobs, 'cache': args.cache,
        'evidenceFormat': args.evidence_format,
        'scope': 'Four-data exact cyclic roots plus independent physical eta-kernel comparison; uniform I,J physical section recorded separately.'})
    return 0 if complete else 1


if __name__ == '__main__':
    raise SystemExit(main())
