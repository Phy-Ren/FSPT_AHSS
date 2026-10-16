#!/usr/bin/env python3
"""Verify the completed unchanged-H SG226 spinless parent and full E8 result offline."""
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import runpy
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


def verify(repository, validator_root=None):
    manifest = read(BASE / 'manifest.json')
    names = {str(p.relative_to(BASE)) for p in BASE.rglob('*')
             if p.is_file() and p != BASE / 'manifest.json' and '__pycache__' not in p.parts}
    assert names == set(manifest['filesSHA256'])
    for name, expected in manifest['filesSHA256'].items():
        assert sha((BASE / name).read_bytes()) == expected, name
    proof, final, download = [read(BASE / name) for name in
                              ('provenance.json', 'finalization.json', 'download_verification.json')]
    tag, node, count = proof['tag'], proof['node'], proof['count']
    for name, expected in proof['retainedDownloadFilesSHA256'].items():
        assert sha((BASE / name).read_bytes()) == expected
    assert final['tag'] == tag and final['node'] == node and final['state'] == 'complete'
    assert final['selectedCount'] == final['acceptedCount'] == count == 1
    assert final['sourceVerified'] is True and final['runtimeVerified'] is True
    assert final['sourceSHA256'] == proof['ciSourceSHA256']
    assert final['source'] == '/home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-h'
    assert final['postprocessor'] == '/home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-g'
    archive = (BASE / 'raw.tar.gz').read_bytes()
    assert sha(archive) == final['archiveSHA256'] == download['archiveSHA256']
    assert len(archive) == final['archiveBytes'] == download['archiveBytes']
    assert download['finalizationSHA256'] == sha((BASE / 'finalization.json').read_bytes())
    for key in ('requiredCompleteBeforeDownload', 'finalizationUnchangedAcrossDownload',
                'archiveMemberSafetyVerified', 'originalFilesUnchanged', 'frozenCollectorExactReplay'):
        assert download[key] is True
    assert download['frozenCollectorExitCode'] == 0 and download['acceptedCount'] == count
    assert download['frozenCollectorCommit'] == proof['postprocessorCommit']
    raw = {}
    with tarfile.open(fileobj=io.BytesIO(archive), mode='r:gz') as tar:
        seen = set()
        for member in tar.getmembers():
            path = Path(member.name)
            assert not path.is_absolute() and '..' not in path.parts
            assert member.name not in seen and (member.isfile() or member.isdir())
            seen.add(member.name)
            if member.isfile():
                raw[member.name] = tar.extractfile(member).read()
    assert set(raw) == set(download['originalFilesSHA256'])
    for name, expected in download['originalFilesSHA256'].items():
        assert sha(raw[name]) == expected, name
    j = lambda name: json.loads(raw[name])
    source, e8_source = j(tag + '/source.json'), j(tag + '-e8/source.json')
    assert source['sha256'] == proof['ciSourceSHA256']
    assert e8_source['sha256'] == proof['e8SourceSHA256']
    source_files = 0
    for metadata, commit in [(source, proof['ciCommit']), (e8_source, proof['postprocessorCommit'])]:
        assert sha(canonical(metadata['files'])) == metadata['sha256']
        for name, expected in metadata['files'].items():
            assert sha(subprocess.check_output(['git', 'show', commit + ':' + name], cwd=repository)) == expected
            source_files += 1
    launch = read(BASE / 'launch.json')
    finalizer = read(BASE / 'finalizer_launch.json')
    expected_raw = gzip.decompress((BASE / 'expected.json.gz').read_bytes())
    assert sha(expected_raw) == proof['expectedOriginalSHA256']
    expected = json.loads(expected_raw)['sourceH']
    capture_raw = gzip.decompress((BASE / 'launch_verification.json.gz').read_bytes())
    assert sha(capture_raw) == proof['launchVerificationOriginalSHA256']
    captured = json.loads(capture_raw)
    remote_prefix = '/home/user/xyren/AllFSPT_insulator/runs/'
    for name, original in [('launch.json', tag + '-launch.json'),
                           ('finalizer_launch.json', tag + '-finalizer-launch.json'),
                           ('admission.json', 'sg226-dual-shadow-admission-20261015.json')]:
        item = captured['files'][remote_prefix + original]
        assert read(BASE / name) == item['value']
        assert sha((BASE / name).read_bytes()) == item['sha256']
    admission = read(BASE / 'admission.json')
    assert admission['expectedSHA256'] == sha(expected_raw)
    assert launch['admissionSHA256'] == sha((BASE / 'admission.json').read_bytes())
    assert launch['pid'] == final['runnerPID'] == finalizer['runnerPID']
    assert launch['finalizerPID'] == finalizer['pid'] and launch['node'] == finalizer['node'] == node
    assert launch['sourceTag'] == finalizer['sourceTag'] == 'sgfull-20261015-h'
    assert launch['role'] == 'unchanged_h' and launch['sourceVerifiedBeforeLaunch'] is True
    assert launch['acceptanceFinalizerStarted'] is True and launch['eligibleAfterOrdinaryAcceptance'] is True
    assert launch['source'] == source == expected['source']
    assert expected['sourceCommit'] == proof['ciCommit']
    runtime = j(tag + '/formula_runtime.json')
    assert runtime == expected['formulaRuntime'] and runtime['libraryPresent'] is True
    assert runtime['librarySHA256'] == proof['sharedFormulaVMSHA256'] == launch['formulaVM']['sha256']
    assert runtime['libraryPath'] == launch['formulaVM']['path'] == final['source'] + '/insulator/_compiled/u1_dag_vm.so'
    for name in ('source.json', 'selection.json', 'formula_runtime.json'):
        item = captured['files'][remote_prefix + tag + '/' + name]
        assert item['value'] == j(tag + '/' + name) and item['sha256'] == sha(raw[tag + '/' + name])
    selected = j(tag + '/selection.json')
    assert len(selected) == len(set(selected)) == count
    assert selected == ['spacegroup_226_spinless'] == j(tag + '-e8/selection.json')
    assert sha(raw[tag + '/selection.json']) == final['selectionSHA256'] == e8_source['ciSelectionSHA256']
    assert launch['paired'] is False and launch['jobs'] == count
    assert launch['memoryPerJob'] == '32g' and launch['timeoutSecondsPerCase'] == 14400
    assert launch['gapBinarySHA256'] == expected['gapBinarySHA256']
    assert finalizer['finalizerSHA256'] == expected['finalizerSHA256']
    role = captured['roles']['unchanged_h']
    assert role == {'VMVerified': True, 'inputVerified': True, 'sourceFilesVerified': 60,
                    'sourceSHA256': source['sha256']}
    additional = read(BASE / 'additional_source_check.json')
    assert sha((BASE / 'original_verify_downloaded_h.py').read_bytes()) == proof['additionalSourceVerifierSHA256']
    assert additional['status'] == 'PASS' and additional['acceptedOrdinaryHShadow'] is True
    assert additional['archiveSHA256'] == final['archiveSHA256']
    assert sha((BASE / 'integer_checks.py').read_bytes()) == proof['integerCheckerSHA256']
    independent = runpy.run_path(str(BASE / 'integer_checks.py'))
    scientific, group = independent['scientific'], independent['group']
    checks, ci_records, e8_records = {}, {}, {}
    for case in selected:
        cp, ep = tag + '/' + case + '/', tag + '-e8/' + case + '/'
        data, run, native, ci = [j(cp + name) for name in ('input.json', 'run.json', 'native.json', 'result.json')]
        assert ci == {'input': data, 'run': run, 'classification': native}
        assert run['status'] == 'complete' and type(run['exitCode']) is int and run['exitCode'] == 0 and run['id'] == data['id'] == case
        assert run['sourceSHA256'] == source['sha256']
        assert not run.get('pairedSpins') and not any(key.startswith('batch') for key in run)
        assert run['timeoutSeconds'] == 14400 and run['host'] == 'n08.local'
        initial = captured['files'][remote_prefix + tag + '/' + case + '/run.json']['value']
        assert initial['status'] == 'running'
        assert {k: v for k, v in run.items() if k not in ('elapsedSeconds', 'exitCode', 'status')} == {
            k: v for k, v in initial.items() if k != 'status'}
        assert additional['nativeSHA256'] == sha(raw[cp + 'native.json'])
        assert additional['resultSHA256'] == sha(raw[cp + 'result.json'])
        assert run['command'][-1] == remote_prefix + tag + '/' + case + '/driver.g'
        assert run['command'][run['command'].index('-K') + 1] == '32g'
        assert run['inputSHA256'] == sha(raw[cp + 'input.json']) == launch['inputSHA256'][case]
        assert sha(raw[cp + 'input.json']) == expected['inputSHA256'][case]
        assert raw[cp + 'input.json'] == subprocess.check_output(
            ['git', 'show', proof['ciCommit'] + ':insulator_catalog/generated/' + case + '.json'], cwd=repository)
        checks[case] = scientific(native)
        e8, erun = j(ep + 'result.json'), j(ep + 'run.json')
        assert e8['run'] == erun and e8['input'] == data == j(ep + 'input.json')
        assert raw[ep + 'input.json'] == raw[cp + 'input.json']
        assert raw[ep + 'ci_result.json'] == raw[cp + 'result.json']
        assert erun['status'] == 'complete' and erun['exitCode'] == 0 and erun['id'] == case
        assert erun['ciResultSHA256'] == sha(raw[cp + 'result.json'])
        assert erun['ciSourceSHA256'] == source['sha256'] and erun['ciRun'] == run
        assert erun['inputSHA256'] == sha(raw[ep + 'input.json']) and erun['sourceSHA256'] == e8_source['sha256']
        c = e8['classification']
        assert c['ciSector'] == native and c['physicalClassificationCertified'] is False
        assert c['neutralE8Included'] is True and c['orderedFields'] == ['e_1', 'n_1', 'n_3', 'nu_4']
        assert group(c['presentation'], c['presentationGeneratorCount']) == {key: c[key] for key in ('freeRank', 'torsion')}
        h1 = c['e8H1']
        assert group(h1['presentation'], h1['generatorCount']) == {key: h1[key] for key in ('freeRank', 'torsion')}
        offset, ci_count = h1['generatorCount'], native['presentationGeneratorCount']
        assert c['presentationGeneratorCount'] == offset + ci_count == len(c['generators'])
        assert c['presentation'] == ([row + [0] * ci_count for row in h1['presentation']]
                                     + [[0] * offset + row for row in native['presentation']])
        assert c['generators'][:offset] == h1['roots']
        for index, generator in enumerate(c['generators'][offset:]):
            assert generator == {'kind': 'embedded-CI-root', 'ciGeneratorIndex': index,
                                 'combinedGeneratorIndex': offset + index, 'e1': 0,
                                 'completedCIRoot': native['generators'][index]}
        for key in ('fullAffinePresentationUsed', 'principalCoboundaryVerified', 'saturatedIntegerKernel'):
            assert h1['certificate'][key] is True
        assert h1['certificate']['holonomySubstitutionUsedForCohomology'] is False
        assert h1['certificate']['primitiveTranslationWordsVerified'] == 3
        ci_records[case], e8_records[case] = ci, e8
    accepted_prefix = tag + '-accepted/'
    collection = j(accepted_prefix + 'collection.json')
    assert collection['accepted'] is True and len(collection['collections']) == 1
    row = collection['collections'][0]
    assert (row['family'], row['path'], row['count']) == ('spacegroup', '3p1d/space_groups', count)
    prefix = accepted_prefix + row['path'] + '/'
    for name, expected in row['filesSHA256'].items():
        assert sha(raw[prefix + name]) == expected
    validation = j(prefix + 'validation.json')
    assert validation['accepted'] is True and validation['completeResultCount'] == count
    assert set(validation['selectedCases']) == set(selected) and not validation['missingOrFailedSelectedCases']
    assert {x['input']['id']: x for x in j(prefix + 'ci_results.json')} == ci_records
    assert {x['input']['id']: x for x in j(prefix + 'results.json')} == e8_records
    origins = j(prefix + 'provenance.json')
    assert len(origins) == 2 and {origin['kind'] for origin in origins} == {'ci', 'e8'}
    for origin in origins:
        original_tag = tag if origin['kind'] == 'ci' else tag + '-e8'
        assert set(origin['selection']) == set(selected)
        assert origin['selectionSHA256'] == sha(raw[original_tag + '/selection.json'])
        assert origin['source'] == j(original_tag + '/source.json')
        assert set(origin['resultHashes']) == set(selected)
        for case, expected in origin['resultHashes'].items():
            assert sha(raw[original_tag + '/' + case + '/result.json']) == expected
    assert sha(subprocess.check_output(['git', 'show', proof['postprocessorCommit'] + ':scripts/collect_expansion.py'],
                                       cwd=repository)) == collection['collectorSHA256']
    if (BASE / 'frozen_replay.json').exists():
        replay = read(BASE / 'frozen_replay.json')
        assert replay['exitCode'] == 0 and replay['frozenCollectorExactReplay'] is True
        assert replay['neutralSectionRecomputed'] is True and replay['CIClassificationRecomputed'] is False
        assert replay['logSHA256'] == sha((BASE / 'frozen_replay.log').read_bytes())
        assert replay['verifierSHA256'] == sha((BASE / 'verify.py').read_bytes())
        assert replay['collectorSHA256'] == collection['collectorSHA256']
    readiness = read(BASE / 'readiness_validation.json')
    assert sha((BASE / 'readiness_validator.py').read_bytes()) == readiness['validatorSHA256'] == proof['readinessValidatorSHA256']
    assert readiness['parent']['state'] == 'validated' and set(readiness['parent']['cases']) == set(selected)
    assert readiness['download']['archiveSHA256'] == final['archiveSHA256']
    assert len(readiness['parent']['scientificChecks']) == count
    for recorded in readiness['parent']['scientificChecks']:
        assert all(checks[recorded['id']][key] == value for key, value in recorded.items() if key != 'id')
    if validator_root is not None:
        validator_root = Path(validator_root).resolve()
        assert sha((validator_root / 'scripts/collect_expansion.py').read_bytes()) == collection['collectorSHA256']
        for name, expected in e8_source['files'].items():
            assert sha((validator_root / name).read_bytes()) == expected, name
        with tempfile.TemporaryDirectory(prefix='u1-h226-replay-') as tmp:
            temp = Path(tmp)
            for name, value in raw.items():
                path = temp / name
                path.parent.mkdir(parents=True, exist_ok=True)
                path.write_bytes(value)
            output = temp / 'rechecked'
            subprocess.run([sys.executable, str(validator_root / 'scripts/collect_expansion.py'),
                            '--ci-root', str(temp / tag), '--e8-root', str(temp / (tag + '-e8')),
                            '--output', str(output)], check=True)
            for name in ('results.json', 'ci_results.json', 'validation.json'):
                assert sha((output / row['path'] / name).read_bytes()) == row['filesSHA256'][name]
            # Recompute only the exact neutral section and its block presentation.
            # The CI cochain classification remains the unchanged saved parent.
            program = ('import json,sys; from pathlib import Path; sys.dont_write_bytecode=True; '
                       'sys.path.insert(0,sys.argv[1]); '
                       'from insulator.e8_spacegroup import extend_spacegroup_classification as extend; '
                       'root=Path(sys.argv[2]); tag=sys.argv[3]; '
                       'ids=json.loads((root/tag/"selection.json").read_bytes()); '
                       'pairs=[(json.loads((root/tag/k/"result.json").read_bytes()), '
                       'json.loads((root/(tag+"-e8")/k/"result.json").read_bytes())) for k in ids]; '
                       'assert all(extend(ci)==e["classification"] for ci,e in pairs); '
                       'print("Frozen neutral-section recomputation PASS:",len(ids))')
            subprocess.run([sys.executable, '-c', program, str(validator_root), str(temp), tag], check=True)
            assert all(sha((temp / name).read_bytes()) == digest for name, digest in download['originalFilesSHA256'].items())
    return {'verified': True, 'node': node, 'acceptedCount': count,
            'archiveSHA256': final['archiveSHA256'], 'rawFiles': len(raw),
            'sourceFilesCheckedAgainstGit': source_files,
            'independentScientificChecks': len(checks),
            'group': {'freeRank': c['freeRank'], 'torsion': c['torsion']},
            'exactCIParentBytesVerified': True, 'ordinaryCompletionOnly': True,
            'frozenCollectorAndNeutralSectionRepeated': validator_root is not None,
            'CIClassificationRecomputed': False, 'physicalClassificationCertified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path,
                        default=next((p for p in BASE.parents if (p / '.git').exists()), Path.cwd()))
    parser.add_argument('--validator-root', type=Path, help='Optional exact frozen c07c6e5 collector/neutral-section checkout')
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve(), args.validator_root), indent=2, sort_keys=True))
