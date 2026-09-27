#!/usr/bin/env python3
"""Static C4 pullback audit, with an explicitly external physical input.

No cochains are recomputed. This checks archived character/gauge certificates
and that the reviewed natural factories use identical frozen source bytes.
The physical input is a published S4 result, not the program's finite answer.
"""
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES = ('pip_stacking.g', 'pip_c4_data.g', 'pip_coordinates.g', 'pip_diagonal_data.g')


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def read_archived(folder, name, manifest):
    raw = (folder / name).read_bytes()
    if sha(raw) != manifest['files'][name]['sha256']:
        raise ValueError('archived file hash mismatch: ' + name)
    return json.loads(raw), sha(raw)


def frozen_sources(folder, manifest):
    answer = {}
    for name in SOURCES:
        path = 'source/gap/' + name
        raw = (folder / path).read_bytes()
        digest = sha(raw)
        if digest != manifest['files'][path]['sha256']:
            raise ValueError('frozen natural-factory source hash mismatch')
        answer[name] = digest
    return answer


def check_character(d):
    g = d['stacking']['pipGenerator']
    c = g['C4PullbackCertificate']
    t, s = c['nativeCharacter1'], c['orientationReduction']
    if (c['modulus'] != 4 or not any(x % 2 for x in t)
            or [x % 2 for x in t] != s or [x % 2 for x in g['integer1']] != s
            or any(x % 4 for x in c['integerCharacterDifferential'])
            or c['universalFlatTower'] != 'gap/pip_c4_data.g'
            or g['construction'] != 'proved-orientation-character-pullback-of-complete-universal-C4-tower'):
        raise ValueError('native character certificate is inconsistent')
    return c


def check_extension_gauge(d):
    b = d['crystalline_background']
    if not b['gaugeReducedToZero'] or any(b['affineCohomologyCoordinates']):
        raise ValueError('nonzero background is not certified trivialized')
    lam, matrix, w = b['trivializingNative1'], b['nativeDifferential1F2'], b['nativeOriginalOmega2']
    if len(lam) != len(matrix) or any(len(row) != len(w) for row in matrix):
        raise ValueError('background primitive dimensions differ')
    if [sum(lam[i] * matrix[i][j] for i in range(len(lam))) % 2
            for j in range(len(w))] != w:
        raise ValueError('native background primitive does not differentiate to omega')
    if b['trivializationRecipe'] != 'AFSSolve on the original Pin-minus pullback, including comparison homotopy':
        raise ValueError('exact bar primitive reconstruction is not specified')
    return dict(native_primitive=lam, native_omega=w,
                native_equation_independently_checked=True,
                bar_primitive_recipe=b['trivializationRecipe'],
                scope='central-extension gauge equivalence; relation remains in the saved zero-background gauge')


def main():
    point = ROOT / 'results/point_groups'
    pm = json.loads((point / 'archive.json').read_bytes())
    pg, pgsha = read_archived(point, 'half_pg10.json', pm)
    s = pg['stacking']
    if (pg['point_group']['hermannMauguin'] != '-4'
            or pg['point_group']['order'] != 4
            or pg['point_group']['translationSubgroupPresent']
            or pg['crystalline_spin'] != 'half'
            or pg['pip']['orders'] != [2] or pg['majorana'] != []
            or pg['complex_fermion'] != [2] or pg['bosonic'] != []
            or s['lower']['invariants'] != [2]
            or len(s['lower']['generators']) != 1
            or s['lower']['generators'][0]['layer'] != 1
            or s['fullPresentation'] != [[2, 0], [-1, 2]]):
        raise ValueError('finite candidate does not have the required unique nonzero CF square')
    check_character(pg)
    common = frozen_sources(point, pm)
    rows, archives = {}, {}
    for key, directory in [('spin_half', 'space_groups'), ('spinless', 'space_groups_spinless')]:
        folder = ROOT / 'results' / directory
        raw = (folder / 'archive.json').read_bytes()
        manifest = json.loads(raw)
        if frozen_sources(folder, manifest) != common:
            raise ValueError('finite and affine pullback/square formulas differ')
        archives[key] = dict(source_id=manifest['source_id'], archive_sha256=sha(raw))
        items = []
        for number in range(1, 231):
            d, digest = read_archived(folder, 'sg%d.json' % number, manifest)
            if 'C4PullbackCertificate' not in d['stacking'].get('pipGenerator', {}):
                continue
            c = check_character(d)
            item = dict(space_group=number, result_sha256=digest,
                        native_character=c['nativeCharacter1'],
                        native_character_differential=c['integerCharacterDifferential'],
                        orientation_native=c['orientationReduction'],
                        marked_square=[-x for x in d['stacking']['fullPresentation'][-1][:-1]],
                        lower_generator_names=[g['name'] for g in d['stacking']['lower']['generators']],
                        full_invariants=d['stacking']['invariants'])
            if key == 'spinless':
                item['background_gauge'] = check_extension_gauge(d)
            items.append(item)
        rows[key] = items
    if len(rows['spin_half']) != 26 or len(rows['spinless']) != 6:
        raise ValueError('C4 pullback cohort size changed')
    result = dict(schema=1, scope='static archived-certificate audit plus the stated mathematical naturality argument',
        new_gap_computation=False, new_bar_evaluation=False,
        script_sha256=sha(Path(__file__).read_bytes()), archives=archives,
        physical_input=dict(doi='10.1103/PhysRevX.15.031029',
            pdf_sha256='eda983b3c093877d7b6d34da1092ae8c8c5dc272746e6f4eaf28f35a7438c692',
            full_group_source='Table I (page 4), crystalline spin-half S4; independent real-space argument in section III B (pages 11-13)',
            full_group=[4],
            filtration_source='Table III (page 51), internal-spinless S4 panel; also independently computed by known lower-sector operations',
            layers={'pip': [2], 'majorana': [], 'complex_fermion': [2], 'bosonic': []},
            interpretation='S4 means the geometric fourfold roto-reflection, abstractly cyclic order four, not the permutation group',
            input_independent_of_selected_Gamma=True),
        finite_candidate=dict(path='results/point_groups/half_pg10.json', sha256=pgsha,
            source_id=pg['source_id'], archive_sha256=sha((point / 'archive.json').read_bytes()),
            purpose='checks the selected natural square represents the unique nonzero CF class; not the physical justification'),
        common_frozen_natural_sources=common, groups=rows,
        conclusion='Given crystalline equivalence, the published S4 physical result, the known lower-sector identification and stacking naturality, these 26+6 torsion square classes are fixed independently of the unspecified general upper twisters.',
        limits=['No arbitrary upper product or full coherence theorem is derived.',
                'Character differential values are retained archived certificates; this static audit does not reconstruct their resolution matrices.',
                'Spinless relations are certified in the stored trivialized-extension gauge, not newly transformed into original Pin-minus cochain coordinates.',
                'Other affine torsion cases and the sixteen marked-unknown cases are not certified by this C4 argument.'])
    out = ROOT / 'results/upper_carry_scope/c4_naturality_calibration.json'
    out.write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    print(out)


if __name__ == '__main__':
    main()
