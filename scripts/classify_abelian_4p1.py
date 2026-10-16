#!/usr/bin/env python3
"""Compute complete 4+1D four-data models for commuting finite abelian groups.

All obstruction kernels, mixed root products, incoming H^3 gauge actions, and
integer root relations are computed by GAP from the adopted local formulas.
Reference classifications are deliberately not imported by this runner.
"""
from __future__ import annotations
import argparse
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
import hashlib
import json
import math
import os
from pathlib import Path
import platform
import signal
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.classify import gap_literal, source_manifest, formula_runtime_manifest, write_json

DEFAULT = [(2, 2), (2, 4), (3, 3)]

def parse_factors(text):
    factors = tuple(int(n) for n in text.lower().replace(',', 'x').split('x'))
    if not factors or any(n < 2 for n in factors):
        raise ValueError('Use cyclic factors of order at least two, e.g. 2x4')
    return factors

def manifest():
    source = source_manifest()
    for relative in ['formulas/examples/cyclic_4p1.g', 'formulas/v015_provenance.json']:
        source['files'][relative] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    source['sha256'] = hashlib.sha256(json.dumps(source['files'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    return source

def input_record(factors):
    name = 'x'.join(map(str, factors))
    return {'id': 'internal_abelian_{}_4p1'.format(name), 'dimension': 4,
            'family': 'internal_abelian', 'referenceTarget': 'internal_abelian_' + name, 'factors': list(factors), 'order': math.prod(factors),
            's': 0, 'rho': 0, 'omega': '0', 'background': {'s': 0, 'rho': 0, 'omega': '0'},
            'physicalSpin': 'not_applicable', 'crystallineSpinConvention': 'not_assumed',
            'orderedFields': ['e_2', 'n_2', 'n_4', 'nu_5'],
            'intrinsicRowIncluded': False, 'intrinsicPair': [0, 0]}

def launch(factors, output, source, gap, python, timeout, memory, charge_primary="bar"):
    inputs = input_record(factors)
    directory = output / inputs['id']
    directory.mkdir()
    write_json(directory / 'input.json', inputs)
    native, driver = directory / 'native.json', directory / 'driver.g'
    driver.write_text('U1_ROOT:=' + gap_literal(str(ROOT)) + ';;\n'
                      'U1_FORMULA_PYTHON:=' + gap_literal(python) + ';;\n'
                      'Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n'
                      'Read(Concatenation(U1_ROOT,"/gap/abelian4p1.g"));;\n'
                      'result:=U1AbelianFourData(' + gap_literal(list(factors)) + ',' + gap_literal(charge_primary) + ');;\n'
                      'out:=OutputTextFile(' + gap_literal(str(native)) + ',false);;\n'
                      'SetPrintFormattingStatus(out,false);;WriteLine(out,U1JSON(result));;CloseStream(out);;QUIT_GAP(0);\n')
    command = [gap, '-q', '-b', '--quitonbreak', '-m', '256m', '-K', memory, str(driver)]
    run = {'id': inputs['id'], 'status': 'running', 'host': platform.node(), 'command': command,
           'startedUTC': datetime.now(timezone.utc).isoformat(), 'sourceSHA256': source['sha256'],
           'inputSHA256': hashlib.sha256((directory / 'input.json').read_bytes()).hexdigest(),
           'timeoutSeconds': timeout, 'formulaRuntime': formula_runtime_manifest(), 'chargePrimaryMode': charge_primary}
    write_json(directory / 'run.json', run)
    start = time.monotonic()
    with (directory / 'stdout.log').open('w') as stdout, (directory / 'stderr.log').open('w') as stderr:
        process = subprocess.Popen(command, stdout=stdout, stderr=stderr, cwd=ROOT, start_new_session=True)
        try:
            code = process.wait(timeout=timeout)
        except subprocess.TimeoutExpired:
            os.killpg(process.pid, signal.SIGTERM)
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                os.killpg(process.pid, signal.SIGKILL)
                process.wait()
            code = 124
    run.update(exitCode=code, elapsedSeconds=round(time.monotonic() - start, 6),
               finishedUTC=datetime.now(timezone.utc).isoformat(),
               status='timeout' if code == 124 else 'failed')
    if code == 0:
        try:
            classification = json.loads(native.read_text())
            required = {'presentation', 'witnesses', 'torsion', 'incomingRelations', 'commutatorWitnesses', 'actualGroupOrder'}
            if not required <= classification.keys():
                raise ValueError('Incomplete mathematical artifact')
        except (OSError, ValueError, TypeError, AttributeError) as error:
            # Keep the raw native file and finalize failed metadata even when
            # GAP exited successfully but emitted an invalid artifact.
            run.update(status='failed', exitCode=65, processExitCode=code,
                       artifactError='{}: {}'.format(type(error).__name__, error))
        else:
            run['status'] = 'complete'
            write_json(directory / 'result.json', {'schema': 'u1-abelian-4p1-complete-roots-v1',
                                                  'input': inputs, 'classification': classification, 'run': run})
    write_json(directory / 'run.json', run)
    return run

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--factors', action='append', type=parse_factors)
    parser.add_argument('--output', required=True, type=Path)
    parser.add_argument('--jobs', type=int, default=1)
    parser.add_argument('--timeout', type=int, default=1800)
    parser.add_argument('--memory', default='16g')
    parser.add_argument('--gap', default='gap')
    parser.add_argument('--python', default=sys.executable)
    parser.add_argument('--charge-primary', choices=('bar', 'native', 'compare'), default='bar')
    args = parser.parse_args()
    factors = args.factors or DEFAULT
    if args.jobs < 1 or args.timeout < 1 or len(factors) != len(set(factors)):
        parser.error('Use distinct factors and positive jobs/timeout')
    output = args.output.resolve()
    output.mkdir(parents=True, exist_ok=False)
    source = manifest()
    write_json(output / 'source.json', source)
    write_json(output / 'selection.json', [input_record(f)['id'] for f in factors])
    rows = []
    with ThreadPoolExecutor(max_workers=args.jobs) as pool:
        futures = [pool.submit(launch, f, output, source, args.gap, args.python, args.timeout, args.memory, args.charge_primary) for f in factors]
        for future in as_completed(futures):
            row = future.result()
            rows.append(row)
            write_json(output / 'summary.json', sorted(rows, key=lambda r: r['id']))
            print(row['id'], row['status'], row['elapsedSeconds'], flush=True)
    if manifest() != source:
        raise RuntimeError('Source snapshot changed during execution; results remain unaccepted')
    success = all(row['status'] == 'complete' for row in rows)
    write_json(output / 'campaign.json', {'status': 'complete' if success else 'incomplete',
                                        'cases': len(rows), 'sourceSHA256': source['sha256']})
    return 0 if success else 1

if __name__ == '__main__':
    raise SystemExit(main())
