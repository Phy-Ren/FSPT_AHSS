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
timing and recovery tooling passed all 116 tests in 68.609 seconds.
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

New paired runs measure elapsed time from monotonic observations of exact
completion markers. Older paired records that derived elapsed time from NFS
file timestamps retain their original values, including negative values;
those values cannot support timing comparisons. Classification acceptance is
independent of these timing fields.

Space-group campaigns run on compute nodes with immutable source snapshots.
Concurrency is bounded by measured memory as well as CPU capacity. A failed
or incomplete process is retained as evidence and retried separately; launch
coverage is never reported as completed classification coverage.
