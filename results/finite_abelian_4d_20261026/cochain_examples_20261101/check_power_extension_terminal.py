#!/usr/bin/env python3
"""Audit whether terminal bosonic changes can alter the abstract stacking group.

The archived relation matrix is reduced to the subgroup with zero p+ip layer.
Every bosonic class is embedded in this subgroup using an exact Smith basis.
The exhaustive cases vary every p+ip power relation by every such class.
Counterexample searches stop at the first change of abstract group.
No manuscript or public formula file is changed.
"""
import argparse
import hashlib
import itertools
import json
from pathlib import Path

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp


def invariant_factors(rows):
    diagonal = smith_normal_form(Matrix(rows), domain=ZZ)
    return tuple(abs(int(diagonal[i, i])) for i in range(min(diagonal.shape))
                 if abs(diagonal[i, i]) > 1)


def audit(path, repository_root, exhaustive=True):
    data = json.loads(path.read_text())
    generators = data['generators']
    relations = data['presentation']
    lower = [i for i, g in enumerate(generators) if g['layer'] < 3]
    integer = [i for i, g in enumerate(generators) if g['layer'] == 3]
    bosonic = [i for i, g in enumerate(generators) if g['layer'] == 0]
    assert integer
    for p in integer:
        assert relations[p][p] == generators[p]['quotientOrder']
        assert all(relations[p][q] == 0 for q in integer if p != q)
    for row in relations[len(generators):]:
        assert all(row[p] == 0 for p in integer), 'Unexpected integer incoming identification'

    lower_relations = Matrix([[row[j] for j in lower] for row in relations
                              if all(row[p] == 0 for p in integer)])
    diagonal, left, right = smith_normal_decomp(
        DomainMatrix.from_Matrix(lower_relations).convert_to(ZZ))
    diagonal = diagonal.to_Matrix()
    right = right.to_Matrix()
    kept = [i for i in range(len(lower)) if abs(diagonal[i, i]) > 1]
    orders = [abs(int(diagonal[i, i])) for i in kept]
    rank = len(orders)

    embedded = [tuple(int(right[lower.index(d), i]) % q
                      for i, q in zip(kept, orders)) for d in bosonic]
    bosonic_elements = {(0,) * rank}
    for vector, d in zip(embedded, bosonic):
        bosonic_elements = {
            tuple((a + j * v) % q for a, v, q in zip(z, vector, orders))
            for z in bosonic_elements
            for j in range(generators[d]['quotientOrder'])
        }
    bosonic_elements = sorted(bosonic_elements)

    integer_rows = []
    for p in integer:
        transformed = Matrix([[relations[p][j] for j in lower]]) * right
        integer_rows.append([int(transformed[0, i]) for i in kept]
                            + [relations[p][q] for q in integer])
    reduced = [[q if j == i else 0 for j in range(rank + len(integer))]
               for i, q in enumerate(orders)] + integer_rows
    expected = tuple(data['invariants'])
    assert invariant_factors(reduced) == expected

    output = {
        'source': path.relative_to(repository_root).as_posix(),
        'sha256': hashlib.sha256(path.read_bytes()).hexdigest(),
        'background': data.get('model'),
        'original_group': expected,
        'non_integer_subgroup': orders,
        'bosonic_subgroup_order': len(bosonic_elements),
        'bosonic_generator_names': [generators[d]['name'] for d in bosonic],
        'bosonic_embeddings': embedded,
        'integer_generator_names': [generators[p]['name'] for p in integer],
        'integer_quotient_orders': [generators[p]['quotientOrder'] for p in integer],
        'reduced_relation_matrix': reduced,
        'exhaustive': exhaustive,
    }
    fourth_page = next(page for page in data['pipPages'] if page['page'] == 4)
    assert fourth_page['sourceOrders'] == fourth_page['survivingOrders']
    assert all(entry['status'] == 'survives' and not any(entry['d4'])
               for entry in fourth_page['evaluations'])
    output['fourth_obstruction_zero_on_generators'] = True
    output['integer_layer_before_and_after_fourth_obstruction'] = fourth_page['sourceOrders']
    if exhaustive:
        shifts = itertools.product(bosonic_elements, repeat=len(integer))
    else:
        shifts = (tuple(z if i == p else (0,) * rank for i in range(len(integer)))
                  for p in range(len(integer)) for z in bosonic_elements)
    groups = set()
    checked = 0
    for shift in shifts:
        trial = [row[:] for row in reduced]
        for j, vector in enumerate(shift):
            for i, v in enumerate(vector):
                trial[rank + j][i] += v
        result = invariant_factors(trial)
        groups.add(result)
        checked += 1
        if result != expected and 'counterexample' not in output:
            output['counterexample'] = {'bosonic_shifts': shift, 'group': result}
            if not exhaustive:
                break
    output['shifts_checked'] = checked
    output['groups_obtained'] = sorted(groups)
    output['all_bosonic_changes_leave_group_unchanged'] = exhaustive and groups == {expected}
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--formula-repo', type=Path,
                        default=Path(__file__).resolve().parents[3])
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    repository_root = args.formula_repo.resolve()
    raw = repository_root / 'results/complete_formulas/raw'
    safe = ['C2_w1_s0', 'C4_orbit_001', 'C2xC2_orbit_001',
            'C4xC2_orbit_001', 'C4xC2_orbit_004', 'C4xC4_orbit_001']
    unsafe = ['C8_orbit_001', 'C8xC2_orbit_001', 'C8xC2_orbit_004']
    results = [audit(raw / f'd4_{tag}.json', repository_root, True) for tag in safe]
    results += [audit(raw / f'd4_{tag}.json', repository_root, False) for tag in unsafe]
    assert all(r['all_bosonic_changes_leave_group_unchanged'] for r in results[:len(safe)])
    assert all('counterexample' in r for r in results[len(safe):])
    if args.output:
        args.output.write_text(json.dumps(results, indent=2) + '\n')
    for result in results:
        print(result['background'], 'exhaustive=' + str(result['exhaustive']),
              'cases=' + str(result['shifts_checked']),
              'groups=' + str(result['groups_obtained']))


if __name__ == '__main__':
    main()
