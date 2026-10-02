"""Public exact API: arbitrary integer n2, omega2=s1=0.
Run in a fresh Python process, separately from the legacy eager cochain engine.
"""
from dataclasses import dataclass
from fractions import Fraction
from itertools import combinations
from model import C as Cochain, F, cup
from product import stack as _stack, source48

@dataclass(frozen=True)
class Product:
    n2: Cochain
    n3: Cochain
    n4: Cochain
    phase_numerator48: Cochain
    def phase(self, face):
        """The additive correction in Q/Z, with canonical value in [0,1)."""
        return Fraction(self.phase_numerator48(tuple(face)) % 48, 48)

def validate(n2, n3, n4, vertices):
    if (n2.deg,n3.deg,n4.deg)!=(2,3,4):
        raise ValueError('Required degrees: integer n2, binary n3, binary n4.')
    if (n2.mod,n3.mod,n4.mod)!=(None,2,2):
        raise ValueError('Required coefficient types are Z, F2, F2.')
    vertices=tuple(vertices)
    if len(vertices)<6 or len(set(vertices))!=len(vertices):
        raise ValueError('Supply an ordered simplex with at least six distinct vertices.')
    conditions=(('d n2',n2.d()),('d n3 - [n2]^2',n3.d()-cup(n2.reduce(2),n2.reduce(2))),('d n4 - F5',n4.d()-F(n2,n3)))
    for name,cochain in conditions:
        for f in combinations(vertices,cochain.deg+1):
            if cochain(f)!=0:raise ValueError(f'Invalid lower data: {name} is nonzero on {f}.')
    return vertices

def stacking(n2,n3,n4,n2_prime,n3_prime,n4_prime,*,vertices,check=True):
    """Complete zero-background terminal product; not a fractional seed.

    Returns N2,N3,N4 and the additive bosonic correction. For complete input
    states add this correction to the two input bosonic phases modulo one.
    No backgrounds are accepted or silently discarded by this API.
    """
    if check:
        validate(n2,n3,n4,vertices);validate(n2_prime,n3_prime,n4_prime,vertices)
    N,U,C,E=_stack(n2,n3,n4,n2_prime,n3_prime,n4_prime)
    return Product(N,U,C,E)

def obstruction(n2,n3,n4,face):
    """The fixed B/APS d4 source in Q/Z on an ordered six-simplex."""
    if len(face)!=7:raise ValueError('An obstruction value needs seven vertices.')
    return Fraction(source48(n2,n3,n4)(tuple(face)) % 48,48)
