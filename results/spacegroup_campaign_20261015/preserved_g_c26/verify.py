#!/usr/bin/env python3
"""Replay preserved G evidence offline with the exact c26 helpers reconstructed from Git."""
import argparse
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


def read(path):
    return json.loads(path.read_bytes())


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def git_bytes(repository, commit, name):
    return subprocess.check_output(['git', 'show', commit + ':' + name], cwd=repository)


def verify(repository, replay_log=None):
    manifest = read(BASE / 'manifest.json')
    actual = {str(p.relative_to(BASE)) for p in BASE.rglob('*')
              if p.is_file() and p != BASE / 'manifest.json' and '__pycache__' not in p.parts}
    assert actual == set(manifest['filesSHA256'])
    for name, expected in manifest['filesSHA256'].items():
        assert sha((BASE / name).read_bytes()) == expected, name
    provenance = read(BASE / 'provenance.json')
    for name, meta in provenance['retainedOriginalFiles'].items():
        assert sha((BASE / name).read_bytes()) == meta['sha256']
    pipeline = BASE / 'common/pipeline'
    config = read(pipeline / 'prepared_config.json')
    assert sha((pipeline / 'postprocess_g.py').read_bytes()) == '70cc4c24c29a348b51b37bba0322e223cc29d234d89fd80030358dc76cea7c57'
    assert sha(canonical(config['helperSnapshot']['files'])) == config['helperSnapshot']['treeSHA256']
    assert config['helperSnapshot']['commit'] == provenance['helperCommit']
    for folder in (pipeline, BASE / 'common/readiness'):
        for name, meta in read(folder / 'artifact_manifest.json')['files'].items():
            data = (folder / name).read_bytes()
            assert len(data) == meta['bytes'] and sha(data) == meta['sha256']
    deployment = read(pipeline / 'root_deployment.json')
    assert deployment['archiveSHA256'] == sha((pipeline / 'snapshot-g-postprocess-70cc4c24.tar.gz').read_bytes())
    assert deployment['deploymentManifestSHA256'] == sha((pipeline / 'snapshot_metadata.json').read_bytes())
    readiness_raw = (BASE / 'common/readiness/readiness.json').read_bytes()
    readiness = json.loads(readiness_raw)
    assert readiness_raw == (BASE / 'common/root_actions/readiness.json').read_bytes()
    assert readiness['acceptedH24'] is True and readiness['requiredG88OrdinaryVerified'] is True
    assert readiness['everyActiveGCaseCoveredByAcceptedH24'] is True
    assert readiness['authorizesSignals'] is False
    assert readiness['configSHA256'] == sha((pipeline / 'prepared_config.json').read_bytes())
    assert readiness['helperTreeSHA256'] == config['helperSnapshot']['treeSHA256']
    assert readiness['scriptSHA256'] == sha((BASE / 'common/readiness/check_supplement.py').read_bytes())
    accepted_h = {case for parent in readiness['acceptedHParents'] for case in parent['cases']}
    assert len(accepted_h) == 24 and set(readiness['activeGCaseIDs']) <= accepted_h
    assert all(parent['state'] == 'validated' for parent in readiness['acceptedHParents'])
    rows, all_required, all_preserved, all_recovered, logs = [], set(), set(), set(), []
    source_cache = {}
    with tempfile.TemporaryDirectory(prefix='u1-preserved-g-c26-verify-') as temporary:
        temp = Path(temporary)
        helper, catalog = temp / 'helper', temp / 'catalog'
        helper.mkdir(); catalog.mkdir()
        for name, meta in config['helperSnapshot']['files'].items():
            data = git_bytes(repository, config['helperSnapshot']['commit'], name)
            assert len(data) == meta['bytes'] and sha(data) == meta['sha256'], name
            path = helper / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(data)
        assert len(config['helperSnapshot']['files']) == 65
        for node in ('n02', 'n03'):
            folder, spec = BASE / node, config['nodes'][node]
            final = read(folder / 'completion.json')
            assert (folder / 'completion.json').read_bytes() == (folder / 'completion.second.json').read_bytes()
            assert final['state'] == 'accepted-preserved-subset' and final['node'] == node
            assert final['signalsSent'] is False and final['originalParentUnmodified'] is True
            assert final['configSHA256'] == sha((pipeline / 'prepared_config.json').read_bytes())
            assert final['scriptSHA256'] == sha((pipeline / 'postprocess_g.py').read_bytes())
            original_download, download = read(folder / 'download_proof.json'), read(folder / 'download_verification.json')
            assert original_download['completionUnchangedAcrossDownload'] is True and original_download['verificationExitCode'] == 0
            assert original_download['completionSHA256'] == download['completionSHA256'] == sha((folder / 'completion.json').read_bytes())
            assert download['frozenCollectorExactReplay'] is True and download['originalExtractedFilesUnchanged'] is True
            archive = (folder / 'evidence.tar.gz').read_bytes()
            assert len(archive) == final['archiveBytes']
            assert sha(archive) == final['archiveSHA256'] == original_download['archiveSHA256'] == download['archiveSHA256']
            raw = {}
            with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
                for member in tar.getmembers():
                    path = Path(member.name)
                    assert member.isfile() and not path.is_absolute() and '..' not in path.parts
                    assert member.name not in raw
                    raw[member.name] = tar.extractfile(member).read()
            assert set(raw) == set(final['archiveMembersSHA256'])
            assert all(sha(data) == final['archiveMembersSHA256'][name] for name, data in raw.items())
            roots = final['roots']
            j = lambda name: json.loads(raw[name])
            original, ci, e8 = roots['original'], roots['ci'], roots['e8']
            source = j(original + '/source.json')
            assert sha(canonical(source['files'])) == source['sha256'] == spec['sourceSHA256']
            assert source == j(ci + '/source.json')
            for name, expected in source['files'].items():
                key = (provenance['ciSourceCommit'], name)
                if key not in source_cache:
                    source_cache[key] = sha(git_bytes(repository, *key))
                assert source_cache[key] == expected
            original_selection = j(original + '/selection.json')
            assert sha(raw[original + '/selection.json']) == spec['selectionSHA256']
            assert len(original_selection) == final['originalSelectedCount']
            for case in original_selection:
                data = git_bytes(repository, provenance['catalogueCommit'], 'insulator_catalog/generated/' + case + '.json')
                assert raw[original + '/' + case + '/input.json'] == data
                (catalog / (case + '.json')).write_bytes(data)
            e8_source = j(e8 + '/source.json')
            assert sha(canonical(e8_source['files'])) == e8_source['sha256']
            for name, expected in e8_source['files'].items():
                assert sha((helper / name).read_bytes()) == expected
            runtime = j(original + '/formula_runtime.json')
            assert runtime == j(ci + '/_recovery/original_campaign/formula_runtime.json')
            assert runtime['libraryPresent'] is True and runtime['librarySHA256'] == '0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2'
            ledger = j(ci + '/recovery.json')
            assert raw[ci + '/recovery.json'] == (folder / 'recovery.json').read_bytes()
            preserved, ordinary, recovered = [set(ledger[key]) for key in ('preservedCases', 'ordinaryCompleteCases', 'recoveredCases')]
            required = set(spec['requiredCases'])
            assert required <= ordinary and required.isdisjoint(recovered)
            assert preserved == ordinary | recovered and not ordinary & recovered
            assert preserved == set(j(ci + '/selection.json')) == set(j(e8 + '/selection.json'))
            assert preserved | set(ledger['retryCases']) == set(original_selection)
            assert not preserved & set(ledger['retryCases'])
            assert sorted(required) == final['requiredCases'] == download['requiredCases']
            assert len(preserved) == final['preservedCount'] == download['preservedCount']
            for case in ordinary:
                for name in ('result.json', 'run.json', 'native.json', 'input.json'):
                    assert raw[ci + '/' + case + '/' + name] == raw[original + '/' + case + '/' + name]
            for case in preserved:
                result = j(ci + '/' + case + '/result.json')
                assert result['run']['status'] == ('complete' if case in ordinary else 'recovered_complete')
                assert raw[e8 + '/' + case + '/ci_result.json'] == raw[ci + '/' + case + '/result.json']
                assert j(e8 + '/' + case + '/result.json')['classification']['physicalClassificationCertified'] is False
            report = j(roots['operation'] + '/external_report/cancellation.json')
            assert sha(raw[roots['operation'] + '/external_report/cancellation.json']) == final['reportSHA256']
            assert report['allOwnedProcessesStopped'] is True
            assert report['sourceSnapshotVerified'] is True and report['formulaRuntimeVerified'] is True
            for item in report['evidence']:
                assert sha(raw[roots['operation'] + '/external_report/' + item['path']]) == item['sha256']
            plan = read(BASE / 'common/root_actions' / (node + '-plan.json'))
            assert plan['readinessSHA256'] == sha(readiness_raw)
            action = [json.loads(line) for line in (BASE / 'common/root_actions' / (node + '-stdout.log')).read_text().splitlines() if line.strip()]
            preflight, stopped = action
            assert preflight['readinessSHA256'] == sha(readiness_raw) and preflight['allActiveCasesAcceptedInH'] is True
            assert set(preflight['activeCases']) <= accepted_h and preflight['requiredOrdinaryCount'] == len(required)
            runner = next(p for p in report['processes'] if p['role'] == 'runner')
            assert (preflight['runnerPID'], preflight['runnerStartTicks']) == (runner['pid'], runner['startTicks'])
            assert stopped['stoppedProcesses'] == len(report['processes']) and stopped['stoppedGroups'] == len(report['batches'])
            assert all(p['observedState'] in ('absent', 'Z') for p in report['processes'])
            summary = provenance['nodes'][node]
            assert summary['preservedCount'] == len(preserved) and summary['ordinaryCount'] == len(ordinary)
            assert summary['recoveredCases'] == ledger['recoveredCases'] and summary['retryCases'] == ledger['retryCases']
            assert summary['extraControlCases'] == sorted(preserved - required)
            assert summary['rawArchiveMembers'] == len(raw) and summary['allRequiredOrdinary'] is True
            assert all_required.isdisjoint(required) and all_preserved.isdisjoint(preserved)
            all_required.update(required); all_preserved.update(preserved); all_recovered.update(recovered)
            output = temp / ('replay-' + node)
            command = [sys.executable, str(pipeline / 'postprocess_g.py'), 'verify', '--node', node,
                       '--completion', str(folder / 'completion.json'), '--archive', str(folder / 'evidence.tar.gz'),
                       '--output', str(output), '--helper', str(helper), '--catalog', str(catalog)]
            process = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            logs.append({'node': node, 'command': command, 'exitCode': process.returncode,
                         'stdout': process.stdout.decode(), 'stderr': process.stderr.decode()})
            assert process.returncode == 0, process.stderr.decode()
            replay = read(output / 'download_verification.json')
            assert replay['frozenCollectorExactReplay'] is True and replay['originalExtractedFilesUnchanged'] is True
            assert replay['requiredCases'] == sorted(required) and replay['preservedCount'] == len(preserved)
            # The archive includes failed original records and complete full preserved parents.
            # The pinned pipeline revalidates all recovered cases before its full-parent collector replay.
            rows.append({'node': node, 'originalCount': len(original_selection), 'preservedCount': len(preserved),
                         'requiredOrdinaryCount': len(required), 'extraControls': len(preserved - required),
                         'ordinaryCount': len(ordinary), 'recoveredCount': len(recovered),
                         'retryCount': len(ledger['retryCases']), 'archiveSHA256': final['archiveSHA256']})
    assert len(all_required) == 88 and len(all_preserved) == 105 and len(all_recovered) == 5
    assert not all_required & all_recovered and len(all_preserved - all_required) == 17
    if replay_log is not None:
        replay_log = Path(replay_log)
        if replay_log.exists():
            raise ValueError('Replay log requires a new output path')
        replay_log.write_text(json.dumps(logs, indent=2, sort_keys=True) + '\n')
    return {'verified': True, 'nodes': rows, 'requiredOrdinaryTotal': 88, 'preservedTotal': 105,
            'extraControlTotal': 17, 'recoveredExtraControls': 5, 'frozenCollectorReplayRepeated': True,
            'helperFilesReconstructedFromGit': 65, 'CIClassificationRecomputed': False,
            'originalCampaignsDeclaredSuccessful': False, 'verificationSignalsSent': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path,
                        default=next((p for p in BASE.parents if (p / '.git').exists()), Path.cwd()))
    parser.add_argument('--replay-log', type=Path, help='Optional new external JSON log for the two replay subprocesses')
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve(), args.replay_log), indent=2, sort_keys=True))
