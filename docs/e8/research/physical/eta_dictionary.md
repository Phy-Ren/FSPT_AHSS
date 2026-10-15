# 4+1D E8 physical calibration: the C3 lens-space generator dictionary

Date: 2026-10-15 UTC. This is an independent physical-calibration artifact. This review track changed no production code or supplied bundle; integration work by other tracks is separate.

The state notation is **E8 first**, `(e_p, n_p, n_{p+2}, nu_{p+3})`, with `p=d-2` and `d` the spatial dimension. Thus the relevant 4+1D state is `(e_2, n_2, n_4, nu_5)`. All actions below take values in `R/Z`; the partition function is their exponential with factor `2 pi i`.

The C3 calibration can be resolved. With the explicitly fixed lens orientation and flat line below,

\[
 b(L)=\frac13,\qquad X_{\rm geom}(L)=\frac79,
 \qquad X_\eta(L)=\frac19,
 \qquad X_\eta=X_{\rm geom}+b=4X_{\rm geom}.
\]

Here `X_geom=-C` is the geometric response with E8 anomaly sign `-p_1/3`. The inverse of the particular signature eta displayed by Saito–Tachikawa–Zhang is `X_eta`, a different lift of the same E8 decoration. Both obey `3X=b`. A sign convention alone does not identify these two lifts. The correction is a **named ordinary-phase shift**, not a change to the order-nine extension.

## 1. Primary definitions and the APS normalization

Saito, Tachikawa and Zhang (STZ), arXiv:2607.14662v2, define

\[
 C(M,a)=\int_W\frac{y p_1-y^3}{3},\qquad
 D(M,a)=\int_W y^3=\int_M a(\beta a)^2,
\]

where the flat circle line on the boundary may extend as a nonflat circle line on `W`; the finite-group bundle need not extend. Their Eq. (2.43) gives `3C=-D` for C3. Eq. (3.32) gives the twisted-signature density

\[
 S=\frac43y^3+\frac23yp_1=2C+2D.
\]

