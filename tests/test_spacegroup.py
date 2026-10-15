"""Full affine presentations and weak neutral E8 roots, including screws."""
from copy import deepcopy
import unittest

from insulator_catalog.catalog import build_group
from insulator.e8_spacegroup import spacegroup_h1, extend_spacegroup_classification
from insulator.e8_pointgroup import finite_pointgroup_h1


class SpaceGroupNeutralExtension(unittest.TestCase):
    def test_elementary_affine_h1_and_screw_periods(self):
        # These elementary groups are checked from their exported presentations,
        # independently of any literature table or classification fixture.
        for n, free, torsion in ((1, 3, []), (2, 3, [2]), (4, 1, []),
                                 (6, 1, [2]), (14, 1, [2]), (19, 0, [])):
            with self.subTest(space_group=n):
                data = build_group("spacegroup", n)
                answer = spacegroup_h1(data)
                self.assertEqual(answer["freeRank"], free)
                self.assertEqual(answer["torsion"], torsion)
                self.assertTrue(answer["certificate"]["fullAffinePresentationUsed"])
                self.assertFalse(answer["certificate"]["holonomySubstitutionUsedForCohomology"])
                q = answer["principalCoboundaryCoordinates"]
                for row in answer["primitiveTranslationValues"]:
                    self.assertEqual(sum(x*y for x,y in zip(row,q)), 0)
                self.assertEqual(answer, spacegroup_h1(build_group("spacegroup", n, "spin_half")))
        for n, period in ((4, 2), (76, 4), (144, 3), (169, 6)):
            h = spacegroup_h1(build_group("spacegroup", n))
            self.assertEqual(h["freeRank"], 1)
            self.assertEqual(sorted(abs(row[0]) for row in h["primitiveTranslationValues"]), [0, 0, period])

    def test_free_and_torsion_full_model_presentation(self):
        data = build_group("spacegroup", 2)
        ci = {"theory": "U(1)^f insulator", "spatialDimension": 3,
              "torsion": [3], "freeRank": 1,
              "presentationGeneratorCount": 2, "presentation": [[3,0]],
              "generators": [{"kind": "test-torsion"}, {"kind": "test-free"}],
              "witnesses": [], "nativeChainIdentitiesVerified": True}
        result = {"input": data, "classification": ci,
                  "run": {"id": data["id"], "status": "complete", "exitCode": 0}}
        answer = extend_spacegroup_classification(result)
        self.assertEqual(answer["torsion"], [6])
        self.assertEqual(answer["freeRank"], 4)
        self.assertEqual(answer["coordinateBlocks"]["ciSector"]["start"], 4)
        self.assertEqual(answer["ciSector"], ci)
        self.assertFalse(answer["physicalClassificationCertified"])
        self.assertTrue(any(w["kind"] == "neutral-principal-gauge" for w in answer["witnesses"]))
        self.assertFalse(any(w["kind"] == "neutral-root-power" for w in answer["witnesses"]))
        self.assertEqual(answer["e8H1"]["torsionRootWitness"]["order"], 2)

    def test_rejects_holonomy_substitution_and_corrupt_affine_words(self):
        data = build_group("spacegroup", 4)
        with self.assertRaises(ValueError):
            finite_pointgroup_h1(data)
        changed = deepcopy(data)
        changed["finite_presentation"]["relators"].append([1])
        with self.assertRaises(ValueError):
            spacegroup_h1(changed)
        changed = deepcopy(data)
        changed["primitive_translations"]["words"][0] = []
        with self.assertRaises(ValueError):
            spacegroup_h1(changed)
        changed = deepcopy(data)
        changed["finite_presentation"]["isomorphism_verified"] = False
        with self.assertRaises(ValueError):
            spacegroup_h1(changed)


if __name__ == "__main__":
    unittest.main()
