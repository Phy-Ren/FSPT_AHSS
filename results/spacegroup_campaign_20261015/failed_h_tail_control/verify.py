#!/usr/bin/env python3
"""Verify archived incomplete H-tail diagnostics offline; no acceptance or live actions."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

BASE = Path(__file__).resolve().parent
TAG = 'sgfull-20261015-h-tail-n08'


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def verify(repository):
    manifest = read(BASE / 'manifest.json')
    names = {str(p.relative_to(BASE)) for p in BASE.rglob('*')
             if p.is_file() and p != BASE / 'manifest.json' and '__pycache__' not in p.parts}
    assert names == set(manifest['filesSHA256'])
    for name, expected in manifest['filesSHA256'].items():
        assert sha((BASE / name).read_bytes()) == expected, name
    capture, proof = read(BASE / 'capture.json'), read(BASE / 'provenance.json')
    assert sha((BASE / 'capture.py').read_bytes()) == proof['captureScriptSHA256']
    assert sha((BASE / 'capture.json').read_bytes()) == proof['captureSHA256']
    assert capture['tag'] == TAG and capture['artifactsStableAcrossRead'] is True
    assert capture['sourceSnapshotVerified'] is True and capture['formulaRuntimeVerified'] is True
    for key in ('remoteFilesChanged', 'signalsSent', 'classificationRun', 'acceptedClassificationClaimed'):
        assert capture[key] is False
    archive = (BASE / 'raw.tar.gz').read_bytes()
    assert sha(archive) == capture['archiveSHA256'] and len(archive) == capture['archiveBytes']
    raw = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
        for member in tar.getmembers():
            path = Path(member.name)
            assert member.isfile() and not path.is_absolute() and '..' not in path.parts
            assert member.name not in raw
            raw[member.name] = tar.extractfile(member).read()
    assert set(raw) == set(capture['files']) and len(raw) == 33
    for name, meta in capture['files'].items():
        assert len(raw[name]) == meta['bytes'] and sha(raw[name]) == meta['sha256']
    prefix = 'runs/' + TAG
    j = lambda name: json.loads(raw[prefix + name])
    source, runtime, selected = j('/source.json'), j('/formula_runtime.json'), j('/selection.json')
    canonical = json.dumps(source['files'], sort_keys=True, separators=(',', ':')).encode()
    assert sha(canonical) == source['sha256'] == capture['sourceSHA256'] == proof['sourceSHA256']
    assert source['files'] == capture['sourceSnapshotFilesSHA256'] and len(source['files']) == 60
    for name, expected in source['files'].items():
        assert sha(subprocess.check_output(['git', 'show', proof['ciCommit'] + ':' + name], cwd=repository)) == expected
    assert runtime == capture['formulaRuntime']
    assert runtime['requestedMode'] == 'auto' and runtime['libraryPresent'] is True
    assert runtime['librarySHA256'] == capture['actualFormulaLibrarySHA256'] == proof['formulaVMSHA256']
    assert runtime['libraryPath'] == capture['sourceSnapshot'] + '/insulator/_compiled/u1_dag_vm.so'
    launch_archive = repository / 'results/spacegroup_campaign_20261015/deployment_h_tail/initial_metadata.tar.gz'
    assert sha(launch_archive.read_bytes()) == proof['launchArchiveSHA256']
    with tarfile.open(launch_archive) as tar:
        for suffix in ('-launch.json', '-finalizer-launch.json', '/source.json', '/selection.json', '/formula_runtime.json'):
            assert raw[prefix + suffix] == tar.extractfile(prefix + suffix).read()
    launch, finalizer, final = j('-launch.json'), j('-finalizer-launch.json'), j('-finalization.json')
    assert launch['pid'] == finalizer['runnerPID'] == final['runnerPID'] == 10773
    assert launch['finalizerPID'] == finalizer['pid'] == 10776
    assert final['state'] == 'incomplete' and final['sourceSHA256'] == source['sha256']
    assert len(selected) == len(set(selected)) == final['selectedCount'] == 4
    expected = {'spacegroup_%03d_%s' % (n, s) for n in (226, 230) for s in ('spin_half', 'spinless')}
    failed = {'spacegroup_226_spin_half', 'spacegroup_226_spinless'}
    assert set(selected) == expected and set(final['retryCases']) == failed
    assert sha(raw[prefix + '/selection.json']) == final['selectionSHA256'] == capture['selectionSHA256']
    assert sha(raw[prefix + '/source.json']) == capture['sourceArtifactSHA256']
    summary = {r['id']: r for r in j('/summary.json')}
    assert set(summary) == expected
    statuses = {}
    for case in selected:
        path = prefix + '/' + case + '/'
        run, data = json.loads(raw[path + 'run.json']), json.loads(raw[path + 'input.json'])
        assert run == summary[case] and run['id'] == data['id'] == case
        assert run['sourceSHA256'] == source['sha256'] and run['inputSHA256'] == sha(raw[path + 'input.json'])
        assert raw[path + 'input.json'] == subprocess.check_output(
            ['git', 'show', proof['ciCommit'] + ':insulator_catalog/generated/' + case + '.json'], cwd=repository)
        assert run['pairedSpins'] is True and run['command'][run['command'].index('-K') + 1] == '8g'
        assert run['batchCaseIDs'] == [case[:14] + '_spin_half', case[:14] + '_spinless']
        assert run['stdoutCapture']['eofObserved'] is True
        if case in failed:
            assert run['status'] == 'failed' and type(run['exitCode']) is int and run['exitCode'] == 1
            assert run['batchExitCode'] == 1 and run['batchElapsedSeconds'] == 7750.144
            assert run['completionMarkerObserved'] is False and run['caseTimingAvailable'] is False
            assert run['elapsedSeconds'] is None
            assert run['caseStartBoundaryAvailable'] is case.endswith('_spin_half')
            if case.endswith('_spinless'):
                assert run['startedUTCMethod'] == 'batch-wall-anchor; individual-case-start-unavailable'
            assert path + 'native.json' not in raw and path + 'result.json' not in raw
            assert b'U1_PAIR_CASE_DONE' not in raw[path + 'stdout.log']
            assert sha(raw[path + 'stderr.log']) == '2a1a68e213d42def67d28aed98ba2fb34c5d0439c04b1aee3657e4be228512e2'
            assert b'cannot extend the workspace any more' in raw[path + 'stderr.log']
        else:
            assert run['status'] == 'complete' and type(run['exitCode']) is int and run['exitCode'] == 0
            assert run['batchExitCode'] == 0 and run['completionMarkerObserved'] is True
            native = json.loads(raw[path + 'native.json'])
            assert json.loads(raw[path + 'result.json']) == {'input': data, 'run': run, 'classification': native}
            assert raw[path + 'stderr.log'] == b''
        statuses[case] = run['status']
    assert proof['acceptedClassificationClaimed'] is False and proof['physicalClassificationCertified'] is False
    return {'verified': True, 'archiveSHA256': capture['archiveSHA256'], 'rawFiles': 33,
            'sourceFilesCheckedAgainstGit': 60, 'statuses': statuses,
            'failureReason': 'GAP 8g workspace exhaustion during the first SG226 case',
            'spinlessNeverStartedMetadataConfirmed': True,
            'ordinarySG230RecordsAreDiagnosticsOnly': True, 'acceptedClassificationClaimed': False,
            'cochainsRecomputed': False, 'liveActionsPerformed': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path,
                        default=next((p for p in BASE.parents if (p / '.git').exists()), Path.cwd()))
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve()), indent=2, sort_keys=True))
