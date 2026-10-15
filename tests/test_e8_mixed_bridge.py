"""Executable mixed source/product/prism identities; no parity dependency."""
from fractions import Fraction as F
import random
import unittest

from insulator._engine import e8_4p1 as neutral
from insulator._engine.simplex import C, rand
from insulator.parity_bridge import (
    e8_ci_source_bridge_4p1,
    e8_ci_product_bridge_4p1,
    e8_ci_gauge_bridge_4p1,
)


class MixedBridge(unittest.TestCase):
    def test_source_product_and_gauge_with_independent_integer_sheets(self):
        rng = random.Random(164004)
        for _ in range(6):
            N = 6
            sign = (0,) + tuple(rng.randrange(2) for _ in range(N))
            e, n, f, m = [rand(N, 1, sign, rng).d() for _ in range(4)]
            a, b = n.sc(2), m.sc(2)
            r = e8_ci_source_bridge_4p1(e, n)
            cube = lambda x: x.cup(x).cup(x).sc(F(1, 12))
            residual = cube(a + e.sc(16)) - cube(a) - neutral.source(e) - r.d()
            self.assertEqual(residual.mod(1).maxabs(), 0)

            p = neutral.product
            product_residual = (p(a, b) + p(e, f) + p(a + b, e + f)
                                - p(a, e) - p(b, f) - p(a + e, b + f))
            k = e8_ci_product_bridge_4p1(e, n, f, m)
            self.assertEqual((k.d() - product_residual).mod(1).maxabs(), 0)

            v, u = rand(N, 1, sign, rng), rand(N, 1, sign, rng)
            h = e8_ci_gauge_bridge_4p1(e, n, v, u)
            gauge_residual = (neutral.gauge(a, u.sc(2)) + neutral.gauge(e, v)
                              + p(a + u.d().sc(2), e + v.d()) - p(a, e)
                              - neutral.gauge(a + e, u.sc(2) + v))
            self.assertEqual((h.d() - gauge_residual).mod(1).maxabs(), 0)

    def test_open_and_fractional_sheets_are_rejected(self):
        rng = random.Random(165001)
        sign = (0, 1, 0, 1, 0, 1, 0)
        e = rand(6, 1, sign, rng).d()
        open_n = rand(6, 2, sign, rng)
        self.assertNotEqual(open_n.d().maxabs(), 0)
        with self.assertRaises(ValueError):
            e8_ci_source_bridge_4p1(e, open_n)
        fractional_n = C(6, 1, {(1, 2): 1}, sign).d().sc(F(1, 2))
        self.assertEqual(fractional_n.d().maxabs(), 0)
        with self.assertRaises(ValueError):
            e8_ci_source_bridge_4p1(e, fractional_n)
        with self.assertRaises(ValueError):
            e8_ci_product_bridge_4p1(e, fractional_n, e, e)


if __name__ == '__main__':
    unittest.main()
