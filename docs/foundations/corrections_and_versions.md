# Corrections and versions of the crystalline classification references

Search date: 2026-10-14. This is a bibliographic and scope audit, not a judgement about an author. Runtime calculations and frozen comparisons are unchanged.

One formal erratum was positively identified in the nearby point-group literature: **Physical Review B 103, 099902(E) (2021)**, correcting the 2020 parity-only point-group paper. No formal erratum or corrigendum to either **Physical Review Research 4, 033081 (2022)** or **Physical Review X 15, 031029 (2025)** was located by the searches below. That negative finding is bounded by the consulted records and access date; it is not proof that no correction exists.

## Confirmed formal erratum

Jian-Hao Zhang, Qing-Rui Wang, Shuo Yang, Yang Qi and Zheng-Cheng Gu, *Erratum: Construction and classification of point-group symmetry-protected topological phases in two-dimensional interacting fermionic systems [Phys. Rev. B 101, 100501(R) (2020)]*, **Physical Review B 103**, 099902(E), published **15 March 2021**, DOI [10.1103/PhysRevB.103.099902](https://doi.org/10.1103/PhysRevB.103.099902). The [original publisher page](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.101.100501) explicitly links it; both pages and the complete two-page [publisher PDF](https://journals.aps.org/prb/pdf/10.1103/PhysRevB.103.099902) were read.

The seven numbered corrections affect these locations:

| Erratum item | Original location | Correction |
|---|---|---|
| 1 | Table I, last row, second column | Spinless crystalline \(D_{2m}\): \(\mathbb Z_2\) for odd \(m\), \(\mathbb Z_2^2\) for even \(m\); the odd case forbids the proposed 1D decoration. |
| 2 | Paragraph after Eq. (13) | The proposed trivialization of the odd-parity center state violates reflection symmetry. |
| 3 | Table II, last row, last column | The corresponding internal-symmetry entry has the same odd/even formula. |
| 4 | Paragraph after Table II | Spinless \(D_2,D_6\) differ from \(D_4\) because the 1D decoration is absent. |
| 5 | Supplement, Section V | The Majorana-chain trivialization construction is not reflection compatible. |
| 6 | Supplement, Eq. (43) | Replaces the three \(H^2(D_n,\mathbb Z_2)\) generators and the spin-half extension \(\omega_2\); corrected formulas are erratum Eqs. (6),(7). |
| 7 | Supplement, penultimate paragraph | Distinguishes \(n=0,2\pmod4\) obstructions and removes the \(n_2=\omega_2\) class. |

The corrected paper treats interacting fermions with fermion parity and point symmetry, without the additional charge-conserving \(U(1)^f\) symmetry of this branch. Consequently these revised numerical entries are **not insulator benchmark replacements**. They do demonstrate why one must check the symmetry extension, admissible decorations and incoming identifications before comparing tables. No superconducting formulas or results from this correction have been installed in the insulator runtime.

The [arXiv record 1909.05519](https://arxiv.org/abs/1909.05519) still lists v4 dated **6 March 2020** as its latest version, preceding the erratum. The retrieved `combine.tex` retains the old Table I spinless \(D_{2m}=\mathbb Z_2\) entry. Its comment “Published version” therefore does not certify incorporation of the 2021 correction.

## The two insulator benchmark records

| Reference | Publisher date | arXiv versions actually listed | Formal correction located? |
|---|---|---|---|
| J.-H. Zhang, S. Yang, Y. Qi, Z.-C. Gu, *Real-space construction of crystalline topological superconductors and insulators in 2D interacting fermionic systems*, [PRR 4, 033081](https://doi.org/10.1103/PhysRevResearch.4.033081) | 2022-07-29 | [2012.15657](https://arxiv.org/abs/2012.15657): v1 2020-12-31; v2 2023-06-20 | None in this search |
| J.-H. Zhang, S.-Q. Ning, Y. Qi, Z.-C. Gu, *Construction and Classification of Crystalline Topological Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems*, [PRX 15, 031029](https://doi.org/10.1103/PhysRevX.15.031029) | 2025-07-28 | [2204.13558](https://arxiv.org/abs/2204.13558): v1 2022-04-28; v2 2024-06-18 | None in this search |

Both are explicitly **interacting** real-space construction papers. They are not free-band classification tables, and they are not independent bordism computations. Whether particular generators admit free realizations is a separate question from the scope of the classification being asserted. A disagreement with their tables cannot be dismissed as an interacting-versus-free difference without checking the precise cell, symmetry and equivalence relation.

An arXiv replacement or a changed journal table is distinct from a separately published erratum. The existing [version ledger](../reference_ledger_20261014.md) records the observed 2D preprint/supplement differences. Its 3D audit independently extracted all 256 journal Table II entries: four full-group cells and four graded-layer cells differ from arXiv v2, affecting spin-half \(D_{2d}\), spin-half \(C_{6h}\), and both spins of \(D_{3h}\). These are documented publication-version changes; no formal correction notice was located that labels them errata.

Our [independent bordism audits](../../benchmarks/point3_mismatch_audit_20261016/README.md) are **project-generated evidence**, not author or publisher corrections. They justify the current full E8-inclusive stacking groups for the reviewed cases. Printed reference values remain unchanged, with each discrepancy linked to its mathematical justification.

The independent mathematical reference also needs a pinned version. Arun Debray's [arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3), dated 2026-02-03, reports further corrections to its own calculations. The introduction to its tetrahedral/octahedral/icosahedral section explicitly attributes earlier discrepancies to its own calculation errors and says the revised results agree with Zhang–Ning–Qi–Gu (2025). This is a statement about that preprint's revisions, not a formal publisher erratum to a Zhang paper, and not evidence for a general assessment of either author. The calculation method is independent; the final tables were not obtained blind to the other paper. Our separately documented [D2/D6 grading audit](debray_d2_grading_audit.md) checks one remaining printed derivation against its cited mathematical ingredients while preserving the printed reference value.

## Search procedure and limitations

The search used exact DOI/title queries together with the terms `Erratum`, `Correction` and `Corrigendum`; author-name queries; the two primary publisher article pages; the 2020 parent article and its erratum; arXiv version histories; Crossref DOI metadata and bibliographic search; and the author's [personal page](https://sites.google.com/view/jianhao-sergio-zhang) and [institutional representative-publication list](https://en.westlake.edu.cn/faculty/jianhao-zhang.html). The latter is a selected list, not an exhaustive correction registry. Broad author searches surfaced the 2021 erratum; they do not establish exhaustive coverage of every nearby paper or every spelling of an author's name.

The four inspected DOI records returned no Crossref `update-to` or `updated-by` values. For the exact two benchmark DOIs, the rendered Crossmark contents said “Document is current” and displayed no update entry. **These indicators are insufficient on their own:** the corrected 2020 parent paper also returned “Document is current” with no update entry, despite its publisher page explicitly linking the 2021 erratum. This positive control is why the conclusion is phrased as “not located” rather than “there is no erratum.” The [Crossref metadata endpoint](https://api.crossref.org/works/10.1103/PhysRevB.101.100501) and [Crossmark content endpoint](https://crossmark.crossref.org/dialog-content?doi=10.1103%2FPhysRevB.101.100501&domain=pdf) make that check reproducible.

The academic-paper `fulltext` workflow was invoked for every cited paper. The 2020 original was cached as TeX; the PRR DOI resolved to its cached arXiv text, which is explicitly **not** evidence of journal identity; the PRX journal PDF was already cached. For the erratum, automatic download failed and no browser download tool was available. The complete publisher PDF was nevertheless read through the web PDF tool and its extracted text saved as `/home/arxiv/10.1103_physrevb.103.099902.publisher_web.txt`, with this access provenance. No local erratum PDF hash is claimed. Exact supplementary cocycle typography should be checked in the linked PDF, not the imperfect extracted mathematical glyphs.

The compact [metadata snapshot](corrections_search_20261014.json) records dates, endpoints, statuses, source hashes and the positive-control limitation. Two supplementary Crossref bibliographic searches returned HTTP 429 and are recorded as failed searches, not negative results; the exact four DOI metadata lookups succeeded. Neither search-engine ranking nor an absent metadata field proves absence. No personal correspondence or unpublished author communication was sought.

## How to use this audit

1. Pin the journal/preprint version, corrected locations, symmetry extension and physical sector with each comparison.
2. Use the 2021 erratum only for the parity-only paper it corrects; do not transfer its group entries into \(U(1)^f\) insulators.
3. Keep journal revisions, formal errata, our cochain calculations and independent mathematical calculations separately attributed.
4. Seek an interacting bordism/generalized-homology calculation with the same symmetry type and response normalization. A theorem about the mathematical classification ansatz and a theorem identifying that ansatz with all microscopic phases are different assertions.
5. Do not infer a general assessment of an author's work from one formal correction, an unchanged table total, or our unresolved discrepancies.
