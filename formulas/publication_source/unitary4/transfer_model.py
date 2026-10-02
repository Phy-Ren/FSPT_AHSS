"""Finite unitary-background transfer, lower multiplication branch 1.

The new background cell is verified in check_background_cell.py.
These helpers transport the accepted zero-background tensor primitive to
the characteristic-star coordinate; unitary_product.py assembles the
complete source/product in the retained characteristic-B/APS coordinate.
All internal binary arithmetic is exact over F2.
"""
from graded import *
from cubic_repair import repaired_residual,star_fractional_seed16,cubic_coordinate16,binary_correction,star_source16
from fractional import third_product,upper_seed16
from explicit_pip import binary_completion
# The imported terminal_general model module is named `model`; use its symbols
# through `graded` rather than importing this file under that same name.
import model as zero
from product import binary_product as zero_Zold
from tensor_compact import tensor5 as zero_Lold
from ez_pair import homotopy as zero_H

# Use Ostar for the internal binary transfer.  The public complete product
# is transported to B/APS by the explicit cubic pair and coordinate change.
def seed16(n,u,m,v,w):return star_fractional_seed16(n,u,m,v,w,C(1))
def old_frac_dyadic16(n,u,m,v):
 # 1/12 has dyadic coefficient 3/4; its odd-primary component has a separate product.
 D=zero.pair_data(n,u,m,v);bb,bp,la,r,dd=(D[k] for k in ('B','Bp','lam','R','D'))
 bn=C(2,fun=lambda f:m(f)*(m(f)-1)//2,mod=None);q=cup(n,m,1)
 quart=(cup(bb,bp,3)+cup(bb+bp,dd,3)+cup(la,la,1)+cup(la,la.d(),2)+cup(r,la.d(),3)+zero.ZetaZ(m,n)-cup(bn,cup(n,n,1)))
 cubic=cup(n+m.scaled(2),q)+cup(q,n.scaled(2)+m)
 return quart.scaled(4)-cubic.scaled(12)
def source_gauge16(n,u):return cup(u,n.reduce(2)).lift().scaled(8)+cup(n,u.lift()).scaled(4)
def quarter_gauge4(n,u,m,v):
 a=n.reduce(2);b=m.reduce(2);t=cup(a,b,1)
 return cup(v,a,1)+cup(b,t,1)+zero.op('23123',a,b,b)

def diff5(n,u,m,v):
 N,U,e=zero.lower(n,u,m,v)
 # EdyadicB = Estar + Delta(G), with G=ua/2+nu/4 at w=0.
 G=source_gauge16(N,U)-source_gauge16(n,u)-source_gauge16(m,v)
 return (old_frac_dyadic16(n,u,m,v)-G-seed16(n,u,m,v,C(2))-quarter_gauge4(n,u,m,v).lift().d().scaled(4)).div(8).reduce(2)

def sh_diff(p,q,n,u,m,v):
 # Inputs are on an ordered p+q simplex but belong to its front/back factors.
 f=tuple(range(p+q+1));out=0
 for ones in itertools.combinations(range(p+q),p):
  on=set(ones);i=0;j=p;path=[(i,j)]
  for z in range(p+q):
   i+=z in on;j+=z not in on;path.append((i,j))
  def P(c,k):return C(c.deg,fun=lambda g:c(tuple(path[i][k] for i in g)),mod=c.mod)
  out+=diff5(P(n,0),P(u,0),P(m,1),P(v,1))(f)
 return out%2

def Lstar(S):
 n,u,m,v=(field(S,j) for j in (2,3,4,5));top=tuple(range(6))
 if S[0]!=5:raise ValueError(S[0])
 return (zero_Lold(n,u,m,v)(top)+sh_diff(2,3,n,u,m,v)+sh_diff(3,2,n,u,m,v))%2

@lru_cache(maxsize=10000)
def kernel(S):
 if S[0]!=6:raise ValueError(S[0])
 n,u,m,v,w=decode(S)
 if not any(S[1]):
  return (zero.residual(n,u,m,v)+diff5(n,u,m,v).d())(tuple(range(7)))
 ys=[]
 for x in (n,m,n+m):
  yy=binary_completion(x,w,C(1),vertices=7,accelerate=True);ys.append(yy)
 try:return repaired_residual(n,u,m,v,w,C(1),ys=ys)(tuple(range(7)))
 finally:
  for y in ys:
   if hasattr(y,'engine'):y.engine.close()

def cut_diff(n,u,m,v):
 def ev(f):
  out=0
  for g in zero_H(4):
   projections=([f[z[0]] for z in g],[f[z[1]] for z in g])
   def P(c,k):return C(c.deg,fun=lambda face:c(tuple(projections[k][i] for i in face)),mod=c.mod)
   out+=diff5(P(n,0),P(u,0),P(m,1),P(v,1))(tuple(range(6)))
  return out%2
 return C(4,fun=ev)

@lru_cache(maxsize=5000)
def Zstar0(S):
 n,u,m,v=(field(S,j) for j in (2,3,4,5));f=tuple(range(6))
 return (zero_Zold(n,u,m,v)+diff5(n,u,m,v)+cut_diff(n,u,m,v).d())(f)

def kernel222(S):
 n,u,m,v,w=decode(S);s=C(1);N,U,e=zero_NUe(n,u,m,v,w)
 y=binary_completion(N,w,s,vertices=7,accelerate=True)
 try:
  O=star_source16(N,U,e,w,s,binary_y=y)
  z=(O-seed16(n,u,m,v,w).d()).div(8).reduce(2)
  return z(tuple(range(7)))
 finally:
  if hasattr(y,'engine'):y.engine.close()

def zero_NUe(n,u,m,v,w):
 return n+m,u+v+cup(n.reduce(2),m.reduce(2),1),third_product(n,u,m,v,w,C(1))

def transfer222(x,y,verbose=False):
 st=__import__('time').time();chain=degree222(x,y);dchain=set()
 for S in chain:
  for T in delta(S):xor_add(dchain,T)
 if verbose:print('222',x,y,'sh',len(chain),'delta',len(dchain),'wzero',all(not any(T[1]) for T in dchain),flush=True)
 a=0
 for i,S in enumerate(chain):
  a^=kernel222(S)
  if verbose and i%10==0:print('kernel',i,a,'seconds',__import__('time').time()-st,flush=True)
 if verbose:print('ALL R_SH',a,flush=True)
 b=0
 for i,S in enumerate(dchain):
  b^=Zstar0(S)
  if verbose and i%10==0:print('zeroZ',i,b,'seconds',__import__('time').time()-st,flush=True)
 return {'x':x,'y':y,'shuffle':len(chain),'twist_boundary':len(dchain),'R_sh':a,'Z_delta_sh':b,'remaining':a^b,'seconds':__import__('time').time()-st}
