"""Pointwise domain check for the optional closed-CF phase specialization."""
from itertools import combinations
from pathlib import Path
import random
import sys
import unittest
import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from fspt.formulas import evaluate, formula


def short(c):
    return (c((0,3,4,5))*c((0,1,2,3))
            + c((0,1,4,5))*c((1,2,3,4))
            + c((0,1,2,5))*c((2,3,4,5))) % 2


class ClosedCFTests(unittest.TestCase):
    def test_all_closed_local_cf_cochains_and_signs(self):
        values = np.arange(1024, dtype=np.int64)
        cone = {(0,)+f:(values >> i) & 1
                for i,f in enumerate(combinations(range(1,6),3))}
        def c(f):
            if f[0] == 0:
                return cone[f]
            return sum(cone[(0,)+f[:i]+f[i+1:]] for i in range(4)) % 2
        for f in combinations(range(6),5):
            assert np.all(sum(c(f[:i]+f[i+1:]) for i in range(5)) % 2 == 0)
        for mask in range(32):
            eps = [0]+[(mask >> i) & 1 for i in range(5)]
            fields = dict(a=lambda f:0,w=lambda f:0,c=c,
                          s=lambda f:eps[f[0]] ^ eps[f[1]])
            full = evaluate(formula('obstruction',2),fields)
            self.assertTrue(np.array_equal(full,4*short(c)))

    def test_nonclosed_input_is_outside_specialization(self):
        rng = random.Random(448109)
        witnessed = False
        for _ in range(64):
            table = {f:rng.randrange(2) for f in combinations(range(6),4)}
            c = table.__getitem__
            full = evaluate(formula('obstruction',2),
                dict(a=lambda f:0,w=lambda f:0,c=c,s=lambda f:0))
            if full != 4*short(c):
                self.assertTrue(any(sum(c(f[:i]+f[i+1:]) for i in range(5)) % 2
                                    for f in combinations(range(6),5)))
                witnessed = True
                break
        self.assertTrue(witnessed, 'Negative-domain fixture did not distinguish the omitted term')


if __name__ == '__main__':
    unittest.main(verbosity=2)
