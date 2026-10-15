"""Exact free-sheet lattice and paired full-affine classification regressions."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

from insulator.e8_spacegroup import extend_spacegroup_classification

ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("insulator_classify_runner", ROOT / "scripts/classify.py")
RUNNER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RUNNER)


@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class AffineBackendTests(unittest.TestCase):
    def test_free_kernel_keeps_multiples_and_combinations_modulo_charge_image(self):
        # Enumerate both the integer obstruction kernel and the subsequent
        # terminal quotient kernel. This tests exact image lattices, not a
        # rational nullspace or a list of individually surviving generators.
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "kernel.g"
            script.write_text('''U1_ROOT:="%s";;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
M:=[[1],[1]];;K:=U1MapKernel(M,[2],2);;Ki:=Inverse(K);;
if AbsInt(DeterminantMat(K))<>2 then Error("wrong kernel index");fi;
for a in [-4..4] do for b in [-4..4] do
 v:=[a,b];;member:=ForAll(v*Ki,IsInt);;
 if member<>((a+b) mod 2=0) then Error("lost combination or multiple");fi;
od;od;
target:=[4,6];;incoming:=[[2,0],[0,3]];;
quotient:=U1Smith(Concatenation(DiagonalMat(target),incoming),4,2);;
inds:=Filtered([1..quotient.rank],i->AbsInt(quotient.diag[i])>1);;
orders:=List(inds,i->AbsInt(quotient.diag[i]));;
terminal:=[[1,1],[1,0],[0,1]];;
projected:=List(terminal,row->(row*quotient.V){inds});;
K:=U1MapKernel(projected,orders,3);;Ki:=Inverse(K);;
for a in [-3..3] do for b in [-3..3] do for d in [-3..3] do
 v:=[a,b,d];;member:=ForAll(v*Ki,IsInt);;
 lift:=U1MapPreimage(incoming,target,2,v*terminal);;
 if member<>(lift<>fail) then Error("terminal quotient kernel mismatch");fi;
od;od;od;
Print("EXACT_FREE_KERNEL_PASS\\n");;QUIT_GAP(0);
''' % ROOT)
            proc = subprocess.run(["gap", "-q", "-b", "--quitonbreak", str(script)],
                                  text=True, capture_output=True, timeout=60)
            self.assertEqual(proc.returncode, 0, proc.stdout + proc.stderr)
            self.assertIn("EXACT_FREE_KERNEL_PASS", proc.stdout)

    def test_p1_pair_matches_independent_full_affine_runs_and_primitive_filling(self):
        paths = [ROOT / "insulator_catalog/generated" / f"spacegroup_001_{spin}.json"
                 for spin in ("spin_half", "spinless")]
        source = RUNNER.source_manifest()
        with tempfile.TemporaryDirectory() as tmp:
            independent, paired = Path(tmp) / "independent", Path(tmp) / "paired"
            independent.mkdir()
            paired.mkdir()
            for path in paths:
                meta = RUNNER.run_case(path, independent, "gap", 120, "2g", source)
                self.assertEqual(meta["status"], "complete", meta)
            pair = RUNNER.run_spin_pair(paths, paired, "gap", 120, "2g", source)
            for meta in pair:
                self.assertEqual(meta["status"], "complete", meta)
                self.assertEqual(meta["batchTimeoutSeconds"], 240)
                case = meta["id"]
                first = json.loads((independent / case / "result.json").read_text())
                second = json.loads((paired / case / "result.json").read_text())
                a, b = first["classification"], second["classification"]
                for key in ("torsion", "freeRank", "presentation", "generators", "witnesses",
                            "gaugeReductionWitnesses", "spaceGroupSheetLattice", "spaceGroupFilling"):
                    self.assertEqual(a[key], b[key], (case, key))
                self.assertEqual((b["freeRank"], b["torsion"]), (4, []))
                self.assertEqual(b["finalSheetFreeRank"], 3)
                filling = b["spaceGroupFilling"]
                self.assertEqual(filling["fillingStep"], 1)
                self.assertTrue(filling["primitiveBasisGeneratesFullTranslationKernel"])
                self.assertTrue(filling["allPresentationRelationsHaveZeroFilling"])
                extended = extend_spacegroup_classification(second)
                self.assertEqual((extended["freeRank"], extended["torsion"]), (7, []))
            self.assertTrue(b["pairedGeometryReuse"])


if __name__ == "__main__":
    unittest.main()
