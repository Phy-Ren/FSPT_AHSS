"""4+1D full-background terminal source and corrected multiplication.
The binary transfer is a finite chain formula. No primitive solve is called.
The only physical lower product exported here includes [n]_2 cup [m]_2.
"""
from kernel_full import *
from fractions import Fraction

def carry(n):return (n-n.reduce(2).lift()).div(2).reduce(2)
def lower(n,u,m,v,w,s):
 a=n.reduce(2);b=m.reduce(2)
 return n+m,u+v+cup(a,b,1),third_product(n,u,m,v,w,s)+cup(a,b)

def negation_pair(x,y):
 """The new (1,2,2) tensor coefficient, a three-group parity polynomial.
 Floors are mathematical floors, also on negative integers.
 """
 a,h,g=x%2,(x//2)%2,(x//4)%2
 b,k,l=y%2,(y//2)%2,(y//4)%2
 return ((a+h)*k*(1+b)+h*(b+l)+g*b*(1+k))%2

def Ls(S):
 if S[0]!=5:raise ValueError(S[0])
 ss=field(S,1)((0,1));x=field(S,3)((1,2,3));y=field(S,5)((3,4,5))
 return ss*negation_pair(x,y)%2

def L(S):return (Lzero(S)+Ls(S))%2

@lru_cache(maxsize=5000)
def Zvalue(S):
 if S[0]!=5:raise ValueError(S[0])
 if not normalized(S):return 0
 if not any(S[1]) and not any(S[2]):return Zzero(S)
 chain={S};answer=0
 for iteration in range(6):
  if not chain:return answer%2
  # Sum normalized chains before invoking the expensive source: many cuts
  # cancel exactly. This is an optimization of the same finite sum.
  hchain=set()
  for T in chain:
   answer^=L(T)
   for Q in H(T):xor_add(hchain,Q)
  for Q in hchain:answer^=rho(Q)
  chain=deltaH(chain)
 if chain:raise ArithmeticError('Background filtration did not terminate')
 return answer%2

def binary_phase(n,u,m,v,w,s):
 def ev(f):
  def R(x):return C(x.deg,fun=lambda g:x(tuple(f[i]for i in g)),mod=x.mod)
  return Zvalue(encode(*map(R,(n,u,m,v,w,s)),5))
 return C(5,fun=ev)

def collected_blocks(n,u,c,m,v,cp,w,s):
 a=n.reduce(2);b=m.reduce(2);h=carry(n);k=carry(m)
 N,U,e=lower(n,u,m,v,w,s);z=cup(a,b);t=cup(a,b,1);q=cup(a,b,2)
 D=pair_data(n,u,m,v,w,s);B,Bp,la=(D[x]for x in ('B','Bp','lambda'))
 r=B.reduce(2);rp=Bp.reduce(2);l=la.reduce(2);Db=l.d()+cup(b,a)
 W,_,alpha,hw,_=background_data(w,s)
 J=(op('1231343',b,b,a,a)+cup(v,a)+cup(b,u)+cup(cup(W,b,1),a)+cup(k,cup(a,a,1))
   +cup(cup(s,b),h)+cup(cup(s,cup(b,s,1)),a))
 V=(cup(r,rp,3)+cup(r.d(),rp,4)+cup(r+rp,Db,3)+cup(r.d()+rp.d(),Db,4)
   +sq(l,2)+cup(cup(b,a),l.d(),3)+cup(w,l)+cup(hw+alpha,q)+J)
 Phi=(op('1231343',a,a,b,b)+cup(a,v.d(),1)+cup(h,cup(b,b,1))
     +cup(cup(W,a,1),b)+cup(cup(s,a),k)+cup(cup(s,cup(a,s,1)),b)+cup(t,a+b)+cup(W,t))
 Pi=(cup(N,U.lift(),s=s,twists=(1,0))-cup(n,u.lift(),s=s,twists=(1,0))-cup(m,v.lift(),s=s,twists=(1,0))
    +cup(cup(n,W.lift(),1,s=s,twists=(1,1)),m,s=s,twists=(0,1))
    +cup(cup(m,W.lift(),1,s=s,twists=(1,1)),n,s=s,twists=(0,1)))
 Cnew=c+cp+e
 eps=(cup(c,cp,3)+cup(c.d(),cp,4)+cup(c+cp,e,3)+cup(e+z,z,3)+cup(Cnew.d(),z,4))
 nq=cup(n,m,1,s=s,twists=(1,1))
 cub=cup(m-n,nq,s=s,twists=(1,0))-cup(nq,m-n,s=s,twists=(0,1))
 top=(eps+Phi).lift().scaled(24)+(V.lift()+Pi).scaled(12)+cup(W.lift(),nq,s=s,twists=(1,0)).scaled(6)+cub.scaled(16)
 return {'nonbinary48':top,'V5':V,'Phi5':Phi,'Pi5':Pi,'epsilon5':eps,
         'pair_gauge48':cup(a,v,1).lift().scaled(24),'N':N,'U':U,'e':e,'C':Cnew}

def phase48(n,u,c,m,v,cp,w,s):
 D=collected_blocks(n,u,c,m,v,cp,w,s)
 total=D['nonbinary48']+binary_phase(n,u,m,v,w,s).lift().scaled(24)
 return C(5,fun=lambda f:int(total(f))%48,mod=None)

def full_source48(n,u,c,w,s):
 def ev(f):
  def R(x):return C(x.deg,fun=lambda g:x(tuple(f[i]for i in g)),mod=x.mod)
  nn,uu,cc,ww,ss=map(R,(n,u,c,w,s));ww.closed=ss.closed=True
  return int(source48(nn,uu,cc,ww,ss)(TOP))%48
 return C(6,fun=ev,mod=None)
