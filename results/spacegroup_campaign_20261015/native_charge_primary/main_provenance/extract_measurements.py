#!/usr/bin/env python3
"""Extract measured main-branch run metadata, keeping physical spins separate."""
from pathlib import Path
import argparse
import hashlib
import json


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--main', type=Path, required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    args.output.mkdir(parents=True, exist_ok=True)
    flag_names = ('canonicalFaceCache', 'cfPrimaryEvaluation', 'mcPrimaryEvaluation',
                  'majoranaN0Kernel', 'fermionN0Kernel', 'pureCFSource3Kernel',
                  'n0Source3Kernel', 'closedCFSource', 'formulaIntegerVectorCache',
                  'formulaIntegerVectorCacheHits', 'formulaIntegerVectorCacheLookups',
                  'partialMajoranaCache', 'f2ParityFilter', 'vacuumMajoranaKernel',
                  'vacuumFermionKernel', 'certifiedCharacterMajorana',
                  'certifiedCFSquare', 'certifiedCubePrimitive',
                  'certifiedBinaryPrimitive', 'certifiedZeroLowerSources')
    driver_path = 'gap/run_full_space_group.g'
    driver = (args.main / driver_path).read_bytes()
    driver_hash = hashlib.sha256(driver).hexdigest()
    for spin, file_spin, archive in [('spinless', 'spinless', 'space_groups_spinless'),
                                     ('spin_half', 'half', 'space_groups')]:
        rows = []
        for number in (1, 14, 19, 166, 195, 214, 219):
            path = 'results/complete_formulas/raw/d3_SG%d_%s.json' % (number, file_spin)
            data = (args.main / path).read_bytes()
            record = json.loads(data)
            rows.append({'spaceGroup': number, 'physicalSpin': spin,
                         'path': path, 'fileSHA256': hashlib.sha256(data).hexdigest(),
                         'sourceID': record['source_id'], 'wallSeconds': record['wall_seconds'],
                         'gapCPUMilliseconds': record['cpuMs'], 'scope': record['scope'],
                         'status': record['status'], 'resolutionDimensions': record['resolutionDimensions'],
                         'formulaCoordinates': record['formulaCoordinates'],
                         'driverHashMatchesCurrentMain': record['source_sha256'][driver_path] == driver_hash,
                         'recordedFlags': {key: record[key] for key in flag_names if key in record},
                         'unrecordedFlags': [key for key in flag_names if key not in record],
                         'nativeLibrarySHA256': record['source_sha256'].get('fspt/full_formula/native.so')})
        payload = {'scope': 'Measured retained complete-formula runs; hardware and source versions vary. No U1 speed ratio.',
                   'physicalSpin': spin, 'driver': {'path': driver_path, 'sha256': driver_hash,
                     'mod2Contraction': 'AFS_USE_MOD2_CONTRACTION:=true' in driver.decode().replace(' ', ''),
                     'mod2Bar': 'AFS_USE_MOD2_BAR:=true' in driver.decode().replace(' ', '')},
                   'rows': rows}
        (args.output / ('complete_publication_' + spin + '.json')).write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')
        path = 'results/' + archive + '/performance.json'
        data = (args.main / path).read_bytes()
        record = json.loads(data)
        payload = {'physicalSpin': spin, 'path': path, 'fileSHA256': hashlib.sha256(data).hexdigest(),
                   'campaign': record.get('campaign', 'UNRECORDED in this file'), 'sourceID': record['source_id'],
                   'complete': record['complete'], 'expectedGroups': record.get('expected_groups', 'UNRECORDED in this file'),
                   'scope': record['scope'], 'observer': record['observer'], 'totals': record['totals'],
                   'maxSingleTaskRSS': record['max_single_task_rss'],
                   'markedWitnessScope': {key: record[key] for key in ('unique_full_groups', 'groups_with_complete_marked_evidence', 'unresolved_upper_families') if key in record},
                   'selectedMeasurements': [row for row in record['group_measurements'] if row['space_group'] in (1, 14, 19, 166, 195, 214, 219)]}
        (args.output / ('earlier_archive_' + spin + '.json')).write_text(json.dumps(payload, indent=2, sort_keys=True) + '\n')


if __name__ == '__main__':
    main()
