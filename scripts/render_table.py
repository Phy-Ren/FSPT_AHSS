#!/usr/bin/env python3
"""Render a complete audited result set as a standalone LaTeX table/PDF."""
import argparse
from collections import Counter
import json
from pathlib import Path
import subprocess

from audit_run import check_result


def group_tex(orders):
    parts = []
    for order, count in sorted(Counter(orders).items()):
        value = r'\mathbb{Z}' + ('_{%d}' % order if order else '')
        if count > 1:
            value += '^{%d}' % count
        parts.append(value)
    return r'\oplus '.join(parts) if parts else '0'


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('run', type=Path)
    ap.add_argument('--output', type=Path, required=True, help='Output .tex file')
    ap.add_argument('--pdf', action='store_true')
    args = ap.parse_args()
    if not __debug__:
        ap.error('certificate auditing requires Python without -O or PYTHONOPTIMIZE')
    rows = []
    for sg in range(1, 231):
        d = json.loads((args.run/('sg%d.json'%sg)).read_text())
        if d['space_group'] != sg:
            ap.error('result filename/group mismatch for SG%d'%sg)
        check_result(d)
        if d.get('stacking', {}).get('status') != 'computed':
            ap.error('full stacking is missing for SG%d'%sg)
        free = d['pip'].get('free_lattice')
        index = str(free['latticeIndex']) if free else ('--' if not d['pip']['free_rank'] else '?')
        factors = [d['pip']['orders'], d['majorana'], d['complex_fermion'],
                   d['bosonic'], d['stacking']['invariants']]
        rows.append(str(sg)+' & '+' & '.join('$'+group_tex(x)+'$' for x in factors)+' & '+index+r' \\')
    text = r'''\documentclass[10pt]{article}
\usepackage[a4paper,landscape,margin=16mm]{geometry}
\usepackage{amsmath,amssymb,booktabs,longtable}
\usepackage[hidelinks]{hyperref}
\title{Independent FSPT Classification and Stacking}
\author{FSPT\_AHSS}
\date{26 September 2026}
\begin{document}
\maketitle
\noindent Three spatial dimensions; physical spin-half convention;
$(-1)^s=\det$ and $\omega_{\mathrm{eff}}=0$; complete infinite affine space groups.
Translations, weak phases, and atomic fermion parity are retained.
The four decoration columns are the surviving associated-graded layers.
The full group is computed from the stacking relations.
The final column is the index of the primitive surviving free $p+ip$ lattice
in the free part of $H^1(G,\mathbb Z_s)$; a dash means there is no free factor.
A question mark would mean that the marked free lattice is unavailable.
Exact presentations, cochain data, conventions, and source hashes are in the
companion JSON files. Formula and validation scope are documented separately.
\small
\begin{longtable}{rlllllr}
\toprule
SG & $p+ip$ ($n_1$) & Majorana ($B_2$) & CF ($C_3$) & Bosonic ($\nu_4$) & Full stacking group & Free index\\
\midrule
\endfirsthead
\toprule
SG & $p+ip$ ($n_1$) & Majorana ($B_2$) & CF ($C_3$) & Bosonic ($\nu_4$) & Full stacking group & Free index\\
\midrule
\endhead
\bottomrule
\endfoot
'''+ '\n'.join(rows)+r'''
\end{longtable}
\end{document}
'''
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(text)
    if args.pdf:
        for _ in range(2):
            subprocess.run(['pdflatex', '-interaction=nonstopmode', '-halt-on-error',
                            args.output.name], cwd=args.output.parent, check=True,
                           stdout=subprocess.DEVNULL)
    print(args.output.with_suffix('.pdf') if args.pdf else args.output)


if __name__ == '__main__':
    main()
