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
from insulator.notation import legacy_metadata_view
from insulator.cyclic_physical import compare_physical
from scripts.collect_expansion import cyclic_filtration


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return legacy_metadata_view(json.loads(path.read_text()))


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
            source["columnLabel"] = labels.get(key, source.get('columnLabel', key))
            source["location"] = reference.get("locator", source.get("locator", ""))
            if key == "v015_cyclic":
                source.update(title="Electronic Insulator AHSS v0.15: physical cyclic proof",
                              url="https://github.com/Phy-Ren/FSPT_AHSS/blob/insulator/formulas/v015_reference/manuscript/appendices/K_cyclic_proof.tex")
        else:
            key = "derived_" + "__".join(reference["sources"])
            if 'derivationURL' in reference:
                identity = json.dumps([reference.get('columnLabel'), reference.get('method'),
                                       reference['derivationURL']], separators=(',', ':')).encode()
                key += '_' + hashlib.sha256(identity).hexdigest()[:12]
            originals = [ledger["sources"][k] for k in reference["sources"]]
            source = {"authors": "Independent bordism derivation",
                      "version": "2026 review of pinned primary theorems",
                      "title": "Specified Smith sequence and bordism coefficients",
                      "columnLabel": reference.get('columnLabel', "Smith/Freed–Hopkins derivation"),
                      "url": reference.get('derivationURL', "https://github.com/Phy-Ren/FSPT_AHSS/blob/insulator/docs/4p1d/calibration/BORDISM_TARGETS.md"),
                      "location": "Source-specific tangent structures and exact sequence",
                      "method": reference.get("method", "") + "; " + "; ".join(
                          "[" + item.get("locator", item.get("version", "primary source"))
                          + "](" + item["url"] + ")" for item in originals)}
            if 'derivationURL' in reference:
                source['title'] = 'Specified Spin-c bordism decomposition'
                source['location'] = 'Explicit derivation from the linked primary theorems'
        sources[key] = source
        references[key] = {"group": deepcopy(reference["group"]),
                           "scope": reference["scope"],
                           "method": reference.get("method", source.get("method", "")),
                           "fullUniformSectionApplicable": family in ("internal_cyclic", "internal_abelian", "translations")}
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
        if inputs["s"] != 0 or inputs["r"] != 0 or inputs["omega"] != "0":
            raise ValueError("Cyclic physical calibration has the wrong symmetry background.")
        physical = compare_physical(inputs["order"], classification["presentation"])
        if record["physicalComparison"] != physical:
            raise ValueError("Saved physical character kernel does not reproduce.")
        classification["finalFiltration"] = cyclic_filtration(classification)
        if classification["actualGroupOrder"] != inputs["order"] ** 4:
            raise ValueError("Cyclic presentation has the wrong total order.")
    elif inputs['family'] == 'translations':
        from insulator.translation4p1 import verify_certificate
        certificate = read(path.parent / evidence['path'])
        if (certificate['resolution']['rank'] != inputs['translationRank']
                or (inputs['s'], inputs['r'], inputs['omega']) != (0, 0, '0')):
            raise ValueError('Translation certificate has a different input rank or symmetry background.')
        replay = verify_certificate(classification, certificate)
        if replay != record['certificateVerification']:
            raise ValueError('Saved translation certificate does not reproduce.')
    elif inputs['family'] == 'internal_abelian':
        from scripts.verify_abelian_4p1 import verify
        if (classification['group'] != {'family': 'internal_abelian', 'factors': inputs['factors']}
                or classification['background'] != {'schema_version': 2, 's': 0, 'r': 0, 'rho': 0, 'omega': 0}
                or (inputs['s'], inputs['r'], inputs['omega']) != (0, 0, '0')):
            raise ValueError('Finite abelian certificate has a different input group or symmetry background.')
        if read(path.parent / 'native.json') != classification:
            raise ValueError('Saved native abelian output differs from the mathematical record.')
        record['certificateVerification'] = verify(classification)
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
    for key in ("s", "r", "rho", "omega"):
        if canonical(inputs[key]) != canonical(target["background"][key]):
            raise ValueError("Physical reference uses a different symmetry background: " + key)
    if inputs["family"] == "internal_cyclic":
        if target["background"]["G"] != "C" + str(inputs["order"]):
            raise ValueError("Physical reference uses a different cyclic group.")
    elif inputs['family'] == 'internal_abelian':
        if inputs['factors'] != target['background']['factors']:
            raise ValueError('Physical reference uses different finite abelian factors.')
    elif inputs['family'] == 'translations':
        if inputs['translationRank'] != target['background']['translationRank']:
            raise ValueError('Physical reference uses a different translation rank.')
    elif (inputs["group"] != "C2" or inputs["intrinsic"]["n0I"] != 0
          or inputs["intrinsic"]["n0J"] != 0):
        raise ValueError("Signed calibration requires the selected C2 intrinsic-zero sector.")


