#!/usr/bin/env python3
"""Post-freeze comparison; never modifies an independently computed result."""
import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import re

from audit_run import check_complete_witnesses, check_result

CURRENT_FORMULA_CONVENTION = 'normalized-pip-aw-edge-transport-v2'


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def invariant_factors(orders):
    """Canonicalize a direct sum, including zero for each free factor."""
    free = sum(x == 0 for x in orders)
    prime_powers = {}
    for order in orders:
        if not isinstance(order, int) or order < 0:
            raise ValueError("invalid cyclic factor")
        value, prime = order, 2
        while value > 1 and prime * prime <= value:
            exponent = 0
            while value % prime == 0:
                value //= prime
                exponent += 1
            if exponent:
                prime_powers.setdefault(prime, []).append(prime ** exponent)
            prime += 1
        if value > 1:
            prime_powers.setdefault(value, []).append(value)
    width = max(map(len, prime_powers.values()), default=0)
    result = [1] * width
    for powers in prime_powers.values():
        padded = [1] * (width - len(powers)) + sorted(powers)
        result = [x * y for x, y in zip(result, padded)]
    return [0] * free + result


def factors(data):
    if data is None:
        return None
    return invariant_factors([part['order'] for part in data
                              for _ in range(part['multiplicity'])])


def read_results(directory, known_source_hashes=None):
    if not __debug__:
        raise ValueError('Run without Python -O: the certificate auditor uses assertions')
    records = {}
    for path in directory.glob('sg*.json'):
        if '.raw.' in path.name:
            continue
        if not path.stem[2:].isdigit():
            raise ValueError('unexpected result filename: ' + str(path))
        number = int(path.stem[2:])
        if not 1 <= number <= 230 or number in records or path.name != 'sg%d.json' % number:
            raise ValueError('invalid or duplicate result filename: ' + str(path))
        record = json.loads(path.read_text())
        if record['space_group'] != number:
            raise ValueError('result filename/group mismatch: ' + str(path))
        if 'source_sha256' not in record:
            # GAP classification checkpoints record the source ID, while the
            # completed Python wrapper adds the full source-file hash map.
            # Recover only that metadata from a separately audited result of
            # the exact same source; never alter a saved checkpoint.
            source = record.get('source_id')
            if source not in (known_source_hashes or {}):
                raise ValueError('checkpoint has no verifiable source-file hash map: ' + str(path))
            record = dict(record, source_sha256=known_source_hashes[source])
        check_result(record)
        records[number] = record
    return records


def load_frozen(directory):
    path = directory / 'manifest.json'
    manifest = json.loads(path.read_text())
    expected = {'sg%d.json' % n for n in range(1, 231)}
    if manifest['groups'] != 230 or manifest['external_answers_consulted'] is not False:
        raise ValueError('require all-230 independent classification freeze before external comparison')
    if set(manifest['result_sha256']) != expected:
        raise ValueError('frozen manifest does not certify exactly 230 groups')
    for name, checksum in manifest['result_sha256'].items():
        if digest(directory / name) != checksum:
            raise ValueError('frozen result hash mismatch: ' + name)
    records = read_results(directory)
    if set(records) != set(range(1, 231)):
        raise ValueError('frozen classification is incomplete')
    return records, manifest, dict(directory=str(directory), manifest_sha256=digest(path),
        frozen_at=manifest['frozen_at'], external_answers_consulted_at_freeze=False,
        result_sha256=manifest['result_sha256'])


def audit_computed(records, require_complete=False):
    if not require_complete:
        return
    if set(records) != set(range(1, 231)):
        raise ValueError('final comparison requires all 230 complete results')
    for number, record in sorted(records.items()):
        try:
            check_complete_witnesses(record, CURRENT_FORMULA_CONVENTION)
        except (AssertionError, KeyError, TypeError, ValueError, IndexError) as exc:
            raise ValueError('SG%d failed strict complete-witness audit: %s' % (number, exc)) from exc
    if len({record['source_id'] for record in records.values()}) != 1:
        raise ValueError('final comparison requires one uniform source for all 230 groups')


