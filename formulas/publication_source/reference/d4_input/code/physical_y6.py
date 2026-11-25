"""Integer-layer completion y_6 of the physical F-move parity count O_5^psi.

The construction is the fixed grid homotopy of explicit_pip.binary_completion,
applied to the residual whose parity term is the physical O_5^psi, with the
tensor coefficients physical_Y6_total.json. No coefficient is solved here.
"""
from cochains import C,cup,op,sq,ds,zeta2,background_data,mc_phase4
from compact import integer_inputs,kappa,ell
from explicit_pip import seed16

def carry(n):
    return (n-n.reduce(2).lift()).div(2).reduce(2)

def physical_pure_parity(n,omega2,s1):
    """O_5^psi: intrinsic zero modes, projective zero modes and their pairs."""
    a=n.reduce(2);h=carry(n);W=omega2+cup(s1,s1)
    aa=cup(a,a);Wa=cup(W,a);W1W=cup(W,W,1)
    return (zeta2(a,a)+cup(h,cup(a,a,1))+cup(s1,cup(h,a))
            +zeta2(W,a)+cup(W1W+cup(s1,W),h)+cup(cup(W1W,s1,1)+cup(s1,cup(s1,W,1)),a)
            +cup(aa,Wa,3)+cup(s1,cup(aa,Wa,4)))

def physical_residual(n,omega2,s1):
    """Binary residual of the pure seed with the physical parity count."""
    p=n.deg;A,_,_,_=integer_inputs(n,omega2,s1)
    Psi=physical_pure_parity(n,omega2,s1);F=kappa(A,omega2,s1)
    theta=cup(omega2.lift(),A.lift()).scaled(4)+cup(A,ell(omega2,s1),1).lift().scaled(8)
    base=cup(Psi,Psi,p+1)+cup(F,Psi,p+2)+cup(omega2,Psi)
    numerator=ds(seed16(n,omega2,s1)+theta,s1)+base.lift().scaled(8)+mc_phase4(A,C(p+3),omega2,s1).scaled(4)
    return numerator.div(8).reduce(2)

def physical_completion(n,omega2,s1):
    """y_6 = (h_6^(3))^* R_7 + AW^* Y_6^tot for the physical parity count."""
    from ez_homotopy import ez_homotopy
    from polynomial_tables import total_cochain
    if n.deg!=2:raise ValueError('The physical completion is defined for the integer two-cocycle n_2')
    H=ez_homotopy(6)
    aw=total_cochain(n,omega2,s1,'physical_Y6_total.json',6)
    def sign(a,b):return (-1)**(s1(tuple(sorted((a,b)))) if a!=b else 0)
    ng=C(2,fun=lambda f:sign(f[0][0],f[0][1])*n(tuple(v[1] for v in f)),mod=None)
    wg=C(2,fun=lambda f:omega2(tuple(v[2] for v in f)));wg.closed=True
    sg=C(1,fun=lambda f:s1(tuple(v[0] for v in f)));sg.closed=True
    R=physical_residual(ng,wg,sg)
    def val(face):
        ans=aw(face)
        for simplex in H:ans^=R(tuple(tuple(face[c] for c in v) for v in simplex))
        return ans
    return C(6,fun=val)
