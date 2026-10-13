"""Physical little-group induction independently checks center-charge claims."""
from pathlib import Path
import importlib.util
import json
import unittest
import sympy as sp

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("center_orbit_audit", ROOT / "benchmarks/audit_center_orbits.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class CenterOrbitTests(unittest.TestCase):
    def test_d2_odd_center_charge_is_forbidden_by_physical_spin(self):
        rx = sp.I * sp.Matrix([[0, 1], [1, 0]])
        ry = sp.I * sp.Matrix([[0, -sp.I], [sp.I, 0]])
        self.assertEqual(rx * ry, -ry * rx)
        record = json.loads((ROOT / "insulator_catalog/generated/point3_06_spin_half.json").read_text())
        result = module.audit(record)
        self.assertFalse(result["odd_charge_center_has_one_dimensional_representation"])
        self.assertEqual(result["center_charge_step"], 2)
        self.assertIn([1, 0, 0], result["atomic_orbit_relations"])
        self.assertEqual(result["torsion_before_CI_bubbles"], [2, 2])

    def test_d2d_neutral_axis_orbit_removes_a_center_character(self):
        for spin, expected in (("spinless", [2]), ("spin_half", [2, 2])):
            record = json.loads((ROOT / f"insulator_catalog/generated/point3_14_{spin}.json").read_text())
            result = module.audit(record)
            witness = next(w for w in result["orbit_witnesses"] if w["relation"] == [0, 0, 1])
            self.assertEqual(witness["site_charge"], 0)
            self.assertEqual(witness["orbit_size"], 2)
            self.assertEqual(witness["point_stabilizer"], [0, 3, 4, 6])
            self.assertEqual(result["torsion_before_CI_bubbles"], expected)


if __name__ == "__main__":
    unittest.main()
