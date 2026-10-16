# 3+1D Spin-1/2 point-group mismatch audit

Audit date: 2026-10-16. All displayed groups include E8. These are
interacting classifications. Each source column retains its printed value;
**✓** / **×** compare that value with the current computation.
UNVERIFIED means no pinned printed entry was extracted for that source.

[Audit scope and conclusions](README.md). Independent calculations below
support the current groups within the crystalline/bordism ansatz. They
are our recomputations, not author-issued corrections.

| Group | E8 layer | Current stacking | Arun Debray v3 (2026) | Zhang–Ning–Qi–Gu arXiv v2 (2024) | Zhang–Ning–Qi–Gu PRX (2025) | Independent audit |
| --- | --- | --- | --- | --- | --- | --- |
| D2 | 0 | Z2^2 | Z2^3 **×** | Z2^3 **×** | Z2^3 **×** | [D2 degree count and independent charge obstruction](debray_d2.md) |
| S4 | Z2 | Z2^2 × Z4 | UNVERIFIED | Z2^4 **×** | Z2^4 **×** | [C4 determinant Thom cofiber and exact Gysin presentation](S4_gysin.md) |
| D2d | Z2 | Z2^3 × Z8 | UNVERIFIED | Z2^5 × Z8 **×** | Z2^4 × Z8 **×** | [Independent D8 Steenrod/Koszul bordism computation](d2d_bordism.md) |
| C3i | Z2 | Z2 × Z8 | UNVERIFIED | Z2^2 × Z4 **×** | Z2^2 × Z4 **×** | [Normal C3 reduction to the Pin-c/Ci anchor](other_mismatches.md) |
| D3d | Z2 | Z2 × Z4 × Z8 | UNVERIFIED | Z2^3 × Z8 **×** | Z2^3 × Z8 **×** | [Normal C3 reduction to the independent C2h anchor](other_mismatches.md) |
| C6h | Z2 | Z2 × Z4 × Z8 | UNVERIFIED | Z2 × Z4 × Z8 **✓** | Z2^3 × Z8 **×** | [Normal C3 reduction to the independent C2h anchor](other_mismatches.md) |
| D6 | 0 | Z2^2 | Z2^3 **×** | Z2^3 **×** | Z2^3 **×** | [D2 bordism anchor and odd-kernel/odd-prime checks](debray_d2.md) |
| D3h | Z2 | Z2 × Z4 × Z8 | UNVERIFIED | Z2^3 × Z4 × Z8 **×** | Z2^2 × Z4 × Z8 **×** | [Normal C3 reduction to the C2v anchor](other_mismatches.md) |

## Sources

- Arun Debray, [Invertible phases for mixed spatial symmetries and the fermionic crystalline equivalence principle](https://arxiv.org/abs/2102.02941v3); v3, 2026-02-03. Method: Spin-c/Pin-c bordism, Adams spectral sequences, Anderson-dual equivariant phase homology.
- Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi, Zheng-Cheng Gu, [Construction and classification of crystalline topological superconductor and insulators in three-dimensional interacting fermion systems](https://arxiv.org/abs/2204.13558v2); arXiv v2, 2024-06-18. Method: Interacting real-space topological crystals, boundary gapping, bubble equivalence and stacking.
- Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi, Zheng-Cheng Gu, [Construction and Classification of Crystalline Topological Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems](https://doi.org/10.1103/PhysRevX.15.031029); Published 2025-07-28; supplement dated 2025-07-08. Method: Interacting real-space topological crystals, boundary gapping, bubble equivalence and stacking.

For C6h, the older arXiv value agrees; the journal value differs.
