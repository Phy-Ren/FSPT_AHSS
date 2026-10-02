"""A fully specified universal degree-six primitive for the full-twist residual.

The fixed total-complex coefficients are in Y6_total.json. No linear solve
is performed by the evaluator. All cochain products follow cochains.py.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
from cochains import C,pure_target

from ez_homotopy import simplex_shuffles, ez_homotopy, chain_boundary, verify_ez

@lru_cache(None)
def coefficients():
    data=json.loads((Path(__file__).parent/'Y6_total.json').read_text())
    if not data.get('verified_total_coboundary'):raise ValueError('Unverified coefficient file')
    blocks=[]
    for block in data['blocks']:
        parsed=[]
        for code,wcode in block['terms']:
            code=int(code);factors=[];e=0
            while code:
                k=code&15
                if k:factors.append((e,k))
                code>>=4;e+=1
            parsed.append((tuple(factors),wcode))
        blocks.append((block['i'],block['j'],block['k'],tuple(parsed)))
    return tuple(blocks)

def Y6(N:C,w:C,s:C,include_h:bool=True)->C:
    if N.deg!=2 or N.mod is not None:raise ValueError('Y6 expects an integer degree-two cocycle')
    def sign_transport(u,v):
        return (-1)**(s(tuple(sorted((u,v)))) if u!=v else 0)
    Ng=C(2,fun=lambda f:sign_transport(f[0][0],f[0][1])*N(tuple(v[1] for v in f)),mod=None)
    wg=C(2,fun=lambda f:w(tuple(v[2] for v in f)))
    sg=C(1,fun=lambda f:s(tuple(v[0] for v in f)))
    wg.closed=sg.closed=True
    Rg=pure_target(Ng,wg,sg)
    H=ez_homotopy(6) if include_h else ();blocks=coefficients()
    def evaluate(face):
        ans=0
        for simplex in H:
            ans^=Rg(tuple(tuple(face[c] for c in v) for v in simplex))
        for i,j,k,terms in blocks:
            if any(not s((face[t-1],face[t])) for t in range(1,i+1)):continue
            middle=face[i:i+j+1];last=face[i+j:]
            def M(f):return sign_transport(face[0],f[0])*N(f)
            ns=[M((middle[u-1],middle[u],middle[v]))-M((middle[u-1],middle[u],middle[v-1]))
                for u,v in combinations(range(1,j+1),2)]
            wb=0
            for e,(u,v) in enumerate(combinations(range(1,k+1),2)):
                b=w((last[u-1],last[u],last[v]))^w((last[u-1],last[u],last[v-1]))
                wb|=b<<e
            for factors,wcode in terms:
                if (wb&wcode)==wcode and all((ns[e]&mult)==mult for e,mult in factors):ans^=1
        return ans
    out=C(6,fun=evaluate);out._grid_residual=Rg
    return out

if __name__=='__main__':
    print(json.dumps(verify_ez(),indent=2))
