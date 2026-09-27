#!/usr/bin/env python3
"""Audit saved spinless/Pin-minus certificates without reference answers or GAP.

Finite Pin tables, native F2 background certificates, integral presentations,
filtered H0 quotients and Ext-family algebra are recomputed exactly. Native
nonlinear cochain lifts retain their source/homotopy recipes; this audit does not
reconstruct their bar callbacks or rerun the physical classification.
"""
import argparse
from collections import Counter
import copy
import csv
from fractions import Fraction
import hashlib
import json
import math
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent))
from audit_run import check_result as check_zero_result, check_complete_witnesses as check_zero_witnesses
from audit_run import check_smith, determinant, product, order_signature

CONVENTION = 'physical-spinless-det-sign-Pin-minus'
FORMULA = 'normalized-pip-aw-edge-transport-v2'


def integer(x):
    return type(x) is int


def matrix(a, rows, cols, binary=False):
    assert isinstance(a, list) and len(a) == rows and all(isinstance(r, list) and len(r) == cols for r in a), 'matrix dimensions differ'
    assert all(integer(x) and (not binary or x in (0, 1)) for row in a for x in row), 'invalid matrix coefficient'


def vector(v, width, binary=False):
    matrix([v], 1, width, binary)


def rowmul(v, a, width=None):
    if width is None:
        width = len(a[0]) if a else 0
    assert len(v) == len(a)
    return [sum(v[i]*a[i][j] for i in range(len(v))) for j in range(width)]


def rank2(rows):
    pivots = {}
    for row in rows:
        value = sum((x % 2) << i for i, x in enumerate(row))
        while value:
            pivot = value.bit_length()-1
            if pivot in pivots:
                value ^= pivots[pivot]
            else:
                pivots[pivot] = value
                break
    return len(pivots)


def in_span(rows, target):
    return rank2(rows+[target]) == rank2(rows)


def rational(pair):
    assert isinstance(pair, list) and len(pair) == 2 and all(map(integer, pair)) and pair[1] > 0, 'bad rational encoding'
    return Fraction(*pair)


def rational_matrix(a):
    return [[rational(v) for v in row] for row in a]


def transpose(a):
    return [list(row) for row in zip(*a)]


def det3(a):
    return sum(a[0][i]*(a[1][(i+1)%3]*a[2][(i+2)%3]-a[1][(i+2)%3]*a[2][(i+1)%3]) for i in range(3))


def inverse(a):
    n = len(a)
    work = [[Fraction(x) for x in row]+[Fraction(i == j) for j in range(n)] for i, row in enumerate(a)]
    for j in range(n):
        p = next((i for i in range(j, n) if work[i][j]), None)
        assert p is not None, 'singular rational change of basis'
        work[j], work[p] = work[p], work[j]
        value = work[j][j]
        work[j] = [x/value for x in work[j]]
        for i in range(n):
            if i != j:
                scale = work[i][j]
                work[i] = [x-scale*y for x, y in zip(work[i], work[j])]
    return [row[n:] for row in work]


def clifford_table(norms):
    table = {}
    for a in range(8):
        for b in range(8):
            swaps = sum(((a >> i) & 1)*((b >> j) & 1) for i in range(3) for j in range(i))
            coeff = Fraction((-1)**swaps)
            for i in range(3):
                if (a & b) >> i & 1:
                    coeff *= -norms[i]
            table[a, b] = (a ^ b, coeff)
    return table


def clifford(a, b, table):
    result = [Fraction(0)]*8
    for i, x in enumerate(a):
        if x:
            for j, y in enumerate(b):
                if y:
                    mask, coefficient = table[i, j]
                    result[mask] += x*y*coefficient
    return result


def check_pin(background):
    b = background
    assert b['characteristicClass'] == 'w2(V)+w1(V)^2'
    assert b['construction'] == 'exact-rational-spin-lift-of-det-times-point-representation'
    assert b['normalizedCocycleChecked'] is True
    n, identity = b['pointOrder'], b['identityIndex']-1
    assert integer(n) and 1 <= n <= 48 and 0 <= identity < n
    mul, omega, signs = b['multiplication'], b['omegaTable'], b['signTable']
    matrix(mul, n, n); matrix(omega, n, n, True); vector(signs, n, True)
    assert all(1 <= x <= n for row in mul for x in row)
    elements = [rational_matrix(x) for x in b['pointElements']]
    assert len(elements) == n and all(len(x) == 3 and all(len(r) == 3 for r in x) for x in elements)
    assert len({tuple(v for row in x for v in row) for x in elements}) == n
    eye = [[Fraction(i == j) for j in range(3)] for i in range(3)]
    assert elements[identity] == eye
    metric, basis = rational_matrix(b['metric']), rational_matrix(b['orthogonalBasis'])
    assert len(metric) == len(basis) == 3 and all(len(r) == 3 for r in metric+basis)
    assert transpose(metric) == metric and metric[0][0] > 0
    assert metric[0][0]*metric[1][1]-metric[0][1]**2 > 0 and det3(metric) > 0
    norms = [rational(x) for x in b['metricDiagonal']]
    assert len(norms) == 3 and all(x > 0 for x in norms)
    diagonal = [[norms[i] if i == j else 0 for j in range(3)] for i in range(3)]
    assert product(product(transpose(basis), metric), basis) == diagonal
    invbasis, table = inverse(basis), clifford_table(norms)
    lifts = [[rational(x) for x in row] for row in b['rationalSpinLifts']]
    assert len(lifts) == n and all(len(x) == 8 for x in lifts)
    assert lifts[identity] == [1, 0, 0, 0, 0, 0, 0, 0]
    for i, R in enumerate(elements):
        det = det3(R)
        assert det in (-1, 1) and signs[i] == (1-det)/2
        assert product(product(transpose(R), metric), R) == metric
        q = lifts[i]
        assert any(q) and all(q[k] == 0 for k in (1, 2, 4, 7))
        rev = [(-x if k in (3, 5, 6) else x) for k, x in enumerate(q)]
        norm = clifford(rev, q, table)
        assert norm[0] > 0 and not any(norm[1:])
        oriented = product(product(invbasis, [[det*x for x in row] for row in R]), basis)
        for j in range(3):
            e, image = [0]*8, [0]*8
            e[1 << j] = 1
            for k in range(3):
                image[1 << k] = oriented[k][j]
            assert clifford(q, e, table) == clifford(image, q, table), 'spin lift does not cover det(R)R'
        assert omega[identity][i] == omega[i][identity] == 0
        for j in range(n):
            k = mul[i][j]-1
            assert product(R, elements[j]) == elements[k], 'point multiplication differs from matrices'
            assert (signs[i]+signs[j]) % 2 == signs[k]
            value = clifford(q, lifts[j], table)
            pivot = next(t for t, x in enumerate(lifts[k]) if x)
            scale = value[pivot]/lifts[k][pivot]
            assert scale and value == [scale*x for x in lifts[k]]
            assert omega[i][j] == int(scale < 0), 'Pin cocycle differs from rational spin product'
            for l in range(n):
                assert (omega[j][l]+omega[k][l]+omega[i][mul[j][l]-1]+omega[i][j]) % 2 == 0, 'Pin cocycle fails'
    return not any(signs)


