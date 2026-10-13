# Completed insulator campaigns — 2026-10-13

All requested campaigns completed on `n01.local`, reached through the persistent
`cluster3` SSH connection: **172 successful classifications, zero failed cases**.
The implementation and all evidence belong to the independent `insulator` branch.

The [59-group table](summary_20261013/summary.md) displays both physical spin
conventions. The [CSV](summary_20261013/summary.csv) also retains the full uniform
IQH groups. Detailed [2D](two_dimensional_20261013/README.md) and
[3D](three_dimensional_20261013/README.md) reports link numerical comparisons to
source provenance; raw inputs, logs and presentations are in [evidence](evidence/README.md).

## Coverage and execution

| Campaign | Groups | Physical spins | Completed calculations |
| --- | --- | --- | --- |
| 2+1D point groups, uniform IQH fixed to zero | 10 | Both | 20 |
| 2+1D full affine wallpaper groups, uniform IQH fixed to zero | 17 | Both | 34 |
| 2+1D point groups, uniform IQH obstruction and lift included | 10 | Both | 20 |
| 2+1D full affine wallpaper groups, uniform IQH obstruction and lift included | 17 | Both | 34 |
| 3+1D point groups | 32 | Both | 64 |

The original relative and full-IQH-derived relative answers agree in all 54
two-dimensional cases, including the final charge and phase subquotients.
See the [independent-run checks](two_dimensional_20261013/independent_run_crosscheck.json).
Uniform IQH multiplicity is one for the five orientation-preserving planar
point groups and five orientation-preserving wallpaper groups, for both spins;
it is forbidden for the other groups. These conclusions come from completed
sheet lifts, not from appending a free factor to a relative answer.

Each campaign used four GAP workers, at most 12 GB of GAP workspace per worker,
and a 7,200-second per-case timeout. The original and full-IQH campaigns briefly
overlapped, for at most eight workers. Source snapshots `23f9d9c` and `cd8b24d`
were immutable. The longest case, spin-half D6h, completed in 757.131 seconds.

## Formula implementation and validation

The supplied calibrated v0.7 tower is implemented in exact integer and rational
arithmetic: charge-to-phase, CI-to-charge and completed CI-to-phase obstruction
representatives; integer stacking correction and phase twister; joint and short
charge gauges; background transport where supplied; complete inverses and powers.
Local formulas cover 2+1D, 3+1D and 4+1D. The global solver currently covers
2+1D and 3+1D. See [formula coverage](../formulas/README.md) and
[the classification procedure](../docs/computation.md).

The [recorded 47-test run](validation/unittest.log) passed. It includes universal
coefficient certificates, signed and nonabelian cochain identities, independent
background actions, exact root extensions, affine wallpaper controls, source
comparison safeguards, and report completeness checks. Additional discrepancy
audits have their own recorded evidence and regression tests.

The computed sector contains CI-generated, localized-charge and
group-cohomological phase data. **Independent neutral E8 and intrinsic
higher-response sectors are not implemented.** This report does not claim a
complete classification beyond that tower, nor a global 4+1D calculation.

## Two-dimensional comparisons

All **34 wallpaper cases** agree with the primary-source final stacking group,
final charge layer and final phase layer: 102 matching checks. The comparison
uses the computed `n0=0` subgroup of the full IQH presentation.

For planar point groups, 14 of 20 cases match the printed primary table.
The six remaining entries are C2, C4 and C6, for both spins:

| Group | Computed relative group, either spin | Printed primary table |
| --- | --- | --- |
| C2 | Z4 | Z2 x Z2 |
| C4 | Z2 x Z8 | Z4 x Z4 |
| C6 | Z3 x Z12 | Z6 x Z6 |

An independent interacting reduction of rotation-protected band phases gives
the same nontrivial extension as the computation. All ten cyclic rotation
controls agree. That control concerns band-generated phases and does not prove
the absence of additional interaction-only roots. The six printed discrepancies
remain explicit. See [source and version audits](../benchmarks/point2_discrepancy.md).

