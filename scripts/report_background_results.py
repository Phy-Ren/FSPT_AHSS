#!/usr/bin/env python3
"""Report strictly audited spinless results, preserving upper-extension uncertainty.

Example after the accepted archive exists:
  python3 scripts/report_background_results.py results/space_groups_spinless \
    --output results/space_groups_spinless/report --tex

Development inputs require --allow-partial. A malformed available result is
always rejected before the new report directory is created. No reference
answer is loaded.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

from audit_background_run import audit, write_report


def tex_group(orders):
    if orders is None:
        return r'\text{missing}'
    if not orders:
        return '0'
    counts = Counter(orders)
    factors = []
    for x in sorted(counts):
        factor = r'\mathbb{Z}' if x == 0 else r'\mathbb{Z}_{%d}' % x
        if counts[x] > 1:
            factor += '^{%d}' % counts[x]
        factors.append(factor)
    return r'\oplus '.join(factors)


def write_tex(report, output):
    rows = {row['space_group']: row for row in report['rows']}
    lines = [r'\documentclass[10pt]{article}', r'\usepackage[landscape,margin=12mm]{geometry}',
             r'\usepackage{amsmath,amssymb,longtable}', r'\begin{document}',
             r'\section*{Spinless crystalline space groups}',
             r'Crystalline: $s_{\rm crys}=\omega_{\rm crys}=0$. Internal: '
             r'$s=w_1(V)$, $\omega=w_2(V)+w_1(V)^2$. Full infinite affine symmetry is retained.',
             r'An abstract upper-extension group does not specify an actual marked upper relation. '
             r'``Native'' denotes retained native lifts or their exact reconstruction recipes; the report does not rerun bar operations.',
             r'\small\begin{longtable}{r|lllll|rrl}',
             r'SG & $p+ip$ & MC & CF & Boson & Full group / family & Free index & H0 order & Evidence\\\hline\endhead']
    for n in range(1, 231):
        row = rows.get(n)
        if row is None:
            lines.append('%d & -- & -- & -- & -- & -- & -- & -- & Missing\\\\' % n)
            continue
        groups = row['invariants']
        full = tex_group(groups) if groups is not None else r'\{'+', '.join(tex_group(x) for x in row['invariant_options'] or [])+r'\}'
        values = [tex_group(row['layers'][key]) for key in ('pip', 'majorana', 'complex_fermion', 'bosonic')]+[full]
        label = 'Native marked' if row['marked_witnesses'] else ('Abstract only' if row['full_group'] else 'Unresolved family')
        lines.append('%d & %s & %s & %s & %s\\\\' % (n, ' & '.join('$'+v+'$' for v in values),
            (row['free_lattice'] or {}).get('index', '--'), row.get('h0_quotient', {}).get('incoming_order', '--'), label))
    lines.extend([r'\end{longtable}', r'\end{document}'])
    (output/'space_groups.tex').write_text('\n'.join(lines)+'\n')


def generate(run, output, allow_partial=False, tex=False):
    if not __debug__:
        raise ValueError('run without Python -O: mathematical checks use assertions')
    if output.exists() or output.is_symlink():
        raise ValueError('report output already exists')
    report, failed = audit(run, allow_partial=allow_partial)
    if failed:
        raise ValueError('strict background audit refused report: '+json.dumps(
            {'errors': report['errors'], 'missing': report['missing']}, sort_keys=True))
    if not report['rows']:
        raise ValueError('no strictly audited results to report')
    if len(report['source_ids']) != 1:
        raise ValueError('report requires one uniform source snapshot')
    report['reporter_sha256'] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    report['partial_report'] = bool(report['missing'])
    write_report(report, output)
    if tex:
        write_tex(report, output)
    return {'output': str(output), 'groups': report['groups_passed'],
            'partial': report['partial_report'], 'source_id': report['source_ids'][0],
            'kinds': report['kinds'], 'all_230_full_groups_determined': report['all_230_full_groups_determined'],
            'all_230_marked_witnesses_complete': report['all_230_marked_witnesses_complete']}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('run', type=Path)
    parser.add_argument('--output', type=Path, required=True)
    parser.add_argument('--allow-partial', action='store_true')
    parser.add_argument('--tex', action='store_true', help='Also write standalone LaTeX source')
    args = parser.parse_args(argv)
    try:
        result = generate(args.run, args.output, args.allow_partial, args.tex)
    except (OSError, ValueError, AssertionError, KeyError, TypeError) as exc:
        print('Background report refused: '+str(exc), file=sys.stderr)
        return 2
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
