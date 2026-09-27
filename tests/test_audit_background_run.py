"""Exact algebra and tamper controls for the separate Pin-minus auditor."""
import copy
from functools import lru_cache
import importlib.util
import itertools
import json
from pathlib import Path
import random
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('audit_background_run', ROOT/'scripts/audit_background_run.py')
audit = importlib.util.module_from_spec(spec); spec.loader.exec_module(audit)


@lru_cache(None)
def examples():
    found = {}
    # The public release retains current certificates and the original small
    # legacy-export controls. Development run directories are only fallbacks.
    directories = [
        ROOT/'results/space_groups_spinless',
        ROOT/'results/optimization_validation/background_v3/runs/v1_initial_controls',
        ROOT/'results/optimization_validation/background_v3/runs/v1_baseline',
        ROOT/'runs/spinless_230_v1_20260927T040004Z',
        ROOT/'runs/spinless_full_controls_v1',
    ]
    paths = [path for directory in directories for path in sorted(directory.glob('sg*.json'))]
    for path in paths:
        if '.raw.' in path.name:
            continue
        d = json.loads(path.read_text()); b = d['crystalline_background']; s = d['stacking']
        strict = 'nativeDifferential1F2' in b
        tags = []
        if strict and b['gaugeReducedToZero']:
            tags.append('zero')
            if any(b['nativeOriginalOmega2']):
                tags.append('nontrivial_gauge')
        if strict and 'h0IncomingQuotient' in s:
            tags.append('h0')
        if strict and 'pipExtensionCertificate' in s:
            tags.append('ext')
            if d['pip']['free_rank']:
                tags.append('ext_free')
        if strict and d['pip']['free_rank'] and not b['gaugeReducedToZero']:
            tags.append('free')
        if strict and any('nativeCF3Seed' in g for g in s.get('lower', {}).get('generators', [])):
            tags.append('native_cf')
        if not strict:
            tags.append('legacy')
        for tag in tags:
            found.setdefault(tag, d)
        if len(found) == 8:
            break
    return found


def example(tag):
    if tag not in examples():
        raise unittest.SkipTest('optional saved spinless fixture unavailable: '+tag)
    return copy.deepcopy(examples()[tag])


class ExactExtensionTests(unittest.TestCase):
    def test_rank_and_span(self):
        self.assertEqual(audit.rank2([[1, 1], [1, 0], [0, 1]]), 2)
        self.assertTrue(audit.in_span([[1, 1]], [1, 1]))
        self.assertFalse(audit.in_span([[1, 1]], [1, 0]))

    def test_ext_height_family_against_explicit_smith_enumeration(self):
        from sympy import Matrix, ZZ
        from sympy.matrices.normalforms import smith_normal_form
        rng = random.Random(880721)
        for diagonal in ([2, 4, 8], [3, 6, 12], [2, 8, 0], [1, 2, 0]):
            for trial in range(8):
                n = len(diagonal)
                V = [[int(i == j) for j in range(n)] for i in range(n)]
                for _ in range(5):
                    i, j = rng.sample(range(n), 2)
                    sign = rng.choice((-1, 1))
                    V[i] = [a+sign*b for a, b in zip(V[i], V[j])]
                Vi = audit.inverse(V)
                assert all(x.denominator == 1 for row in Vi for x in row)
                R = [[int(diagonal[i]*x) for x in Vi[i]] for i in range(n)]
                lower = {'smithDiagonal': list(diagonal), 'smithColumnTransform': V,
                         'invariants': [0]*diagonal.count(0)+[x for x in diagonal if x > 1]}
                leading = [rng.randrange(2) for _ in range(n)]
                ambiguous = sorted(rng.sample(range(n), rng.randrange(n+1)))
                expected = audit.extension_options(lower, leading, ambiguous)
                actual = set()
                for bits in itertools.product(range(2), repeat=len(ambiguous)):
                    relation = leading[:]
                    for i, bit in zip(ambiguous, bits):
                        relation[i] += bit
                    presentation = [row+[0] for row in R]+[[-x for x in relation]+[2]]
                    S = smith_normal_form(Matrix(presentation), domain=ZZ)
                    diagonal_smith = [abs(int(S[i, i])) for i in range(n+1)]
                    inv = tuple([0]*diagonal_smith.count(0)+[x for x in diagonal_smith if x > 1])
                    actual.add(inv)
                self.assertEqual({tuple(x) for x in expected['invariantOptions']}, actual)

    def test_same_order_distinct_invariant_factors(self):
        self.assertEqual(audit.canonical_orders([4, 2, 3]), [2, 12])
        self.assertNotEqual(audit.canonical_orders([2, 2]), audit.canonical_orders([4]))

    def test_ambiguous_ext_family_stays_unresolved(self):
        low = {'generators': [{'layer': 0}, {'layer': 2}], 'smithDiagonal': [2, 2],
               'smithColumnTransform': [[1, 0], [0, 1]], 'invariants': [2, 2]}
        family = audit.extension_options(low, [0, 0], [0])
        family.update(method='abelian-Ext1-height-stratification', enumeratedExtensionClasses=0,
                      ambiguousGeneratorIndices=[1], inputRelationModuloAmbiguity=[0, 0], status='ambiguous')
        d = {'pip': {'free_rank': 0}, 'crystalline_background': {'affineCohomologyCoordinates': []},
             'stacking': {'status': 'unresolved', 'fullUpperPhaseWitness': False,
                 'pipExtensionCertificate': family, 'pipSquareCertificate': {
                     'majoranaCoordinates': [0], 'majoranaCohomologyClass': [],
                     'unknownCarries': ['complex-fermion', 'bosonic'], 'fullUpperPhaseWitness': False}}}
        self.assertEqual(audit.check_extension(d, low), 'unresolved-upper-extension-family')
        d['stacking']['invariants'] = [2, 4]
        with self.assertRaisesRegex(AssertionError, 'selected group'):
            audit.check_extension(d, low)

    def test_report_refuses_existing_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            with self.assertRaises(ValueError):
                audit.write_report({}, Path(directory))


