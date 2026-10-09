"""Current 3+1D geometric pairing coordinate and complete phase transport.

The bundled publication cochain engine is a frozen evaluator. This module is
its current coordinate boundary: old CF arguments are never physical n3.
The published phase coefficient tables are evaluated on checked_fermion(...),
and their product receives face_phase_numerator(...)/2. No numerical fit,
cohomology solve, or floating point operation is used.
"""
from pathlib import Path
import sys
ROOT=Path(__file__).resolve().parents[1]
CODE=ROOT/'formulas/publication_source/reference/d4_input/code'
if str(CODE) not in sys.path:sys.path.insert(0,str(CODE))
from cochains import C,cup,parity


def second_digit(n):
    return C(n.deg,fun=lambda f:n(f)//2)


def checked_majorana(n,n2,s):
    return n2+cup(s,second_digit(n))


def single_reference(m):
    return cup(m,m,1)


def checked_fermion(n3,m):
    return n3+single_reference(m)


def pair_reference(n,np,m,mp,s):
    a,b=n.reduce(2),np.reduce(2)
    h,k=second_digit(n),second_digit(np)
    e=cup(a,b)
    return (cup(a,k)+cup(h,b)+cup(h,k)+cup(m,mp,2)
            +cup(e,m+mp,2)+cup(cup(s,h,1),b)
            +cup(cup(s,cup(a,b,1),1),a+b))


def obstruction(n,n2,w,s):
    m=checked_majorana(n,n2,s)
    return parity(n,n2,w,s)+single_reference(m).d()


def lower_product(n,np,n2,n2p,w,s):
    a,b=n.reduce(2),np.reduce(2)
    h=second_digit(n)
    m,mp=checked_majorana(n,n2,s),checked_majorana(np,n2p,s)
    e=cup(a,b)
    E2=e+cup(s,cup(a,b,1))
    gamma=cup(m,mp,1)+cup(s,cup(m,mp,2))
    mixed=cup(m,mp.d(),2)+cup(m+mp,e,1)+cup(s,cup(m+mp,e,2))
    psi=cup(cup(a,e,1),b)+cup(h,cup(b,b))+cup(cup(s,h),b)
    return n+np,n2+n2p+E2,gamma+mixed+psi


def face_phase_numerator(previous_output,face_reference,w):
    """Binary numerator; divide the whole 0/1 value by two modulo one.

    previous_output is checked N3+dB2, i.e. the frozen product's output.
    Its differential need not vanish. s1 is arbitrary: the differential
    of a half-valued phase is its binary differential divided by two.
    """
    b=face_reference;z=b.d()
    return cup(w,b)+cup(b,b)+cup(z,b,1)+cup(previous_output,z,2)


def source_arguments(n,n2,n3,w,s):
    """Arguments of the retained complete phase source, in its fixed order."""
    m=checked_majorana(n,n2,s)
    return n,n2,checked_fermion(n3,m),w,s


def transported_product(n,np,n2,n2p,n3,n3p,w,s,previous_phase):
    """Current full product, from a retained phase callback.

    previous_phase takes (n,n2,checked_n3,np,n2p,checked_n3p,w,s) and returns
    an additive degree-four cochain over exact rational values (mod=None).
    It evaluates the frozen paired reader phase, not a different native phase.
    """
    N,N2,E3=lower_product(n,np,n2,n2p,w,s)
    N3=n3+n3p+E3
    m,mp=checked_majorana(n,n2,s),checked_majorana(np,n2p,s)
    c,cp=checked_fermion(n3,m),checked_fermion(n3p,mp)
    b=pair_reference(n,np,m,mp,s)
    old_output=checked_fermion(N3,checked_majorana(N,N2,s))+b.d()
    K=face_phase_numerator(old_output,b,w)
    from fractions import Fraction
    phase=previous_phase(n,n2,c,np,n2p,cp,w,s)+K.lift().scaled(Fraction(1,2))
    return N,N2,N3,phase