def natural_uniform_section(inputs):
    """Independent physical section; never an intrinsic cochain calculation."""
    if (inputs['family'] != 'internal_abelian' or inputs['s'] != 0 or inputs['r'] != 0
            or inputs['omega'] != '0' or inputs.get('intrinsicPair') != [0, 0]):
        raise ValueError('The natural-section attachment requires the stated commuting direct product.')
    return {'intrinsicFreeRank': 2, 'intrinsicBasis': ['I', 'J'],
            'cochainIntrinsicImplemented': False,
            'zeroLowerLift': {'intrinsicInputs': [[1, 0], [0, 1]],
                             'lowerFields': {'e_2': 0, 'n_2': 0, 'n_4': 0, 'nu_5': 0},
                             'check': 'At s=r=omega=0, B=0 and the reviewed opened-sheet equations admit both zero-lower-data unit roots.',
                             'evidenceType': 'Direct substitution and naturality, not execution of an intrinsic solver.'},
            'section': 'Give each intrinsic I,J root the trivial action of the finite abelian group.',
            'splitting': 'Restriction composed with this inflation is the identity; the full physical group splits into its true relative kernel and Z^2.',
            'scope': 'This section alone does not identify the computed four-data model with the true relative kernel.'}


def collect(campaigns, output, additional_ledgers=(), extends=(), completed_selections=None):
    completed_selections = completed_selections or {}
    if set(completed_selections) - {family for family, _ in campaigns}:
        raise ValueError('A completed selection names an absent campaign.')
    ledger_path = ROOT / "docs/4p1d/calibration/bordism_targets.json"
    ledger = read(ledger_path)
    ledger_paths = [ledger_path] + [Path(p).resolve() for p in additional_ledgers]
    for path in ledger_paths[1:]:
        extra = read(path)
        for key, source in extra['sources'].items():
            if key in ledger['sources'] and ledger['sources'][key] != source:
                raise ValueError('Reference ledgers disagree on source metadata: ' + key)
            ledger['sources'][key] = source
        existing = {c['id']: c for c in ledger['cases']}
        overlaps = {c['id'] for c in extra['cases']} & set(existing)
        if overlaps != set(extra.get('replacesTargets', [])):
            raise ValueError('Duplicate physical reference target requires an explicit metadata refinement.')
        for case in extra['cases']:
            if case['id'] in overlaps:
                old = existing[case['id']]
                if (any(case['background'][k] != old['background'][k] for k in ('G', 's', 'r', 'rho', 'omega'))
                        or case['zero_uniform_target'] != old['zero_uniform_target']
                        or case['full_target'] != old['full_target']):
                    raise ValueError('A metadata refinement changed the physical target.')
            existing[case['id']] = case
        ledger['cases'] = list(existing.values())
    targets = {case["id"]: case for case in ledger["cases"]}
    sources, records, hashes, checks, campaign_checks = {}, [], {}, [], []
    output.mkdir(parents=True, exist_ok=False)
    for family, directory in campaigns:
        destination = output / "raw" / family
        shutil.copytree(directory, destination)
        source = read(destination / "source.json")
        encoded = json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()
        if hashlib.sha256(encoded).hexdigest() != source["sha256"]:
            raise ValueError("Invalid computation source manifest.")
        campaign = read(destination / "campaign.json")
        explicit = completed_selections.get(family)
        if (campaign["sourceSHA256"] != source["sha256"]
                or (campaign["status"] != "complete" and explicit is None)):
            raise ValueError("Only a completed selected campaign can be accepted.")
        case_paths = sorted(destination.rglob("result.json"))
        if not case_paths:
            raise ValueError("No completed case records were found.")
        selected = read(destination / "selection.json")
        original_selected = deepcopy(selected)
        if explicit is not None:
            if family in ('cyclic', 'signed'):
                raise ValueError('Explicit completed subsets currently require abelian/translation case IDs.')
            if (not isinstance(explicit, list) or not explicit
                    or any(not isinstance(case, str) for case in explicit)
                    or len(explicit) != len(set(explicit)) or not set(explicit) <= set(selected)):
                raise ValueError('A completed subset must be a nonempty distinct subset of the original selection.')
            selected = explicit
            case_paths = [path for path in case_paths if read(path)['input']['id'] in set(explicit)]
        if family == "cyclic":
            actual = sorted(read(path)["input"]["order"] for path in case_paths)
        elif family == 'signed':
            actual = sorted(read(path)["input"]["id"] for path in case_paths)
            selected = ["signed_" + case + "_4p1" for case in selected]
        else:
            actual = sorted(read(path)['input']['id'] for path in case_paths)
        if actual != sorted(selected) or len(actual) != len(set(actual)):
            raise ValueError("Selected case coverage is incomplete or duplicated.")
        campaign_checks.append({'campaign': family, 'originalStatus': campaign['status'],
                                'campaignSHA256': digest(destination / 'campaign.json'),
                                'originalSelection': original_selected, 'acceptedSelection': selected,
                                'explicitCompletedSubset': explicit is not None,
                                'excludedSelection': sorted(set(original_selected) - set(selected))
                                if explicit is not None else [],
                                'rawCampaignPreserved': True})
        for path in case_paths:
            raw = validate_record(path, source)
            inputs, classification = deepcopy(raw["input"]), deepcopy(raw["classification"])
            target = targets[target_id(inputs)]
            validate_background(inputs, target)
            additions, references = source_columns(ledger, target, inputs["family"])
            sources.update(additions)
            if inputs["family"] == "internal_cyclic":
                inputs["name"] = "C" + str(inputs["order"])
                inputs["background"] = {"schema_version": 2, "s": 0, "r": 0, "rho": 0, "omega": "0"}
            else:
                inputs.setdefault("name", target.get("symmetry", target['background']['G']))
                inputs.setdefault("background", deepcopy(target["background"]))
            provenance = {"path": str(path.relative_to(ROOT)), "record_sha256": digest(path),
                          "source_sha256": raw["run"]["sourceSHA256"],
                          "input_sha256": raw["run"]["inputSHA256"],
                          "started_utc": raw["run"]["startedUTC"],
                          "physical_reference_target": target["id"]}
            normalized = {"input": inputs, "classification": classification,
                          "run": raw["run"], "provenance": provenance,
                          "references": references}
            if 'certificateVerification' in raw:
                normalized['certificateVerification'] = raw['certificateVerification']
            if inputs["family"] in ("internal_cyclic", "internal_abelian", "translations"):
                uniform = raw.get('uniformResponse') or natural_uniform_section(inputs)
                if (uniform["intrinsicFreeRank"] != 2 or uniform["intrinsicBasis"] != ["I", "J"]
                        or uniform["cochainIntrinsicImplemented"] is not False
                        or uniform["zeroLowerLift"]["intrinsicInputs"] != [[1, 0], [0, 1]]):
                    raise ValueError("The direct-product uniform section is not fully specified.")
                normalized["uniformResponse"] = {"freeRank": 2, "canonicalSectionVerified": True,
                                                 "basis": ["I", "J"], "source": uniform}
                if 'physicalComparison' in raw:
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
    write(output / 'reference_targets.json', ledger)
    hashes["reference_targets.json"] = digest(output / "reference_targets.json")
    validation = {"accepted": True, "status": "PASS", "completeResultCount": len(records),
                  "selectedCases": sorted(r["input"]["id"] for r in records), "checks": checks,
                  "campaignSelections": campaign_checks,
                  "policy": "Complete mathematical runs are preserved even if an independent physical reference disagrees."}
    write(output / "validation.json", validation)
    hashes["validation.json"] = digest(output / "validation.json")
    accepted = {"schemaVersion": 1, "accepted": True, "records": records,
                "sources": sources, "filesSHA256": dict(sorted(hashes.items())),
                "scope": "Explicit selected 4+1D internal and translation backgrounds; no general global or intrinsic solver is asserted."}
    if extends:
        accepted['extends'] = [{'path': str(Path(p).resolve().relative_to(ROOT)), 'sha256': digest(Path(p))}
                               for p in extends]
    accepted['referenceLedgers'] = [{'path': str(p.relative_to(ROOT)), 'sha256': digest(p)} for p in ledger_paths]
    write(output / "accepted.json", accepted)
    return validation


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--cyclic", type=Path)
    parser.add_argument("--signed", type=Path)
    parser.add_argument('--abelian', type=Path, action='append', default=[],
                        help='Completed abelian campaign; repeat for separately bounded runs.')
    parser.add_argument('--translations', type=Path)
    parser.add_argument('--ledger', type=Path, action='append', default=[])
    parser.add_argument('--extends', type=Path, action='append', default=[])
    parser.add_argument('--completed-selections', type=Path,
                        help='Explicit JSON mapping of campaign labels to completed case IDs; original incomplete campaigns remain unchanged.')
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    campaigns = [(key, getattr(args, key).resolve()) for key in ('cyclic', 'signed', 'translations')
                 if getattr(args, key)]
    campaigns += [('abelian' if i == 0 else 'abelian_' + str(i+1), path.resolve())
                  for i, path in enumerate(args.abelian)]
    if not campaigns:
        parser.error('At least one explicit completed campaign is required.')
    result = collect(campaigns, args.output.resolve(), args.ledger, args.extends,
                     read(args.completed_selections) if args.completed_selections else None)
    print("PASS:", result["completeResultCount"], "accepted 4+1D backgrounds")


if __name__ == "__main__":
    main()