These are different response polynomials. STZ Appendix A.1 uses the particular representation `rho_1(g)=zeta` and obtains `eta=-1/9`. It uses eta to detect an order-nine class; it does not identify that eta character with `C`. [STZ, Eqs. (2.37), (2.40), (2.43), (3.32), (A.2)](https://arxiv.org/html/2607.14662v2)

The original source of that eta sum fixes the normalization. Gilkey defines

\[
 \bar\eta(P)=\frac{\eta(0,P)+\dim\ker P}{2}\pmod{\mathbb Z}
\]

on printed page 422. His Lemma 2.1(a), page 427, is the reduced-eta formula for the **full tangential signature complex**. Page 426 explains its even/odd decomposition; substituting only an even-form operator would require changing the formula. Thus the sum used by STZ is already the reduced APS eta. An additional division or multiplication by two would be incorrect. The standard APS formula is `index=integral-density - reduced-eta`. Gilkey's Theorem 2.5, page 432, independently supplies the corresponding lens-space characteristic-polynomial formula. [Gilkey, *Inventiones mathematicae* 76 (1984), 421–453, DOI 10.1007/BF01388468](https://doi.org/10.1007/BF01388468)

This also agrees with Gilkey's author-hosted book, *Invariance Theory, the Heat Equation, and the Atiyah–Singer Index Theorem*, first edition: Theorem 4.3.11, printed page 269; reduced eta at page 270; Lemmas 4.6.2–4.6.3, pages 296–297. The book and journal article were read separately, and their source bytes are pinned in `source_manifest.json`. [Author-hosted book PDF](https://pages.uoregon.edu/gilkey/dirPDF/InvarianceTheory1Ed.pdf)

## 2. An explicit bounding manifold, orientation and flat line

Let

\[
 W_N=D(\mathcal O(-N)\longrightarrow\mathbb{CP}^2),
 \qquad L_N=\partial W_N,
 \qquad h=c_1(\mathcal O(1)),\quad\int_{\mathbb{CP}^2}h^2=1.
\]

Give the base and disk fiber their complex orientations, and the boundary its outward orientation. Then `L_N` is the standard oriented quotient `S^5/C_N`, with scalar action `g:z -> zeta z`. One way to check the orientation is to begin with `N=1`: the boundary of the tautological disk bundle maps to the unit sphere by complex blowdown. On a fiber the map from `N=1` to general `N` is the degree-`N` power map, preserving orientation. We do not reverse the lens orientation later.

Let `U` be the integral Thom class. Its image in absolute cohomology is

\[
 j(U)=-Nh.
\]

Hence the unique rational relative lift of `h` is `-U/N`, and

\[
 \int_{W_N}h^3=-\frac1N.
\]

This is a **relative characteristic integral**, not the evaluation of an absolute degree-six class on the disk bundle. The latter retracts onto a four-dimensional base. The stable tangent splitting gives

\[
 TW_N\simeq\pi^*(T\mathbb{CP}^2\oplus\mathcal O(-N)),
 \qquad p_1(TW_N)=(3+N^2)h^2.
\]

Extend the boundary line as `E_s=pi^*O(s)` and choose its connection flat near the boundary. Such a connection exists because the restricted line is torsion. Since `H^1(L_N;R)=0`, there is no continuous flat-connection parameter left after fixing that torsion line. Setting `y=sh`, the relative integrals are

\[
 D_s=-\frac{s^3}{N},\qquad P_s:=\int yp_1=-\frac{s(N^2+3)}N,
 \qquad C_s=\frac{s^3-s(N^2+3)}{3N}.
 \tag{1}
\]

The representation convention is essential. In the explicit quotient

\[
 (z,v)\sim(gz,\rho_s(g)v),\qquad\rho_s(g)=\zeta^s,
\]

the line is `O(s)`: for `s=1`, evaluating a dual tautological vector on `z` transforms by `zeta`. Parallel transport along the path lifting from `z` to `gz` keeps the upstairs coordinate `v` fixed, so its return map in the original fiber is `rho_s(g)^{-1}`. Therefore the convention

\[
 a(g)=+\frac1N
\]

on that oriented loop selects **`s=-1`**. This is an explicit definition of loop/associated-bundle conventions, not a claim that other authors must call their representation parameter an inverse. It also fixes

\[
 \beta a=-h|_{L_N},\qquad
 b(L_N)=D_{-1}=+\frac1N.
\]

Equivalently, the oriented circle fiber has `a` period `1/N` and the base has `h^2` integral one, giving the same pairing of `a(beta a)^2`. This matches the chosen positive bar-phase period without an unstated orientation reversal.

## 3. Independent spectral and geometric computations

For the same standard scalar deck action, Gilkey's formula is

\[
 \bar\eta_s(L_N)=\frac1N\sum_{k=1}^{N-1}
 \zeta^{sk}\left(\frac{\zeta^k+1}{\zeta^k-1}\right)^3
 \pmod{\mathbb Z}.
 \tag{2}
\]

The untwisted sum `s=0` vanishes in dimension five by pairing `k` and `N-k`; at order two each term is zero. Thus subtracting the trivial representation, as in a reduced bordism character, leaves this value unchanged.

Applying APS with the density above to (1) gives independently

\[
 \bar\eta_s=\frac{4D_s+2P_s}{3}=2C_s+2D_s
 \pmod{\mathbb Z}.
 \tag{3}
\]

Gilkey's lens formula also yields (3) directly. The program `lens_calibration.py` computes (2) in the exact quotient field `Q[z]/Phi_N(z)` and separately computes (1) using rational characteristic numbers. It does not insert the expected eta value into the spectral calculation. For `N=2,3,4,5,6,9,12` and `s=-1,0,1`, all 21 signature comparisons agree modulo integers. For the nine spin Dirac comparisons described below, the independent formulas also agree. Raw integral and raw finite-sum values are saved separately, since they need not be equal as rational numbers.

For C3 these exact values are:

| Explicit line convention | `X_geom=-C` mod Z | `D` mod Z | Signature reduced eta mod Z | Raw finite sum |
|---|---:|---:|---:|---:|
| `s=-1`, flat transport `a(g)=+1/3` | `7/9` | `1/3` | `1/9` | `1/9` |
| `s=+1`, STZ representation weight `rho_1` | `2/9` | `2/3` | `8/9` | `-1/9` |

For example, at `s=-1` the raw values are `C=11/9`, `X_geom=-11/9`, `D=1/3`, and signature density integral `28/9`. The last differs from the spectral `1/9` by the integer three. No claimed equality of raw integrals is used.

Now fix the first row. Since `3C=-D`, writing `X_geom=-C` and `b=D` gives

\[
 3X_{\rm geom}=b,\qquad
 \bar\eta_{-1}=2C+2D=-2X_{\rm geom}+2b
 =4X_{\rm geom}=X_{\rm geom}+b.
 \tag{4}
\]

Also `eta_{-1}=-eta_{+1}` in this dimension. Thus negating STZ's displayed `-1/9` gives exactly the shifted root in (4), with no unresolved APS factor or orientation ambiguity left under the stated conventions.

## 4. Corrected physical prescription for the cochain roots

Write `c=beta a` for the cyclic carry. In E8-first state order the local roots under discussion are

\[
 X=(c,0,0,\tfrac13ac^2),\qquad
 I=(0,c,0,\tfrac16ac^2),\qquad
 b=(0,0,0,ac^2).
\]

A physical calibration must specify their differential/gravitational completion. For the **unshifted geometric convention**, define the neutral root response by

\[
 Z_{X_{\rm geom}}(M,a)
 =\exp\left(2\pi i\int_W\frac{y^3-yp_1}{3}\right),
 \qquad
 Z_b(M,a)=\exp\left(2\pi i\int_W y^3\right).
 \tag{5}
\]

The first term includes the displayed cubic completion; the second part includes the gravitational E8 response with the sign `-p_1/3`. A change of extension alters the action by an integer because the closed-manifold polynomial is integral. This is a calibrated physical map for these cyclic generators, not evaluation of `nu_5` alone.

If the application wishes instead to retain the old lens value `+1/9`, it must explicitly name that lift

\[
 X_\eta=X_{\rm geom}+b.
\]

Relative to (5), this adds the ordinary phase `ac^2` to the root, or changes its displayed local phase representative from `ac^2/3` to `4ac^2/3`. The same physical element written as

\[
 xX_\eta+kb=xX_{\rm geom}+(k+x)b
\]

has a shifted phase coordinate. A result should either use (5) and the value `7/9`, or explicitly use this shifted dictionary and the value `1/9`. The state-level stacking and gauge conventions must be transported with the change of root. The physical formula does not select an arbitrary unrecorded trivialization of every cochain representative on every group.

The v0.9 sentence at `note.tex:533` should therefore be replaced by the explicit dictionary (4)–(5). Its order-nine conclusion and `3X=b` survive. Its statement that the number follows from the inverse E8 anomaly sign alone is insufficient. This resolves the previously identified physical calibration gap on the chosen cyclic controls, without asserting a global realization theorem for the full local cochain model.

## 5. Two actual manifold detectors for the cyclic extension

For every `N`, (1) with `s=-1` yields

\[
 X_{\rm geom}(L_N)=-\frac{N^2+2}{3N},\qquad b(L_N)=\frac1N.
\]

On the separately oriented background `M_N=CP^2 x S^1` with flat holonomy `+1/N` along the circle, use `CP^2 x D^2` and a disk connection of flux `1/N`. Since `y^3=0` and `integral_CP2 p1=3`,

\[
 X_{\rm geom}(M_N)=-\frac1N,\qquad b(M_N)=0.
\]

These give the relation

\[
 NX_{\rm geom}=q_Nb,\qquad Nb=0,
 \qquad q_N=\frac{N(1-N^2)}3\pmod N.
\]

On `L_N` the difference of the unreduced expressions is the integer `-1`; on `M_N` it is also an integer. The two periods distinguish all `N^2` representatives with E8 coordinate `0<=e<N` and phase coordinate `0<=k<N`: the product background first determines `e`, then the lens determines `k`. The relation matrix therefore has invariant factors

\[
 \mathbb Z_N\oplus\mathbb Z_N\quad(3\nmid N),\qquad
 \mathbb Z_{N/3}\oplus\mathbb Z_{3N}\quad(3\mid N)
\]

for this generated reduced sector. The executable checks this pairing and the invariant factors for seven orders. At `N=2`, the lens alone gives `X_geom(L_2)=0`, while the product background gives `1/2`; this illustrates why one lens is not a universal completeness test.

The relation itself is global, not inferred merely from those two evaluations. On any oriented background, taking tensor powers of the same extending line gives

\[
 C(ka)=kC(a)-\frac{k^3-k}{3}D(a).
\]

For a flat C_N line, `Na=0`, so `C(Na)=0`; the displayed relation follows with the integer coefficient `q_N=N(1-N^2)/3`. Thus the response characters define a homomorphism from the presented cochain-root group. The two explicit manifold periods then prove that this homomorphism is injective on that generated sector. This argument does not replace a construction of the physical map for every cochain on a general group.

There is also an electronic strengthening for **split `U(1)^f x C_N`**. Every `W_N` is stably complex and hence Spin-c, with canonical determinant class `(3-N)h`; its boundary inherits a Spin-c structure for every `N`. The other detector `CP^2 x S^1` admits determinant class `h`, since `w_2=h mod 2`. Thus both oriented detectors lift to actual `Spin-c x BC_N` backgrounds. The neutral responses do not depend on the electromagnetic determinant connection, so their `N^2` distinct pairs of values remain distinct after this pullback. This proves injection of the generated neutral-plus-DW subgroup into the electronic response group. It does not require all these backgrounds to be spin or to have trivial determinant. It also does not quotient intrinsic electromagnetic or other invertible responses as trivial; such an additional quotient would be a different comparison. The restricted charged test in the next section deliberately uses only odd `N` and a trivial determinant.

Yang and Cheng independently obtain the same cyclic group pattern by an interacting block construction and the permutation anomaly of E8 edge theories; their Appendix B also writes precisely the polynomial in (5) as `S_3`. Their positive-chirality E8 root in Appendix A is separately named `x`; Appendix B records that `S_3` has `c_-=-8` under its unit-flux reduction. Thus the response polynomial and group pattern are compared here, while a bare identification of their named root `x` with `X_geom` is not assumed. [Yang–Cheng, arXiv:2303.00719v3, Appendices A–B; *Phys. Rev. B* 110, 045137 (2024)](https://arxiv.org/html/2303.00719v3)

## 6. Charged C3 check on a specified spin background

For odd `N`, `w_2(TW_N)=(3-N)h mod 2=0`, so the disk bundle itself is spin; the boundary has the unique spin structure. Set the electromagnetic Spin-c determinant line to be trivial and retain the independent internal flat C_N line. The unit complex fermion's index density restricted to this background is

\[
 I_s=\int_W[\widehat A(TW)e^y]_6
 =\frac{D_s}{6}-\frac{P_s}{24}
 =\frac{s(N^2+3-4s^2)}{24N}.
\]

Gilkey's Lemma 2.1(c) computes the same reduced spin Dirac eta using the unique odd-order spin lift. The exact code uses `sqrt(zeta)=zeta^{(N+1)/2}` and the independent sum

\[
 \frac1N\sum_{k=1}^{N-1}
 \frac{\zeta^{k(s+3(N+1)/2)}}{(\zeta^k-1)^3}.
\]

For `N=3,s=-1`, both give `I=-1/9=8/9 mod Z`, and hence

\[
 3I=\frac23=2b,\qquad 3(X_{\rm geom}+I)=0.
\]

This is an actual geometric consistency check on the charged relation, independent of the supplied CI evaluator. It is not a full charged Spin-c classification: the electromagnetic connection has deliberately been restricted, and one lens does not distinguish every charged/neutral combination. Replacing `X_geom` by `X_eta=X_geom+b` leaves the displayed triple relation true, so that relation alone could not have fixed the neutral phase shift.

## 7. Scope and remaining obligations

- The C3 eta/generator ambiguity is resolved under explicit orientation, line, operator and APS conventions. The geometric prescription is reproducible.
- The cyclic tests calibrate the reduced oriented bosonic E8-plus-DW sector; they do not add the intrinsic unoriented or purely gravitational sectors of a different theory. Their spin restriction shows the neutral order-nine response is nonzero on a legitimate electronic background.
- The charged check uses a specified restricted background. It is not a proof of the entire general-discrete-group cochain realization.
- Space groups can restrict to these finite/internal controls, but passing the controls does not establish naturality, incoming identifications or completeness on every infinite crystallographic group. Those are separate mathematical and implementation obligations.
- No validation here relies on Jian-Hao Zhang's point-group tables, free-fermion classification alone, or an assumed equality of groups after removing unnamed factors.

Reproduction: run `python lens_calibration.py` in this directory. The dimension-pinned output is `calibration_4p1.json`; it records 30 exact index comparisons, seven two-manifold cyclic controls and the C3 root dictionary. The original source PDFs and selected visual formula checks are in `sources/`.

Other dimensions are kept in separate documents and data files: [3+1D mirror control](mirror_3p1.md) and [2+1D uniform coefficient dictionary](coefficient_2p1.md). No table or classification cell in this document combines dimensions.
