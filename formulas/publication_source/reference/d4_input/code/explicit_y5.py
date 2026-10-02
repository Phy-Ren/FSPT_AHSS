"""Independent degree-five pure-p+ip cochain completion.

Coefficients were obtained from the degree-six residual, not by desuspending
or evaluating the degree-six obstruction. No degree-six correction is used.
"""
from __future__ import annotations
import json
from functools import lru_cache
from itertools import combinations
from pathlib import Path
from cochains import C,pure_target
from ez_homotopy import ez_homotopy

@lru_cache(None)
def coefficients5():
    data=json.loads(Path(__file__).with_name('Y5_total.json').read_text())
    out=[]
    for b in data['blocks']:
        parsed=[]
        for nc,wc in b['terms']:
            n=int(nc);exps=[]
            for e in range(b['j']):
                k=(n>>(4*e))&15
                if k:exps.append((e,k))
            parsed.append((tuple(exps),wc))
        out.append((b['i'],b['j'],b['k'],tuple(parsed)))
    return tuple(out)

def Y5(n1:C,omega2:C,s1:C,include_h=True)->C:
    if n1.deg!=1 or n1.mod is not None:raise ValueError('n1 must be an integral one-cochain')
    def transport(u,v):return (-1)**(s1(tuple(sorted((u,v)))) if u!=v else 0)
    ng=C(1,fun=lambda f:transport(f[0][0],f[0][1])*n1(tuple(v[1] for v in f)),mod=None)
    wg=C(2,fun=lambda f:omega2(tuple(v[2] for v in f)))
    sg=C(1,fun=lambda f:s1(tuple(v[0] for v in f)))
    wg.closed=sg.closed=True
    Rg=pure_target(ng,wg,sg);H=ez_homotopy(5) if include_h else ()
    def value(face):
        result=0
        for simplex in H:result^=Rg(tuple(tuple(face[c] for c in v) for v in simplex))
        for i,j,k,terms in coefficients5():
            if any(not s1((face[t-1],face[t])) for t in range(1,i+1)):continue
            middle=face[i:i+j+1];last=face[i+j:]
            ns=[transport(face[0],middle[t-1])*n1((middle[t-1],middle[t])) for t in range(1,j+1)]
            wb=0
            for e,(u,v) in enumerate(combinations(range(1,k+1),2)):
                bit=omega2((last[u-1],last[u],last[v]))^omega2((last[u-1],last[u],last[v-1]))
                wb|=bit<<e
            for factors,wcode in terms:
                if wb&wcode==wcode and all(ns[e]&mult==mult for e,mult in factors):result^=1
        return result
    return C(5,fun=value)
