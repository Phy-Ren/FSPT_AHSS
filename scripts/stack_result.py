#!/usr/bin/env python3
"""Stack integer combinations of marked generators from a computed SG result."""
import argparse
import json
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fspt.stacking import PresentedStackingGroup
from audit_run import check_result


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
        check_result(result)
        g=PresentedStackingGroup(result)
        left,right=json.loads(a.left),json.loads(a.right)
    except (AssertionError, KeyError, ValueError, TypeError, IndexError, OSError) as exc:
        ap.error('invalid saved result or coefficient input: '+str(exc))
    print(json.dumps(dict(marked_generators=g.generator_names,invariants=g.invariants,
        free_generator_scope=g.free_generator_scope,
        free_lattice_basis=g.free_lattice.get('latticeBasis') if g.free_lattice is not None else None,
        free_h1_coordinates=g.free_h1_coordinates,
        left=g.canonical(left),right=g.canonical(right),stacked=g.stack(left,right),
        stacked_marked=g.stack_marked(left,right),
        left_order=g.order(left),right_order=g.order(right)),indent=2))

if __name__=='__main__':main()
