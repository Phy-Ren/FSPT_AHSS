#!/usr/bin/env python3
"""Verify the four-case H control launch offline; do not infer completion."""
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
sys.path.insert(0,str(BASE.parent / 'deployment_h_remaining'))
from evidence_checks import archive_files, launch_check, package_check, read, sha, source_check


def verify():
    package_check(BASE)
    package_check(BASE.parent / 'deployment_h_remaining')
    files = archive_files(BASE / 'initial_metadata.tar.gz')
    download = read(BASE / 'download.json')
    assert sha((BASE / 'initial_metadata.tar.gz').read_bytes()) == download['archiveSHA256']
    assert set(files) == set(download['files']) and len(files) == 9
    for name, meta in download['files'].items():
        assert sha(files[name]) == meta['sha256'] and len(files[name]) == meta['bytes']
    expected = json.loads(files['snapshots/u1_h_tail_expected_20261015.json'])
    source = source_check(BASE, expected)
    cases = ['spacegroup_%03d_%s' % (n,s) for n in (226,230) for s in ('spin_half','spinless')]
    launch = launch_check(BASE, files, expected, 'sgfull-20261015-h-tail-n08', 'n08', 2, '8g', cases, True)
    assert launch['pid'] == 10773 and launch['finalizerPID'] == 10776
    assert launch['expectedSHA256'] == sha(files['snapshots/u1_h_tail_expected_20261015.json'])
    assert launch['launcherSHA256'] == sha(files['snapshots/u1_launch_h_tail_20261015.py'])
    assert launch['finalizerSHA256'] == sha(files['snapshots/u1_finalize_campaign_20261015.py'])
    assert files['snapshots/u1_finalize_campaign_20261015.py'] == (BASE.parent / 'deployment_h/finalizers/u1_finalize_campaign_20261015.py').read_bytes()
    assert launch['inputSHA256'] == expected['inputSHA256']
    return {'verified':True,'sourceFilesCheckedAgainstGit':len(source['files']),
            'cases':cases,'pairedGeometryJobs':2,'recordedRunnerPID':10773,'recordedFinalizerPID':10776,
            'completionClaimed':False}


if __name__ == '__main__':
    print(json.dumps(verify(),indent=2,sort_keys=True))
