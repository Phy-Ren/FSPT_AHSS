"""Saved-evidence parsing controls; no new cochain computation."""
import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("pip_diagnostics", ROOT / "scripts/analyze_pip_diagnostics.py")
diag = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(diag)


def empty_result():
    return dict(space_group=1, source_id="fixture", formula_convention="fixture",
        convention="physical-spinless-det-sign-Pin-minus", status="computed",
        classification_status="computed", majorana=[], complex_fermion=[], bosonic=[],
        pip=dict(orders=[], free_rank=0, torsion=[]), stacking=dict(status="computed", invariants=[]))


class DiagnosticsTests(unittest.TestCase):
    def test_h0_successive_images(self):
        d = empty_result()
        d["preH0IncomingGraded"] = dict(majorana=[2], complex_fermion=[2], bosonic=[2])
        q = dict(graded=dict(majorana=[], complex_fermion=[], bosonic=[]),
            incomingOrder=8, incomingCoordinates=[0, 0, 1],
            preQuotientLower=dict(invariants=[8]),
            basisChange=dict(incomingMCCohomologyCoordinates=[1]))
        d["stacking"]["h0IncomingQuotient"] = dict(backgroundQuotient=q, lower=dict(invariants=[]))
        result = diag.h0_incoming(d)
        self.assertEqual([result["differential_images"][f"d{i}"]["source_integer_multiple"]
                          for i in (2, 3, 4)], [1, 2, 4])
        self.assertEqual(result["source_kernel_after_d4"], 8)
        self.assertFalse(result["raw_d3_d4_coordinates_reconstructed"])
        d["majorana"] = [2]
        with self.assertRaises(ValueError):
            diag.h0_incoming(d)
        d["majorana"] = []
        q["incomingOrder"] = 4
        with self.assertRaises(ValueError):
            diag.h0_incoming(d)

    def test_unknown_carries_survive_unique_abstract_answer(self):
        d = empty_result()
        d["stacking"].update(invariants=[16], fullUpperPhaseWitness=False,
            pipSquareCertificate=dict(majoranaCoordinates=[1], majoranaCohomologyClass=[1],
                unknownCarries=["complex-fermion", "bosonic"], fullUpperPhaseWitness=False),
            pipExtensionCertificate=dict(status="computed", invariantOptions=[[16]], possibleHeights=[3]))
        square = diag.square_relation(d)
        self.assertEqual(square["unknown_layers"], ["complex-fermion", "bosonic"])
        self.assertNotIn("lower_coordinates", square)
        self.assertEqual(diag.upper_family(d)["full_invariant_options"], [[16]])
        d["stacking"]["pipExtensionCertificate"]["invariantOptions"] = [[8, 2]]
        with self.assertRaises(ValueError):
            diag.upper_family(d)

    def test_complete_known_ambiguous_family_is_inventory_not_failure(self):
        d = empty_result()
        d["status"] = d["stacking"]["status"] = "unresolved"
        d["stacking"]["pipExtensionCertificate"] = dict(status="ambiguous",
            invariantOptions=[[2, 8], [16]], possibleHeights=[2, 3])
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "sg1.json").write_text(json.dumps(d))
            result = diag.analyze(root, allow_partial=True)
            self.assertEqual(result["cohorts"]["upper_extension_ambiguous_isotype"], [1])
            d["stacking"].pop("pipExtensionCertificate")
            (root / "sg1.json").write_text(json.dumps(d))
            with self.assertRaises(ValueError):
                diag.analyze(root, allow_partial=True)

    def test_integer_period_16_does_not_merge_distinct_odd_candidates(self):
        d = empty_result()
        d["pip"].update(orders=[0], free_rank=1, free_lattice=dict(rank=1,
            h1BasisOrders=[0, 2], freeIndices=[1], certifiedIntegerPeriod=16,
            latticeBasis=[[1]], latticeIndex=1, generators=[],
            parityCandidates=[dict(status="killed", page=2, h1Coordinates=[1, 0], obstruction=[1]),
                dict(status="survives", page=4, h1Coordinates=[3, 0],
                    certificate=diag.ZERO_TARGET, d4_target=[]),
                dict(status="survives", page=4, h1Coordinates=[1, 1],
                    certificate=diag.ZERO_TARGET, d4_target=[])]))
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "sg1.json").write_text(json.dumps(d))
            free = diag.analyze(root, True)["records"][0]["free_lattice"]
            self.assertEqual(free["tested_free_residues"], [[1], [3]])
            self.assertEqual(free["candidate_changes_preserving_free_parity"], [])
            changes = free["candidate_changes_preserving_free_residue"]
            self.assertEqual(len(changes), 1)
            self.assertEqual(changes[0]["free_residue"], [1])

    def test_wrong_classification_does_not_become_diagnostic_success(self):
        d = empty_result()
        d["status"] = "failed"
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            (root / "sg1.json").write_text(json.dumps(d))
            with self.assertRaises(ValueError):
                diag.analyze(root, True)


if __name__ == "__main__":
    unittest.main()