def check_native_background(d, allow_legacy):
    b, dims = d['crystalline_background'], d['resolution_dimensions']
    w, co = b['nativeOriginalOmega2'], b['affineCohomologyCoordinates']
    vector(w, dims[2], True); vector(co, len(co), True)
    reduced = b['gaugeReducedToZero']
    assert type(reduced) is bool and reduced == (not any(co)), 'background gauge choice disagrees with native class'
    fields = ('nativeDifferential1F2', 'nativeDifferential2F2', 'nativeH2Generators')
    if not all(k in b for k in fields):
        assert allow_legacy, 'missing native D1/D2/H2 certificate (legacy export)'
        if reduced:
            vector(b['trivializingNative1'], dims[1], True)
        return ['legacy export lacks independent native background matrix replay']
    D1, D2, H = [b[k] for k in fields]
    matrix(D1, dims[1], dims[2], True); matrix(D2, dims[2], dims[3], True); matrix(H, len(co), dims[2], True)
    assert all(not any(x % 2 for x in rowmul(row, D2)) for row in D1+H+[w]), 'native background is not closed'
    r1 = rank2(D1)
    assert r1+len(H) == dims[2]-rank2(D2) and rank2(D1+H) == r1+len(H), 'native H2 basis is incomplete or dependent'
    residual = [(x-y) % 2 for x, y in zip(w, rowmul(co, H, dims[2]))]
    assert in_span(D1, residual), 'native omega and reported H2 coordinates disagree'
    if reduced:
        gauge = b['trivializingNative1']; vector(gauge, dims[1], True)
        assert [x % 2 for x in rowmul(gauge, D1)] == w, 'native gauge coboundary differs from original omega'
        assert b['trivializationRecipe']
    return []


def smith_invariants(diag, width):
    rank = sum(x != 0 for x in diag)
    assert all(diag[i] != 0 for i in range(rank)) and all(x == 0 for x in diag[rank:])
    return [0]*(width-rank)+[abs(x) for x in diag if abs(x) > 1]


def check_smith_record(R, S, width):
    matrix(R, len(R), width)
    matrix(S['U'], len(R), len(R)); matrix(S['V'], width, width)
    vector(S['diag'], len(S['diag']))
    check_smith(R, S['U'], S['V'], S['diag'])
    assert S['rank'] == sum(x != 0 for x in S['diag'])
    if 'D' in S:
        assert S['D'] == product(product(S['U'], R), S['V'])
    for name, forward in [('Ui', 'U'), ('Vi', 'V')]:
        if name in S:
            n = len(S[forward]); matrix(S[name], n, n)
            assert product(S[name], S[forward]) == [[int(i == j) for j in range(n)] for i in range(n)]
    return smith_invariants(S['diag'], width)


def check_lift(lift, dims, integer_layer=False):
    for name, degree in [('majorana2', 2), ('fermion3', 3)]:
        vector(lift[name], dims[degree], True)
    assert len(lift['phase4']) == dims[4]
    for value in lift['phase4']:
        q = rational(value)
        assert 0 <= q < 1, 'phase coordinate not reduced modulo one'
    if integer_layer:
        vector(lift['integer1'], dims[1])


def phase_vector(values, width, reduced=False):
    assert isinstance(values, list) and len(values) == width, 'native phase vector dimensions differ'
    result = [rational(x) for x in values]
    assert values == [[x.numerator, x.denominator] for x in result], 'native phase fraction is not canonical'
    if reduced:
        assert all(0 <= x < 1 for x in result), 'phase coordinate not reduced modulo one'
    return result


