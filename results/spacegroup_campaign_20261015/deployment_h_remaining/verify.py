#!/usr/bin/env python3
"""Verify launch-only H replacement evidence offline; never run the downloader."""
import json
from pathlib import Path
from evidence_checks import archive_files, launch_check, package_check, read, sha, source_check

BASE = Path(__file__).resolve().parent


def verify():
    package_check(BASE)
    files = archive_files(BASE / 'initial_metadata.tar.gz')
    download = json.loads(files['download.json'])
    assert set(files) == set(download['files']) | {'download.json'}
    for name, meta in download['files'].items():
        assert sha(files[name]) == meta['sha256'] and len(files[name]) == meta['bytes']
    summary = read(BASE / 'download_summary.json')
    assert summary['archiveSHA256'] == sha((BASE / 'initial_metadata.tar.gz').read_bytes())
    assert summary['metadataFiles'] == len(download['files']) == 39
    plan_raw = files['snapshots/u1_h_remaining_plan_20261015.json']
    plan = json.loads(plan_raw)
    expected = json.loads(files['snapshots/u1_h_tail_expected_20261015.json'])
    assert plan['expected'] == expected and plan['expectedSHA256'] == sha(files['snapshots/u1_h_tail_expected_20261015.json'])
    source = source_check(BASE, expected)
    universe = {'spacegroup_%03d_%s' % (n,s) for n in range(1,231) for s in ('spinless','spin_half')}
    assert set(plan['fullCoverageMap']) == universe and plan['uniqueCoverageCount'] == 460
    reconstructed = {}
    for parent in plan['coverageParents']:
        for case in parent['selection']:
            reconstructed.setdefault(case, []).append({'family': parent['family'], 'root': parent['root']})
    assert reconstructed == plan['fullCoverageMap']
    g_cases = [case for selected in plan['GSelections'].values() for case in selected]
    assert len(g_cases) == len(set(g_cases)) == 201
    tail = {'spacegroup_%03d_%s' % (n,s) for n in (226,230) for s in ('spinless','spin_half')}
    assert set(plan['excludedTailCases']) == tail
    available = {x['id'] for x in plan['availabilityObservations'] if x['nativeAvailable']}
    assert len(available) == 173
    for record in plan['availabilityObservations']:
        if record['nativeAvailable']:
            assert len(record['nativeSHA256']) == 64 and len(record['inputSHA256']) == 64
            checks = record['scientificChecks']
            assert checks['nativeChainIdentitiesVerified'] and checks['completeWitnessListsPresent']
            assert checks['nativeCompletionChecks'] > 0
    assert set(plan['candidateCases']) == set(g_cases) - available - tail
    assert plan['candidateCount'] == len(plan['candidateCases']) == 24
    all_cases = []; launches = []
    for node in ['n02','n03']:
        tag = 'sgfull-20261015-h-remaining-' + node
        cases = plan['assignments'][node]
        assert len(cases) == 12
        launch = launch_check(BASE, files, expected, tag, node, 12, '12g', cases, False)
        assert launch['planSHA256'] == sha(plan_raw)
        assert launch['launcherSHA256'] == sha(files['snapshots/u1_launch_h_remaining_20261015.py'])
        assert all(not item['excludedAvailable'] for item in launch['finalAvailabilityChecks'])
        assert {x['id'] for x in launch['finalAvailabilityChecks']} == set(cases)
        for item in launch['finalAvailabilityChecks']:
            assert all(not x['nativeAvailable'] for x in item['observations'])
        for case in cases:
            assert plan['parentGRoot'][case] in plan['GSelections']
            assert case in plan['GSelections'][plan['parentGRoot'][case]]
            assert launch['inputSHA256'][case] == plan['candidateInputSHA256'][case]
            run = json.loads(files['runs/' + tag + '/' + case + '/run.json'])
            assert run['id'] == case and run['status'] == 'running' and not run.get('batchCaseIDs')
            assert run['inputSHA256'] == launch['inputSHA256'][case] and run['sourceSHA256'] == source['sha256']
        all_cases += cases
        launches.append({'node':node,'runnerPID':launch['pid'],'finalizerPID':launch['finalizerPID'],'cases':len(cases)})
    assert len(all_cases) == len(set(all_cases)) == 24 and set(all_cases) == set(plan['candidateCases'])
    downloader = BASE / 'downloader'
    config, launch = read(downloader / 'config.json'), read(downloader / 'launch.json')
    assert sha((downloader / 'download_completed.py').read_bytes()) == config['helperSHA256'] == launch['helperSHA256']
    assert (downloader / 'download_completed.py').read_bytes() == (BASE.parent / 'completed_h/download_tool/download_completed.py').read_bytes()
    assert sha((downloader / 'config.json').read_bytes()) == launch['configSHA256']
    assert sha((downloader / 'run_download.py').read_bytes()) == launch['wrapperSHA256']
    assert launch['existingDownloaderModuleUnchanged'] and launch['existingDownloaderArgvUnchanged'] and launch['noClassificationOrSignals']
    assert launch['existingDownloaderPID'] == 7779 and launch['pid'] == 223851
    assert config['tags'] == ['sgfull-20261015-h-tail-n08','sgfull-20261015-h-remaining-n02','sgfull-20261015-h-remaining-n03']
    assert config['downloadDirectory'] == '/home/xingyu/insulator-campaign-download'
    assert config['frozenCollectorCommit'] == 'c07c6e5d4a69d79c9c2aeb0739ae1e189029f824'
    status = read(downloader / 'initial_status.json')
    assert status['pid'] == launch['pid'] and set(status['tags']) == set(config['tags'])
    assert all(record['state'] == 'waiting' for record in status['tags'].values())
    return {'verified':True,'sourceFilesCheckedAgainstGit':len(source['files']),
            'newStandaloneCases':24,'existingNativeAvailabilityRecords':173,'coverageUnique':460,
            'launches':launches,'separateDownloaderPID':launch['pid'],'completionClaimed':False}


if __name__ == '__main__':
    print(json.dumps(verify(),indent=2,sort_keys=True))
