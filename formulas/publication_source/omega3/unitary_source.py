"""Fixed unitary d4 source in characteristic-B coordinates.
The inherited numerical polynomial and prism operations are not refitted.
All phase arithmetic is exact; denominators are explicitly 2,4,8,16.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,sq,op,prism_transgression,pure_parity,background_data
from compact import beta_open,integer_inputs,kappa
from explicit_pip import cartan_word,binary_completion,full_terms16,sum_terms

def blocks(n,u,c,w,y):
 a=n.reduce(2);b=beta_open(u);A,K,_,_=integer_inputs(n,w,C(1));B=b+K
 alpha=w.lift().d().div(2).reduce(2);Xi=pure_parity(n,w,C(1))
 H=(sq(c,2)+cup(w,c)+prism_transgression(u,w,C(1))+cup(u,alpha)
   +cup(kappa(u,w,C(1)),Xi,4)+y+cup(b.reduce(2),K.reduce(2),2))
 Q=(cup(B,B,2)+cup(B,B.d(),3)+cup(w.lift(),B)-cartan_word(n,w,C(1)).lift())
 P=cup(w.lift(),w.lift())+cup(w.lift(),w.lift().d(),1)
 return H,Q,cup(P,n),cup(w.lift(),cup(n,n))

def characteristic_rephasing16(n,u,w):
 _,K,_,_=integer_inputs(n,w,C(1))
 return cup(beta_open(u),K,3).scaled(4)

def high_blocks(NN,UU,CC,ww,*,accelerate=True,validate=False):
 cache={}
 def values(f):
  if f not in cache:
   def restrict(z):return C(z.deg,fun=lambda g:z(tuple(f[j] for j in g)),mod=z.mod)
   n,u,c,w=map(restrict,(NN,UU,CC,ww));s=C(1)
   if validate:
    from pip_d4 import validate_tower
    validate_tower(2,(n,u,c,w,s),7)
   y=binary_completion(n,w,s,vertices=7,accelerate=accelerate)
   try:
    bs=blocks(n,u,c,w,y);cache[f]=tuple(z(tuple(range(7))) for z in bs)
   finally:
    if hasattr(y,'engine'):y.engine.close()
  return cache[f]
 return tuple(C(6,fun=lambda f,j=j:values(f)[j],mod=2 if j==0 else None) for j in range(4))

def high_source16(NN,UU,CC,ww,*,accelerate=True,validate=False):
 H,Q,Pn,wnn=high_blocks(NN,UU,CC,ww,accelerate=accelerate,validate=validate)
 return H.lift().scaled(8)+Q.scaled(4)+Pn+wnn.scaled(2)
