"""Cached exact unitary kernel. Only immutable single-state values are cached."""
from transfer_model import *
from fractional import pair_data,fractional_seed16,cartan_word,binary_H,upper_residual,background_data
from compact import kappa
from cochains import pure_parity
from functools import lru_cache
TOP=tuple(range(7))
ACCELERATE=True

def one_key(n,u,w):
 return tuple(tuple(x(f) for f in faces(6,x.deg)) for x in (n,u,w))
def source_degenerate(n,u,w):
 # An ordinary simultaneous simplicial degeneracy of these three cochains.
 originals=one_key(n,u,w)
 for i in range(6):
  ff=tuple(j for j in range(7) if j!=i+1)
  projection=tuple(ff[j if j<=i else j-1] for j in range(7))
  if all(tuple(x(tuple(projection[z] for z in f)) for f in faces(6,x.deg))==vv for x,vv in zip((n,u,w),originals)):return True
 return False
@lru_cache(maxsize=20000)
def Yvalue(nn,ww):
 n=C(2,values=dict(zip(faces(6,2),nn)),mod=None);w=C(2,values=dict(zip(faces(6,2),ww)));s=C(1)
 n.closed=w.closed=True
 y=binary_completion(n,w,s,vertices=7,accelerate=ACCELERATE)
 try:return y(TOP)
 finally:
  if hasattr(y,'engine'):y.engine.close()
@lru_cache(maxsize=20000)
def Hvalue(key):
 nn,uu,ww=key
 n=C(2,values={f:v for f,v in zip(faces(6,2),nn) if v},mod=None)
 u=C(3,values={f:v for f,v in zip(faces(6,3),uu) if v})
 w=C(2,values={f:v for f,v in zip(faces(6,2),ww) if v});n.closed=w.closed=True
 if source_degenerate(n,u,w):return 0
 y=C(6,values={TOP:Yvalue(nn,ww)})
 return binary_H(n,u,w,C(1),y)(TOP)
@lru_cache(maxsize=20000)
def rho(S):
 if S[0]!=6:raise ValueError(S[0])
 n,u,m,v,w=decode(S);s=C(1)
 if not any(S[1]):return kernel(S)
 D=pair_data(n,u,m,v,w,s);N,U=D['N'],D['U'];B,Bp,BN=D['B'],D['Bp'],D['BN'];W,vi,alpha,hv,P=background_data(w,s)
 ef=fractional_seed16(n,u,m,v,w,s,native=False)
 V=(ef-cup(W.lift(),D['T']).scaled(2)).div(4).reduce(2)
 Q=lambda x:cup(x,x,2)+cup(x,x.d(),3)
 I=(Q(BN)-Q(B)-Q(Bp)+cup(w.lift(),D['lambda'].d()-D['R'])
    -cartan_word(N,w,s).lift()+cartan_word(n,w,s).lift()+cartan_word(m,w,s).lift()
    +cup(W.lift(),D['R'])-cup(vi,D['T'])-V.lift().d())
 HH=Hvalue(one_key(N,U,w))^Hvalue(one_key(n,u,w))^Hvalue(one_key(m,v,w))
 F=kappa(u,w,s)+pure_parity(n,w,s);Fp=kappa(v,w,s)+pure_parity(m,w,s);e=third_product(n,u,m,v,w,s)
 change=(binary_correction(N,U,w,s)+binary_correction(n,u,w,s)+binary_correction(m,v,w,s)
         +cup(w,D['R'].reduce(2))+cup(alpha,D['t']))
 return (upper_residual(F,Fp,e,w)(TOP)+HH+I.div(2).reduce(2)(TOP)+change(TOP))%2

def mixed_cell(S):
 n,u,m,v,w=decode(S)
 return cup(w,cup(n.reduce(2),m.reduce(2)))(TOP)

def rho_compatible(S):return (rho(S)+mixed_cell(S))%2
