# Guarded 3+1D integer-DAG performance evidence

The compiled source and stacking phase evaluate the current U1 insulator
formulas exactly. The generic integer VM/builder architecture was adapted from
main commit `0864495`; none of that branch's superconducting expressions or
runtime imports is included. See [the execution-domain documentation](../../../insulator/_compiled/README.md)
for the precise guard, original validation, negative-integer arithmetic,
64-bit overflow fallback, and arbitrary-rational reference path.

## Complete SG14 result

The final isolated implementation classified `spacegroup_014_spin_half` in
**32.456 s**, compared with **70.919 s** for the preceding exact Python kernel,
a **2.185×** improvement. Its GAP/backend files remained identical to the
reference, so this comparison isolates formula execution. An earlier prototype
completed in 30.402 s; the archived final run is the reported measurement.
These are local actual classifications, not cluster throughput estimates.

The complete native output records agree, including every root relation,
incoming relation, integer correction, phase primitive, obstruction map,
worker request count, cache statistic, and space-group filling witness.
`sg14_equivalence.json` ignores only `resolutionBuildTimings` by policy; in
this final pair even that field happened to agree. The normalized native SHA256
is `a14ee434d71902dd806c79ff43883655a6656d1405499287b9807fada97c5e41`.

The prior unoptimized frozen-C result was also mathematically identical, but
its 345.367 s timing belongs to the separate
[Python kernel audit](../python_kernel_performance/README.md). It is not the
reference timing used to calculate this new change's 2.185× gain.

## Whole-request replay

All **19,099** captured cache-miss requests from the complete original run were
replayed through unchanged worker decoding, `Symmetry` construction, public
validation, and result serialization. They include 2,047 sources, 2,167
products, 13,638 gauge requests, and 1,247 integer obstruction/product requests.
All response dictionaries were compared exactly before computing the digest.

| Evaluation mode | CPU seconds | Exact full-response digest |
| --- | ---: | --- |
| Existing reference cochains | 41.520 | `fc0e36dd2ee7a5c73d15a9e294b5ebb9563294d3295ec9acb941f6c6dabde259` |
| Integer DAG with native VM | 3.991 | same |
| Integer DAG with Python integers | 4.448 | same |

Native source dispatch occurred 2,030 times and product dispatch 2,152 times;
all other requests retained reference evaluation. No native overflow occurred
in this captured run. The independent tests deliberately trigger both an
out-of-range input and intermediate multiplication overflow and compare the
big-integer fallback with the full reference. Replaying the remaining gauge
requests is essential: no gauge formula or gauge equivalence was replaced.

The native gain over the current reference on this request set is 10.4×; the
Python DAG gain is 9.3×. The difference between request replay and full-case
speedup reflects the remaining GAP work. No universal speedup is inferred.

## Exact checks and provenance

The six focused tests cover 48 randomized source/product cases with independent
vertex signs, negative decorations, and both completed lower towers and partial
simplex inputs. They compare reference, Python-DAG, and native modes; test
non-half-integral backgrounds, malformed input/error equivalence, missing
native libraries, repeated contexts, reproducible compilation, source-hash
freshness guards, and both kinds of integer overflow. The additional 36
signed-rational background requests span all supported dimensions and retain
the reference behavior. See the saved test log and replay artifacts.

The combined working-tree suite, including the separate GAP primary-class
transfer work, passed **95 tests in 54.272 s**, with no skips. The complete SG14
comparison above intentionally used its earlier unchanged GAP backend to
isolate the formula optimization. The suite and the SG14 timing therefore
measure different, explicitly recorded source combinations.

`provenance.json` records the exact main source identities, immutable input
archive hash, captured-request compressed and uncompressed hashes, and the
integer-DAG payload hashes. Both DAG payloads remained identical between the
whole-request replay and final integrated implementation; only provenance
metadata and the freshness guard were added afterward. The final complete
SG14 run exercised that guard. `implementation_sha256.json` identifies the
integrated implementation files, and each SG14 folder includes its original
source manifest and run metadata. `build.json` records compiler/version,
flags, C++ source hash and binary hash. No executable is committed.

The independent read-only review found no arithmetic or dispatch defect.
A fast-domain guard is not a proof of lower-tower closure: the original
`validate` parameter continues to decide whether that check is required.

Check the archived evidence without running a classification:

```sh
python results/spacegroup_campaign_20261015/compiled_formula_performance/check_evidence.py
```

Replay every original request against the current checkout (roughly several
CPU seconds with the DAG, or roughly 40 seconds with the reference locally):

```sh
python results/spacegroup_campaign_20261015/compiled_formula_performance/check_evidence.py --replay --mode python
```

`--mode auto` additionally uses a native library if one has been built with
`scripts/build_formula_vm.py`; otherwise it uses the same Python integer DAG.
`--mode reference` repeats the exact cochain baseline. The evidence checker
never launches a group classification or modifies archived files.
