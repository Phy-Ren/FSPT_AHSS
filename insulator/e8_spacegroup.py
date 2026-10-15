"""Exact selected-section neutral extension for full rank-three space groups.

Signed integer H1 is computed from the full affine finite presentation. The
finite holonomy table supplies only the background character, never H1.
"""
from __future__ import annotations

from functools import reduce
from math import gcd

from sympy import ImmutableMatrix, Rational, eye

from .e8_h1 import relation_row, twisted_h1
from .e8_pointgroup import _extend_classification, presentation_invariants


def _matrix(entries):
    if not isinstance(entries, list) or len(entries) != 4 or any(len(row) != 4 for row in entries):
        raise ValueError("Expected an exact four-by-four affine matrix.")
    matrix = ImmutableMatrix([[Rational(x) for x in row] for row in entries])
    if list(matrix[:, 3]) != [0, 0, 0, 1] or matrix.det() not in (-1, 1):
        raise ValueError("Invalid row-action affine matrix.")
    return matrix


def spacegroup_h1(data: dict) -> dict:
    if data.get("family") != "spacegroup" or data.get("dimension") != 3 or data.get("translation_rank") != 3:
        raise ValueError("Expected a full rank-three space-group catalog input.")
    if data.get("translation_subgroup_present") is not True:
        raise ValueError("The full translation subgroup must be retained.")
    presentation = data["finite_presentation"]
    if presentation.get("isomorphism_verified") is not True:
        raise ValueError("A certified full affine presentation is required.")
    generators = [_matrix(m) for m in presentation["generator_affine_matrices"]]
    signs = [int(g.det()) for g in generators]
    indices = presentation["generator_point_indices"]
    if len(indices) != len(generators):
        raise ValueError("Presentation/background generator counts disagree.")
    for j, index in enumerate(indices):
        if (generators[j][:3, :3] != ImmutableMatrix(data["matrices"][index])
                or signs[j] != 1 - 2 * data["s"][index]):
            raise ValueError("The affine generator does not induce its stated holonomy character.")
    inverse = [g.inv() for g in generators]

    def word_matrix(word):
        out = ImmutableMatrix(eye(4))
        for letter in word:
            if type(letter) is not int or not 1 <= abs(letter) <= len(generators):
                raise ValueError("A signed presentation word has an invalid generator.")
            out = out * (generators[letter - 1] if letter > 0 else inverse[-letter - 1])
        return out

    relators = presentation["relators"]
    if any(word_matrix(word) != eye(4) for word in relators):
        raise ValueError("A full affine presentation relation does not hold geometrically.")
    h1 = twisted_h1(signs, relators)
    basis, q = h1.cocycle_basis_columns, h1.coboundary_coordinates
    width = len(q)
    translations = data["primitive_translations"]
    if translations.get("basis_of_full_translation_kernel") is not True:
        raise ValueError("A primitive basis of the full translation kernel is required.")
    matrices = [_matrix(m) for m in translations["affine_matrices"]]
    words = translations["words"]
    if len(matrices) != 3 or len(words) != 3 or any(
            m[:3, :3] != eye(3) or word_matrix(word) != m for m, word in zip(matrices, words)):
        raise ValueError("Translation words do not represent the stated rank-three lattice.")
    vectors = ImmutableMatrix([list(m[3, :3]) for m in matrices])
    if vectors.det() == 0:
        raise ValueError("The translation vectors are not independent.")
    translation_values = []
    for word in words:
        coefficients = relation_row(word, signs)
        translation_values.append([sum(coefficients[j] * basis[j][k] for j in range(len(signs)))
                                   for k in range(width)])
    if any(sum(row[k] * q[k] for k in range(width)) for row in translation_values):
        raise ArithmeticError("A principal signed coboundary is nonzero on translations.")
    rows = [q] if any(q) else []
    smith = presentation_invariants(rows, width)
    if smith["torsion"] != list(h1.torsion) or smith["freeRank"] != h1.free_rank:
        raise ArithmeticError("Independent H1 and Smith quotient invariants disagree.")
    roots = [{"kind": "neutral-E8", "presentationGeneratorValues": [row[k] for row in basis],
              "primitiveTranslationValues": [row[k] for row in translation_values],
              "n1": 0, "n3": 0, "nu4": 0,
              "source": "0", "neutralProductTwister": "0", "neutralGaugePhase": "0"}
             for k in range(width)]
    relation_witness = {"coefficients": q, "removalGaugeV0": -1,
                        "identity": "sum(q_i * e_i) + d_s(-1) = 0",
                        "phaseCorrection": "0"}
    divisor = reduce(gcd, map(abs, q), 0)
    torsion_witness = None
    if divisor > 1:
        torsion_witness = {"coefficients": [x // divisor for x in q],
                           "order": divisor, "removalGaugeV0": -1,
                           "phaseCorrection": "0"}
    return {"coefficientAction": "Z_s", "freeRank": h1.free_rank,
            "torsion": list(h1.torsion), "generatorCount": width,
            "presentation": rows, "groupPresentation": presentation,
            "relatorMatrix": h1.relator_matrix,
            "cocycleBasisColumnsOnGenerators": basis,
            "principalCoboundaryCoordinates": q,
            "principalCoboundaryValuesOnGenerators": [sign - 1 for sign in signs],
            "principalGaugeRelation": relation_witness,
            "torsionRootWitness": torsion_witness,
            "primitiveTranslationValues": translation_values,
            "primitiveTranslations": translations, "roots": roots,
            "certificate": {"fullAffinePresentationUsed": True,
                            "affineRelatorsVerified": len(relators),
                            "primitiveTranslationWordsVerified": 3,
                            "saturatedIntegerKernel": True,
                            "principalCoboundaryVerified": True,
                            "holonomySubstitutionUsedForCohomology": False,
                            "neutralPhaseAndTwister": "zero in the selected 3+1D section"}}


def extend_spacegroup_classification(result: dict) -> dict:
    return _extend_classification(result, spacegroup_h1)
