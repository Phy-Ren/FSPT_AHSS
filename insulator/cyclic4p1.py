"""Complete four-data roots on unsigned internal C_N, with exact memoization.

This is a specialized global calculation: the periodic five-cycle detects all
of H^5(C_N,R/Z), the obstruction target H^6(C_N,R/Z) is zero, and incoming
H^1/H^3(C_N,Z) vanish. Every root power and both actual integer-removal gauges
are evaluated using the adopted local formulas. No analytic group answer is
used to construct a root relation.
"""
from collections import Counter, OrderedDict
from fractions import Fraction as F
from itertools import combinations, product

from . import api as ci, e8
from .cyclic_physical import determinant, smith_factors


def _freeze(value):
    """An exact key includes degrees, simplex, signs, and every nonzero value."""
    if isinstance(value, ci.Cochain):
        ci._exact(value)
        return ('cochain', value.N, value.p, value.tw,
                tuple((face, F(v)) for face, v in sorted(value.v.items()) if v))
    if isinstance(value, ci.Symmetry):
        return ('symmetry', _freeze(value.omega2_real), _freeze(value.s1), _freeze(value.r1))
    if isinstance(value, e8.State):
        return ('state', *(_freeze(c) for c in (value.e_p, value.n_p, value.n_p2, value.nu_p3)))
    if isinstance(value, tuple):
        return ('tuple', *map(_freeze, value))
    if value is None or isinstance(value, (int, F)):
        return ('scalar', value)
    raise TypeError('Only exact cochains, backgrounds, states, tuples, and scalars can be cached')


def _thaw(value):
    kind = value[0]
    if kind == 'cochain':
        return ci.Cochain(value[1], value[2], dict(value[4]), value[3])
    if kind == 'tuple':
        return tuple(_thaw(v) for v in value[1:])
    if kind == 'scalar':
        return value[1]
    if kind == 'state':
        return e8.State(*(_thaw(v) for v in value[1:]))
    raise ValueError('Unsupported cached result')


