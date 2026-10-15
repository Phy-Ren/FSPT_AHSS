#!/usr/bin/env python3
"""Independent presentation and primitive-filling audit of the hard-spin control."""
from pathlib import Path
from functools import reduce
from math import gcd
import hashlib
import json
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    run = ROOT / 'sg221_spin_half'
    case = run / 'spacegroup_221_spin_half'
    payload = json.loads((case / 'result.json').read_text())
    record = payload['classification']
    assert payload['run']['status'] == 'complete' and payload['run']['exitCode'] == 0
    assert payload['run']['inputSHA256'] == digest(case / 'input.json')
    assert record == json.loads((case / 'native.json').read_text())
    manifest = json.loads((run / 'source.json').read_text())
    assert manifest == json.loads((ROOT / 'run/source.json').read_text())
    assert payload['run']['sourceSHA256'] == manifest['sha256']
    for filename, expected in manifest['files'].items():
        assert digest(ROOT / 'source' / filename) == expected
    matrix = sp.Matrix(record['presentation'])
    assert matrix.cols == record['presentationGeneratorCount'] == len(record['generators'])
    smith = smith_normal_form(matrix, domain=sp.ZZ)
    diagonal = [abs(int(smith[i, i])) for i in range(min(smith.shape))]
    torsion = [x for x in diagonal if x > 1]
    free = matrix.cols - sum(x != 0 for x in diagonal)
    assert torsion == record['torsion'] and free == record['freeRank']
    filling = record['spaceGroupFilling']
    periods = filling['generatorFillings']
    assert len(periods) == matrix.cols and all(type(x) is int for x in periods)
    assert matrix * sp.Matrix(periods) == sp.zeros(matrix.rows, 1)
    assert reduce(gcd, map(abs, periods), 0) == filling['fillingStep']
    charge = [value for value, root in zip(periods, record['generators']) if root['kind'] == 'charge']
    ci = [value for value, root in zip(periods, record['generators']) if root['kind'] == 'CI']
    assert charge == filling['chargeRootSubgroupGeneratorFillings']
    assert ci == filling['ciGeneratorFillings']
    assert reduce(gcd, map(abs, charge), 0) == filling['chargeRootSubgroupFillingStep']
    volume = sp.Matrix(filling['primitiveTranslationVectors']).det()
    assert volume > 0 and volume == sp.Rational(filling['primitiveCellVolume'])
    assert record['nativeChainIdentitiesVerified'] is True and record['nativeCompletionChecks'] == 20
    report = {'status': 'PASS', 'id': payload['input']['id'], 'resultSHA256': digest(case / 'result.json'),
              'sourceSHA256': manifest['sha256'], 'verifiedSourceFiles': len(manifest['files']),
              'presentationShape': list(matrix.shape), 'torsion': torsion, 'freeRank': free,
              'fillingStep': filling['fillingStep'], 'primitiveCellVolume': str(volume),
              'nativeRuntimeCompletionChecks': record['nativeCompletionChecks'],
              'elapsedSeconds': payload['run']['elapsedSeconds'],
              'scope': 'Independent exact SNF, primitive filling relations and source/input provenance; native completion flag retained, no nonlinear recalculation.',
              'scriptSHA256': digest(Path(__file__))}
    (ROOT / 'sg221_spin_half_audit.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