def check_lower_witnesses(low, dims):
    gens, rows, witnesses = low['generators'], low['presentation'], low['witnesses']
    assert len(witnesses) == len(rows), 'a lower presentation relation lacks its witness'
    boson_indices = [i for i, g in enumerate(gens) if g['layer'] == 0]
    by_name = {g['name']: i for i, g in enumerate(gens)}
    for row, w in zip(rows, witnesses):
        level = w['certificateLevel']
        if level == 'final-bosonic-quotient':
            i = by_name[w['generator']]; g = gens[i]
            assert g['layer'] == 0 and w['order'] == g['quotientOrder']
            assert row == [w['order'] if j == i else 0 for j in range(len(gens))]
        elif level == 'native-Gu-Wen-doubling-class':
            i = by_name[w['generator']]; g = gens[i]
            assert g['layer'] == 1 and w['order'] == g['quotientOrder'] == 2
            assert w['fullBarPhaseWitness'] is False
            assert w['nativeCF3Seed'] == g['nativeCF3Seed'] and w['nativePhase4Primitive'] == g['nativePhase4Seed']
            primitive = phase_vector(w['nativePhase4Primitive'], dims[4])
            phase_vector(w['nativeObstruction5'], dims[5])
            vector(w['primitiveIntegerResidual'], dims[5])
            vector(w['nativeSq1'], dims[4], True)
            doubled = phase_vector(w['nativeDoublePhase4'], dims[4], reduced=True)
            assert doubled == [(2*x+Fraction(y, 2)) % 1 for x, y in zip(primitive, w['nativeSq1'])], 'native CF doubled phase differs from its saved primitive and Sq1'
            co = w['finalBosonicCoordinates']; vector(co, len(boson_indices))
            vector(w['bosonicCohomologyCoordinates'], len(w['bosonicCohomologyCoordinates']))
            expected = [0]*len(gens); expected[i] = 2
            for j, coefficient in zip(boson_indices, co):
                expected[j] = -coefficient
            assert row == expected, 'native CF presentation relation differs from its saved lower carry'
        elif level == 'comparison-homotopy':
            assert type(w['checkedComparisonSupport']) is bool
            vector(w['cfGauge2'], dims[2], True)
            phase_vector(w['phaseGauge3'], dims[3], reduced=True)
            check_lift(w['canonical'], dims); check_lift(w['boundary'], dims)
            for name in ('cfIncomingCoordinates', 'bosonicIncomingCoordinates'):
                vector(w[name], len(w[name]))
        elif level == 'actual-H0-pip-boundary-relation':
            assert w['coordinateRow'] == row
        else:
            raise AssertionError('unknown lower relation witness: '+str(level))


def check_lower(low, dims):
    assert low['status'] == 'computed' and low['enumeratedPhaseProducts'] == 0
    generators = low['generators']; width = len(generators)
    names = [g['name'] for g in generators]
    assert len(set(names)) == width and all(isinstance(n, str) and n for n in names)
    assert all(g['layer'] in (0, 1, 2) for g in generators)
    for g in generators:
        if 'lift' in g:
            check_lift(g['lift'], dims)
        else:
            assert 'nativePhase4Seed' in g, 'marked generator lacks both an actual lift and a native phase seed'
            seed = g['nativePhase4Seed']
            assert isinstance(seed, list) and len(seed) == dims[4], 'native phase seed dimensions differ'
            for value in seed:
                q = rational(value)
                # This is an unreduced primitive seed, not a U(1) phase value.
                # Integer and negative seeds are valid, but the exact encoding
                # must be the canonical fraction emitted by GAP.
                assert value == [q.numerator, q.denominator], 'native phase seed fraction is not canonical'
            if g['layer'] == 1:
                assert g.get('construction') == 'native-Gu-Wen-primitive-class', 'missing native CF lift construction'
                assert 'nativeCF3Seed' in g, 'missing native CF seed'
                vector(g['nativeCF3Seed'], dims[3], True)
            else:
                assert g['layer'] == 0 and g.get('construction') == 'bosonic-cohomology-quotient', 'missing native bosonic lift construction'
                assert 'nativeCF3Seed' not in g, 'bosonic recipe contains an unexpected CF seed'
    matrix(low['presentation'], len(low['presentation']), width)
    matrix(low['smithRowTransform'], len(low['presentation']), len(low['presentation']))
    matrix(low['smithColumnTransform'], width, width); vector(low['smithDiagonal'], len(low['smithDiagonal']))
    check_smith(low['presentation'], low['smithRowTransform'], low['smithColumnTransform'], low['smithDiagonal'])
    inv = smith_invariants(low['smithDiagonal'], width)
    assert low['invariants'] == inv, 'lower invariants differ from exact presentation'
    check_lower_witnesses(low, dims)
    return inv


def check_filtered(R, generators, records, graded):
    layers, width = [g['layer'] for g in generators], len(generators)
    assert len(records) == 3
    for level, record in enumerate(records):
        assert record['layer'] == level
        indices = [i for i in range(width) if layers[i] == level]
        prefix = [i for i in range(width) if layers[i] <= level]
        upper = [i for i in range(width) if layers[i] > level]
        for key, expected in [('generatorIndices', indices), ('prefixIndices', prefix), ('upperIndices', upper)]:
            assert record[key] == [i+1 for i in expected]
        tail = [[row[i] for i in upper] for row in R]
        assert record['highColumnMatrix'] == tail
        S = record['highColumnSmith']; check_smith_record(tail, S, len(upper))
        kernel = S['U'][S['rank']:]
        assert record['relationCombinationRows'] == kernel, 'relation-intersection kernel is not the saturated Smith kernel'
        intersection = product(kernel, R)
        assert record['intersectionRelationRows'] == intersection
        assert all(all(row[i] == 0 for i in upper) for row in intersection)
        for label, columns in [('graded', indices), ('subgroup', prefix)]:
            projection = [[row[i] for i in columns] for row in intersection]
            assert record[label+'Presentation'] == projection
            inv = check_smith_record(projection, record[label+'Smith'], len(columns))
            assert record[label+'Invariants'] == inv
        assert record['gradedInvariants'] == graded[('bosonic', 'complex_fermion', 'majorana')[level]]


