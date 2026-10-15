"""Certified finite-point-group extension in the selected 3+1D E8 section.

This computes a presentation, not a factor taken from a reference table.  Its
physical interpretation still requires the CI model to identify the physical
kernel.  No 4+1D global extension or infinite-group algorithm is claimed here.
"""
from __future__ import annotations

from collections import deque
from copy import deepcopy
from typing import Any

from .e8_h1 import twisted_h1


MODEL = "3p1-selected-neutral-section-direct-product-v1"
PHYSICAL_CAVEAT = (
    "This is the E8-inclusive selected four-data model. Identification with the "
    "full physical classification additionally requires identifying the CI "
    "model with the physical kernel; the universal nonzero-CI terminal "
    "comparison is not certified by this calculation."
)


def _integer(value: Any) -> bool:
    return isinstance(value, int) and not isinstance(value, bool)


def _validate_table(data: dict) -> tuple[list[list[int]], list[int], int]:
    if data.get("family") != "point3" or data.get("dimension") != 3:
        raise ValueError("Only spatially three-dimensional finite point groups are supported.")
    if data.get("translation_subgroup_present") is not False:
        raise ValueError("The finite-point-group extension excludes translation subgroups.")
    table = data.get("multiplication")
    if not isinstance(table, list) or not table:
        raise ValueError("A nonempty finite multiplication table is required.")
    size = len(table)
    if data.get("order") != size:
        raise ValueError("The declared group order disagrees with its table.")
    if any(not isinstance(row, list) or len(row) != size or
           any(not _integer(x) or not 0 <= x < size for x in row) for row in table):
        raise ValueError("The multiplication table has invalid entries or dimensions.")
    identity = data.get("identity_index")
    if not _integer(identity) or not 0 <= identity < size:
        raise ValueError("The identity index is invalid.")
    indices = set(range(size))
    if any(table[identity][g] != g or table[g][identity] != g for g in indices):
        raise ValueError("The declared identity does not act as the identity.")
    if any(set(row) != indices for row in table) or any(
            {table[g][h] for g in indices} != indices for h in indices):
        raise ValueError("The multiplication table lacks the group cancellation property.")
    for g in range(size):
        for h in range(size):
            if any(table[table[g][h]][k] != table[g][table[h][k]] for k in range(size)):
                raise ValueError("The multiplication table is not associative.")
    bits = data.get("s")
    if not isinstance(bits, list) or len(bits) != size or any(
            not _integer(bit) or bit not in (0, 1) for bit in bits):
        raise ValueError("The orientation character must be a bit for every element.")
    if any(bits[table[g][h]] != (bits[g] ^ bits[h])
           for g in range(size) for h in range(size)):
        raise ValueError("The orientation bits do not define a group character.")
    return table, [1 - 2 * bit for bit in bits], identity


def _cayley_presentation(table: list[list[int]], identity: int) -> tuple[list[int], list[list[int]], list[list[int]]]:
    """A deterministic presentation from a small generating set and its Cayley graph.

    Relations w(g) x_j = w(g x_j) reduce every positive word to one of the
    supplied group elements. Inverses also reduce because every generator has
    finite order. Consequently the presented group is exactly the input group.
    """
    generators: list[int] = []
    words: dict[int, list[int]] = {identity: []}
    while len(words) != len(table):
        generators.append(next(g for g in range(len(table)) if g not in words))
        words = {identity: []}
        queue = deque([identity])
        while queue:
            g = queue.popleft()
            for j, x in enumerate(generators):
                h = table[g][x]
                if h not in words:
                    words[h] = words[g] + [j + 1]
                    queue.append(h)
    representatives = [words[g] for g in range(len(table))]
    relators = [words[g] + [j + 1] + [-letter for letter in reversed(words[table[g][x]])]
                for g in range(len(table)) for j, x in enumerate(generators)]
    return generators, representatives, relators


