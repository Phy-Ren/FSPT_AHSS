#!/usr/bin/env python3
"""Compare computed insulator data only where source scope permits equality."""
from pathlib import Path
import argparse
import json
import sympy as sp

ROOT = Path(__file__).resolve().parent
ALIASES = {"pm": "p1m1", "pg": "p1g1", "cm": "c1m1", "pmm": "p2mm",
           "pmg": "p2mg", "pgg": "p2gg", "cmm": "c2mm", "p4m": "p4mm",
           "p4g": "p4gm", "p6m": "p6mm"}
PLANAR_NAMES = {"Cs": "D1", "C2v": "D2", "C3v": "D3", "C4v": "D4", "C6v": "D6"}
POINT3_NAMES = {"C3i": "S6", "Ci": "Ci", "Cs": "Cs"}


def group_signature(orders):
    """Canonical invariant factors and free rank for a finitely generated group."""
    orders = [int(x) for x in orders]
    if any(x < 0 for x in orders):
        raise ValueError("negative cyclic order")
    rank = orders.count(0)
    primary = {}
    for order in orders:
        if order > 1:
            for p, e in sp.factorint(order).items():
                primary.setdefault(int(p), []).append(int(e))
    width = max(map(len, primary.values()), default=0)
    invariant = [1] * width
    for prime, powers in primary.items():
        for i, exponent in enumerate([0] * (width - len(powers)) + sorted(powers)):
            invariant[i] *= prime ** exponent
    return {"torsion": invariant, "freeRank": rank}


def _check(label, calculated, expected, source):
    if calculated is None:
        return {"quantity": label, "status": "not_computed", "source": source}
    actual = group_signature(calculated)
    target = group_signature(expected)
    return {"quantity": label, "status": "match" if actual == target else "mismatch",
            "calculated": actual, "published": target, "source": source}


def _load(filename):
    return json.loads((ROOT / filename).read_text())


def compare(result):
    """Accept backend result plus id/family/name/spin metadata from the runner.

    Raw phaseOrders and chargeOrders deliberately never substitute for the final
    quotients. A missing quantity is reported as such, not inferred from a table.
    """
    if "input" in result and "classification" in result:
        result = {**result["input"], **result["classification"]}
    family = result.get("family") or result["id"].split("_")[0]
    name, spin = result["name"], result["spin"]
    checks = []
    if family in ("point2", "wallpaper") and result.get("uniformIQHIncluded") is not False:
        return {"id": result["id"], "checks": [{"status": "scope_mismatch",
                "reason": "2D source comparison requires explicitly fixed uniform IQH n0=0"}]}
    final = None
    if "torsion" in result and "freeRank" in result:
        final = result["torsion"] + [0] * result["freeRank"]
    if family == "wallpaper":
        table = _load("wallpaper_layers_2112.15533.json")
        row = next(r for r in table["rows"] if r["physical_spin"] == spin
                   and r["name_as_printed"] == ALIASES.get(name, name))
        for key, expected_key in (("finalChargeOrders", "charge_orders"),
                                  ("finalPhaseOrders", "phase_after_incoming_orders")):
            computed = result.get(key)
            if computed is not None:
                computed = list(computed) + [0] * result.get(key.replace("Orders", "FreeRank"), 0)
            checks.append(_check(key, computed, row[expected_key], table["source"]))
        table = _load("wallpaper_stacking_2012.15657.json")
        row = next(r for r in table["rows"] if r["physical_spin"] == spin and r["name"] == name)
        checks.append(_check("stacking", final, row["stacking_orders"], table["source"]))
        # Embedded free charge normalization requires an actual witness. Group
        # isomorphism alone cannot establish equality of Z and the physical 2Z.
        checks.append({"quantity": "free_charge_embedding", "status": "requires_generator_witness",
                       "published_charge_step": row["free_charge_step_as_printed"]})
    elif family == "point2":
        table = _load("point2_stacking_2012.15657.json")
        row = next(r for r in table["rows"] if r["physical_spin"] == spin
                   and r["name_as_printed"] == PLANAR_NAMES.get(name, name))
        check = _check("stacking", final, row["stacking_orders_as_printed"], table["source"])
        if row["comparison_status"] == "source_discrepancy_requires_review":
            check["status"] = "published_source_discrepancy"
            check["reason"] = table["discrepancy"]
        checks.append(check)
    elif family == "point3":
        table = _load("point3_full_2204.13558.json")
        target_name = POINT3_NAMES.get(name, name)
        def plain_name(row):
            return row["name_as_printed"].split("=")[0].replace("$", "").replace("_", "").replace("{", "").replace("}", "")
        row = next(r for r in table["rows"] if r["physical_spin"] == spin and plain_name(r) == target_name)
        check = _check("stacking", final, row["stacking_orders"], table["source"])
        if not (result.get("neutralE8Included") is True or
                result.get("neutralE8AbsentByCohomology") is True):
            check["status"] = "scope_mismatch"
            check["reason"] = "Published classification includes an independent neutral E8 sector; no sector projection witness supplied."
        checks.append(check)
        if result.get("neutralE8Included") is not True:
            projections = _load("point3_named_e8_quotient_2204.13558.json")
            projection = next((r for r in projections["rows"]
                               if r["name"] == name and r["physical_spin"] == spin), None)
            if projection is not None:
                projected = _check("stacking_mod_named_neutral_E8", final,
                                   projection["quotient_by_named_E8_orders"], projections["source"])
                projected["neutral_generator"] = {key: projection[key] for key in
                    ("named_generator", "generator_order", "generator_description", "source_root_line")}
                projected["comparison_limit"] = projection["comparison_limit"]
                checks.append(projected)
    else:
        raise ValueError(f"unknown family {family!r}")
    return {"id": result["id"], "checks": checks}


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("result", type=Path)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args()
    data = json.loads(args.result.read_text())
    answer = [compare(row) for row in data] if isinstance(data, list) else compare(data)
    output = json.dumps(answer, indent=2) + "\n"
    if args.output:
        args.output.write_text(output)
    else:
        print(output, end="")
