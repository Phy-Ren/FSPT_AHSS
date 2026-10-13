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
        self.assertEqual(module.compare(result)["checks"][0]["status"], "published_source_discrepancy")

    def test_primary_tables_have_complete_coverage(self):
        for filename, count in [("wallpaper_layers_2112.15533.json", 34),
                                ("wallpaper_stacking_2012.15657.json", 34),
                                ("point2_stacking_2012.15657.json", 20),
                                ("point3_full_2204.13558.json", 64),
                                ("point3_named_e8_quotient_2204.13558.json", 42)]:
            data = json.loads((ROOT / "benchmarks" / filename).read_text())
            self.assertEqual(len(data["rows"]), count)
            self.assertEqual(len(data["source"]["source_sha256"]), 64)

if __name__ == "__main__":
    unittest.main()
