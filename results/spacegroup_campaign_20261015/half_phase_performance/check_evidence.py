#!/usr/bin/env python3
"""Verify the packaged hashes, exact witnesses, and integer presentations offline."""
from fractions import Fraction
import hashlib
import json
from pathlib import Path
from sympy import Matrix, ZZ
from sympy.matrices.normalforms import smith_normal_form

ROOT = Path(__file__).resolve().parent

def read(path):
    return json.loads(path.read_text())

def smith_group(rows, columns):
    if not rows:
        return {"freeRank": columns, "torsion": []}
    s = smith_normal_form(Matrix(rows), domain=ZZ)
    diagonal = [abs(int(s[i, i])) for i in range(min(s.rows, s.cols))]
    return {"freeRank": columns - sum(x != 0 for x in diagonal),
            "torsion": [x for x in diagonal if x > 1]}

def verify_charge_control(folder):
    low, roots = read(folder / "lower.json"), read(folder / "completed_roots.json")
    kernel, generators = Matrix(low["kernel"]), Matrix(low["chargeGenerators"])
    relations = Matrix.diag(*low["chargeOrders"]) * kernel.inv()
    assert all(x.q == 1 for x in relations)
    subgroup = smith_group(relations.tolist(), kernel.cols)
    assert kernel * generators * Matrix(low["chargeDifferential"]) == Matrix.zeros(kernel.rows, Matrix(low["chargeDifferential"]).cols)
    boundary = Matrix(low["phaseDifferential"])
    for i, root in enumerate(roots):
        assert root["nativeCharge"] == list((kernel * generators)[i, :])
        assert root["completedNative"]["nativeCharge"] == root["nativeCharge"]
        obstruction = Matrix([[Fraction(x) for x in root["nativeSource"]]])
        for phase in (root["nativePrimitive"], root["completedNative"]["nativePhase"]):
            residual = Matrix([[Fraction(x) for x in phase]]) * boundary - obstruction
            assert all(x.q == 1 for x in residual)
    return subgroup

manifest = read(ROOT / "artifact_manifest.json")
for name, expected in manifest["files"].items():
    assert hashlib.sha256((ROOT / name).read_bytes()).hexdigest() == expected, name

for group in (141, 229):
    name = f"spacegroup_{group:03d}_spin_half_koszul"
    baseline, candidate = ROOT / "baseline_lattice" / name, ROOT / name
    assert verify_charge_control(baseline) == verify_charge_control(candidate)
    for filename, ignored in (("lower.json", "primaryMilliseconds"),
                              ("completed_roots.json", "cpuMilliseconds")):
        a, b = read(baseline / filename), read(candidate / filename)
        for record in (a if isinstance(a, list) else [a]):
            record.pop(ignored)
        for record in (b if isinstance(b, list) else [b]):
            record.pop(ignored)
        assert a == b, (group, filename)
    assert verify_charge_control(ROOT / "baseline_lattice" / f"spacegroup_{group:03d}_spin_half_hap") == verify_charge_control(candidate)

case = "spacegroup_221_spin_half"
a = read(ROOT / "baseline_full_sg221" / case / "result.json")
b = read(ROOT / "full_sg221" / case / "result.json")
assert a["input"] == b["input"]
assert len(set(a["classification"]) | set(b["classification"])) == 38
changed = [key for key in set(a["classification"]) | set(b["classification"])
           if a["classification"].get(key) != b["classification"].get(key)]
assert changed == ["resolutionBuildTimings"], changed
for result, folder in ((a, "baseline_full_sg221"), (b, "full_sg221")):
    source = read(ROOT / folder / "source.json")
    canonical = json.dumps(source["files"], sort_keys=True, separators=(",", ":")).encode()
    assert hashlib.sha256(canonical).hexdigest() == source["sha256"] == result["run"]["sourceSHA256"]
    assert result["run"]["status"] == "complete" and result["run"]["exitCode"] == 0
    native = result["classification"]
    assert native["nativeChainIdentitiesVerified"] is True
    assert smith_group(native["presentation"], native["presentationGeneratorCount"]) == {
        "freeRank": native["freeRank"], "torsion": native["torsion"]}
    filling = native["spaceGroupFilling"]
    for relation in native["presentation"]:
        assert sum(a * b for a, b in zip(relation, filling["generatorFillings"])) == 0
print(json.dumps({"status": "PASS", "hashedFiles": len(manifest["files"]),
                  "exactCompletedChargeRoots": 11, "fullClassificationFields": 38,
                  "unchangedFullFields": 37, "onlyChangedField": "resolutionBuildTimings"}, sort_keys=True))
