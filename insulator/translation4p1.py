"""Exact four-data classification on the finite simplicial torus B Z^r.

The torus is (Delta[1]/boundary)^r, not a truncated bar resolution. Its
nondegenerate simplices are ordered disjoint nonempty coordinate subsets.
This is a finite K(Z^r,1), so for r <= 4 the degree-five and degree-six
cochain modules are actually zero. The nonzero sheet product is evaluated
with the adopted local API, and its complete integral gauge quotient is
certified by unimodular decompositions of the cellular coboundaries.
"""
from __future__ import annotations

from itertools import combinations, permutations, product
from sympy import Matrix, ZZ
from sympy.polys.matrices import DomainMatrix
from sympy.polys.matrices.normalforms import smith_normal_decomp

from . import api as ci
from . import e8


def matrix_record(matrix):
    return {"rows": matrix.rows, "cols": matrix.cols,
            "entries": [[int(value) for value in row] for row in matrix.tolist()]}


def permutation_sign(sequence):
    return (-1) ** sum(sequence[i] > sequence[j] for i in range(len(sequence))
                       for j in range(i + 1, len(sequence)))


class SimplicialTorus:
    """Normalized chains of a product of minimal simplicial circles."""

    def __init__(self, rank):
        if type(rank) is not int or not 1 <= rank <= 4:
            raise ValueError("Translation rank must be an integer from one to four")
        self.rank = rank
        self.cells = {0: [()]}
        for degree in range(1, 7):
            cells = []
            if degree <= rank:
                # Coordinate zero means that coordinate stays at the vertex;
                # values 1..degree locate its unique nondegenerate edge.
                for assignment in product(range(degree + 1), repeat=rank):
                    if set(range(1, degree + 1)).issubset(assignment):
                        cells.append(tuple(sum(1 << i for i, value in enumerate(assignment)
                                               if value == step)
                                           for step in range(1, degree + 1)))
            self.cells[degree] = sorted(cells)
        self.indices = {p: {cell: i for i, cell in enumerate(cells)}
                        for p, cells in self.cells.items()}
        self.d = {}
        for degree in range(6):
            result = Matrix.zeros(len(self.cells[degree + 1]), len(self.cells[degree]))
            for row, cell in enumerate(self.cells[degree + 1]):
                for i in range(degree + 2):
                    result[row, self.indices[degree][self.face(cell, i)]] += (-1) ** i
            self.d[degree] = result
        self.basis_subsets = {p: list(combinations(range(rank), p)) for p in range(6)}
        self.basis = {p: self._basis_matrix(p) for p in range(6)}
        self.periods = {p: self._period_matrix(p) for p in range(6)}
        self.smith = {p: self._smith(self.d[p]) for p in range(6)}
        self.decompositions = {}
        for degree in range(6):
            self.decompositions[degree] = self._decompose(degree)

    @staticmethod
    def face(cell, index):
        if index == 0:
            return cell[1:]
        if index == len(cell):
            return cell[:-1]
        return cell[:index - 1] + (cell[index - 1] | cell[index],) + cell[index + 1:]

    @staticmethod
    def _smith(matrix):
        if matrix.rows == 0 or matrix.cols == 0:
            return matrix.copy(), Matrix.eye(matrix.rows), Matrix.eye(matrix.cols), 0
        diagonal, left, right = smith_normal_decomp(
            DomainMatrix.from_Matrix(matrix).convert_to(ZZ))
        diagonal, left, right = (x.to_Matrix() for x in (diagonal, left, right))
        rank = sum(bool(diagonal[i, i]) for i in range(min(diagonal.shape)))
        if left * matrix * right != diagonal:
            raise ArithmeticError("The Smith transform failed its exact matrix identity")
        if abs(left.det()) != 1 or abs(right.det()) != 1:
            raise ArithmeticError("A Smith basis change is not unimodular")
        if any(abs(diagonal[i, i]) != 1 for i in range(rank)):
            raise ArithmeticError("The torus coboundary has unexpected nonprimitive image")
        return diagonal, left, right, rank

    def _basis_matrix(self, degree):
        result = Matrix.zeros(len(self.cells[degree]), len(self.basis_subsets[degree]))
        for row, cell in enumerate(self.cells[degree]):
            for column, subset in enumerate(self.basis_subsets[degree]):
                result[row, column] = int(all(cell[j] & (1 << coordinate)
                                              for j, coordinate in enumerate(subset)))
        return result

    def _period_matrix(self, degree):
        result = Matrix.zeros(len(self.basis_subsets[degree]), len(self.cells[degree]))
        for row, subset in enumerate(self.basis_subsets[degree]):
            for permuted in permutations(subset):
                cell = tuple(1 << coordinate for coordinate in permuted)
                result[row, self.indices[degree][cell]] = permutation_sign(permuted)
        return result

    def _decompose(self, degree):
        diagonal, left, right, outgoing_rank = self.smith[degree]
        inverse = right.inv()
        kernel = right[:, outgoing_rank:]
        if degree:
            previous_right = self.smith[degree - 1][2]
            incoming_rank = self.smith[degree - 1][3]
            gauge_basis = previous_right[:, :incoming_rank]
            incoming = self.d[degree - 1] * gauge_basis
        else:
            incoming_rank = 0
            gauge_basis = Matrix.zeros(0, 0)
            incoming = Matrix.zeros(len(self.cells[degree]), 0)
        joined = self.basis[degree].row_join(incoming)
        kernel_coordinates = (inverse * joined)[outgoing_rank:, :]
        if (kernel_coordinates.rows != kernel_coordinates.cols
                or abs(kernel_coordinates.det()) != 1):
            raise ArithmeticError("Canonical periods and gauge images do not span the full integer kernel")
        if self.d[degree] * joined != Matrix.zeros(self.d[degree].rows, joined.cols):
            raise ArithmeticError("A retained kernel vector is not closed")
        if self.periods[degree] * self.basis[degree] != Matrix.eye(self.basis[degree].cols):
            raise ArithmeticError("The primitive torus periods are not dual to the retained cocycles")
        if degree and self.periods[degree] * self.d[degree - 1] != Matrix.zeros(
                self.periods[degree].rows, self.d[degree - 1].cols):
            raise ArithmeticError("A gauge transformation changes a primitive period")
        if degree and self.d[degree] * self.d[degree - 1] != Matrix.zeros(
                self.d[degree].rows, self.d[degree - 1].cols):
            raise ArithmeticError("The simplicial boundary does not square to zero")
        return {"kernel": kernel, "kernelCoordinates": kernel_coordinates,
                "kernelCoordinatesInverse": kernel_coordinates.inv(),
                "rightInverse": inverse, "gaugeBasis": gauge_basis,
                "outgoingRank": outgoing_rank, "incomingRank": incoming_rank}

    def canonicalize(self, degree, vector):
        """Return all integral periods and an explicit integer removal gauge."""
        if vector.shape != (len(self.cells[degree]), 1):
            raise ValueError("The cochain vector has the wrong degree or size")
        if any(value.q != 1 for value in vector):
            raise ValueError("Only integral decoration cochains have an integer gauge quotient")
        if self.d[degree] * vector != Matrix.zeros(self.d[degree].rows, 1):
            raise ValueError("The decoration cochain is not closed")
        decomposition = self.decompositions[degree]
        kernel_vector = (decomposition["rightInverse"] * vector)[decomposition["outgoingRank"]:, :]
        coordinates = decomposition["kernelCoordinatesInverse"] * kernel_vector
        count = self.basis[degree].cols
        periods = coordinates[:count, :]
        gauge = decomposition["gaugeBasis"] * coordinates[count:, :]
        removed = self.basis[degree] * periods
        if degree:
            removed += self.d[degree - 1] * gauge
        if removed != vector or periods != self.periods[degree] * vector:
            raise ArithmeticError("The integral canonicalization witness failed")
        return periods, gauge

    def pullback(self, degree, vector, cell):
        dimension = len(cell)
        values = {}
        for vertices in combinations(range(dimension + 1), degree + 1):
            face = tuple(sum(cell[a:b]) for a, b in zip(vertices, vertices[1:]))
            values[vertices] = int(vector[self.indices[degree][face]])
        return ci.Cochain(dimension, degree, values)

    def api_sheet_product(self, left, right):
        values = []
        for cell in self.cells[4]:
            a = self.pullback(2, left, cell)
            b = self.pullback(2, right, cell)
            zero = lambda degree: ci.Cochain(4, degree, {})
            symmetry = ci.Symmetry(zero(2), zero(1), zero(1))
            actual = ci.integer_product(symmetry, 4, a, b)
            values.append(actual(tuple(range(5))))
        return Matrix(len(values), 1, values)

    def certificate(self):
        degrees = []
        for degree in range(6):
            diagonal, left, right, rank = self.smith[degree]
            decomp = self.decompositions[degree]
            degrees.append({"degree": degree, "cells": [list(c) for c in self.cells[degree]],
                            "coboundary": matrix_record(self.d[degree]),
                            "smithDiagonal": matrix_record(diagonal),
                            "smithLeft": matrix_record(left), "smithRight": matrix_record(right),
                            "coboundaryRank": rank,
                            "cohomologyBasisSubsets": [list(s) for s in self.basis_subsets[degree]],
                            "canonicalCocycles": matrix_record(self.basis[degree]),
                            "periods": matrix_record(self.periods[degree]),
                            "kernelBasis": matrix_record(decomp["kernel"]),
                            "gaugeBasis": matrix_record(decomp["gaugeBasis"]),
                            "kernelCoordinates": matrix_record(decomp["kernelCoordinates"]),
                            "kernelCoordinatesInverse": matrix_record(decomp["kernelCoordinatesInverse"]),
                            "cohomologyFreeRank": self.basis[degree].cols})
        return {"model": "(Delta[1]/boundary Delta[1])^r", "rank": self.rank,
                "isClassifyingSpace": "Product of r circles, hence K(Z^r,1); not a truncated resolution.",
                "cellCounts": [len(self.cells[p]) for p in range(7)], "degrees": degrees}


