#!/usr/bin/env python3
"""Pointwise carry and Cartan checks for the commuting nonsplit examples.

The proof for general orders is the Cartan identity with Sq1(carry)=0.
This script exhausts cyclic M=2,4 and the pair (2,2), then replays the
identity on reproducible samples for the other orders, including M=10.
The p+ip parity check uses the native formula coordinate, and is not used
to declare a physical upper-cochain representative identically zero.
"""
import argparse
import itertools
import json
import random
import sys
from fractions import Fraction
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--formula-repo', type=Path, default=Path(__file__).resolve().parents[3])
parser.add_argument('--output', type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.formula_repo.resolve()))
from fspt.formulas import field, cup, zero, word, square, evaluate, pip_majorana, pip_parity
from fspt.majorana_complete import obstruction

random.seed(20261101)
coordinate = field('coordinate', 1, None)
carry = field('carry', 2)
coordinate2 = field('coordinate2', 1, None)
carry2 = field('carry2', 2)
cyclic_cf = carry * carry
cyclic_cartan = word('1231343', carry, carry, carry, carry)
mixed_cf = carry * carry2
mixed_cartan = word('1231343', carry, carry, carry2, carry2)


def integer_cup(a, b):
    return cup(a, b, integer=True)


def fields(vertices, orders):
    result = {}
    for j, N in enumerate(orders):
        def coordinate_value(face, j=j, N=N):
            return (vertices[face[1]][j] - vertices[face[0]][j]) % N
        def carry_value(face, j=j, N=N):
            return (((vertices[face[1]][j] - vertices[face[0]][j]) % N)
                    + ((vertices[face[2]][j] - vertices[face[1]][j]) % N)) // N
        suffix = '' if j == 0 else '2'
        result['coordinate' + suffix] = coordinate_value
        result['carry' + suffix] = carry_value
    return result


records = []
for M in [2, 4, 6, 8, 10, 12]:
    cyclic_phase = integer_cup(coordinate, integer_cup(carry, carry)).scale(Fraction(1, 2*M))
    cyclic_phase = cyclic_phase + cyclic_cartan.lift().scale(Fraction(1, 2))
    residual = (obstruction(zero(3), cyclic_cf, carry, zero(1)).scale(Fraction(1, 8))
                - cyclic_phase.differential()).reduce(1)
    secondary = obstruction(carry, zero(3), carry, zero(1))
    first = pip_majorana(carry.lift(), carry, zero(1))
    second = pip_parity(carry.lift(), zero(3), carry, zero(1))
    points = itertools.product(range(M), repeat=6) if M in (2,4) else (
        tuple(random.randrange(M) for _ in range(6)) for _ in range(2000))
    count = 0
    for values in points:
        vertices = [(0,)] + [(x,) for x in values]
        data = fields(vertices, [M])
        for name, expr in [('complex phase', residual), ('incoming secondary', secondary),
                           ('integer first', first), ('native integer second', second)]:
            assert evaluate(expr, data) == 0, (M, name, values)
        count += 1
    records.append({'cyclic_order': M, 'six_simplices': count,
                    'exhaustive': M in (2,4), 'all_residuals': 0})

for M,N in [(2,2),(2,4),(4,2),(4,4),(6,10),(10,4),(8,12)]:
    mixed_phase = integer_cup(carry, integer_cup(coordinate2,carry2)).scale(Fraction(1,2*N))
    mixed_phase = mixed_phase + mixed_cartan.lift().scale(Fraction(1,2))
    residual = (obstruction(zero(3),mixed_cf,carry,zero(1)).scale(Fraction(1,8))
                - mixed_phase.differential()).reduce(1)
    points = itertools.product(range(M*N),repeat=6) if (M,N)==(2,2) else (
        tuple(random.randrange(M*N) for _ in range(6)) for _ in range(3000))
    count=0
    for values in points:
        vertices=[(0,0)]+[(x//N,x%N) for x in values]
        assert evaluate(residual,fields(vertices,[M,N]))==0,(M,N,values)
        count+=1
    records.append({'orders':[M,N], 'six_simplices':count,
                    'exhaustive':(M,N)==(2,2), 'mixed_phase_residual':0})
if args.output:
    args.output.write_text(json.dumps(records,indent=2)+'\n')
print(json.dumps(records,indent=2))
