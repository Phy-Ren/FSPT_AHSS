#!/usr/bin/env python3
"""Verify the 25-to-7 MS source exchange identity on universal cochains.

The old word list is frozen here as the independent comparison expression.
The certificate uses arbitrary Majorana and CF cochains and closed symmetry
backgrounds on a five-simplex. No physical source equation, sampling, or
cohomology-class test is used: the entire binary cochain is identical.
"""
from itertools import combinations
import json
import verify_three_dimensional_canonical_self_stacking as m


def run():
    m.faces = lambda degree: tuple(combinations(range(6), degree + 1))
    labels = []

    def free(name, degree, closed=False):
        values = {}
        for face in m.faces(degree):
            if not closed or face[0] == 0:
                values[face] = m.Polynomial({1 << len(labels): 1}, 2)
                labels.append((name, face))
        if closed:
            for face in m.faces(degree):
                if face[0]:
                    values[face] = sum(values[(0,) + face[:j] + face[j+1:]]
                                       for j in range(len(face)))
        return m.Cochain(degree, values)

    u, c = free('check_n2', 2), free('n3', 3)
    w, s = free('omega2', 2, True), free('s1', 1, True)
    A, dc = u.differential(), c.differential()
    old_groups = [
        ((c, w, A), ['121231', '121313']),
        ((w, c, A), ['121323']),
        ((A, c, s, u), ['12312124', '12312142', '12312412',
                       '12312421', '12321242', '12321412', '12321421']),
        ((A, s, c, u), ['12131413', '12134131', '12313413', '12314131']),
        ((c, s, A, u), ['12131413', '12134131', '12134143', '12341431']),
        ((c, s, u, A), ['12131413', '12134131', '12134143', '12341431']),
        ((s, A, c, u), ['12324342', '12343423']),
        ((s, c, u, A), ['12342432']),
    ]
    new_groups = [
        ((dc, w, A), ['1212313']),
        ((dc, s, u, A), ['121341431', '241431341', '124214131',
                        '121431341', '142141314', '142141341']),
    ]
    top = tuple(range(6))

    def evaluate(groups):
        return sum((m.operation(word, *inputs)(top)
                    for inputs, words in groups for word in words),
                   m.Polynomial(0, 2))

    old, new = evaluate(old_groups), evaluate(new_groups)
    omega_residual = evaluate(old_groups[:2]) - evaluate(new_groups[:1])
    signed_residual = evaluate(old_groups[2:]) - evaluate(new_groups[1:])
    residuals = {'omega_part': len(omega_residual.terms),
                 'signed_part': len(signed_residual.terms),
                 'complete_exchange_sum': len((old-new).terms)}
    assert not any(residuals.values()), residuals
    return {'status': 'PASS', 'independent_binary_variables': len(labels),
            'method': 'Exact universal Boolean coefficient identity',
            'old_MS_terms': 25, 'new_MS_terms': 7,
            'new_inputs': [['dn3', 'omega2', 'dcheckn2'],
                           ['dn3', 's1', 'checkn2', 'dcheckn2']],
            'collected_face_coefficients': len(old.terms),
            'residual_coefficients': residuals,
            'closed_backgrounds': ['omega2', 's1'],
            'lower_source_equations_imposed': False,
            'phase_representative_change': False,
            'source_or_stacking_transport_required': False}


if __name__ == '__main__':
    print(json.dumps(run(), indent=2))