def stack_coordinates(left, right, polarizer):
    """The actual sheet/charge product in primitive integral periods."""
    e, n, q = left
    f, m, charge = right
    correction = [sum(n[i] * m[j] * polarizer[i][j][k]
                      for i in range(len(n)) for j in range(len(m)))
                  for k in range(len(q))]
    return ([a + b for a, b in zip(e, f)], [a + b for a, b in zip(n, m)],
            [a + b + c for a, b, c in zip(q, charge, correction)])


def straightened_charge(sheet, charge, polarizer):
    square = [sum(sheet[i] * sheet[j] * polarizer[i][j][k]
                  for i in range(len(sheet)) for j in range(len(sheet)))
              for k in range(len(charge))]
    if any(value % 2 for value in square):
        raise ArithmeticError("An integral torus sheet square has an odd period")
    return [q - value // 2 for q, value in zip(charge, square)]


def _api_checks(torus):
    """Global finite-cell API checks, including nonclosed unit gauge parameters."""
    sheet_count = torus.basis[2].cols
    checks = {"sourceCells": len(torus.cells[6]), "integerObstructionCells": len(torus.cells[5]),
              "phaseProductCells": len(torus.cells[5]), "phaseGaugeCells": len(torus.cells[5]),
              "unitGaugeEvaluations": 0, "completedRootSimplexChecks": 0}
    # All top cells are used. Root source and product phase APIs are additionally
    # evaluated there, making the empty target-degree reasoning executable.
    top_cells = torus.cells[torus.rank]
    for cell in top_cells:
        dimension = len(cell)
        zero = lambda degree: ci.Cochain(dimension, degree, {})
        symmetry = ci.Symmetry(zero(2), zero(1), zero(1))
        empty = e8.State(zero(2), zero(2), zero(4), zero(5))
        for index in range(sheet_count):
            sheet = torus.pullback(2, torus.basis[2][:, index], cell)
            for root in (e8.State(sheet, zero(2), zero(4), zero(5)),
                         e8.State(zero(2), sheet, zero(4), zero(5))):
                root.validate(symmetry, 4)
                root.stack(empty, symmetry, 4).validate(symmetry, 4)
                checks["completedRootSimplexChecks"] += 1
        for index in range(torus.basis[4].cols):
            charge = torus.pullback(4, torus.basis[4][:, index], cell)
            root = e8.State(zero(2), zero(2), charge, zero(5))
            root.validate(symmetry, 4)
            root.stack(empty, symmetry, 4).validate(symmetry, 4)
            checks["completedRootSimplexChecks"] += 1
        for degree in (1, 3):
            for index in range(len(torus.cells[degree])):
                unit = Matrix.zeros(len(torus.cells[degree]), 1)
                unit[index] = 1
                parameter = torus.pullback(degree, unit, cell)
                expected = parameter.d()
                state = empty.gauge(symmetry, 4, zero(1),
                                    parameter if degree == 1 else zero(1),
                                    parameter if degree == 3 else zero(3))
                actual = state.n_p if degree == 1 else state.n_p2
                if (actual - expected).maxabs() or state.nu_p3.maxabs():
                    raise ArithmeticError("The full gauge API disagrees with the retained simplicial differential")
                if degree == 1:
                    e_state = empty.gauge(symmetry, 4, parameter, zero(1), zero(3))
                    if (e_state.e_p - expected).maxabs() or e_state.nu_p3.maxabs():
                        raise ArithmeticError("The neutral gauge API disagrees with its full integral image")
                checks["unitGaugeEvaluations"] += 1
    return checks


def calculate(rank):
    torus = SimplicialTorus(rank)
    sheets, charges = torus.basis[2].cols, torus.basis[4].cols
    products, polarizer = [], [[None for _ in range(sheets)] for _ in range(sheets)]
    for i in range(sheets):
        for j in range(sheets):
            actual = torus.api_sheet_product(torus.basis[2][:, i], torus.basis[2][:, j])
            periods, gauge = torus.canonicalize(4, actual)
            polarizer[i][j] = list(map(int, periods))
            products.append({"leftSheet": i, "rightSheet": j,
                             "actualIntegerProduct": list(map(int, actual)),
                             "chargePeriods": list(map(int, periods)),
                             "chargeGaugeRemoval": list(map(lambda x: -int(x), gauge))})
    for i in range(sheets):
        if any(polarizer[i][i]):
            raise ArithmeticError("A decomposable torus sheet has a nonzero square")
        for j in range(sheets):
            if polarizer[i][j] != polarizer[j][i]:
                raise ArithmeticError("Even-degree torus periods fail commutativity")
    checks = _api_checks(torus)
    generators = []
    for kind, degree in (("neutral-E8", 2), ("CI-sheet", 2), ("charge", 4)):
        for subset in torus.basis_subsets[degree]:
            generators.append({"kind": kind, "coordinates": list(subset), "order": "infinite"})
    free_rank = len(generators)
    classification = {
        "presentation": [], "presentationGeneratorCount": free_rank, "generators": generators,
        "torsion": [], "freeRank": free_rank, "actualGroupOrder": 1 if not free_rank else "infinite",
        "finalFiltration": {name: {"torsion": [], "freeRank": count}
                            for name, count in (("e", sheets), ("n", sheets), ("charge", charges), ("phase", 0))},
        "incomingCohomology": {"E8GaugeFreeRank": torus.basis[1].cols,
                               "CIGaugeFreeRank": torus.basis[1].cols,
                               "chargeGaugeFreeRank": torus.basis[3].cols,
                               "phaseGaugeFreeRank": torus.basis[4].cols,
                               "action": "Trivial on periods: B=r=0 and C^5(T^r,R/Z)=0; complete nonclosed gauge images retained."},
        "coordinateStacking": {"orderedFields": ["e_2", "n_2", "n_4", "nu_5"],
                               "sheetPolarizer": polarizer,
                               "rawProduct": "(e+f,n+m,q+t+n wedge m)",
                               "additiveCharge": "Q=q-(n wedge n)/2",
                               "integrality": "The computed polarizer is symmetric with zero diagonal, so the half-square is integral for every integer sheet.",
                               "inverse": "(-e,-n,-q+n wedge n)",
                               "integerPower": "(k e,k n,k q+binomial(k,2) n wedge n), for every k in Z",
                               "freeKernelProof": "(e,n,q) -> (e,n,Q) is an explicit integral bijection and homomorphism. The unimodular kernel certificates prove every state and every incoming gauge are represented."},
        "modelClassificationComplete": True, "physicalClassificationCertified": False,
        "scope": "Complete four-data model on the finite K(Z^r,1), with s=r=omega=0 and intrinsic pair zero; physical stable-splitting comparison is separate."}
    evidence = {"schema": "u1-translation-4p1-simplicial-certificate-v1", "resolution": torus.certificate(),
                "completedIntegerProducts": products, "apiChecks": checks,
                "terminalTargets": {"C5": 0, "C6": 0,
                                    "reason": "The finite simplicial classifying space has dimension r<=4. Every formula target above that dimension is the zero cochain module, not an omitted operation."},
                "checks": {"allCoboundariesSquareZero": True, "allSmithTransformsUnimodular": True,
                           "allCanonicalPeriodsPrimitive": True, "entireClosedIntegerKernelDecomposed": True,
                           "allSheetBasisProductsEvaluated": True, "allProductGaugeCorrectionsIntegral": True,
                           "freeStackingCoordinatesProved": True}}
    return classification, evidence


def verify_certificate(classification, evidence):
    """Replay the retained integer certificate without constructing a Smith form.

    This checks every lattice identity, every gauge-removal primitive, and the
    ordered AW products directly from saved cell coordinates. No expected
    physical group or bordism rank is an input.
    """
    resolution = evidence["resolution"]
    rank = resolution["rank"]
    if type(rank) is not int or not 1 <= rank <= 4:
        raise ValueError("Invalid translation rank")

    def read(record):
        rows, cols, entries = record["rows"], record["cols"], record["entries"]
        if (type(rows) is not int or type(cols) is not int or rows < 0 or cols < 0
                or len(entries) != rows or any(len(row) != cols for row in entries)
                or any(type(value) is not int for row in entries for value in row)):
            raise ValueError("Malformed exact matrix record")
        return Matrix(rows, cols, [value for row in entries for value in row])

    records = resolution["degrees"]
    if [row["degree"] for row in records] != list(range(6)):
        raise ValueError("Missing cochain degree")
    matrices, cells, indices = {}, {}, {}
    for degree, record in enumerate(records):
        cells[degree] = [tuple(cell) for cell in record["cells"]]
        expected = {()} if degree == 0 else set()
        if 1 <= degree <= rank:
            for assignment in product(range(degree + 1), repeat=rank):
                if set(range(1, degree + 1)).issubset(assignment):
                    expected.add(tuple(sum(1 << i for i, step in enumerate(assignment) if step == k)
                                       for k in range(1, degree + 1)))
        if len(set(cells[degree])) != len(cells[degree]) or set(cells[degree]) != expected:
            raise ValueError("The certificate is not the complete finite simplicial torus")
        indices[degree] = {cell: i for i, cell in enumerate(cells[degree])}
        matrices[degree] = {name: read(record[name]) for name in (
            "coboundary", "smithDiagonal", "smithLeft", "smithRight", "canonicalCocycles",
            "periods", "kernelBasis", "gaugeBasis", "kernelCoordinates", "kernelCoordinatesInverse")}
    cells[6] = []
    if resolution["cellCounts"] != [len(cells[p]) for p in range(7)]:
        raise ValueError("Cell count mismatch")
    for degree, record in enumerate(records):
        m = matrices[degree]
        differential = Matrix.zeros(len(cells[degree + 1]), len(cells[degree]))
        for row, cell in enumerate(cells[degree + 1]):
            for i in range(degree + 2):
                if i == 0:
                    face = cell[1:]
                elif i == len(cell):
                    face = cell[:-1]
                else:
                    face = cell[:i - 1] + (cell[i - 1] + cell[i],) + cell[i + 1:]
                differential[row, indices[degree][face]] += (-1) ** i
        if m["coboundary"] != differential:
            raise ValueError("The retained differential disagrees with simplex faces")
        diag, left, right = m["smithDiagonal"], m["smithLeft"], m["smithRight"]
        if left * differential * right != diag or abs(left.det()) != 1 or abs(right.det()) != 1:
            raise ValueError("Invalid unimodular Smith certificate")
        outgoing = record["coboundaryRank"]
        expected_diagonal = Matrix.zeros(*diag.shape)
        for i in range(outgoing):
            if abs(diag[i, i]) != 1:
                raise ValueError("Nonprimitive incoming image")
            expected_diagonal[i, i] = diag[i, i]
        if diag != expected_diagonal or m["kernelBasis"] != right[:, outgoing:]:
            raise ValueError("Incomplete integer kernel")
        basis, periods = m["canonicalCocycles"], m["periods"]
        subsets = list(combinations(range(rank), degree))
        if record["cohomologyBasisSubsets"] != [list(s) for s in subsets]:
            raise ValueError("Wrong primitive period labels")
        actual_basis = Matrix.zeros(len(cells[degree]), len(subsets))
        actual_periods = Matrix.zeros(len(subsets), len(cells[degree]))
        for column, subset in enumerate(subsets):
            for row, cell in enumerate(cells[degree]):
                actual_basis[row, column] = int(all(cell[j] & (1 << coordinate)
                                                   for j, coordinate in enumerate(subset)))
            for permuted in permutations(subset):
                actual_periods[column, indices[degree][tuple(1 << k for k in permuted)]] = permutation_sign(permuted)
        if basis != actual_basis or periods != actual_periods:
            raise ValueError("Canonical cocycle or primitive period was changed")
        if periods * basis != Matrix.eye(basis.cols) or differential * basis != Matrix.zeros(differential.rows, basis.cols):
            raise ValueError("Invalid primitive cocycle basis")
        previous = matrices[degree - 1]["coboundary"] if degree else Matrix.zeros(len(cells[0]), 0)
        incoming = previous * m["gaugeBasis"]
        joined = basis.row_join(incoming)
        coordinates = m["kernelCoordinates"]
        if (coordinates.rows != coordinates.cols or abs(coordinates.det()) != 1
                or coordinates * m["kernelCoordinatesInverse"] != Matrix.eye(coordinates.rows)
                or m["kernelBasis"] * coordinates != joined
                or differential * previous != Matrix.zeros(differential.rows, previous.cols)
                or periods * previous != Matrix.zeros(periods.rows, previous.cols)):
            raise ValueError("The retained gauges fail to span the entire closed integer kernel")
        if record["cohomologyFreeRank"] != basis.cols:
            raise ValueError("Cohomology rank mismatch")
    sheets, charges = matrices[2]["canonicalCocycles"].cols, matrices[4]["canonicalCocycles"].cols
    polarizer = [[None for _ in range(sheets)] for _ in range(sheets)]
    seen = set()
    for record in evidence["completedIntegerProducts"]:
        i, j = record["leftSheet"], record["rightSheet"]
        if not 0 <= i < sheets or not 0 <= j < sheets or (i, j) in seen:
            raise ValueError("Invalid or duplicate product witness")
        seen.add((i, j))
        actual = Matrix(len(cells[4]), 1, [
            matrices[2]["canonicalCocycles"][indices[2][cell[:2]], i]
            * matrices[2]["canonicalCocycles"][indices[2][cell[2:]], j]
            for cell in cells[4]])
        if list(actual) != record["actualIntegerProduct"]:
            raise ValueError("The integer product is not the adopted Alexander-Whitney cup")
        periods = matrices[4]["periods"] * actual
        gauge = Matrix(len(cells[3]), 1, record["chargeGaugeRemoval"])
        if (list(periods) != record["chargePeriods"]
                or actual + matrices[3]["coboundary"] * gauge != matrices[4]["canonicalCocycles"] * periods):
            raise ValueError("The complete product gauge correction is incorrect")
        polarizer[i][j] = list(map(int, periods))
    if len(seen) != sheets * sheets or polarizer != classification["coordinateStacking"]["sheetPolarizer"]:
        raise ValueError("The ordered sheet product table is incomplete")
    if any(any(polarizer[i][i]) or any(polarizer[i][j] != polarizer[j][i] for j in range(sheets))
           for i in range(sheets)):
        raise ValueError("The integral straightening polynomial is invalid")
    free_rank = 2 * sheets + charges
    if (classification["torsion"] != [] or classification["freeRank"] != free_rank
            or classification["presentationGeneratorCount"] != free_rank
            or classification["presentation"] != []):
        raise ValueError("The final presentation does not equal the certified additive lattice")
    expected_filtration = {name: {"torsion": [], "freeRank": count}
                           for name, count in (("e", sheets), ("n", sheets),
                                               ("charge", charges), ("phase", 0))}
    if classification["finalFiltration"] != expected_filtration:
        raise ValueError("A filtration layer disagrees with its independently certified integer cohomology basis")
    expected_generators = [
        {"kind": kind, "coordinates": list(subset), "order": "infinite"}
        for kind, degree in (("neutral-E8", 2), ("CI-sheet", 2), ("charge", 4))
        for subset in records[degree]["cohomologyBasisSubsets"]]
    if classification["generators"] != expected_generators:
        raise ValueError("The presentation generator dictionary disagrees with the primitive coordinate periods")
    return {"status": "PASS", "freeRank": free_rank, "degreesVerified": 6,
            "orderedProductsVerified": len(seen), "referenceGroupUsed": False}
