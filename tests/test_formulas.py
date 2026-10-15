"""Exact algebraic identities, C2 roots, and persistent-worker integration."""
from fractions import Fraction as F
from itertools import combinations
from pathlib import Path
import json
import random
import subprocess
import sys
import unittest

import insulator as U
from insulator._engine.simplex import primitive, rand
from insulator._engine.simplex import O4d
from insulator._engine.transgression import O3canonical, E4canonical
from insulator._engine.product4d import E5
from insulator._engine.prism import gauge3 as unoptimized_gauge3
from insulator.worker import evaluate


def c2(N, p, value, twist=0):
    colors = [i % 2 for i in range(N + 1)]
    return U.Cochain(N, p, {f: F(value) for f in combinations(range(N + 1), p + 1)
        if all(colors[f[j]] != colors[f[j + 1]] for j in range(p))},
        [twist * color for color in colors])


def c2_background(N, rho, s, omega):
    return U.Symmetry(c2(N, 2, omega, rho ^ s), c2(N, 1, s, s), c2(N, 1, rho, rho))


def random_state(d, N, seed):
    rng = random.Random(seed)
    st = [0] + [rng.randrange(2) for _ in range(N)]
    rt = [0] + [rng.randrange(2) for _ in range(N)]
    if d == 2:
        st = [0] * (N + 1)  # A nonzero uniform IQH sheet requires trivial s.
    tt = [a ^ b for a, b in zip(st, rt)]
    sym = U.Symmetry(rand(N, 2, tt, rng) + rand(N, 1, tt, rng).d().sc(F(1, 7)),
                     U.char(N, st).ret(st), U.char(N, rt).ret(rt))
    k = (U.Cochain(N, 0, {(j,): -3 for j in range(N + 1)}, st) if d == 2
         else rand(N, d - 3, st, rng).d())
    n = primitive(U.integer_obstruction(sym, d, k)) + rand(N, d - 1, rt, rng).d()
    phase = primitive(U.source(sym, d, k, n))
    return sym, U.State(k, n, phase), rng


