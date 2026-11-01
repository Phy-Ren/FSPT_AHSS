"""Check the normalized-bar Cartan correction for split rank-two examples.

Usage: python check_split_pair_cochains.py [--formula-repo /path/to/FSPT_AHSS]
The formula repository supplies the published cochain operations.
"""
import argparse, sys, itertools, random, json
from pathlib import Path
from fractions import Fraction
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--formula-repo', type=Path,
                    default=Path(__file__).resolve().parents[3],
                    help='Formula checkout; defaults to this repository.')
args=parser.parse_args()
sys.path.insert(0, str(args.formula_repo.resolve()))
from fspt.formulas import field, word, cup, square, evaluate
x,y=field('x',2),field('y',2)
z=word('1231343',x,x,y,y)
res=(z.differential()+square(x*y,2)+x*x*y+x*y*y).reduce(2)
s1=square(x,1)
random.seed(20261101)
records=[]
for M,N in [(2,2),(2,4),(2,8),(4,4),(4,8),(8,16),(6,10),(5,7)]:
 total=0
 points=(tuple((a//N,a%N) for a in seq) for seq in itertools.product(range(M*N),repeat=6)) if (M,N)==(2,2) else (tuple((random.randrange(M),random.randrange(N)) for _ in range(6)) for __ in range(1000))
 for seq in points:
  verts=((0,0),)+seq
  def carry(k,n):
   def fn(f):
    a,b,c=(verts[i][k] for i in f)
    return (((b-a)%n)+((c-b)%n))//n
   return fn
  fields={'x':carry(0,M),'y':carry(1,N)}
  assert evaluate(res,fields)==0,(M,N,seq)
  assert evaluate(s1,fields,tuple(range(4)))==0,(M,N,seq)
  def phase(face):
   v=tuple(face)
   c1=Fraction(((verts[v[1]][0]-verts[v[0]][0])%M)
               *fields['x'](v[1:4])*fields['y'](v[3:6]),M)
   c2=Fraction(fields['x'](v[:3])
               *((verts[v[3]][1]-verts[v[2]][1])%N)
               *fields['y'](v[3:6]),N)
   return (c1+c2+evaluate(z,fields,v))/2
  face=tuple(range(7))
  derivative=sum((-1)**j*phase(face[:j]+face[j+1:]) for j in range(7))
  target=Fraction(evaluate(square(x*y,2),fields),2)
  assert (derivative-target)%1==0,(M,N,seq,derivative,target)
  total+=1
 records.append({'orders':[M,N],'simplices':total,'cartan_residual':0,'Sq1_carry':0,'phase_obstruction_residual':0})
print(json.dumps(records,indent=2))
