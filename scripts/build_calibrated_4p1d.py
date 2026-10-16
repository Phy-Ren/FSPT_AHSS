"""Render accepted 4+1D computations with separate intrinsic response sectors."""
from copy import deepcopy
import hashlib
from pathlib import Path


def load_collection(catalogue, path, ancestors=()):
    absolute_path = (Path(__file__).resolve().parents[1] / path).resolve()
    if absolute_path in ancestors:
        raise ValueError('Cyclic accepted-collection inheritance.')
    data = catalogue.load(path)
    if data.get("accepted") is not True or data.get("schemaVersion") != 1:
        raise ValueError("The 4+1D collection must pass explicit acceptance.")
    base = Path(path).parent
    for relative, expected in data["filesSHA256"].items():
        target = base / relative
        absolute = Path(__file__).resolve().parents[1] / target
        actual = hashlib.sha256(absolute.read_bytes()).hexdigest()
        catalogue.inputs[catalogue.path_name(absolute)] = actual
        if actual != expected:
            raise ValueError("Accepted 4+1D evidence changed: " + str(target))
    inherited_records, inherited_sources, lineage = {}, {}, []
    for parent in data.get('extends', []):
        parent_path = Path(__file__).resolve().parents[1] / parent['path']
        if hashlib.sha256(parent_path.read_bytes()).hexdigest() != parent['sha256']:
            raise ValueError('Inherited accepted collection changed.')
        inherited = load_collection(catalogue, parent['path'], ancestors + (absolute_path,))
        lineage.extend(inherited['acceptedLineage'])
        for record in inherited['records']:
            key = record['input']['id']
            if key in inherited_records:
                raise ValueError('Duplicate inherited background.')
            inherited_records[key] = record
        for key, source in inherited['sources'].items():
            if key in inherited_sources and inherited_sources[key] != source:
                raise ValueError('Conflicting inherited source metadata: ' + key)
            inherited_sources[key] = source
    for record in data['records']:
        key = record['input']['id']
        if key in inherited_records:
            raise ValueError('A new batch must not silently replace an accepted background.')
    for key, source in data['sources'].items():
        if key in inherited_sources and inherited_sources[key] != source:
            raise ValueError('Conflicting current source metadata: ' + key)
        inherited_sources[key] = source
    lineage.append({'path': str(path), 'newInputCount': len(data['records'])})
    records = list(inherited_records.values()) + data["records"]
    data['records'], data['sources'] = records, inherited_sources
    if not records or len({r["input"]["id"] for r in records}) != len(records):
        raise ValueError("Empty or duplicate 4+1D records.")
    for record in records:
        if record["input"]["dimension"] != 4 or record["run"]["status"] != "complete":
            raise ValueError("An accepted 4+1D record is incomplete or mislabelled.")
    data["acceptedPath"] = str(path)
    data['acceptedLineage'] = lineage
    return data