def result_provenance(directory, records):
    sources = {}
    for record in records.values():
        source = record['source_id']
        if source in sources and sources[source] != record['source_sha256']:
            raise ValueError('inconsistent source hashes for ' + source)
        sources[source] = record['source_sha256']
    return dict(directory=str(directory), groups=len(records),
        result_sha256={'sg%d.json' % n: digest(directory / ('sg%d.json' % n)) for n in sorted(records)},
        source_sha256=sources, source_ids=sorted(sources))


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument('--boss-root', type=Path, required=True)
    ap.add_argument('--reference-root', type=Path, required=True)
    ap.add_argument('--classification', type=Path, default=Path('runs/classification_frozen'))
    ap.add_argument('--computed', type=Path, default=Path('runs/accepted'))
    ap.add_argument('--current-classification', type=Path,
                    help='Current immutable campaign classification checkpoints; completed full outputs take precedence')
    ap.add_argument('--require-complete', action='store_true',
                    help='Final comparison: require 230 complete AW-v2 witness results from one uniform source')
    ap.add_argument('--finite-controls', type=Path, default=Path('runs/finite_c2_controls.json'))
    ap.add_argument('--output', type=Path, default=Path('runs/comparison_external'))
    a = ap.parse_args()
    frozen, manifest, frozen_provenance = load_frozen(a.classification)
    computed = read_results(a.computed)
    audit_computed(computed, a.require_complete)
    known_sources = {record['source_id']: record['source_sha256'] for record in computed.values()}
    checkpoints = read_results(a.current_classification, known_sources) if a.current_classification else {}
    current = dict(checkpoints)
    current.update({n: r for n, r in computed.items() if 'complex_fermion' in r})
    graded = dict(frozen)
    graded.update(current)
    draft_path = a.boss_root/'output/space_group_230/draft_table.json'
    draft = json.loads(draft_path.read_text())
    layer_fields = [('E2D','pip'), ('E1D','majorana'),
                    ('E0D','complex_fermion'), ('Eb','bosonic')]
    rows = []
    for old in draft:
        number = old['number']; actual = graded[number]; layers = {}
        for external, internal in layer_fields:
            ours = actual[internal]['orders'] if internal == 'pip' else actual[internal]
            expected = factors(old.get(external+'_factors'))
            layers[external] = dict(reference=expected, independent=invariant_factors(ours),
                                    match=None if expected is None else expected == invariant_factors(ours))
        same = all(x['match'] is True for x in layers.values())
        changed = any(x['match'] is False for x in layers.values())
        reference_stack = factors(old.get('Extension_factors'))
        stack = computed.get(number, {}).get('stacking', {})
        ours = invariant_factors(stack['invariants']) if stack.get('status') == 'computed' else None
        match = None if reference_stack is None or ours is None else reference_stack == ours
        category = 'no-draft-stack-reference' if reference_stack is None else (
            'independent-stacking-pending' if ours is None else (
            'match' if match else ('mismatch-same-four-layers' if same else (
            'mismatch-also-changed-layers' if changed else 'mismatch-draft-layers-incomplete'))))
        rows.append(dict(space_group=number, reference_status=old['status'],
            layers=layers, reference_stack=reference_stack, independent_stack=ours,
            stack_match=match, category=category,
            independent_source_id=computed.get(number, {}).get('source_id')))
    foundations_path = a.boss_root/'output/space_group_230/backend/FOUNDATIONS.md'
    geometric = []
    for line in foundations_path.read_text().splitlines():
        if not re.match(r'^\|\s*\d+\s*\|', line):
            continue
        cells = [x.strip() for x in line.split('|')[1:-1]]
        number = int(cells[0]); expression = cells[-1]; orders = []
        for part in expression.split('+'):
            m = re.fullmatch(r'Z(?:(\d+))?(?:\^(\d+))?', part.strip())
            if not m:
                raise ValueError(('unexpected geometric group notation', part))
            orders.extend([int(m.group(1) or 0)] * int(m.group(2) or 1))
        expected = invariant_factors(orders)
        stack = computed.get(number, {}).get('stacking', {})
        ours = invariant_factors(stack['invariants']) if stack.get('status') == 'computed' else None
        geometric.append(dict(space_group=number, reference_expression=expression,
            reference=expected, independent=ours, match=None if ours is None else expected == ours))
    finite_path = a.reference_root/'data/extension-paper-results-20260926-transfer.json'
    finite_reference = json.loads(finite_path.read_text())
    finite_controls = json.loads(a.finite_controls.read_text()) if a.finite_controls.exists() else None
    finite_rows = []
    for reference in finite_reference['results']:
        if (reference['spatialDimension'] != 3 or reference['input']['omega'] != 0
                or reference['input']['group'] != 'CyclicGroup(2)'):
            continue
        sign = int(reference['input']['s'] != 0)
        ours = next((r for r in (finite_controls or {}).get('results', [])
                     if r['s'] == sign and r.get('group') == 'CyclicGroup(2)'
                     and r.get('omega') == 0 and r.get('spatialDimension') == 3
                     and r.get('status') == 'computed'), None)
        actual = invariant_factors(ours['invariants']) if ours is not None else None
        expected = invariant_factors(reference['actual'])
        finite_rows.append(dict(case_id=reference['caseId'], spatial_dimension=3,
            group='CyclicGroup(2)', omega=0, sign=sign, reference=expected,
            independent=actual, match=None if actual is None else expected == actual))
    e2_path = a.boss_root/'output/space_group_230/backend/hap_all230_e2.json'
    e2_rows = json.loads(e2_path.read_text())['rows']
    e2_checks = []
    for row in e2_rows:
        for degree in (1,2,3):
            key = f'H{degree}_F2_dimension'
            if type(row.get(key)) is int:
                ours = graded[row['number']]['ranks'][f'H{degree}F2']
                e2_checks.append(dict(space_group=row['number'],degree=degree,
                    reference=row[key],independent=ours,match=row[key]==ours))
    h1_path = a.boss_root/'output/space_group_230/backend/h1_all230.json'
    h1_checks = []
    for row in json.loads(h1_path.read_text())['rows']:
        pip = graded[row['number']]['pip']
        expected = [row['H1_Zs_free_rank'],row['H1_Zs_Z2_rank']]
        ours = [pip['free_rank'],len(pip['torsion'])]
        h1_checks.append(dict(space_group=row['number'],reference=expected,
            independent=ours,match=expected==ours))
    report = dict(scope='post-freeze-external-comparison-without-result-mutation',
        chronology='The original independent classification freeze preceded consultation of external answers. '
                   'Current results are later formula/performance regression runs, not additional pre-reference freezes.',
        frozen=frozen_provenance,
        computed=result_provenance(a.computed, computed),
        complete_witnesses_required=a.require_complete,
        required_formula_convention=CURRENT_FORMULA_CONVENTION if a.require_complete else None,
        frozen_at=manifest['frozen_at'], independent_classification_count=len(graded),
        current_classification_count=len(current),
        classification_current_source_ids=sorted({r['source_id'] for r in current.values() if 'source_id' in r}),
        current_formula_conventions=sorted({r['formula_convention'] for r in current.values() if 'formula_convention' in r}),
        computed_directory=str(a.computed),
        current_classification_directory=str(a.current_classification) if a.current_classification else None,
        independent_full_stack_count=sum(d.get('stacking',{}).get('status')=='computed' for d in computed.values()),
        draft_reference_kind='historical manuscript transcription; four same-layer disagreements confirmed in original completed logs; not boss new computed final output',
        draft_reference_path=str(draft_path), draft_reference_sha256=hashlib.sha256(draft_path.read_bytes()).hexdigest(),
        draft_categories=dict(Counter(r['category'] for r in rows)), draft_rows=rows,
        geometric_reference_path=str(foundations_path), geometric_rows=geometric,
        geometric_reference_sha256=hashlib.sha256(foundations_path.read_bytes()).hexdigest(),
        finite_reference_path=str(finite_path), finite_rows=finite_rows,
        finite_reference_sha256=hashlib.sha256(finite_path.read_bytes()).hexdigest(),
        finite_controls_path=str(a.finite_controls),
        finite_controls_sha256=digest(a.finite_controls) if a.finite_controls.exists() else None,
        finite_distinct_inputs=len({(r['sign'],r['omega']) for r in finite_rows}),
        finite_reference_scope=finite_reference['scope'], finite_reference_certified_ko=finite_reference['certified_ko'])
    report['boss_initial_cohomology'] = dict(
        mod2_reference_path=str(e2_path), mod2_reference_sha256=digest(e2_path),
        signed_H1_reference_path=str(h1_path), signed_H1_reference_sha256=digest(h1_path),
        mod2_dimensions_compared=len(e2_checks),mod2_matches=sum(r['match'] for r in e2_checks),
        mod2_mismatches=[r for r in e2_checks if not r['match']],
        signed_H1_groups_compared=len(h1_checks),signed_H1_matches=sum(r['match'] for r in h1_checks),
        signed_H1_mismatches=[r for r in h1_checks if not r['match']])
    if a.current_classification:
        report['current_classification_provenance'] = result_provenance(
            a.current_classification, checkpoints)
        report['current_classification_provenance']['checkpoint_source_hash_origin'] = (
            'Missing checkpoint source-file maps are taken only from audited complete result '
            'metadata with the identical source ID; saved checkpoint bytes remain unchanged.')
    a.output.mkdir(parents=True,exist_ok=True)
    (a.output/'comparison.json').write_text(json.dumps(report,indent=2)+'\n')
    print(json.dumps({k:v for k,v in report.items() if k not in
                     ['draft_rows','geometric_rows','finite_rows','frozen','computed',
                      'current_classification_provenance']},indent=2))
    print('DRAFT_STACK_MISMATCHES',[(r['space_group'],r['category'],r['reference_stack'],r['independent_stack'])
                                     for r in rows if r['stack_match'] is False])
    print('GEOMETRIC_COMPARISON',[(r['space_group'],r['match']) for r in geometric])
    print('FINITE_C2_COMPARISON',finite_rows)


if __name__ == '__main__':
    main()
