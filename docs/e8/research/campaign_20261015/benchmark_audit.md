# Benchmark audit for the 2026-10-15 rerun

This is a campaign planning and source audit, not a new calculation report.
It preserves the immutable 2026-10-13 outputs and the source-specific
2026-10-14 comparisons. Each source/version remains a separate column in the
actual result tables. Physical spins and spacetime dimensions must remain in
separate result files. Only interacting classifications belong in their main
comparison columns; graded layers and restricted diagnostics remain distinct.

## 3+1D: what the new formulas can change

The original run contains 64 finite point-group cases, 32 groups for each
physical spin. Its scope is the CI, localized-charge, and common
cohomological-phase model, without independent neutral E8 decoration.

The current E8-first theory has `(e_1,n_1,n_3,nu_4)`. Its neutral source,
stacking correction, and phase gauge correction vanish in this dimension.
The neutral addition is consequently the explicit model factor `H1(G,Z_s)`:
zero for the 22 proper-rotation cases, and `Z2` for the 42 improper cases.
This is a new sector, not a change to a previously computed CI differential
or stacking twister. The recently proved mixed cubic bridge is 4+1D and does
not modify these 3+1D formulas. The new uniform-response domain guard and
background transport concern 2+1D and do not change valid 3+1D inputs.

Read-only Git comparison from the campaign's named base revision `23f9d9c`
shows no changes to the calibrated CI kernels `calibrated.py`,
`transgression.py`, `product4d.py`, `simplex.py`, or `cochains.py`. The global
GAP code does have subsequent validation, caching/snapshot, witness, filling,
and relative-kernel changes. Therefore the appropriate expectation is
unchanged CI groups, but that is not a substitute for the requested fresh
run. The old run records its actual source digest, which must be retained
alongside the new run digest; a directory's abbreviated revision name alone
is not proof of source-byte identity.

For a new calculation that actually computes the neutral `H1` factor, compare
its full four-data group to full interacting source groups. Also retain the
newly rerun CI-only group and its old-source comparisons. Do not compare a
CI-only result to a full E8-inclusive source and interpret the extra factor
as a failed calculation.

## 3+1D: all historical differences

The arXiv-v2 R3 comparison had 51 equal groups and 13 different groups:
spinless 26/6 and spin-half 25/7. The journal-2025 comparison also had 51/13,
but split as spinless 27/5 and spin-half 24/8. Their union is 14 concrete
cases. Journal D3h spinless becomes equal; journal C6h spin-half becomes
different. The table below preserves both facts.

Here **✓** means the same reported group and **×** a different reported group.
The R3 authors are Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi, and Zheng-Cheng
Gu. Both versions use interacting real-space topological crystals; these are
not bordism calculations. For improper groups, the historical source entry
is its explicitly named independent-E8 quotient. This is a source-side
operation, not an inferred deletion of an arbitrary factor or a constructed
root map to our model.

The historical comparison tables are separated by physical spin:

- [3+1D spinless historical differences](3p1d/spinless/historical_differences.md).
- [3+1D spin-1/2 historical differences](3p1d/spin_half/historical_differences.md).

## 3+1D: valid source columns and E8 content

