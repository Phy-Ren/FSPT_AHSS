"""Replay small saved certificates and reject mathematically meaningful tampering.

No test runs GAP, recalculates a campaign, or supplies a physical target group
to an engine.  Fixtures are complete repository artifacts from cluster runs.
"""
from copy import deepcopy
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import shutil
import tempfile
import unittest

from sympy import Matrix

from insulator.e8_pointgroup import presentation_invariants
from insulator.translation4p1 import verify_certificate
from scripts.collect_calibrated_4p1d import collect, source_columns, validate_record
from scripts.verify_abelian_4p1 import verify


ROOT = Path(__file__).resolve().parents[1]
TRANSLATIONS = ROOT / "results/four_dimensional_batch2_20261016/raw/translations"
ABELIAN = ROOT / "results/four_dimensional_abelian_20261016/raw/abelian"
REFERENCE_LEDGER = ROOT / "docs/4p1d/calibration/batch2_targets.json"


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class SavedCaseTest(unittest.TestCase):
    """Copy only one small case when a test needs to mutate provenance."""

    def copied_case(self, campaign, case_id):
        temporary = tempfile.TemporaryDirectory(prefix="batch2-certificate-")
        self.addCleanup(temporary.cleanup)
        directory = Path(temporary.name) / case_id
        shutil.copytree(campaign / case_id, directory)
        return directory, read(campaign / "source.json")

    @staticmethod
    def replace_input(directory, record, changed):
        # Keep the sidecars and their hashes consistent: rejection must come
        # from mathematical/background binding, not stale provenance bytes.
        write(directory / "input.json", changed)
        record["input"] = changed
        record["run"]["inputSHA256"] = digest(directory / "input.json")
        write(directory / "run.json", record["run"])
        write(directory / "result.json", record)


class SavedTranslationCertificateTests(SavedCaseTest):
    @classmethod
    def setUpClass(cls):
        path = TRANSLATIONS / "translations_z2_4p1/result.json"
        if not path.exists():
            raise unittest.SkipTest("The saved batch-two translation campaign is not present.")
        cls.record = read(path)
        cls.evidence = read(path.parent / cls.record["evidence"]["path"])

    def test_saved_certificate_replays_without_a_physical_target(self):
        replay = verify_certificate(self.record["classification"], self.evidence)
        self.assertEqual(replay, self.record["certificateVerification"])
        self.assertFalse(replay["referenceGroupUsed"])

    def test_nonunimodular_change_of_basis_is_rejected(self):
        evidence = deepcopy(self.evidence)
        # At degree zero the differential vanishes, so multiplying a Smith
        # basis vector by two still satisfies L*d*R=D.  Unimodularity must be
        # checked separately to avoid silently discarding integer states.
        degree = evidence["resolution"]["degrees"][0]
        degree["smithRight"]["entries"][0][0] *= 2
        with self.assertRaisesRegex(ValueError, "unimodular"):
            verify_certificate(self.record["classification"], evidence)

    def test_period_and_cocycle_rescaling_cannot_change_the_primitive_lattice(self):
        evidence = deepcopy(self.evidence)
        degree = evidence["resolution"]["degrees"][2]
        basis = degree["canonicalCocycles"]["entries"]
        row = next(i for i, values in enumerate(basis) if values[0])
        basis[row][0] *= 2
        with self.assertRaisesRegex(ValueError, "Canonical cocycle or primitive period"):
            verify_certificate(self.record["classification"], evidence)

    def test_consistently_rehashed_wrong_differential_is_still_rejected(self):
        directory, source = self.copied_case(TRANSLATIONS, "translations_z2_4p1")
        record = read(directory / "result.json")
        path = directory / record["evidence"]["path"]
        evidence = read(path)
        evidence["resolution"]["degrees"][1]["coboundary"]["entries"][0][0] += 1
        write(path, evidence)
        record["evidence"]["sha256"] = digest(path)
        write(directory / "result.json", record)
        with self.assertRaisesRegex(ValueError, "differential disagrees with simplex faces"):
            validate_record(directory / "result.json", source)

    def test_translation_rank_is_bound_to_the_saved_resolution(self):
        directory, source = self.copied_case(TRANSLATIONS, "translations_z2_4p1")
        record = read(directory / "result.json")
        changed = deepcopy(record["input"])
        changed["translationRank"] = 3
        self.replace_input(directory, record, changed)
        with self.assertRaises(ValueError):
            validate_record(directory / "result.json", source)

    def test_translation_filtration_is_bound_to_the_certified_integer_lattices(self):
        directory, source = self.copied_case(TRANSLATIONS, "translations_z2_4p1")
        record = read(directory / "result.json")
        record["classification"]["finalFiltration"]["e"]["freeRank"] += 1
        write(directory / "result.json", record)
        with self.assertRaises(ValueError):
            validate_record(directory / "result.json", source)


