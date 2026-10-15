#!/usr/bin/env python3
"""Portable offline verification; optional local exact regression replay."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile

BASE = Path(__file__).resolve().parent


def sha(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def read(path):
    return json.loads(path.read_bytes())


def members(data):
    result = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:') as archive:
        for item in archive.getmembers():
            name = Path(item.name)
            assert not name.is_absolute() and '..' not in name.parts
            if item.isdir():
                continue
            assert item.isfile() and item.name not in result
            result[item.name] = archive.extractfile(item).read()
    return result


def clean(value):
    if isinstance(value, dict):
        return {k: clean(v) for k, v in value.items() if k != 'resolutionBuildTimings'}
    if isinstance(value, list):
        return [clean(v) for v in value]
    return value


def verify(repository, replay):
    manifest = read(BASE/'manifest.json')['filesSHA256']
    actual = {str(p.relative_to(BASE)) for p in BASE.rglob('*') if p.is_file()
              and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    assert set(manifest) == actual
    for name, expected in manifest.items():
        assert sha((BASE/name).read_bytes()) == expected, name
    proof = read(BASE/'provenance.json')
    packed = (BASE/'evidence.tar.gz').read_bytes()
    assert len(packed) == proof['archiveBytes'] and sha(packed) == proof['archiveSHA256']
    tar = gzip.decompress(packed)
    assert sha(tar) == proof['uncompressedTarSHA256']
    raw = members(tar)
    assert set(raw) == set(proof['members']) and len(raw) == 34
    for name, metadata in proof['members'].items():
        assert len(raw[name]) == metadata['bytes'] and sha(raw[name]) == metadata['sha256']
    for name, expected in proof['originalMetadataSHA256'].items():
        assert sha(raw[name]) == expected
    original = json.loads(raw['provenance.json'])
    assert original['baseCommit'] == proof['baseCommit']
    assert len(original['sourceFiles']) == proof['sourceFileCount'] == 1289
    assert sha(canonical(original['sourceFiles'])) == proof['sourceManifestSHA256']
    baseline = members(subprocess.check_output(
        ['git', 'archive', proof['baseCommit']] + proof['sourceDirectories'], cwd=repository))
    assert set(baseline) == set(original['sourceFiles'])
    for name, expected in original['sourceFiles'].items():
        assert sha(baseline[name]) == expected, name
    patch = (BASE/'duplicate_native_reuse.patch').read_bytes()
    changed = (BASE/'candidate_classification.g').read_bytes()
    assert sha(patch) == proof['patchSHA256'] == original['patchSHA256']
    assert sha(changed) == proof['candidateClassificationSHA256']
    assert original['candidateChanges'] == {'gap/classification.g': sha(changed)}
    with tempfile.TemporaryDirectory(prefix='u1-native-vector-patch-') as temporary:
        folder = Path(temporary)
        (folder/'gap').mkdir()
        (folder/'gap/classification.g').write_bytes(baseline['gap/classification.g'])
        subprocess.run(['git', 'apply', '--no-index', '--whitespace=error', '-'],
                       input=patch, cwd=folder, check=True, capture_output=True)
        assert (folder/'gap/classification.g').read_bytes() == changed
        assert {str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file()} == {'gap/classification.g'}
    run = json.loads(raw['test_run.json'])
    assert run['exitCode'] == 0 and run['testSHA256'] == sha(raw['test_duplicate_native_reuse.py'])
    assert run['logSHA256'] == sha(raw['tests.log'])
    assert b'Ran 3 tests in 26.822s' in raw['tests.log'] and b'\nOK\n' in raw['tests.log']
    classifications = [json.loads(raw['checks/'+tree+'/classifications.json'])
                       for tree in ['reference', 'candidate']]
    assert all(len(rows) == 10 for rows in classifications)
    before = after = 0
    savings = []
    for old, new in zip(*classifications):
        assert old['name'] == new['name'] and clean(old['result']) == clean(new['result'])
        x, y = old['counts'], new['counts']
        assert x['reductions'] == y['reductions'] and x['chargeReductions'] == y['chargeReductions']
        difference = x['native'] - y['native']
        assert difference == x['reductions'] + x['chargeReductions'] > 0
        assert x['nonzeroNative'] - y['nonzeroNative'] == difference
        before += x['native']; after += y['native']
        savings.append({'case': old['name'], 'referenceCalls': x['native'], 'candidateCalls': y['native'],
                        'exactCallsRemoved': difference, 'nonzeroCallsRemoved': difference})
    assert (before, after) == (proof['nativeCallsBefore'], proof['nativeCallsAfter']) == (384, 352)
    assert json.loads(raw['checks/classification_comparison.json']) == {
        'passed': True, 'caseCount': 10, 'ignoredResultFields': ['resolutionBuildTimings'],
        'savings': savings, 'wallTimeSpeedupClaimed': False}
    roots = classifications[0]
    assert roots[0]['result']['torsion'] == [4]
    assert roots[0]['result']['generators'][1]['nativePhase'] == ['1/4']
    assert roots[6]['result']['torsion'] == [8]
    assert roots[7]['result']['generators'][-1]['nativePhase'] == ['1/16']
    gauges = [json.loads(raw['checks/'+tree+'/gauges.json']) for tree in ['reference', 'candidate']]
    assert all(len(rows) == 16 for rows in gauges)
    values = 0
    for old, new in zip(*gauges):
        assert {k:v for k,v in old.items() if k!='counts'} == {k:v for k,v in new.items() if k!='counts'}
        assert old['counts']['native']-new['counts']['native'] == 1
        values += len(old['values'])
    assert values == proof['exactGaugePhaseValues'] == 864
    assert {tuple(x['signs']) for x in gauges[0]} == {(0,0),(0,1),(1,0),(1,1)}
    assert {x['mode'] for x in gauges[0]} == {'canonical','reference'}
    assert {x['dimension'] for x in gauges[0]} == {2,3}
    for tree in ['reference','candidate']:
        prefix = 'checks/'+tree+'/'
        for label in ['classifications','gauges','invalid_phase']:
            process = json.loads(raw[prefix+label+'.process.json'])
            assert process['U1_DAG_MODE'] == 'python'
            assert (process['returncode'] != 0) == (label == 'invalid_phase')
        assert b'Completed phase does not solve its native source' in (
            raw[prefix+'invalid_phase.stdout']+raw[prefix+'invalid_phase.stderr'])
    if replay:
        with tempfile.TemporaryDirectory(prefix='u1-native-vector-replay-') as temporary:
            folder = Path(temporary)
            for tree in ['reference','candidate']:
                for name, data in baseline.items():
                    dest = folder/tree/name; dest.parent.mkdir(parents=True,exist_ok=True)
                    dest.write_bytes(data)
            (folder/'candidate/gap/classification.g').write_bytes(changed)
            test = folder/'test_duplicate_native_reuse.py'; test.write_bytes(raw['test_duplicate_native_reuse.py'])
            subprocess.run([sys.executable,str(test)],cwd=folder,check=True)
    return {'verified':True,'baseCommit':proof['baseCommit'],'gitSourceFiles':len(baseline),
            'retainedOriginalFiles':len(raw),'fullClassifications':10,'exactGaugePhaseValues':values,
            'nativeCallsBefore':before,'nativeCallsAfter':after,'allChecksAndOutputsPreserved':True,
            'invalidPhaseStillRejected':True,'wallTimeSpeedupClaimed':False,'replayed':replay}


if __name__ == '__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository',type=Path,default=BASE.parents[2])
    parser.add_argument('--replay',action='store_true',help='Run the three exact local GAP/HAP controls in temporary trees')
    args=parser.parse_args()
    print(json.dumps(verify(args.repository.resolve(),args.replay),indent=2,sort_keys=True))
