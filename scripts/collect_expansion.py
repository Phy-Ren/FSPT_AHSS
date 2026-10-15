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


def load_campaign(root, kind, allow_recovered=False):
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
        recovery_check = None
        if run.get("status") == "recovered_complete":
            if not allow_recovered or kind != "ci":
                raise ValueError(f"Recovered CI runs require explicit --allow-recovered: {directory}")
            from scripts.recover_paired_campaign import validate_recovered_case
            recovery_check = validate_recovered_case(root, case)
        elif run.get("status") != "complete" or run.get("exitCode") != 0:
            raise ValueError(f"Failed or incomplete selected run: {directory}")
        if result["run"] != run:
            raise ValueError(f"Inconsistent selected run metadata: {directory}")
        if data != result["input"] or data["id"] != case or run["id"] != case:
            raise ValueError(f"Input identity mismatch: {directory}")
        if sha(directory / "input.json") != run["inputSHA256"] or run["sourceSHA256"] != source["sha256"]:
            raise ValueError(f"Input/source hash mismatch: {directory}")
        c = result["classification"]
        check = {"id": case, "inputHashVerified": True, "sourceHashVerified": True,
                 "independentSmithGroup": presentation_check(c)}
        if recovery_check is not None:
            check["explicitRecoveryAcceptance"] = recovery_check
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
            if parent.get("run", {}).get("status") == "recovered_complete":
                proof = run.get("ciRecoveryValidation", {})
                if (not allow_recovered or proof.get("recoveredComplete") is not True
                        or proof.get("cancellationReportSHA256") != parent["run"].get("cancellationReportSHA256")):
                    raise ValueError(f"Recovered CI parent requires explicit validated recovery: {case}")
                check["recoveredCIParentRequiresMatchingValidatedCICampaign"] = True
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


def selection_plan_requests(path):
    """Parse explicit subsets; relative roots are relative to the plan file.

    A plan never edits or weakens a parent's selection/recovery ledger. The
    caller validates the complete parent before applying any subset below.
    """
    path = path.resolve()
    raw = path.read_bytes()
    entries = json.loads(raw)
    if not isinstance(entries, list) or not entries:
        raise ValueError("A selection plan must be a nonempty JSON list.")
    requests = []
    for index, entry in enumerate(entries):
        if not isinstance(entry, dict) or set(entry) != {"kind", "root", "cases"}:
            raise ValueError("Each selection-plan entry requires exactly kind, root and cases.")
        kind, name, cases = entry["kind"], entry["root"], entry["cases"]
        if not isinstance(kind, str) or kind not in ("ci", "e8", "four"):
            raise ValueError("Unknown selection-plan calculation kind.")
        if not isinstance(name, str) or not name.strip() or "\x00" in name:
            raise ValueError("A selection-plan root must be a nonempty filesystem path.")
        root = Path(name)
        if not root.is_absolute():
            root = path.parent / root
        root = root.resolve()
        if not root.is_dir():
            raise ValueError(f"Selection-plan root is not a directory: {root}")
        if (not isinstance(cases, list) or not cases
                or any(not isinstance(case, str) or not case or Path(case).name != case
                       or case in (".", "..") for case in cases)
                or len(set(cases)) != len(cases)):
            raise ValueError("Selection-plan cases must be distinct, nonempty case identifiers.")
        requests.append({"kind": kind, "root": root, "cases": cases,
                         "plan": {"path": str(path), "SHA256": hashlib.sha256(raw).hexdigest(),
                                  "entryIndex": index}})
    return requests


def load_requests(requests, allow_recovered=False):
    """Validate every original campaign, then select explicit complete cases."""
    seen = set()
    for request in requests:
        key = (request["kind"], request["root"].resolve())
        if key in seen:
            raise ValueError(f"Duplicate campaign request: {key[0]} {key[1]}")
        seen.add(key)
    records = {kind: {} for kind in ("ci", "e8", "four")}
    checks, provenance = [], []
    for request in requests:
        kind = request["kind"]
        loaded, audited, source = load_campaign(request["root"], kind, allow_recovered=allow_recovered)
        if request["cases"] is not None:
            selected = request["cases"]
            missing = set(selected) - set(loaded)
            if missing:
                raise ValueError(f"Selection-plan cases are missing from the validated {kind} parent: {sorted(missing)}")
            # Keep the original selection-file identity, including the recovery
            # ledger's full selection. Only result/check inclusion is narrowed.
            source.update(originalSelection=list(source["selection"]),
                          originalSelectionSHA256=source["selectionSHA256"],
                          requestedSubset=list(selected), acceptedSelection=list(selected),
                          fullParentValidation={"allSelectedParentCasesPassed": True,
                                                "caseCount": len(loaded)},
                          selectionPlan=request["plan"])
            loaded = {case: loaded[case] for case in selected}
            audited = [item for item in audited if item["id"] in loaded]
            source["resultHashes"] = {case: source["resultHashes"][case] for case in selected}
        duplicates = set(records[kind]) & set(loaded)
        if duplicates:
            raise ValueError(f"Duplicate {kind} cases: {sorted(duplicates)}")
        records[kind].update(loaded)
        checks.extend(dict(item, kind=kind) for item in audited)
        provenance.append(source)
    return records, checks, provenance


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    for kind in ("ci", "e8", "four"):
        parser.add_argument("--" + kind + "-root", type=Path, action="append", default=[])
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--selection-plan", type=Path,
                        help="JSON list of {kind, root, cases}; fully validate each original parent before selecting its subset. Relative roots use the plan directory.")
    parser.add_argument("--allow-recovered", action="store_true",
                        help="Revalidate stopped-campaign recovery evidence; ordinary acceptance remains the default")
    args = parser.parse_args()
    if not any((args.ci_root, args.e8_root, args.four_root, args.selection_plan)):
        parser.error("At least one calculation root is required.")
    requests = [{"kind": kind, "root": root.resolve(), "cases": None}
                for kind in ("ci", "e8", "four") for root in getattr(args, kind + "_root")]
    if args.selection_plan:
        requests.extend(selection_plan_requests(args.selection_plan))
    records, checks, provenance = load_requests(requests, allow_recovered=args.allow_recovered)
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
