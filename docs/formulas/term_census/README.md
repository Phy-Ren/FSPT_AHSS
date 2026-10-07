# Term census data and verification

Read the [counting conventions and tables](../TERM_COUNTS.md) before
comparing numbers. Nested cup expressions, fully flattened MS words,
scalar face monomials, and raw indexed occurrences are different metrics.
The primary reader count preserves fully defined lower differentials and
stacking twisters.
Substituting their lower equations is a supplementary verification, not a
requirement for understanding or using the higher formula.

- [Structured count ledger](STRUCTURED_TERM_COUNTS.json): displayed terms
  with the defined lower differentials, stacking twisters and integer
  carries retained, including all explicit finite-sum and lift-interior counts.
- [Supplementary lower-layer expansions](LOWER_TERM_COUNTS.json): every 2+1D law and the lower
  3+1D/4+1D laws, with separate ordinary-derivative and tower-expanded counts.
- [3+1D terminal index](three_dimensional/INDEX.json): twelve files containing
  the actual retained MS words, physical input alphabets and degrees,
  reference scalar polynomials, and the separate integer and face terms.
- [4+1D substituted source terms](four_dimensional/SOURCE_SUBSTITUTED_TERMS.json):
  the explicit source operations and protected integer expressions in the
  six physical contributions, with total 628,789 at this supplementary boundary.
- [Complete 4+1D pure-source polynomial](../FOUR_DIMENSIONAL_Y6_FACES.md):
  623,880 distinct physical face monomials, with every coefficient supplied.
- [Complete 4+1D Majorana stacking contribution](../FOUR_DIMENSIONAL_MAJORANA_STACKING_FACES.md):
  6,176 terms with standard differential inputs, plus the independently
  replayable 87,189-term lower-equation substitution.
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
```

All scripts use only the Python standard library. The first independently
expands every retained MS word and checks the entire binary scalar polynomial
against its recorded unreduced target, for all twelve contributions.
It does not re-derive the integer carry expressions or pure face tables.
The historical 4+1D weight script derives every kernel weight from the literal
formulas and complete local coefficient data, for both the baseline and
current formulas. The final script independently recomputes the finite
construction multiplicities from those verified weights. These reproduce
the historical execution census, not the current reader-facing counts.
Neither check is a cobordism comparison or a new physical calibration.

The term alphabets use physical expressions. They are data indices for
replaying a coefficient list, not additional notation in the reader formulas.
Canonical lift and exact-division boundaries are part of the recorded
expressions and must be preserved.
