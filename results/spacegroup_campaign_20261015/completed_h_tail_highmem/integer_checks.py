#!/usr/bin/env python3
"""Verify the finite SG210 overlap offline; never read or signal live jobs."""
import argparse
from fractions import Fraction
from functools import reduce
import gzip
import hashlib
import io
import json
from math import gcd
from pathlib import Path
import subprocess
import tarfile

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

BASE = Path(__file__).resolve().parent
CASE = 'spacegroup_210_spinless'
SOURCES = {
    'G': ('sgfull-20261015-g-n03', 'c07c6e5d4a69d79c9c2aeb0739ae1e189029f824'),
    'H': ('sgfull-20261015-h-remaining-n02', 'ea44c1f55314ddd66587cf452bbaae9331f3a1db'),
}
EXECUTION_KEYS = {'formulaCacheStats', 'formulaWorkerCalls', 'pairedGeometryReuse', 'resolutionBuildTimings'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def read(path):
    return json.loads(path.read_bytes())


def group(rows, count):
    assert type(count) is int and count >= 0
    assert all(len(row) == count and all(type(x) is int for x in row) for row in rows)
    if not rows or not count:
        return {'torsion': [], 'freeRank': count}
    diagonal = smith_normal_form(Matrix(rows), domain=ZZ)
    nonzero = [abs(int(diagonal[i, i])) for i in range(min(diagonal.shape)) if diagonal[i, i]]
    return {'torsion': [x for x in nonzero if x > 1], 'freeRank': count - len(nonzero)}


def scientific(native):
    """Independent integer checks and consistency of the saved native witnesses."""
    count = native['presentationGeneratorCount']
    actual = group(native['presentation'], count)
    assert actual == {k: native[k] for k in ('torsion', 'freeRank')}
    assert native['theory'] == 'U(1)^f insulator' and native['spatialDimension'] == 3
    assert native['nativeChainIdentitiesVerified'] is True
    assert type(native['nativeCompletionChecks']) is int and native['nativeCompletionChecks'] > 0
    assert native['inputValidation']['independentCharactersChecked'] is True
    dimensions = native['resolutionDimensions']
    assert len(dimensions) >= 6 and all(type(x) is int and x >= 0 for x in dimensions)
    assert len(native['generators']) == count
    for root in native['generators']:
        fields = {'phase': [('nativePhase', 4)],
                  'charge': [('nativeCharge', 3), ('nativePhase', 4)],
                  'CI': [('nativeSheet', 1), ('nativeCharge', 3), ('nativePhase', 4)]}[root['kind']]
        for name, degree in fields:
            vector = root[name]
            assert len(vector) == dimensions[degree] and all(type(x) in (int, str) for x in vector)
            values = [Fraction(x) for x in vector]
            assert name == 'nativePhase' or all(x.denominator == 1 for x in values)
    assert all(isinstance(native[name], list) and all(isinstance(x, dict) for x in native[name])
               for name in ('witnesses', 'gaugeReductionWitnesses'))
    filling = native['spaceGroupFilling']
    values = filling['generatorFillings']
    assert len(values) == count and all(type(x) is int for x in values)
    assert all(sum(a*b for a, b in zip(row, values)) == 0 for row in native['presentation'])
    roots = native['generators']
    charge = [value for root, value in zip(roots, values) if root['kind'] == 'charge']
    sheet = [value for root, value in zip(roots, values) if root['kind'] == 'CI']
    assert charge == filling['chargeRootSubgroupGeneratorFillings'] and sheet == filling['ciGeneratorFillings']
    assert all(value == 0 for root, value in zip(roots, values) if root['kind'] == 'phase')
    step = reduce(gcd, map(abs, values), 0)
    charge_step = reduce(gcd, map(abs, charge), 0)
    assert step == filling['fillingStep'] and charge_step == filling['chargeRootSubgroupFillingStep']
    basis = filling['primitiveTranslationVectors']
    assert len(basis) == 3 and all(len(row) == 3 for row in basis)
    volume = Matrix([[Fraction(str(x)) for x in row] for row in basis]).det()
    assert volume > 0 and volume == Fraction(str(filling['primitiveCellVolume']))
    assert filling['primitiveBasisGeneratesFullTranslationKernel'] is True
    assert filling['allPresentationRelationsHaveZeroFilling'] is True
    layers = {}
    for name in ('sheet', 'charge', 'phase'):
        rows = native['filtrationPresentations'][name]
        width = len(rows[0]) if rows else len(native[name + 'Orders'])
        layers[name] = group(rows, width)
        assert layers[name] == {'torsion': native['final' + name.title() + 'Orders'],
                                'freeRank': native['final' + name.title() + 'FreeRank']}
    return {'independentSmithGroup': actual,
            'independentPresentationFillingCheck': {
                'fillingStep': step, 'chargeSubgroupFillingStep': charge_step,
                'everyPresentationRelationPreservesFilling': True,
                'positivePrimitiveCellVolume': str(volume), 'nativePrimitiveLatticeCertificatePresent': True},
            'nativeCompletionChecks': native['nativeCompletionChecks'],
            'nativeChainIdentitiesVerified': True, 'completeWitnessListsPresent': True,
            'independentFiltrationSmithGroups': layers}


def verify(repository):
    manifest = read(BASE / 'manifest.json')
    names = {str(p.relative_to(BASE)) for p in BASE.rglob('*')
             if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    assert names == set(manifest['filesSHA256'])
    for name, expected in manifest['filesSHA256'].items():
        assert sha((BASE / name).read_bytes()) == expected, name
    provenance = read(BASE / 'provenance.json')
    for name, expected in provenance['retainedMetadataOriginalSHA256'].items():
        assert sha((BASE / name).read_bytes()) == expected
    for name, expected in provenance['originalScriptsSHA256'].items():
        assert sha((BASE / 'original_scripts' / name).read_bytes()) == expected
    archive = (BASE / 'raw.tar.gz').read_bytes()
    assert len(archive) == provenance['archiveBytes'] and sha(archive) == provenance['archiveSHA256']
    tar_raw = gzip.decompress(archive)
    assert sha(tar_raw) == provenance['uncompressedTarSHA256']
    raw = {}
    with tarfile.open(fileobj=io.BytesIO(tar_raw), mode='r:') as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            assert member.isfile() and not path.is_absolute() and '..' not in path.parts
            assert member.name not in raw
            raw[member.name] = tar.extractfile(member).read()
    download = read(BASE / 'download.json')
    assert download['exitCode'] == 0 and download['unchangedDuringRead'] is True
    assert len(raw) == provenance['rawMemberCount'] == 20 and set(raw) == set(download['files'])
    for name, meta in download['files'].items():
        assert len(raw[name]) == meta['size'] and sha(raw[name]) == meta['sha256']
    result = read(BASE / 'comparison.json')
    assert result['status'] == 'PASS' and result['case'] == CASE
    assert result['comparisonScriptSHA256'] == sha((BASE / 'original_scripts/compare.py').read_bytes())
    records = {}
    for label, (tag, commit) in SOURCES.items():
        j = lambda name: json.loads(raw[tag + '/' + name])
        source, runtime = j('source.json'), j('formula_runtime.json')
        assert sha(canonical(source['files'])) == source['sha256']
        for name, expected in source['files'].items():
            assert sha(subprocess.check_output(['git', 'show', commit + ':' + name], cwd=repository)) == expected
        prefix = CASE + '/'
        data, run, native = j(prefix + 'input.json'), j(prefix + 'run.json'), j(prefix + 'native.json')
        saved = j(prefix + 'result.json')
        assert saved == {'input': data, 'classification': native, 'run': run}
        assert data['id'] == run['id'] == CASE and data['dimension'] == 3 and data['family'] == 'spacegroup'
        assert run['status'] == 'complete' and run['exitCode'] == 0
        assert run['sourceSHA256'] == source['sha256'] and run['inputSHA256'] == sha(raw[tag + '/' + prefix + 'input.json'])
        assert raw[tag + '/' + prefix + 'input.json'] == subprocess.check_output(
            ['git', 'show', commit + ':insulator_catalog/generated/' + CASE + '.json'], cwd=repository)
        assert CASE in j('selection.json')
        recorded = result['checks'][label]
        assert recorded['sourceCommit'] == commit and recorded['sourceSHA256'] == source['sha256']
        assert recorded['sourceFileCount'] == len(source['files']) and recorded['formulaRuntime'] == runtime
        checks = scientific(native)
        assert all(recorded[key] == value for key, value in checks.items())
        records[label] = saved
    g, h = records['G'], records['H']
    assert g['input'] == h['input']
    assert raw[SOURCES['G'][0] + '/' + CASE + '/input.json'] == raw[SOURCES['H'][0] + '/' + CASE + '/input.json']
    ng, nh = g['classification'], h['classification']
    assert set(ng) == set(nh)
    differences = {key: {'G': ng[key], 'H': nh[key]} for key in ng if ng[key] != nh[key]}
    assert set(differences) == EXECUTION_KEYS and differences == result['executionMetadataDifferences']
    science = {key: value for key, value in ng.items() if key not in EXECUTION_KEYS}
    assert science == {key: value for key, value in nh.items() if key not in EXECUTION_KEYS}
    assert len(science) == result['scientificFieldCount'] == 34 and sorted(science) == result['scientificFields']
    assert sha(canonical(science)) == result['canonicalScientificObjectSHA256']
    run_diff = {key: {'G': g['run'].get(key), 'H': h['run'].get(key),
                      'GPresent': key in g['run'], 'HPresent': key in h['run']}
                for key in set(g['run']) | set(h['run']) if g['run'].get(key) != h['run'].get(key)}
    assert run_diff == result['runMetadataDifferences']
    assert result['entireNativeObjectEquality'] is False and result['scientificFieldsLiterallyEqual'] is True
    assert result['inputByteEquality'] is True
    return {'status': 'PASS', 'case': CASE, 'scientificFieldsLiterallyEqual': len(science),
            'executionDifferenceKeys': sorted(differences), 'group': result['group'],
            'sourceFilesCheckedAgainstGit': {key: result['checks'][key]['sourceFileCount'] for key in SOURCES},
            'controlledSpeedupClaimed': False, 'cochainsRecomputed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=BASE.parents[2])
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve()), indent=2, sort_keys=True))
