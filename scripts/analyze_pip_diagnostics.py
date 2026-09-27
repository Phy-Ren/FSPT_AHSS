#!/usr/bin/env python3
"""Describe saved p+ip differentials and marked square relations, without GAP.

This is an evidence inventory, not a new evaluation of missing obstructions.
One invocation accepts only one convention/source version. No reference answers
are read. Archive hashes are checked when archive.json is present.
"""
import argparse
from collections import Counter, defaultdict
import hashlib
import json
import math
from pathlib import Path


ZERO_TARGET = "d2-and-d3-primitives-zero-two-primary-d4-target"
EXPLICIT = "explicit-full-O5-in-E4-quotient"
LAYER_NAMES = {0: "bosonic", 1: "complex_fermion", 2: "majorana"}


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def nonzero(value):
    return any(x != 0 for x in value)


def candidate(number, kind, index, raw):
    prefix = "/pip/torsion" if kind == "torsion" else "/pip/free_lattice/parityCandidates"
    status, page = raw.get("status"), raw.get("page")
    evidence = f"sg{number}.json#{prefix}/{index}"
    d3 = {"evaluation": "not_reached"}
    d4 = {"evaluation": "not_reached"}
    if status == "killed" and page == 2:
        d2 = "killed"
    elif page in (3, 4):
        d2 = "solved"
        if status == "killed" and page == 3:
            d3 = dict(evaluation="killed_after_lower_choice_solve",
                      initial_coordinates=raw.get("obstruction"))
        elif page == 4:
            d3 = dict(evaluation="solved", initial_coordinates=raw.get("d3_initial_coordinates"),
                      initial_coordinates_saved="d3_initial_coordinates" in raw,
                      majorana_choice_adjustment=raw.get("majorana_adjustment"))
            if "d3_initial_coordinates" in raw:
                d3["initial_nonzero"] = nonzero(raw["d3_initial_coordinates"])
            if raw.get("certificate") == ZERO_TARGET:
                orders = raw["d4_target"]
                if any(o == 0 or o % 2 == 0 for o in orders):
                    raise ValueError(f"Invalid no-two-primary certificate: {evidence}")
                d4 = dict(evaluation="class_evaluation_skipped_no_two_primary_target",
                          quotient_orders=orders, whole_target_zero=not orders,
                          raw_H5_coordinates_saved=False)
            elif raw.get("certificate") == EXPLICIT:
                co = raw["d4_raw_coordinates"]
                d4 = dict(evaluation="explicit_class_survives_in_quotient",
                          quotient_orders=raw["d4_target"], raw_H5_coordinates=co,
                          raw_H5_coordinates_saved=True, raw_H5_nonzero=nonzero(co),
                          projected_obstruction="zero_by_recorded_survival_certificate")
            elif status == "killed" and page == 4:
                d4 = dict(evaluation="killed_in_quotient", quotient_orders=raw.get("d4_target"),
                          projected_obstruction=raw.get("obstruction"),
                          raw_H5_coordinates_saved="d4_raw_coordinates" in raw)
            else:
                d4 = dict(evaluation="unrecognized_saved_certificate")
    else:
        d2 = "not_determined_from_saved_record"
    return dict(space_group=number, kind=kind, candidate_index=index,
                evidence=evidence, saved_record=raw, d2=d2, d3=d3, d4=d4)


