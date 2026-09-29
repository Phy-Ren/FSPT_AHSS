#!/usr/bin/env python3
"""Independent normalized-bar detector of the V4 quaternion-extension CF map.

No GAP, HAP, reference classification table, or compiled phase is imported.
The explicit cup-one and Bockstein are evaluated on all seven degree-six
shuffle cycles. A nonzero mod-two Bockstein rules out an exact U(1) phase.
"""
import argparse
from itertools import combinations, product
import json
from pathlib import Path


def chars(g):
    return g & 1, (g >> 1) & 1


def omega(g, h):
    x, y = chars(g)
    u, v = chars(h)
    return (x*u + x*v + y*v) % 2


def h3(args, x_count):
    answer = 1
    for i, g in enumerate(args):
        answer *= chars(g)[0 if i < x_count else 1]
    return answer


def phase_numerator(args, x_count):
    """Twice O5=(Sq2+omega) n3, returned as its canonical binary lift."""
    g = tuple(args)
    answer = omega(g[0], g[1]) * h3(g[2:], x_count)
    # Cup_1 of two degree-three cochains, in normalized bar coordinates.
    for j in range(3):
        merged = g[j] ^ g[j+1] ^ g[j+2]
        left = g[:j] + (merged,) + g[j+3:]
        answer += h3(left, x_count) * h3(g[j:j+3], x_count)
    return answer % 2


def boundary_terms(args):
    args = tuple(args)
    yield 1, args[1:]
    for i in range(len(args)-1):
        yield (-1)**(i+1), args[:i] + (args[i] ^ args[i+1],) + args[i+2:]
    yield (-1)**len(args), args[:-1]


def beta_phase(args, x_count):
    value = sum(sign * phase_numerator(face, x_count)
                for sign, face in boundary_terms(args))
    assert value % 2 == 0, ('nonclosed binary source', args, value)
    return (value//2) % 2


def shuffle_cycle(x_count):
    return [tuple(1 if j in places else 2 for j in range(6))
            for places in combinations(range(6), x_count)]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--output', required=True)
    args = parser.parse_args()
    cycles = []
    for degree_x in range(7):
        terms = shuffle_cycle(degree_x)
        boundary = set()
        for simplex in terms:
            for _, face in boundary_terms(simplex):
                if 0 in face:
                    continue
                if face in boundary:
                    boundary.remove(face)
                else:
                    boundary.add(face)
        assert not boundary
        cycles.append(terms)
    images = []
    for degree_x in [3, 2, 1, 0]:
        # Verify closure on EVERY normalized bar six-simplex, not only cycles.
        for simplex in product([1, 2, 3], repeat=6):
            beta_phase(simplex, degree_x)
        pairings = [sum(beta_phase(simplex, degree_x) for simplex in cycle) % 2
                    for cycle in cycles]
        expected = [0]*7
        if degree_x in [1, 2]:
            expected[2] = expected[4] = 1
        assert pairings == expected, (degree_x, pairings)
        images.append({'n3': ['y^3', 'x*y^2', 'x^2*y', 'x^3'][degree_x],
                       'bockstein_cycle_pairings': pairings})
    result = {
        'model': 'V4_wa2+b2+ab_s0',
        'operation': 'CF incoming d2: one-half (Sq2 + omega2) n3',
        'omega2': 'x^2 + x*y + y^2',
        'input_basis': ['x^3', 'x^2*y', 'x*y^2', 'y^3'],
        'detector_cycles': [{'x_count': i, 'y_count': 6-i,
                            'term_count': len(cycle), 'boundary_mod2': []}
                           for i, cycle in enumerate(cycles)],
        'images': images,
        'rank': 1,
        'nonzero_integral_class_mod2': 'x^4*y^2 + x^2*y^4',
        'normalized_six_simplex_closure_checks': 4*3**6,
        'conclusion': 'The CF primary image removes one of the four initial bosonic C2 factors.',
    }
    Path(args.output).write_text(json.dumps(result, indent=2)+'\n')
    print('AFS_V4_CF_BAR_DETECTOR_PASS rank=1 closure_checks=2916')

if __name__ == '__main__':
    main()