def check_h0(d, low, allow_legacy=False):
    s = d['stacking']; wrapped = s['h0IncomingQuotient']; q = wrapped['backgroundQuotient']
    old = q['preQuotientLower']; check_lower(old, d['resolution_dimensions'])
    assert wrapped['lower'] == low and s['lowerBeforeH0Incoming'] == old
    assert low['generators'] == old['generators']
    x = q['incomingCoordinates']; vector(x, len(old['generators']))
    assert low['presentation'] == old['presentation']+[x], 'H0 quotient did not append its actual marked coordinate'
    sx = rowmul(x, old['smithColumnTransform'])
    assert sx == q['incomingSmithCoordinates']
    diag = old['smithDiagonal']; rank = sum(v != 0 for v in diag)
    order = 1
    for i, value in enumerate(sx):
        if i >= rank:
            if value:
                order = 0; break
        else:
            factor = abs(diag[i])//math.gcd(abs(diag[i]), value)
            order = order*factor//math.gcd(order, factor)
    assert order == q['incomingOrder'] and order > 0 and 16 % order == 0
    assert q['certificate'].get('orderDivides') == 16 or (allow_legacy and 'orderDivides' not in q['certificate']), 'missing H0 order bound certificate'
    assert d['h0PipIncoming'] == {'coordinates': x, 'order': order}
    assert order_signature(old['invariants'])[0] == order_signature(low['invariants'])[0]
    assert math.prod(v for v in old['invariants'] if v) == order*math.prod(v for v in low['invariants'] if v)
    assert low['backgroundMarkedGeneratorsMayBeRedundant'] is True
    assert low['witnesses'][:-1] == old['witnesses']
    witness = low['witnesses'][-1]
    assert witness['certificateLevel'] == 'actual-H0-pip-boundary-relation'
    assert witness['coordinateRow'] == x and witness['incomingOrder'] == order and witness['certificate'] == q['certificate']
    for name in ('majorana', 'complex_fermion', 'bosonic'):
        assert q['graded'][name] == d[name]
    check_filtered(low['presentation'], low['generators'], q['filtration'], q['graded'])
    assert order_signature(sum((d['preH0IncomingGraded'][k] for k in ('majorana', 'complex_fermion', 'bosonic')), [])) == order_signature(old['invariants'])
    state = q['incomingState']; check_lift(state, d['resolution_dimensions'])
    assert state['majorana2'] == d['crystalline_background']['nativeOriginalOmega2']
    basis = q.get('basisChange', {}); mc = [g for g in old['generators'] if g['layer'] == 2]
    if basis:
        T = basis['newMCCohomologyRowsInOldBasis']; matrix(T, len(mc), len(mc), True)
        assert rank2(T) == len(mc)
        assert basis['newMCNames'] == [g['name'] for g in mc]
        co = basis['incomingMCClassCoordinates']; vector(co, len(mc), True)
        assert basis['incomingMCCohomologyCoordinates'] == d['crystalline_background']['affineCohomologyCoordinates']
        if 'replacedMCPivot' in basis:
            pivot = basis['replacedMCPivot']-1
            assert 0 <= pivot < len(mc) and co[pivot] == 1
            assert T[pivot] == co and all(T[i] == [int(i == j) for j in range(len(mc))] for i in range(len(mc)) if i != pivot)
            expected = [int(g['name'] == mc[pivot]['name']) for g in old['generators']]
            assert x == expected and q['coordinateMethod'] == 'incoming-state-is-literally-a-marked-generator'
            assert all(mc[pivot]['lift'][k] == state[k] for k in ('majorana2', 'fermion3', 'phase4'))
    return {'incoming_order': order, 'filtered_layers_recomputed': 3}


def canonical_orders(orders):
    free, primes = orders.count(0), {}
    for original in orders:
        v, p = original, 2
        while v > 1 and p*p <= v:
            power = 1
            while v % p == 0:
                v //= p; power *= p
            if power > 1:
                primes.setdefault(p, []).append(power)
            p += 1
        if v > 1:
            primes.setdefault(v, []).append(v)
    width = max((len(v) for v in primes.values()), default=0)
    result = [1]*width
    for values in primes.values():
        padded = [1]*(width-len(values))+sorted(values)
        result = [a*b for a, b in zip(result, padded)]
    return [0]*free+result


def v2(n):
    count = 0
    while n and n % 2 == 0:
        count += 1; n //= 2
    return count


