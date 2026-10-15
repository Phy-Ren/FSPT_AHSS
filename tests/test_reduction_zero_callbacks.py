"""Pointwise signed lower-field identities and unchanged complete gauge phases."""
import json
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = r'''
OnBreak:=function() Where(20);QUIT_GAP(1);end;;
U1_ROOT:="@ROOT@";;
Read(Concatenation(U1_ROOT,"/gap/load.g"));;
rows:=[];;
for spec in [[0,0],[0,1],[1,0],[1,1]] do
 data:=rec(multiplication:=[[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]],identity_index:=0,
 s:=List([0,1,0,1],x->spec[1]*x),rho:=List([0,0,1,1],x->spec[2]*x),
 omega:=[["0","0","0","0"],["0","1/2","0","1/2"],["0","0","0","0"],["0","1/2","0","1/2"]]);;
 c:=U1FiniteContext(data,6);;one:=Identity(c.G);;els:=Filtered(Elements(c.G),g->g<>one);;
 for d in [2,3] do
  if d=2 then
   u:=U1Zero;;v:=function(g) if g=one then return 0;fi;return 2*c.elementIndex(g)-7;end;;
  else
   if spec[1]=1 then u:=function() return -3;end;else u:=U1Zero;fi;
   v:=function(g,h) if g=one or h=one then return 0;fi;return 2*c.elementIndex(g)-3*c.elementIndex(h)+1;end;;
  fi;
  a:=U1Gauge(c,d,U1Vacuum(),u,v);;U1CheckCompletedState(c,d,a);;
  raw:=a;;sheetCount:=0;;
  if raw.sheet<>U1Zero then
   gu:=U1Solve(c,d-2,"Zs",U1Scale(-1,raw.sheet));;
   if gu=fail then Error("exact sheet failed");fi;
   raw:=U1Gauge(c,d,raw,gu,U1Zero);;
   for xs in Tuples(els,d-2) do
    if CallFuncList(raw.sheet,xs)<>0 then Error("discarded sheet not pointwise zero");fi;
    sheetCount:=sheetCount+1;
   od;
   raw.sheet:=U1Zero;
  fi;
  dq:=U1Coboundary(c,"Zr",raw.charge);;
  for xs in Tuples(els,d+1) do
   if CallFuncList(dq,xs)<>0 then Error("charge is not closed after sheet gauge");fi;
  od;
  gv:=U1Solve(c,d,"Zr",U1Scale(-1,raw.charge));;
  if gv=fail then Error("exact charge failed");fi;
  raw:=U1Gauge(c,d,raw,U1Zero,gv);;
  for xs in Tuples(els,d) do
   if CallFuncList(raw.charge,xs)<>0 then Error("discarded charge not pointwise zero");fi;
  od;
  c.vacuumReductionMode:="reference";;reference:=U1ReduceVacuum(c,d,a);;oldWitness:=ShallowCopy(c.reductionWitnesses[Length(c.reductionWitnesses)]);;
  c.vacuumReductionMode:="canonical";;candidate:=U1ReduceVacuum(c,d,a);;newWitness:=c.reductionWitnesses[Length(c.reductionWitnesses)];;
  if oldWitness<>newWitness then Error("native gauge/phase witness differs");fi;
  for xs in Tuples(els,d+1) do
   if U1Mod1(CallFuncList(reference,xs)-CallFuncList(candidate,xs))<>0 then Error("phase representative changed");fi;
  od;
  Add(rows,rec(dimension:=d,sSign:=spec[1],rhoSign:=spec[2],sheetValuesChecked:=sheetCount,
   chargeValuesChecked:=3^d,chargeClosureValuesChecked:=3^(d+1),phaseEqualityValuesChecked:=3^(d+1),
   nativeWitnessesIdentical:=true));;
 od;
od;
f:=OutputTextFile("@OUTPUT@",false);;SetPrintFormattingStatus(f,false);;
WriteLine(f,U1JSON(rec(passed:=true,rows:=rows)));;CloseStream(f);;QUIT_GAP(0);
'''

@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class VacuumReductionTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        with tempfile.TemporaryDirectory(prefix="u1-reduction-zero-") as temporary:
            folder = Path(temporary)
            output = folder / "checks.json"
            script = folder / "checks.g"
            script.write_text(PROGRAM.replace("@ROOT@", str(ROOT)).replace("@OUTPUT@", str(output)))
            run = subprocess.run(["gap", "-q", "-b", "--quitonbreak", str(script)],
                                 text=True, capture_output=True, timeout=120)
            if run.returncode:
                raise AssertionError(run.stdout + run.stderr)
            result = json.loads(output.read_text())
            if result.get("passed") is not True:
                raise AssertionError("Pointwise reduction audit did not pass")
            cls.rows = result["rows"]

    def test_2p1_signed_exact_charge_and_reference_phase(self):
        rows = [row for row in self.rows if row["dimension"] == 2]
        self.assertEqual(len(rows), 4)
        self.assertEqual(sum(row["chargeValuesChecked"] for row in rows), 36)
        self.assertEqual(sum(row["phaseEqualityValuesChecked"] for row in rows), 108)
        self.assertTrue(all(row["nativeWitnessesIdentical"] for row in rows))

    def test_3p1_signed_exact_sheet_charge_and_reference_phase(self):
        rows = [row for row in self.rows if row["dimension"] == 3]
        self.assertEqual(len(rows), 4)
        self.assertEqual(sum(row["sheetValuesChecked"] for row in rows), 6)
        self.assertEqual(sum(row["chargeValuesChecked"] for row in rows), 108)
        self.assertEqual(sum(row["chargeClosureValuesChecked"] for row in rows), 324)
        self.assertEqual(sum(row["phaseEqualityValuesChecked"] for row in rows), 324)
        self.assertTrue(all(row["nativeWitnessesIdentical"] for row in rows))

    def test_unknown_mode_is_rejected(self):
        program = ('OnBreak:=function() QUIT_GAP(1);end;;\n'
                   'U1_ROOT:="' + str(ROOT) + '";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n'
                   'c:=U1CyclicContext(2,0,0,0);;c.vacuumReductionMode:="unknown";;\n'
                   'U1ReduceVacuum(c,2,U1Vacuum());;QUIT_GAP(0);\n')
        with tempfile.TemporaryDirectory(prefix="u1-reduction-mode-") as temporary:
            script = Path(temporary) / "invalid.g"
            script.write_text(program)
            run = subprocess.run(["gap", "-q", "-b", "--quitonbreak", str(script)],
                                 text=True, capture_output=True, timeout=30)
        self.assertNotEqual(run.returncode, 0)
        self.assertIn("Unknown vacuum reduction mode", run.stdout + run.stderr)

if __name__ == "__main__":
    unittest.main()
