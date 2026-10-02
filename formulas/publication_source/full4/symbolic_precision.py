"""Conservative power-of-two precision tracking for the proof-only ring.
Multiplication by a known even integer increases known precision before a
subsequent exact division. No proof is allowed to reduce a modulus-one
quantity to a parity bit.
"""
from boolean_polynomials import Bit,Z
from math import gcd
CAP=64
_oldmul=Z.__mul__
def mul(self,o):
 if isinstance(o,int):
  if o==0:return Z(0,CAP)
  return Z({k:v*o for k,v in self.t.items()},min(CAP,self.m*(abs(o)&-abs(o))))
 o=Z.cast(o,self.m)
 # Product uncertainty is bounded by the valuations of both factors.
 vx=gcd(self.m,*self.t.values()) if self.t else self.m
 vy=gcd(o.m,*o.t.values()) if o.t else o.m
 precision=min(CAP,self.m*vy,o.m*vx,self.m*o.m)
 out={}
 for x,u in self.t.items():
  for y,v in o.t.items():
   k=x|y;out[k]=out.get(k,0)+u*v
 return Z(out,precision)
Z.__mul__=mul;Z.__rmul__=mul
_oldcast=Bit.cast
def cast(x):
 if isinstance(x,Z) and x.m<2:raise ArithmeticError('Cannot infer a parity from precision modulo one')
 return _oldcast(x)
Bit.cast=staticmethod(cast)
