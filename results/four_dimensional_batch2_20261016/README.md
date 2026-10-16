# Expanded cyclic and translation calculations in 4+1D

This accepted batch contains **27 newly computed symmetry inputs**: 23 finite
cyclic groups and four infinite translation groups. It extends the
[first 18 accepted inputs](../four_dimensional_20261016/accepted.json) by a
SHA256-pinned link; earlier raw calculations are not copied or changed.

The computed lower data are `(e2,n2,n4,nu5)`, with E8 included. The uniform
response pair `(n0I,n0J)` is separate. These backgrounds have
`s=rho=omega=0` and no rotations, so a crystalline spinless/spin-half label
would not distinguish two inputs.

## Reader tables

- [Cyclic groups, uniform pair zero](../current/4p1d/internal_cyclic/intrinsic_zero.md).
- [Cyclic groups, all uniform responses](../current/4p1d/internal_cyclic/intrinsic_all.md).
- [Translations, uniform pair zero](../current/4p1d/translations/intrinsic_zero.md).
- [Translations, all uniform responses](../current/4p1d/translations/intrinsic_all.md).

The new cyclic orders are
`11,13,14,17,19,20,21,22,23,24,25,26,27,28,29,30,31,32,36,40,48,54,64`.
Together with the earlier batch this covers every order 1 through 32 and
orders 36, 40, 48, 54 and 64. Each calculation retains completed sheet and
charge roots, their powers, actual gauge corrections and the integer relation
matrix. The independent exact eta pairing reproduces the entire relation
kernel in every case. Bahri–Gilkey's 1987 theorem provides an additional
published comparison for the cyclic 2-groups; it is a separate source column.

Translations use the finite simplicial model `(Delta[1]/boundary)^r` of the
**full** classifying space `B Z^r`, for ranks 1 through 4. This is not a finite
quotient of the infinite group. The charge correction in the stacking law is
retained:

```
(e,n,q) + (f,m,t) = (e+f, n+m, q+t+n wedge m).
```

The integral coordinate `Q=q-n wedge n/2` straightens this law. The actual
ordered cup products, all integral cycle/gauge decompositions and primitive
periods are saved and independently replayed. Degrees 5 and 6 are absent in
this complete model, which explains the vanishing phase row and terminal
obstruction for these translation examples. It is not an assumed general
vanishing differential.

| Translation rank in four spatial dimensions | Uniform pair zero | All uniform responses |
|---|---|---|
| 1 | 0 | Z² |
| 2 | Z² | Z⁴ |
| 3 | Z⁶ | Z⁸ |
| 4 | Z¹³ | Z¹⁵ |

The rank-four charge generator is atomic filling per cell and is retained.
Ranks below four describe partial translation symmetry in four dimensions.
Independent stable torus splitting with the interacting Spin-c coefficient
groups gives every row above. The natural trivial-action section supplies
the two uniform roots. This is an explicit physical section, not a general
intrinsic cochain solver.

See the [translation construction](../../docs/4p1d/calibration/TRANSLATIONS.md)
and [independent primary-source derivations](../../docs/4p1d/calibration/BATCH2_TARGETS.md).
The latter also contains prospective targets; only accepted records count
as computed examples. Interacting bordism targets are kept separate from
the classifier, and no free-fermion classification is used.

## Acceptance and provenance

- [Accepted records and inherited-batch hash](accepted.json).
- [Case acceptance checks](validation.json) and [pinned reference ledger](reference_targets.json).
- [Cyclic campaign](raw/cyclic/campaign.json) and [translation campaign](raw/translations/campaign.json).
- [Cyclic source snapshot](cyclic_source_snapshot.tar.gz) and
  [translation source snapshot](translations_source_snapshot.tar.gz).
- [Every source-manifest entry checked against the snapshots](source_snapshot_verification.json).
- [Cluster translation tests](verification/translations_tests.log),
  [runtime](verification/translations_runtime.json), and
  [transport verification](verification/translations_transport_verification.json).
- [Performance measurements](performance.json) and [scope of the timings](PERFORMANCE.md).

Acceptance checks complete selected coverage, input/source/evidence hashes,
independent Smith reduction, exact cyclic physical kernels, and replay of the
translation certificates. Inherited batches are independently hash-checked.
No classification is altered to agree with a reference.

## Reproduction

Use an immutable source snapshot on a compute node. The cyclic selection is
recorded in `raw/cyclic/selection.json`.

```sh
python3 scripts/classify_cyclic_4p1.py --order 11 --order 13 --jobs 8 --evidence-format json-gzip --output NEW_CYCLIC
python3 scripts/classify_translation_4p1.py --output NEW_TRANSLATIONS
```

Append each remaining selected cyclic order as another `--order`. Accept a
complete new campaign, then build the current tables:

```sh
python3 scripts/collect_calibrated_4p1d.py --cyclic NEW_CYCLIC --translations NEW_TRANSLATIONS --ledger docs/4p1d/calibration/batch2_targets.json --extends results/four_dimensional_20261016/accepted.json --output results/NEW_ACCEPTED
python3 scripts/build_current_tables.py --four-dimensional results/NEW_ACCEPTED/accepted.json
python3 scripts/build_current_tables.py --check
```
