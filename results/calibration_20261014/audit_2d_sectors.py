#!/usr/bin/env python3
"""Audit the exact n0 kernel using frozen relative and full 2D presentations.

This reads saved evidence only; it never runs classification or edits that evidence.
"""
import csv
from collections import Counter
import hashlib
import json
from math import gcd
from pathlib import Path
import tarfile

from sympy import Matrix, ZZ
from sympy.matrices.normalforms import hermite_normal_form, smith_normal_form

ROOT = Path(__file__).resolve().parents[2]
HERE = Path(__file__).resolve().parent
FULL = ROOT / "results/two_dimensional_20261013/results.json"
ARCHIVE = ROOT / "results/evidence/two_dimensional_runs.tar.gz"


def sha(data):
    return hashlib.sha256(data).hexdigest()


def row_lattice(rows, width):
    return hermite_normal_form(Matrix(rows).T) if rows else Matrix.zeros(width, 0)


def group_from_presentation(rows, width):
    if not rows:
        return {"torsion": [], "freeRank": width}
    diagonal = smith_normal_form(Matrix(rows), domain=ZZ)
    values = [abs(int(diagonal[i, i])) for i in range(min(diagonal.shape))]
    return {"torsion": [n for n in values if n > 1], "freeRank": width - sum(n != 0 for n in values)}


def signature(record):
    return {key: record[key] for key in ("torsion", "freeRank")}


def display(record):
    factors = []
    if record["freeRank"]:
        factors.append("Z" if record["freeRank"] == 1 else f"Z^{record['freeRank']}")
    for order, multiplicity in sorted(Counter(record["torsion"]).items()):
        factors.append(f"Z{order}" + (f"^{multiplicity}" if multiplicity > 1 else ""))
    return " x ".join(factors) or "0"


