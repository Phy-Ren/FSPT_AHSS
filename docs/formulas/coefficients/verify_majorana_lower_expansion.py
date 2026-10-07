#!/usr/bin/env python3
"""Replay the 4+1D Majorana face substitution using only public manifests.

Run beside the JSON files with Python 3. No project imports or dependencies.
This checks the entire binary coefficient table, its exact term census, and
all sixteen canonical-quarter carry cases. It is not a cohomology solver.
"""
from pathlib import Path
from itertools import product
import hashlib
import json

HERE = Path(__file__).resolve().parent
SOURCE = HERE / 'FOUR_DIMENSIONAL_MAJORANA_STACKING_FACES.json'
TARGET = HERE / 'FOUR_DIMENSIONAL_MAJORANA_STACKING_LOWER_EXPANDED.json'

def load(path):
    return json.loads(path.read_text())

def replay():
    old, new = load(SOURCE), load(TARGET)
    alphabet = new['face_factor_alphabet']
    ids = {(x['cochain'], tuple(x['face'])): i for i, x in enumerate(alphabet)}
    assert len(ids) == len(alphabet)
    actual = [int(x, 16) for x in new['face_monomials_hex']]
    assert len(actual) == len(set(actual))
    assert all(0 <= x < 1 << len(alphabet) for x in actual)
    def bit(name, face):
        return 1 << ids[name, tuple(face)]
    def substitute(factor):
        name, f = factor['cochain'], factor['face']
        for prime in ['', "'"]:
            u = r'\check n' + prime + '_3'
            a = r'\bar n' + prime + '_2'
            A = r'(' + a + r')^2+\check\omega_2' + a
            if name == r'\overline{d' + u + '}':
                assert len(f) == 5
                tail = bit(a, f[2:])
                return [bit(a, f[:3]) | tail,
                        bit(r'\check\omega_2', f[:3]) | tail]
            if name == r'\overline{\beta\overline{d' + u + '}}':
                return [bit(r'\overline{\beta[' + A + ']}', f)]
        return [bit(name, f)]
    expected, raw = set(), 0
    for term in old['terms']:
        expanded = [0]
        for factor in term:
            expanded = [x | y for x in expanded for y in substitute(factor)]
        raw += len(expanded)
        for mask in expanded:
            expected.symmetric_difference_update([mask])
    assert expected == set(actual), 'The complete lower-expanded face polynomial differs.'
    ms = new['ordinary_MS']
    assert len(ms) == len({(x['word'], tuple(x['arguments'])) for x in ms})
    for row in ms:
        assert set(map(int, row['word'])) == set(range(1, len(row['arguments']) + 1))
        assert all(x != y for x, y in zip(row['word'], row['word'][1:]))
    counts = {'ordinary_MS': len(ms), 'binary_face_products': len(actual),
              'other_half_cups': len(new['half_cups']),
              'quarter_cups': len(new['quarter_cups'])}
    assert counts == new['counts']
    assert sum(counts.values()) == new['count']
    assert raw == new['lower_face_substitution']['raw_occurrences']
    # Compare in quarter units, so all arithmetic is exact over integers.
    for x, y, z, t in product([0, 1], repeat=4):
        left = (x ^ y) * (z ^ t)
        right = x*z+x*t+y*z+y*t - 2*(x*y*z+x*y*t+x*z*t+y*z*t)
        assert (left - right) % 4 == 0
    return {'status': 'PASS', 'counts': counts, 'total': sum(counts.values()),
            'source_face_terms': len(old['terms']), 'raw_substitution_occurrences': raw,
            'quarter_carry_cases': 16,
            'sha256': {p.name: hashlib.sha256(p.read_bytes()).hexdigest()
                       for p in [SOURCE, TARGET]}}

if __name__ == '__main__':
    print(json.dumps(replay(), indent=2))
