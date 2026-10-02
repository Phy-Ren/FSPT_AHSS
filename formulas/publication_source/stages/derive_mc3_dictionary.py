"""Exact word-basis derivation of the zero-background closed-Majorana dictionary.
Only degree-three closed input is used; no assumption for open input is made.
"""
from pathlib import Path
import sys,json,time
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT/'joint'))
from symbolic_lazy import *
from cochains import C,cup,op,adem,prism_transgression
from functools import lru_cache
from itertools import combinations
st=time.time();dim=6;top=tuple(range(7));faces=list(combinations(range(1,7),3));z=C(3,values={(0,)+f:Bit.var(i) for i,f in enumerate(faces)})
u=C(3,fun=lambda f:z(f) if f[0]==0 else sum(z((0,)+f[:i]+f[i+1:]) for i in range(4)));u.closed=True
D=json.loads(ROOT.joinpath('stages/data/T6_zero_anf.json').read_text());uf=[u(tuple(f)) for f in D['faces']]
val=Bit.cast(0)
for mm in D['ANF_masks']:
 mask=int(mm);term=Bit.cast(1)
 while mask:
  i=(mask&-mask).bit_length()-1;term*=uf[i];mask&=mask-1
 val+=term
val+=adem(u)(top)+cup(u,u)(top)
print('target',len(val.t),'time',time.time()-st,flush=True)
def canon(w):
 names={};o=[]
 for x in w:
  if x not in names:names[x]=len(names)+1
  o.append(names[x])
 return tuple(o)
@lru_cache(None)
def dwords(w):
 out=set()
 for j in range(len(w)):
  v=w[:j]+w[j+1:]
  if set(v)!=set(w) or any(v[k]==v[k+1] for k in range(len(v)-1)):continue
  v=canon(v)
  if v in out:out.remove(v)
  else:out.add(v)
 return out
@lru_cache(None)
def evalword(w):return op(''.join(map(str,w)),u,u,u,u)(top)
words=[]
def rec(w,c):
 if len(w)==11:
  if len(c)==4:words.append(tuple(w))
  return
 for x in range(1,min(4,len(c)+1)+1):
  if x==w[-1]:continue
  if x>len(c):rec(w+[x],c+[1])
  elif c[x-1]<4:
   q=c[:];q[x-1]+=1;rec(w+[x],q)
rec([1],[1])
words.sort(key=lambda w:(len(dwords(w)),w))
indices={}
def vector(t):
 out=0
 for m in t:
  if m not in indices:indices[m]=len(indices)
  out^=1<<indices[m]
 return out
rhs=vector(val.t);basis={};done=False
for j,w in enumerate(words):
 pol=Bit.cast(0)
 for dw in dwords(w):pol+=evalword(dw)
 col=vector(pol.t);wit=1<<j
 while col:
  p=col.bit_length()-1
  if p not in basis:basis[p]=(col,wit);break
  co,wi=basis[p];col^=co;wit^=wi
 if j%100==0:
  v=rhs;sol=0
  while v:
   p=v.bit_length()-1
   if p not in basis:break
   co,wi=basis[p];v^=co;sol^=wi
  print(j,'rank',len(basis),'rows',len(indices),'time',time.time()-st,flush=True)
  if not v:
   answer=[words[i] for i in range(j+1) if (sol>>i)&1];done=True;break
if not done:raise RuntimeError('Not in the diagonal arity-four word span')
ans=C(5)
for w in answer:ans=ans+op(''.join(map(str,w)),u,u,u,u)
assert not (ans.d()(top)+val)
result={'identity':'d H5=T6(u)+x3(u)+u cup u, du=0','words':[''.join(map(str,w)) for w in answer],'independent_bits':len(faces),'exact_polynomial_check':True,'seconds':time.time()-st}
ROOT.joinpath('stages/results/mc3_zero_dictionary_derived.json').write_text(json.dumps(result,indent=2))
print('EXACT DICTIONARY',len(answer),result['words'],time.time()-st,flush=True)
