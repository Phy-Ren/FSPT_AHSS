# Calibrated 4+1D examples

All **18 selected backgrounds** completed on `n08.local` through the persistent
cluster3 SSH connection. Acceptance checks the selected coverage, input/source
hashes, complete evidence, and independent integer presentations. Comparisons
use the exact symmetry and intrinsic-response sector, after classification.

Current reader tables:

- [14 commuting cyclic groups: intrinsic pair zero](../current/4p1d/internal_cyclic/intrinsic_zero.md).
- [The same groups: all intrinsic responses](../current/4p1d/internal_cyclic/intrinsic_all.md).
- [Two unitary charge-conjugation groups](../current/4p1d/charge_conjugation.md).
- [AI and AII: intrinsic pair zero](../current/4p1d/time_reversal_intrinsic_zero.md).

The lower tuple is `(e2,n2,n4,nu5)`, E8 first. The uniform pair `(n0I,n0J)` is
separate. These are internal symmetries, so crystalline spinless/spin-half
labels do not apply. The 18 backgrounds give 32 response-sector entries.

## What was checked

For cyclic orders `1,2,3,4,5,6,7,8,9,10,12,15,16,18`, the calculation retains
complete root powers, actual sheet/charge gauge corrections, source values,
and all normalized terms of the generating five-cycle. It computes the
integer relation matrix before consulting the physical calibration. The
independent exact eta pairing reproduces the **entire relation lattice**.
The physical identification also uses the Spin-c bordism order bound.
The direct-product trivial-action section supplies the two uniform roots;
this is an explicit physical section, not a general intrinsic formula solver.

For signed C2, the normalized bar complex has one generator in every degree.
The solver retains all completions, incoming gauge actions, ordered products,
and the final quotient table. Results are `Z2` for unitary `C^2=1`, `Z2^3`
for unitary `C^2=(-1)^F`, and zero for both zero-intrinsic time-reversal cases.
The two unitary groups have no invariant intrinsic row. AI/AII full intrinsic
groups are not outputs of this calculation.

Every compared source agrees. External results and project proofs are separate
columns: Bahri–Gilkey (1987) applies to cyclic 2-groups; the stated Smith and
Freed–Hopkins theorems give the specified C2 comparisons; v0.15 supplies the
all-order cyclic physical proof. These are interacting bordism comparisons.
See [reference derivations](../../docs/4p1d/calibration/BORDISM_TARGETS.md),
[validation method](../../docs/4p1d/calibration/VALIDATION_METHOD.md), and
[signed formulas](../../docs/4p1d/calibration/SIGNED_C2.md).

## Evidence and performance

- [Accepted records](accepted.json), [acceptance checks](validation.json),
  and [pinned reference targets](reference_targets.json).
- [Cyclic campaign](raw/cyclic/campaign.json) and
  [signed campaign](raw/signed/campaign.json); their case directories retain
  the exact inputs, full mathematical records, run metadata and source hashes.
- [Cache/reference benchmark](benchmark.json): C3 **0.744347 → 0.313270 s**;
  C6 **5.161713 → 1.492532 s**. All mathematical fields and retained witnesses
  agree literally. These timings cover complete cochain classification,
  excluding the separate physical eta calibration and process/file overhead.
- [Independent GAP controls](native_control.json): six complete cyclic
  presentations agree; twelve native phase-boundary equations were rechecked
  using the actual GAP differential on the compute node.
- [Focused cluster tests](tests.log): 15 tests ran in 84.634 s, 14 passed and
  one GAP-discovery-dependent test was skipped. The separate GAP-native
  control above passed using the explicit optimized executable path.
- [Eight acceptance/table integration tests](collection_tests.log) passed,
  including altered inputs/evidence, incomplete selection, and an AI/AII
  reference swap despite their equal abstract zero-intrinsic groups.
- [Independent peer checks](peer/): 160 HNF checks against SymPy, 20 brute
  finite-character kernels, 13 eta-kernel orders, 64 off-cycle complete-root
  reductions, and 256 signed global pullback/source/gauge checks passed.

The cyclic batch used four processes. Its case execution interval was
13.23 s; C18 was the longest case at 11.41 s. The four signed cases ran
sequentially alongside it in 29.85 s. Runtime: Python 3.13.12 and SymPy 1.14.0
in an isolated environment. The node had 56 CPUs and about 127 GB available
before launch. No general speedup factor is inferred from this small batch.

The immutable [source snapshot](source_snapshot.tar.gz) has SHA256
`b5081fc80e19d68cde585971b6b595350baca8daacf1ad762f47dafc255c9350`.
It preserves the exact calculation code while presentation and acceptance
documentation were finalized separately. The reviewed input archive and
unchanged proof files are pinned in [v0.15 provenance](../../formulas/v015_provenance.json).
Every file in both calculation manifests was checked against that snapshot;
the [snapshot verification](source_snapshot_verification.json) and
[verification artifact hashes](verification_manifest.json) retain the checks.

## Reproduction

Run in an immutable checkout or unpacked source snapshot on a compute node:

```sh
python3 scripts/classify_cyclic_4p1.py --jobs 4 --timeout 600 --output NEW_CYCLIC
python3 scripts/signed_charge_conjugation_4p1.py --output NEW_SIGNED
python3 scripts/benchmark_cyclic_4p1.py --order 3 --order 6 --output NEW_BENCHMARK.json
```

From the repository, accept selected completed runs and rebuild the tables:

```sh
python3 scripts/collect_calibrated_4p1d.py --cyclic NEW_CYCLIC --signed NEW_SIGNED --output results/NEW_ACCEPTED
python3 scripts/build_current_tables.py --four-dimensional results/NEW_ACCEPTED/accepted.json
python3 scripts/build_current_tables.py --check
```

Commuting `C2 x C2` and rank-four translations `Z^4` are computed in the
subsequent accepted batches linked from the
[current 4+1D catalogue](../current/4p1d/README.md#accepted-calculation-lineage).
They are separate from the 18 backgrounds retained in this immutable batch.
