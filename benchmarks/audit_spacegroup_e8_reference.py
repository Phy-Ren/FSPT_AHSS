#!/usr/bin/env python3
"""Audit neutral signed H1 for all 230 affine space-group presentations.

Only H1(G,Z_det) is compared with Song-Xiong-Huang's neutral E8 column.
This is not a full interacting electronic-classification calculation.
"""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
from pathlib import Path
import platform
import sys

import sympy
from sympy import Matrix, Rational, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from insulator.e8_h1 import relation_row, twisted_h1


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def recorded_path(path):
    try:
        return str(path.resolve().relative_to(ROOT))
    except ValueError:
        return str(path.resolve())


def affine(matrix):
    result = Matrix([[Rational(str(value)) for value in row] for row in matrix])
    if result.shape != (4, 4) or list(result[:, 3]) != [0, 0, 0, 1]:
        raise ValueError("Expected a 4x4 row-action affine matrix.")
    return result


def word_matrix(word, matrices, inverses):
    result = sympy.eye(4)
    for letter in word:
        if not isinstance(letter, int) or not 1 <= abs(letter) <= len(matrices):
            raise ValueError("Word letter outside the presentation generator range.")
        result = result * (matrices[letter - 1] if letter > 0 else inverses[-letter - 1])
    return result


def invariants(matrix, generator_count):
    if not matrix or not matrix[0]:
        return {"torsion": [], "freeRank": generator_count}
    smith = smith_normal_form(Matrix(matrix), domain=ZZ)
    diagonal = [abs(int(smith[i, i])) for i in range(min(smith.shape)) if smith[i, i]]
    return {"torsion": [value for value in diagonal if value > 1],
            "freeRank": generator_count - len(diagonal)}