- **Zhang–Ning–Qi–Gu, arXiv v2 (2024):** [arXiv:2204.13558v2](https://arxiv.org/abs/2204.13558v2), *Construction and classification of crystalline topological superconductor and insulators in three-dimensional interacting fermion systems*, Table II and individual group root lists. Interacting real-space blocks, boundary-gapping constraints, bubble equivalence, and stacking. Covers all 64 cases. Includes named neutral E8 roots for all 42 improper cases. Preserve this as a historical version column.
- **Zhang–Ning–Qi–Gu, journal (2025):** [Physical Review X 15, 031029](https://doi.org/10.1103/PhysRevX.15.031029), main Table II, printed p.031029-5, and the journal supplement's Sec.III root lists. Same construction method, distinct version. Four full-group cells changed from arXiv v2: spin-half D2d and C6h, and both D3h spins. All 42 named E8 roots were reread independently in the journal main/supplementary text; `benchmarks/point3_named_e8_journal_2025.json` records their exact locations and their exclusion from the stated nontrivial extensions. Use the full journal fixture for a new E8-inclusive comparison, not the old quotient fixture.
- **Arun Debray, v3 (2026):** [arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3), *Invertible phases for mixed spatial symmetries and the fermionic crystalline equivalence principle*, Tables 1–6, using Spin-c/Pin-c bordism, Adams spectral sequences, and Anderson-dual phase homology. The pinned Class-A extraction contains 40 of the 64 point-group cases: all 22 proper cases and 18 improper cases. Its `fullPhysical` entries include neutral bosonic contributions. Do not quotient an improper entry by reading an unnamed factor from its invariant factors. With a new full four-data result, compare the full entries directly. The other 24 cells remain unavailable. This is a different mathematical method; v3 acknowledges revisions after comparison with R3, so table agreement is not blind independent replication.
- **Ning–Mao–Li–Wang (2021):** [arXiv:2105.02682v1](https://arxiv.org/abs/2105.02682v1), [Physical Review B 104, 075111](https://doi.org/10.1103/PhysRevB.104.075111), *Anomaly indicators and bulk-boundary correspondences for 3D interacting topological crystalline phases with mirror and continuous symmetries*. Interacting dimensional reduction, folding, and complete anomaly indicators for the specified mirror symmetry. This supplies two Cs cells, one per physical spin. Sec.III.B.1, Eqs.(19)–(20), pp.12–13, and Appendix B.1, Eq.(B4), p.31 identify full `Z2 x Z8`, with the neutral E8 detected by `eta_2f=(-1)^mu1`; its named quotient is `Z8`. Unrelated groups are N/A, not failed comparisons. The mirror results build on earlier work and are not wholly independent of that literature.

The printed Debray spin-half D2/D6 values remain `Z2^3`. The targeted
[grading audit](../../../foundations/debray_d2_grading_audit.md) finds a
source-internal conflict between the proof's count and its cited degree-two
polynomial generators. Its separate derivation yields `Z2^2`. Keep the printed
source cell and this mathematical audit distinct; there is no published
erratum in the pinned fixture, and the source column must not be silently
corrected. The independent ku calculation here is a tool in interacting
bordism, not a substituted free-band classification.

As a **forecast only**, taking the old CI result and the now-specified neutral
model factor gives 37 equal / 3 different groups among Debray's 40 full
entries. The three differences are spin-half D2 and D6 (`Z2^2` versus printed
`Z2^3`) and spinless Oh (`Z2^5 x Z4` versus printed full `Z2^4 x Z4`). The old
Oh CI group happened to equal that full source's abstract group; that was not
a valid sector comparison. The new campaign must calculate and label its
neutral factor before replacing this forecast by an observed comparison.
For R3, adding the same independently named `Z2` to each improper-side
comparison preserves its version-specific 51/13 forecast. These predictions
must never be used as calculation inputs.

## 2+1D: recommended difficult cases

Run the following first diagnostic set for each physical spin separately,
with the all-allowed-`n0` calculation retaining the actual `n0=0` kernel.
Keep `e0=0` and any independently implemented E8-inclusive sector in separate
files. A fixed nonzero `n0` fiber is not a group.

1. `point2_02` C2, `point2_05` C4, `point2_09` C6: six cases across the two spins. They test full root powers and extensions, not just graded-layer cardinalities. The old relative groups were `Z4`, `Z2 x Z8`, and `Z3 x Z12`. Both R2 versions print different even-rotation groups, while the matched Debray interacting relative-sector entries agree with these old calculations. L2 also explicitly gives the internal charge-preserving C2 interacting result `Z4`.
2. `wallpaper_04` pg and `wallpaper_08` pgg: four cases. They retain glide relations and the full translation kernel, rather than replacing the wallpaper group by its point quotient. Check the primitive-cell charge homomorphism and its values on every relation. They have orientation reversal, so physical uniform `n0=e0=0`.
3. `wallpaper_10` p4: two cases. This combines nontrivial relative extensions, translations, and a nonzero uniform IQH direction. It has a separate interacting response-classification benchmark from Manjunath–Calvera–Barkeshli, including the full E8 direction.
4. `wallpaper_12` p4g and `wallpaper_17` p6m: four cases. Their spin conventions give different torsion groups; p4g also tests nonsymmorphic input. Reflection again forces uniform `n0=e0=0`. These are useful checks that the newly explicit uniform-domain restriction removes no valid state.

This is 16 concrete calculations. An optional second set is
`point2_04` C2v, `point2_06` C4v, `point2_10` C6v, both spins (six more cases).
The older R2 journal supplement differs from its later arXiv v2 for their
spinless entries. Extra orientation-preserving wallpaper checks `wallpaper_02`
p2 and `wallpaper_16` p6 would extend the independent chiral-response controls.
All surviving uniform IQH generators in the old 54 crystallographic cases
had multiplicity one; this proposed set therefore does not test an IQH
response image of index greater than one.

## 2+1D: source columns and sector discipline

- **Zhang–Yang–Qi–Gu, journal 2022:** [Physical Review Research 4, 033081](https://doi.org/10.1103/PhysRevResearch.4.033081), *Real-space construction of crystalline topological superconductors and insulators in 2D interacting fermionic systems*. Main Table III (wallpaper) and supplemental Table I (points); interacting nonchiral real-space blocks and stacking. Compare the relative `n0=e0=0` subgroup. The old wallpaper stacking comparison was 34/34 equal; planar points were 11 equal / 9 different.
- **Zhang–Yang–Qi–Gu, arXiv v2 2023:** [arXiv:2012.15657v2](https://arxiv.org/abs/2012.15657v2), same title and methods, separate version column. Wallpaper Table III again gives 34/34 equality; its point table gives 14 equal / 6 different. These two counts must not be conflated.
- **Wang–Qi–Fang–Cheng–Gu, arXiv v1 / journal 2023:** [arXiv:2112.15533v1](https://arxiv.org/abs/2112.15533v1), [Physical Review B 108, L121104](https://doi.org/10.1103/PhysRevB.108.L121104), *Exactly solvable lattice models for interacting electronic insulators in two dimensions*. Charge-decoration commuting-projector construction. Supplement H, Tables II–III, p.17 supply separate charge and final phase layers, not wallpaper stacking groups. Each layer had 34/34 equality. The table's internal spin convention is exchanged under crystalline equivalence, and its circle-action character equals this package's `rho+s`. This construction excludes uniform IQH/E8. Keep layers in separate columns, never multiply them to manufacture a stacking answer.
- **Debray 2026v3:** the pinned interacting Class-A fixture covers all 20 planar cases. `relativeN0E0Zero` is the matching relative entry; `allN0WithE0Zero` retains one free response for orientation-preserving rotations. All 20 old relative entries match. The full source includes two intrinsic integer responses in those rotation cases; the source response restriction, not arbitrary removal of a free factor, defines the compared sector.
- **Manjunath–Calvera–Barkeshli 2024:** [arXiv:2309.12389v1](https://arxiv.org/abs/2309.12389v1), [Physical Review B 109, 035168](https://doi.org/10.1103/PhysRevB.109.035168), *Characterization and classification of interacting (2+1)D topological crystalline insulators with orientation-preserving wallpaper groups*. G-crossed braided-category consistency, response theory, and partial-rotation invariants, with crystalline equivalence as an assumption. Use the **interacting** column of Table I and the response dictionary `C=n0`, `c_minus=n0+8e0`, `k1=-e0`, at zero magnetic flux. For p1,p2,p3,p4,p6, relative means `C=c_minus=0`; all-`n0`, `e0=0` means `k1=0`; the full reference retains independent E8. The old response-defined abstract subgroup checks were 10/10 equal in each of the first two sectors. This does not identify every stored cochain root with a physical response operator.

The shift-insulator paper's interacting reduction of band-generated phases is
not a complete interacting classification. It remains excluded from the main
classification columns. No raw free-fermion group belongs in this campaign's
interacting benchmark columns.

The old wallpaper filling records also contained 34 source-coordinate flags.
Those were not abstract stacking mismatches. Distinguish a lattice `2Z` of
physical charge per primitive cell from an abstract free `Z` factor; the
source's Wyckoff/orbit generator and the runtime's primitive translation cell
must be identified before comparing their numerical filling generators.

## Immutable provenance and limits

The source fixture paths are `benchmarks/point3_full_2204.13558.json`,
`point3_full_journal_2025.json`, `point3_named_e8_journal_2025.json`,
`debray_class_a_2102.02941v3.json`, `mirror_interacting_2105.02682.json`,
`point2_stacking_2012.15657.json`, `point2_source_version_audit.json`,
`wallpaper_stacking_2012.15657.json`, and `wallpaper_layers_2112.15533.json`.
The 2024 wallpaper response audit is
`results/calibration_20261014/wallpaper_2024_response_comparison.json`.
They retain exact source locations, version labels, hashes, and restrictions.
Primary full texts are cached under `/home/arxiv`; no new primary paper was
introduced in this audit. The comprehensive
[version ledger](../../../reference_ledger_20261014.md) records journal versus
preprint differences and the inspected publisher PDFs.

Frozen output hashes:

- `results/three_dimensional_20261013/results.json`: `31c7739b39e9634e46a76ddca97f55741bff6990aa2780b36d90eea319e4622a`.
- `results/two_dimensional_20261013/results.json`: `bb21c2f171ef98a31d29dadef49a98e9d71a96ad3902d12ee4ee001cf9939b25`.

No frozen outputs, reference numbers, active tables, runners, or solver code
were edited by this audit. New runs are being orchestrated separately. Any
new discrepancy or changed result needs its own source, input, and complete
presentation witnesses before receiving an interpretation.
