#!/usr/bin/env python3
"""Independent physical D2/D2d center-state adjoining audit.

Induce every one-dimensional site representation to a finite symmetry orbit.
Fermionic orbit states use a determinant; bosonic orbit states use a product.
This audits 0D states and ordinary mobile atomic orbits only, before CI bubbles.
It never supplies values to the AHSS backend.
"""
from functools import lru_cache
from itertools import product
from pathlib import Path
import argparse
import hashlib
import json
import sympy as sp
from sympy.matrices.normalforms import smith_normal_form

MOD = 16  # All character denominators of the groups audited here divide 16.


class DoubleGroup:
    def __init__(self, record):
        self.n = record["order"]
        self.table = record["multiplication"]
        self.epsilon = record["geometric_pin_minus"]
        if record["spin"] == "spinless":
            self.epsilon = [[0] * self.n for _ in range(self.n)]
        self.identity = 0
        self.parity = self.n
        self.inverses = [next(y for y in range(2 * self.n) if self.mul(x, y) == 0)
                         for x in range(2 * self.n)]

    def mul(self, x, y):
        ex, gx = divmod(x, self.n)
        ey, gy = divmod(y, self.n)
        return self.table[gx][gy] + self.n * ((ex + ey + self.epsilon[gx][gy]) % 2)

    def closure(self, generators):
        members = [0]
        for x in members:
            for g in generators:
                y = self.mul(x, g)
                if y not in members:
                    members.append(y)
        return members

    def generators(self, subgroup):
        generators = []
        for g in subgroup:
            if g not in self.closure(generators):
                generators.append(g)
        return generators

    @lru_cache(maxsize=None)
    def characters(self, subgroup, parity):
        generators = self.generators(subgroup)
        choices = []
        for g in generators:
            order = len(self.closure([g]))
            assert MOD % order == 0
            choices.append(range(0, MOD, MOD // order))
        answer = []
        for assigned in product(*choices):
            phases = {0: 0}
            queue = [0]
            valid = True
            for x in queue:
                for g, exponent in zip(generators, assigned):
                    y = self.mul(x, g)
                    value = (phases[x] + exponent) % MOD
                    if y in phases and phases[y] != value:
                        valid = False
                        break
                    if y not in phases:
                        phases[y] = value
                        queue.append(y)
                if not valid:
                    break
            if valid and phases[self.parity] == parity * (MOD // 2):
                answer.append(phases)
        return answer

    def induced_orbit_phase(self, subgroup, character, g, fermionic):
        cosets, representatives = [], []
        for r in range(2 * self.n):
            if any(r in c for c in cosets):
                continue
            representatives.append(r)
            cosets.append({self.mul(r, h) for h in subgroup})
        permutation, phase = [], 0
        for r in representatives:
            gr = self.mul(g, r)
            j = next(j for j, c in enumerate(cosets) if gr in c)
            permutation.append(j)
            h = self.mul(self.inverses[representatives[j]], gr)
            phase += character[h]
        sign = sum(permutation[i] > permutation[j]
                   for i in range(len(permutation)) for j in range(i + 1, len(permutation))) % 2
        if fermionic:
            phase += (MOD // 2) * sign
        return phase % MOD, permutation


def audit(record):
    if record["name"] not in ("D2", "D2d") or record["dimension"] != 3:
        raise ValueError("This audit is restricted to spatial D2 and D2d.")
    group = DoubleGroup(record)
    entire = tuple(range(2 * group.n))
    central_characters = group.characters(entire, 0)
    assert len(central_characters) == 4
    center_generators = next((a, b) for a in range(1, group.n) for b in range(a + 1, group.n)
                             if len({(chi[a], chi[b]) for chi in central_characters}) == 4)
    charge_step = 1 if group.characters(entire, 1) else 2
    matrices = [sp.Matrix(m) for m in record["matrices"]]
    # Every point stabilizer fixes an intersection of group-element fixed
    # subspaces. Enumerate that finite arrangement exactly, then choose a point
    # outside its proper subspaces. This is exhaustive, not a grid heuristic.
    equation_spaces = [sp.zeros(0, 3)]
    seen = {()}
    for equations in equation_spaces:
        for matrix in matrices:
            combined = equations.col_join(matrix - sp.eye(3))
            rref, pivots = combined.rref()
            reduced = rref[:len(pivots), :]
            key = tuple(reduced)
            if key not in seen and len(pivots) < 3:
                seen.add(key)
                equation_spaces.append(reduced)
    stabilizers = {}
    for equations in equation_spaces:
        basis = sp.Matrix.hstack(*equations.nullspace())
        fixed = tuple(i for i, matrix in enumerate(matrices)
                      if (matrix - sp.eye(3)) * basis == sp.zeros(3, basis.cols))
        for trial in range(1, 2 * group.n + 2):
            v = basis * sp.Matrix([trial ** k for k in range(basis.cols)])
            if tuple(i for i, matrix in enumerate(matrices) if matrix * v == v) == fixed:
                denominator = sp.ilcm(*[value.q for value in v])
                stabilizers[fixed] = [int(value * denominator) for value in v]
                break
        else:
            raise AssertionError("failed to choose a generic point on a fixed-space stratum")
    relations = [[0, 2, 0], [0, 0, 2]]
    witnesses = []
    for fixed, point in sorted(stabilizers.items()):
        subgroup = tuple(sorted([g + e * group.n for g in fixed for e in (0, 1)]))
        multiplicity = group.n // len(fixed)
        for site_charge in (0, 1, 2):
            for character in group.characters(subgroup, site_charge % 2):
                charge = site_charge * multiplicity
                assert charge % charge_step == 0
                orbit_data = [group.induced_orbit_phase(subgroup, character, g, site_charge % 2)
                              for g in range(group.n)]
                all_phases = [data[0] for data in orbit_data]
                for g in range(group.n):
                    for h in range(group.n):
                        assert (all_phases[g] + all_phases[h] - all_phases[group.table[g][h]]
                                - (MOD // 2) * charge * group.epsilon[g][h]) % MOD == 0
                phases = [all_phases[g] for g in center_generators]
                assert all(x in (0, MOD // 2) for x in phases)
                relation = [charge // charge_step] + [x // (MOD // 2) for x in phases]
                if any(relation) and relation not in relations:
                    relations.append(relation)
                    witnesses.append({"point": list(point), "point_stabilizer": list(fixed),
                                      "orbit_size": multiplicity, "site_charge": site_charge,
                                      "site_character_exponents_mod_16": {str(g): character[g] for g in subgroup},
                                      "induced_center_character_exponents_mod_16": all_phases,
                                      "center_generator_orbit_permutations": [orbit_data[g][1] for g in center_generators],
                                      "relation": relation})
    diagonal = smith_normal_form(sp.Matrix(relations), domain=sp.ZZ).diagonal()
    orders = [abs(int(x)) for x in diagonal]
    return {"id": record["id"], "physical_spin": record["spin"],
            "scope": "Physical center states modulo all point-stabilizer atomic orbits, before any CI bubble relation.",
            "stabilizer_coverage": "Exact arrangement of intersections of Fix(g); one generic representative per nonzero stratum, with every full center projective-character identity verified.",
            "center_charge_step": charge_step,
            "odd_charge_center_has_one_dimensional_representation": charge_step == 1,
            "center_character_generator_indices": list(center_generators),
            "presentation_coordinate_order": [f"charge/{charge_step}", "character_1", "character_2"],
            "atomic_orbit_relations": relations,
            "torsion_before_CI_bubbles": [x for x in orders if x > 1],
            "freeRank_before_CI_bubbles": orders.count(0),
            "orbit_witnesses": witnesses}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    record = json.loads(args.input.read_text())
    result = audit(record)
    result["inputSHA256"] = hashlib.sha256(args.input.read_bytes()).hexdigest()
    text = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.write_text(text)
    else:
        print(text, end="")
