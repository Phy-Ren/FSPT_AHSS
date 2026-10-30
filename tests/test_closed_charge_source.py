"""Pointwise certified charge source and stale-certificate regressions."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = r'''checks:=0;;evenChecks:=0;;
data:=rec(schema_version:=2,multiplication:=[[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]],identity_index:=0,
 s:=[0,1,0,1],r:=[0,0,1,1],omega:=[["0","0","0","0"],["0","1/2","0","1/2"],["0","0","0","0"],["0","1/2","0","1/2"]]);;
contexts:=[U1FiniteContext(data,6),U1CyclicContext(3,0,0,1/2),U1CyclicContext(4,0,1,1/2),U1CyclicContext(2,1,0,1/2)];;
for c in contexts do
 els:=Filtered(Elements(c.G),g->g<>Identity(c.G));;
 for d in [2,3] do
  H:=U1Cohomology(c,d,"Zr");;
  vectors:=ShallowCopy(H.generators);;
  # Include exact signed cocycles even when the integral cohomology vanishes.
  Append(vectors,U1Differential(c,d-1,"Zr"));;
  for vector in vectors do
   for scale in [-3,-2,1,2] do
    v:=scale*vector;;state:=U1CertifiedClosedChargeState(c,d,v);;
    fast:=state.closedChargeSourceCertificate.source;;
    reference:=U1ChargeSource(c,d,state.charge);;
    if ForAll(v,x->x mod 2=0) then
     if fast<>U1Zero then Error("Even integer vector did not give literal zero");fi;
     evenChecks:=evenChecks+1;
    fi;
    for xs in Tuples(els,d+2) do
     if U1Mod1(CallFuncList(reference,xs)-CallFuncList(fast,xs))<>0 then Error("Closed source pointwise disagreement");fi;
     checks:=checks+1;
    od;
   od;
  od;
 od;
od;
Print("CLOSED_CHARGE_SOURCE_POINTWISE_CHECKS ",checks," EVEN_NATIVE_ZERO ",evenChecks,"\n");;
QUIT_GAP(0);'''

@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class ClosedChargeSourceTests(unittest.TestCase):
    def run_gap(self, program):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "check.g"
            script.write_text('U1_ROOT:="%s";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n' % ROOT + program)
            return subprocess.run(["gap", "-q", "-b", "--quitonbreak", str(script)],
                                  text=True, capture_output=True, timeout=60)

    def test_pointwise_signed_source_and_literal_even_zero(self):
        result = self.run_gap(PROGRAM)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CLOSED_CHARGE_SOURCE_POINTWISE_CHECKS 9664 EVEN_NATIVE_ZERO 60", result.stdout)

    def test_context_and_charge_changes_invalidate_source_certificates(self):
        result = self.run_gap(r'''
c:=U1CyclicContext(2,0,0,0);;g:=GeneratorsOfGroup(c.G)[1];;
state:=U1CertifiedClosedChargeState(c,2,[1]);;before:=U1Source(c,2,state);;
if before(g,g,g,g)<>1/2 then Error("Wrong starting charge source");fi;
c.omega:=function(x,y) return QuoInt(x!.exponents[1]+y!.exponents[1],2)/2;end;;
after:=U1Source(c,2,state);;
if IsIdenticalObj(before,after) or U1Mod1(after(g,g,g,g))<>0 then Error("Stale background source cache");fi;
c:=U1CyclicContext(2,0,0,0);;g:=GeneratorsOfGroup(c.G)[1];;
state:=U1CertifiedClosedChargeState(c,2,[1]);;before:=U1Source(c,2,state);;
state.charge:=U1Scale(2,state.charge);;after:=U1Source(c,2,state);;
if IsIdenticalObj(before,after) or U1Mod1(after(g,g,g,g))<>0 then Error("Stale charge source certificate");fi;
c:=U1CyclicContext(3,0,0,1/3);;state:=U1CertifiedClosedChargeState(c,2,[1]);;
if IsBound(state.closedChargeSourceCertificate) then Error("Non-half-integral background specialized");fi;
c:=U1CyclicContext(2,0,0,1/2);;c.closedChargeSourceMode:="reference";;
state:=U1CertifiedClosedChargeState(c,2,[1]);;
if IsBound(state.closedChargeSourceCertificate) then Error("Reference mode specialized");fi;
c.closedChargeSourceMode:="compare";;state:=U1CertifiedClosedChargeState(c,2,[1]);;
g:=GeneratorsOfGroup(c.G)[1];;source:=U1Source(c,2,state);;value:=source(g,g,g,g);;
Print("CLOSED_SOURCE_GUARDS_PASS\n");;QUIT_GAP(0);
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("CLOSED_SOURCE_GUARDS_PASS", result.stdout)

    def test_nonclosed_integer_vector_is_rejected(self):
        result = self.run_gap('c:=U1CyclicContext(2,1,1,0);;U1CertifiedClosedChargeState(c,2,[1]);;')
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)

if __name__ == "__main__":
    unittest.main()
