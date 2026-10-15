#!/usr/bin/env python3
"""Focused offline checks of a failed run and unchanged ordinary companion."""
import argparse
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile

BASE = Path(__file__).resolve().parent
sha = lambda data: hashlib.sha256(data).hexdigest()


def unpack(data):
    result = {}
    with tarfile.open(fileobj=io.BytesIO(data), mode='r:gz') as archive:
        for member in archive.getmembers():
            name = Path(member.name)
            assert member.isfile() and not name.is_absolute() and '..' not in name.parts
            assert member.name not in result
            result[member.name] = archive.extractfile(member).read()
    return result


def verify(repository):
    read = lambda name: json.loads((BASE / name).read_bytes())
    manifest = read('manifest.json')['filesSHA256']
    assert set(manifest) == {str(p.relative_to(BASE)) for p in BASE.rglob('*')
                             if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    for name, expected in manifest.items():
        assert sha((BASE / name).read_bytes()) == expected
    proof, capture = read('provenance.json'), read('capture.json')
    archive = (BASE / 'raw.tar.gz').read_bytes()
    assert sha(archive) == proof['rawArchiveSHA256']
    raw = unpack(archive)
    assert raw['capture.json'] == (BASE / 'capture.json').read_bytes()
    assert set(raw) == {'capture.json'} | {'raw/' + name for name in capture['files']}
    for name, expected in capture['files'].items():
        assert sha(raw['raw/' + name]) == expected['sha256']
        assert len(raw['raw/' + name]) == expected['bytes']
    assert capture['twoReadsEqual'] is True and capture['originalParentAccepted'] is False
    tag = 'sgfull-20261015-h-tail-spinless-n08'
    prefix = 'raw/runs/' + tag + '/'
    j = lambda name: json.loads(raw[name])
    source = j(prefix + 'source.json')
    assert sha(json.dumps(source['files'], sort_keys=True, separators=(',', ':')).encode()) == source['sha256'] == proof['sourceSHA256']
    for name, expected in source['files'].items():
        assert sha(subprocess.check_output(['git', 'show', proof['sourceCommit'] + ':' + name], cwd=repository)) == expected
    assert j(prefix + 'selection.json') == ['spacegroup_226_spinless', 'spacegroup_230_spinless']
    runtime = j(prefix + 'formula_runtime.json')
    assert runtime['libraryPresent'] is True and runtime['librarySHA256'] == proof['formulaVMSHA256']
    launch_path = repository / 'results/spacegroup_campaign_20261015/deployment_h_tail_spinless/initial_metadata.tar.gz'
    assert sha(launch_path.read_bytes()) == proof['launchArchiveSHA256']
    launch_files = unpack(launch_path.read_bytes())
    launch_name = 'runs/' + tag + '-launch.json'
    assert raw['raw/' + launch_name] == launch_files[launch_name]
    launch = j('raw/' + launch_name)
    assert launch['source'] == source and launch['formulaRuntime'] == runtime
    assert launch['memoryPerJob'] == '12g' and launch['paired'] is False
    for case in j(prefix + 'selection.json'):
        p = prefix + case + '/'
        run, data = j(p + 'run.json'), j(p + 'input.json')
        assert run['id'] == data['id'] == case and run['sourceSHA256'] == source['sha256']
        assert run['inputSHA256'] == sha(raw[p + 'input.json']) == launch['inputSHA256'][case]
        assert raw[p + 'input.json'] == subprocess.check_output(['git', 'show', proof['sourceCommit'] + ':insulator_catalog/generated/' + case + '.json'], cwd=repository)
        assert run['command'][-1] == launch['output'] + '/' + case + '/driver.g'
        assert run['command'][run['command'].index('-K') + 1] == '12g'
        assert not run.get('pairedSpins') and not any(k.startswith('batch') for k in run)
    failed = prefix + 'spacegroup_226_spinless/'
    run = j(failed + 'run.json')
    assert run['status'] == 'failed' and type(run['exitCode']) is int and run['exitCode'] == 1
    assert run['elapsedSeconds'] == 11708.782
    assert failed + 'native.json' not in raw and failed + 'result.json' not in raw
    error = raw[failed + 'stderr.log'].decode()
    assert error == 'Panic in /home/user/xyren/software/gap-4.13.1/src/gasman.c:1379: cannot extend the workspace any more!!\n'
    ordinary = prefix + 'spacegroup_230_spinless/'
    run, native, data, result = [j(ordinary + n) for n in ['run.json', 'native.json', 'input.json', 'result.json']]
    assert run['status'] == 'complete' and type(run['exitCode']) is int and run['exitCode'] == 0
    assert result == {'input': data, 'run': run, 'classification': native}
    approved_path = repository / 'results/spacegroup_campaign_20261015/preserved_h_230_spinless/raw.tar.gz'
    assert sha(approved_path.read_bytes()) == proof['approved230ArchiveSHA256']
    approved = unpack(approved_path.read_bytes())
    for name in ['input.json', 'driver.g', 'run.json', 'native.json', 'result.json', 'stdout.log', 'stderr.log']:
        assert raw[ordinary + name] == approved['original/spacegroup_230_spinless/' + name]
    final = j('raw/runs/' + tag + '-finalization.json')
    assert final['state'] == 'incomplete' and final['retryCases'] == ['spacegroup_226_spinless']
    assert final['sourceSHA256'] == source['sha256']
    gc_raw = (BASE / 'gc_evidence.tar.gz').read_bytes()
    assert sha(gc_raw) == proof['gcArchiveSHA256']
    gc = unpack(gc_raw)
    for name, expected in json.loads(gc['manifest.json'])['filesSHA256'].items():
        assert sha(gc[name]) == expected
    observation, linkage = json.loads(gc['raw/observation.json']), json.loads(gc['linkage.json'])
    assert observation['targetPID'] == linkage['targetPID'] == 11603
    assert int(observation['targetStartTicks']) == linkage['targetStartTicks'] == 2689930714
    assert observation['targetCommand'][-1] == launch['output'] + '/spacegroup_226_spinless/driver.g'
    assert linkage['sourceSHA256'] == source['sha256']
    assert linkage['directPerfWindowSeconds'] == 5 and linkage['perfSamples'] == 244
    assert linkage['monitoringIntervalSeconds'] == 198.180428
    return {'verified': True, 'originalFiles': len(capture['files']), 'sourceFilesCheckedAgainstGit': len(source['files']),
            'failedCase': 'spacegroup_226_spinless', 'failedCaseHasNative': False,
            'failedCaseAccepted': False, 'originalParentAccepted': False,
            'ordinary230BytesEqualApprovedSingleton': True, 'GCAndMonitoringEvidenceLinked': True}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path,
                        default=next((p for p in BASE.parents if (p / '.git').exists()), Path.cwd()))
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve()), indent=2, sort_keys=True))
