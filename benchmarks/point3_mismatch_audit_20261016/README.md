# 3+1D interacting point-group mismatch audit

Audit date: **2026-10-16**. Baseline: `f413c19f8dadbc51953b77acadf7457be64fb603`.
This review covers the full E8-inclusive U(1)^f groups in the current catalogue.
It does not change classifier formulas, accepted classifications, or the
values actually printed by the comparison papers.

## Conclusion

Independent bordism recomputations support the current stacking groups for
the cases reviewed here. In particular, all three disagreements with Arun
Debray v3 have specific mathematical explanations on the source side:

- **Physical spin-1/2 D2 and D6:** current Z2^2, printed Z2^3. The degree-four
  polynomial summand in the proof has dimension two, not three.
- **Physical spinless Oh:** current Z4 × Z2^5, printed Z4 × Z2^4. The displayed
  Adams calculation gives ku4; passing to Spin-c bordism requires the additional
  shifted-ku0 summand, which is Z2.

These conclusions use the interacting crystalline/bordism ansatz shared with
the source. Connective ku is a tool for computing that bordism spectrum;
no free-fermion band classification is substituted for the interacting problem.
The audit is our recomputation, **not an author-issued erratum**.

## Separate comparison tables

- **[Spinless point groups](spinless.md)** — six backgrounds in the union of
  mismatches; [machine-readable evidence](spinless.json).
- **[Spin-1/2 point groups](spin_half.md)** — eight backgrounds in that union;
  [machine-readable evidence](spin_half.json).

Each reference keeps its own column and version. A printed mismatch remains
**×** even when this audit supports our value. The columns are not rewritten
to agree with us. E8 is included on both sides. The current Debray comparison
has 37 matches and three mismatches among 40 covered backgrounds; 24 other
backgrounds have no extracted Debray entry. The PRX table has 13 mismatches.
The union across the older arXiv and journal versions has 14 backgrounds.
Ning–Mao–Li–Wang adds no mismatch in its current covered cases.

## Mathematical evidence

| Calculation | Independent result or test | Derivation |
| --- | --- | --- |
| D2 degree count, charge obstruction and D6 odd-kernel reduction | Degree-four Spin-c torsion Z2^2; normalized-bar obstruction independently nonzero | [D2/D6 audit](debray_d2.md) |
| Oh Steenrod module, dual Koszul complex and Spin-c splitting | Missing shifted-ku0 accounts for the exact extra factor; spin-half positive control agrees with the paper | [Oh audit](oh_audit.md) |
| D2d Steenrod module and actual Thom-spectrum retract | Both physical spin cases independently reproduced; relevant differentials and stacking extensions resolved | [D2d bordism audit](d2d_bordism.md) |
| S4 determinant Thom cofiber and Gysin map | Exact cyclic presentation fixes the order-four extension | [S4 Gysin audit](S4_gysin.md) |
| Normal C3 subgroups with exact spatial intertwiners and spin-extension gauges | C3i, D3d, C6h and D3h reduce to independently identified Ci, C2h and C2v anchors, including stacking | [Odd-kernel and reference audit](other_mismatches.md) |

The D2d and S4 calculations are new computations in the cited general bordism
framework; they are not claimed as entries already published by Debray.
The odd-kernel argument checks the actual spatial representation and spin
extension, not just the abstract finite group. Odd-primary and rational pieces
are checked separately. Thus an isomorphism of graded AHSS layers alone is
never used to infer a final extension.

## A correction to our own previous argument

The old printed-relation audit for spinless Oh must not be used to claim an
extra atomic Z2. Its literal twelve-site fermion orbit has a negative
diagonal-reflection sign. Correcting the printed row from `(12,0,0)` to
`(12,0,1)` gives the paper's stated center quotient Z4. The source's printed
rows were inconsistent, but that inconsistency did not prove our physical
classification. The independent bordism calculation above supplies the
stronger evidence. The old note now points to this correction.

The PRX Oh discussion also assigns two Haldane factors in its body but one in
Table II. This is a separate internal inconsistency. We do not infer any
author's motives or the causal origin of an error from agreement of tables.
Debray explicitly acknowledges revisions after comparison with that work;
the final tables therefore should not be treated as blind independent checks.

## Implementation control

All three Debray mismatch cases were freshly recomputed on **n08**, through
the persistent cluster3 SSH connection, from an immutable source snapshot.
The unified workflow ran CI classification, E8 and acceptance, with
`charge-primary=bar`, `closed-charge-source=reference`,
`vacuum-reduction=reference`, and `formula-mode=reference`.

All three passed acceptance in **55.8 seconds**. Their inputs and every full
classification field agree with the current accepted records after removing
only the execution statistics `chargePrimaryStats` and `pairedGeometryReuse`.
No obstruction, generator, relation, Smith invariant, E8 witness or mathematical
classification field was excluded from the comparison.

- [Exact comparison](reference_rerun_comparison.json).
- [Workflow and hashes](reference_run/workflow.json).
- [Accepted records](reference_run/accepted/3p1d/point_groups/results.json).
- [Execution command](run_reference.sh).

This control checks the optimized implementation. The separate polynomial,
Koszul and Gysin calculations check the mathematical answer by different
methods; repeating our own classifier would not provide that independence.

## Scope and reproducibility

The result is evidence for these specific final groups. It does not establish
the universal map from our four-data formulas to the physical spectrum, a
canonical identification of every cochain root with a microscopic construction,
or the correctness of every unreviewed space group. In particular, the added
Oh spectral summand is not automatically a canonical E8 generator in our
coordinates. No neutral factor is counted twice.

The detailed notes give primary-source dates, versions, pages and theorem
numbers. Downloaded papers remain in the research cache; this directory
contains our derivations, exact scripts, results, source hashes and run records.
From the repository root, representative reproducibility commands are:

```bash
python3 benchmarks/point3_mismatch_audit_20261016/d2_polynomial_audit.py
python3 benchmarks/point3_mismatch_audit_20261016/oh_ext_audit.py
python3 benchmarks/point3_mismatch_audit_20261016/oh_atomic_orbits.py
python3 benchmarks/point3_mismatch_audit_20261016/d2d_geometry_audit.py
python3 benchmarks/point3_mismatch_audit_20261016/d2d_ext_audit.py
python3 benchmarks/point3_mismatch_audit_20261016/d2d_peer_oh.py
python3 benchmarks/point3_mismatch_audit_20261016/check_odd_c3_maps.py
python3 benchmarks/point3_mismatch_audit_20261016/S4_gysin.py
python3 benchmarks/point3_mismatch_audit_20261016/build_tables.py
```

Scripts use exact integers, rationals or binary linear algebra. SymPy is needed
for Smith forms and spatial intertwiners. The mathematical scripts do not read
expected classification tables as calculation inputs; only `build_tables.py`
reads those tables to display the comparison.
