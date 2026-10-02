"""Complete normalized zero-background terminal product, arbitrary integer n2.

All routines are explicit evaluation formulas. No linear solve, lookup of a
phase table, or choice of a primitive is performed at evaluation time.
The Cartan chain operator and its eight tetrahedral correction polynomials
are fixed independently and reproduced in the accompanying mathematical note.
Return integer phase numerators modulo 48; divide by 48 before exponentiation.
"""
from model import *
from ez_pair import homotopy
from tensor_compact import tensor5

H5=tuple(g for g in homotopy(5) if min(len(set(v[k] for v in g)) for k in (0,1))>=3)

def binary_product(n,u,m,v):
    """The constructed five-cochain Z5, including both odd input parities."""
    corr=tensor5(n,u,m,v)
    def value(face):
        if len(face)!=6:raise ValueError('Expected a five-simplex')
        ans=corr(face)
        for g in H5:
            p=[face[v[0]] for v in g];q=[face[v[1]] for v in g]
            nn,uu,mm,vv=pull(n,p),pull(u,p),pull(m,q),pull(v,q)
            ans+=residual(nn,uu,mm,vv)(tuple(range(7)))
        return ans%2
    return C(5,fun=value)

def product48(n,u,c,m,v,cp):
    """48 times the COMPLETE terminal stacking phase, not the fractional seed."""
    if (n.deg,u.deg,c.deg,m.deg,v.deg,cp.deg)!=(2,3,4,2,3,4):
        raise ValueError('Expected two sets of degrees (2,3,4)')
    if n.mod is not None or m.mod is not None or any(x.mod!=2 for x in (u,c,v,cp)):
        raise ValueError('Integer leading inputs and binary upper inputs are required')
    N,U,e=lower(n,u,m,v)
    z=binary_product(n,u,m,v)
    out=upper48(c,cp,e)+fraction48(n,u,m,v)+z.lift().scaled(24)
    return C(5,fun=lambda f:out(f)%48,mod=None)

def stack(n,u,c,m,v,cp):
    N,U,e=lower(n,u,m,v)
    return N,U,c+cp+e,product48(n,u,c,m,v,cp)
