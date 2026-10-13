"""Adapted from the frozen U1f consolidated v0.7 formula archive."""
from .simplex import C, F, background
from itertools import combinations
def evalface(c,face):
    if len(set(face))!=len(face):return 0
    return c(tuple(face))

def pull_on_path(c,path):
    N=len(path)-1;tw=[c.tw[v] for t,v in path]
    return C(N,c.p,{f:evalface(c,tuple(path[j][1] for j in f)) for f in combinations(range(N+1),c.p+1)},tw)

def gauge_path(a,k,n,s,r,u,v,path):
    aa,kk,nn,ss,rr=[pull_on_path(c,path) for c in (a,k,n,s,r)];N=len(path)-1
    U=C(N,0,{(i,):t*u((j,)) for i,(t,j) in enumerate(path)},kk.tw)
    V=C(N,2,{f:path[f[0]][0]*evalface(v,tuple(path[j][1] for j in f)) for f in combinations(range(N+1),3)},nn.tw)
    A,B=background(aa,ss)
    return aa,kk+U.d(),nn+B.cup(U)+V.d(),ss,rr

def interval_paths(baseN):
    for pos in range(baseN+1):
        path=[(0,j) for j in range(pos+1)]+[(1,j) for j in range(pos,baseN+1)]
        yield tuple(path),(-1)**pos

def gauge3(a,k,n,s,r,u,v,phase_formula):
    N=a.N;vals={}
    for f in combinations(range(N+1),5):
        val=F(0)
        for path,sign in interval_paths(4):
            path=tuple((t,f[j]) for t,j in path)
            aa,kk,nn,ss,rr=gauge_path(a,k,n,s,r,u,v,path)
            val+=sign*phase_formula(aa,kk,nn,ss,rr)(tuple(range(6)))
        vals[f]=val%1
    return C(N,4,vals,s.tw)

