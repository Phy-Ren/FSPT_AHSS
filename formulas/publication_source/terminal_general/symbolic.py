"""Exact Boolean arithmetic adapter; three integer input bits are retained."""
from model import *
sys.path.insert(0,str(ROOT/'code'))
from boolean_polynomials import Bit,Z
PREC=8
Bit.__xor__=Bit.__add__;Bit.__rxor__=Bit.__radd__
oldreduce=C.reduce

def reduce(self,mod):
    if mod is None and self.mod==2:
        if self.known_zero:return C(self.deg,mod=None)
        def ev(f):
            x=self(f)
            return x.lift(PREC) if isinstance(x,Bit) else x
        z=C(self.deg,fun=ev,mod=None);z.closed=False
        return z
    return oldreduce(self,mod)
C.reduce=reduce

def free_state(d,start=0):
    ns={};us={};labels=[];j=start
    for ij in combinations(range(1,d+1),2):
        terms={}
        for q in range(3):
            terms[1<<j]=1<<q;labels.append(('n',ij,q));j+=1
        ns[ij]=Z(terms,PREC)
    for f in combinations(range(d+1),4):
        if f[0]==0:us[f]=Bit.var(j);labels.append(('u',f,0));j+=1
    n,u=dk_state(d,ns,us)
    return n,u,j,labels

def as_bit(x):return Bit.cast(x)

def poly_eval(p,assignment):
    return sum(1 for m in as_bit(p).t if m&assignment==m)%2
