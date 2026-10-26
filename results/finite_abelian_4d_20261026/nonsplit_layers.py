#!/usr/bin/env python3
"""Final decoration-layer quotients for finite unitary Abelian groups.

Input: G_f=C_(2m)^f times C_N1 times ... with all m,Ni powers of two.
These are associated-graded groups, not a direct-product decomposition of
its stacking group. Lower-layer doubling extensions are retained separately.
"""
from itertools import combinations
from math import gcd

NAMES=('pip','majorana','complex_fermion','bosonic')
def clean(ns):return sorted(n for n in ns if n>1)

def support_layers(m,spectators=()):
    if m<2 or m&(m-1) or any(n<2 or n&(n-1) for n in spectators):
        raise ValueError('All orders must be powers of two at least two')
    ns=sorted(spectators);r=len(ns)
    out={name:[] for name in NAMES}
    if r==0:
        out.update(pip=[m],majorana=[2],complex_fermion=[2],bosonic=[m])
    elif r==1:
        n=ns[0]
        out.update(pip=clean([n//2]),majorana=[2],complex_fermion=[2],
                   bosonic=clean([n//2,gcd(m,n),gcd(m//2,n)]))
    elif r==2:
        g=ns[0];unique=ns[1]>g
        if g<=m:
            out['complex_fermion']=[2]*(1+int(unique and g<m))
            out['bosonic']=clean([g//2]*(3-unique)+[g]*(3+unique))
        else:
            out['complex_fermion']=[2]
            out['bosonic']=clean([m//2]+[m]*3+[g//2]*(2-unique)+[g]*unique)
    elif r==3:
        g=ns[0];unique=ns.count(g)==1
        out['complex_fermion']=[2]*unique
        out['bosonic']=clean([g//2]+[g]*6 if g<=m else [m]*3+[g]*4)
    elif r==4:
        g=ns[0]
        out['complex_fermion']=[2]*int(g>=2*m)
        out['bosonic']=clean([g]*3+[min(m,g)])
    elif r==5:
        out['bosonic']=[ns[0]]
    return out

def nonsplit_2primary_layers(m,spectators=()):
    """Final layer invariant factors, after all incoming identifications."""
    out=support_layers(m)
    for r in range(1,min(5,len(spectators))+1):
        for subset in combinations(spectators,r):
            part=support_layers(m,subset)
            for key in NAMES:out[key].extend(part[key])
    return {k:sorted(v) for k,v in out.items()}


def nonsplit_layers(m,spectators=()):
    """Final layer invariant factors for C_(2m)^f times arbitrary spectators."""
    try:
        from .split_layers import split_layers,invariant_factors
    except ImportError:
        from split_layers import split_layers,invariant_factors
    if int(m)!=m or m<1 or any(int(n)!=n or n<1 for n in spectators):
        raise ValueError('All cyclic orders must be positive integers')
    m=int(m);spectators=list(map(int,spectators))
    if m%2:
        return split_layers([m,*spectators])
    base_two=m&-m
    twos=[n&-n for n in spectators if n%2==0]
    odds=[m//base_two]+[n//(n&-n) for n in spectators]
    result=nonsplit_2primary_layers(base_two,twos)
    odd_layers=split_layers(odds)
    return {name:invariant_factors(result[name]+odd_layers[name]) for name in NAMES}
