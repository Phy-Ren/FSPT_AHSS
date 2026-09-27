# Exact optimization of a marked complex-fermion lift

The optional branch in `AFSStackLift(ctx,1,c)` applies only when `c` is a
closed degree-three mod-two representative. The supplied obstruction then
restricts literally to

\[
O_5(0,c)=\tfrac12(c\smile_1c+c\smile_2\delta c)
        =\tfrac12c\smile_1c.
\]

The branch uses `AFSClosedCFObstructionLazy` to evaluate the three cup-one
products. It evaluates each short face first and skips the corresponding
long face when the short factor is zero. This changes evaluation order,
without changing the cochain. The general obstruction remains in use for
nonclosed defining cochains, including Majorana lifts.

`AFSSolveHalfPhaseData` transfers this actual bar cochain to the native
resolution. Its values are in `(1/2)Z/Z`, so even chain coefficients
contribute zero and either coefficient sign acts identically. The helper
checks the half-valued condition on every evaluated term. It then uses the
same rational native solve and the same integral comparison-homotopy
correction as the general solver. The returned `nativePrimitive` is retained
with the marked state, avoiding a second transfer of the same obstruction.

This procedure does not replace the transferred bar operation by an
independently constructed native higher diagonal. Equality in cohomology
would not be enough to preserve a marked phase primitive.

The accepted `gap/run_one.g` enables `AFS_USE_CLOSED_CF_OBSTRUCTION` by default.
It requires `gap/stacking_closed_cf.g` and
`gap/backend_half_phase.g`; missing helpers produce an error. The separate
mod-two bar comparison map can be enabled with `AFS_USE_MOD2_BAR` after its
helper is loaded. The immutable v08 comparison campaign enables both options.
The accepted v09 configuration keeps the lazy closed-CF/half-phase branch
enabled but disables the mod-two bar comparison map. All live GAP source files
now match the accepted frozen source in `results/space_groups/source`.

## Compare complete campaign configurations

| Campaign | Mod-two bar comparison map (`AFS_USE_MOD2_BAR`) | Lazy closed-CF and half-phase transfer (`AFS_USE_CLOSED_CF_OBSTRUCTION`) |
|---|---|---|
| Corrected v07 baseline | Off | Off |
| Optimized v08 comparison | On | On |
| Accepted closed-CF v09 | Off | On |

These switches do not change the obstruction, coefficient convention,
stacking law, or canonical marked phase. They change how identical cochain
values are evaluated and cached. The separate mod-two contraction option
used during classification is retained in all three configurations; turning
off the mod-two **bar comparison map** does not turn off that classification
optimization.

The immutable v08 source is
`6ac87338038729efff1462add90fb1ce901963048551e28d232aae34773de971`
in `runs/optimized_v08_source`, with outputs in `runs/full_optimized_v08`.
The v09 source is
`9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`,
with original outputs in `runs/full_closed_cf_v09` and the accepted archive in
`results/space_groups`. Both run the complete per-group
classification, free-generator construction, and stacking sequence in one
process and retain the same classification object for subsequent operations.
The cross-configuration audit compares actual native generator fields and
relations as well as the final group types.

The v09 comparison was prompted by SG73 profiling: v08 made its CF lift
faster, but the following Majorana B1 lift took approximately twice as long.
Cache behavior across stages can therefore offset a local CF improvement.
A faster first CF lift does **not** establish a faster complete calculation.
The accepted uniform v09 run completed all 230 groups in 12699.328 observed
seconds, with classification checkpoints complete in 783.017 seconds. All 230
saved mathematical outputs agree literally with the complete generic v07
baseline, including marked fields, phase primitives, relation gauges, actual
free lattices and Smith transformations. No per-group configuration selection
was made. Exact comparison records and the second complete configuration are
archived in `results/optimization_validation`.
The complete v08 run took 14751.680 observed seconds, compared with
12699.328 for v09; their summed GAP CPU times were 70171.795 and 62963.022
seconds, respectively. Peak single-task RSS was 20.063 GiB versus 16.869 GiB.
All saved mathematical fields match for all 230 groups across these two
complete campaigns as well.
The campaigns share five PBS workers (28 slots each) with other candidate and
validation jobs. Observed completion times describe this deployment, including
queueing and shared load; they are not an isolated benchmark establishing an
intrinsic algorithm ranking.

## Exactness controls

Validation includes an independent exhaustive comparison of the closed
restriction on all 32,768 local sign/cochain states, a nonclosed negative
fixture, direct-versus-generic cup-one checks, and exact half-phase native
transfer checks. The earlier SG87 marked-lift control compared both native
phase seeds, complete obstruction support, and all 2,690 phase support tuples
for each of two generators. That control used the earlier generic closed
helper and general transfer; its timings are not a production benchmark
because classification warmed integral contractions.

A separate cubic SG228 control passed equality of all 231 native
obstruction coordinates. Its records, along with exact half-phase native
and translated primitive tests, are preserved in
`docs/validation_runs/cf_backend_optimizations.json`.

The corresponding earlier SG228 control timed out after 1,800 seconds and
is inconclusive. It has not been counted as a passing check. Both outcomes
are preserved in `docs/validation_runs/closed_cf_optional.json`.

The current lazy/half-phase branch passed the same complete SG87
marked-lift comparison, with mod-two classification contractions enabled: task `20260927T011014-closed-cf-half-marked-sg87-458d9ae3`, immutable
source `91c3e193efcb02e1e748b4db7a527e51250f05ca737a8bcadc18c2eee2477ee7`.
It completed in 209.975 seconds. Both native phase seeds, complete obstruction
support, and all 2,690 phase support values for each of the two generators
agreed exactly. Evidence is in
`docs/validation_runs/closed_cf_half_phase.json`. The test evaluates the old
path before the new path in one context, so its timing comparison is not an
independent-process production benchmark.
