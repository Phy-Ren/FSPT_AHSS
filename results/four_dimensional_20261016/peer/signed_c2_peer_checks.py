#!/usr/bin/env python3
"""Independent signed scalar-versus-global pullbacks, including degeneracies."""
import json
import sys
import time
from fractions import Fraction as F
from itertools import combinations, product
from pathlib import Path

REPOSITORY = Path(sys.argv[1]) if len(sys.argv) > 1 else Path('/home/xingyu/FSPT_AHSS_insulator')
sys.path.insert(0, str(REPOSITORY))
from insulator import api as ci, e8
from insulator.signed_charge_conjugation_4p1 import C2FourData

started = time.monotonic()
count = 0
summary = {}
for name in ('H_plus', 'H_minus', 'AI_relative', 'AII_relative'):
    solver = C2FourData(name)
    state = (solver.completions(1, 1 if name == 'H_minus' else 0)[0]
             if name.startswith('H_') else
             solver.completions(0, 0, 1 if name == 'AI_relative' else 0)[0])
    expected = solver.gauge(state, 2, -3, 5, F(7, 13))
    for arguments in product((0, 1), repeat=6):
        vertices = [0]
        for value in arguments:
            vertices.append((vertices[-1] + value) % 2)

        def cochain(degree, value=0, sign=0):
            return ci.Cochain(
                6, degree,
                {face: value for face in combinations(range(7), degree + 1)
                 if all(vertices[i] != vertices[j] for i, j in zip(face, face[1:]))},
                tuple(sign * vertex for vertex in vertices))

        symmetry = ci.Symmetry(cochain(2, F(solver.k, 2), solver.s ^ solver.rho),
                               cochain(1, solver.s, solver.s),
                               cochain(1, solver.rho, solver.rho))
        local = e8.State(cochain(2, state.e, solver.s), cochain(2, state.n, solver.s),
                         cochain(4, state.charge, solver.rho), cochain(5, state.phase, solver.s))
        local.validate(symmetry, 4)
        actual = local.gauge(symmetry, 4, cochain(1, 2, solver.s),
                             cochain(1, -3, solver.s), cochain(3, 5, solver.rho),
                             cochain(4, F(7, 13), solver.s))
        expected_fields = (cochain(2, expected.e, solver.s), cochain(2, expected.n, solver.s),
                           cochain(4, expected.charge, solver.rho),
                           cochain(5, expected.phase, solver.s))
        for index, (got, want) in enumerate(zip(
                (actual.e_p, actual.n_p, actual.n_p2, actual.nu_p3), expected_fields)):
            difference = got - want
            assert not (difference.mod(1) if index == 3 else difference).maxabs(), (name, arguments, index)
        count += 1
    summary[name] = {'state': state.json(), 'jointGaugeEndpoint': expected.json(), 'allSixWords': 64}

result = {'status': 'PASS', 'completeSixWordJointGaugeChecks': count, 'cases': summary,
          'seconds': time.monotonic() - started,
          'scope': 'All 64 C2 six-words, including degenerate words, for one nontrivial completed state and one mixed noncanonical joint gauge in each of four backgrounds.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result, indent=2) + '\n')
print(json.dumps(result, indent=2))
