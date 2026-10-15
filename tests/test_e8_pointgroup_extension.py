"""Global E8 cocycle/gauge certificates and immutable 3+1D model extension."""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

from insulator.e8_pointgroup import extend_classification, finite_pointgroup_h1, presentation_invariants


ROOT = Path(__file__).resolve().parents[1]


def catalog(index, spin="spinless"):
    path = ROOT / "insulator_catalog/generated" / f"point3_{index:02d}_{spin}.json"
    return json.loads(path.read_text())


def ci_fixture(data, order=3):
    """Small exact presentation fixture; this is not a claimed physical result."""
    return {"input": data,
            "classification": {"theory": "U(1)^f insulator", "spatialDimension": 3,
                               "scope": "test presentation only",
                               "torsion": [order], "freeRank": 0,
                               "presentationGeneratorCount": 1, "presentation": [[order]],
                               "generators": [{"kind": "phase", "nativePhase": [f"1/{order}"]}],
                               "witnesses": [{"kind": "fixture-root-power", "order": order}],
                               "neutralE8AbsentByCohomology": False},
            "run": {"id": data["id"], "status": "complete", "exitCode": 0,
                    "sourceSHA256": "a" * 64}}


class E8PointGroupExtension(unittest.TestCase):
    def test_all_64_catalog_presentations_and_global_gauges(self):
        counts = {"proper": 0, "improper": 0}
        for spin in ("spinless", "spin_half"):
            for index in range(1, 33):
                data = catalog(index, spin)
                with self.subTest(case=data["id"]):
                    answer = finite_pointgroup_h1(data)
                    reversing = any(data["s"])
                    counts["improper" if reversing else "proper"] += 1
                    self.assertEqual(answer["freeRank"], 0)
                    self.assertEqual(answer["torsion"], [2] if reversing else [])
                    table, signs = data["multiplication"], [1 - 2 * bit for bit in data["s"]]
                    for root in answer["roots"]:
                        values = root["e1ValuesByElement"]
                        gauge = root["rootPowerRemovalGauge"]["v0"]
                        # An independent characterization of finite crossed
                        # homomorphisms: zero on ker(s), one constant on its coset.
                        odd_values = {values[g] for g in range(len(table)) if signs[g] == -1}
                        self.assertEqual(len(odd_values), 1)
                        self.assertEqual(abs(next(iter(odd_values))), 1)
                        for g in range(len(table)):
                            self.assertEqual(2 * values[g] + (signs[g] - 1) * gauge, 0)
                            for h in range(len(table)):
                                self.assertEqual(values[table[g][h]], values[g] + signs[g] * values[h])
                    self.assertEqual(answer["certificate"]["crossedHomomorphismIdentityCount"],
                                     data["order"] ** 2 * int(reversing))
        self.assertEqual(counts, {"proper": 22, "improper": 42})

    def test_independent_factor_smith_form_and_witness_embedding(self):
        base = ci_fixture(catalog(4), order=3)
        original = deepcopy(base)
        result = extend_classification(base)
        self.assertEqual(result["torsion"], [6])  # Z2 x Z3, not [2,3].
        self.assertEqual(result["freeRank"], 0)
        self.assertEqual(result["presentationGeneratorCount"], 2)
        self.assertEqual(abs(result["presentation"][0][0]), 2)
        self.assertEqual(result["presentation"][0][1], 0)
        self.assertEqual(result["presentation"][1], [0, 3])
        self.assertEqual(result["ciSector"], original["classification"])
        self.assertEqual(result["generators"][1]["completedCIRoot"],
                         original["classification"]["generators"][0])
        self.assertEqual(result["coordinateBlocks"]["ciSector"], {"start": 1, "count": 1})
        self.assertFalse(result["physicalClassificationCertified"])
        self.assertFalse(result["legacyNeutralE8AbsentByCohomology"]["usedAsPhysicalCertificate"])
        self.assertEqual(base, original)
        proper = extend_classification(ci_fixture(catalog(6), order=4))
        self.assertEqual(proper["torsion"], [4])
        self.assertEqual(proper["coordinateBlocks"]["ciSector"]["start"], 0)

    def test_trivial_and_free_presentations(self):
        self.assertEqual(presentation_invariants([], 2)["freeRank"], 2)
        self.assertEqual(presentation_invariants([[]], 0)["torsion"], [])
        base = ci_fixture(catalog(2))
        base["classification"].update(torsion=[], freeRank=0, presentationGeneratorCount=0,
                                       presentation=[], generators=[], witnesses=[])
        answer = extend_classification(base)
        self.assertEqual(answer["torsion"], [2])
        self.assertEqual(answer["freeRank"], 0)
        base["classification"].update(freeRank=1, presentationGeneratorCount=1,
                                       presentation=[], generators=[{"kind": "free-fixture"}])
        answer = extend_classification(base)
        self.assertEqual(answer["torsion"], [2])
        self.assertEqual(answer["freeRank"], 1)

    def test_rejects_incompatible_or_uncertified_input_presentations(self):
        changes = (
            lambda a: a["run"].update(status="running"),
            lambda a: a["classification"].update(spatialDimension=4),
            lambda a: a["classification"].update(neutralE8Included=True),
            lambda a: a["classification"].update(theory="Z2^f superconductor"),
            lambda a: a["classification"].update(nativeChainIdentitiesVerified=False),
            lambda a: a["classification"].update(torsion=[5]),
            lambda a: a["classification"].update(generators=[]),
            lambda a: a["input"].update(translation_subgroup_present=True),
            lambda a: a["input"].update(s=[1, 1]),
            lambda a: a["input"].update(multiplication=[[0, 1], [1, 1]]),
        )
        for change in changes:
            base = ci_fixture(catalog(4))
            change(base)
            with self.subTest(change=change), self.assertRaises(ValueError):
                extend_classification(base)

    def test_cli_consumes_exact_ci_artifacts_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory(prefix="insulator-e8-extension-test-") as temp:
            root = Path(temp)
            campaign, output = root / "ci", root / "e8"
            campaign.mkdir()
            data = catalog(4)
            case = campaign / data["id"]
            case.mkdir()
            raw_input = (json.dumps(data, sort_keys=True) + "\n").encode()
            (case / "input.json").write_bytes(raw_input)
            result = ci_fixture(data)
            result["run"]["inputSHA256"] = hashlib.sha256(raw_input).hexdigest()
            raw_result = (json.dumps(result, indent=2) + "\n").encode()
            (case / "result.json").write_bytes(raw_result)
            (campaign / "selection.json").write_text(json.dumps([data["id"]]))
            command = [sys.executable, str(ROOT / "scripts/extend_e8_3p1.py"),
                       "--ci-root", str(campaign), "--output", str(output), "--spin", "spinless"]
            first = subprocess.run(command, capture_output=True, text=True, cwd=ROOT)
            self.assertEqual(first.returncode, 0, first.stderr)
            target = output / data["id"]
            answer = json.loads((target / "result.json").read_text())
            self.assertEqual(answer["classification"]["torsion"], [6])
            self.assertEqual(answer["run"]["ciResultSHA256"], hashlib.sha256(raw_result).hexdigest())
            self.assertEqual((target / "ci_result.json").read_bytes(), raw_result)
            self.assertEqual((target / "input.json").read_bytes(), raw_input)
            before = (target / "result.json").read_bytes()
            second = subprocess.run(command, capture_output=True, text=True, cwd=ROOT)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual((target / "result.json").read_bytes(), before)
            result["run"]["inputSHA256"] = "0" * 64
            (case / "result.json").write_text(json.dumps(result))
            command[command.index(str(output))] = str(root / "bad-hash")
            bad = subprocess.run(command, capture_output=True, text=True, cwd=ROOT)
            self.assertNotEqual(bad.returncode, 0)
            self.assertIn("input hash", bad.stderr)


if __name__ == "__main__":
    unittest.main()
