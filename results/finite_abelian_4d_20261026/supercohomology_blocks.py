#!/usr/bin/env python3
"""Exact CF/bosonic Smith presentation for nonsplit spectator support >=2.

All cyclic orders must be powers of two. The distinguished first order is m
in C_(2m)^f, followed by the spectator orders. The chosen support includes
every spectator and allows degree zero in the distinguished factor.

The chain complex is the tensor product of the cyclic periodic resolutions.
All required operations are Sq^2 + y_0 and integral chain linear algebra.
This program intentionally does not claim the support-0/1 p+ip extensions.
"""

from itertools import combinations
from argparse import ArgumentParser
from sympy import Matrix, ZZ, zeros, Rational
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp
from sympy.matrices.normalforms import smith_normal_form


def compositions(total, length):
    if length == 1:
        if total >= 0:
            yield (total,)
        return
    for first in range(total+1):
        for tail in compositions(total-first, length-1):
            yield (first,) + tail


def basis(degree, rank):
    return [a for a in compositions(degree,rank) if all(x>0 for x in a[1:])]


def differential(degree, orders):
    source=basis(degree,len(orders)); target=basis(degree+1,len(orders))
    positions={a:i for i,a in enumerate(target)}
    result=zeros(len(target),len(source))
    for col,a in enumerate(source):
        for j,n in enumerate(orders):
            if a[j]%2:
                b=list(a);b[j]+=1
                result[positions[tuple(b)],col] += (-1)**sum(a[:j])*n
    return result


