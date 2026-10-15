"""Exact closed-phase Smith periods, domain guards and source-map comparisons."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class PhaseClassCoordinatesTests(unittest.TestCase):
    def run_gap(self, program):
        prefix = ('OnBreak:=function() Where(8);QUIT_GAP(1);end;;\n'
                  'U1_ROOT:="%s";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n' % ROOT)
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "check.g"
            script.write_text(prefix + program)
            return subprocess.run(["gap", "-q", "-b", str(script)],
                                  capture_output=True, text=True, timeout=90)

    def test_arbitrary_torsion_signed_periods_and_charge_sources(self):
        result = self.run_gap(r'''
checks:=0;;ordersSeen:=[];;
for n in [2,3,4,6,8,9] do
 for signs in [[0,0],[0,1],[1,0],[1,1]] do
  if n mod 2=1 and signs<>[0,0] then continue;fi;
  c:=U1CyclicContext(n,signs[1],signs[2],1/2);;
  c.phaseClassMode:="compare";;
  for k in [1..5] do
   H:=U1Cohomology(c,k,"U1s");;Append(ordersSeen,H.orders);;
   for i in [1..Length(H.generators)] do
    f:=U1Bar(c,k,"U1s",H.generators[i]);;
    v:=List([1..Dimension(c.R)(k-1)],j->(2*j-5)/7);;
    exact:=U1Coboundary(c,"U1s",U1Bar(c,k-1,"U1s",v));;
    for phase in [f,U1Add(U1Scale(-3,f),exact)] do
     certificate:=U1NativePhaseClosureCertificate(c,k,H,phase);;
     if certificate=fail then Error("Closed phase rejected");fi;
     co:=U1ClosedBarPhaseCoordinates(c,k,H,phase,certificate);;
     if co<>H.coordinates(U1Native(c,k,"U1s",phase)) then Error("Wrong Smith period");fi;
     checks:=checks+1;
    od;
   od;
  od;
  for d in [2,3] do
   H:=U1Cohomology(c,d+2,"U1s");;HQ:=U1Cohomology(c,d,"Zr");;
   for v in HQ.generators do
    co:=U1ChargeObstructionCoordinates(c,d,H,v);;
    q:=U1Bar(c,d,"Zr",v);;
    if co<>H.coordinates(U1Native(c,d+2,"U1s",U1ChargeSource(c,d,q))) then
     Error("Charge obstruction class changed");fi;
    checks:=checks+1;
   od;
  od;
 od;
od;
if Set(ordersSeen)<>[2,3,4,6,8,9] then Error("Missing nonbinary torsion controls");fi;
# An arbitrary context has no algebraic background certificate; use the checked
# native fallback. A changed omega cannot reuse an earlier algebraic certificate.
c:=U1CyclicContext(4,0,0,1/2);;old:=c.omega;;
c.omega:=function(g,h) return 3*old(g,h);end;;
H:=U1Cohomology(c,4,"U1s");;HQ:=U1Cohomology(c,2,"Zr");;
co:=U1ChargeObstructionCoordinates(c,2,H,HQ.generators[1]);;
if co<>[] then Error("Unexpected cyclic even phase class");fi;
# Detect a native noncocycle before any period-only evaluation is allowed.
c:=U1CyclicContext(2,0,0,0);;H:=U1Cohomology(c,1,"U1s");;
f:=U1Bar(c,1,"U1s",[1/3]);;
if U1NativePhaseClosureCertificate(c,1,H,f)<>fail then Error("Open phase accepted");fi;
Print("PHASE_PERIOD_CHECKS ",checks,"\n");;QUIT_GAP(0);
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("PHASE_PERIOD_CHECKS", result.stdout)

    def test_full_nonabelian_and_affine_comparison_modes(self):
        result = self.run_gap(r'''
U1_USE_KOSZUL:=true;;
for name in ["point3_06_spin_half","point3_06_spinless","wallpaper_04_spinless","spacegroup_001_spinless"] do
 Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/",name,".g"));;
 c:=U1CatalogContext(U1_INPUT,6);;c.phaseClassMode:="compare";;
 r:=U1Classify(c,U1_INPUT.dimension);;
 if not r.nativeChainIdentitiesVerified then Error("Missing completion checks");fi;
 if IsBound(c.worker) then CloseStream(c.worker);fi;
od;
# Siblings have the same signed geometry but distinct extension cocycles.
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point3_06_spinless.g"));;
c:=U1CatalogContext(U1_INPUT,6);;H:=U1Cohomology(c,5,"U1s");;
HQ:=U1Cohomology(c,3,"Zr");;c.phaseClassMode:="compare";;
a:=List(HQ.generators,v->U1ChargeObstructionCoordinates(c,3,H,v));;
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point3_06_spin_half.g"));;
sibling:=U1SiblingContext(c,U1_INPUT);;sibling.phaseClassMode:="compare";;
if IsBound(sibling.phaseClassCycles) then Error("Sibling inherited phase cycle cache");fi;
b:=List(HQ.generators,v->U1ChargeObstructionCoordinates(sibling,3,H,v));;
if a=b then Error("Background-dependent obstruction was lost");fi;
Print("FULL_PHASE_CLASS_COMPARISON_PASS\n");;QUIT_GAP(0);
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("FULL_PHASE_CLASS_COMPARISON_PASS", result.stdout)

    def test_certificate_and_integer_charge_domain_guards(self):
        programs = [
            'c:=U1CyclicContext(2,0,0,0);;H:=U1Cohomology(c,1,"U1s");;'
            'U1ClosedBarPhaseCoordinates(c,1,H,U1Zero,fail);;',
            'c:=U1CyclicContext(2,1,1,0);;H:=U1Cohomology(c,4,"U1s");;'
            'U1ChargeObstructionCoordinates(c,2,H,[1]);;',
            'c:=U1CyclicContext(2,0,0,0);;H:=U1Cohomology(c,1,"U1s");;'
            'cert:=U1NativePhaseClosureCertificate(c,1,H,U1Zero);;'
            'U1ClosedBarPhaseCoordinates(c,1,H,x->1/3,cert);;',
        ]
        for program in programs:
            with self.subTest(program=program):
                result = self.run_gap(program)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
