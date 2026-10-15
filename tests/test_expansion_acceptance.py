"""Independent checks on primitive filling in completed affine presentations."""
from copy import deepcopy
import json
from pathlib import Path
import unittest

from scripts.collect_expansion import filling_check


class PrimitiveFillingAcceptance(unittest.TestCase):
    def setUp(self):
        # Z/2 phase plus two free roots modulo 3 charge - 2 CI = 0.
        # The completed CI root lowers the filling step from four to two.
        self.record = {
            "presentationGeneratorCount": 3,
            "generators": [{"kind": name} for name in ("phase", "charge", "CI")],
            "presentation": [[2, 0, 0], [0, 3, -2]],
            "spaceGroupFilling": {
                "generatorFillings": [0, 4, 6], "fillingStep": 2,
                "chargeRootSubgroupGeneratorFillings": [4],
                "chargeRootSubgroupFillingStep": 4, "ciGeneratorFillings": [6],
                "primitiveTranslationVectors": [["1/2", 0, 0], [0, 1, 0], [0, 0, 1]],
                "primitiveCellVolume": "1/2",
                "primitiveBasisGeneratesFullTranslationKernel": True,
                "allPresentationRelationsHaveZeroFilling": True}}

    def test_completed_ci_contribution_is_retained(self):
        answer = filling_check(self.record)
        self.assertEqual(answer["fillingStep"], 2)
        self.assertEqual(answer["chargeSubgroupFillingStep"], 4)
        self.assertEqual(answer["positivePrimitiveCellVolume"], "1/2")

    def test_actual_sg19_cluster_results(self):
        base = Path(__file__).resolve().parents[1] / "results/spacegroup_campaign_20261015/performance/cluster_d"
        for spin in ("spinless", "spin_half"):
            path = base / ("spacegroup_019_" + spin) / "result.json"
            answer = filling_check(json.loads(path.read_text())["classification"])
            self.assertEqual(answer["fillingStep"], 4)

    def test_false_certificate_does_not_hide_bad_relation(self):
        changed = deepcopy(self.record)
        changed["presentation"][1][1] = 2
        with self.assertRaisesRegex(ValueError, "relation changes"):
            filling_check(changed)

    def test_rejects_wrong_subgroup_or_cell_volume(self):
        for key, wrong in (("fillingStep", 4), ("chargeRootSubgroupFillingStep", 2),
                           ("ciGeneratorFillings", [0]), ("primitiveCellVolume", "1")):
            with self.subTest(field=key):
                changed = deepcopy(self.record)
                changed["spaceGroupFilling"][key] = wrong
                with self.assertRaises(ValueError):
                    filling_check(changed)


if __name__ == "__main__":
    unittest.main()
