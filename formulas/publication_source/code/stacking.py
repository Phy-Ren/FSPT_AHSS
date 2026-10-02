"""Complete factorized stacking, with the compact pure Majorana formula."""
from cochains import *
from manuscript import source,mk,gamma,GW,operator_gauge,Oop
from compact import majorana

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
