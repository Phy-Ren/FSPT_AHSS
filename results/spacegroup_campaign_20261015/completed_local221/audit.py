#!/usr/bin/env python3
"""Replay hashes, exact native equations, Smith groups and the pinned E8 extension."""
from fractions import Fraction
from functools import reduce
import hashlib
import importlib
import json
from math import gcd
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import types

import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parent
REPO = ROOT.parents[2]
CASE = 'spacegroup_221_spinless'


def sha(data):
    return hashlib.sha256(data).hexdigest()


def read(path):
    return json.loads(path.read_text())


def committed(commit, name):
    return subprocess.check_output(['git', 'show', commit + ':' + name], cwd=REPO)


def smith(c):
    matrix = sp.Matrix(c['presentation'])
    width = c.get('presentationGeneratorCount', c.get('generatorCount'))
    assert matrix.cols == width
    diagonal = smith_normal_form(matrix, domain=sp.ZZ)
    values = [abs(int(diagonal[i, i])) for i in range(min(diagonal.shape))]
    result = {'torsion': [v for v in values if v > 1],
              'freeRank': width - sum(v != 0 for v in values)}
    assert result == {k: c[k] for k in result}
    return result


def multiply(vector, matrix):
    assert len(vector) == len(matrix)
    out = [Fraction(0)] * len(matrix[0]) if matrix else []
    for a, row in zip(vector, matrix):
        a = Fraction(a)
        if a:
            for j, b in enumerate(row):
                if b:
                    out[j] += a * b
    return out


