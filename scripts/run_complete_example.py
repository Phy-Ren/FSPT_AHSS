#!/usr/bin/env python3
"""Recompute one published input with the complete serial classification/stacking engine."""
import argparse
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--list', action='store_true')
    ap.add_argument('--case', help='Record ID from results/complete_formulas/index.json')
    ap.add_argument('--output', type=Path)
    ap.add_argument('--gap', default=os.environ.get('AFS_GAP'))
    ap.add_argument('--python', default=sys.executable)
    ap.add_argument('--audit', action='store_true', help='Also run the engine coherence audit; its recorded selection can be expensive.')
    ap.add_argument('--dry-run', action='store_true', help='Print the exact command without computing.')
    args = ap.parse_args()
    index = json.loads((ROOT/'results/complete_formulas/index.json').read_text())
    if args.list:
        for r in index['cases']: print(r['id'], r['invariant_factors'], ','.join(r['collections']))
        return
    if not args.case or not args.output: ap.error('--case and --output are required')
    matches = [r for r in index['cases'] if r['id'] == args.case]
    if not matches: ap.error('Unknown record ID: ' + args.case)
    r = matches[0]
    saved = json.loads((ROOT/r['result']).read_text())
    if 'space_group' in r:
        cmd = [args.python, str(ROOT/'scripts/run_full_space_group.py'), str(r['space_group']), '--crystalline-spin', r['crystalline_spin']]
    elif 'point_group_index' in r:
        cmd = [args.python, str(ROOT/'scripts/run_full_point_group.py'), str(r['point_group_index']), '--crystalline-spin', r['crystalline_spin']]
    else:
        cmd = [args.python, str(ROOT/'scripts/run_full_finite.py'), '--catalog', str(ROOT/r['input_catalog']), '--model', r['model'], '--dimension', str(r['dimension'])]
        coordinate = r['formula_coordinate']
        if coordinate in ('majorana-ca', 'majorana-operator'): cmd += ['--coordinate', coordinate]
        if saved.get('zeroChiralFiber'): cmd += ['--zero-chiral-fiber']
        for key, flag in [('canonicalFaceCache','canonical-face-cache'), ('certifiedZeroLowerSources','certified-zero-lowers'), ('certifiedCubePrimitive','certified-cube-primitive'), ('certifiedBinaryPrimitive','certified-binary-primitive'), ('certifiedCFSquare','certified-cf-square'), ('certifiedCharacterMajorana','certified-character-mc'), ('vacuumMajoranaKernel','vacuum-mc-kernel'), ('vacuumFermionKernel','vacuum-cf-kernel'), ('binaryExtensionNormalizationRequested','normalize-binary-extension')]:
            if saved.get(key) is True: cmd += ['--' + flag]
    for key, flag in [('majoranaN0Kernel','mc-n0-kernel'), ('fermionN0Kernel','cf-n0-kernel'), ('formulaIntegerVectorCache','vector-request-cache'), ('pureCFSource3Kernel','pure-cf-source'), ('n0Source3Kernel','n0-source'), ('closedCFSource','closed-cf-source'), ('f2ParityFilter','f2-parity-filter')]:
        if saved.get(key) is True: cmd += ['--' + flag]
    for key, flag in [('cfPrimaryEvaluation','cf-primary'), ('mcPrimaryEvaluation','mc-primary')]:
        if saved.get(key) in ('bar','native','compare'): cmd += ['--' + flag, saved[key]]
    cache = saved.get('partialMajoranaCache', {})
    if isinstance(cache, dict) and cache.get('limit', 0): cmd += ['--mc-partial-cache-limit', str(cache['limit'])]
    cmd += ['--output', str(args.output.resolve()), '--python', args.python]
    if args.gap: cmd += ['--gap', args.gap]
    if args.audit: cmd += ['--audit']
    print(shlex.join(cmd), flush=True)
    if args.dry_run: return
    subprocess.run(cmd, check=True, cwd=ROOT)
    result = json.loads(args.output.read_text())
    sys.path.insert(0, str(ROOT))
    from fspt.result_validation import verify_result
    checked = verify_result(result)
    if checked['invariant_factors'] != r['invariant_factors']:
        raise SystemExit('Fresh result differs from the published group: ' + repr(checked['invariant_factors']))
    print(json.dumps(dict(status='reproduced', record_id=r['id'], invariant_factors=checked['invariant_factors'])))


if __name__ == '__main__': main()
