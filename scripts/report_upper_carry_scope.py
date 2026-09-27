#!/usr/bin/env python3
"""Read immutable archives and audit upper-carry presentation choices.

Only finite integer presentation algebra is recomputed. No GAP, cochains,
reference classification answers, or physical product is evaluated.
"""
import hashlib
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.stacking import invariant_factors


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def rank2(rows):
    basis = {}
    for row in rows:
        x = sum((v % 2) << i for i, v in enumerate(row))
        while x:
            pivot = x.bit_length() - 1
            if pivot in basis:
                x ^= basis[pivot]
            else:
                basis[pivot] = x
                break
    return len(basis)


def independent_rows2(rows):
    """Return original row indices spanning the same binary row space."""
    chosen = []
    for i, row in enumerate(rows):
        if rank2([rows[j] for j in chosen] + [row]) > len(chosen):
            chosen.append(i)
    return chosen


def load_archive(folder):
    raw = (folder / 'archive.json').read_bytes()
    manifest = json.loads(raw)
    result = []
    for number in range(1, 231):
        name = 'sg%d.json' % number
        blob = (folder / name).read_bytes()
        d = json.loads(blob)
        if (sha(blob) != manifest['files'][name]['sha256']
                or d['space_group'] != number
                or d['source_id'] != manifest['source_id']):
            raise ValueError('archive identity mismatch: ' + name)
        result.append((d, sha(blob)))
    return result, {'source_id': manifest['source_id'], 'archive_sha256': sha(raw)}


def ambiguity(lower):
    v, diagonal = lower['smithColumnTransform'], lower['smithDiagonal']
    indices = [i for i, g in enumerate(lower['generators']) if g['layer'] < 2]
    active = [j for j in range(len(v)) if j >= len(diagonal) or diagonal[j] % 2 == 0]
    rows = [[v[i][j] % 2 for j in active] for i in indices]
    return indices, active, rows


def named(row, generators):
    return {g['name']: x for g, x in zip(generators, row) if x}


def extension(lower, square, free_rank):
    matrix = [row + [0] for row in lower['presentation']]
    matrix.append([-x for x in square] + [2])
    return [0] * free_rank + invariant_factors(matrix, len(square) + 1)


