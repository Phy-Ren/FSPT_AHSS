"""Recheck accepted payload bytes and performance using only a portable archive."""
from datetime import datetime, timezone
import argparse
import hashlib
import json
from pathlib import Path
import sys
ROOT = next(p for p in Path(__file__).resolve().parents
            if (p/'scripts/audit_background_run.py').is_file())
sys.path.insert(0, str(ROOT/'scripts'))
from audit_background_run import check_background_result
from background_performance import collect_background_performance

def sha(raw):
    return hashlib.sha256(raw).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write', action='store_true', help='Save new audit evidence, refusing overwrite')
    args = parser.parse_args()
    if not __debug__:
        raise ValueError('Run without Python -O: strict certificate checks require assertions')
    run = ROOT/'results/space_groups_spinless'
    archive_raw = (run/'archive.json').read_bytes()
    archive = json.loads(archive_raw)
    assert archive['groups'] == list(range(1,231))
    for relative, row in archive['files'].items():
        path = Path(relative)
        assert not path.is_absolute() and '..' not in path.parts
        raw = (run/path).read_bytes()
        assert sha(raw) == row['sha256'] and len(raw) == row['bytes'], relative
    source = {str(p.relative_to(run/'source')): sha(p.read_bytes())
              for p in (run/'source/gap').glob('*.g')}
    assert source == archive['source_sha256']
    assert sha(json.dumps(source, sort_keys=True).encode()) == archive['source_id']
    audits = {n: check_background_result(json.loads((run/('sg%d.json'%n)).read_bytes()),
                 strict_background=True) for n in range(1,231)}
    assert audits == {int(k): v for k,v in archive['per_group_audits'].items()}
    collected = collect_background_performance(run, run/'tasks', audits)
    original = json.loads((run/'performance.json').read_bytes())
    old_hashes = original.pop('evidence_sha256')
    new_hashes = collected.pop('evidence_sha256')
    by_original = {row['original_path']: row for row in archive['files'].values()
                   if row['original_path'] is not None}
    translated = {str((run/by_original[p]['archive_path']).resolve()): h
                  for p,h in old_hashes.items()}
    assert translated == new_hashes
    # The producer used Python 3.8's left-to-right float sum. Python 3.12
    # changed built-in sum(float), so reproduce the original evaluation order
    # explicitly instead of accepting a tolerance or rewriting its report.
    portable_runtime_totals = dict(collected['totals'])
    def left_sum(values):
        total = 0
        for value in values:
            total += value
        return total
    rows = collected['group_measurements']
    for target, field in [('gap_total_cpu_seconds', 'gap_total_cpu_seconds'),
                          ('gap_classification_cpu_seconds', 'gap_classification_cpu_seconds')]:
        collected['totals'][target] = left_sum(row[field] for row in rows)
    collected['totals']['process_cpu_seconds'] = left_sum(
        row['gnu_time']['process_cpu_seconds'] for row in rows)
    assert original == collected
    proof = dict(schema='fspt-spinless-portable-delivery-audit-v1', complete=True,
        checked_at_utc=datetime.now(timezone.utc).isoformat(),
        archive_sha256=sha(archive_raw), source_id=archive['source_id'],
        payload_files_verified=len(archive['files']), all_230_strict_result_audits=True,
        all_archived_per_group_audits_reproduced=True,
        performance_matches_after_exact_path_translation=True,
        total_summation='explicit left-to-right binary64, matching original Python 3.8; no tolerance used',
        portable_runtime_builtin_sum_totals=portable_runtime_totals,
        reproduced_original_totals=collected['totals'],
        portable_performance_evidence_sha256={str(Path(p).relative_to(run)): h
                                             for p,h in new_hashes.items()},
        auditor_sha256={name:sha((ROOT/'scripts'/name).read_bytes()) for name in
            ('audit_background_run.py','background_performance.py','collect_performance.py')},
        verifier_sha256=sha(Path(__file__).read_bytes()),
        original_archive_or_payload_bytes_modified=False)
    out = run/'audits/portable_performance.json'
    if args.write:
        assert not out.exists()
        out.parent.mkdir(exist_ok=True)
        out.write_text(json.dumps(proof, indent=2, sort_keys=True)+'\n')
        (out.parent/'verify_spinless_delivery.py').write_bytes(Path(__file__).read_bytes())
    print(json.dumps({k:v for k,v in proof.items()
          if k not in ('portable_performance_evidence_sha256','auditor_sha256')}, indent=2))

if __name__ == '__main__':
    main()
