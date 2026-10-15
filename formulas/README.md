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
- [Computed 4+1D cyclic examples](../docs/formulas/FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md).

The TeX source, coefficient appendices, frozen regression vectors, and
universal certificates in this directory preserve the supplied calibrated
input and its proofs. They are evidence for the current formulas, not
alternative runtime conventions. The CI archive is pinned in
[provenance.json](provenance.json), and the reviewed E8 supplement is pinned
in [e8_provenance.json](e8_provenance.json). The fixed convention remains
sheet-linear, cubic coefficient `1/6`, and additional coefficient
`epsilon=0`. Source, product, and gauge coordinates are changed together.

The [research record](../docs/e8/research/README.md) separates mathematical
cochain identities, completed global computations, and the remaining
physical comparison. No external checkout is a runtime dependency.
