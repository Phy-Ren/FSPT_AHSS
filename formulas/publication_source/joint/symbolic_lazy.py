"""Exact scalar-to-Boolean adapter for the independent lazy reference engine.
Only changes coefficient arithmetic; not the cochain formulas.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'code'))
from boolean_polynomials import Bit,Z
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,ds
PREC=32
Bit.__xor__=Bit.__add__;Bit.__rxor__=Bit.__radd__
Bit.__and__=Bit.__mul__;Bit.__rand__=Bit.__rmul__
def rp(self,b):
    if b!=-1:raise ValueError('only sign exponent supported')
    return 1-2*self.lift(PREC)
Bit.__rpow__=rp
oldcall=C.__call__
def call(self,f):
    v=oldcall(self,f)
    if self.mod==2:return Bit.cast(v)
    return v if isinstance(v,Z) else Z(v,PREC)
C.__call__=call
oldreduce=C.reduce
def reduce(self,m):
    if m is None and self.mod==2:
        if self.known_zero:return C(self.deg,mod=None)
        out=C(self.deg,fun=lambda f:self(f).lift(PREC),mod=None)
        out._binary_origin=self
        return out
    return oldreduce(self,m)
C.reduce=reduce

def integer_bar_cochain(degree,dimension,offset=0,bits=2):
    if degree!=1:raise NotImplementedError
    edge=[];labels=[]
    for i in range(dimension):
        z=Z(0,PREC)
        for j in range(bits):
            z+=Z({1<<offset:1<<j},PREC);labels.append((i,j));offset+=1
        edge.append(z)
    n=C(1,fun=lambda f:sum(edge[f[0]:f[1]]),mod=None);n.closed=True
    return n,offset,labels
_olddiv=Z.__floordiv__
def zfloor(self,k):
    if k!=2 or all(v%2==0 for v in self.t.values()):return _olddiv(self,k)
    return _olddiv(self-(self%2).lift(self.m),2)
Z.__floordiv__=zfloor

from math import gcd
oldscaled=C.scaled
def scaled(self,k):
    if self.mod is None and hasattr(self,'_binary_origin') and k:
        origin=self._binary_origin;m=PREC//gcd(abs(k),PREC)
        def val(f):
            z=origin(f).lift(m)
            return Z({i:k*v for i,v in z.t.items()},PREC)
        out=C(self.deg,fun=val,mod=None);out.closed=self.closed;return out
    return oldscaled(self,k)
C.scaled=scaled
