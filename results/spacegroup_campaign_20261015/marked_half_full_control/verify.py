#!/usr/bin/env python3
"""Portable offline source/observation/result audit; never executes a solver."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import tarfile

HERE = Path(__file__).resolve().parent
CASE = 'spacegroup_141_spin_half'
DELTA = ['gap/backend_half_phase.g', 'gap/classification.g']
EXECUTION = {'resolutionBuildTimings', 'formulaWorkerCalls', 'formulaCacheStats'}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def members(archive):
    raw = {}
    for item in archive.getmembers():
        p = PurePosixPath(item.name)
        assert not p.is_absolute() and '..' not in p.parts
        if item.isdir():
            continue
        assert item.isfile() and item.name not in raw
        raw[item.name] = archive.extractfile(item).read()
    return raw


def repository_default():
    for p in HERE.parents:
        if (p / '.git').exists():
            return p
    return Path.cwd()


def gap(value):
    if value is True:
        return 'true'
    if value is False:
        return 'false'
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=True)
    if isinstance(value, int):
        return str(value)
    if isinstance(value, list):
        return '[' + ','.join(gap(x) for x in value) + ']'
    if isinstance(value, dict):
        assert all(k.replace('_', '').isalnum() and not k[0].isdigit() for k in value)
        return 'rec(' + ','.join(k + ':=' + gap(v) for k, v in value.items()) + ')'
    raise TypeError('Unexpected exact catalogue value')


def expected_driver(snapshot, root, data, python):
    return ('U1_ROOT:=' + gap(snapshot) + ';;\n'
            + 'U1_FORMULA_PYTHON:=' + gap(python) + ';;\n'
            + 'U1_USE_KOSZUL:=true;;\n'
            + 'Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n'
            + 'U1_INPUT:=' + gap(data) + ';;\n'
            + 'c:=U1CatalogContext(U1_INPUT,6);;\n'
            + 'c.chargePrimaryMode:="native";;\n'
            + 'c.phaseClassMode:="cycles";;\n'
            + 'c.closedChargeSourceMode:="certified";;\n'
            + 'c.vacuumReductionMode:="canonical";;\n'
            + 'result:=U1Classify(c,U1_INPUT.dimension,rec(uniformIQH:=false));;\n'
            + 'output:=OutputTextFile(' + gap(root + '/' + CASE + '/native.json') + ',false);;\n'
            + 'SetPrintFormattingStatus(output,false);;\n'
            + 'PrintTo(output,U1JSON(result),"\\n");;\n'
            + 'CloseStream(output);;\nif IsBound(c.worker) then CloseStream(c.worker);fi;\nQUIT;\n').encode()


def measurements(raw):
    text = raw.decode()
    def field(label):
        found = re.search(r'^\s*' + re.escape(label) + r':\s*(.+)$', text, re.M)
        assert found, label
        return found.group(1)
    wall = 0.
    for part in field('Elapsed (wall clock) time (h:mm:ss or m:ss)').split(':'):
        wall = 60 * wall + float(part)
    out = {'wallSeconds': wall, 'userCPUSeconds': float(field('User time (seconds)')),
           'systemCPUSeconds': float(field('System time (seconds)')),
           'maximumResidentSetSizeKiB': int(field('Maximum resident set size (kbytes)')),
           'exitStatus': int(field('Exit status'))}
    out['totalCPUSeconds'] = out['userCPUSeconds'] + out['systemCPUSeconds']
    assert out['exitStatus'] == 0
    return out


def verify(repository):
    manifest = read(HERE / 'manifest.json')['files']
    actual = {str(p.relative_to(HERE)) for p in HERE.rglob('*') if p.is_file()
              and p.name != 'manifest.json' and '__pycache__' not in p.parts}
    assert set(manifest) == actual
    for name, digest in manifest.items():
        assert sha((HERE / name).read_bytes()) == digest, name
    proof = read(HERE / 'provenance.json')
    packed = (HERE / 'raw.tar.gz').read_bytes()
    assert len(packed) == proof['archiveBytes'] and sha(packed) == proof['archiveSHA256']
    with tarfile.open(fileobj=io.BytesIO(packed)) as archive:
        assert all(x.isfile() for x in archive.getmembers())
        raw = members(archive)
    assert len(raw) == 46 and {n: sha(b) for n, b in raw.items()} == proof['archiveMembers']
    load = lambda n: json.loads(raw[n])
    for name, digest in proof['originalMetadataSHA256'].items():
        assert sha((HERE / name).read_bytes()) == digest
    capture = read(HERE / 'capture_verification.json')
    original_hashes = {n: sha(b) for n, b in raw.items() if n != 'capture_remote_proof.json'}
    assert capture['status'] == 'CAPTURE_VERIFIED' and capture['files'] == original_hashes
    assert capture['archiveSHA256'] == proof['archiveSHA256'] and capture['fileCount'] == 45
    for record in [read(HERE / 'before.json'), read(HERE / 'after.json'), load('capture_remote_proof.json')]:
        assert record['files'] == original_hashes
        assert record['roles'] == read(HERE / 'before.json')['roles']
        assert record['exactSourceDifferences'] == DELTA
        assert record['diagnosticOnly'] is True and record['selectedForCatalogue'] is False
    plan = load('instrumentation/plan.json')
    pins = proof['preparedBundlePins']
    assert sha(raw['instrumentation/plan.json']) == pins['planSHA256']
    assert sha(raw['instrumentation/launch_reviewed.py']) == pins['launcherSHA256']
    assert sha(raw['instrumentation/gap_observed.py']) == pins['wrapperSHA256'] == plan['wrapperSHA256']
    assert sha(raw['instrumentation/observe_marked_hits.g']) == pins['observerSHA256'] == plan['observerSHA256']
    assert plan['baseCommit'] == proof['baselineCommit'] and plan['diagnosticOnly'] is True
    assert plan['selectedForCatalogue'] is False and plan['case'] == CASE
    assert plan['roles']['baseline']['source']['sha256'] == proof['baselineSourceSHA256']
    assert plan['roles']['candidate']['source']['sha256'] == proof['candidateSourceSHA256']
    baseline = plan['roles']['baseline']['snapshotFiles']
    archived = subprocess.check_output(['git', 'archive', proof['baselineCommit'], '--'] + sorted(baseline), cwd=repository)
    with tarfile.open(fileobj=io.BytesIO(archived), mode='r:') as archive:
        git = members(archive)
    assert set(git) == set(baseline)
    assert {n: sha(b) for n, b in git.items()} == baseline
    overlays = {n: (HERE / 'candidate_overlay' / n).read_bytes() for n in DELTA}
    assert {n: sha(b) for n, b in overlays.items()} == proof['overlaySHA256']
    freeze = read(HERE / 'prototype_freeze_manifest.json')
    assert sha((HERE / 'prototype_freeze_manifest.json').read_bytes()) == plan['ownerFreezeManifestSHA256']
    for n in DELTA:
        assert sha(overlays[n]) == freeze['files']['candidate/' + n]
    peer = read(HERE / 'marked_half_double_review_20261015.json')
    assert peer['status'] == 'PASS' and peer['sourceSHA256'] == proof['candidateSourceSHA256']
    assert peer['reviewedFilesSHA256']['freeze_manifest.json'] == plan['ownerFreezeManifestSHA256']
    assert peer['reviewedFilesSHA256']['proof.md'] == sha((HERE/'prototype_proof.md').read_bytes())
    for name in DELTA:
        assert peer['reviewedFilesSHA256']['candidate/'+name] == sha(overlays[name])
    assert proof['exactSourceDifferences'] == DELTA
    admission = load('sg141-marked-half-pair-admission-20261015.json')
    assert admission['planSHA256'] == pins['planSHA256'] and admission['launcherSHA256'] == pins['launcherSHA256']
    assert admission['signalsSent'] is False and admission['existingRunsModified'] is False
    assert admission['exactRuntimeDifferences'] == DELTA and admission['resources']['configuredCapBudgetFits'] is True
    assert admission['resources']['reservedExistingCapsGiB'] == 64 and admission['resources']['additionalCapsGiB'] == 32
    comparison = read(HERE / 'exact_comparison.json')
    assert comparison['captureVerificationSHA256'] == sha((HERE / 'capture_verification.json').read_bytes())
    native, sources, times, counts, launches = {}, {}, {}, {}, {}
    for role, spec in plan['roles'].items():
        tag = spec['tag']; prefix = tag + '/' + CASE + '/'
        sources[role] = load(tag + '/source.json')
        assert sources[role] == spec['source']
        assert sha(json.dumps(sources[role]['files'], sort_keys=True, separators=(',', ':')).encode()) == sources[role]['sha256']
        expected = dict(git)
        if role == 'candidate':
            expected.update(overlays)
        assert {n: sha(b) for n, b in expected.items()} == spec['snapshotFiles']
        for n, digest in sources[role]['files'].items():
            assert sha(expected[n]) == digest, (role, n)
        assert 'gap/backend_bar_mod2.g' not in expected
        assert sha(raw['instrumentation/' + role + '_worker_preflight.g']) == spec['workerPreflightSHA256']
        data = load(prefix + 'input.json')
        assert raw[prefix + 'input.json'] == git['insulator_catalog/generated/' + CASE + '.json']
        assert sha(raw[prefix + 'input.json']) == plan['inputSHA256']
        assert data['id'] == CASE and data['family'] == 'spacegroup' and data['dimension'] == 3
        run = load(prefix + 'run.json'); result = load(prefix + 'result.json'); native[role] = load(prefix + 'native.json')
        assert load(tag + '/selection.json') == [CASE] and load(tag + '/summary.json') == [run]
        assert run['status'] == 'complete' and type(run['exitCode']) is int and run['exitCode'] == 0
        assert result['run'] == run and result['input'] == data and result['classification'] == native[role]
        assert native[role]['nativeChainIdentitiesVerified'] is True and native[role]['nativeCompletionChecks'] > 0
        assert run['sourceSHA256'] == sources[role]['sha256'] and run['inputSHA256'] == plan['inputSHA256']
        assert run['host'].split('.')[0] == 'n08' and run['timeoutSeconds'] == 2400 and 'batchCaseIDs' not in run
        assert run['formulaWorkerPython'] == plan['workerPythonExpected']
        root = '/home/user/xyren/AllFSPT_insulator/runs/' + tag
        wrapper = plan['remoteTools'] + '/gap_observed.py'
        assert run['command'] == [wrapper, '-q', '-b', '--quitonbreak', '-m', '256m', '-K', '16g', root + '/' + CASE + '/driver.g']
        for key, value in [('chargePrimaryRequested', 'native'), ('phaseClassRequested', 'cycles'),
                           ('closedChargeSourceRequested', 'certified'), ('vacuumReductionRequested', 'canonical')]:
            assert run[key] == value
        assert raw[prefix + 'driver.g'] == expected_driver(spec['snapshot'], root, data, plan['workerPythonExpected'])
        insertion = ('Read(' + json.dumps(plan['remoteTools'] + '/observe_marked_hits.g') + ');;\n').encode()
        assert raw[prefix + 'observed_driver.g'] == raw[prefix + 'driver.g'][:-6] + insertion + b'QUIT;\n'
        binding = load(prefix + 'driver_observation.json')
        assert binding['originalSHA256'] == sha(raw[prefix + 'driver.g']) and binding['observedSHA256'] == sha(raw[prefix + 'observed_driver.g'])
        assert binding['observerSHA256'] == plan['observerSHA256'] and binding['wrapperSHA256'] == plan['wrapperSHA256']
        assert binding['exactInsertionUTF8'] == insertion.decode() and binding['terminalQUITUnchanged'] is True
        assert binding['originalBytesUnchanged'] is True and binding['solverSourcesModified'] is False
        assert binding['originalArguments'] == run['command'][1:]
        assert binding['executedArguments'] == run['command'][1:-1] + [root + '/' + CASE + '/observed_driver.g']
        observation = load(tag + '-process-observation.json')
        assert observation['actualGAP']['argv'][-len(binding['executedArguments']):] == binding['executedArguments']
        assert observation['actualGAP']['executable'] == plan['gapBinary'] and observation['actualExecutableSHA256'] == plan['gapBinarySHA256']
        assert observation['driverObservationSHA256'] == sha(raw[prefix + 'driver_observation.json'])
        assert observation['originalDriverSHA256'] == binding['originalSHA256'] and observation['executedDriverSHA256'] == binding['observedSHA256']
        assert observation['signalsSent'] is False
        launch = load(tag + '-launch.json'); finish = load(tag + '-finished.json'); launches[role] = launch
        assert launch['role'] == role and launch['tag'] == tag and launch['source'] == sources[role]
        assert launch['diagnosticOnly'] is True and launch['selectedForCatalogue'] is False
        assert type(finish['exitCode']) is int and finish['exitCode'] == 0 and all(finish[k] == v for k, v in launch.items())
        assert launch['planSHA256'] == pins['planSHA256'] and launch['admissionSHA256'] == sha(raw['sg141-marked-half-pair-admission-20261015.json'])
        assert launch['environment']['PATH'].split(':')[0] == plan['runtimeBin']
        assert launch['environment']['U1_DAG_MODE'] == 'auto'
        assert launch['workerPreflight']['returncode'] == 0 and 'U1_WORKER_PREFLIGHT_PING_PASS' in launch['workerPreflight']['stdout']
        assert launch['librarySHA256'] == plan['librarySHA256'] and launch['gapBinarySHA256'] == plan['gapBinarySHA256']
        runtime = load(tag + '/formula_runtime.json')
        assert runtime['librarySHA256'] == plan['librarySHA256'] and runtime['libraryPresent'] is True and runtime['requestedMode'] == 'auto'
        assert runtime['libraryPath'] == spec['snapshot'] + '/insulator/_compiled/u1_dag_vm.so'
        hits = re.findall(rb'^U1_MARKED_HALF_OBSERVATION hits=(\d+) counterBound=(true|false) completedCertificate=true$', raw[prefix + 'stdout.log'], re.M)
        assert len(hits) == 1
        counts[role] = int(hits[0][0])
        assert hits == [(b'0', b'false')] if role == 'baseline' else hits == [(b'6', b'true')]
        times[role] = measurements(raw[tag + '-resources.txt'])
        assert times[role] == comparison['resources'][role]
    assert launches['baseline']['pythonExecutableSHA256'] == launches['candidate']['pythonExecutableSHA256']
    assert launches['baseline']['pythonVersion'] == launches['candidate']['pythonVersion']
    changed = sorted(n for n in set(sources['baseline']['files']) | set(sources['candidate']['files'])
                     if sources['baseline']['files'].get(n) != sources['candidate']['files'].get(n))
    assert changed == DELTA
    assert set(native['baseline']) == set(native['candidate'])
    fields = sorted(set(native['baseline']) - EXECUTION)
    assert len(fields) == 35 and fields == comparison['scientificFields']
    assert all(native['baseline'][n] == native['candidate'][n] for n in fields)
    assert native['baseline']['formulaWorkerCalls'] == native['candidate']['formulaWorkerCalls'] == 64826
    assert native['baseline']['formulaCacheStats'] == native['candidate']['formulaCacheStats']
    assert comparison['status'] == 'PASS' and comparison['differingScientificFields'] == []
    assert comparison['normalizationOrBasisChangeApplied'] is False and comparison['markedHalfDoubleHits'] == counts
    for name in ['wallSeconds', 'totalCPUSeconds', 'maximumResidentSetSizeKiB']:
        assert times['candidate'][name] >= times['baseline'][name]
        assert comparison['baselineDividedByCandidate'][name] == times['baseline'][name] / times['candidate'][name]
    assert proof['productionAdopted'] is False and proof['markedSG226Launched'] is False and proof['catalogueSelectionChanged'] is False
    return {'status': 'PASS', 'archiveMembers': len(raw), 'baselineGitFiles': len(git),
            'sourceFilesPerRole': len(sources['baseline']['files']), 'exactScientificFields': len(fields),
            'markedHalfDoubleHits': counts, 'resources': times, 'wholeRunImprovement': False,
            'solverRerun': False, 'catalogueSelectionChanged': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path, default=repository_default())
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve()), indent=2, sort_keys=True))
