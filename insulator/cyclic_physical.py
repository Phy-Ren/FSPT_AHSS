"""Independent Spin-c eta-character lattice for U(1)^f x C_N in 4+1D.

The physical generators and geometric input follow the reviewed supplied
Electronic_Insulator_AHSS_v0_15, Appendix K, equations v14:physicalcharacters
and v14:etamatrix. The group-ring eta evaluation is independent of the local
AHSS cochain engine. Small integer-lattice algorithms are self-contained and
use exact arithmetic; no reference classification table is read.
"""
from fractions import Fraction as F
from functools import lru_cache
from itertools import combinations
from math import comb, gcd


REFERENCES = [
    {"id": "FreedHopkins", "title": "Reflection positivity and invertible topological phases",
     "authors": "D. S. Freed and M. J. Hopkins", "year": 2021,
     "url": "https://arxiv.org/abs/1604.06527v6", "version": "v6",
     "use": "Structured invertible phases and low Spin-c coefficient groups."},
    {"id": "BahriGilkey", "title": "The eta invariant, Pin^c bordism, and equivariant Spin^c bordism for cyclic 2-groups",
     "authors": "A. Bahri and P. Gilkey", "year": 1987,
     "doi": "10.2140/pjm.1987.128.1", "url": "https://doi.org/10.2140/pjm.1987.128.1",
     "use": "Spin-c lens eta input; Theorem 0.1 is not an all-N classification theorem."},
    {"id": "Hsieh", "title": "Discrete gauge anomalies revisited",
     "authors": "C.-T. Hsieh", "year": 2018,
     "url": "https://arxiv.org/abs/1808.02881v1", "version": "v1",
     "use": "Exact lens eta arithmetic. Its finite fermionic-charge symmetry is not identified with Spin-c x C_N."},
    {"id": "SuppliedV015", "title": "Electronic Insulator AHSS v0.15",
     "locator": "Appendix K, v14:physicalcharacters, v14:etamatrix, faithful cyclic pairing",
     "use": "Reviewed independent physical generator dictionary and all-N order proof; supplied manuscript, not a published external classification."},
]


def determinant(matrix):
    n = len(matrix)
    if not n:
        return 1
    if any(len(row) != n for row in matrix):
        raise ValueError("A square matrix is required")
    if n == 1:
        return matrix[0][0]
    return sum((-1)**j * matrix[0][j] * determinant(
        [row[:j] + row[j+1:] for row in matrix[1:]]) for j in range(n))


