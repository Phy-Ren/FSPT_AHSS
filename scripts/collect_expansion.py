#!/usr/bin/env python3
"""Accept complete immutable 3+1D affine and 4+1D cyclic calculation campaigns.

All selected inputs must be present and complete. No literature value enters
acceptance or independent integer-presentation checks. Raw records are preserved.
"""
from __future__ import annotations

import argparse
from functools import reduce
from fractions import Fraction
import hashlib
import json
from math import gcd
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insulator.e8_h1 import saturated_kernel
from insulator.e8_pointgroup import presentation_invariants


def read(path):
    return json.loads(path.read_text())


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def group(record):
    return {key: record[key] for key in ("torsion", "freeRank")}


def presentation_check(classification):
    count = classification.get("presentationGeneratorCount", classification.get("generatorCount"))
    if type(count) is not int or count < 0:
        raise ValueError("An explicit nonnegative presentation generator count is required.")
    actual = presentation_invariants(classification["presentation"], count)
    if group(actual) != group(classification):
        raise ValueError("Independent Smith reduction disagrees with the reported group.")
    return group(actual)


def filling_check(classification):
    """Check the saved primitive-cell charge descends through every relation."""
    filling = classification["spaceGroupFilling"]
    values = filling["generatorFillings"]
    generators = classification["generators"]
    count = classification["presentationGeneratorCount"]
    if (len(values) != count or len(generators) != count
            or any(type(value) is not int for value in values)
            or any(root["kind"] not in ("phase", "charge", "CI") for root in generators)):
        raise ValueError("Primitive filling must give one integer per presentation generator.")
    if any(len(row) != count or sum(x*y for x,y in zip(row, values)) != 0
           for row in classification["presentation"]):
        raise ValueError("A presentation relation changes primitive-cell filling.")
    charge = [value for value, root in zip(values, generators) if root["kind"] == "charge"]
    sheet = [value for value, root in zip(values, generators) if root["kind"] == "CI"]
    if (charge != filling["chargeRootSubgroupGeneratorFillings"]
            or sheet != filling["ciGeneratorFillings"]
            or any(value != 0 for value, root in zip(values, generators) if root["kind"] == "phase")):
        raise ValueError("Primitive filling does not respect the saved root decomposition.")
    step = reduce(gcd, map(abs, values), 0)
    charge_step = reduce(gcd, map(abs, charge), 0)
    if step != filling["fillingStep"] or charge_step != filling["chargeRootSubgroupFillingStep"]:
        raise ValueError("The claimed filling subgroup disagrees with the generator gcd.")
    basis = filling["primitiveTranslationVectors"]
    if len(basis) != 3 or any(len(row) != 3 for row in basis):
        raise ValueError("Primitive translation filling requires a rank-three basis.")
    a, b, c = [[Fraction(str(x)) for x in row] for row in basis]
    volume = (a[0]*(b[1]*c[2]-b[2]*c[1]) - a[1]*(b[0]*c[2]-b[2]*c[0])
              + a[2]*(b[0]*c[1]-b[1]*c[0]))
    if volume <= 0 or volume != Fraction(str(filling["primitiveCellVolume"])):
        raise ValueError("Primitive-cell orientation or volume is inconsistent.")
    if (filling.get("primitiveBasisGeneratesFullTranslationKernel") is not True
            or filling.get("allPresentationRelationsHaveZeroFilling") is not True):
        raise ValueError("The native primitive-lattice certificate is missing.")
    return {"fillingStep": step, "chargeSubgroupFillingStep": charge_step,
            "everyPresentationRelationPreservesFilling": True,
            "positivePrimitiveCellVolume": str(volume),
            "nativePrimitiveLatticeCertificatePresent": True}


def cyclic_filtration(classification):
    """F_k/F_(k+1) by exact elimination, F_k=span of root indices k,... ."""
    count = classification["presentationGeneratorCount"]
    kinds = [x["kind"] for x in classification["generators"]]
    if count == 0:
        if kinds or classification["presentation"] or group(classification) != {"torsion": [], "freeRank": 0}:
            raise ValueError("Inconsistent zero-generator cyclic presentation.")
        return {key: {"torsion": [], "freeRank": 0} for key in ("e", "n", "charge", "phase")}
    if count != 4 or kinds != ["neutral-E8", "CI-sheet", "charge", "shared-phase"]:
        raise ValueError("Cyclic filtration requires the recorded four ordered roots.")
    relations = classification["presentation"]
    result = {}
    for k, name in enumerate(("e", "n", "charge", "phase")):
        equations = [[row[i] for row in relations] for i in range(k)]
        kernel = saturated_kernel(equations, len(relations))
        width = len(kernel[0]) if kernel else 0
        values = [sum(kernel[i][j]*relations[i][k] for i in range(len(relations))) for j in range(width)]
        divisor = reduce(gcd, (abs(x) for x in values), 0)
        result[name] = {"torsion": [divisor] if divisor > 1 else [], "freeRank": int(divisor == 0)}
    return result


