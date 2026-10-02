"""Explicit unitary omega2 loop-source and terminal product in 3+1D.
No s1 or 4+1D stacking operation is used.  Phase numerators are /16.
The terminal source is the displayed transgression of the fixed supplied d4.
"""
from pathlib import Path
import sys,itertools
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,parity,sq
from explicit_pip import binary_completion,full_terms16,sum_terms
from suspension import ez2_H
sys.path.insert(0,str(ROOT/'omega3'))
from prism import pull,param,theta,phi,chi,shuffles,integrate,pair_fields
def endpoint(n,u,w):
 """Two-term multiplication-normalized suspension correction."""
 a=n.reduce(2);h=(n-a.lift()).div(2).reduce(2)
 return cup(w,h)+cup(u,u.d(),2)
sys.path.insert(0,str(ROOT/'bosonic'))
from fractional import third_product


def lower_pair_gauge(n,u,m,v):
 """Four cups; transports the triangle parity product to the accepted E3."""
 a=n.reduce(2);b=m.reduce(2)
 h=(n-a.lift()).div(2).reduce(2);k=(m-b.lift()).div(2).reduce(2)
 t=cup(a,b)
 return cup(h,b)+cup(a+h,k)+cup(t,u+v,2)+t


def product_homotopy(Q):
 """Fixed normalized EZ homotopy of parameter simplex x base simplex."""
 H=ez2_H(Q.deg-1)
 return C(Q.deg-1,fun=lambda f:sum(Q(tuple((f[a][0],f[b][1]) for a,b in g)) for g in H),mod=2)


def fields_on_triangle(n,u,c,m,v,cp,w):
 NN,UU,ww=pair_fields(n,u,m,v,w);J=parity(NN,UU,ww,C(1))
 a=n.reduce(2);b=m.reduce(2);U=u+v+cup(a,b);N=n+m
 DX=endpoint(n,u,w);DY=endpoint(m,v,w);DN=endpoint(N,U,w)
 e=third_product(n,u,m,v,w,C(1));g=lower_pair_gauge(n,u,m,v)
 th=theta().reduce(2);ph=phi().reduce(2);ch=chi()
 CC=(product_homotopy(J)+cup(th,pull(c+DX))+cup(ph,pull(cp+DY))
    +cup(ch,pull(e+DN+DX+DY))+cup(ch.d(),pull(g)))
 return NN,UU,CC,ww


def fields_on_interval(n,u,c,w):
 th=theta().reduce(2);ni=pull(n);ui=pull(u);ww=pull(w);ai=ni.reduce(2)
 NN=cup(theta(),ni)
 UU=cup(th,ui)+cup(cup(ww,th,1),ai)
 J=parity(NN,UU,ww,C(1))
 CC=product_homotopy(J)+cup(th,pull(c+endpoint(n,u,w)))
 return NN,UU,CC,ww


from unitary_source import high_source16,high_blocks

def source16(n,u,c,w,*,accelerate=True,validate=False):
 return integrate(high_source16(*fields_on_interval(n,u,c,w),accelerate=accelerate,validate=validate),(0,1))

def product16(n,u,c,m,v,cp,w,*,accelerate=True,validate=False):
 return integrate(high_source16(*fields_on_triangle(n,u,c,m,v,cp,w),accelerate=accelerate,validate=validate),(0,1,2))

def source_parts16(n,u,c,w,*,accelerate=True,validate=False):
 H,Q,Pn,wnn=high_blocks(*fields_on_interval(n,u,c,w),accelerate=accelerate,validate=validate)
 P=cup(w.lift(),w.lift())+cup(w.lift(),w.lift().d(),1)
 return (integrate(H,(0,1)).lift().scaled(8),integrate(Q,(0,1)).scaled(4),cup(P,n))

def product_parts16(n,u,c,m,v,cp,w,*,accelerate=True,validate=False):
 H,Q,Pn,wnn=high_blocks(*fields_on_triangle(n,u,c,m,v,cp,w),accelerate=accelerate,validate=validate)
 return (integrate(H,(0,1,2)).lift().scaled(8),integrate(Q,(0,1,2)).scaled(4),cup(w.lift(),cup(n,m)).scaled(-2))
