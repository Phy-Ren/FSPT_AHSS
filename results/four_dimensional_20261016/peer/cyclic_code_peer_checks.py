#!/usr/bin/env python3
"""Independent bounded arithmetic and off-cycle review, not a campaign."""
import json
import random
import sys
import time
from fractions import Fraction as F
from itertools import product
from pathlib import Path

REPOSITORY = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/home/xingyu/FSPT_AHSS_insulator')
sys.path.insert(0, str(REPOSITORY))
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
from insulator import cyclic_physical as physical
from insulator.cyclic4p1 import ExactOperations, canonical_roots

rng = random.Random(20261016)
checks = {}
started = time.monotonic()
count = 0
for dimension in range(1, 5):
    for sample in range(40):
        while True:
            matrix = [[rng.randrange(-10, 11) for j in range(dimension)]
                      for i in range(dimension)]
            if physical.determinant(matrix):
                break
        assert physical.column_hnf(matrix) == hermite_normal_form(Matrix(matrix)).tolist()
        count += 1
checks['independent_sympy_column_hnf'] = count

count = 0
for denominator in (2, 3, 4, 5, 6):
    for sample in range(4):
        integers = [[rng.randrange(-denominator, denominator + 1) for j in range(4)]
                    for i in range(5)]
        rows = [[F(value, denominator) for value in row] for row in integers]
        kernel = physical.character_kernel(rows)
        kernel_count = sum(
            all(sum(a * b for a, b in zip(row, vector)) % denominator == 0
                for row in integers)
            for vector in product(range(denominator), repeat=4))
        assert abs(physical.determinant(kernel)) == denominator**4 // kernel_count
        count += 1
checks['independent_brute_character_kernel'] = count

count = 0
for order in (2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 16, 18):
    kernel = physical.character_kernel(physical.eta_characters(order))
    assert abs(physical.determinant(kernel)) == order**4
    count += 1
checks['independent_eta_kernel_order'] = count

count = 0
for order in (2, 3, 4, 6):
    for sample in range(4):
        arguments = tuple(rng.randrange(order) for _ in range(6))
        a, x, zero, symmetry, roots = canonical_roots(order, arguments)
        operations = ExactOperations()
        q = order * (order - 1) // 2 % order
        negative_charge = operations.power(symmetry, roots[2], -q)
        for index, root in enumerate(roots):
            operations.validate(symmetry, root)
            power = operations.power(symmetry, root, order)
            power = operations.gauge(
                symmetry, power, a.sc(-1) if index == 0 else zero(1),
                a.sc(-1) if index == 1 else zero(1), zero(3))
            if index == 1 and q:
                power = operations.stack(symmetry, power, negative_charge)
            multiple = ((order * (order - 1) // 2 - q) // order if index == 1
                        else 1 if index == 2 else 0)
            power = operations.gauge(symmetry, power, zero(1), zero(1), a.cup(x).sc(-multiple))
            assert all(not value.maxabs() for value in (power.e_p, power.n_p, power.n_p2))
            assert not power.nu_p3.d().mod(1).maxabs()
            count += 1
checks['off_cycle_six_simplex_full_relation_checks'] = count

result = {'status': 'PASS', 'seed': 20261016, 'checks': checks,
          'seconds': time.monotonic() - started,
          'scope': 'Independent bounded arithmetic and off-cycle degree-six completion checks; not a replacement for universal identities or a full classification campaign.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
