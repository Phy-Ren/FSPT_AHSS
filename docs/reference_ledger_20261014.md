# Reference and comparison ledger, 2026-10-14

This audit separates primary-source versions, abstract-group comparisons, and physical calibration. It does not change calculation inputs, reference fixtures, or the immutable campaign reports. In particular, the saved status `published_source_discrepancy` means a difference from a specified printed table; it is not a finding that an author or publication is wrong.

The four original benchmark papers below use real-space constructions, charge-decorated lattice models, or interacting reductions of band phases. **None of these four comparisons is an independent bordism calculation.** Citing bordism in an introduction does not turn a paper's block-state computation into a bordism benchmark. Exact implementation of the supplied AHSS formulas and agreement with these tables are different levels of evidence.

## Bibliographic records and actual benchmark locations

| Key | Authors and title | First/latest arXiv versions, checked 2026-10-14 | Journal record |
| --- | --- | --- | --- |
| R2 | Jian-Hao Zhang, Shuo Yang, Yang Qi, Zheng-Cheng Gu, *Real-space construction of crystalline topological superconductors and insulators in 2D interacting fermionic systems* | [2012.15657](https://arxiv.org/abs/2012.15657): v1 2020-12-31; v2 2023-06-20 | [Physical Review Research **4**, 033081 (2022)](https://doi.org/10.1103/PhysRevResearch.4.033081), published 2022-07-29 |
| L2 | Qing-Rui Wang, Yang Qi, Chen Fang, Meng Cheng, Zheng-Cheng Gu, *Exactly solvable lattice models for interacting electronic insulators in two dimensions* | [2112.15533](https://arxiv.org/abs/2112.15533): v1 2021-12-31; no later arXiv version listed | [Physical Review B **108**, L121104 (2023)](https://doi.org/10.1103/PhysRevB.108.L121104), published 2023-09-06 |
| B2 | Shang Liu, Ashvin Vishwanath, Eslam Khalaf, *Shift Insulators: Rotation-Protected Two-Dimensional Topological Crystalline Insulators* | [1809.01636](https://arxiv.org/abs/1809.01636): v1 2018-09-05; v2 2019-07-18 | [Physical Review X **9**, 031003 (2019)](https://doi.org/10.1103/PhysRevX.9.031003), published 2019-07-03 |
| R3 | Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi, Zheng-Cheng Gu, *Construction and Classification of Crystalline Topological Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems* | [2204.13558](https://arxiv.org/abs/2204.13558): v1 2022-04-28; v2 2024-06-18 | [Physical Review X **15**, 031029 (2025)](https://doi.org/10.1103/PhysRevX.15.031029), published 2025-07-28 |

The arXiv submission year, latest revision year, and journal year must not be substituted for one another. R3's arXiv landing page does not currently list its journal DOI; the journal's own title, authors, and article establish the publication record. The R2 and R3 arXiv and journal tables actually differ.

| Key | Method used for the cited result | Precise location and quantity | Scope and convention for our comparison |
| --- | --- | --- | --- |
| R2 | Symmetric real-space cell decomposition; lower-dimensional block states; obstruction/no-open-edge checks; bubble equivalence; stacking | Main Table III, journal p.033081-4: 17 wallpaper groups, two physical spins, full abstract stacking. Supplement Sec.II, Table I, p.2: planar point groups. Cached v2 TeX: main table lines 334–376; point table lines 3547–3568. | Compare the nonchiral, relative uniform-IQH-zero subgroup. The free wallpaper charge coordinate remains present. These tables do not include an independent uniform neutral E8 phase. Physical spin columns are used directly. |
| L2 | Charge decoration at symmetry-domain-wall junctions; super-cocycle consistency; exactly solvable fixed-point wavefunctions/commuting-projector Hamiltonians; finite-resolution computations for examples | [arXiv v1 PDF](https://arxiv.org/pdf/2112.15533), Supplement H, Tables II and III, p.17: charge C and bosonic phase B layers. Table III's arrow means quotient by the incoming trivialization. Main text, “More Examples,” also states the internal U(1)^f × C2 result Z4. | These are graded layers, not a full wallpaper stacking-group table. Use the final B layer. Table II's internal spinless column maps to physical spin-half; Table III maps to physical spinless. The paper's rho is the circle automorphism, while the supplied package's rho is the action on integral charge; thus rho_paper = rho_package + s. The n2/nu3 construction supplies the nonchiral n0=0 sector used here, not the full uniform IQH/E8 tower. |
| B2 | Band/Wannier and dimensional-reduction construction; reduction to a rotation-center representation; adjoining operations; interacting reduction of band-generated states | [Journal PDF](https://journals.aps.org/prx/pdf/10.1103/PhysRevX.9.031003), Table VI, p.031003-24; Sec.VI B, pp.24–25. Cached TeX table lines 1090–1108 and scope restriction at 1114. | Class A and both eta=0,1. The paper explicitly restricts this calculation to reduction of the noninteracting classification, leaving potential interaction-only phases outside its claim. Rotation only; translations are not assumed. The adjoining quotient is explicit. Uniform Hall response and a neutral E8 direction are not the compared center classification. |
| R3 | Real-space topological crystals; lower-dimensional decorations; K-matrix/null-vector boundary gapping and anomaly tests; bubble equivalence; extension/stacking analysis | Main Table II: all 32 point groups and two physical spins; both block layers and full groups. [Journal PDF](https://journals.aps.org/prx/pdf/10.1103/PhysRevX.15.031029), p.031029-5. [Journal supplement](https://journals.aps.org/prx/supplemental/10.1103/PhysRevX.15.031029/3DpointCombine__supp.pdf), Sec.III, individual group root lists. Cached arXiv v2: TeX label TI, lines 242–316. | The reference includes independent neutral E8 block decorations. Our runtime computes the supplied CI/charge/group-cohomological phase sector. For improper groups compare only the reference quotient by its explicitly named independent E8 root, with the abstract-quotient limitation stated below. For proper finite rotations H1(G,Z)=0 excludes E8 decorations of that form; it does not prove every possible physical response is covered. |

The B2 section is **VI B in the published PDF**; some earlier working notes called it V B from the draft organization. Table VI is the unambiguous common locator. L2's two wallpaper tables are Tables II and III, despite their duplicate TeX label. The L2 journal landing-page metadata was verified, but a complete journal-supplement table comparison was not obtained; its numerical benchmark remains explicitly pinned to arXiv v1.

## 2D: what matches, and which version differs

The immutable 2D report has 54 completed cases: 20 planar point-group cases and 34 wallpaper cases. Every literature comparison uses the **actual `relativeUniformIQH0` subgroup** extracted from the complete presentation. Keeping the full calculation and then taking this kernel is more precise than silently suppressing a generator.

| Comparison | Matching checks | Differing checks | Qualification |
| --- | ---: | ---: | --- |
| Wallpaper stacking vs R2 arXiv v2 | 34 | 0 | All 17 groups, both physical spins |
| Wallpaper stacking vs R2 journal Table III | 34 | 0 | All 34 printed cells rechecked against the published p.4 table; same as arXiv v2 |
| Wallpaper charge layers vs L2 arXiv v1 Table II/III | 34 | 0 | Final charge layer |
| Wallpaper phase layers vs L2 arXiv v1 Table II/III | 34 | 0 | Final phase layer after incoming relations |
| Planar stacking vs R2 arXiv v2 point table | 14 | 6 | Saved campaign comparison |
| Planar stacking vs R2 journal supplement Table I | 11 | 9 | Three additional older spinless dihedral cells differ |
| Cyclic planar stacking vs B2 Table VI class A | 10 | 0 | Independent band-generated interacting-reduction control; not a completeness proof |

There are 34 further `requires_source_coordinate_map` records. They concern the **embedding of free charge into physical filling**, not unequal abstract classification groups. For example, Z and 2Z are isomorphic abstract groups. A generator defined per symmetry-related site orbit can carry two units per primitive cell. Matching the printed coefficient to a primitive-cell charge needs a Wyckoff/orbit-coordinate map. Thus “all wallpaper stacking groups match” is correct for the tested relative sector; “all wallpaper generators and physical filling normalizations have been identified” is not established.

The saved total of 126 matches counts 102 wallpaper stacking/layer checks, 14 point-table checks, and 10 B2 checks. It does not count 126 distinct systems. The six saved printed differences are planar C2, C4 and C6 for both spins. All come from **Zhang, Yang, Qi and Gu (R2, journal 2022; arXiv v2 2023), a real-space construction**, not from L2 or a bordism table.

| Planar group | Physical spin | Computed relative group | R2 arXiv v2 point Table I | R2 journal point Table I | B2 band-generated control |
| --- | --- | --- | --- | --- | --- |
| C2 | Spinless and spin-half | Z4 | Z2 × Z2 | Z2 × Z2 | Z4 |
| C4 | Spinless and spin-half | Z2 × Z8 | Z4 × Z4 | Z4 × Z4 | Z2 × Z8 |
| C6 | Spinless and spin-half | Z3 × Z12 | Z6 × Z6 | Z6 × Z6 | Z3 × Z12 |
| C2v = planar D2 | Spinless | Z4 | Z4 | Z2 | Not covered |
| C4v = planar D4 | Spinless | Z8 | Z8 | Z4 | Not covered |
| C6v = planar D6 | Spinless | Z12 | Z12 | Z6 | Not covered |

The R2 even-cyclic formula is unchanged between arXiv v1, v2, and the journal supplement. Its spinless even-dihedral formula changed in arXiv v2. The journal supplement p.2 Eq.(6) still gives spinless D4=Z4. These version differences are observations, not an inferred erratum. No author-confirmed reconciliation of the even-cyclic difference was found in this audit.

The point and wallpaper statements concern different symmetry groups: translations remain in wallpaper computations and are absent for a point group. Furthermore L2 gives layers, while R2 gives stacking groups. Equality of the wallpaper tables does not imply equality of the separate planar point table. B2 also explicitly explains that including translations and quotienting general Wyckoff fillings changes the classification problem; its point result cannot be substituted wholesale for a wallpaper table.

## 3D: latest journal versus the pinned arXiv table

The saved 64-case comparison is against **R3 arXiv v2 (2024-06-18)**: 51 abstract-group matches and 13 differences after the stated E8 scope handling. Its additional 42 `scope_mismatch` entries concern attempted full-reference comparisons in a theory without the independent E8 sector; they are not 42 computation failures.

The 2025 journal Table II is not identical to that arXiv version. A fresh independent extraction of all 256 table cells (64 full groups and 192 block-layer groups) finds exactly **four changed full-group cells and four changed layer cells**. The extraction reads subscript/superscript glyph coordinates from the publisher PDF, also inspected visually; it does not use the runtime's answers. See [the extraction script](../benchmarks/audit_point3_journal_2025.py) and [the full journal reference](../benchmarks/point3_full_journal_2025.json).

| R3 case | Changed layer: arXiv v2 → journal | Full group: arXiv v2 → journal | Journal named E8 evidence |
| --- | --- | --- | --- |
| D2d, spin-half | E2D: Z8 × Z2² → Z8 × Z2 | Z8 × Z2⁵ → Z8 × Z2⁴ | Supplement III K, p.15, root 3; the stated extension joins roots 1 and 2 |
| C6h, spin-half | E0D: Z4 → Z2² | Z8 × Z4 × Z2 → Z8 × Z2³ | Supplement III T, p.25, root 3; the stated extension joins roots 1 and 2 |
| D3h, spinless | E0D: Z2 → 1 | Z2⁵ → Z2⁴ | Supplement III W, p.28, root 3, order two |
| D3h, spin-half | E0D: Z2² → Z2 | Z8 × Z4 × Z2³ → Z8 × Z4 × Z2² | Supplement III W, p.29, root 4; the listed CI/fSPT extension excludes this root |

These changed root lists were read in the **journal** supplement dated 2025-07-08, not inferred from abstract orders. The [independently reviewed journal E8 ledger](../benchmarks/point3_named_e8_journal_2025.json) confirms all 42 spin-specific named roots, their locations and exclusion from the stated nontrivial extensions. The [separate journal comparison](../benchmarks/point3_comparison_journal_2025.json) records every computed/reference group and scope. Deleting an arbitrary Z2 because it improves agreement is never the comparison rule.

The following table records the union of differing cases across both R3 versions. Every row is attributed to **Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi and Zheng-Cheng Gu, the R3 title above, Table II and the corresponding group root list, using the real-space topological-crystal method**. For D2 and D6 the reference is the full group; all other rows show the quotient by the reference's named independent neutral E8 root. A parenthetical “match” marks equality only for that version.

| Group | Physical spin | Computed CI/charge/phase group | R3 arXiv v2 reference | R3 journal 2025 reference |
| --- | --- | --- | --- | --- |
| D2 | Spin-half | Z2² | Z2³ | Z2³ |
| S4 | Spinless | Z2 × Z4 | Z2³ | Z2³ |
| S4 | Spin-half | Z2 × Z4 | Z2³ | Z2³ |
| D2d | Spinless | Z2³ | Z2² × Z4 | Z2² × Z4 |
| D2d | Spin-half | Z2² × Z8 | Z2⁴ × Z8 | Z2³ × Z8 |
| C3i = S6 | Spinless | Z8 | Z2 × Z4 | Z2 × Z4 |
| C3i = S6 | Spin-half | Z8 | Z2 × Z4 | Z2 × Z4 |
| D3d | Spinless | Z4 × Z8 | Z2 × Z4 | Z2 × Z4 |
| D3d | Spin-half | Z4 × Z8 | Z2² × Z8 | Z2² × Z8 |
| C6h | Spin-half | Z4 × Z8 | Z4 × Z8 (match) | Z2² × Z8 |
| D6 | Spin-half | Z2² | Z2³ | Z2³ |
| D3h | Spinless | Z2³ | Z2⁴ | Z2³ (match) |
| D3h | Spin-half | Z4 × Z8 | Z2² × Z4 × Z8 | Z2 × Z4 × Z8 |
| Oh | Spinless | Z2⁴ × Z4 | Z2³ × Z4 | Z2³ × Z4 |

The version-specific meaningful totals remain **51 matches / 13 differences**, but the identity of one differing case changes: journal D3h spinless matches, while journal C6h spin-half differs. Reporting only the unchanged total hides this material revision. Journal counts by spin are 27 matches / 5 differences for spinless, and 24 / 8 for spin-half; proper/improper counts remain 20 / 2 and 31 / 11. A direct, unprojected numerical comparison with all 64 full journal groups gives 21 equal / 43 unequal abstract groups. That is not a valid physical success rate: the 42 improper cases still have the E8 scope difference, and accidental equality does not identify their sectors.

Reproduce the extraction and comparison with the pinned publisher PDF:

```bash
python benchmarks/audit_point3_journal_2025.py /home/arxiv/10.1103_physrevx.15.031029.pdf \
  --output /tmp/point3_full_journal_2025.json \
  --arxiv-reference benchmarks/point3_full_2204.13558.json \
  --results results/three_dimensional_20261013/results.json \
  --journal-e8-ledger benchmarks/point3_named_e8_journal_2025.json \
  --comparison-output /tmp/point3_comparison_journal_2025.json
```

## Levels of calibration and unresolved questions

1. **Source transcription:** paper, version, table, spin convention, group name and exact invariant factors. This audit discovered real version changes. The old campaign outputs remain correct descriptions of their pinned comparisons.
2. **Exact implementation:** cochain equations, incoming gauges, completions, nontrivial root powers and presentations. Internal tests certify these properties for the supplied theory, not the completeness of its physical interpretation.
3. **Independent calculations inside that theory:** cyclic bar/periodic cochain audits, the D2 Steenrod obstruction, and exact normal-C3 subgroup/background checks substantiate particular outputs without importing a target table into the computation.
4. **Physical identification:** matching the crystalline symmetry extension, charge action, reflection convention, boundary/atomic adjoining equivalence, neutral sector and individual response invariants remains a separate obligation. An abstract named-E8 quotient is not an implemented physical projection map.
5. **Independent physical completeness:** an appropriate bordism or other complete invertible-phase calculation with an explicit coefficient/response dictionary has not been supplied by these four benchmark sources.

Consequently, the existing D2 representation obstruction, S4/S6 root-extension certificates, conditional atomic-orbit quotients, and Oh printed-relation Smith calculation should be presented as targeted evidence to investigate the comparison. They do not, by themselves, establish that the literature is wrong or that the implementation realizes every interacting insulator. In particular the atomic-orbit quotient requires an allowed adjoining/bubble path, and the Oh printed relation list may omit an additional physical relation. Earlier source-text critiques pinned to arXiv v2 must not be transferred to a journal passage without rereading that passage; this table-version audit does not claim a complete line-by-line audit of every journal derivation.

## Reproducibility and source bytes

| Artifact | SHA-256 |
| --- | --- |
| R2 cached arXiv v2 `combine_sub.tex` | `6f0723e1f4bfeab26ba50edeee66e5d4c17123d6407aa57ea7a0295e3b396fe9` |
| R2 explicit arXiv v1 `combine_arXiv.tex` | `9f2290710647a692f4eee47ec5b3835030d25393dccc5b4b20978932cd4cdbc9` |
| L2 cached arXiv v1 `U1f.tex` | `e1f27c17480e681d09bc293c51ff972a6553cd2f6a1e723797368764ddb2d457` |
| B2 cached arXiv v2 `Shift.tex` | `738f678b2121cd8ce68a0ede7ef48e1ffa4148be0fe4921b9a4caa53c45ea103` |
| R3 cached arXiv v2 `main.tex` | `f4fbece88797281b9e8b5b41280b351ffbd4716e305abfad55e169388920e351` |
| R3 journal PDF, 56 pages, `/home/arxiv/10.1103_physrevx.15.031029.pdf` | `eda983b3c093877d7b6d34da1092ae8c8c5dc272746e6f4eaf28f35a7438c692` |
| Immutable 2D `results.json` | `bb21c2f171ef98a31d29dadef49a98e9d71a96ad3902d12ee4ee001cf9939b25` |
| Immutable 3D `results.json` | `31c7739b39e9634e46a76ddca97f55741bff6990aa2780b36d90eea319e4622a` |

The publisher PDF and supplement were consulted directly for the version checks. Where only a web PDF view was available, no local PDF hash is invented. The arXiv fulltext tool can return a cached latest preprint when given a DOI or version suffix; its success message does not establish identity with a journal version. Explicit publisher inspection is required.
