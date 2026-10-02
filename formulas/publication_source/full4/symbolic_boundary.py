"""Coefficient-exact transferred tensor differential, with all free tetrahedron data.
No source evaluations and no fitting are used. The output is compared with
independently recomputed source-shuffle polynomials by check_tensor_exact.py.
"""
from symbolic_target import *
import transfer_model as unt
from tensor_compact import gamma

def L0(n,u,m,v):
 return zero_L(n,u,m,v)+C(5,fun=lambda f: shdiff_local(2,3,n,u,m,v,f)+shdiff_local(3,2,n,u,m,v,f))
def zero_L(n,u,m,v):
 from tensor_compact import tensor5
 return tensor5(n,u,m,v)
def shdiff_local(p,q,n,u,m,v,f):
 def P(x):return C(x.deg,fun=lambda g:x(tuple(f[i] for i in g)),mod=x.mod)
 return unt.sh_diff(p,q,*map(P,(n,u,m,v)))
def gam_value(x,i):
 out=Bit.cast(1)
 for j in range(3):
  if i>>j&1:out*=digit(x,j)
 return out

def sample_inputs(deg):
 X=[Z({1<<(3*j+k):1<<k for k in range(3)},32) for j in range(4)]
 x,p,q,r=X;eps=Bit.var(12)
 small=C(2,values={(0,1,2):x},mod=None);small.closed=True
 tet=C(2,values={(0,1,2):p,(0,1,3):p+q,(0,2,3):q+r,(1,2,3):r},mod=None);tet.closed=True
 tu=C(3,values={(0,1,2,3):eps})
 return (small,C(3),tet,tu) if deg==(1,2,3) else (tet,tu,small,C(3))

if __name__=='__main__':
 deg=tuple(map(int,sys.argv[1:4]));start=time.time()
 n0,u0,m0,v0=sample_inputs(deg)
 s0=C(1,values={(0,1):1});w0=C(2);starts=(0,1,1+deg[1]);top5=tuple(range(6))
 R=Bit();newrows=[Bit() for _ in range(28)]
 basis=[(i,j)for i in range(1,8)for j in range(1,9-i)]
 paths=[g for g in simplex_shuffles(6)if g[0]==starts]
 for ix,g in enumerate(paths):
  pp=tuple(tuple(z[c]-starts[c]for z in g)for c in range(3))
  def P(x,i):return C(x.deg,fun=lambda f:x(tuple(pp[i][j]for j in f)),mod=x.mod)
  ss=P(s0,0);ww=P(w0,0);ns,us,ms,vs=P(n0,1),P(u0,1),P(m0,2),P(v0,2)
  ss.closed=ww.closed=ns.closed=ms.closed=True
  for j in range(7):
   ff=tuple(i for i in range(7)if i!=j)
   def restrict(x):return C(x.deg,fun=lambda f:x(tuple(ff[i]for i in f)),mod=x.mod)
   ssf,wwf,nn,uu,mm,vv=map(restrict,(ss,ww,ns,us,ms,vs))
   if j==0:
    # Actual d_0 of the decoded shared-background product, then re-encoding.
    sn=ss((0,1));nn=nn.scaled(1-2*int(bool(sn))) if sn in (0,1) else nn
    mm=mm.scaled(1-2*int(bool(sn))) if sn in (0,1) else mm
    # In base degree one W=s^2 is identically zero on every shuffle.
    # Hence the only first-face twist is simultaneous integer negation.
   R+=Bit.cast(L0(nn,uu,mm,vv)(top5))
   sv=ssf((0,1));nv=nn((1,2,3));mv=mm((3,4,5))
   for t,(a,b)in enumerate(basis):newrows[t]+=sv*gam_value(nv,a)*gam_value(mv,b)
  if ix%10==0:print('path',ix,'L terms',len(R.t),'seconds',time.time()-start,flush=True)
 out={'tridegree':deg,'variables':13,'Lzero_boundary_masks':sorted(R.t),'basis':basis,'new_differential_masks':[sorted(x.t)for x in newrows],'seconds':time.time()-start}
 (ROOT/f'full4/results/exact_boundary_{deg[1]}_{deg[2]}.json').write_text(json.dumps(out,indent=2))
 print('DONE',deg,len(R.t),time.time()-start,flush=True)
