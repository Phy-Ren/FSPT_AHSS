# Term census data and verification

Read the [counting conventions and tables](../TERM_COUNTS.md) before
comparing numbers. Nested cup expressions, fully flattened MS words,
scalar face monomials, and raw indexed occurrences are different metrics.

- [Lower layers](LOWER_TERM_COUNTS.json): every 2+1D law and the lower
  3+1D/4+1D laws, with separate ordinary-derivative and tower-expanded counts.
- [3+1D terminal index](three_dimensional/INDEX.json): twelve files containing
  the actual retained MS words, physical input alphabets and degrees,
  reference scalar polynomials, and the separate integer and face terms.
- [4+1D terminal census](four_dimensional/FOUR_DIMENSIONAL_CENSUS.json):
  exact raw occurrence counts, including the full source completion and
  finite path kernels. The remaining fully collected scalar totals are
  explicitly unspecified.
- [4+1D counting data](four_dimensional/FOUR_DIMENSIONAL_COUNT_DATA.json):
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
The 4+1D weight script derives every kernel weight from the literal
formulas and complete local coefficient data, for both the baseline and
current formulas. The final script independently recomputes the finite
path multiplicities and terminal totals from those verified weights.
Neither check is a cobordism comparison or a new physical calibration.

The term alphabets use physical expressions. They are data indices for
replaying a coefficient list, not additional notation in the reader formulas.
Canonical lift and exact-division boundaries are part of the recorded
expressions and must be preserved.
