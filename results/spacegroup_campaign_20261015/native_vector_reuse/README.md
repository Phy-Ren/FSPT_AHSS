# Exact reuse of immediately checked native vectors

This package retains the isolated comparison against commit
`d3b2dcc6fe9f4ecda3e957d74edae2012ac46198`. The patch changes only two adjacent
uses in `gap/classification.g`; it introduces no cache, new formula, shortened
check, half-source doubling, or q2 mod-two operation. Existing running campaign
snapshots were not changed.

`U1CheckCompletedState(c,d,a)` evaluates the native sheet, charge and phase,
checks their full defining equations and source closure, then returns those
vectors. The patch keeps that call and every check. `U1ReduceVacuum` immediately
uses the returned `nativePhase` for its existing gauge witness; the local
`reduceCharge` immediately uses the returned `nativeCharge` for the existing
cohomology-coordinate calculation. Each replaced statement previously repeated
the same deterministic integral bar transfer. No context, coefficient action,
resolution or callback changes between evaluation and reuse.

The variables are local to these calls. There is no delayed lookup, persisted
certificate or invalidation rule. The reused object is the exact native
cochain, not a cohomology-class substitute or native primitive seed. All phase
callbacks, products, integer gauges, incoming relations, completion checks,
full root witnesses and output structures remain intact.

## Recorded controls

Three focused tests passed in 26.822 seconds. That duration describes the test
run, not a reference/candidate speed comparison.

- **Ten full classifications:** cyclic orders 2, 3 and 4; all four cyclic sign
  pairs; the nonlinear CI root; quarter- and sixteenth-valued phases;
  independently signed V4; and full affine space group 4. Every output field
  agrees except the explicitly excluded resolution construction timings.
  Complete native roots, gauges, primitives, presentations, filtration,
  filling, check counts and worker/cache statistics are retained and equal.
- **Sixteen gauge controls:** four independent sign pairs, negative integer
  parameters, spatial dimensions two and three, and both canonical and
  reference reduction modes. All **864 phase values** and full gauge witnesses
  agree exactly. Each invocation removes precisely one duplicate transfer.
- **Failure control:** the original completed-state equation check still
  rejects an invalid nonclosed one-third phase in both implementations.

Test-only counters record **384 → 352 native transfer calls** across the ten
classifications. For each case the difference equals its number of vacuum
reductions plus charge reductions, as predicted by the two changed sites.
All 32 removed calls used callbacks other than the literal `U1Zero`; this does
not assert that their evaluated cochains or cohomology classes are nonzero.
There is **no measured wall-time speedup claim**.

## Artifacts and verification

`duplicate_native_reuse.patch` is the complete implementation diff, and
`candidate_classification.g` is its exact resulting source. The 72 kB
`evidence.tar.gz` retains 34 original files: the test and invocation, log,
complete reference/candidate outputs, generated GAP drivers, process records,
comparison summaries and the original source manifest. The package does not
duplicate either full checkout. `provenance.json` records compressed and
uncompressed hashes, member hashes and the base-source identity. Original
absolute paths inside the captured artifacts are preserved as evidence.

From any working directory:

```sh
python3 results/spacegroup_campaign_20261015/native_vector_reuse/verify.py \
  --repository /path/to/FSPT_AHSS_insulator
```

The default verifier checks every retained byte, safe archive membership,
all 1,289 base source-file hashes against Git, exact patch reconstruction,
full output equality, predicted call counts, phase values and saved rejection
evidence. It performs no classification. Add `--replay` to reconstruct both
trees in a temporary directory and rerun the three original tests using
installed GAP/HAP and Python; replay uses `U1_DAG_MODE=python` for both trees.
No cluster access is used. The recorded run and default verification are the
evidence for this package; replay is optional.
