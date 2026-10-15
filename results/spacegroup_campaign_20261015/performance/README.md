# Space-group performance validation

The candidate adds only exact computational changes: literal `delta(U1Zero) = U1Zero`, complete serialized-request caching, and cached simplex geometry using consecutive group products. Each new cache is capped at 8,192 entries. It changes no differential, stacking or gauge formula.

`check_results.py` compares both SG19 spins against the original cluster pilot. It requires identical inputs, all prior classification fields, complete presentations, roots, incoming relations, native charge/phase vectors and completion checks. The only allowed normalization identifies an omitted zero sheet gauge (`[]`) with its explicit all-zero vector (`[0]`). Timing/cache metadata are excluded from the mathematical comparison. Primitive filling must independently equal four.

The local candidate pair completed in 50.94 seconds (22.48 seconds spin-half and 28.43 seconds spinless). These local timings must not be compared as speed ratios to the cluster reference: the processors and GAP builds differ. `local/comparison.json` therefore reports no cross-host ratio. `local/validation_original_paths.json` retains the original temporary artifact paths and source hashes.

The bounded baseline profile received 66,076 Python requests, of which only 1,731 required a distinct formula evaluation. GAP request construction and group arithmetic dominated; native bar contraction used under one CPU second in this sample. The optimized full local SG19 pair made 923 and 1,893 worker calls. Profiling files retain their original source paths, and the baseline GAP excerpt omits zero-cost entries while its complete original SHA256 is in the archive manifest.

Cluster smokes C and D use the same frozen commit `80d565de744bbd5ef6ac4cca3530511f549547f4`, source manifest, n02 node, library/package tree, spin order and paired-run policy. C uses the original GAP kernel compiled without an optimization flag; D uses the separately built `-O2` kernel, SHA256 `873e902ee797706160601846c1ad6582c05e0aebd069bdd7efcff3d081f96fea`. Neither the original kernel nor the formulas were changed by the rebuild. [Build provenance](gap_o2_build/README.md) distinguishes startup/arithmetic microbenchmarks from the following complete calculation.

| SG19 measurement | C: original kernel | D: optimized kernel |
|---|---:|---:|
| Spin-half case interval | 608.668 s | 85.570 s |
| Spinless case interval | 638.254 s | 163.201 s |
| Full paired process | 1,278.120 s | 279.974 s |
| Actual formula-worker calls | 923 + 1,893 | 923 + 1,893 |

Both spins agree with pilot A in every prior mathematical field, subject only to the zero-gauge normalization above. C and D additionally agree exactly in all current classification fields except resolution build timings, including their new primitive-cell filling witness (step four), cache counts and every root relation. `check_runtime_pair.py` regenerates [this exact comparison](cluster_cd_comparison.json). The observed full-process ratio is 4.565; the ratio of summed case intervals is 5.012. The first case interval includes shared startup and the second uses the sibling context. Full batch timing also includes final worker shutdown/process exit. The source-identical campaigns overlapped under production-B load; this is a same-node campaign comparison, not a controlled isolated benchmark.

Pilot A ran each spin in its own process: 1,103.716 and 1,151.751 seconds. Comparing their summed durations with D's full paired process gives an observed ratio of 8.056, jointly reflecting the exact cache changes, paired reuse, compiler optimization and different background load. The 9.066 ratio obtained using D's summed case intervals excludes final process overhead and is not an end-to-end timing.

Resource samples read `/proc` only. Their sampled `VmHWM` is a lower bound on the eventual process peak, not a final `wait4` measurement. The observed SG19 GAP peaks were 342,964 KiB (C) and 312,352 KiB (D); sparse sampling does not support a memory-reduction claim. `cluster_cd_resources.jsonl` retains the raw samples. SG14 smoke runs continue separately; their pending results are not used in the SG19 correctness claim.

The preserved completed production-B SG195 pair is under `reference_b_n08/`, for comparison with the new optimized full campaign when its matching pair finishes. It includes nontrivial torsion and is not counted as an optimized-runtime equivalence check until both new results pass.

Reproduce a saved comparison with:

```sh
python results/spacegroup_campaign_20261015/performance/check_results.py --campaign results/spacegroup_campaign_20261015/performance/cluster_c
```

The separate [optimized-runtime validation](optimized_runtime_validation/README.md) records 15 passing focused tests with no skips and independent exact Smith/filling checks. It is supplementary evidence, distinct from the completed SG19 cochain comparisons above.

The selected four-data model and its physical-kernel calibration caveat are unchanged. These performance checks do not resolve that separate physical identification.
