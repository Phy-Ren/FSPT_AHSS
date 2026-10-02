from pathlib import Path
import sys,itertools,json,time
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'joint'))
from symbolic_lazy import *
sys.path.insert(0,str(ROOT/'omega3'))
from prism import *

def bits_data(dim):
 n,o,_=integer_bar_cochain(1,dim,0,bits=2)
 m,o,_=integer_bar_cochain(1,dim,o,bits=2)
 def cochain_z2(q,o):
  values={};anchor={}
  for f in itertools.combinations(range(1,dim+1),q):anchor[(0,)+f]=Bit.var(o);o+=1
  def val(f):
   if f[0]==0:return anchor[f]
   return sum(anchor[(0,)+f[:j]+f[j+1:]] for j in range(q+1))
  out=C(q,fun=val);out.closed=True;return out,o
 w,o=cochain_z2(2,o)
 def upper(nn,o):
  z,o=cochain_z2(2,o)
  return primitive(cup(w,nn.reduce(2)))+z,o
 u,o=upper(n,o);v,o=upper(m,o)
 return (n,u,m,v,w),o

def endpoint(n,u,w):
 a=n.reduce(2)
 def value(f):
  i,j,k,l=f
  return ((a((i,j))+a((i,k)))*(u((i,j,k))+u((i,j,l)))
    +w((i,j,k))*(a((i,k))+a((i,l)))*(u((i,j,k))+u((i,k,l))))
 h=(n-a.lift()).div(2).reduce(2)
 return C(3,fun=value)+cup(a,u)+cup(w,h)+cup(cup(w,a,1),a)

def ediff(fields):
 n,u,m,v,w=fields;NN,UU,wi=pair_fields(*fields);J=parity(NN,UU,wi,C(1))
 U=u+v+cup(n.reduce(2),m.reduce(2));N=n+m
 out=integrate(J,(0,1,2))+endpoint(n,u,w)+endpoint(m,v,w)+endpoint(N,U,w)+third_product(n,u,m,v,w,C(1))
 return out

def features(fields,face):
 n,u,m,v,w=fields;i,j,k=face
 return [n((i,j))%2,n((j,k))%2,(n((i,j))//2)%2,(n((j,k))//2)%2,
         m((i,j))%2,m((j,k))%2,(m((i,j))//2)%2,(m((j,k))//2)%2,
         w(face),u(face),v(face)]

def mono(fs,mm):
 out=Bit.cast(1)
 for j in range(len(fs)):
  if mm>>j&1:out=out*fs[j]
 return out

if __name__=='__main__':
 st=time.time();fs,nb=bits_data(3);top=tuple(range(4));target=ediff(fs)(top)
 print('bits',nb,'terms',len(target.t),flush=True)
 terms={};basis={}
 def vec(poly):
  o=0
  for m in poly.t:
   if m not in terms:terms[m]=len(terms)
   o^=1<<terms[m]
  return o
 rhs=vec(target);sol=0
 F=[features(fs,top[:i]+top[i+1:]) for i in range(4)]
 masks=list(range(1,1<<11));masks.sort(key=lambda m:(m.bit_count(),m))
 used=[]
 for mm in masks:
  # vacuum axes: first factors 0..3,9; second 4..7,10.
  if not(mm&((15)|(1<<9))) or not(mm&((15<<4)|(1<<10))):continue
  if not (mm&(7<<8)):
   if not mm&((1<<0)|(1<<2)|(1<<4)|(1<<6)) or not mm&((1<<1)|(1<<3)|(1<<5)|(1<<7)):continue
  poly=sum(mono(f,mm) for f in F);col=vec(poly);wit=1<<len(used);used.append(mm)
  while col:
   i=col.bit_length()-1
   if i not in basis:basis[i]=(col,wit);break
   a,b=basis[i];col^=a;wit^=b
  while rhs:
   i=rhs.bit_length()-1
   if i not in basis:break
   a,b=basis[i];rhs^=a;sol^=b
  if not rhs:break
 print('rank',len(basis),'cols',len(used),'unsolved',rhs.bit_count(),'seconds',time.time()-st,flush=True)
 if not rhs:
  ans=[used[j] for j in range(len(used)) if sol>>j&1]
  names=['a01','a12','h01','h12','b01','b12','k01','k12','w012','u012','v012']
  print('solution',ans,flush=True)
  for mm in ans:print('*'.join(names[j] for j in range(11) if mm>>j&1))
  C2=C(2,fun=lambda f:sum(mono(features(fs,f),mm) for mm in ans))
  assert not(C2.d()(top)+target).t
  Path(__file__).with_name('results').joinpath('loop_lower_dictionary.json').write_text(json.dumps({'bits':nb,'monomials':ans,'features':names,'seconds':time.time()-st},indent=2))
 fs,nb=bits_data(4);n,u,m,v,w=fs;NN,UU,wi=pair_fields(*fs);J=parity(NN,UU,wi,C(1));top=tuple(range(5))
 res=(integrate(J,(0,1))+parity(n,u,w,C(1))+endpoint(n,u,w).d())(top)
 print('endpoint exact',not res.t,'remaining',len(res.t),'bits',nb,'seconds',time.time()-st,flush=True)
 assert not res.t
