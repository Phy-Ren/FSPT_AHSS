# Independent D2/D6 spin-half mismatch audit

Audit date: 2026-10-16. Production code, current tables, and printed-reference fixtures were not changed.

## Conclusion

For the proper point groups **D2 and D6 with physical spin-half, charge-preserving fermions**, there is strong mathematical evidence that **the printed Z2^3 value is erroneous and Z2^2 is the correct value within the cited interacting crystalline/bordism ansatz**. This conclusion is stronger than noticing an incomplete proof: the cited bordism ingredients, independently checked low-degree Spin^c splitting, and a separate cochain obstruction all give Z2^2.

This is our audit, not an author-issued erratum. It does not imply that all other mismatches are literature errors. It does not establish that Debray obtained the erroneous arithmetic from Zhang or anyone else.

## 1. Symmetry and degree are the same

Debray, *Invertible phases for mixed spatial symmetries and the fermionic crystalline equivalence principle*, [arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3), revised 3 February 2026, Table 5 (p.52), prints Z2^3 for class A, spin-half, n=2 mod4. Theorem 4.82 (p.57) gives the corresponding bordism calculation. His D_{2n} has order 2n: n=2 and n=6 are our proper D2 and D6. Section 4.5.4 explicitly identifies this spin-half class-A problem with untwisted Spin^c bordism of BD_{2n}.

The local catalogue independently has s=rho=omega=0 for both physical spin-half inputs. This is the effective onsite background after the crystalline spin twist, not a claim that physical spin-half rotations commute before the crystalline correspondence. The symmetry assignment therefore matches the paper.

Spatial dimension three uses degree five Anderson duality:

    0 → Ext(Ω_4^SpinC(BG), Z) → classification
      → Hom(Ω_5^SpinC(BG), Z) → 0.

Finite G has no positive-degree rational group homology. Ω_5^SpinC(pt) vanishes, so Ω_5^SpinC(BG) is torsion and the Hom term is zero. The relevant finite group is precisely torsion in Ω_4, not Ω_3 or Ω_5. There is no extra degree-zero normalization factor.

## 2. The printed counting error

Put P=BZ2, V=Z2×Z2. Equation (4.59), p.49, gives

    ku ∧ P ∧ P ≃ (ku ∧ Σ²P) ∨ Σ²H(F2[u,v]),   |u|=|v|=2.

Theorem 4.82's proof, item (4), instead counts the Eilenberg–Mac Lane summand with dimension k−1 in every degree k≥2. Its actual degree-k basis consists of the monomials satisfying

    2 + 2a + 2b = k,  a,b≥0.

Consequently it has rank k/2 in positive even degrees k≥2 and zero rank in odd degrees. In degree four the two monomials are u and v. The printed proof inserts three factors there.

This count follows independently from Bruner–Mira–Stanley–Snaith, *Ossa's Theorem via the Kunneth Formula*, Mathematics and Statistics 3(3), 58–64 (2015), [arXiv:1008.0166](https://arxiv.org/abs/1008.0166), Theorem 2.12. At p=2 its Eilenberg–Mac Lane terms have degrees 2i+2j−2 with i,j>0. Exactly (i,j)=(1,2),(2,1) contribute in degree four. That theorem is an isomorphism of graded groups; using it requires no assumption about a spectrum-level realization of the algebraic splitting map.

The unreduced stable splitting contributes one sphere, two copies of P, and P∧P. Since reduced ku_even(P)=0,

    ku_4(BV) = Z ⊕ Z2²,
    ku_0(BV) = Z.

The sphere/degree-zero term occurs once. Adding a second degree-zero torsion factor cannot repair the printed result.

## 3. The low-degree Spin^c-to-ku comparison was checked independently

This audit did not merely assume Debray's invocation of Anderson–Brown–Peterson.

