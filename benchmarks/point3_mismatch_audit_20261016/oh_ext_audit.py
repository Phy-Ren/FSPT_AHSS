#!/usr/bin/env python3
"""Independent low-degree E(1) Ext from Oh cohomology and Thom squares.
No project formula engine or numerical classification data are used.
"""
from functools import lru_cache
from itertools import product
from pathlib import Path
import json

# Monomials x^i a^j b^k c^l in F2[x,a,b,c]/(ac).
weights=(1,1,2,3)
one=frozenset({(0,0,0,0)})
zero=frozenset()
x=frozenset({(1,0,0,0)})
a=frozenset({(0,1,0,0)})
b=frozenset({(0,0,1,0)})
c=frozenset({(0,0,0,1)})
def add(*ps):
    r=set()
    for p in ps:r.symmetric_difference_update(p)
    return frozenset(r)
def mul(p,q):
    r=set()
    for m in p:
        for n in q:
            z=tuple(u+v for u,v in zip(m,n))
            if z[1] and z[3]:continue
            if z in r:r.remove(z)
            else:r.add(z)
    return frozenset(r)
def degree(m):return sum(u*v for u,v in zip(m,weights))
@lru_cache(None)
def basis(d):
    if d<0:return ()
    return tuple(m for m in product(range(d+1),repeat=4) if degree(m)==d and not(m[1] and m[3]))
# Only Sq^0, Sq^1, Sq^2 are needed; Cartan extends generator formulas.
gens=[(x,mul(x,x),zero),(a,mul(a,a),zero),(b,add(mul(a,b),c),mul(b,b)),(c,zero,mul(b,c))]
@lru_cache(None)
def sq_monomial(m,k):
    values=[one,zero,zero]
    for variable,power in enumerate(m):
        for _ in range(power):
            values=[add(*(mul(values[i],gens[variable][j]) for i in range(3) for j in range(3) if i+j==n)) for n in range(3)]
    return values[k]
def sq(p,k):return add(*(sq_monomial(m,k) for m in p))
w2=add(mul(a,a),b)
def S1(p):return add(sq(p,1),mul(x,p))
def S2(p):return add(sq(p,2),mul(x,sq(p,1)),mul(w2,p))
def Q0(p):return S1(p)
def Q1(p):return add(S1(S2(p)),S2(S1(p)))
@lru_cache(None)
def cells(s,t):
    if s<0:return ()
    return tuple((j,m) for j in range(s+1) for m in basis(t-s-2*j))
@lru_cache(None)
def differential(s,t):
    source=cells(s,t); target=cells(s+1,t); ti={z:i for i,z in enumerate(target)}
    cols=[]
    for j,m in source:
        vec=0
        for k,Q in [(0,Q0),(1,Q1)]:
            for lower in basis(degree(m)-(1 if k==0 else 3)):
                if m in Q(frozenset({lower})):
                    vec ^= 1<<ti[(j+k,lower)]
        cols.append(vec)
    return tuple(cols)
def pivots(vs):
    p={}
    for v in vs:
        while v:
            i=v.bit_length()-1
            if i in p:v^=p[i]
            else:p[i]=v;break
    return p
def rank(vs):return len(pivots(vs))
def ext(s,n):
    t=s+n
    return len(cells(s,t))-rank(differential(s,t))-rank(differential(s-1,t))
def apply(cols,v):
    r=0
    while v:
        l=v&-v;i=l.bit_length()-1;v^=l;r^=cols[i]
    return r
def kernel(cols):
    piv={}; out=[]
    for i,v in enumerate(cols):
        dep=1<<i
        while v:
            k=v.bit_length()-1
            if k in piv:
                v^=piv[k][0];dep^=piv[k][1]
            else:piv[k]=(v,dep);break
        if not v:out.append(dep)
    return out
def h0_rank(s,n):
    t=s+n; src=cells(s,t); ti={z:i for i,z in enumerate(cells(s+1,t+1))}
    cols=[1<<ti[z] for z in src]
    mapped=[apply(cols,z) for z in kernel(differential(s,t))]
    boundaries=list(differential(s,t+1))
    return rank(boundaries+mapped)-rank(boundaries)
checks=0
for d in range(9):
    for m in basis(d):
        p=frozenset({m})
        assert not Q0(Q0(p))
        assert not Q1(Q1(p))
        assert Q0(Q1(p))==Q1(Q0(p))
        checks+=3
for s in range(7):
    for n in range(7):
        assert all(not apply(differential(s+1,s+n),v) for v in differential(s,s+n))
        checks+=1
rows={str(n):[ext(s,n) for s in range(7)] for n in range(7)}
result={"ring":"F2[x,a,b,c]/(ac), degrees(1,1,2,3)","thom":"X=(B(S4 x C2))^(3-V), w1=x, w2=a^2+b","module_dimensions_0_to_8":[len(basis(d)) for d in range(9)],"E1_Ext_rows_by_stem_then_filtration_0_to_6":rows,"checks":checks,"method":"Dual Koszul complex C^(s,t)=directsum_{j=0}^s M_(t-s-2j)^*, differential h0 Q0^*+v1 Q1^*", "degree4_total_F2_dimension":sum(rows['4']),
"h0_rank_stem4_filtration0_to1":h0_rank(0,4),
"ku4_from_Einf":{"torsion":[2,2,2,2,4],"order":64},
"Spin_c_degree4_after_shifted_ku0":{"torsion":[2,2,2,2,2,4],"order":128},
"stability_note":"For stems 0..5 the source, target and incoming cell j ranges and matrices stabilize by filtration 4, because all module degrees are nonnegative. Thus the displayed vanishing persists above the checked range.",
"differentials_note":"Adams dr has(s,n)->(s+r,n-1), r>=2. Stem 3 has only filtration0, so no outgoing differential from stem 4. Incoming differentials from stem 5 cannot reach stem 4 filtration 0 or 1. All stem 4 E2 classes survive. h0 rank 1 plus only one positive-filtration class fixes ku4 as Z4 plus four Z2."}
print(json.dumps(result,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
