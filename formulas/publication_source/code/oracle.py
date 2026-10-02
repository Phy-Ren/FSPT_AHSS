"""Explicit 4+1D Majorana stacking; phases are integer numerators over eight.

The eighteen face substitutions are fixed constants, not fitted coefficients.
All backgrounds are retained. The full source is the fixed uploaded obstruction.
"""
from cochains import C,faces,cup,phase
from manuscript import source,mk,gamma,GW,operator_gauge,Oop
from derive_ez import residual,pull_grid

FACE_MAPS = (
    (1, '0111111', '0112333', '0133345'),
    (1, '0111111', '0112223', '0133455'),
    (-1, '0111111', '0111223', '0134455'),
    (1, '0111111', '0111123', '0134555'),
    (1, '0111111', '0112344', '0144445'),
    (1, '0111111', '0112234', '0144555'),
    (-1, '0111111', '0111234', '0145555'),
    (-1, '0122222', '0122333', '0123345'),
    (1, '0122222', '0122233', '0123445'),
    (-1, '0122222', '0122223', '0123455'),
    (-1, '0122222', '0122344', '0124445'),
    (1, '0122222', '0122334', '0124455'),
    (-1, '0122222', '0122234', '0124555'),
    (-1, '0122222', '0122345', '0125555'),
    (1, '0123333', '0123344', '0123445'),
    (-1, '0123333', '0123334', '0123455'),
    (1, '0123333', '0123345', '0123555'),
    (-1, '0123444', '0123445', '0123455'),
)

def majorana(a,b,w,s):
    """Eight times E^gamma_5. Binary inputs have degrees (3,3,2,1)."""
    if (a.d,b.d,w.d,s.d)!=(3,3,2,1) or len({x.N for x in (a,b,w,s)})!=1:
        raise ValueError('Expected cochains of degrees (3,3,2,1) on one simplex')
    if any(x.mod!=2 for x in (a,b,w,s)):
        raise ValueError('All Majorana/background inputs must have modulus two')
    out={}
    for f in faces(a.N,5):
        ans=0
        for coef,r,u,v in FACE_MAPS:
            grid=tuple((f[int(r[j])],f[int(u[j])],f[int(v[j])]) for j in range(7))
            ans=ans+coef*residual(*pull_grid(a,b,w,s,grid)).top()
        out[f]=ans%8
    return C(a.N,5,out,8)

def complex_factor(a,c,b,d,w,s):
    m=mk(a,b,s)
    return phase((4,cup(c,d,3)+cup(c+d,m,3)))

def mixed_factor(a,c,b,d,w,s):
    Ctot=c+d+mk(a,b,s)
    return phase((4,cup(c.di(),d,4)+cup(Ctot,Ctot.di(),4)+cup(c,c.di(),4)+cup(d,d.di(),4)))

def correction(a,c,b,d,w,s,operator=True):
    """Eight times the full top stacking correction; no p+ip input is allowed."""
    if c.d!=4 or d.d!=4:raise ValueError('Complex-fermion cochains must have degree four')
    e=majorana(a,b,w,s)
    if operator:return (e+complex_factor(a,c,b,d,w,s)+mixed_factor(a,c,b,d,w,s)).red(8)
    return (e+GW(a,c,b,d,w,s)).red(8)

def stack_lower(a,c,b,d,w,s):
    return a+b,c+d+mk(a,b,s)