Wallpaper charge is also restricted to a primitive translation cell. For
example, pg, pmg, pgg and p4g have charge-root filling step two for both spins.
The source's decoration coordinates have not been mapped to that physical
normalization. Accordingly, all 34 filling comparisons remain marked
`requires_source_coordinate_map`; abstract `Z` does not specify a filling step.

## Three-dimensional comparisons

There are **51 matching abstract group comparisons and 13 discrepancies**:
20 matches and two discrepancies among 22 proper-point-group cases; 31 matches
and 11 discrepancies among 42 improper-point-group cases. For the latter, the
reference group is the quotient by the neutral order-two E8 generator explicitly
named in each source root list. This is a documented reference-side abstract
quotient, **not a constructed cochain map from the full physical classification**.
The separate comparison against each full source group remains `scope_mismatch`.

| Group | Physical spin | Computed sector | Reference in compared scope |
| --- | --- | --- | --- |
| D2 | Spin-half | Z2^2 | Z2^3 |
| S4 | Both | Z2 x Z4 | Z2^3 |
| D2d | Spinless | Z2^3 | Z2^2 x Z4 |
| D2d | Spin-half | Z2^2 x Z8 | Z2^4 x Z8 |
| C3i (S6) | Both | Z8 | Z2 x Z4 |
| D3d | Spinless | Z4 x Z8 | Z2 x Z4 |
| D3d | Spin-half | Z4 x Z8 | Z2^2 x Z8 |
| D6 | Spin-half | Z2^2 | Z2^3 |
| D3h | Spinless | Z2^3 | Z2^4 |
| D3h | Spin-half | Z4 x Z8 | Z2^2 x Z4 x Z8 |
| Oh | Spinless | Z2^4 x Z4 | Z2^3 x Z4 |

Several differences have checks independent of the classification run:

- D2 spin-half has a nonzero charge obstruction, proved by an explicit
  Steenrod/Bockstein calculation. The source's named odd-charge center root also
  conflicts with a one-dimensional physical spin-half representation of D2.
- For S4, explicit normalized cyclic cochains and three gauge paths give
  `2x=b`, with nonzero order-two phase root `b`. This forces the order-four
  extension. For C3i, a split parity projection preserves an order-eight root.
  See [the cyclic certificates](../docs/cyclic_root_audits.md).
- Normal-C3 quotients and exact background gauges relate D3d to C2h, D6 to D2,
  and D3h to C2v. Their cohomology and stacking controls support the computed
  groups. See [the backend derivations](../gap/BACKEND.md).
- D2d has explicit obstruction, proper-D2 restriction and charge-gauge checks.
  The two supplied gauge representatives give identical cohomology classes.
  Its remaining physical root and adjoining-equivalence comparison is unresolved.
- For spinless Oh, the source's explicitly printed center relations have Smith
  quotient `Z4 x Z2`, whereas its next sentence claims `Z4`. This provides a
  source-internal arithmetic discrepancy consistent with an extra factor, but
  does not exclude additional unlisted physical relations. Its 1D-layer count
  also differs between the discussion and table. See the
  [independent final review](../benchmarks/final_point3_review_20261013.md).
  A [saved-witness audit](audits/Oh_spinless_saved_witnesses.json) verifies 15
  native equations and the incoming quotient. Its entire surviving phase group
  injects into the independently computed D4h phase quotient. These checks give
  no evidence of a spurious Oh-only phase, without identifying its physical root.

The [discrepancy discussion](../benchmarks/point3_discrepancies.md) distinguishes
exact cochain identities, literal source inconsistencies, and conditional
physical interpretations. No runtime result was changed to fit a reference
table. Matching abstract groups do not by themselves identify physical roots.

## Remaining research questions

The next scientific step is to construct explicit maps between the cochain
generators and the real-space block generators, beginning with D2d and the
discrepant cubic case. Atomic representation induction alone does not establish
an allowed physical bubble: inverse-paired creation and the adjoining path must
be exhibited. Wallpaper decoration coordinates likewise need an explicit map
to primitive-cell charge. An independent neutral E8 module would extend the
implemented tower; it cannot be supplied by silently adding or removing factors.
