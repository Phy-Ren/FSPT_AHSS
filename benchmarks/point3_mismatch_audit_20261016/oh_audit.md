# Independent audit: spinless O_h in 3+1 dimensions

Date: 2026-10-16 UTC. Scope: the full interacting Class-A point-group problem, including the neutral decoration, with physical spinless fermions. No runtime formulas, accepted results, reference fixtures, or cluster jobs were changed.

## Finding

There is now a concrete mathematical reason to retain our current answer

$$
\mathbb Z_4\oplus(\mathbb Z_2)^5.
$$

An independent reconstruction of the relevant bordism calculation gives this group. Debray's v3 Theorem 5.92 prints $\mathbb Z_4\oplus(\mathbb Z_2)^4$, but the displayed calculation on the same page computes connective complex K-homology $ku_4$, not the complete Spin-c bordism group. The low-degree Spin-c splitting requires a further $ku_0=\mathbb Z_2$ summand. The discrepancy is therefore localized to the transition from the Adams calculation to the stated Spin-c theorem.

This is substantially stronger than agreement with our own cochain engine or a suspicious real-space paragraph. It independently computes the same bordism problem Debray assigns to physical spinless O_h. It does not prove a universal equivalence between our entire four-data theory and the physical spectrum.

Confidence is high for this particular stacking group, after a separate peer review of the Steenrod action, Koszul computation, filtration bounds, differentials, extensions, and Spin-c splitting. The paper's authors have not confirmed a correction; the stored reference remains the result they actually printed.

## Sources and precise locations