def extension_options(low, leading, ambiguous):
    diag, V = low['smithDiagonal'], low['smithColumnTransform']
    width, rank = len(V), sum(x != 0 for x in diag)
    active = [i for i in range(width) if i >= rank or diag[i] % 2 == 0]
    weights = [-1 if i >= rank else v2(abs(diag[i])) for i in active]
    transformed = rowmul(leading, V)
    z = [transformed[i] % 2 for i in active]
    W = [[V[i][j] % 2 for j in active] for i in ambiguous]
    heights = [0] if in_span(W, z) else []
    for h in sorted(set(weights)-{-1}):
        high = [i for i, w in enumerate(weights) if w == -1 or w > h]
        together = high+[i for i, w in enumerate(weights) if w == h]
        sub = lambda columns: [[row[i] for i in columns] for row in W]
        target = lambda columns: [z[i] for i in columns]
        if in_span(sub(high), target(high)):
            if rank2(sub(together)) > rank2(sub(high)) or not in_span(sub(together), target(together)):
                heights.append(h)
    free = [i for i, w in enumerate(weights) if w == -1]
    if any(z[i] for i in free) or any(row[i] for row in W for i in free):
        heights.append(-1)
    assert heights
    results, options = [], []
    for h in heights:
        orders = list(low['invariants'])
        if h == 0:
            orders.append(2)
        elif h > 0:
            i = next(i for i, order in enumerate(orders) if order and v2(order) == h)
            orders[i] *= 2
        inv = canonical_orders(orders)
        results.append({'height': h, 'invariants': inv})
        if inv not in options:
            options.append(inv)
    return {'modTwoCyclicColumns': [i+1 for i in active], 'modTwoWeights': weights,
            'modTwoRelation': z, 'modTwoAmbiguityRows': W, 'possibleHeights': heights,
            'heightResults': results, 'invariantOptions': options}


def check_extension(d, low):
    s = d['stacking']; f = s['pipExtensionCertificate']; square = s['pipSquareCertificate']
    assert f['method'] == 'abelian-Ext1-height-stratification' and f['enumeratedExtensionClasses'] == 0
    assert s['fullUpperPhaseWitness'] is False and square['fullUpperPhaseWitness'] is False
    assert square['unknownCarries'] == ['complex-fermion', 'bosonic']
    assert square['majoranaCohomologyClass'] == d['crystalline_background']['affineCohomologyCoordinates']
    mc = [i for i, g in enumerate(low['generators']) if g['layer'] == 2]
    coordinates = square['majoranaCoordinates']; vector(coordinates, len(mc), True)
    leading = [0]*len(low['generators'])
    for i, coefficient in zip(mc, coordinates):
        leading[i] = coefficient
    assert leading == f['inputRelationModuloAmbiguity']
    b = d['crystalline_background']
    if 'nativeDifferential1F2' in b:
        represented = rowmul(coordinates, [low['generators'][i]['lift']['majorana2'] for i in mc], len(b['nativeOriginalOmega2']))
        assert in_span(b['nativeDifferential1F2'], [(a-c) % 2 for a, c in zip(represented, b['nativeOriginalOmega2'])]), 'leading square is not the native omega class'
    ambiguous = [i for i, g in enumerate(low['generators']) if g['layer'] < 2]
    assert f['ambiguousGeneratorIndices'] == [i+1 for i in ambiguous]
    expected = extension_options(low, leading, ambiguous)
    for key, value in expected.items():
        assert f[key] == value, 'Ext-family certificate differs: '+key
    unique = len(expected['invariantOptions']) == 1
    assert f['status'] == ('computed' if unique else 'ambiguous')
    assert s['status'] == ('computed' if unique else 'unresolved')
    if unique:
        assert f['invariants'] == expected['invariantOptions'][0]
        assert s['invariants'] == [0]*d['pip']['free_rank']+f['invariants']
    else:
        assert 'invariants' not in s and 'invariants' not in f, 'ambiguous Ext family presented as a selected group'
    assert 'pipGenerator' not in s and 'pipRelation' not in s, 'unknown upper carry presented as an actual marked relation'
    return 'abstract-upper-family-single-group' if unique else 'unresolved-upper-extension-family'


def check_candidate(candidate, width, bound):
    coordinates = candidate.get('h1Coordinates')
    if coordinates is not None:
        vector(coordinates, width)
    page, status = candidate['page'], candidate['status']
    assert page in (2, 3, 4) and status in ('survives', 'killed')
    if status == 'killed':
        obstruction = candidate['obstruction']; vector(obstruction, len(obstruction))
        assert any(obstruction)
        if page in (2, 3):
            assert all(x in (0, 1) for x in obstruction)
        else:
            orders = candidate['d4_target']; assert len(orders) == len(obstruction)
            assert all((x == 0 if order == 0 else 0 <= x < order and bound*x % order == 0) for order, x in zip(orders, obstruction))
    else:
        assert page == 4
        target = candidate['d4_target']; order_signature(target)
        if candidate['certificate'] == 'd2-and-d3-primitives-zero-two-primary-d4-target':
            assert all(order > 0 and order % 2 == 1 for order in target)
        else:
            assert candidate['certificate'] == 'explicit-full-O5-in-E4-quotient'
            assert len(candidate['d4_projected_coordinates']) == len(target) and not any(candidate['d4_projected_coordinates'])
    return page


