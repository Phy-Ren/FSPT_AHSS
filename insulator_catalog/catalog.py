"""Geometry and U(1)^f backgrounds for crystallographic insulator campaigns.

Matrix multiplication and all Clifford arithmetic are exact. The catalog
contains symmetry input only; published classification data live in benchmarks.
"""
from __future__ import annotations

from functools import lru_cache
from itertools import product
from pathlib import Path
import ast
import hashlib
import json
import re
import sympy as sp

SOURCE = Path(__file__).with_name("source")
POINT3 = [
    ("1", "C1", 1, 1), ("-1", "Ci", 2, 2), ("2", "C2", 3, 2),
    ("m", "Cs", 6, 2), ("2/m", "C2h", 10, 4), ("222", "D2", 16, 4),
    ("mm2", "C2v", 25, 4), ("mmm", "D2h", 47, 8), ("4", "C4", 75, 4),
    ("-4", "S4", 81, 4), ("4/m", "C4h", 83, 8), ("422", "D4", 89, 8),
    ("4mm", "C4v", 99, 8), ("-42m", "D2d", 111, 8), ("4/mmm", "D4h", 123, 16),
    ("3", "C3", 143, 3), ("-3", "C3i", 147, 6), ("32", "D3", 149, 6),
    ("3m", "C3v", 156, 6), ("-3m", "D3d", 162, 12), ("6", "C6", 168, 6),
    ("-6", "C3h", 174, 6), ("6/m", "C6h", 175, 12), ("622", "D6", 177, 12),
    ("6mm", "C6v", 183, 12), ("-6m2", "D3h", 187, 12), ("6/mmm", "D6h", 191, 24),
    ("23", "T", 195, 12), ("m-3", "Th", 200, 24), ("432", "O", 207, 24),
    ("-43m", "Td", 215, 24), ("m-3m", "Oh", 221, 48),
]
# The wallpaper representatives select the actual planar linear representation.
POINT2 = [("1", "C1", 1, 1), ("2", "C2", 2, 2), ("m", "Cs", 3, 2),
          ("2mm", "C2v", 6, 4), ("4", "C4", 10, 4), ("4mm", "C4v", 11, 8),
          ("3", "C3", 13, 3), ("3m", "C3v", 14, 6), ("6", "C6", 16, 6),
          ("6mm", "C6v", 17, 12)]
WALLPAPER = ["p1", "p2", "pm", "pg", "cm", "pmm", "pmg", "pgg", "cmm",
             "p4", "p4m", "p4g", "p3", "p3m1", "p31m", "p6", "p6m"]
PUBLISHED_NAMES = {"pm": "p1m1", "pg": "p1g1", "cm": "c1m1", "pmm": "p2mm",
                   "pmg": "p2mg", "pgg": "p2gg", "cmm": "c2mm", "p4m": "p4mm",
                   "p4g": "p4gm", "p6m": "p6mm"}


def _read_geometry(name):
    """Parse only lists and exact numeric literals from the recorded GAP output."""
    raw = (SOURCE / name).read_text()
    records = {}
    for chunk in raw.split("U1_GEOMETRY")[1:]:
        chunk = chunk.split("U1_VERSION")[0].strip()
        # Encode rational literals as strings before literal_eval; never eval code.
        chunk = re.sub(r"(?<![\w/])(\d+/\d+)", r'"\1"', chunk)
        row = ast.literal_eval(chunk)
        records[row[0]] = row[1:]
    return records


def _matrix(values):
    return sp.ImmutableMatrix([[sp.Rational(x) for x in row] for row in values])


def _entries(m):
    return [[int(x) if x.q == 1 else str(x) for x in row] for row in m.tolist()]


def _closure(generators, dimension):
    identity = sp.ImmutableMatrix(sp.eye(dimension))
    elements = [identity]
    positions = {identity: 0}
    for g in elements:
        for h in generators:
            gh = g * h
            if gh not in positions:
                positions[gh] = len(elements)
                elements.append(gh)
                if len(elements) > 48:
                    raise ValueError("geometry does not close as a crystallographic point group")
    return elements


