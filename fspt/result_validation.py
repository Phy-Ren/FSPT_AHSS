"""Independent integer presentation checks for a completed FSPT result.

Smith reduction and column Hermite reduction use SymPy, independently of GAP.
This checks quotient arithmetic and filtration, not local cochain identities or
physical correctness of the supplied obstruction and stacking formulas.
"""
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form


def invariant_factors(rows, width):
    if not width:
        return []
    matrix = Matrix(rows) if rows else Matrix.zeros(0, width)
    diagonal = smith_normal_form(matrix, domain=ZZ)
    entries = [abs(int(diagonal[i, i])) for i in range(min(diagonal.shape))]
    rank = sum(x != 0 for x in entries)
    return [0] * (width - rank) + [x for x in entries if x > 1]


def verify_result(data):
    if data.get('status') != 'computed':
        raise ValueError('Only completed results can be accepted')
    generators, rows = data['generators'], data['presentation']
    width = len(generators)
    assert all(len(row) == width for row in rows)
    assert [g['layer'] for g in generators] == sorted(g['layer'] for g in generators)
    actual = invariant_factors(rows, width)
    assert actual == data['invariants'], (data['model'], actual, data['invariants'])
    if width:
        matrix = Matrix(rows) if rows else Matrix.zeros(0, width)
        left, right = Matrix(data['smithRows']), Matrix(data['smithColumns'])
        assert abs(left.det()) == abs(right.det()) == 1
        diagonal = left * matrix * right
        for i in range(diagonal.rows):
            for j in range(diagonal.cols):
                expected = data['smithDiagonal'][i] if i == j and i < len(data['smithDiagonal']) else 0
                assert diagonal[i, j] == expected
        hnf = hermite_normal_form(matrix.T)
        padded = [[0] * width for _ in range(width)]
        pivots = []
        for column in range(hnf.cols):
            pivot = max(i for i in range(width) if hnf[i, column])
            pivots.append(pivot)
            padded[pivot] = [int(hnf[i, column]) for i in range(width)]
        assert pivots == sorted(set(pivots))
    else:
        padded = []
    boundaries = [sum(g['layer'] < k for g in generators) for k in range(5)]
    filtration = []
    for k, name in enumerate(('bosonic', 'complex_fermion', 'majorana', 'pip')):
        start, end = boundaries[k:k + 2]
        filtration.append(dict(layer=name,
            quotient_invariants=invariant_factors([r[start:end] for r in padded[start:end]], end - start),
            subgroup_invariants=invariant_factors([r[:end] for r in padded[:end]], end)))
    return dict(model=data['model'], dimension=data['dimension'], invariant_factors=actual,
                smith_and_unimodular_certificates=True, final_filtration=filtration)
