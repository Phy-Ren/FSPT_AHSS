"""Finite simplicial classifying-space, integral gauge, and mixed stacking tests."""
from copy import deepcopy
import unittest

from sympy import Matrix

from insulator import api as ci
from insulator import e8
from insulator.translation4p1 import (
    SimplicialTorus, calculate, stack_coordinates, straightened_charge, verify_certificate,
)


class TranslationFourDataTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results = {rank: calculate(rank) for rank in (1, 2, 3, 4)}

    def test_full_integer_kernel_and_independent_stable_splitting_targets(self):
        # Independent stable torus splitting, not supplied to the solver.
        targets = {1: 0, 2: 2, 3: 6, 4: 13}
        for rank, target in targets.items():
            classification, evidence = self.results[rank]
            with self.subTest(rank=rank):
                replay = verify_certificate(classification, evidence)
                self.assertEqual(replay["status"], "PASS")
                self.assertFalse(replay["referenceGroupUsed"])
                self.assertEqual(classification["freeRank"], target)
                self.assertFalse(classification["physicalClassificationCertified"])
                self.assertEqual(evidence["resolution"]["cellCounts"][rank + 1:], [0] * (6 - rank))

    def test_integral_canonicalization_covers_arbitrary_gauge_representatives(self):
        torus = SimplicialTorus(4)
        for degree in (1, 2, 3, 4):
            periods = Matrix([(-1) ** i * (i + 2) for i in range(torus.basis[degree].cols)])
            gauge = Matrix([i % 7 - 3 for i in range(len(torus.cells[degree - 1]))])
            cochain = torus.basis[degree] * periods + torus.d[degree - 1] * gauge
            actual, removal = torus.canonicalize(degree, cochain)
            self.assertEqual(actual, periods)
            self.assertEqual(cochain - torus.d[degree - 1] * removal, torus.basis[degree] * periods)
        self.assertGreater(torus.d[1].rank(), 0)
        self.assertGreater(torus.d[3].rank(), 0)

    def test_mixed_ci_product_is_nonzero_and_straightening_is_integral(self):
        result, _ = self.results[4]
        polarizer = result["coordinateStacking"]["sheetPolarizer"]
        # Basis order is 01,02,03,12,13,23. A pair of transverse CI sheets
        # generates charge, including the orientation-sensitive negative term.
        self.assertEqual(polarizer[0][5], [1])
        self.assertEqual(polarizer[1][4], [-1])
        self.assertEqual(polarizer[2][3], [1])
        a = ([0] * 6, [2, -1, 3, 1, -2, 4], [7])
        b = ([0] * 6, [-1, 2, 1, -3, 2, 5], [-4])
        stacked = stack_coordinates(a, b, polarizer)
        self.assertEqual(straightened_charge(stacked[1], stacked[2], polarizer),
                         [straightened_charge(a[1], a[2], polarizer)[0]
                          + straightened_charge(b[1], b[2], polarizer)[0]])
        square = stack_coordinates(a, a, polarizer)
        self.assertEqual(straightened_charge(square[1], square[2], polarizer),
                         [2 * straightened_charge(a[1], a[2], polarizer)[0]])

    def test_public_full_state_product_on_every_top_simplex(self):
        torus = SimplicialTorus(4)
        a = torus.basis[2] * Matrix([2, -1, 0, 3, 1, -2])
        b = torus.basis[2] * Matrix([-1, 2, 1, 0, -3, 1])
        expected = torus.api_sheet_product(a, b)
        actual = []
        for cell in torus.cells[4]:
            zero = lambda degree: ci.Cochain(4, degree, {})
            symmetry = ci.Symmetry(zero(2), zero(1), zero(1))
            left = e8.State(zero(2), torus.pullback(2, a, cell), zero(4), zero(5))
            right = e8.State(zero(2), torus.pullback(2, b, cell), zero(4), zero(5))
            result = left.stack(right, symmetry, 4)
            actual.append(result.n_p2(tuple(range(5))))
            self.assertFalse(result.nu_p3.v)
        self.assertEqual(Matrix(actual), expected)

    def test_corrupted_gauge_and_omitted_product_are_rejected(self):
        result, evidence = self.results[4]
        corrupted = deepcopy(evidence)
        # This product genuinely requires an integer charge gauge correction.
        item = next(row for row in corrupted["completedIntegerProducts"]
                    if any(row["chargeGaugeRemoval"]))
        # A closed unit parameter would be invisible; perturb a parameter
        # with an explicitly nonzero coboundary instead.
        torus = SimplicialTorus(4)
        column = next(i for i in range(torus.d[3].cols) if any(torus.d[3][:, i]))
        item["chargeGaugeRemoval"][column] += 1
        with self.assertRaises(ValueError):
            verify_certificate(result, corrupted)
        omitted = deepcopy(evidence)
        omitted["completedIntegerProducts"].pop()
        with self.assertRaises(ValueError):
            verify_certificate(result, omitted)
        wrong_group = deepcopy(result)
        wrong_group["freeRank"] -= 1
        with self.assertRaises(ValueError):
            verify_certificate(wrong_group, evidence)
        wrong_filtration = deepcopy(result)
        wrong_filtration["finalFiltration"]["e"]["freeRank"] -= 1
        wrong_filtration["finalFiltration"]["n"]["freeRank"] += 1
        with self.assertRaises(ValueError):
            verify_certificate(wrong_filtration, evidence)
        wrong_generator = deepcopy(result)
        wrong_generator["generators"][0]["coordinates"] = [0, 2]
        with self.assertRaises(ValueError):
            verify_certificate(wrong_generator, evidence)
        missing_generator = deepcopy(result)
        missing_generator["generators"].pop()
        with self.assertRaises(ValueError):
            verify_certificate(missing_generator, evidence)

    def test_dimension_and_nonintegral_inputs_are_rejected(self):
        for rank in (0, 5, 1.0, True):
            with self.assertRaises(ValueError):
                SimplicialTorus(rank)
        torus = SimplicialTorus(2)
        with self.assertRaises(ValueError):
            torus.canonicalize(2, Matrix([1, 1]) / 2)


if __name__ == "__main__":
    unittest.main()
