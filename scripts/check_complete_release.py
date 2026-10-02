#!/usr/bin/env python3
"""Run portable release checks, formula recompilation and small end-to-end cases.

Use a compute node. Formula recompilation is optional and takes several minutes.
The output directory must be new; all generated products remain there.
"""
import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--output', required=True, type=Path)
    ap.add_argument('--gap', required=True)
    ap.add_argument('--recompile-formulas', action='store_true')
    ap.add_argument('--compiler-python', default=sys.executable, help='Python 3.9+ interpreter for the readable source compiler.')
    ap.add_argument('--skip-saved-arithmetic', action='store_true', help='Run only remaining stages after a saved-inventory check has already passed.')
    args = ap.parse_args()
    out = args.output.resolve()
    out.mkdir(parents=True, exist_ok=False)
    started = time.monotonic()
    commands = []
    def run(arguments):
        command = [sys.executable] + arguments
        commands.append(command)
        subprocess.run(command, check=True, cwd=ROOT)
    if not args.skip_saved_arithmetic:
        run(['scripts/check_full_finite_cli.py', '--output', str(out/'cli.json')])
        run(['scripts/verify_complete_results.py', '--arithmetic', '--output', str(out/'arithmetic.json')])
    compiled = []
    if args.recompile_formulas:
        sys.path.insert(0, str(ROOT))
        from fspt.full_formula.compiler import TARGETS
        for name in TARGETS:
            retained = ROOT/'fspt/data/full_formula'/(name+'.json')
            if not retained.exists(): continue
            fresh = out/'compiled'/(name+'.json')
            subprocess.run([args.compiler_python, '-m', 'fspt.full_formula.compiler', '--source', str(ROOT/'formulas/publication_source'), '--target', name, '--out', str(fresh)], check=True, cwd=ROOT)
            actual, expected = json.loads(fresh.read_text()), json.loads(retained.read_text())
            # Imported source inventory changes under the public package layout;
            # every mathematical instruction and output index must stay identical.
            assert actual['program'] == expected['program'], name
            assert actual['outputs'] == expected['outputs'], name
            assert actual['top_degree'] == expected['top_degree'], name
            assert actual['denominator'] == expected['denominator'], name
            compiled.append(dict(target=name, nodes=len(actual['program']), program_and_outputs_identical=True))
    for case in ('d1_C2_w0_s1', 'd2_E01', 'd3_C2_w1_s1', 'd4_C2_w1_s0', 'd3_PG2_half', 'd3_SG1_half'):
        run(['scripts/run_complete_example.py', '--case', case, '--output', str(out/(case+'.json')), '--gap', args.gap, '--audit'])
    report = dict(success=True, elapsed_seconds=time.monotonic()-started, saved_results_verified=0 if args.skip_saved_arithmetic else 832,
                  formula_recompilations=compiled, reproduced_cases=['d1_C2_w0_s1','d2_E01','d3_C2_w1_s1','d4_C2_w1_s0','d3_PG2_half','d3_SG1_half'],
                  scope='Independent saved integer arithmetic; exact readable-source-to-DAG bridge when requested; six fresh complete classification/stacking calculations with coherence audits.',
                  checker_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest())
    (out/'summary.json').write_text(json.dumps(report, indent=2)+'\n')
    print(json.dumps(report), flush=True)


if __name__ == '__main__': main()
