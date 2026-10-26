#!/usr/bin/env python3
"""Closed 4+1D group for C_(2m)^f times arbitrary finite Abelian spectators.

The distinguished fermion parity is the order-two element of C_(2m).
The input m is the bosonic quotient order of that factor.  When m is odd,
this marked group is split and is reduced accordingly.  All calculations
below are exact integer arithmetic on supports of size at most five.

This implementation accompanies the Gysin and cochain proofs.
It computes the full mathematical classification, without asserting a
physical construction of the terminal p+ip Berry phase.
"""

from itertools import combinations
from math import prod
from pathlib import Path
import importlib.util
from sympy import factorint
try:
    from .higher_support import closed as higher_support
except ImportError:
    from higher_support import closed as higher_support


def _split_module():
    path=Path(__file__).resolve().with_name('split_closed_formula.py')
    spec=importlib.util.spec_from_file_location('finite_abelian_split_closed_formula',path)
    module=importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def block(m,spectators):
    """Full anchored support block for powers-of-two input orders."""
    spectators=sorted(spectators)
    if m<2 or m&(m-1) or any(n<2 or n&(n-1) for n in spectators):
        raise ValueError('The 2-primary block requires powers of two >=2')
    if not spectators:
        result=[m//2,8*m]
    elif len(spectators)==1:
        n=spectators[0]
        if n<m:
            result=[n//2]*2+[n,4*n]
        elif n==m:
            result=[m//2]*3+[4*m]
        elif n<4*m:
            result=[m//2]+[n//2]*2+[4*m]
        else:
            result=[m//2,2*m,n//2,n]
    else:
        result=higher_support(m,spectators)
    return sorted(n for n in result if n>1)


def nonsplit_2primary(m,spectators):
    """Return 2-primary invariant factors, including all stable supports."""
    result=block(m,[])
    for size in range(1,min(5,len(spectators))+1):
        for subset in combinations(spectators,size):
            result.extend(block(m,subset))
    return sorted(result)


def combine_primary(factors):
    groups={}
    for n in factors:
        if n<=1:
            continue
        for p,a in factorint(n).items():
            groups.setdefault(int(p),[]).append(int(p)**int(a))
    width=max(map(len,groups.values()),default=0)
    rows=[[1]*(width-len(ns))+sorted(ns) for ns in groups.values()]
    return [prod(column) for column in zip(*rows)] if rows else []


def nonsplit_closed_formula(m,ns=()):
    """Invariant factors for G_f=C_(2m)^f x product_i C_(ns[i])."""
    if m<1 or any(n<1 for n in ns):
        raise ValueError('All cyclic orders must be positive integers')
    split=_split_module()
    if m%2:
        return split.invariant_factors([m,*ns])
    first_factors=factorint(m)
    first_two=2**int(first_factors[2])
    spectator_twos=[]
    odd_orders=[m//first_two]
    for n in ns:
        exponent=int(factorint(n).get(2,0))
        if exponent:
            spectator_twos.append(2**exponent)
        odd_orders.append(n//2**exponent)
    primary=nonsplit_2primary(first_two,spectator_twos)
    primary.extend(split.primary_factors(odd_orders))
    return combine_primary(primary)