Hopkins–Hovey, *Spin cobordism determines real K-theory*, Math. Z. 210, 181–196 (1992), [DOI:10.1007/BF02571790](https://doi.org/10.1007/BF02571790), Section 2 (pp.3–5 of the accessible 1995 author preprint), describes the 2-local Spin^c splitting into Σ^{4|I|}ku, with all partitions I allowed, plus suspended HF2 terms. The manuscript full text is retained at `/home/arxiv/10.1007_bf02571790.pdf`.

A second independent source makes the needed range explicit: Buchanan–McKean, *KSp-characteristic classes determine Spin^h cobordism*, Algebraic & Geometric Topology 26 (2026), 485–551, [DOI:10.2140/agt.2026.26.485](https://doi.org/10.2140/agt.2026.26.485). Theorem 3.6, p.492, gives the Spin^c splitting, and Table 3, p.538, has no Spin^c coefficient torsion in degrees zero through nine. Hence no HF2 summand starts in degrees ≤7. Among partitions, only the empty partition and {1} start below degree eight. Thus, 2-locally,

    MSpinC = ku ∨ Σ⁴ku ∨ R,    R has no cells/homotopy below degree eight.

For every connective spectrum X, smashing cannot lower this connectivity. Therefore

    Ω_k^SpinC(X)_(2) ≅ ku_k(X)_(2) ⊕ ku_{k−4}(X)_(2),  k≤7.

This suffices for the degrees four and five used here. The paper's isolated phrase “degrees 8 and below” is unnecessary; no degree-eight claim is used. For V all reduced torsion is 2-primary. We therefore obtain

    Ω_4^SpinC(BV) = Z² ⊕ Z2²,
    classification(D2, spin-half) = Z2².

The calculation is interacting bordism. Connective ku is a mathematical splitting summand of that bordism spectrum; no free-fermion classification is inserted.

## 4. Independent differential check, with no ku splitting or expected table

The mod-two cohomology is F2[x,y], |x|=|y|=1. The nonzero integral charge class in H³(BV,Z)=Z2 is

    n3 = β(xy),   reduction(n3)=x²y+xy².

With the verified s=rho=omega=0 background, the obstruction is j Sq²(reduction(n3)), where j sends 1∈F2 to 1/2∈R/Z. Cartan's formula gives

    Sq²(x²y+xy²)=x⁴y+xy⁴,
    Sq¹Sq²(x²y+xy²)=x⁴y²+x²y⁴ ≠ 0.

The second line is the mod-two reduction of the integral Bockstein of the U(1) obstruction. Its nonzero value proves the obstruction itself is nonzero. The charge class cannot survive.

The remaining phase layer is H⁴(BV,R/Z)=Z2². Incoming degree-two integral charge parameters reduce to x²,y². Their square images x⁴,y⁴ have zero j-image: the associated integral Bockstein reductions vanish, and integral H⁵(BV,Z) has exponent two. CI incoming charge is zero because B3=0. Finally,

    H¹(BV,Z)=Hom(V,Z)=0,

so both integer CI and E8 sheet classes vanish. The four-data model therefore has only the two order-two phase generators. No stacking extension is available between surviving filtration layers.

New standalone verification `d2_polynomial_audit.py` imports no project modules and reads no classification tables. It checks the Cartan expressions, all 256 unnormalized bar tuples for integral closure, and independently constructs the normalized bar differential over F2. On its 729 degree-six cells, Gaussian elimination finds rank(d5)=179 and proves that the obstruction Bockstein is nonzero modulo boundaries and equals both the charge square and the displayed polynomial in cohomology. This is independent of GAP/HAP's native resolution.

The existing GAP audit was also rerun from current source with its full witness output retained as `d2_cochain_fresh.json`; it reproduced the nonzero charge obstruction, zero incoming phase images, and final Z2². The unit test `tests/test_backend_d2_audit.py` separately passed. These reruns confirm the current implementation rather than relying only on archived output.

## 5. Why D6 follows, including the odd prime

The order-twelve proper dihedral group has normal C3 quotient V. At the prime two, the Lyndon–Hochschild–Serre spectral sequence collapses along the normal odd-order subgroup, giving the same 2-primary bordism as BV. This can also be represented by restriction to the explicit Sylow-two complement. The exact catalogue audit freshly verifies the normal subgroup, quotient identification, representation traces, all signs, and extension restriction; see `odd_kernel_fresh.json`.

There is no hidden 3-primary torsion in Ω_4. At odd primes Spin^c is equivalent to SO bordism with the determinant-line BU1 factor. Below total degree five its coefficient groups occur in even degree. For D12, H2 and H4 have no odd-primary part: restrict to C3; its positive even integral homology vanishes. Thus all potential 3-primary contributions to total degree four vanish. Ω5 again has no free part by rationality. Therefore the same final group Z2² follows for D6.

Equivalently, for the explicit four-data calculation, restriction to the Sylow C3 sees no H¹(C3,Z), H³(C3,Z), or H⁴(C3,R/Z), so none of its 3D filtration layers can add a 3-primary factor. Naturality transports the two-primary obstruction and stacking relations.

## 6. Physical root check and limits

The project already identified a distinct problem with the real-space paper's named D2 spin-half odd-charge center root: orthogonal physical π-rotation lifts satisfy Rx Ry = (−1)^F Ry Rx. A nondegenerate one-dimensional center state has commuting scalar rotations, forcing even charge. Multiplying the rotations by U(1) phases does not remove their commutator. This rules out the named odd-charge root under that physical symmetry convention. It is consistent with the independent obstruction above, but is not by itself a full classification proof.

No E8 omission is responsible here: both groups are finite and proper, so the integer neutral E8 decoration group H¹(G,Z) is zero. These particular cases also avoid the project's unresolved physical identification of a nonzero CI kernel, because H¹(G,Z)=0 for the CI layer as well.

The corrected Z2² result is therefore highly supported for these two concrete symmetries. The remaining general qualification is the physical crystalline/bordism ansatz itself, shared with the comparison paper. No generator-by-generator equivalence between our two phase representatives and specific physical many-body Hamiltonians was constructed in this audit.

## 7. Evidence and changes from the previous audit

The degree mistake and its BMSS cross-check were already documented in the repository on 2026-10-14. This audit freshly checked canonical v3 bytes against pinned source hashes, independently justified the low-degree Spin^c comparison using two additional primary publications, verified the exact symmetry and degree-zero conventions, reran the cochain and D6 subgroup witnesses, and added an independent normalized-bar calculation.

- `debray_d2_provenance.json`: source/PDF/catalogue hashes; all three relevant canonical Debray TeX files equal pinned v3.
- `debray_ku_grading_fresh.json`: fresh existing seven-degree counting audit.
- `d2_cochain_fresh.json`, `odd_kernel_fresh.json`: fresh exact GAP witnesses.
- `fresh_d2_and_d6.g`, `.stdout`, `.stderr`: retained driver and logs.
- `d2_polynomial_audit.py`, `.json`: standalone polynomial/normalized-bar check.
- `bm_journal_page_10.png`, `bm_journal_page_56.png`: theorem and table pages inspected.

The original ABP DOI's automatic fulltext retrieval failed. We did not claim to have inspected that original paper. The full comparison used the independently retrieved Hopkins–Hovey primary research paper and Buchanan–McKean journal version instead. The accessible Hopkins–Hovey file is dated 25 July 1995 although the journal publication is 1992; this version distinction is recorded explicitly.
