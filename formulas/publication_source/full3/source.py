"""The fixed all-background source in characteristic B coordinates.
Internal Majorana arguments are shifted. No cochain solve is performed.
All returned phase cochains are exact integer numerators over sixteen.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'full3'))
from lower import *
from cochains import background_data,prism_transgression,pure_parity
from compact import beta_open,integer_inputs,kappa,ell
from explicit_pip import cartan_word,binary_completion,full_terms16,sum_terms

def blocks(n,u,c,w,s,y):
 """Virtual degrees 2,3,4; u is shifted, du=a^2+(w+s^2)a."""
 a=n.reduce(2);b=beta_open(u);A,K,_,_=integer_inputs(n,w,s);B=b+K
 Xi=pure_parity(n,w,s);W,_,_,_,P=background_data(w,s)
 H=(sq(c,2)+cup(w,c)+prism_transgression(u,w,s)+cup(u,ell(w,s))
    +cup(kappa(u,w,s),Xi,4)+y+cup(b.reduce(2),K.reduce(2),2)
    +cup(s,cup(b.reduce(2),K.reduce(2),3)))
 Q=(cup(B,B,2)+cup(B,B.d(),3)+cup(w.lift(),B)-cartan_word(n,w,s).lift())
 Pn=cup(P,n,s=s,twists=(0,1))
 Wnn=cup(W.lift(),cup(n,n,s=s,twists=(1,1)),s=s,twists=(1,0))
 return H,Q,Pn,Wnn

def characteristic_rephasing16(n,u,w,s):
 _,K,_,_=integer_inputs(n,w,s)
 return cup(beta_open(u),K,3).scaled(4)

def high_blocks(NN,UU,CC,ww,ss,*,accelerate=True,validate=False):
 cache={}
 def values(f):
  if f not in cache:
   def restrict(z):return C(z.deg,fun=lambda g:z(tuple(f[j] for j in g)),mod=z.mod)
   n,u,c,w,s=map(restrict,(NN,UU,CC,ww,ss))
   if validate:
    from pip_d4 import validate_tower
    validate_tower(2,(n,u+cup(s,carry(n)),c,w,s),7)
   y=binary_completion(n,w,s,vertices=7,accelerate=accelerate)
   try:cache[f]=tuple(z(tuple(range(7))) for z in blocks(n,u,c,w,s,y))
   finally:
    if hasattr(y,'engine'):y.engine.close()
  return cache[f]
 return tuple(C(6,fun=lambda f,j=j:values(f)[j],mod=2 if j==0 else None) for j in range(4))

def high_source16(NN,UU,CC,ww,ss,*,accelerate=True,validate=False):
 H,Q,Pn,Wnn=high_blocks(NN,UU,CC,ww,ss,accelerate=accelerate,validate=validate)
 return H.lift().scaled(8)+Q.scaled(4)+Pn+Wnn.scaled(2)

def source16(n,u,c,w,s,*,accelerate=True,validate=False):
 return integrate(high_source16(*fields_on_interval(n,u,c,w,s),accelerate=accelerate,validate=validate),(0,1))

def product16(n,u,c,m,v,cp,w,s,*,accelerate=True,validate=False):
 return integrate(high_source16(*fields_on_triangle(n,u,c,m,v,cp,w,s),accelerate=accelerate,validate=validate),(0,1,2))

def source_parts16(n,u,c,w,s,*,accelerate=True,validate=False):
 H,Q,_,_=high_blocks(*fields_on_interval(n,u,c,w,s),accelerate=accelerate,validate=validate)
 _,_,_,_,P=background_data(w,s)
 return integrate(H,(0,1)).lift().scaled(8),integrate(Q,(0,1)).scaled(4),cup(P,n,s=s,twists=(0,1))

def product_parts16(n,u,c,m,v,cp,w,s,*,accelerate=True,validate=False):
 H,Q,_,_=high_blocks(*fields_on_triangle(n,u,c,m,v,cp,w,s),accelerate=accelerate,validate=validate)
 W=w+cup(s,s)
 explicit=cup(W.lift(),cup(n,m,s=s,twists=(1,1)),s=s,twists=(1,0)).scaled(-2)
 return integrate(H,(0,1,2)).lift().scaled(8),integrate(Q,(0,1,2)).scaled(4),explicit
