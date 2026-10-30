"""Versioned symmetry characters: s antiunitary, r charge, rho circle."""
from copy import deepcopy

SCHEMA_VERSION = 2
LEGACY_NOTATION = 'legacy-charge-rho'


def _xor_values(a, b):
    if isinstance(a, (list, tuple)) and isinstance(b, (list, tuple)):
        if len(a) != len(b):
            raise ValueError('Character arrays have different lengths.')
        return [_xor_values(x, y) for x, y in zip(a, b)]
    if type(a) is int and type(b) is int and a in (0, 1) and b in (0, 1):
        return a ^ b
    # Signed C2 report metadata uses the named binary character alpha.
    if a in ('0', 'alpha') and b in ('0', 'alpha'):
        return '0' if a == b else 'alpha'
    raise ValueError('Characters must be bits, bit arrays, or the C2 metadata labels 0/alpha.')


def migrate_legacy_input(record):
    """Explicitly translate one historical background without changing it."""
    version = record.get('schema_version')
    if 'r' in record or (version is not None and (type(version) is not int or version != 1)):
        raise ValueError('Input is not an unambiguous legacy charge-rho record.')
    if record.get('notation', LEGACY_NOTATION) != LEGACY_NOTATION:
        raise ValueError('The supplied notation tag is not legacy-charge-rho.')
    if 's' not in record or 'rho' not in record:
        raise ValueError('Legacy background requires s and its old charge rho.')
    result = deepcopy(record)
    result['r'] = result['rho']
    result['rho'] = _xor_values(result['r'], result['s'])
    if 'circle_action' in result and result['circle_action'] != result['rho']:
        raise ValueError('Legacy circle_action disagrees with the two characters.')
    result.pop('notation', None)
    result['schema_version'] = SCHEMA_VERSION
    return result


def legacy_metadata_view(value):
    """Explicit read-only view of archived results in current notation.

    Collectors opt in at their historical-file boundary.  This does not rewrite
    any record, hash, witness, or calculation output on disk.
    """
    if isinstance(value, list):
        return [legacy_metadata_view(item) for item in value]
    if not isinstance(value, dict):
        return value
    result = {key: legacy_metadata_view(item) for key, item in value.items()}
    if 's' in result and 'rho' in result and 'r' not in result:
        result = migrate_legacy_input(result)
    # These are the two recorded historical schemas, not a free-text rewrite.
    if result.get('coefficientActions') == ['s', 's', 'rho', 's']:
        result['coefficientActions'] = ['s', 's', 'r', 's']
    elif result.get('coefficientActions') == ['CI: s1', 'charge: rho1', 'extension: rho1+s1', 'phase: s1']:
        result['coefficientActions'] = ['CI: s1', 'charge: r1', 'extension: rho1', 'phase: s1']
    return result


def character_signs(record, length):
    """Validate canonical vertex arrays; derive an omitted circle character."""
    version = record.get('schema_version', SCHEMA_VERSION)
    if type(version) is not int or version != SCHEMA_VERSION:
        raise ValueError('Use schema_version=2 with s,r (rho optional); explicitly migrate legacy charge-rho inputs.')
    signs = {}
    for name in ('s', 'r'):
        if name not in record:
            raise ValueError('Canonical symmetry input requires ' + name + '.')
        values = record[name]
        if not isinstance(values, (list, tuple)) or len(values) != length:
            raise ValueError(name + ' must contain one bit per vertex.')
        if any(type(bit) is not int or bit not in (0, 1) for bit in values):
            raise ValueError(name + ' must contain integer bits 0 or 1.')
        signs[name] = list(values)
    signs['rho'] = [r ^ s for r, s in zip(signs['r'], signs['s'])]
    for name in ('rho', 'circle_action'):
        if name in record and (not isinstance(record[name], (list, tuple))
                               or list(record[name]) != signs['rho']
                               or any(type(x) is not int for x in record[name])):
            raise ValueError(name + ' must equal r XOR s at every vertex.')
    return signs['s'], signs['r'], signs['rho']


def migrate_legacy_request(request):
    """Return a new v2 request; the caller explicitly identifies old rho=charge.

    Historical input dictionaries and files are never modified.  Calling this
    function is the opt-in for an unversioned historical request.
    """
    result = deepcopy(request)
    version = result.get('schema_version')
    if version is not None and (type(version) is not int or version != 1):
        raise ValueError('Only legacy/unversioned requests can be migrated.')
    if result.get('notation', LEGACY_NOTATION) != LEGACY_NOTATION:
        raise ValueError('The supplied notation tag is not legacy-charge-rho.')
    if 'r' in result:
        raise ValueError('Legacy request already contains r; its convention is ambiguous.')
    if result.get('op') == 'batch':
        result['requests'] = [migrate_legacy_request(x) for x in result['requests']]
    elif result.get('op') not in ('ping', 'cache_info', 'cache_clear'):
        length = result['simplex_dimension'] + 1
        result['s'] = result.get('s', [0] * length)
        result['r'] = result.pop('rho', [0] * length)
        result['rho'] = [r ^ s for r, s in zip(result['r'], result['s'])]
        if result.get('op') == 'differential':
            result['coefficient'] = {'rho': 'r', 'extension': 'rho'}.get(
                result.get('coefficient'), result.get('coefficient', 'trivial'))
    result.pop('notation', None)
    result['schema_version'] = SCHEMA_VERSION
    if 'simplex_dimension' in result:
        character_signs(result, result['simplex_dimension'] + 1)
    return result