def sq2_twisted(degree,orders):
    source=basis(degree,len(orders));target=basis(degree+2,len(orders))
    positions={a:i for i,a in enumerate(target)}
    result=zeros(len(target),len(source))
    epsilon=[(n//2)%2 for n in orders]
    for col,a in enumerate(source):
        b=list(a);b[0]+=2
        result[positions[tuple(b)],col]+=1
        for j in range(len(orders)):
            if (a[j]//2)%2:
                b=list(a);b[j]+=2
                result[positions[tuple(b)],col]+=1
        odd=[j for j in range(len(orders)) if a[j]%2 and epsilon[j]]
        for i,j in combinations(odd,2):
            b=list(a);b[i]+=1;b[j]+=1
            result[positions[tuple(b)],col]+=1
    return result.applyfunc(lambda x:int(x)%2)


def binary_rref(matrix):
    a=[[int(matrix[i,j])%2 for j in range(matrix.cols)] for i in range(matrix.rows)]
    pivots=[];row=0
    for col in range(matrix.cols):
        pivot=next((i for i in range(row,matrix.rows) if a[i][col]),None)
        if pivot is None:
            continue
        a[row],a[pivot]=a[pivot],a[row]
        for i in range(matrix.rows):
            if i!=row and a[i][col]:
                a[i]=[u^v for u,v in zip(a[i],a[row])]
        pivots.append(col);row+=1
        if row==matrix.rows:
            break
    return a,pivots


def binary_kernel(matrix):
    a,pivots=binary_rref(matrix)
    free=[j for j in range(matrix.cols) if j not in pivots]
    answer=zeros(matrix.cols,len(free))
    for k,j in enumerate(free):
        answer[j,k]=1
        for i,p in enumerate(pivots):
            answer[p,k]=a[i][j]
    return answer


def binary_complement(kernel,incoming):
    current=incoming.copy()
    rank=len(binary_rref(current)[1])
    kept=[]
    for j in range(kernel.cols):
        trial=current.row_join(kernel[:,j])
        newrank=len(binary_rref(trial)[1])
        if newrank>rank:
            kept.append(kernel[:,j]);current=trial;rank=newrank
    return Matrix.hstack(*kept) if kept else zeros(kernel.rows,0)


def smith_decomposition(matrix):
    diagonal,left,right=smith_normal_decomp(DomainMatrix.from_Matrix(matrix).convert_to(ZZ))
    return diagonal.to_Matrix(),left.to_Matrix(),right.to_Matrix()


def invariant_factors(matrix):
    if matrix.cols==0:
        return []
    diagonal=smith_normal_form(matrix,domain=ZZ)
    return [abs(int(diagonal[i,i])) for i in range(min(diagonal.shape))
            if abs(diagonal[i,i])>1]


def compute(orders,include_presentation=False):
    if len(orders)<3 or any(n<2 or n&(n-1) for n in orders):
        raise ValueError('Need distinguished m plus at least two spectators, all powers of two >=2')
    d4=differential(4,orders);d5=differential(5,orders);d6=differential(6,orders)
    assert d5*d4==zeros(d5.rows,d4.cols)
    assert d6*d5==zeros(d6.rows,d5.cols)
    diagonal,left,right=smith_decomposition(d5)
    rank=sum(diagonal[i,i]!=0 for i in range(min(diagonal.shape)))
    divisors=[abs(int(diagonal[i,i])) for i in range(rank)]
    assert d4.rank()+rank==d5.cols, 'Unexpected rational H5'
    # Normalize the Smith diagonal to positive values by changing left rows.
    for i in range(rank):
        if diagonal[i,i]<0:
            left[i,:]=-left[i,:]
            diagonal[i,i]=-diagonal[i,i]
    transformed=left*sq2_twisted(4,orders)
    obstruction=transformed[rank:,:].applyfunc(lambda x:int(x)%2)
    kernel=binary_kernel(obstruction)
    incoming_cf=sq2_twisted(2,orders)
    assert (obstruction*incoming_cf).applyfunc(lambda x:int(x)%2)==zeros(obstruction.rows,incoming_cf.cols)
    cf=binary_complement(kernel,incoming_cf)
    # Phase classes are labeled by s_i (V^{-1} nu)_i mod s_i.
    incoming_phases=right.inv()*sq2_twisted(3,orders)/2
    incoming_bosonic=zeros(rank,incoming_phases.cols)
    for i,s in enumerate(divisors):
        for j in range(incoming_phases.cols):
            coefficient=s*incoming_phases[i,j]
            assert coefficient.q==1
            incoming_bosonic[i,j]=int(coefficient)%s
    bosonic_relations=Matrix.diag(*divisors).col_join(incoming_bosonic.T)
    carry=(transformed[:rank,:]*cf).applyfunc(lambda x:int(x)%2)
    rows=[]
    for i,s in enumerate(divisors):
        row=[0]*(rank+cf.cols);row[i]=s;rows.append(row)
    for j in range(incoming_bosonic.cols):
        rows.append(list(incoming_bosonic[:,j])+[0]*cf.cols)
    for j in range(cf.cols):
        row=[-int(carry[i,j]) for i in range(rank)]+[0]*cf.cols
        row[rank+j]=2;rows.append(row)
    presentation=Matrix(rows) if rows else zeros(0,0)
    answer={
        'orders':list(orders),'support':len(orders)-1,
        'bosonic':invariant_factors(bosonic_relations),
        'complex_fermion_rank':cf.cols,
        'full_group':invariant_factors(presentation),
        'matrix_shape':list(presentation.shape),
    }
    if include_presentation:
        answer.update({'presentation':presentation.tolist(),
                       'degree4_basis':basis(4,len(orders)),
                       'cf_representatives':cf.tolist(),
                       'bosonic_raw_divisors':divisors,
                       'bosonic_incoming':incoming_bosonic.tolist(),
                       'doubling_carries':carry.tolist()})
    return answer


if __name__=='__main__':
    import json
    parser=ArgumentParser(description=__doc__)
    parser.add_argument('orders',type=int,nargs='+')
    parser.add_argument('--presentation',action='store_true')
    args=parser.parse_args()
    print(json.dumps(compute(tuple(args.orders),args.presentation),indent=2))