class SavedBackgroundTests(unittest.TestCase):
    def test_lower_relation_witness_tamper_rejected(self):
        original = example('native_cf')
        d = copy.deepcopy(original); d['stacking']['lower']['witnesses'].pop()
        with self.assertRaisesRegex(AssertionError, 'lacks its witness'):
            audit.check_background_result(d)
        d = copy.deepcopy(original)
        w = next(w for w in d['stacking']['lower']['witnesses'] if w['certificateLevel'] == 'native-Gu-Wen-doubling-class')
        w['nativeDoublePhase4'][0] = [1, 3]
        with self.assertRaisesRegex(AssertionError, 'doubled phase'):
            audit.check_background_result(d)

    def test_native_generator_seed_tamper_rejected(self):
        original = example('native_cf')
        audit.check_background_result(original)
        index = next(i for i, g in enumerate(original['stacking']['lower']['generators']) if 'nativeCF3Seed' in g)
        for field, value in [('nativeCF3Seed', []), ('nativePhase4Seed', []), ('construction', 'unknown')]:
            with self.subTest(field=field):
                d = copy.deepcopy(original)
                d['stacking']['lower']['generators'][index][field] = value
                with self.assertRaises(AssertionError):
                    audit.check_background_result(d)
        d = copy.deepcopy(original)
        g = d['stacking']['lower']['generators'][index]
        g['nativePhase4Seed'][0] = [2, 4]
        with self.assertRaisesRegex(AssertionError, 'not canonical'):
            audit.check_background_result(d)
        d = copy.deepcopy(original)
        del d['stacking']['lower']['generators'][index]['nativePhase4Seed']
        with self.assertRaisesRegex(AssertionError, 'lacks both'):
            audit.check_background_result(d)

    def test_current_strict_examples(self):
        for tag in ('zero', 'nontrivial_gauge', 'h0', 'ext', 'free'):
            d = example(tag)
            result = audit.check_background_result(d)
            self.assertFalse(result['missing_evidence'])
            if tag == 'ext':
                self.assertFalse(result['marked_witnesses'])
                self.assertEqual(result['kind'], 'abstract-upper-family-single-group')

    def test_legacy_is_explicitly_incomplete(self):
        d = example('legacy')
        with self.assertRaisesRegex(AssertionError, 'legacy'):
            audit.check_background_result(d)
        self.assertTrue(audit.check_background_result(d, strict_background=False)['missing_evidence'])

    def test_pin_cocycle_requires_actual_spin_lift(self):
        d = example('h0'); b = d['crystalline_background']
        b['omegaTable'] = [[0]*b['pointOrder'] for _ in range(b['pointOrder'])]
        with self.assertRaisesRegex(AssertionError, 'Pin cocycle differs'):
            audit.check_background_result(d)

    def test_native_gauge_tamper_rejected(self):
        d = example('nontrivial_gauge'); b = d['crystalline_background']
        b['trivializingNative1'] = [0]*len(b['trivializingNative1'])
        with self.assertRaisesRegex(AssertionError, 'gauge coboundary'):
            audit.check_background_result(d)

    def test_native_h2_missing_basis_rejected(self):
        d = example('h0'); b = d['crystalline_background']
        b['nativeH2Generators'][0] = [0]*len(b['nativeOriginalOmega2'])
        with self.assertRaisesRegex(AssertionError, 'H2 basis'):
            audit.check_background_result(d)

    def test_h0_append_and_intersection_tamper_rejected(self):
        d = example('h0'); q = d['stacking']['h0IncomingQuotient']['backgroundQuotient']
        q['incomingCoordinates'] = [0]*len(q['incomingCoordinates'])
        with self.assertRaisesRegex(AssertionError, 'append'):
            audit.check_background_result(d)
        d = example('h0'); record = d['stacking']['h0IncomingQuotient']['backgroundQuotient']['filtration'][0]
        record['relationCombinationRows'][0][0] += 1
        with self.assertRaisesRegex(AssertionError, 'saturated Smith kernel'):
            audit.check_background_result(d)

    def test_ext_family_tamper_and_false_witness_rejected(self):
        d = example('ext'); f = d['stacking']['pipExtensionCertificate']
        f['possibleHeights'] = [0]
        with self.assertRaisesRegex(AssertionError, 'Ext-family'):
            audit.check_background_result(d)
        d = example('ext'); d['stacking']['fullUpperPhaseWitness'] = True
        with self.assertRaises(AssertionError):
            audit.check_background_result(d)

    def test_free_candidate_and_lift_mismatch_rejected(self):
        d = example('free'); f = d['pip']['free_lattice']
        f['generators'][0]['integer1'][0] += 1
        with self.assertRaisesRegex(AssertionError, 'integer cochain'):
            audit.check_background_result(d)
        d = example('free'); f = d['pip']['free_lattice']
        f['parityCandidates'][-1]['status'] = 'killed'
        with self.assertRaises((AssertionError, KeyError)):
            audit.check_background_result(d)


if __name__ == '__main__':
    unittest.main()
