#!/usr/bin/env python3
"""Verify twelve archived G/H overlaps offline, without accepting any campaign."""
import argparse
from collections import Counter
import copy
import gzip
import hashlib
import io
import json
from pathlib import Path
import runpy
import subprocess
import tarfile

BASE = Path(__file__).resolve().parent
EXECUTION = {'formulaCacheStats', 'formulaWorkerCalls', 'pairedGeometryReuse',
             'resolutionBuildTimings'}
SCOPES = {'completed-parent-overlap': 'both_case_records_ordinary_complete',
          'native-only-diagnostic-not-accepted': 'H_ordinary_G_native_only_diagnostic'}
SCOPE_TEXT = ('Five comparisons have both ordinary case records complete; seven have '
              'H ordinary case records and G native-only diagnostics. The containing '
              'campaigns were incomplete at capture; this review establishes no '
              'full-campaign acceptance.')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def active_report(original):
    report = copy.deepcopy(original)
    report['counts'] = {SCOPES[key]: value for key, value in report['counts'].items()}
    for row in report['cases']:
        row['scope'] = SCOPES[row['scope']]
    report['scope'] = SCOPE_TEXT
    report['campaignAcceptanceEstablished'] = False
    return report


def verify(repository):
    manifest = read(BASE / 'manifest.json')
    names = {str(p.relative_to(BASE)) for p in BASE.rglob('*')
             if p.is_file() and p != BASE / 'manifest.json' and '__pycache__' not in p.parts}
    assert names == set(manifest['filesSHA256'])
    for name, expected in manifest['filesSHA256'].items():
        assert sha((BASE / name).read_bytes()) == expected, name
    provenance = read(BASE / 'provenance.json')
    original_dir = BASE / 'original_review'
    for name, expected in provenance['retainedOriginalSHA256'].items():
        assert sha((original_dir / name).read_bytes()) == expected, name
    assert sha((original_dir / 'manifest.json').read_bytes()) == provenance['originalManifestSHA256']
    assert sha((original_dir / 'comparison.json').read_bytes()) == provenance['originalComparisonSHA256']
    original_manifest = read(original_dir / 'manifest.json')['filesSHA256']
    original = read(original_dir / 'comparison.json')
    report = read(BASE / 'comparison.json')
    assert report == active_report(original)
    assert report['status'] == 'PASS'
    assert all(report[key] is False for key in ('acceptancePerformed', 'cochainsRecomputed',
                                               'controlledSpeedupClaimed', 'campaignAcceptanceEstablished'))
    assert original['comparisonScriptSHA256'] == sha((original_dir / 'compare.py').read_bytes())
    assert original['integerCheckSourceSHA256'] == sha((original_dir / 'integer_checks.py').read_bytes())
    scientific = runpy.run_path(str(original_dir / 'integer_checks.py'))['scientific']

    archive = (BASE / 'raw.tar.gz').read_bytes()
    assert sha(archive) == provenance['archiveSHA256'] and len(archive) == provenance['archiveBytes']
    unpacked = gzip.decompress(archive)
    assert sha(unpacked) == provenance['uncompressedTarSHA256']
    assert len(unpacked) == provenance['uncompressedTarBytes']
    raw = {}
    with tarfile.open(fileobj=io.BytesIO(unpacked), mode='r:') as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            assert member.isfile() and not path.is_absolute() and '..' not in path.parts
            assert member.name not in raw
            raw[member.name] = tar.extractfile(member).read()
    download = read(original_dir / 'download.json')
    assert download['exitCode'] == 0 and not download['failed']
    assert len(raw) == provenance['rawMemberCount'] == 173
    assert set(raw) == set(download['files'])
    for name, meta in download['files'].items():
        assert len(raw[name]) == meta['size'] and sha(raw[name]) == meta['sha256'], name
        assert sha(raw[name]) == original_manifest['raw/' + name]
    retained = {name: value for name, value in original_manifest.items()
                if not name.startswith('raw/') and name != 'transport.json'}
    assert all(sha((original_dir / name).read_bytes()) == value for name, value in retained.items())
    assert original_manifest['transport.json'] == provenance['omittedTransport']['sha256']
    assert set(original_manifest) == ({'raw/' + name for name in raw} | set(retained) | {'transport.json'})

    pairs = download['pairs']
    assert len(pairs) == len({row['id'] for row in pairs}) == 12
    assert download['fixedSelectedCases'] == [row['id'] for row in pairs]
    assert 'spacegroup_210_spinless' not in download['fixedSelectedCases']
    rows, sources, git_hashes = [], {}, {}
    for pair in pairs:
        case = pair['id']
        assert pair['stableDuringRead'] is True
        assert pair['gResultPresent'] is pair['gOrdinaryComplete']
        natives, checks, runtimes, inputs = {}, {}, {}, {}
        for label in ('G', 'H'):
            tag = pair[label]
            prefix = tag + '/' + case + '/'
            j = lambda name: json.loads(raw[tag + '/' + name])
            source, runtime = j('source.json'), j('formula_runtime.json')
            pin = provenance['sourcePins'][label]
            if tag not in sources:
                assert source['sha256'] == pin['sha256'] == sha(canonical(source['files']))
                assert len(source['files']) == pin['fileCount']
                for name, expected in source['files'].items():
                    git_key = (pin['commit'], name)
                    if git_key not in git_hashes:
                        git_hashes[git_key] = sha(subprocess.check_output(
                            ['git', 'show', pin['commit'] + ':' + name], cwd=repository))
                    assert git_hashes[git_key] == expected, git_key
                sources[tag] = pin
            assert runtime['libraryPresent'] is True and runtime['requestedMode'] == 'auto'
            assert runtime['librarySHA256'] == provenance['sharedLibrarySHA256']
            data, run, native = [json.loads(raw[prefix + name])
                                 for name in ('input.json', 'run.json', 'native.json')]
            assert run['id'] == data['id'] == case and data['dimension'] == 3 and data['family'] == 'spacegroup'
            assert run['sourceSHA256'] == source['sha256']
            assert run['inputSHA256'] == sha(raw[prefix + 'input.json'])
            assert raw[prefix + 'input.json'] == subprocess.check_output(
                ['git', 'show', pin['commit'] + ':insulator_catalog/generated/' + case + '.json'], cwd=repository)
            assert case in j('selection.json')
            ordinary = label == 'H' or pair['gOrdinaryComplete']
            if ordinary:
                assert run['status'] == 'complete' and run['exitCode'] == 0
                assert json.loads(raw[prefix + 'result.json']) == {'input': data, 'run': run, 'classification': native}
            else:
                assert prefix + 'result.json' not in raw and run['status'] != 'complete'
                assert pair['scope'] == 'native-only-diagnostic-not-accepted'
                assert ('U1_PAIR_CASE_DONE ' + case).encode() in raw[prefix + 'stdout.log'].splitlines()
            checks[label] = scientific(native)
            natives[label], runtimes[label], inputs[label] = native, runtime, raw[prefix + 'input.json']
        assert inputs['G'] == inputs['H']
        assert runtimes['G']['librarySHA256'] == runtimes['H']['librarySHA256']
        g, h = natives['G'], natives['H']
        assert set(g) == set(h) and checks['G'] == checks['H']
        differences = {key: {'G': g[key], 'H': h[key]} for key in g if g[key] != h[key]}
        science = {key: value for key, value in g.items() if key not in EXECUTION}
        assert not set(differences) - EXECUTION
        assert science == {key: value for key, value in h.items() if key not in EXECUTION}
        assert len(science) == 34
        rows.append({'id': case, 'scope': SCOPES[pair['scope']],
                     'gOrdinaryComplete': pair['gOrdinaryComplete'],
                     'scientificFieldCount': len(science), 'scientificFields': sorted(science),
                     'scientificFieldsLiterallyEqual': True, 'canonicalScientificSHA256': sha(canonical(science)),
                     'entireNativeObjectsEqual': g == h, 'executionDifferences': differences,
                     'scientificDifferences': [], 'independentChecks': checks['G'],
                     'group': {key: g[key] for key in ('torsion', 'freeRank')},
                     'acceptancePerformed': False, 'coordinateChangeRequired': False})
    assert rows == report['cases'] and sources == report['sources']
    counts = dict(Counter(row['scope'] for row in rows))
    assert counts == report['counts'] == {'both_case_records_ordinary_complete': 5,
                                        'H_ordinary_G_native_only_diagnostic': 7}
    return {'status': 'PASS', 'counts': counts, 'rawMembers': len(raw),
            'scientificFieldsLiterallyEqualPerCase': 34,
            'distinctSourceFilesCheckedAgainstGit': len(git_hashes),
            'campaignAcceptanceEstablished': False, 'cochainsRecomputed': False,
            'controlledSpeedupClaimed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=BASE.parents[2])
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve()), indent=2, sort_keys=True))