def main():
    manifest = read(ROOT / 'artifact_manifest.json')
    for name, expected in manifest['files'].items():
        assert sha((ROOT / name).read_bytes()) == expected, name
    archive_manifest = read(ROOT / 'archive_members.json')
    raw = {}
    with tarfile.open(ROOT / 'raw_ci_e8_acceptance.tar.gz', 'r:gz') as archive:
        for member in archive.getmembers():
            assert member.isfile() and member.name not in raw
            assert not Path(member.name).is_absolute() and '..' not in Path(member.name).parts
            raw[member.name] = archive.extractfile(member).read()
    assert set(raw) == set(archive_manifest['files'])
    for name, data in raw.items():
        assert {'SHA256': sha(data), 'bytes': len(data)} == archive_manifest['files'][name]
    payload = lambda name: json.loads(raw[name])
    provenance = read(ROOT / 'source_verification.json')
    for name, expected in provenance['proofReferences'].items():
        assert sha((REPO / name).read_bytes()) == expected, name
    proof = REPO / 'results/spacegroup_campaign_20261015/generic_cochain_performance/sg221'
    overlay = read(proof / 'overlay.json')
    for family in ('ci', 'e8'):
        source = payload(family + '/source.json')
        assert sha(json.dumps(source['files'], sort_keys=True, separators=(',', ':')).encode()) == source['sha256']
        for name, expected in source['files'].items():
            if family == 'ci':
                data = ((proof / 'candidate/overlay_sources' / name).read_bytes()
                        if name in overlay['changedFiles'] else committed(provenance['ciBaseCommit'], name))
            else:
                data = committed(provenance['e8SourceCommit'], name)
            assert sha(data) == expected, (family, name)
    for name, expected in provenance['collectorFiles'].items():
        assert sha(committed(provenance['collectorSourceCommit'], name)) == expected

    ci_bytes = raw['ci/' + CASE + '/result.json']
    assert ci_bytes == raw['e8/' + CASE + '/ci_result.json'] == (proof / 'candidate/result.json').read_bytes()
    ci, e8 = json.loads(ci_bytes), payload('e8/' + CASE + '/result.json')
    for family, result in (('ci', ci), ('e8', e8)):
        run = payload(family + '/' + CASE + '/run.json')
        assert run == result['run'] and run['status'] == 'complete' and run['exitCode'] == 0
        assert run['inputSHA256'] == sha(raw[family + '/' + CASE + '/input.json'])
        assert result['input'] == payload(family + '/' + CASE + '/input.json')
        assert run['sourceSHA256'] == payload(family + '/source.json')['sha256']
    assert raw['ci/' + CASE + '/input.json'] == raw['e8/' + CASE + '/input.json']
    assert e8['run']['ciResultSHA256'] == sha(ci_bytes)
    assert e8['run']['ciRun'] == ci['run'] and e8['run']['ciSourceSHA256'] == ci['run']['sourceSHA256']
    assert e8['classification']['ciSector'] == ci['classification'] == payload('ci/' + CASE + '/native.json')
    assert not e8['classification']['physicalClassificationCertified']
    vm = payload('ci/formula_runtime.json')
    assert vm == provenance['formulaRuntime'] and vm['librarySHA256'] == overlay['nativeVM_SHA256']

    c = ci['classification']
    baseline = read(proof / 'baseline/result.json')['classification']
    changed = [k for k in set(c) | set(baseline) if c.get(k) != baseline.get(k)]
    assert changed == ['resolutionBuildTimings'], changed
    assert c['nativeChainIdentitiesVerified'] is True and c['nativeCompletionChecks'] > 0
    groups = {'ci': smith(c), 'e8': smith(e8['classification']), 'neutral': smith(e8['classification']['e8H1'])}
    filling = c['spaceGroupFilling']
    periods = filling['generatorFillings']
    assert len(periods) == c['presentationGeneratorCount']
    assert sp.Matrix(c['presentation']) * sp.Matrix(periods) == sp.zeros(len(c['presentation']), 1)
    assert reduce(gcd, map(abs, periods), 0) == filling['fillingStep']
    charge = [v for v, g in zip(periods, c['generators']) if g['kind'] == 'charge']
    sheet = [v for v, g in zip(periods, c['generators']) if g['kind'] == 'CI']
    assert charge == filling['chargeRootSubgroupGeneratorFillings']
    assert sheet == filling['ciGeneratorFillings']
    assert reduce(gcd, map(abs, charge), 0) == filling['chargeRootSubgroupFillingStep']
    volume = sp.Matrix(filling['primitiveTranslationVectors']).det()
    assert volume > 0 and volume == sp.Rational(filling['primitiveCellVolume'])
    assert filling['primitiveBasisGeneratesFullTranslationKernel'] is True
    d = read(proof / 'baseline/differentials.json')
    counts = dict(phaseGeneratorClosures=0, chargeGeneratorClosures=0, sheetGeneratorClosures=0,
                  savedPhasePrimitiveEquations=0, savedSourceClosures=0, gaugeReducedPhaseClosures=0)
    for generator in c['generators']:
        kind = generator['kind']
        field, matrix, count = {'phase': ('nativePhase', 'phaseD4', 'phaseGeneratorClosures'),
                                'charge': ('nativeCharge', 'chargeD3', 'chargeGeneratorClosures'),
                                'CI': ('nativeSheet', 'sheetD1', 'sheetGeneratorClosures')}[kind]
        values = multiply(generator[field], d[matrix])
        assert all(x.denominator == 1 for x in values) if kind == 'phase' else all(x == 0 for x in values)
        counts[count] += 1
    for witness in c['witnesses']:
        if 'nativeSource' in witness and 'nativePhase' in witness:
            source, phase = witness['nativeSource'], witness['nativePhase']
        elif 'nativeResidualSource' in witness and 'nativePhaseCorrection' in witness:
            source, phase = witness['nativeResidualSource'], witness['nativePhaseCorrection']
        else:
            continue
        boundary = multiply(phase, d['phaseD4'])
        assert len(boundary) == len(source)
        assert all((a - Fraction(b)).denominator == 1 for a, b in zip(boundary, source))
        assert all(x.denominator == 1 for x in multiply(source, d['phaseD5']))
        counts['savedPhasePrimitiveEquations'] += 1
        counts['savedSourceClosures'] += 1
    for witness in c['gaugeReductionWitnesses']:
        assert all(x.denominator == 1 for x in multiply(witness['nativeFinalPhase'], d['phaseD4']))
        counts['gaugeReducedPhaseClosures'] += 1
    assert sum(counts.values()) == 51

    # Replay the exact small E8 computation from committed source, without
    # importing the evolving checkout or repeating the nonlinear CI solve.
    with tempfile.TemporaryDirectory(prefix='u1-local221-e8-audit-') as temporary:
        namespace = '_u1_local221_pinned'
        package = types.ModuleType(namespace)
        package.__path__ = [temporary]
        sys.modules[namespace] = package
        for name in ('e8_h1', 'e8_pointgroup', 'e8_spacegroup'):
            (Path(temporary) / (name + '.py')).write_bytes(
                committed(provenance['e8SourceCommit'], 'insulator/' + name + '.py'))
        module = importlib.import_module(namespace + '.e8_spacegroup')
        replay = module.extend_spacegroup_classification(ci)
        assert replay == e8['classification']
    collection = payload('accepted/collection.json')
    assert collection['accepted'] is True and len(collection['collections']) == 1
    item = collection['collections'][0]
    assert item['count'] == 1
    for name, expected in item['filesSHA256'].items():
        assert sha(raw['accepted/' + item['path'] + '/' + name]) == expected
    accepted = 'accepted/' + item['path'] + '/'
    assert payload(accepted + 'ci_results.json') == [ci]
    assert payload(accepted + 'results.json') == [e8]
    validation = payload(accepted + 'validation.json')
    assert validation['accepted'] is True and validation['selectedCases'] == [CASE]
    assert validation['missingOrFailedSelectedCases'] == []
    result = {'status': 'PASS', 'id': CASE, 'archiveMembersVerified': len(raw),
              'ciSourceFilesVerified': len(payload('ci/source.json')['files']),
              'e8SourceFilesVerified': len(payload('e8/source.json')['files']),
              'ciResultSHA256': sha(ci_bytes), 'e8ResultSHA256': sha(raw['e8/' + CASE + '/result.json']),
              'ciParentBytesEqual': True, 'e8ClassificationReplayExact': True,
              'independentSmithGroups': groups, 'fillingStep': filling['fillingStep'],
              'primitiveCellVolume': str(volume), 'linearEquationCounts': counts,
              'nativeRuntimeCompletionChecks': c['nativeCompletionChecks'],
              'acceptedCollectionContainsExactCIAndE8Records': True,
              'physicalClassificationCertified': False,
              'scope': 'Selected four-data model; source identities, saved native equations, presentations, filling and neutral-section replay. No new nonlinear CI run or physical-kernel theorem.'}
    print(json.dumps(result, indent=2, sort_keys=True))


if __name__ == '__main__':
    main()
