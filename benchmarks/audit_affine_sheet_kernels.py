#!/usr/bin/env python3
"""Bounded independent mixed-lattice and affine-input audit; no classification run."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import subprocess
import tempfile

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "results/spacegroup_campaign_20261015/affine_kernel_review.json"
REVIEW_RUNTIME_COMMIT = "80d565de744bbd5ef6ac4cca3530511f549547f4"


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def audit(gap):
    # Raw sheet group Z2 + Z + Z. The second obstruction is valued in
    # Z6 / <3> = Z3. Torsion relations must be transformed with both kernels.
    program = r'''
U1_ROOT:="ROOT_PATH";;Read(Concatenation(U1_ROOT,"/gap/load.g"));;
ReviewMixedKernels:=function()
 local killTorsion,M,K3,quotient,inds,orders,terminal,projected,K4,K,Ki,
       x,y,z,expected,relation,result;
for killTorsion in [true,false] do
 if killTorsion then M:=[[1],[1],[0]]; else M:=[[0],[1],[0]]; fi;
 K3:=U1MapKernel(M,[2],3);;
 quotient:=U1Smith([[6],[3]],2,1);;
 inds:=Filtered([1..quotient.rank],i->AbsInt(quotient.diag[i])>1);;
 orders:=List(inds,i->AbsInt(quotient.diag[i]));;
 terminal:=K3*[[0],[0],[1]];;
 projected:=List(terminal,row->(row*quotient.V){inds});;
 K4:=U1MapKernel(projected,orders,3);;K:=K4*K3;;Ki:=Inverse(K);;
 for x in [-3..3] do for y in [-3..3] do for z in [-3..3] do
  expected:=(z mod 3=0) and
    ((killTorsion and (x+y) mod 2=0) or (not killTorsion and y mod 2=0));
  if ForAll([x,y,z]*Ki,IsInt)<>expected then Error("Mixed kernel lost a vector");fi;
 od;od;od;
 relation:=[2,0,0]*Ki;;
 if not ForAll(relation,IsInt) then Error("Original torsion relation was lost");fi;
 result:=U1Smith([relation],1,3);;
 if result.rank<>1 or (killTorsion and AbsInt(result.diag[1])<>1)
   or (not killTorsion and AbsInt(result.diag[1])<>2) then
   Error("Wrong torsion after original-relation transport");fi;
 Print("MIXED_KERNEL_PASS killTorsion=",killTorsion," freeRank=2\n");
od;
if U1MapKernel([[],[],[]],[],3)<>IdentityMat(3) then Error("Empty target kernel");fi;
if U1MapKernel([],[],0)<>[] then Error("Empty source kernel");fi;
end;;ReviewMixedKernels();;
Print("GAP_VERSION=",GAPInfo.Version,"\nAUDIT_PASS\n");QUIT;
'''.replace("ROOT_PATH", str(ROOT))
    with tempfile.TemporaryDirectory(prefix="insulator-affine-review-") as directory:
        path = Path(directory) / "kernels.g"
        path.write_text(program)
        process = subprocess.run([gap, "-q", "-b", str(path)], cwd=ROOT,
                                 capture_output=True, text=True, timeout=60)
    if process.returncode or process.stdout.count("MIXED_KERNEL_PASS") != 2 or "AUDIT_PASS" not in process.stdout:
        raise ValueError(process.stdout + process.stderr)

    export_path = ROOT / "insulator_catalog/source/spacegroup_gap_export.json"
    export_sha = sha(export_path)
    geometry = {r["number"]: r for r in json.loads(export_path.read_text())["records"]}
    paths = sorted((ROOT / "insulator_catalog/generated").glob("spacegroup_*_*.json"))
    if len(paths) != 460:
        raise ValueError("Expected the complete 230 by two-spin input catalogue")
    input_hashes = {}
    for path in paths:
        data = json.loads(path.read_text())
        original = geometry[data["catalog_number"]]
        checks = (
            data["geometry_export"]["sha256"] == export_sha,
            data["affine_generators"] == original["affineGenerators"],
            sorted(data["matrices"]) == sorted(original["pointMatrices"]),
            data["finite_presentation"]["generator_affine_matrices"] == original["presentationGeneratorMatrices"],
            data["finite_presentation"]["relators"] == original["presentationRelators"],
            data["primitive_translations"]["affine_matrices"] == original["translationGeneratorMatrices"],
            data["primitive_translations"]["words"] == original["translationGeneratorWords"],
            data["finite_presentation"]["isomorphism_verified"] is True,
            data["primitive_translations"]["basis_of_full_translation_kernel"] is True,
        )
        if not all(checks):
            raise ValueError(f"Input does not reproduce the certified affine export: {path}")
        input_hashes[str(path.relative_to(ROOT))] = sha(path)
    sources = ["gap/classification.g", "gap/context.g", "gap/backend.g", "gap/backend_resolution.g", "gap/cochains.g",
               "insulator/e8_h1.py", "insulator/e8_spacegroup.py", "insulator/e8_pointgroup.py",
               "insulator/worker.py",
               "scripts/classify.py", "scripts/extend_e8_3p1.py", "tests/test_backend_spacegroup.py",
               "tests/test_spacegroup.py", "tests/test_formula_cache.py", "insulator_catalog/source/export_spacegroups.g"]
    return {"status": "PASS", "scope": "Independent bounded pre-production review; not a 460-case classification",
            "reviewRuntimeCommit": REVIEW_RUNTIME_COMMIT, "scriptSHA256": sha(Path(__file__)),
            "reviewedSourceSHA256": {name: sha(ROOT / name) for name in sources},
            "geometryExportSHA256": export_sha, "catalogueCount": len(paths), "catalogueSHA256": input_hashes,
            "latticeChecks": {"rawGroup": "Z2 + Z + Z", "integerTarget": "Z2",
                "terminalTargetModuloChargeImage": "Z6/<3> = Z3", "enumeratedVectorsPerCase": 343,
                "torsionKilledResult": {"freeRank": 2, "torsion": []},
                "torsionRetainedResult": {"freeRank": 2, "torsion": [2]},
                "emptySourceAndTargetChecked": True,
                "programSHA256": hashlib.sha256(program.encode()).hexdigest(),
                "stdout": process.stdout, "stderr": process.stderr}}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--gap", default="gap")
    parser.add_argument("--output", type=Path, default=OUTPUT)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    result = json.dumps(audit(args.gap), indent=2, sort_keys=True) + "\n"
    if args.check:
        if args.output.read_text() != result:
            raise ValueError("Saved audit differs from exact recomputation")
    else:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(result)
    print("PASS: two mixed free/torsion kernels, 686 membership checks, 460 certified catalogue inputs")


if __name__ == "__main__":
    main()
