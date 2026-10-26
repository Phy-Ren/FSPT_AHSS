#!/usr/bin/env python3
"""Unrestricted Smith certificates for final bosonic decoration layers."""
from sympy import Matrix,Symbol,zeros
try:
    from .koszul_stabilization import normalized_data,all_signatures,symbolic_smith_by_dividing_pivots
    from .supercohomology_blocks import smith_decomposition,binary_kernel,sq2_twisted
except ImportError:
    from koszul_stabilization import normalized_data,all_signatures,symbolic_smith_by_dividing_pivots
    from supercohomology_blocks import smith_decomposition,binary_kernel,sq2_twisted

def certificate(orders):
    m,*ns=orders;r=len(ns);g=min(ns);unique=ns.count(g)==1
    desc,incoming,carry=normalized_data(orders)
    t=Symbol('t',integer=True,positive=True)
    assert binary_kernel(sq2_twisted(2,orders)).cols==0
    assert binary_kernel(sq2_twisted(3,orders)).cols==int(r==1)
    if r==1:
        assert carry.cols==1
        if g<=m:
            scale='N/2';norms=[2]*3
            expected=[1,1 if g==m else 2,2]
        else:
            scale='m/2';norms=[4*t if d['order']==g else 2 for d in desc]
            expected=[1,2,2*t]
    elif r==2:
        assert carry.cols==1+int(unique and g<m)
        if g<=m:
            scale='g/2';norms=[2]*6
            expected=[1]*(3-unique)+[2]*(3+unique)
        else:
            scale='m/2';norms=[4*t if d['order']==g else 2 for d in desc]
            expected=[1,2,2,2,2*t,4*t if unique else 2*t]
    elif r==3:
        assert carry.cols==int(unique)
        if g<=m:
            scale='g/2';norms=[2]*7;expected=[1]+[2]*6
        else:
            scale='m';norms=[2*t if d['order']==g else 1 for d in desc]
            expected=[1]*3+[2*t]*4
    else:raise ValueError('Symbolic certificates cover one through three spectators')
    matrix=Matrix.diag(*norms).col_join(Matrix([[norms[i]*incoming[i,j]/2 for i in range(len(norms))] for j in range(incoming.cols)]))
    if g<=m:
        diagonal,left,right=smith_decomposition(matrix)
        result=[abs(int(diagonal[i,i])) for i in range(matrix.cols)]
    else:
        result,left,right,_=symbolic_smith_by_dividing_pivots(matrix,t)
    assert result==expected,(orders,result,expected)
    assert left.det() in (1,-1) and right.det() in (1,-1)
    serial=lambda a:[[str(x) for x in row] for row in a.tolist()]
    return {'orders':list(orders),'scale':scale,'parameter':'g/m=2t' if g>m else None,
            'bosonic_matrix':serial(matrix),'left':serial(left),'right':serial(right),
            'normalized_diagonal':[str(x) for x in result],
            'complex_fermion_rank':carry.cols,'majorana_primary_kernel_rank':int(r==1)}

def all_certificates():
    return [certificate(ns) for r in [1,2,3] for ns in all_signatures(r)]

if __name__=='__main__':
    import json
    from pathlib import Path
    rows=all_certificates()
    (Path(__file__).parent/'data/nonsplit_layer_certificates.json').write_text(json.dumps({'certificates':rows},indent=2)+'\n')
    print(f'Certified {len(rows)} exhaustive order patterns for the final decoration layers.')
