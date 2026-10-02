"""Equivalent interval-cut enumeration using the exact input-degree budgets.
The sum of vertex counts forces disjoint intervals for each repeated label.
No change of signs or lift convention.
"""
from functools import lru_cache
import itertools as it

@lru_cache(None)
def compositions(total,parts):
 if parts==0:return ((),) if total==0 else ()
 if parts==1:return ((total,),) if total>=1 else ()
 return tuple((first,)+tail for first in range(1,total-parts+2) for tail in compositions(total-first,parts-1))

@lru_cache(None)
def fast_cuts(word,degs):
 N=sum(degs)-len(word)+len(degs)
 if N<0:return ()
 occ=[tuple(i for i,x in enumerate(word) if x==j) for j in range(1,len(degs)+1)]
 if any(not o for o in occ):return ()
 out=[]
 for blocks in it.product(*(compositions(d+1,len(o)) for d,o in zip(degs,occ))):
  ls=[0]*len(word)
  for inds,block in zip(occ,blocks):
   for i,value in zip(inds,block):ls[i]=value
  starts=[];v=0
  for leng in ls:starts.append(v);v+=leng-1
  assert v==N
  fs=[];valid=True
  for inds,d in zip(occ,degs):
   seq=tuple(z for i in inds for z in range(starts[i],starts[i]+ls[i]))
   if len(set(seq))!=len(seq):valid=False;break
   assert len(seq)==d+1
   fs.append(seq)
  if not valid:continue
  sign=(-1)**sum(ls[i]*ls[j] for i in range(len(word)) for j in range(i+1,len(word)) if word[i]>word[j])
  out.append((tuple(fs),sign))
 return tuple(out)
