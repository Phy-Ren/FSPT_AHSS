# Term census data and verification

Read the [counting conventions and tables](../TERM_COUNTS.md) before
comparing numbers. Current counts are uncollected displayed expression
occurrences. Every finite word sum, scalar face sum, and evaluation of
the fixed terminal phase map is expanded; the complete lower output
cochains, standard operations, and protected integer lifts retain their
stated scopes. These are not minimal cochain normal forms.

The current 4+1D source has **625,821 terms**. Its Majorana contribution
has **16**, its mixed Majorana–p+ip contribution **1,907**, and its pure
p+ip contribution **623,886**. The current paired product has
**8,555,622 expression occurrences**, including **760 Majorana leaves**
in **618 outer addends**. Replacing that one lift-interior count by its
outer count gives **8,555,480**. The four protected lift interiors still
contain 5, 15, 10, and 116 products.

The phase map with zero complex-fermion argument has 44 half-valued
terms and one quarter-valued term. The displayed general formulas use
three, three, and one such evaluations in the Majorana, mixed, and pure
p+ip contributions. Each contribution also has one additional lower
stacking term. The exact additions are therefore **136, 136, and 46**
at this counting boundary, before collecting across evaluations.
The full self-stack has **4,407,636 outer occurrences**; expanding the
four Majorana lift interiors in the count gives **4,407,738**.

- [Current structured ledger](STRUCTURED_TERM_COUNTS.json) records every
  physical contribution, the phase-map costs, exact current totals,
  protected interiors, and source hashes.
- [Archived lower-layer expansions](LOWER_TERM_COUNTS.json) substitute
  the lower equations at a separate boundary.
- [Archived 3+1D terminal expansions](three_dimensional/INDEX.json) retain
  the actual word lists and integer and face terms. The shared X5 has
  four words; the current pure Majorana O5 still has 15 terms.
- [Archived 4+1D source expansion](four_dimensional/SOURCE_SUBSTITUTED_TERMS.json)
  and its 628,789 total describe the preceding phase coordinate.
- [Current pure-source polynomial](../FOUR_DIMENSIONAL_Y6_FACES.md)
  contains 623,880 physical face monomials, unchanged by the phase map.
- [Majorana carry data](../FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.md)
  specify every protected lift product. The carry-reduced coefficient
  part and the fixed paired transport are both included in current counts.
- [Archived Majorana expansions](../FOUR_DIMENSIONAL_MAJORANA_STACKING_FACES.md)
  contain the preceding 6,176-term expression and its 87,189-term
  lower-equation expansion.
- [Historical execution census](four_dimensional/FOUR_DIMENSIONAL_CENSUS.json)
  and [construction weights](four_dimensional/FOUR_DIMENSIONAL_COUNT_DATA.json)
  count an earlier finite construction. Their fields named current refer
  to that archived comparison, not the present reader formulas.

From the repository root:

```sh
python docs/formulas/term_census/verify_structured_counts.py
python docs/formulas/term_census/three_dimensional/verify_manifests.py
python docs/formulas/term_census/four_dimensional/derive_four_dimensional_weights.py
python docs/formulas/term_census/four_dimensional/derive_four_dimensional_weights.py --current
python docs/formulas/term_census/four_dimensional/replay_four_dimensional_census.py
python docs/formulas/coefficients/verify_majorana_carry_reduction.py
```

The first checks the current arithmetic, shared operation sizes, phase-map
occurrences, and exact maintained source hashes. The remaining scripts
verify the declared coefficient and historical comparison data at their
own boundaries. They do not turn a prior phase-coordinate count into a
current one. The [phase transport proof](../FOUR_DIMENSIONAL_MAJORANA_PHASE.md)
relates the complete source and product; these counting checks add no
new physical-calibration claim.
