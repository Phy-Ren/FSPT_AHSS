# Prospective 4+1D interacting electronic calibration targets

These are independently specified **reference targets**, not reported classifier
runs. The machine-readable companion is [bordism_targets.json](bordism_targets.json).
All groups use interacting invertible-field-theory/bordism classification;
connective K-homology below appears only as a proven summand of Spin-c bordism.
No free-band classification or crystalline result table supplies a target.

The zero-uniform sector uses `(e2,n2,n4,nu5)`, including E8 decoration. The
intrinsic I,J response is recorded separately and is not an implemented general
intrinsic classifier. Internal symmetries have no crystalline spinless/spin-half
label. Translation-only symmetry has no nontrivial rotational spin lift.

| Priority | Exact symmetry/background | Zero-uniform target | Full target | Independent source and test |
|---|---|---|---|---|
| 1 | U(1)^f × C_N; s=rho=omega=0 | Cyclic formula below | Relative group × Z² | v0.15 Appendix K derives a faithful Spin-c eta pairing and complete physical presentation; tests sheet/charge gauges and stacking extensions |
| 1 | Unitary C, C²=(-1)^F; rho=alpha, s=0, omega=alpha²/2 | Z2³ | Z2³ | Derived Smith calculation below, using [FH, Theorem 9.87](https://arxiv.org/abs/1604.06527v6) and [Smith, Theorem 5.1/Corollary 5.8](https://arxiv.org/abs/2405.04649v2); tests the calibrated CI square and neutral sector |
| 1 | Unitary C, C²=1; rho=alpha, s=0, omega=0 | Z2 | Z2 | Same derivation with the other tangential twist; tests obstruction and incoming removal of the CI/charge/phase sector |
| 1 | AI, antiunitary T²=1; rho=0, s=alpha, omega=0 | 0 | Z² | [FH, Corollary 9.95](https://arxiv.org/abs/1604.06527v6); tests a vanishing zero-uniform group. Uniform image is 2Z{I}⊕2Z{J}, with the stronger labelled statement derived in v0.15 |
| 1 | AII, antiunitary T²=(-1)^F; rho=0, s=alpha, omega=alpha²/2 | 0 | Z² | [FH, Corollary 9.93](https://arxiv.org/abs/1604.06527v6); same abstract full rank as AI, but uniform image Z{I,J} |
| 2 | U(1)^f × (C2)²; s=rho=omega=0 | Z2² × Z4 × Z8² | Relative group × Z² | Derived below from [BMSS, Theorem 2.12](https://arxiv.org/abs/1008.0166v1) and [Buchanan–McKean, Theorem 3.6](https://doi.org/10.2140/agt.2026.26.485); first genuinely noncyclic finite benchmark |
| 2 | Four independent translations, G=Z⁴; s=rho=omega=0 | Z¹³ | Z¹⁵ | Stable splitting of T⁴ plus Spin-c coefficient phases; tests six E8, six CI, and one charge direction, with atomic filling retained |

## Cyclic targets and response scope

For g2=gcd(N,2), g3=gcd(N,3), the physical relative group is

\[
\mathbb Z_{N/(g_2g_3)}\oplus\mathbb Z_{N/g_2}
\oplus\mathbb Z_N\oplus\mathbb Z_{g_2^2g_3N}.
\]

The all-N physical proof is in the reviewed v0.15 Section 5/Appendix K.
Its actual complete-cochain comparisons cover exactly
`2,3,4,5,6,7,8,9,10,12,15,16,18`; this list is not an all-N cochain theorem.
The immediate controls are C2: Z2×Z8, C3: Z3²×Z9, C7: Z7⁴, and
C15: Z5×Z15²×Z45. In the specified E8-first roots, C15 has
`15X=5b, 15Y=10b, 15Q=15b=0`.

The proof uses actual charge-one and composite charge-three electronic anomaly
theories, lens eta evaluations, and an independent bordism AHSS order bound.
[Bahri–Gilkey (1987), Lemmas 2.2–2.3, pp.8–9](https://doi.org/10.2140/pjm.1987.128.1)
supplies product and lens eta input; their classification theorem itself is
restricted to cyclic 2-groups. [Hsieh (2018), §2.3](https://arxiv.org/abs/1808.02881v1)
supplies finite **charge-circle restriction** controls, a different symmetry
problem from adjoining commuting C_N. Neither paper is credited with the
package's new all-N electronic formula.

There is also a directly published **2-power** comparison, suitable for its
own reference column. Bahri–Gilkey Theorem 0.1(b) and the following Remark,
both on printed p.1, give `Omega5 = A5(N) + A1(N)` because the coefficient
torsion kernel vanishes here. For N=2^v, their explicit formula has
`A_(2k−1)(N) = sum_(1≤i<N) Z_(2^t)`, where
`2^s≤i<2^(s+1)` and `t=v−s+floor((k−i)/2^s)` if i≤k, otherwise t=0.
Setting k=3 and k=1 gives the following degree-five specialization:

| N | Bahri–Gilkey relative target |
|---|---|
| 2 | Z2 × Z8 |
| 4 | Z2² × Z4 × Z16 |
| 8 | Z4² × Z8 × Z32 |
| 16 | Z8² × Z16 × Z64 |

These are specializations of their published formula, not invented table
entries. Separately, Smith v2 Example 7.13 combined with FH Theorem 9.87
gives the C2 target Z8×Z2. Both source-specific answers are recorded in JSON.

## The two unitary charge-conjugation targets

Let E be the real plane over BO(2), L=det(E), and alpha=w1(E). All conditions
below refer to tangent bundles and chosen spin lifts, not just characteristic
class equalities.

* H−=(Spin×Pin−(2))/Z2 is the unitary C²=(-1)^F symmetry. Its structure is
  spin(TM⊕E⊕L), so w2(TM)=w2(E)+alpha². The Smith wall dual to alpha
  has spin(TY⊕E⊕2L), hence the Pin-tilde-c+ tangential structure.
* H+=(Spin×Pin+(2))/Z2 is the unitary C²=1 symmetry. Its structure is
  spin(TM⊕E⊕3L), so w2(TM)=w2(E). Its wall has the Pin-tilde-c− structure.

The sphere bundle S(L) is BSO(2); the restricted structure there is Spin-c.
The Smith exact sequence therefore gives

\[
0=\Omega_5^{\mathrm{Spin}^c}\longrightarrow\Omega_5^{H_\mp}
\longrightarrow\Omega_4^{\mathrm{Pin}^{\widetilde c\pm}}
\longrightarrow\Omega_4^{\mathrm{Spin}^c}=\mathbb Z^2.
\]

The middle-right groups are Z2³ and Z2. Their maps to Z² vanish, proving
the asserted Ω5 groups. Rationally H*(BO(2);Q)=Q[p1(E)] and the twists
E+L, E+3L are oriented; Ω6 has no rational part. Anderson duality thus
gives exactly the finite groups in the matrix, with no intrinsic free factor.
This is a derivation from primary theorems, not a copied 4+1D table entry.

[Debray–Ye–Yu v2, Proposition 6.27 and its proof, p.48](https://arxiv.org/abs/2312.13341v2)
independently identifies the Pin-tilde-c+ twist as 3E, equivalent to E+2L
for this purpose, and supplies wall generators. The RP5 background E=1+L
is valid for H− and detects the bosonic sign (-1)^(integral alpha^5). It
fails the H+ w2 condition. The exponent-two H− group rules out a CI square
equal to that nontrivial boson in the calibrated coordinates.

Before using these references, retain the following distinctions:

* Unitary charge conjugation C has s=0; it is not the AI/AII time-reversal
  operation T. Equal-looking C2 quotients do not identify their structures.
* Tangential and normal pin conventions can interchange signs. Use the
  displayed spin twists as the definitive dictionary.
* The current Smith paper is v2 (2026-04-19). Its Spin-c×C2 equivalence
  is **Example 7.13, p.36**, not the unversioned “Example 7.11” still cited
  in the supplied supplement. Theorem 5.1 and Corollary 5.8 remain valid
  locators. No correction to the H± targets was found.
* A local CI-root calibration is not a completed global four-data run.
  The physical total group includes the neutral contribution.

## A finite noncyclic target without a crystalline table

Put P=BC2. BMSS Theorem 2.12 gives the graded-group decomposition

\[
\widetilde{ku}_*(P\wedge P)
\cong\widetilde{ku}_{*-2}(P)
\oplus\bigoplus_{i,j>0}\pi_*(\Sigma^{2i+2j-2}H\mathbb F_2).
\]

Their Corollary 2.5 gives reduced ku_(2k+1)(P)=Z_(2^(k+1)). The
Eilenberg–Mac Lane terms have **even** degrees. Stable splitting of
(P×P)_+ therefore gives ku5(B(C2)²)=Z8²⊕Z4 and ku1(B(C2)²)=Z2².
The 2-local Spin-c splitting in Buchanan–McKean, Theorem 3.6, p.492,
together with Table 3, p.538, reduces through degree seven to
`MSpinC ≃ ku ∨ Σ⁴ku`; all other summands start in degree eight or above.
Thus

\[
\Omega_5^{\mathrm{Spin}^c}(B(C_2)^2)
=\mathbb Z_8^2\oplus\mathbb Z_4\oplus\mathbb Z_2^2.
\]

The reduced group is purely 2-primary. The full phase group also has the
two intrinsic free responses. This argument determines additive extensions
by actual graded-group isomorphisms, not by assuming AHSS collapse. In
particular the shifted ku1 term is necessary. It is not automatically a
canonical choice of pure E8 generators.

## Translation-only benchmark

For G=Z⁴, BG=T⁴ and the derivative action on R⁴ is trivial. The based
stable splitting

\[
\Sigma^\infty T^4_+\simeq
\bigvee_{k=0}^4\binom4k S^k
\]

is obtained by taking four smash products of `S1_+ ≃ S0 ∨ S1` in spectra.
Consequently the 4+1D phase group splits into the coefficient phase groups
in dimensions 5−k. Spin-c has TP5=Z², TP3=Z², TP1=Z, and TP4=TP2=0.
The result is Z²⊕Z¹²⊕Z=Z¹⁵. Removing the uniform TP5 summand leaves
Z¹³, with e2 rank6, n2 rank6, n4 rank1, and no degree-five phase class.

This uses the crystalline/generalized-cohomology framework for translations;
[Thorngren–Else v6, §III.C](https://arxiv.org/abs/1612.00846v6) explains the
crystalline-equivalence assumption on contractible space. It is a new
stable-splitting deduction from the coefficient data, not their printed
4D classification. Here positive filtration is free, so finite-group
averaging cannot be used. The n4 integer is charge per unit cell and is
retained in this benchmark. Quotienting out atomic filling changes the
question and removes one Z. The universal terminal R5/K4 comparison is
not asserted by this benchmark.

## Pinned sources

* FH: D. S. Freed and M. J. Hopkins, *Reflection positivity and invertible
  topological phases*, Geometry & Topology 25 (2021), 1165–1330;
  arXiv:1604.06527v6 (2022-12-18), Theorem 9.87/Table 9.88 and
  Corollaries 9.89, 9.93, 9.95. Use the interacting TP column.
* Smith: A. Debray, S. K. Devalapurkar, C. Krulewski, Y. L. Liu,
  N. Pacheco-Tallaj, R. Thorngren, *The Smith Fiber Sequence and Invertible
  Field Theories*, arXiv:2405.04649v2 (2026-04-19), CMP 407 (2026), 25.
* DYY: A. Debray, W. Ye, M. Yu, *Bosonization and Anomaly Indicators of
  (2+1)-D Fermionic Topological Orders*, arXiv:2312.13341v2 (2025-05-21).
  Only its proved bordism/twist calculation is used here.
* BMSS: R. Bruner, K. Mira, L. Stanley, V. Snaith, *Ossa's Theorem via
  the Kunneth formula*, arXiv:1008.0166v1 (2010-08-01), Corollary 2.5
  and Theorem 2.12; Mathematics and Statistics 3 (2015), 58–64.
* J. Buchanan and S. McKean, *KSp-characteristic classes determine Spin-h
  cobordism*, Algebraic & Geometric Topology 26 (2026), 485–551,
  DOI:10.2140/agt.2026.26.485, Theorem 3.6 and Table 3.
* R. Thorngren and D. V. Else, *Gauging spatial symmetries and the
  classification of topological crystalline phases*, arXiv:1612.00846v6
  (2017-09-12), Physical Review X 8 (2018), 011040.

Primary full texts were retrieved and inspected. The complete source and
model-calibration audit is retained externally in
`AllFSPT_reviews/v015_review_20261016/calibration_review.md` (2026-10-16).