def square_relation(d):
    s = d["stacking"]
    if "pipSquareCertificate" in s and "pipExtensionCertificate" in s:
        cert, family = s["pipSquareCertificate"], s["pipExtensionCertificate"]
        return dict(status="leading_square_known_lower_carries_unresolved",
                    evidence=f"sg{d['space_group']}.json#/stacking/pipSquareCertificate",
                    majorana_cohomology_class=cert.get("majoranaCohomologyClass"),
                    majorana_coordinates=cert.get("majoranaCoordinates"),
                    nonzero_layers=["majorana"] if nonzero(cert.get("majoranaCoordinates", [])) else [],
                    unknown_layers=cert.get("unknownCarries", []),
                    full_upper_phase_witness=cert.get("fullUpperPhaseWitness", False),
                    saved_certificate=cert, extension_family=family,
                    interpretation="Only the leading square is fixed. The CF and bosonic carries are not set to zero, even if every allowed carry gives the same abstract group.")
    if "pipRelation" not in s:
        return dict(status="no_saved_torsion_square", free_rank=d["pip"]["free_rank"],
                    interpretation="Free integer lifts have no finite quotient-order relation; absence is not a zero-twister result.")
    rel, generators = s["pipRelation"], s["lower"]["generators"]
    row = s["fullPresentation"][-1]
    if len(row) != len(generators)+1 or row[-1] != s["pipGenerator"]["quotientOrder"]:
        raise ValueError("Invalid final p+ip presentation row")
    coordinates = [-x for x in row[:-1]]
    saved = rel["lowerCoordinates"]
    if len(saved) > len(coordinates) or coordinates != saved+[0]*(len(coordinates)-len(saved)):
        raise ValueError("Marked square coordinates disagree with full presentation")
    pieces = {name: [] for name in LAYER_NAMES.values()}
    basis = []
    for g, co in zip(generators, coordinates):
        name = LAYER_NAMES[g["layer"]]
        basis.append(dict(name=g["name"], layer=name, quotient_order=g["quotientOrder"]))
        pieces[name].append(dict(generator=g["name"], coefficient=co))
    phase = {}
    for field in ("squareCF3", "squarePhase4", "referenceDiagonalPhase4",
                  "inputCoordinateShift4", "outputCoordinateShift4", "integerGaugePhase4"):
        if field not in rel:
            phase[field] = dict(saved=False)
            continue
        vector = rel[field]
        nz = sum(bool(v[0] % v[1]) if isinstance(v, list) else bool(v) for v in vector)
        phase[field] = dict(saved=True, native_dimension=len(vector), nonzero_native_entries=nz,
                            vector_sha256=sha(json.dumps(vector, separators=(",", ":")).encode()))
    g = s["pipGenerator"]
    return dict(status="saved_marked_square", evidence=f"sg{d['space_group']}.json#/stacking",
                power=row[-1], presentation_row=row, lower_basis=basis,
                lower_coordinates=coordinates, layer_components=pieces,
                nonzero_layers=[name for name, terms in pieces.items() if any(x["coefficient"] for x in terms)],
                generator_construction=g.get("construction"),
                mc_lift_adjustment=g.get("mcIndeterminacyAdjustment"),
                cf_lift_adjustment=g.get("cfIndeterminacyAdjustment"),
                full_upper_phase_witness=s.get("fullUpperPhaseWitness"),
                comparison_support_rechecked=rel.get("checkedComparisonSupport"),
                coefficient_vectors=phase,
                bare_pairwise_twister_fields_saved=False,
                interpretation="Coordinates of the final square after integer-layer gauge removal, in the saved marked lower basis. They are not separately evaluated pairwise twisting functions and are not independent of lift choices.")


