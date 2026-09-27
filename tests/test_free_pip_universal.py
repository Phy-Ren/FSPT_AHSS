"""Exact local identities used in the free p+ip lattice argument.

This checks formulas only. It does not pretend to compute a target group's
primitive surviving lattice or a universal dihedral phase primitive.
"""
import json
from pathlib import Path
import random
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas import evaluate, formula
from fspt.formulas_pip_compile import Builder


class FreePipTests(unittest.TestCase):
    def test_unitary_full_phase_is_symbolically_zero(self):
        # n remains an arbitrary symbolic integer field. All simplifications
        # are exact arithmetic identities in the complete generated formula.
        program = json.loads((ROOT / 'gap/pip_o5_program.json').read_text())
        builder = Builder()
        values = []
        for node in program['program']:
            op = node[0]
            if op == 'const':
                value = builder.scalar(node[1])
            elif op == 'field':
                value = (builder.make('field', node[1], tuple(node[2]))
                         if node[1] == 'n' else builder.scalar(0))
            elif op == 'add':
                value = values[node[1]] + values[node[2]]
            elif op == 'mul':
                value = values[node[1]] * values[node[2]]
            elif op == 'mod':
                value = values[node[1]] % node[2]
            elif op == 'bit':
                value = builder.bit(values[node[1]], node[2])
            elif op == 'floor':
                value = builder.floor(values[node[1]], node[2])
            elif op == 'div':
                value = builder.divide(values[node[1]], node[2])
            else:
                self.fail(op)
            values.append(value)
        self.assertEqual(builder.nodes[values[program['output']].index], ('const', 0))

    def test_unitary_lower_sources(self):
        rng = random.Random(204711)
        for _ in range(32):
            vertices = [rng.randrange(-30, 31) for _ in range(5)]
            fields = dict(n=lambda f: vertices[f[1]] - vertices[f[0]],
                          b=lambda f: 0, w=lambda f: 0, s=lambda f: 0)
            self.assertEqual(evaluate(formula('pip_majorana', 1), fields), 0)
            self.assertEqual(evaluate(formula('pip_parity', 1), fields), 0)

    def test_even_dihedral_reflection_sources(self):
        # Exhaust all homogeneous C2 simplices including degeneracies. The
        # two reflection restrictions of universal 2n are n=0 and n=2s.
        for bits in range(16):
            vertices = [0] + [(bits >> j) & 1 for j in range(4)]
            sign = lambda f: vertices[f[0]] ^ vertices[f[1]]
            for multiple in (0, 2):
                fields = dict(n=lambda f: multiple * sign(f), b=lambda f: 0,
                              w=lambda f: 0, s=sign)
                self.assertEqual(evaluate(formula('pip_majorana', 1), fields), 0)
                self.assertEqual(evaluate(formula('pip_parity', 1), fields), 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
