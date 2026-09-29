#!/usr/bin/env python3
"""Run a published finite symmetry example with GAP; no private inputs required."""
import argparse
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.finite_examples import gap_literal, group_signature, project_result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--catalog', type=Path)
    parser.add_argument('--model')
    parser.add_argument('--dimension', type=int, choices=(3, 4))
    parser.add_argument('--output', type=Path)
    parser.add_argument('--gap', default=os.environ.get('AFS_GAP') or shutil.which('gap'))
    parser.add_argument('--list', action='store_true')
    parser.add_argument('--check', action='store_true', help='Compare final groups with the published result.')
    parser.add_argument('--q8-square', action='store_true', help='Replay the extra Q8 4+1D square certificate.')
    args = parser.parse_args()
    catalog_path = args.catalog
    if catalog_path is None:
        candidates = [ROOT / 'results/finite_examples/models.json', ROOT / 'publication/finite_examples/models.json']
        catalog_path = next((p for p in candidates if p.is_file()), None)
    if catalog_path is None:
        parser.error('Provide --catalog /path/to/models.json.')
    catalog = json.loads(catalog_path.read_text())
    if args.list:
        for model in catalog['models']:
            print(model['id'], ','.join(str(x) + '+1D' for x in model['verified_dimensions']))
        return
    if args.model is None or args.dimension is None or args.output is None:
        parser.error('--model, --dimension, and --output are required unless --list is used.')
    model = next((m for m in catalog['models'] if m['id'] == args.model), None)
    if model is None or args.dimension not in model['verified_dimensions']:
        parser.error('Model/dimension is not in the verified catalog; use --list.')
    if args.q8_square and (args.model != 'Q8_w0_s0' or args.dimension != 4):
        parser.error('--q8-square requires --model Q8_w0_s0 --dimension 4.')
    if not args.gap:
        parser.error('Set AFS_GAP, provide --gap, or place GAP on PATH.')
    args.output.parent.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix='fspt-finite-') as directory:
        work = Path(directory)
        inp = {k: model[k] for k in ('id', 'group', 'order', 'productTable', 's1', 'omega2', 'generatorIndices')}
        (work / 'models.g').write_text('AFS4_TABLE_MODELS:=' + gap_literal([inp]) + ';;\n')
        runner = 'run_finite_3d.g' if args.dimension == 3 else 'run_dimension4.g'
        if args.q8_square:
            runner = 'verify_finite_q8_4d.g'
        settings = {'AFS_ROOT': str(ROOT), 'AFS4_MODEL_FILE': str(work / 'models.g'),
                    'AFS4_MODEL_ID': model['id'], 'AFS_OUT': str(work / 'raw.json')}
        driver = 'AFS_STACK_AUDIT:=true;;\nAFS4_USE_PHASE_CYCLES:=true;;\n'
        driver += ''.join(key + ':=' + gap_literal(value) + ';;\n' for key, value in settings.items())
        driver += 'Read(Concatenation(AFS_ROOT,"/gap/' + runner + '"));\n'
        (work / 'driver.g').write_text(driver)
        process = subprocess.Popen([args.gap, '-q', '-r', '-b', '-T', str(work / 'driver.g')],
                                   stdout=subprocess.PIPE, stderr=subprocess.STDOUT,
                                   universal_newlines=True, bufsize=1)
        sentinel = 'AFS_FINITE_3D_COMPLETE' if args.dimension == 3 else 'AFS_DIMENSION4_COMPLETE'
        if args.q8_square:
            sentinel = 'AFS_Q8_FULL_GROUP_SQUARE_PASS'
        complete, error = False, False
        for line in process.stdout:
            print(line, end='', flush=True)
            complete = complete or sentinel in line
            error = error or line.startswith(('Error,', 'Syntax error:'))
        if process.wait() or not complete or error:
            raise SystemExit('GAP computation failed or lacked its completion marker.')
        raw = json.loads((work / 'raw.json').read_text())
        result = ({k: v for k, v in raw.items() if k not in ('cpuMs', 'source_id')}
                  if args.q8_square else project_result(raw, args.dimension, model['id']))
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    if args.check:
        expected_path = (catalog_path.parent / 'certificates/Q8_w0_s0_square.json' if args.q8_square else
                         catalog_path.parent / 'results' / ('d%d_%s.json' % (args.dimension, model['id'])))
        expected = json.loads(expected_path.read_text())
        signature = (lambda r: {k: r[k] for k in ('filtration', 'fullGroupInvariants', 'projectedSquare')}) if args.q8_square else group_signature
        if signature(result) != signature(expected):
            raise SystemExit('Computed groups differ from the published result.')
        print('PASS published finite-example groups')


if __name__ == '__main__':
    main()