def run():
    half, half_source = load_archive(ROOT / 'results/space_groups')
    spinless, spinless_source = load_archive(ROOT / 'results/space_groups_spinless')
    # Public factual catalogue, containing no classification/stacking answers.
    name_file = ROOT / 'fspt/data/space_group_names.json'
    name_raw = name_file.read_bytes()
    catalog = json.loads(name_raw)['groups']
    names = {entry['number']: entry['name_tex'] for entry in catalog}
    if set(names) != set(range(1, 231)):
        raise ValueError('space-group name coverage differs from 230')
    family_rows, half_rows, nonzero_rows = [], [], []
    for d, digest in spinless:
        s = d['stacking']
        if 'pipExtensionCertificate' not in s:
            continue
        lower, cert = s['lower'], s['pipExtensionCertificate']
        indices, active, rows = ambiguity(lower)
        if ([i + 1 for i in indices] != cert['ambiguousGeneratorIndices']
                or [i + 1 for i in active] != cert['modTwoCyclicColumns']
                or rows != cert['modTwoAmbiguityRows']
                or len(cert['invariantOptions']) != 1
                or s['fullUpperPhaseWitness'] is not False):
            raise ValueError('upper family certificate mismatch')
        square = cert['inputRelationModuloAmbiguity']
        zero_model = extension(lower, square, s['freePipRank'])
        if zero_model != s['invariants']:
            raise ValueError('zero-carry example has another abstract type')
        directions = [i for i, row in zip(indices, rows) if any(row)]
        if not directions:
            raise ValueError('expected nontrivial fixed-lower extension ambiguity')
        alternate = list(square)
        alternate[directions[0]] += 1
        if extension(lower, alternate, s['freePipRank']) != s['invariants']:
            raise ValueError('explicit nonzero-carry example changes claimed unique type')
        # Ext^1(Z/2,H)=H/2H. Enumerate a basis of the entire allowed image,
        # not every redundant generator coefficient. This is at most 32 small
        # integer Smith forms in these sixteen cases, with no cochain work.
        independent = independent_rows2(rows)
        all_options = set()
        for mask in range(1 << len(independent)):
            candidate = list(square)
            for bit, j in enumerate(independent):
                if (mask >> bit) & 1:
                    candidate[indices[j]] += 1
            all_options.add(tuple(extension(lower, candidate, s['freePipRank'])))
        if all_options != {tuple(s['invariants'])}:
            raise ValueError('full allowed carry fiber has another abstract type')
        family_rows.append(dict(space_group=d['space_group'], name_tex=names[d['space_group']],
            result_sha256=digest, lower_invariants=lower['invariants'],
            lower_generators=[dict(name=g['name'], layer=g['layer']) for g in lower['generators']],
            leading_majorana_square=named(square, lower['generators']),
            unknown_carry_names=[lower['generators'][i]['name'] for i in indices],
            ambiguity_dimension_mod_2H=rank2(rows),
            fixed_lower_extension_classes=2 ** rank2(rows),
            independently_replayed_carry_classes=1 << len(independent),
            independent_carry_generators=[lower['generators'][indices[j]]['name'] for j in independent],
            independently_replayed_invariant_options=[list(v) for v in sorted(all_options)],
            mod_two_ambiguity_rows=rows, possible_heights=cert['possibleHeights'],
            all_carry_invariant_options=cert['invariantOptions'],
            free_pip_rank=s['freePipRank'], full_invariants=s['invariants'],
            zero_carry_example_invariants=zero_model,
            alternate_example_carry=lower['generators'][directions[0]]['name'],
            alternate_example_same_isotype=True,
            zero_carry_example_is_not_an_actual_marked_relation=True))
    for d, digest in half:
        s = d['stacking']
        if not s.get('fullUpperPhaseWitness'):
            continue
        lower = s['lower']
        # pipRelation.lowerCoordinates stores only the CF/bosonic prefix;
        # the full presentation supplies the complete marked lower row.
        square = [-x for x in s['fullPresentation'][-1][:-1]]
        if len(square) != len(lower['generators']):
            raise ValueError('full upper relation width mismatch')
        indices, active, rows = ambiguity(lower)
        zero_model = extension(lower, [0] * len(square), s['freePipRank'])
        c4 = 'C4PullbackCertificate' in s['pipGenerator']
        entry = dict(space_group=d['space_group'], name_tex=names[d['space_group']],
            result_sha256=digest, actual_model_square=named(square, lower['generators']),
            lower_invariants=lower['invariants'], full_model_invariants=s['invariants'],
            deleting_all_final_carries_invariants=zero_model,
            deleting_all_final_carries_changes_isotype=zero_model != s['invariants'],
            ambiguity_dimension_if_both_upper_products_withdrawn=rank2(rows),
            universal_C4_pullback=c4,
            physical_scope='Computed relation under the selected calibrated product; closure alone does not identify the physical product.')
        half_rows.append(entry)
        if any(square):
            bos = [x if g['layer'] == 0 else 0 for g, x in zip(lower['generators'], square)]
            no_bos = [x - b for x, b in zip(square, bos)]
            image = [sum(bos[i] * lower['smithColumnTransform'][i][j]
                         for i in range(len(bos))) % 2 for j in active]
            entry = dict(entry, bosonic_final_coordinates=named(bos, lower['generators']),
                deleting_only_final_bosonic_carries_invariants=extension(lower, no_bos, s['freePipRank']),
                bosonic_difference_mod_2H=image,
                bosonic_difference_in_2H=not any(image))
            nonzero_rows.append(entry)
    if len(family_rows) != 16 or len(half_rows) != 32 or len(nonzero_rows) != 12:
        raise ValueError('unexpected cohort size')
    cohorts = {}
    for key, data in [('spin_half', half), ('spinless', spinless)]:
        free = {d['space_group'] for d, _ in data if d['pip']['free_rank']}
        torsion = {d['space_group'] for d, _ in data if any(v > 1 for v in d['pip']['orders'])}
        groups = {'free': free, 'torsion': torsion, 'free_and_torsion': free & torsion,
                  'free_only': free-torsion, 'torsion_only': torsion-free,
                  'nonzero_pip': free|torsion, 'zero_pip': set(range(1,231))-(free|torsion)}
        cohorts[key] = {name: {'count': len(values),
            'groups': [{'space_group': n, 'name_tex': names[n]} for n in sorted(values)]}
            for name, values in groups.items()}
    return dict(schema=1, scope='immutable-archive-presentation-algebra; no cochain product modification',
        new_GAP_computation=False, new_cochain_evaluation=False,
        archives={'spin_half': half_source, 'spinless': spinless_source},
        name_source={'path': str(name_file.relative_to(ROOT)), 'sha256': sha(name_raw),
                     'fields_read': 'space-group number and name only'},
        script_sha256=sha(Path(__file__).read_bytes()),
        pip_cohorts=cohorts,
        spinless_sixteen=family_rows, spin_half_upper_model_scope=half_rows,
        spin_half_nonzero_final_relations=nonzero_rows,
        distinction='Deleting final reduced relation coefficients is not setting a raw cochain twister to zero. Alternative algebraic extension classes are not automatically realizable by natural coherent physical products.')


if __name__ == '__main__':
    output = ROOT / 'results/upper_carry_scope/presentation_audit.json'
    data = run()
    output.parent.mkdir(parents=True, exist_ok=True)
    output.write_text(json.dumps(data, indent=2, sort_keys=True) + '\n')
    print(output)
