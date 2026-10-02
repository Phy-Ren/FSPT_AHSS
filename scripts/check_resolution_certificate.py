#!/usr/bin/env python3
"""Replay saved integral resolution certificates without GAP or FSPT formulas.

Checks the group table, transport, augmented boundary, d squared and every
translated contraction identity through the recorded degrees. Use a compute
node for arithmetic verification. This does not calculate a physical group.
"""
import argparse
import collections
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def check_certificate(c):
    """Use only exported group multiplication and integer chain coefficients."""
    n, dims = c['order'], c['dimensions']
    mul, identity = c['multiplication'], c['identity']
    assert n == 16 and len(dims) == 8 and dims[0] == 1
    assert len(mul) == n and all(len(row) == n for row in mul)
    assert sorted(c['transportImages']) == list(range(1, n + 1))
    for g in range(1, n + 1):
        assert mul[identity - 1][g - 1] == g == mul[g - 1][identity - 1]
        assert sorted(mul[g - 1]) == list(range(1, n + 1))
        for h in range(1, n + 1):
            image = c['transportImages']
            assert image[c['sourceMultiplication'][g - 1][h - 1] - 1] == mul[image[g - 1] - 1][image[h - 1] - 1]
            for j in range(1, n + 1):
                assert mul[mul[g - 1][h - 1] - 1][j - 1] == mul[g - 1][mul[h - 1][j - 1] - 1]

    def combine(terms):
        out = collections.defaultdict(int)
        for a, i, g in terms:
            assert type(a) is int and type(i) is int and type(g) is int
            assert 1 <= g <= n
            out[i, g] += a
        return {key: value for key, value in out.items() if value}

    def boundary(k, terms):
        if k == 0:
            return {}
        result = []
        for (i, g), a in terms.items():
            assert 1 <= i <= dims[k]
            for b, j, h in c['boundaries'][k][i - 1]:
                assert 1 <= j <= dims[k - 1]
                result.append((a * b, j, mul[g - 1][h - 1]))
        return combine(result)

    def contract(k, terms):
        result = []
        for (i, g), a in terms.items():
            assert 1 <= i <= dims[k]
            for b, j, h in c['contractions'][k][i - 1][g - 1]:
                assert 1 <= j <= dims[k + 1]
                result.append((a * b, j, h))
        return combine(result)

    nd, nh = 0, 0
    assert len(c['boundaries']) == 8 and len(c['contractions']) == 7
    for k in range(8):
        assert len(c['boundaries'][k]) == dims[k]
        if k <= 6:
            assert len(c['contractions'][k]) == dims[k]
        for i in range(1, dims[k] + 1):
            if k <= 6:
                assert len(c['contractions'][k][i - 1]) == n
            for g in range(1, n + 1):
                x = {(i, g): 1}
                if k == 1:
                    assert sum(boundary(k, x).values()) == 0
                if k >= 2:
                    assert not boundary(k - 1, boundary(k, x)), (k, i, g, 'd2')
                    nd += 1
                if k <= 6:
                    y = collections.defaultdict(int, boundary(k + 1, contract(k, x)))
                    if k:
                        for key, value in contract(k - 1, boundary(k, x)).items():
                            y[key] += value
                    else:
                        y[1, identity] += 1
                    y[i, g] -= 1
                    assert not any(y.values()), (k, i, g, 'dh+hd')
                    nh += 1
    assert nd == c['dSquaredCells'] == n * sum(dims[2:])
    assert nh == c['contractionCells'] == n * sum(dims[:7])
    assert all(dims[k] == sum(c['factorDimensions'][0][j] * c['factorDimensions'][1][k - j]
                             for j in range(k + 1)) for k in range(8))
    return dict(d_squared_cells=nd, contraction_cells=nh, transport_products=n * n,
                group_associativity_triples=n ** 3, augmented_boundary_cells=n * dims[1])


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('certificates', nargs='*', type=Path)
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    if not __debug__: ap.error('Run without Python -O: certificate checks use assertions')
    if args.output and args.output.exists(): ap.error('Use a fresh output path')
    saved = ROOT/'results/resolution_certificates'
    profiles = json.loads((saved/'PROFILE.json').read_text())['profiles']
    expected = {p['certificate']: p for p in profiles}
    paths = args.certificates or [saved/p['certificate'] for p in profiles]
    results = []
    for path in paths:
        payload = path.read_bytes()
        digest = hashlib.sha256(payload).hexdigest()
        certificate = json.loads(payload)
        arithmetic = check_certificate(certificate)
        retained = path.parent.resolve() == saved.resolve() and path.name in expected
        if retained:
            assert digest == expected[path.name]['certificate_sha256']
            assert arithmetic == expected[path.name]['independent_python_replay']
        results.append(dict(certificate=path.name, sha256=digest, retained_bytes_verified=retained,
                            family=certificate['group'], **arithmetic))
    report = dict(success=True, physical_groups_computed=0, checks=results)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as stream: json.dump(report, stream, indent=2); stream.write('\n')
    print(json.dumps(report))


if __name__ == '__main__': main()
