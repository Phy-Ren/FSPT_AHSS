#!/usr/bin/env python3
"""Check unchanged SG19 source and exact outputs across the two GAP builds."""
from __future__ import annotations
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    rows = []
    for spin in ('spin_half', 'spinless'):
        name = f'spacegroup_019_{spin}'
        paths = [ROOT / tag / name / 'result.json' for tag in ('cluster_c', 'cluster_d')]
        old, new = [json.loads(path.read_text()) for path in paths]
        assert old['input'] == new['input']
        assert old['run']['sourceSHA256'] == new['run']['sourceSHA256']
        assert old['run']['host'] == new['run']['host'] == 'n02.local'
        for result in (old, new):
            assert result['run']['status'] == 'complete'
            assert result['run']['exitCode'] == result['run']['batchExitCode'] == 0
        a, b = old['classification'], new['classification']
        assert a.keys() == b.keys()
        fields = [key for key in a if key != 'resolutionBuildTimings']
        for key in fields:
            assert a[key] == b[key], (name, key)
        assert a['nativeChainIdentitiesVerified'] is True
        assert a['spaceGroupFilling']['fillingStep'] == 4
        rows.append({'id': name, 'status': 'exact_match',
                     'originalResultSHA256': digest(paths[0]),
                     'optimizedResultSHA256': digest(paths[1]),
                     'sourceSHA256': old['run']['sourceSHA256'],
                     'exactMatchingClassificationFields': fields,
                     'originalElapsedSeconds': old['run']['elapsedSeconds'],
                     'optimizedElapsedSeconds': new['run']['elapsedSeconds'],
                     'originalBatchElapsedSeconds': old['run']['batchElapsedSeconds'],
                     'optimizedBatchElapsedSeconds': new['run']['batchElapsedSeconds'],
                     'observedCaseTimeRatio': old['run']['elapsedSeconds'] / new['run']['elapsedSeconds']})
    result = {'status': 'both_exact_matches', 'rows': rows,
              'observedPairBatchTimeRatio': max(row['originalBatchElapsedSeconds'] for row in rows) / max(row['optimizedBatchElapsedSeconds'] for row in rows),
              'observedSummedCaseTimeRatio': sum(row['originalElapsedSeconds'] for row in rows) / sum(row['optimizedElapsedSeconds'] for row in rows),
              'host': 'n02.local',
              'sourceCommit': '80d565de744bbd5ef6ac4cca3530511f549547f4',
              'optimizedBinarySHA256': '873e902ee797706160601846c1ad6582c05e0aebd069bdd7efcff3d081f96fea',
              'timingScope': 'Same source, node, package tree, spin order and paired-run policy; different GAP kernel build. Campaigns overlap under production-B load but are not simultaneous isolated microbenchmarks. Batch timings include final worker shutdown and process exit; case intervals end at saved native-file modification times.'}
    (ROOT / 'cluster_cd_comparison.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(json.dumps({key: value for key, value in result.items() if key != 'rows'}, indent=2))


if __name__ == '__main__':
    main()
