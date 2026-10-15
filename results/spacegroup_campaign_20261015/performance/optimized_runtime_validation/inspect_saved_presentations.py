#!/usr/bin/env python3
"""Independently verify saved optimized-run relation matrices and filling maps."""
import hashlib
import json
from math import gcd
from pathlib import Path

import sympy
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

BASE = Path(__file__).resolve().parent
SOURCE = BASE / "validation_o2/backend_exact_results.json"


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit():
    cases = []
    for i, data in enumerate(json.loads(SOURCE.read_text())):
        count = data["presentationGeneratorCount"]
        relations = data["presentation"]
        assert all(len(row) == count for row in relations)
        if count and relations:
            smith = smith_normal_form(Matrix(relations), domain=ZZ)
            diagonal = [abs(int(smith[j,j])) for j in range(min(smith.shape)) if smith[j,j]]
        else:
            diagonal = []
        torsion = [n for n in diagonal if n > 1]
        free = count-len(diagonal)
        assert torsion == data["torsion"] and free == data["freeRank"], i
        row = {"recordIndex": i, "spatialDimension": data["spatialDimension"],
               "generatorCount": count, "smithDiagonalNonzero": diagonal,
               "torsion": torsion, "freeRank": free, "nativeChainIdentitiesVerified": data["nativeChainIdentitiesVerified"]}
        assert row["nativeChainIdentitiesVerified"] is True
        if "wallpaperFilling" in data:
            filling = data["wallpaperFilling"]
            values = filling["generatorFillings"]
            assert len(values) == count
            assert all(sum(a*b for a,b in zip(relation,values)) == 0 for relation in relations)
            step = 0
            for value in values:
                step = gcd(step,abs(value))
            volume = int(Matrix(filling["primitiveTranslationVectors"]).det())
            assert volume > 0 and volume == filling["primitiveCellArea"]
            assert step == filling["fillingStep"]
            assert filling["primitiveBasisGeneratesFullTranslationKernel"] is True
            row["filling"] = {"generatorValues": values, "independentImageStep": step,
                              "allRelationPairingsZero": True, "positiveCellArea": volume,
                              "nativePrimitiveKernelCertificateRetained": True}
        cases.append(row)
    assert len(cases) == 10
    return {"status": "PASS", "sourceSHA256": digest(SOURCE), "scriptSHA256": digest(Path(__file__)),
            "sympyVersion": sympy.__version__, "presentationCount": len(cases),
            "scope": "Independent integer Smith forms and saved filling homomorphisms; no new cochain classification run",
            "cases": cases}


if __name__ == "__main__":
    report = audit()
    (BASE / "saved_presentation_audit.json").write_text(json.dumps(report,indent=2,sort_keys=True)+"\n")
    print("PASS: all ten actual presentations and both saved primitive-cell filling maps")
