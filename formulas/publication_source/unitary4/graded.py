"""Unitary shared-background tower as a graded product.

The root-zero cone is ONLY a graded coordinate identification. It is never
asserted to be a natural primitive. Its failure to commute with d_0 is kept
explicitly as the perturbation delta; faces d_i, i>0 commute exactly.
"""
from pathlib import Path
import sys,itertools
from functools import lru_cache
from collections import Counter
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'reference/d4_input/code'),str(ROOT/'terminal_general'),str(ROOT/'bosonic'),str(ROOT/'joint')]
from cochains import C,cup,primitive
from ez_homotopy import ez_homotopy,simplex_shuffles
from model import scalar_state

@lru_cache(None)
def faces(d,q):return tuple(itertools.combinations(range(d+1),q+1))
@lru_cache(None)
def index(d,q):return {f:i for i,f in enumerate(faces(d,q))}
# A graded simplex is (d, w, n, u0, m, v0), with normalized all-face arrays.
def field(S,j):
 d=S[0];q=3 if j in (3,5) else 2;mod=None if j in (2,4) else 2
 a=S[j]
 out=C(q,values={f:v for f,v in zip(faces(d,q),a) if v},mod=mod)
 if j in (1,2,4):out.closed=True
 return out
def pack(d,w,n,u,m,v):return (d,)+tuple(tuple(x(f) for f in faces(d,x.deg)) for x in (w,n,u,m,v))
def pull_arr(a,d,q,proj):
 ix=index(d,q)
 return tuple(0 if len(set(g))<len(g) else a[ix[g]] for f in faces(len(proj)-1,q) for g in [tuple(proj[i] for i in f)])
def pull(S,projs):
 d=S[0];dd=len(projs[0])-1
 return (dd,)+tuple(pull_arr(S[j],d,3 if j in (3,5) else 2,projs[0 if j==1 else 1 if j in (2,3) else 2]) for j in range(1,6))
def face(S,i):
 p=tuple(j for j in range(S[0]+1) if j!=i);return pull(S,(p,p,p))
def zero_factor(S,j):return not any(S[j]) and not any(S[j+1])
@lru_cache(maxsize=20000)
def normalized(S):
 """Normalization is in the graded product of base and TWO fiber factors."""
 d=S[0]
 if zero_factor(S,2) or zero_factor(S,4):return False
 for i in range(d):
  f=face(S,i+1);p=tuple(j if j<=i else j-1 for j in range(d+1))
  if pull(f,(p,p,p))==S:return False
 return True

def qroot(w,n):
 a=n.reduce(2)
 return C(3,fun=lambda f:0 if f[0]==0 else w((0,f[0],f[1]))*a(f[1:]))
def decode(S):
 w,n,u,m,v=(field(S,j) for j in range(1,6))
 return n,u+qroot(w,n),m,v+qroot(w,m),w

def encode(n,u,m,v,w,d):return pack(d,w,n,u+qroot(w,n),m,v+qroot(w,m))
@lru_cache(maxsize=20000)
def delta(S):
 """Twisted d_0 minus ordinary d_0, over F2, in graded coordinates."""
 if S[0]<=3 or not any(S[1]):return ()
 plain=face(S,0);n,u,m,v,w=decode(S);pr=tuple(range(1,S[0]+1))
 def P(x):return C(x.deg,fun=lambda f:x(tuple(pr[i] for i in f)),mod=x.mod)
 nn,uu,mm,vv,ww=map(P,(n,u,m,v,w))
 twisted=encode(nn,uu,mm,vv,ww,S[0]-1)
 if twisted==plain:return ()
 return tuple(x for x in (plain,twisted) if normalized(x))

def xor_add(out,x):
 if x in out:out.remove(x)
 else:out.add(x)
@lru_cache(maxsize=2000)
def H(S):
 out=set()
 for g in ez_homotopy(S[0]):
  if min(len(set(v[j] for v in g)) for j in (1,2))<3:continue
  p=tuple(tuple(v[j] for v in g) for j in range(3));ss=pull(S,p)
  if normalized(ss):xor_add(out,ss)
 return tuple(out)
def deltaH(chain):
 out=set()
 for S in chain:
  if not any(S[1]):continue
  for g in ez_homotopy(S[0]):
   # delta is identically zero on any grid with repeated first base vertex.
   if g[0][0]==g[1][0]:continue
   if min(len(set(v[j] for v in g)) for j in (1,2))<3:continue
   p=tuple(tuple(v[j] for v in g) for j in range(3));T=pull(S,p)
   if not normalized(T):continue
   for Q in delta(T):xor_add(out,Q)
 return out

def Hdelta(chain):
 out=set()
 for S in chain:
  for T in delta(S):
   for Q in H(T):xor_add(out,Q)
 return out

def chain_boundary(chain,twisted=False):
 out=set()
 for S in chain:
  for i in range(S[0]+1):
   Q=face(S,i)
   if normalized(Q):xor_add(out,Q)
  if twisted:
   for Q in delta(S):xor_add(out,Q)
 return out

def degree222(x,y,wval=1):
 """The only new shared-base tensor component in total degree six."""
 w=C(2,values={(0,1,2):wval});n=C(2,values={(0,1,2):x},mod=None);m=C(2,values={(0,1,2):y},mod=None)
 u=C(3);v=C(3);out=set()
 for g in simplex_shuffles(6):
  if g[0]!=(0,2,4):continue
  projections=tuple(tuple(v[j]-(0,2,4)[j] for v in g) for j in range(3))
  def P(c,p):return C(c.deg,fun=lambda f:c(tuple(p[i] for i in f)),mod=c.mod)
  S=pack(6,P(w,projections[0]),P(n,projections[1]),P(u,projections[1]),P(m,projections[2]),P(v,projections[2]))
  if normalized(S):xor_add(out,S)
 return out
