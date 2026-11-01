#!/usr/bin/env python3
"""Check the compact arbitrary-order commuting-extension formulas.

These are algebraic simplifications of the proven primary formulas, not new
AHSS runs or an inference of terminal independence from final groups.
"""
import argparse
import json
import math
import sys
from pathlib import Path

parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--verification-dir', type=Path, default=Path(__file__).resolve().parents[1])
parser.add_argument('--through', type=int, default=80)
parser.add_argument('--output', type=Path)
args = parser.parse_args()
sys.path.insert(0, str(args.verification_dir.resolve()))
from nonsplit_closed_formula import nonsplit_closed_formula, combine_primary
from nonsplit_layers import nonsplit_layers

groups_checked = layers_checked = 0
for M in range(2, args.through + 1, 2):
    for N in range(1, args.through + 1):
        d = math.gcd(N, 2)
        g = math.gcd(M, N)
        h = math.gcd(M // 2, N)
        proposed = {
            'pip': [M, N // d],
            'majorana': [2] * d,
            'complex_fermion': [2] * d,
            'bosonic': [M, N // d, g, h],
        }
        expected_layers = nonsplit_layers(M, [N])
        for name, factors in proposed.items():
            assert combine_primary(factors) == expected_layers[name], (M, N, name)
        layers_checked += 1
        if M * N % 3:
            k = math.gcd(N // d, d * g)
            factors = [M // 2, 8 * M, N // d, h, k, d * N * g // k]
            assert combine_primary(factors) == nonsplit_closed_formula(M, [N]), (M, N)
            groups_checked += 1
print(f'Full layer formula: {layers_checked} arbitrary-order pairs passed.')
print(f'3-free full group formula: {groups_checked} arbitrary-order pairs passed.')
if args.output:
    args.output.write_text(json.dumps({'orders_through':args.through,
        'layer_pairs_checked':layers_checked,'group_pairs_checked':groups_checked,
        'all_comparisons_passed':True},indent=2)+'\n')