def h0_incoming(d):
    """Read filtered image orders from the saved exact cyclic quotient.

    These are orders of successive incoming images, not fresh evaluations of
    the raw Sq1/Pontryagin representatives before lower gauge corrections.
    """
    saved = d["stacking"].get("h0IncomingQuotient", {}).get("backgroundQuotient")
    bg = d.get("crystalline_background", {})
    if not saved:
        if bg and any(bg.get("signTable", [])):
            reason = "nonunitary sign: H0(Z_s)=0"
        elif bg.get("gaugeReducedToZero"):
            reason = "physical background explicitly trivialized on the full affine group"
        elif d["convention"] == "physical-spin-half-det-sign-omega0":
            reason = "zero physical extension convention"
        else:
            reason = "no incoming quotient certificate saved"
        return dict(status="no_nonzero_incoming_quotient_saved", reason=reason)
    pre, post = d["preH0IncomingGraded"], saved["graded"]
    if any(d[k] != post[k] for k in LAYER_NAMES.values()):
        raise ValueError("Saved classification omits its H0 incoming quotient")
    stages, multiple = {}, 1
    for page, layer in ((2, "majorana"), (3, "complex_fermion"), (4, "bosonic")):
        if pre[layer].count(0) != post[layer].count(0):
            raise ValueError("Finite H0 boundary changed the free rank")
        a = math.prod(x for x in pre[layer] if x)
        b = math.prod(x for x in post[layer] if x)
        if a % b:
            raise ValueError("H0 incoming graded order ratio is nonintegral")
        image_order = a // b
        stages[f"d{page}"] = dict(layer=layer, source_integer_multiple=multiple,
            incoming_image_order=image_order, nonzero_incoming_image=image_order > 1,
            before_orders=pre[layer], after_orders=post[layer],
            raw_source_coordinates_saved=(page == 2 and "basisChange" in saved),
            interpretation="Incoming image inferred from the certified complete cyclic quotient and its integral filtration intersections.")
        multiple *= image_order
    if multiple != saved["incomingOrder"]:
        raise ValueError("H0 filtered incoming image orders disagree with the cyclic order")
    raw_mc = saved.get("basisChange", {}).get("incomingMCCohomologyCoordinates")
    stages["d2"]["raw_H2_coordinates"] = raw_mc
    return dict(status="actual_cyclic_quotient_saved",
        evidence=f"sg{d['space_group']}.json#/stacking/h0IncomingQuotient/backgroundQuotient",
        incoming_order=saved["incomingOrder"], incoming_coordinates=saved["incomingCoordinates"],
        differential_images=stages, source_kernel_after_d4=multiple,
        raw_d3_d4_coordinates_reconstructed=False,
        coordinate_method=saved.get("coordinateMethod"),
        lower_before=saved["preQuotientLower"]["invariants"],
        lower_after=d["stacking"]["h0IncomingQuotient"]["lower"]["invariants"])


def upper_family(d):
    s = d["stacking"]
    family = s.get("pipExtensionCertificate")
    if family is None:
        return None
    options = family["invariantOptions"]
    if (family["status"] not in ("computed", "ambiguous") or not options
            or (family["status"] == "computed" and len(options) != 1)
            or (family["status"] == "ambiguous" and len(options) < 2)):
        raise ValueError("Invalid saved upper extension family")
    free_rank = s.get("freePipRank", d["pip"]["free_rank"])
    full_options = [[0] * free_rank + x for x in options]
    if s["status"] == "computed" and s["invariants"] != full_options[0]:
        raise ValueError("Full abstract stacking group differs from its Ext certificate")
    return dict(status=family["status"], complete_affine_family=True,
        full_invariant_options=full_options, possible_heights=family["possibleHeights"],
        unknown_carries=s.get("pipSquareCertificate", {}).get("unknownCarries", []),
        full_upper_phase_witness=s.get("fullUpperPhaseWitness", False),
        evidence=f"sg{d['space_group']}.json#/stacking/pipExtensionCertificate",
        saved_certificate=family)