def check_free(d, zero_background):
    rank = d['pip']['free_rank']
    if rank == 0:
        return None
    f = d['pip']['free_lattice']; dims = d['resolution_dimensions']
    assert f['status'] == 'computed' and f['rank'] == rank and f['fullFreePhaseWitness'] is True
    orders, basis = f['h1BasisOrders'], f['h1BasisNative1']
    order_signature(orders); matrix(basis, len(orders), dims[1])
    indices = [i for i, order in enumerate(orders) if order == 0]
    assert f['freeIndices'] == [i+1 for i in indices] and len(indices) == rank
    lattice = f['latticeBasis']; matrix(lattice, rank, rank)
    assert abs(determinant(lattice)) == f['latticeIndex'] > 0
    assert len(f['generators']) == rank
    for i, g in enumerate(f['generators']):
        check_lift(g, dims, True)
        assert g['name'] == 'Pfree%d' % (i+1)
        coordinates = g['h1Coordinates']; vector(coordinates, len(orders))
        assert [coordinates[j] for j in indices] == lattice[i]
        assert g['integer1'] == rowmul(coordinates, basis, dims[1]), 'free generator integer cochain differs from its named H1 basis'
    period = 2 if zero_background else 16
    for candidate in f['parityCandidates']:
        check_candidate(candidate, len(orders), period)
    if zero_background:
        return {'period': 2, 'index': f['latticeIndex'], 'scope': 'existing complete omega-zero lattice certificate'}
    assert rank == 1 and f['certifiedIntegerPeriod'] == 16
    assert f['certificate'] == 'strict-16H-survival-and-complete-rank-one-power-of-two-index-search'
    index = f['latticeIndex']; assert index in (1, 2, 4, 8, 16) and lattice == [[index]]
    assert f['survivingParityBasis'] == []
    torsion = [i for i, order in enumerate(orders) if order]
    assert all(orders[i] == 2 for i in torsion)
    expected_candidates = []
    for k in (1, 2, 4, 8):
        if k > index:
            break
        for mask in range(1 << len(torsion)):
            coords = [0]*len(orders); coords[indices[0]] = k
            for i, t in enumerate(torsion):
                coords[t] = mask >> i & 1
            expected_candidates.append(coords)
            if k == index and coords == f['generators'][0]['h1Coordinates']:
                break
    candidates = f['parityCandidates']
    if index == 16:
        assert [c['h1Coordinates'] for c in candidates] == expected_candidates
        assert all(c['status'] == 'killed' for c in candidates)
        g = f['generators'][0]
        assert g['h1Coordinates'] == [16 if i == indices[0] else 0 for i in range(len(orders))]
        assert not any(g['majorana2']+g['fermion3']) and all(rational(x) == 0 for x in g['phase4'])
        assert g['construction'] == 'strict-universal-16H-zero-lower-tower-from-twice-shift-eight'
    else:
        assert [c['h1Coordinates'] for c in candidates] == expected_candidates
        assert candidates and candidates[-1]['status'] == 'survives' and all(c['status'] == 'killed' for c in candidates[:-1])
        assert candidates[-1]['h1Coordinates'] == f['generators'][0]['h1Coordinates']
    return {'period': 16, 'index': index, 'tested_candidates': len(candidates)}


def check_result(d, allow_legacy=False):
    assert d['convention'] == CONVENTION and d['crystalline_spin'] == 'spinless'
    assert d['sptset_loaded'] is False and d['formula_convention'] == FORMULA
    assert d.get('classification_status', d['status']) == 'computed'
    assert d['pip']['status'] == 'computed'
    for orders in [d['pip']['orders'], d['majorana'], d['complex_fermion'], d['bosonic']]:
        assert isinstance(orders, list) and all(integer(x) and (x == 0 or x > 1) for x in orders)
    dims = d['resolution_dimensions']; assert len(dims) >= 6 and all(integer(x) and x >= 0 for x in dims)
    hashes = d['source_sha256']; assert all(re.fullmatch('[0-9a-f]{64}', x) for x in hashes.values())
    assert hashlib.sha256(json.dumps(hashes, sort_keys=True).encode()).hexdigest() == d['source_id']
    unitary = check_pin(d['crystalline_background'])
    missing = check_native_background(d, allow_legacy)
    zero_background = d['crystalline_background']['gaugeReducedToZero']
    rank = d['pip']['free_rank']; assert integer(rank) and rank >= 0
    assert rank == d['pip']['orders'].count(0) and all(x in (0, 2) for x in d['pip']['orders'])
    survivors = sum(c['status'] == 'survives' for c in d['pip']['torsion'])
    assert survivors == d['pip']['orders'].count(2)
    for candidate in d['pip']['torsion']:
        check_candidate(candidate, 0, 2)
    free = check_free(d, zero_background)
    if free and not zero_background:
        assert free['index'] <= 8, 'physical Pin-minus 8H survival excludes a primitive free lattice index 16'
        free['physical_eight_survival_consistent'] = True
    details = {'background_gauge': 'zero' if zero_background else 'nonzero', 'unitary': unitary,
               'missing_evidence': missing, 'free_lattice': free}
    if 'stacking' not in d:
        return dict(details, kind='classification-only', full_group=False, marked_witnesses=False)
    s = d['stacking']
    assert d['status'] == s['status'], 'outer and stacking computation status disagree'
    if zero_background:
        check_lower(s['lower'], dims)
        converted = copy.deepcopy(d); converted['convention'] = 'physical-spin-half-det-sign-omega0'
        kind = check_zero_result(converted)
        check_zero_witnesses(converted, FORMULA)
        return dict(details, kind='gauge-zero-complete-marked-stacking', full_group=True, marked_witnesses=True)
    low = s.get('lower')
    if low is None:
        assert 'h0IncomingQuotient' in s, 'missing lower presentation'
        low = s['h0IncomingQuotient']['lower']
        details['compatibility_note'] = 'v1 outer lower omitted; exact nested H0 quotient lower audited'
    check_lower(low, dims)
    assert s['freePipRank'] == rank
    if unitary:
        assert 'h0IncomingQuotient' in s
        details['h0_quotient'] = check_h0(d, low, allow_legacy)
    else:
        assert 'h0IncomingQuotient' not in s and 'h0PipIncoming' not in d
    lower_layers = d['majorana']+d['complex_fermion']+d['bosonic']
    assert order_signature(low['invariants']) == order_signature(lower_layers)
    if 2 in d['pip']['orders']:
        kind = check_extension(d, low)
        if s['status'] == 'computed':
            assert order_signature(s['invariants']) == order_signature(d['pip']['orders']+lower_layers)
        return dict(details, kind=kind, full_group=(s['status'] == 'computed'), marked_witnesses=False)
    assert s['status'] == 'computed'
    assert s['invariants'] == [0]*rank+low['invariants']
    assert s['upperCompletion'] == 'no-torsion-pip-extension-required'
    return dict(details, kind='nonzero-background-complete-lower-stacking', full_group=True, marked_witnesses=True)


