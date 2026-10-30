"""Exact normalized source, half-phase transfer, and full-primitive regressions."""
from pathlib import Path
import json
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]

DOMAIN = r'''G:=Group((1,2,3,4),(2,4));;els:=Elements(G);;one:=Identity(G);;
C2:=Group((1,2));;mr:=GroupHomomorphismByImages(G,C2,[(1,2,3,4),(2,4)],[(1,2),Identity(C2)]);;
ms:=GroupHomomorphismByImages(G,C2,[(1,2,3,4),(2,4)],[Identity(C2),(1,2)]);;
r:=function(g)if Image(mr,g)=Identity(C2) then return 0;else return 1;fi;end;;s:=function(g)if Image(ms,g)=Identity(C2) then return 0;else return 1;fi;end;;
c:=rec(G:=G,s:=s,r:=r,omega:=function(g,h)return (s(g)*r(h))/2;end);;
checks:=0;;
for seed in [0,1,2] do
 q:=function(g,h,j)
  if one in [g,h,j] then return 0;fi;
  return (Position(els,g)+2*Position(els,h)+Position(els,h)*Position(els,j)+seed) mod 5-2;
 end;;
 fast:=U1ClosedChargeSource3Lazy(c,q);;
 w:=function(g,h)return 2*c.omega(g,h);end;;
 generic:=U1Add(U1Cup(c,2,w,"F2",3,q,"F2",0,true),U1Cup(c,3,q,"F2",3,q,"F2",1,true));;
 for xs in Tuples(els,5) do
  if U1Mod1(CallFuncList(generic,xs)/2)<>CallFuncList(fast,xs) then Error("Nonabelian lazy source disagreement");fi;
  checks:=checks+1;
 od;
od;
Print("LAZY_NONABELIAN_NEGATIVE_INTEGER_CHECKS ",checks,"\n");;
# Half-valued transfer must agree with the original full signed evaluator,
# retaining negative/even chain coefficients and group action differences.
halfChecks:=0;;ident:=fail;;es:=[];;
for args in [[2,0,0,0],[2,1,0,1/2],[4,1,1,1/2],[3,0,0,1/3]] do
 c:=CallFuncList(U1CyclicContext,args);;es:=Elements(c.G);;ident:=Identity(c.G);;
 f:=function(xs...)
  if ident in xs then return 0;fi;
  return ((Sum(List([1..Length(xs)],i->i*Position(es,xs[i]))) mod 5)-2)/2;
 end;;
 for k in [2..5] do
  if U1Native(c,k,"U1s",f)<>U1NativeHalfPhase(c,k,f) then Error("Signed half phase native mismatch");fi;
  if U1Native(c,k,"U1s",f)<>U1NativeHalfPhaseSmith(c,k,f) then Error("Half phase Smith native mismatch");fi;
  halfChecks:=halfChecks+2;
 od;
od;
Print("HALF_NATIVE_AND_SMITH_CHECKS ",halfChecks,"\n");;
QUIT_GAP(0);'''

