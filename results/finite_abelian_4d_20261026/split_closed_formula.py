"""Closed 4+1D formula for split unitary finite Abelian symmetry.

Input: cyclic orders of A in G_f = C_2^f x A.
Output: abstract stacking-group invariant factors.
Proofs are in the companion derivation notes in proofs/.
This is integer arithmetic on at most five-factor supports, not an AHSS run.
"""
from collections import Counter
from itertools import combinations
from math import prod
from sympy import factorint


def primary_block(p, exponents):
    a=sorted(exponents)
    k=len(a)
    if not a:return []
    g=p**a[0]
    if p!=2:
        if k==1:
            return ([p**(a[0]-1),p**(a[0]+1)] if p==3 else [g,g])
        return [g]*{2:2,3:4,4:3,5:1}.get(k,0)
    if k==1:
        return [] if a[0]==1 else [2**(a[0]-2),g]
    if k==2:
        if a==[1,1]:return []
        if a==[1,2]:return [2]
        if a[0]==1:return [4]
        return [g//2,g if a[0]==a[1] else 2*g]
    if k==3:
        if a[:2]==[1,1]:return [2]*(3 if a[2]==1 else 4)
        if a[0]==1:return [2,2,2,4 if a[1]==2 else 8]
        return [2]+([g]*4 if a[0]==a[1] else [g]*3+[2*g])
    if k==4:
        t=a.count(1)
        if t<=1:return [2]+[g]*3
        if t==2:return [2,2,4]
        return [2]*3
    if k==5:return [g]
    return []


def primary_factors(orders):
    sylow={}
    for n in orders:
        for p,a in factorint(n).items():sylow.setdefault(int(p),[]).append(int(a))
    result=[]
    for p,aa in sylow.items():
        for k in range(1,min(5,len(aa))+1):
            for sub in combinations(aa,k):result.extend(primary_block(p,sub))
    return sorted(n for n in result if n>1)


def invariant_factors(orders):
    pp=primary_factors(orders)
    groups={}
    for n in pp:
        p=int(next(iter(factorint(n))))
        groups.setdefault(p,[]).append(n)
    width=max(map(len,groups.values()),default=0)
    rows=[[1]*(width-len(ns))+sorted(ns) for ns in groups.values()]
    return [prod(col) for col in zip(*rows)] if rows else []


def canonical_primary(ns):
    c=Counter()
    for n in ns:
        for p,a in factorint(n).items():c[int(p)**int(a)]+=1
    return sorted(c.items())
