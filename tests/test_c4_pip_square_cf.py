"""Finite C4 CF-square period; post-computation discrepancy investigation.

No space-group answers are inputs. This checks the lower square formula and
does not by itself replace the full phase or space-group calculation.
"""
from collections import Counter
from itertools import product
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
from fspt.formulas import cup, evaluate, field


B, S = field('b', 2), field('s', 1)
K = cup(B, B, 1) + cup(B, B.differential(), 2) + S*B


def fields(increments):
    vertices = [0]
    for g in increments:
        vertices.append((vertices[-1]+g) % 4)
    sign = lambda f: (vertices[f[1]]-vertices[f[0]]) % 2
    majorana = lambda f: ((vertices[f[1]]-vertices[f[0]]) % 2)*(((vertices[f[2]]-vertices[f[1]]) % 4)//2)
    return dict(s=sign, b=majorana)


class C4SquareTests(unittest.TestCase):
    def test_legal_majorana_and_closed_cf_square(self):
        for increments in product(range(4), repeat=3):
            data = fields(increments)
            self.assertEqual(evaluate(B.differential(), data), evaluate(S*S*S, data))
            a, b, c = increments
            self.assertEqual(evaluate(K, data), (a % 2)*((b+c)//4) % 2)
        for increments in product(range(4), repeat=4):
            self.assertEqual(evaluate(K.differential(), fields(increments)), 0)

    def test_actual_cycle_and_nonzero_period(self):
        cycle = [(1, i, 1) for i in range(4)]
        boundary = Counter()
        for a, b, c in cycle:
            for face in ((b, c), ((a+b) % 4, c), (a, (b+c) % 4), (a, b)):
                if 0 not in face:
                    boundary[face] += 1
        self.assertTrue(all(v % 2 == 0 for v in boundary.values()))
        values = [evaluate(K, fields(x)) for x in cycle]
        self.assertEqual(values, [0, 0, 0, 1])
        self.assertEqual(sum(evaluate(S*S*S, fields(x)) for x in cycle) % 2, 0)


if __name__ == '__main__':
    unittest.main(verbosity=2)
