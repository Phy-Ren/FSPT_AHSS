"""Independent signed/nonabelian cup values, including degree-zero factors."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
PROGRAM = r'''BindGlobal("NewU1Cup",function(c,p,a,ca,q,b,cb,i,binary)
  local degree,cuts;
  if a=U1Zero or b=U1Zero or i<0 or i>Minimum(p,q) then return U1Zero;fi;
  degree:=p+q-i;cuts:=U1CupCuts.(Concatenation("c",String(p),"_",String(q),"_",String(i)));
  return U1Memo(function(xs...)
    local vs,g,term,left,right,value,sg,j,edges,edgeStart,edgeEnd;
    if Length(xs)<>degree then Error("cup arity mismatch");fi;
    # In a nonabelian group, (x1...xi)^-1*(x1...xj)=x(i+1)...xj.
    # Preserve the original order; all coefficient actions still use prefixes.
    edges:=[];
    for edgeStart in [1..degree] do
      edges[edgeStart]:=[];g:=xs[edgeStart];edges[edgeStart][edgeStart+1]:=g;
      for edgeEnd in [edgeStart+2..degree+1] do g:=g*xs[edgeEnd-1];edges[edgeStart][edgeEnd]:=g;od;
    od;
    vs:=[Identity(c.G)];for j in [2..degree+1] do Add(vs,edges[1][j]);od;
    value:=0;
    for term in cuts do
      left:=List([1..Length(term[1])-1],j->edges[term[1][j]][term[1][j+1]]);
      right:=List([1..Length(term[2])-1],j->edges[term[2][j]][term[2][j+1]]);
      sg:=1;
      if not binary then sg:=term[3]*U1CoefficientAction(c,ca,vs[term[1][1]])*U1CoefficientAction(c,cb,vs[term[2][1]]);fi;
      value:=value+sg*CallFuncList(a,left)*CallFuncList(b,right);
    od;
    if binary then return value mod 2;fi;return value;
  end);
end);
r:=(1,2,3,4);;m:=(2,4);;G:=Group(r,m);;
if r*m=m*r then Error("Nonabelian control collapsed");fi;
labels:=Cartesian([0..3],[0..1]);;elements:=List(labels,a->r^a[1]*m^a[2]);;
idx:=g->Position(elements,g);;
c:=rec(G:=G,s:=g->labels[idx(g)][2],r:=g->labels[idx(g)][1] mod 2);;
a:=function(xs...) local v;v:=Sum([1..Length(xs)],i->(2*i+1)*idx(xs[i]))-5;
 if v mod 4=0 then return 0;fi;return v/3;end;;
b:=function(xs...) local v;v:=Sum([1..Length(xs)],i->(3*i+2)*idx(xs[i]))-7;
 if v mod 5=0 then return 0;fi;return v/5;end;;
coeffs:=["Z","F2","Zs","Zr","Zt","U1s"];;checks:=0;;
for p in [0..3] do for q in [0..3] do for i in [0..Minimum(p,q)+1] do
 degree:=p+q-i;if degree<0 then continue;fi;
 for ca in coeffs do for cb in coeffs do for binary in [false,true] do
  old:=U1Cup(c,p,a,ca,q,b,cb,i,binary);;
  new:=NewU1Cup(c,p,a,ca,q,b,cb,i,binary);;
  for offset in [0..5] do
   xs:=List([1..degree],j->elements[1+((3*j+j^2+offset) mod 8)]);;
   if CallFuncList(old,xs)<>CallFuncList(new,xs) then Error("Signed nonabelian cup changed");fi;
   checks:=checks+1;
  od;
 od;od;od;
od;od;od;
Print("NONABELIAN_CUP_EXACT_CHECKS ",checks,"\n");;
QUIT_GAP(0);'''

@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class CupGeometryTests(unittest.TestCase):
    def test_signed_nonabelian_prefix_equivalence(self):
        with tempfile.TemporaryDirectory() as tmp:
            script = Path(tmp) / "check.g"
            script.write_text('U1_ROOT:="%s";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;\n' % ROOT + PROGRAM)
            result = subprocess.run(["gap", "-q", "-b", "--quitonbreak", str(script)],
                                    text=True, capture_output=True, timeout=60)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertIn("NONABELIAN_CUP_EXACT_CHECKS 19440", result.stdout)

if __name__ == "__main__":
    unittest.main()
