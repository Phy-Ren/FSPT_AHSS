#!/usr/bin/env python3
"""Prepare a 460-row table of two different crystalline physical conventions.

This is a comparison of physical problems, not an external validation. Both
input archives must independently pass their own strict mathematical auditor.
No reference table is read and neither input is modified.
"""
import argparse
import csv
import hashlib
import json
from pathlib import Path

from audit_background_run import audit as audit_spinless
from audit_run import check_result, check_complete_witnesses

FORMULA = 'normalized-pip-aw-edge-transport-v2'
HALF_CONVENTION = 'physical-spin-half-det-sign-omega0'
ORIENTED_TORSION_FREE_EXAMPLES = (1, 4, 19, 76, 78, 144, 145, 169, 170)


def odd_primary(orders):
    """Odd torsion invariant factors; free factors and powers of two vanish."""
    result = []
    for order in orders:
        assert type(order) is int and order >= 0
        if order == 0:
            continue
        while order % 2 == 0:
            order //= 2
        if order > 1:
            result.append(order)
    return sorted(result)


def contrast(a, b):
    """Compare already audited row data without treating either as an oracle."""
    changed = {key: a['layers'][key] != b['layers'][key]
               for key in ('pip', 'majorana', 'complex_fermion', 'bosonic')}
    if b['invariants'] is not None:
        full = 'same-abstract-group' if a['invariants'] == b['invariants'] else 'different-abstract-groups'
    elif b['invariant_options']:
        full = ('undetermined-spin-half-group-is-an-option' if a['invariants'] in b['invariant_options']
                else 'all-certified-spinless-options-differ')
    else:
        full = 'spinless-full-group-unavailable'
    options = [b['invariants']] if b['invariants'] is not None else (b['invariant_options'] or [])
    odd_matches = [odd_primary(a['invariants']) == odd_primary(option) for option in options]
    return {'space_group': a['space_group'], **{key+'_changed': value for key, value in changed.items()},
            'full_group_comparison': full,
            'bosonic_odd_primary_equal': odd_primary(a['layers']['bosonic']) == odd_primary(b['layers']['bosonic']),
            'full_odd_primary_equal_for_all_certified_options': all(odd_matches) if odd_matches else None,
            'free_index_changed': (a['free_lattice'] or {}).get('index') != (b['free_lattice'] or {}).get('index'),
            'spin_half_result_sha256': a['result_sha256'], 'spinless_result_sha256': b['result_sha256'],
            'interpretation': 'two-different-physical-problems; not-external-validation'}


def half_rows(directory):
    expected = {'sg%d.json' % n for n in range(1, 231)}
    found = {p.name for p in directory.glob('sg*.json') if '.raw.' not in p.name}
    if found != expected:
        raise ValueError('spin-half archive requires exactly all 230 results')
    rows = []
    for n in range(1, 231):
        path = directory/('sg%d.json' % n); raw = path.read_bytes(); d = json.loads(raw)
        assert d['space_group'] == n and d['convention'] == HALF_CONVENTION
        check_complete_witnesses(d, FORMULA)
        kind = check_result(d)
        rows.append(dict(space_group=n, crystalline_spin='half', physical_convention=HALF_CONVENTION,
            effective_sign='w1(V)=determinant-parity', effective_omega='0',
            layers={'pip': d['pip']['orders'], **{key: d[key] for key in ('majorana', 'complex_fermion', 'bosonic')}},
            invariants=d['stacking']['invariants'], invariant_options=None,
            free_lattice={'index': d['pip']['free_lattice']['latticeIndex']} if d['pip']['free_rank'] else None,
            marked_witnesses=True, kind=kind, source_id=d['source_id'], result_sha256=hashlib.sha256(raw).hexdigest()))
    if len({r['source_id'] for r in rows}) != 1:
        raise ValueError('spin-half archive has mixed source snapshots')
    return rows


