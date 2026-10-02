"""Calculation entry points for the explicit full-twist p+ip d4 cochains.

Use exact integer arithmetic. Phases are fractions modulo one, with
numerator modulo 16. The input lower tower is checked by default.
The p=1 and p=2 formulas use independently fixed coefficient tables.
"""
from __future__ import annotations
from fractions import Fraction
from itertools import combinations
from typing import Callable, Mapping, Sequence, Any
from cochains import C, cup, sq, ds, parity, op, background_data
from explicit_pip import (binary_completion, full_terms16, cartan_word,
                         cartan_rephasing, pure_terms16, sum_terms, cartan_words)
from polynomial_tables import total_cochain

Face = tuple[int, ...]
Field = Callable[[Face], int] | Mapping[Face, int]

def _cochain(degree: int, field: Field, modulus: int | None) -> C:
    def value(face):
        v = field(face) if callable(field) else field[face]
        if not isinstance(v, int):
            try:
                iv = int(v)
                if iv != v: raise ValueError
                v = iv
            except (TypeError,ValueError):
                raise TypeError(f'Nonintegral cochain value {v!r} on {face}')
        if modulus == 2 and v not in (0,1):
            raise ValueError(f'Binary cochains must be 0 or 1, got {v} on {face}')
        return v
    return C(degree, fun=value, mod=modulus)

def validate_tower(p: int, fields: Sequence[C], vertex_count: int) -> None:
    n,majorana,fermion,omega2,s1 = fields
    a=n.reduce(2)
    equations = {
        'd s1 = 0': s1.d(),
        'd omega2 = 0': omega2.d(),
        'd_s1 n_p = 0 over Z': ds(n,s1),
        'Majorana source': majorana.d()+sq(a,2)+cup(omega2,a)+cup(s1,sq(a,1)),
        'complex-fermion source': fermion.d()+parity(n,majorana,omega2,s1),
    }
    for name,residual in equations.items():
        for face in combinations(range(vertex_count),residual.deg+1):
            if residual(face) != 0:
                raise ValueError(f'Invalid lower tower: {name} fails on {face}; residual={residual(face)}')

def evaluate_simplex(p: int, *, n_integer: Field, n_majorana: Field,
                     n_fermion: Field, omega2: Field, s1: Field,
                     validate: bool=True, accelerate: bool=False) -> dict[str, Any]:
    """Evaluate one O5 (p=1) or O6 (p=2) simplex and return every term.

    Vertices are 0,...,p+4. Provide ALL faces of the required degrees.
    Missing dictionary keys are errors, not silently zero values.
    With p=2, accelerate=True needs the optional compiled C++ engine.
    """
    if p not in (1,2):raise ValueError('p must be 1 (O5) or 2 (O6)')
    r=p+4;fields=(_cochain(p,n_integer,None),_cochain(p+1,n_majorana,2),
                 _cochain(p+2,n_fermion,2),_cochain(2,omega2,2),_cochain(1,s1,2))
    if validate:validate_tower(p,fields,r+1)
    n,majorana,fermion,w,s=fields
    y=binary_completion(n,w,s,vertices=r+1,accelerate=(accelerate and p==2))
    try:
        terms=full_terms16(n,majorana,fermion,w,s,binary_y=y)
        face=tuple(range(r+1));values={key:int(cochain(face))%16 for key,cochain in terms.items()}
        numerator=sum(values.values())%16
        # Detailed binary pieces are reported BEFORE their one canonical lift.
        a=n.reduce(2);h=(n-a.lift()).div(2).reduce(2)
        W,v,alpha,hv,P=background_data(w,s)
        cartan_parts={
            'single_word':op(cartan_words(p)['words'][0],alpha,alpha,a,a),
            'background_carry_times_Sq1_n':cup(hv,sq(a,1)),
            's1_Bockstein_h':cup(cup(s,alpha),h),
            's1_cup_order_correction':cup(cup(s,cup(alpha,s,1)),a),
        }
        cartan_values={key:int(c(face)) for key,c in cartan_parts.items()}
        cartan_total=sum(cartan_values.values())%2
        assert cartan_total==int(cartan_word(n,w,s)(face))
        aw_value=int(total_cochain(n,w,s,f'Y{r}_word_total.json',r)(face))
        pontryagin_parts={
            'W_W_n':int(cup(cup(W.lift(),W.lift(),s=s,twists=(1,1)),n,s=s,twists=(0,1))(face))%16,
            'W_cup1_d_s_W_n':int(cup(cup(W.lift(),ds(W.lift(),s),1,s=s,twists=(1,1)),n,s=s,twists=(0,1))(face))%16,
        }
        assert sum(pontryagin_parts.values())%16==values['background_Pontryagin_n']
        return {'degree':r,'numerator_mod16':numerator,'phase_mod1':Fraction(numerator,16),
                'terms_numerator_mod16':values,'binary_y':int(y(face)),
                'binary_Cartan_carry':cartan_total,
                'Cartan_binary_components_before_whole_lift':cartan_values,
                'Pontryagin_numerators_mod16':pontryagin_parts,
                'y_binary_components':{'AW_table':aw_value,'EZ_residual':int(y(face))^aw_value},
                'status':'fixed cochain representative; finite-group physical class calibrated relative to the lower bordism tower and p+ip generator (note Theorem 9.1)'}
    finally:
        if hasattr(y,'engine'):y.engine.close()

def inhomogeneous_fields(arguments: Sequence[Any], *, identity: Any,
                         multiply: Callable[[Any,Any],Any],
                         n_integer: Callable[...,int], n_majorana: Callable[...,int],
                         n_fermion: Callable[...,int], omega2: Callable[...,int],
                         s1: Callable[...,int]) -> dict[str,Callable[[Face],int]]:
    """Pull normalized group cochains to the ordered simplex [g0,...,gr].

    arguments=(g1,...,gr) are successive bar increments. A skipped edge i->j
    is the ordered product g_(i+1)...g_j; nonabelian order is retained.
    Degenerate group simplices (an identity increment) evaluate to zero.
    Integer fields use their own initial-vertex trivialization; transport
    signs are inserted by the cochain operations, not by this adapter.
    """
    def adapt(fn):
        def value(face):
            increments=[]
            for a,b in zip(face,face[1:]):
                z=identity
                for g in arguments[a:b]:z=multiply(z,g)
                if z==identity:return 0
                increments.append(z)
            return int(fn(*increments))
        return value
    return {key:adapt(fn) for key,fn in [('n_integer',n_integer),('n_majorana',n_majorana),
            ('n_fermion',n_fermion),('omega2',omega2),('s1',s1)]}
