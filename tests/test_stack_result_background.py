"""Replay actual incoming quotients without assigning an unknown upper carry."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from fspt.stacking import PresentedStackingGroup, InvalidCertificate
import test_audit_background_run as fixtures

ROOT = Path(__file__).resolve().parents[1]


class NontriangularPresentationTests(unittest.TestCase):
    def result(self):
        # (Z/4)^2 / <D1+D2>, with independent Smith U R V = diag(1,4).
        return dict(status='computed', freePipRank=0, invariants=[4], lower=dict(
            generators=[dict(name='D1'), dict(name='D2')],
            presentation=[[4, 0], [0, 4], [1, 1]],
            smithRowTransform=[[0, 0, 1], [0, 1, 0], [1, 1, -4]],
            smithColumnTransform=[[1, -1], [0, 1]], smithDiagonal=[1, 4]))

    def test_quotient_relation_and_negative_carries(self):
        group = PresentedStackingGroup(self.result())
        self.assertEqual(group.marked_reduction, 'smith-representative')
        self.assertEqual(group.stack_marked({'D1': 1}, {'D2': 1}), {})
        for a in range(-8, 9):
            for b in range(-8, 9):
                marked = group.stack_marked({'D1': a}, {'D2': b})
                self.assertEqual(marked, {'D2': (b-a) % 4} if (b-a) % 4 else {})
                self.assertEqual(group.canonical(marked), ((b-a) % 4,))

    def test_free_coordinates_survive_smith_lift(self):
        data = self.result(); data.update(freePipRank=1, invariants=[0, 4])
        group = PresentedStackingGroup(data)
        self.assertEqual(group.stack_marked({'Pfree1': -7, 'D1': 3},
                                            {'Pfree1': 2, 'D2': 5}),
                         {'Pfree1': -5, 'D2': 2})

    def test_nonunimodular_inverse_is_not_rounded(self):
        data = self.result(); data['lower']['smithColumnTransform'] = [[2, -2], [0, 2]]
        group = PresentedStackingGroup(data)
        with self.assertRaisesRegex(InvalidCertificate, 'non-unimodular'):
            group.stack_marked({'D1': 1}, {})


class BackgroundReplayCliTests(unittest.TestCase):
    def call(self, data, left):
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory)/'result.json'; path.write_text(json.dumps(data))
            return subprocess.run([sys.executable, str(ROOT/'scripts/stack_result.py'), str(path),
                '--left', json.dumps(left)], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                text=True)

    def test_actual_h0_incoming_is_zero_in_quotient(self):
        data = fixtures.example('h0'); lower = data['stacking']['lower']
        names = [g['name'] for g in lower['generators']]
        incoming = {name: c for name, c in zip(names, lower['presentation'][-1]) if c}
        self.assertTrue(incoming)
        result = self.call(data, incoming)
        self.assertEqual(result.returncode, 0, result.stderr)
        answer = json.loads(result.stdout)
        self.assertEqual(answer['marked_reduction'], 'smith-representative')
        self.assertEqual(answer['stacked_marked'], {})
        self.assertFalse(any(answer['stacked']))

    def test_unknown_upper_carry_is_refused_cleanly(self):
        result = self.call(fixtures.example('ext'), {'P1': 1})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('marked carry is missing', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertFalse(result.stdout)

    def test_unknown_generator_is_refused_cleanly(self):
        result = self.call(fixtures.example('h0'), {'NOT_A_GENERATOR': 1})
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('unknown marked generators', result.stderr)
        self.assertNotIn('Traceback', result.stderr)
        self.assertFalse(result.stdout)


if __name__ == '__main__':
    unittest.main()
