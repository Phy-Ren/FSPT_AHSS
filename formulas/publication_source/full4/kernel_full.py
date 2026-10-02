"""Full-background binary terminal kernel and the explicit nonbinary phase.

This module defines the closed construction kernel and the proved fractional
assembly. The complete binary primitive is implemented in product_full.py.
"""
from graded_full import *
from fractional import pair_data,fractional_seed16,binary_H,upper_residual,third_product,upper_seed16,relative_B
from cubic_repair import repaired_residual,star_fractional_seed16,star_source16,cubic_coordinate16,binary_correction,cube
from cochains import pure_parity,background_data,sq,op
from explicit_pip import binary_completion,cartan_word
from compact import kappa
import transfer_model as unt
import hashlib,pickle,atexit,os
TOP=tuple(range(7));ACCELERATE=True
CACHE_PATH=Path(os.environ.get('FULL4_CACHE_PATH',str(ROOT/'full4/results/source_cache.pickle')))
try:
 with CACHE_PATH.open('rb') as f:STORE=pickle.load(f)
except FileNotFoundError:STORE={}
def save_cache():
 tmp=CACHE_PATH.with_suffix('.tmp')
 with tmp.open('wb') as f:pickle.dump(STORE,f,pickle.HIGHEST_PROTOCOL)
 tmp.replace(CACHE_PATH)
atexit.register(save_cache)

def onekey(n,u,w,s):
 return tuple(tuple(x(f) for f in faces(6,x.deg)) for x in (n,u,w,s))
def source_degenerate(xs):
 originals=tuple(tuple(x(f) for f in faces(6,x.deg)) for x in xs)
 for i in range(6):
  ff=tuple(j for j in range(7) if j!=i+1)
  proj=tuple(ff[j if j<=i else j-1] for j in range(7))
  if all(tuple(x(tuple(proj[z] for z in f)) for f in faces(6,x.deg))==vv for x,vv in zip(xs,originals)):return True
 return False

def Yvalue(nn,ww,ss):
 key=('Y',nn,ww,ss)
 if key in STORE:return STORE[key]
 n=C(2,values=dict(zip(faces(6,2),nn)),mod=None);w=C(2,values=dict(zip(faces(6,2),ww)));s=C(1,values=dict(zip(faces(6,1),ss)))
 w.closed=s.closed=True
 # Do not mark a twisted integral cocycle ordinary-closed.
 if not any(ss):n.closed=True
 if source_degenerate((n,w,s)):value=0
 else:
  yy=binary_completion(n,w,s,vertices=7,accelerate=ACCELERATE)
  try:value=yy(TOP)
  finally:
   if hasattr(yy,'engine'):yy.engine.close()
 STORE[key]=value;return value

def Hvalue(key):
 kk=('H',key)
 if kk in STORE:return STORE[kk]
 nn,uu,ww,ss=key
 n=C(2,values=dict(zip(faces(6,2),nn)),mod=None);u=C(3,values=dict(zip(faces(6,3),uu)))
 w=C(2,values=dict(zip(faces(6,2),ww)));s=C(1,values=dict(zip(faces(6,1),ss)));w.closed=s.closed=True
 if not any(ss):n.closed=True
 if source_degenerate((n,u,w,s)):value=0
 else:
  yy=C(6,values={TOP:Yvalue(nn,ww,ss)})
  value=binary_H(n,u,w,s,yy)(TOP)
 STORE[kk]=value;return value