@lru_cache(maxsize=None)
def _pin_minus(matrices):
    """Normalized binary cocycle of Spin(det(R) R), in exact Cl(0,3).

    A planar representation is embedded as diag(R,1). Normalization to unit
    spinors is unnecessary: a positive scalar does not affect the sign cocycle.
    This independently transcribes the generic geometric construction in
    FSPT_AHSS main ac45fa7, gap/crystalline_background.g.
    """
    mats = [sp.ImmutableMatrix(m) for m in matrices]
    if mats[0].rows == 2:
        mats = [sp.ImmutableMatrix(sp.diag(m, 1)) for m in mats]
    metric = sum((m.T * m for m in mats), sp.zeros(3))
    basis, norms = [], []
    for j in range(3):
        v = sp.eye(3)[:, j]
        for u, norm in zip(basis, norms):
            v -= ((u.T * metric * v)[0] / norm) * u
        basis.append(v)
        norms.append((v.T * metric * v)[0])
    change = sp.Matrix.hstack(*basis)
    change_inverse = change.inv()
    constants = {}
    for a, b in product(range(8), repeat=2):
        swaps = sum(((a >> i) & 1) * ((b >> j) & 1)
                    for i in range(3) for j in range(i))
        factor = sp.Integer((-1) ** swaps)
        for i in range(3):
            if (a & b) >> i & 1:
                factor *= -norms[i]
        constants[a, b] = (a ^ b, factor)

    def mul(a, b):
        result = [sp.Integer(0)] * 8
        for i, ai in enumerate(a):
            if ai:
                for j, bj in enumerate(b):
                    if bj:
                        k, c = constants[i, j]
                        result[k] += ai * bj * c
        return sp.Matrix(result)

    blades = [sp.eye(8)[:, j] for j in (0, 3, 5, 6)]
    lifts = []
    for matrix in mats:
        rotation = change_inverse * (matrix.det() * matrix) * change
        columns = []
        for q in blades:
            column = []
            for j in range(3):
                e = sp.eye(8)[:, 1 << j]
                mapped = sum((rotation[i, j] * sp.eye(8)[:, 1 << i]
                              for i in range(3)), sp.zeros(8, 1))
                column.extend(mul(q, e) - mul(mapped, q))
            columns.append(sp.Matrix(column))
        kernel = sp.Matrix.hstack(*columns).nullspace()
        if len(kernel) != 1:
            raise ValueError("nonunique projective spin lift")
        vector = kernel[0]
        vector /= next(x for x in vector if x)
        lifts.append(sum((x * blade for x, blade in zip(vector, blades)), sp.zeros(8, 1)))
    indices = {m: i for i, m in enumerate(mats)}
    omega = []
    for i, matrix in enumerate(mats):
        row = []
        for j, other in enumerate(mats):
            k = indices[matrix * other]
            result = mul(lifts[i], lifts[j])
            first = next(t for t, x in enumerate(lifts[k]) if x)
            factor = result[first] / lifts[k][first]
            if not factor or result != factor * lifts[k]:
                raise ValueError("spin product failed proportionality")
            row.append(int(bool(factor < 0)))
        omega.append(tuple(row))
    return tuple(omega)


def crystalline_background(matrices, spin):
    """Effective onsite background for unitary charge-preserving spatial symmetry.

    The approved convention is s=r=w1 and rho=0: r reverses charge,
    rho acts on the charge circle, and r=rho+s modulo two.
    Physical spinless gives half the Pin-minus cocycle, physical spin-1/2
    cancels that class. A representative omega=0 is used for the latter.
    """
    if spin not in ("spinless", "spin_half"):
        raise ValueError("spin must be spinless or spin_half")
    mats = tuple(_matrix(m) for m in matrices)
    signs = [int((1 - m.det()) / 2) for m in mats]
    pin = _pin_minus(mats)
    omega = [["1/2" if value and spin == "spinless" else "0" for value in row]
             for row in pin]
    return {"schema_version": 2, "s": signs, "r": signs.copy(),
            "rho": [0] * len(mats), "circle_action": [0] * len(mats),
            "omega": omega, "geometric_pin_minus": [list(row) for row in pin],
            "effective_extension": "half_pin_minus" if spin == "spinless" else "zero",
            "physical_symmetry": "unitary_charge_preserving_crystalline"}


