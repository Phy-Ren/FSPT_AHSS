"""Portable finite-example input encoding and mathematical result projection."""
import json


def gap_literal(value):
    if isinstance(value, bool):
        return 'true' if value else 'false'
    if isinstance(value, str):
        return json.dumps(value, ensure_ascii=True)
    if isinstance(value, list):
        return '[' + ','.join(map(gap_literal, value)) + ']'
    if isinstance(value, dict):
        return 'rec(' + ','.join(k + ':=' + gap_literal(v) for k, v in value.items()) + ')'
    if isinstance(value, int):
        return str(value)
    raise TypeError(type(value))


def selected(data, names):
    return {name: data[name] for name in names if name in data}


def project_result(raw, dimension, model_id):
    """Exclude environment metadata; retain exact mathematical certificates."""
    result = {'schema': 'fspt-finite-example-v1', 'model_id': model_id,
              'spacetime_dimension': str(dimension) + '+1D', 'status': raw['status']}
    if dimension == 4:
        result.update(selected(raw, ['initial', 'layers', 'pipPages', 'incomingPip',
                                    'maps', 'targets', 'nativeCohomology', 'witnesses',
                                    'resolutionDimensions']))
        result['stacking_scope'] = 'associated-graded layers; no general 4+1D stacking extension asserted'
        return result
    if dimension != 3:
        raise ValueError('Supported dimensions are 3+1D and 4+1D.')
    result['layers'] = {'pip': raw['pip']['orders'], 'majorana': raw['majorana'],
                        'complex_fermion': raw['complex_fermion'], 'bosonic': raw['bosonic']}
    result['pipPages'] = raw['pip']['torsion']
    result['ranks'] = raw['ranks']
    result['resolutionDimensions'] = raw['resolution_dimensions']
    stack = raw['stacking']
    lower_fields = ['invariants', 'presentation', 'generators', 'witnesses',
                    'smithColumnTransform', 'smithDiagonal', 'smithRowTransform']
    result['stacking'] = {'known_lower_formula': 'complete manuscript-aligned U4 in 3+1D',
                         'lower': selected(stack['lower'], lower_fields)}
    if 'h0IncomingQuotient' in stack:
        result['stacking']['h0_incoming_quotient'] = {
            k: v for k, v in stack['h0IncomingQuotient']['backgroundQuotient'].items()
            if k != 'preQuotientLower'}
        result['stacking']['lower_before_h0'] = selected(stack['lowerBeforeH0Incoming'], lower_fields)
    family = raw.get('publicPipExtension')
    if family is None:
        family = raw.get('stackingScope', {}).get('conservativePipFamily')
    if family is None:
        family = stack.get('pipExtensionCertificate')
    if raw['pip']['orders']:
        if family is None:
            raise ValueError('A surviving p+ip layer requires its complete lower-carry family.')
        options = family['invariantOptions']
        result['stacking']['pip_extension'] = family
    else:
        options = [stack['lower']['invariants']]
    result['stacking']['invariant_options'] = options
    result['stacking']['abstract_group_unique'] = len(options) == 1
    if len(options) == 1:
        result['stacking']['invariants'] = options[0]
    return result


def group_signature(result):
    """Basis-independent fields used for portable result comparison."""
    return {'layers': result['layers'],
            'stacking': result.get('stacking', {}).get('invariant_options')}