PRIMITIVES = r'''primitiveChecks:=0;;nativeChecks:=0;;quarterPrimitives:=0;;c:=fail;;
for args in [[2,1,1,0],[2,1,0,1/2],[3,0,0,1/2],[4,1,1,1/2]] do
 c:=CallFuncList(U1CyclicContext,args);;els:=Filtered(Elements(c.G),g->g<>Identity(c.G));;
 for d in [2,3] do
  H:=U1Cohomology(c,d,"Zr");;vectors:=ShallowCopy(H.generators);;Append(vectors,U1Differential(c,d-1,"Zr"));;
  for v in vectors do
   for scale in [-3,1,2] do
    state:=U1CertifiedClosedChargeState(c,d,scale*v);;source:=U1Source(c,d,state);;
    a:=U1SolveData(c,d+2,"U1s",source);;b:=U1SolveCertifiedChargeData(c,d,state);;
    if (a=fail)<>(b=fail) then Error("Half phase solvability changed");fi;
    if a<>fail then
     if a.nativeObstruction<>b.nativeObstruction or a.nativePrimitive<>b.nativePrimitive then Error("Half phase native coordinates changed");fi;
     nativeChecks:=nativeChecks+1;
     if ForAny(b.nativePrimitive,x->DenominatorRat(x)=4) then quarterPrimitives:=quarterPrimitives+1;fi;
     for xs in Tuples(els,d+1) do
      if CallFuncList(a.primitive,xs)<>CallFuncList(b.primitive,xs) then Error("Integral homotopy correction changed");fi;
      primitiveChecks:=primitiveChecks+1;
     od;
    fi;
   od;
  od;
 od;
od;
# An exact non-half background does not receive the half-valued certificate.
c:=U1CyclicContext(3,0,0,1/3);;state:=U1CertifiedClosedChargeState(c,2,[1]);;
if IsBound(state.closedChargeSourceCertificate) then Error("Quarter/third background incorrectly certified");fi;
a:=U1SolveData(c,4,"U1s",U1Source(c,2,state));;b:=U1SolveCertifiedChargeData(c,2,state);;
if (a=fail)<>(b=fail) then Error("Uncertified fallback changed");fi;
# Replacing either the context action or source invalidates its exact identity.
c:=U1CyclicContext(2,1,1,0);;state:=U1CertifiedClosedChargeState(c,3,[1]);;
c.omega:=function(g,h)return 0;end;;
a:=U1SolveData(c,5,"U1s",U1Source(c,3,state));;b:=U1SolveCertifiedChargeData(c,3,state);;
if (a=fail)<>(b=fail) or (a<>fail and a.nativePrimitive<>b.nativePrimitive) then Error("Stale source certificate accepted");fi;
c:=U1CyclicContext(3,0,0,0);;state:=U1CertifiedClosedChargeState(c,2,[1]);;
c.omega:=function(g,h)return QuoInt(g!.exponents[1]+h!.exponents[1],3)/3;end;;
a:=U1SolveData(c,4,"U1s",U1Source(c,2,state));;b:=U1SolveCertifiedChargeData(c,2,state);;
if (a=fail)<>(b=fail) or (a<>fail and a.nativePrimitive<>b.nativePrimitive) then Error("Changed rational background did not fall back");fi;
c:=U1CyclicContext(2,1,1,0);;state:=U1CertifiedClosedChargeState(c,3,[2]);;
zero:=U1SolveCertifiedChargeData(c,3,state);;
if not IsIdenticalObj(zero.primitive,U1Zero) then Error("Certified zero source lost its literal zero primitive");fi;
zero:=U1SolveHalfPhaseData(c,5,U1Zero);;
if not IsIdenticalObj(zero.primitive,U1Zero) then Error("Generic zero source lost its literal zero primitive");fi;
Print("LITERAL_ZERO_PRIMITIVES_PASS\n");;
Print("NATIVE_SOLVES ",nativeChecks," EXACT_PRIMITIVE_VALUES ",primitiveChecks," QUARTER_PRIMITIVES ",quarterPrimitives,"\n");;
QUIT_GAP(0);'''

@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class HalfPhaseTransferTests(unittest.TestCase):
    def run_gap(self, program):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "check.g"
            path.write_text('U1_ROOT:=' + json.dumps(str(ROOT)) + ';;Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n' + program)
            return subprocess.run(["gap", "-q", "-b", "--quitonbreak", str(path)],
                                  text=True, capture_output=True, timeout=60)

    def test_nonabelian_source_and_signed_native_transfer(self):
        result = self.run_gap(DOMAIN)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("LAZY_NONABELIAN_NEGATIVE_INTEGER_CHECKS 98304", result.stdout)
        self.assertIn("HALF_NATIVE_AND_SMITH_CHECKS 32", result.stdout)

    def test_complete_primitive_and_certificate_guards(self):
        result = self.run_gap(PRIMITIVES)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NATIVE_SOLVES 42 EXACT_PRIMITIVE_VALUES 1005 QUARTER_PRIMITIVES 2", result.stdout)
        self.assertIn("LITERAL_ZERO_PRIMITIVES_PASS", result.stdout)

    def test_non_half_phase_value_rejected(self):
        result = self.run_gap('c:=U1CyclicContext(2,0,0,0);;g:=GeneratorsOfGroup(c.G)[1];;U1EvaluateHalfPhaseChain([[1,g,[g,g]]],function(xs...)return 1/4;end);;')
        self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("outside (1/2)Z/Z", result.stdout + result.stderr)

if __name__ == "__main__":
    unittest.main()
