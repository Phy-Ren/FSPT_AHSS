"""Exact Boolean polynomial rings: x_i^2=x_i. No sampling.
Bit expressions use XOR. Integer lifts use the exact finite parity expansion,
truncated only modulo the requested power of two.
"""
from math import gcd
class Bit:
 def __init__(self,t=()):self.t=frozenset(t)
 @staticmethod
 def var(i):return Bit([1<<i])
 @staticmethod
 def cast(x):
  if isinstance(x,Bit):return x
  if isinstance(x,Z):return Bit(k for k,v in x.t.items() if v%2)
  return Bit([0]) if int(x)%2 else Bit()
 def __add__(self,o):
  if isinstance(o,Z):return self.lift()+o
  return Bit(self.t ^ Bit.cast(o).t)
 __radd__=__add__;__sub__=__add__;__rsub__=__add__
 def __mul__(self,o):
  if isinstance(o,Z):return self.lift()*o
  o=Bit.cast(o);out=set()
  for x in self.t:
   for y in o.t:
    k=x|y
    if k in out:out.remove(k)
    else:out.add(k)
  return Bit(out)
 __rmul__=__mul__
 def __mod__(self,m):
  if m!=2:raise ValueError('Use an integer lift before reducing a bit polynomial modulo '+str(m))
  return self
 def __bool__(self):return bool(self.t)
 def __eq__(self,o):return self.t==Bit.cast(o).t
 def lift(self,m=16):
  # parity of m_1,...,m_l is z <- z + m_i - 2 z m_i.
  if m==2:return Z({k:1 for k in self.t},2)
  z=Z({},m)
  for k in sorted(self.t):z=z+Z({k:1},m)-2*z*Z({k:1},m)
  return z
 def __repr__(self):return 'Bit('+str(len(self.t))+' monomials)'
class Z:
 def __init__(self,t=0,m=16):
  if isinstance(t,int):t={0:t} if t else {}
  self.m=m;self.t={k:int(v)%m for k,v in t.items() if int(v)%m}
 @staticmethod
 def cast(o,m):
  if isinstance(o,Bit):return o.lift(m)
  return o if isinstance(o,Z) else Z(int(o),m)
 def __add__(self,o):
  o=Z.cast(o,self.m);m=min(self.m,o.m);out=dict(self.t)
  for k,v in o.t.items():out[k]=out.get(k,0)+v
  return Z(out,m)
 __radd__=__add__
 def __neg__(self):return Z({k:-v for k,v in self.t.items()},self.m)
 def __sub__(self,o):return self+-Z.cast(o,self.m)
 def __rsub__(self,o):return Z.cast(o,self.m)+-self
 def __mul__(self,o):
  if isinstance(o,int):return Z({k:v*o for k,v in self.t.items()},self.m)
  o=Z.cast(o,self.m);m=min(self.m,o.m);out={}
  for x,u in self.t.items():
   for y,v in o.t.items():k=x|y;out[k]=out.get(k,0)+u*v
  return Z(out,m)
 __rmul__=__mul__
 def __mod__(self,m):return Bit.cast(self) if m==2 else Z(self.t,m)
 def __floordiv__(self,k):
  assert self.m%k==0 and all(v%k==0 for v in self.t.values()),'non-exact polynomial division'
  return Z({j:v//k for j,v in self.t.items()},self.m//k)
 def __bool__(self):return bool(self.t)
 def __eq__(self,o):return not bool(self-Z.cast(o,self.m))
 def __repr__(self):return 'Z/'+str(self.m)+'('+str(len(self.t))+' monomials)'

def install():
 import cochains as cc
 C=cc.C
 old_lift=C.lift
 def lift(self):return C(self.N,self.d,{f:v.lift() if isinstance(v,Bit) else v for f,v in self.v.items()},None)
 C.lift=lift
 def di(self,mod=2):
  x=self if mod==2 else self.lift()
  out=C(self.N,self.d+1,{f:sum((-1)**j*x[f[:j]+f[j+1:]] for j in range(len(f))) for f in cc.faces(self.N,self.d+1)},None)
  return out.red(mod) if mod else out
 C.di=di
 def phase(*args):
  N=args[0][1].N;d=args[0][1].d;out={}
  for f in cc.faces(N,d):
   z=Z(0,8)
   for k,c in args:
    v=c[f]
    if isinstance(v,Bit):
     m=8//gcd(abs(k),8);vv=v.lift(max(2,m));v=Z({q:k*t for q,t in vv.t.items()},8)
    else:v=Z({q:k*t for q,t in v.t.items()},8) if isinstance(v,Z) else Z(k*v,8)
    z=z+v
   out[f]=z
  return C(N,d,out,8)
 cc.phase=phase
 oldword=cc.word
 def word(w,*xs,integer=False):
  if integer:xs=tuple(x.lift() for x in xs)
  return oldword(w,*xs,integer=integer)
 cc.word=word

def free_cocycle(N,d,offset=0):
 from cochains import C,faces
 v={};j=offset
 for f in faces(N,d):
  if f[0]==0:v[f]=Bit.var(j);j+=1
 c=C(N,d,v)
 for f in faces(N,d):
  if f[0]:c.v[f]=sum(c[(0,)+f[:i]+f[i+1:]] for i in range(len(f)))
 return c,j
