"""Native binary primary classes retain integer charge and signed phase data."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class NativeChargePrimaryTests(unittest.TestCase):
    def run_gap(self, program):
        prefix = ('OnBreak:=function() Where(8);QUIT_GAP(1);end;;\n'
                  'U1_ROOT:="%s";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n' % ROOT)
        with tempfile.TemporaryDirectory() as directory:
            script = Path(directory) / "check.g"
            script.write_text(prefix + program)
            return subprocess.run(["gap", "-q", "-b", str(script)], capture_output=True,
                                  text=True, timeout=120)

    def test_nonzero_affine_obstructions_match_both_bar_projections(self):
        result = self.run_gap(r'''
U1_USE_KOSZUL:=true;;checks:=0;;nonzero:=0;;
for name in ["spacegroup_016_spinless","spacegroup_016_spin_half",
             "spacegroup_025_spinless","spacegroup_025_spin_half"] do
 Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/",name,".g"));;
 c:=U1CatalogContext(U1_INPUT,6);;c.chargePrimaryMode:="compare";;c.phaseClassMode:="compare";;
 HQ:=U1Cohomology(c,3,"Zr");;H:=U1Cohomology(c,5,"U1s");;
 for v in HQ.generators do
  co:=U1ChargeObstructionCoordinates(c,3,H,v);;
  if ForAny(co,x->x<>0) then nonzero:=nonzero+1;fi;
  checks:=checks+1;
 od;
 if c.chargePrimaryStats.nativeCalls<>Length(HQ.generators)
  or c.chargePrimaryStats.comparisons<>Length(HQ.generators)
  or c.chargePrimaryStats.omegaClosureChecks<>1 then Error("Native comparison was not exercised");fi;
od;
if checks<>32 or nonzero<>16 then Error("Nonzero affine obstruction controls changed");fi;
Print("AFFINE_PRIMARY_CHECKS ",checks," NONZERO ",nonzero,"\n");;QUIT_GAP(0);
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("AFFINE_PRIMARY_CHECKS 32 NONZERO 16", result.stdout)

    def test_signed_coefficients_general_rational_fallback_and_modes(self):
        result = self.run_gap(r'''
checks:=0;;
for signs in [[0,0],[0,1],[1,0],[1,1]] do
 c:=U1CyclicContext(4,signs[1],signs[2],1/2);;
 c.chargePrimaryMode:="compare";;c.phaseClassMode:="compare";;
 for d in [2,3] do
  H:=U1Cohomology(c,d+2,"U1s");;HQ:=U1Cohomology(c,d,"Zr");;
  for v in HQ.generators do
   co:=U1ChargeObstructionCoordinates(c,d,H,v);;checks:=checks+1;
  od;
 od;
od;
# A general rational extension is not reduced modulo two.
c:=U1CyclicContext(3,0,0,1/3);;c.chargePrimaryMode:="native";;
H:=U1Cohomology(c,4,"U1s");;HQ:=U1Cohomology(c,2,"Zr");;v:=HQ.generators[1];;
co:=U1ChargeObstructionCoordinates(c,2,H,v);;
if co<>H.coordinates(U1Native(c,4,"U1s",U1ChargeSource(c,2,U1Bar(c,2,"Zr",v))))
 or c.chargePrimaryStats.nativeCalls<>0 or c.chargePrimaryStats.barFallbacks<>1 then
 Error("General rational background did not use the bar fallback");fi;
# Callback replacement invalidates the stored certificate, even on the same group.
c:=U1CyclicContext(4,0,0,1/2);;old:=c.omega;;c.omega:=function(g,h) return old(g,h)/3;end;;
H:=U1Cohomology(c,4,"U1s");;HQ:=U1Cohomology(c,2,"Zr");;
co:=U1ChargeObstructionCoordinates(c,2,H,HQ.generators[1]);;
if c.chargePrimaryStats.nativeCalls<>0 or c.chargePrimaryStats.barFallbacks<>1 then Error("Stale callback certificate reused");fi;
# An uncertified arbitrary context uses the checked bar route.
base:=U1CyclicContext(4,0,0,0);;
c:=U1NewContext(base.G,base.R,base.s,base.rho,base.omega,0);;
H:=U1Cohomology(c,4,"U1s");;HQ:=U1Cohomology(c,2,"Zr");;
co:=U1ChargeObstructionCoordinates(c,2,H,HQ.generators[1]);;
if c.chargePrimaryStats.nativeCalls<>0 then Error("Uncertified context used native primary");fi;
# Existing phase-mode audits retain their meaning; explicit charge mode wins.
c:=U1CyclicContext(4,0,0,0);;c.phaseClassMode:="cycles";;
H:=U1Cohomology(c,4,"U1s");;HQ:=U1Cohomology(c,2,"Zr");;v:=HQ.generators[1];;
co:=U1ChargeObstructionCoordinates(c,2,H,v);;
if c.chargePrimaryStats.phaseModeOverrides<>1 then Error("Implicit mode precedence changed");fi;
c.chargePrimaryMode:="native";;co:=U1ChargeObstructionCoordinates(c,2,H,v);;
if c.chargePrimaryStats.nativeCalls<>1 then Error("Explicit native mode did not win");fi;
c.chargePrimaryMode:="bar";;co:=U1ChargeObstructionCoordinates(c,2,H,v);;
if c.chargePrimaryStats.nativeCalls<>1 then Error("Explicit bar mode did not fall back");fi;
Print("SIGNED_PRIMARY_AND_FALLBACK_PASS ",checks,"\n");;QUIT_GAP(0);
''')
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("SIGNED_PRIMARY_AND_FALLBACK_PASS", result.stdout)

    def test_reject_nonintegral_open_charge_and_wrong_target(self):
        programs = [
            'c:=U1CyclicContext(2,0,0,0);;H:=U1Cohomology(c,4,"U1s");;'
            'U1ChargeObstructionCoordinates(c,2,H,[1/2]);;',
            'c:=U1CyclicContext(2,1,1,0);;H:=U1Cohomology(c,4,"U1s");;'
            'U1ChargeObstructionCoordinates(c,2,H,[1]);;',
            'c:=U1CyclicContext(2,0,0,0);;H:=U1Cohomology(c,3,"U1s");;'
            'U1ChargeObstructionCoordinates(c,2,H,[1]);;',
        ]
        for program in programs:
            with self.subTest(program=program):
                result = self.run_gap(program)
                self.assertNotEqual(result.returncode, 0, result.stdout + result.stderr)


if __name__ == "__main__":
    unittest.main()