1. Arun Debray, *Invertible phases for mixed spatial symmetries and the fermionic crystalline equivalence principle*, [arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3), revised 3 February 2026. Relevant locations: p.22, low-degree Spin-c splitting; p.60, Table 6; pp.81–82, full-octahedral cohomology and Stiefel–Whitney classes; p.85, §5.5.3, Theorem 5.92, equations (5.93) and (5.94). The current cached source agrees byte for byte with the previously pinned v3 source for `full_octahedral.tex`.
2. Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi, Zheng-Cheng Gu, *Construction and Classification of Crystalline Topological Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems*, [Physical Review X 15, 031029 (2025)](https://doi.org/10.1103/PhysRevX.15.031029), published 28 July 2025. Relevant locations: Table II on p.031029-5; §IV G, pp.031029-48–50; the atomic states explicitly reused in the insulator discussion are equations (209)–(210), p.031029-37. The journal PDF, rather than only the arXiv draft, was checked.
3. The independent peer reviewer also checked the modern Spin-c splitting statement in [Buchanan–McKean, Algebraic & Geometric Topology 26 (2026), 485–551](https://doi.org/10.2140/agt.2026.26.485), Theorem 3.6 on p.492 and Table 3 on p.538. Up to degree seven, the two relevant connective-complex-K summands are the unshifted summand and its degree-four shift; no additional mod-two Eilenberg–Mac Lane summand occurs in this range. See `oh_peer_d2.json` and the independent D2 audit for the source check.

## Reconstructing the bordism calculation

Put

$$
G=O_h=S_4\times C_2,\qquad X=(BG)^{3-V_\lambda}.
$$

This is exactly the spinless Class-A Thom spectrum used in Debray §5.5.3. Its virtual bundle has rank zero, so X is connective. In the notation of the paper,

$$
H^*(BG;\mathbb F_2)=\mathbb F_2[x,a,b,c]/(ac),
\qquad |x|=|a|=1,\ |b|=2,\ |c|=3.
$$

The standard three-dimensional spatial representation has

$$
w_1(V_\lambda)=x,\quad w_2(V_\lambda)=a^2+b+x^2,
$$

and hence

$$
w_1(3-V_\lambda)=x,\quad w_2(3-V_\lambda)=a^2+b.
$$

The base Steenrod operations are specified by

$$
Sq(x)=x+x^2,\quad Sq(a)=a+a^2,\quad
Sq(b)=b+ab+c+b^2,\quad Sq(c)=c+bc+c^2.
$$

For a Thom class U in degree zero, these imply

$$
Sq^1(Uf)=U(Sq^1f+xf),
$$

$$
Sq^2(Uf)=U(Sq^2f+xSq^1f+(a^2+b)f).
$$

We then calculate the module over

$$
E(1)=\Lambda(Q_0,Q_1),\quad Q_0=Sq^1,\quad
Q_1=Sq^1Sq^2+Sq^2Sq^1.
$$

The computation does not import the decomposition asserted in equation (5.93), the paper's Adams picture, or any project classification output. It constructs the polynomial quotient and the two operations directly, verifies the exterior-algebra identities, and computes the dual Koszul complex over exact binary linear algebra:

$$
C^{s,t}=\bigoplus_{j=0}^{s}M_{t-s-2j}^{\vee},
\qquad d=h_0Q_0^{\vee}+v_1Q_1^{\vee}.
$$

Here M is the Thom cohomology module and $|h_0|=(1,1)$, $|v_1|=(1,3)$. The result is:

| Stem t-s | Filtration 0 | Filtration 1 | Filtration 2 and higher |
| --- | ---: | ---: | ---: |
| 0 | 1 | 0 | 0 |
| 1 | 1 | 0 | 0 |
| 2 | 3 | 0 | 0 |
| 3 | 3 | 0 | 0 |
| 4 | 5 | 1 | 0 |
| 5 | 6 | 1 | 0 |

For stems through five, the cell ranges and differentials stabilize by filtration four, since all module degrees are nonnegative. Thus the higher-filtration zero statement is not extrapolated from an arbitrary numerical cutoff. The independent reviewer also checked through filtration twelve.

An Adams differential has bidegree $(s,n)\mapsto(s+r,n-1)$, with r at least two. Every possible outgoing differential from stem four has a zero target in stem three. Incoming differentials cannot reach the only occupied filtrations zero and one. Hence the stem-four classes survive.

Multiplication by h_0 from filtration zero to filtration one has rank one. This gives exactly one order-four summand, and the remaining four classes give order-two summands. There is no additional positive-filtration class that could support another hidden multiplication-by-two extension. Therefore

$$
\widetilde{ku}_4(X)=\mathbb Z_4\oplus(\mathbb Z_2)^4.
$$

This reproduces the numerical group printed in Theorem 5.92, but identifies it as ku, not the full bordism group.

The paper itself states on p.22 that, for a connective spectrum in this range,

$$
\widetilde\Omega^{\mathrm{Spin}^c}_4(X)_{(2)}
\cong \widetilde{ku}_4(X)_{(2)}\oplus
\widetilde{ku}_0(X)_{(2)}.
$$

There is an elementary independent check of the second summand:

$$
\widetilde{ku}_0(X)=\widetilde H_0(X;\mathbb Z)
=H_0(G;\mathbb Z_{\det V_\lambda})=\mathbb Z_2.
$$

The central inversion acts by minus one on this orientation coefficient. After inverting two, its group homology vanishes; the twisted homology and connective-bordism spectral sequences therefore have neither odd-primary nor rational contributions. This avoids relying on the imprecise sentence about mod-two cohomology in the paper.

Consequently the complete answer is

$$
\boxed{\widetilde\Omega^{\mathrm{Spin}^c}_4(X)
=\mathbb Z_4\oplus(\mathbb Z_2)^5.}
$$

The green degree-four dot in equation (5.94) cannot already represent the additional shifted-ku contribution: it belongs to the decomposition of H*(X) itself. Its presence is independently reproduced by the Koszul calculation. The additional summand enters only when passing from ku to Spin-c bordism.

The extra summand in this particular K-theory splitting must not automatically be named the neutral E8 root in our cochain coordinates. A splitting of coefficient spectra can mix the charge and gravitational normalizations. No canonical root-by-root map was constructed here. The group equality and the missing summand in the cited theorem do not depend on choosing that map.

## Positive control: physical spin-half O_h

The same independent code, with only the Thom twist changed to

$$
X_{1/2}=(BG)^{\det(V_\lambda)-1},\quad w_1=x,\quad w_2=0,
$$

gives stem-four Ext dimensions (5,2,1), and successive h_0 ranks (2,1). For this positive control the filtration-two class is protected by the actual split summand $(BC_2)^{\sigma-1}$: projection to the central inversion factor and its section split the spectrum. Its known three-step h_0 tower cannot receive a differential from the complementary spectrum. The complement has no stem-four class at filtration two or higher, so the same degree argument handles it. Thus

$$
ku_4(X_{1/2})=\mathbb Z_8\oplus\mathbb Z_4\oplus(\mathbb Z_2)^3,
$$

and the shifted ku_0 summand produces

$$
\Omega^{\mathrm{Spin}^c}_4(X_{1/2})
=\mathbb Z_8\oplus\mathbb Z_4\oplus(\mathbb Z_2)^4.
$$

This agrees with both Debray Theorem 5.95 and our current spin-half result. It is a useful control against a uniform convention error or indiscriminately adding one Z2 to every printed answer.

## What the real-space paper does and does not prove

The old printed-relation audit is arithmetically correct but is insufficient to identify the physical extra root. The published p.031029-49 prints the three atomic relations

$$
(8,0,0),\quad(6,1,0),\quad(12,0,0)
$$

in coordinates (integer charge, coordinate-reflection bit, diagonal-reflection bit). Including the two character periods, Smith reduction gives (1,2,4), hence a quotient Z4 × Z2, whereas the paragraph claims Z4.

However, a literal filled orbit of twelve spinless scalar fermions on the edge directions has diagonal-reflection sign minus one. For reflection (x,y,z) ↦ (y,x,z), the twelve-site permutation has two fixed points and five transpositions. Its many-body determinant is therefore minus one. The correct literal orbit relation is

$$
(12,0,1).
$$

The paper's own equations (209)–(210), p.031029-37, provide the same check: the xy four-fermion state changes sign, while the yz and xz blocks are exchanged. Exchanging two even-parity four-fermion blocks contributes plus one. Their product thus has the negative sign, contrary to the later insulator paragraph.

With this corrected sign the three orbit relations give Smith form (1,1,4), so the center quotient is Z4, as claimed in the paper. Generic 24- and 48-site orbits add no new relation in this scalar-orbital check. Therefore the old argument “the printed 0D relation leaves an extra Z2, so our extra Z2 is correct” must not be used as a physical proof. The independent bordism reconstruction above supplies the stronger evidence.

There is a separate inconsistency in the real-space presentation. Table II gives only Z2 for the spinless O_h one-dimensional block layer, but §IV G 2 on p.031029-49 explicitly gives Z2², with Haldane chains on the two axis orbits. The same body's two-dimensional layer is Z2³ on p.031029-48, and its corrected center quotient is Z4. Taking those stated surviving body layers gives total order 8 × 4 × 4 = 128, whereas Table II and the final group have order 64. A group extension cannot reduce the order by two. An additional identification would have to be supplied to reconcile the smaller table with those body claims. We did not locate such a relation in the relevant insulator section. The body's higher-order-surface paragraph also calls the 2D layer Z2², another incompatible count.

These internal contradictions are specific, checkable statements. They do not show that every calculation by any author is unreliable. They also do not establish a causal story about why Debray's revision agrees with the real-space table.

## Dependence and independence of the two sources

The introductory paragraph to Debray's sporadic-group section states that discrepancies in the first version were corrected following comparison with Zhang–Ning–Qi–Gu, and thanks Zheng-Cheng Gu, Yang Qi, and Weicheng Ye. Thus blind independence of the two final tables should not be asserted.

However, §5.5.3 contains its own E(1)-module and Adams calculation. It does not invoke a theorem of Zhang–Ning–Qi–Gu as the mathematical proof of O_h. Our audit locates an internal missing summand using that calculation and a separately checked spectrum splitting. Agreement of the final tables alone would not establish which author's calculation influenced a particular erroneous step.

## Relation to our saved cochain results

Our selected four-data model has an explicit completed-charge/phase presentation with group Z4 × Z2⁴ and an independently calculated neutral section of order two. Previous audits checked the saved native closures, phase completions, incoming charge-gauge image, Smith form, physical symmetry input, and restrictions to D4h, Th, O, and Td. Those checks already made a basic cochain implementation failure unlikely, but did not establish the physical identification.

The calculation in this note supplies an independent bordism-group cross-check for this one case. It does not construct the canonical map from the individual cochain generators to the real-space Haldane or atomic generators, and it does not certify the universal CI-kernel comparison or every other point/space group. No arbitrary quotient relation should be added to force agreement with the smaller published cell.

## Reproducible artifacts

All paths below are in this audit directory unless specified otherwise.

- `oh_ext_audit.py` / `.json`: independent polynomial Steenrod module and dual-Koszul calculation, h_0 rank, and final groups. Initial operation/complex checks: 382.
- `oh_peer_d2.json`: separate review, including higher-filtration and 91 h_0 chain-map checks.
- `oh_spin_half_ext_control.py` / `.json`: positive control using the determinant Thom twist.
- `oh_atomic_orbits.py` / `.json`: explicit 48 signed-permutation matrices, orbit permutations, Fock-state signs, and both printed/corrected Smith forms.
- `oh_printed_relations.json`: rerun of the existing printed-TeX relation extractor.
- `debray_v3.pdf`, plus extracted relevant pages `debray_p22.txt`, `debray_p60.txt`, `debray_p82.txt`, `debray_p85.txt`.
- `prx_p37.txt`, `prx_p48.txt`, `prx_p49.txt`, `prx_p50.txt`: relevant journal-page extracts; canonical full PDF is `/home/arxiv/10.1103_physrevx.15.031029.pdf`.

Source hashes:

- Debray v3 PDF: `e3ee818735646e68fe382ead0580e92e57425bd47ac9ccff15ba91285a727929`.
- Debray `full_octahedral.tex`: `223b5c061bbae1a16cf60101a709a25fd248be859147b85db1cafaaebb7cfed9`.
- PRX journal PDF: `eda983b3c093877d7b6d34da1092ae8c8c5dc272746e6f4eaf28f35a7438c692`.

The live reference tables should continue to show the printed references with a difference marker, accompanied by the audit conclusion. This audit provides grounds to label the spinless O_h discrepancy as a specific likely source-side omission, rather than an unresolved anonymous mismatch.