class SavedAbelianCertificateTests(SavedCaseTest):
    @classmethod
    def setUpClass(cls):
        path = ABELIAN / "internal_abelian_2x2_4p1/result.json"
        if not path.exists():
            raise unittest.SkipTest("The saved batch-two abelian campaign is not present.")
        cls.record = read(path)

    def classification(self):
        return deepcopy(self.record["classification"])

    def test_saved_nontrivial_incoming_certificate_replays(self):
        c = self.classification()
        replay = verify(c)
        self.assertEqual(replay["status"], "PASS")
        self.assertGreater(replay["incomingGenerators"], 0)
        self.assertGreater(c["preIncomingOrder"], c["actualGroupOrder"])
        self.assertTrue(replay["incomingStateIndependentBeforeQuotient"])
        self.assertTrue(replay["chargeKernelMaximalityVerified"])
        self.assertFalse(replay["referenceGroupUsed"])

    def test_incoming_action_must_be_state_independent_before_its_own_quotient(self):
        c = self.classification()
        size = c["presentationGeneratorCount"]
        pre = Matrix(c["presentation"][:size])
        incoming = c["incomingRelations"][0]
        # This incoming element is genuinely nonzero before quotienting.
        self.assertTrue(any(value.q != 1 for value in Matrix([incoming]) * pre.inv()))
        c["incomingRelations"][1] = [2 * value for value in incoming]
        c["presentation"][size + 1] = list(c["incomingRelations"][1])
        witness = next(w for w in c["witnesses"]
                       if w["kind"] == "incoming-charge-gauge"
                       and w["index"] == 1 and w["baseRoot"] == 1)
        witness["phaseCoordinates"] = [2 * value for value in witness["phaseCoordinates"]]
        witness["chargeCoordinates"] = [2 * value for value in witness["chargeCoordinates"]]
        nonphase = sum(not g["kind"].startswith("phase_") for g in c["generators"])
        phase_witnesses = [w for w in c["witnesses"] if w["kind"] == "phase-reduction"]
        phase_witnesses[nonphase + 1]["phaseCoordinates"] = list(witness["phaseCoordinates"])
        # The final quotient is unchanged: a check there would miss this error.
        self.assertEqual(presentation_invariants(c["presentation"], size),
                         presentation_invariants(self.record["classification"]["presentation"], size))
        with self.assertRaisesRegex(ValueError, "before quotient"):
            verify(c)

    def test_incoming_relation_list_cannot_disagree_with_the_final_presentation(self):
        c = self.classification()
        c["incomingRelations"] = [[0] * len(row) for row in c["incomingRelations"]]
        with self.assertRaises(ValueError):
            verify(c)

    def test_duplicate_commutator_does_not_count_as_complete_pair_coverage(self):
        c = self.classification()
        c["commutatorWitnesses"][1] = deepcopy(c["commutatorWitnesses"][0])
        with self.assertRaises(ValueError):
            verify(c)

    def test_missing_charge_lift_cannot_silently_remove_a_boundary_check(self):
        c = self.classification()
        index = next(i for i, w in enumerate(c["witnesses"]) if w["kind"] == "charge-lift")
        c["witnesses"].pop(index)
        with self.assertRaises(ValueError):
            verify(c)

    def test_contained_but_nonmaximal_charge_kernel_is_rejected(self):
        c = self.classification()
        self.assertTrue(all(not any(row) for row in c["chargeObstructionMap"]))
        c["chargeKernelLattice"][0] = [2 * value for value in c["chargeKernelLattice"][0]]
        lift = next(w for w in c["witnesses"] if w["kind"] == "charge-lift")
        lift["chargeCohomology"] = list(c["chargeKernelLattice"][0])
        # Containment still holds. The independent index check must reject it.
        with self.assertRaisesRegex(ValueError, "complete obstruction kernel"):
            verify(c)

    def test_an_obstructed_retained_charge_generator_is_rejected(self):
        c = self.classification()
        c["chargeObstructionMap"][0][0] = 1
        with self.assertRaisesRegex(ValueError, "remains obstructed"):
            verify(c)

    def test_charge_lift_and_phase_primitives_are_checked_exactly_modulo_one(self):
        for kind, field in (("charge-lift", "nativeSource"),
                            ("phase-reduction", "nativeResidualPhase")):
            with self.subTest(kind=kind):
                c = self.classification()
                witness = next(w for w in c["witnesses"] if w["kind"] == kind)
                witness[field][0] = str(Fraction(witness[field][0]) + Fraction(1, 2))
                with self.assertRaisesRegex(ValueError, "exact boundary equation"):
                    verify(c)

    def test_graded_group_is_not_accepted_merely_because_the_total_group_matches(self):
        directory, source = self.copied_case(ABELIAN, "internal_abelian_2x2_4p1")
        record = read(directory / "result.json")
        record["classification"]["finalFiltration"]["charge"]["torsion"] = []
        write(directory / "result.json", record)
        write(directory / "native.json", record["classification"])
        with self.assertRaisesRegex(ValueError, "final filtration does not reproduce"):
            validate_record(directory / "result.json", source)

    def test_computed_abelian_factors_are_bound_to_the_input(self):
        directory, source = self.copied_case(ABELIAN, "internal_abelian_2x2_4p1")
        record = read(directory / "result.json")
        changed = deepcopy(record["input"])
        changed["factors"] = [2, 4]
        changed["order"] = 8
        self.replace_input(directory, record, changed)
        with self.assertRaises(ValueError):
            validate_record(directory / "result.json", source)


class CompletedSubsetCollectionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        if not (ABELIAN / "campaign.json").exists():
            raise unittest.SkipTest("The saved abelian campaign is not present.")
        cls.selected = sorted(read(path)["input"]["id"] for path in ABELIAN.glob("*/result.json"))
        cls.failed = "internal_abelian_4x8_4p1"

    def setUp(self):
        # Accepted provenance is deliberately relative to the repository root.
        temporary = tempfile.TemporaryDirectory(prefix=".test-batch2-subset-", dir=ROOT)
        self.addCleanup(temporary.cleanup)
        self.directory = Path(temporary.name)

    def collect(self, name, selection=None):
        output = self.directory / name
        result = collect([("abelian", ABELIAN)], output,
                         additional_ledgers=[REFERENCE_LEDGER], completed_selections=selection)
        return output, result

    def test_an_incomplete_campaign_is_rejected_without_an_explicit_selection(self):
        self.assertEqual(read(ABELIAN / "campaign.json")["status"], "incomplete")
        with self.assertRaisesRegex(ValueError, "Only a completed selected campaign"):
            self.collect("implicit")

    def test_explicit_complete_subset_preserves_the_entire_original_campaign(self):
        self.assertEqual(len(self.selected), 12)
        original = {str(path.relative_to(ABELIAN)): path.read_bytes()
                    for path in ABELIAN.rglob("*") if path.is_file()}
        output, validation = self.collect("explicit", {"abelian": self.selected})
        copied = output / "raw/abelian"
        self.assertEqual({str(path.relative_to(copied)): path.read_bytes()
                          for path in copied.rglob("*") if path.is_file()}, original)
        self.assertEqual(read(copied / "campaign.json")["status"], "incomplete")
        self.assertEqual(read(copied / self.failed / "run.json")["status"], "timeout")
        self.assertFalse((copied / self.failed / "result.json").exists())
        self.assertEqual(validation["completeResultCount"], 12)
        selection = validation["campaignSelections"][0]
        self.assertEqual(selection["originalSelection"], read(ABELIAN / "selection.json"))
        self.assertEqual(selection["acceptedSelection"], self.selected)
        self.assertEqual(selection["excludedSelection"], [self.failed])
        self.assertEqual(selection["originalStatus"], "incomplete")
        self.assertEqual(selection["campaignSHA256"], digest(ABELIAN / "campaign.json"))
        self.assertTrue(selection["explicitCompletedSubset"])
        self.assertTrue(selection["rawCampaignPreserved"])
        accepted = read(output / "accepted.json")
        self.assertEqual(sorted(row["input"]["id"] for row in accepted["records"]), self.selected)
        for relative, contents in original.items():
            self.assertEqual(accepted["filesSHA256"]["raw/abelian/" + relative],
                             hashlib.sha256(contents).hexdigest())
        # The selection/exclusion decision is itself pinned, not just raw bytes.
        self.assertEqual(accepted["filesSHA256"]["validation.json"], digest(output / "validation.json"))
        labels = {source["columnLabel"] for source in accepted["sources"].values()}
        self.assertIn("Spin-c bordism derivation", labels)
        self.assertIn("Ossa/Spin-c derivation", labels)

    def test_selecting_a_timed_out_case_cannot_create_an_accepted_result(self):
        with self.assertRaisesRegex(ValueError, "Selected case coverage"):
            self.collect("failed", {"abelian": self.selected + [self.failed]})

    def test_malformed_duplicate_unknown_and_absent_campaign_selections_are_rejected(self):
        malformed = [[], self.selected[0], {"case": self.selected[0]},
                     [self.selected[0], self.selected[0]], [123], ["unknown_case"]]
        for index, selection in enumerate(malformed):
            with self.subTest(selection=selection), self.assertRaisesRegex(ValueError, "nonempty distinct subset"):
                self.collect("malformed_" + str(index), {"abelian": selection})
        with self.assertRaisesRegex(ValueError, "absent campaign"):
            self.collect("absent", {"unknown_campaign": self.selected})

    def test_distinct_derivations_do_not_overwrite_a_shared_primary_source_column(self):
        ledger = read(REFERENCE_LEDGER)
        rank_two = deepcopy(next(case for case in ledger["cases"] if case["id"] == "internal_abelian_2x2"))
        higher = deepcopy(next(case for case in ledger["cases"] if case["id"] == "internal_abelian_2x2x2"))
        # Different derivations can cite exactly the same primary papers.
        # Their column identity must also retain the derivation and its scope.
        higher["sources"][0]["sources"] = list(rank_two["sources"][0]["sources"])
        first_sources, first_refs = source_columns(ledger, rank_two, "internal_abelian")
        second_sources, second_refs = source_columns(ledger, higher, "internal_abelian")
        self.assertFalse(set(first_sources) & set(second_sources))
        combined = {**first_sources, **second_sources}
        self.assertEqual({source["columnLabel"] for source in combined.values()},
                         {"Spin-c bordism derivation", "Ossa/Spin-c derivation"})
        self.assertEqual(set(first_refs), set(first_sources))
        self.assertEqual(set(second_refs), set(second_sources))
        for source, target in ((next(iter(first_sources.values())), rank_two),
                               (next(iter(second_sources.values())), higher)):
            self.assertIn(target["sources"][0]["method"], source["method"])
            self.assertEqual(source["url"], target["sources"][0]["derivationURL"])
        same_derivation = next(case for case in ledger["cases"] if case["id"] == "internal_abelian_2x4")
        same_sources, _ = source_columns(ledger, same_derivation, "internal_abelian")
        self.assertEqual(set(same_sources), set(first_sources))


if __name__ == "__main__":
    unittest.main()
