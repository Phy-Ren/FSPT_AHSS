#!/usr/bin/env python3
"""Compare full saved mathematical trees, including native witnesses.

Only enumerated runtime metadata and documented early-export changes are
normalized. Newly added native certificate matrices are separately audited,
never represented as a successful comparison with absent earlier matrices.
No input is modified and no reference answer is read.
"""
import argparse
import copy
import hashlib
import json
from pathlib import Path
import re

from audit_background_run import CONVENTION, FORMULA, check_background_result
from audit_run import check_result as check_half, check_complete_witnesses as check_half_witnesses


METADATA = {
    'cpu_ms': 'GAP classification CPU time',
    'free_pip_cpu_ms': 'GAP free-lattice CPU time',
    'total_cpu_ms': 'total GAP CPU time',
    'wall_seconds': 'per-run elapsed time',
    'started': 'execution start timestamp',
    'finished': 'execution completion timestamp',
    'resolution_timings': 'resolution construction timing breakdown',
    'stage_timings': 'execution-stage CPU timestamps',
    'source_id': 'distinct immutable implementation snapshot, preserved in provenance',
    'source_sha256': 'implementation-file checksums, preserved in original input and provenance',
    'source_snapshot': 'filesystem location of the immutable implementation snapshot',
    'background_projected_native_cup': 'implementation dispatch flag for the cup-zero optimization; not a physical background input',
    'background_pip_compiled_calls': 'full-background formula evaluator invocation count',
    'background_even_pip_compiled_calls': 'even-integer-layer specialized evaluator invocation count',
    'background_sign_pip_compiled_calls': 'canonical-sign integer-layer specialized evaluator invocation count',
    'generic_pip_compiled_calls': 'zero-background general evaluator invocation count',
}


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def leaves(value):
    if isinstance(value, dict):
        return sum(leaves(x) for x in value.values())
    if isinstance(value, list):
        return sum(leaves(x) for x in value)
    return 1


def evidence(path, reason, a=None, b=None):
    return {'path': path, 'reason': reason, 'baseline_value_sha256': digest(a),
            'candidate_value_sha256': digest(b), 'baseline_scalar_leaves': leaves(a),
            'candidate_scalar_leaves': leaves(b)}


