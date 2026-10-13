"""Benchmark comparisons must respect mathematical scope and group extensions."""
from pathlib import Path
import importlib.util
import json
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("insulator_benchmark_comparison", ROOT / "benchmarks/compare.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class BenchmarkTests(unittest.TestCase):
    def test_abelian_group_comparison_is_not_order_comparison(self):
        self.assertEqual(module.group_signature([2, 3, 0]), module.group_signature([6, 0]))
        self.assertNotEqual(module.group_signature([2, 2]), module.group_signature([4]))

    def test_wallpaper_uses_final_filtration_not_raw_cohomology(self):
        result = {"id": "wallpaper_06_spinless", "family": "wallpaper", "name": "pmm",
                  "spin": "spinless", "uniformIQHIncluded": False,
                  "phaseOrders": [2] * 8, "chargeOrders": [2] * 3 + [0],
                  "finalPhaseOrders": [2] * 7, "finalPhaseFreeRank": 0,
                  "finalChargeOrders": [2] * 3, "finalChargeFreeRank": 1,
                  "torsion": [2] * 4 + [4] * 3, "freeRank": 1}
        checks = module.compare(result)["checks"]
        self.assertEqual([row["status"] for row in checks[:3]], ["match"] * 3)
        del result["finalPhaseOrders"]
        self.assertEqual(module.compare(result)["checks"][1]["status"], "not_computed")

    def test_nested_runner_record(self):
        row = {"input": {"id": "wallpaper_01_spinless", "name": "p1", "spin": "spinless"},
               "classification": {"uniformIQHIncluded": False, "finalChargeOrders": [],
                                  "finalChargeFreeRank": 1, "finalPhaseOrders": [],
                                  "finalPhaseFreeRank": 0, "torsion": [], "freeRank": 1},
               "run": {"status": "completed"}}
        self.assertEqual([x["status"] for x in module.compare(row)["checks"][:3]], ["match"] * 3)

    def test_wallpaper_filling_requires_restriction_witness(self):
        result = {"id": "wallpaper_04_spinless", "name": "pg", "spin": "spinless",
                  "uniformIQHIncluded": False, "torsion": [], "freeRank": 1}
        self.assertEqual(module.compare(result)["checks"][-1]["status"], "requires_generator_witness")
        result["wallpaperFilling"] = {"primitiveTranslationVectors": [[1, 0], [0, 1]],
                                     "primitiveCellArea": 1, "generatorFillings": [2], "fillingStep": 2}
        check = module.compare(result)["checks"][-1]
        self.assertEqual(check["status"], "requires_source_coordinate_map")
        self.assertEqual(check["calculated_primitive_cell_charge_step"], 2)
        self.assertEqual(check["published_charge_step"], 1)
        result["wallpaperFilling"]["fillingStep"] = 1
        self.assertEqual(module.compare(result)["checks"][-1]["status"], "requires_source_coordinate_map")

    def test_e8_sector_mismatch_is_never_automatic_failure(self):
        result = {"id": "point3_04_spinless", "name": "Cs", "spin": "spinless",
                  "torsion": [8], "freeRank": 0}
        checks = module.compare(result)["checks"]
        check = checks[0]
        self.assertEqual(check["status"], "scope_mismatch")
        self.assertEqual(checks[1]["status"], "match")
        self.assertEqual(checks[1]["neutral_generator"]["source_root_line"], 4566)
        self.assertEqual(check["published"], {"torsion": [2, 8], "freeRank": 0})

    def test_primary_source_discrepancy_is_preserved(self):
        result = {"id": "point2_02_spin_half", "name": "C2", "spin": "spin_half",
                  "uniformIQHIncluded": False, "torsion": [4], "freeRank": 0}
        checks = module.compare(result)["checks"]
        self.assertEqual(checks[0]["status"], "published_source_discrepancy")
        self.assertEqual(checks[1]["status"], "match")
        self.assertIn("interaction-only", checks[1]["comparison_limit"])

    def test_rotation_adjoining_relation_has_a_nontrivial_extension(self):
        from sympy.matrices.normalforms import smith_normal_form
        rows = json.loads((ROOT / "benchmarks/point2_rotation_reduction_1809.01636.json").read_text())["rows"]
        for row in rows:
            matrix = module.sp.Matrix(row["center_presentation"])
            diagonal = smith_normal_form(matrix, domain=module.sp.ZZ).diagonal()
            self.assertEqual(module.group_signature([abs(int(x)) for x in diagonal]),
                             module.group_signature(row["band_generated_stacking_orders"]))

    def test_full_iqh_comparison_uses_certified_relative_subgroup(self):
        result = {"id": "wallpaper_04_spinless", "name": "pg", "spin": "spinless",
                  "uniformIQHIncluded": True, "torsion": [4], "freeRank": 2,
                  "wallpaperFilling": {"primitiveTranslationVectors": [[1, 0], [0, 1]],
                                       "primitiveCellArea": 1, "generatorFillings": [1], "fillingStep": 1}}
        self.assertEqual(module.compare(result)["checks"][0]["status"], "scope_mismatch")
        result["relativeUniformIQH0"] = {"uniformIQHIncluded": False, "torsion": [], "freeRank": 1,
                                       "wallpaperFilling": {**result["wallpaperFilling"],
                                                           "generatorFillings": [2], "fillingStep": 2}}
        compared = module.compare(result)
        self.assertIn("relativeUniformIQH0", compared["comparison_scope"])
        self.assertEqual(compared["checks"][2]["status"], "match")
        self.assertEqual(compared["checks"][-1]["status"], "requires_source_coordinate_map")
        self.assertEqual(compared["checks"][-1]["calculated_primitive_cell_charge_step"], 2)
        del result["relativeUniformIQH0"]["wallpaperFilling"]
        self.assertEqual(module.compare(result)["checks"][-1]["status"], "requires_generator_witness")

    def test_primary_tables_have_complete_coverage(self):
        for filename, count in [("wallpaper_layers_2112.15533.json", 34),
                                ("wallpaper_stacking_2012.15657.json", 34),
                                ("point2_stacking_2012.15657.json", 20),
                                ("point2_rotation_reduction_1809.01636.json", 10),
                                ("point3_full_2204.13558.json", 64),
                                ("point3_named_e8_quotient_2204.13558.json", 42)]:
            data = json.loads((ROOT / "benchmarks" / filename).read_text())
            self.assertEqual(len(data["rows"]), count)
            self.assertEqual(len(data["source"]["source_sha256"]), 64)

if __name__ == "__main__":
    unittest.main()
