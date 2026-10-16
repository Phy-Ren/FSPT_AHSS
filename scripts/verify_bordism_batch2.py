#!/usr/bin/env python3
"""Independently replay the arithmetic of the prospective bordism ledger.

Only the standard library and primary-reference data are used.  In particular,
this script neither imports a classification engine nor reads computed results.
The topological theorems are assumptions documented in BATCH2_TARGETS.md; the
script checks their finite integer consequences, not the theorems themselves.
"""
from __future__ import annotations

import argparse
from collections import Counter
from functools import reduce
import hashlib
from itertools import combinations, product
import json
from math import comb, gcd, prod
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
DEFAULT_LEDGER = ROOT / "docs/4p1d/calibration/batch2_targets.json"
DEFAULT_OUTPUT = ROOT / "docs/4p1d/calibration/batch2_reference_replay.json"


def require(condition, message):
    if not condition:
        raise ValueError(message)


def prime_factors(number):
    factors = {}
    prime = 2
    while prime * prime <= number:
        while number % prime == 0:
            factors[prime] = factors.get(prime, 0) + 1
            number //= prime
        prime += 1
    if number > 1:
        factors[number] = factors.get(number, 0) + 1
    return factors


def invariant_factors(cyclic_orders):
    """Combine cyclic summands by independent primary decomposition."""
    primary = {}
    for order in cyclic_orders:
        require(type(order) is int and order >= 1, "Invalid cyclic order")
        for prime, exponent in prime_factors(order).items():
            primary.setdefault(prime, []).append(prime ** exponent)
    width = max(map(len, primary.values()), default=0)
    result = [1] * width
    for orders in primary.values():
        padded = [1] * (width - len(orders)) + sorted(orders)
        result = [a * b for a, b in zip(result, padded)]
    require(all(b % a == 0 for a, b in zip(result, result[1:])), "Noncanonical invariant factors")
    return result


def determinant(matrix):
    if not matrix:
        return 1
    return sum((-1) ** j * value * determinant(
        [row[:j] + row[j + 1:] for row in matrix[1:]])
        for j, value in enumerate(matrix[0]))