def build_tables(catalogue, data):
    zero = {"torsion": [], "freeRank": 0}
    configurations = [
        ("internal_cyclic", "intrinsic_zero", "4p1d/internal_cyclic/intrinsic_zero",
         "4+1D internal cyclic groups: zero intrinsic response"),
        ("internal_cyclic", "intrinsic_all", "4p1d/internal_cyclic/intrinsic_all",
         "4+1D internal cyclic groups: all intrinsic responses"),
        ("charge_conjugation", "intrinsic_zero", "4p1d/charge_conjugation",
         "4+1D unitary charge conjugation"),
        ("time_reversal", "intrinsic_zero", "4p1d/time_reversal_intrinsic_zero",
         "4+1D time reversal: zero intrinsic response"),
        ("internal_abelian", "intrinsic_zero", "4p1d/internal_abelian/intrinsic_zero",
         "4+1D internal abelian products: zero intrinsic response"),
        ("internal_abelian", "intrinsic_all", "4p1d/internal_abelian/intrinsic_all",
         "4+1D internal abelian products: all intrinsic responses"),
        ("translations", "intrinsic_zero", "4p1d/translations/intrinsic_zero",
         "4+1D translations: zero intrinsic response"),
        ("translations", "intrinsic_all", "4p1d/translations/intrinsic_all",
         "4+1D translations: all intrinsic responses"),
    ]
    for family, sector, destination, title in configurations:
        selected = [r for r in data["records"] if r["input"]["family"] == family]
        if not selected:
            continue
        selected.sort(key=lambda r: (r["input"].get("translationRank", r["input"].get("order", 0)), r["input"]["id"]))
        full = sector == "intrinsic_all"
        spin_scope = 'not_applicable_translations' if family == 'translations' else 'not_applicable_internal'
        reference_keys = sorted({key for record in selected for key in record["references"]})
        missing_reference = any(not r['references'] for r in selected)
        columns = [{"key": key, "label": label} for key, label in (
            ("e", "e2 (E8)"), ("n", "n2 (CI)"), ("charge", "n4 (charge)"),
            ("phase", "nu5 (phase)"), ("intrinsic", "(n0I,n0J)"),
            ("stacking", "Final stacking"))]
        columns += [{"key": key, "label": data["sources"][key]["columnLabel"]}
                    for key in reference_keys]
        if missing_reference:
            columns += [{'key': 'independent_reference', 'label': 'Independent interacting reference'}]
        rows = []
        for record in selected:
            inputs, classification = record["input"], record["classification"]
            layers = deepcopy(classification["finalFiltration"])
            group = {"torsion": list(classification["torsion"]),
                     "freeRank": classification["freeRank"]}
            intrinsic = deepcopy(zero)
            if full:
                section = record["uniformResponse"]
                if section.get("canonicalSectionVerified") is not True:
                    raise ValueError("A full result requires its uniform-section certificate.")
                intrinsic["freeRank"] = section["freeRank"]
                group["freeRank"] += section["freeRank"]
            cells = {key: catalogue.cell(value) for key, value in layers.items()}
            cells.update(intrinsic=catalogue.cell(intrinsic), stacking=catalogue.cell(group))
            for key in reference_keys:
                if key not in record["references"]:
                    cells[key] = {"availability": "not_applicable", "comparison_status": "not_compared"}
                    continue
                reference = deepcopy(record["references"][key])
                if full:
                    if not reference.pop("fullUniformSectionApplicable", False):
                        cells[key] = {"availability": "not_applicable", "comparison_status": "not_compared"}
                        continue
                    reference["group"]["freeRank"] += intrinsic["freeRank"]
                cells[key] = catalogue.reference({"availability": "available", "source": key,
                                                  **reference}, group)
            if missing_reference:
                cells['independent_reference'] = {'availability': 'not_applicable' if record['references'] else 'unverified',
                                                  'comparison_status': 'not_compared'}
            row = {"id": inputs["id"], "name": inputs["name"], "hermann_mauguin": None,
                   "display_name": inputs["name"], "family": family,
                   "physical_spin": spin_scope, "spatial_dimension": 4,
                   "spacetime_dimension": 5, "n0_scope": sector, "e0_scope": "not_applicable",
                   "e8_scope": "four_data_included", "cells": cells,
                   "background": deepcopy(inputs["background"]),
                   "provenance": deepcopy(record["provenance"])}
            rows.append(row)
            catalogue.index.append({**{k: deepcopy(v) for k, v in row.items() if k != "cells"},
                                    "table": destination + ".json", "stacking": group,
                                    "final_filtration": layers,
                                    "intrinsic_response": deepcopy(intrinsic)})
        scope = ("Each row is one exact internal electronic symmetry; crystalline spin labels do not apply. "
                 "E8, CI, charge and the common phase are computed with complete products and gauges. ")
        if family == 'translations':
            scope = ("Each row specifies the free translation rank in four spatial dimensions. "
                     "Only rank four is a full space-group translation lattice; lower ranks impose fewer translations. "
                     "There are no rotations and hence no distinct spin lifts. "
                     "The complete finite simplicial torus retains E8, CI, charge, gauges and the actual stacking correction. ")
        if family == 'internal_abelian':
            scope += ("Rows retain the specified product presentation. Coprime cyclic products can be isomorphic "
                      "to cyclic inputs in the separate table and serve as independent calculation controls. ")
        if full:
            scope += ("The two symmetry-independent intrinsic roots I,J supply an explicit canonical "
                      "Z^2 section for this direct-product symmetry. The general opened intrinsic solver is not inferred. ")
        else:
            scope += "The intrinsic response pair (n0I,n0J) is fixed to zero. "
        if family == "charge_conjugation":
            scope += "The invariant intrinsic row vanishes for these backgrounds, so this is the full group. "
        if family == "time_reversal":
            scope += ("The cited zero-intrinsic targets follow from the full physical groups and their "
                      "uniform response maps. Full AI/AII intrinsic classifications are not computed in this table. ")
        scope += ("Reference answers are applied after calculation. Physical derivations and their exact "
                  "scope are recorded in the cited sources and accepted evidence.")
        catalogue.render(Path(destination), {"title": title, "scope": scope, "family": family,
                         "spatial_dimension": 4, "spacetime_dimension": 5,
                         "physical_spin": spin_scope, "n0_scope": sector,
                         "e0_scope": "not_applicable", "e8_scope": "four_data_included",
                         "columns": columns,
                         "sources": {k: deepcopy(data["sources"][k]) for k in reference_keys},
                         "rows": rows})
