from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'joint'))
from symbolic_lazy import *
sys.path.insert(0,str(ROOT/'omega3'))
from derive_loop_lower import bits_data
from loop_product import *
from cochains import zeta2
fs,nb=bits_data(4);n,u,m,v,w=fs;a=n.reduce(2);h=(n-a.lift()).div(2).reduce(2)
NN,UU,_,ww=fields_on_interval(n,u,C(3),w);A=NN.reduce(2);H=(NN-A.lift()).div(2).reduce(2)
top=tuple(range(5))
terms={'Sq2U':sq(UU,2),'wU':cup(ww,UU),'zetaAA':zeta2(A,A),'zetaWA':zeta2(ww,A),
       'mixed':cup(cup(A,A),cup(ww,A),3),'HdH':cup(H,H.d()),'alphaH':cup(ww.lift().d().div(2).reduce(2),H)}
atoms={'S2u':sq(u,2),'wu':cup(w,u),'zetaWa':zeta2(w,a),'wa2':cup(w,cup(a,a)),
       'alpha_h':cup(w.lift().d().div(2).reduce(2),h),'u_cup1du':cup(u,u.d(),1),'du_cup1u':cup(u.d(),u,1),
       'du_cup2du':cup(u.d(),u.d(),2),'w_cup1_du':cup(w,u.d(),1),
       'wa_cup2wa':cup(cup(w,a),cup(w,a),2),'w_cup1w_a':cup(cup(w,w,1),a)}
rows={};basis={};cols=list(atoms)
def vec(P):
 o=0
 for mm in P.t:
  if mm not in rows:rows[mm]=len(rows)
  o^=1<<rows[mm]
 return o
for i,name in enumerate(cols):
 col=vec(atoms[name](top));wit=1<<i
 while col:
  b=col.bit_length()-1
  if b not in basis:basis[b]=(col,wit);break
  co,wi=basis[b];col^=co;wit^=wi
out={}
for name,expr in terms.items():
 P=integrate(expr,(0,1))(top);rhs=vec(P);sol=0
 while rhs:
  b=rhs.bit_length()-1
  if b not in basis:break
  co,wi=basis[b];rhs^=co;sol^=wi
 ans=[cols[i] for i in range(len(cols)) if sol>>i&1]
 print(name,'terms',len(P.t),'=',ans,'rem',rhs.bit_count(),flush=True);out[name]={'terms':ans,'remainder':rhs.bit_count()}
Path(__file__).with_name('results').joinpath('interval_blocks.json').write_text(json.dumps(out,indent=2))