def finite_presentation_factors(rows):
    """Use determinantal divisors, not the classifier's Smith implementation."""
    size = len(rows)
    require(all(len(row) == size for row in rows), "Expected square finite presentation")
    previous, factors = 1, []
    for width in range(1, size + 1):
        minors = (abs(determinant([[rows[i][j] for j in cols] for i in indices]))
                  for indices in combinations(range(size), width)
                  for cols in combinations(range(size), width))
        divisor = reduce(gcd, minors, 0)
        require(divisor and divisor % previous == 0, "Invalid determinantal divisors")
        factors.append(divisor // previous)
        previous = divisor
    return [value for value in factors if value > 1]


def cyclic_ku5_rows(order):
    return [[order, 0, 0], [comb(order, 2), order, 0],
            [comb(order, 3), comb(order, 2), order]]


def cyclic_target(order):
    g2, g3 = gcd(order, 2), gcd(order, 3)
    return invariant_factors([order // (g2 * g3), order // g2, order,
                              g2 * g2 * g3 * order])


def logarithm_exact(value, prime):
    exponent = 0
    while value > 1 and value % prime == 0:
        value //= prime
        exponent += 1
    require(value == 1, "An annihilator count is not a prime power")
    return exponent


def tor_kernel(order, other, saved):
    """Enumerate ker(D_M) in A_N, keeping the nonsplit integral lattice."""
    rows = [[order, 0, 0], [comb(order, 2), order, 0], [0, 0, order]]
    endomorphism = [[other, 0, comb(other, 2)], [0, other, 0], [0, 0, other]]
    require(saved["domain_relation_rows"] == rows, "Wrong Tor domain relation matrix")
    require(saved["endomorphism_column_matrix"] == endomorphism, "Wrong Tor endomorphism")

    def canonical(vector):
        x, y, z = vector
        quotient, y = divmod(y, order)
        return ((x - quotient * comb(order, 2)) % order, y, z % order)

    def apply(vector):
        return canonical([sum(a * b for a, b in zip(row, vector)) for row in endomorphism])

    zero = (0, 0, 0)
    require(all(canonical(row) == zero and apply(row) == zero for row in rows),
            "The map does not descend through the domain relations")
    representatives = list(product(range(order), repeat=3))
    require(len(representatives) == abs(determinant(rows)) == saved["domain_order"],
            "Wrong finite Tor domain order")
    kernel = [vector for vector in representatives if apply(vector) == zero]
    counts, primary = {}, []
    for prime in prime_factors(order):
        sequence = [1]
        power = prime
        while True:
            count = sum(canonical([power * value for value in vector]) == zero for vector in kernel)
            if count == sequence[-1]:
                break
            sequence.append(count)
            power *= prime
        logs = [logarithm_exact(value, prime) for value in sequence]
        at_least = [b - a for a, b in zip(logs, logs[1:])] + [0]
        require(all(a >= b for a, b in zip(at_least, at_least[1:])),
                "Annihilator counts cannot be those of a finite abelian group")
        for exponent in range(1, len(at_least)):
            primary.extend([prime ** exponent] * (at_least[exponent - 1] - at_least[exponent]))
        counts[str(prime)] = sequence
    factors = invariant_factors(primary)
    require(len(kernel) == prod(factors) == saved["kernel_order"], "Wrong mixed kernel order")
    require(counts == saved["kernel_prime_power_annihilator_counts"], "Wrong kernel annihilator counts")
    require(factors == saved["torsion"], "Wrong mixed Tor invariant factors")
    return {"domainOrder": len(representatives), "kernelOrder": len(kernel),
            "kernelPrimePowerAnnihilatorCounts": counts, "torsion": factors,
            "endomorphismWellDefined": True}


def mod2_smash_homology_rank(factors, degree):
    # Reduced H_*(BC2;F2) has one class in each positive degree.
    if factors == 0:
        return int(degree == 0)
    return comb(degree - 1, factors - 1) if degree >= factors else 0


def ossa_odd_ku(factors, degree):
    """Iterate the actual Ossa spectrum splitting, in the required odd degrees."""
    require(factors >= 1 and degree % 2 == 1, "Ossa replay uses positive smash rank and odd degree")
    if degree < 1:
        return []
    if factors == 1:
        return [2 ** ((degree + 1) // 2)]
    result = ossa_odd_ku(factors - 1, degree - 2)
    for j in range((degree - 2) // 2 + 1):
        multiplicity = (j + 1) * mod2_smash_homology_rank(factors - 2, degree - 2 - 2 * j)
        result += [2] * multiplicity
    return invariant_factors(result)


def derive_case(case):
    background, identifier = case["background"], case["id"]
    require(all(str(background[key]) == "0" for key in ("s", "rho", "omega")),
            "The reference derivation requires the stated trivial direct-product background")
    detail, free = {}, 0
    if identifier.startswith("internal_cyclic_"):
        family, order = "cyclic", background["order"]
        torsion = cyclic_target(order)
        ku = finite_presentation_factors(cyclic_ku5_rows(order))
        require(torsion == invariant_factors(ku + [order]), "Cyclic eta and bordism presentations disagree")
        require(prod(torsion) == order ** 4, "Wrong cyclic bordism order")
        detail = {"cyclicKu5": ku, "shiftedKu1": [order], "groupOrder": prod(torsion)}
        if any(ref.get("source") == "bahri_gilkey_1987" for ref in case["sources"]):
            require(order > 2 and order & (order - 1) == 0, "Bahri-Gilkey comparison has the wrong scope")
            published = invariant_factors([order // 2, order // 2, order, 4 * order])
            require(published == torsion, "Published 2-power comparison disagrees")
            detail["bahriGilkeyPowerOfTwoComparison"] = "PASS"
    elif identifier.startswith("internal_abelian_"):
        factors, derivation = background["factors"], case["derivation"]
        if len(factors) == 2:
            family = "rank_two_finite"
            order, other = factors
            rows = [cyclic_ku5_rows(value) for value in factors]
            ku = [finite_presentation_factors(matrix) for matrix in rows]
            require(rows == derivation["cyclic_presentation_rows"], "Wrong cyclic presentation witnesses")
            require(ku == derivation["ku5_cyclic_terms"], "Wrong cyclic ku5 terms")
            mixed = tor_kernel(order, other, derivation["ku5_mixed_kernel"])
            torsion = invariant_factors(ku[0] + ku[1] + mixed["torsion"] + factors)
            require(derivation["shifted_ku1"] == factors, "Wrong shifted ku1 summands")
            require(derivation["decomposition_invariant_factors"] == torsion, "Wrong product decomposition")
            detail = {"cyclicKu5": ku, "mixedTorKernel": mixed, "shiftedKu1": factors}
        else:
            family, rank = "higher_elementary_two", len(factors)
            require(3 <= rank <= 4 and factors == [2] * rank, "Unsupported higher finite reference")
            smash = {str(k): ossa_odd_ku(k, 5) for k in range(1, 5)}
            multiplicities = [comb(rank, k) for k in range(1, rank + 1)]
            require(smash == derivation["ku5_smash_terms_by_number_of_factors"], "Wrong Ossa smash terms")
            require(multiplicities == derivation["cartesian_multiplicities"], "Wrong Cartesian multiplicities")
            require(derivation["shifted_ku1"] == [2] * rank, "Wrong elementary-two shifted ku1")
            cyclic = [2] * rank
            for k, multiplicity in enumerate(multiplicities, start=1):
                cyclic += smash[str(k)] * multiplicity
            torsion = invariant_factors(cyclic)
            require(prod(torsion) == derivation["zero_uniform_group_order"], "Wrong higher elementary-two order")
            detail = {"ku5SmashTerms": smash, "cartesianMultiplicities": multiplicities,
                      "shiftedKu1": [2] * rank, "groupOrder": prod(torsion)}
    elif identifier.startswith("translations_"):
        rank = background["translationRank"]
        require(1 <= rank <= 4 and case["atomic_filling_retained"] is True, "Wrong torus scope")
        multiplicities = {"TP5": 1, "TP3": comb(rank, 2), "TP1": comb(rank, 4)}
        free = 2 * comb(rank, 2) + comb(rank, 4)
        if "order" in background:
            family, order = "prospective_mixed_translations", background["order"]
            g2 = gcd(order, 2)
            a5, a3, a1 = cyclic_target(order), invariant_factors([order // g2, g2 * order]), [order]
            lower_rows = [[order, 0], [comb(order, 2), order]]
            require(a3 == finite_presentation_factors(lower_rows), "Wrong lower cyclic bordism extension")
            torsion = invariant_factors(a5 + a3 * comb(rank, 2) + a1 * comb(rank, 4))
            derivation = case["derivation"]
            expected = {"cyclic_TP5_torsion": a5, "cyclic_TP3_torsion": a3,
                        "cyclic_TP1_torsion": a1, "torus_multiplicities": multiplicities,
                        "full_free_rank": free + 2}
            require(derivation == expected, "Wrong mixed torus stable-splitting witness")
            detail = {"stableSplitting": expected, "cochainCampaignCompletedByThisReplay": False}
        else:
            family, torsion = "translations", []
            layers = {"e2": comb(rank, 2), "n2": comb(rank, 2), "n4": comb(rank, 4), "nu5": 0}
            require(case["zero_uniform_layer_ranks"] == layers, "Wrong translation layer multiplicities")
            detail = {"torusMultiplicities": multiplicities, "layerRanks": layers}
    else:
        raise ValueError("Unsupported reference target: " + identifier)
    zero = {"torsion": torsion, "freeRank": free}
    full = {"torsion": torsion, "freeRank": free + 2}
    require(case["zero_uniform_target"] == zero and case["full_target"] == full,
            "The independently derived group disagrees with the ledger: " + identifier)
    require(case["calculation_completed"] is False and case["record_kind"] == "prospective_reference_target",
            "A reference ledger must not masquerade as a completed computation")
    require(case["e8_included"] is True and case["spatial_dimension"] == 4
            and case["spacetime_dimension"] == 5, "Wrong physical scope")
    for reference in case["sources"]:
        require(reference["scope"] in ("zero_uniform", "full_and_zero_uniform"), "Unexpected reference scope")
        require(reference["group"] == zero, "Source comparison group differs from the derived target")
    return {"id": identifier, "family": family, "status": "PASS",
            "zeroUniformTarget": zero, "fullTarget": full, "derivation": detail}


def replay(ledger):
    cases = ledger["cases"]
    require(len({case["id"] for case in cases}) == len(cases), "Duplicate target IDs")
    for case in cases:
        for reference in case["sources"]:
            keys = [reference["source"]] if "source" in reference else reference["sources"]
            require(all(key in ledger["sources"] for key in keys), "Missing primary source metadata")
    records = [derive_case(case) for case in cases]
    return {"schema": "independent_bordism_batch2_reference_replay_v1", "status": "PASS",
            "referenceTargetsVerified": len(records),
            "families": dict(sorted(Counter(row["family"] for row in records).items())),
            "engineOutputUsed": False, "classificationEngineImported": False,
            "theoremAssumptions": [
                "Integral reduced degree-five Spin-c to ku plus shifted-ku bridge from the displayed ABS Euler-square construction.",
                "Cyclic connective K-homology Gysin presentations and length-one Kunneth resolution.",
                "The actual Ossa spectrum equivalence, not merely an abstract homology-group decomposition.",
                "Interacting Spin-c coefficient groups and stable torus splitting with atomic filling retained."],
            "limitations": [
                "This is a reference-arithmetic replay, not a proof of the cited topological theorems.",
                "No formula-engine run, differential, stacking primitive, or physical cochain-root identification is certified here.",
                "All ledger entries remain prospective reference targets; completed campaigns are recorded separately.",
                "Mixed translation targets are future benchmarks, not computed formula examples.",
                "Only commuting direct-product backgrounds s=rho=omega=0 are covered; twisted and nonsymmorphic groups are outside scope."],
            "records": records}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger", type=Path, default=DEFAULT_LEDGER)
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    data = replay(json.loads(args.ledger.read_text()))
    data["referenceLedgerSHA256"] = hashlib.sha256(args.ledger.read_bytes()).hexdigest()
    data["verifierSHA256"] = hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(data, indent=2, sort_keys=True) + "\n")
    print(json.dumps({key: data[key] for key in ("status", "referenceTargetsVerified", "families", "engineOutputUsed")}, sort_keys=True))


if __name__ == "__main__":
    main()
