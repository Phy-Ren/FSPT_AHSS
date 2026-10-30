#!/usr/bin/env python3
"""Independently audit saved unsigned cyclic four-data root relations.

The Python check pairs explicit bar cochains with the standard cyclic
five-cycle. It does not use the GAP resolution, its completed charge root,
or its primitive solver. A separate exact GAP check verifies the saved
native phase primitives against the actual resolution differential.
"""
from __future__ import annotations

import argparse
from fractions import Fraction
import hashlib
from itertools import combinations, product
import json
from pathlib import Path
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insulator import api as ci, e8
from insulator.notation import legacy_metadata_view
from scripts.classify import gap_literal, write_json


def canonical_local(order, arguments):
    vertices = [0]
    for value in arguments:
        vertices.append((vertices[-1] + value) % order)
    a = ci.Cochain(5, 1, {(i, j): (vertices[j] - vertices[i]) % order
                          for i, j in combinations(range(6), 2)})
    x = a.d().sc(Fraction(1, order))
    xx = x.cup(x)
    zero = lambda degree: ci.Cochain(5, degree, {})
    symmetry = ci.Symmetry(zero(2), zero(1), zero(1))
    charge = e8.State(zero(2), zero(2), xx,
                      ci.integral_cartan(x, x).sc(Fraction(1, 2)))
    neutral = e8.State(x, zero(2), zero(4),
                       a.cup(xx).sc(Fraction(1, 3 * order)))
    sheet = e8.State(zero(2), x, zero(4),
                     a.cup(xx).sc(Fraction(1, 6 * order)))
    return a, x, zero, symmetry, charge, neutral, sheet


