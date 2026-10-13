"""Independent periodic-cycle certificates for the C4 and C6 extension audit."""
import importlib.util
from pathlib import Path
import unittest


class CyclicRootAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        path = Path(__file__).resolve().parents[1] / 'formulas/audits/cyclic_roots.py'
        spec = importlib.util.spec_from_file_location('cyclic_root_audit', path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cls.result = module.run_audit()

    def test_c4_ci_square_is_nonzero_for_all_three_gauge_paths(self):
        root = self.result['CI_root']
        self.assertEqual(root['final_phase_period'], '1/2')
        self.assertEqual(root['short_charge_gauge_period'], '1/2')
        self.assertEqual(root['single_joint_gauge_period'], '1/2')
        self.assertEqual(len(root['cycle_ledger']), 9)

    def test_c4_independent_charge_root_has_order_two(self):
        self.assertEqual(self.result['charge_root']['final_phase_period'], '0')
        self.assertEqual(self.result['presentation'], [[2, 0, 0], [0, 2, 0], [-1, 0, 2]])
        self.assertEqual(self.result['torsion'], [2, 4])

    def test_c6_split_inflation_preserves_order_eight(self):
        proof = self.result['C6_split_inflation_audit']
        self.assertEqual(proof['periodic_maps'], {'g_minus_1_on_Z_sign': -2, 'norm_on_Z_sign': 0})
        self.assertEqual(proof['tower_order'], 8)
        self.assertEqual(proof['torsion'], [8])


if __name__ == '__main__':
    unittest.main()
