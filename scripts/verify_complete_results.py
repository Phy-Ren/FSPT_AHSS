#!/usr/bin/env python3
"""Verify the published result inventory; optionally recompute integer arithmetic."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--index', type=Path, default=ROOT/'results/complete_formulas/index.json',
                    help='Published inventory or a separately dated supplementary index.')
    ap.add_argument('--arithmetic', action='store_true', help='Independently recompute SNF and final HNF filtration (requires SymPy).')
    ap.add_argument('--case', action='append', help='Select record IDs; default is the complete inventory.')
    ap.add_argument('--output', type=Path)
    args = ap.parse_args()
    index = json.loads(args.index.read_text())
    records = index['cases']
    assert len(records) == index['record_count']
    assert len({r['id'] for r in records}) == len(records)
    counts = Counter(c for r in records for c in r['collections'])
    if args.index.resolve() == (ROOT/'results/complete_formulas/index.json').resolve():
        assert len(records) == 832
        assert counts['finite_production'] == 245 and counts['crystalline_production'] == 524
        assert counts['finite_canonical_202'] == 202
    if args.case:
        missing = set(args.case) - {r['id'] for r in records}
        if missing: ap.error('Unknown records: ' + ', '.join(sorted(missing)))
        records = [r for r in records if r['id'] in args.case]
    if args.arithmetic:
        from fspt.result_validation import verify_result
    checks = []
    for r in records:
        path = ROOT/r['result']
        payload = path.read_bytes()
        assert hashlib.sha256(payload).hexdigest() == r['sha256'], r['id']
        data = json.loads(payload)
        assert data['status'] == 'computed'
        assert data['model'] == r['model'] and data['dimension'] == r['dimension']
        assert data['invariants'] == r['invariant_factors']
        if 'input_catalog' in r:
            catalog = json.loads((ROOT/r['input_catalog']).read_text())
            assert catalog['models'] == [data['inputModel']]
        if 'expected_invariant_factors' in r:
            assert r['expected_invariant_factors'] == r['invariant_factors'], r['id']
        check = dict(id=r['id'], sha256_verified=True)
        if args.arithmetic:
            arithmetic = verify_result(data)
            if r.get('final_filtration') is not None:
                assert arithmetic['final_filtration'] == r['final_filtration'], r['id']
            check.update(arithmetic)
        checks.append(check)
    report = dict(success=True, checked=len(checks), arithmetic=args.arithmetic,
        scope='Saved bytes, input identity and completed status' + ('; independent SNF, GAP unimodular certificates and HNF filtration' if args.arithmetic else ''),
        collection_counts=dict(counts), checks=checks)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        with args.output.open('x') as f: json.dump(report, f, indent=2); f.write('\n')
    print(json.dumps({k:v for k,v in report.items() if k != 'checks'}))


if __name__ == '__main__': main()
