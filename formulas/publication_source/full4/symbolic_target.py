"""Independent coefficient-exact s tensor fiber calculation (not a sampled fit)."""
from graded_full import *
# Install exact lift arithmetic for the unmodified lazy source evaluator.
from symbolic_lazy import Bit,Z
import symbolic_precision
from model import digit
from fractional import *
from cubic_repair import repaired_residual
import explicit_pip,polynomial_tables
import json,time
from symbolic_fastcuts import install
install()
sys.setrecursionlimit(30000)

def total_polynomial(n,w,s,filename,degree,**kw):
 data=polynomial_tables.table(filename)
 def gam(x,e):
  ans=Bit.cast(1)
  for j in range(4):
   if e>>j&1:ans*=digit(x,j)
  return ans
 def ev(f):
  out=Bit()
  for block in data['blocks']:
   i,j,k=block['i'],block['j'],block['k'];ans=Bit.cast(1)
   for v in range(i):ans*=s((f[v],f[v+1]))
   if not ans:continue
   mid=f[i:i+j+1];end=f[i+j:]
   def nv(ff):return ((-1)**(s(tuple(sorted((f[0],ff[0])))) if f[0]!=ff[0] else 0))*n(ff)
   ns=[nv((mid[r-1],mid[r],mid[t]))-nv((mid[r-1],mid[r],mid[t-1])) for r,t in itertools.combinations(range(1,j+1),2)]
   ws=[w((end[r-1],end[r],end[t]))+w((end[r-1],end[r],end[t-1])) for r,t in itertools.combinations(range(1,k+1),2)]
   for nc,wc in block['terms']:
    term=ans;nc=int(nc)
    for z,x in enumerate(ws):
     if wc>>z&1:term*=x
    if not term:continue
    for z,x in enumerate(ns):
     ee=(nc>>(4*z))&15
     if ee:term*=gam(x,ee)
     if not term:break
    out+=term
  return out
 return C(degree,fun=ev)
polynomial_tables.total_cochain=total_polynomial

def rho_direct(n,u,m,v,w,s):
 # On a 1,2,3 or 1,3,2 shuffle, each individual state factors through
 # a simplicial set of dimension <=4. Every individual natural six-cochain
 # is zero. Only the merged high source must be evaluated.
 N=n+m;U=u+v+cup(n.reduce(2),m.reduce(2),1)
 y=explicit_pip.binary_completion(N,w,s,accelerate=False)
 rr=repaired_residual(n,u,m,v,w,s,ys=[C(6),C(6),y])
 return rr+cup(w+cup(s,s),cup(n.reduce(2),m.reduce(2)))

if __name__=='__main__':
 import sys
 deg=tuple(map(int,sys.argv[1:4]));start=int(sys.argv[4]) if len(sys.argv)>4 else 0;stop=int(sys.argv[5]) if len(sys.argv)>5 else 60
 st=time.time();prec=32
 X=[]
 for j in range(4):X.append(Z({1<<(3*j+k):1<<k for k in range(3)},prec))
 x,p,q,r=X;eps=Bit.var(12)
 small=C(2,values={(0,1,2):x},mod=None);small.closed=True
 tet=C(2,values={(0,1,2):p,(0,1,3):p+q,(0,2,3):q+r,(1,2,3):r},mod=None);tet.closed=True
 tu=C(3,values={(0,1,2,3):eps})
 n0,u0,m0,v0=(small,C(3),tet,tu) if deg==(1,2,3) else (tet,tu,small,C(3))
 s0=C(1,values={(0,1):1});w0=C(2);starts=(0,1,1+deg[1]);d=6;R=Bit();rows=[]
 paths=[g for g in simplex_shuffles(d) if g[0]==starts]
 for ix,g in enumerate(paths):
  if ix<start or ix>=stop:continue
  pp=tuple(tuple(z[c]-starts[c] for z in g) for c in range(3))
  def P(c,i):return C(c.deg,fun=lambda f:c(tuple(pp[i][j] for j in f)),mod=c.mod)
  s=P(s0,0);w=P(w0,0);s.closed=w.closed=True
  n=trivialize(P(n0,1),s);m=trivialize(P(m0,2),s);u=P(u0,1);v=P(v0,2)
  ti=time.time();rr=Bit.cast(rho_direct(n,u,m,v,w,s)(tuple(range(7))));R+=rr
  rows.append({'index':ix,'masks':sorted(rr.t),'seconds':time.time()-ti})
  print('shuffle',ix,'terms',len(rr.t),'seconds',time.time()-ti,'total',time.time()-st,flush=True)
  (ROOT/f'full4/results/exact_s_{deg[1]}_{deg[2]}_{start}_{stop}.json').write_text(json.dumps({'tridegree':deg,'variables':13,'rows':rows,'sum_masks':sorted(R.t),'seconds':time.time()-st}))
