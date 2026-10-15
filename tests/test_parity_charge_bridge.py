"""Independent signed parity equations versus the charge-conserving API."""
from fractions import Fraction as F
import random
import unittest

from insulator import api as ci
from insulator import parity_bridge as bridge
from insulator._engine.simplex import rand, char, bin0, Fopen


class ChargeCircleBridge(unittest.TestCase):
    def test_source_product_gauge_and_open_remainder(self):
        rng = random.Random(2026101501)
        for d in (2, 3, 4):
            for case in range(8):
                with self.subTest(d=d, case=case):
                    N = d + 2
                    s = [rng.randrange(2) for _ in range(N + 1)]
                    rho = [rng.randrange(2) for _ in range(N + 1)]
                    chi = [a ^ b for a, b in zip(s, rho)]
                    X = rand(N, 1, chi, rng).sc(F(1, 7))
                    W = rand(N, 1, None, rng).d().mod(2)
                    M = W.ret(chi) + rand(N, 2, chi, rng).sc(2)
                    bg = ci.Symmetry((M - X.d()).sc(F(1, 2)),
                                     char(N, s).ret(s), char(N, rho).ret(rho))
                    self.assertEqual((bridge.circle_carry(bg, X) - M).maxabs(), 0)
                    self.assertEqual((bridge.parity_extension(bg, X) - W).maxabs(), 0)
                    z = rand(N, d - 1, rho, rng).d()
                    zp = rand(N, d - 1, rho, rng).d()
                    u = rand(N, d - 1, rho, rng)
                    def R(value):
                        return bridge.charge_phase_correction(bg, X, value)
                    def parity_source(value):
                        return (W.cup(bin0(value)) + bin0(value).sq(2)).sc(F(1, 2)).ret(s)
                    residual = parity_source(z) - ci.charge_source(bg, z) - R(z).d()
                    self.assertEqual(residual.mod(1).maxabs(), 0)
                    residual = (ci.charge_product(bg, z, zp)
                                - Fopen(bin0(z), bin0(zp)).ret(s) + R(z + zp) - R(z) - R(zp))
                    self.assertEqual(residual.mod(1).maxabs(), 0)
                    parity_gauge = ((W.cup(bin0(u)) + bin0(u).sq(2)).sc(F(1, 2))
                                    + Fopen(bin0(z), bin0(u).d())).ret(s)
                    residual = (ci.charge_gauge(bg, z, u) + R(z + u.d()) - R(z)
                                - parity_gauge - bridge.charge_gauge_phase(bg, X, u).d())
                    self.assertEqual(residual.mod(1).maxabs(), 0)
                    opened = rand(N, d, rho, rng)
                    with self.assertRaises(ValueError):
                        R(opened)
                    residual = (parity_source(opened) - ci.charge_source(bg, opened)
                                - X.cup(opened).sc(F(1, 2)).d()
                                - X.cup(opened.d()).sc(F(1, 2)))
                    self.assertEqual(residual.mod(1).maxabs(), 0)


if __name__ == '__main__':
    unittest.main()
