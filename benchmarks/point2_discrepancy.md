# Even cyclic point-group source audit

Audit date: 2026-10-13. The printed even-rotation entries of
[Zhang et al., arXiv:2012.15657v2](https://arxiv.org/abs/2012.15657v2)
remain inconsistent with an independent rotation-only interacting reduction
and the complete onsite C2 control. The evidence supports a missed stacking
extension in that table. This is our mathematical inference, not an
author-confirmed erratum. The comparator preserves the printed answer and its
`published_source_discrepancy` status.

## What the sources actually establish

| Source and location | Statement | Scope |
| --- | --- | --- |
| 2012.15657v1, supplemental Table `point`, source line 3481 | C_N: Z_N x Z_N for even N, both spins | Claimed interacting nonchiral point-group classification |
| 2012.15657v2, same table, source line 3555 | Same even-cyclic answer | Same declared scope |
| Liu, Vishwanath and Khalaf, [1809.01636v2](https://arxiv.org/abs/1809.01636v2), Table VI, class A; Sec V B | Even N: Z_(2N) x Z_(N/2); odd N: Z_N x Z_N; both rotation spin conventions | Interacting reduction of band-generated phases, without translation |
| Wang et al., [2112.15533](https://arxiv.org/abs/2112.15533), main-text example (1), source line 974 | U(1)^f x C2 has full stacking Z4 | Onsite nonchiral charge/phase sector |

The independent rotation paper explicitly limits Sec V B to the reduction of
noninteracting phases under interactions (`Shift.tex:1114`). It does not by
itself prove completeness against additional interaction-only phases. That
limitation does not reconcile the discrepancy: its surviving root of order
2N cannot be a subgroup of the exponent-N group Z_N x Z_N. Our benchmark JSON
labels the reference as a band-generated-sector control, not a proof that all
possible interacting roots have been enumerated.

The spin-half rotation-only onsite extension can be split by redefining the
rotation generator by a U(1) phase. Thus the onsite C2 example is relevant to
both physical spin conventions after crystalline equivalence. This statement
uses charge conservation and a cyclic rotation group; it is not a license to
remove general projective extensions for groups with mirrors or multiple
generators.

## Direct center-state calculation

The following is an independent elementary reconstruction of the adjoining
relation, using the equivalence operations specified by the sources. It is
comparison evidence, never a runtime input to the cochain solver.

For spinless C_N, label the center state by total integer charge q and angular
momentum k modulo N. A filled generic rotation orbit has N electrons. Rotating
its ordered creation operators produces the fermionic permutation sign
(-1)^(N-1), hence this removable orbit changes (q,k) by (N,N/2) for even N
and by (N,0) for odd N. One must quotient by this single coupled relation.
Charge and angular momentum cannot be trivialized independently.

With generators (q,k), the relation matrix is

```
even N:  [[0, N], [N, N/2]]
odd N:   [[0, N], [N, 0]]
```

Its Smith invariants are (N/2,2N) for even N and (N,N) for odd N. In
particular C2 gives Z4, C4 gives Z2 x Z8, and C6 gives Z3 x Z12.
All have N^2 elements, just as the printed Z_N x Z_N; counting states or
concatenating associated-graded factors would miss the distinction.

For spin-half rotation, R^N=(-1)^F and center angular momentum is shifted by
q/2. Absorbing that shift in an integer angular-momentum coordinate gives
the same removable-orbit relation. This change of coordinates is worked out
explicitly in `Shift.tex:1138`. The result therefore cannot be reconciled by
interchanging spinless and spin-half labels.

## Scope checks

Both real-space discussions retain nontrivial atomic data at the rotation
center and identify generic orbits that can be moved away. Zhang et al.'s
supplement begins with charge and one-dimensional representations at the
center, then moves a symmetry orbit to infinity (`combine_sub.tex:3490-3542`).
Liu et al. implement the same generic-position adjoining operation
(`Shift.tex:1118-1128,1157-1162`). Neither of these point-group tables is a
quotient by every atomic insulator. Taking that latter quotient would erase
the center data from which both tables are constructed; no stated such
quotient explains their difference.

The rotation reference also discusses a separate convention difference for
*translation-invariant* classifications: quotienting general Wyckoff fillings
can change the free filling factor. That warning is explicit at
`Shift.tex:1157-1162` and matters for wallpaper comparisons. It does not apply
to the point-only discrepancy, where translation is absent in both sources.
We consequently do not use its product-over-Wyckoff rule to replace the
separate wallpaper references or their retained free filling classes.

All comparisons here fix the uniform IQH index to zero. Adding a uniform
chiral free summand does not change the order-2N versus order-N discrepancy
within this nonchiral center-state sector. We found no source statement that
the cyclic table is instead an associated-graded answer; its caption claims
the classification and the adjoining calculation is intended to determine
the quotient. A missed extension is the supported interpretation, but the
authors' explanation remains unverified.

## Version and correction audit

[arXiv's submission history](https://arxiv.org/abs/2012.15657) lists v1
(2020-12-31) and v2 (2023-06-20). Explicit v1 source was fetched separately
because the local arxiv CLI normalized a versioned request to its existing
unversioned cache. Both source hashes and relevant exact cells are retained
in `point2_source_version_audit.json`.

The even-cyclic table is unchanged. The spinless D4 worked answer changes
from Z4 to Z8, and the spinless D_(2m) row from Z_(2m) to Z_(4m). The
spin-half even-dihedral row is also refined by the parity of m. The current
[APS supplemental PDF](https://journals.aps.org/prresearch/supplemental/10.1103/PhysRevResearch.4.033081/supplementarysub.pdf),
page 2, Eq (6) and Table I, retains D4=Z4 and spinless D_(2m)=Z_(2m),
while its spin-half row already has the parity cases. Thus the journal
supplement and latest arXiv are not identical versions of this table.

Searches of the article page and primary-source web results for its DOI with
`erratum` and `correction` found no explicit author explanation of the cyclic
entry. This is a bounded search result, not a claim that no correction or
private clarification exists. Do not silently repair the source table or tune
the backend to either printed version.