def calculate(record):
    if record.get("presentationIsomorphismVerified") is not True:
        raise ValueError("The geometry export does not certify its presentation isomorphism.")
    matrices = [affine(m) for m in record["presentationGeneratorMatrices"]]
    inverses = [m.inv() for m in matrices]
    signs = [int(m[:3, :3].det()) for m in matrices]
    if any(sign not in (-1, 1) for sign in signs):
        raise ValueError("A linear part has determinant other than +/-1.")
    for word in record["presentationRelators"]:
        if word_matrix(word, matrices, inverses) != sympy.eye(4):
            raise ValueError("An exported relator is not an affine identity.")
    h1 = twisted_h1(signs, record["presentationRelators"])
    actual = {"torsion": list(h1.torsion), "freeRank": h1.free_rank}
    if invariants([h1.coboundary_coordinates], len(h1.coboundary_coordinates)) != actual:
        raise ArithmeticError("Independent Smith reduction disagrees with H1.")
    width = len(h1.coboundary_coordinates)
    translations = []
    period_rows = []
    if len(record["translationGeneratorWords"]) != len(record["translationGeneratorMatrices"]):
        raise ValueError("Translation words/matrices have different lengths.")
    for word, supplied in zip(record["translationGeneratorWords"], record["translationGeneratorMatrices"]):
        matrix = word_matrix(word, matrices, inverses)
        if matrix != affine(supplied) or matrix[:3, :3] != sympy.eye(3):
            raise ValueError("A primitive translation word has the wrong affine image.")
        coefficients = relation_row(word, signs)
        values = [sum(coefficients[i] * h1.cocycle_basis_columns[i][j]
                      for i in range(len(signs))) for j in range(width)]
        if sum(a*b for a, b in zip(values, h1.coboundary_coordinates)) != 0:
            raise ArithmeticError("A principal coboundary has nonzero translation restriction.")
        translations.append({"word": word, "translationVector": [str(x) for x in matrix[3, :3]],
                             "cocycleBasisValues": values, "principalCoboundaryValue": 0})
        period_rows.append(values)
    if len(translations) != 3:
        raise ValueError("Expected three primitive translation generators.")
    lattice_volume = Matrix([[Rational(x) for x in item["translationVector"]] for item in translations]).det()
    if not lattice_volume:
        raise ValueError("Exported translations do not span a rank-three lattice.")
    period_smith = smith_normal_form(Matrix(period_rows), domain=ZZ) if width else sympy.zeros(3, 0)
    periods = [abs(int(period_smith[i, i])) for i in range(min(period_smith.shape)) if period_smith[i, i]]
    return {"spaceGroupNumber": record["number"], "name": record["name"],
            "generatorSigns": signs, "neutralE8": actual,
            "relatorMatrix": h1.relator_matrix,
            "cocycleBasisColumnsOnPresentationGenerators": h1.cocycle_basis_columns,
            "principalCoboundaryCoordinates": h1.coboundary_coordinates,
            "primitiveTranslations": translations,
            "translationRestrictionSmithNonzeroDiagonal": periods,
            "signedTranslationCellVolume": str(lattice_volume),
            "checks": {"allAffineRelatorIdentities": True,
                       "allTranslationWordsMatchMatrices": True,
                       "principalCoboundaryRestrictsToZero": True,
                       "independentSmithCalculation": True,
                       "exportReportsPresentationIsomorphism": record["presentationIsomorphismVerified"] is True},
            "geometryRecordSHA256": hashlib.sha256(json.dumps(record, sort_keys=True, separators=(",", ":")).encode()).hexdigest()}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--geometry", type=Path, default=ROOT / "insulator_catalog/source/spacegroup_gap_export.json")
    parser.add_argument("--reference", type=Path, default=ROOT / "benchmarks/spacegroup_e8_1811.06558v1.json")
    parser.add_argument("--source-tex", type=Path, default=Path("/home/arxiv/1811.06558_Bosonic_Crystalline_Symmetry_Protected_T/cSRE_arXiv_v1.tex"))
    parser.add_argument("--output", type=Path, default=ROOT / "results/spacegroup_campaign_20261015/e8_reference_audit.json")
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    geometry = json.loads(args.geometry.read_text())
    reference = json.loads(args.reference.read_text())
    if [row["number"] for row in geometry["records"]] != list(range(1, 231)):
        raise ValueError("Expected all 230 geometry records in order.")
    if [row["spaceGroupNumber"] for row in reference["rows"]] != list(range(1, 231)):
        raise ValueError("Expected all 230 reference entries in order.")
    source_lines = args.source_tex.read_text().splitlines()
    if sha(args.source_tex) != reference["source"]["sourceSHA256"]:
        raise ValueError("Primary full-text hash disagrees with the pinned reference.")
    rows = []
    # Compute every group before reading an expected classification into a row.
    computed = [calculate(record) for record in geometry["records"]]
    for actual, expected in zip(computed, reference["rows"]):
        line = source_lines[expected["sourceLine"]-1]
        if (int(line.split("&")[0]) != expected["spaceGroupNumber"]
                or line.split("&")[3].strip() != expected["sourceCellTeX"]):
            raise ValueError("Reference cell does not match its pinned source line.")
        actual.update(referenceNeutralE8=expected["neutralE8"],
                      comparisonStatus="match" if actual["neutralE8"] == expected["neutralE8"] else "mismatch",
                      sourceLine=expected["sourceLine"], sourceCellTeX=expected["sourceCellTeX"])
        rows.append(actual)
    mismatches = [row["spaceGroupNumber"] for row in rows if row["comparisonStatus"] == "mismatch"]
    paths = {"geometry": args.geometry, "reference": args.reference,
             "runtime": ROOT / "insulator/e8_h1.py", "auditScript": Path(__file__),
             "geometryExporter": ROOT / "insulator_catalog/source/export_spacegroups.g",
             "referenceExtractor": ROOT / "benchmarks/extract_spacegroup_e8.py",
             "primaryFullText": args.source_tex}
    result = {"scope": "3+1D neutral E8 coefficient sector H1(G,Z_orientation) only; no full electronic classification comparison.",
              "spinScope": "The neutral coefficient calculation is independent of the electronic spin convention; this is one geometry audit, not two electronic classification runs.",
              "source": reference["source"],
              "method": "Saturated integer crossed-homomorphism kernel of the full affine presentation modulo its single principal coboundary column; independent Smith reduction and exact affine-word checks.",
              "translationBasisScope": "Cocycle columns are an integral basis before quotienting by the recorded principal column. Translation periods descend through that quotient. Their Smith diagonal records primitive-period divisibility, not merely the abstract H1 free rank.",
              "provenance": {key: {"path": recorded_path(path), "sha256": sha(path)} for key, path in paths.items()},
              "software": {"python": platform.python_version(), "sympy": sympy.__version__,
                           "geometryGAP": geometry["GAP"], "geometryCrystCat": geometry["CrystCat"],
                           "geometryPolycyclic": geometry["Polycyclic"]},
              "counts": dict(Counter(row["comparisonStatus"] for row in rows)),
              "mismatchingSpaceGroups": mismatches,
              "translationRestrictionWithNonunitPeriod": [row["spaceGroupNumber"] for row in rows if any(x > 1 for x in row["translationRestrictionSmithNonzeroDiagonal"])],
              "rows": rows}
    text = json.dumps(result, indent=2) + "\n"
    if args.check:
        if args.output.read_text() != text:
            raise ValueError("Saved audit differs from the reproducible calculation.")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(text)
    print(json.dumps({key: result[key] for key in ("counts", "mismatchingSpaceGroups", "translationRestrictionWithNonunitPeriod")}, indent=2))


if __name__ == "__main__":
    main()
