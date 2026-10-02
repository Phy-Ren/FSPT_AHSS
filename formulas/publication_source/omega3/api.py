"""Public 3+1D unitary-extension source and stacking API.

The phase coordinate is the explicitly defined interval/triangle transgression
coordinate in Section 20, not the original raw O5 coordinate. omega2 is fixed
under stacking; s1 is identically zero. No primitive is solved during evaluation.
"""
from pathlib import Path
import sys
from fractions import Fraction
from itertools import combinations
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'omega3'))
from loop_product import C,cup,parity,third_product,source_parts16,product_parts16
from pip_d4 import _cochain,validate_tower

def source(*, n_integer,n_majorana,n_fermion,omega2,accelerate=True,validate=True):
    """Evaluate O5 on vertices 0,...,5. Missing face keys are errors."""
    n,u,c,w=(_cochain(1,n_integer,None),_cochain(2,n_majorana,2),
             _cochain(3,n_fermion,2),_cochain(2,omega2,2))
    if validate:validate_tower(1,(n,u,c,w,C(1)),6)
    f=tuple(range(6));parts=source_parts16(n,u,c,w,accelerate=accelerate,validate=validate)
    values=[int(x(f))%16 for x in parts];num=sum(values)%16
    return {'phase':Fraction(num,16),'numerator_mod16':num,
            'parts_mod16':dict(zip(('binary_transgression','characteristic_transgression','Pontryagin_linear'),values)),
            'coordinate':'multiplicative interval transgression, Section 20','s1':0}

def stack(*,first,second,omega2,accelerate=True,validate=True):
    """Evaluate a full lower product and E4 on vertices 0,...,4.

    first/second contain n_integer, n_majorana, n_fermion: dictionaries on ALL
    respective faces or callables returning exact integers. Returns all output
    lower face values and a Fraction modulo one. nu4 input phases simply multiply
    and acquire exp(2*pi*i*phase).
    """
    w=_cochain(2,omega2,2)
    def state(data):return (_cochain(1,data['n_integer'],None),_cochain(2,data['n_majorana'],2),_cochain(3,data['n_fermion'],2))
    n,u,c=state(first);m,v,cp=state(second)
    if validate:
        for nn,uu,cc in ((n,u,c),(m,v,cp)):validate_tower(1,(nn,uu,cc,w,C(1)),5)
    N=n+m;U=u+v+cup(n.reduce(2),m.reduce(2));E3=third_product(n,u,m,v,w,C(1));CF=c+cp+E3
    if validate:validate_tower(1,(N,U,CF,w,C(1)),5)
    f=tuple(range(5));parts=product_parts16(n,u,c,m,v,cp,w,accelerate=accelerate,validate=validate)
    vals=[int(x(f))%16 for x in parts];num=sum(vals)%16
    fields={key:{face:int(z(face)) for face in combinations(range(5),z.deg+1)} for key,z in [('n_integer',N),('n_majorana',U),('n_fermion',CF)]}
    return {'lower_output':fields,'phase':Fraction(num,16),'numerator_mod16':num,
            'parts_mod16':dict(zip(('binary_transgression','characteristic_transgression','explicit_minus_omega_n_m'),vals)),
            'coordinate':'multiplicative interval transgression, Section 20','s1':0}
