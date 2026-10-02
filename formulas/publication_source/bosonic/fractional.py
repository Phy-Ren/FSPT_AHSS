"""Proved fractional reduction of the terminal p+ip stacking equation.

NOT a complete stacking rule: the remaining half-valued cochain must still be
integrated, with the accepted Majorana restriction and multiplicative coherence.
All returned phase cochains are exact integer numerators over sixteen.
Use the bundled d4 reference cochain engine, in a separate Python process.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'reference/d4_input/code'))
from cochains import C,cup,sq,ds,op,background_data,primitive,random_cochain
from compact import beta_open,integer_inputs,kappa,ell
from explicit_pip import cartan_word,seed16,gamma_terms16,sum_cochains


def relative_B(n,u,w,s):
    p=n.deg
    W= w+cup(s,s)
    L=cup(n,n,p-2,s=s,twists=(1,1))+cup(W.lift(),n,s=s,twists=(1,1))
    return (u.lift().d()-L).div(2)


def state_rephasing16(n,u,w,s):
    p=n.deg
    _,K,_,_=integer_inputs(n,w,s)
    return cup(beta_open(u),K,p+1).scaled(4*((-1)**p))


def cartan_polarization_homotopy(alpha,a,b):
    if a.deg==1:return C(4)
    if a.deg!=2:raise ValueError('Only p=1,2 are established')
    # The sole interval cut is alpha(0123)^2 a(345)b(345).
    return cup(alpha,cup(a,b,2))


def unstable_square_primitive(n,u,np,v,w,s):
    p=n.deg
    if p==1:return C(4)
    if p!=2:raise ValueError('Only p=1,2 are established')
    a=n.reduce(2);b=np.reduce(2)
    h=(n-a.lift()).div(2).reduce(2);hp=(np-b.lift()).div(2).reduce(2)
    W=w+cup(s,s);r=cup(a,a,1)
    return (op('1231343',b,b,a,a)+cup(v,a)+cup(b,u)
          +cup(cup(W,b,1),a)+cup(hp,r)+cup(cup(s,b),h)
          +cup(cup(s,cup(b,s,1)),a))


def pair_data(n,u,np,v,w,s):
    p=n.deg
    if p not in (1,2) or np.deg!=p or u.deg!=p+1 or v.deg!=p+1:
        raise ValueError('Expected integer p, shifted Majorana p+1, p=1 or 2')
    a=n.reduce(2);b=np.reduce(2)
    t=cup(a,b,p-1);overlap=cup(a,b,p)
    N=n+np;U=u+v+t
    T=cup(n,np,p-1,s=s,twists=(1,1)).scaled((-1)**(p+1))
    R=cup(np,n,p-2,s=s,twists=(1,1))
    lam=(U.lift()-u.lift()-v.lift()-T).div(2)
    B=relative_B(n,u,w,s);Bp=relative_B(np,v,w,s);BN=relative_B(N,U,w,s)
    return {'N':N,'U':U,'t':t,'overlap':overlap,'T':T,'R':R,
            'lambda':lam,'B':B,'Bp':Bp,'BN':BN}


def fractional_seed16(n,u,np,v,w,s,*,native=True):
    """An explicit primitive only modulo half-valued cochains.

    native=True includes the exact rephasing back to the supplied d4 source.
    No source y-table is evaluated by this function. The remaining binary
    obstruction is not asserted to vanish or to have a binary primitive.
    """
    p=n.deg;m=p+2;D=pair_data(n,u,np,v,w,s)
    B=D['B'].reduce(2);Bp=D['Bp'].reduce(2);la=D['lambda'].reduce(2)
    r=D['R'].reduce(2);dlt=la.d()+r
    W,vi,alpha,hv,_=background_data(w,s)
    binary=(cup(B,Bp,m-1)+cup(B.d(),Bp,m)
           +cup(B+Bp,dlt,m-1)+cup(B.d()+Bp.d(),dlt,m)
           +sq(la,2)+cup(r,la.d(),m-1)+cup(w,la)
           +cup(hv,D['overlap'])
           +cartan_polarization_homotopy(alpha,n.reduce(2),np.reduce(2))
           +unstable_square_primitive(n,u,np,v,w,s))
    out=cup(W.lift(),D['T'],s=s,twists=(1,0)).scaled(2)+binary.lift().scaled(4)
    if native:
        out=out-state_rephasing16(D['N'],D['U'],w,s)+state_rephasing16(n,u,w,s)+state_rephasing16(np,v,w,s)
    return out


def fractional_source16(n,u,w,s):
    """Exactly the non-half-valued terms of the supplied obstruction."""
    p=n.deg
    gt=gamma_terms16(u,w,s)
    return (sum_cochains([gt[k] for k in gt if k.startswith('Majorana_open')],p+4)
            +seed16(n,w,s))


def combined_source_fraction16(n,u,w,s):
    """The simplified B-coordinate source, omitting its half-valued bracket."""
    p=n.deg;B=relative_B(n,u,w,s);W,vi,alpha,hv,P=background_data(w,s)
    return ((cup(B,B,p)+cup(B,B.d(),p+1)+cup(w.lift(),B)-cartan_word(n,w,s).lift()).scaled(4)
         +cup(P,n,s=s,twists=(0,1))
         +cup(W.lift(),cup(n,n,p-2,s=s,twists=(1,1)),s=s,twists=(1,0)).scaled(2))


def upper_seed16(c,cp,e):
    m=c.deg
    return (cup(c,cp,m-1)+cup(c.d(),cp,m)+cup(c+cp,e,m-1)).lift().scaled(8)


def upper_residual(c_source,cp_source,e,w):
    m=e.deg
    return (sq(e,2)+cup(w,e)+cup(c_source,cp_source,m)
            +cup(c_source+cp_source,e,m-1)+cup(e,c_source+cp_source,m-1))


def make_pair(p,dimension,rng_seed):
    import random
    random.seed(rng_seed)
    s=random_cochain(0,dimension).d();w=random_cochain(1,dimension).d();W=w+cup(s,s)
    def one():
        pot=C(p-1,values={f:random.randint(-9,9) for f in __import__('itertools').combinations(range(dimension+1),p)},mod=None)
        n=ds(pot,s);a=n.reduce(2);a.closed=True
        A=cup(a,a,p-2)+cup(W,a)
        u=primitive(A)+random_cochain(p,dimension).d()
        return n,u
    n,u=one();np,v=one()
    return n,u,np,v,w,s


def third_product(n,u,np,v,w,s):
    """Direct transcription of the already accepted native binary E_{p+2}."""
    p=n.deg;a=n.reduce(2);b=np.reduce(2);N=a+b
    h=(n-a.lift()).div(2).reduce(2);k=(np-b.lift()).div(2).reduce(2)
    W=w+cup(s,s);t=cup(a,b,p-1);z=cup(a,b,p)
    if p==1:intrinsic=op('12314',a,a,b,b);ell_carry=C(2)
    else:
        intrinsic=(op('12413423',a,a,a,b)+op('12314132',a,a,b,b)
                 +op('12314324',a,a,b,b)+op('12341321',a,a,b,b)
                 +op('12132413',a,b,b,b)+op('12324214',a,b,b,b))
        ell_carry=op('123142341',a,b,a,b)+op('123412143',b,b,a,b)
    pure=(intrinsic+cup(cup(W,N),t,p+1)+cup(cup(b,b,p-2),cup(W,a),p+2)
          +cup(t.d(),cup(W,N),p+2)+cup(h+a,k+b,p-2)+cup(h.d(),k,p-1)
          +cup(h+k,z,p-2)+cup(cup(s,a),cup(b,b,p-1),p)
          +cup(a,cup(s,b),p-1)+cup(z,cup(s,N),p-1)
          +cup(s,cup(s,z)+cup(a,k.d(),p)+cup(z,N,p-1)+ell_carry))
    if p==1:
        endpoint=lambda x:cup(cup(cup(x,x),s,1),x)
        pure=pure+endpoint(N)+endpoint(a)+endpoint(b)
    upper=(cup(u,v,p)+cup(u.d(),v,p+1)+cup(u+v,t,p)
          +cup(s,cup(u,v,p+1)+cup(u.d(),v,p+2)+cup(u+v,t,p+1)))
    return upper+pure


def binary_H(n,u,w,s,y):
    """Explicit binary bracket of the B-coordinate source; y is the fixed source input."""
    from cochains import prism_transgression,pure_parity
    p=n.deg;_,K,_,_=integer_inputs(n,w,s);j=beta_open(u).reduce(2);k=K.reduce(2)
    return (prism_transgression(u,w,s)+cup(u,ell(w,s))+cup(kappa(u,w,s),pure_parity(n,w,s),p+2)
           +y+cup(j,k,p)+cup(s,cup(j,k,p+1)))


def terminal_residual(n,u,np,v,w,s,*,ys=None,vertices=None,accelerate=False):
    """The exact remaining F2 cocycle. This function DOES NOT integrate it.

    Returns (R, even integer I). Use of the word residual is deliberate.
    The two requested complete top twisters are not exported by this module.
    """
    from explicit_pip import binary_completion
    from cochains import pure_parity
    p=n.deg;D=pair_data(n,u,np,v,w,s);N=D['N'];U=D['U'];B=D['B'];Bp=D['Bp'];BN=D['BN']
    W,vi,alpha,hv,P=background_data(w,s)
    EfracB=fractional_seed16(n,u,np,v,w,s,native=False)
    V=(EfracB-cup(W.lift(),D['T'],s=s,twists=(1,0)).scaled(2)).div(4).reduce(2)
    Q=lambda x:cup(x,x,p)+cup(x,x.d(),p+1)
    I=(Q(BN)-Q(B)-Q(Bp)+cup(w.lift(),D['lambda'].d()-D['R'])
       -cartan_word(N,w,s).lift()+cartan_word(n,w,s).lift()+cartan_word(np,w,s).lift()
       +cup(W.lift(),D['R'],s=s,twists=(1,0))-cup(vi,D['T'],s=s,twists=(1,0))-ds(V.lift(),s))
    if ys is None:
        kwargs={'vertices':vertices,'accelerate':accelerate}
        ys=[binary_completion(x,w,s,**kwargs) for x in (n,np,N)]
    HH=binary_H(N,U,w,s,ys[2])+binary_H(n,u,w,s,ys[0])+binary_H(np,v,w,s,ys[1])
    F=kappa(u,w,s)+pure_parity(n,w,s);Fp=kappa(v,w,s)+pure_parity(np,w,s)
    e=third_product(n,u,np,v,w,s)
    return upper_residual(F,Fp,e,w)+HH+I.div(2).reduce(2),I