def audit():
    archive_rows = {}
    with tarfile.open(ARCHIVE) as archive:
        for member in archive.getmembers():
            if not member.name.endswith("/result.json"):
                continue
            data = archive.extractfile(member).read()
            row = json.loads(data)
            key = (row["input"]["id"], row["classification"]["uniformIQHIncluded"])
            assert key not in archive_rows, key
            archive_rows[key] = (row, member.name, sha(data))
    full_rows = json.loads(FULL.read_text())
    assert len(full_rows) == 54 and len(archive_rows) == 108
    output = []
    for row in full_rows:
        identity = row["input"]["id"]
        full = row["classification"]
        relative = full["relativeUniformIQH0"]
        old, old_member, old_hash = archive_rows[(identity, False)]
        archived, full_member, full_hash = archive_rows[(identity, True)]
        old = old["classification"]
        assert full == archived["classification"], identity
        assert relative["generators"] == old["generators"], identity
        width = relative["presentationGeneratorCount"]
        ci = [(i, g) for i, g in enumerate(full["generators"]) if g["kind"] == "CI"]
        assert len(ci) <= 1 and full["presentationGeneratorCount"] == width + len(ci)
        projection = [0] * full["presentationGeneratorCount"]
        image_step = 0
        for i, generator in ci:
            assert i == width and len(generator["nativeSheet"]) == 1
            coefficient = int(generator["nativeSheet"][0])
            assert coefficient != 0
            projection[i] = coefficient
            image_step = gcd(image_step, abs(coefficient))
        assert all(sum(x * y for x, y in zip(relation, projection)) == 0 for relation in full["presentation"])
        assert all(relation[i] == 0 for relation in full["presentation"] for i, _ in ci)
        kernel_lattice = row_lattice([r[:width] for r in full["presentation"]], width)
        assert kernel_lattice == row_lattice(relative["presentation"], width)
        assert kernel_lattice == row_lattice(old["presentation"], width)
        assert group_from_presentation(full["presentation"], len(projection)) == signature(full)
        assert group_from_presentation(relative["presentation"], width) == signature(relative) == signature(old)
        assert full["torsion"] == relative["torsion"] and full["freeRank"] == relative["freeRank"] + len(ci)
        witnesses = [w for w in full["witnesses"] if w["kind"] == "uniform-IQH-lift"]
        assert len(witnesses) == len(ci)
        if ci:
            assert image_step == witnesses[0]["sheetMultiplicity"] == 1
            assert not any(row["input"]["s"])
        else:
            assert any(row["input"]["s"])
        for key in ("finalPhaseOrders", "finalPhaseFreeRank", "finalChargeOrders", "finalChargeFreeRank"):
            assert relative[key] == old[key], (identity, key)
        filling = relative.get("wallpaperFilling")
        output.append({
            "id": identity, "family": row["input"]["family"], "name": row["input"]["name"],
            "index": row["input"]["index"], "spin": row["input"]["spin"],
            "relative_n0_zero": signature(relative), "full_supplied_model": signature(full),
            "n0_projection_on_saved_generators": projection,
            "n0_image_step": image_step, "n0_image": "Z" if image_step == 1 else "0",
            "relative_generator_cochains_identical_to_independent_run": True,
            "relative_relation_lattices_identical_by_HNF": True,
            "relative_equals_full_n0_kernel": True,
            "independent_SNF_verified": True,
            "full_abstract_splitting": "noncanonical A0 plus Z" if ci else "A0; nonzero n0 forbidden",
            "fixed_nonzero_n0_sector": "A0 torsor for every nonzero integer; not a stacking group" if ci else "empty",
            "physical_normalization": "I: explicit full-IQH model; universal physical product comparison open" if ci else "R: relative construction; no nonzero-IQH sector",
            "neutral_E8": "omitted, not declared zero; 2D relative physical SPT also fixes e0=0",
            "primitive_cell_charge_step": filling["fillingStep"] if filling else None,
            "chosen_CI_lift_charge_fillings": full.get("wallpaperFilling", {}).get("ciGeneratorFillings", []),
            "relative_archive_member": old_member, "relative_archive_result_sha256": old_hash,
            "full_archive_member": full_member, "full_archive_result_sha256": full_hash,
        })
    summary = {
        "scope": "Algebraic sector audit of the supplied model; no full physical classification claim",
        "relative_runs": 54, "full_runs": 54,
        "exact_kernel_checks_passed": len(output),
        "n0_image_Z_cases": sum(r["n0_image_step"] == 1 for r in output),
        "n0_image_zero_cases": sum(r["n0_image_step"] == 0 for r in output),
        "proof": "One or zero CI columns, nonzero scalar n0 on each CI generator, and zero CI coefficients in every relation; delete that free column to obtain precisely ker(n0). Its generator cochains and integer relation lattice equal the independent n0=0 run.",
        "provenance": {
            "archive_sha256": sha(ARCHIVE.read_bytes()), "full_results_sha256": sha(FULL.read_bytes()),
            "audit_script_sha256": sha(Path(__file__).read_bytes()),
        },
        "rows": output,
    }
    (HERE / "two_dimensional_sectors.json").write_text(json.dumps(summary, indent=2) + "\n")
    columns = ["id", "name", "spin", "relative_n0_zero", "full_supplied_model", "n0_image", "physical_normalization", "primitive_cell_charge_step"]
    with (HERE / "two_dimensional_sectors.csv").open("w") as stream:
        writer = csv.DictWriter(stream, fieldnames=columns)
        writer.writeheader()
        for item in output:
            flat = {key: item[key] for key in columns}
            flat["relative_n0_zero"] = display(item["relative_n0_zero"])
            flat["full_supplied_model"] = display(item["full_supplied_model"])
            writer.writerow(flat)
    lines = [
        "# Two-dimensional sectors: supplied-model audit, 2026-10-14", "",
        "All 54 independently computed zero-IQH groups equal the exact n0 kernels of their full runs: generator cochains are identical, relation lattices agree by integer HNF, and independent SNF reproduces every listed group. The 20 nonzero-IQH-capable cases have actual image n0=Z; the other 34 have image zero.", "",
        "R means the relative charge construction. I means the explicit full-IQH model whose universal physical product normalization remains open in the supplied note. All rows omit the independent E8 coordinate. A fixed allowed nonzero n0 is a torsor for A0, not the group in either group column. Zm^r denotes r copies of Zm.", "",
        "| Family / group | A0 spinless | A0 spin-half | Full model spinless | Full model spin-half | n0 image | Status | Cell charge step (spinless / half) |",
        "| --- | --- | --- | --- | --- | --- | --- | --- |",
    ]
    grouped = {}
    for item in output:
        grouped.setdefault((item["family"], item["index"]), {})[item["spin"]] = item
    for key in sorted(grouped):
        left, right = (grouped[key][spin] for spin in ("spinless", "spin_half"))
        assert left["n0_image"] == right["n0_image"]
        cell = "—" if left["primitive_cell_charge_step"] is None else f"{left['primitive_cell_charge_step']} / {right['primitive_cell_charge_step']}"
        lines.append("| " + " | ".join([f"{left['family']} / {left['name']}", display(left["relative_n0_zero"]), display(right["relative_n0_zero"]), display(left["full_supplied_model"]), display(right["full_supplied_model"]), left["n0_image"], "I" if left["n0_image_step"] else "R", cell]) + " |")
    lines.extend(["", "Cell charge steps use completed charge roots and the actual primitive translation lattice. All ten wallpaper CI lifts chosen by the solver have zero additional cell charge, but a different IQH lift may be shifted by an A0 state. A printed literature free factor Z or 2Z is not a primitive-cell normalization without a separate coordinate map.", "", "Reproduce with `python results/calibration_20261014/audit_2d_sectors.py`. This reads the immutable evidence archive and does not change the original runs or reports.", ""])
    (HERE / "two_dimensional_sectors.md").write_text("\n".join(lines))
    print(json.dumps({key: summary[key] for key in ("exact_kernel_checks_passed", "n0_image_Z_cases", "n0_image_zero_cases")}))


if __name__ == "__main__":
    audit()
