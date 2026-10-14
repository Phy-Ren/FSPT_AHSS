# Calibration review — 2026-10-14

This review corrects the interpretation and version labels of the first
campaign. It changes no obstruction, stacking formula, symmetry input or saved
classification. The October 13 outputs remain immutable computation evidence.
An abstract group match is not, by itself, a physical calibration certificate.

Read the [reference and version ledger](../../docs/reference_ledger_20261014.md),
[E8 and IQH scope audit](../../docs/e8_and_iqh_scope_20261014.md), and
[comparison protocol](../../docs/comparison_protocol_20261014.md) together.

## Which references were compared?

| Computed data | Reference and method | Version-specific arithmetic result |
| --- | --- | --- |
| 2D point groups, both uniform responses zero | Zhang, Yang, Qi, Gu, PRR 4, 033081 (2022), real-space construction, supplemental point-group table | Latest arXiv v2 (2023): 14 matches, 6 differences. Published 2022 supplement: 11 matches, 9 differences. |
| 2D wallpaper final stacking, both uniform responses zero | Same paper, main Table III | 34/34 match for both published and latest-arXiv tables. |
| 2D wallpaper charge and phase layers | Wang, Qi, Fang, Cheng, Gu, PRB 108, L121104 (2023), exactly solvable charge-decoration lattice construction | 68/68 layer comparisons match the pinned arXiv v1 (2021) tables; a complete journal-supplement comparison has not been obtained. |
| 3D point groups | Zhang, Ning, Qi, Gu, PRX 15, 031029 (2025), real-space topological crystals and bubble equivalence | The earlier 51/13 tally used arXiv v2 (2024). The journal changes four full-group cells. After the source-side named-E8 quotient, the journal also gives 51/13, but with different cases. |

The large tables above are **not a case-by-case bordism comparison**.
Bordism enters through separate, explicitly identified calibration examples.
References have independent authorship/method labels, exact source versions,
and source hashes; their data never enter the classifier.

For a separate bordism control, the split unitary U(1)^f x C2 relative sector
has

\[
 \widetilde\Omega_3^{\mathrm{Spin}^c}(BC_2)
 \simeq\Omega_2^{\mathrm{Pin}^c}\simeq\mathbb Z_4.
\]