class ExactOperations:
    """Bounded, per-case cache around the existing formulas, never a new formula.

    Cached results are frozen and reconstructed, so callers cannot mutate a
    stored answer. The cache's namespace fixes spatial dimension and theory;
    each key includes the full symmetry and all operation inputs. Phases are
    omitted only from an operation that mathematically does not take them.
    """
    def __init__(self, cache=True, capacity=4096):
        if type(capacity) is not int or capacity < 1:
            raise ValueError('Cache capacity must be a positive integer')
        self.enabled, self.capacity = cache, capacity
        self.cache = OrderedDict()
        self.hits, self.misses = Counter(), Counter()
        self.evictions = 0

    def call(self, name, args, function):
        if not self.enabled:
            self.misses[name] += 1
            return function()
        key = ('U1f-four-data-4p1', name, _freeze(args))
        if key in self.cache:
            self.hits[name] += 1
            result = self.cache.pop(key)
            self.cache[key] = result
            return _thaw(result)
        self.misses[name] += 1
        result = function()
        frozen = _freeze(result)
        self.cache[key] = frozen
        if len(self.cache) > self.capacity:
            self.cache.popitem(last=False)
            self.evictions += 1
        return _thaw(frozen)

    def source(self, symmetry, state):
        return self.call('source', (symmetry, state.e_p, state.n_p, state.n_p2),
                         lambda: e8.source(symmetry, 4, state.e_p, state.n_p, state.n_p2))

    def validate(self, symmetry, state):
        expected = self.source(symmetry, state)
        e8._typed(state.nu_p3, 5, symmetry)
        if (state.nu_p3.d() - expected).mod(1).maxabs():
            raise ValueError('A completed cyclic state failed its full source equation')
        return expected

    def stack(self, symmetry, left, right):
        self.validate(symmetry, left)
        self.validate(symmetry, right)
        k, charge, phase = self.call('ci_product',
            (symmetry, left.n_p, left.n_p2, right.n_p, right.n_p2),
            lambda: ci.product(symmetry, 4, left.n_p, left.n_p2, right.n_p, right.n_p2))
        phase = phase + self.call('neutral_product', (left.e_p, right.e_p),
                                  lambda: e8.neutral.product(left.e_p, right.e_p))
        result = e8.State(left.e_p + right.e_p, k, charge,
                          (left.nu_p3 + right.nu_p3 + phase).mod(1))
        self.validate(symmetry, result)
        return result

    def gauge(self, symmetry, state, v, u, w):
        self.validate(symmetry, state)
        e8._typed(v, 1, symmetry, integral=True)
        k, charge, phase = self.call('ci_gauge', (symmetry, state.n_p, state.n_p2, u, w),
                                    lambda: ci.gauge(symmetry, 4, state.n_p, state.n_p2, u, w))
        phase = phase + self.call('neutral_gauge', (state.e_p, v),
                                  lambda: e8.neutral.gauge(state.e_p, v))
        result = e8.State(state.e_p + v.d(), k, charge, (state.nu_p3 + phase).mod(1))
        self.validate(symmetry, result)
        return result

    def inverse(self, symmetry, state):
        self.validate(symmetry, state)
        k = state.n_p.sc(-1)
        charge = state.n_p2.sc(-1) + ci.integer_product(symmetry, 4, state.n_p, state.n_p)
        lower = e8.State(state.e_p.sc(-1), k, charge, state.nu_p3.sc(0))
        # Evaluate the inverse twister on lower fields; the inverse phase is
        # not yet completed, so it must not be passed to stack/validate.
        _, _, phase = self.call('ci_product', (symmetry, state.n_p, state.n_p2, k, charge),
                                lambda: ci.product(symmetry, 4, state.n_p, state.n_p2, k, charge))
        phase = phase + self.call('neutral_product', (state.e_p, lower.e_p),
                                  lambda: e8.neutral.product(state.e_p, lower.e_p))
        result = e8.State(lower.e_p, k, charge, (state.nu_p3.sc(-1) - phase).mod(1))
        self.validate(symmetry, result)
        return result

    def power(self, symmetry, state, exponent):
        if type(exponent) is not int:
            raise TypeError('An integer exponent is required')
        self.validate(symmetry, state)
        base = state if exponent >= 0 else self.inverse(symmetry, state)
        result = e8.State(*(c.sc(0) for c in (state.e_p, state.n_p, state.n_p2, state.nu_p3)))
        exponent = abs(exponent)
        while exponent:
            if exponent & 1:
                result = self.stack(symmetry, result, base)
            exponent //= 2
            if exponent:
                base = self.stack(symmetry, base, base)
        return result

    def stats(self):
        return {'enabled': self.enabled, 'capacity': self.capacity, 'entries': len(self.cache),
                'hits': dict(self.hits), 'misses': dict(self.misses), 'evictions': self.evictions}


def canonical_roots(order, arguments):
    """Canonical completed roots on any ordered bar simplex, E8 first."""
    vertices = [0]
    for value in arguments:
        if type(value) is not int or not 0 <= value < order:
            raise ValueError('Cyclic arguments must be least nonnegative residues')
        vertices.append((vertices[-1] + value) % order)
    dimension = len(arguments)
    a = ci.Cochain(dimension, 1,
                   {(i, j): (vertices[j] - vertices[i]) % order
                    for i, j in combinations(range(dimension + 1), 2)})
    x = a.d().sc(F(1, order))
    xx = x.cup(x)
    zero = lambda degree: ci.Cochain(dimension, degree, {})
    symmetry = ci.Symmetry(zero(2), zero(1), zero(1))
    roots = (
        e8.State(x, zero(2), zero(4), a.cup(xx).sc(F(1, 3*order))),
        e8.State(zero(2), x, zero(4), a.cup(xx).sc(F(1, 6*order))),
        e8.State(zero(2), zero(2), xx, ci.integral_cartan(x, x).sc(F(1, 2))),
        e8.State(zero(2), zero(2), zero(4), a.cup(xx).sc(F(1, order))),
    )
    return a, x, zero, symmetry, roots


