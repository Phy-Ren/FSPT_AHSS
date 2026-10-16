"""Complete intrinsic-zero four-data calculation on the normalized C2 bar complex.

There is one nondegenerate simplex (c,...,c) in every degree. A normalized
cochain is therefore one scalar, and d_chi in degree p is
(-1)^chi + (-1)^(p+1). All source, product and joint-gauge operations below
are evaluated by the adopted exact engine, including their shared phase.
This is a global computation for the four specified backgrounds, not a
general 4+1D classifier or a physical-spectrum identification theorem.
"""
from __future__ import annotations

from dataclasses import dataclass
from fractions import Fraction
from functools import lru_cache
from itertools import combinations, product
from math import gcd, prod

from . import api as ci
from . import e8


CASES = {
    "H_plus": {"s": 0, "rho": 1, "omega_half": 0,
               "family": "charge_conjugation", "generator_square": "+1",
               "referenceTarget": "unitary_charge_conjugation_Hplus"},
    "H_minus": {"s": 0, "rho": 1, "omega_half": 1,
                "family": "charge_conjugation", "generator_square": "(-1)^F",
                "referenceTarget": "unitary_charge_conjugation_Hminus"},
    "AI_relative": {"s": 1, "rho": 0, "omega_half": 0,
                    "family": "time_reversal", "generator_square": "+1",
                    "referenceTarget": "time_reversal_AI"},
    "AII_relative": {"s": 1, "rho": 0, "omega_half": 1,
                     "family": "time_reversal", "generator_square": "(-1)^F",
                     "referenceTarget": "time_reversal_AII"},
}


def differential(degree: int, sign: int) -> int:
    return (-1) ** sign + (-1) ** (degree + 1)


@dataclass(frozen=True, order=True)
class ScalarState:
    e: int = 0
    n: int = 0
    charge: int = 0
    phase: Fraction = Fraction(0)

    def json(self):
        return {"e_2": self.e, "n_2": self.n, "n_4": self.charge,
                "nu_5": str(self.phase)}


ZERO = ScalarState()


def _determinant(matrix):
    if not matrix:
        return 1
    return sum((-1) ** j * value * _determinant(
        [[row[k] for k in range(len(matrix)) if k != j] for row in matrix[1:]])
        for j, value in enumerate(matrix[0]))


