"""Accepted 4+1D provenance, physical symmetry dictionaries, and response tables.

These integration checks reuse saved complete cluster computations. They never
rerun a formula engine or replace computed groups by reference answers.
"""
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "results/four_dimensional_20261016"

from scripts.collect_calibrated_4p1d import collect, validate_background, validate_record
from scripts.build_calibrated_4p1d import build_tables, load_collection

# The public catalogue script uses sibling CLI-module imports. Exercise its
# real renderer without loading unrelated 2+1D/3+1D catalogues.
with patch.object(sys, "path", [str(ROOT / "scripts"), *sys.path]):
    from scripts.build_current_tables import Catalogue


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class CalibratedFourDimensionalCollectionTests(unittest.TestCase):
    def test_inherited_acceptance_is_hash_pinned_and_does_not_duplicate_records(self):
        parent = FIXTURE / 'accepted.json'
        child = self.base / 'inherited.json'
        data = {'schemaVersion': 1, 'accepted': True, 'filesSHA256': {}, 'records': [], 'sources': {},
                'extends': [{'path': str(parent.relative_to(ROOT)), 'sha256': digest(parent)}]}
        write(child, data)
        merged = load_collection(self._catalogue(), child)
        expected = read(parent)['records']
        self.assertEqual([r['input']['id'] for r in merged['records']], [r['input']['id'] for r in expected])
        self.assertEqual(merged['records'][0]['provenance'], expected[0]['provenance'])
        data['extends'][0]['sha256'] = '0' * 64
        write(child, data)
        with self.assertRaisesRegex(ValueError, 'Inherited accepted collection changed'):
            load_collection(self._catalogue(), child)
        data['extends'][0]['sha256'] = digest(parent)
        data['records'] = [expected[0]]
        write(child, data)
        with self.assertRaisesRegex(ValueError, 'silently replace'):
            load_collection(self._catalogue(), child)

    def setUp(self):
        # Collector provenance deliberately uses paths relative to ROOT.
        temporary = tempfile.TemporaryDirectory(prefix=".test-calibrated-4p1-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.base = Path(temporary.name)
        self.cyclic = self.base / "cyclic"
        self.signed = self.base / "signed"
        self._selected_campaign("cyclic", self.cyclic, ["internal_cyclic_2_4p1"], [2])
        self._selected_campaign("signed", self.signed,
                                ["signed_" + case + "_4p1" for case in
                                 ("H_plus", "H_minus", "AI_relative", "AII_relative")],
                                ["H_plus", "H_minus", "AI_relative", "AII_relative"])
        self.campaigns = [("cyclic", self.cyclic), ("signed", self.signed)]

    @staticmethod
    def _selected_campaign(family, destination, case_ids, selection):
        source = FIXTURE / "raw" / family
        destination.mkdir()
        shutil.copy2(source / "source.json", destination / "source.json")
        for case in case_ids:
            shutil.copytree(source / case, destination / case)
        write(destination / "selection.json", selection)
        summary = [row for row in read(source / "summary.json") if row["id"] in case_ids]
        write(destination / "summary.json", summary)
        campaign = read(source / "campaign.json")
        if family == "cyclic":
            campaign.update(orders=selection, completed=len(case_ids))
        else:
            campaign.update(selectedCases=selection, caseCount=len(case_ids), runs=summary)
        write(destination / "campaign.json", campaign)

    def _collect(self, name="accepted"):
        output = self.base / name
        validation = collect(self.campaigns, output)
        return output, validation

    def _catalogue(self):
        catalogue = Catalogue.__new__(Catalogue)
        catalogue.output = self.base / "tables"
        catalogue.inputs, catalogue.files, catalogue.index = {}, {}, []
        return catalogue

    def _refresh_signed_input(self, case, changed_input):
        """Keep sidecars consistent so the physical dictionary is the rejection."""
        directory = self.signed / case
        write(directory / "input.json", changed_input)
        record = read(directory / "result.json")
        record["input"] = changed_input
        record["run"]["inputSHA256"] = digest(directory / "input.json")
        write(directory / "result.json", record)
        write(directory / "run.json", record["run"])
        summary = read(self.signed / "summary.json")
        summary = [record["run"] if row["id"] == case else row for row in summary]
        write(self.signed / "summary.json", summary)
        campaign = read(self.signed / "campaign.json")
        campaign["runs"] = summary
        write(self.signed / "campaign.json", campaign)

    def test_selected_cyclic_and_signed_acceptance_preserves_complete_records(self):
        original = {str(path.relative_to(directory)): path.read_bytes()
                    for _, directory in self.campaigns for path in directory.rglob("result.json")}
        output, validation = self._collect()
        self.assertTrue(validation["accepted"])
        self.assertEqual(validation["status"], "PASS")
        self.assertEqual(validation["completeResultCount"], 5)
        data = read(output / "accepted.json")
        self.assertEqual(set(validation["selectedCases"]),
                         {r["input"]["id"] for r in data["records"]})
        for record in data["records"]:
            provenance = record["provenance"]
            self.assertFalse(Path(provenance["path"]).is_absolute())
            raw = ROOT / provenance["path"]
            self.assertEqual(digest(raw), provenance["record_sha256"])
            self.assertEqual(raw.read_bytes(), original[str(Path(record["input"]["id"]) / "result.json")])
        # Acceptance hashes every raw artifact and its pinned reference ledger.
        for relative, expected in data["filesSHA256"].items():
            self.assertEqual(digest(output / relative), expected)
        self.assertEqual(read(output / "raw/cyclic/selection.json"), [2])
        self.assertEqual(len(read(output / "raw/signed/selection.json")), 4)

    def test_tampered_input_is_rejected_before_reference_comparison(self):
        path = self.cyclic / "internal_cyclic_2_4p1" / "input.json"
        changed = read(path)
        changed["omega"] = "alpha^2/2"
        write(path, changed)
        with self.assertRaisesRegex(ValueError, "input hash mismatch"):
            self._collect()

    def test_tampered_complete_cycle_evidence_is_rejected(self):
        directory = self.cyclic / "internal_cyclic_2_4p1"
        evidence = read(directory / "result.json")["evidence"]
        path = directory / evidence["path"]
        # Whitespace preserves the JSON data, but changes the recorded evidence.
        path.write_bytes(path.read_bytes() + b" \n")
        with self.assertRaisesRegex(ValueError, "evidence hash mismatch"):
            self._collect()

    def test_equal_abstract_groups_do_not_allow_AI_AII_reference_swap(self):
        ai = read(self.signed / "signed_AI_relative_4p1/result.json")
        aii = read(self.signed / "signed_AII_relative_4p1/result.json")
        self.assertEqual(ai["classification"]["torsion"], aii["classification"]["torsion"])
        self.assertEqual(ai["classification"]["freeRank"], aii["classification"]["freeRank"])
        changed = deepcopy(ai["input"])
        changed["referenceTarget"] = "time_reversal_AII"
        self._refresh_signed_input("signed_AI_relative_4p1", changed)
        # Input integrity itself passes; the failure must be the omega dictionary.
        validate_record(self.signed / "signed_AI_relative_4p1/result.json",
                        read(self.signed / "source.json"))
        with self.assertRaisesRegex(ValueError, "different symmetry background: omega"):
            self._collect()

    def test_signed_dictionary_checks_s_and_rho_independently(self):
        ledger = read(FIXTURE / "reference_targets.json")
        target = next(case for case in ledger["cases"] if case["id"] == "unitary_charge_conjugation_Hplus")
        inputs = read(self.signed / "signed_H_plus_4p1/input.json")
        validate_background(inputs, target)
        for key, value in (("s", "alpha"), ("rho", "0")):
            changed = dict(inputs, **{key: value})
            with self.subTest(key=key), self.assertRaisesRegex(ValueError, "different symmetry background: " + key):
                validate_background(changed, target)

    def test_missing_selected_case_is_rejected(self):
        shutil.rmtree(self.signed / "signed_AII_relative_4p1")
        with self.assertRaisesRegex(ValueError, "Selected case coverage"):
            self._collect()

    def test_accepted_evidence_mutation_is_rejected_by_table_loader(self):
        output, _ = self._collect()
        path = output / "raw/signed/signed_H_minus_4p1/result.json"
        path.write_bytes(path.read_bytes() + b"\n")
        with self.assertRaisesRegex(ValueError, "Accepted 4\\+1D evidence changed"):
            load_collection(self._catalogue(), output / "accepted.json")

    def test_table_signatures_keep_intrinsic_sectors_and_internal_symmetries_separate(self):
        output, _ = self._collect()
        catalogue = self._catalogue()
        accepted = load_collection(catalogue, output / "accepted.json")
        original = deepcopy(accepted)
        build_tables(catalogue, accepted)
        self.assertEqual(accepted, original, "Rendering must not mutate accepted raw results")
        paths = {
            "relative": "4p1d/internal_cyclic/intrinsic_zero.json",
            "full": "4p1d/internal_cyclic/intrinsic_all.json",
            "charge_conjugation": "4p1d/charge_conjugation.json",
            "time_reversal": "4p1d/time_reversal_intrinsic_zero.json",
        }
        tables = {key: json.loads(catalogue.files[path]) for key, path in paths.items()}
        zero = {"torsion": [], "freeRank": 0}
        c2 = {"torsion": [2, 8], "freeRank": 0}
        self.assertEqual(tables["relative"]["rows"][0]["cells"]["stacking"]["group"], c2)
        self.assertEqual(tables["full"]["rows"][0]["cells"]["stacking"]["group"],
                         {"torsion": [2, 8], "freeRank": 2})
        self.assertEqual(tables["relative"]["rows"][0]["cells"]["intrinsic"]["group"], zero)
        self.assertEqual(tables["full"]["rows"][0]["cells"]["intrinsic"]["group"],
                         {"torsion": [], "freeRank": 2})
        signed = {row["id"]: row for row in tables["charge_conjugation"]["rows"]}
        self.assertEqual(signed["signed_H_plus_4p1"]["cells"]["stacking"]["group"],
                         {"torsion": [2], "freeRank": 0})
        self.assertEqual(signed["signed_H_minus_4p1"]["cells"]["stacking"]["group"],
                         {"torsion": [2, 2, 2], "freeRank": 0})
        self.assertEqual({row["id"] for row in tables["time_reversal"]["rows"]},
                         {"signed_AI_relative_4p1", "signed_AII_relative_4p1"})
        for row in tables["time_reversal"]["rows"]:
            self.assertEqual(row["cells"]["stacking"]["group"], zero)
            self.assertEqual(row["cells"]["intrinsic"]["group"], zero)
        self.assertEqual(len(catalogue.index), 6)  # C2 has two distinct sectors.
        self.assertEqual(len({(row["id"], row["n0_scope"]) for row in catalogue.index}), 6)
        for key, table in tables.items():
            self.assertEqual([c["key"] for c in table["columns"][:4]], ["e", "n", "charge", "phase"])
            self.assertEqual(table["spatial_dimension"], 4)
            self.assertEqual(table["physical_spin"], "not_applicable_internal")
            self.assertEqual(table["n0_scope"], "intrinsic_all" if key == "full" else "intrinsic_zero")
            markdown = catalogue.files[paths[key].replace(".json", ".md")]
            self.assertIn("**✓**", markdown)
            self.assertNotIn("**×** ", "\n".join(line for line in markdown.splitlines() if line.startswith("|")))
            for row in table["rows"]:
                for source in table["sources"]:
                    reference = row["cells"][source]
                    if reference["availability"] == "available":
                        self.assertEqual(reference["comparison_status"], "match")


if __name__ == "__main__":
    unittest.main()
