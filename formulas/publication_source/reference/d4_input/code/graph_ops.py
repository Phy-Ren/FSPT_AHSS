"""Normalized numerical-polynomial cochains on K(Z,2), and binary K(F2,2)."""
from functools import lru_cache
from itertools import combinations,product
from math import comb
@lru_cache(None)
def edges(n):return tuple(combinations(range(1,n+1),2))
@lru_cache(None)
def edgeidx(n):return {e:i for i,e in enumerate(edges(n))}
def exponents(code,n):return [(code>>(4*i))&15 for i in range(len(edges(n)))]
def encode(xs):return sum(x<<(4*i) for i,x in enumerate(xs))
def weight(code,n):return sum(exponents(code,n))
def rank(code,n):
 j=0;r=0
 for i,k in enumerate(exponents(code,n)):
  for z in range(k):j+=1;r+=comb(i+j-1,j)
 return r
@lru_cache(None)
def differential(code,n):
 """Vertex splitting. Each graph edge has a nonnegative multiplicity."""
 es=edges(n);ts=edgeidx(n+1);a=exponents(code,n);ans=set()
 for v in range(1,n+1):
  b=[0]*len(ts);inc=[]
  for e,k in zip(es,a):
   if not k:continue
   u,w=e
   if v not in e:b[ts[u+(u>v),w+(w>v)]]=k;continue
   other=w if u==v else u;other+=other>v
   e1=ts[tuple(sorted((v,other)))];e2=ts[tuple(sorted((v+1,other)))];inc.append((e1,e2,k))
  for choice in product(*(range(k+1) for _,_,k in inc)):
   if sum(choice)==0 or sum(choice)==sum(k for _,_,k in inc):continue
   for (e1,e2,k),a1 in zip(inc,choice):b[e1]=a1;b[e2]=k-a1
   term=encode(b)
   if term in ans:ans.remove(term)
   else:ans.add(term)
 return frozenset(ans)
@lru_cache(None)
def inversion(code,n):
 options=[]
 for k in exponents(code,n):
  options.append([0] if not k else [j for j in range(1,k+1) if comb(k-1,j-1)%2])
 return frozenset(encode(ks) for ks in product(*options))
def w_to_code(mask,n):return sum(((mask>>i)&1)<<(4*i) for i in range(len(edges(n))))
def code_to_w(code,n):
 xs=exponents(code,n)
 if any(k>1 for k in xs):raise ValueError('not a simple graph')
 return sum(k<<i for i,k in enumerate(xs))
@lru_cache(None)
def dw(mask,n):return frozenset(code_to_w(c,n+1) for c in differential(w_to_code(mask,n),n))
def toggle(s,x):
 if x in s:s.remove(x)
 else:s.add(x)

def load_anf(data):
 j=data['j'];k=data['k'];m=len(edges(j));result=set()
 for mask in data['masks']:
  nc=encode([((mask>>t)&1)+2*((mask>>(m+t))&1) for t in range(m)])
  wc=mask>>(2*m);toggle(result,(nc,wc))
 return result

def normal_w(mask,n):
 cover=0
 for t,(a,b) in enumerate(edges(n)):
  if mask>>t&1:cover|=1<<(a-1)|1<<(b-1)
 return cover==(1<<n)-1