def geometric_overlap(directory, half, spinless):
    """Transfer only the nine previously checked oriented affine examples.

    No geometric answer table is read here. The exact native gauge and the
    agreement of the two independently audited physical outputs are checked.
    """
    A = {r['space_group']: r for r in half}
    B = {r['space_group']: r for r in spinless}
    rows = []
    for n in ORIENTED_TORSION_FREE_EXAMPLES:
        raw = (directory/('sg%d.json' % n)).read_bytes()
        assert hashlib.sha256(raw).hexdigest() == B[n]['result_sha256']
        background = json.loads(raw)['crystalline_background']
        gauge, differential = background['trivializingNative1'], background['nativeDifferential1F2']
        omega = background['nativeOriginalOmega2']
        assert background['gaugeReducedToZero'] and not any(background['signTable'])
        assert len(gauge) == len(differential)
        reconstructed = [sum(x*row[j] for x, row in zip(gauge, differential)) % 2 for j in range(len(omega))]
        assert reconstructed == omega
        assert A[n]['layers'] == B[n]['layers'] and A[n]['invariants'] == B[n]['invariants']
        hash_value = lambda value: hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()
        rows.append(dict(space_group=n, orientation_sign_zero=True,
            native_affine_background_trivialized=True, original_native_cocycle_nonzero=any(omega),
            graded_layers_equal=True, full_abstract_group_equal=True,
            free_lattice_index_equal=(A[n]['free_lattice'] or {}).get('index') == (B[n]['free_lattice'] or {}).get('index'),
            native_gauge_vector_sha256=hash_value(gauge), native_differential1_sha256=hash_value(differential),
            spin_half_result_sha256=A[n]['result_sha256'], spinless_result_sha256=B[n]['result_sha256'],
            interpretation='Existing nine-example geometric comparison transfers after verified native trivialization and equality; not a new 230-group external comparison.'))
    return rows


