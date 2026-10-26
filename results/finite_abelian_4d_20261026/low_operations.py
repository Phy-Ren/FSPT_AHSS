"""Exact low-degree tensor-resolution operations for cyclic 2-groups.

Positive exponents in every factor isolate a stable smash support.
The integral differential and mod-2 Steenrod action are standard.
No secondary operation or extension is assumed by this module.
"""
from itertools import product
from math import comb
from functools import lru_cache
from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


@lru_cache(None)
def comps(n,k,minimum=1):
    if k==0:return ((),) if n==0 else ()
    return tuple((a,)+b for a in range(minimum,n+1)
                 for b in comps(n-a,k-1,minimum))


def differential(ns,n):
    src=comps(n,len(ns)); dst=comps(n+1,len(ns)); idx={a:i for i,a in enumerate(dst)}
    d=Matrix.zeros(len(dst),len(src))
    for j,a in enumerate(src):
        for i,k in enumerate(a):
            if k%2:
                b=list(a);b[i]+=1
                d[idx[tuple(b)],j]=(-1)**sum(a[:i])*ns[i]
    return d


def sq_single(N,q,k):
    if N==2:return comb(q,k)%2 if k<=q else 0
    if k%2:return 0
    return comb(q//2,k//2)%2 if k//2<=q//2 else 0


def sq(ns,n,k):
    src=comps(n,len(ns)); dst=comps(n+k,len(ns)); idx={a:i for i,a in enumerate(dst)}
    mat=Matrix.zeros(len(dst),len(src))
    for j,a in enumerate(src):
        for ks in comps(k,len(ns),0):
            if all(sq_single(N,q,v) for N,q,v in zip(ns,a,ks)):
                b=tuple(q+v for q,v in zip(a,ks));mat[idx[b],j]^=1
    return mat


def f2rank(m):
    rows=[sum((int(x)%2)<<j for j,x in enumerate(row)) for row in m.tolist()]
    piv={}
    for row in rows:
        while row:
            p=row.bit_length()-1
            if p in piv:row^=piv[p]
            else:piv[p]=row;break
    return len(piv)


def integral_lift_obstruction(ns,n):
    """Matrix whose F2 kernel is reduction of integral n-cocycles."""
    d=differential(ns,n)
    dm=DomainMatrix.from_Matrix(d).convert_to(ZZ)
    diag,u,v=smith_normal_decomp(dm)
    dd=diag.to_Matrix();vv=v.to_Matrix()
    rank=sum(dd[i,i]!=0 for i in range(min(dd.shape)))
    return vv.inv()[:rank,:].applyfunc(lambda x:int(x)%2)


def ranks(ns):
    r=len(ns)
    sq23=sq(ns,3,2)
    sq24=sq(ns,4,2)
    cf=integral_lift_obstruction(ns,6)*sq24
    inc=integral_lift_obstruction(ns,5)*sq23
    return {'mc_first_kernel':len(comps(3,r))-f2rank(sq23),
            'cf_obstruction_kernel':len(comps(4,r))-f2rank(cf),
            'cf_incoming_rank':f2rank(sq(ns,2,2)),
            'bos_incoming_cf_rank':f2rank(inc)}


if __name__=='__main__':
    for r in [2,3,4]:
        from itertools import combinations_with_replacement
        for ns in combinations_with_replacement([2,4,8,16],r):
            print(ns,ranks(ns))
