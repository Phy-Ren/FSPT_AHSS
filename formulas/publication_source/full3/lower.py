"""Three-dimensional lower tower and parameter lifts with both backgrounds.
The Majorana argument in the internal functions is the shifted cochain.
"""
from pathlib import Path
import sys,itertools
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,sq,ds,parity,primitive,op
sys.path.insert(0,str(ROOT/'bosonic'))
from fractional import third_product
sys.path.insert(0,str(ROOT/'omega3'))
from prism import pull,theta,phi,chi,shuffles,integrate
from suspension import ez2_H

def carry(n):return (n-n.reduce(2).lift()).div(2).reduce(2)
def shifted_parity(n,u,w,s):return parity(n,u+cup(s,carry(n)),w,s)
def lower_product(n,u,m,v,w,s):
 a=n.reduce(2);b=m.reduce(2);t=cup(a,b)
 return n+m,u+v+t,third_product(n,u,m,v,w,s)

def pair_fields(n,u,m,v,w,s):
 th=theta();ph=phi();tb=th.reduce(2);pb=ph.reduce(2);ch=chi()
 ni=pull(n);mi=pull(m);ui=pull(u);vi=pull(v);wi=pull(w);si=pull(s)
 W=wi+cup(si,si);a=ni.reduce(2);b=mi.reduce(2)
 NN=cup(th,ni,s=si,twists=(0,1))+cup(ph,mi,s=si,twists=(0,1))
 UU=(cup(tb,ui)+cup(pb,vi)+cup(cup(W,tb,1),a)+cup(cup(W,pb,1),b)
     +cup(ch,cup(a,b))+cup(cup(tb,cup(a,pb,1)),b))
 return NN,UU,wi,si

def interval_fields(n,u,w,s):
 th=theta();tb=th.reduce(2);ni=pull(n);ui=pull(u);wi=pull(w);si=pull(s)
 W=wi+cup(si,si);a=ni.reduce(2)
 return cup(th,ni,s=si,twists=(0,1)),cup(tb,ui)+cup(cup(W,tb,1),a),wi,si

def endpoint0(n,u,w,s):return cup(w+cup(s,s),carry(n))+cup(u,u.d(),2)
def gauge0(n,u,m,v,w,s):
 a=n.reduce(2);b=m.reduce(2);h=carry(n);k=carry(m);t=cup(a,b)
 return cup(h,b)+cup(a+h,k)+cup(t,u+v,2)+t

def endpoint(n,u,w,s):
 """Three-term suspension correction in shifted Majorana coordinates."""
 return endpoint0(n,u,w,s)+cup(cup(s,w,1),n.reduce(2))

def lower_pair_gauge(n,u,m,v,w,s):
 """Six grouped cups, fixing the native fermion coordinate on the output edge."""
 a=n.reduce(2);b=m.reduce(2);q=cup(a,b,1)
 return gauge0(n,u,m,v,w,s)+cup(cup(s,a,1),q)+cup(cup(s,q,1),a+b)

def product_homotopy(Q):
 H=ez2_H(Q.deg-1)
 return C(Q.deg-1,fun=lambda f:sum(Q(tuple((f[a][0],f[b][1]) for a,b in g)) for g in H),mod=2)

def fields_on_triangle(n,u,c,m,v,cp,w,s):
 NN,UU,ww,ss=pair_fields(n,u,m,v,w,s);J=shifted_parity(NN,UU,ww,ss)
 N,U,e=lower_product(n,u,m,v,w,s)
 DX=endpoint(n,u,w,s);DY=endpoint(m,v,w,s);DN=endpoint(N,U,w,s)
 g=lower_pair_gauge(n,u,m,v,w,s)
 th=theta().reduce(2);ph=phi().reduce(2);ch=chi()
 CC=(product_homotopy(J)+cup(th,pull(c+DX))+cup(ph,pull(cp+DY))
     +cup(ch,pull(e+DN+DX+DY))+cup(ch.d(),pull(g)))
 return NN,UU,CC,ww,ss

def fields_on_interval(n,u,c,w,s):
 NN,UU,ww,ss=interval_fields(n,u,w,s);J=shifted_parity(NN,UU,ww,ss)
 CC=product_homotopy(J)+cup(theta().reduce(2),pull(c+endpoint(n,u,w,s)))
 return NN,UU,CC,ww,ss
