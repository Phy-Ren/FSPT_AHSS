"""The D2 spin-half odd-charge obstruction is tested before any table comparison."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which('gap'),'GAP and HAP are required')
class D2AuditTests(unittest.TestCase):
    def test_nonzero_steenrod_bockstein_obstructs_charge(self):
        with tempfile.TemporaryDirectory() as td:
            result=Path(td)/'audit.json';script=Path(td)/'audit.g'
            script.write_text('OnBreak:=function() Where(10);QUIT_GAP(1);end;;\n'
                f'U1_ROOT:="{ROOT}";;Read(Concatenation(U1_ROOT,"/gap/load.g"));\n'
                f'U1_D2_AUDIT_OUT:="{result}";;Read(Concatenation(U1_ROOT,"/gap/audit_d2.g"));\nQUIT_GAP(0);\n')
            p=subprocess.run(['gap','-q','-b',str(script)],capture_output=True,text=True,timeout=90)
            self.assertEqual(p.returncode,0,p.stdout+p.stderr)
            audit=json.loads(result.read_text())
        self.assertEqual(audit['integralChargeOrders'],[2])
        self.assertEqual(audit['integralChargeClass'],[1])
        self.assertTrue(any(audit['phaseObstructionClass']))
        self.assertFalse(audit['phaseObstructionHasPrimitive'])
        self.assertEqual(audit['mod2BocksteinCoordinates'],audit['mod2ChargeSquareCoordinates'])
        self.assertEqual(audit['mod2BocksteinCoordinates'],audit['mod2PolynomialCoordinates'])
        self.assertTrue(any(audit['mod2BocksteinCoordinates']))
        self.assertEqual(audit['incomingChargePhaseCoordinates'],[[0,0],[0,0]])
        self.assertEqual(audit['classification']['torsion'],[2,2])
        self.assertEqual(audit['explicitIntegralBarClosureChecks'],81)

if __name__=='__main__': unittest.main()
