"""Independent regressions for the per-edge Alexander--Whitney transport.

The unchanged supplied evaluator is the oracle. An optional archived earlier
graph checks the exact error formula; it is never a production dependency.
"""
import argparse
from fractions import Fraction
import hashlib
from itertools import combinations
import json
from pathlib import Path
import random
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas_pip_compile import evaluate_program
from fspt.pip_coordinates import sign_power
sys.path.insert(0, str(ROOT / 'vendor/p_ip_d4_normalized_package/code'))
import cochains as q
from pip_d4 import evaluate_simplex


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--old-program', type=Path)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    path = ROOT / 'gap/pip_o5_program.json'
    program = json.loads(path.read_text())
    old = json.loads(args.old_program.read_text()) if args.old_program else None
    zero = q.C(2)
    face = tuple(range(6))
    checks = dict(bit_identity=0, legal_sign_oracle=0,
                  torsion_rephasing=0, exact_square_gauge=0,
                  old_new_error_formula=0, unchanged_even_integer=0)
    for x in range(-128, 129):
        assert (((-x) >> 1) ^ (x >> 1)) & 1 == x % 2
        checks['bit_identity'] += 1
    for mask in range(32):
        eps = [0] + [(mask >> i) & 1 for i in range(5)]
        s = q.C(1, fun=lambda f: eps[f[0]] ^ eps[f[1]])
        for choice in range(2):
            random.seed(274811 + 2 * mask + choice)
            b = q.primitive(q.cup(s, q.sq(s, 1))) + q.random_cochain(1, 5).d()
            c = q.primitive(q.parity(s.lift(), b, zero, s)) + q.random_cochain(2, 5).d()
            fields = dict(n=s, b=b, c=c, s=s)
            expected = evaluate_simplex(1, n_integer=s.lift(), n_majorana=b,
                n_fermion=c, omega2=zero, s1=s)['numerator_mod16']
            assert evaluate_program(program, fields) == expected, (mask, choice)
            checks['legal_sign_oracle'] += 1
            s4 = q.C(4, fun=lambda f: Fraction(sign_power(s, f), 4), mod=None)
            assert (q.ds(s4, s)(face) + Fraction(sign_power(s, face), 2)) % 1 == 0
            checks['torsion_rephasing'] += 1
            # The surviving square-coordinate change is precisely a phase
            # gauge: d_s(1/2 s B)=1/2 s^4 when dB=s^3.
            gauge = q.C(3, fun=lambda f: Fraction(s(f[:2]) * b(f[1:]), 2), mod=None)
            for f in combinations(range(6), 5):
                assert (q.ds(gauge, s)(f) - Fraction(sign_power(s, f), 2)) % 1 == 0
                checks['exact_square_gauge'] += 1
    if old:
        for seed in range(128):
            random.seed(692731 + seed)
            s = q.random_cochain(0, 5).d()
            vertex = [random.randrange(-512, 513) for _ in range(6)]
            for multiple in (1, 2):
                n = q.C(1, fun=lambda f: multiple * ((1 - 2*s(f))*vertex[f[1]]-vertex[f[0]]), mod=None)
                b = q.primitive(q.cup(s, q.sq(n.reduce(2), 1))) + q.random_cochain(1, 5).d()
                c = q.primitive(q.parity(n, b, zero, s)) + q.random_cochain(2, 5).d()
                fields = dict(n=n, b=b, c=c, s=s)
                delta = (evaluate_program(program, fields)-evaluate_program(old, fields)) % 16
                expected = (8*s((0,1))*s((1,2))*s((2,3))*s((3,4))
                    * ((((1-2*s((0,3)))*n((3,4))) >> 1) & 1) * (n((4,5)) % 2)) % 16
                assert delta == expected, (seed, multiple, delta, expected)
                checks['old_new_error_formula'] += 1
                if multiple == 2:
                    assert delta == 0
                    checks['unchanged_even_integer'] += 1
    result = dict(status='passed', formula_convention='normalized-pip-aw-edge-transport-v2',
        current_program_sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
        previous_program_sha256=(hashlib.sha256(args.old_program.read_bytes()).hexdigest() if old else None),
        unchanged_oracle='vendor/p_ip_d4_normalized_package/code/pip_d4.py::evaluate_simplex',
        checks=checks)
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