def generate(half, spinless, output):
    if not __debug__:
        raise ValueError('run without Python -O')
    if output.exists() or output.is_symlink():
        raise ValueError('output directory already exists')
    a = half_rows(half)
    background, failed = audit_spinless(spinless)
    if failed or not background['all_230_certificates_strictly_valid']:
        raise ValueError('spinless archive must pass the strict full-230 certificate audit')
    if len(background['source_ids']) != 1:
        raise ValueError('spinless archive has mixed source snapshots')
    b = background['rows']
    changes = [contrast(x, y) for x, y in zip(a, b)]
    odd_failures = [r['space_group'] for r in changes if not r['bosonic_odd_primary_equal']
                    or r['full_odd_primary_equal_for_all_certified_options'] is False]
    if odd_failures:
        raise ValueError('odd-primary physical-convention consistency failed for SG '+str(odd_failures))
    geometry = geometric_overlap(spinless, a, b)
    report = dict(schema='fspt-two-physical-conventions-report-v1',
        interpretation='Two different physical symmetry problems. Differences are not failures of external validation.',
        spin_half_input=str(half), spinless_input=str(spinless),
        source_ids={'half': a[0]['source_id'], 'spinless': b[0]['source_id']},
        rows=a+b, per_space_group_comparison=changes, external_reference_answers_read=False,
        oriented_torsion_free_geometric_overlap=geometry,
        odd_primary_consistency=dict(
            interpretation='Internal cross-convention consistency: the common sign action and only 2-primary new operations preserve the odd torsion sector; not an external validation.',
            bosonic_matches=sum(r['bosonic_odd_primary_equal'] for r in changes),
            full_matches_for_all_certified_options=sum(r['full_odd_primary_equal_for_all_certified_options'] is True for r in changes),
            full_unavailable=sum(r['full_odd_primary_equal_for_all_certified_options'] is None for r in changes),
            mismatching_space_groups=odd_failures),
        tool_sha256={name: hashlib.sha256((Path(__file__).parent/name).read_bytes()).hexdigest()
                     for name in ('report_physical_conventions.py', 'audit_run.py', 'audit_background_run.py')})
    output.mkdir(parents=True)
    (output/'comparison.json').write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    fields = ['space_group', 'crystalline_spin', 'physical_convention', 'effective_sign', 'effective_omega',
              'pip', 'majorana', 'complex_fermion', 'bosonic', 'full_invariants', 'invariant_options',
              'free_lattice_index', 'h0_incoming_order', 'certificate_kind', 'actual_marked_witnesses',
              'source_id', 'result_sha256']
    with (output/'physical_conventions_460.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=fields); writer.writeheader()
        for row in a+b:
            record = {key: row[key] for key in ('space_group', 'crystalline_spin', 'physical_convention', 'effective_sign', 'effective_omega', 'source_id', 'result_sha256')}
            record.update({key: json.dumps(value) for key, value in row['layers'].items()})
            record.update(full_invariants=json.dumps(row['invariants']), invariant_options=json.dumps(row['invariant_options']),
                free_lattice_index=(row['free_lattice'] or {}).get('index', ''),
                h0_incoming_order=row.get('h0_quotient', {}).get('incoming_order', ''),
                certificate_kind=row['kind'], actual_marked_witnesses=row['marked_witnesses'])
            writer.writerow(record)
    with (output/'per_space_group_changes.csv').open('w', newline='') as handle:
        writer = csv.DictWriter(handle, fieldnames=list(changes[0])); writer.writeheader(); writer.writerows(changes)
    (output/'geometric_overlap_9.json').write_text(json.dumps(geometry, indent=2, sort_keys=True)+'\n')
    lines = ['# Two physical crystalline conventions', '',
             'This table compares different physical problems; it is not an external verification of either result.', '',
             'Spin-half crystalline: effective internal s=w1(V), omega=0. Spinless crystalline: effective internal s=w1(V), omega=w2(V)+w1(V)^2. Both use the full infinite affine group.', '',
             'The [460-row table](physical_conventions_460.csv) retains four graded layers separately from full stacking, free-lattice index, H0 order, upper-certificate scope, actual marked status, and source/result hashes. '
             'Possible full groups retain their free p+ip factors. Abstract agreement does not identify physical generators or phase witnesses.', '',
             'The odd-primary consistency check compares the bosonic layer and every certified full-group option. '
             'It uses the common sign action and the 2-primary nature of the changed operations; it is an internal consistency check, not an external validation. '
             'The exact counts are retained in comparison.json and the per-SG CSV.', '',
             'The [nine oriented torsion-free examples](geometric_overlap_9.json) retain an exact native trivialization of the new background and equal graded layers/full abstract groups. '
             'This permits reuse of the earlier nine-example geometric check; it is not an additional 230-group external comparison.', '',
             '| SG | p+ip changed | MC changed | CF changed | Bosonic changed | Full abstract group comparison | Free index changed |',
             '|---:|---|---|---|---|---|---|']
    for row in changes:
        lines.append('| %d | %s | %s | %s | %s | %s | %s |' % tuple(row[key] for key in
            ('space_group', 'pip_changed', 'majorana_changed', 'complex_fermion_changed', 'bosonic_changed', 'full_group_comparison', 'free_index_changed')))
    (output/'README.md').write_text('\n'.join(lines)+'\n')
    return {'output': str(output), 'rows': 460, 'space_groups': 230, 'source_ids': report['source_ids']}


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--half', type=Path, default=Path('results/space_groups'))
    p.add_argument('--spinless', type=Path, default=Path('results/space_groups_spinless'))
    p.add_argument('--output', type=Path, required=True)
    a = p.parse_args(argv)
    try:
        result = generate(a.half, a.spinless, a.output)
    except (OSError, ValueError, AssertionError, KeyError, TypeError) as exc:
        p.exit(2, 'Physical-convention report refused: '+str(exc)+'\n')
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
