# Term census data and verification

Read the [counting conventions and tables](../TERM_COUNTS.md) before
comparing numbers. Counts are uncollected displayed expression
occurrences. Every finite word sum, scalar face sum, and evaluation of
the fixed terminal phase map is expanded; the complete lower output
cochains, standard operations, and protected integer lifts retain their
stated scopes. These are not minimal cochain normal forms.

The 4+1D source has **460,594 terms**. Its Majorana contribution
has **16**, its mixed Majorana–p+ip contribution **1,907**, and its pure
p+ip contribution **458,653**. The paired product has
**8,555,644 expression occurrences**, including **760 Majorana leaves**
in **618 outer addends**. Replacing that one lift-interior count by its
outer count gives **8,555,502**. The four protected lift interiors
contain 5, 15, 10, and 116 products.

The phase map with zero complex-fermion argument has 44 half-valued
terms and one quarter-valued term. The displayed general formulas use
three, three, and one such evaluations in the Majorana, mixed, and pure
p+ip contributions. Each contribution also has one additional lower
stacking term. The exact additions are therefore **136, 136, and 46**
at this counting boundary, before collecting across evaluations.
The full self-stack has **4,407,643 outer occurrences**; expanding the
four Majorana lift interiors in the count gives **4,407,745**.

- [Structured ledger](STRUCTURED_TERM_COUNTS.json) records every
  physical contribution, the phase-map costs, exact totals,
  protected interiors, and source hashes. The shared X5 has four words;
  the pure Majorana O5 has 15 terms.
- [3+1D term manifests](three_dimensional/INDEX.json) list the actual
  word lists, integer and face terms, and the retained representative
  choices of the word-index pages.
- [Pure-source polynomial](../FOUR_DIMENSIONAL_Y6_FACES.md)
  contains 458,647 physical face monomials, unchanged by the phase map.
- [Majorana carry data](../FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.md)
  specify every protected lift product. The carry-reduced coefficient
  part and the fixed paired transport are both included in these counts.

From the repository root:

```sh
python docs/formulas/term_census/verify_structured_counts.py
python docs/formulas/term_census/three_dimensional/verify_manifests.py
python docs/formulas/coefficients/verify_majorana_carry_reduction.py
```

The first checks the arithmetic, shared operation sizes, phase-map
occurrences, and exact maintained source hashes. The others verify the
3+1D manifests and the Majorana carry reduction. The
[phase transport proof](../FOUR_DIMENSIONAL_MAJORANA_PHASE.md)
relates the complete source and product; these counting checks add no
new physical-calibration claim.
