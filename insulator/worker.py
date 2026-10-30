"""Persistent exact JSONL transport for local simplex formula evaluation.

It has no finite-group assumption: GAP supplies face values and vertex signs,
so the same protocol works with finite, point, and infinite wallpaper groups.
Every request is independent; a failed request does not poison the process.
"""
from __future__ import annotations

from fractions import Fraction
from functools import lru_cache
from itertools import combinations
import json
import sys

from . import api as U
from .notation import character_signs, migrate_legacy_request, LEGACY_NOTATION


def exact(value):
    if isinstance(value, bool) or not isinstance(value, (int, str)):
        raise TypeError('Wire scalars must be integers or exact rational strings.')
    return Fraction(value)


def decode(data, N, degree, sign):
    """Accept sparse face dictionaries or dense lexicographic face arrays."""
    if isinstance(data, dict) and 'values' in data:
        if data.get('degree', degree) != degree:
            raise ValueError('The explicit cochain degree disagrees with its field.')
        if tuple(data.get('sign', sign)) != tuple(sign):
            raise ValueError('The explicit coefficient action disagrees with its field.')
        data = data['values']
    if isinstance(data, list):
        faces = list(combinations(range(N + 1), degree + 1))
        if len(data) != len(faces):
            raise ValueError('A dense cochain array must contain every lexicographic face.')
        entries = dict(zip(faces, map(exact, data)))
    elif isinstance(data, dict):
        entries = {}
        for key, value in data.items():
            face = tuple(int(x) for x in key.split(','))
            if len(face) != degree + 1 or tuple(sorted(set(face))) != face:
                raise ValueError('Cochain faces must be strictly increasing and have the right degree.')
            if not all(0 <= vertex <= N for vertex in face):
                raise ValueError('A cochain face is outside the simplex.')
            entries[face] = exact(value)
    else:
        raise TypeError('A cochain must be a face dictionary or lexicographic array.')
    return U.Cochain(N, degree, entries, sign)


def encode(cochain, top=False):
    if top:
        if cochain.N != cochain.p:
            raise ValueError('return:top requires simplex_dimension equal to the output degree.')
        return str(Fraction(cochain(tuple(range(cochain.N + 1)))))
    result = {'degree': cochain.p, 'sign': list(cochain.tw),
              'values': {','.join(map(str, f)): str(Fraction(v))
                         for f, v in cochain.v.items() if v}}
    if cochain.p == cochain.N:
        result['top'] = str(Fraction(cochain(tuple(range(cochain.N + 1)))))
    return result


def _evaluate(request):
    if request['op'] == 'ping':
        return {'protocol': 2, 'schema_version': 2, 'theory': 'U1f-insulator',
                'characters': {'s': 'antiunitarity', 'r': 'charge reversal', 'rho': 'r XOR s; circle action'},
                'convention': 'sheet-linear',
                'cubic': '1/6', 'epsilon': 0, 'dimensions': [2, 3, 4]}
    if request['op'] == 'batch':
        return [evaluate(item) for item in request['requests']]
    d = request.get('dimension', 2)
    if d not in (2, 3, 4):
        raise ValueError('dimension must be 2, 3, or 4.')
    N = request['simplex_dimension']
    if not isinstance(N, int) or N < 0:
        raise ValueError('simplex_dimension must be a nonnegative integer.')
    s, r, rho = character_signs(request, N + 1)
    symmetry = U.Symmetry(decode(request.get('omega', {}), N, 2, rho),
                          U.char(N, s).ret(s), U.char(N, r).ret(r))
    get = lambda key, degree, sign: decode(request.get(key, {}), N, degree, sign)
    sheet = get('sheet', d - 2, s)
    charge = get('charge', d, r)
    op = request['op']
    validate = request.get('validate', True)
    if not isinstance(validate, bool):
        raise ValueError('validate must be a Boolean.')
    if op in ('source', 'd4'):
        result = U.source(symmetry, d, sheet, charge, validate=validate)
    elif op in ('integer_obstruction', 'd3'):
        result = U.integer_obstruction(symmetry, d, sheet)
    elif op in ('charge_source', 'd2'):
        result = U.charge_source(symmetry, get('charge', request.get('charge_degree', d), r))
    elif op == 'charge_product':
        p = request.get('charge_degree', d)
        result = U.charge_product(symmetry, get('charge', p, r), get('charge_prime', p, r))
    elif op == 'charge_gauge':
        p = request.get('charge_degree', d)
        result = U.charge_gauge(symmetry, get('charge', p, r), get('charge_parameter', p - 1, r))
    elif op in ('product', 'integer_product', 'lower_exchange'):
        sheet_prime, charge_prime = get('sheet_prime', d - 2, s), get('charge_prime', d, r)
        if op == 'integer_product':
            result = U.integer_product(symmetry, d, sheet, sheet_prime)
        elif op == 'lower_exchange':
            result = U.lower_exchange(symmetry, d, sheet, sheet_prime)
        else:
            result = dict(zip(('sheet', 'charge', 'phase'), U.product(
                symmetry, d, sheet, charge, sheet_prime, charge_prime, validate=validate)))
    elif op == 'gauge':
        u = None if d == 2 else get('sheet_parameter', d - 3, s)
        v = get('charge_parameter', d - 1, r)
        result = dict(zip(('sheet', 'charge', 'phase'), U.gauge(
            symmetry, d, sheet, charge, u, v, validate=validate)))
    elif op in ('background_lift', 'background_section'):
        kind = 'lift' if op == 'background_lift' else 'section'
        parameter = get('background_parameter', 2 if kind == 'lift' else 1, rho)
        new_sym, k, n, phase = U.background_change(symmetry, d, sheet, charge, parameter,
                                                  kind, validate=validate)
        result = {'omega': new_sym.omega2_real, 'sheet': k, 'charge': n, 'phase': phase}
    elif op == 'differential':
        sign = {'s': s, 'r': r, 'rho': rho,
                'trivial': [0] * (N + 1)}[request.get('coefficient', 'trivial')]
        result = get('cochain', request['degree'], sign).d()
    else:
        raise ValueError('Unknown formula operation: ' + str(op))
    if isinstance(result, dict) and request.get('output_component'):
        result = result[request['output_component']]
    top = request.get('return') == 'top'
    if isinstance(result, dict):
        if top:
            raise ValueError('Select output_component before requesting return:top.')
        return {key: encode(value) for key, value in result.items()}
    return encode(result, top)


