from cochains import *
from functools import lru_cache
G3_MASKS=[4097,8193,4098,8194,4104,8200,4112,8208,
131,529,4113,16401,545,8225,4161,8257,4225,8449,530,546,4130,8322,8450,4624,
16912,4640,16928,43,83,275,4115,16403,547,8227,195,323,387,4227,8323,16515,
4355,8451,16643,4121,8217,16409,553,4137,8233,16425,4145,8241,16433,593,657,609,
673,538,4122,8218,16410,554,4138,8234,16426,4146,658,786,674,802,59,155,
283,115,179,563,4147,8243,16435,659,787,675,803,569]
assert len(G3_MASKS)==84

def pull_prism(x):return C(x.deg,fun=lambda f:x(tuple(v//2 for v in f)),mod=x.mod)
def tau(x):
 def value(face):
  return sum((-1)**j*x(tuple(2*v for v in face[:j+1])+tuple(2*v+1 for v in face[j:])) for j in range(len(face)))
 return C(x.deg-1,fun=value,mod=x.mod)

def G3(N,b,w,s):
 def value(f):
  z0,z1,z2,z3=f
  one=[(z0,z1),(z0,z2),(z0,z3)];two=[(z0,z1,z2),(z0,z1,z3),(z0,z2,z3)]
  bits=[s(e) for e in one]+[N(e)%2 for e in one]+[(N(e)//2)%2 for e in one]+[w(e) for e in two]+[b(e) for e in two]
  mask=sum(v<<i for i,v in enumerate(bits));return sum((mask&t)==t for t in G3_MASKS)%2
 return C(3,fun=value)

def lower_suspension(N,b,w,s):
 sI=pull_prism(s);wI=pull_prism(w);NI=pull_prism(N);aI=NI.reduce(2);bI=pull_prism(b)
 u=C(1,fun=lambda f:(f[1]%2)-(f[0]%2));u.closed=True
 Ns=cup(u.lift(),NI,s=sI,twists=(0,1))
 tI=cup(aI,aI)
 # The psi-Cartan word in degree one has face value u01*a12*u12*a23;
 # it vanishes on monotone interval simplices, but is kept explicitly.
 z=C(3,fun=lambda f:u(f[:2])*aI(f[1:3])*u(f[1:3])*aI(f[2:4]))
 bs=cup(u,bI)+z+cup(cup(sI,u,1),tI)+cup(cup(wI,u,1),aI)
 return Ns,bs,wI,sI,u

@lru_cache(None)
def ez2_GAW(n):
 ans=[]
 for a in range(n+1):
  counts=[a,n-a];path=[(0,a)]
  def rec():
   if not any(counts):ans.append(tuple(path));return
   for d in range(2):
    if counts[d]:
     counts[d]-=1;v=list(path[-1]);v[d]+=1;path.append(tuple(v));rec();path.pop();counts[d]+=1
  rec()
 return tuple(ans)
@lru_cache(None)
def ez2_H(n):
 if n==0:return ()
 zero=(0,0);ans=set()
 for t in ez2_GAW(n):
  if t[0]!=zero:ans.symmetric_difference_update(((zero,)+t,))
 for t in ez2_H(n-1):ans.symmetric_difference_update(((zero,)+tuple((a+1,b+1) for a,b in t),))
 return tuple(sorted(ans))

def prism_relative_h(Q):
 """H^*Q on I x X, first factor interval; Q vanishes at both endpoints."""
 H=ez2_H(Q.deg-1)
 def value(f):
  ans=0
  for simplex in H:
   out=tuple(2*(f[b]//2)+(f[a]%2) for a,b in simplex)
   # A repeated projected vertex is a genuine degeneracy, not removed.
   ans^=Q(out)
  return ans
 return C(Q.deg-1,fun=value)

def full_suspension(N,b,c,w,s):
 Ns,bs,wI,sI,u=lower_suspension(N,b,w,s)
 Qs=parity(Ns,bs,wI,sI)
 cs=cup(u,pull_prism(c+G3(N,b,w,s)))+prism_relative_h(Qs)
 return Ns,bs,cs,wI,sI