The Smith equivalence is discussed in Debray, Devalapurkar, Krulewski, Liu,
Pacheco-Tallaj and Thorngren,
[The Smith Fiber Sequence and Invertible Field Theories](https://arxiv.org/abs/2405.04649)
(2024 preprint; Commun. Math. Phys. 407, 25, 2026), the Spin-c example
`spinc_Z2_exm` in Sec. 7.1. The low-dimensional Pin-c value is in
Freed and Hopkins, [Reflection positivity and invertible topological phases](https://arxiv.org/abs/1604.06527)
(2016 preprint; Geometry & Topology 25, 1165–1330, 2021), Theorem 9.87.
For this finite reduced sector, physical characters have the dual cyclic group.
This supports the relative order-four structure; it does not fix all physical
crystalline generator coordinates or the nonzero-uniform-IQH product.

The six latest-arXiv planar differences are C2, C4 and C6 for both spins.
The published 2022 supplement adds spinless C2v, C4v and C6v differences.
Its dihedral labels D2, D4 and D6 are these planar point groups, not the
three-dimensional proper-rotation groups with the same Schoenflies names.
No author-confirmed explanation of the even-cyclic discrepancy is assumed.

The journal 3D differences are D2 (half), S4 (both), D2d (both), C3i (both),
D3d (both), C6h (half), D6 (half), D3h (half), and Oh (spinless).
Compared with the old arXiv tally, spinless D3h becomes a match and spin-half
C6h becomes a difference. The D2d-half and D3h-half reference group orders
also change. See the version ledger for the complete cells and root evidence.
The [journal comparison](../../benchmarks/point3_comparison_journal_2025.json)
uses an [independent named-E8 ledger](../../benchmarks/point3_named_e8_journal_2025.json)
covering all 42 improper spin-specific cases; every root has a journal location
and stated extension evidence. This is source-side quotient provenance, not
a map from our computed generators to physical roots.

## Separate the 2D sectors

Write the intrinsic electronic coefficient as

\[
 \sigma_{xy}=n_0,\qquad c_-=n_0+8e_0,
 \qquad (n_0,e_0)\in\mathbb Z^2.
\]

Every existing run omits the independent E8 coordinate `e0`. Therefore:

| Object | Definition | What the saved calculation establishes |
| --- | --- | --- |
| Relative group A0 | n0=e0=0 | Relative charge/phase classification, with the source's independent lattice normalization. |
| Full current model A_CI | e0=0, all allowed n0 | Group of the supplied consistent cochain model; general nonzero-n0 physical product matching remains open in the source. |
| Fixed nonzero sector | n0=k, e0=0 | An A0-torsor when nonempty, not a subgroup closed under stacking. |
| Full electronic invertible group | Both n0 and e0 allowed | Not computed by the current implementation. |

The [new 27-row sector table](two_dimensional_sectors.md) displays A0 and
A_CI in separate columns for both spins. Its
[reproducible audit](audit_2d_sectors.py) reads all 108 saved 2D cases and
proves more than equality of abstract groups: the independently computed
relative generator cochains equal those of `relativeUniformIQH0`, and integer
Hermite normal forms give identical relation lattices. Independent Smith
forms reproduce all relative and full answers.

For C1, C2, C3, C4, C6 and p1, p2, p3, p4, p6, each spin has an actual
completed n0=1 lift. Hence the current model fits

\[
 0\longrightarrow A_0\longrightarrow A_{\rm CI}
 \xrightarrow{n_0}\mathbb Z\longrightarrow0.
\]

It splits as an abstract abelian group after choosing a lift; the choice
does not identify a unique physical IQH generator with all crystalline
responses fixed. Reflection or glide forces n0=0 in the remaining cases.
The free Z in a relative wallpaper answer is charge/filling, not uniform IQH.
Its physical primitive-cell normalization is distinct from the source's
decoration-coordinate normalization. The 34 old filling flags were pending
coordinate maps, not 34 stacking mismatches.

## Additional 2024 response-theory control

Naren Manjunath, Vladimir Calvera, and Maissam Barkeshli,
[PRB 109, 035168 (2024), arXiv:2309.12389](https://doi.org/10.1103/PhysRevB.109.035168),
derive the orientation-preserving wallpaper classification using symmetry
defects, G-crossed theory, crystalline equivalence, and real-space response
invariants. Their Table I and Sec. III keep independent integers
`c_minus`, `k1=(C-c_minus)/8`, and `kappa` (primitive-cell filling at zero flux).
The finite factors are independent invariants after defect relabeling.

Their response basis and the archive's intended basis are related by
`C=n0`, `c_minus=n0+8e0`, `k1=-e0`. Thus the comparison fixes actual response
coordinates, rather than deleting an unnamed free factor.

| Group | Finite part F | A0: C=c_minus=0 | Current all-n0 model versus k1=0 | Full physical reference |
| --- | --- | --- | --- | --- |
| p1 | 0 | Z | Z^2 | Z^3 |
| p2 | Z4^3 x Z2 | Z x F | Z^2 x F | Z^3 x F |
| p3 | Z3^5 | Z x F | Z^2 x F | Z^3 x F |
| p4 | Z8 x Z4^2 x Z2 | Z x F | Z^2 x F | Z^3 x F |
| p6 | Z12 x Z6 x Z3 | Z x F | Z^2 x F | Z^3 x F |

Both spin conventions pass these abstract subgroup comparisons. The source
defines rotation operators whose Mth powers are respectively 1 and fermion
parity, related by a charge rotation; the translations are unchanged.
The [saved audit](wallpaper_2024_response_comparison.json) and
[executable](../../benchmarks/audit_wallpaper_2024.py) pin the source cells and
record this convention. A separate reviewer reproduced the output exactly.
This is useful additional evidence, but does not supply a native-root-to-response
map or settle the universal nonzero-n0 cochain product.

## What E8 does and does not imply

The current model retains ordinary bosonic group-cohomological phases. It
omits independent neutral E8 decorations and their local operations. Omitting
E8 is different from quotienting a fermionic classification by all bosonic
phases. In the charge-conserving coefficient lattice, charge-two BIQH obeys
`BIQH2 = 8 CI - E8`; a bosonic image can therefore intersect electronic roots.

For 3+1D there is a bounded full-AHSS argument against an additional incoming
identification from the E8 H0 row: with unitary internal symmetry, a neutral
E8 layer with trivial symmetry action exists and makes that coefficient
generator permanent; with an antiunitary sign, H0(G,Z_s)=0. This is stronger
than the legacy run flag based only on vanishing H1. Applying the argument to
this program still requires identifying its tower with that full filtration.
It establishes neither all mixed extensions nor all 4+1D E8 operations.

The journal's separately named E8 root allows an arithmetic quotient of its
claimed group. Identifying our model with that quotient additionally requires
a physical map and control of its kernel, image, and intersection with E8.
Consequently, “51 abstract matches” is not “51 complete physical calibrations.”

## Calibration order

1. Fix source versions, the physical symmetry and spin-charge extension,
   crystalline-equivalence twists, response units, and allowed adjoining
   operations before comparing any groups.
2. Begin with n0=e0=0 and the split U(1)^f x C2 root: identify the order-four
   root and its nontrivial bosonic square. Compare to both a physical lattice
   construction and the reduced Spin-c bordism character, not just a table order.
3. Extend through C4/C6 and their real-space charge/rotation relations, then
   construct wallpaper response/filling maps. Keep the independent tests of
   equations and gauge transport separate from physical calibration.
4. For nonzero n0, identify the primitive IQH lift and its crystalline
   responses using the 2024 reference, then check mixed stacking at the level
   of those observables. A noncanonical abstract Z splitting is insufficient.
5. In 3+1D use the precise AIII/AII/AI and mirror benchmarks, with E8 explicitly
   present on the reference side, before interpreting the remaining point-group
   differences. Add an E8 module only with specified operations and a verified
   electronic embedding; never tune the CI formulas to a disputed table.
