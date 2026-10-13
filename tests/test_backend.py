"""End-to-end exact group regressions, independent of the native cell basis."""
from __future__ import annotations
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which('gap'), 'GAP and HAP are required')
class BackendTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.tmp = tempfile.TemporaryDirectory()
        work = Path(cls.tmp.name)
        out = work / 'results.jsonl'
        script = work / 'check.g'
        script.write_text('''OnBreak:=function() Where(12);QUIT_GAP(1);end;;
U1_ROOT:="%s";; Read(Concatenation(U1_ROOT,"/gap/load.g"));
out:=OutputTextFile("%s",false);;SetPrintFormattingStatus(out,false);;
for spec in [[1,0,0,0,2],[2,0,0,0,2],[3,0,0,0,2],[4,0,0,0,2],
             [2,1,1,0,3],[2,1,0,1/2,3],[2,1,0,0,3]] do
 c:=U1CyclicContext(spec[1],spec[2],spec[3],spec[4]);;
 r:=U1Classify(c,spec[5]);;WriteLine(out,U1JSON(r));
od;
c:=U1CyclicContext(2,0,0,1/2);;r:=U1Classify(c,2,rec(uniformIQH:=true));;WriteLine(out,U1JSON(r));
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/wallpaper_04_spinless.g"));
c:=U1WallpaperContext(U1_INPUT,6);;r:=U1Classify(c,2);;WriteLine(out,U1JSON(r));
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/wallpaper_01_spinless.g"));
c:=U1WallpaperContext(U1_INPUT,6);;r:=U1Classify(c,2);;WriteLine(out,U1JSON(r));
CloseStream(out);QUIT_GAP(0);
''' % (ROOT, out))
        proc = subprocess.run(['gap','-q','-b',str(script)], capture_output=True, text=True, timeout=180)
        if proc.returncode:
            raise AssertionError(proc.stdout + proc.stderr)
        cls.results = [json.loads(s) for s in out.read_text().splitlines()]
        if len(cls.results) != 10:
            raise AssertionError(proc.stdout + proc.stderr)

    @classmethod
    def tearDownClass(cls):
        cls.tmp.cleanup()

    def test_trivial_relative_insulator(self):
        self.assertEqual((self.results[0]['freeRank'],self.results[0]['torsion']),(0,[]))

    def test_charge_root_keeps_quarter_phase(self):
        r=self.results[1]
        self.assertEqual(r['torsion'],[4])
        self.assertEqual(r['finalChargeOrders'],[2])
        self.assertEqual(r['finalPhaseOrders'],[2])
        self.assertEqual(r['generators'][1]['nativePhase'],['1/4'])
        self.assertIn([-1,2],r['presentation'])

    def test_nonbinary_roots(self):
        self.assertEqual(self.results[2]['torsion'],[3,3])
        self.assertEqual(self.results[3]['torsion'],[2,8])

    def test_completed_ci_roots(self):
        self.assertEqual(self.results[4]['torsion'],[8])
        self.assertEqual(self.results[5]['torsion'],[2,2])
        self.assertEqual(self.results[4]['finalSheetOrders'],[2])
        self.assertTrue(any(w['kind']=='CI-root' and w['chargeCoordinates']==[1]
                            for w in self.results[4]['witnesses']))

    def test_incoming_quotient_and_integral_obstruction(self):
        r=self.results[6]
        self.assertEqual(r['torsion'],[])
        self.assertEqual(r['phaseOrders'],[2])
        self.assertEqual(r['finalPhaseOrders'],[])
        self.assertEqual(r['obstructedSheets'][0]['stage'],'d3')
        self.assertTrue(any(w['kind']=='incoming-charge-gauge' and w['phaseCoordinates']==[1]
                            for w in r['witnesses']))

    def test_uniform_iqh_is_lifted_not_inferred(self):
        r=self.results[7]
        self.assertEqual((r['freeRank'],r['torsion']),(1,[4]))
        self.assertTrue(r['uniformIQHIncluded'])
        witness=next(w for w in r['witnesses'] if w['kind']=='uniform-IQH-lift')
        self.assertEqual(witness['sheetMultiplicity'],1)
        self.assertEqual(witness['nativePhase'],['1/16'])

    def test_wallpaper_retains_infinite_affine_group(self):
        r=self.results[8]
        self.assertEqual((r['freeRank'],r['torsion']),(1,[]))
        self.assertEqual(r['chargeOrders'],[0])
        self.assertEqual(r['finalChargeFreeRank'],1)
        self.assertEqual(r['wallpaperFilling']['fillingStep'],2)
        self.assertTrue(r['wallpaperFilling']['primitiveBasisGeneratesFullTranslationKernel'])
        self.assertEqual(self.results[9]['wallpaperFilling']['fillingStep'],1)

if __name__ == '__main__':
    unittest.main()
