"""Evaluate the incoming Majorana class for Z2 x Z4 in normalized bar cochains.

Usage: python check_split_pair_secondary.py [--formula-repo /path/to/FSPT_AHSS]
Checks the trivialization on every four-simplex and the two mixed periods.
"""
import argparse, sys,itertools,json
from pathlib import Path
from fractions import Fraction
from collections import defaultdict
parser=argparse.ArgumentParser(description=__doc__)
parser.add_argument('--formula-repo', type=Path,
                    default=Path(__file__).resolve().parents[3],
                    help='Formula checkout; defaults to this repository.')
args=parser.parse_args()
sys.path.insert(0,str(args.formula_repo.resolve()))
from fspt.formulas import field,cup,zero,obstruction,evaluate
x,y,h=field('x',1),field('y',1),field('h',1)
a=x*y
c=x*x*h+x*cup(y,x,1)*y
res=(c.differential()+a*a).reduce(2)
O=obstruction(a,c,zero(2),zero(1))
def fields(seq):
 v=[(0,0)]
 for ga,gb in seq:v.append(((v[-1][0]+ga)%2,(v[-1][1]+gb)%4))
 def one(k,n):return lambda f:(v[f[1]][k]-v[f[0]][k])%n
 fx=one(0,2);fy=one(1,4)
 return {'x':fx,'y':lambda f:fy(f)%2,'h':lambda f:fy(f)//2}
for s in itertools.product(list(itertools.product(range(2),range(4))),repeat=4):assert evaluate(res,fields(s))==0

def cyc(n,k):
 if k==1:return [((1,),1)]
 if k==2:return [((i,1),1) for i in range(n)]
 if k==3:return [((1,i,1),1) for i in range(n)]
 if k==4:return [((i,1,j,1),1) for i,j in itertools.product(range(n),repeat=2)]

def shuffle(p,q):
 for pp in itertools.combinations(range(p+q),p):
  pp=set(pp);arr=[0 if i in pp else 1 for i in range(p+q)]
  inv=sum(arr[i]>arr[j] for i in range(p+q) for j in range(i+1,p+q))
  yield arr,(-1)**inv

def ext(p,q):
 for ca,sgna in cyc(2,p):
  for cb,sgnb in cyc(4,q):
   for arr,sgn in shuffle(p,q):
    ia=ib=0;out=[]
    for which in arr:
     if which==0:out.append((ca[ia],0));ia+=1
     else:out.append((0,cb[ib]));ib+=1
    yield tuple(out),sgn*sgna*sgnb

def vals(seq):
 f=fields(seq)
 # C1 = m1a m2a m2b/2; C2=m2a m1b m2b/4
 a=[g[0] for g in seq];b=[g[1] for g in seq]
 C1=Fraction(a[0]*((a[1]+a[2])//2)*((b[3]+b[4])//4),2)
 C2=Fraction(((a[0]+a[1])//2)*b[2]*((b[3]+b[4])//4),4)
 return [Fraction(evaluate(O,f),8),C1,C2]
periods=[]
for terms in [[(1,1,4),(2,2,3)],[(1,3,2),(2,4,1)]]:
 sums=[Fraction(0)]*3
 boundary=defaultdict(int)
 for k,p,q in terms:
  for seq,sgn in ext(p,q):
   sums=[z+k*sgn*w for z,w in zip(sums,vals(seq))]
   faces=[seq[1:]]
   for j in range(4):
    merged=((seq[j][0]+seq[j+1][0])%2,(seq[j][1]+seq[j+1][1])%4)
    faces.append(seq[:j]+(merged,)+seq[j+2:])
   faces.append(seq[:-1])
   for j,face in enumerate(faces):
    if (0,0) not in face:boundary[face]+=k*sgn*(-1)**j
 assert not any(boundary.values()), 'The purported bar cycle is not closed'
 periods.append([z%1 for z in sums])
assert periods==[[Fraction(0),Fraction(0),Fraction(1,2)],
                 [Fraction(1,2),Fraction(1,2),Fraction(0)]]
print(json.dumps({'group':'Z2 x Z4','four_simplices_checked':4096,
 'period_columns':['Majorana secondary obstruction','C5^(1)','C5^(2)'],
 'periods':[[str(x) for x in row] for row in periods],
 'result':'The incoming Majorana class equals C5^(1).'},indent=2))
