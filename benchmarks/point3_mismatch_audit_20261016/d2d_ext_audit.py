#!/usr/bin/env python3
"""Independent E(1)-Koszul audit for D2d Thom twists; no classifier inputs."""
from functools import lru_cache
from itertools import product
from pathlib import Path
import json
weights=(1,1,2)
one=frozenset({(0,0,0)});zero=frozenset()
a=frozenset({(1,0,0)});b=frozenset({(0,1,0)});w=frozenset({(0,0,1)})
def add(*ps):
 r=set()
 for p in ps:r.symmetric_difference_update(p)
 return frozenset(r)
def mul(p,q):
 r=set()
 for m in p:
  for n in q:
   z=tuple(x+y for x,y in zip(m,n))
   if z[0] and z[1]:continue
   r.symmetric_difference_update({z})
 return frozenset(r)
def degree(m):return sum(x*y for x,y in zip(m,weights))
@lru_cache(None)
def basis(d):
 if d<0:return ()
 return tuple(m for m in product(range(d+1),repeat=3) if degree(m)==d and not(m[0] and m[1]))
v=add(a,b)
gens=[(a,mul(a,a),zero),(b,mul(b,b),zero),(w,mul(v,w),mul(w,w))]
@lru_cache(None)
def sq_monomial(m,k):
 vals=[one,zero,zero]
 for i,power in enumerate(m):
  for _ in range(power):
   vals=[add(*(mul(vals[l],gens[i][j]) for l in range(3) for j in range(3) if l+j==n)) for n in range(3)]
 return vals[k]
def sq(p,k):return add(*(sq_monomial(m,k) for m in p))
def S1(p):return add(sq(p,1),mul(a,p))
def S2(p):return add(sq(p,2),mul(a,sq(p,1)),mul(w2,p))
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

result={}
for spin,w2 in [('spinless',add(w,mul(v,v))),('spin_half',zero)]:
 differential.cache_clear()
 checks=0
 for d in range(10):
  for m in basis(d):
   p=frozenset({m})
   assert not Q0(Q0(p)) and not Q1(Q1(p)) and Q0(Q1(p))==Q1(Q0(p))
   checks+=3
 for s in range(13):
  for n in range(7):
   t=s+n
   assert all(not apply(differential(s+1,t),x) for x in differential(s,t))
   checks+=1
 for ss in range(13):
  for nn in range(7):
   tt=ss+nn;src=cells(ss,tt);dst=cells(ss+1,tt+1);di={z:i for i,z in enumerate(dst)}
   hh=[1<<di[z] for z in src]
   src2=cells(ss+1,tt);dst2=cells(ss+2,tt+1);di2={z:i for i,z in enumerate(dst2)}
   hh2=[1<<di2[z] for z in src2]
   assert [apply(differential(ss+1,tt+1),z) for z in hh]==[apply(hh2,z) for z in differential(ss,tt)]
   checks+=1
 rows={str(n):[ext(s,n) for s in range(13)] for n in range(7)}
 h0={str(n):[h0_rank(s,n) for s in range(5)] for n in range(7)}
 result[spin]={'w1':'a','w2':sorted(w2),'E2_by_stem_and_filtration':rows,'h0_ranks':h0,'checks':checks}
print(json.dumps(result,indent=2))
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
