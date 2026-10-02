"""Native exact evaluator for the closed-Majorana CA/operator coordinates.

This adapter deliberately names its coordinate. Its output is not implicitly
substituted into the separate publication integer-layer coordinate.
"""
from fractions import Fraction
from .full_formula.runtime import Backend


class ClosedMajoranaBackend:
    def __init__(self, backend=None, coordinate="ca"):
        if coordinate not in ("ca", "operator"):
            raise ValueError(coordinate)
        self.backend = backend or Backend()
        self.coordinate = coordinate

    def evaluate(self, q, operation, fields):
        if q not in (1, 2, 3):
            raise ValueError("Supported Majorana degrees are one, two, and three")
        if operation not in ("majorana_source", "majorana_product", "obstruction", "stacking"):
            raise ValueError(operation)
        phase = operation in ("obstruction", "stacking")
        coordinate = self.coordinate if phase else "ca"
        name = "majorana_%d_%s_%s" % (q, operation, coordinate)
        value = self.backend.program(name, fields)[0]
        return Fraction(value % 8, 8) if phase else value % 2

    def source(self, dimension, stage, fields):
        if stage == "fermion":
            return self.evaluate(dimension-1, "majorana_source", fields)
        if stage == "bosonic":
            return self.evaluate(dimension-1, "obstruction", fields)
        raise ValueError("Closed-Majorana source stages are fermion and bosonic")

    def product(self, dimension, stage, left, right, background):
        fields = dict(background, a=left["a"], c=left["c"],
                      b=right["a"], cp=right["c"])
        if stage == "fermion":
            return self.evaluate(dimension-1, "majorana_product", fields)
        if stage == "bosonic":
            return self.evaluate(dimension-1, "stacking", fields)
        raise ValueError("Closed-Majorana product stages are fermion and bosonic")
