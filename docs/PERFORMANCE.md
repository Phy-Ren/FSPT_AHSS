# Exact classification performance

The insulator engine reuses the generic fast paths used by the superconducting
`main` branch at commit `0864495b90297d3e1a0747b77aae17980f6d1f3f`.
There is no runtime dependency on that checkout. U1 obstruction, stacking and
gauge formulas remain in this branch.

## Reused algorithms

1. **Native primary obstruction classes.** For a certified closed integer
   charge `q` and half-integral extension `omega`, compute the class of
   `j[(2 omega mod 2) cup (q mod 2) + Sq^2(q mod 2)]`, where `j(1)=1/2`.
   The coefficient map is equivariant for every phase sign. Its induced map
   on cohomology need not be injective: the result is evaluated in the actual
   signed U1 target. Integer charge lattices, arbitrary torsion orders and
   free generators remain intact. General rational extensions use the bar
   reference. See [charge_primary.g](../gap/charge_primary.g).
2. **Smith cycle periods.** A certified closed phase can be projected to its
   cohomology class by evaluating the dual Smith cycles. This avoids evaluating
   every resolution cell merely to obtain a class. Complete cochains and
   comparison homotopies are still used to solve primitives and construct
   roots and gauge witnesses. See [class_coordinates.g](../gap/class_coordinates.g).
3. **Generated integer formulas.** The generic scalar DAG execution method
   from `main` evaluates expressions generated from the U1 3+1D source and
   stacking formulas. Python integers provide the default portable execution;
   an optional checked C++ VM falls back to Python on overflow. The original
   public validation runs first. Unsupported domains retain the original
   evaluator. See the [compiled formula specification](../insulator/_compiled/README.md).
4. **Certified closed charge sources.** The full source of a checked integer
   native cocycle has an exact binary expression modulo one. Its zero derivative
   is not repeatedly expanded. An even native charge has a literally zero U1
   source while retaining its full integer charge. Every nonzero source still
   uses the comparison homotopy when solving its primitive. Ordered contiguous
   group products also avoid redundant inversions in cup evaluation, including
   for nonabelian groups. See [charge_source.g](../gap/charge_source.g).

5. **Certified half-valued source transfer.** For an initial closed charge root,
   even comparison-chain coefficients contribute zero to its half-valued phase
   source. The source evaluator skips those terms and evaluates the normalized
   three-term degree-three cup-one expression lazily. The certificate binds the
   exact context, charge/source callbacks and background actions. The native
   primitive and full integral comparison homotopy remain unchanged, including
   quarter-valued completed phases. Literal zero sources retain literal zero
   primitives; uncertified or non-half-integral inputs retain the reference
   route. See [backend_half_phase.g](../gap/backend_half_phase.g).
6. **Canonical zero lower fields.** After the complete vacuum gauge has
   eliminated a sheet or charge cocycle, replace its proved pointwise-zero
   callback by the canonical zero function. The full phase transformation
   still uses the original completed state and unchanged gauge parameters.
   This avoids repeatedly expanding zero lower fields inside later stacking
   operations. It applies to completed states in the internal reduction
   routine; the unrestricted local formula API is unchanged. See the
   [full-cochain proof](../results/spacegroup_campaign_20261015/vacuum_reduction_performance/proof.md).

These optimizations supplement the existing exact simplex plans, bounded
request caches, paired-spin geometry reuse, and optimized GAP executable.
The two spins retain separate extension cocycles and output files.

## Controls and provenance

The production defaults are `--charge-primary native --phase-class cycles`.
`--charge-primary compare --phase-class compare` checks the native primary
against both bar class projections. The full reference is:

```sh
U1_DAG_MODE=reference python scripts/classify.py \
  --case point3_06_spin_half --charge-primary bar --phase-class native \
  --closed-charge-source reference --vacuum-reduction reference \
  --output /absolute/path/new-reference-run
```

`--phase-class` controls the bar class projection when that route is used;
explicit `--charge-primary native` takes precedence for eligible primaries.
It does not change the full primitive calculation. Each case records the
requested modes and actual native/bar primary call counts. Each campaign
records source hashes, selected inputs, logs, witnesses and
`formula_runtime.json`, including the optional VM binary hash. The runner
rejects a campaign whose source or selected VM artifact changes during execution.
`--closed-charge-source compare` additionally checks the certified full-source
expression against the original expression pointwise modulo one.
`--vacuum-reduction canonical` is the production default; its `reference`
mode retains the original lower-field callbacks after vacuum gauges.

## Measured checks

