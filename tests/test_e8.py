"""E8 completion, exact gauges, cyclic extensions, and infinite presentations."""
from dataclasses import replace
from fractions import Fraction as F
from itertools import combinations, product
import random
import unittest

from insulator import api as ci
from insulator.e8 import State, source, thermal_sheet
from insulator.e8_h1 import twisted_h1
from insulator._engine import e8_4p1 as e8
from insulator._engine.simplex import C, char, primitive, rand


def complete(d, rng, signs=None):
    N = d + 2
    s = signs if signs is not None else [0] + [rng.randrange(2) for _ in range(N)]
    if d == 2:
        s = [0] * (N + 1)
    r = [0] + [rng.randrange(2) for _ in range(N)]
    omega_sign = [x ^ y for x, y in zip(s, r)]
    bg = ci.Symmetry(rand(N, 2, omega_sign, rng)
                     + rand(N, 1, omega_sign, rng).d().sc(F(1, 5)),
                     char(N, s).ret(s), char(N, r).ret(r))
    def sheet():
        if d == 2:
            return C(N, 0, {(i,): 3 for i in range(N + 1)}, s)
        return rand(N, d - 3, s, rng).d()
    e, n = sheet(), sheet()
    charge = primitive(ci.integer_obstruction(bg, d, n)) + rand(N, d - 1, r, rng).d()
    phase = primitive(source(bg, d, e, n, charge)).mod(1)
    return bg, State(e, n, charge, phase)


