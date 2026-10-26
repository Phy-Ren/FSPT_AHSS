"""Surviving 4+1D decoration layers for split finite Abelian symmetry.

Input cyclic orders describe A in G_f = Z_2^f x A.
The output gives invariant factors for each associated-graded layer, after
all outgoing obstructions and incoming identifications, before stacking
extensions.  Proof: proofs/SPLIT_DECORATION_LAYERS.md.
"""
from itertools import combinations
from math import prod
from sympy import factorint, isprime

LAYER_NAMES = ("pip", "majorana", "complex_fermion", "bosonic")


def _empty():
    return {name: [] for name in LAYER_NAMES}


def _clean(result):
    return {name: sorted(n for n in result[name] if n > 1)
            for name in LAYER_NAMES}


def split_support_layers(p, exponents):
    """Primary-support layer groups; positive exponents, prime p."""
    p = int(p)
    aa = sorted(int(a) for a in exponents)
    if not isprime(p) or any(a < 1 for a in aa):
        raise ValueError("p must be prime and exponents must be positive")
    result = _empty()
    k = len(aa)
    if k == 0 or k > 5:
        return result
    g = p**aa[0]
    if p != 2:
        if k == 1:
            result["pip"] = [g]
            result["bosonic"] = [g]
        else:
            result["bosonic"] = [g] * {2: 2, 3: 4, 4: 3, 5: 1}[k]
        return result
    if k == 1:
        result["pip"] = [g // 2]
        result["bosonic"] = [g // 2]
    elif k == 2:
        if aa != [1, 1]:
            result["complex_fermion"] = [2]
        if aa == [1, 2]:
            pass  # The incoming Majorana secondary class removes BSPT.
        elif aa[0] == aa[1]:
            result["bosonic"] = [g // 2, g // 2]
        else:
            result["bosonic"] = [g, g // 2]
    elif k == 3:
        result["bosonic"] = [2]*3 if aa == [1, 1, 1] else [g]*4
        if aa[0] < aa[1]:
            result["complex_fermion"] = [2]
        if aa[0] >= 2 or (aa[0] == 1 and aa[1] >= 3):
            result["majorana"] = [2]
    elif k == 4:
        result["bosonic"] = [g]*3
        if aa.count(1) <= 2:
            result["complex_fermion"] = [2]
    else:
        result["bosonic"] = [g]
    return _clean(result)


def invariant_factors(cyclic_orders):
    """Combine primary cyclic factors into invariant-factor order."""
    primary = {}
    for n in cyclic_orders:
        for p, a in factorint(int(n)).items():
            primary.setdefault(int(p), []).append(int(p)**int(a))
    width = max((len(ns) for ns in primary.values()), default=0)
    rows = [[1]*(width-len(ns)) + sorted(ns) for ns in primary.values()]
    return [prod(entries) for entries in zip(*rows)] if rows else []


def split_layers(orders):
    """Return {'pip': [...], 'majorana': [...], 'complex_fermion': [...], 'bosonic': [...]}.

    All lists are invariant factors, with trivial factors omitted.
    Every cyclic order must be a positive integer; order-one factors
    are harmless and are ignored.
    """
    sylow = {}
    for n in orders:
        if int(n) != n or n < 1:
            raise ValueError("cyclic orders must be positive integers")
        for p, a in factorint(int(n)).items():
            sylow.setdefault(int(p), []).append(int(a))
    result = _empty()
    for p, aa in sylow.items():
        for k in range(1, min(5, len(aa)) + 1):
            for subset in combinations(aa, k):
                block = split_support_layers(p, subset)
                for name in LAYER_NAMES:
                    result[name].extend(block[name])
    return {name: invariant_factors(values)
            for name, values in result.items()}


if __name__ == "__main__":
    import json
    import sys
    print(json.dumps(split_layers([int(n) for n in sys.argv[1:]]), indent=2))
