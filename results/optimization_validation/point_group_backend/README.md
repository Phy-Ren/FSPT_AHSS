# Finite point-group development controls

The accepted 64-model calculation is in [../../point_groups](../../point_groups/). This directory preserves the three earlier development trials, including failures. These trials used geometric matrix inputs and the independent FSPT engine; no classification or stacking reference table supplied calculation inputs.

| Trial | Successful tasks | Failed tasks | What changed afterward |
|---|---:|---:|---|
| v1 | 2 | 9 | Direct conversion from matrix groups to Pcp groups was unreliable for the small inputs. The finite backend now transports through the exact right regular permutation representation and checks every multiplication. Both initial Oh models completed. |
| v2 | 10 | 1 | The backend control and nine model runs completed. Spinless C1 exposed an empty positive-degree matrix operation in the generic zero-background gauge path. The finite adapter now certifies the exhaustively zero Pin cocycle with its literal zero primitive. |
| v3 | 3 | 0 | Spinless C1 and both Ci conventions completed. This numerical source was then frozen for all 64 production models. |

Each `cohorts/` directory contains the original source snapshot, pilot specification, generated drivers and available raw/final/checkpoint results. `tasks/` contains all 25 original worker states, GNU time metrics and logs. Logs are renamed from `stdout.log` to `stdout.txt` without changing their bytes. Failed attempts remain failed; successful later runs do not replace them.

[archive.json](archive.json) records the original paths, sizes and SHA256 hashes of all 301 payload files (11,621,033 bytes). Its own SHA256 is `5991cb959c422fa2b865568c86b0c74c18286d464b9393985719c5b9d82bdd42`. All three numerical source maps match the original pilot `source_id` values. `harness_current/` contains harness files copied at archival time, as explicitly recorded; it does not retroactively attest to an unrecorded earlier harness hash.

The successful backend control verifies all 32 geometric inputs and five representative finite resolutions, including signed/integer/F2 differentials, cohomology coordinates, and comparison-homotopy primitive equations. It is a numerical/backend control, not a proof of the physical uniqueness of any selected p+ip product.

[final_run_freeze_manifest.json](final_run_freeze_manifest.json) inventories the unmodified production source and all 64 completed result payloads. Its SHA256 is `899677ef6ae30b701956503ad9e33a4bfd66e8e6d2122a8a224b21684b9779e2`. This inventory was written after completion and strict audit, and records its actual creation time. The numerical source itself was frozen before execution. The accepted production archive has its own separate manifest; neither manifest is rewritten by this development archive.

To repeat the backend control on an allocated compute node with GAP/HAP available, set `AFS_ROOT` to the absolute path of `cohorts/point_group_controls_v3/source`, then read `harness_current/tests/test_point_group_backend.g` through `scripts/run_gap.py --sentinel AFS_POINT_BACKEND_TEST_PASS`. Follow [the cluster instructions](../../../docs/CLUSTER_RUN.md) for allocation and persistent SSH reuse. Development timings from these overlapping small trials are not the uniform 64-model benchmark.

## Follow-up marked cochain controls

After the independent 64-model calculation, discrepancies between external tables motivated four further controls. Their original source, results, drivers, task states, metrics and logs are separately preserved in [marked_audit/archive.json](marked_audit/archive.json): 71 payload files, 3,422,357 bytes; manifest SHA256 `1e9b3e53639f6f57c4739262b7d04d378e551f4c62faeb2412d878c4d9a1135e`. All four tasks completed normally within their original 600-second budgets. They did not read reference values or change the accepted results.

For spinless point groups 10 (`-4`), 20 (`-3m`) and 22 (`-6`), `AFS_STACK_AUDIT=true` checks individual bar simplices in the resolution-comparison support: lift flatness, incoming MC boundaries, secondary-coordinate corrections, and exact CF/phase gauges in each lower relation. These are support checks, not an exhaustive enumeration of all finite-group simplices. All numerical fields and native witnesses match the formal run. The only differences are measured CPU timestamps and `checkedComparisonSupport` becoming true. Point group 22 retains its original upper-carry scope; these checks do not turn an unknown upper phase into a marked witness.

The separate point-group-10 control uses the complete bar lower model, interpreted CA formulas, integral contraction, general phase solver, and full native cup product. It disables compiled CA formulas, the closed-CF/half-phase shortcut, mod2 contraction and mod2 bar evaluation, and the projected background cup0 shortcut. On this actual four-element group it checks every nondegenerate tuple needed for lift flatness, all ordered generator products, literal generator squares, and their reduction gauges. There are 18 degree-two, 270 degree-three, 810 degree-four and 1,458 degree-five equality checks. Its full lower export, including native witnesses, matches the formal result. The measured relation is `2 B1 = D1`, with `2 D1 = 0`, in the saved common marked basis.

The comparison proves agreement with the delivered formulas and the exact group/cochain implementation on these finite controls. It does not independently establish the physical completeness or uniqueness of those formulas. Every ignored field and its reason is listed in [marked_audit/comparison.json](marked_audit/comparison.json). Reproduce it in a new output file with:

```sh
python3 scripts/compare_point_group_marked_controls.py \
  --formal results/point_groups \
  --controls results/optimization_validation/point_group_backend/marked_audit/run \
  --tasks results/optimization_validation/point_group_backend/marked_audit/tasks \
  --output /tmp/point_group_marked_comparison.json
```