def bar_root_relations(order):
    """Return coefficients in the canonical E8, CI, charge, phase basis."""
    if order == 1:
        return {"presentation": [], "cycleTerms": 0,
                "canonicalChargePhasePairing": "0"}
    phase_pairings = [Fraction(0)] * 3
    charge_pairing = Fraction(0)
    charge_coefficient = (order * (order - 1) // 2) % order
    # Terms with i=0 or j=0 vanish in the normalized bar complex.
    for i, j in product(range(1, order), repeat=2):
        a, x, zero, symmetry, charge, neutral, sheet = canonical_local(
            order, (1, i, 1, j, 1))
        top = tuple(range(6))
        charge_pairing += charge.nu_p3(top)
        for index, root in enumerate((neutral, sheet, charge)):
            power = root.power(order, symmetry, 4).gauge(
                symmetry, 4, a.sc(-1) if index == 0 else zero(1),
                a.sc(-1) if index == 1 else zero(1), zero(3))
            q = charge_coefficient if index == 1 else 0
            power = power.stack(charge.power(-q, symmetry, 4), symmetry, 4)
            multiple = ((order * (order - 1) // 2 - q) // order
                        if index == 1 else 1 if index == 2 else 0)
            power = power.gauge(symmetry, 4, zero(1), zero(1),
                                a.cup(x).sc(-multiple))
            assert power.e_p.maxabs() == power.n_p.maxabs() == power.n_p2.maxabs() == 0
            phase_pairings[index] += power.nu_p3(top)
    coefficients = [(value * order) % order for value in phase_pairings]
    assert all(value.denominator == 1 for value in coefficients)
    # The analytic neutral relation supplies an independent closed formula.
    assert coefficients[0] == (order * (1 - order * order) // 3) % order
    phase_coefficients = [int(value) for value in coefficients]
    rows = [[order, 0, 0, -phase_coefficients[0]],
            [0, order, -charge_coefficient, -phase_coefficients[1]],
            [0, 0, order, -phase_coefficients[2]], [0, 0, 0, order]]
    return {"presentation": rows, "cycleTerms": (order - 1) ** 2,
            "rootPhasePairings": [str(value % 1) for value in phase_pairings],
            "canonicalChargePhasePairing": str(charge_pairing % 1)}


def native_witness_audit(records, gap="gap"):
    """Check d(native primitive)=saved native phase residual, modulo one."""
    lines = ['U1_ROOT:=' + gap_literal(str(ROOT)) + ';;',
             'Read(Concatenation(U1_ROOT,"/gap/load.g"));;', 'checks:=[];;']
    for data in records:
        result = data["classification"]
        order = result["group"]["order"]
        lines.append('c:=U1CyclicContext(' + str(order) + ',0,0,0);;')
        for witness in result["witnesses"]:
            # Build GAP rational expressions explicitly; JSON strings would
            # otherwise remain strings in the GAP list.
            rational_list = lambda values: '[' + ','.join(str(Fraction(x)) for x in values) + ']'
            primitive = rational_list(witness["nativePhasePrimitive"])
            residual = rational_list(witness["residualNativePhase"])
            lines.extend([
                'p:=' + primitive + ';;r:=' + residual + ';;',
                'image:=U1ApplyDifferential(c,4,"U1s",p);;',
                'if Length(image)<>Length(r) or ForAny(image-r,x->U1Mod1(x)<>0) then Error("Saved phase witness is not a boundary");fi;',
                'Add(checks,rec(order:=' + str(order) + ',root:=' + gap_literal(witness["root"])
                + ',verified:=true,nonzeroResidual:=ForAny(r,x->U1Mod1(x)<>0)));;'])
    with tempfile.TemporaryDirectory() as directory:
        output = Path(directory) / "native.json"
        driver = Path(directory) / "audit.g"
        lines.extend(['out:=OutputTextFile(' + gap_literal(str(output)) + ',false);;',
                      'SetPrintFormattingStatus(out,false);;WriteLine(out,U1JSON(checks));;CloseStream(out);;QUIT_GAP(0);'])
        driver.write_text('\n'.join(lines) + '\n')
        process = subprocess.run([gap, "-q", "-b", "--quitonbreak", str(driver)],
                                 cwd=ROOT, capture_output=True, text=True, timeout=120)
        if process.returncode or not output.is_file():
            raise RuntimeError(process.stdout + process.stderr)
        return json.loads(output.read_text())


def audit(paths, gap="gap"):
    records, output = [], []
    for path in sorted(paths):
        data = legacy_metadata_view(json.loads(path.read_text()))
        result, inputs, run = data["classification"], data["input"], data["run"]
        order = inputs["order"]
        assert inputs["family"] == "internal_cyclic" and inputs["dimension"] == 4
        assert inputs["s"] == inputs["r"] == 0 and inputs["omega"] == "0"
        assert run["status"] == "complete" and run["exitCode"] == 0
        assert not result["physicalClassificationCertified"]
        assert result["incomingCohomology"] == {"sheet": [], "charge": []}
        assert result["terminalObstructionTargetOrders"] == []
        bar = bar_root_relations(order)
        assert bar["presentation"] == result["presentation"], (order, bar, result["presentation"])
        assert result["actualGroupOrder"] == result["expectedOrderFromFiltration"] == order ** 4
        # Record the explicit Cartan completion used by this independent
        # computation. Equality of the resulting presentations is checked
        # above; no pointwise equality with GAP's chosen primitive is used.
        assert bar["canonicalChargePhasePairing"] == "0"
        records.append(data)
        output.append({"order": order, "resultSHA256": hashlib.sha256(path.read_bytes()).hexdigest(),
                       "sourceSHA256": run["sourceSHA256"], "torsion": result["torsion"],
                       "independentBarCheck": bar})
    native = native_witness_audit(records, gap)
    return {"status": "PASS", "spatialDimension": 4,
            "scope": "Unsigned internal cyclic original four-data model; physical identification not inferred",
            "orderedFields": ["e_2", "n_2", "n_4", "nu_5"],
            "scriptSHA256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
            "cases": output, "nativePhaseBoundaryChecks": native,
            "nativePhaseBoundaryCheckCount": len(native)}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", type=Path, action="append", required=True,
                        help="A result.json or a directory containing such records")
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--gap", default="gap")
    args = parser.parse_args()
    if args.output.exists():
        parser.error("Use a new audit output path")
    paths = set()
    for path in args.input:
        paths.update([path] if path.is_file() else path.rglob("result.json"))
    if not paths:
        parser.error("No result.json records found")
    result = audit(paths, args.gap)
    write_json(args.output, result)
    print("PASS:", len(result["cases"]), "cyclic cases;",
          result["nativePhaseBoundaryCheckCount"], "native phase boundaries")


if __name__ == "__main__":
    main()
