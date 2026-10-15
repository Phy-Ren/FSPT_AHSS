"""Universal middle-four interchange identity and signed realization checks."""
from collections import Counter
from itertools import product
from pathlib import Path
from random import Random
import json
import sys

sys.path.insert(0,'/home/xingyu/FSPT_AHSS_insulator')
from insulator._engine import e8_4p1 as neutral
from insulator._engine.simplex import rand


def add(a,b):
    return tuple(x+y for x,y in zip(a,b))


def symbol(a,b):
    return Counter({(a,b):1})


def linear(*terms):
    out=Counter()
    for coefficient,term in terms:
        for key,value in term.items():
            out[key]+=coefficient*value
    return Counter({k:v for k,v in out.items() if v})


def dA(a,b,c):
    return linear((1,symbol(a,b)),(1,symbol(add(a,b),c)),
                  (-1,symbol(b,c)),(-1,symbol(a,add(b,c))))


def dC(a,b):
    return linear((1,symbol(a,b)),(-1,symbol(b,a)))


a,b,e,f = tuple(tuple(int(i==j) for j in range(4)) for i in range(4))
residual = linear((1,symbol(a,b)),(1,symbol(e,f)),(1,symbol(add(a,b),add(e,f))),
                  (-1,symbol(a,e)),(-1,symbol(b,f)),(-1,symbol(add(a,e),add(b,f))))
primitive_differential = linear((1,dC(b,e)),(1,dA(a,b,e)),(-1,dA(a,e,b)),
                               (-1,dA(add(a,b),e,f)),(1,dA(add(a,e),b,f)))
assert linear((1,residual),(-1,primitive_differential)) == {}

rng=Random(2026101517)
checks=0
gauge_checks=0
for signs in product((0,1),repeat=6):
    a,b,e,f=(rand(5,1,signs,rng,lo=-3,hi=4).d() for _ in range(4))
    P,A,C=neutral.product,neutral.associator,neutral.commutator
    D=P(a,b)+P(e,f)+P(a+b,e+f)-P(a,e)-P(b,f)-P(a+e,b+f)
    K=C(b,e)+A(a,b,e)-A(a,e,b)-A(a+b,e,f)+A(a+e,b,f)
    assert (D-K.d()).mod(1).maxabs()==0
    checks+=1
    u,v=(rand(5,1,signs,rng,lo=-2,hi=3) for _ in range(2))
    H=neutral.pair_gauge(a,e,u,v)
    gauge_residual=(neutral.gauge(a,u)+neutral.gauge(e,v)
                    +P(a+u.d(),e+v.d())-P(a,e)
                    -neutral.gauge(a+e,u+v))
    assert (gauge_residual-H.d()).mod(1).maxabs()==0
    gauge_checks+=1

result={'status':'PASS','universal_formal_identity':True,
        'formal_identity_assumptions':'dA=P(a,b)+P(a+b,c)-P(b,c)-P(a,b+c); dC=P(a,b)-P(b,a)',
        'signed_realization_checks':checks,
        'signed_gauge_prism_checks':gauge_checks,
        'parity_mixed_periodicity_status':'Established separately by paired-DAG and normalized-chain certificates; not inferred from this identity',
        'scope':'4+1D relative E8 mixed product primitive, not the missing pure-CI R/K'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
