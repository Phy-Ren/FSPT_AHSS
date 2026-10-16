# U(1)^f formulas and computed examples

Start with the [current formula guide](../docs/FORMULA_GUIDE.md). It uses
the state order **E8, CI, charge, shared phase** and separates the three
spacetime dimensions.

- [2+1D equations](../docs/formulas/TWO_DIMENSIONAL.md).
- [3+1D equations](../docs/formulas/THREE_DIMENSIONAL.md).
- [4+1D equations](../docs/formulas/FOUR_DIMENSIONAL.md).
- [Operations](../docs/formulas/OPERATIONS.md),
  [exact coefficients](../docs/formulas/COEFFICIENTS.md), and
  [root-power presentations](../docs/formulas/ROOT_POWER_PRESENTATIONS.md).
- [Executable API and worker](../docs/formulas/IMPLEMENTATION.md).
- [Computed 4+1D cyclic examples](../docs/formulas/FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md),
  including the complete physical relation kernel and the uniform response section.
- [Finite abelian products](../docs/4p1d/calibration/ABELIAN_PRODUCTS.md), including
  mixed cohomology, incoming gauges, and complete stacking presentations.
- [Infinite translations](../docs/4p1d/calibration/TRANSLATIONS.md), including
  the full integer cochain/gauge quotient and integral stacking coordinates.
- [Signed C2 calculations](../docs/4p1d/calibration/SIGNED_C2.md) and
  [independent interacting bordism targets](../docs/4p1d/calibration/BORDISM_TARGETS.md).
- [Additional finite-group and translation benchmarks](../docs/4p1d/calibration/BATCH2_TARGETS.md).

The TeX source, coefficient appendices, frozen regression vectors, and
universal certificates in this directory preserve the supplied calibrated
input and its proofs. They are evidence for the current formulas, not
alternative runtime conventions. The CI archive is pinned in
[provenance.json](provenance.json), and the reviewed E8 supplement is pinned
in [e8_provenance.json](e8_provenance.json). The fixed convention remains
sheet-linear, cubic coefficient `1/6`, and additional coefficient
`epsilon=0`. Source, product, and gauge coordinates are changed together.

The [v0.15 provenance](v015_provenance.json) pins the reviewed intrinsic
pair `(n0I,n0J)` and physical cyclic calibration. The retained
[reference extracts](v015_reference/) support those arguments; they do
not replace the active reduced source/product/gauge convention.

Current 4+1D tables separate [cyclic intrinsic-zero](../results/current/4p1d/internal_cyclic/intrinsic_zero.md),
[cyclic all-intrinsic](../results/current/4p1d/internal_cyclic/intrinsic_all.md),
[abelian intrinsic-zero](../results/current/4p1d/internal_abelian/intrinsic_zero.md),
[abelian all-intrinsic](../results/current/4p1d/internal_abelian/intrinsic_all.md),
[translation intrinsic-zero](../results/current/4p1d/translations/intrinsic_zero.md),
[translation all-intrinsic](../results/current/4p1d/translations/intrinsic_all.md),
[unitary charge conjugation](../results/current/4p1d/charge_conjugation.md),
and [AI/AII intrinsic-zero](../results/current/4p1d/time_reversal_intrinsic_zero.md).
The [current index](../results/current/4p1d/README.md) links every accepted
batch and derives its counts from that lineage. The cyclic physical
comparison checks the entire relation lattice; abelian and signed
comparisons use source-specific interacting bordism targets, and
translations use the stable torus splitting. The all-intrinsic direct-product
results use the explicit trivial-action `Z²` section. These family-specific
checks do not supply a general opened-intrinsic solver or a universal
terminal CI comparison.

The [research record](../docs/e8/research/README.md) separates mathematical
cochain identities, completed global computations, and the remaining
physical comparison. No external checkout is a runtime dependency.