Measurements below refer to specific workloads, not universal speed factors.

The [calibrated 4+1D campaign](../results/four_dimensional_20261016/README.md)
uses a bounded exact cache keyed by the full background and cochain values,
binary completed-state powers, and faithful cyclic cohomology pairings.
The signed C2 path uses its complete normalized one-generator complex.
All source, stacking and gauge corrections remain in the calculation.
On `n08.local`, cache off/on measurements for the complete cyclic cochain
classification were **0.744347/0.313270 s for C3** and
**5.161713/1.492532 s for C6** (2.38x and 3.46x). Every retained mathematical
field and witness agrees literally; independent eta calibration and process
overhead are outside these microbenchmark timings. The full 14-order batch,
including physical calibration, used four processes with a 13.23 s case
execution interval. C18 took 11.41 s. Exact source evaluations for C6 fell
from 2175 to 156 and CI-product evaluations from 525 to 72.

The [expanded cyclic and translation batch](../results/four_dimensional_batch2_20261016/PERFORMANCE.md)
adds 23 cyclic inputs through C64: eight workers completed the full batch,
including physical calibration, in 150.817 seconds. Complete witness JSON is
retained with deterministic lossless gzip, reducing 189,833,767 bytes to
3,234,519 bytes. Four infinite translation inputs use complete finite
classifying spaces and took 6.969 seconds of case time including certificate
replay; rank four took 6.746 seconds.

The finite-abelian engine also offers `--charge-primary native|compare`.
It replaces only the degree-four primary class calculation; actual phase
completions, root powers, gauges and mixed commutators remain unchanged.
Full C2² and C2³ calculations agree literally in bar, native and compare
modes after excluding the two mode flags. The native path shows no overall
speedup in these measurements (13.184 versus 12.833 seconds for C2²;
119.671 versus 118.357 seconds for C2³), so `bar` remains the default.
The [abelian campaign evidence](../results/four_dimensional_abelian_20261016/README.md)
records the comparisons and any bounded run failures separately.

The [adjacent native-vector reuse check](../results/spacegroup_campaign_20261015/native_vector_reuse/README.md)
reduces native transfer calls from **384 to 352 across ten complete classifications**
by immediately reusing vectors already returned by the full completed-state check.
All output fields other than resolution construction timings agree, including
every check and witness; 864 signed gauge-phase values also agree exactly.
This is an operation-count result, with no measured wall-time speedup claim.

The isolated [q2 mod-two transfer control](../results/spacegroup_campaign_20261015/q2_full_control/README.md)
preserves all 35 scientific fields in a complete same-node SG141 spin-half
comparison, but shows no whole-run benefit: 1342.36 versus 1356.01 wall seconds.
It is not part of the production defaults. A faster individual source
evaluation is insufficient evidence for a faster complete classification.

The isolated [marked-half doubling control](../results/spacegroup_campaign_20261015/marked_half_full_control/README.md)
also preserves all 35 scientific fields in SG141 spin-half and exercises six
marked doubles, but shows no whole-run improvement: 1359.28 versus 1360.11 wall
seconds, with slightly higher CPU time and maximum RSS. It was not adopted;
no marked-only SG226 run was launched.

| Workload on the same local host | Reference | Accelerated | Scope |
| --- | ---: | ---: | --- |
| Complete SG14 classification, exact simplex engine versus added source/product DAG | 70.919 s | 32.456 s | Complete roots, gauges, primitives and presentation agree |
| Replay of 19,099 captured SG14 cache-miss responses | 41.520 CPU s | 4.448 CPU s, Python DAG; 3.991 CPU s, native DAG | Every response agrees; includes unchanged gauge operations |
| Seven-generator SG221 spin-half primary charge obstruction map | Not complete after 120 wall s | 0.547 CPU s | One stage only; not an end-to-end speed comparison |
| Complete SG221 spinless, native primary/DAG baseline versus added closed-source and cup optimizations | 429.263 s | 268.854 s | All mathematical fields agree literally; peak RSS 2.46 to 1.74 GiB |
| SG141 spin-half, initial charge completion with fixed Koszul resolution | 60.853 CPU s | 20.573 CPU s | Five full charge lifts and every native witness agree; later gauges/stacking excluded |
| SG229 spin-half, initial charge completion with fixed Koszul resolution | 74.107 CPU s | 21.351 CPU s | Six full charge lifts and every native witness agree; later gauges/stacking excluded |
| Complete SG221 spin-half, G baseline versus half-source/lazy-cup candidate | 234.922 s | 224.534 s | All 37 mathematical/operation fields agree; only resolution timings differ; modest observed whole-run change |
| Complete SG221 spin-half, G baseline versus canonical zero lower fields | 234.922 s | 127.065 s | All 35 mathematical fields agree literally; peak RSS 1,823,532 to 1,301,088 KiB |

