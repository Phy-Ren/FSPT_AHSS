#!/usr/bin/env python3
"""All-exponent certificates for the two-spectator closed factors.

The periodic tensor complex splits into Koszul blocks indexed by ceil(alpha/2).
Changing e_i to z_i=e_i-(N_i/h)e_min gives an explicit Smith basis with every
nonzero entry h=min N_i in that block. Modulo two, the basis changes depend
only on the minimum-order indices. This gives finitely many exhaustive
order signatures, not a finite exponent extrapolation.
"""

from itertools import combinations,product
from sympy import Matrix,zeros,Symbol,Poly,ZZ,expand
try:
    from .supercohomology_blocks import (basis,sq2_twisted,binary_kernel,
                                       binary_complement,invariant_factors,
                                       smith_decomposition)
except ImportError:
    from supercohomology_blocks import (basis,sq2_twisted,binary_kernel,
                                       binary_complement,invariant_factors,
                                       smith_decomposition)


def metadata(alpha):
    return tuple((a+1)//2 for a in alpha)


def alpha_from(k,odd):
    return tuple(2*n-(i in odd) for i,n in enumerate(k))


def projection(degree,orders):
    source=basis(degree,len(orders));positions={a:i for i,a in enumerate(source)}
    blocks=sorted(set(metadata(a) for a in source))
    descriptors=[];rows=[]
    for k in blocks:
        active=[i for i,n in enumerate(k) if n]
        pivot=min(active,key=lambda i:(orders[i],i))
        h=orders[pivot]
        odd_count=2*sum(k)-degree
        if odd_count<1:
            continue
        remaining=[i for i in active if i!=pivot]
        for tail in combinations(remaining,odd_count-1):
            row=[0]*len(source)
            # Signs disappear modulo two. This is contraction with N_i/h,
            # followed by projection to wedges of the z_i.
            for i in active:
                if i not in tail and (orders[i]//h)%2:
                    odd=tuple(sorted((*tail,i)))
                    alpha=alpha_from(k,odd)
                    row[positions[alpha]]^=1
            descriptors.append({'k':k,'pivot':pivot,'tail':tail,'order':h})
            rows.append(row)
    return descriptors,Matrix(rows) if rows else zeros(0,len(source))


def normalized_data(orders):
    descriptors,p5=projection(5,orders)
    _,z6=projection(6,orders)
    t4=sq2_twisted(4,orders)
    obstruction=(z6*t4).applyfunc(lambda x:int(x)%2)
    kernel=binary_kernel(obstruction)
    incoming=sq2_twisted(2,orders)
    assert (obstruction*incoming).applyfunc(lambda x:int(x)%2)==zeros(obstruction.rows,incoming.cols)
    cf=binary_complement(kernel,incoming)
    positions={a:i for i,a in enumerate(basis(6,len(orders)))}
    select=zeros(len(descriptors),t4.rows)
    for i,d in enumerate(descriptors):
        select[i,positions[alpha_from(d['k'],d['tail'])]]=1
    carry=(select*t4*cf).applyfunc(lambda x:int(x)%2)
    incoming_phase=(p5*sq2_twisted(3,orders)).applyfunc(lambda x:int(x)%2)
    return descriptors,incoming_phase,carry


def relation_matrix(descriptors,incoming,carry,orders_override=None):
    norms=orders_override or [d['order'] for d in descriptors]
    rank=len(norms);rows=[]
    for i,n in enumerate(norms):
        row=[0]*(rank+carry.cols);row[i]=n;rows.append(row)
    for j in range(incoming.cols):
        rows.append([n*incoming[i,j]/2 for i,n in enumerate(norms)]+[0]*carry.cols)
    for j in range(carry.cols):
        row=[-carry[i,j] for i in range(rank)]+[0]*carry.cols
        row[rank+j]=2;rows.append(row)
    return Matrix(rows)


def eliminate_cf(matrix,cf_count):
    """Remove the primitive CF relations by unimodular unit elimination."""
    a=matrix.copy()
    for _ in range(cf_count):
        relation=a.rows-1
        pivot=next(j for j in range(a.cols) if a[relation,j] in (1,-1))
        if a[relation,pivot]==-1:
            a[relation,:]=-a[relation,:]
        for i in range(a.rows-1):
            coefficient=a[i,pivot]
            a[i,:]=a[i,:]-coefficient*a[relation,:]
        a.row_del(relation);a.col_del(pivot)
    return a.applyfunc(expand)


def polynomial_division(a,b,t):
    q,r=Poly(a,t,domain=ZZ).div(Poly(b,t,domain=ZZ))
    return q.as_expr(),r.as_expr()


def symbolic_smith_by_dividing_pivots(matrix,t):
    """Exact ZZ[t] unimodular reduction for the small matrices in this proof."""
    a=matrix.copy();left=Matrix.eye(a.rows);right=Matrix.eye(a.cols)
    diagonal=[]
    for k in range(min(a.shape)):
        entries=[(i,j) for i in range(k,a.rows) for j in range(k,a.cols) if a[i,j]!=0]
        if not entries:
            break
        def priority(ij):
            p=Poly(a[ij],t,domain=ZZ)
            return (p.degree(),abs(int(p.LC())),str(p.as_expr()))
        entries.sort(key=priority)
        selected=None
        for i,j in entries:
            p=a[i,j]
            if all(polynomial_division(a[u,v],p,t)[1]==0
                   for u in range(k,a.rows) for v in range(k,a.cols)):
                selected=(i,j);break
        if selected is None:
            raise ValueError(('No dividing pivot',k,a[k:,k:]))
        i,j=selected
        a.row_swap(k,i);left.row_swap(k,i)
        a.col_swap(k,j);right.col_swap(k,j)
        p=a[k,k]
        if Poly(p,t,domain=ZZ).LC()<0:
            a[k,:]=-a[k,:];left[k,:]=-left[k,:];p=-p
        for i in range(k+1,a.rows):
            quotient,remainder=polynomial_division(a[i,k],p,t)
            assert remainder==0
            a[i,:]=a[i,:]-quotient*a[k,:]
            left[i,:]=left[i,:]-quotient*left[k,:]
        for j in range(k+1,a.cols):
            quotient,remainder=polynomial_division(a[k,j],p,t)
            assert remainder==0
            a[:,j]=a[:,j]-quotient*a[:,k]
            right[:,j]=right[:,j]-quotient*right[:,k]
        a=a.applyfunc(expand);left=left.applyfunc(expand);right=right.applyfunc(expand)
        diagonal.append(p)
    assert (left*matrix*right-a).applyfunc(expand)==zeros(*a.shape)
    assert left.det() in (1,-1) and right.det() in (1,-1)
    return diagonal,left,right,a


def signature(orders):
    return (tuple((a>b)-(a<b) for a in orders for b in orders),
            tuple(n==2 for n in orders))


def all_signatures(spectator_count=2):
    representatives={}
    values=tuple(2**i for i in range(1,spectator_count+3))
    for orders in product(values,repeat=spectator_count+1):
        if list(orders[1:])!=sorted(orders[1:]):
            continue
        representatives.setdefault(signature(orders),orders)
    return list(representatives.values())


def certificate(orders):
    m,g,n2=orders
    descriptors,incoming,carry=normalized_data(orders)
    assert len(descriptors)==6
    t=Symbol('t',integer=True,positive=True)
    if g<=m:
        norms=[2]*6
        matrix=eliminate_cf(relation_matrix(descriptors,incoming,carry,norms),carry.cols)
        diagonal,left,right=smith_decomposition(matrix)
        result=[abs(int(diagonal[i,i])) for i in range(6)]
        expected=([1,1,1,2,2,4] if g==n2 else
                  [1,1,2,2,4,4] if g<m else [1,1,2,2,2,4])
        assert result==expected,(orders,result,expected)
        serial=lambda a:[[int(v) for v in row] for row in a.tolist()]
        return {'orders':orders,'scale':'g/2','normalized_diagonal':result,
                'matrix':serial(matrix),'left':serial(left),'right':serial(right)}
    norms=[4*t if d['order']==g else 2 for d in descriptors]
    matrix=eliminate_cf(relation_matrix(descriptors,incoming,carry,norms),carry.cols)
    diagonal,left,right,reduced=symbolic_smith_by_dividing_pivots(matrix,t)
    expected=[1,2,2,2,2*t,4*t if g==n2 else 8*t]
    assert diagonal==expected,(orders,diagonal,expected)
    serial=lambda a:[[str(v) for v in row] for row in a.tolist()]
    return {'orders':orders,'scale':'m/2','parameter':'g/m=2t',
            'normalized_diagonal':[str(v) for v in diagonal],
            'matrix':serial(matrix),'left':serial(left),'right':serial(right)}


def certificate_three(orders):
    m,*spectators=orders
    g=min(spectators);unique=spectators.count(g)==1
    descriptors,incoming,carry=normalized_data(orders)
    assert len(descriptors)==7 and carry.cols==int(unique)
    t=Symbol('t',integer=True,positive=True)
    if g<=m:
        matrix=eliminate_cf(relation_matrix(descriptors,incoming,carry,[2]*7),carry.cols)
        diagonal,left,right=smith_decomposition(matrix)
        result=[abs(int(diagonal[i,i])) for i in range(7)]
        expected=[1]+[2]*(6-unique)+[4]*unique
        assert result==expected,(orders,result,expected)
        serial=lambda a:[[int(v) for v in row] for row in a.tolist()]
        return {'orders':orders,'scale':'g/2','normalized_diagonal':result,
                'matrix':serial(matrix),'left':serial(left),'right':serial(right)}
    # Here the incoming order-two relation is identically zero.
    assert incoming==zeros(*incoming.shape)
    norms=[2*t if d['order']==g else 1 for d in descriptors]
    matrix=eliminate_cf(relation_matrix(descriptors,incoming,carry,norms),carry.cols)
    diagonal,left,right,reduced=symbolic_smith_by_dividing_pivots(matrix,t)
    expected=[1]*3+[2*t]*(4-unique)+[4*t]*unique
    assert diagonal==expected,(orders,diagonal,expected)
    serial=lambda a:[[str(v) for v in row] for row in a.tolist()]
    return {'orders':orders,'scale':'m','parameter':'g/m=2t',
            'normalized_diagonal':[str(v) for v in diagonal],
            'matrix':serial(matrix),'left':serial(left),'right':serial(right)}


if __name__=='__main__':
    import json
    from pathlib import Path
    for support,method in [(2,certificate),(3,certificate_three)]:
        certificates=[method(orders) for orders in all_signatures(support)]
        output=Path(__file__).parent/'data'/f'support{support}_symbolic_certificates.json'
        output.write_text(json.dumps({'method':'Exhaustive weak-order signatures and exact unimodular polynomial reductions',
                                      'certificates':certificates},indent=2)+'\n')
        print('Support',support,': certified all',len(certificates),'exhaustive order signatures.')
