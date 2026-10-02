"""Complete 3+1D terminal cochain pair with arbitrary omega2 and s1.

Inputs use the manuscripts' native Majorana coordinate. The final phase
coordinate is the explicitly specified multiplicative suspension of the current 3+1D terminal section.
The inherited high obstruction is not silently replaced or refitted.
"""
from pathlib import Path
import sys
from fractions import Fraction
from itertools import combinations
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'full3'))
from source import C,cup,carry,lower_product,source_parts16,product_parts16
from pip_d4 import _cochain,validate_tower

COORDINATE='current full-background multiplicative suspension'

def _state(data):
 return (_cochain(1,data['n_integer'],None),_cochain(2,data['n_majorana'],2),_cochain(3,data['n_fermion'],2))

def source(*,n_integer,n_majorana,n_fermion,omega2,s1,accelerate=True,validate=True):
 """O5 on vertices 0,...,5; exact Fraction, never a floating-point phase.

Each field must provide every face of its degree, either as a dictionary
whose keys are ordered tuples or as a callable. All input lower equations
are checked before starting the source evaluation when validate=True.
 """
 n,r,c=_state(dict(n_integer=n_integer,n_majorana=n_majorana,n_fermion=n_fermion))
 w=_cochain(2,omega2,2);s=_cochain(1,s1,2)
 if validate:validate_tower(1,(n,r,c,w,s),6)
 u=r+cup(s,carry(n));face=tuple(range(6))
 parts=source_parts16(n,u,c,w,s,accelerate=accelerate,validate=validate)
 nums=[int(p(face))%16 for p in parts];num=sum(nums)%16
 return {'phase':Fraction(num,16),'numerator_mod16':num,
         'parts_mod16':dict(zip(('binary_transgression','integer_transgression','twisted_Pontryagin_linear'),nums)),
         'coordinate':COORDINATE}

def stack(*,first,second,omega2,s1,accelerate=True,validate=True):
 """Full lower output and terminal E4 on vertices 0,...,4.

The three fields of first/second are n_integer (degree 1, Z_s),
n_majorana (degree 2, F2, UNSHIFTED), and n_fermion (degree 3, F2).
nu4 phases multiply and acquire exp(2 pi i * result['phase']).
No input-dependent cochain solve occurs in the evaluator.
 """
 w=_cochain(2,omega2,2);s=_cochain(1,s1,2)
 n,r,c=_state(first);m,rp,cp=_state(second)
 if validate:
  validate_tower(1,(n,r,c,w,s),5);validate_tower(1,(m,rp,cp,w,s),5)
 u=r+cup(s,carry(n));v=rp+cup(s,carry(m))
 N,U,e=lower_product(n,u,m,v,w,s);RN=U+cup(s,carry(N));CN=c+cp+e
 if validate:validate_tower(1,(N,RN,CN,w,s),5)
 parts=product_parts16(n,u,c,m,v,cp,w,s,accelerate=accelerate,validate=validate)
 nums=[int(p(tuple(range(5))))%16 for p in parts];num=sum(nums)%16
 outputs={key:{f:int(z(f)) for f in combinations(range(5),z.deg+1)} for key,z in [('n_integer',N),('n_majorana',RN),('n_fermion',CN)]}
 return {'phase':Fraction(num,16),'numerator_mod16':num,
         'parts_mod16':dict(zip(('binary_transgression','integer_transgression','explicit_minus_W_n_m'),nums)),
         'lower_output':outputs,'coordinate':COORDINATE}