def smith_invariants(rows, columns):
    """Exact determinantal divisors; this bounded solver has at most three roots."""
    previous, diagonal = 1, []
    for size in range(1, columns + 1):
        divisor = 0
        for chosen_rows in combinations(rows, size):
            for chosen_columns in combinations(range(columns), size):
                minor = [[row[j] for j in chosen_columns] for row in chosen_rows]
                divisor = gcd(divisor, abs(_determinant(minor)))
        if divisor == 0:
            break
        diagonal.append(divisor // previous)
        previous = divisor
    return {"torsion": [n for n in diagonal if n > 1],
            "freeRank": columns - len(diagonal), "smithDiagonal": diagonal}


class C2FourData:
    """Exact global cochains, completion, full gauges, and coupled stacking."""

    def __init__(self, case: str):
        if case not in CASES:
            raise ValueError("Unknown signed C2 background: " + case)
        self.case = case
        self.data = CASES[case]
        self.s, self.rho, self.k = (self.data[key] for key in ("s", "rho", "omega_half"))
        self.symmetry = ci.Symmetry(
            self.cochain(2, Fraction(self.k, 2), self.s ^ self.rho),
            self.cochain(1, self.s, self.s), self.cochain(1, self.rho, self.rho))
        self.counts = {"normalizationFaceChecks": 0, "sourceEvaluations": 0,
                       "productEvaluations": 0, "gaugeEvaluations": 0}

    @staticmethod
    @lru_cache(maxsize=None)
    def cochain(degree, value=0, sign=0):
        # Pull the entire normalized bar cochain back to the universal all-c
        # six-simplex. Faces with an identity argument have value zero.
        vertices = tuple(i % 2 for i in range(7))
        return ci.Cochain(6, degree, {
            face: value for face in combinations(range(7), degree + 1)
            if all(vertices[a] != vertices[b] for a, b in zip(face, face[1:]))
        }, tuple(sign * v for v in vertices))

    def scalar(self, cochain, *, phase=False):
        value = Fraction(cochain(tuple(range(cochain.p + 1))))
        if phase:
            value %= 1
        elif value.denominator != 1:
            raise AssertionError("A nonintegral lower decoration was produced")
        sign = cochain.tw[1]
        expected = self.cochain(cochain.p, value, sign)
        for face in combinations(range(7), cochain.p + 1):
            difference = cochain(face) - expected(face)
            if (difference % 1 if phase else difference) != 0:
                raise AssertionError("Operation did not descend to a normalized global C2 cochain")
            self.counts["normalizationFaceChecks"] += 1
        return value if phase else int(value)

    @lru_cache(maxsize=None)
    def embed(self, state):
        return e8.State(self.cochain(2, state.e, self.s),
                        self.cochain(2, state.n, self.s),
                        self.cochain(4, state.charge, self.rho),
                        self.cochain(5, state.phase, self.s))

    def decode(self, state):
        return ScalarState(self.scalar(state.e_p), self.scalar(state.n_p),
                           self.scalar(state.n_p2), self.scalar(state.nu_p3, phase=True))

    @lru_cache(maxsize=None)
    def integer_source(self, n):
        return self.scalar(ci.integer_obstruction(self.symmetry, 4,
                                                  self.cochain(2, n, self.s)))

    @lru_cache(maxsize=None)
    def phase_source(self, e, n, charge):
        self.counts["sourceEvaluations"] += 1
        return self.scalar(e8.source(self.symmetry, 4, self.cochain(2, e, self.s),
                                    self.cochain(2, n, self.s),
                                    self.cochain(4, charge, self.rho)), phase=True)

    def completions(self, e, n, charge=None):
        """All phase cohomology choices after solving the actual lower source."""
        if differential(2, self.s) * e or differential(2, self.s) * n:
            return []
        obstruction = self.integer_source(n)
        delta = differential(4, self.rho)
        if delta:
            unique_charge = Fraction(obstruction, delta)
            if unique_charge.denominator != 1:
                return []
            if charge is not None and charge != unique_charge:
                return []
            charge = int(unique_charge)
        elif obstruction:
            return []
        elif charge is None:
            raise ValueError("The closed charge class must be specified")
        source = self.phase_source(e, n, charge)
        phase_delta = differential(5, self.s)
        if phase_delta:
            phases = [(source / phase_delta + Fraction(i, phase_delta)) % 1
                      for i in range(phase_delta)]
        elif source:
            return []
        else:
            # Signed U(1) degree-five phases are killed by d_4=-2.
            phases = [Fraction(0)]
        result = [ScalarState(e, n, charge, phase) for phase in phases]
        for state in result:
            self.embed(state).validate(self.symmetry, 4)
        return result

    @lru_cache(maxsize=None)
    def stack(self, first, second):
        self.counts["productEvaluations"] += 1
        return self.decode(self.embed(first).stack(self.embed(second), self.symmetry, 4))

    @lru_cache(maxsize=None)
    def gauge(self, state, e_parameter=0, n_parameter=0, charge_parameter=0,
              phase_parameter=Fraction(0)):
        self.counts["gaugeEvaluations"] += 1
        return self.decode(self.embed(state).gauge(
            self.symmetry, 4, self.cochain(1, e_parameter, self.s),
            self.cochain(1, n_parameter, self.s),
            self.cochain(3, charge_parameter, self.rho),
            self.cochain(4, phase_parameter, self.s)))

    def canonicalize(self, state):
        """Actual joint gauges, retaining a witness for every nonzero step."""
        steps = []

        def apply(e_parameter=0, n_parameter=0, charge_parameter=0,
                  phase_parameter=Fraction(0)):
            nonlocal state
            before = state
            state = self.gauge(state, e_parameter, n_parameter,
                               charge_parameter, phase_parameter)
            steps.append({"before": before.json(), "after": state.json(),
                          "parameters": {"v_1": e_parameter, "u_1": n_parameter,
                                         "u_3": charge_parameter, "lambda_4": str(phase_parameter)},
                          "phaseCorrection": str((state.phase - before.phase) % 1)})

        if not self.s:
            e_parameter = (state.e % 2 - state.e) // 2
            n_parameter = (state.n % 2 - state.n) // 2
            if e_parameter or n_parameter:
                apply(e_parameter=e_parameter, n_parameter=n_parameter)
        elif state.e or state.n:
            raise AssertionError("A signed closed integer sheet must vanish")
        if not self.rho:
            parameter = (state.charge % 2 - state.charge) // 2
            if parameter:
                apply(charge_parameter=parameter)
        if self.s and state.phase:
            apply(phase_parameter=state.phase / 2)
        return state, steps

    def input(self):
        return {"id": "signed_" + self.case + "_4p1", "dimension": 4,
                "family": self.data["family"], "group": "C2",
                "s": "alpha" if self.s else "0", "rho": "alpha" if self.rho else "0",
                "omega": "alpha^2/2" if self.k else "0",
                "generatorSquare": self.data["generator_square"],
                "referenceTarget": self.data["referenceTarget"],
                "physicalSpin": "not_applicable_internal",
                "orderedFields": ["e_2", "n_2", "n_4", "nu_5"],
                "intrinsic": {"n0I": 0, "n0J": 0,
                              "status": "forced_zero" if not self.s else "restricted_zero"},
                "phaseGaugeConvention": "adopted joint source-cylinder gauge"}

    def classify(self):
        sheets = [0, 1] if not self.s else [0]
        charges = [None] if self.rho else [0, 1]
        states = sorted(state for e, n, charge in product(sheets, sheets, charges)
                        for state in self.completions(e, n, charge))
        index = {state: i for i, state in enumerate(states)}
        if len(index) != len(states) or ZERO not in index:
            raise AssertionError("Invalid canonical root enumeration")
        parent = list(range(len(states)))

        def find(i):
            while parent[i] != i:
                parent[i] = parent[parent[i]]
                i = parent[i]
            return i

        def join(i, j):
            i, j = find(i), find(j)
            parent[max(i, j)] = min(i, j)

        loops = []
        if self.s:
            loops += [("closed_E8_v1", (1, 0, 0)), ("closed_CI_u1", (0, 1, 0))]
        if self.rho:
            loops += [("closed_charge_u3", (0, 0, 1))]
        incoming = []
        for name, parameters in loops:
            for i, state in enumerate(states):
                raw = self.gauge(state, *parameters)
                endpoint, reduction = self.canonicalize(raw)
                j = index[endpoint]
                join(i, j)
                incoming.append({"name": name, "inputIndex": i, "outputIndex": j,
                                 "input": state.json(), "rawEndpoint": raw.json(),
                                 "parameters": dict(zip(("v_1", "u_1", "u_3"), parameters)),
                                 "canonicalEndpoint": endpoint.json(), "reduction": reduction})

        roots = []
        for label, predicate in (
                ("E8", lambda t: t.e == 1 and t.n == 0 and t.charge == 0),
                ("CI", lambda t: t.e == 0 and t.n == 1),
                ("charge", lambda t: t.e == 0 and t.n == 0 and t.charge == 1),
                ("phase", lambda t: t.e == 0 and t.n == 0 and t.charge == 0
                 and t.phase == Fraction(1, 2))):
            candidates = [state for state in states if predicate(state)]
            if candidates:
                roots.append((label, min(candidates)))
        words = {}
        for coefficients in product((0, 1), repeat=len(roots)):
            state = ZERO
            for coefficient, (_, root) in zip(coefficients, roots):
                if coefficient:
                    state, _ = self.canonicalize(self.stack(state, root))
            if state in words:
                raise AssertionError("Binary roots do not uniquely enumerate the pre-incoming states")
            words[state] = coefficients
        if set(words) != set(states):
            raise AssertionError("Full completed root enumeration failed")

        relations, root_relations = [], []
        for position, (label, root) in enumerate(roots):
            raw = self.stack(root, root)
            endpoint, reduction = self.canonicalize(raw)
            row = [-x for x in words[endpoint]]
            row[position] += 2
            relations.append(row)
            root_relations.append({"root": label, "input": root.json(), "power": 2,
                                   "rawPower": raw.json(), "canonicalEndpoint": endpoint.json(),
                                   "reduction": reduction, "relation": row})
        for action in incoming:
            before = words[states[action["inputIndex"]]]
            after = words[states[action["outputIndex"]]]
            row = [b - a for a, b in zip(before, after)]
            action["relation"] = row
            if any(row) and row not in relations and [-x for x in row] not in relations:
                relations.append(row)

        # Every ordered pair is computed using the coupled exact product.
        products, pre_table = [], []
        for i, first in enumerate(states):
            row = []
            for j, second in enumerate(states):
                raw = self.stack(first, second)
                endpoint, reduction = self.canonicalize(raw)
                row.append(index[endpoint])
                products.append({"left": i, "right": j, "output": index[endpoint],
                                 "rawProduct": raw.json(), "reduction": reduction})
            pre_table.append(row)
        representatives = sorted({find(i) for i in range(len(states))})
        quotient_index = {representative: i for i, representative in enumerate(representatives)}
        class_of = [quotient_index[find(i)] for i in range(len(states))]
        table = [[class_of[pre_table[i][j]] for j in representatives] for i in representatives]
        compatibility_checks = 0
        for i, j in product(range(len(states)), repeat=2):
            if class_of[pre_table[i][j]] != table[class_of[i]][class_of[j]]:
                raise AssertionError("Stacking does not descend through the incoming quotient")
            compatibility_checks += 1
        identity = class_of[index[ZERO]]
        for i, j, k in product(range(len(table)), repeat=3):
            if table[table[i][j]][k] != table[i][table[j][k]]:
                raise AssertionError("Nonassociative final stacking")
        for i, j in product(range(len(table)), repeat=2):
            if table[i][j] != table[j][i] or table[i][identity] != i:
                raise AssertionError("Final stacking is not an abelian unital product")
        if any(not any(table[i][j] == identity for j in range(len(table)))
               for i in range(len(table))):
            raise AssertionError("A completed class lacks an inverse")

        # Include nonclosed unit gauges as well as the residual closed loops.
        # This explicitly checks the normalization section against every
        # additive gauge direction and simultaneous lower-coordinate changes.
        gauge_moves = []
        for i, state in enumerate(states):
            for parameters in ((1, 0, 0), (-1, 0, 0), (0, 1, 0), (0, -1, 0),
                               (0, 0, 1), (0, 0, -1), (1, 1, 1), (-1, -1, -1)):
                raw = self.gauge(state, *parameters)
                endpoint, reduction = self.canonicalize(raw)
                j = index[endpoint]
                if class_of[i] != class_of[j]:
                    raise AssertionError("A full lower gauge changes the final class")
                gauge_moves.append({"inputIndex": i, "outputIndex": j,
                                    "parameters": dict(zip(("v_1", "u_1", "u_3"), parameters)),
                                    "rawEndpoint": raw.json(), "reduction": reduction})

        invariants = smith_invariants(relations, len(roots))
        if invariants["freeRank"] or prod(invariants["torsion"]) != len(table):
            raise AssertionError("Presentation and exhaustive gauge quotient disagree")
        filtration = self._filtration(states, class_of, table, identity)
        return {"status": "complete_fixed_four_data_model", "presentation": relations,
                **invariants, "presentationGeneratorCount": len(roots),
                "generators": [{"name": name, "state": state.json(),
                                "quotientClass": class_of[index[state]]} for name, state in roots],
                "finalFiltration": filtration, "actualGroupOrder": len(table),
                "preIncomingStateCount": len(states), "incomingGeneratorCount": len(loops),
                "physicalClassificationCertified": False,
                "physicalCertificationScope": "Independent order/character calibration is external to this solver",
                "intrinsicScope": self.input()["intrinsic"],
                "witnesses": {"canonicalStates": [state.json() for state in states],
                              "stateWords": [list(words[state]) for state in states],
                              "rootRelations": root_relations, "incomingActions": incoming,
                              "fullGaugeMoves": gauge_moves,
                              "orderedProducts": products, "preIncomingProductTable": pre_table,
                              "quotientClassOfState": class_of, "quotientRepresentatives": representatives,
                              "finalProductTable": table, "identityClass": identity,
                              "resolution": self.resolution_certificate(),
                              "checks": {**self.counts, "quotientCompatibilityChecks": compatibility_checks,
                                         "fullGaugeMoveChecks": len(gauge_moves),
                                         "associativityChecks": len(table) ** 3,
                                         "commutativityChecks": len(table) ** 2}}}

    @staticmethod
    def _filtration(states, class_of, table, identity):
        phase = {class_of[i] for i, t in enumerate(states) if not (t.e or t.n or t.charge)}
        charge = {class_of[i] for i, t in enumerate(states) if not (t.e or t.n)}
        n = {class_of[i] for i, t in enumerate(states) if not t.e}
        e = set(class_of)
        groups = {}
        for name, upper, lower in (("e", e, n), ("n", n, charge),
                                   ("charge", charge, phase), ("phase", phase, {identity})):
            if not lower <= upper or len(upper) % len(lower):
                raise AssertionError("Invalid final filtration")
            if any(table[a][b] not in upper for a in upper for b in upper):
                raise AssertionError("Filtration image is not a subgroup")
            order = len(upper) // len(lower)
            if order & (order - 1) or any(table[a][a] not in lower for a in upper):
                raise AssertionError("Unexpected non-elementary filtration quotient")
            groups[name] = {"torsion": [2] * (order.bit_length() - 1),
                            "freeRank": 0, "order": order,
                            "subgroupClasses": sorted(upper), "lowerSubgroupClasses": sorted(lower)}
        return groups

    def resolution_certificate(self):
        return {"complex": "complete normalized inhomogeneous C2 bar complex",
                "nondegenerateCellsInEachDegree": 1,
                "basis": "(c,...,c); alpha(c)=1",
                "differentialFormula": "d_chi in degree p = (-1)^chi + (-1)^(p+1)",
                "integerSignedDifferentials": {str(sign): [differential(p, sign) for p in range(7)]
                                               for sign in (0, 1)},
                "sheetParameterDegree": 1, "chargeParameterDegree": 3, "phaseParameterDegree": 4,
                "closedIncomingScalarFormulas": (
                    {"u3=m": "nu5 -> nu5 + (omega_half+1)*m/2 mod 1",
                     "CI_H1": "0", "E8_H1": "0"}
                    if not self.s else
                    {"u1=m": "n4 -> n4 + (omega_half-1)*m; phase is an exact signed U(1) gauge",
                     "v1=m": "lower state unchanged; phase is exact", "charge_H3": "0"}),
                "completeness": [
                    "All normalized cochains are scalar; every degree-five and degree-six equation is evaluated.",
                    "For trivial integer signs the even-degree cohomology representatives are 0,1; exact parts are removed by actual joint gauges.",
                    "For the nontrivial integer sign closed even-degree cochains vanish; odd-degree closed parameters generate the recorded incoming actions.",
                    "Every integer gauge parameter is generated by unit scalar parameters; after sheet/charge normalization the remaining closed parameter actions are included on every complete state.",
                    "For s=1 every closed phase is removed by the surjective rational phase gauge d_4=-2; for s=0 the two exact phase completions are retained.",
                    "The complete ordered product table, incoming compatibility, abelian group laws and presentation order are checked exactly."],
                "limitations": [
                    "Only the four declared signed C2 backgrounds are accepted.",
                    "n0I=n0J=0; forced for H+/H-, a restriction for AI/AII.",
                    "This proves the fixed four-data cochain quotient; physical-spectrum identification needs independent calibration."]}
