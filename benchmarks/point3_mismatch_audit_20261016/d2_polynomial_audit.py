#!/usr/bin/env python3
"""Standalone Steenrod/Bockstein audit over F2[x,y] and normalized bar cochains.
No project modules or classification tables are imported.
"""
from itertools import product
from math import comb
from pathlib import Path
import hashlib,json

def plus(*polys):
    z=set()
    for p in polys:z.symmetric_difference_update(p)
    return z

def sq(p,k):
    z=set()
    for a,b in p:
        for i in range(k+1):
            j=k-i
            if i<=a and j<=b and comb(a,i)*comb(b,j)%2:
                z.symmetric_difference_update({(a+i,b+j)})
    return z

def poly(p):return sorted([list(x) for x in p])
def x(g):return g&1
def y(g):return (g>>1)&1
def q(t):
    g,h,k=t
    return x(g)*x(h)*y(k)-x(g)*y(h)*y(k)
def delta(f,t):
    a=f(t[1:])+(-1)**len(t)*f(t[:-1])
    for i in range(len(t)-1):a+=(-1)**(i+1)*f(t[:i]+(t[i]^t[i+1],)+t[i+2:])
    return a

def cup1(t):
    z=0
    for j in range(3):
        block=t[j:j+3];merged=block[0]^block[1]^block[2]
        z^=(q(t[:j]+(merged,)+t[j+3:])%2)*(q(block)%2)
    return z

def bock(t):
    z=delta(cup1,t)
    assert z%2==0
    return z//2

def bar_vector(f,n):
    out=0
    for i,t in enumerate(product((1,2,3),repeat=n)):
        if f(t)%2:out|=1<<i
    return out

def boundary_basis(n):
    cols=list(product((1,2,3),repeat=n));ci={t:i for i,t in enumerate(cols)}
    v=[0]*len(cols)
    for row,t in enumerate(product((1,2,3),repeat=n+1)):
        terms=[t[1:],t[:-1]]
        terms += [t[:i]+(t[i]^t[i+1],)+t[i+2:] for i in range(n)]
        for u in terms:
            if 0 not in u:v[ci[u]]^=1<<row
    basis={}
    for a in v:
        while a:
            p=a.bit_length()-1
            if p in basis:a^=basis[p]
            else:basis[p]=a;break
    return basis

def rem(a,basis):
    for p in sorted(basis,reverse=True):
        if (a>>p)&1:a^=basis[p]
    return a

c={(2,1),(1,2)};o=sq(c,2);b=sq(o,1)
assert o=={(4,1),(1,4)} and b=={(4,2),(2,4)}
assert sq(c,1)==set() and b=={(2*a,2*d) for a,d in c}
assert sq(sq({(2,0)},2),1)==sq(sq({(0,2)},2),1)==set()
phase=[sq({(3,1)},1),sq({(1,3)},1)]
assert all(phase) and phase[0]!=phase[1]
assert all(delta(q,t)==0 for t in product(range(4),repeat=4))
B=boundary_basis(5)
bv=bar_vector(bock,6)
q2=bar_vector(lambda t:q(t[:3])*q(t[3:]),6)
pv=bar_vector(lambda t:x(t[0])*x(t[1])*x(t[2])*x(t[3])*y(t[4])*y(t[5]) ^ x(t[0])*x(t[1])*y(t[2])*y(t[3])*y(t[4])*y(t[5]),6)
assert rem(bv,B)!=0
assert rem(bv^q2,B)==rem(bv^pv,B)==0
out={'status':'PASS','scope':'Independent normalized-bar F2 cohomology and polynomial Cartan audit; no classifier imports.',
 'charge_mod2':poly(c),'Sq2_charge':poly(o),'Sq1_Sq2_charge':poly(b),
 'phase_integral_reductions':[poly(z) for z in phase],
 'incoming_closed_charge_gauge_reductions':[[],[]],
 'all_bar_integer_closure_checks':4**4,'normalized_degree6_cells':3**6,
 'normalized_d5_rank_mod2':len(B),'bockstein_nonzero':True,'bockstein_equals_charge_square_in_cohomology':True,
 'bockstein_equals_polynomial_in_cohomology':True,
 'source_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
p=Path(__file__).with_suffix('.json');p.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps(out))
