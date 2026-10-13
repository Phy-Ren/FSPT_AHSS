"""Summary tables preserve relative scopes, actual IQH lifts and absent cases."""
from pathlib import Path
import importlib.util
import json
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location("campaign_summary", ROOT / "scripts/summarize_results.py")
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SummaryTests(unittest.TestCase):
    def test_relative_group_and_actual_uniform_multiplicity(self):
        case = {"id": "point2_02_spinless", "family": "point2", "spin": "spinless", "status": "complete",
                "metadata": {"index": 2, "name": "C2"}, "report": "example", "comparison": None,
                "classification": {"torsion": [4], "freeRank": 1, "uniformIQHIncluded": True,
                                   "witnesses": [{"kind": "uniform-IQH-lift", "sheetMultiplicity": 2}],
                                   "relativeUniformIQH0": {"torsion": [4], "freeRank": 0}}}
        row = module.rows_from_cases({case["id"]: case})[0]
        self.assertEqual(row["spinless_group"], "Z4")
        self.assertEqual(row["spinless_full_uniform_IQH_group"], "Z x Z4")
        self.assertEqual(row["spinless_uniform_IQH_multiplicity"], "2")
        self.assertEqual(row["spin_half_status"], "not in supplied reports")

    def test_failed_and_selected_without_records_stay_explicit(self):
        with tempfile.TemporaryDirectory() as directory:
            directory = Path(directory)
            (directory / "results.json").write_text("[]")
            (directory / "failures.json").write_text(json.dumps([{"id": "point3_06_spin_half", "status": "timeout"}]))
            (directory / "run_provenance.json").write_text(json.dumps([{"selection": ["point3_06_spinless", "point3_06_spin_half"]}]))
            row = module.rows_from_cases(module.read_reports([directory]))[0]
            self.assertEqual(row["name"], "D2")
            self.assertEqual(row["spin_half_status"], "timeout")
            self.assertEqual(row["spinless_status"], "no result record")
            self.assertEqual(row["spin_half_group"], "not computed")
            self.assertEqual(row["spin_half_comparison"], "comparison unavailable")

    def test_3d_uses_named_reference_quotient_without_hiding_mismatch(self):
        comparison = {"checks": [{"quantity": "stacking", "status": "scope_mismatch",
                                  "published": {"torsion": [2, 2, 2, 2], "freeRank": 0}},
                                 {"quantity": "stacking_mod_named_neutral_E8", "status": "mismatch",
                                  "published": {"torsion": [2, 2, 2], "freeRank": 0}}]}
        status, expected = module.comparison_text(comparison, "point3")
        self.assertEqual(status, "named-E8 quotient: mismatch")
        self.assertEqual(expected, "Z2^3")


if __name__ == "__main__":
    unittest.main()
