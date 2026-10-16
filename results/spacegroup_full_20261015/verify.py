#!/usr/bin/env python3
"""Offline arithmetic and saved-certificate audit of the exact 230 x 2 catalogue.

Needs Python, SymPy and the pinned helper files in this repository. Historical
cluster/download paths are evidence strings, never live filesystem dependencies.
Does not rerun nonlinear CI classification or external recovery-ledger acceptance.
"""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def read(path):
    return json.loads(path.read_bytes())


def canonical(value):
    return json.dumps(value, sort_keys=True, separators=(',', ':')).encode()


def original_record_bytes(record):
    # The source result writers used this exact serialization; all 920 hashes
    # must agree with the recorded original artifact hashes, not only JSON values.
    return (json.dumps(record, sort_keys=True, indent=2) + '\n').encode()


def indexed(rows, key):
    result = {key(row): row for row in rows}
    assert len(result) == len(rows), 'Duplicate record keys'
    return result


def verify(repository):
    manifest = read(BASE / 'manifest.json')
    files = {str(p.relative_to(BASE)) for p in BASE.rglob('*')
             if p.is_file() and p != BASE / 'manifest.json' and '__pycache__' not in p.parts}
    assert files == set(manifest['filesSHA256'])
    for name, expected in manifest['filesSHA256'].items():
        assert sha(BASE / name) == expected, name
    audit = BASE / 'provenance/assembly'
    original_manifest = read(audit / 'artifact_manifest.json')['files']
    assert set(original_manifest) == {'assembly.json', 'input_manifest.json',
                                      'selection_plan.json', 'collector.stdout.log', 'collector.stderr.log'}
    for name, expected in original_manifest.items():
        assert sha(audit / name) == expected
    assembly = read(audit / 'assembly.json')
    assert assembly['accepted'] is True and assembly['preflightPassed'] is True
    assert assembly['expectedCount'] == assembly['selectedCount'] == 460
    assert assembly['allowRecovered'] is True
    assert sha(BASE / 'provenance/assemble_full460.py') == assembly['assemblerSHA256']
    assert sha(audit / 'input_manifest.json') == assembly['manifestSHA256']
    assert sha(audit / 'selection_plan.json') == assembly['selectionPlanSHA256']
    assert sha(BASE / 'collection.json') == assembly['collectionSHA256']
    for name, expected in assembly['validationSourceSHA256'].items():
        assert sha(repository / name) == expected, 'Pinned helper differs: ' + name
    sys.path.insert(0, str(repository))
    from scripts.collect_expansion import presentation_check
    from scripts.recover_paired_campaign import scientific_checks
    from insulator.e8_pointgroup import presentation_invariants
    from insulator.e8_spacegroup import spacegroup_h1

    expected_ids = {'spacegroup_%03d_%s' % (n, spin)
                    for n in range(1, 231) for spin in ('spinless', 'spin_half')}
    assert set(assembly['selectedCases']) == expected_ids and len(assembly['selectedCases']) == 460
    assert set(assembly['exactCatalogInputSHA256']) == expected_ids
    catalog = repository / 'insulator_catalog/generated'
    assert {p.stem for p in catalog.glob('spacegroup_*_spin*.json')} == expected_ids
    collection = read(BASE / 'collection.json')
    assert collection['accepted'] is True and len(collection['collections']) == 1
    row = collection['collections'][0]
    assert (row['family'], row['path'], row['count']) == ('spacegroup', '3p1d/space_groups', 460)
    assert row['filesSHA256'] == assembly['acceptedFilesSHA256']
    assert collection['collectorSHA256'] == assembly['validationSourceSHA256']['scripts/collect_expansion.py']
    assert collection['integerKernelRuntimeSHA256'] == assembly['validationSourceSHA256']['insulator/e8_h1.py']
    assert collection['smithRuntimeSHA256'] == assembly['validationSourceSHA256']['insulator/e8_pointgroup.py']
    folder = BASE / row['path']
    for name, expected in row['filesSHA256'].items():
        assert sha(folder / name) == expected
    ci = indexed(read(folder / 'ci_results.json'), lambda x: x['input']['id'])
    e8 = indexed(read(folder / 'results.json'), lambda x: x['input']['id'])
    assert set(ci) == set(e8) == expected_ids
    validation = read(folder / 'validation.json')
    assert validation['accepted'] is True and validation['completeResultCount'] == 460
    assert set(validation['selectedCases']) == expected_ids and len(validation['selectedCases']) == 460
    assert not validation['missingOrFailedSelectedCases']
    checks = indexed(validation['checks'], lambda x: (x['kind'], x['id']))
    assert set(checks) == {(kind, case) for kind in ('ci', 'e8') for case in expected_ids}
    native_checks = indexed(assembly['nativeChecks'], lambda x: x['id'])
    assert set(native_checks) == expected_ids

    origins = read(folder / 'provenance.json')
    plan = read(audit / 'selection_plan.json')
    campaigns = assembly['campaigns']
    entries = read(audit / 'input_manifest.json')['campaigns']
    assert len(origins) == len(plan) == 2 * len(campaigns) == 30
    assert len(entries) == len(campaigns)
    seen = set()
    source_for_case = {}
    result_hashes = {}
    for campaign_index, (entry, campaign) in enumerate(zip(entries, campaigns)):
        selected = campaign['selectedCases']
        assert selected and len(set(selected)) == len(selected) and not seen.intersection(selected)
        seen.update(selected)
        assert entry['ci'] == campaign['ciRoot'] and entry['e8'] == campaign['e8Root']
        assert selected == entry.get('cases', sorted(campaign['originalCIProvenance']['selection']))
        for offset, kind in enumerate(('ci', 'e8')):
            index = 2 * campaign_index + offset
            origin, selected_plan = origins[index], plan[index]
            original = campaign['original' + kind.upper() + 'Provenance']
            assert selected_plan == {'kind': kind, 'root': campaign[kind + 'Root'], 'cases': selected}
            assert all(origin[k] == value for k, value in original.items() if k != 'resultHashes')
            assert origin['kind'] == kind and origin['directory'] == campaign[kind + 'Root']
            assert origin['acceptedSelection'] == origin['requestedSubset'] == selected
            assert origin['originalSelection'] == original['selection']
            assert origin['originalSelectionSHA256'] == origin['selectionSHA256'] == original['selectionSHA256']
            assert set(selected) <= set(original['selection']) == set(original['resultHashes'])
            assert len(set(original['selection'])) == len(original['selection'])
            assert origin['fullParentValidation'] == {'allSelectedParentCasesPassed': True,
                                                     'caseCount': len(original['selection'])}
            assert origin['selectionPlan']['SHA256'] == assembly['selectionPlanSHA256']
            assert origin['selectionPlan']['entryIndex'] == index
            source = origin['source']
            assert digest(canonical(source['files'])) == source['sha256']
            selected_hashes = {case: original['resultHashes'][case] for case in selected}
            assert selected_hashes == campaign['selected' + kind.upper() + 'ResultHashes'] == origin['resultHashes']
            for case in selected:
                source_for_case[kind, case] = source['sha256']
                result_hashes[kind, case] = selected_hashes[case]
    assert seen == expected_ids
    tail = read(BASE / 'provenance/tail_acceptance.json')
    assert tail['acceptedTailCount'] == 4 and tail['readOnlyValidation'] is True
    assert tail['manifestSHA256'] == assembly['manifestSHA256']
    assert tail['originalSpinlessParentAccepted'] is False
    assert tail['approvedSingleton'] == 'spacegroup_230_spinless'
    assert len(tail['parents']) == 2
    assert {case for parent in tail['parents'] for case in parent['validation']['cases']} == {
        'spacegroup_226_spin_half', 'spacegroup_230_spin_half', 'spacegroup_226_spinless'}
    assert all(parent['validation']['state'] == 'validated' for parent in tail['parents'])

    statuses, spins = Counter(), Counter()
    for case in sorted(expected_ids):
        parent, result = ci[case], e8[case]
        data = parent['input']
        raw_input = (catalog / (case + '.json')).read_bytes()
        input_hash = digest(raw_input)
        assert input_hash == assembly['exactCatalogInputSHA256'][case]
        assert json.loads(raw_input) == data == result['input']
        assert data['family'] == 'spacegroup' and data['dimension'] == 3
        assert data['translation_rank'] == 3 and data['translation_subgroup_present'] is True
        assert case == 'spacegroup_%03d_%s' % (data['catalog_number'], data['spin'])
        spins[data['spin']] += 1
        run, erun = parent['run'], result['run']
        for kind, record in (('ci', parent), ('e8', result)):
            assert record['run']['id'] == case and record['run']['inputSHA256'] == input_hash
            assert record['run']['sourceSHA256'] == source_for_case[kind, case]
            assert digest(original_record_bytes(record)) == result_hashes[kind, case]
        assert run['status'] in ('complete', 'recovered_complete')
        statuses[run['status']] += 1
        ccheck, echeck = checks['ci', case], checks['e8', case]
        assert ccheck['inputHashVerified'] is ccheck['sourceHashVerified'] is True
        assert echeck['inputHashVerified'] is echeck['sourceHashVerified'] is True
        native = parent['classification']
        scientific = scientific_checks(native, data)
        assert native_checks[case] == {'id': case, 'runStatus': run['status'], **scientific}
        assert all(ccheck[k] == value for k, value in scientific.items() if k != 'completeWitnessListsPresent')
        if run['status'] == 'complete':
            assert type(run['exitCode']) is int and run['exitCode'] == 0
            assert 'explicitRecoveryAcceptance' not in ccheck
        else:
            assert 'exitCode' not in run
            assert run['executionExitStatus'] == 'not_inferred_from_native_completion'
            assert run['operation'] == 'offline-paired-native-recovery'
            recovery = ccheck['explicitRecoveryAcceptance']
            assert recovery['cancellationReportSHA256'] == run['cancellationReportSHA256']
            for field in ('recoveredComplete', 'capturedProcessTreeStopped', 'driverCompletionMarkerVerified',
                          'originalInputSourceAndNativeBytesVerified'):
                assert recovery[field] is True
            assert all(recovery[k] == value for k, value in scientific.items())
        for layer in ('sheet', 'charge', 'phase'):
            rows = native['filtrationPresentations'][layer]
            width = len(rows[0]) if rows else len(native[layer + 'Orders'])
            actual = presentation_invariants(rows, width)
            assert {k: actual[k] for k in ('freeRank', 'torsion')} == {
                'freeRank': native['final' + layer.title() + 'FreeRank'],
                'torsion': native['final' + layer.title() + 'Orders']}
        assert erun['status'] == 'complete' and type(erun['exitCode']) is int and erun['exitCode'] == 0
        assert erun['ciRun'] == run and erun['ciSourceSHA256'] == run['sourceSHA256']
        assert erun['ciResultSHA256'] == result_hashes['ci', case] == echeck['ciParentSHA256']
        full = result['classification']
        assert full['ciSector'] == native and full['physicalClassificationCertified'] is False
        assert full['neutralE8Included'] is True and full['orderedFields'] == ['e_1', 'n_1', 'n_3', 'nu_4']
        assert presentation_check(full) == echeck['independentSmithGroup']
        h1 = full['e8H1']
        assert presentation_check(h1) == echeck['neutralSmithGroup']
        # Recompute H1 from the full affine presentation, including signed integer
        # cocycles, primitive translations and principal-gauge witnesses. This
        # function does not inspect or rewrite the original CI execution status.
        assert spacegroup_h1(data) == h1
        offset, ci_count = h1['generatorCount'], native['presentationGeneratorCount']
        assert full['presentationGeneratorCount'] == offset + ci_count == len(full['generators'])
        assert full['presentation'] == ([row + [0] * ci_count for row in h1['presentation']]
                                        + [[0] * offset + row for row in native['presentation']])
        assert full['generators'][:offset] == h1['roots']
        for i, generator in enumerate(full['generators'][offset:]):
            assert generator == {'kind': 'embedded-CI-root', 'ciGeneratorIndex': i,
                                 'combinedGeneratorIndex': offset + i, 'e1': 0,
                                 'completedCIRoot': native['generators'][i]}
    assert statuses == {'complete': 389, 'recovered_complete': 71}
    assert spins == {'spinless': 230, 'spin_half': 230}
    return {'status': 'PASS', 'acceptedCount': 460, 'spinCounts': dict(spins),
            'originalCIStatuses': dict(statuses), 'E8CompleteCount': 460,
            'sourceParentPairs': len(campaigns), 'exactOriginalResultHashesVerified': 920,
            'fullAndNeutralSmithChecks': 920, 'CISmithAndFillingChecks': 460,
            'CIFiltrationSmithChecks': 1380, 'neutralAffineH1Recomputed': 460,
            'savedNativeChainAndCompletionCertificatesChecked': 460,
            'savedRecoveryAcceptanceCertificatesChecked': 71,
            'externalRecoveryLedgersReplayed': False, 'nonlinearCICochainsRecomputed': False,
            'runStatusesModified': False, 'physicalClassificationCertified': False}


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repository', type=Path,
                        default=next((p for p in BASE.parents if (p / '.git').exists()), Path.cwd()))
    args = parser.parse_args()
    print(json.dumps(verify(args.repository.resolve()), indent=2, sort_keys=True))
