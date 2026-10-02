"""Shared s,w background: graded coordinates and exact first-face twist.

One coordinate chart is used ONLY inside the finite EZ perturbation. Its
root choice is NOT a natural phase primitive. The change under d_0 is kept.
State format: (dimension, s, w, n0, u0, m0, v0), all-face arrays.
"""
from pathlib import Path
import sys,itertools
from functools import lru_cache
ROOT=Path(__file__).resolve().parents[1]
sys.path[:0]=[str(ROOT/'reference/d4_input/code'),str(ROOT/'terminal_general'),str(ROOT/'bosonic'),str(ROOT/'joint'),str(ROOT/'unitary4')]
from cochains import C,cup,ds,primitive
from ez_homotopy import ez_homotopy,simplex_shuffles
from model import scalar_state
@lru_cache(None)
def faces(d,q):return tuple(itertools.combinations(range(d+1),q+1))
@lru_cache(None)
def index(d,q):return {f:i for i,f in enumerate(faces(d,q))}
def field(S,j):
 d=S[0];q=1 if j==1 else 3 if j in (4,6) else 2;mod=None if j in (3,5) else 2
 out=C(q,values={f:v for f,v in zip(faces(d,q),S[j]) if v},mod=mod)
 if j in (1,2,3,5):out.closed=True
 return out

def pack(d,s,w,n,u,m,v):return (d,)+tuple(tuple(x(f) for f in faces(d,x.deg)) for x in (s,w,n,u,m,v))
def pull_arr(a,d,q,proj):
 ix=index(d,q)
 return tuple(0 if len(set(g))<len(g) else a[ix[g]] for f in faces(len(proj)-1,q) for g in [tuple(proj[i] for i in f)])
def pull(S,projs):
 d=S[0];dd=len(projs[0])-1
 return (dd,)+tuple(pull_arr(S[j],d,1 if j==1 else 3 if j in (4,6) else 2,projs[0 if j in (1,2) else 1 if j in (3,4) else 2]) for j in range(1,7))
def face(S,i):
 p=tuple(j for j in range(S[0]+1) if j!=i);return pull(S,(p,p,p))
def zero_factor(S,j):return not any(S[j]) and not any(S[j+1])
@lru_cache(maxsize=100000)
def normalized(S):
 d=S[0]
 if zero_factor(S,3) or zero_factor(S,5):return False
 for i in range(d):
  f=face(S,i+1);p=tuple(j if j<=i else j-1 for j in range(d+1))
  if pull(f,(p,p,p))==S:return False
 return True

def qroot(W,n):
 a=n.reduce(2)
 return C(3,fun=lambda f:0 if f[0]==0 else W((0,f[0],f[1]))*a(f[1:]))
def trivialize(n,s):
 """T is its own inverse and converts twisted to ordinary integral cochains."""
 return C(n.deg,fun=lambda f:n(f)*((-1)**(s((0,f[0])) if f[0] else 0)),mod=None)
def decode(S):
 s,w,n0,u0,m0,v0=(field(S,j) for j in range(1,7));W=w+cup(s,s)
 n=trivialize(n0,s);m=trivialize(m0,s)
 return n,u0+qroot(W,n),m,v0+qroot(W,m),w,s

def encode(n,u,m,v,w,s,d):
 W=w+cup(s,s)
 return pack(d,s,w,trivialize(n,s),u+qroot(W,n),trivialize(m,s),v+qroot(W,m))
@lru_cache(maxsize=100000)
def delta(S):
 if S[0]<=2 or (not any(S[1]) and not any(S[2])):return ()
 plain=face(S,0);n,u,m,v,w,s=decode(S);pr=tuple(range(1,S[0]+1))
 def P(x):return C(x.deg,fun=lambda f:x(tuple(pr[i] for i in f)),mod=x.mod)
 nn,uu,mm,vv,ww,ss=map(P,(n,u,m,v,w,s))
 twisted=encode(nn,uu,mm,vv,ww,ss,S[0]-1)
 if twisted==plain:return ()
 return tuple(x for x in (plain,twisted) if normalized(x))
def xor_add(out,x):
 if x in out:out.remove(x)
 else:out.add(x)
@lru_cache(maxsize=3000)
def H(S):
 out=set()
 for g in ez_homotopy(S[0]):
  if min(len(set(v[j] for v in g)) for j in (1,2))<3:continue
  T=pull(S,tuple(tuple(v[j] for v in g) for j in range(3)))
  if normalized(T):xor_add(out,T)
 return tuple(out)
def deltaH(chain):
 out=set()
 for S in chain:
  if not any(S[1]) and not any(S[2]):continue
  for g in ez_homotopy(S[0]):
   if g[0][0]==g[1][0]:continue
   if min(len(set(v[j] for v in g)) for j in (1,2))<3:continue
   T=pull(S,tuple(tuple(v[j] for v in g) for j in range(3)))
   if not normalized(T):continue
   for Q in delta(T):xor_add(out,Q)
 return out

def boundary(chain,twisted=False):
 out=set()
 for S in chain:
  for j in range(S[0]+1):
   Q=face(S,j)
   if normalized(Q):xor_add(out,Q)
  if twisted:
   for Q in delta(S):xor_add(out,Q)
 return out

def tensor_cell(i,j,k,s,w,n,u,m,v):
 """Shuffle of factor cells, each numbered locally from zero."""
 d=i+j+k;out=set();starts=(0,i,i+j)
 for g in simplex_shuffles(d):
  if g[0]!=starts:continue
  pp=tuple(tuple(z[c]-starts[c] for z in g) for c in range(3))
  def P(x,c):return C(x.deg,fun=lambda f:x(tuple(pp[c][t] for t in f)),mod=x.mod)
  S=pack(d,P(s,0),P(w,0),P(n,1),P(u,1),P(m,2),P(v,2))
  if normalized(S):xor_add(out,S)
 return out
