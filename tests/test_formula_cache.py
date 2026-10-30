"""Exact cache/transport checks, independently reviewed on nonabelian inputs."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class FormulaCacheTests(unittest.TestCase):
    def test_context_isolation_transport_and_literal_zero(self):
        script = r'''U1_ROOT:="%s";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point2_02_spinless.g"));;a:=U1_INPUT;;
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point2_02_spin_half.g"));;b:=U1_INPUT;;
c0:=U1FiniteContext(a,7);;
q:=function(g,h) return QuoInt(c0.elementIndex(g)+c0.elementIndex(h)-2,2);end;;
g:=First(Elements(c0.G),x->x<>Identity(c0.G));;
state:=rec(sheet:=U1Zero,charge:=q,phase:=U1Zero);;
f0:=U1Formula(c0,"source",2,state,rec(),fail,4);;r0:=f0(g,g,g,g);;
f0b:=U1Formula(c0,"source",2,ShallowCopy(state),rec(),fail,4);;
if f0b(g,g,g,g)<>r0 or c0.requestCacheHits<1 then Error("Request reuse failed");fi;
c1:=U1SiblingContext(c0,b);;
if IsBound(c1.requestCache) or IsBound(c1.formulaGeometryCache) then Error("Sibling inherited local request/geometry caches");fi;
f1:=U1Formula(c1,"source",2,state,rec(),fail,4);;r1:=f1(g,g,g,g);;
cf:=U1FiniteContext(b,7);;
qf:=function(g,h) return QuoInt(cf.elementIndex(g)+cf.elementIndex(h)-2,2);end;;
gf:=First(Elements(cf.G),x->x<>Identity(cf.G));;
ff:=U1Formula(cf,"source",2,rec(sheet:=U1Zero,charge:=qf),rec(),fail,4);;
if r1<>ff(gf,gf,gf,gf) or r0=r1 then Error("Different omega sibling leaked a cached result");fi;
# A literally zero input is canonicalized. A nonzero exact cochain is not.
if not IsIdenticalObj(U1Coboundary(c0,"Zs",U1Zero),U1Zero) then Error("Literal zero not canonicalized");fi;
primitive:=function(x) return c0.elementIndex(x)-1;end;;
exactNonzero:=U1Coboundary(c0,"Zs",primitive);;
if exactNonzero=U1Zero or exactNonzero(g,g)<>2 then Error("Exact nonzero cochain was discarded");fi;
# Geometry cache agrees with old inverse-prefix transport for every face.
r:=(1,2,3,4);;m:=(2,4);;G:=Group(r,m);;
elts:=Elements(G);;idx:=x->Position(elts,x);;
cc:=rec(G:=G,s:=x->(1-SignPerm(x))/2,r:=x->0,omega:=function(x,y) return (idx(x)-2*idx(y))/7;end);;
f:=function(xs...) return Sum([1..Length(xs)],i->i*idx(xs[i]))-3;end;;
checks:=0;;
for len in [1..6] do
 xs:=List([1..len],i->r^(i mod 4)*m^(i mod 2));;
 geom:=U1FormulaGeometry(cc,xs);;
 for p in [0..len] do
  if U1LocalFieldGeometry(cc,p,f,geom)<>U1LocalField(cc,p,f,geom.vs) then Error("Nonabelian face transport changed");fi;
  checks:=checks+1;
 od;
 if not IsIdenticalObj(geom,U1FormulaGeometry(cc,xs)) then Error("Geometry reuse failed");fi;
od;
old:=U1FormulaGeometry(cc,[r,m,r]);;
cc.omega:=function(x,y) return (idx(x)+idx(y))/5;end;;
new:=U1FormulaGeometry(cc,[r,m,r]);;
if IsIdenticalObj(old,new) or new.omega<>U1LocalField(cc,2,cc.omega,new.vs) then Error("Omega function replacement did not invalidate geometry");fi;
Print("INDEPENDENT_CANDIDATE_PASS: sibling omega ",r0," -> ",r1,"; ",checks," nonabelian face-degree checks; exact nonzero retained\n");;
# Force the bounded cache eviction path; values must remain identical.
c0.requestCacheSize:=8192;;
c0.omega:=U1Zero;;
fc:=U1Formula(c0,"source",2,state,rec(),fail,4);;
if fc(g,g,g,g)<>r1 or c0.requestCacheFlushes<>1 then Error("Request eviction changed the formula");fi;
c0.formulaGeometryCount:=8192;;geom:=U1FormulaGeometry(c0,[g,g,g]);;
if c0.formulaGeometryFlushes<>1 or geom.omega<>U1LocalField(c0,2,c0.omega,geom.vs) then Error("Geometry eviction changed the formula");fi;
for coeff in ["Zs","Zr","Zt","Z","F2","U1s"] do
 if U1Coboundary(c0,coeff,U1Zero)<>U1Zero then Error("Zero was not preserved for coefficient action");fi;
od;
QUIT_GAP(0);
'''
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "cache.g"
            path.write_text(script % ROOT)
            result = subprocess.run(["gap", "-q", "-b", "--quitonbreak", str(path)],
                                    text=True, capture_output=True, timeout=60)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            self.assertIn("INDEPENDENT_CANDIDATE_PASS", result.stdout)


if __name__ == "__main__":
    unittest.main()