def finite_pointgroup_h1(data: dict) -> dict:
    """Return exact H1, global integer cocycles, and principal-gauge witnesses."""
    table, character, identity = _validate_table(data)
    generators, words, relators = _cayley_presentation(table, identity)
    signs = [character[g] for g in generators]
    h1 = twisted_h1(signs, relators)
    width = len(h1.coboundary_coordinates)
    values: list[list[int]] = []
    for word in words:
        row, prefix = [0] * width, 1
        for letter in word:
            j = letter - 1  # Representatives contain only positive letters.
            for k in range(width):
                row[k] += prefix * h1.cocycle_basis_columns[j][k]
            prefix *= signs[j]
        values.append(row)
    pair_checks = 0
    for g in range(len(table)):
        for h in range(len(table)):
            for k in range(width):
                if values[table[g][h]][k] != values[g][k] + character[g] * values[h][k]:
                    raise ArithmeticError("A presentation cocycle failed a global crossed-homomorphism identity.")
                pair_checks += 1
    q = h1.coboundary_coordinates
    if any(sum(values[g][k] * q[k] for k in range(width)) != character[g] - 1
           for g in range(len(table))):
        raise ArithmeticError("The principal coboundary witness failed on the full group.")
    # Independent finite-group sanity check, after the integer presentation was
    # computed. A finite group has no free signed H1; its nontrivial sign case
    # has one crossed-homomorphism direction and a principal sublattice of index 2.
    reversing = any(sign == -1 for sign in character)
    if h1.free_rank != 0 or h1.torsion != ((2,) if reversing else ()):
        raise ArithmeticError("Computed H1 contradicts the finite-group transfer check.")
    if width != int(reversing):
        raise ArithmeticError("Unexpected rank of the finite-group crossed-homomorphism lattice.")
    roots = []
    if width:
        order = abs(q[0])
        multiple = order // q[0]
        root_values = [row[0] for row in values]
        if any(order * root_values[g] + (character[g] - 1) * (-multiple)
               for g in range(len(table))):
            raise ArithmeticError("The neutral root-power removal gauge is invalid.")
        roots.append({
            "kind": "neutral-E8", "e1ValuesByElement": root_values,
            "n1": 0, "n3": 0, "nu4": 0, "order": order,
            "rootPowerRemovalGauge": {"v0": -multiple, "u0": 0, "w2": 0,
                                       "phaseCorrection": "0"},
            "rootPowerIdentity": "order * e1 + d_s(v0) = 0 on every group element",
            "source": "0", "neutralProductTwister": "0", "neutralGaugePhase": "0",
        })
    return {
        "coefficientAction": "Z_s", "freeRank": h1.free_rank,
        "torsion": list(h1.torsion), "generatorCount": width,
        "presentation": [q] if any(q) else [],
        "groupPresentation": {"generatorElementIndices": generators,
                              "generatorSigns": signs,
                              "representativeWordsByElement": words,
                              "relators": relators},
        "relatorMatrix": h1.relator_matrix,
        "cocycleBasisColumnsOnGenerators": h1.cocycle_basis_columns,
        "cocycleBasisColumnsOnAllElements": values,
        "principalCoboundaryCoordinates": q,
        "principalCoboundaryValuesByElement": [sign - 1 for sign in character],
        "roots": roots,
        "certificate": {"multiplicationTableValidated": True,
                        "characterValidated": True,
                        "saturatedIntegerKernel": True,
                        "allCrossedHomomorphismPairsChecked": True,
                        "crossedHomomorphismIdentityCount": pair_checks,
                        "principalCoboundaryElementCount": len(table),
                        "neutralRootPowerElementCount": len(table) * len(roots),
                        "finiteGroupSanityCheckPassed": True},
    }


def presentation_invariants(rows: list[list[int]], columns: int) -> dict:
    """Smith invariants of an actual integer relation presentation."""
    from sympy import Matrix, ZZ
    from sympy.matrices.normalforms import smith_normal_form

    if not _integer(columns) or columns < 0:
        raise ValueError("Presentation generator count must be a nonnegative integer.")
    if not isinstance(rows, list) or any(not isinstance(row, list) or len(row) != columns or
           any(not _integer(x) for x in row) for row in rows):
        raise ValueError("The integer relation presentation has invalid entries or dimensions.")
    matrix = Matrix(rows) if rows and columns else Matrix.zeros(len(rows), columns)
    smith = smith_normal_form(matrix, domain=ZZ)
    diagonal = [abs(int(smith[i, i])) for i in range(min(smith.shape)) if smith[i, i]]
    if any(b % a for a, b in zip(diagonal, diagonal[1:])):
        raise ArithmeticError("Smith diagonal is not in divisibility order.")
    return {"torsion": [x for x in diagonal if x > 1],
            "freeRank": columns - len(diagonal), "smithNonzeroDiagonal": diagonal}