def normalize_pair(baseline, candidate, crystalline_spin='spinless'):
    a, b = copy.deepcopy(baseline), copy.deepcopy(candidate)
    ignored, schema, added = [], [], []
    for key, reason in METADATA.items():
        if key in a or key in b:
            if key == 'background_projected_native_cup':
                assert all(type(x[key]) is bool for x in (a, b) if key in x)
            if key.endswith('_calls'):
                assert all(type(x[key]) is int and x[key] >= 0 for x in (a, b) if key in x)
            ignored.append(evidence('/'+key, reason, a.get(key), b.get(key)))
            a.pop(key, None); b.pop(key, None)

    if crystalline_spin == 'half':
        convention = 'physical-spin-half-det-sign-omega0'
        for data, side in ((a, 'baseline'), (b, 'candidate')):
            assert data['convention'] == convention
            if 'crystalline_spin' not in data:
                data['crystalline_spin'] = 'half'
                schema.append({'side': side, 'path': '/crystalline_spin',
                    'reason': 'New redundant physical-spin selector is fixed by the existing root spin-half convention.'})
            assert data['crystalline_spin'] == 'half'
            if 'physicalConvention' not in data['stacking']:
                data['stacking']['physicalConvention'] = convention
                schema.append({'side': side, 'path': '/stacking/physicalConvention',
                    'reason': 'New redundant stacking convention label is fixed by the already audited root convention.'})
        diagnostic_lists = [('/pip/torsion', a['pip']['torsion'], b['pip']['torsion'])]
        if 'free_lattice' in a['pip'] and 'free_lattice' in b['pip']:
            diagnostic_lists.append(('/pip/free_lattice/parityCandidates',
                a['pip']['free_lattice']['parityCandidates'], b['pip']['free_lattice']['parityCandidates']))
        for parent_path, old_list, new_list in diagnostic_lists:
            if len(old_list) != len(new_list):
                continue
            for i, (x, y) in enumerate(zip(old_list, new_list)):
                for key in ('d3_initial_coordinates', 'd4_projected_coordinates'):
                    if (key in x) == (key in y):
                        continue
                    present = x if key in x else y
                    value = present[key]
                    assert present['status'] == 'survives' and present['page'] == 4
                    assert isinstance(value, list) and all(type(v) is int and v in (0, 1) for v in value)
                    if key == 'd3_initial_coordinates':
                        if not any(present['majorana_adjustment']):
                            assert not any(value)
                            reason = ('Added zero d3 diagnostic, consistent with the unchanged zero Majorana adjustment and retained actual lower lift. ')
                        else:
                            reason = ('Added binary initial d3 diagnostic before the unchanged nonzero Majorana adjustment. '
                                      'Its values are new source-linked evidence, not independently reconstructed or compared with a missing old vector. ')
                        reason += ('The earlier export has no diagnostic vector; its cohomology-space dimension is not independently reconstructed by this comparison.')
                    else:
                        assert len(value) == len(present['d4_target']) and not any(value)
                        if not any(present['d4_raw_coordinates']):
                            reason = ('Added d4 quotient coordinate: the unchanged raw class is zero, so its projection is exactly zero; target length checked. ')
                        else:
                            reason = ('Added zero d4 quotient diagnostic consistent with the unchanged surviving status; target length checked. '
                                      'The projection of the unchanged nonzero raw class is not reconstructed by this comparison. ')
                        reason += 'The earlier export did not contain this diagnostic.'
                    added.append(evidence('%s/%d/%s' % (parent_path, i, key), reason, x.get(key), y.get(key)))
                    x.pop(key, None); y.pop(key, None)
        return a, b, ignored, schema, added
    assert crystalline_spin == 'spinless' and a['convention'] == b['convention'] == CONVENTION

    for data, original, side in ((a, baseline, 'baseline'), (b, candidate, 'candidate')):
        s = data['stacking']
        if 'lower' not in s and 'h0IncomingQuotient' in s:
            s['lower'] = copy.deepcopy(s['h0IncomingQuotient']['lower'])
            schema.append({'side': side, 'path': '/stacking/lower',
                'reason': 'Early exporter omitted the outer alias; compare the complete retained h0IncomingQuotient.lower tree here.',
                'canonical_value_sha256': digest(s['lower'])})
        if 'physicalConvention' not in s:
            assert original['convention'] == CONVENTION
            s['physicalConvention'] = original['convention']
            schema.append({'side': side, 'path': '/stacking/physicalConvention',
                'reason': 'Fill redundant stacking label from the already audited physical root convention.'})
        if s['scope'] == 'full-3+1D-spin-half-affine-stacking':
            assert original['convention'] == CONVENTION
            s['scope'] = '3+1D-crystalline-spinless-affine-stacking'
            schema.append({'side': side, 'path': '/stacking/scope',
                'reason': 'Early shared exporter left a stale spin-half display label; the root physical convention is spinless in both runs.'})
        elif s['scope'] == 'full-3+1D-crystalline-spinless-affine-stacking':
            s['scope'] = '3+1D-crystalline-spinless-affine-stacking'
            schema.append({'side': side, 'path': '/stacking/scope',
                'reason': 'Remove the redundant full prefix from the spinless display-scope label; computed/unresolved status and witnesses are unchanged.'})

    native = ('nativeDifferential1F2', 'nativeDifferential2F2', 'nativeH2Generators')
    A, B = a['crystalline_background'], b['crystalline_background']
    for key in native:
        if (key in A) != (key in B):
            added.append(evidence('/crystalline_background/'+key,
                'New independently audited native background matrix certificate. No earlier matrix exists for literal comparison; all original omega/H2 coordinates and gauge vectors remain compared.',
                A.get(key), B.get(key)))
            A.pop(key, None); B.pop(key, None)

    def labels(x, path, side):
        if isinstance(x, dict):
            if '/finalFiltrationCertificate' in path:
                if x.get('convention') == 'spin-half-omega0-det':
                    x['convention'] = CONVENTION
                    schema.append({'side': side, 'path': path+'/convention',
                        'reason': 'Correct the stale shared-exporter filtration label; all filtered group data are retained.'})
                if x.get('convention') == CONVENTION and 'beforeH0Incoming' not in x:
                    before = any(part in path for part in ('/preQuotientCertificate', '/preQuotientLower', '/lowerBeforeH0Incoming'))
                    x['beforeH0Incoming'] = before
                    schema.append({'side': side, 'path': path+'/beforeH0Incoming',
                        'reason': 'Explicit annotation inferred from the containing pre-quotient or final presentation, without changing either presentation.'})
            for key, value in x.items():
                labels(value, path+'/'+key, side)
        elif isinstance(x, list):
            for i, value in enumerate(x):
                labels(value, path+'/'+str(i), side)
    labels(a, '', 'baseline'); labels(b, '', 'candidate')

    def bounds(x, y, path):
        if isinstance(x, dict) and isinstance(y, dict):
            if path.endswith('/certificate') and 'pip-boundary' in str(x.get('formula', '')):
                if ('orderDivides' in x) != ('orderDivides' in y):
                    value = x.get('orderDivides', y.get('orderDivides'))
                    assert value == 16
                    added.append(evidence(path+'/orderDivides',
                        'Added universal H0 order bound 16, independently checked against the measured incoming order by the candidate auditor.',
                        x.get('orderDivides'), y.get('orderDivides')))
                    x.pop('orderDivides', None); y.pop('orderDivides', None)
            for key in x.keys() & y.keys():
                bounds(x[key], y[key], path+'/'+key)
        elif isinstance(x, list) and isinstance(y, list) and len(x) == len(y):
            for i, (u, v) in enumerate(zip(x, y)):
                bounds(u, v, path+'/'+str(i))
    bounds(a, b, '')
    return a, b, ignored, schema, added


