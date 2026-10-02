"""Exact finite background transfer for the lambda=1 lower-product branch.
The phase formula is enabled only together with e4_new=e4_old+a cup b.
It is not the unitary extension of the old lambda=0 lower product.
"""
from kernel_cached import *
from collections import Counter

@lru_cache(maxsize=10000)
def Zunit(S):
 if S[0]!=5:raise ValueError(S[0])
 if not any(S[1]):return Zstar0(S)
 chain={S};answer=0
 for r in range(6):
  if not chain:return answer%2
  # This explicitly finite perturbation formula includes its terminal base-zero pieces.
  zero_part={Q for Q in chain if not any(Q[1])}
  for Q in zero_part:answer+=Zstar0(Q)
  chain-=zero_part
  if not chain:return answer%2
  for Q in chain:
   answer+=Lstar(Q)
   for T in H(Q):answer+=rho_compatible(T)
  chain=deltaH(chain)
 raise ArithmeticError('Background filtration did not terminate in degree five')

def Z(n,u,m,v,w):
 return C(5,fun=lambda f:Zunit(encode(*[C(x.deg,fun=lambda g,x=x:x(tuple(f[i] for i in g)),mod=x.mod) for x in (n,u,m,v,w)],5)))

def square_pair_primitive(n,u,m,v,w):
 a=n.reduce(2);b=m.reduce(2);h=zero.half_floor(n).reduce(2)
 return zero.zeta(a,b)+cup(u,b)+cup(a,v)+cup(h,cup(b,b,1))+cup(cup(w,a,1),b)

def old_lower(n,u,m,v,w):return zero_NUe(n,u,m,v,w)

def source48(n,u,c,w,*,accelerate=True):
 s=C(1)
 def ev(f):
  def R(x):return C(x.deg,fun=lambda g:x(tuple(f[i] for i in g)),mod=x.mod)
  nn,uu,cc,ww=map(R,(n,u,c,w));nn.closed=ww.closed=True
  yy=binary_completion(nn,ww,s,vertices=7,accelerate=accelerate)
  try:
   Ostar=star_source16(nn,uu,cc,ww,s,binary_y=yy)
   G=cup(uu,nn.reduce(2)).lift().scaled(8)+cubic_coordinate16(nn,uu,ww,s)
   # B/APS = star + n^3/3 + dG + w*a^2/2.
   O=Ostar.scaled(3)+cup(cup(nn,nn),nn).scaled(16)+G.d().scaled(3)+cup(ww,cup(nn.reduce(2),nn.reduce(2))).lift().scaled(24)
   return O(TOP)%48
  finally:
   if hasattr(yy,'engine'):yy.engine.close()
 return C(6,fun=ev,mod=None)

def phase48(n,u,c,m,v,cp,w):
 s=C(1);N,U,e=old_lower(n,u,m,v,w);z=cup(n.reduce(2),m.reduce(2));cold=c+cp+e
 upper=upper_seed16(c,cp,e);frac=seed16(n,u,m,v,w)
 shift=cup(cold,z,3)+cup(cold.d(),z,4)+square_pair_primitive(n,u,m,v,w)
 binary=Z(n,u,m,v,w)
 def G(nn,uu):return cup(uu,nn.reduce(2)).lift().scaled(8)+cubic_coordinate16(nn,uu,w,s)
 cubq=cup(n,m,1);cubic=(cup(m-n,cubq)-cup(cubq,m-n)).scaled(16)
 extra=G(N,U)-G(n,u)-G(m,v)
 wt=cup(w,cup(n.reduce(2),m.reduce(2),1)).lift().scaled(24)
 total=(upper+frac).scaled(3)+(shift+binary).lift().scaled(24)+cubic+extra.scaled(3)+wt
 return C(5,fun=lambda f:total(f)%48,mod=None)

def stack(n,u,c,m,v,cp,w):
 N,U,e=old_lower(n,u,m,v,w);z=cup(n.reduce(2),m.reduce(2))
 return N,U,c+cp+e+z,phase48(n,u,c,m,v,cp,w)

def collected_blocks(n,u,c,m,v,cp,w):
 """The displayed short phase, in a stated pair-coboundary gauge."""
 from cochains import background_data,sq
 from fractional import relative_B
 a=n.reduce(2);b=m.reduce(2);h=zero.half_floor(n).reduce(2);k=zero.half_floor(m).reduce(2)
 N,U,e=old_lower(n,u,m,v,w);z=cup(a,b);t=cup(a,b,1);q=cup(a,b,2)
 B=relative_B(n,u,w,C(1));Bp=relative_B(m,v,w,C(1));r=B.reduce(2);rp=Bp.reduce(2)
 la=(U.lift()-u.lift()-v.lift()+cup(n,m,1)).div(2);l=la.reduce(2);R=cup(b,a);D=l.d()+R
 _,_,alpha,hw,_=background_data(w,C(1))
 J=zero.zeta(b,a)+cup(v,a)+cup(b,u)+cup(cup(w,b,1),a)+cup(k,cup(a,a,1))
 V=(cup(r,rp,3)+cup(r.d(),rp,4)+cup(r+rp,D,3)+cup(r.d()+rp.d(),D,4)
    +sq(l,2)+cup(R,l.d(),3)+cup(w,l)+cup(hw+alpha,q)+J)
 Phi=(zero.zeta(a,b)+cup(a,cup(b,b)+cup(w,b),1)+cup(h,cup(b,b,1))
      +cup(cup(w,a,1),b)+cup(t,a+b)+cup(w,t))
 Pi=(cup(N,U.lift())-cup(n,u.lift())-cup(m,v.lift())
     +cup(cup(n,w.lift(),1),m)+cup(cup(m,w.lift(),1),n))
 C0=c+cp+e
 eps=(cup(c,cp,3)+cup(c.d(),cp,4)+cup(c+cp,e,3)+cup(C0,z,3)+cup(C0.d(),z,4))
 nq=cup(n,m,1);cub=cup(m-n,nq)-cup(nq,m-n)
 nonbinary=(eps+Phi).lift().scaled(24)+(V.lift()+Pi).scaled(12)+cup(w.lift(),nq).scaled(6)+cub.scaled(16)
 return {'nonbinary48':nonbinary,'pair_gauge4':cup(a,v,1).lift().scaled(24),
         'V5':V,'Phi5':Phi,'Pi5':Pi,'epsilon5':eps}

def neat_phase48(n,u,c,m,v,cp,w):
 D=collected_blocks(n,u,c,m,v,cp,w)
 total=D['nonbinary48']+Z(n,u,m,v,w).lift().scaled(24)
 return C(5,fun=lambda f:total(f)%48,mod=None)
