"""Complete zero-background terminal product on n2=2m2 (pointwise even).
The chosen source agrees with the accepted closed-Majorana coordinate and
has the explicit new half-valued cube [m2]_2^3. All phases are numerators /16.
This file makes no assertion for odd leading n2 or nonzero backgrounds.
"""
from pathlib import Path
import sys,json
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,op,sq,adem
TERMS=json.loads(ROOT.joinpath('reference/intrinsic_terms.json').read_text())
def beta(x):return x.lift().d().div(2)
def z5(x,y):
 N=x+y;f={'a':x,'b':y,'N':N,'u':cup(x,y,3),'t':cup(x,y,2),'r':beta(x).reduce(2),
          'B':cup(y,y,1),'AN':cup(N,N,1)}
 def expr(e):
  if isinstance(e,str):return f[e]
  i,a,b=e;return cup(expr(a),expr(b),i)
 out=C(5)
 for term in TERMS:
  if term[0]=='cup':out=out+expr(term[1])
  elif term[0] in ('ternary','quarticN'):out=out+op(term[1],*(f[v] for v in term[2]))
  else:
   wd,split=term;out=out+op(wd,*([x]*split+[y]*(4-split)))
 return out

def mc_source16(x,c):return (sq(c,2)+adem(x)).lift().scaled(8)+cup(beta(x),beta(x),2).scaled(4)
def mc_product16(x,c,y,cp):
 P=beta(x);Q=beta(y);N=x+y;S=cup(x,y,3).lift();e=cup(x,y,2)
 binary=cup(c,cp,3)+cup(c.d(),cp,4)+cup(c+cp,e,3)+z5(x,y)
 integer=cup(P,Q,3)-cup(P+Q,S,2)-cup(S,beta(N),2)+cup(S,S,1)
 return binary.lift().scaled(8)+integer.scaled(4)

def root_data(m,mp):
 h=m.reduce(2);k=mp.reduce(2);g=(m-h.lift()).div(2).reduce(2)
 z=cup(h,k);v=cup(h,k,1)
 L=op('1231343',h,h,k,k)+cup(v,h)+cup(k,v)+cup(g,beta(k).reduce(2))
 return h,k,z,L

def pure16(m,mp):return root_data(m,mp)[3].lift().scaled(8)
def source16(m,u,c):
 h=m.reduce(2)
 return mc_source16(u,c)+cup(cup(h,h),h).lift().scaled(8)
def lower(m,u,c,mp,v,cp):
 h,k,z,L=root_data(m,mp)
 return m+mp,u+v,c+cp+cup(u,v,2)+z

def product16(m,u,c,mp,v,cp):
 h,k,z,L=root_data(m,mp);c0=c+cp+cup(u,v,2)
 cross=cup(c0,z,3)+cup(c0.d(),z,4)
 return mc_product16(u,c,v,cp)+(cross+L).lift().scaled(8)
def operator_coordinate16(c):return cup(c,c.d(),4).lift().scaled(8)
def operator_source16(m,u,c):return source16(m,u,c)+operator_coordinate16(c).d()
def operator_product16(m,u,c,mp,v,cp):
 M,U,F=lower(m,u,c,mp,v,cp)
 return product16(m,u,c,mp,v,cp)+operator_coordinate16(F)-operator_coordinate16(c)-operator_coordinate16(cp)

MC_DICTIONARY_WORDS=json.loads(ROOT.joinpath('stages/data/mc3_zero_dictionary.json').read_text())['words']
def raw_coordinate16(u):
 """Explicit raw-to-accepted Majorana dictionary at zero backgrounds."""
 H=C(5)
 for wd in MC_DICTIONARY_WORDS:H=H+op(wd,u,u,u,u)
 return (H+cup(u,beta(u).reduce(2),2)).lift().scaled(8)+cup(u.lift(),u.lift(),1).scaled(4)
def raw_source16(m,u,c):return source16(m,u,c)+raw_coordinate16(u).d()
def raw_product16(m,u,c,mp,v,cp):
 M,U,F=lower(m,u,c,mp,v,cp)
 return product16(m,u,c,mp,v,cp)+raw_coordinate16(U)-raw_coordinate16(u)-raw_coordinate16(v)