class FormulaIdentities(unittest.TestCase):
    def equal(self, a, b, modulus=None):
        residual = a - b
        if modulus:
            residual = residual.mod(modulus)
        self.assertEqual(residual.maxabs(), 0)

    def test_sources_products_gauges_inverse(self):
        for d in (2, 3, 4):
            with self.subTest(d=d):
                sym, state, rng = random_state(d, d + 3, 9730 + d)
                state.validate(sym, d)
                self.assertEqual(U.source(sym, d, state.sheet, state.charge).d().mod(1).maxabs(), 0)
                doubled = state.stack(state, sym, d)
                doubled.validate(sym, d)
                u = None if d == 2 else rand(state.sheet.N, d - 3, sym.s1.tw, rng)
                v = rand(state.sheet.N, d - 1, sym.rho1.tw, rng)
                gauged = state.gauge(sym, d, u, v)
                gauged.validate(sym, d)
                zero = state.stack(state.inverse(sym, d), sym, d)
                self.assertEqual(zero.sheet.maxabs(), 0)
                self.assertEqual(zero.charge.maxabs(), 0)
                self.assertEqual(zero.phase.mod(1).maxabs(), 0)
                state.power(3, sym, d).validate(sym, d)
                state.power(-3, sym, d).validate(sym, d)
                self.assertEqual(state.power(0, sym, d).phase.maxabs(), 0)

    def test_independent_sign_pure_charge_reductions(self):
        for d in (2, 3, 4):
            for sb in (0, 1):
                for rb in (0, 1):
                    with self.subTest(d=d, s=sb, rho=rb):
                        N = d + 2
                        st = [sb * (i % 2) for i in range(N + 1)]
                        rt = [rb * (i % 2) for i in range(N + 1)]
                        tt = [a ^ b for a, b in zip(st, rt)]
                        rng = random.Random(831 + 13*d + 2*sb + rb)
                        sym = U.Symmetry(rand(N, 1, tt, rng).sc(F(1, 5)).d(),
                                         U.char(N, st).ret(st), U.char(N, rt).ret(rt))
                        k = U.Cochain(N, d - 2, {}, st)
                        n, m = rand(N, d - 1, rt, rng).d(), rand(N, d - 1, rt, rng).d()
                        self.equal(U.source(sym, d, k, n), U.charge_source(sym, n), 1)
                        self.equal(U.product(sym, d, k, n, k, m)[2], U.charge_product(sym, n, m), 1)
                        if d in (3, 4):
                            a, s, r = sym.omega2_real, sym.s1, sym.rho1
                            raw_source = O3canonical(a,k,n,s,r) if d == 3 else O4d(a,k,n,s,r)
                            raw_product = E4canonical(a,k,n,k,m,s,r) if d == 3 else E5(a,k,n,k,m,s,r)
                            self.equal(U.source(sym, d, k, n), raw_source, 1)
                            self.equal(U.product(sym, d, k, n, k, m)[2], raw_product, 1)
                        v = rand(N, d - 1, rt, rng)
                        u = None if d == 2 else U.Cochain(N, d - 3, {}, st)
                        expected = (sym.omega2_real.cup(v) + U.bin0(v).sq(2).sc(F(1, 2))
                                    + U.charge_product(sym, n, v.d())).ret(st)
                        short = U.charge_gauge(sym, n, v)
                        cylinder = U.gauge(sym, d, k, n, u, v)[2]
                        self.equal(short, expected, 1)
                        self.equal(short.d(), U.source(sym, d, k, n + v.d()) - U.source(sym, d, k, n), 1)
                        self.equal(cylinder.d(), short.d(), 1)
                        if d == 2:
                            self.equal(cylinder, short, 1)
                        elif d == 3:
                            self.equal(cylinder, unoptimized_gauge3(a,k,n,s,r,u,v,O3canonical), 1)

    def test_background_lifts_sections(self):
        for d in (2, 3, 4):
            sym, state, rng = random_state(d, d + 2, 567 + d)
            for kind, degree in (('lift', 2), ('section', 1)):
                parameter = rand(state.sheet.N, degree, sym.omega2_real.tw, rng)
                if kind == 'section':
                    parameter = parameter.sc(F(1, 7))
                new_sym, k, n, phase = U.background_change(sym, d, state.sheet, state.charge,
                                                           parameter, kind)
                U.State(k, n, (state.phase + phase).mod(1)).validate(new_sym, d)

    def test_background_endpoint_pure_charge_signs(self):
        N = 4
        for sb in (0, 1):
            for rb in (0, 1):
                rng = random.Random(22000 + 2 * sb + rb)
                st = [sb * (i % 2) for i in range(N + 1)]
                rt = [rb * (i % 2) for i in range(N + 1)]
                tt = [a ^ b for a, b in zip(st, rt)]
                sym = U.Symmetry(rand(N, 1, tt, rng).d().sc(F(1, 5)),
                                 U.char(N, st).ret(st), U.char(N, rt).ret(rt))
                sheet = U.Cochain(N, 0, {}, st)
                charge = rand(N, 1, rt, rng).d()
                phase = primitive(U.source(sym, 2, sheet, charge))
                for kind, degree in (('lift', 2), ('section', 1)):
                    parameter = rand(N, degree, tt, rng)
                    if kind == 'section':
                        parameter = parameter.sc(F(1, 7))
                    out_sym, out_sheet, out_charge, correction = U.background_change(
                        sym, 2, sheet, charge, parameter, kind)
                    U.State(out_sheet, out_charge, phase + correction).validate(out_sym, 2)

    def test_lower_exchange(self):
        for d in (3, 4):
            sym, x, rng = random_state(d, d + 1, 327 + d)
            y = rand(x.sheet.N, d - 3, sym.s1.tw, rng).d()
            self.equal(U.lower_exchange(sym, d, x.sheet, y).d(),
                       U.integer_product(sym, d, x.sheet, y) - U.integer_product(sym, d, y, x.sheet))

    def test_explicit_three_dimensional_associator(self):
        sym, state, rng = random_state(3, 4, 74501)
        sheets = [state.sheet] + [rand(4, 0, sym.s1.tw, rng).d() for _ in range(2)]
        charges = [primitive(U.integer_obstruction(sym, 3, k))
                   + rand(4, 2, sym.rho1.tw, rng).d() for k in sheets]
        k01, n01, e01 = U.product(sym, 3, sheets[0], charges[0], sheets[1], charges[1])
        k12, n12, e12 = U.product(sym, 3, sheets[1], charges[1], sheets[2], charges[2])
        left = e01 + U.product(sym, 3, k01, n01, sheets[2], charges[2])[2]
        right = e12 + U.product(sym, 3, sheets[0], charges[0], k12, n12)[2]
        self.equal(U.associator_3p1(sym, sheets, charges).d(), left - right, 1)

    def test_negative_integer_carries_and_invalid_scalars(self):
        c = U.Cochain(2, 0, {(0,): -1, (1,): -2, (2,): -3})
        self.assertEqual([U.halves(c)((i,)) for i in range(3)], [1, 1, 0])
        with self.assertRaises(TypeError):
            U.Symmetry(U.Cochain(2, 2, {(0, 1, 2): .5}), U.char(2, [0]*3), U.char(2, [0]*3))
        with self.assertRaises(ValueError):
            sym, state, _ = random_state(2, 4, 125)
            U.background_change(sym, 1, state.sheet, state.charge, sym.omega2_real, 'lift')


