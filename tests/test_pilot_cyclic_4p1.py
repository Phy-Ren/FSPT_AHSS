"""Complete four-data root relations for the smallest unsigned cyclic groups."""
from fractions import Fraction
from itertools import combinations, product
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from insulator import api as ci
from insulator import e8
from scripts.audit_cyclic_4p1 import bar_root_relations, native_witness_audit

ROOT = Path(__file__).resolve().parents[1]


class NeutralCyclicRootTests(unittest.TestCase):
    def test_independent_cyclic_five_cycle_root_reduction(self):
        # Includes the shared three-primary extension and the even-order
        # charge-removal phase; this path never calls GAP.
        expected = {
            2: [[2, 0, 0, 0], [0, 2, -1, -1], [0, 0, 2, -1], [0, 0, 0, 2]],
            3: [[3, 0, 0, -1], [0, 3, 0, -2], [0, 0, 3, 0], [0, 0, 0, 3]],
            6: [[6, 0, 0, -2], [0, 6, -3, -1], [0, 0, 6, -3], [0, 0, 0, 6]],
        }
        for order, rows in expected.items():
            self.assertEqual(bar_root_relations(order)["presentation"], rows)

    def test_c3_global_neutral_cube_is_the_phase_root(self):
        # The complete normalized bar complex of C3 has 2^5 nondegenerate
        # five-simplices. This checks a global root relation, not random faces.
        order = 3
        for arguments in product((1, 2), repeat=5):
            vertices = [0]
            for value in arguments:
                vertices.append((vertices[-1] + value) % order)
            a = ci.Cochain(5, 1, {(i, j): (vertices[j] - vertices[i]) % order
                                     for i, j in combinations(range(6), 2)})
            x = a.d().sc(Fraction(1, order))
            xx = x.cup(x)
            background = ci.Symmetry(ci.Cochain(5, 2, {}), ci.Cochain(5, 1, {}),
                                     ci.Cochain(5, 1, {}))
            zero2, zero4 = ci.Cochain(5, 2, {}), ci.Cochain(5, 4, {})
            root = e8.State(x, zero2, zero4, a.cup(xx).sc(Fraction(1, 3 * order)))
            cube = root.power(order, background, 4).gauge(
                background, 4, a.sc(-1), ci.Cochain(5, 1, {}), ci.Cochain(5, 3, {}))
            phase_root = a.cup(xx).sc(Fraction(1, order))
            self.assertEqual(cube.e_p.maxabs(), 0)
            self.assertEqual((cube.nu_p3 - phase_root).mod(1).maxabs(), 0)
        # The phase root is nonzero: its value on a normalized cyclic
        # representative is 1/3, and its periodic-resolution coordinate is
        # certified by the independent GAP classification below.


@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class CyclicFourDataPilotTests(unittest.TestCase):
    def test_c1_c2_c3_complete_coupled_presentations(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "roots.json"
            driver = Path(directory) / "roots.g"
            driver.write_text(
                'OnBreak:=function() Where(10);QUIT_GAP(1);end;;\n'
                'U1_ROOT:="' + str(ROOT) + '";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n'
                'Read(Concatenation(U1_ROOT,"/formulas/examples/cyclic_4p1.g"));;\n'
                'r:=List([1,2,3],U1CyclicFourData);;\n'
                'out:=OutputTextFile("' + str(output) + '",false);;\n'
                'SetPrintFormattingStatus(out,false);;WriteLine(out,U1JSON(r));;CloseStream(out);;QUIT_GAP(0);\n')
            process = subprocess.run(["gap", "-q", "-b", str(driver)],
                                     capture_output=True, text=True, timeout=120)
            self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
            trivial, c2, c3 = json.loads(output.read_text())
        self.assertEqual(trivial["torsion"], [])
        self.assertEqual(c2["torsion"], [2, 8])
        self.assertEqual(c3["torsion"], [3, 3, 9])
        self.assertEqual(c2["presentation"], [[2, 0, 0, 0], [0, 2, -1, -1],
                                                [0, 0, 2, -1], [0, 0, 0, 2]])
        self.assertEqual(c3["presentation"], [[3, 0, 0, -1], [0, 3, 0, -2],
                                                [0, 0, 3, 0], [0, 0, 0, 3]])
        for order, item in enumerate((trivial, c2, c3), 1):
            self.assertEqual(item["actualGroupOrder"], order ** 4)
            self.assertEqual(item["incomingCohomology"], {"sheet": [], "charge": []})
            self.assertEqual(item["terminalObstructionTargetOrders"], [])
            self.assertFalse(item["physicalClassificationCertified"])
            self.assertGreater(item["nativeCompletionChecks"], 0)
        checks = native_witness_audit([{"classification": item} for item in (trivial, c2, c3)])
        self.assertEqual(len(checks), 8)
        self.assertTrue(all(check["verified"] for check in checks))


if __name__ == "__main__":
    unittest.main()
