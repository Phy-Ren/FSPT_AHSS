#!/usr/bin/env python3
"""Validate saved example metadata, hashes and exact input coverage without GAP."""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
PREFIX = 'results/computed_examples/'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def canonical(value):
    return json.dumps(value,sort_keys=True,separators=(',',':')).encode()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--repository-root',type=Path,default=HERE.parents[1],
                    help='Repository containing the unchanged earlier complete-result release.')
    args = ap.parse_args()
    def path(name):
        p = Path(name)
        assert not p.is_absolute() and '..' not in p.parts,name
        return HERE / name[len(PREFIX):] if name.startswith(PREFIX) else args.repository_root / p
    def read(name):
        return json.loads(path(name).read_text())
    index = json.loads((HERE/'index.json').read_text())
    records = index['cases']
    assert index['record_count']==len(records)==len({r['id'] for r in records})
    keys = defaultdict(list)
    artifacts = Counter()
    for r in records:
        rp = path(r['result'])
        b = rp.read_bytes()
        assert digest(b)==r['sha256'],r['id']
        saved = json.loads(b)
        assert saved['status']=='computed'
        assert saved['model']==r['model'] and saved['dimension']==r['dimension']
        assert saved['invariants']==r['invariant_factors']
        assert r['final_filtration'][-1]['subgroup_invariants']==r['invariant_factors']
        artifacts[r['artifact_kind']]+=1
        if r['artifact_kind']=='accepted-scientific-summary':
            assert saved['artifact_kind']==r['artifact_kind']
            assert saved['final_filtration']==r['final_filtration']
            assert saved['source_id']==r['source_id']
            assert saved['acceptance']['complete_classification_and_stacking'] is True
        if r.get('input_catalog'):
            models = read(r['input_catalog'])['models']
            assert len(models)==1
            m = models[0]
            assert m==saved['inputModel']
            assert m['id']==r['model']
            assert digest(json.dumps(m,sort_keys=True).encode())==r['input_model_sha256']
            exact = {k:m[k] for k in ('order','productTable','s1','omega2')}
            h = digest(canonical(exact))
            assert h==r['exact_input_sha256']
            expected = f"d{r['dimension']}:finite:{h}"
            if r.get('abstract_chiral_completion'):
                expected += ':zero-chiral-fiber'
            assert expected==r['deduplication_key']
        keys[r['deduplication_key']].append(r['id'])
    assert len(keys)==index['exact_input_and_scope_count']
    lookup = {r['id']:r for r in records}
    for k,ids in keys.items():
        assert len({canonical(lookup[i]['invariant_factors']) for i in ids})==1
        for identifier in ids:
            assert lookup[identifier]['exact_input_alias_records']==sorted(ids)
    pending = json.loads((HERE/'pending.json').read_text())['cases']
    for r in pending:
        assert r['id'] not in lookup and 'invariant_factors' not in r
        assert r['status']=='pending-full-acceptance'
        m = read(r['input_catalog'])['models'][0]
        assert m['id']==r['model']
        assert digest(canonical({k:m[k] for k in ('order','productTable','s1','omega2')}))==r['exact_input_sha256']
    coverage = json.loads((HERE/'coverage.json').read_text())
    assert coverage['accepted_named_records']==len(records)
    assert coverage['prior_finite_examples_unmatched']==0
    for row in coverage['historical_finite_example_aliases']:
        assert row['current_records']
        for identifier in row['current_records']:
            assert lookup[identifier]['dimension']==row['dimension']
            assert lookup[identifier]['exact_input_sha256']==row['exact_input_sha256']
    print(json.dumps(dict(status='passed',records=len(records),exact_input_and_scope_keys=len(keys),
        artifacts=dict(artifacts),pending=len(pending),historical_finite_records_covered=len(coverage['historical_finite_example_aliases']),
        scope='Saved metadata, exact input equality, hashes and aliases only; no cochain or presentation arithmetic replay.'),sort_keys=True))


if __name__=='__main__':
    main()