class E8Operations(unittest.TestCase):
    def test_completed_states_all_dimensions(self):
        rng = random.Random(20261015)
        for d in (2, 3, 4):
            for _ in range(3):
                bg, state = complete(d, rng)
                state.validate(bg, d)
                state.stack(state, bg, d).validate(bg, d)
                other_e = (state.e_p.sc(-2) if d == 2
                           else rand(state.e_p.N, d - 3, bg.s1.tw, rng).d())
                other = State(other_e, state.n_p, state.n_p2,
                              primitive(source(bg, d, other_e, state.n_p, state.n_p2)).mod(1))
                state.stack(other, bg, d).validate(bg, d)
                zero = state.stack(state.inverse(bg, d), bg, d)
                for c in (zero.e_p, zero.n_p, zero.n_p2, zero.nu_p3):
                    self.assertEqual(c.maxabs(), 0)
                N = state.e_p.N
                ep = None if d == 2 else rand(N, d - 3, bg.s1.tw, rng)
                np = None if d == 2 else rand(N, d - 3, bg.s1.tw, rng)
                state.gauge(bg, d, ep, np, rand(N, d - 1, bg.r1.tw, rng),
                            rand(N, d, bg.s1.tw, rng).sc(F(1, 7))).validate(bg, d)
                state.power(-3, bg, d).validate(bg, d)

    def test_background_transport_keeps_neutral_coordinate(self):
        rng = random.Random(8301)
        for d in (2, 3, 4):
            bg, state = complete(d, rng)
            for kind, degree in (('lift', 2), ('section', 1)):
                parameter = rand(state.e_p.N, degree, bg.omega2_real.tw, rng)
                if kind == 'section':
                    parameter = parameter.sc(F(1, 7))
                transported_bg, transported = state.background_change(bg, d, parameter, kind)
                transported.validate(transported_bg, d)
                self.assertEqual((transported.e_p - state.e_p).maxabs(), 0)

    def test_phase_validation_rejects_wrong_type_and_inexact_values(self):
        rng = random.Random(77)
        bg, state = complete(4, rng)
        wrong_sign = tuple(x ^ (i == 1) for i, x in enumerate(bg.s1.tw))
        invalid = (C(6, 5, {}, wrong_sign), C(6, 4, {}, bg.s1.tw),
                   C(5, 5, {}, bg.s1.tw[:6]),
                   C(6, 5, {tuple(range(6)): 0.5}, bg.s1.tw))
        for phase in invalid:
            with self.assertRaises((ValueError, TypeError)):
                replace(state, nu_p3=phase).validate(bg, 4)

    def test_gauge_composition_over_rational_lifts(self):
        rng = random.Random(2015)
        for signs in product((0, 1), repeat=6):
            tw = (0,) + signs
            e = rand(6, 1, tw, rng).d()
            v, w = rand(6, 1, tw, rng), rand(6, 1, tw, rng)
            residual = (e8.gauge(e, v) + e8.gauge(e + v.d(), w)
                        - e8.gauge(e, v + w) - e8.gauge_composition(e, v, w).d())
            self.assertEqual(residual.maxabs(), 0)

    def test_universal_neutral_hexagons(self):
        for bits in product((0, 1), repeat=4):
            tw = (0,) + bits
            basis = [C(4, 1, {edge: 1}, tw).d() for edge in combinations(range(1, 5), 2)]
            for a, b, c in product(basis, repeat=3):
                first = (e8.commutator(a, b + c) - e8.commutator(a, b) - e8.commutator(a, c)
                         + e8.associator(a, b, c) + e8.associator(b, c, a) - e8.associator(b, a, c))
                second = (e8.commutator(a + b, c) - e8.commutator(a, c) - e8.commutator(b, c)
                          - e8.associator(a, b, c) - e8.associator(c, a, b) + e8.associator(a, c, b))
                self.assertEqual((first - e8.hexagon_first(a, b, c).d()).mod(1).maxabs(), 0)
                self.assertEqual((second - e8.hexagon_second(a, b, c).d()).mod(1).maxabs(), 0)

    def test_c3_completed_root_includes_sheet_removal_gauge(self):
        period = F(0)
        for i, j in product(range(3), repeat=2):
            vertices = [0]
            for g in (1, i, 1, j, 1):
                vertices.append((vertices[-1] + g) % 3)
            a = C(5, 1, {(u, v): F((vertices[v] - vertices[u]) % 3, 3)
                          for u, v in combinations(range(6), 2)})
            e = a.d()
            bg = ci.Symmetry(C(5, 2, {}), char(5, [0] * 6), char(5, [0] * 6))
            root = State(e, C(5, 2, {}), C(5, 4, {}), a.cup(e).cup(e).sc(F(1, 3)))
            reduced = root.power(3, bg, 4).gauge(bg, 4, a.sc(-3), C(5, 1, {}), C(5, 3, {}))
            self.assertEqual(reduced.e_p.maxabs(), 0)
            period += reduced.nu_p3(tuple(range(6)))
            ninth = root.power(9, bg, 4).gauge(bg, 4, a.sc(-9), C(5, 1, {}), C(5, 3, {}))
            self.assertEqual(ninth.nu_p3.mod(1).maxabs(), 0)
        self.assertEqual(period % 1, F(1, 3))

    def test_thermal_map_retains_integer_e8(self):
        e = C(2, 0, {(i,): -2 for i in range(3)})
        n = C(2, 0, {(i,): 3 for i in range(3)})
        self.assertEqual(thermal_sheet(e, n)((0,)), -26)


class InfinitePresentations(unittest.TestCase):
    def test_translation_reflection_and_glide(self):
        def comm(i, j):
            return [i, j, -i, -j]
        translations = [comm(1, 2), comm(1, 3), comm(2, 3)]
        cases = [
            ([], [], 0, ()),
            ([1, 1, 1], translations, 3, ()),
            ([1, -1], [[2, 2], [2, 1, 2, 1]], 1, (2,)),
            ([1, 1, 1, -1], translations + [[4, 4, -2], [4, 1, -4, 1],
                [4, 2, -4, -2], [4, 3, -4, -3]], 1, (2,)),
        ]
        for signs, relators, free, torsion in cases:
            result = twisted_h1(signs, relators)
            self.assertEqual((result.free_rank, result.torsion), (free, torsion))


if __name__ == '__main__':
    unittest.main()
