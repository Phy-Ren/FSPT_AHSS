# Same-source optimized GAP compatibility validation

This validation runs serially on n08 using an isolated full archive of commit `80d565de744bbd5ef6ac4cca3530511f549547f4`. It does not start or cancel production classification jobs. The archive contains 1610 files, including the original tests and fixtures; its SHA256 is `cea5836a0bb9d447c7f99bea66fa3c46c16bef72276f69a7bb417cebcf3edd95`.

All 45 files used by the classifier's runtime source manifest match the snapshot-C smoke manifest byte for byte: `63887ca47cf557f30a3a867bac16392b05c8d107a8cdb87ffbd4d47784ccdc88`. The runtime-only and full-validation archive hashes differ because their file sets differ. `same_source_verification.json` records the exact comparison file and its hash.

The optimized GAP 4.13.1 executable is `/home/user/xyren/software/gap-4.13.1-o2-20261015/gap`, SHA256 `873e902ee797706160601846c1ad6582c05e0aebd069bdd7efcff3d081f96fea`. Its isolated `gap-o2` launcher uses the original package tree. Build/compiler/package provenance is copied into `binary_build_evidence_final/`; packages and the original executable remain unchanged.

## Environment and invocation

On n08, after reusing the persistent SSH channel:

```sh
export PATH=/home/user/xyren/AllFSPT_insulator/runtime/bin:$PATH
export LC_ALL=C LANG=C OMP_NUM_THREADS=1 OPENBLAS_NUM_THREADS=1
cd /home/user/xyren/AllFSPT_insulator/validations/gap_o2_80d565d_20261015
PYTHONDONTWRITEBYTECODE=1 python3 run_validation.py \
  --launcher /home/user/xyren/software/gap-4.13.1-o2-20261015/gap-o2 \
  --binary /home/user/xyren/software/gap-4.13.1-o2-20261015/gap
```

The campaign wrapper resolves Python 3.8.16 and also ensures that GAP's formula-worker subprocess uses this interpreter. The first setup attempt used bare node Python 3.5 and stopped before invoking GAP or any test; its exact script and logs are retained in `setup_attempt_01/`. The second attempt completed the optimized GAP/package version probe but stopped before tests because the external validation harness tried to hash its own relative path after changing directory. The harness path was corrected, and `setup_attempt_02/` preserves that attempt. Neither setup failure is counted as a classification or optimized-binary test failure.

The validation script creates `validation_o2/` exclusively and refuses to overwrite an existing result. It places a `gap` symlink to the optimized launcher first in its test PATH, checks the binary hash, records package versions and commands, and checks all archived file hashes before and after the tests.

## Bounded coverage

Fifteen tests from the frozen source are selected:

- `test_backend` (seven tests): 2+1D cyclic complete roots, nonbinary extensions, incoming relations, a genuinely lifted uniform IQH root, and full infinite wallpaper groups with primitive filling; 3+1D CI completions and integral obstructions. The ten computed native records are preserved in `backend_exact_results.json`.
- `test_backend_cochains` (one): 108 independent signed bar/gauge and integral-primitive evaluations.
- `test_backend_source_cache` (one): exact context/background isolation, including shallow copies and cyclic records.
- `test_formula_cache` (one): complete-request cache isolation, nonabelian face transport, eviction, and literal zero versus nonzero exact cochains.
- `test_backend_spacegroup` (two): integer obstruction preimage lattices and paired versus independent full-affine P1 runs; exact presentations, roots, gauge witnesses, sheet lattices and primitive filling must agree, followed by the E8 extension.
- `test_spacegroup` (three): neutral signed H1, primitive screw periods, mixed free/torsion presentations and rejection of corrupt affine words.

No test is permitted to skip, and the final count must equal 15. This is compatibility validation against the optimized cluster binary, not a second execution of the 78-test local suite or a full 460-case campaign. Separate SG14/SG19 optimized smoke runs are coordinated by the parent and are not duplicated here.

## Acceptance evidence

`validation_o2/result.json` is authoritative for pass/fail, test count, failures/skips, timings, unchanged-source checks and output hashes. `metadata.json` records the executable/launcher hashes, exact interpreter/environment, GAP/package versions, command and source identity. `tests.log` retains individual test outcomes. Root-relation, Smith and primitive-filling conclusions are limited to the selected actual tests and any separately linked saved-run comparisons; matching abstract groups alone is not sufficient.
