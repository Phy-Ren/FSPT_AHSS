"""Adapted from the frozen U1f consolidated v0.7 formula archive."""
from __future__ import annotations
from functools import lru_cache
from itertools import combinations_with_replacement
@lru_cache(None)
def interval_cuts(p,q,i):
    if i<0: return ()
    N=p+q-i
    if N<0:return ()
    L=i+2; word=tuple(j%2 for j in range(L)); result=[]
    for mid in combinations_with_replacement(range(N+1),L-1):
        cuts=(0,)+mid+(N,)
        S=[[],[]]; lengths=[]; inner=[]
        for j,w in enumerate(word):
            S[w].extend(range(cuts[j],cuts[j+1]+1))
            inn=w in word[j+1:];inner.append(inn)
            lengths.append(cuts[j+1]-cuts[j]+int(inn))
        if len(S[0])!=p+1 or len(S[1])!=q+1: continue
        if any(len(set(s))!=len(s) for s in S):continue
        exp=i*(p+q)+i*(i-1)//2
        exp+=sum(cuts[j+1] for j in range(L) if inner[j])
        exp+=sum(lengths[j]*lengths[k] for j in range(L) for k in range(j+1,L) if word[j]>word[k])
        result.append((tuple(S[0]),tuple(S[1]),(-1)**exp))
    return tuple(result)

