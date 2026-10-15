#!/usr/bin/env python3
"""Verify the two standalone H launch records offline, without completion claims."""
import json
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE.parent / 'deployment_h_remaining'))
from evidence_checks import archive_files, launch_check, package_check, read, sha, source_check

TAG = 'sgfull-20261015-h-tail-highmem-n02'
CASES = ['spacegroup_226_spin_half', 'spacegroup_230_spin_half']


def verify():
    package_check(BASE)
    package_check(BASE.parent / 'deployment_h_remaining')
    files = archive_files(BASE / 'initial_metadata.tar.gz')
    download = read(BASE / 'download.json')
    assert sha((BASE / 'initial_metadata.tar.gz').read_bytes()) == download['archiveSHA256']
    assert len(files) == 19 and set(files) == set(download['files'])
    for name, meta in download['files'].items():
        assert sha(files[name]) == meta['sha256'] and len(files[name]) == meta['bytes']
    expected = json.loads(files['snapshots/u1_h_tail_expected_20261015.json'])
    source = source_check(BASE, expected)
    launch = launch_check(BASE, files, expected, TAG, 'n02', 2, '32g', CASES, False)
    assert launch['pid'] == 42816 and launch['finalizerPID'] == 42819
    assert launch['expectedSHA256'] == sha(files['snapshots/u1_h_tail_expected_20261015.json'])
    assert launch['launcherSHA256'] == sha(files['snapshots/u1_launch_h_tail_highmem_20261015.py'])
    assert launch['finalizerSHA256'] == sha(files['snapshots/u1_finalize_campaign_20261015.py'])
    assert files['snapshots/u1_finalize_campaign_20261015.py'] == (
        BASE.parent / 'deployment_h/finalizers/u1_finalize_campaign_20261015.py').read_bytes()
    assert set(launch['inputSHA256']) == set(CASES)
    assert launch['batchTimeoutSeconds'] == launch['timeoutSecondsPerCase'] == 14400
    assert launch['jobs'] == 2 and launch['paired'] is False
    for case in CASES:
        prefix = 'runs/' + TAG + '/' + case + '/'
        input_raw = files[prefix + 'input.json']
        assert sha(input_raw) == launch['inputSHA256'][case] == expected['inputSHA256'][case]
        git_raw = subprocess.check_output(
            ['git', 'show', expected['sourceCommit'] + ':insulator_catalog/generated/' + case + '.json'],
            cwd=BASE.parents[2])
        assert input_raw == git_raw
        run = json.loads(files[prefix + 'run.json'])
        assert run['id'] == case and run['status'] == 'running'
        assert run['sourceSHA256'] == source['sha256'] and run['inputSHA256'] == sha(input_raw)
        assert not run.get('pairedSpins') and not any(key.startswith('batch') for key in run)
        assert run['command'][-1] == launch['output'] + '/' + case + '/driver.g'
        assert run['command'][run['command'].index('-K') + 1] == '32g'
        assert 'U1_PAIR_CASE_DONE' not in files[prefix + 'driver.g'].decode()
    preparation = read(BASE / 'preparation.json')
    assert preparation['authorizedCases'] == CASES and preparation['existingTasksChanged'] is False
    assert preparation['launcherSHA256'] == launch['launcherSHA256']
    sample = read(BASE / 'prelaunch_process_sample.json')
    gaps = [row for row in sample['processes'] if row['kind'] == 'GAP']
    assert len(gaps) == 16
    assert all(row['sourceSHA256'] in {source['sha256'],
        '17150f175fffd703f2d1008ec0066f53f25d23abfc63dbb15dd71440243a08fc'} for row in gaps)
    pressured = [row for row in gaps if row['family'] == 'G' and 'spacegroup_226_spin_half' in row['caseIDs']]
    assert len(pressured) == 1 and pressured[0]['workspaceLimit'] == '8g'
    assert pressured[0]['rssKiB'] >= 8 * 1024**2
    assert sample['physicalCores'] == 28 and sample['loadavg'][0] < 20
    assert sample['memoryKiB']['MemFree'] > 400 * 1024**2
    downloader = BASE / 'download_tool'
    config = read(downloader / 'config.json')
    dl_launch = read(downloader / 'launch.json')
    assert config['tags'] == [TAG]
    assert config['frozenCollectorCommit'] == 'c07c6e5d4a69d79c9c2aeb0739ae1e189029f824'
    assert sha((downloader / 'download_completed.py').read_bytes()) == config['helperSHA256'] == dl_launch['helperSHA256']
    assert config['helperSHA256'] == '15b4501bb0bfbb35c316221cbfdcd77299ff4590ed7d6928abf4b616fa8b7ba3'
    assert sha((downloader / 'run_download.py').read_bytes()) == dl_launch['wrapperSHA256']
    assert sha((downloader / 'config.json').read_bytes()) == dl_launch['configSHA256']
    assert dl_launch['pid'] == 459428 and dl_launch['originalArtifactsUnchanged']
    assert dl_launch['noClassificationOrSignals'] is True
    return {'verified': True, 'sourceFilesCheckedAgainstGit': len(source['files']),
            'cases': CASES, 'standaloneJobs': 2, 'memoryPerJob': '32g',
            'recordedRunnerPID': 42816, 'recordedFinalizerPID': 42819,
            'recordedDownloaderPID': 459428, 'completionClaimed': False,
            'selectionIntoFinalCatalogueClaimed': False}


if __name__ == '__main__':
    print(json.dumps(verify(), indent=2, sort_keys=True))
