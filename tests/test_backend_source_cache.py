"""A source cache belongs to its exact symmetry context, including omega."""
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


@unittest.skipUnless(shutil.which("gap"), "GAP and HAP are required")
class SourceCacheTests(unittest.TestCase):
    def test_reused_and_shallow_copied_states_respect_background(self):
        program = r'''
OnBreak:=function() Where(10);QUIT_GAP(1);end;;
U1_ROOT:="@ROOT@";;Read(Concatenation(U1_ROOT,"/gap/load.g"));
c0:=U1CyclicContext(2,0,0,0);;
q:=function(g,h)
  return QuoInt(g!.exponents[1]+h!.exponents[1],2);
end;;
c1:=U1NewContext(c0.G,c0.R,c0.s,c0.rho,
  function(g,h) return q(g,h)/2;end,0);;
g:=GeneratorsOfGroup(c0.G)[1];;
state:=rec(sheet:=U1Zero,charge:=q,phase:=U1Zero);;
source0:=U1Source(c0,2,state);;
if U1Mod1(source0(g,g,g,g))<>1/2 then Error("Incorrect zero-extension control");fi;
if not IsIdenticalObj(source0,U1Source(c0,2,state)) then Error("Same-context cache miss");fi;
# The caller may keep complete states on the context, creating a record cycle.
# Identity comparison must neither recurse through it nor compare by value.
c0.classificationStates:=rec(charge:=[state]);;
source1:=U1Source(c1,2,state);;
fresh:=U1Source(c1,2,rec(sheet:=U1Zero,charge:=q,phase:=U1Zero));;
if U1Mod1(source1(g,g,g,g))<>0 or source1(g,g,g,g)<>fresh(g,g,g,g) then
  Error("State source cache leaked the previous omega background");
fi;
copy:=ShallowCopy(state);;
copiedSource0:=U1Source(c0,2,copy);;
if copiedSource0(g,g,g,g)<>source0(g,g,g,g) then
  Error("Shallow-copied state reused another context's source");
fi;
if not IsIdenticalObj(source1,U1Source(c1,2,state)) then
  Error("Replacing the shallow copy's cache mutated the original state");
fi;
Print("CONTEXT_SOURCE_CACHE_PASSED\n");QUIT_GAP(0);
'''.replace("@ROOT@", str(ROOT))
        with tempfile.TemporaryDirectory() as directory:
            path = Path(directory) / "cache.g"
            path.write_text(program)
            process = subprocess.run(
                ["gap", "-q", "-b", str(path)], capture_output=True,
                text=True, timeout=30,
            )
        self.assertEqual(process.returncode, 0, process.stdout + process.stderr)
        self.assertIn("CONTEXT_SOURCE_CACHE_PASSED", process.stdout)


if __name__ == "__main__":
    unittest.main()
