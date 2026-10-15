"""Exact primitive Spin^c response lattice and formal transgression audit."""
from fractions import Fraction as F
from pathlib import Path
import json,hashlib

def values(x,y): return ((F(x)-F(y))/48,F(x)/2)
a=values(8,8)             # CP3, determinant c=2h
b=values(6,6)             # CP2 x S2, c=h+2u
c=values(64,16)           # CP3, c=4h
assert a==(0,4) and b==(0,3) and c==(1,32)
u=tuple(x-y for x,y in zip(a,b))
v=tuple(x-32*y for x,y in zip(c,u))
assert u==(0,1) and v==(1,0)
# Characteristic polynomial coordinates are (coefficient of c^3, of c*p1).
index=lambda q:(F(q**3,48),F(-q,48))
J=tuple(a-3*b for a,b in zip(index(3),index(1)))
assert J==(F(1,2),0)
# (n_IQH,e_E8) response polynomials: IQH=c²/8-p1/24, E8=-p1/3.
# Formal d3(c)=-2B. These equalities do not prove an integral AHSS operation.
dI=(F(-1,8),F(1,24));dJ=(F(-3),F(0))
assert dI==(-F(1,8),F(1,24))
assert dJ==(-24*F(1,8),24*F(1,24)-3*F(1,3))
source=Path('/home/arxiv/1604.06527/positive.arxiv6.tex')
result={'status':'PASS','response_basis':{'I':'(c^3-c*p1)/48','J':'c^3/2 = Index(D tensor L)-3Index(D)'},'manifold_evaluations':{'CP3_c2h':[str(x) for x in a],'CP2xS2_c_h_plus_2u':[str(x) for x in b],'CP3_c4h':[str(x) for x in c]},'primitive_cycles':{'U=CP3_c2h-CP2xS2_c_h_plus_2u':[str(x) for x in u],'V=CP3_c4h-32U':[str(x) for x in v]},'Spin_restriction':'I=J=0 at c=0; TP5(Spin)=0','coefficient_system':'Z_rho1^2','formal_transgression_candidate_E8_first':{'I':[0,-1],'J':[3,-24],'common_factor':'B=beta(omega)','status':'formal characteristic-polynomial identity only; not a proved integral AHSS differential'},'primary_source':{'arxiv':'1604.06527v6','tex_lines':'6576-6613; Eq74 and Eq115','sha256':hashlib.sha256(source.read_bytes()).hexdigest()},'scope':'Integral response basis uses Dirac-index integrality and the published Spin^c bordism coefficient rank; arithmetic is independent of stored classifier outputs.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
