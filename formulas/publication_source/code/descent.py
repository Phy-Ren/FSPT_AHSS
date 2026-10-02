"""Cone-last suspension, background extension, and evaluation.

Adapted from the supplied aligned stacking bundle. Only the three neutral
coordinate helpers are retained; obsolete obstruction/product routines
from that source file are intentionally omitted.
"""

from cochains import *

def susp(x):
    NN=x.N+1
    return C(NN,x.d+1,{f:(x[f[:-1]] if f[-1]==NN else 0) for f in faces(NN,x.d+1)},x.mod)

def extend_bg(x):
    NN=x.N+1
    v={}
    for f in faces(NN,x.d):
        t=tuple(min(i,x.N) for i in f)
        v[f]=x[t] if len(set(t))==len(t) else 0
    return C(NN,x.d,v,x.mod)

def tau(x):
    NN=x.N-1
    return C(NN,x.d-1,{f:x[f+(x.N,)] for f in faces(NN,x.d-1)},x.mod)

