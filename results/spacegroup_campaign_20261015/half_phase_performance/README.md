# Certified half-phase performance evidence

Date: 2026-10-15 UTC. This package preserves isolated local controls and exact comparisons for the generic half-valued phase transfer and lazy normalized cup-one evaluator reused from main commit `0864495b90297d3e1a0747b77aae17980f6d1f3f`. No superconducting formula engine is loaded. The production F/G snapshots and their running results were not modified.

The implementation domain and proof are in [proof.md](proof.md). The final proposed files are preserved in [final_overlay](final_overlay/manifest.json), with the exact [patch](final.patch). The full-run source before the final literal-zero refinement is separately preserved in [candidate_v1_overlay](candidate_v1_overlay/manifest.json). Both overlays are relative to insulator G commit `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`.

## Measurements and exact agreement

| Spin-half workload | G baseline | Candidate | Scope |
|---|---:|---:|---|
| SG141 initial charge completion, fixed Koszul resolution | 60.853 CPU s | 20.573 CPU s | Five completed charge roots; observed 2.96× stage ratio |
| SG229 initial charge completion, fixed Koszul resolution | 74.107 CPU s | 21.351 CPU s | Six completed charge roots; observed 3.47× stage ratio |
| Full SG221 classification | 234.922 wall s | 224.534 wall s | Observed 1.046× whole-run ratio; modest change |

For both charge-stage controls, all lower differentials, cohomology generators, obstruction maps, kernel matrices, native source/primitive vectors and completed native root records agree literally. Only timing fields were excluded. The completed source and its chosen full integral homotopy correction remain intact; no gauge or stacking computation is inferred from graded pieces.

The full SG221 comparison covers all 38 classification fields: 37 are literally identical, and only `resolutionBuildTimings` differs. This includes the full presentation, every completed root/gauge witness, primitive filling and operation statistics. The roughly threefold gains apply to the measured initial charge stages. The full example shows only a modest improvement; neither measurement supplies a universal campaign speed factor or a reason to replace active immutable runs.

Raw stage records are under `spacegroup_141_spin_half_koszul/` and `spacegroup_229_spin_half_koszul/`. Their unmodified reference runs are under [baseline_lattice](baseline_lattice/README.md). Full raw input, output, logs and source/runtime manifests are under [full_sg221](full_sg221/source.json) and [baseline_full_sg221](baseline_full_sg221/source.json). [comparison.json](comparison.json) and [full_comparison.json](full_comparison.json) record exact comparisons; their original absolute paths are retained as provenance.

## Domain tests and review

The controls include 98,304 exhaustive normalized nonabelian source comparisons with negative integer values, 32 signed native/Smith transfer comparisons, 42 exact solves and 1,005 complete primitive-value comparisons. Two controls have quarter-valued primitives. The existing closed-source suite adds 9,664 pointwise comparisons, literal-even zero checks, stale-context guards and nonclosed rejection. The new tests also reject non-half-valued inputs and preserve exact `U1Zero` primitive identity.

The full-run candidate originally returned a memoized zero primitive for a literal zero source. The final overlay restores the original `U1SolveData` fast path, as requested during independent review. This changes no nonzero-source calculation; the final focused primitive and literal-identity tests pass. The full run uses the archived version-one overlay; it is not mislabeled as a rerun after that refinement. [peer_review.json](peer_review.json) records the bounded independent mathematical review, distinct from the author's executable tests.

The separate HAP/Koszul controls found no general resolution advantage. SG141's HAP basis happens to contain two literally even charge roots, so two source completions finish immediately; its first nonzero primitive cost is nearly identical. SG229 gives essentially equal completion times. No resolution or charge-basis switch is included.

## Reproduction

Run the offline package audit from any working directory:

```sh
python results/spacegroup_campaign_20261015/half_phase_performance/check_evidence.py
```

It verifies every package hash, independently checks the saved integer/phase equations and initial charge-kernel Smith groups, compares all full classification fields, verifies source-manifest identities, and checks the full presentation and filling relations.

To repeat one bounded local stage against an explicit checkout, use a fresh output directory:

```sh
python results/spacegroup_campaign_20261015/half_phase_performance/reproduce_control.py \
  --source /absolute/path/to/insulator-checkout --group 141 --variant half \
  --output /absolute/path/new-control
```

Use `--variant baseline` with a checkout of G commit `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`. Baseline lattice selection accepts `--lattice koszul` or `--lattice hap`. The reproducer copies only the required GAP source and exact input into a new local snapshot and retains hashes; each setup, primary and completion stage has a 120-second default bound. It neither connects to a cluster nor modifies the source checkout. The original raw drivers and launch scripts are also preserved.

For a complete rerun, use the normal classifier on a fresh output directory with `--case spacegroup_221_spin_half --charge-primary native --phase-class cycles --closed-charge-source certified`. Pin the source commit/overlay and optional VM exactly as the saved manifests specify. Full source trees and compiled executables are omitted from this small package; source hashes, changed source files, VM identity, exact scientific outputs and raw timing evidence remain available.