def differences(a, b, path=''):
    if type(a) is not type(b):
        return [dict(path=path, baseline=a, candidate=b, reason='type differs')]
    if isinstance(a, dict):
        result = []
        for key in sorted(a.keys() | b.keys()):
            if key not in a or key not in b:
                result.append(dict(path=path+'/'+key, reason='field missing',
                                   baseline_present=key in a, candidate_present=key in b))
            else:
                result.extend(differences(a[key], b[key], path+'/'+key))
        return result
    if isinstance(a, list):
        if len(a) != len(b):
            return [dict(path=path, reason='list length differs', baseline_length=len(a), candidate_length=len(b))]
        return [item for i, (u, v) in enumerate(zip(a, b)) for item in differences(u, v, path+'/'+str(i))]
    return [] if a == b else [dict(path=path, baseline=a, candidate=b, reason='value differs')]


def inputs(directory):
    paths = {}
    for p in directory.glob('sg*.json'):
        if '.raw.' in p.name:
            continue
        m = re.fullmatch(r'sg([1-9][0-9]*)\.json', p.name)
        if not m or not 1 <= int(m.group(1)) <= 230:
            raise ValueError('invalid result path: '+str(p))
        paths[int(m.group(1))] = p
    return paths


def compare(baseline, candidate, allow_legacy_baseline=False, crystalline_spin='spinless', expected_groups=None):
    A, B = inputs(baseline), inputs(candidate)
    if expected_groups is not None:
        assert expected_groups and len(set(expected_groups)) == len(expected_groups)
        assert all(type(n) is int and 1 <= n <= 230 for n in expected_groups)
    rows, errors = [], []
    for sg in sorted(A.keys() & B.keys()):
        try:
            raw_a, raw_b = A[sg].read_bytes(), B[sg].read_bytes()
            old, new = json.loads(raw_a), json.loads(raw_b)
            assert old['space_group'] == new['space_group'] == sg
            if crystalline_spin == 'spinless':
                audit_a = check_background_result(old, strict_background=not allow_legacy_baseline)
                audit_b = check_background_result(new)
            else:
                assert crystalline_spin == 'half' and not allow_legacy_baseline
                check_half_witnesses(old, FORMULA); check_half_witnesses(new, FORMULA)
                audit_a = {'kind': check_half(old), 'marked_witnesses': True}
                audit_b = {'kind': check_half(new), 'marked_witnesses': True}
            a, b, ignored, schema, added = normalize_pair(old, new, crystalline_spin)
            diff = differences(a, b)
            rows.append(dict(space_group=sg, literal_mathematical_tree_equal=not diff,
                baseline_path=str(A[sg]), candidate_path=str(B[sg]),
                baseline_sha256=hashlib.sha256(raw_a).hexdigest(), candidate_sha256=hashlib.sha256(raw_b).hexdigest(),
                baseline_source_id=old['source_id'], candidate_source_id=new['source_id'],
                baseline_audit=audit_a, candidate_audit=audit_b,
                baseline_mathematical_projection_sha256=digest(a), candidate_mathematical_projection_sha256=digest(b),
                compared_scalar_leaves=leaves(a), excluded_runtime_metadata=ignored,
                explicit_export_normalizations=schema, separately_audited_added_evidence=added,
                differences=diff))
        except (AssertionError, KeyError, ValueError, TypeError, IndexError) as exc:
            errors.append(dict(space_group=sg, reason=str(exc) or type(exc).__name__))
    equal = bool(rows) and not errors and all(r['literal_mathematical_tree_equal'] for r in rows)
    return dict(schema='fspt-background-literal-mathematical-comparison-v1',
        baseline=str(baseline), candidate=str(candidate), allow_legacy_baseline=allow_legacy_baseline,
        crystalline_spin=crystalline_spin,
        comparison_sha256=hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
        auditor_sha256=hashlib.sha256((Path(__file__).parent/'audit_background_run.py').read_bytes()).hexdigest(),
        common_groups=sorted(A.keys() & B.keys()), candidate_only_groups=sorted(B.keys()-A.keys()),
        expected_candidate_groups=expected_groups,
        pending_expected_candidates=sorted(set(expected_groups or [])-B.keys()),
        unexpected_candidate_groups=sorted(B.keys()-set(expected_groups)) if expected_groups is not None else [],
        baseline_only_groups=sorted(A.keys()-B.keys()), rows=rows, errors=errors,
        compared_groups=len(rows), all_common_groups_literal_equal=equal,
        all_expected_groups_compared_and_equal=(equal and set(expected_groups) == set(B) and set(expected_groups) <= set(A)
                                                if expected_groups is not None else None),
        native_witnesses_compared=True, reference_answers_read=False,
        scope='Recursive equality of every mathematical field, list element and native witness retained in both exports. Excluded runtime metadata, exact schema aliases and new certificates absent in early exports are enumerated per group. This is not merely an invariant-factor comparison.')


def main(argv=None):
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('--baseline', required=True, type=Path)
    p.add_argument('--candidate', required=True, type=Path)
    p.add_argument('--output', required=True, type=Path)
    p.add_argument('--allow-legacy-baseline', action='store_true')
    p.add_argument('--crystalline-spin', choices=['spinless', 'half'], default='spinless')
    p.add_argument('--expected-groups', type=int, nargs='+', help='Record pending expected pilot results explicitly')
    a = p.parse_args(argv)
    if not __debug__:
        p.error('run without Python -O')
    if a.output.exists() or a.output.is_symlink():
        p.error('output exists; preserve previous comparison')
    report = compare(a.baseline, a.candidate, a.allow_legacy_baseline, a.crystalline_spin, a.expected_groups)
    a.output.parent.mkdir(parents=True, exist_ok=True)
    a.output.write_text(json.dumps(report, indent=2, sort_keys=True)+'\n')
    print(json.dumps({key: value for key, value in report.items() if key not in ('rows', 'baseline_only_groups')}, indent=2, sort_keys=True))
    return 0 if report['all_common_groups_literal_equal'] else 1


if __name__ == '__main__':
    raise SystemExit(main())
