"""Explicit quarter-cubic repair and a short source-coordinate dictionary.
All phases are integer numerators over sixteen. This module does not assert
that its fractional seeds are the completed terminal products.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'bosonic'))
from fractional import *

def cube(n,s):
    if n.deg!=2:return C(n.deg+4,mod=None)
    return cup(cup(n,n,s=s,twists=(1,1)),n,s=s,twists=(0,1))

def cubic_coordinate16(n,u,w,s):
    """16 Psi_5, zero in p=1.  Ostar = Oraw + cube/4 + d(Lambda-Psi)."""
    if n.deg==1:return C(4,mod=None)
    W=w+cup(s,s)
    return (cup(n,u.lift(),s=s,twists=(1,0))
          +cup(cup(n,W.lift(),1,s=s,twists=(1,1)),n,s=s,twists=(0,1))).scaled(4)

def binary_correction(n,u,w,s):
    if n.deg==1:return C(5)
    B=relative_B(n,u,w,s);W,vi,alpha,hv,P=background_data(w,s)
    a=n.reduce(2)
    return cup(a,B.reduce(2))+cup(cup(a,alpha,1),a)

def star_source16(n,u,c,w,s,*,binary_y=None,vertices=None,accelerate=False):
    """The complete supplied source with +n2^3/4, in the short B-star coordinate.
    This is an explicitly closed candidate, not a claim of full multiplicativity.
    """
    from explicit_pip import binary_completion
    p=n.deg
    if binary_y is None:
        binary_y=binary_completion(n,w,s,vertices=vertices,accelerate=accelerate)
    H=binary_H(n,u,w,s,binary_y)+binary_correction(n,u,w,s)
    B=relative_B(n,u,w,s);W,vi,alpha,hv,P=background_data(w,s)
    square=cup(n,n,p-2,s=s,twists=(1,1))
    return ((sq(c,2)+cup(w,c)+H).lift().scaled(8)
      +(cup(B,B,p)+cup(B,B.d(),p+1)+cup(w.lift(),B)-cartan_word(n,w,s).lift()).scaled(4)
      +cup(P,n,s=s,twists=(0,1))
      -cup(W.lift(),square,s=s,twists=(1,0)).scaled(2))

def star_fractional_seed16(n,u,np,v,w,s,c=None,cp=None):
    D=pair_data(n,u,np,v,w,s);W=w+cup(s,s)
    out=fractional_seed16(n,u,np,v,w,s,native=False)
    if n.deg==2:out=out-cup(W.lift(),D['T'],s=s,twists=(1,0)).scaled(4)
    if c is not None:
        out=out+upper_seed16(c,cp,third_product(n,u,np,v,w,s))
    return out

def repaired_residual(n,u,np,v,w,s,*,ys=None,vertices=None,accelerate=False):
    R,I=terminal_residual(n,u,np,v,w,s,ys=ys,vertices=vertices,accelerate=accelerate)
    if n.deg==1:return R
    D=pair_data(n,u,np,v,w,s);W,vi,alpha,hv,P=background_data(w,s)
    change=(binary_correction(D['N'],D['U'],w,s)+binary_correction(n,u,w,s)
          +binary_correction(np,v,w,s)+cup(W,D['R'].reduce(2))+cup(alpha,D['t']))
    return R+change
