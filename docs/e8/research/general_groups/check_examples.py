"""Exact review examples for (e_p, n_p, n_{p+2}, nu_{p+3}).

No classifier or production source is modified. H1 uses the pinned supplied
presentation algorithm; the bar-cochain completion calculation is independent.
"""
from dataclasses import asdict
from fractions import Fraction
from itertools import combinations
from math import comb
from pathlib import Path
from random import Random
import hashlib
import importlib.util
import json
import sys

ROOT = Path(__file__).resolve().parent
SUPPLIED = Path('/home/xingyu/AllFSPT_reviews/e8_v09_da3ad936/E8_AHSS_v0_9/src/twisted_h1.py')
spec = importlib.util.spec_from_file_location('review_twisted_h1', SUPPLIED)
module = importlib.util.module_from_spec(spec)
sys.modules[spec.name] = module
spec.loader.exec_module(module)


def comm(i, j):
    return [i, j, -i, -j]


def translations(r):
    return [comm(i, j) for i, j in combinations(range(1, r + 1), 2)]


def diagonal_real_ranks(diagonal, sign):
    r = len(diagonal)
    out = []
    for k in range(7):
        count = 0
        for subset in combinations(range(r), k):
            eigenvalue = sign
            for i in subset:
                eigenvalue *= diagonal[i]
            count += eigenvalue == 1
        out.append(count)
    return out


records = []


def add_case(name, generators, signs, relators, expected, rank, diagonal=None, holonomy_sign=1):
    result = module.twisted_h1(signs, relators)
    assert (result.free_rank, result.torsion) == expected, (name, result)
    real = ([comb(rank, k) if k <= rank else 0 for k in range(7)]
            if diagonal is None else diagonal_real_ranks(diagonal, holonomy_sign))
    assert result.free_rank == real[1]
    assert real[5] == real[6] == 0
    records.append({'name': name, 'generators': generators, 'signs': signs,
                    'relators': relators, 'unitary_translation_rank': rank,
                    'real_cohomology_ranks_0_to_6': real, **asdict(result)})
    return result


add_case('P1: Z^3', ['tx', 'ty', 'tz'], [1] * 3, translations(3), (3, ()), 3)
for name, square in [('Pm: mirror', [4, 4]), ('Pc: glide', [4, 4, -2])]:
    add_case(name, ['tx', 'ty', 'tz', 'm_or_g'], [1, 1, 1, -1],
             translations(3) + [square, [4, 1, -4, 1], [4, 2, -4, -2], [4, 3, -4, -3]],
             (1, (2,)), 3, [-1, 1, 1], -1)
add_case('Pbar1: inversion', ['tx', 'ty', 'tz', 'i'], [1, 1, 1, -1],
         translations(3) + [[4, 4]] + [[4, j, -4, j] for j in (1, 2, 3)],
         (3, (2,)), 3, [-1, -1, -1], -1)
screw = add_case('P2_1: screw', ['tx', 'ty', 'tz', 'g'], [1] * 4,
                 translations(3) + [[4, 4, -3], [4, 1, -4, 1], [4, 2, -4, 2], [4, 3, -4, -3]],
                 (1, ()), 3, [-1, -1, 1], 1)
v = [row[0] for row in screw.cocycle_basis_columns]
assert v[0] == v[1] == 0 and abs(v[3]) == 1 and v[2] == 2 * v[3]
add_case('P1 x C2^T: finite internal antiunitary kernel', ['tx', 'ty', 'tz', 'T'], [1, 1, 1, -1],
         translations(3) + [[4, 4]] + [comm(4, j) for j in (1, 2, 3)],
         (0, (2,)), 3, [1, 1, 1], -1)
add_case('Antiunitary primitive translation: Z^3', ['a', 'ty', 'tz'], [-1, 1, 1],
         translations(3), (0, (2,)), 3, [1, 1, 1], -1)
add_case('Four translations: Z^4', ['t1', 't2', 't3', 't4'], [1] * 4,
         translations(4), (4, ()), 4)
add_case('Four-dimensional glide: Klein bottle group x Z^2', ['tx', 'ty', 'tz', 'tw', 'g'],
         [1, 1, 1, 1, -1], translations(4) + [[5, 5, -2], [5, 1, -5, 1]]
         + [[5, j, -5, -j] for j in (2, 3, 4)], (1, (2,)), 4, [-1, 1, 1, 1], -1)


def add(g, h):
    return tuple(a + b for a, b in zip(g, h))


def delta(function, word):
    result = function(word[1:])
    for i in range(len(word) - 1):
        merged = word[:i] + (add(word[i], word[i + 1]),) + word[i + 2:]
        result += (-1) ** (i + 1) * function(merged)
    return result + (-1) ** len(word) * function(word[:-1])


def e_2(g, h, offset=0):
    return g[offset] * h[offset + 1]


def h_3(word, offset=0):
    g, h, k = word
    xg, xh = g[offset], h[offset]
    yh, yk = h[offset + 1], k[offset + 1]
    return xg * xh * yh * yk + (xg * (xg - 1) // 2) * yh * yk


def nu_5_single(word, offset=0):
    return Fraction(h_3(word[:3], offset) * e_2(word[3], word[4], offset), 3)


def cup1(word):
    g, h, k = word
    return e_2(add(g, h), k) * e_2(g, h, 2) - e_2(g, add(h, k)) * e_2(h, k, 2)


def phase_twister(word):
    a = cup1(word[:3]) * (e_2(word[3], word[4]) - e_2(word[3], word[4], 2))
    b = (e_2(word[0], word[1]) - e_2(word[0], word[1], 2)) * cup1(word[2:])
    return Fraction(a - b, 3)


def nu_5_pair(word):
    return nu_5_single(word) + nu_5_single(word, 2) + phase_twister(word)


rng = Random(20261015)
checks = {'decomposable_square_primitive': 0, 'free_e_2_source_completion': 0,
          'two_free_e_2_components_completion': 0}
for _ in range(3000):
    word = tuple(tuple(rng.randrange(-4, 5) for _ in range(4)) for _ in range(6))
    assert delta(h_3, word[:4]) == e_2(word[0], word[1]) * e_2(word[2], word[3])
    checks['decomposable_square_primitive'] += 1
    source = Fraction(e_2(word[0], word[1]) * e_2(word[2], word[3]) * e_2(word[4], word[5]), 3)
    assert delta(nu_5_single, word) == source
    checks['free_e_2_source_completion'] += 1
    factors = [e_2(word[i], word[i + 1]) + e_2(word[i], word[i + 1], 2) for i in (0, 2, 4)]
    source = Fraction(factors[0] * factors[1] * factors[2], 3)
    assert (delta(nu_5_pair, word) - source).denominator == 1
    checks['two_free_e_2_components_completion'] += 1

report = {'status': 'PASS', 'state_order': '(e_p,n_p,n_{p+2},nu_{p+3})',
          'h1_source_sha256': hashlib.sha256(SUPPLIED.read_bytes()).hexdigest(),
          'presentation_cases': records, 'bar_checks': checks,
          'scope': 'H1 lattices, real-cohomology ranks, and exact flat-model completions; not a new physical classification'}
(ROOT / 'examples.json').write_text(json.dumps(report, indent=2) + '\n')
print(json.dumps({'status': 'PASS', 'presentation_cases': len(records), 'bar_checks': checks}))
