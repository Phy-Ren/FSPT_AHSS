#!/usr/bin/env python3
"""Accept exact 4+1D case records and attach separately sourced comparisons."""
from __future__ import annotations

import argparse
from copy import deepcopy
import hashlib
import json
from pathlib import Path
import shutil
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insulator.e8_pointgroup import presentation_invariants
from insulator.cyclic_physical import compare_physical
from scripts.collect_expansion import cyclic_filtration


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(value, indent=2, sort_keys=True) + "\n")


def group(value):
    return {"torsion": list(value["torsion"]), "freeRank": value["freeRank"]}


def source_columns(ledger, target, family):
    references, sources = {}, {}
    labels = {"v015_cyclic": "v0.15 physical eta proof",
              "bahri_gilkey_1987": "Bahri–Gilkey 1987",
              "freed_hopkins_v6": "Freed–Hopkins v6: stated sector"}
    for reference in target["sources"]:
        if reference["scope"] not in ("zero_uniform", "full_and_zero_uniform"):
            continue
        if "source" in reference:
            key = reference["source"]
            source = deepcopy(ledger["sources"][key])
            source["columnLabel"] = labels.get(key, key)
            source["location"] = reference.get("locator", source.get("locator", ""))
            if key == "v015_cyclic":
                source.update(title="Electronic Insulator AHSS v0.15: physical cyclic proof",
                              url="https://github.com/Phy-Ren/FSPT_AHSS/blob/insulator/formulas/v015_reference/manuscript/appendices/K_cyclic_proof.tex")
        else:
            key = "derived_" + "__".join(reference["sources"])
            originals = [ledger["sources"][k] for k in reference["sources"]]
            source = {"authors": "Independent bordism derivation",
                      "version": "2026 review of pinned primary theorems",
                      "title": "Specified Smith sequence and bordism coefficients",
                      "columnLabel": "Smith/Freed–Hopkins derivation",
                      "url": "https://github.com/Phy-Ren/FSPT_AHSS/blob/insulator/docs/4p1d/calibration/BORDISM_TARGETS.md",
                      "location": "Source-specific tangent structures and exact sequence",
                      "method": reference.get("method", "") + "; " + "; ".join(
                          "[" + item.get("locator", item.get("version", "primary source"))
                          + "](" + item["url"] + ")" for item in originals)}
        sources[key] = source
        references[key] = {"group": deepcopy(reference["group"]),
                           "scope": reference["scope"],
                           "method": reference.get("method", source.get("method", "")),
                           "fullUniformSectionApplicable": family == "internal_cyclic"}
    if not references:
        raise ValueError("No independently sourced reference for the computed response sector.")
    return sources, references


def validate_record(path, source):
    record = read(path)
    run, inputs, classification = record["run"], record["input"], record["classification"]
    if (run["status"] != "complete" or run["exitCode"] != 0
            or inputs["dimension"] != 4 or run["sourceSHA256"] != source["sha256"]):
        raise ValueError("Incomplete or mismatched 4+1D case: " + str(path))
    if read(path.parent / "input.json") != inputs or digest(path.parent / "input.json") != run["inputSHA256"]:
        raise ValueError("Case input hash mismatch.")
    if read(path.parent / "run.json") != run:
        raise ValueError("Case run metadata disagrees with its completed record.")
    count = classification["presentationGeneratorCount"]
    if group(presentation_invariants(classification["presentation"], count)) != group(classification):
        raise ValueError("Independent Smith reduction disagrees with the computed presentation.")
    evidence = record.get("evidence")
    if evidence and digest(path.parent / evidence["path"]) != evidence["sha256"]:
        raise ValueError("Complete root/gauge evidence hash mismatch.")
    if inputs["family"] == "internal_cyclic":
        if inputs["s"] != 0 or inputs["rho"] != 0 or inputs["omega"] != "0":
            raise ValueError("Cyclic physical calibration has the wrong symmetry background.")
        physical = compare_physical(inputs["order"], classification["presentation"])
        if record["physicalComparison"] != physical:
            raise ValueError("Saved physical character kernel does not reproduce.")
        classification["finalFiltration"] = cyclic_filtration(classification)
        if classification["actualGroupOrder"] != inputs["order"] ** 4:
            raise ValueError("Cyclic presentation has the wrong total order.")
    if set(classification["finalFiltration"]) != {"e", "n", "charge", "phase"}:
        raise ValueError("Four final filtration groups are required.")
    return record


def target_id(inputs):
    if inputs["family"] == "internal_cyclic":
        return "internal_cyclic_" + str(inputs["order"])
    return inputs["referenceTarget"]


def validate_background(inputs, target):
    """A group match alone cannot validate the symmetry dictionary."""
    def canonical(value):
        return str(value).replace("alpha cup alpha / 2", "alpha^2/2")
    for key in ("s", "rho", "omega"):
        if canonical(inputs[key]) != canonical(target["background"][key]):
            raise ValueError("Physical reference uses a different symmetry background: " + key)
    if inputs["family"] == "internal_cyclic":
        if target["background"]["G"] != "C" + str(inputs["order"]):
            raise ValueError("Physical reference uses a different cyclic group.")
    elif (inputs["group"] != "C2" or inputs["intrinsic"]["n0I"] != 0
          or inputs["intrinsic"]["n0J"] != 0):
        raise ValueError("Signed calibration requires the selected C2 intrinsic-zero sector.")