class CompleteC2Roots(unittest.TestCase):
    def run_root(self, d, rho, s, omega, root):
        N = d + 2
        sym = c2_background(N, rho, s, omega)
        state = U.State(c2(N, d - 2, root[0], s), c2(N, d, root[1], rho),
                        c2(N, d + 1, root[2], s))
        def coordinates(x):
            return [x.sheet(tuple(range(d - 1))), x.charge(tuple(range(d + 1))),
                    x.phase(tuple(range(d + 2))) % 1]
        state.validate(sym, d)
        result = [coordinates(state)]
        for _ in range(3):
            state = state.stack(state, sym, d)
            k, n, _ = coordinates(state)
            if d == 4 and s == 0 and k // 2:
                state = state.gauge(sym, d, c2(N, 1, -(k // 2), s), c2(N, 3, 0, rho))
            elif d == 3 and s == 1 and k // 2:
                state = state.gauge(sym, d, c2(N, 0, k // 2, s), c2(N, 2, 0, rho))
            _, n, _ = coordinates(state)
            if d == 4 and rho == 0 and n // 2:
                state = state.gauge(sym, d, c2(N, 1, 0, s), c2(N, 3, -(n // 2), rho))
            elif d == 3 and rho == 1 and n // 2:
                state = state.gauge(sym, d, c2(N, 0, 0, s), c2(N, 2, n // 2, rho))
            elif d == 2 and rho == 0 and n // 2:
                state = state.gauge(sym, d, None, c2(N, 1, -(n // 2), rho))
            state.validate(sym, d)
            result.append(coordinates(state))
        self.assertEqual(result[-1], [0, 0, 0])
        return result

    def test_calibrated_roots(self):
        self.assertEqual(self.run_root(2, 0, 0, 0, (0, 1, F(1, 4)))[1], [0, 0, F(1, 2)])
        self.assertEqual(self.run_root(3, 1, 1, 0, (1, 0, F(-1, 16)))[1:3],
                         [[0, 1, F(1, 4)], [0, 0, F(1, 2)]])
        self.assertEqual(self.run_root(3, 0, 1, F(1, 2), (1, 0, 0))[1], [0, 0, 0])
        self.assertEqual(self.run_root(4, 0, 0, 0, (1, 0, F(1, 12)))[2], [0, 0, F(1, 2)])
        self.assertEqual(self.run_root(4, 1, 0, F(1, 2), (1, 0, F(7, 48)))[1], [0, 0, 0])

    def test_incoming_charge_images_and_obstructed_AI(self):
        for p, rho, s, w, expected in ((2, 0, 1, 0, F(1,2)), (2, 0, 1, F(1,2), 0),
                                        (3, 1, 0, F(1,2), 0), (3, 1, 0, 0, F(1,2))):
            N = p + 2
            value = U.d2(c2_background(N, rho, s, w), c2(N, p, 1, rho))(tuple(range(N + 1))) % 1
            self.assertEqual(value, expected)
        with self.assertRaises(ValueError):
            sym = c2_background(5, 0, 1, 0)
            U.source(sym, 3, c2(5, 1, 1, 1), c2(5, 3, 0, 0))


class WorkerProtocol(unittest.TestCase):
    def test_content_cache_ignores_request_id_and_output_transport(self):
        evaluate({'op': 'cache_clear'})
        evaluate({'op': 'ping', 'id': 1})
        evaluate({'op': 'ping', 'id': 2, 'response_format': 'gap'})
        self.assertEqual(evaluate({'op': 'cache_info'})['hits'], 1)

    def test_frozen_reference_vectors(self):
        fixture = Path(__file__).resolve().parents[1] / 'formulas/reference_vectors.json'
        vectors = json.loads(fixture.read_text())['vectors']
        self.assertEqual(len(vectors), 9)
        for item in vectors:
            with self.subTest(dimension=item['request']['dimension'], op=item['request']['op']):
                self.assertEqual(evaluate(item['request']), item['expected'])

    def test_persistent_json_recovery_and_gap_format(self):
        requests = [
            {'id': 1, 'op': 'ping'},
            {'id': 2, 'op': 'source', 'simplex_dimension': 4, 'charge': {'0,1,2': .5}},
            {'id': 3, 'op': 'd2', 'dimension': 2, 'simplex_dimension': 4,
             'charge': {','.join(map(str, f)): str(v) for f, v in c2(4,2,1).v.items()}, 'return': 'top'},
            {'id': 4, 'op': 'd3', 'simplex_dimension': 3, 'return': 'top', 'response_format': 'gap'},
        ]
        worker = Path(__file__).resolve().parents[1] / 'scripts/formula_worker.py'
        completed = subprocess.run([sys.executable, str(worker)], input=''.join(json.dumps(r)+'\n' for r in requests),
                                   capture_output=True, text=True, check=True, cwd='/tmp')
        lines = completed.stdout.splitlines()
        self.assertTrue(json.loads(lines[0])['ok'])
        self.assertFalse(json.loads(lines[1])['ok'])
        self.assertEqual(json.loads(lines[2])['result'], '1/2')
        self.assertIn('("ok"):=true', lines[3])
        self.assertIn('("result"):="0"', lines[3])


if __name__ == '__main__':
    unittest.main()