@lru_cache(maxsize=20000)
def rho(S):
 """Repaired star-kernel including the closed fermion ab branch."""
 if S[0]!=6:raise ValueError(S[0])
 if not normalized(S):return 0
 if not any(S[1]):
  import kernel_cached
  old=(S[0],)+S[2:]
  # unitary slots: w,n,u0,m,v0, exactly the remaining entries
  return kernel_cached.rho_compatible(old)
 n,u,m,v,w,s=decode(S);D=pair_data(n,u,m,v,w,s);N,U=D['N'],D['U'];B,Bp,BN=D['B'],D['Bp'],D['BN']
 W,vi,alpha,hv,P=background_data(w,s)
 ef=fractional_seed16(n,u,m,v,w,s,native=False)
 V=(ef-cup(W.lift(),D['T'],s=s,twists=(1,0)).scaled(2)).div(4).reduce(2)
 Q=lambda x:cup(x,x,2)+cup(x,x.d(),3)
 I=(Q(BN)-Q(B)-Q(Bp)+cup(w.lift(),D['lambda'].d()-D['R'])
    -cartan_word(N,w,s).lift()+cartan_word(n,w,s).lift()+cartan_word(m,w,s).lift()
    +cup(W.lift(),D['R'],s=s,twists=(1,0))-cup(vi,D['T'],s=s,twists=(1,0))-ds(V.lift(),s))
 HH=Hvalue(onekey(N,U,w,s))^Hvalue(onekey(n,u,w,s))^Hvalue(onekey(m,v,w,s))
 F=kappa(u,w,s)+pure_parity(n,w,s);Fp=kappa(v,w,s)+pure_parity(m,w,s);e=third_product(n,u,m,v,w,s)
 change=(binary_correction(N,U,w,s)+binary_correction(n,u,w,s)+binary_correction(m,v,w,s)
         +cup(W,D['R'].reduce(2))+cup(alpha,D['t'])+cup(W,cup(n.reduce(2),m.reduce(2))))
 return (upper_residual(F,Fp,e,w)(TOP)+HH+I.div(2).reduce(2)(TOP)+change(TOP))%2

def P5(n,u,m,v,w,s):
 a=n.reduce(2);b=m.reduce(2);h=(n-a.lift()).div(2).reduce(2);k=(m-b.lift()).div(2).reduce(2);W=w+cup(s,s)
 return (op('1231343',a,a,b,b)+cup(u,b)+cup(a,v)+cup(h,cup(b,b,1))
    +cup(cup(W,a,1),b)+cup(cup(s,a),k)+cup(cup(s,cup(a,s,1)),b))

def Lzero(S):
 """The fixed zero-background tensor cochain evaluated by front/back AW."""
 if S[0]!=5:raise ValueError(S[0])
 # The background-degree-zero piece uses all fiber data; no decoding.
 old=(5,(0,)*len(S[2]))+S[3:]
 return unt.Lstar(old)

def Zzero(S):
 if S[0]!=5 or any(S[1]) or any(S[2]):raise ValueError('not a zero-background five-simplex')
 return unt.Zstar0((5,)+S[2:])

def phase_seed48(n,u,c,m,v,cp,w,s):
 """All terms except the new binary background transfer. Denominator 48."""
 N=n+m;U=u+v+cup(n.reduce(2),m.reduce(2),1);e=third_product(n,u,m,v,w,s)
 z=cup(n.reduce(2),m.reduce(2));cold=c+cp+e
 up=upper_seed16(c,cp,e);frac=star_fractional_seed16(n,u,m,v,w,s)
 shift=cup(cold,z,3)+cup(cold.d(),z,4)+P5(n,u,m,v,w,s)
 def G(nn,uu):return cup(uu,nn.reduce(2)).lift().scaled(8)+cubic_coordinate16(nn,uu,w,s)
 nq=cup(n,m,1,s=s,twists=(1,1))
 cub=(cup(m-n,nq,s=s,twists=(1,0))-cup(nq,m-n,s=s,twists=(0,1))).scaled(16)
 W=w+cup(s,s);wt=cup(W,cup(n.reduce(2),m.reduce(2),1)).lift().scaled(24)
 return ((up+frac).scaled(3)+shift.lift().scaled(24)+cub+(G(N,U)-G(n,u)-G(m,v)).scaled(3)+wt)

def source48(n,u,c,w,s):
 D=onekey(n,u,w,s);yy=C(6,values={TOP:Yvalue(D[0],D[2],D[3])})
 o=star_source16(n,u,c,w,s,binary_y=yy)
 G=cup(u,n.reduce(2)).lift().scaled(8)+cubic_coordinate16(n,u,w,s)
 a=n.reduce(2);W=w+cup(s,s)
 return o.scaled(3)+cube(n,s).scaled(16)+ds(G,s).scaled(3)+cup(W,cup(a,a)).lift().scaled(24)
