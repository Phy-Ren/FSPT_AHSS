# Term census data and verification

Read the [counting conventions and tables](../TERM_COUNTS.md) before
comparing numbers. Nested cup expressions, fully flattened MS words,
scalar face monomials, and raw indexed occurrences are different metrics.
The primary reader count preserves fully defined lower differentials and
stacking twisters, standard operations and the defined integral quadratic
cochain.
Substituting their lower equations is a supplementary verification, not a
requirement for understanding or using the higher formula.

The current 4+1D Majorana twister has **624 explicit expression leaves**
and **482 outer addends**. The difference comes from four separate
canonical lifts with 5, 15, 10 and 116 interior products: 624 = 482 − 4 + 146.
These products remain inside the nonlinear lifts; they are not separate
quarter-valued phase addends. The ledger records both boundaries. Its
complete E5 total of **8,555,388** uses this 624-leaf entry and the declared
boundaries of the other contributions; replacing that entry by its outer
count instead gives **8,555,246**.

- [Structured count ledger](STRUCTURED_TERM_COUNTS.json): displayed terms
  with the defined lower differentials, stacking twisters and integer
  carries retained, including all explicit finite-sum and lift-interior counts.
- [Archived supplementary lower-layer expansions](LOWER_TERM_COUNTS.json): every 2+1D law and the lower
  3+1D/4+1D laws, with separate ordinary-derivative and tower-expanded counts.
- [Archived 3+1D terminal expansions](three_dimensional/INDEX.json): twelve files containing
  the actual retained MS words, physical input alphabets and degrees,
  reference scalar polynomials, and the separate integer and face terms.
- [Archived 4+1D substituted source terms](four_dimensional/SOURCE_SUBSTITUTED_TERMS.json):
  the explicit source operations and protected integer expressions in the
  six physical contributions, with total 628,789 at this supplementary boundary.
- [Complete 4+1D pure-source polynomial](../FOUR_DIMENSIONAL_Y6_FACES.md):
  623,880 distinct physical face monomials, with every coefficient supplied.
- [Current 4+1D Majorana stacking formula](../FOUR_DIMENSIONAL.md#majorana-decoration-1):
  624 explicit leaves in 482 outer addends, with every protected interior
  product in the [canonical-lift table](../FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.md).
- [Archived 4+1D Majorana expansions](../FOUR_DIMENSIONAL_MAJORANA_STACKING_FACES.md):
  the previous 6,176-term expression with standard differential inputs,
  plus its replayable 87,189-term lower-equation substitution. The current
  formula is an exact rewriting of the former, with no additional gauge.
- [Historical 4+1D execution census](four_dimensional/FOUR_DIMENSIONAL_CENSUS.json):
  raw occurrences in an earlier construction. These are not final formula
  term counts and do not replace the explicit coefficient lists above.
- [Historical 4+1D construction data](four_dimensional/FOUR_DIMENSIONAL_COUNT_DATA.json):
  the kernel weights, tensor weights, and visible contributions used by
  the finite-index recurrence.

From the repository root, run:

```sh
python docs/formulas/term_census/three_dimensional/verify_manifests.py
python docs/formulas/term_census/four_dimensional/derive_four_dimensional_weights.py
python docs/formulas/term_census/four_dimensional/derive_four_dimensional_weights.py --current
python docs/formulas/term_census/four_dimensional/replay_four_dimensional_census.py
python docs/formulas/coefficients/verify_majorana_carry_reduction.py
```

All scripts use only the Python standard library. The first independently
expands every retained MS word and checks the entire binary scalar polynomial
against its recorded unreduced target, for all twelve contributions.
It does not re-derive the integer carry expressions or pure face tables.
The historical 4+1D weight script derives every kernel weight from the literal
formulas and complete local coefficient data, for both the baseline and
current formulas. The census replay independently recomputes the finite
construction multiplicities from those verified weights. These reproduce
the historical execution census, not the current reader-facing counts.
The last script compares the current signed-carry expression with the
archived 5,707-term Majorana face polynomial, preserving its four separate
canonical lifts. It is an input replay of the cochain identity, not a
replacement for its algebraic derivation. None of these checks is a
cobordism comparison or a new physical calibration.

The term alphabets use physical expressions. They are data indices for
replaying a coefficient list, not additional notation in the reader formulas.
Canonical lift and exact-division boundaries are part of the recorded
expressions and must be preserved.
