#!/usr/bin/env python3
"""Independent review checks for the D2d E(1) audit and its actual C2 retract."""
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
import hashlib,json,runpy
import sympy as sp
root=Path(__file__).parent
with redirect_stdout(StringIO()):n=runpy.run_path(root/'d2d_ext_audit.py')
r=sp.Matrix([[0,-1,0],[1,0,0],[0,0,-1]])
s=sp.diag(1,-1,-1)
assert r**4==sp.eye(3) and s**2==sp.eye(3) and s*r*s==r**-1
j=s*r
assert j**2==sp.eye(3) and j.det()==-1
# r has u=1,v=0; s has u=0,v=1; j=sr has u=v=1.
# Therefore a=u restricts to t, b=u+v restricts to0, w2(W) restricts to0.
g=n['Q0'].__globals__
checks=0
for spin,w2 in [('spinless',n['add'](n['w'],n['mul'](n['v'],n['v']))),('spin_half',n['zero'])]:
 g['w2']=w2;n['differential'].cache_clear()
 for ss in range(10):
  for stem in range(7):
   t=ss+stem
   src=n['cells'](ss,t);nexti={x:i for i,x in enumerate(n['cells'](ss+1,t+1))}
   left_map=[1<<nexti[x] for x in src]
   desti={x:i for i,x in enumerate(n['cells'](ss+2,t+1))}
   right_map=[1<<desti[x] for x in n['cells'](ss+1,t)]
   for index in range(len(src)):
    lhs=n['apply'](n['differential'](ss+1,t+1),left_map[index])
    rhs=n['apply'](right_map,n['differential'](ss,t)[index])
    assert lhs==rhs
   checks+=1
# At spin-half the actual spectrum retract has module projection b,w ->0.
def projection(p):return frozenset(m for m in p if m[1]==0 and m[2]==0)
for d in range(12):
 for monomial in n['basis'](d):
  p=frozenset({monomial})
  for Q in [n['Q0'],n['Q1']]:
   assert projection(Q(p))==Q(projection(p))
   checks+=1
oldbasis=g['basis']
def retract_basis(d):return () if d<0 else ((d,0,0),)
g['basis']=retract_basis
n['cells'].cache_clear();n['differential'].cache_clear()
retract={str(stem):[n['ext'](ss,stem) for ss in range(8)] for stem in range(6)}
retract_h0=[n['h0_rank'](ss,4) for ss in range(4)]
assert retract['4']==[1,1,1,0,0,0,0,0]
assert retract['3']==retract['5']==[0]*8
assert retract_h0==[1,1,0,0]
result={
 'status':'PASS',
 'reviewed_script_sha256':hashlib.sha256((root/'d2d_ext_audit.py').read_bytes()).hexdigest(),
 'primary_source':'Debray v3, dihedral.tex lines52–69 and dihedral_spinless_0mod4.tex lines30–43: x=v,y=u,w=w2(W), relationu²+uv; Sq1(w)=vw.',
 'spatial_matrices':{'r':[[int(x) for x in row] for row in r.tolist()],'s':[[int(x) for x in row] for row in s.tolist()],'section_C2_generator_sr':[[int(x) for x in row] for row in j.tolist()]},
 'representation_check':'V=W+(u+v), w1(V)=u, w2(V)=w+uv+v²; inverse spinless twist has w2=w+v². Spin-half det(V)-1 has w1=u,w2=0.',
 'h0_chain_map_and_retract_checks':checks,
 'spin_half_retract_Ext':retract,
 'spin_half_retract_h0_stem4':retract_h0,
 'differentials':'Spinless stem4 occupies filtrations0,1; no incoming dr for r>=2 and no outgoing target in stem3. Spin-half only possible incoming target in stem4 filtration2 belongs to actual split BC2 Thom summand. Its stem3 and stem5 vanish, so its Z8 tower survives. Complementary stem4 consists of two filtration0 classes and has no possible differentials.',
 'extensions':'Spinless h0 acts as0 and filtration>=2 vanishes, so all three ku4 classes have order2. Spin-half the actual spectrum splitting gives an independent Z8; complementary ku4 has only filtration0 and isZ2². Add independent ku0=Z2 viaABP in both cases.',
 'full_Spin_c_degree4':{'spinless':[2,2,2,2],'spin_half':[2,2,2,8]}
}
(root/'d2d_peer_oh.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
