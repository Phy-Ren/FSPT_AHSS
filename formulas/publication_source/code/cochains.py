"""Simplicial cochains, vectorized over assignments. Integer phases are in units 1/8."""
import itertools as it
from functools import lru_cache
import numpy as np

@lru_cache(None)
def faces(N,d): return tuple(it.combinations(range(N+1),d+1))

@lru_cache(None)
def cuts(word,degs):
    N=sum(degs)-len(word)+len(degs)
    if N<0: return ()
    out=[]
    for mid in it.combinations_with_replacement(range(N+1),len(word)-1):
        cut=(0,)+mid+(N,)
        vs=[]
        for j,d in enumerate(degs,1):
            f=tuple(sorted(set(x for k,w in enumerate(word) if w==j for x in range(cut[k],cut[k+1]+1))))
            if len(f)!=d+1: break
            vs.append(f)
        else:
            ls=[cut[k+1]-cut[k]+1 for k in range(len(word))]
            sign=(-1)**sum(ls[k]*ls[l] for k in range(len(word)) for l in range(k+1,len(word)) if word[k]>word[l])
            out.append((tuple(vs),sign))
    return tuple(out)

class C:
    def __init__(self,N,d,v,mod=2): self.N,self.d,self.v,self.mod=N,d,v,mod
    def __getitem__(self,f): return self.v.get(tuple(f),0)
    def __add__(self,o):
        assert self.N==o.N and self.d==o.d
        mod=self.mod if self.mod==o.mod else None
        return C(self.N,self.d,{f:(self[f]+o[f])%mod if mod else self[f]+o[f] for f in faces(self.N,self.d)},mod)
    def __sub__(self,o): return self+o.scale(-1)
    def scale(self,k): return C(self.N,self.d,{f:k*v for f,v in self.v.items()},self.mod)
    def lift(self): return C(self.N,self.d,self.v,None)
    def red(self,m=2): return C(self.N,self.d,{f:v%m for f,v in self.v.items()},m)
    def __mul__(self,o): return cup(self,o)
    def di(self,mod=2):
        return C(self.N,self.d+1,{f:sum((-1)**j*self[f[:j]+f[j+1:]] for j in range(len(f))) for f in faces(self.N,self.d+1)},None).red(mod) if mod else C(self.N,self.d+1,{f:sum((-1)**j*self[f[:j]+f[j+1:]] for j in range(len(f))) for f in faces(self.N,self.d+1)},None)
    def beta(self):
        d=self.di(None)
        assert all(np.all(v%2==0) for v in d.v.values())
        return C(self.N,self.d+1,{f:v//2 for f,v in d.v.items()},None)
    def top(self): return self[tuple(range(self.N+1))]
    def D(self,s,mod=8): return (self.lift().di(None)-cup(s,self,i=0,integer=True).scale(2)).red(mod)

def word(w,*xs,integer=False):
    w=tuple(map(int,w)) if isinstance(w,str) else tuple(w)
    N=xs[0].N; degs=tuple(x.d for x in xs); d=sum(degs)-len(w)+len(xs)
    cc=cuts(w,degs)
    vs={}
    for f in faces(N,d):
        z=0
        for fs,sg in cc:
            term=sg if integer else 1
            for x,inds in zip(xs,fs): term=term*x[tuple(f[k] for k in inds)]
            z=z+term
        vs[f]=z if integer else z%2
    return C(N,d,vs,None if integer else 2)

def cup(x,y,i=0,integer=False):
    if i<0: return C(x.N,x.d+y.d-i,{},None if integer else 2)
    return word(tuple(k%2+1 for k in range(i+2)),x,y,integer=integer)

def phase(*args):
    # Each (integer coeff, F2 or integral cochain). No implicit XOR between terms.
    k,c=args[0]; z=c.lift().scale(k)
    for k,c in args[1:]: z=z+c.lift().scale(k)
    return z.red(8)

def cone(N,d,bits):
    v={f:((bits>>i)&1).astype(np.int64) if isinstance(bits,np.ndarray) else ((bits>>i)&1) for i,f in enumerate(f for f in faces(N,d) if f[0]==0)}
    c=C(N,d,v)
    for f in faces(N,d):
        if f[0]!=0: c.v[f]=sum(c[(0,)+f[:j]+f[j+1:]] for j in range(len(f)))%2
    return c

def upper(a,w,s,bits=0):
    N=a.N; f=w*a+s*a*a
    p=cone(N,2,bits)
    for t in faces(N,2):
        if t[0]!=0: p.v[t]=(p[t]+f[(0,)+t])%2
    return p

def restriction(x,vs):
    return C(len(vs)-1,x.d,{f:x[tuple(vs[k] for k in f)] for f in faces(len(vs)-1,x.d)},x.mod)


# Degree-budget enumeration; the reference enumeration above is retained for tests.
reference_cuts=cuts
from fast_cuts import fast_cuts
cuts=fast_cuts
