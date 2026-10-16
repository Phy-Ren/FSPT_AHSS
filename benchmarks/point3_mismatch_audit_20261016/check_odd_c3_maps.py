#!/usr/bin/env python3
"""Independent finite-table subgroup/background audit; no classification backend."""
from pathlib import Path
from fractions import Fraction
from itertools import combinations, permutations, product
import hashlib
import json
import sympy as sp

ROOT = Path(__file__).resolve().parents[2]
OUT = Path(__file__).with_name('odd_c3_current_witnesses.json')

def closure(table, generators):
    out = {0}
    while True:
        new = out | {table[x][g] for x in out for g in generators}
        if new == out:
            return out
        out = new

def gauge(table, difference):
    """Solve d lambda = difference over F2 by exhaustive normalized cochains."""
    n = len(table)
    for tail in product((0, 1), repeat=n-1):
        bits = (0,) + tail
        if all((bits[a] + bits[b] + bits[table[a][b]]) % 2 == difference[a][b]
               for a in range(n) for b in range(n)):
            return list(bits)
    raise AssertionError('No normalized half-valued extension gauge')

def audit(source_index, target_index, spin):
    files = [ROOT / f'insulator_catalog/generated/point3_{i:02d}_{spin}.json'
             for i in (source_index, target_index)]
    src, dst = [json.loads(p.read_text()) for p in files]
    t, u = src['multiplication'], dst['multiplication']
    n, m = src['order'], dst['order']
    assert n == 3*m and src['identity_index'] == dst['identity_index'] == 0
    inv = [next(j for j in range(n) if t[i][j] == 0) for i in range(n)]
    kernels = {tuple(sorted(closure(t, [x]))) for x in range(n)
               if len(closure(t, [x])) == 3}
    kernels = [set(k) for k in kernels if all(t[t[a][x]][inv[a]] in k
               for a in range(n) for x in k)]
    assert len(kernels) == 1
    kernel = kernels[0]
    complement = next((0,)+xs for xs in combinations(range(1,n),m-1)
        if closure(t,(0,)+xs) == set((0,)+xs)
        and kernel.intersection((0,)+xs) == {0})
    trace = lambda mat: sum(mat[i][i] for i in range(3))
    for mapped_tail in permutations(range(1,m)):
        mapped = (0,)+mapped_tail
        section = [complement[mapped.index(a)] for a in range(m)]
        if not all(t[section[a]][section[b]] == section[u[a][b]]
                   for a in range(m) for b in range(m)):
            continue
        if not all(trace(src['matrices'][section[a]]) == trace(dst['matrices'][a])
                   and all(src[key][section[a]] == dst[key][a]
                           for key in ('s','rho','circle_action')) for a in range(m)):
            continue
        break
    else:
        raise AssertionError('No representation/background preserving complement')
    quotient = [-1]*n
    for a in range(m):
        for k in kernel:
            x = t[k][section[a]]
            assert quotient[x] == -1
            quotient[x] = a
    assert all(quotient[t[a][b]] == u[quotient[a]][quotient[b]]
               for a in range(n) for b in range(n))
    assert all(quotient[section[a]] == a for a in range(m))
    assert all(src[key][a] == dst[key][quotient[a]]
               for key in ('s','rho','circle_action') for a in range(n))
    assert not any(src['circle_action'])
    omega_difference = [[int(2*(Fraction(src['omega'][a][b])-
        Fraction(dst['omega'][quotient[a]][quotient[b]]))) % 2
        for b in range(n)] for a in range(n)]
    omega_gauge = gauge(t, omega_difference)
    pin_difference = [[(src['geometric_pin_minus'][a][b]-
        dst['geometric_pin_minus'][quotient[a]][quotient[b]]) % 2
        for b in range(n)] for a in range(n)]
    pin_gauge = gauge(t, pin_difference)
    # Explicit rational intertwiner certifies actual representation restriction.
    symbols = sp.symbols('x:9')
    X = sp.Matrix(3,3,symbols)
    equations = []
    for a in range(m):
        equations.extend(sp.Matrix(src['matrices'][section[a]])*X-
                         X*sp.Matrix(dst['matrices'][a]))
    matrix, _ = sp.linear_eq_to_matrix(equations,symbols)
    basis = matrix.nullspace()
    for coeff in product((-1,0,1),repeat=len(basis)):
        vector = sum((c*b for c,b in zip(coeff,basis)),sp.zeros(9,1))
        intertwiner = sp.Matrix(3,3,vector)
        if intertwiner.det():
            break
    else:
        raise AssertionError('No nonsingular intertwiner found')
    assert all(sp.Matrix(src['matrices'][section[a]])*intertwiner ==
               intertwiner*sp.Matrix(dst['matrices'][a]) for a in range(m))
    # E8 is included: the orientation cocycle pulls back identically and its
    # signed coboundary vanishes exactly; twice it is d_s(-1).
    e = src['s']
    assert all(e[t[a][b]] == e[a]+(-1)**e[a]*e[b]
               for a in range(n) for b in range(n))
    assert all(2*e[a] == (-1)**e[a]*(-1)-(-1) for a in range(n))
    return {
        'source':src['id'], 'target':dst['id'],
        'source_name':src['name'], 'target_name':dst['name'], 'physical_spin':spin,
        'input_sha256':[hashlib.sha256(p.read_bytes()).hexdigest() for p in files],
        'normal_C3_indices':sorted(kernel), 'complement_indices':list(complement),
        'section_target_to_source':section, 'quotient_source_to_target':quotient,
        'full_quotient_multiplication_checks':n*n,
        'intertwiner_source_X_equals_X_target':[[str(x) for x in row]
                                             for row in intertwiner.tolist()],
        'intertwiner_determinant':str(intertwiner.det()),
        'full_effective_extension_gauge_lambda': [str(Fraction(x,2)) for x in omega_gauge],
        'geometric_pin_minus_coboundary_bits':pin_gauge,
        'gauge_equation':'omega_source - quotient^*omega_target = d(lambda) mod 1',
        'physical_spin_extension_checked': True,
        'E8_orientation_root_pulls_back_exactly':True,
        'E8_root_has_order_two':True,
        'all_checks_pass':True,
    }

