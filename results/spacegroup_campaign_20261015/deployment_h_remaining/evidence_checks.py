"""Offline launch-evidence checks; never query or signal a recorded process."""
import hashlib
import io
import json
from pathlib import Path
import subprocess
import tarfile


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def package_check(base):
    manifest = read(base / 'manifest.json')
    files = {str(p.relative_to(base)) for p in base.rglob('*')
             if p.is_file() and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    assert files == set(manifest['filesSHA256'])
    for name, value in manifest['filesSHA256'].items():
        assert sha((base / name).read_bytes()) == value, name


def archive_files(path):
    result = {}
    with tarfile.open(fileobj=io.BytesIO(path.read_bytes())) as archive:
        for member in archive.getmembers():
            name = Path(member.name)
            assert member.isfile() and not name.is_absolute() and '..' not in name.parts
            assert member.name not in result
            result[member.name] = archive.extractfile(member).read()
    return result


def source_check(base, expected):
    repo = base.parents[2]
    primary = read(base.parent / 'deployment_h/expected.json')
    assert expected['sourceCommit'] == primary['sourceCommit'] == 'ea44c1f55314ddd66587cf452bbaae9331f3a1db'
    assert expected['source'] == primary['source']
    source = expected['source']
    assert sha(json.dumps(source['files'], sort_keys=True, separators=(',', ':')).encode()) == source['sha256']
    for name, value in source['files'].items():
        assert sha(subprocess.check_output(['git', 'show', expected['sourceCommit'] + ':' + name], cwd=repo)) == value, name
    assert expected['archiveSHA256'] == primary['archiveSHA256']
    runtime = expected['formulaRuntime']
    assert runtime == read(base.parent / 'deployment_h/formula_runtime.json')
    library = read(base.parent / 'deployment_h/formula_library_verification.json')
    assert runtime['librarySHA256'] == library['actualLibrarySHA256'] == library['declaredLibrarySHA256']
    assert library['verified'] and runtime['libraryPresent'] and runtime['requestedMode'] == 'auto'
    assert expected['gapBinarySHA256'] == '873e902ee797706160601846c1ad6582c05e0aebd069bdd7efcff3d081f96fea'
    return source


def launch_check(base, files, expected, tag, node, jobs, memory, cases, paired):
    launch = json.loads(files['runs/' + tag + '-launch.json'])
    selection = json.loads(files['runs/' + tag + '/selection.json'])
    finalizer = json.loads(files['runs/' + tag + '-finalizer-launch.json'])
    state = json.loads(files['runs/' + tag + '-finalization.json'])
    assert launch['state'] == 'launched' and launch['node'] == node and launch['tag'] == tag
    assert launch['sourceVerifiedBeforeLaunch'] and launch['formulaRuntimeVerifiedBeforeLaunch']
    assert launch['campaignMetadataVerified'] and launch['source'] == expected['source']
    assert launch['sourceCommit'] == expected['sourceCommit']
    assert launch['snapshotSHA256'] == expected['archiveSHA256']
    assert launch['formulaRuntime'] == expected['formulaRuntime']
    assert launch['gapBinarySHA256'] == expected['gapBinarySHA256']
    assert launch['finalizerSHA256'] == expected['finalizerSHA256']
    assert json.loads(files['runs/' + tag + '/source.json']) == expected['source']
    assert json.loads(files['runs/' + tag + '/formula_runtime.json']) == expected['formulaRuntime']
    assert len(selection) == len(set(selection)) == len(cases) == launch['caseCount']
    assert set(selection) == set(cases) == set(launch['cases'])
    command = launch['command']
    assert ('--pair-spins' in command) == paired
    for option, value in [('--jobs', str(jobs)), ('--memory', memory), ('--timeout', '14400'),
                          ('--charge-primary', 'native'), ('--phase-class', 'cycles'),
                          ('--closed-charge-source', 'certified'), ('--vacuum-reduction', 'canonical')]:
        assert command[command.index(option) + 1] == value
    assert [command[i+1] for i, value in enumerate(command) if value == '--case'] == launch['cases']
    assert command[1].endswith('/snapshots/sgfull-20261015-h/scripts/classify.py')
    assert command[command.index('--output')+1] == launch['output']
    assert launch['timeoutSecondsPerCase'] == 14400
    if paired:
        assert launch['batchTimeoutSecondsPerGeometry'] == 28800
    else:
        assert launch['paired'] is False
    resources = launch['resourcePreflight']
    assert resources['logicalCPUs'] == 56 and resources['loadAverage'][0] + jobs < 56
    assert resources['availableEstimateGiB'] > jobs * int(memory[:-1])
    assert finalizer['runnerPID'] == launch['pid'] and finalizer['pid'] == launch['finalizerPID']
    assert finalizer['sourceTag'] == 'sgfull-20261015-h' and finalizer['node'] == node
    assert finalizer['finalizerSHA256'] == expected['finalizerSHA256']
    command = finalizer['command']
    assert int(command[command.index('--runner-pid')+1]) == launch['pid']
    assert command[command.index('--source-tag')+1] == 'sgfull-20261015-h'
    assert state['state'] == 'waiting' and state['runnerPID'] == launch['pid']
    assert state['selectionSHA256'] == sha(files['runs/' + tag + '/selection.json'])
    assert state['sourceSHA256'] == expected['source']['sha256']
    for case in cases:
        raw = subprocess.check_output(['git', 'show', expected['sourceCommit'] + ':insulator_catalog/generated/' + case + '.json'], cwd=base.parents[2])
        assert sha(raw) == launch['inputSHA256'][case], case
    return launch