def check_background_result(data, strict_background=True):
    """Public archive API. Return explicit scope; reject malformed certificates.

    A verified multi-group Ext family is a valid *unresolved* result, never an
    actual upper marked witness. strict_background=False is reserved for labeled
    legacy exports with missing native background matrices.
    """
    assert type(strict_background) is bool
    return check_result(data, allow_legacy=not strict_background)


def audit(directory, allow_partial=False, allow_legacy=False, require_witnesses=False):
    rows, errors, seen = [], [], set()
    for path in sorted(directory.glob('sg*.json')):
        if '.raw.' in path.name:
            continue
        try:
            match = re.fullmatch(r'sg([1-9][0-9]*)\.json', path.name)
            assert match, 'invalid result filename'
            n = int(match.group(1)); assert 1 <= n <= 230 and n not in seen
            seen.add(n); raw = path.read_bytes(); d = json.loads(raw); assert d['space_group'] == n
            result = check_result(d, allow_legacy)
            if require_witnesses:
                assert result['marked_witnesses'] and not result['missing_evidence'], 'complete actual marked witnesses required'
            rows.append(dict(space_group=n, result_sha256=hashlib.sha256(raw).hexdigest(), source_id=d['source_id'],
                             crystalline_spin=d['crystalline_spin'], physical_convention=d['convention'],
                             formula_convention=d['formula_convention'],
                             effective_sign='w1(V)=determinant-parity',
                             effective_omega=d['crystalline_background']['characteristicClass'],
                             layers={'pip': d['pip']['orders'], **{k: d[k] for k in ('majorana', 'complex_fermion', 'bosonic')}},
                             invariants=d.get('stacking', {}).get('invariants'),
                             invariant_options=([([0]*d['pip']['free_rank'])+option for option in
                                 d['stacking']['pipExtensionCertificate']['invariantOptions']]
                                 if 'pipExtensionCertificate' in d.get('stacking', {}) else None),
                             candidate_pages=[dict(sector=sector, h1_coordinates=c.get('h1Coordinates'),
                                 page=c['page'], status=c['status'], certificate=c.get('certificate'),
                                 obstruction=c.get('obstruction'))
                                 for sector, candidates in [('torsion', d['pip']['torsion']),
                                     ('free', d['pip'].get('free_lattice', {}).get('parityCandidates', []))]
                                 for c in candidates], **result))
        except (AssertionError, KeyError, ValueError, TypeError, IndexError, ZeroDivisionError, StopIteration) as exc:
            errors.append({'file': path.name, 'reason': str(exc) or type(exc).__name__})
    missing = sorted(set(range(1, 231))-seen)
    report = {'schema': 'fspt-spinless-background-audit-v1', 'scope': __doc__, 'directory': str(directory),
              'groups_present': len(seen), 'groups_passed': len(rows), 'missing': missing, 'errors': errors,
              'kinds': dict(Counter(r['kind'] for r in rows)), 'rows': sorted(rows, key=lambda r: r['space_group']),
              'source_ids': sorted(set(r['source_id'] for r in rows)), 'external_answers_consulted': False,
              'all_230_classifications_present_and_valid': not missing and not errors,
              'all_230_full_groups_determined': not missing and not errors and all(r['full_group'] for r in rows),
              'all_230_marked_witnesses_complete': not missing and not errors and all(r['marked_witnesses'] and not r['missing_evidence'] for r in rows),
              'all_230_certificates_strictly_valid': not missing and not errors and all(not r['missing_evidence'] for r in rows),
              'auditor_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
              'mathematical_scope_limit': 'Saved native nonlinear lifts and candidate page obstructions retain their source/homotopy recipes. This algebraic audit does not rebuild bar cochains or independently rederive the physical leading-square operation.',
              'allow_legacy_evidence': allow_legacy, 'complete_marked_witnesses_required': require_witnesses}
    failed = bool(errors or (missing and not allow_partial))
    return report, failed


