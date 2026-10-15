#!/usr/bin/env python3
"""Retain raw differences and check the explicitly stated comparison controls."""
from pathlib import Path
import copy
import hashlib
import json

ROOT = Path(__file__).resolve().parent


def load(folder, cid):
    return json.loads((ROOT / folder / cid / 'result.json').read_text())


def differences(a, b):
    return sorted(key for key in set(a) | set(b) if a.get(key) != b.get(key))


def main():
    reference = json.loads((ROOT / 'source/results/four_data_campaign_20261015/e8_results.json').read_text())
    accepted = {row['input']['id']: row for row in reference}
    serialization = {'addedSheetRelationCoordinates': 0, 'omittedZeroSheetGauge': 0}
    still_different = []
    groups = presentations = 0
    for cid, row in accepted.items():
        old = row['classification']['ciSector']
        current = load('run', cid)['classification']
        groups += (old['torsion'], old['freeRank']) == (current['torsion'], current['freeRank'])
        presentations += old['presentation'] == current['presentation']
        a = copy.deepcopy(old)
        b = {key: copy.deepcopy(current[key]) for key in a}
        assert len(a['witnesses']) == len(b['witnesses'])
        for wa, wb in zip(a['witnesses'], b['witnesses']):
            if wa.get('kind') == 'CI-root' and 'sheetCoefficients' not in wa and 'sheetCoefficients' in wb:
                expected = [0] * len(a['sheetOrders'])
                expected[wa['index'] - 1] = wa['order']
                assert wb['sheetCoefficients'] == expected
                del wb['sheetCoefficients']
                serialization['addedSheetRelationCoordinates'] += 1
        assert len(a['gaugeReductionWitnesses']) == len(b['gaugeReductionWitnesses'])
        for wa, wb in zip(a['gaugeReductionWitnesses'], b['gaugeReductionWitnesses']):
            if wa['nativeSheetParameter'] == [0] and wb['nativeSheetParameter'] == []:
                wa['nativeSheetParameter'] = []
                serialization['omittedZeroSheetGauge'] += 1
        if a != b:
            still_different.append({'id': cid, 'fields': differences(a, b)})
    assert groups == presentations == 64
    controls = []
    for cid in ('point3_30_spinless', 'point3_31_spinless'):
        paired = load('run', cid)
        standalone = load('standalone_optimized', cid)
        exact = load('standalone_reference', cid)
        paired_exact = load('paired_reference', cid)
        old_local = load('old_code_local', cid)
        checks = {
            'pairedVersusStandaloneOnlyDiffersInReuseMetadata': differences(paired['classification'], standalone['classification']) == ['pairedGeometryReuse'],
            'standaloneOptimizedVersusReferenceOnlyDiffersInPrimaryCounters': differences(standalone['classification'], exact['classification']) == ['chargePrimaryStats'],
            'pairedOptimizedVersusReferenceOnlyDiffersInPrimaryCounters': differences(paired['classification'], paired_exact['classification']) == ['chargePrimaryStats'],
            'oldLocalSourceExactlyMatchesArchivedSource': old_local['run']['sourceSHA256'] == accepted[cid]['run']['ciSourceSHA256'],
            'oldLocalInputExactlyMatchesArchivedInput': old_local['run']['inputSHA256'] == accepted[cid]['run']['inputSHA256'],
        }
        a = copy.deepcopy(old_local['classification'])
        b = {key: exact['classification'][key] for key in a}
        zero_changes = 0
        for wa, wb in zip(a['gaugeReductionWitnesses'], b['gaugeReductionWitnesses']):
            if wa['nativeSheetParameter'] == [0] and wb['nativeSheetParameter'] == []:
                wa['nativeSheetParameter'] = []
                zero_changes += 1
        checks['oldLocalVersusCurrentReferenceEqualAfterRecordedZeroGaugeSerialization'] = a == b
        assert all(checks.values())
        controls.append({'id': cid, 'checks': checks, 'zeroGaugeSerializationChanges': zero_changes,
                         'sameOldSourceLocalVersusClusterChangedFields': differences(old_local['classification'], accepted[cid]['classification']['ciSector']),
                         'oldSourceSHA256': old_local['run']['sourceSHA256']})
    report = {'status': 'PASS', 'exactFinalGroups': groups, 'exactCompletePresentations': presentations,
              'explicitSerializationRules': serialization, 'remainingRawRepresentativeDifferences': still_different,
              'controls': controls,
              'proofScope': 'The two serialization rules are proved by the saved coefficient equality and literal-zero semantics of U1Bar/U1ReduceVacuum. Raw comparison reports remain unchanged. Same-source local-versus-cluster replay identifies an environmental difference; the exact transport map was not reconstructed.',
              'files': {str(p.relative_to(ROOT)): hashlib.sha256(p.read_bytes()).hexdigest()
                        for folder in ('run', 'standalone_optimized', 'standalone_reference', 'paired_reference', 'old_code_local')
                        for p in sorted((ROOT / folder).rglob('result.json'))}}
    (ROOT / 'control_audit.json').write_text(json.dumps(report, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: report[key] for key in ('status', 'exactFinalGroups', 'exactCompletePresentations', 'explicitSerializationRules', 'remainingRawRepresentativeDifferences')}, indent=2))


if __name__ == '__main__':
    main()
