"""Current evaluators for the native p+ip -> complex-fermion stacking rule.
The degree-two pure product includes the terminal-compatible closed correction.

Inputs use the ordered-simplex cochain class cochains.C. Integer n is never
silently reduced before reading its second bit. All returned corrections
are binary. This module does not compute bosonic stacking in the p+ip sector.
"""
from dataclasses import dataclass
import numpy as np
from cochains import C,cup,faces
from pip_current import q,r,source,upper_product,pure_product_compact,zero

def _vanishes(x):
    return all(np.all(v==0) for v in x.v.values())

def bits(n):
    """Canonical first and second bits, including negative integer values."""
    return n.red(2),C(n.N,n.d,{f:(n[f]//2)%2 for f in faces(n.N,n.d)})

def _check(n,m,w,s):
    if n.d not in (1,2):raise ValueError('n must have degree 1 or 2')
    if m.d!=n.d+1 or w.d!=2 or s.d!=1:
        raise ValueError('Expected degrees (p,p+1,2,1) for (n,m,w,s)')
    if len({n.N,m.N,w.N,s.N})!=1:raise ValueError('Simplex sizes disagree')
    if not _vanishes(w.di()) or not _vanishes(s.di()):
        raise ValueError('The fixed backgrounds must be binary cocycles')
    if not _vanishes(n.di(None)-cup(s,n,integer=True).scale(2)):
        raise ValueError('The leading integer cochain is not d_s-closed')
    a,h=bits(n)
    if not _vanishes(m.di()+q(a)+w*a+s*r(a)):
        raise ValueError('The Majorana cochain does not solve its lower equation')

@dataclass
class ThirdOrderProduct:
    integer:C
    majorana:C
    second_twister:C
    third_twister:C
    gamma:C
    gamma_psi:C
    psi:C

def third_twister(n,m,n_prime,m_prime,w,s,*,validate=True):
    """Evaluate both lower twisters with unshifted manuscript input cochains.

    Parameters n,n_prime: signed integral p-cochains (p=1 or 2).
    m,m_prime: binary (p+1)-cochains satisfying the prescribed first source.
    w,s: fixed binary extension and anti-unitary cocycles.
    The result's integer adds in Z; its Majorana adds with E^psi_{p+1}.
    third_twister is E_{p+2}=E^gamma+E^{gamma psi}+E^psi, all over F2.
    """
    if validate:
        _check(n,m,w,s);_check(n_prime,m_prime,w,s)
    if n_prime.d!=n.d:raise ValueError('Leading degrees disagree')
    p=n.d;a,h=bits(n);b,k=bits(n_prime)
    c=m+s*h;e=m_prime+s*k;W=w+s*s
    t=cup(a,b,p-1);u=cup(a,b,p)
    gamma=cup(c,e,p)+s*cup(c,e,p+1)
    mixed=upper_product(a,c,b,e,s)+gamma
    pure=pure_product_compact(a,h,b,k,W,s)
    first=t+s*u
    return ThirdOrderProduct(n.lift()+n_prime.lift(),m+m_prime+first,first,
                             gamma+mixed+pure,gamma,mixed,pure)

def fermion_source(n,m,w,s,*,validate=True):
    if validate:_check(n,m,w,s)
    a,h=bits(n)
    return source(a,h,m+s*h,w+s*s,s)

def stack(n,m,f,n_prime,m_prime,f_prime,w,s,*,validate=True):
    """Return the stacked (integer,Majorana,fermion) triple, not a top phase."""
    res=third_twister(n,m,n_prime,m_prime,w,s,validate=validate)
    if validate:
        for ni,mi,fi in [(n,m,f),(n_prime,m_prime,f_prime)]:
            if fi.d!=ni.d+2 or fi.N!=ni.N:
                raise ValueError('Incorrect degree or simplex size of fermion input')
            if not _vanishes(fi.di()+fermion_source(ni,mi,w,s,validate=False)):
                raise ValueError('The fermion input does not solve the native source')
    return res.integer,res.majorana,f+f_prime+res.third_twister