def load_campaign(root, kind):
    root = root.resolve()
    selection, source = read(root / "selection.json"), read(root / "source.json")
    if not isinstance(selection, list) or not selection or len(set(selection)) != len(selection):
        raise ValueError(f"Empty or duplicated selection: {root}")
    encoded = json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()
    if hashlib.sha256(encoded).hexdigest() != source["sha256"]:
        raise ValueError(f"Invalid source manifest: {root}")
    cases = [f"internal_cyclic_{n}_4p1" for n in selection] if kind == "four" else selection
    records, checks = {}, []
    for case in cases:
        if not isinstance(case, str) or Path(case).name != case or case in ("", ".", ".."):
            raise ValueError(f"Invalid selected case: {case}")
        directory = root / case
        run, result, data = read(directory / "run.json"), read(directory / "result.json"), read(directory / "input.json")
        if run.get("status") != "complete" or run.get("exitCode") != 0 or result["run"] != run:
            raise ValueError(f"Failed, incomplete, or inconsistent selected run: {directory}")
        if data != result["input"] or data["id"] != case or run["id"] != case:
            raise ValueError(f"Input identity mismatch: {directory}")
        if sha(directory / "input.json") != run["inputSHA256"] or run["sourceSHA256"] != source["sha256"]:
            raise ValueError(f"Input/source hash mismatch: {directory}")
        c = result["classification"]
        check = {"id": case, "inputHashVerified": True, "sourceHashVerified": True,
                 "independentSmithGroup": presentation_check(c)}
        if kind in ("ci", "four"):
            if read(directory / "native.json") != c:
                raise ValueError(f"Native output differs from the accepted result: {directory}")
            if not isinstance(c.get("nativeCompletionChecks"), int) or c["nativeCompletionChecks"] < 1:
                raise ValueError(f"No completed-state certificate: {directory}")
            check["nativeCompletionChecks"] = c["nativeCompletionChecks"]
        if kind == "ci":
            if data["dimension"] != 3 or data["family"] not in ("spacegroup", "point3"):
                raise ValueError(f"Not a 3+1D crystalline input: {case}")
            if c.get("nativeChainIdentitiesVerified") is not True:
                raise ValueError(f"Missing native chain certificate: {case}")
            check["nativeChainIdentitiesVerified"] = True
            if data["family"] == "spacegroup":
                check["independentPresentationFillingCheck"] = filling_check(c)
        elif kind == "four":
            if (data["dimension"], data["family"], data["s"], data["rho"], data["omega"], data["intrinsicR0Included"]) != (4, "internal_cyclic", 0, 0, "0", False):
                raise ValueError(f"Unexpected cyclic4D symmetry or coefficient scope: {case}")
            if data["crystallineSpinConvention"] != "not_assumed" or data["orderedFields"] != ["e_2", "n_2", "n_4", "nu_5"]:
                raise ValueError(f"Unexpected cyclic4D field/spin convention: {case}")
            if c["actualGroupOrder"] != c["expectedOrderFromFiltration"] or c["freeRank"] != 0:
                raise ValueError(f"Cyclic order check failed: {case}")
            product = 1
            for n in c["torsion"]:
                product *= n
            if product != c["actualGroupOrder"]:
                raise ValueError(f"Cyclic group order disagrees with Smith factors: {case}")
            if data["order"] > 1 and (c.get("barCompletionChecks", 0) < 1 or len(c["witnesses"]) != 4):
                raise ValueError(f"Missing cyclic root/bar completion certificates: {case}")
            # U1SolveData.nativeObstruction is the solved input cochain, not
            # the remainder after subtracting d(nativePrimitive). It can be
            # nonzero even when the recorded relation is exact (e.g. C6).
            for witness in c["witnesses"]:
                for key in ("nativePhasePrimitive", "residualNativePhase"):
                    if not isinstance(witness.get(key), list):
                        raise ValueError(f"Missing exact root phase primitive witness: {case}")
                    for value in witness[key]:
                        Fraction(str(value))
            check.update(barCompletionChecks=c["barCompletionChecks"],
                         rootPhasePrimitiveWitnessesPresent=True,
                         finalFiltrationFromPresentation=cyclic_filtration(c),
                         filtrationMethod="Saturated integer relation combinations with all earlier root coordinates zero; gcd of the next coordinate.")
        elif kind == "e8":
            if data["dimension"] != 3 or data["family"] not in ("spacegroup", "point3") or c.get("neutralE8Included") is not True:
                raise ValueError(f"Not an accepted 3+1D E8 extension: {case}")
            parent_path = directory / "ci_result.json"
            parent = read(parent_path)
            if sha(parent_path) != run["ciResultSHA256"] or parent["input"] != data or c["ciSector"] != parent["classification"]:
                raise ValueError(f"E8 parent record mismatch: {case}")
            if parent["run"]["sourceSHA256"] != run["ciSourceSHA256"] or parent["run"] != run["ciRun"]:
                raise ValueError(f"E8 parent provenance mismatch: {case}")
            check.update(ciParentSHA256=sha(parent_path), neutralSmithGroup=presentation_check(c["e8H1"]))
        records[case] = {"record": result, "directory": directory}
        checks.append(check)
    provenance = {"directory": str(root), "selection": selection, "kind": kind,
                  "selectionSHA256": sha(root / "selection.json"), "source": source,
                  "resultHashes": {case: sha(root / case / "result.json") for case in cases}}
    return records, checks, provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for kind in ("ci", "e8", "four"):
        parser.add_argument("--" + kind + "-root", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    if not any((args.ci_root, args.e8_root, args.four_root)):
        parser.error("At least one calculation root is required.")
    records = {kind: {} for kind in ("ci", "e8", "four")}
    checks, provenance = [], []
    for kind in records:
        for root in getattr(args, kind + "_root"):
            loaded, audited, source = load_campaign(root, kind)
            duplicates = set(records[kind]) & set(loaded)
            if duplicates:
                raise ValueError(f"Duplicate {kind} cases: {sorted(duplicates)}")
            records[kind].update(loaded)
            checks.extend(dict(item, kind=kind) for item in audited)
            provenance.append(source)
    if set(records["ci"]) != set(records["e8"]):
        raise ValueError("The selected 3+1D CI and E8 cases must cover exactly the same inputs.")
    for case, extended in records["e8"].items():
        parent = extended["directory"] / "ci_result.json"
        original = records["ci"][case]
        if read(parent) != original["record"] or parent.read_bytes() != (original["directory"] / "result.json").read_bytes():
            raise ValueError(f"The E8 extension consumed a different exact CI artifact: {case}")
    # All validation finishes before the output is created; accepted records are immutable.
    args.output.mkdir(parents=True, exist_ok=False)
    collections = []
    for family, path, kind in (("spacegroup", "3p1d/space_groups", "e8"),
                               ("point3", "3p1d/point_groups", "e8"),
                               ("internal_cyclic", "4p1d/internal_cyclic", "four")):
        selected = [value["record"] for value in records[kind].values() if value["record"]["input"]["family"] == family]
        if not selected:
            continue
        selected.sort(key=lambda x: x["input"]["id"])
        ids = {r["input"]["id"] for r in selected}
        target = args.output / path
        write(target / "results.json", selected)
        if kind == "e8":
            write(target / "ci_results.json", [records["ci"][r["input"]["id"]]["record"] for r in selected])
        own_checks = [item for item in checks if item["id"] in ids]
        write(target / "validation.json", {"accepted": True, "selectedCases": sorted(ids),
              "completeResultCount": len(selected), "missingOrFailedSelectedCases": [],
              "scope": selected[0]["classification"]["scope"], "checks": own_checks})
        write(target / "provenance.json", [entry for entry in provenance if ids & set(entry["resultHashes"])])
        files = ["results.json", "validation.json", "provenance.json"]
        if kind == "e8":
            files.append("ci_results.json")
        collections.append({"family": family, "path": path, "count": len(selected),
                            "filesSHA256": {name: sha(target / name) for name in files}})
    write(args.output / "collection.json", {"accepted": True, "collections": collections,
          "collectorSHA256": sha(Path(__file__)), "smithRuntimeSHA256": sha(ROOT / "insulator/e8_pointgroup.py"),
          "integerKernelRuntimeSHA256": sha(ROOT / "insulator/e8_h1.py")})
    print(json.dumps(collections, indent=2))


if __name__ == "__main__":
    main()
