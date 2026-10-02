from cochains import *
from manuscript import gamma,source,mk,GW,operator_gauge,Oop
from ez_signed import signed_H,signed_G
import numpy as np
from functools import lru_cache


def residual(a,b,w,s):
    p=a.d;N=a+b;m=mk(a,b,s);f=source(a,w,s);g=source(b,w,s)
    h=w*m+cup(m,m,p-1)+cup(m,m.di(),p)+cup(f+g,m,p)+cup(m,f+g,p)+cup(f,g,p+1)
    return (gamma(N,w,s)-gamma(a,w,s)-gamma(b,w,s)+phase((4,h))).red(8)


def pull_grid(a,b,w,s,grid):
    size=len(grid)-1
    def pull(c,j):
        vv={}
        for f in faces(size,c.d):
            proj=tuple(grid[i][j] for i in f)
            vv[f]=c[proj] if len(set(proj))==len(proj) else 0
        return C(size,c.d,vv,c.mod)
    return pull(a,1),pull(b,2),pull(w,0),pull(s,0)

@lru_cache(None)
def reduced_H(n,p):
    return tuple((g,c) for g,c in signed_H(n).items()
                  if len({v[1] for v in g})>=p+1 and len({v[2] for v in g})>=p+1)

def E_H(a,b,w,s):
    p=a.d;hh=reduced_H(p+2,p);out={}
    for f in faces(a.N,p+2):
        ans=0
        for g,c in hh:
            gg=tuple(tuple(f[j] for j in v) for v in g)
            aa,bb,ww,ss=pull_grid(a,b,w,s,gg)
            ans=ans+c*residual(aa,bb,ww,ss).top()
        out[f]=ans%8
    return C(a.N,p+2,out,8)

if __name__=='__main__':
    from time import perf_counter
    t0=perf_counter(); p=3;N=6;top=(0,1,2,3);a=C(N,p,{top:1});b=C(N,p,{top:1});w=C(N,2,{});s=C(N,1,{})
    vals=[]
    for grid,c in signed_G(6).items():
        # The only potentially nonzero AW split: (background degree 0, a 3, b 3).
        if grid[0]!=(0,0,3):continue
        if grid[-1]!=(0,3,6):continue
        aa,bb,ww,ss=pull_grid(a,C(N,p,{(3,4,5,6):1}),w,s,grid)
        vals.append((c,int(residual(aa,bb,ww,ss).top())))
    print('AW',vals,'sum=',sum(c*v for c,v in vals)%8,'seconds',perf_counter()-t0,flush=True)
    rng=np.random.default_rng(940);N=6;B=8
    def ran(d):return cone(N,d,rng.integers(0,1<<len(faces(N-1,d-1)),B))
    a=ran(3);b=ran(3);w=ran(2);s=ran(1)
    t0=perf_counter();ee=E_H(a,b,w,s);print('E seconds',perf_counter()-t0,flush=True)
    print('E residual=',(ee.D(s)-residual(a,b,w,s)).top(),flush=True)