def main():
    result = {'method':'Independent Python finite-table exhaustive subgroup/gauge and exact rational intertwiner audit',
              'runtime_classifier_imported':False,
              'rows':[audit(a,b,spin) for a,b in [(17,2),(20,5),(23,5),(26,7)]
                      for spin in ('spinless','spin_half')]}
    OUT.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({'rows':len(result['rows']), 'all_pass':all(r['all_checks_pass'] for r in result['rows']),
                      'output':str(OUT)},indent=2))
    cyclic = []
    for index in (10,17):
        for spin in ('spinless','spin_half'):
            path = ROOT / f'insulator_catalog/generated/point3_{index:02d}_{spin}.json'
            record = json.loads(path.read_text())
            table,n = record['multiplication'],record['order']
            generator = next(a for a in range(n) if len(closure(table,[a])) == n)
            powers = [0]
            for k in range(1,n):
                powers.append(table[powers[-1]][generator])
            omega = [[Fraction(record['omega'][a][b]) for b in powers] for a in powers]
            slope = sum(row[1] for row in omega)/n
            lam = [k*slope-sum(omega[j][1] for j in range(k)) for k in range(n)]
            assert all((lam[a]+lam[b]-lam[(a+b)%n]-omega[a][b]).denominator == 1
                       for a in range(n) for b in range(n))
            assert all(record['s'][powers[a]] == record['rho'][powers[a]] == a%2
                       for a in range(n))
            assert not any(record['circle_action'])
            cyclic.append({'source':record['id'], 'input_sha256':hashlib.sha256(path.read_bytes()).hexdigest(),
               'cyclic_power_to_catalog_index':powers,'standard_s_rho':'parity',
               'omega_gauge_to_zero':[str(x) for x in lam],
               'gauge_equation':'omega(a,b) = lambda(a)+lambda(b)-lambda(a+b) mod 1',
               'pair_checks':n*n, 'all_checks_pass':True})
    Path(__file__).with_name('cyclic_current_backgrounds.json').write_text(json.dumps(cyclic,indent=2)+'\n')

if __name__ == '__main__':
    main()
