"""Independent bar checks for transport, negative gauges and exact primitives."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]

@unittest.skipUnless(shutil.which('gap'), 'GAP and HAP are required')
class CochainBackendTests(unittest.TestCase):
    def test_independent_characters_and_negative_integer_gauges(self):
        program=r'''
OnBreak:=function() Where(12);QUIT_GAP(1);end;;
U1_ROOT:="@ROOT@";;Read(Concatenation(U1_ROOT,"/gap/load.g"));
data:=rec(multiplication:=[[0,1,2,3],[1,0,3,2],[2,3,0,1],[3,2,1,0]],identity_index:=0,
s:=[0,1,0,1],rho:=[0,0,1,1],omega:=[["0","0","0","0"],["0","1/2","0","1/2"],["0","0","0","0"],["0","1/2","0","1/2"]]);;
c:=U1FiniteContext(data,6);;
if U1Differential(c,0,"Zs")=U1Differential(c,0,"Zr") then Error("Independent sign caches collapsed");fi;
if U1Differential(c,0,"Zt")=U1Differential(c,0,"Zr") then Error("Extension sign collapsed into charge sign");fi;
one:=Identity(c.G);;els:=Filtered(Elements(c.G),g->g<>one);;
v:=g->[0,-3,2,5][c.elementIndex(g)];;
q:=U1Coboundary(c,"Zr",v);;
phase:=U1ChargeGauge(c,2,U1Zero,v);;
dphase:=U1Coboundary(c,"U1s",phase);;source:=U1ChargeSource(c,2,q);;
for xs in Tuples(els,4) do
 if U1Mod1(CallFuncList(dphase,xs)-CallFuncList(source,xs))<>0 then Error("Signed negative-charge gauge failed on bar tuple");fi;
od;
f:=function(g,h)
 if g=one or h=one then return 0;fi;
 return 2*c.elementIndex(g)-3*c.elementIndex(h)+c.elementIndex(g*h);
end;;
df:=U1Coboundary(c,"Zr",f);;primitive:=U1Solve(c,3,"Zr",df);;
if primitive=fail then Error("Exact integral bar source was rejected");fi;
dprimitive:=U1Coboundary(c,"Zr",primitive);;
for xs in Tuples(els,3) do
 if CallFuncList(dprimitive,xs)<>CallFuncList(df,xs) then Error("Native/bar homotopy correction failed");fi;
od;
Print("BAR_CHECKS_PASSED=108\n");QUIT_GAP(0);
'''.replace('@ROOT@',str(ROOT))
        with tempfile.TemporaryDirectory() as td:
            path=Path(td)/'checks.g';path.write_text(program)
            p=subprocess.run(['gap','-q','-b',str(path)],capture_output=True,text=True,timeout=60)
        self.assertEqual(p.returncode,0,p.stdout+p.stderr)
        self.assertIn('BAR_CHECKS_PASSED=108',p.stdout)

if __name__=='__main__': unittest.main()