The primary class tests include 32 affine charge generators, 16 nonzero
obstructions, independent coefficient signs and general rational fallback.
The period tests include torsion orders 2, 3, 4, 6, 8 and 9. Formula tests
include negative carries, huge integers, native overflow, invalid inputs and
context isolation. The integrated engine, canonical zero reduction, runner
timing, recovery and explicit collection-selection tooling passed all 122
tests in 69.325 seconds. The [recorded invocation and source hashes](../results/spacegroup_campaign_20261015/deployment_h/README.md)
distinguish this complete run from the earlier 116-test summary.
The half-source addition has focused tests covering 98,304 nonabelian source
values, signed transfers, complete primitive values, quarter-valued primitives,
and literal-zero identity. A complete rerun of all 64 spatial point-group backgrounds
preserves every final group and integer presentation; the
[point-group audit](../results/point3_optimized_20261015/README.md) also records
and investigates environment-dependent cochain representatives.

The [formula evidence](../results/spacegroup_campaign_20261015/compiled_formula_performance/README.md)
and [native primary evidence](../results/spacegroup_campaign_20261015/native_charge_primary/README.md)
contain immutable records, source identities and reproducible checks.
The [closed-source and cup evidence](../results/spacegroup_campaign_20261015/generic_cochain_performance/README.md)
includes the complete SG221 comparison and independent native-equation checks.
The [half-source evidence](../results/spacegroup_campaign_20261015/half_phase_performance/README.md)
preserves its bounded stage controls, full SG221 comparison, final zero-path
regression, source overlays and independent review. The roughly threefold
charge-stage gains do not imply the same speedup for a full classification.
The full SG221 half-source observation was only about 4.6%.
The separate [canonical zero-field experiment](../results/spacegroup_campaign_20261015/vacuum_reduction_performance/README.md)
preserves the complete before/after records and signed pointwise controls for
its 1.85-fold observed improvement. Neither experiment establishes a universal
campaign speed factor.

An actual [SG210 spinless G/H overlap](../results/spacegroup_campaign_20261015/overlap_g_h_210/README.md)
preserves 34 literally identical scientific fields, including complete roots,
native phases, gauges, presentations and primitive filling. The paired G and
standalone H native classifications differ only in four execution fields. Their different
nodes, scheduling, memory limits and older G timing method prevent a controlled
speedup claim; the archived verifier checks the exact equality and independent
Smith/filling calculations.

The [twelve further G/H comparisons](../results/spacegroup_campaign_20261015/overlap_g_h_remaining/README.md)
also agree literally in all 34 scientific fields. Five have both ordinary case
records complete; seven are H ordinary / G native-only diagnostics. Their
containing campaigns were incomplete at capture, so this is additional
correctness coverage, not campaign acceptance or a controlled speedup result.

New paired runs measure elapsed time from monotonic observations of exact
completion markers. Older paired records that derived elapsed time from NFS
file timestamps retain their original values, including negative values;
those values cannot support timing comparisons. Classification acceptance is
independent of these timing fields.

Space-group campaigns run on compute nodes with immutable source snapshots.
Concurrency is bounded by measured memory as well as CPU capacity. A failed
or incomplete process is retained as evidence and retried separately; launch
coverage is never reported as completed classification coverage.

The [paired 8g tail control](../results/spacegroup_campaign_20261015/failed_h_tail_control/README.md)
exhausted GAP workspace during SG226 spin-half; its spinless partner never
started. The README's full-space-group example therefore explicitly requests
`--memory 32g --timeout 14400`: a workspace cap per GAP process and a time
budget per case, doubled for a paired process. Concurrency must also leave room
for the Python workers. The separate [32g spin-half launch evidence](../results/spacegroup_campaign_20261015/deployment_h_tail_highmem/README.md)
records the higher-memory controls; it does not establish their completion or
a performance gain.

The [accepted high-memory tail](../results/spacegroup_campaign_20261015/completed_h_tail_highmem/README.md)
records the subsequently completed SG226 and SG230 spin-half classifications.
The separate [12g SG226 spinless failure](../results/spacegroup_campaign_20261015/failed_h_spinless_12g/README.md)
retains its workspace-exhaustion error and a bounded profile showing garbage
collection. It is not an accepted result; its retry has independent provenance.
