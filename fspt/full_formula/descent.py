"""Literal cone-last descent of the complete matched 3+1D cochain tower.

Decoration fields are suspended; backgrounds are pulled back by the map that
identifies the new last vertex with the previous last vertex. Restriction of
the higher formula to the cone gives the lower formula. This preserves the
source/product coordinate pair and does not fit group-valued output tables.

Low-dimensional physical calibration is recorded separately from this exact
cochain construction. In particular, coordinate agreement with a published
projective-representation convention is not asserted here.
"""
from .runtime import faces, restriction


def suspend(array, top_degree, field_degree):
    result = [0]*(1 << (top_degree+2))
    if field_degree < 0:
        if any(array):
            raise ValueError("Negative-degree decoration must vanish")
        return tuple(result)
    apex = 1 << (top_degree+1)
    for face in faces(top_degree, field_degree):
        mask = sum(1 << j for j in face)
        result[mask | apex] = array[mask]
    return tuple(result)


def extend_background(array, top_degree):
    return restriction(array, tuple(range(top_degree+1))+(top_degree,))


def lift_fields(dimension, top_degree, fields, names):
    fields = dict(fields)
    for current in range(dimension, 3):
        new = {}
        for name in names:
            degree = current-2 if name in ("n", "m") else current-1 if name in ("a", "b") else current
            new[name] = suspend(fields[name], top_degree, degree)
        for name in ("w", "s"):
            if name in fields:
                new[name] = extend_background(fields[name], top_degree)
        fields = new
        top_degree += 1
    return fields


class DescendedBackend:
    def __init__(self, backend):
        self.backend = backend

    def source(self, dimension, stage, fields):
        if dimension not in (0, 1, 2):
            raise ValueError("Cone-last low-dimensional adapter supports dimensions zero through two")
        offset = {"majorana": 0, "fermion": 1, "bosonic": 2}[stage]
        lifted = lift_fields(dimension, dimension+offset, fields, ("n", "a", "c"))
        return self.backend.source(3, stage, lifted)

    def product(self, dimension, stage, left, right, background):
        if dimension not in (0, 1, 2):
            raise ValueError("Cone-last low-dimensional adapter supports dimensions zero through two")
        offset = {"majorana": -1, "fermion": 0, "bosonic": 1}[stage]
        top = dimension+offset
        if top < 0:
            return 0
        l = lift_fields(dimension, top, dict(background, **left), ("n", "a", "c"))
        r = lift_fields(dimension, top, right, ("n", "a", "c"))
        bg = {name: l.pop(name) for name in ("w", "s")}
        return self.backend.product(3, stage, l, r, bg)
