"""Bounded check of read-only public parity evaluator against neutral E8."""
from pathlib import Path
from fractions import Fraction as F
from itertools import combinations
import sys,random,json,hashlib,argparse,subprocess
ap=argparse.ArgumentParser()
ap.add_argument("--public-reference",type=Path,default=Path("/home/xingyu/FSPT_AHSS_public"))
ap.add_argument("--e8-reference",type=Path,default=Path("/home/xingyu/AllFSPT_reviews/e8_v09_da3ad936/E8_AHSS_v0_9"))
args=ap.parse_args()
sys.dont_write_bytecode=True
PUBLIC=args.public_reference
E8=args.e8_reference
sys.path.insert(0,str(PUBLIC));sys.path.insert(0,str(E8/'src'))
from fspt.full_formula.runtime import Backend
from e8_4p1 import source,product
from simplex import rand,char,C
backend=Backend(use_native=False)
rng=random.Random(2026101516);checks=[]
def array(c):
 out=[0]*(1<<(c.N+1))
 for f,v in c.v.items():out[sum(1<<j for j in f)]=int(v)
 return tuple(out)
for case in range(4):
 N=6;tw=[0]*(N+1) if case==0 else [rng.randrange(2) for _ in range(N+1)]
 e=rand(N,1,tw,rng,lo=-2,hi=3).d();f=rand(N,1,tw,rng,lo=-2,hi=3).d()
 s=char(N,tw);w=rand(N,1,None,rng).d().mod(2)
 zero=(0,)*(1<<(N+1))
 fields={'n':array(e.sc(16)),'a':zero,'c':zero,'s':array(s),'w':array(w)}
 actual=backend.source(4,'bosonic',fields);expected=source(e)(tuple(range(7)))%1
 assert actual==expected,(case,'source',actual,expected)
 # The separately certified binary4 is identically zero; verify the remaining
 # exact compiled polynomial on every six-vertex face, retaining all signs.
 for face in combinations(range(7),6):
  def restrict(arr):
   ans=[0]*64
   for mask in range(64):ans[mask]=arr[sum(1<<face[j] for j in range(6) if mask&(1<<j))]
   return tuple(ans)
  ff={k:restrict(v) for k,v in fields.items()}
  ff.update(m=restrict(array(f.sc(16))),b=(0,)*64,cp=(0,)*64)
  actual=F(backend.program('nonbinary4',ff)[0]%48,48)
  expected=product(e,f)(face)%1
  assert actual==expected,(case,'product',face,actual,expected)
 checks.append({'case':case,'source':str(expected),'product_faces':7})
result={'status':'PASS','source_checks':4,'product_checks':28,'binary_product_certificate':'probe_parity_sixteen_valuation.json','public_revision':subprocess.check_output(['git','-C',str(PUBLIC),'rev-parse','HEAD'],text=True).strip(),'public_reference':str(PUBLIC),'e8_reference':str(E8),'backend_sha256':hashlib.sha256((PUBLIC/'fspt/full_formula/runtime.py').read_bytes()).hexdigest(),'scope':'Pure sixteen-sheet source and product only; no nonzero-CI universal parity dictionary claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