def build_group(family, index, spin="spinless"):
    """Return one JSON-serializable input; all multiplication indices are zero based."""
    counts = {"point2": 10, "point3": 32, "wallpaper": 17, "spacegroup": 230}
    if family not in counts or not 1 <= index <= counts[family]:
        raise ValueError("family or one-based catalog index out of range")
    if family == "spacegroup":
        record = dict(_spacegroup_geometry(index))
        record.update(id=f"spacegroup_{index:03d}_{spin}", spin=spin)
        record.update(crystalline_background(record["matrices"], spin))
        return record
    planar = _read_geometry("wallpaper_gap_export.txt")
    if family == "point2":
        hm, name, representative, order = POINT2[index - 1]
        matrices = [_matrix(m) for m in planar[representative][1]]
        generators = matrices
        dimension = 2
    elif family == "point3":
        hm, name, representative, order = POINT3[index - 1]
        rows = _read_geometry("point3_gap_export.txt")
        generators = [_matrix(m) for m in rows[representative][0]]
        dimension = 3
    elif family == "wallpaper":
        name = hm = WALLPAPER[index - 1]
        representative = index
        matrices = [_matrix(m) for m in planar[index][1]]
        generators = matrices
        order = len(matrices)
        dimension = 2
    else:
        raise ValueError(f"unknown family {family!r}")
    elements = _closure(generators, dimension)
    if len(elements) != order:
        raise ValueError("catalog point-group order mismatch")
    positions = {m: i for i, m in enumerate(elements)}
    record = {"id": f"{family}_{index:02d}_{spin}", "family": family,
              "index": index, "name": name, "hermann_mauguin": hm,
              "dimension": dimension, "spin": spin, "identity_index": 0,
              "order": order, "matrices": [_entries(m) for m in elements],
              "multiplication": [[positions[g * h] for h in elements] for g in elements],
              "translation_subgroup_present": family == "wallpaper",
              "input_scope": "geometry_and_background_only"}
    record.update(crystalline_background(record["matrices"], spin))
    if family == "wallpaper":
        record.update(catalog_number=index, catalog_constructor="SpaceGroupBBNWZ(2,index)",
                      affine_generators=planar[index][0],
                      affine_matrix_convention="row_vectors_translation_in_last_row",
                      published_name=PUBLISHED_NAMES.get(name, name),
                      point_table_scope="finite_holonomy_only_use_full_affine_group_for_cohomology")
    else:
        record["representative_catalog_number"] = representative
    return record


@lru_cache(maxsize=1)
def _spacegroup_export():
    path = SOURCE / "spacegroup_gap_export.json"
    data = json.loads(path.read_text())
    return data, hashlib.sha256(path.read_bytes()).hexdigest()


@lru_cache(maxsize=230)
def _spacegroup_geometry(index):
    data, digest = _spacegroup_export()
    raw = data["records"][index - 1]
    if raw["number"] != index or not raw["presentationIsomorphismVerified"]:
        raise ValueError("Space-group geometry export is inconsistent")
    elements = _closure([_matrix(m) for m in raw["pointMatrices"]], 3)
    positions = {m: i for i, m in enumerate(elements)}
    fp_matrices = [_matrix(m) for m in raw["presentationGeneratorMatrices"]]
    generator_point_indices = [positions[sp.ImmutableMatrix(m[:3, :3])] for m in fp_matrices]
    return {"family": "spacegroup", "index": index, "name": raw["name"],
            "hermann_mauguin": raw["name"], "dimension": 3,
            "identity_index": 0, "order": len(elements),
            "group_order": "infinite", "holonomy_order": len(elements),
            "matrices": [_entries(m) for m in elements],
            "multiplication": [[positions[g * h] for h in elements] for g in elements],
            "translation_subgroup_present": True, "translation_rank": 3,
            "input_scope": "geometry_and_background_only",
            "catalog_number": index, "catalog_constructor": "SpaceGroupBBNWZ(3,index)",
            "affine_generators": raw["affineGenerators"],
            "affine_matrix_convention": "row_vectors_translation_in_last_row",
            "point_table_scope": "finite_holonomy_only_use_full_affine_group_for_cohomology",
            "finite_presentation": {"generator_affine_matrices": raw["presentationGeneratorMatrices"],
                                    "generator_point_indices": generator_point_indices,
                                    "relators": raw["presentationRelators"],
                                    "provenance": "GAP IsomorphismFpGroup of the full affine Pcp group",
                                    "isomorphism_verified": True},
            "primitive_translations": {"affine_matrices": raw["translationGeneratorMatrices"],
                                       "words": raw["translationGeneratorWords"],
                                       "basis_of_full_translation_kernel": True},
            "geometry_export": {"sha256": digest, "GAP": data["GAP"],
                                "CrystCat": data["CrystCat"], "Polycyclic": data["Polycyclic"],
                                "crystcat_parameters": raw["crystcatParameters"]}}


def catalog(family=None, spins=("spinless", "spin_half")):
    families = {"point2": 10, "wallpaper": 17, "point3": 32, "spacegroup": 230}
    if family is not None:
        families = {family: families[family]}
    return [build_group(kind, i, spin) for kind, count in families.items()
            for i in range(1, count + 1) for spin in spins]


def gap_literal(value):
    """Serialize data to a GAP literal without needing a JSON GAP package."""
    if isinstance(value, dict):
        return "rec(" + ",".join(f"{key}:={gap_literal(v)}" for key, v in value.items()) + ")"
    if isinstance(value, list):
        return "[" + ",".join(map(gap_literal, value)) + "]"
    if isinstance(value, bool):
        return "true" if value else "false"
    if isinstance(value, str):
        return json.dumps(value)
    if isinstance(value, int):
        return str(value)
    raise TypeError(type(value))
