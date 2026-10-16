"""End-to-end mixed-root and incoming-gauge checks for the abelian engine."""
import json
from fractions import Fraction
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form
from scripts.classify import gap_literal
from scripts.classify_abelian_4p1 import input_record, parse_factors, launch

ROOT = Path(__file__).resolve().parents[1]


class AbelianInputTests(unittest.TestCase):
    def test_explicit_internal_relative_dictionary(self):
        item = input_record(parse_factors('2x4'))
        self.assertEqual(item['factors'], [2, 4])
        self.assertEqual(item['referenceTarget'], 'internal_abelian_2x4')
        self.assertEqual(item['background'], {'s': 0, 'rho': 0, 'omega': '0'})
        self.assertFalse(item['intrinsicRowIncluded'])
        self.assertEqual(item['physicalSpin'], 'not_applicable')
        for bad in ('1x2', '0x4', '-2x2'):
            with self.assertRaises(ValueError):
                parse_factors(bad)
    def test_missing_native_artifact_finalizes_failed_metadata(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            fake = root / 'fake-gap'
            fake.write_text('#!/bin/sh\nexit 0\n')
            fake.chmod(0o700)
            output = root / 'output'
            output.mkdir()
            run = launch((2, 2), output, {'sha256': 'test-source'}, str(fake),
                         sys.executable, 10, '16g')
            written = json.loads((output / run['id'] / 'run.json').read_text())
            self.assertEqual(written, run)
            self.assertEqual(run['status'], 'failed')
            self.assertEqual(run['exitCode'], 65)
            self.assertEqual(run['processExitCode'], 0)
            self.assertIn('FileNotFoundError', run['artifactError'])
            self.assertFalse((output / run['id'] / 'result.json').exists())


@unittest.skipUnless(shutil.which('gap'), 'GAP/HAP are required')
class AbelianRootTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / 'roots.json'
            driver = Path(directory) / 'roots.g'
            driver.write_text(
                'U1_ROOT:=' + gap_literal(str(ROOT)) + ';;\n'
                'Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n'
                'Read(Concatenation(U1_ROOT,"/gap/abelian4p1.g"));;\n'
                'r:=List([[2],[2,2]],U1AbelianFourData);;\n'
                'c:=U1AbelianFourContext([2,2,2]);;hq:=U1Cohomology(c,4,"Zr");;ho:=U1Cohomology(c,6,"U1s");;\n'
                'maps:=List(hq.generators,q->U1AbelianFourChargeClass(c,ho,q,"compare"));;Add(r,maps);;\n'
                'out:=OutputTextFile(' + gap_literal(str(output)) + ',false);;\n'
                'SetPrintFormattingStatus(out,false);;WriteLine(out,U1JSON(r));;CloseStream(out);;QUIT_GAP(0);\n')
            done = subprocess.run(['gap', '-q', '-b', '--quitonbreak', str(driver)],
                                  capture_output=True, text=True, timeout=180)
            if done.returncode or not output.is_file():
                raise AssertionError(done.stdout + done.stderr)
            cls.cyclic, cls.product, cls.compared_rank3_map = json.loads(output.read_text())

    def test_cyclic_control_and_independent_smith_reduction(self):
        self.assertEqual(self.cyclic['torsion'], [2, 8])
        self.assertEqual(self.cyclic['incomingCohomology'], {'sheet': [], 'charge': []})
        self.assertEqual(self.product['torsion'], [2, 2, 4, 8, 8])
        for item in (self.cyclic, self.product):
            smith = smith_normal_form(Matrix(item['presentation']), domain=ZZ)
            actual = [abs(int(smith[i, i])) for i in range(min(smith.shape)) if abs(smith[i, i]) > 1]
            self.assertEqual(actual, item['torsion'])
            self.assertEqual(item['freeRank'], 0)
            self.assertFalse(item['physicalClassificationCertified'])

    def test_native_degree_four_primary_matches_bar_on_nonzero_map(self):
        # The third C2 factor introduces an integral mixed class with a
        # nonzero terminal charge obstruction, so this is not a zero-map check.
        self.assertTrue(any(any(row) for row in self.compared_rank3_map))

    def test_incoming_h3_really_removes_a_phase(self):
        item = self.product
        self.assertEqual(item['incomingCohomology']['charge'], [2])
        self.assertEqual(item['cohomology']['phase'], [2, 2, 2, 2])
        self.assertEqual(item['finalFiltration']['phase']['torsion'], [2, 2, 2])
        self.assertEqual(item['preIncomingOrder'], 2048)
        self.assertEqual(item['actualGroupOrder'], 1024)
        self.assertTrue(any(any(row) for row in item['incomingRelations']))
        # The nontrivial image is checked at the vacuum and every lower root.
        self.assertEqual(len(item['incomingRelations']), 8)
        self.assertEqual(len({tuple(row) for row in item['incomingRelations']}), 1)

    def test_all_mixed_commutator_witnesses_reconstruct(self):
        item = self.product
        perm = item['outputColumnPermutation']
        original = [[row[perm.index(i + 1)] for i in range(len(perm))]
                    for row in item['presentation']]
        self.assertEqual(len(item['commutatorWitnesses']), 21)
        for witness in item['commutatorWitnesses']:
            actual = list(Matrix([witness['relationCoefficients']]) * Matrix(original))
            self.assertEqual(actual, witness['reducedCoordinates'])
        phase_reductions = [w for w in item['witnesses'] if w['kind'] == 'phase-reduction']
        self.assertGreater(len(phase_reductions), 21)
        # Native integer/phase differential matrices remain available to audit
        # each stored gauge and residual primitive independently of GAP.
        self.assertEqual(len(item['differentialMatrices']['Zs']), 7)
        differential = item['differentialMatrices']['Zs'][4]
        for witness in phase_reductions:
            primitive = [Fraction(x) for x in witness['nativePhasePrimitive']]
            residual = [Fraction(x) for x in witness['nativeResidualPhase']]
            for column, expected in enumerate(residual):
                coboundary = sum(value * differential[row][column]
                                  for row, value in enumerate(primitive))
                self.assertEqual((coboundary - expected) % 1, 0)
        # Each finite sheet root is removed by its stored full integer gauge.
        ns = len(item['group']['factors'])
        for witness in item['witnesses']:
            if witness['kind'] != 'sheet-root':
                continue
            internal = witness['index'] - 1
            is_ci = internal < ns
            output_index = (ns if is_ci else 0) + internal % ns
            root = item['generators'][output_index]['nativeState']
            parameter = witness['nativeCIGauge' if is_ci else 'nativeNeutralGauge']
            target = root['n_p' if is_ci else 'e_p']
            differential = item['differentialMatrices']['Zs'][1]
            for column, value in enumerate(target):
                coboundary = sum(coefficient * differential[row][column]
                                  for row, coefficient in enumerate(parameter))
                self.assertEqual(coboundary + witness['order'] * value, 0)


if __name__ == '__main__':
    unittest.main()
