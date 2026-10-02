"""Explicit chain-homotopy witnesses for exchange, associativity and descent.

No linear solve or unspecified primitive is used. signed_H_k is the same
normalized acyclic-carrier recursion in each degree and arity.
"""
from functools import lru_cache
from collections import Counter
from itertools import combinations_with_replacement
from cochains import *
from manuscript import *
from stacking import majorana,correction
from derive_ez import pull_grid
from descent import tau,susp,extend_bg
from low_formulas import Uca as low_Uca


def clean(d):return {g:c for g,c in d.items() if c}

@lru_cache(None)
def signed_G_k(n,k):
    ans=Counter()
    for cuts in combinations_with_replacement(range(n+1),k-1):
        bounds=(0,)+cuts+(n,);counts=[bounds[i+1]-bounds[i] for i in range(k)]
        path=[bounds[:-1]];letters=[]
        def visit():
            if not any(counts):
                inv=sum(letters[i]>letters[j] for i in range(n) for j in range(i+1,n))
                ans[tuple(path)]+=(-1)**inv;return
            for i in range(k):
                if counts[i]:
                    counts[i]-=1;v=list(path[-1]);v[i]+=1;path.append(tuple(v));letters.append(i)
                    visit();letters.pop();path.pop();counts[i]+=1
        visit()
    return clean(ans)

@lru_cache(None)
def signed_H_k(n,k):
    if n==0:return {}
    ans=Counter();zero=(0,)*k
    for g,c in signed_G_k(n,k).items():
        if g[0]!=zero:ans[(zero,)+g]-=c
    for g,c in signed_H_k(n-1,k).items():
        ans[(zero,)+tuple(tuple(x+1 for x in v) for v in g)]-=c
    return clean(ans)


def pull(c,grid,j):
    N=len(grid)-1;vv={}
    for f in faces(N,c.d):
        p=tuple(grid[i][j] for i in f)
        vv[f]=c[p] if len(set(p))==len(p) else 0
    return C(N,c.d,vv,c.mod)


def primitive(callback,decorations,w,s,out_degree):
    """H^* of an explicitly supplied normalized closed residual.

    Its use in the note always has a proved zero shuffle/AW projection.
    This routine is NOT a primitive for an arbitrary closed cochain.
    """
    k=1+len(decorations);N=w.N
    hs=[(g,c) for g,c in signed_H_k(out_degree,k).items()
        if all(len({v[j+1] for v in g})>=a.d+1 for j,a in enumerate(decorations))]
    out={}
    for f in faces(N,out_degree):
        ans=0
        for g,c in hs:
            grid=tuple(tuple(f[i] for i in v) for v in g)
            aa=[pull(a,grid,j+1) for j,a in enumerate(decorations)]
            ww=pull(w,grid,0);ss=pull(s,grid,0)
            ans+=c*callback(*aa,ww,ss).top()
        out[f]=ans%8
    return C(N,out_degree,out,8)


def gauge_CA(c,u,w):
    v=u.di()
    return phase((4,cup(c,v,3)+cup(c.di(),v,4)+cup(u,u,1)+cup(u,v,2)+w*u))

def gauge_operator(c,u,w):
    return (gauge_CA(c,u,w)+operator_gauge(c+u.di())-operator_gauge(c)).red(8)


def commutator_residual(a,b,w,s):
    f=source(a,w,s);g=source(b,w,s);u=cup(a,b,3);v=u.di();rev=mk(b,a,s)
    z=cup(f,g,5)+cup(rev,v,3)+cup(f+g+rev.di(),v,4)+cup(u,u,1)+cup(u,v,2)+w*u
    return (majorana(a,b,w,s)-majorana(b,a,w,s)+phase((4,z))).red(8)


def commutator_boundary(a,c,b,d,w,s):
    return (phase((4,cup(c,d,4)))+primitive(commutator_residual,[a,b],w,s,4)).red(8)


def associator_residual(a,b,h,w,s):
    m=mk(a,b,s);n=mk(b,h,s);r=mk(a,h,s);fa=source(a,w,s);fh=source(h,w,s)
    z=cup(m,fh,4)+cup(fa,n,4)+cup(m,r+n,3)+cup(n,m+r,3)
    return (majorana(a,b,w,s)+majorana(a+b,h,w,s)-majorana(b,h,w,s)-majorana(a,b+h,w,s)+phase((4,z))).red(8)


def associator_boundary(a,c,b,d,h,e,w,s):
    return (phase((4,cup(mk(a,b,s),e,4)))+primitive(associator_residual,[a,b,h],w,s,4)).red(8)


def descent_residual(a,b,w,s):
    high=tau(majorana(susp(a),susp(b),extend_bg(w),extend_bg(s)))
    zero=C(a.N,3,{})
    low=low_Uca(a,zero,b,zero,w,s)-GW(a,zero,b,zero,w,s)
    return (high-low).red(8)


def descent_boundary(a,b,w,s):
    return primitive(descent_residual,[a,b],w,s,3)
