#!/usr/bin/env python3
"""Verify background identifications and build the current example index.

The saved calculation index stays immutable. Repeated calculations and section
choices become provenance of one reader example at a fixed dimension and scope.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]


def canonical(data):
    return json.dumps(data, sort_keys=True, separators=(',', ':')).encode()


def verify_background(source, target, witness):
    n = source['order']
    phi = [i-1 for i in witness['source_to_target_elements_one_based']]
    lam = witness['section_one_cochain']
    assert target['order'] == n and sorted(phi) == list(range(n))
    assert len(lam) == n and lam[0] == 0
    for g in range(n):
        assert source['s1'][g] == target['s1'][phi[g]]
        for h in range(n):
            gh = source['productTable'][g][h]-1
            assert phi[gh] == target['productTable'][phi[g]][phi[h]]-1
            assert source['omega2'][g][h] == (target['omega2'][phi[g]][phi[h]] ^ lam[g] ^ lam[h] ^ lam[gh])


def build():
    index = json.loads((HERE/'index.json').read_text())
    four = json.loads((HERE/'tables/internal_4d_symbolic.json').read_text())
    targets = {r['background_id']:r for r in four['records']}
    maps = {}
    for row in four['record_coverage']:
        h = row['exact_input_sha256']
        if h in maps:
            assert maps[h]['background_id'] == row['background_id']
        maps[h] = row
    groups = defaultdict(list)
    witnesses = {}
    for r in index['cases']:
        scope = 'zero-chiral-fiber' if r.get('abstract_chiral_completion') else 'full'
        if r['symmetry_kind'] == 'finite_internal':
            match = maps.get(r['exact_input_sha256'])
            if match:
                background = match['background_id']
                source = json.loads((ROOT/r['input_catalog']).read_text())['models'][0]
                verify_background(source, targets[background]['input_model'], match['background_isomorphism'])
                witnesses[r['id']] = dict(canonical_background=background,
                    background_isomorphism=match['background_isomorphism'])
            else:
                background = 'literal:' + r['exact_input_sha256']
                witnesses[r['id']] = dict(canonical_background=background,
                    background_isomorphism='identity on the saved input')
            key = f"d{r['dimension']}:finite:{background}:{scope}"
        else:
            key = r['deduplication_key']
        groups[key].append(r)
    examples = []
    for key, records in sorted(groups.items()):
        records.sort(key=lambda r:(r['id'][3:].startswith('E'), r['id']))
        r = records[0]
        filtration = lambda x: {y['layer']:y['quotient_invariants'] for y in x['final_filtration']}
        for other in records:
            assert other['invariant_factors'] == r['invariant_factors'], (r['id'], other['id'])
            assert filtration(other) == filtration(r), (r['id'], other['id'])
        examples.append(dict(example_key=key, representative_record=r['id'],
            calculation_records=[x['id'] for x in records], dimension=r['dimension'],
            symmetry_kind=r['symmetry_kind'], scope=('zero-chiral-fiber' if r.get('abstract_chiral_completion') else 'full'),
            invariant_factors=r['invariant_factors'], final_filtration=r['final_filtration'],
            verified_background_maps={x['id']:witnesses[x['id']] for x in records if x['id'] in witnesses}))
    assert sum(len(x['calculation_records']) for x in examples) == index['record_count']
    assert len({a for x in examples for a in x['calculation_records']}) == index['record_count']
    counts = Counter(str(x['dimension']) for x in examples if x['symmetry_kind']=='finite_internal')
    assert counts == {'1':6, '2':16, '3':72, '4':572}, counts
    return dict(schema='fspt-unique-reader-examples-v1',
        unique_examples=len(examples), retained_calculation_records=index['record_count'],
        additional_verification_records=index['record_count']-len(examples),
        finite_backgrounds_by_dimension=dict(sorted(counts.items())),
        crystalline_examples=sum(x['symmetry_kind']!='finite_internal' for x in examples),
        source_index_sha256=hashlib.sha256((HERE/'index.json').read_bytes()).hexdigest(),
        four_dimensional_translation_sha256=hashlib.sha256((HERE/'tables/internal_4d_symbolic.json').read_bytes()).hexdigest(),
        scope='One reader entry per verified symmetry background at a fixed dimension and calculation scope. Numbered crystalline inputs and physical spin conventions remain distinct. Historical numerical records remain provenance.',
        examples=examples)


def selected_records(index, unique):
    lookup={r['id']:r for r in index['cases']}
    result=[]
    for e in unique['examples']:
        r=dict(lookup[e['representative_record']])
        r['reader_example_key']=e['example_key']
        r['reader_alias_records']=e['calculation_records']
        r['collections']=sorted({c for i in e['calculation_records'] for c in lookup[i]['collections']})
        result.append(r)
    return result


def main():
    ap=argparse.ArgumentParser(description=__doc__);ap.add_argument('--check', action='store_true');args=ap.parse_args()
    data=build();payload=json.dumps(data,indent=2,sort_keys=True)+'\n';p=HERE/'unique_examples.json'
    if args.check:assert p.read_text()==payload
    else:p.write_text(payload)
    print(json.dumps({k:data[k] for k in ('unique_examples','retained_calculation_records','additional_verification_records','finite_backgrounds_by_dimension','crystalline_examples')}))


if __name__=='__main__':main()