@lru_cache(maxsize=4096)
def _cached_evaluation(canonical_request):
    return _evaluate(json.loads(canonical_request))


def evaluate(request):
    """Reuse identical local data independently of group-tuple names and IDs."""
    version = request.get('schema_version', 2)
    if type(version) is not int or version not in (1, 2):
        raise ValueError('schema_version must be the integer 2, or explicit legacy version 1.')
    if request.get('schema_version') == 1:
        if request.get('notation') != LEGACY_NOTATION:
            raise ValueError('schema_version=1 requires notation="legacy-charge-rho".')
        request = migrate_legacy_request(request)
    if request.get('op') == 'cache_info':
        return dict(_cached_evaluation.cache_info()._asdict())
    if request.get('op') == 'cache_clear':
        _cached_evaluation.cache_clear()
        return {'cleared': True}
    mathematical_request = {key: value for key, value in request.items()
                            if key not in ('id', 'response_format')}
    canonical = json.dumps(mathematical_request, sort_keys=True, separators=(',', ':'))
    return _cached_evaluation(canonical)


def gap_literal(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if value is None:
        return 'fail'
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=True)
    if isinstance(value, (int, float)):
        return str(value)
    if isinstance(value, list):
        return '[' + ','.join(gap_literal(x) for x in value) + ']'
    if isinstance(value, dict):
        return 'rec(' + ','.join('(' + json.dumps(str(k)) + '):=' + gap_literal(v)
                                 for k, v in value.items()) + ')'
    raise TypeError(type(value).__name__)


def input_lines(stream):
    """A GAP PTY closes with EIO instead of ordinary pipe EOF on some systems."""
    while True:
        try:
            line = stream.readline()
        except OSError as error:
            if error.errno == 5:
                return
            raise
        if not line:
            return
        yield line


def main(stdin=None, stdout=None):
    stdin, stdout = stdin or sys.stdin, stdout or sys.stdout
    for line in input_lines(stdin):
        request = {}
        try:
            request = json.loads(line)
            if not isinstance(request, dict):
                request = {}
                raise TypeError('A formula request must be a JSON object.')
            response = {'id': request.get('id'), 'ok': True, 'result': evaluate(request)}
        except Exception as error:
            response = {'id': request.get('id'), 'ok': False,
                        'error': type(error).__name__ + ': ' + str(error)}
        if request.get('response_format') == 'gap':
            text = gap_literal(response) + ';'
        else:
            text = json.dumps(response, separators=(',', ':'))
        try:
            stdout.write(text + '\n')
            stdout.flush()
        except BrokenPipeError:
            return


if __name__ == '__main__':
    main()
