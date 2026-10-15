#!/usr/bin/env python3
"""Independent exact presentation/filling/native linear-equation audit."""
from fractions import Fraction
from functools import reduce
from math import gcd
from pathlib import Path
import hashlib
import json
import subprocess
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parent
REPO = Path('/home/xingyu/FSPT_AHSS_insulator')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def multiply(vector, matrix):
    if not matrix:
        return []
    assert len(vector) == len(matrix)
    result = [Fraction(0)] * len(matrix[0])
    for value, row in zip(vector, matrix):
        value = Fraction(value)
        if value:
            for j, entry in enumerate(row):
                if entry:
                    result[j] += value * entry
    return result


def main():
    path = ROOT / 'run/spacegroup_221_spinless/result.json'
    payload = json.loads(path.read_text())
    c = payload['classification']
    run = payload['run']
    folder = path.parent
    assert run['status'] == 'complete' and run['exitCode'] == 0
    assert run['inputSHA256'] == digest(folder / 'input.json')
    assert c == json.loads((folder / 'native.json').read_text())
    manifest = json.loads((ROOT / 'run/source.json').read_text())
    assert run['sourceSHA256'] == manifest['sha256']
    assert manifest['sha256'] == hashlib.sha256(json.dumps(manifest['files'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    commit_differences = []
    for filename, expected in manifest['files'].items():
        assert digest(ROOT / 'source' / filename) == expected
        data = subprocess.check_output(['git', 'show', 'd922a12:' + filename], cwd=REPO)
        if hashlib.sha256(data).hexdigest() != expected:
            commit_differences.append(filename)
    vm = json.loads((ROOT / 'run/formula_runtime.json').read_text())
    assert digest(Path(vm['libraryPath'])) == vm['librarySHA256']
    presentation = sp.Matrix(c['presentation'])
    assert presentation.cols == c['presentationGeneratorCount'] == len(c['generators'])
    smith = smith_normal_form(presentation, domain=sp.ZZ)
    diagonal = [abs(int(smith[i, i])) for i in range(min(smith.shape))]
    torsion = [x for x in diagonal if x > 1]
    free = presentation.cols - sum(x != 0 for x in diagonal)
    assert torsion == c['torsion'] and free == c['freeRank']
    filling = c['spaceGroupFilling']
    periods = filling['generatorFillings']
    assert len(periods) == presentation.cols and all(type(x) is int for x in periods)
    assert presentation * sp.Matrix(periods) == sp.zeros(presentation.rows, 1)
    assert reduce(gcd, map(abs, periods), 0) == filling['fillingStep']
    charge_periods = [v for v, g in zip(periods, c['generators']) if g['kind'] == 'charge']
    ci_periods = [v for v, g in zip(periods, c['generators']) if g['kind'] == 'CI']
    assert charge_periods == filling['chargeRootSubgroupGeneratorFillings']
    assert ci_periods == filling['ciGeneratorFillings']
    assert reduce(gcd, map(abs, charge_periods), 0) == filling['chargeRootSubgroupFillingStep']
    volume = sp.Matrix(filling['primitiveTranslationVectors']).det()
    assert volume > 0 and volume == sp.Rational(filling['primitiveCellVolume'])
    differential = json.loads((ROOT / 'differentials.json').read_text())
    counts = {'phaseGeneratorClosures': 0, 'chargeGeneratorClosures': 0,
              'sheetGeneratorClosures': 0, 'savedPhasePrimitiveEquations': 0,
              'savedSourceClosures': 0, 'gaugeReducedPhaseClosures': 0}
    for generator in c['generators']:
        kind = generator['kind']
        if kind == 'phase':
            assert all(x.denominator == 1 for x in multiply(generator['nativePhase'], differential['phaseD4']))
            counts['phaseGeneratorClosures'] += 1
        elif kind == 'charge':
            assert all(x == 0 for x in multiply(generator['nativeCharge'], differential['chargeD3']))
            counts['chargeGeneratorClosures'] += 1
        elif kind == 'CI':
            assert all(x == 0 for x in multiply(generator['nativeSheet'], differential['sheetD1']))
            counts['sheetGeneratorClosures'] += 1
    for witness in c['witnesses']:
        if 'nativeSource' in witness and 'nativePhase' in witness:
            source, phase = witness['nativeSource'], witness['nativePhase']
        elif 'nativeResidualSource' in witness and 'nativePhaseCorrection' in witness:
            source, phase = witness['nativeResidualSource'], witness['nativePhaseCorrection']
        else:
            continue
        boundary = multiply(phase, differential['phaseD4'])
        assert len(boundary) == len(source)
        assert all((a - Fraction(b)).denominator == 1 for a, b in zip(boundary, source))
        assert all(x.denominator == 1 for x in multiply(source, differential['phaseD5']))
        counts['savedPhasePrimitiveEquations'] += 1
        counts['savedSourceClosures'] += 1
    for witness in c['gaugeReductionWitnesses']:
        assert all(x.denominator == 1 for x in multiply(witness['nativeFinalPhase'], differential['phaseD4']))
        counts['gaugeReducedPhaseClosures'] += 1
    assert c['nativeChainIdentitiesVerified'] is True and c['nativeCompletionChecks'] > 0
    report = {'status': 'PASS', 'id': payload['input']['id'], 'resultSHA256': digest(path),
              'sourceSHA256': manifest['sha256'], 'sourceFilesVerified': len(manifest['files']),
              'differencesFromCommittedD922a12': commit_differences,
              'formulaRuntime': vm, 'torsion': torsion, 'freeRank': free,
              'presentationShape': list(presentation.shape), 'fillingStep': filling['fillingStep'],
              'primitiveCellVolume': str(volume), 'linearEquationCounts': counts,
              'nativeRuntimeCertificationCount': c['nativeCompletionChecks'],
              'formulaWorkerCalls': c['formulaWorkerCalls'], 'formulaCacheStats': c['formulaCacheStats'],
              'chargePrimaryStats': c['chargePrimaryStats'], 'resolutionBuildTimings': c['resolutionBuildTimings'],
              'elapsedSeconds': run['elapsedSeconds'],
              'scope': 'Independent SNF, primitive-period relations, saved native linear equations and source hashes; no rerun of nonlinear classification or universal physical completeness claim.',
              'files': {p.name: digest(p) for p in [ROOT / 'audit_result.py', ROOT / 'differentials.json', ROOT / 'export_differentials.g', ROOT / 'time.txt']}}
    (ROOT / 'independent_audit.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: report[k] for k in ('status', 'torsion', 'freeRank', 'linearEquationCounts', 'differencesFromCommittedD922a12')}, indent=2))


if __name__ == '__main__':
    main()