def write_report(report, directory):
    """Write a new portable table, retaining ambiguous options and missing rows."""
    if directory.exists() or directory.is_symlink():
        raise ValueError('report directory exists; preserve previous evidence')
    directory.mkdir(parents=True)
    (directory/'audit.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    fields = ['space_group', 'crystalline_spin', 'physical_convention', 'effective_sign', 'effective_omega',
              'background_gauge', 'formula_convention', 'pip', 'majorana', 'complex_fermion', 'bosonic',
              'full_invariants', 'invariant_options', 'audit_kind', 'free_lattice_index',
              'h0_incoming_order', 'actual_marked_witnesses', 'missing_evidence', 'result_sha256', 'source_id']
    indexed = {r['space_group']: r for r in report['rows']}
    candidates = []
    lines = ['# Spinless space-group certificate report', '',
             'Physical crystalline convention: spinless, with crystalline sign and extension both zero. '
             'Equivalent internal convention on the full infinite affine group: s=w1(V), omega=w2(V)+w1(V)^2 (Pin-minus). '
             'The separate spin-half crystalline calculation has effective omega=0 and is not merged into this table.', '',
             '**An abstract extension group is not an actual upper generator relation.** Unresolved families retain every certified possible group.', '',
             'Results present: %d; certificate checks passed: %d; errors: %d.' % (report['groups_present'], report['groups_passed'], len(report['errors'])),
             'All 230 full groups determined: `%s`; all 230 actual marked witnesses complete: `%s`.' % (report['all_230_full_groups_determined'], report['all_230_marked_witnesses_complete']), '',
             report['mathematical_scope_limit'], '',
             'Cyclic factors are JSON arrays: `0` denotes Z; an empty array is the trivial group. An absent result is explicitly missing.', '',
             'Source snapshots: '+', '.join('`'+s+'`' for s in report['source_ids'])+'. '
             'Every result hash, physical/gauge label and source hash is retained in [space_groups.csv](space_groups.csv); '
             'the exact auditor hash and per-row scope are in [audit.json](audit.json).', '',
             'A zero background gauge means an actual affine trivializing cochain was certified; it does not change the physical spinless label. '
             'H0 order is shown only when an actual incoming quotient was recorded. Native reconstruction recipes count as retained marked evidence; bar cochains were not reevaluated here.', '',
             '| SG | p+ip | Majorana | CF | Bosonic | Full group / possible groups | Free index | H0 order | Actual marked | Certificate scope |',
             '|---:|---|---|---|---|---|---:|---:|---|---|']
    with (directory/'space_groups.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader()
        for n in range(1, 231):
            row = indexed.get(n)
            if row is None:
                writer.writerow({'space_group': n, 'audit_kind': 'missing-or-rejected'})
                lines.append('| %d | — | — | — | — | — | — | — | — | missing or rejected |' % n)
                continue
            record = {'space_group': n, 'audit_kind': row['kind'],
                      **{key: row[key] for key in ('crystalline_spin', 'physical_convention', 'effective_sign',
                          'effective_omega', 'background_gauge', 'formula_convention')},
                      'full_invariants': json.dumps(row['invariants']) if row['invariants'] is not None else '',
                      'invariant_options': json.dumps(row['invariant_options']) if row['invariant_options'] is not None else '',
                      'free_lattice_index': (row['free_lattice'] or {}).get('index', ''),
                      'h0_incoming_order': row.get('h0_quotient', {}).get('incoming_order', ''),
                      'actual_marked_witnesses': row['marked_witnesses'],
                      'missing_evidence': json.dumps(row['missing_evidence']),
                      'result_sha256': row['result_sha256'], 'source_id': row['source_id']}
            record.update({k: json.dumps(v) for k, v in row['layers'].items()})
            writer.writerow(record)
            expression = record['full_invariants'] or record['invariant_options'] or 'not computed'
            lines.append('| %d | %s | %s | %s | %s | %s | %s | %s | %s | %s |' %
                         (n, record['pip'], record['majorana'], record['complex_fermion'], record['bosonic'], expression,
                          record['free_lattice_index'], record['h0_incoming_order'], record['actual_marked_witnesses'], row['kind']))
            candidates += [dict(space_group=n, **candidate) for candidate in row['candidate_pages']]
    with (directory/'candidate_pages.csv').open('w', newline='') as handle:
        names = ['space_group', 'sector', 'h1_coordinates', 'page', 'status', 'certificate', 'obstruction']
        writer = csv.DictWriter(handle, fieldnames=names); writer.writeheader()
        for row in candidates:
            writer.writerow({k: json.dumps(v) if isinstance(v, (list, dict)) else v for k, v in row.items()})
    (directory/'README.md').write_text('\n'.join(lines)+'\n')


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('run', type=Path)
    p.add_argument('--allow-partial', action='store_true')
    p.add_argument('--allow-legacy-evidence', action='store_true', help='Explicitly label old exports lacking native matrices; never claim complete archived witnesses')
    p.add_argument('--require-complete-witnesses', action='store_true')
    p.add_argument('--output', type=Path, help='Write a new audit JSON; refuses an existing file')
    p.add_argument('--report', type=Path, help='Write a new directory with audit JSON, 230-row CSV/Markdown and candidate pages')
    a = p.parse_args()
    if not __debug__:
        p.error('run without Python -O or PYTHONOPTIMIZE')
    if a.report and (a.report.exists() or a.report.is_symlink()):
        p.error('report directory exists; preserve the previous report')
    if a.output and a.output.exists():
        p.error('output exists; preserve the previous audit')
    report, failed = audit(a.run, a.allow_partial, a.allow_legacy_evidence, a.require_complete_witnesses)
    raw = json.dumps(report, indent=2, sort_keys=True)+'\n'
    if a.output:
        a.output.parent.mkdir(parents=True, exist_ok=True); a.output.write_text(raw)
    if a.report:
        write_report(report, a.report)
    summary = {k: v for k, v in report.items() if k not in ('rows', 'scope')}
    print(json.dumps(summary, indent=2, sort_keys=True))
    return int(failed)


if __name__ == '__main__':
    sys.exit(main())
