#!/usr/bin/env python3
"""Audit saved independent results without consulting any reference answers."""
import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys


def product(a, b):
    if not a:
        return []
    cols = list(zip(*b))
    return [[sum(x*y for x, y in zip(row, col)) for col in cols] for row in a]


def determinant(matrix):
    """Fraction-free elimination; all matrices here have exact integer entries."""
    a = [list(r) for r in matrix]
    n = len(a)
    sign, previous = 1, 1
    for k in range(n-1):
        p = next((i for i in range(k, n) if a[i][k]), None)
        if p is None:
            return 0
        if p != k:
            a[k], a[p] = a[p], a[k]
            sign = -sign
        pivot = a[k][k]
        for i in range(k+1, n):
            for j in range(k+1, n):
                numerator = pivot*a[i][j]-a[i][k]*a[k][j]
                assert numerator % previous == 0, "nonexact Bareiss division"
                a[i][j] = numerator//previous
            a[i][k] = 0
        previous = pivot
    return sign*a[-1][-1] if n else 1


def order_signature(orders):
    assert all(isinstance(x, int) and (x == 0 or x > 1) for x in orders)
    return orders.count(0), math.prod(x for x in orders if x)


def check_smith(matrix, left, right, diag):
    m, n = len(matrix), len(right)
    assert len(left) == m and all(len(row) == m for row in left), 'Smith left matrix has wrong shape'
    assert all(len(row) == n for row in right), 'Smith right matrix is not square'
    assert all(len(row) == n for row in matrix), 'presentation has inconsistent column count'
    assert len(diag) <= min(m, n), 'Smith diagonal has wrong length'
    assert abs(determinant(left)) == abs(determinant(right)) == 1, 'non-unimodular Smith transformation'
    transformed = product(product(left, matrix), right)
    for i, row in enumerate(transformed):
        for j, value in enumerate(row):
            assert value == (diag[i] if i == j and i < len(diag) else 0), 'Smith matrix identity failed'
    nonzero = [abs(x) for x in diag if x]
    assert all(b % a == 0 for a, b in zip(nonzero, nonzero[1:])), 'Smith factors do not divide'


def check_result(d):
    assert d['convention'] == 'physical-spin-half-det-sign-omega0'
    assert d['sptset_loaded'] is False, 'unexpected SptSet runtime dependency'
    assert d.get('classification_status', d['status']) == 'computed'
    assert d['pip']['status'] == 'computed'
    orders = d['pip']['orders']+d['majorana']+d['complex_fermion']+d['bosonic']
    layer_order = order_signature(orders)
    assert d['pip']['free_rank'] == d['pip']['orders'].count(0)
    if 'free_lattice' in d['pip']:
        free = d['pip']['free_lattice']
        r = d['pip']['free_rank']
        assert free['status'] == 'computed' and free['rank'] == r
        assert free['fullFreePhaseWitness'] is True
        basis = free['latticeBasis']
        assert len(basis) == r and all(len(row) == r for row in basis)
        assert all(isinstance(x, int) for row in basis for x in row)
        assert abs(determinant(basis)) == free['latticeIndex']
        parity = free['survivingParityBasis']
        assert all(len(row) == r and all(x in (0, 1) for x in row) for row in parity)
        assert all(1 in row for row in parity)
        pivots = [row.index(1) for row in parity]
        assert pivots == sorted(set(pivots))
        assert all(parity[i][p] == int(i == j) for j, p in enumerate(pivots) for i in range(len(parity)))
        for row in basis:
            residual = [x % 2 for x in row]
            for pivot, vector in zip(pivots, parity):
                if residual[pivot]:
                    residual = [(x+y) % 2 for x, y in zip(residual, vector)]
            assert not any(residual), 'free lattice is outside its surviving parity span'
        assert free['latticeIndex'] == 2**(r-len(parity))
        indices = free['freeIndices']
        assert len(indices) == r and len(set(indices)) == r and all(i > 0 for i in indices)
        assert len(free['generators']) == r
        for i, generator in enumerate(free['generators']):
            assert generator['name'] == 'Pfree%d' % (i+1)
            assert [generator['h1Coordinates'][j-1] for j in indices] == basis[i]
            for value in generator['phase4']:
                assert len(value) == 2 and all(isinstance(x, int) for x in value) and value[1] > 0
    hashes = d['source_sha256']
    assert hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest() == d['source_id']
    if 'stacking' not in d:
        return 'classification'
    s = d['stacking']
    if s['status'] != 'computed':
        return 'stacking-unresolved'
    assert order_signature(s['invariants']) == layer_order, 'stacking does not preserve graded order/rank'
    low = s['lower']
    assert order_signature(low['invariants']) == order_signature(d['majorana']+d['complex_fermion']+d['bosonic'])
    matrix = low['presentation']
    left, right = low['smithRowTransform'], low['smithColumnTransform']
    diag = low['smithDiagonal']
    check_smith(matrix, left, right, diag)
    lower_rank = sum(x != 0 for x in diag)
    lower_invariants = [0]*(len(right)-lower_rank)+[abs(x) for x in diag if abs(x) > 1]
    assert low['invariants'] == lower_invariants, 'lower presentation and reported group differ'
    # Older zero-free-rank exports can omit this redundant field.
    free_pip = s.get('freePipRank', 0)
    assert type(free_pip) is int and free_pip == d['pip']['free_rank'], 'stacking/classification free p+ip rank differs'
    if s.get('fullUpperPhaseWitness') is True:
        check_smith(s['fullPresentation'], s['fullSmithRowTransform'],
                    s['fullSmithColumnTransform'], s['fullSmithDiagonal'])
        assert 'pipGenerator' in s and 'pipRelation' in s
        inv = [abs(x) for x in s['fullSmithDiagonal'] if abs(x) > 1]
        rank = sum(x != 0 for x in s['fullSmithDiagonal'])
        free = len(s['fullSmithColumnTransform'])-rank+free_pip
        assert s['invariants'] == [0]*free+inv, 'full presentation and reported group differ'
    if not any(d['pip']['orders']):
        assert s['invariants'] == [0]*free_pip+lower_invariants, 'free p+ip split and reported group differ'
    assert low['enumeratedPhaseProducts'] == 0
    if s.get('fullUpperPhaseWitness') is False:
        return 'stacking-upper-abstract-certificate'
    return 'stacking-with-generator-relations'


