#!/usr/bin/env python3
"""Exhaustive pointwise checks for the extra Majorana root of Z4f x Z2.

Uses the published closed-Majorana operations, with additive phases represented
by integer numerators modulo eight. No terminal p+ip operation is used.
Run: python verify_abelian_z4f_z2.py [--formula-repo /path/to/FSPT_AHSS]
"""
import argparse, json, sys
from itertools import product
from pathlib import Path
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--formula-repo', type=Path,
                    default=Path(__file__).resolve().parents[3],
                    help='Formula checkout; defaults to this repository.')
args = parser.parse_args()
formula_repo = args.formula_repo.resolve()
sys.path.insert(0, str(formula_repo))
from fspt.formulas import field, zero, cup, phase, evaluate, majorana_source
from fspt.majorana_complete import obstruction, stacking

a,b=field('a',1),field('b',1)
a2,a3,a4=a*a,a*a*a,a*a*a*a
b2,b4=b*b,b*b*b*b
w=a2
n3=a2*b
n4=a2*b2
nu=phase((2,a3*b2),(3,a*b4))
B4=phase((2,a3*b))
checks={
 'Incoming Majorana secondary obstruction vanishes':obstruction(a2,zero(3),w,zero(1)),
 'Majorana primary obstruction vanishes':majorana_source(n3,w,zero(1)),
 'Majorana phase has explicit primitive':(obstruction(n3,zero(4),w,zero(1))-nu.differential()).reduce(8),
 'Majorana phase has two terms':(obstruction(n3,zero(4),w,zero(1))-phase((4,a4*b2),(6,a2*b4))).reduce(8),
 'Majorana self-stacking complex decoration':(cup(n3,n3,2)-n4).reduce(2),
 'Majorana self-stacking phase':(stacking(n3,zero(4),n3,zero(4),w,zero(1))-phase((4,a4*b))).reduce(8),
 'Two copies give the stated complex lift':(nu.scale(2)+stacking(n3,zero(4),n3,zero(4),w,zero(1))-phase((6,a*b4))-B4.differential()).reduce(8),
 'Complex lift solves its obstruction':(obstruction(zero(3),n4,w,zero(1))-phase((6,a*b4)).differential()).reduce(8),
 'Complex self-stacking phase vanishes':stacking(zero(3),n4,zero(3),n4,w,zero(1)),
 'Four copies give the bosonic root':(phase((6,a*b4)).scale(2)-phase((4,a*b4))).reduce(8),
}
results=[]
for name,expr in checks.items():
 count=0
 for edges in product(range(4),repeat=expr.degree):
  verts=[0]
  for g in edges:verts.append(verts[-1]^g)
  fs={'a':lambda f:(verts[f[0]]^verts[f[1]])&1,
      'b':lambda f:((verts[f[0]]^verts[f[1]])>>1)&1}
  assert evaluate(expr,fs)==0,(name,edges,evaluate(expr,fs))
  count+=1
 results.append({'check':name,'ordered_tuples':count,'passed':True})
print(json.dumps({'group':'Z4f x Z2','checks':results},indent=2))
