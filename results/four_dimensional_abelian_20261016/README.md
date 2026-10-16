# Finite abelian four-data calculations in 4+1D

This collection accepts **12 completed symmetry inputs** from a 13-input
bounded campaign. Ten are noncyclic groups; the other two,
`C2 × C3 ≅ C6` and `C3 × C4 ≅ C12`, are independent presentations of
previous cyclic controls. The `C4 × C8` attempt timed out after 1800 seconds
and is **not included in the classification tables**.

The [original campaign](raw/abelian/campaign.json) remains marked
`incomplete`. Its full raw directory, including the timeout, is preserved
unchanged. The [explicit completed selection](completed_selections.json)
and [acceptance record](validation.json) identify the included and excluded
inputs and hash the original campaign. No partial result or reference value
is used to fill an unfinished case.

## Current results

- [Uniform pair fixed to zero](../current/4p1d/internal_abelian/intrinsic_zero.md).
- [All uniform responses](../current/4p1d/internal_abelian/intrinsic_all.md).
- [Current 4+1D catalogue](../current/4p1d/README.md).

Every input is the interacting electronic direct product `U(1)^f × G`, with
`s=rho=omega=0`, and has no crystalline spin label. The lower fields are
`(e2,n2,n4,nu5)`, E8 first. The uniform pair `(n0I,n0J)` has separate tables.
The completed product factors are

```
2×2, 2×3, 2×4, 3×3, 2×6, 2×8, 3×6, 4×4,
3×9, 2×2×2, 3×4, 2×10.
```

All 12 final stacking groups agree with the independent interacting Spin-c
bordism targets. The targets are derived from explicit primary theorems,
with their integral/2-local scope distinguished; they are not free-band
classifications. Rank-two and higher elementary-two derivations have
separate source columns. See the
[primary-source derivations](../../docs/4p1d/calibration/BATCH2_TARGETS.md)
and [independent arithmetic replay](../../docs/4p1d/calibration/batch2_reference_replay.json).
The reference ledger also lists future targets and is not a run-completion list.

This is a comparison of additive group types and extensions. It does not
supply a labelled physical character dictionary for all noncyclic roots.
The coprime controls agree in their final groups and filtration signatures;
an explicit CRT matrix transporting their labelled roots has not been
computed. The two uniform generators have a separate natural physical
section obtained by giving them trivial finite-group action. That section
is not a general intrinsic-row formula solver.

## What the examples test

- `C2 × C2`: incoming `H3(G,Z)` removes a genuine order-two phase. The order
  changes from 2048 to 1024, giving `Z2² × Z4 × Z8²`.
- `C2³`: the charge differential has index two, and incoming gauges have
  image order eight. The candidate order `2^26` becomes `2^25` after the
  differential and `2^22` after incoming identifications. The final group is
  `Z2^7 × Z4^3 × Z8^3`.
- `C2 × C4` and `C2 × C8`: `H3` is nonzero but its incoming image is zero.
  The engine computes the image rather than quotienting by the entire
  gauge cohomology group.
- `C3 × C3`: the odd-primary result `Z3^7 × Z9²` tests mixed stacking
  extensions that cannot be found by multiplying final layer groups.
- `C3 × C9`: unequal odd exponents give `Z3^6 × Z9³ × Z27`.

The [formula and completeness argument](../../docs/4p1d/calibration/ABELIAN_PRODUCTS.md)
explains why the full mixed charge kernel, phase cohomology, incoming gauges
and completed roots generate the classification. Every non-phase root pair
has a computed commutator witness in the existing relation lattice.

## Independent acceptance

[The witness verifier](../../scripts/verify_abelian_4p1.py) uses no physical
target group. It checks:

1. Native integer sheet-removal gauges and every charge/phase primitive.
2. Complete root and commutator coverage, including reconstruction of the
   entire final relation matrix from the retained witnesses.
3. Maximality of the charge-obstruction kernel by an independent index
   calculation, in addition to checking that each generator is unobstructed.
4. Incoming-state independence modulo the **pre-incoming** lattice.
5. All four final filtration lattices by saturated integer elimination and
   Hermite normal forms, together with independent final Smith reduction.

The input group and symmetry background are bound to the raw native record.
A hash-pinned inherited collection supplies the earlier cyclic, signed and
translation examples without copying or replacing them.

- [Accepted records](accepted.json) and [acceptance checks](validation.json).
- [Independent witness replay](verification/main_witness_validation.json).
- [Separate physical reference comparison](verification/main_independent_reference_comparison.json).
- [Exact source snapshots](source_snapshots.tar.gz) and
  [source-manifest verification](verification/source_archive_validation.json).
- [Complete mode comparison](verification/native_comparison.json) and
  [independent parity/certificate replay](verification/independent_native_comparison_replay.json).
- [Performance and bounded failures](PERFORMANCE.md).
- [Fifty focused tests](verification/focused_tests.log): all passed with no
  skips, including exact primitives, incomplete-campaign selection,
  pre-quotient incoming checks and derived-source column separation.

## Reproduction

Run a new campaign from an immutable source tree on an idle compute node:

```sh
python3 scripts/classify_abelian_4p1.py --factors 2x2 --factors 2x4 --factors 3x3 --jobs 3 --timeout 1800 --memory 16g --output NEW_ABELIAN
```

Accept a fully completed campaign with `--abelian NEW_ABELIAN`:

```sh
python3 scripts/collect_calibrated_4p1d.py --abelian NEW_ABELIAN --ledger docs/4p1d/calibration/batch2_targets.json --extends results/four_dimensional_batch2_20261016/accepted.json --output results/NEW_ACCEPTED
python3 scripts/build_current_tables.py --four-dimensional results/NEW_ACCEPTED/accepted.json
python3 scripts/build_current_tables.py --check
```

For an incomplete campaign, add `--completed-selections SELECTED.json`, an
explicit mapping from `abelian` to the exact completed IDs. The retained
`completed_selections.json` records this batch's 12-input selection from the
original 13-input campaign. A new file must match the new campaign's actual
inputs; it cannot authorize a failed or absent result. The original campaign
status and all raw failures remain unchanged. Repeat `--abelian`
for separate completed campaigns, labelled `abelian_2`, `abelian_3`, etc.