def smith_factors(matrix):
    """Determinantal divisors, bounded here to four generators."""
    if not matrix:
        return []
    previous, result = 1, []
    for size in range(1, min(len(matrix), len(matrix[0])) + 1):
        divisor = 0
        for rows in combinations(range(len(matrix)), size):
            for columns in combinations(range(len(matrix[0])), size):
                divisor = gcd(divisor, abs(determinant(
                    [[matrix[i][j] for j in columns] for i in rows])))
        if not divisor:
            break
        if divisor % previous:
            raise ArithmeticError("Invalid determinantal divisors")
        result.append(divisor // previous)
        previous = divisor
    return [value for value in result if value > 1]


def column_hnf(matrix):
    """Canonical column lattice for a nonsingular square integer matrix."""
    a = [list(row) for row in matrix]
    n = len(a)
    if any(len(row) != n for row in a) or not determinant(a):
        raise ValueError("A nonsingular square integer matrix is required")
    def swap(j, k):
        for row in a:
            row[j], row[k] = row[k], row[j]
    def add(j, k, q):
        for row in a:
            row[j] += q * row[k]
    for k in range(n-1, -1, -1):
        swap(next(j for j in range(k, -1, -1) if a[k][j]), k)
        for j in range(k):
            while a[k][j]:
                add(j, k, -(a[k][j] // a[k][k]))
                if a[k][j]:
                    swap(j, k)
        if a[k][k] < 0:
            for row in a:
                row[k] = -row[k]
        for j in range(k+1, n):
            add(j, k, -(a[k][j] // a[k][k]))
    return a


def _bezout(a, b):
    r, rr, s, ss, t, tt = a, b, 1, 0, 0, 1
    while rr:
        q = r // rr
        r, rr, s, ss, t, tt = rr, r-q*rr, ss, s-q*ss, tt, t-q*tt
    return (r, s, t) if r >= 0 else (-r, -s, -t)


def character_kernel(rows):
    """Exact column basis of ker(Z^4 -> (Q/Z)^m), without group enumeration."""
    n = 4
    kernel = [[int(i == j) for j in range(n)] for i in range(n)]
    for row in rows:
        image = [sum(F(row[i]) * kernel[i][j] for i in range(n)) for j in range(n)]
        denominator = 1
        for value in image:
            denominator = denominator * value.denominator // gcd(denominator, value.denominator)
        z = [int(denominator * value) for value in image]
        change = [[int(i == j) for j in range(n)] for i in range(n)]
        for j in range(1, n):
            a, b = z[0], z[j]
            if not b:
                continue
            g, u, v = _bezout(a, b)
            for vector in change:
                left, right = vector[0], vector[j]
                vector[0], vector[j] = u*left + v*right, -(b//g)*left + (a//g)*right
            z[0], z[j] = g, 0
        if not z[0]:
            continue
        multiplier = denominator // gcd(denominator, z[0])
        for vector in change:
            vector[0] *= multiplier
        kernel = column_hnf([[sum(kernel[i][k]*change[k][j] for k in range(n))
                              for j in range(n)] for i in range(n)])
    if any(sum(F(row[i])*kernel[i][j] for i in range(n)).denominator != 1
           for row in rows for j in range(n)):
        raise ArithmeticError("Computed lattice is not in the character kernel")
    return kernel


@lru_cache(maxsize=64)
def _eta_cube(order):
    d = tuple(F(order-1-2*j, 2*order) for j in range(order))
    def multiply(a, b):
        return tuple(sum(a[i]*b[(k-i) % order] for i in range(order)) for k in range(order))
    return multiply(multiply(d, d), d)


def eta_characters(order):
    """Physical anomaly characters, computed in Q[C_N], in X,Y,Q,b order."""
    if type(order) is not int or order < 2:
        raise ValueError("A cyclic order at least two is required")
    cube = _eta_cube(order)
    def anomaly(charge, structure, power):
        shift = (3*charge+3)//2 + charge*structure
        return sum((-1)**(power-weight)*comb(power, weight)
                   * cube[-(shift+weight) % order] for weight in range(power+1))
    rows = []
    for structure in range(order):
        a = anomaly(1, structure, 1)
        c = anomaly(1, structure, 2)
        b = anomaly(1, structure, 3)
        d = 9*a - anomaly(3, structure, 1)
        row = [(d-3*c+2*b) % 1, (a-c+b) % 1, (c-b) % 1, b % 1]
        analytic = [F(2*(order*order-1), 3*order),
                    F(order*order-6*order+5+6*structure*(structure+2-order), 12*order),
                    F(2*structure+order+3, 2*order), F(1, order)]
        if row != [value % 1 for value in analytic]:
            raise ArithmeticError("Group-ring eta and analytic character disagree")
        rows.append(row)
    rows.append([F(-1, order) % 1, F(0), F(0), F(0)])
    return rows


def compare_physical(order, presentation):
    """Compare full relation lattices; this function does not compute model roots."""
    if order == 1:
        if presentation:
            raise ValueError("The trivial reduced group has an empty presentation")
        return {"status": "PASS", "exactRelationLatticeMatch": True, "etaPairing": [],
                "physicalRelativeOrder": 1, "modelRelationHNF": [], "etaKernelHNF": [],
                "references": REFERENCES, "scope": "Trivial additional symmetry: relative group is zero."}
    if len(presentation) != 4 or any(len(row) != 4 for row in presentation):
        raise ValueError("Four complete root relations in X,Y,Q,b order are required")
    rows = eta_characters(order)
    kernel = character_kernel(rows)
    model = column_hnf(list(map(list, zip(*presentation))))
    checks = [sum(value*coefficient for value, coefficient in zip(row, relation)).denominator == 1
              for row in rows for relation in presentation]
    if not all(checks) or model != kernel or abs(determinant(kernel)) != order**4:
        raise ArithmeticError("Complete cochain relation lattice disagrees with physical eta kernel")
    return {"status": "PASS", "exactRelationLatticeMatch": True,
            "generatorOrder": ["X_E8", "Y_CI", "Q_charge", "b_phase"],
            "physicalGenerators": ["A1(9R-3R^2+2R^3)-A3(R)", "A1(R-R^2+R^3)",
                                   "A1(R^2-R^3)", "A1(R^3)"],
            "etaCycles": ["L5(N;1,1,1), canonical complex-induced Spin-c structure twisted by lambda^p (determinant (3+2p)x), p=" + str(p) for p in range(order)]
                         + ["S1 x CP2, unit cyclic holonomy, determinant h"],
            "etaPairing": [[str(value) for value in row] for row in rows],
            "etaEvaluations": "Exact Q[C_N] pseudoinverse cube; independently checked against analytic eta formula.",
            "modelRelationHNF": model, "etaKernelHNF": kernel,
            "physicalRelativeOrder": abs(determinant(kernel)),
            "independentAHSSOrderBound": order**4,
            "orderBoundReason": "Omega_q^Spin-c: Z at q=0,2; Z^2 at q=4; zero at odd q<=5. Total-degree-five reduced AHSS has size at most N^4.",
            "relationCharacterChecks": len(checks), "references": REFERENCES,
            "scope": "Full relation lattice in the reviewed physical-root dictionary for this internal direct-product cyclic symmetry; no universal terminal map claimed."}
