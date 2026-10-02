"""Explicit full-twist cochain-closed candidates for independently constructed O5 and O6.

Status: exact cochain construction. Physical Postnikov normalization beyond
the Majorana restriction has NOT been fixed by cobordism calibration.
All public functions return an integer numerator with denominator sixteen.
"""
from __future__ import annotations
from cochains import C, cup, positive_residual_data, prism_transgression, polarization

def O6_16(n2:C,n3:C,n4:C,omega2:C,s1:C,vertices:int|None=None,*,accelerate:bool=False)->C:
    """Sixteen times the degree-six additive candidate (reduce values mod 16).

    Inputs: n2 in Z_s^2, n3 in C^3(F2), n4 in C^4(F2),
    omega2 in Z^2(F2), s1 in Z^1(F2). They must obey the lower equations in the accompanying note.
    With acceleration, vertices must be labelled 0,...,vertices-1. This function does not solve
    those lower equations. Setting accelerate=False uses the exact Python
    evaluator and can be substantially slower.
    """
    from explicit_y6 import Y6
    N,b,c,w,s=n2,n3,n4,omega2,s1
    expected=[(N,2,None),(b,3,2),(c,4,2),(w,2,2),(s,1,2)]
    if any(x.deg!=d or x.mod!=m for x,d,m in expected):
        raise ValueError('Expected degrees/coefficient moduli: (2,Z),(3,2),(4,2),(2,2),(1,2)')
    if vertices is not None and vertices<1:raise ValueError('vertices must be positive')
    if accelerate and vertices is None:raise ValueError('Supply vertices when using the optional C++ engine')
    seed,_,_=positive_residual_data(N,b,c,w,s)
    h=(N-N.reduce(2).lift()).div(2).reduce(2);bp=b+cup(s,h)
    ell=w.lift().d().div(2).reduce(2)+cup(s,w)
    if accelerate:
        try:
            from fast_y6 import fast_Y6
        except (ImportError,OSError) as e:
            raise RuntimeError('Build the optional C++ engine first, or use accelerate=False.') from e
        y=fast_Y6(N,w,s,vertices)
    else:y=Y6(N,w,s)
    X=prism_transgression(bp,w,s)+polarization(N,b,w,s)+cup(bp,ell)+y
    out=seed+X.lift().scaled(8)
    # Keep the optional engine reachable; callers may release it explicitly.
    out.Y6=y
    return out

def O5_16(n1:C,n2:C,n3:C,omega2:C,s1:C,vertices:int|None=None,*,accelerate:bool=False)->C:
    """Independent degree-five cochain candidate, sixteen times the phase.

    No call to O6, Y6 or to a suspension of the input data is made.
    vertices and accelerate are accepted for API symmetry and have no effect here.
    """
    from explicit_y5 import Y5
    expected=[(n1,1,None),(n2,2,2),(n3,3,2),(omega2,2,2),(s1,1,2)]
    if any(x.deg!=d or x.mod!=m for x,d,m in expected):
        raise ValueError('Expected (n1:Z_s^1,n2:F2^2,n3:F2^3,omega2:F2^2,s1:F2^1)')
    seed,_,_=positive_residual_data(n1,n2,n3,omega2,s1)
    h1=(n1-n1.reduce(2).lift()).div(2).reduce(2)
    n2prime=n2+cup(s1,h1)
    ell=omega2.lift().d().div(2).reduce(2)+cup(s1,omega2)
    y5=Y5(n1,omega2,s1)
    correction=(prism_transgression(n2prime,omega2,s1)
                +polarization(n1,n2,omega2,s1)+cup(n2prime,ell)+y5)
    out=seed+correction.lift().scaled(8)
    out.Y5=y5
    return out


def comparison5_16(n1:C,n2:C,n3:C,omega2:C,s1:C,vertices:int,*,accelerate:bool=False)->C:
    """Sixteen times tau(O6)-O5 on the COMPLETE suspended lower tower.

    This computes a closed comparison, not an asserted zero cochain and not
    a definition of the independently constructed O5. See Section 4 of the note.
    """
    from suspension import full_suspension,tau
    high=O6_16(*full_suspension(n1,n2,n3,omega2,s1),vertices=2*vertices,accelerate=accelerate)
    return tau(high)-O5_16(n1,n2,n3,omega2,s1,vertices=vertices)
