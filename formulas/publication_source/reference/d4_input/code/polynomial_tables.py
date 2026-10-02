"""Fixed total-cochain tables and exact factored evaluation.

Coordinates are local to this evaluator, never additional physical fields.
"""
from __future__ import annotations
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json
from cochains import C,pure_target
from ez_homotopy import ez_homotopy

@lru_cache(None)
def table(filename):return json.loads(Path(__file__).with_name(filename).read_text())

def total_cochain(n:C,omega2:C,s1:C,filename:str,degree:int,*,circuit=False)->C:
    p=n.deg
    if p not in (1,2) or n.mod is not None:raise ValueError('Expected an integer degree-one or degree-two input')
    data=table(filename)
    def transport(a,b):return (-1)**(s1(tuple(sorted((a,b)))) if a!=b else 0)
    def value(face):
        out=0
        for block in data['blocks']:
            i,j,k=block['i'],block['j'],block['k']
            if i+j+k!=degree:raise ValueError('Table degree mismatch')
            if any(not s1((face[t-1],face[t])) for t in range(1,i+1)):continue
            middle=face[i:i+j+1];last=face[i+j:]
            def M(f):return transport(face[0],f[0])*n(f)
            if p==1:ns=[M((middle[t-1],middle[t])) for t in range(1,j+1)]
            else:
                ns=[M((middle[u-1],middle[u],middle[v]))-M((middle[u-1],middle[u],middle[v-1]))
                    for u,v in combinations(range(1,j+1),2)]
            ws=[omega2((last[u-1],last[u],last[v]))^omega2((last[u-1],last[u],last[v-1]))
                for u,v in combinations(range(1,k+1),2)]
            if circuit:
                bits=[(m>>r)&1 for m in ns for r in range(3)]+ws;vals=[]
                for node in block['nodes']:
                    op=node[0]
                    if op=='const':v=node[1]
                    elif op=='var':v=bits[node[1]]
                    elif op=='xor':v=vals[node[1]]^vals[node[2]]
                    elif op=='and':v=vals[node[1]]&vals[node[2]]
                    else:raise ValueError(f'Unknown circuit operation: {op}')
                    vals.append(v)
                out^=vals[block['output']]
            else:
                wb=sum(bit<<e for e,bit in enumerate(ws))
                for nc,wc in block['terms']:
                    if wb&wc!=wc:continue
                    nc=int(nc)
                    if all((m&((nc>>(4*e))&15))==((nc>>(4*e))&15) for e,m in enumerate(ns)):out^=1
        return out
    return C(degree,fun=value)

def binary_completion(n:C,omega2:C,s1:C,*,factored=True)->C:
    """H*R + AW*(fixed coefficients); Y5 and Y6 remain independently fixed."""
    p=n.deg;r=p+4
    if p not in (1,2):raise ValueError('Only the independent degrees one and two are specified')
    def transport(a,b):return (-1)**(s1(tuple(sorted((a,b)))) if a!=b else 0)
    ng=C(p,fun=lambda f:transport(f[0][0],f[0][1])*n(tuple(v[1] for v in f)),mod=None)
    wg=C(2,fun=lambda f:omega2(tuple(v[2] for v in f)));wg.closed=True
    sg=C(1,fun=lambda f:s1(tuple(v[0] for v in f)));sg.closed=True
    # pure_target is the optimized expansion of compact.readable_residual.
    # Their equality is the descent/polarization identity proved in the note.
    R=pure_target(ng,wg,sg);H=ez_homotopy(r)
    filename=f'Y{r}_circuits.json' if factored else ('Y5_total.json' if p==1 else 'Y6_total_reduced.json')
    aw=total_cochain(n,omega2,s1,filename,r,circuit=factored)
    def value(face):
        out=aw(face)
        for simplex in H:
            out^=R(tuple(tuple(face[c] for c in vertex) for vertex in simplex))
        return out
    return C(r,fun=value)

def compression_rephasing(n:C,omega2:C,s1:C)->C:
    """The binary AW witness: old y6 + reduced y6 = d(this)."""
    if n.deg==1:return C(4)
    return total_cochain(n,omega2,s1,'Y6_rephasing_total.json',5)


def accelerated_binary_completion(n:C,omega2:C,s1:C,vertices:int)->C:
    """Exact C++ grid residual with the NEW factored 960-entry AW polynomial.

    Vertices must be labelled 0,...,vertices-1. Build residual_engine.so first;
    the dependency on NumPy/C++ is optional and isolated to this path.
    """
    if n.deg!=2 or n.mod is not None:raise ValueError('Only the degree-two integer input is supported here')
    try:
        from fast_y6 import ResidualEngine
    except (ImportError,OSError) as error:
        raise RuntimeError('Build the optional residual_engine.so and install NumPy, or use accelerate=False.') from error
    engine=ResidualEngine(n,omega2,s1,vertices)
    aw=total_cochain(n,omega2,s1,'Y6_circuits.json',6,circuit=True)
    H=ez_homotopy(6)
    def value(face):
        if any(not isinstance(v,int) or v<0 or v>=vertices for v in face):
            raise ValueError('Acceleration requires the specified consecutive integer vertex labels')
        chain=[tuple(tuple(face[c] for c in vertex) for vertex in simplex) for simplex in H]
        result=engine.evaluate_chain(chain)^aw(face)
        engine.clear()
        return result
    result=C(6,fun=value);result.engine=engine
    return result
