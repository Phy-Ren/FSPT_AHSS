#!/usr/bin/env python3
"""Compare every saved native CI field against the accepted E8 ciSector."""
from pathlib import Path
import hashlib
import json
import sys
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parent
REFERENCE = ROOT / 'source/results/four_data_campaign_20261015/e8_results.json'
ALLOWED_ADDED_METADATA = {'chargePrimaryStats', 'formulaCacheStats', 'formulaWorkerCalls',
                          'pairedGeometryReuse', 'resolutionBuildTimings', 'closedChargeSourceStats'}


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    selected = json.loads((ROOT / 'run/selection.json').read_text())
    references = {row['input']['id']: row for row in json.loads(REFERENCE.read_text())}
    assert len(selected) == len(set(selected)) == len(references) == 64
    assert set(selected) == set(references)
    source = json.loads((ROOT / 'run/source.json').read_text())
    assert source['sha256'] == hashlib.sha256(json.dumps(source['files'], sort_keys=True, separators=(',', ':')).encode()).hexdigest()
    for name, expected in source['files'].items():
        assert digest(ROOT / 'source' / name) == expected
    reports = {'spinless': [], 'spin_half': []}
    incomplete = []
    for cid in selected:
        path = ROOT / 'run' / cid / 'result.json'
        if not path.exists():
            status = ROOT / 'run' / cid / 'run.json'
            incomplete.append({'id': cid, 'run': json.loads(status.read_text()) if status.exists() else None})
            continue
        candidate = json.loads(path.read_text())
        reference = references[cid]
        run = candidate['run']
        old = reference['classification']['ciSector']
        new = candidate['classification']
        checks = {
            'completeExitZero': run['status'] == 'complete' and run['exitCode'] == 0,
            'sourceManifestMatches': run['sourceSHA256'] == source['sha256'],
            'inputHashVerified': run['inputSHA256'] == digest(path.parent / 'input.json'),
            'acceptedInputHashIdentical': run['inputSHA256'] == reference['run']['inputSHA256'],
            'inputExactlyIdentical': candidate['input'] == reference['input'],
            'nativeRecordIdentical': new == json.loads((path.parent / 'native.json').read_text()),
            'nativeCertificationPresent': new['nativeChainIdentitiesVerified'] is True and new['nativeCompletionChecks'] > 0,
        }
        missing = sorted(set(old) - set(new))
        changed = sorted(k for k in old if k in new and old[k] != new[k])
        added = sorted(set(new) - set(old))
        unexpected = sorted(set(added) - ALLOWED_ADDED_METADATA)
        matrix = sp.Matrix(new['presentation'])
        count = new['presentationGeneratorCount']
        if not new['presentation']:
            matrix = sp.zeros(0, count)
        checks['presentationColumnsMatch'] = matrix.cols == count == len(new['generators'])
        smith = smith_normal_form(matrix, domain=sp.ZZ)
        diagonal = [abs(int(smith[i, i])) for i in range(min(smith.shape))]
        torsion = [x for x in diagonal if x > 1]
        free = count - sum(x != 0 for x in diagonal)
        checks['independentSNFMatches'] = torsion == new['torsion'] and free == new['freeRank']
        result = {'id': cid, 'physicalSpin': candidate['input']['spin'],
                  'status': 'PASS' if all(checks.values()) and not missing and not changed and not unexpected else 'DIFFERENCE',
                  'checks': checks, 'existingFieldsCompared': sorted(old), 'missingFields': missing,
                  'changedFields': changed, 'addedMetadataFields': added, 'unexpectedAddedFields': unexpected,
                  'normalization': 'none; exact JSON value equality', 'candidateResultSHA256': digest(path),
                  'acceptedCIResultSHA256': reference['run']['ciResultSHA256'],
                  'candidateSourceSHA256': run['sourceSHA256'], 'acceptedCISourceSHA256': reference['run']['ciSourceSHA256'],
                  'elapsedSeconds': run['elapsedSeconds'], 'torsion': torsion, 'freeRank': free,
                  'nativePrimaryStats': new.get('chargePrimaryStats')}
        if changed:
            result['differences'] = {key: {'accepted': old[key], 'candidate': new[key]} for key in changed}
        reports[result['physicalSpin']].append(result)
    output = ROOT / 'comparison'
    output.mkdir(exist_ok=True)
    for spin, rows in reports.items():
        (output / (spin + '.json')).write_text(json.dumps({'physicalSpin': spin, 'rows': rows}, indent=2, sort_keys=True) + '\n')
    summary = {'status': 'PASS' if not incomplete and all(row['status'] == 'PASS' for rows in reports.values() for row in rows) else 'INCOMPLETE_OR_DIFFERENCE',
               'selected': 64, 'completed': sum(map(len, reports.values())), 'incomplete': incomplete,
               'countsBySpin': {spin: {'matched': sum(row['status'] == 'PASS' for row in rows),
                                     'different': sum(row['status'] != 'PASS' for row in rows)} for spin, rows in reports.items()},
               'reference': {'path': str(REFERENCE.relative_to(ROOT)), 'sha256': digest(REFERENCE),
                             'sector': 'classification.ciSector; E8 postprocessor not rerun'},
               'candidateSourceSHA256': source['sha256'],
               'normalization': 'none; every preexisting native field compared exactly',
               'scope': 'Same physical backgrounds and retained CI model; no new physical-completeness or literature-match claim.'}
    (output / 'summary.json').write_text(json.dumps(summary, indent=2, sort_keys=True) + '\n')
    print(json.dumps({k: summary[k] for k in ('status', 'selected', 'completed', 'countsBySpin')}, indent=2))
    return 0 if summary['status'] == 'PASS' else 1


if __name__ == '__main__':
    sys.exit(main())
