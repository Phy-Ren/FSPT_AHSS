"""Normalized parameter products, signed shuffle integration, and valid test data."""
from pathlib import Path
import sys,itertools,random,time,json
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,parity,primitive,random_cochain,op

sys.path.insert(0,str(ROOT/'bosonic'))
from fractional import third_product

def pull(z):return C(z.deg,fun=lambda f:z(tuple(v[1] for v in f)),mod=z.mod)
def param(z):return C(z.deg,fun=lambda f:z(tuple(v[0] for v in f)),mod=z.mod)
def theta():return param(C(1,values={(0,1):1,(0,2):1},mod=None))
def phi():return param(C(1,values={(1,2):1,(0,2):1},mod=None))
def chi():return param(C(1,values={(0,2):1}))
def pair_fields(n,u,m,v,w):
 th=theta();ph=phi();tb=th.reduce(2);pb=ph.reduce(2);ch=chi()
 ni=pull(n);mi=pull(m);ui=pull(u);vi=pull(v);wi=pull(w)
 a=ni.reduce(2);b=mi.reduce(2)
 NN=cup(th,ni)+cup(ph,mi)
 UU=(cup(tb,ui)+cup(pb,vi)+cup(cup(wi,tb,1),a)+cup(cup(wi,pb,1),b)
     +cup(ch,cup(a,b))+cup(cup(tb,cup(a,pb,1)),b))
 return NN,UU,wi

def shuffles(paramface,baseface):
 r=len(paramface)-1;d=len(baseface)-1
 for Is in itertools.combinations(range(r+d),r):
  Is=set(Is);i=j=0;path=[(paramface[0],baseface[0])];ex=0
  for k in range(r+d):
   if k in Is:i+=1;ex+=j
   else:j+=1
   path.append((paramface[i],baseface[j]))
  yield tuple(path),(-1)**ex

def integrate(Q,paramface):
 d=Q.deg-len(paramface)+1
 return C(d,fun=lambda f:sum(s*Q(g) for g,s in shuffles(paramface,f)),mod=Q.mod)

def make(dim,seed):
 random.seed(seed);w=random_cochain(1,dim).d()
 def one():
  nn=C(0,values={(j,):random.randrange(-9,10) for j in range(dim+1)},mod=None).d()
  uu=primitive(cup(w,nn.reduce(2)))+random_cochain(1,dim).d()
  return nn,uu
 n,u=one();m,v=one();return n,u,m,v,w

