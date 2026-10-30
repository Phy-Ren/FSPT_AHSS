"""Exact controls for source discrepancies, independent of published tables."""
from fractions import Fraction
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


def run_audit(name, variable):
    with tempfile.TemporaryDirectory() as td:
        result = Path(td) / "audit.json"
        script = Path(td) / "audit.g"
        script.write_text(
            'OnBreak:=function() Where(10);QUIT_GAP(1);end;;\n'
            f'U1_ROOT:="{ROOT}";;Read(Concatenation(U1_ROOT,"/gap/load.g"));\n'
            f'{variable}:="{result}";;Read(Concatenation(U1_ROOT,"/gap/{name}.g"));\n'
            'QUIT_GAP(0);\n'
        )
        process = subprocess.run(
            ["gap", "-q", "-b", str(script)], capture_output=True,
            text=True, timeout=180,
        )
        if process.returncode:
            raise AssertionError(process.stdout + process.stderr)
        return json.loads(result.read_text())


@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class DiscrepancyAuditTests(unittest.TestCase):
    def test_d2d_obstruction_restriction_and_gauge_independence(self):
        audit = run_audit("audit_d2d", "U1_D2D_AUDIT_OUT")
        for spin, item in audit.items():
            self.assertEqual(item["rawChargeOrders"], [2, 2])
            self.assertEqual(item["rawPhaseOrders"], [2, 2, 2])
            self.assertEqual(sum(r["obstructed"] for r in item["chargeRoots"]), 1)
            for root in item["chargeRoots"]:
                self.assertEqual(root["obstructed"], any(root["obstructionClass"]))
                if not root["obstructed"]:
                    self.assertEqual(root["fullGaugeRootPhase"], root["shortGaugeRootPhase"])
                    self.assertEqual(any(root["fullGaugeRootPhase"]), spin == "spin_half")
            for incoming in item["incomingCharge"]:
                self.assertEqual(incoming["full"], incoming["short"])
                self.assertEqual(any(incoming["full"]), spin == "spinless")
            self.assertEqual(any(item["integerCIObstructionClass"]), spin == "spinless")
            nonzero_restriction = [r for r in item["chargeRoots"] if any(r["properD2ChargeClass"])]
            self.assertEqual(len(nonzero_restriction), 1)
            root = nonzero_restriction[0]
            self.assertEqual(root["obstructed"], spin == "spin_half")
            self.assertEqual(any(root["properD2ObstructionClass"]), spin == "spin_half")

    def test_odd_kernel_embeddings_and_explicit_background_gauges(self):
        audit = run_audit("audit_odd_kernel", "U1_ODD_KERNEL_AUDIT_OUT")
        self.assertEqual(len(audit), 6)
        for item in audit:
            source = json.loads((ROOT / "insulator_catalog/generated" / (item["source"] + ".json")).read_text())
            target = json.loads((ROOT / "insulator_catalog/generated" / (item["target"] + ".json")).read_text())
            h = item["sylow2OriginalIndices"]
            image = item["targetIndicesBySylow2Index"]
            quotient = item["quotientIndexByOriginalIndex"]
            ht = item["subgroupMultiplication"]
            gauge = list(map(Fraction, item["restrictedExtensionGauge"]))
            self.assertEqual(item["normalOddKernelOrder"], 3)
            self.assertTrue(item["normalOddKernelVerified"])
            self.assertTrue(item["complementIdentifiesWithQuotient"])
            self.assertEqual(sorted(image), list(range(4)))
            for i in range(4):
                self.assertEqual(source["s"][h[i]], target["s"][image[i]])
                self.assertEqual(source["r"][h[i]], target["r"][image[i]])
                self.assertEqual(source["rho"][h[i]], target["rho"][image[i]])
                for j in range(4):
                    product = ht[i][j]
                    self.assertEqual(h[product], source["multiplication"][h[i]][h[j]])
                    self.assertEqual(image[product], target["multiplication"][image[i]][image[j]])
                    difference = Fraction(source["omega"][h[i]][h[j]]) - Fraction(target["omega"][image[i]][image[j]])
                    self.assertEqual((difference - gauge[j] + gauge[product] - gauge[i]).denominator, 1)
            for i in range(source["order"]):
                for j in range(source["order"]):
                    self.assertEqual(quotient[source["multiplication"][i][j]], ht[quotient[i]][quotient[j]])


if __name__ == "__main__":
    unittest.main()