def check_complete_witnesses(d, formula_convention=None):
    """Require actual lifts, beyond abstract group/presentation consistency."""
    check_result(d)
    s = d.get('stacking', {})
    assert s.get('status') == 'computed', 'full stacking is missing'
    if 2 in d['pip']['orders']:
        assert s.get('fullUpperPhaseWitness') is True, 'torsion p+ip phase witness is missing'
    if d['pip']['free_rank']:
        f = d['pip'].get('free_lattice', {})
        assert f.get('status') == 'computed' and f.get('fullFreePhaseWitness') is True, 'primitive free p+ip phase witnesses are missing'
    if formula_convention is not None:
        assert d.get('formula_convention') == formula_convention, 'formula convention differs from the required version'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('run')
    ap.add_argument('--allow-partial', action='store_true')
    ap.add_argument('--write', action='store_true')
    ap.add_argument('--require-complete-witnesses', action='store_true')
    ap.add_argument('--require-formula-convention')
    args = ap.parse_args()
    if not __debug__:
        ap.error('certificate auditing requires Python without -O or PYTHONOPTIMIZE')
    root = Path(args.run)
    errors, kinds, groups = [], Counter(), set()
    for path in sorted(root.glob('sg*.json')):
        if '.raw.' in path.name:
            continue
        try:
            d = json.loads(path.read_text())
            n = d['space_group']
            assert 1 <= n <= 230 and n not in groups, 'invalid or duplicate group'
            groups.add(n)
            kinds[check_result(d)] += 1
            if args.require_complete_witnesses or args.require_formula_convention:
                check_complete_witnesses(d, args.require_formula_convention)
        except (AssertionError, KeyError, ValueError, TypeError, IndexError) as exc:
            errors.append(dict(file=path.name, reason=str(exc)))
    missing = sorted(set(range(1, 231))-groups)
    report = dict(groups=len(groups), checks=dict(kinds), errors=errors,
                  missing=missing, complete=not missing and not errors and not kinds['stacking-unresolved'],
                  external_answers_consulted=False)
    report['complete_witnesses_required'] = args.require_complete_witnesses or bool(args.require_formula_convention)
    report['required_formula_convention'] = args.require_formula_convention
    text = json.dumps(report, indent=2, sort_keys=True)+'\n'
    print(text, end='')
    if args.write:
        (root/'audit.json').write_text(text)
    return bool(errors or kinds['stacking-unresolved'] or (missing and not args.allow_partial))


if __name__ == '__main__':
    sys.exit(main())
