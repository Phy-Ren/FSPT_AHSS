#!/usr/bin/env python3
"""Check the current 3+1D Z4^{f,T} root cochains, including their phases.

The complete physical O5 manifests, including the finite face polynomial,
are evaluated on all 32 C2 bar five-tuples. No classification or cohomology
solver is run. This checker deliberately does not substitute the historical
independent low-degree candidate for the current paired reader coordinate.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
CODE = ROOT / 'formulas/publication_source/reference/d4_input/code'
sys.path.insert(0, str(CODE))
from cochains import C, cup, ds, op, parity, sq
from compact import beta_open, kappa

MANIFESTS = ROOT / 'docs/formulas/term_census/three_dimensional'
SECTORS = ('C', 'CGAMMA', 'CPSI', 'GAMMA', 'GAMMAPSI', 'PSI')
ROOTS = (('p_ip', 1, 0, 0, Fraction(1, 4)),
         ('Majorana', 0, 1, 0, Fraction(1, 4)),
         ('complex_fermion', 0, 0, 1, Fraction(0)),
         ('bosonic', 0, 0, 0, Fraction(1, 2)))


def fraction(value):
    value = Fraction(value) % 1
    return f'{value.numerator}/{value.denominator}'


def fields(edges, has_n, has_u, has_c):
    vertices = [0]
    for edge in edges:
        vertices.append(vertices[-1] ^ edge)

    def m(degree, modulus=2):
        return C(degree, fun=lambda face: int(all(
            vertices[a] != vertices[b] for a, b in zip(face, face[1:]))),
                 mod=modulus)

    n = m(1, None) if has_n else C(1, mod=None)
    u, c = m(2) if has_u else C(2), m(3) if has_c else C(3)
    w, s = m(2), m(1)
    W = w + cup(s, s)
    beta_u = beta_open(u)
    beta_W = ds(W.lift(), s).div(2)
    h = C(1, fun=lambda f: n(f) // 2)
    a, v = n.reduce(2), beta_W.reduce(2)
    second_v = C(3, fun=lambda f: beta_W(f) // 2)
    whole = cup(cup(v, v, 2), a) + cup(cup(s, v), h)
    whole = whole + cup(cup(s, cup(s, v, 1)), a)
    values = {
        r'\bar n_1': a, r'\widetilde n_1': h,
        r'\overline{\lfloor n_1/4\rfloor}': C(1, fun=lambda f: n(f) // 4),
        r'\check n_2': u, 'n_3': c, 'n_1': n,
        r'\check\omega_2': W, r'\omega_2': w, 's_1': s,
        r'\overline{\beta\omega_2}': w.lift().d().div(2).reduce(2),
        r'\beta^\circ\check n_2': beta_u,
        r'\overline{\beta^\circ\check n_2}': beta_u.reduce(2),
        r'\beta_{s_1}\check\omega_2': beta_W,
        r'\overline{\check\omega_2\bar n_1}': cup(W, a),
        r'\overline{(\overline{\beta_{s_1}\check\omega_2}\cup_2\overline{\beta_{s_1}\check\omega_2})\bar n_1+s_1\overline{\beta_{s_1}\check\omega_2}\widetilde n_1+s_1(s_1\cup_1\overline{\beta_{s_1}\check\omega_2})\bar n_1}': whole,
        r'\overline{\widetilde{\beta_{s_1}\check\omega_2}\bar n_1^2}': cup(second_v, cup(a, a)),
    }
    return m, n, u, c, w, s, values


def zero_on_simplex(cochain, vertices):
    return all(cochain(face) == 0
               for face in combinations(range(vertices), cochain.deg + 1))


def integer_zero_witness(expression, values, vertices):
    """Certify zero without assuming a transport for a nonzero integer cup.

    Every higher-denominator source term in these four roots has a zero
    factor on the entire simplex. Thus its value is zero with the specified
    local system, independently of the transport sign on a nonzero factor.
    This is a restricted zero certificate, not a general integer AST engine.
    """
    if 'physical_expression' in expression:
        return zero_on_simplex(values[expression['physical_expression']], vertices)
    operation = expression['operation']
    if operation == 'integer_cup':
        return any(integer_zero_witness(arg, values, vertices)
                   for arg in expression['arguments'])
    if operation == 'twisted_integer_differential':
        return integer_zero_witness(expression['argument'], values, vertices)
    raise ValueError(operation)


def source_sector(data, values, top):
    half = data['half_phase']
    inputs = [values[row['physical_expression']] for row in half['input_cochains']]
    assert all(a.deg == row['degree'] and a.mod == 2
               for a, row in zip(inputs, half['input_cochains']))
    # Integer labels above nine must remain a sequence, not a decimal string.
    words = sum(op(row['word'], *(inputs[i] for i in row['input_indices']))(top)
                for row in half['ms_terms']) % 2
    faces = 0
    polynomial = data['physical_binary_face_polynomial']
    if polynomial:
        atoms = [values[row['physical_expression']](row['face'])
                 for row in polynomial['factor_alphabet']]
        faces = sum(all(atoms[i] for i in monomial)
                    for monomial in polynomial['monomials']) % 2
    zero_terms = []
    for term in data['other_phase_terms']:
        zero_terms.append(integer_zero_witness(term['expression'], values, len(top)))
    for term in data['signed_integer_face_terms']:
        zero_terms.append(any(values[factor['physical_expression']](factor['face']) == 0
                              for factor in term['integer_factors']))
    assert all(zero_terms), 'A nonzero integer term requires full signed evaluation.'
    return {'MS_parity': words, 'physical_face_parity': faces,
            'higher_denominator_terms_certified_zero': len(zero_terms),
            'phase': fraction(Fraction(words ^ faces, 2))}


def self_stacking_check():
    """Specialize the already verified current self laws before integer gauge."""
    certificate = json.loads((ROOT / 'docs/formulas/coefficients/three_dimensional_canonical_self_stacking.json').read_text())
    result = {}
    for name, has_n, has_u, has_c, nu in ROOTS:
        rows = []
        for edges in product((0, 1), repeat=4):
            m, n, u, c, w, s, _ = fields(edges, has_n, has_u, has_c)
            top = tuple(range(5))
            N3 = sq(u, 1) + u.d() + cup(s, u)
            if has_n:
                inputs = {'s': s, 'w': w, 'u_root': u, 'c_root': c}
                mask = sum(inputs[v['field']](v['face']) << i
                           for i, v in enumerate(certificate['variables']))
                numerator = sum(coefficient for monomial, coefficient in
                                certificate['reference_total_phase_mod16']
                                if monomial & mask == monomial) % 16
                correction = Fraction(numerator, 16)
                sectors = {sector: sum(coefficient for monomial, coefficient in terms
                                      if monomial & mask == monomial) % 16
                           for sector, terms in certificate['reference_sector_phases_mod16'].items()}
                assert sum(sectors.values()) % 16 == numerator
            else:
                b = beta_open(u)
                lower = kappa(u, w, s)
                half = cup(c, c, 2) + cup(lower, c, 3)
                half += cup(cup(w, s, 1), u) + cup(b.reduce(2), cup(s, u), 2)
                half += cup(s, N3) + cup(s, cup(cup(s, u), u, 2)) + cup(u, u)
                quarter = cup(b, b, 2) + cup(s.lift(), b.reduce(2).lift()) - lower.lift()
                correction = Fraction(half(top), 2) + Fraction(quarter(top), 4)
            rows.append({'tuple': list(edges), 'E4': fraction(correction),
                         'N3': N3((0, 1, 2, 3)),
                         'output_phase': fraction(2 * nu * m(4)(top) + correction)})
        expected = {'p_ip': Fraction(1, 4), 'Majorana': Fraction(1, 2),
                    'complex_fermion': Fraction(1, 2), 'bosonic': Fraction(0)}[name]
        assert all(row['E4'] == fraction(expected * all(row['tuple'])) for row in rows)
        result[name] = {'E4_coefficient': fraction(expected), 'values': rows,
                        'output_phase_coefficient': rows[-1]['output_phase']}
    return result


def check():
    index = json.loads((MANIFESTS / 'INDEX.json').read_text())
    hashes = {row['file']: row['sha256'] for row in index['files']}
    data = {}
    pins = {}
    for sector in SECTORS:
        path = MANIFESTS / f'O5_{sector}_TERMS.json'
        digest = hashlib.sha256(path.read_bytes()).hexdigest()
        assert digest == hashes[path.name]
        pins[str(path.relative_to(ROOT))] = digest
        data[sector] = json.loads(path.read_text())
    records = {}
    top = tuple(range(6))
    for name, has_n, has_u, has_c, nu in ROOTS:
        rows = []
        for edges in product((0, 1), repeat=5):
            m, n, u, c, w, s, values = fields(edges, has_n, has_u, has_c)
            # Test every face, including degenerate bar tuples. These tests
            # cover all 4 pairs, 8 triples, and 16 four-tuples globally.
            assert zero_on_simplex(ds(n, s), 6)
            O3 = cup(w, n.reduce(2)) + cup(s, cup(n.reduce(2), n.reduce(2)))
            assert zero_on_simplex(u.d() + O3, 6)
            assert zero_on_simplex(c.d() + parity(n, u, w, s), 6)
            sectors = {sector: source_sector(data[sector], values, top)
                       for sector in SECTORS}
            source = sum(Fraction(row['phase']) for row in sectors.values()) % 1
            dnu = ds(m(4, None).scaled(nu), s)(top) % 1
            assert (dnu - source) % 1 == 0
            rows.append({'tuple': list(edges), 'sectors': sectors,
                         'source': fraction(source), 'd_s_nu': fraction(dnu),
                         'residual': fraction(dnu - source)})
        records[name] = {'phase_coefficient': fraction(nu),
                         'source_coefficient': rows[-1]['source'],
                         'nonzero_residual_count': 0, 'values': rows}
    for relative in (
        'docs/formulas/source/equations/three-dimensional--p-ip-decoration--18.tex',
        'docs/formulas/source/equations/three-dimensional--majorana-decoration--14.tex',
        'docs/formulas/source/pages/THREE_DIMENSIONAL_INTEGER_SOURCE_FACES.md',
        'docs/formulas/coefficients/three_dimensional_canonical_self_stacking.json',
        'docs/formulas/source/equations/three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--11.tex',
    ):
        pins[relative] = hashlib.sha256((ROOT / relative).read_bytes()).hexdigest()
    return {'status': 'PASS', 'dimension': '3+1D',
            'symmetry': {'Gf': 'Z4^{f,T}', 'Gb': 'C2', 'omega2': 'm1^2', 's1': 'm1'},
            'phase_convention': 'Current paired physical reader coordinate.',
            'normalization': 'm1^q(g1,...,gq)=product(gj), gj in {0,1}; all tuples included.',
            'five_tuples_checked_per_root': 32,
            'lower_equations': {'d_s_n1': 'PASS all 4 pairs', 'd_n2': 'PASS all 8 triples',
                                'd_n3': 'PASS all 16 four-tuples'},
            'roots': records, 'self_stacking_before_integer_gauge': self_stacking_check(),
            'source_sha256': pins,
            'scope': 'Exact cochain solutions and raw self products in the current reader coordinate. No new classification or claim that a raw integer-root square is already gauge reduced.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path, help='Write the exact cochain receipt.')
    args = parser.parse_args()
    result = check()
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps({'status': result['status'], 'tuples_per_root': 32,
                      'phases': {name: row['phase_coefficient'] for name, row in result['roots'].items()},
                      'sources': {name: row['source_coefficient'] for name, row in result['roots'].items()}}))


if __name__ == '__main__':
    main()