def collect(campaigns, output):
    ledger_path = ROOT / "docs/4p1d/calibration/bordism_targets.json"
    ledger = read(ledger_path)
    targets = {case["id"]: case for case in ledger["cases"]}
    sources, records, hashes, checks = {}, [], {}, []
    output.mkdir(parents=True, exist_ok=False)
    for family, directory in campaigns:
        destination = output / "raw" / family
        shutil.copytree(directory, destination)
        source = read(destination / "source.json")
        encoded = json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(encoded).hexdigest() != source["sha256"]:
            raise ValueError("Invalid computation source manifest.")
        campaign = read(destination / "campaign.json")
        if campaign["status"] != "complete" or campaign["sourceSHA256"] != source["sha256"]:
            raise ValueError("Only a completed selected campaign can be accepted.")
        case_paths = sorted(destination.rglob("result.json"))
        if not case_paths:
            raise ValueError("No completed case records were found.")
        selected = read(destination / "selection.json")
        if family == "cyclic":
            actual = sorted(read(path)["input"]["order"] for path in case_paths)
        else:
            actual = sorted(read(path)["input"]["id"] for path in case_paths)
            selected = ["signed_" + case + "_4p1" for case in selected]
        if actual != sorted(selected) or len(actual) != len(set(actual)):
            raise ValueError("Selected case coverage is incomplete or duplicated.")
        for path in case_paths:
            raw = validate_record(path, source)
            inputs, classification = deepcopy(raw["input"]), deepcopy(raw["classification"])
            target = targets[target_id(inputs)]
            validate_background(inputs, target)
            additions, references = source_columns(ledger, target, inputs["family"])
            sources.update(additions)
            if inputs["family"] == "internal_cyclic":
                inputs["name"] = "C" + str(inputs["order"])
                inputs["background"] = {"s": 0, "rho": 0, "omega": "0"}
            else:
                inputs.setdefault("name", target["symmetry"])
                inputs.setdefault("background", deepcopy(target["background"]))
            provenance = {"path": str(path.relative_to(ROOT)), "record_sha256": digest(path),
                          "source_sha256": raw["run"]["sourceSHA256"],
                          "input_sha256": raw["run"]["inputSHA256"],
                          "started_utc": raw["run"]["startedUTC"],
                          "physical_reference_target": target["id"]}
            normalized = {"input": inputs, "classification": classification,
                          "run": raw["run"], "provenance": provenance,
                          "references": references}
            if inputs["family"] == "internal_cyclic":
                uniform = raw["uniformResponse"]
                if (uniform["intrinsicFreeRank"] != 2 or uniform["intrinsicBasis"] != ["I", "J"]
                        or uniform["cochainIntrinsicImplemented"] is not False
                        or uniform["zeroLowerLift"]["intrinsicInputs"] != [[1, 0], [0, 1]]):
                    raise ValueError("The direct-product uniform section is not fully specified.")
                normalized["uniformResponse"] = {"freeRank": 2, "canonicalSectionVerified": True,
                                                 "basis": ["I", "J"], "source": uniform}
                normalized["physicalComparison"] = raw["physicalComparison"]
            records.append(normalized)
            checks.append({"id": inputs["id"], "independentSmith": "PASS",
                           "caseEvidenceHash": "PASS", "referenceComparisons": {
                               key: "match" if group(value["group"]) == group(classification) else "mismatch"
                               for key, value in references.items()}})
        for path in destination.rglob("*"):
            if path.is_file():
                hashes[str(path.relative_to(output))] = digest(path)
    if len({r["input"]["id"] for r in records}) != len(records):
        raise ValueError("Duplicate cases across campaigns.")
    shutil.copyfile(ledger_path, output / "reference_targets.json")
    hashes["reference_targets.json"] = digest(output / "reference_targets.json")
    validation = {"accepted": True, "status": "PASS", "completeResultCount": len(records),
                  "selectedCases": sorted(r["input"]["id"] for r in records), "checks": checks,
                  "policy": "Complete mathematical runs are preserved even if an independent physical reference disagrees."}
    write(output / "validation.json", validation)
    hashes["validation.json"] = digest(output / "validation.json")
    accepted = {"schemaVersion": 1, "accepted": True, "records": records,
                "sources": sources, "filesSHA256": dict(sorted(hashes.items())),
                "scope": "Explicit selected 4+1D internal backgrounds; no general global or intrinsic solver is asserted."}
    write(output / "accepted.json", accepted)
    return validation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cyclic", type=Path, required=True)
    parser.add_argument("--signed", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    campaigns = [("cyclic", args.cyclic.resolve())]
    if args.signed:
        campaigns.append(("signed", args.signed.resolve()))
    result = collect(campaigns, args.output.resolve())
    print("PASS:", result["completeResultCount"], "accepted 4+1D backgrounds")


if __name__ == "__main__":
    main()
