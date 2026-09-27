"""Report structure/certificate checks; synthetic fixtures assert no physics."""
from pathlib import Path
import sys
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from report_results import free_lattice, group_name


def fixture():
    dimensions = [1, 2, 3, 4, 5, 6, 7]
    generators = []
    for i, coordinates in enumerate([[1, 1, 1], [0, 0, 2]], 1):
        generators.append(dict(name='Pfree%d' % i, h1Coordinates=coordinates,
                               integer1=[0]*2, majorana2=[0]*3,
                               fermion3=[0]*4, phase4=[[0, 1]]*5))
    return dict(resolution_dimensions=dimensions, pip=dict(free_rank=2,
        free_lattice=dict(status='computed', rank=2, freeIndices=[2, 3],
            latticeBasis=[[1, 1], [0, 2]], latticeIndex=2,
            survivingParityBasis=[[1, 1]], generators=generators,
            fullFreePhaseWitness=True, certificate='synthetic-structure-test')))


class ReportTests(unittest.TestCase):
    def test_trivial_and_free_are_distinct(self):
        self.assertEqual(group_name([]), '0')
        self.assertEqual(group_name([0]), 'Z')

    def test_legacy_scope(self):
        data = fixture()
        del data['pip']['free_lattice']
        self.assertFalse(free_lattice(data)['free_pip_lattice_basis_available'])

    def test_marked_lattice_structure(self):
        result = free_lattice(fixture())
        self.assertTrue(result['free_pip_lattice_basis_available'])
        self.assertEqual(result['free_pip_lattice_index'], 2)
        self.assertTrue(result['free_pip_phase_witness'])

    def test_corrupt_certificates_are_rejected(self):
        for mutation in ('index', 'coordinates', 'parity', 'phase'):
            data = fixture()
            free = data['pip']['free_lattice']
            if mutation == 'index':
                free['latticeIndex'] = 1
            elif mutation == 'coordinates':
                free['generators'][0]['h1Coordinates'][1] = 2
            elif mutation == 'parity':
                free['survivingParityBasis'] = [[1, 0]]
            else:
                free['generators'][0]['phase4'][0] = [1, 0]
            with self.assertRaises(ValueError, msg=mutation):
                free_lattice(data)


if __name__ == '__main__':
    unittest.main(verbosity=2)
