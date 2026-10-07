"""Signed acyclic-carrier extension of the frozen binary three-factor EZ map.
Standalone integer-chain certificate for the Majorana carry reduction.
"""
from functools import lru_cache
from collections import defaultdict

def clean(x):return {k:v for k,v in x.items()if v}
@lru_cache(None)
def shuffles(n):
 out=defaultdict(int)
 for a in range(n+1):
  for b in range(a,n+1):
   counts=[a,b-a,n-b];path=[(0,a,b)];steps=[]
   def rec():
    if not any(counts):
     sign=(-1)**sum(x>y for i,x in enumerate(steps)for y in steps[i+1:]);out[tuple(path)]+=sign;return
    for d in range(3):
     if counts[d]:
      counts[d]-=1;v=list(path[-1]);v[d]+=1;path.append(tuple(v));steps.append(d)
      rec();steps.pop();path.pop();counts[d]+=1
   rec()
 return clean(out)
@lru_cache(None)
def homotopy(n):
 if n==0:return{}
 zero=(0,0,0);out=defaultdict(int)
 for f,c in shuffles(n).items():
  if f[0]!=zero:out[(zero,)+f]-=c
 for f,c in homotopy(n-1).items():out[(zero,)+tuple(tuple(j+1 for j in v)for v in f)]-=c
 return clean(out)
def boundary(chain):
 out=defaultdict(int)
 for f,c in chain.items():
  for j in range(len(f)):
   ff=f[:j]+f[j+1:]
   if len(set(ff))==len(ff):out[ff]+=(-1)**j*c
 return clean(out)
def verify(max_degree=6):
 records=[]
 for n in range(1,max_degree+1):
  residual=defaultdict(int,boundary(homotopy(n)))
  for j in range(n+1):
   face=[i for i in range(n+1)if i!=j]
   for f,c in homotopy(n-1).items():residual[tuple(tuple(face[v]for v in t)for t in f)]+=(-1)**j*c
  residual[tuple((i,i,i)for i in range(n+1))]-=1
  for f,c in shuffles(n).items():residual[f]+=c
  assert not clean(residual),(n,clean(residual))
  for collapse in range(n):
   out=defaultdict(int)
   for f,c in homotopy(n).items():
    image=tuple(tuple(j-(j>collapse)for j in v)for v in f)
    if len(set(image))==len(image):out[image]+=c
   assert not clean(out),(n,collapse,clean(out))
  records.append({'degree':n,'terms':len(homotopy(n)),'boundary_residual':0,'normalized':True})
 return records
if __name__=='__main__':
 import json
 print(json.dumps({'status':'PASS','identity':'dH+Hd=id-shAW over Z','checks':verify()},indent=2))
