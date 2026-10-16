# Why we retain the 3+1D point-group results

Date: **2026-10-16**. This note summarizes the independent checks behind the
remaining literature mismatches for interacting U(1)^f insulators. **E8 is
included on both sides.** The conclusions use the crystalline/bordism
classification framework; they are our recomputations, not author-issued errata.

The exact comparisons remain in separate **[spinless](../benchmarks/point3_mismatch_audit_20261016/spinless.md)**
and **[spin-1/2](../benchmarks/point3_mismatch_audit_20261016/spin_half.md)** tables,
with each source/version in its own column. Their union contains 14 backgrounds.
Printed values and **×** markers are retained.

## 1. D2 and D6, spin-1/2: an incorrect degree count

Our result is **Z2²**; Debray [D] prints **Z2³**. Equation (4.59), p.49, contains
the summand `Σ²H(F₂[u,v])` with `|u|=|v|=2`. Its degree-four part has two
generators, u and v. The proof of Theorem 4.82, p.57, counts three.
Correcting this count gives

$$
\Omega_4^{\mathrm{Spin}^c}(B(C_2\times C_2))
\cong \mathbb Z^2\oplus\mathbb Z_2^2.
$$

The finite phase group is its torsion subgroup. An independent normalized-bar
calculation also finds a nonzero obstruction to the candidate charge root.
D6 reduces to D2 at the prime two; its possible odd-primary contribution
vanishes. Both groups have zero E8 sheet group, so E8 cannot explain the mismatch.
[Proof and exact witnesses](../benchmarks/point3_mismatch_audit_20261016/debray_d2.md).

## 2. Oh, spinless: a missing Spin-c summand

Our result is **Z4 × Z2⁵**; Debray [D] and Zhang–Ning–Qi–Gu [Z] print
**Z4 × Z2⁴**. For `X=(BOh)^(3−V)`, an independent Steenrod/Koszul calculation
reproduces `ku₄(X)=Z4 × Z2⁴`. However, the low-degree Spin-c splitting requires

$$
\widetilde\Omega_4^{\mathrm{Spin}^c}(X)
\cong \widetilde{ku}_4(X)\oplus\widetilde{ku}_0(X),
\qquad \widetilde{ku}_0(X)=\mathbb Z_2.
$$

Debray states this splitting on p.22 but omits the second contribution in
Theorem 5.92, p.85. Relevant differentials and extensions have been checked.
Here ku is a tool for computing interacting bordism, not a free-band
classification. The extra spectral summand is not automatically a canonical
E8 generator in our coordinates.
[Proof and positive control](../benchmarks/point3_mismatch_audit_20261016/oh_audit.md).

## 3. S4 rotoinversion: the order-four extension survives

For each physical spin, the result is **Z2² × Z4**, whereas [Z] gives **Z2⁴**.
This crystallographic S4 is C4, not the permutation group. Spin-c Thom
orientation reduces its spatial twist to `X=(BC4)^(σ−1)`. The actual cofiber
`BC2₊ → BC4₊ → ΣX` determines `ku₄(X)` through the subgroup inclusion.
Applying Hashimoto's Gysin presentation [H] to this inclusion gives the matrix

$$
Q=\begin{pmatrix}2&2&1\\0&2&2\\0&0&2\end{pmatrix},
\qquad \operatorname{SNF}(Q)=(1,2,4).
$$

Thus `ku₄(X)=Z2 × Z4`; adding `ku₀(X)=Z2` gives our full group. Equal group
orders do not remove this extension disagreement.
[Natural-map derivation](../benchmarks/point3_mismatch_audit_20261016/S4_gysin.md).

## 4. D2d: an independent bordism calculation

**Spinless:** the Steenrod/Koszul calculation gives `ku₄=Z2³`; the shifted
`ku₀=Z2` gives our **Z2⁴**, rather than [Z]'s **Z2³ × Z4**.

**Spin-1/2:** an actual determinant Thom-spectrum retract protects the Z8 tower
against the potentially relevant Adams differential. The remaining classes
and shifted ku₀ give our **Z8 × Z2³**, rather than the journal's **Z8 × Z2⁴**.

These are new computations using the general bordism framework, not published
Debray D2d entries. They fix the groups without assuming the previously proposed
atomic bubble path.
[Calculation and independent review](../benchmarks/point3_mismatch_audit_20261016/d2d_bordism.md).

## 5. Normal-C3 reductions constrain the other entries

The reductions are `C3i → Ci`, `D3d → C2h`, `C6h → C2h`, and `D3h → C2v`.
Exact subgroup maps, spatial intertwiners and spin-extension gauges identify
the correct physical backgrounds. The resulting Thom spectra agree after
2-completion, so the comparison preserves **full stacking extensions**.
Odd-primary and free contributions are excluded separately.

The lower-group bordism calculations support our results for both spins of
C3i, D3d and D3h, and spin-1/2 C6h. The spinless D3h mismatch occurs only in
the older arXiv version; spin-1/2 C6h agrees there but differs in the journal.
[Anchors, source locators and exact checks](../benchmarks/point3_mismatch_audit_20261016/other_mismatches.md).

## Checks and limits

The three Debray mismatch cases also passed a fresh reference-path calculation
on n08, including E8 and acceptance. All mathematical output fields agree
with the current records. This checks implementation consistency; the independent
bordism arguments above justify the particular groups.

We also corrected our own earlier Oh argument: the twelve-site atomic orbit
has a negative fermionic permutation sign. Correcting that sign restores the
source's center quotient Z4, so that old argument does not prove an extra Z2.
The bordism calculation above supplies the justification instead.

These checks do not establish a universal equivalence between the four-data
formulas and the physical spectrum, or a microscopic map for every generator.
The [complete audit](../benchmarks/point3_mismatch_audit_20261016/README.md)
retains the proofs, source hashes, computation records and review evidence.

## References

- **[D]** Arun Debray, *Invertible phases for mixed spatial symmetries and the fermionic crystalline equivalence principle*, [arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3), revised **3 February 2026**. Method: interacting bordism and Adams spectral sequences.
- **[Z]** Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi, Zheng-Cheng Gu, *Construction and Classification of Crystalline Topological Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems*, [Phys. Rev. X **15**, 031029 (2025)](https://doi.org/10.1103/PhysRevX.15.031029), published **28 July 2025**, Table II and supplement. The separate [arXiv v2](https://arxiv.org/abs/2204.13558v2) is dated **18 June 2024**. Method: interacting real-space construction and bubble equivalence.
- **[H]** Shin Hashimoto, *On the connective K-homology groups of the classifying spaces BZ/p^r*, [Publ. RIMS **19**, 765–771 (1983)](https://doi.org/10.2977/prims/1195182451), §2, especially Proposition 2.1 and Lemmas 2.5–2.6.