def cochain_record(cochain):
    return {'degree': cochain.p, 'simplexDimension': cochain.N, 'sign': list(cochain.tw),
            'values': {','.join(map(str, face)): str(value)
                       for face, value in sorted(cochain.v.items()) if value}}


def state_record(state):
    return {name: cochain_record(value) for name, value in zip(
        ('e_2', 'n_2', 'n_4', 'nu_5'), (state.e_p, state.n_p, state.n_p2, state.nu_p3))}


def calculate(order, cache=True, retain_ledger=True):
    """Full relative model presentation and complete finite cycle evidence."""
    if type(order) is not int or order < 1:
        raise ValueError('A positive integer cyclic order is required')
    engine = ExactOperations(cache=cache)
    ledger, completion_checks = [], []
    periods = [F(0)] * 4
    charge_period = F(0)
    q = (order*(order-1)//2) % order
    if order > 1:
        for i, j in product(range(1, order), repeat=2):
            word = (1, i, 1, j, 1)
            # Nonvacuous degree-six source checks are separate from degree-five
            # root-period evaluation. The source identities below are global;
            # these checks regress their local implementation on every cycle term.
            _, _, _, six_sym, six_roots = canonical_roots(order, word + (1,))
            source_values = []
            for name, root in zip(('X', 'Y', 'Q', 'b'), six_roots):
                source = engine.validate(six_sym, root)
                source_values.append({'root': name, 'sourceTop': str(source(tuple(range(7)))),
                                      'phaseCoboundaryTop': str(root.nu_p3.d()(tuple(range(7))) % 1)})
            completion_checks.append({'word': list(word + (1,)), 'completedRoots': 4,
                                      'sourcePhaseValues': source_values})
            a, x, zero, symmetry, roots = canonical_roots(order, word)
            top = tuple(range(6))
            charge_period += roots[2].nu_p3(top)
            negative_charge = engine.power(symmetry, roots[2], -q)
            row = {'word': list(word), 'roots': []}
            if retain_ledger:
                row['canonicalA1'] = cochain_record(a)
                row['canonicalX2'] = cochain_record(x)
                row['canonicalStates'] = [state_record(root) for root in roots]
            for index, root in enumerate(roots):
                power = engine.power(symmetry, root, order)
                v = a.sc(-1) if index == 0 else zero(1)
                u = a.sc(-1) if index == 1 else zero(1)
                sheet_removed = engine.gauge(symmetry, power, v, u, zero(3))
                charge_coefficient = q if index == 1 else 0
                charge_removed = (engine.stack(symmetry, sheet_removed, negative_charge)
                                  if charge_coefficient else sheet_removed)
                multiple = ((order*(order-1)//2-q)//order if index == 1
                            else 1 if index == 2 else 0)
                w = a.cup(x).sc(-multiple)
                reduced = engine.gauge(symmetry, charge_removed, zero(1), zero(1), w)
                if any(c.maxabs() for c in (reduced.e_p, reduced.n_p, reduced.n_p2)):
                    raise ArithmeticError('A cyclic root relation retains a lower decoration')
                periods[index] += reduced.nu_p3(top)
                record = {'root': ('X', 'Y', 'Q', 'b')[index],
                          'chargeCoefficient': charge_coefficient,
                          'phaseAfterPower': str(power.nu_p3(top)),
                          'phaseAfterSheetGauge': str(sheet_removed.nu_p3(top)),
                          'phaseAfterChargeRootRemoval': str(charge_removed.nu_p3(top)),
                          'phaseAfterChargeGauge': str(reduced.nu_p3(top))}
                if retain_ledger:
                    record.update(power=state_record(power), afterSheetGauge=state_record(sheet_removed),
                                  afterChargeRootRemoval=state_record(charge_removed), reduced=state_record(reduced),
                                  neutralGauge=cochain_record(v), ciGauge=cochain_record(u),
                                  chargeGauge=cochain_record(w))
                row['roots'].append(record)
            ledger.append(row)
    coefficients = [(period*order) % order for period in periods]
    if any(value.denominator != 1 for value in coefficients):
        raise ArithmeticError('A terminal period is not an integral phase-root coefficient')
    if coefficients[3] or (charge_period % 1):
        raise ArithmeticError('Canonical shared-phase/charge-root normalization failed')
    presentation = ([[order, 0, 0, -int(coefficients[0])],
                     [0, order, -q, -int(coefficients[1])],
                     [0, 0, order, -int(coefficients[2])], [0, 0, 0, order]]
                    if order > 1 else [])
    torsion = smith_factors(presentation)
    size = abs(determinant(presentation))
    if size != order**4:
        raise ArithmeticError('Complete presentation has the wrong filtration size')
    neutral_closed_formula = (order*(1-order*order)//3) % order
    if coefficients[0] != neutral_closed_formula:
        raise ArithmeticError('Independent neutral cubic root formula disagrees')
    classification = {
        'theory': 'U(1)^f insulator', 'spatialDimension': 4,
        'group': {'family': 'internal_cyclic', 'order': order},
        'orderedFields': ['e_2', 'n_2', 'n_4', 'nu_5'],
        'presentation': presentation, 'presentationGeneratorCount': len(presentation),
        'generators': [{'kind': name} for name in ('neutral-E8', 'CI-sheet', 'charge', 'shared-phase')]
                      if order > 1 else [],
        'torsion': torsion, 'freeRank': 0, 'actualGroupOrder': size,
        'expectedOrderFromFiltration': order**4,
        'filtrationOrders': [[order]]*4 if order > 1 else [[], [], [], []],
        'incomingCohomology': {'sheet': [], 'charge': []}, 'terminalObstructionTargetOrders': [],
        'integerSourceIdenticallyZero': True,
        'rootPhasePairings': [str(period % 1) for period in periods],
        'rootWitnesses': [{'root': name, 'power': order, 'chargeCoefficient': q if index == 1 else 0,
                          'phaseCoefficient': int(coefficients[index])}
                         for index, name in enumerate(('X', 'Y', 'Q', 'b'))] if order > 1 else [],
        'cycleTerms': (order-1)**2, 'nonvacuousRootCompletionChecks': len(completion_checks)*4,
        'sourceIdentity': [
            'da=Nx and dx=0 give d(a*x^2/(3N))=x^3/3 and d(a*x^2/(6N))=x^3/6.',
            'The integral Cartan identity gives d(zeta_22(x,x)/2)=Sq^2(bar(x^2))/2 modulo one.',
            'Full source/product/gauge identities transport these completed roots through every operation.'
        ],
        'phaseDetection': {
            'cycle': 'sum_(i,j=0)^(N-1) [g|g^i|g|g^j|g]',
            'phaseRootPeriod': str(F(1, order)) if order > 1 else '0',
            'reason': 'H^5(C_N,R/Z)=Z_N and this normalized cycle generates H_5(C_N,Z); pairing determines the entire phase class.',
            'phasePrimitive': 'Relations are certified as exact by complete periodic-cycle detection; no explicit full-bar primitive is asserted.'},
        'scope': 'Complete original four-data model for internal s=r=omega=0; intrinsic row excluded from this cochain calculation.',
        'physicalClassificationCertified': False,
    }
    evidence = {'orderedFields': classification['orderedFields'], 'order': order,
                'completionChecks': completion_checks, 'cycleLedger': ledger,
                'canonicalChargePhasePairing': str(charge_period % 1)}
    return classification, evidence, engine.stats()
