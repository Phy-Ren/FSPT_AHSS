"""Numerical regression for exact simplex kernel geometry and scalar storage.

The independent oracle expands face cuts afresh. In particular, it does not
share the optimized geometry cache or reduce cochain values to residue classes.
"""
import random
import unittest
from fractions import Fraction
from itertools import combinations

from insulator._engine.simplex import C
from insulator._engine.cochains import interval_cuts


class ExactSimplexKernel(unittest.TestCase):
    def test_signed_rational_geometry_against_direct_face_expansion(self):
        rng = random.Random(105142026)
        scalars = [0, 1, -1, 3, -7, Fraction(0), Fraction(3), Fraction(-11),
                   Fraction(1, 2), Fraction(-5, 3), Fraction(7, 12),
                   Fraction(10 ** 30 + 1, 17)]
        comparisons = 0
        noncommuting = 0
        for N in range(1, 7):
            for p in range(N + 1):
                for _ in range(3):
                    tw = tuple(rng.randrange(2) for _ in range(N + 1))
                    values = {f: rng.choice(scalars)
                              for f in combinations(range(N + 1), p + 1)
                              if rng.randrange(3)}
                    a = C(N, p, values, tw)
                    self.assertEqual(a.v, values)
                    expected_d = {}
                    for f in combinations(range(N + 1), p + 2):
                        expected_d[f] = sum(
                            (-1) ** j * ((-1) ** (tw[f[0]] + tw[f[1]])
                                         if j == 0 else 1)
                            * values.get(f[:j] + f[j + 1:], 0)
                            for j in range(len(f)))
                    self.assertEqual(a.d().v, expected_d)
                    comparisons += 1
                    for q in range(N + 1):
                        bt = tuple(rng.randrange(2) for _ in range(N + 1))
                        other = {f: rng.choice(scalars)
                                 for f in combinations(range(N + 1), q + 1)
                                 if rng.randrange(3)}
                        b = C(N, q, other, bt)
                        for i in range(min(p, q) + 1):
                            D = p + q - i
                            if D > N:
                                continue
                            for binary in (False, True):
                                expected = {}
                                for f in combinations(range(N + 1), D + 1):
                                    value = 0
                                    for left, right, sign in interval_cuts(p, q, i):
                                        ff = tuple(f[j] for j in left)
                                        gg = tuple(f[j] for j in right)
                                        action = 1 if binary else sign * (-1) ** (
                                            tw[f[0]] + tw[ff[0]]
                                            + bt[f[0]] + bt[gg[0]])
                                        value += action * values.get(ff, 0) * other.get(gg, 0)
                                    expected[f] = value % 2 if binary else value
                                result = a.cup(b, i, binary)
                                self.assertEqual(result.v, expected)
                                self.assertEqual(result.tw, tuple(x ^ y for x, y in zip(tw, bt)))
                                comparisons += 1
                        if p + q <= N and a.cup(b).v != b.cup(a).v:
                            noncommuting += 1
        self.assertEqual(comparisons, 1335)
        self.assertEqual(noncommuting, 183)


if __name__ == '__main__':
    unittest.main()
