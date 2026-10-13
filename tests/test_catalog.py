"""Independent algebraic validation of the campaign's symmetry inputs."""
import json
from pathlib import Path
from fractions import Fraction
from itertools import product
import unittest

from insulator_catalog.catalog import build_group, POINT2, POINT3, WALLPAPER

GENERATED = Path(__file__).resolve().parents[1] / "insulator_catalog" / "generated"


class CatalogTests(unittest.TestCase):
    def test_catalog_coverage_and_background_cocycles(self):
        paths = list(GENERATED.glob("*.json"))
        records = [json.loads(path.read_text()) for path in paths if ".index." not in path.name]
        self.assertEqual(len(records), 118)
        self.assertEqual((len(POINT2), len(WALLPAPER), len(POINT3)), (10, 17, 32))
        for r in records:
            with self.subTest(group=r["id"]):
                n, table = r["order"], r["multiplication"]
                pin = r["geometric_pin_minus"]
                self.assertEqual(table[0], list(range(n)))
                self.assertEqual([row[0] for row in table], list(range(n)))
                self.assertEqual(r["s"], r["rho"])
                self.assertEqual(r["circle_action"], [0] * n)
                self.assertTrue(all(0 in row for row in table))
                self.assertEqual(pin[0], [0] * n)
                self.assertEqual([row[0] for row in pin], [0] * n)
                # Full triple exhaustion, including cubic groups of order 48.
                for i, j, k in product(range(n), repeat=3):
                    self.assertEqual(table[table[i][j]][k], table[i][table[j][k]])
                    self.assertEqual((pin[j][k] - pin[table[i][j]][k]
                                      + pin[i][table[j][k]] - pin[i][j]) % 2, 0)
                for i, j in product(range(n), repeat=2):
                    self.assertEqual(r["s"][table[i][j]], (r["s"][i] + r["s"][j]) % 2)
                    self.assertEqual(Fraction(r["omega"][i][j]),
                                     Fraction(pin[i][j], 2) if r["spin"] == "spinless" else 0)

    def test_known_spin_lifts_and_physical_spin_cancellation(self):
        # A mirror and a pi rotation lift to square -1, while inversion lifts
        # to +1 because det(-I)(-I)=I. These test the geometric convention.
        for family, index, square in [("point2", 2, "1/2"), ("point2", 3, "1/2"),
                                      ("point3", 2, "0"), ("point3", 3, "1/2"),
                                      ("point3", 4, "1/2")]:
            r = build_group(family, index)
            self.assertEqual(r["omega"][1][1], square)
            self.assertTrue(all(x == "0" for row in build_group(family, index, "spin_half")["omega"] for x in row))

    def test_nonsymmorphic_wallpaper_geometry_survives(self):
        pg = build_group("wallpaper", 4)
        self.assertTrue(pg["translation_subgroup_present"])
        self.assertEqual(pg["catalog_constructor"], "SpaceGroupBBNWZ(2,index)")
        self.assertEqual(pg["affine_generators"][0][2][0], "1/2")
        self.assertEqual(pg["order"], 2)  # holonomy order; affine group is infinite
        self.assertIn("full_affine_group", pg["point_table_scope"])

    def test_invalid_indices_fail(self):
        for family, index in [("point2", 0), ("point3", 33), ("wallpaper", -1)]:
            with self.assertRaises(ValueError):
                build_group(family, index)

if __name__ == "__main__":
    unittest.main()
