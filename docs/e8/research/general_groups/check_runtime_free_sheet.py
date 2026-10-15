"""Independent global Z^4 free-sheet check of the new local production API.

This does not run a global classifier or write into the production repository.
The completed neutral phase is constructed directly on the infinite group.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
from random import Random
import json
import sys

sys.path.insert(0, '/home/xingyu/FSPT_AHSS_insulator')
from insulator import api as ci
from insulator.e8 import State
from insulator._engine.simplex import C, char


def add(g, h):
    return tuple(a + b for a, b in zip(g, h))


def difference(g, h):
    return tuple(b - a for a, b in zip(g, h))


def e_2(g, h, offset=0):
    return g[offset] * h[offset + 1]


def h_3(g, h, k, offset=0):
    xg, xh, yh, yk = g[offset], h[offset], h[offset + 1], k[offset + 1]
    return xg*xh*yh*yk + xg*(xg-1)//2*yh*yk


def higher_cup(g, h, k):
    return e_2(add(g,h),k)*e_2(g,h,2) - e_2(g,add(h,k))*e_2(h,k,2)


def nu_5(g, h, k, l, m):
    direct = h_3(g,h,k)*e_2(l,m) + h_3(g,h,k,2)*e_2(l,m,2)
    twist = (higher_cup(g,h,k)*(e_2(l,m)-e_2(l,m,2))
             - (e_2(g,h)-e_2(g,h,2))*higher_cup(k,l,m))
    return Fraction(direct+twist,3)


def local(vertices, degree, operation):
    data = {}
    for face in combinations(range(len(vertices)), degree+1):
        word = tuple(difference(vertices[a],vertices[b]) for a,b in zip(face,face[1:]))
        data[face] = operation(*word)
    return C(len(vertices)-1,degree,data)


rng = Random(2026101501)
checks = {'global_free_sheet_validations':0, 'nonzero_integer_gauges':0,
          'exact_inverse_states':0, 'self_stacks':0}
for _ in range(6):
    vertices = [tuple(rng.randrange(-8,9) for _ in range(4))]
    for _ in range(6):
        vertices.append(add(vertices[-1],tuple(rng.randrange(-4,5) for _ in range(4))))
    symmetry = ci.Symmetry(C(6,2,{}),char(6,[0]*7),char(6,[0]*7))
    sheet = local(vertices,2,lambda g,h:e_2(g,h)+e_2(g,h,2))
    state = State(sheet,C(6,2,{}),C(6,4,{}),local(vertices,5,nu_5))
    state.validate(symmetry,4)
    checks['global_free_sheet_validations'] += 1
    parameter = local(vertices,1,lambda g:g[0]*g[1]-g[2])
    state.gauge(symmetry,4,parameter,C(6,1,{}),C(6,3,{})).validate(symmetry,4)
    checks['nonzero_integer_gauges'] += 1
    identity = state.stack(state.inverse(symmetry,4),symmetry,4)
    assert all(c.maxabs()==0 for c in (identity.e_p,identity.n_p,identity.n_p2,identity.nu_p3))
    checks['exact_inverse_states'] += 1
    state.stack(state,symmetry,4).validate(symmetry,4)
    checks['self_stacks'] += 1

result = {'status':'PASS','group':'Z^4','state_order':'(e_2,n_2,n_4,nu_5)',
          'checks':checks,'scope':'Independent global free neutral sheets; local production API only'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result))
