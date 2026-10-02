"""4+1D unitary shared-background cochain pair, Section 22.

The source is the retained characteristic-B/APS source.  The lower fermion
product is explicitly branch 1: e4_old + [n2]_2 cup [n2']_2.  This must not be
silently combined with branch-0 output data.  The top phase uses the shortened
pair-coboundary gauge in the displayed Section 22 formula.
"""
from __future__ import annotations
from pathlib import Path
import sys
from fractions import Fraction
from itertools import combinations
from typing import Any
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'unitary4'))
import kernel_cached as cache
from unitary_product import C,cup,old_lower,neat_phase48,source48,collected_blocks,Z
from pip_d4 import _cochain,validate_tower
COORDINATE='unitary-lower-branch-1 / characteristic-B-APS / shortened pair gauge, Section 22'

def _state(data):
    return (_cochain(2,data['n_integer'],None),_cochain(3,data['n_majorana'],2),
            _cochain(4,data['n_fermion'],2))

def source(*,n_integer,n_majorana,n_fermion,omega2,accelerate=True,validate=True) -> dict[str,Any]:
    """Evaluate the full O6 on vertices 0,...,6, returning an exact Fraction."""
    n,u,c=_state(dict(n_integer=n_integer,n_majorana=n_majorana,n_fermion=n_fermion))
    w=_cochain(2,omega2,2)
    if validate:validate_tower(2,(n,u,c,w,C(1)),7)
    n.closed=w.closed=True
    num=int(source48(n,u,c,w,accelerate=accelerate)(tuple(range(7))))%48
    return {'phase':Fraction(num,48),'numerator_mod48':num,'coordinate':COORDINATE,'s1':0}

def stack(*,first,second,omega2,accelerate=True,validate=True) -> dict[str,Any]:
    """Evaluate the full lower output and E5 on vertices 0,...,5.

    Fields are mappings on every face of the indicated degree or exact-integer
    callables.  Missing faces, nonintegral values and invalid lower towers are
    errors.  Input nu5 phases multiply and acquire exp(2*pi*i*result['phase']).
    Caches are process-local; run independent tests in separate processes.
    """
    n,u,c=_state(first);m,v,cp=_state(second);w=_cochain(2,omega2,2)
    if validate:
        validate_tower(2,(n,u,c,w,C(1)),6);validate_tower(2,(m,v,cp,w,C(1)),6)
    n.closed=m.closed=w.closed=True
    N,U,e=old_lower(n,u,m,v,w);z=cup(n.reduce(2),m.reduce(2));CF=c+cp+e+z
    if validate:validate_tower(2,(N,U,CF,w,C(1)),6)
    cache.ACCELERATE=bool(accelerate)
    blocks=collected_blocks(n,u,c,m,v,cp,w);f=tuple(range(6))
    zz=int(Z(n,u,m,v,w)(f))%2
    seed=int(blocks['nonbinary48'](f))%48;num=(seed+24*zz)%48
    outputs={key:{face:int(x(face)) for face in combinations(range(6),x.deg+1)}
             for key,x in [('n_integer',N),('n_majorana',U),('n_fermion',CF)]}
    return {'phase':Fraction(num,48),'numerator_mod48':num,
            'parts_mod48':{'displayed_nontransfer_terms':seed,'binary_transfer':24*zz},
            'lower_output':outputs,'closed_lower_correction':{face:int(z(face)) for face in combinations(range(6),5)},
            'coordinate':COORDINATE,'s1':0}
