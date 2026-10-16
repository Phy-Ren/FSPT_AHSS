"""Replay saved abelian native lattice and gauge witnesses, without GAP."""
from fractions import Fraction
from itertools import combinations
from math import prod
from sympy import Matrix
from sympy.matrices.normalforms import hermite_normal_form
from insulator.e8_h1 import saturated_kernel
from insulator.e8_pointgroup import presentation_invariants


def signature(value):
    return {key: value[key] for key in ('torsion', 'freeRank')}


def verify(classification):
    c = classification
    ns = len(c['group']['factors'])
    np = len(c['cohomology']['phase'])
    nq = len(c['cohomology']['charge'])
    size = c['presentationGeneratorCount']
    names = ([f'phase_{i+1}' for i in range(np)] + [f'charge_{i+1}' for i in range(nq)]
             + [f'CI_{i+1}' for i in range(ns)] + [f'E8_{i+1}' for i in range(ns)])
    perm = c['outputColumnPermutation']
    expected_perm = (list(range(np+nq+ns+1, size+1)) + list(range(np+nq+1, np+nq+ns+1))
                     + list(range(np+1, np+nq+1)) + list(range(1, np+1)))
    if (size != len(names) or perm != expected_perm or sorted(perm) != list(range(1, size+1))
            or c['witnessCoordinateOrder'] != names
            or [g['kind'] for g in c['generators']] != [names[i-1] for i in perm]):
        raise ValueError('Invalid presentation column permutation or generating root coverage.')
    if any(len(row) != size for row in c['presentation']):
        raise ValueError('Invalid relation dimensions.')
    original = [[row[perm.index(i+1)] for i in range(size)] for row in c['presentation']]
    matrix = Matrix(original)
    pre = Matrix(c['presentation'][:size])
    if (pre.rows != pre.cols or abs(int(pre.det())) != c['preIncomingOrder']
            or c['freeRank'] != 0 or prod(c['torsion']) != c['actualGroupOrder']):
        raise ValueError('The pre-incoming lattice or final group has the wrong index.')
    if c['presentation'][size:] != c['incomingRelations']:
        raise ValueError('Incoming relations are not the actual final presentation rows.')
    pre_inverse = pre.inv()
    commutators = c['commutatorWitnesses']
    nonphase = nq + 2*ns
    if sorted(tuple(w['roots']) for w in commutators) != list(combinations(range(np+1, size+1), 2)):
        raise ValueError('Incomplete or duplicated mixed commutator coverage.')
    for witness in commutators:
        if list(Matrix([witness['relationCoefficients']]) * matrix) != witness['reducedCoordinates']:
            raise ValueError('A mixed commutator does not lie in the relation lattice.')
    checks = 0

    def boundary(parameter, target, degree, modulo=False):
        nonlocal checks
        differential = c['differentialMatrices']['Zs'][degree]
        if len(parameter) != len(differential):
            raise ValueError('Native primitive has the wrong size.')
        if differential and any(len(row) != len(target) for row in differential):
            raise ValueError('Native differential has the wrong target size.')
        for column, expected in enumerate(target):
            value = sum(Fraction(a) * row[column] for a, row in zip(parameter, differential)) - Fraction(expected)
            if (value % 1 if modulo else value):
                raise ValueError('Native gauge or phase primitive failed its exact boundary equation.')
        checks += 1

    by_kind = {}
    for witness in c['witnesses']:
        by_kind.setdefault(witness['kind'], []).append(witness)
    incoming_count = len(c['incomingCohomology']['charge'])
    block = nonphase + 1
    expected_counts = {'charge-lift': nq, 'charge-root': nq, 'sheet-root': 2*ns,
                       'incoming-charge-gauge': incoming_count*block,
                       'phase-reduction': nonphase+incoming_count*block+len(commutators)}
    if ({key: len(value) for key, value in by_kind.items()}
            != {key: value for key, value in expected_counts.items() if value}):
        raise ValueError('Incomplete native root, gauge or phase witness coverage.')
    phase_witnesses = iter(by_kind.get('phase-reduction', []))
    for witness in by_kind.get('phase-reduction', []):
        boundary(witness['nativePhasePrimitive'], witness['nativeResidualPhase'], 4, True)
    if [w['chargeCohomology'] for w in by_kind.get('charge-lift', [])] != c['chargeKernelLattice']:
        raise ValueError('Completed charge roots do not cover the retained kernel basis.')
    for witness in by_kind.get('charge-lift', []):
        boundary(witness['nativePhase'], witness['nativeSource'], 5, True)
    reproduced = [[order if i == j else 0 for j in range(size)]
                  for i, order in enumerate(c['cohomology']['phase'])]
    for witness in by_kind.get('charge-root', []):
        if next(phase_witnesses)['phaseCoordinates'] != witness['phaseCoordinates']:
            raise ValueError('Charge root relation is not tied to its phase reduction.')
        reproduced.append([-v for v in witness['phaseCoordinates']] + witness['coefficients'] + [0]*(2*ns))
    if [w['index'] for w in by_kind.get('sheet-root', [])] != list(range(1, 2*ns+1)):
        raise ValueError('Incomplete finite sheet root coverage.')
    for witness in by_kind.get('sheet-root', []):
        internal = witness['index'] - 1
        is_ci = internal < ns
        output_index = (ns if is_ci else 0) + internal % ns
        root = c['generators'][output_index]['nativeState']
        if witness['order'] != c['group']['factors'][internal % ns]:
            raise ValueError('Finite sheet relation has the wrong factor order.')
        target = [-witness['order'] * v for v in root['n_p' if is_ci else 'e_p']]
        boundary(witness['nativeCIGauge' if is_ci else 'nativeNeutralGauge'], target, 1)
        if next(phase_witnesses)['phaseCoordinates'] != witness['phaseCoordinates']:
            raise ValueError('Sheet root relation is not tied to its phase reduction.')
        row = [-v for v in witness['phaseCoordinates'] + witness['chargeCoordinates']] + [0]*(2*ns)
        row[np+nq+internal] = witness['order']
        reproduced.append(row)
    incoming = by_kind.get('incoming-charge-gauge', [])
    if [(w['index'], w['baseRoot']) for w in incoming] != [
            (i, j) for i in range(1, incoming_count+1) for j in range(block)]:
        raise ValueError('An incoming gauge was not checked at every generating state.')
    if len(c['incomingRelations']) != incoming_count*block:
        raise ValueError('Incorrect incoming relation count.')
    for witness in incoming:
        if next(phase_witnesses)['phaseCoordinates'] != witness['phaseCoordinates']:
            raise ValueError('Incoming relation is not tied to its phase reduction.')
        reproduced.append(witness['phaseCoordinates'] + witness['chargeCoordinates'] + [0]*(2*ns))
    if reproduced != original:
        raise ValueError('Root and incoming witnesses do not reproduce the full relation matrix.')
    for witness, phase in zip(commutators, phase_witnesses):
        if phase['phaseCoordinates'] != witness['reducedCoordinates'][:np]:
            raise ValueError('Commutator is not tied to its phase reduction.')
    for i in range(incoming_count):
        rows = c['incomingRelations'][i*block:(i+1)*block]
        for row in rows[1:]:
            coordinates = (Matrix([row]) - Matrix([rows[0]])) * pre_inverse
            if any(value.q != 1 for value in coordinates):
                raise ValueError('Incoming action depends on the generating state before quotient.')
    charge_map, kernel = c['chargeObstructionMap'], c['chargeKernelLattice']
    target_orders = c['cohomology']['terminalObstruction']
    if (len(charge_map) != nq or len(kernel) != nq or any(len(row) != nq for row in kernel)
            or any(len(row) != len(target_orders) for row in charge_map)):
        raise ValueError('Invalid charge obstruction or kernel lattice dimensions.')
    for vector in kernel:
        for j, order in enumerate(target_orders):
            if sum(a * charge_map[i][j] for i, a in enumerate(vector)) % order:
                raise ValueError('A retained charge kernel generator remains obstructed.')
    target_relations = [[order if i == j else 0 for j in range(len(target_orders))]
                        for i, order in enumerate(target_orders)]
    cokernel = presentation_invariants(target_relations + charge_map, len(target_orders))
    image_order = prod(target_orders) // prod(cokernel['torsion'])
    kernel_index = abs(int(Matrix(kernel).det()))
    if cokernel['freeRank'] or kernel_index != image_order:
        raise ValueError('The retained charge kernel is not the complete obstruction kernel.')
    if c['preIncomingOrder']*kernel_index != prod(c['cohomology']['phase']+c['cohomology']['charge']+c['group']['factors']*2):
        raise ValueError('The pre-incoming order does not exhaust the surviving filtration.')

    start = 0
    rows = c['presentation']
    for name, width in (('e', ns), ('n', ns), ('charge', nq), ('phase', np)):
        equations = [[row[i] for row in rows] for i in range(start)]
        elimination = saturated_kernel(equations, len(rows))
        columns = len(elimination[0]) if elimination else 0
        reduced = [[sum(elimination[i][j]*rows[i][k] for i in range(len(rows)))
                    for k in range(start, start+width)] for j in range(columns)]
        saved = c['finalFiltration'][name]
        computed = presentation_invariants(reduced, width)
        if (signature(computed) != signature(saved)
                or signature(presentation_invariants(saved['presentation'], width)) != signature(saved)
                or hermite_normal_form(Matrix(len(reduced), width, sum(reduced, [])).T)
                != hermite_normal_form(Matrix(len(saved['presentation']), width, sum(saved['presentation'], [])).T)):
            raise ValueError('Saved final filtration does not reproduce from the full presentation.')
        start += width
    return {'status': 'PASS', 'nativeBoundaryEquations': checks,
            'mixedCommutators': len(commutators), 'incomingGenerators': incoming_count,
            'incomingStateIndependentBeforeQuotient': True,
            'chargeKernelMaximalityVerified': True, 'fullRelationMatrixFromWitnesses': True,
            'finalFiltrationFromPresentation': True, 'referenceGroupUsed': False}
