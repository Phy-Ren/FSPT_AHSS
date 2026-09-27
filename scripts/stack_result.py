#!/usr/bin/env python3
"""Stack integer combinations of marked generators from a computed SG result."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fspt.stacking import PresentedStackingGroup, UnresolvedStacking
from audit_run import check_result
from audit_background_run import check_background_result


def main():
    ap=argparse.ArgumentParser(description=__doc__)
    ap.add_argument('result',type=Path)
    ap.add_argument('--left',default='{}',help='JSON coefficients, e.g. {"P1":1}')
    ap.add_argument('--right',default='{}',help='JSON coefficients, e.g. {"C1":2}')
    a=ap.parse_args()
    if not __debug__:
        ap.error('certificate auditing requires Python without -O or PYTHONOPTIMIZE')
    try:
        result=json.loads(a.result.read_text())
        # Annihilating relation rows alone does not prove that Smith coordinates
        # preserve the group: a zero column transform would annihilate everything.
        if result.get('convention') == 'physical-spinless-det-sign-Pin-minus':
            check_background_result(result, strict_background=True)
        else:
            check_result(result)
        g=PresentedStackingGroup(result)
        left,right=json.loads(a.left),json.loads(a.right)
        answer=dict(marked_generators=g.generator_names,invariants=g.invariants,
            free_generator_scope=g.free_generator_scope,
            free_lattice_basis=g.free_lattice.get('latticeBasis') if g.free_lattice is not None else None,
            free_h1_coordinates=g.free_h1_coordinates,
            marked_reduction=g.marked_reduction,
            left=g.canonical(left),right=g.canonical(right),stacked=g.stack(left,right),
            stacked_marked=g.stack_marked(left,right),
            left_order=g.order(left),right_order=g.order(right))
    except (AssertionError, KeyError, ValueError, TypeError, IndexError, OSError, UnresolvedStacking) as exc:
        ap.error('invalid saved result or coefficient input: '+str(exc))
    print(json.dumps(answer,indent=2))

if __name__=='__main__':main()
