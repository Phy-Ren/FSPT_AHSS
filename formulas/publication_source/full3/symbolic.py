"""Exact independent digits for twisted lower cochains on one simplex."""
from pathlib import Path
import sys,itertools
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'joint'))
from symbolic_lazy import *
sys.path.insert(0,str(ROOT/'full3'))
from lower import *

def bits_data(dim,*,pair=True,mode='both'):
 off=0
 def cochain_z2(q):
  nonlocal off
  anchor={}
  for f in itertools.combinations(range(1,dim+1),q):anchor[(0,)+f]=Bit.var(off);off+=1
  def val(f):
   if f[0]==0:return anchor[f]
   return sum(anchor[(0,)+f[:j]+f[j+1:]] for j in range(q+1))
  out=C(q,fun=val);out.closed=True;return out
 s=cochain_z2(1) if mode!='omega' else C(1)
 w=cochain_z2(2) if mode!='s' else C(2)
 W=w+cup(s,s)
 def one():
  nonlocal off
  edges=[]
  for i in range(dim):
   edges.append(Z({1<<off:1,1<<(off+1):2},PREC));off+=2
  def nn(f):
   i,j=f
   return sum(((-1)**s((i,k)))*edges[k] for k in range(i,j))
  n=C(1,fun=nn,mod=None)
  a=n.reduce(2)
  u=primitive(cup(W,a))+cochain_z2(2)
  return n,u
 n,u=one()
 if pair:
  m,v=one();return (n,u,m,v,w,s),off
 return (n,u,w,s),off

if __name__=='__main__':
 import time,json
 deriv=ROOT/'full3/derivation/results';deriv.mkdir(exist_ok=True)
 st=time.time()
 for mode in ['omega','s','both']:
  (n,u,w,s),nb=bits_data(4,pair=False,mode=mode)
  ni,ui,wi,si=interval_fields(n,u,w,s);F=shifted_parity(ni,ui,wi,si)
  target=(integrate(F,(0,1))+shifted_parity(n,u,w,s)+endpoint0(n,u,w,s).d())(tuple(range(5)))
  print(mode,'interval bits',nb,'remainder',len(target.t),'sec',time.time()-st,flush=True)
  out={str(mm):1 for mm in target.t}
  (deriv/('interval_res_'+mode+'.json')).write_text(json.dumps(out))
  fs,nb=bits_data(3,mode=mode);n,u,m,v,w,s=fs
  ni,ui,wi,si=pair_fields(*fs);F=shifted_parity(ni,ui,wi,si)
  N,U,e=lower_product(*fs)
  target=(integrate(F,(0,1,2))+e+endpoint0(N,U,w,s)+endpoint0(n,u,w,s)+endpoint0(m,v,w,s)+gauge0(*fs).d())(tuple(range(4)))
  print(mode,'triangle bits',nb,'remainder',len(target.t),'sec',time.time()-st,flush=True)
  (deriv/('triangle_res_'+mode+'.json')).write_text(json.dumps({str(mm):1 for mm in target.t}))
