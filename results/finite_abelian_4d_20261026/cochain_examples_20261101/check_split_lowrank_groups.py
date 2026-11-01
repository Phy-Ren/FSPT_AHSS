"""Compare the compact low-rank formulas with the retained primary formulas.

This is an independent assembly check, not a rerun of the full AHSS.
The cochain tests are check_split_pair_cochains.py and
check_split_pair_secondary.py.
"""
import json
import math
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from split_closed_formula import invariant_factors as full_group
from split_layers import invariant_factors, split_layers

cyclic_count = 0
for order in range(1, 501):
    reduced_order = order // math.gcd(order, 2)
    extension = math.gcd(reduced_order, 6)
    compact = invariant_factors([reduced_order // extension, reduced_order * extension])
    assert compact == full_group([order]), (order, compact, full_group([order]))
    cyclic_count += 1

pair_count = 0
for first in range(1, 81):
    for second in range(first, 81):
        if first % 3 == 0 or second % 3 == 0 or first % 4 == 0 or second % 4 == 0:
            continue
        first_reduced = first // math.gcd(first, 2)
        second_reduced = second // math.gcd(second, 2)
        common = math.gcd(first_reduced, second_reduced)
        compact = invariant_factors([first_reduced] * 2 + [second_reduced] * 2 + [common] * 2)
        assert compact == full_group([first, second]), (first, second, compact)
        expected_layers = {
            'pip': invariant_factors([first_reduced, second_reduced]),
            'majorana': [],
            'complex_fermion': [],
            'bosonic': invariant_factors([first_reduced, second_reduced, common, common]),
        }
        assert expected_layers == split_layers([first, second]), (first, second)
        pair_count += 1

print(json.dumps({'cyclic_orders_checked': cyclic_count,
                  'eligible_two_factor_pairs_checked': pair_count,
                  'all_comparisons_passed': True}, indent=2))
