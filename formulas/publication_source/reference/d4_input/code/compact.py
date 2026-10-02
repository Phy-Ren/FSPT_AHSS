"""Layer-adapted formulas equivalent to the independent reference candidates.

Every output is an integer numerator over 16; reduce modulo 16 on evaluation.
The only long public operations are the source-aware Majorana phase gamma16
and the pure integer-layer phase yhat16. Neither depends on the CF cochain.
"""
from __future__ import annotations
from typing import Callable
from cochains import (C,cup,sq,ds,mc_phase4,background_data,cartan_carry,
                      prism_transgression,pure_parity)

def kappa(u:C,omega2:C,s1:C)->C:
    return sq(u,2)+cup(s1,sq(u,1))+cup(omega2,u)

def beta_open(u:C)->C:
    """Integral cochain (d lift(u)-lift(du))/2, valid for nonclosed u."""
    return (u.lift().d()-u.d().lift()).div(2)

def ell(omega2:C,s1:C)->C:
    return omega2.lift().d().div(2).reduce(2)+cup(s1,omega2)

def signed_homotopy(operation:Callable[[C,C,C],C],u:C,omega2:C,s1:C)->C:
    """Fixed signed height-prism homotopy in the unrestricted input u.

    This does not suspend an integer decoration into the other spacetime
    dimension. It is a within-degree homotopy 0 -> u, with backgrounds fixed.
    """
    def pull(a):return C(a.deg,fun=lambda f:a(tuple(v//2 for v in f)),mod=a.mod)
    wI,sI=pull(omega2),pull(s1)
    uI=C(u.deg,fun=lambda f:(f[0]&1)*u(tuple(v//2 for v in f)),mod=u.mod)
    F=operation(uI,wI,sI)
    def value(face):
        return sum((-1)**j*F(tuple(2*v for v in face[:j+1])+tuple(2*v+1 for v in face[j:]))
                   for j in range(len(face)))
    return C(F.deg-1,fun=value,mod=F.mod)

def gamma_boundary16(u:C,omega2:C,s1:C)->C:
    """16[G(kappa u)+J(du)] using only the fixed CLOSED Majorana formula J."""
    A=u.d();P=kappa(u,omega2,s1)
    J4=mc_phase4(A,C(A.deg+1),omega2,s1)
    return (sq(P,2)+cup(omega2,P)).lift().scaled(8)+J4.scaled(4)

def gamma16(u:C,omega2:C,s1:C)->C:
    """Source-aware Majorana phase: H[G(kappa u)+J(du)]+(s1 kappa u)/2."""
    if u.mod!=2 or u.deg not in (2,3):raise ValueError('Expected a binary degree-2 or degree-3 cochain')
    if u.known_zero:return C(u.deg+3,mod=None)
    return signed_homotopy(gamma_boundary16,u,omega2,s1)+cup(s1,kappa(u,omega2,s1)).lift().scaled(8)

def gamma_seed16(u:C,omega2:C,s1:C)->C:
    """An explicit lift-coordinate primitive of the same boundary.

    gamma_seed16 - (gamma16-8*s1*kappa(u)) = d_s H(gamma_seed16), modulo 16.
    This auxiliary formula is used only for the exact dictionary.
    """
    p=u.deg-1;A=u.d();b=beta_open(u);l=ell(omega2,s1)
    T=prism_transgression(u,omega2,s1)+cup(u,l)
    quadratic=cup(b,b,p)+cup(b,b.d(),p+1)+cup(omega2.lift(),b)
    theta=cup(omega2.lift(),A.lift()).scaled(4)+cup(A,l,1).lift().scaled(8)
    return T.lift().scaled(8)+quadratic.scaled(4)-theta

def integer_inputs(n:C,omega2:C,s1:C):
    p=n.deg;a=n.reduce(2);a.closed=True
    W,v,alpha,hv,P=background_data(omega2,s1)
    A=sq(a,2)+cup(W,a)
    Nsquare=cup(n,n,p-2,s=s1,twists=(1,1))
    L=Nsquare+cup(W.lift(),n,s=s1,twists=(1,1))
    k=(A.lift()-L).div(2)
    betaA=A.lift().d().div(2)
    grav=cup(P,n,s=s1,twists=(0,1))+cup(W.lift(),Nsquare,s=s1,twists=(1,0)).scaled(2)
    return A,k,betaA,grav

def yhat16(n:C,omega2:C,s1:C,*,binary_y:C|None=None)->C:
    """Pure p+ip phase, independent of Majorana and CF decorations.

    binary_y may supply an equivalent fixed binary primitive with an explicit
    rephasing certificate. It is not a free cocycle or an unknown to be solved.
    """
    p=n.deg
    if p not in (1,2) or n.mod is not None:raise ValueError('Expected n1 or n2 with integer coefficients')
    if n.known_zero and (binary_y is None or binary_y.known_zero):return C(p+4,mod=None)
    if binary_y is None:
        from polynomial_tables import binary_completion
        binary_y=binary_completion(n,omega2,s1)
    A,k,betaA,grav=integer_inputs(n,omega2,s1)
    kb=k.reduce(2);t=betaA.reduce(2);Xi=pure_parity(n,omega2,s1)
    Cbin=cartan_carry(n,omega2,s1)
    half=(binary_y+cup(t,kb,p+1)+cup(s1,cup(t,kb,p+2))
          +cup(A,ell(omega2,s1),1)+cup(Xi,Xi,p+2))
    quarter=(cup(k,k,p)+cup(k,k.d(),p+1)+cup(omega2.lift(),k)
             +cup(betaA,k.d(),p+2).scaled((-1)**p)-Cbin.lift()
             +cup(omega2.lift(),A.lift()))
    return half.lift().scaled(8)+quarter.scaled(4)+grav+cup(s1,Xi).lift().scaled(8)

def compact_phase16(n:C,nmajorana:C,nfermion:C,omega2:C,s1:C,*,binary_y:C|None=None)->C:
    p=n.deg
    if (p,nmajorana.deg,nfermion.deg) not in ((1,2,3),(2,3,4)):
        raise ValueError('Expected the 3+1D or 4+1D decoration degrees')
    h=(n-n.reduce(2).lift()).div(2).reduce(2)
    u=nmajorana+cup(s1,h)
    Xi=pure_parity(n,omega2,s1)
    half=sq(nfermion,2)+cup(omega2,nfermion)+cup(nfermion.d(),Xi,p+2)
    return half.lift().scaled(8)+gamma16(u,omega2,s1)+yhat16(n,omega2,s1,binary_y=binary_y)

def rephasing16(n:C,nmajorana:C,nfermion:C,omega2:C,s1:C)->C:
    """Reference phase = compact phase + d_s(this), modulo 16.

    Both sides use the same binary_y representative. A separate total-complex
    compression changes that representative by an explicitly recorded exact term.
    """
    p=n.deg;h=(n-n.reduce(2).lift()).div(2).reduce(2)
    u=nmajorana+cup(s1,h);b=beta_open(u)
    A,k,betaA,_=integer_inputs(n,omega2,s1)
    L=(cup(b,k,p+1).scaled((-1)**p)+cup(betaA,k,p+2)).scaled(4)
    return L+signed_homotopy(gamma_seed16,u,omega2,s1)+cup(s1,nfermion).lift().scaled(8)


def readable_residual(n:C,omega2:C,s1:C)->C:
    """The pure binary residual without the previous auxiliary alphabet.

    Evaluate the fixed rational phase seed with its table term omitted,
    add the two known descent contributions, divide by eight exactly.
    No Y5/Y6 evaluation or coboundary solve occurs here.
    """
    p=n.deg;Xi=pure_parity(n,omega2,s1);A,_,_,_=integer_inputs(n,omega2,s1)
    seed=yhat16(n,omega2,s1,binary_y=C(p+4))
    J4=mc_phase4(A,C(A.deg+1),omega2,s1)
    half=sq(Xi,2)+cup(omega2,Xi)+cup(s1,Xi.d())
    numerator=ds(seed,s1)+half.lift().scaled(8)+J4.scaled(4)
    return numerator.div(8).reduce(2)


def reference_rephasing16(n:C,nmajorana:C,nfermion:C,omega2:C,s1:C)->C:
    """Old 2638-term reference = compact 960-term phase + d_s(this)."""
    from polynomial_tables import compression_rephasing
    return rephasing16(n,nmajorana,nfermion,omega2,s1)+compression_rephasing(n,omega2,s1).lift().scaled(8)

def O5(n1:C,n2:C,n3:C,omega2:C,s1:C)->C:
    """Numerator of the independent 3+1D phase; divide by 16 modulo one."""
    if n1.deg!=1:raise ValueError('O5 requires n1 as the integral input')
    return compact_phase16(n1,n2,n3,omega2,s1)

def O6(n2:C,n3:C,n4:C,omega2:C,s1:C,*,vertices:int|None=None,accelerate:bool=False)->C:
    """Numerator of the independent 4+1D phase; divide by 16 modulo one."""
    if n2.deg!=2:raise ValueError('O6 requires n2 as the integral input')
    if accelerate:
        from polynomial_tables import accelerated_binary_completion
        if vertices is None or vertices<7:raise ValueError('Supply at least seven consecutive vertex labels for acceleration')
        y=accelerated_binary_completion(n2,omega2,s1,vertices)
        out=compact_phase16(n2,n3,n4,omega2,s1,binary_y=y);out.Y6=y
        return out
    return compact_phase16(n2,n3,n4,omega2,s1)
