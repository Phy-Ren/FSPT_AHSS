"""Measured extensions in a fixed filtered basis.

The finite relations, rather than just generator orders, determine the answer.
No symmetry group elements or finite phase multiplication tables are enumerated.
The supplied backend owns cochains, nonlinear products, and exact gauge checks.
Unknown witnesses are never interpreted as split extensions.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Protocol, Sequence


class UnresolvedStacking(RuntimeError):
    """A required lift or relation has not been established."""


class InvalidCertificate(ValueError):
    """A proposed exact cochain identity is false or malformed."""


@dataclass(frozen=True)
class Generator:
    name: str
    layer: int  # Increasing filtration: boson, complex fermion, Majorana, p+ip.
    order: int  # Order in the associated-graded quotient; zero means free.
    lift: Any = field(compare=False, repr=False)

    def __post_init__(self) -> None:
        if not self.name or type(self.layer) is not int or self.layer < 0:
            raise ValueError("a generator needs a name and nonnegative layer")
        if type(self.order) is not int or self.order < 0 or self.order == 1:
            raise ValueError("quotient order must be zero or an integer >= 2")


@dataclass(frozen=True)
class Reduction:
    coordinates: tuple[int, ...]
    witness: Any


@dataclass(frozen=True)
class Relation:
    generator: str
    power: int
    lower_names: tuple[str, ...]
    lower_coordinates: tuple[int, ...]
    row: tuple[int, ...]
    witness: Any = field(compare=False, repr=False)


class Backend(Protocol):
    def zero(self) -> Any: ...
    def product(self, left: Any, right: Any) -> Any: ...
    def inverse(self, state: Any) -> Any: ...
    def verify_flat(self, state: Any) -> bool: ...
    def reduce(self, state: Any, lower: Sequence[Generator]) -> Reduction: ...
    def verify_relation(self, state: Any, lower_product: Any, witness: Any) -> bool: ...


def ordered_power(backend: Backend, state: Any, exponent: int) -> Any:
    """Use a specified binary product tree, retaining every cochain carry."""
    if type(exponent) is not int:
        raise TypeError("the exponent must be an integer")
    if exponent < 0:
        state, exponent = backend.inverse(state), -exponent
    answer = backend.zero()
    while exponent:
        if exponent & 1:
            answer = backend.product(answer, state)
        exponent >>= 1
        if exponent:
            state = backend.product(state, state)
    return answer


def ordered_product(backend: Backend, generators: Sequence[Generator],
                    coordinates: Sequence[int]) -> Any:
    if len(generators) != len(coordinates):
        raise InvalidCertificate("coordinate length does not match the marked basis")
    answer = backend.zero()
    for generator, coefficient in zip(generators, coordinates):
        if type(coefficient) is not int:
            raise InvalidCertificate("extension coordinates must be exact integers")
        if coefficient:
            answer = backend.product(answer, ordered_power(backend, generator.lift, coefficient))
    return answer


def invariant_factors(rows: Sequence[Sequence[int]], columns: int) -> list[int]:
    """Invariants of Z^columns / rowspan(rows), with 0 denoting Z."""
    if type(columns) is not int or columns < 0:
        raise ValueError("invalid presentation width")
    for row in rows:
        if len(row) != columns or any(type(x) is not int for x in row):
            raise ValueError("presentation must be a rectangular integer matrix")
    if not columns:
        return []
    if not rows:
        return [0] * columns
    from sympy import Matrix, ZZ
    from sympy.matrices.normalforms import smith_normal_form
    smith = smith_normal_form(Matrix(rows), domain=ZZ)
    nonzero = [abs(int(smith[i, i])) for i in range(min(smith.shape)) if smith[i, i]]
    return [0] * (columns - len(nonzero)) + [d for d in nonzero if d > 1]


def relation_row(generators: Sequence[Generator], index: int,
                 lower_names: Sequence[str], coordinates: Sequence[int]) -> tuple[int, ...]:
    generator = generators[index]
    if not generator.order:
        raise InvalidCertificate("a free quotient generator has no torsion relation")
    lower = [g for g in generators if g.layer < generator.layer]
    if tuple(lower_names) != tuple(g.name for g in lower):
        raise InvalidCertificate("relation uses a different lower basis or a nonlower layer")
    if len(coordinates) != len(lower) or any(type(c) is not int for c in coordinates):
        raise InvalidCertificate("invalid lower-coordinate vector")
    positions = {g.name: j for j, g in enumerate(generators)}
    row = [0] * len(generators)
    row[index] = generator.order
    for name, coefficient in zip(lower_names, coordinates):
        row[positions[name]] = -coefficient
    return tuple(row)


def measure_stacking(generators: Sequence[Generator], backend: Backend, *,
                     filtration_certificate: Any,
                     abelian_group_law_certificate: Any) -> dict[str, Any]:
    """Measure one relation for each finite quotient generator, then take SNF.

    The two required certificates identify the independently computed final
    filtration quotients and the cochain product/gauge law. They must come from
    the classification/formula layer, not from a requested expected answer.
    Every returned relation is separately rechecked against its ordered lower
    product, even when a coordinate projector proposed that vector.
    """
    generators = tuple(generators)
    if not filtration_certificate or not abelian_group_law_certificate:
        raise UnresolvedStacking("final filtration and abelian cochain law certificates are required")
    if len({g.name for g in generators}) != len(generators):
        raise ValueError("marked generator names must be unique")
    if any(generators[i].layer > generators[i + 1].layer for i in range(len(generators) - 1)):
        raise ValueError("generators must be ordered from lower to higher filtration")
    for generator in generators:
        if generator.lift is None:
            raise UnresolvedStacking(f"no full lift for {generator.name}")
        if backend.verify_flat(generator.lift) is not True:
            raise InvalidCertificate(f"lift {generator.name} is not flat")
    relations: list[Relation] = []
    for index, generator in enumerate(generators):
        if not generator.order:
            continue
        target = ordered_power(backend, generator.lift, generator.order)
        if backend.verify_flat(target) is not True:
            raise InvalidCertificate(f"power of {generator.name} is not flat")
        lower = tuple(g for g in generators if g.layer < generator.layer)
        reduction = backend.reduce(target, lower)
        if reduction is None:
            raise UnresolvedStacking(f"unresolved lower relation for {generator.name}")
        row = relation_row(generators, index, [g.name for g in lower], reduction.coordinates)
        canonical = ordered_product(backend, lower, reduction.coordinates)
        if backend.verify_relation(target, canonical, reduction.witness) is not True:
            raise InvalidCertificate(f"exact lower comparison failed for {generator.name}")
        relations.append(Relation(generator.name, generator.order,
                                  tuple(g.name for g in lower), reduction.coordinates,
                                  row, reduction.witness))
    rows = [list(relation.row) for relation in relations]
    return {
        "status": "computed",
        "scope": "full-abelian-extension-of-certified-filtration",
        "basis": [{"name": g.name, "layer": g.layer, "quotient_order": g.order}
                  for g in generators],
        "full_lifts": [g.lift for g in generators],
        "relations": relations,
        "presentation": rows,
        "invariants": invariant_factors(rows, len(generators)),
        "filtration_certificate": filtration_certificate,
        "abelian_group_law_certificate": abelian_group_law_certificate,
        "enumerated_phase_products": 0,
    }


class PresentedStackingGroup:
    """Stack marked generators using a persisted, certified joint presentation.

    Inputs are dictionaries of integer coefficients in the exported marked
    generator basis. Outputs are canonical Smith coordinates, in the order of
    ``invariants``. This consumes computed relations; it does not recompute or
    guess any cochain carry and needs no GAP or symbolic-algebra dependency.
    """

    def __init__(self, result: dict[str, Any]):
        from collections.abc import Mapping
        free_lattice = result.get("pip", {}).get("free_lattice")
        if "stacking" in result:
            result = result["stacking"]
        if result.get("status") != "computed":
            raise UnresolvedStacking("the saved stacking calculation is incomplete")
        lower = result["lower"]
        names = [g["name"] for g in lower["generators"]]
        if "fullPresentation" in result:
            if result.get("fullUpperPhaseWitness") is not True:
                raise InvalidCertificate("an upper marked presentation requires its actual relation witness")
            names.append(result["pipGenerator"]["name"])
            rows = result["fullPresentation"]
            diagonal = result["fullSmithDiagonal"]
            transform = result["fullSmithColumnTransform"]
        elif "pipExtensionCertificate" in result:
            raise UnresolvedStacking("only the abstract upper group was certified; its marked carry is missing")
        else:
            rows = lower["presentation"]
            diagonal = lower["smithDiagonal"]
            transform = lower["smithColumnTransform"]
        self.free_rank = result.get("freePipRank", 0)
        if type(self.free_rank) is not int or self.free_rank < 0:
            raise InvalidCertificate("invalid free quotient rank")
        self.free_lattice = free_lattice
        self.free_generator_scope = "abstract-free-splitting" if self.free_rank else "no-free-factors"
        self.free_h1_coordinates = ()
        if free_lattice is not None:
            if (free_lattice.get("status") != "computed"
                    or free_lattice.get("fullFreePhaseWitness") is not True
                    or free_lattice.get("rank") != self.free_rank):
                raise InvalidCertificate("incomplete or inconsistent free-generator witness")
            basis = free_lattice.get("latticeBasis", [])
            if (len(basis) != self.free_rank
                    or any(len(row) != self.free_rank for row in basis)
                    or any(type(x) is not int for row in basis for x in row)):
                raise InvalidCertificate("invalid primitive free lattice basis")
            free_generators = free_lattice.get("generators", [])
            if [g.get("name") for g in free_generators] != [
                    f"Pfree{i+1}" for i in range(self.free_rank)]:
                raise InvalidCertificate("free generator names disagree with the marked basis")
            h1_orders = free_lattice.get("h1BasisOrders", [])
            coordinates = [g.get("h1Coordinates", []) for g in free_generators]
            if (any(len(row) != len(h1_orders) for row in coordinates)
                    or any(type(x) is not int for row in coordinates for x in row)):
                raise InvalidCertificate("invalid integer H1 coordinates for a free lift")
            self.free_h1_coordinates = tuple(tuple(row) for row in coordinates)
            self.free_generator_scope = "explicit-primitive-free-lifts" if self.free_rank else "no-free-factors"
        width = len(names)
        if len(transform) != width or any(len(row) != width for row in transform):
            raise InvalidCertificate("Smith transformation has the wrong width")
        if any(type(x) is not int for row in transform for x in row):
            raise InvalidCertificate("Smith transformation is not integral")
        if len(diagonal) > width or any(type(x) is not int for x in diagonal):
            raise InvalidCertificate("invalid Smith diagonal")
        self._diagonal = tuple(abs(x) for x in diagonal) + (0,) * (width-len(diagonal))
        self._transform = tuple(tuple(row) for row in transform)
        free = tuple(i for i, order in enumerate(self._diagonal) if order == 0)
        torsion = tuple(i for i, order in enumerate(self._diagonal) if order > 1)
        self._active = free + torsion
        self.invariants = (0,) * self.free_rank + tuple(self._diagonal[i] for i in self._active)
        if tuple(result["invariants"]) != self.invariants:
            raise InvalidCertificate("saved invariant factors disagree with the marked presentation")
        self.generator_names = tuple(f"Pfree{i+1}" for i in range(self.free_rank)) + tuple(names)
        if len(set(self.generator_names)) != len(self.generator_names):
            raise InvalidCertificate("duplicate marked generator names")
        self._mapping_type = Mapping
        self._presentation = tuple(tuple(row) for row in rows)
        self._triangular = (len(rows) == width and all(len(row) == width for row in rows) and all(
            row[i] > 0 and all(x == 0 for x in row[i+1:])
            for i, row in enumerate(rows)))
        self.marked_reduction = "ordered-filtration" if self._triangular else "smith-representative"
        self._inverse_transform = None
        for row in rows:
            if len(row) != width or any(type(x) is not int for x in row):
                raise InvalidCertificate("nonintegral or incorrectly sized relation")
            if any(self._project(row)):
                raise InvalidCertificate("Smith coordinates do not annihilate a saved relation")

    def _project(self, coefficients: Sequence[int]) -> tuple[int, ...]:
        transformed = [sum(x * self._transform[i][j] for i, x in enumerate(coefficients))
                       for j in range(len(self._transform))]
        return tuple(transformed[i] % self._diagonal[i] if self._diagonal[i]
                     else transformed[i] for i in self._active)

    def _coefficient_vector(self, coefficients) -> tuple[int, ...]:
        if not isinstance(coefficients, self._mapping_type):
            raise TypeError("use a dictionary of marked-generator integer coefficients")
        unknown = set(coefficients) - set(self.generator_names)
        if unknown:
            raise KeyError("unknown marked generators: " + ", ".join(sorted(unknown)))
        vector = tuple(coefficients.get(name, 0) for name in self.generator_names)
        if any(type(x) is not int for x in vector):
            raise TypeError("marked coefficients must be exact integers")
        return vector

    def canonical(self, coefficients) -> tuple[int, ...]:
        vector = self._coefficient_vector(coefficients)
        return vector[:self.free_rank] + self._project(vector[self.free_rank:])

    def stack(self, left, right) -> tuple[int, ...]:
        a, b = self.canonical(left), self.canonical(right)
        return tuple((x+y) % order if order else x+y
                     for x, y, order in zip(a, b, self.invariants))

    def stack_marked(self, left, right) -> dict[str, int]:
        """Return a marked representative using the certified presentation.

        Triangular presentations retain the ordered filtration normal form.
        An incoming quotient may add redundant rows; there we lift the unique
        Smith normal form through the inverse unimodular column transform.
        This is a representative in the saved basis, not a new cochain product.
        """
        if not self._triangular:
            from fractions import Fraction
            if self._inverse_transform is None:
                n = len(self._transform)
                augmented = [[Fraction(x) for x in row] +
                             [Fraction(i == j) for j in range(n)]
                             for i, row in enumerate(self._transform)]
                for col in range(n):
                    pivot = next((i for i in range(col, n) if augmented[i][col]), None)
                    if pivot is None:
                        raise InvalidCertificate("singular Smith column transform")
                    augmented[col], augmented[pivot] = augmented[pivot], augmented[col]
                    divisor = augmented[col][col]
                    augmented[col] = [x/divisor for x in augmented[col]]
                    for i in range(n):
                        if i != col and augmented[i][col]:
                            factor = augmented[i][col]
                            augmented[i] = [x-factor*y for x, y in zip(augmented[i], augmented[col])]
                inverse = [row[n:] for row in augmented]
                if any(x.denominator != 1 for row in inverse for x in row):
                    raise InvalidCertificate("non-unimodular Smith column transform")
                self._inverse_transform = tuple(tuple(int(x) for x in row) for row in inverse)
            canonical = self.stack(left, right)
            smith = [0] * len(self._transform)
            for index, value in zip(self._active, canonical[self.free_rank:]):
                smith[index] = value
            marked = tuple(sum(x*self._inverse_transform[i][j] for i, x in enumerate(smith))
                           for j in range(len(smith)))
            values = canonical[:self.free_rank] + marked
            return {name: value for name, value in zip(self.generator_names, values) if value}
        a, b = self._coefficient_vector(left), self._coefficient_vector(right)
        values = [x+y for x, y in zip(a, b)]
        for i in range(len(self._presentation)-1, -1, -1):
            row = self._presentation[i]
            quotient, remainder = divmod(values[self.free_rank+i], row[i])
            values[self.free_rank+i] = remainder
            for j in range(i):
                values[self.free_rank+j] -= quotient*row[j]
        return {name:value for name,value in zip(self.generator_names,values) if value}

    def order(self, coefficients):
        """Return the phase order, or None for infinite order."""
        from math import gcd
        answer = 1
        for value, modulus in zip(self.canonical(coefficients), self.invariants):
            if not modulus:
                if value:
                    return None
            else:
                factor = modulus // gcd(modulus, value)
                answer = answer // gcd(answer, factor) * factor
        return answer
