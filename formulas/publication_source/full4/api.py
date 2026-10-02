"""Current full-background 4+1D source and terminal stacking evaluator.

The only exported lower normalization is the corrected one.  Native
Majorana inputs are shifted internally by s1 cup floor(n_integer/2).
Every phase is an exact Fraction; no primitive solver is used.
"""
from __future__ import annotations
from pathlib import Path
import sys
from fractions import Fraction
from itertools import combinations
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'full4'))
import kernel_full as kernel
from product_full import C,cup,carry,lower,collected_blocks,binary_phase,full_source48
from pip_d4 import _cochain,validate_tower
COORDINATE='current full-background corrected lower product / characteristic-B APS / collected phase'

def _state(data):
 return (_cochain(2,data['n_integer'],None),_cochain(3,data['n_majorana'],2),_cochain(4,data['n_fermion'],2))

def _acceleration(enabled):
 kernel.ACCELERATE=bool(enabled)
 import kernel_cached
 kernel_cached.ACCELERATE=bool(enabled)

def source(*,n_integer,n_majorana,n_fermion,omega2,s1,accelerate=True,validate=True)->dict[str,Any]:
 """Evaluate O6 on vertices 0,...,6 from native lower cochains.
 Each input is a mapping on every ordered face of its degree or a callable.
 Missing faces, nonintegral data, nonbinary data and invalid lower equations
 are rejected.  The source contains the retained integer cubic n2^3/12.
 """
 n,r,c=_state(dict(n_integer=n_integer,n_majorana=n_majorana,n_fermion=n_fermion))
 w=_cochain(2,omega2,2);s=_cochain(1,s1,2)
 if validate:validate_tower(2,(n,r,c,w,s),7)
 u=r+cup(s,carry(n));_acceleration(accelerate)
 num=int(full_source48(n,u,c,w,s)(tuple(range(7))))%48
 return {'phase':Fraction(num,48),'numerator_mod48':num,'coordinate':COORDINATE}

def stack(*,first,second,omega2,s1,accelerate=True,validate=True)->dict[str,Any]:
 """Evaluate the full corrected lower product and E5 on vertices 0,...,5.
 first and second have keys n_integer (degree 2, Z_s), n_majorana
 (degree 3, native binary), n_fermion (degree 4, binary).  Bosonic phases
 multiply and acquire exp(2*pi*i*result['phase']).
 """
 n,r,c=_state(first);m,rp,cp=_state(second)
 w=_cochain(2,omega2,2);s=_cochain(1,s1,2)
 if validate:
  validate_tower(2,(n,r,c,w,s),6);validate_tower(2,(m,rp,cp,w,s),6)
 u=r+cup(s,carry(n));v=rp+cup(s,carry(m));N,U,e=lower(n,u,m,v,w,s)
 RN=U+cup(s,carry(N));CN=c+cp+e
 if validate:validate_tower(2,(N,RN,CN,w,s),6)
 _acceleration(accelerate);f=tuple(range(6));D=collected_blocks(n,u,c,m,v,cp,w,s)
 seed=int(D['nonbinary48'](f))%48;zz=int(binary_phase(n,u,m,v,w,s)(f))%2;num=(seed+24*zz)%48
 outputs={key:{g:int(x(g))for g in combinations(range(6),x.deg+1)}for key,x in [('n_integer',N),('n_majorana',RN),('n_fermion',CN)]}
 return {'phase':Fraction(num,48),'numerator_mod48':num,
  'parts_mod48':{'explicit_cup_terms':seed,'binary_background_transfer':24*zz},
  'lower_output':outputs,'coordinate':COORDINATE}