def analyze(root, allow_partial=False):
    archive_path = root/"archive.json"
    archive_raw = archive_path.read_bytes() if archive_path.exists() else None
    archive = json.loads(archive_raw) if archive_raw else None
    records, candidates, sources, conventions, formulas = [], [], set(), set(), set()
    missing = []
    for number in range(1, 231):
        path = root/f"sg{number}.json"
        if not path.exists():
            missing.append(number)
            continue
        raw = path.read_bytes()
        if archive and sha(raw) != archive["files"][path.name]["sha256"]:
            raise ValueError(f"Archive hash mismatch: {path.name}")
        d = json.loads(raw)
        known_ambiguous = (d.get("classification_status") == "computed"
            and d["status"] == "unresolved" and d["stacking"]["status"] == "unresolved"
            and d["stacking"].get("pipExtensionCertificate", {}).get("status") == "ambiguous")
        if d["space_group"] != number or (not known_ambiguous and
                (d["status"] != "computed" or d["stacking"]["status"] != "computed")):
            raise ValueError(f"Incomplete or wrong result: {path.name}")
        sources.add(d["source_id"]); conventions.add(d["convention"]); formulas.add(d.get("formula_convention"))
        own = [candidate(number, "torsion", i, c) for i, c in enumerate(d["pip"].get("torsion", []))]
        free = d["pip"].get("free_lattice")
        own += [candidate(number, "free", i, c) for i, c in enumerate((free or {}).get("parityCandidates", []))]
        candidates.extend(own)
        lattice = None
        if free:
            lattice = {k: free.get(k) for k in ("rank", "h1BasisOrders", "freeIndices", "latticeBasis",
                       "latticeIndex", "survivingParityBasis", "certificate", "fullFreePhaseWitness",
                       "certifiedIntegerPeriod")}
            modulus = free.get("certifiedIntegerPeriod", 2)
            if modulus not in (2, 16):
                raise ValueError("Unknown certified integer search period")
            lattice["candidate_projection_modulus"] = modulus
            lattice["generators"] = [{k: g[k] for k in ("name", "h1Coordinates", "construction",
                                     "mcIndeterminacyAdjustment", "cfIndeterminacyAdjustment") if k in g}
                                    for g in free["generators"]]
            lattice["evidence"] = f"sg{number}.json#/pip/free_lattice"
            alternatives = defaultdict(list)
            for c in own:
                if c["kind"] == "free":
                    h = c["saved_record"]["h1Coordinates"]
                    projection = tuple(h[i-1] % modulus for i in free["freeIndices"])
                    alternatives[projection].append(c)
            lattice["candidate_changes_preserving_free_residue"] = []
            for projection, trials in alternatives.items():
                killed = [c for c in trials if c["saved_record"]["status"] == "killed"]
                survived = [c for c in trials if c["saved_record"]["status"] == "survives"]
                if killed and survived:
                    lattice["candidate_changes_preserving_free_residue"].append(dict(
                        free_residue=list(projection), modulus=modulus, killed=[c["evidence"] for c in killed],
                        survives=[c["evidence"] for c in survived]))
            # Preserve the old parity interpretation only on its actual domain.
            lattice["candidate_changes_preserving_free_parity"] = [
                dict(free_parity=x["free_residue"], killed=x["killed"], survives=x["survives"])
                for x in lattice["candidate_changes_preserving_free_residue"] if modulus == 2]
            lattice["tested_free_residues"] = [list(x) for x in sorted(alternatives)]
            lattice["universal_period_fallback_used"] = any(
                g.get("construction") == "strict-universal-16H-zero-lower-tower-from-twice-shift-eight"
                for g in free["generators"])
        records.append(dict(space_group=number, result_sha256=sha(raw), pip_orders=d["pip"]["orders"],
                            torsion_candidate_count=len(d["pip"].get("torsion", [])), free_lattice=lattice,
                            candidate_evidence=[c["evidence"] for c in own], square=square_relation(d),
                            h0_incoming=h0_incoming(d), upper_extension_family=upper_family(d),
                            stacking_status=d["stacking"]["status"]))
    if missing and not allow_partial:
        raise ValueError(f"Incomplete 230-group input; missing {missing}")
    if len(sources) != 1 or len(conventions) != 1 or len(formulas) != 1:
        raise ValueError("Expected one nonempty convention/source/formula version per invocation")
    cohorts = {}
    for kind in ("torsion", "free"):
        cs = [c for c in candidates if c["kind"] == kind]
        predicates = {
            "killed_d2": lambda c: c["d2"] == "killed",
            "killed_d3": lambda c: c["d3"]["evaluation"] == "killed_after_lower_choice_solve",
            "killed_d4": lambda c: c["d4"]["evaluation"] == "killed_in_quotient",
            "survives": lambda c: c["saved_record"]["status"] == "survives",
            "d3_nonzero_initial_then_solved": lambda c: c["d3"].get("initial_nonzero") is True and c["d3"]["evaluation"] == "solved",
            "d3_solved_initial_missing": lambda c: c["d3"]["evaluation"] == "solved" and not c["d3"].get("initial_coordinates_saved", False),
            "d4_skipped_whole_target_zero": lambda c: c["d4"].get("whole_target_zero") is True,
            "d4_skipped_nonzero_odd_target": lambda c: c["d4"].get("whole_target_zero") is False,
            "d4_explicit_raw_zero_survives": lambda c: c["d4"].get("raw_H5_nonzero") is False,
            "d4_explicit_raw_nonzero_survives": lambda c: c["d4"].get("raw_H5_nonzero") is True,
        }
        cohorts[kind] = {name: dict(candidate_count=len(selected),
                                  space_groups=sorted({c["space_group"] for c in selected}),
                                  evidence=[c["evidence"] for c in selected])
                        for name, pred in predicates.items() for selected in [[c for c in cs if pred(c)]]}
    cohorts["square_nonzero_components"] = {name: [r["space_group"] for r in records if name in r["square"].get("nonzero_layers", [])]
                                           for name in LAYER_NAMES.values()}
    cohorts["free_lattice_index_gt_one"] = [r["space_group"] for r in records if r["free_lattice"] and r["free_lattice"]["latticeIndex"] > 1]
    cohorts["free_candidate_changed_by_torsion"] = [r["space_group"] for r in records if r["free_lattice"] and r["free_lattice"]["candidate_changes_preserving_free_residue"]]
    cohorts["h0_nonzero_incoming"] = {f"d{p}": [r["space_group"] for r in records
        if r["h0_incoming"].get("differential_images", {}).get(f"d{p}", {}).get("nonzero_incoming_image")]
        for p in (2, 3, 4)}
    cohorts["upper_extension_ambiguous_isotype"] = [r["space_group"] for r in records
        if r["upper_extension_family"] and r["upper_extension_family"]["status"] == "ambiguous"]
    cohorts["upper_extension_unique_isotype_without_full_phase"] = [r["space_group"] for r in records
        if r["upper_extension_family"] and r["upper_extension_family"]["status"] == "computed"
        and not r["upper_extension_family"]["full_upper_phase_witness"]]
    return dict(schema=2, input_directory=str(root.resolve()), source_id=sources.pop(),
                convention=conventions.pop(), formula_convention=formulas.pop(),
                archive_sha256=sha(archive_raw) if archive_raw else None,
                full_230=not missing, missing_space_groups=missing, cohorts=cohorts,
                records=records, candidates=candidates,
                scope={"new_cochain_evaluations": False, "reference_answers_read": False,
                       "missing_initial_data_reconstructed": False,
                       "square_components": "Marked final relation coefficients after integer gauge; not bare pairwise twisters.",
                       "phase_vector_nonzero": "Native cochain entries, not a nontrivial cohomology or quotient class.",
                       "free_survival": "A surviving free parity projection may use a torsion-shifted H1 candidate."})


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("run", type=Path)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--allow-partial", action="store_true")
    args = parser.parse_args()
    result = analyze(args.run, args.allow_partial)
    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(json.dumps(result, indent=2, sort_keys=True)+"\n")
    print(json.dumps({"groups": len(result["records"]), "candidates": len(result["candidates"]),
                      "full_230": result["full_230"], "output": str(args.output)}))


if __name__ == "__main__":
    main()