def _extend_classification(result: dict, neutral_computation, recovery_root=None) -> dict:
    """Extend one completed CI result without certifying a physical identification."""
    data, ci, run = result["input"], result["classification"], result["run"]
    if run.get("status") == "recovered_complete" and recovery_root is not None:
        from pathlib import Path
        from scripts.recover_paired_campaign import parse, validate_recovered_case
        validate_recovered_case(recovery_root, data.get("id"))
        original = Path(recovery_root) / data["id"] / "result.json"
        if parse(original.read_bytes()) != result:
            raise ValueError("Recovery validation is not bound to this exact CI result.")
    elif run.get("status") != "complete" or run.get("exitCode") != 0:
        raise ValueError("Only successfully completed or explicitly validated recovered CI runs can be extended.")
    if data.get("id") != run.get("id") or data.get("spin") not in ("spinless", "spin_half"):
        raise ValueError("CI run identity or physical-spin metadata is inconsistent.")
    if ci.get("spatialDimension") != 3:
        raise ValueError("The CI result must have spatial dimension three.")
    if ci.get("theory") != "U(1)^f insulator":
        raise ValueError("The input must be a U(1)^f insulator CI result.")
    if ci.get("neutralE8Included", False):
        raise ValueError("The input result already includes the neutral E8 sector.")
    if ci.get("nativeChainIdentitiesVerified") is False:
        raise ValueError("The CI result reports failed native chain identities.")
    if not isinstance(ci.get("generators"), list) or not isinstance(ci.get("witnesses"), list):
        raise ValueError("The CI result must retain its completed roots and relation witnesses.")
    count = ci.get("presentationGeneratorCount")
    if count != len(ci["generators"]):
        raise ValueError("CI roots do not match its presentation generator count.")
    ci_smith = presentation_invariants(ci.get("presentation"), count)
    if ci_smith["torsion"] != ci.get("torsion") or ci_smith["freeRank"] != ci.get("freeRank"):
        raise ValueError("The CI advertised group disagrees with its actual relation presentation.")
    neutral = neutral_computation(data)
    offset = neutral["generatorCount"]
    rows = [row + [0] * count for row in neutral["presentation"]]
    rows += [[0] * offset + row for row in ci["presentation"]]
    combined = presentation_invariants(rows, offset + count)
    generators = deepcopy(neutral["roots"]) + [
        {"kind": "embedded-CI-root", "ciGeneratorIndex": j,
         "combinedGeneratorIndex": offset + j, "e1": 0,
         "completedCIRoot": deepcopy(generator)} for j, generator in enumerate(ci["generators"])]
    if "principalGaugeRelation" in neutral:
        neutral_witnesses = [{"kind": "neutral-principal-gauge", **deepcopy(neutral["principalGaugeRelation"])}]
        if neutral.get("torsionRootWitness") is not None:
            neutral_witnesses.append({"kind": "neutral-torsion-root", **deepcopy(neutral["torsionRootWitness"])})
    else:
        neutral_witnesses = [{**deepcopy(root), "kind": "neutral-root-power", "neutralRootIndex": j}
                             for j, root in enumerate(neutral["roots"])]
    return {
        "theory": "U(1)^f insulator", "spatialDimension": 3,
        "orderedFields": ["e_1", "n_1", "n_3", "nu_4"],
        "coefficientActions": ["s", "s", "rho", "s"],
        "model": MODEL,
        "scope": "E8-inclusive selected 3+1D four-data model, with the CI sector as computed",
        "neutralE8Included": True,
        "physicalClassificationCertified": False,
        "physicalKernelIdentification": "not_certified_by_this_calculation",
        "physicalScopeCaveat": PHYSICAL_CAVEAT,
        "torsion": combined["torsion"], "freeRank": combined["freeRank"],
        "smithNonzeroDiagonal": combined["smithNonzeroDiagonal"],
        "presentationGeneratorCount": offset + count,
        "presentation": rows, "generators": generators,
        "coordinateBlocks": {"neutralE8": {"start": 0, "count": offset},
                             "ciSector": {"start": offset, "count": count},
                             "indexConvention": "zero_based"},
        "witnesses": neutral_witnesses + [
            {"kind": "CI-witness-embedding", "ciGeneratorOffset": offset,
             "location": "classification.ciSector.witnesses",
             "rule": "Keep each CI coordinate and prepend zero neutral coordinates."}],
        "e8H1": neutral,
        "ciSector": deepcopy(ci),
        "ciPresentationCheck": ci_smith,
        "selectedSection": {"neutralSource": "0", "neutralTerminalTwister": "0",
                            "mixedTerminalTwister": "0", "neutralGaugePhase": "0",
                            "jointGaugeRule": "Independent neutral principal gauge and full CI gauge",
                            "reference": "docs/e8/3p1.md"},
        "legacyNeutralE8AbsentByCohomology": {
            "inputValue": ci.get("neutralE8AbsentByCohomology"),
            "usedAsPhysicalCertificate": False},
    }


def extend_classification(result: dict, *, recovery_root=None) -> dict:
    """Extend a finite point-group result in the selected neutral section."""
    return _extend_classification(result, finite_pointgroup_h1, recovery_root=recovery_root)
