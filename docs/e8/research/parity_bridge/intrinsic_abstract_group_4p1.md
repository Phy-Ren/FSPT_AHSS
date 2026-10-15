# Which intrinsic 4+1D gaps can change the abstract stacking group?

Date: 2026-10-15 UTC. Status: independently reviewed proof within the stated tangential-spectrum framework. This is an auxiliary abstract-group theorem, not completion of the required differential and stacking formulas. This note concerns **4+1D only**, and only the optional enlargement by an intrinsic coefficient row. It is not a missing part of the specified four-coordinate theory. Reduced states retain E8-first notation $(e_2,n_2,n_4,\nu_5)$; the extra uniform intrinsic coordinate is $r_0=(r_0^I,r_0^J)$.

The distinction is between the abstract Abelian group and its physical response coordinates. Under the symmetry-spectrum assumptions stated below, the intrinsic row contributes an abstract $\mathbb Z^2$ whenever $\rho_1=0$. Its uncomputed integral outgoing operations can restrict the response lattice to finite index, but cannot change that abstract contribution. This does not identify the implemented reduced cochain model with the full physical positive-filtration subgroup.

## 1. Scope and claim

Assume an ordinary discrete symmetry quotient

$$1\longrightarrow\Lambda\longrightarrow G\longrightarrow P\longrightarrow1,
\qquad\Lambda\cong\mathbb Z^r,\quad |P|<\infty,\quad r\le4,$$

with the specified fermionic $U(1)^f$ extension, signs $s_1,\rho_1$, and spatial tangent representation of finite holonomy. The circle action is $\chi=\rho_1+s_1$. Arbitrary projective magnetic-translation cocycles $\omega\in H^2(G,\mathbb R/\mathbb Z_\chi)$ are allowed, including irrational commutators. No splitting of this extension as a group is assumed.

Use the interacting generalized-cohomology/tangential-spectrum classification of symmetry-preserving invertible phases, with the actual symmetry type pulled back under restriction. The classification is by deformation classes with unrestricted allowed filling and response; imposing a fixed filling, fixed Hall response, or a fixed intrinsic sector is a different problem. Assume the indicated AHSS converges to this classification and has the stated intrinsic coefficient row. The already established coefficient basis is

$$I=\frac{c^3-cp_1}{48},\qquad J=\frac{c^3}{2},\qquad A=\mathbb Z_{\rho_1}^2.$$

Its integrality and primitivity, from the interacting Spin-c coefficient group, are proved in [intrinsic_response.md](intrinsic_response.md). This note does not substitute a free-band classification for that group.

Let $E$ be the full physical 4+1D stacking group and let

$$L=\operatorname{im}\bigl(E\longrightarrow H^0(G,A)\bigr)=E_\infty^{0,5}$$

be its admissible intrinsic response lattice. Write $F^1=\ker(E\to L)$ for the physical positive-filtration subgroup. The claim is

$$\rho_1=0:\qquad N\mathbb Z^2\subseteq L\subseteq\mathbb Z^2,
\qquad N=2^r|P|,$$

and hence

$$E\cong F^1\oplus\mathbb Z^2\quad(\rho_1=0),
\qquad E=F^1\quad(\rho_1\ne0).$$

The isomorphism is abstract and generally noncanonical. The inclusion bound is sufficient, not asserted to be minimal. The identification $F^1\cong$ the implemented reduced CI/E8 model remains a separate theorem to establish.

## 2. Both intrinsic generators extend on a finite-index translation subgroup

Choose $K=2\Lambda$. It is normal in $G$, has index $N=2^r|P|$, and is contained in the kernels of both sign characters. The spatial tangent representation is trivial on $K$. Thus the restricted symmetry has neither orientation nor circle-conjugation twist. The projective $U(1)$ extension can nevertheless remain non-split.

The ordinary coefficient sequence $0\to\mathbb Z\to\mathbb R\to\mathbb R/\mathbb Z\to0$ gives

$$\beta\omega|_K=0,$$

because $BK\simeq T^r$ and $H^3(T^r,\mathbb Z)\to H^3(T^r,\mathbb R)$ is injective. This handles irrational magnetic flux as well as finite-order projective extensions: a real cocycle lift exists, although the circle extension need not split as a group.

Let $G_b^K=G_f^K/\mathbb Z_2^f$ be the actual bosonic quotient of the restricted fermionic symmetry. Its classifying-space fibration is

$$BU(1)_b\longrightarrow BG_b^K\longrightarrow BK.$$

The only possible outgoing differential from the fiber Euler class $u\in H^2(BU(1)_b,\mathbb Z)$ in its ordinary Serre spectral sequence is

$$d_3u=\beta(2\omega|_K)=0,$$

up to the irrelevant overall sign convention. There are no other possible targets for this degree-two class. Consequently $u$ lifts to an integral class $c_0\in H^2(BG_b^K,\mathbb Z)$.

Let $w\in H^2(BG_b^K,\mathbb Z_2)$ be the parity-extension class. Its restriction to the circle fiber is $u\bmod2$. Therefore $w-(c_0\bmod2)$ restricts to zero on the fiber. The low-degree Serre sequence, using $H^1(BU(1),\mathbb Z_2)=0$, identifies this difference with the pullback of some $a\in H^2(BK,\mathbb Z_2)$. The class $a$ has an integral lift $\widetilde a$ because $H^3(BK,\mathbb Z)$ is torsion-free. Set

$$c=c_0+\pi^*\widetilde a;\qquad c\bmod2=w.$$

On the restricted tangential symmetry, a fermionic structure supplies the spin lift twisted by $w$. The integral lift $c$ therefore supplies a map of tangential classifying spaces $BH_K\to B\mathrm{Spin}^c$ over $BSO$, with determinant class $c$. This need not come from a group homomorphism $H_K\to\mathrm{Spin}^c$ or from a group character defining the line bundle. On the coefficient fiber this is the ordinary Spin-c structure. Pulling back the two intrinsic Spin-c theories $I,J$ produces restricted-symmetry phases with coefficient values $(1,0)$ and $(0,1)$.

This establishes surjectivity of the intrinsic edge map on $K$. It does **not** replace the projective magnetic-translation group by a direct-product group, and it does not require a microscopic construction at a prescribed particle density.

## 3. Transfer preserves the actual symmetry twist

The finite-index inclusion of full symmetry types induces a finite cover of their classifying spaces. The stable tangent representation on the cover is the pullback of the original one. The finite-cover transfer therefore gives a map of the corresponding Thom spectra, in the direction

$$MT H_G\longrightarrow MT H_K.$$

Composing a restricted-symmetry phase with this map gives a phase of the original symmetry. Equivalently, this is the finite-cover transfer for the full pulled-back parametrized phase spectrum. The finite fiber has zero vertical tangent, so this construction requires no new orientation choice. It does not discard the fermionic extension or treat the symmetry as an untwisted internal group.

For clarity, only the transfer's **coefficient edge** is needed. Pull the cover back to the coefficient fiber: it is the disjoint union of $N$ points. By the transfer's pullback property, the intrinsic coefficient of the transferred phase is the coset norm

$$a\longmapsto\sum_{gK\in G/K}g\cdot a.$$

The action on $A$ is $(-1)^{\rho_1(g)}$ on each of the two generators. When $\rho_1=0$, transferring the two phases constructed above gives intrinsic coefficients $N(1,0)$ and $N(0,1)$. Thus $N\mathbb Z^2\subseteq L$. Weak decorations produced by transfer are allowed and do not affect this conclusion.

This proof does not assert that transfer followed by restriction, or restriction followed by transfer, is multiplication by $N$ on the entire generalized-cohomology group. Only the coefficient-edge norm is used. If $\rho_1$ is nontrivial, $H^0(G,\mathbb Z_{\rho_1}^2)=0$ from the outset, so the uniform intrinsic quotient is absent.

Primary transfer reference: J. C. Becker and D. H. Gottlieb, *The transfer map and fiber bundles*, Topology **14** (1975), 1–12, [DOI:10.1016/0040-9383(75)90029-4](https://doi.org/10.1016/0040-9383(75)90029-4). The facts used here are the pullback property in §3, Eq. (3.2), and the finite-cover specialization in §4, pp. 6–7; the Thom version uses the pulled-back stable tangent bundle. The paper explicitly notes that the vertical tangent is zero for a finite cover. Full text is cached at `/home/arxiv/10.1016_0040-9383(75)90029-4.pdf`, SHA256 `3daa4b7004afb96e11b7f2f9514818771b2c5a2482b34c8f024206f687bbce60`. The argument above specifies its application to the actual twisted symmetry and the coefficient edge.

## 4. Consequences for the outgoing AHSS operations

The potentially nonzero outgoing operations from $(0,5)$ are $d_3,d_5,d_6$. Their precise integral normalization, secondary choices, and completed cochain representatives remain uncomputed. Nevertheless, the transfer construction proves that every element of $N\mathbb Z^2$ is a permanent cycle. Each successive surviving subgroup therefore has full rank two, and each outgoing operation has finite image on that subgroup. No operation can send an admissible intrinsic generator nontrivially into the free part of a target.

This explicitly covers the potentially free $H^3(G,\mathbb Z_{s_1}^2)$ target of $d_3$. It is not enough merely to observe that high-degree real cohomology vanishes. The finite-cover argument proves that the image of this particular differential on the intrinsic lattice is torsion. Higher-page quotients are respected because the transferred objects are actual completed phases, hence permanent cycles on every page.

The exact sequence

$$0\longrightarrow F^1\longrightarrow E\longrightarrow L\longrightarrow0$$

splits as a sequence of abstract Abelian groups because $L$ is free. Since $L$ has rank two for $\rho_1=0$, the unknown integral outgoing operations affect the embedding $L\subseteq\mathbb Z^2$, its index, and the smallest physical response generators, but not the abstract factor $\mathbb Z^2$. There is no additional torsion extension ambiguity from a free quotient.

Nor can this new $q=5$ row generate an incoming relation that kills a retained total-degree-five class: an incoming differential would have source total degree four, requiring negative filtration in row five. These statements concern the actual physical filtration; they do not certify a proposed cochain presentation of $F^1$.

## 5. Remaining work that can still change the final abstract answer

| Issue | Can change the abstract group? | What is actually necessary |
|---|---|---|
| Identification of the reduced CI/E8 model with physical $F^1$, including incoming phase identifications | Yes | A physical-spectrum/group equivalence, or an independent interacting calculation of the same group |
| Complete global shared-phase presentation and root powers | Yes; omitting relations or extensions gives a wrong model group | Compute the fixed model with all gauges, incoming maps, and stacking relations |
| Universal charged terminal comparison $R_{p+3}$ and product primitive $K_{p+2}$ | Their absence leaves one equivalence route unproved; it does not make the already fixed model product ambiguous | An abstract equivalence suffices if proved another way; explicit universal coordinates are not logically required |
| Intrinsic outgoing $d_3,d_5,d_6$ under the scope above | No additional abstract ambiguity after this transfer proof | Required for response normalization/index, not for the extra abstract free factor |
| Canonical splitting or explicit physical representatives of $L$ | No | Optional when only the abstract group is requested |

Source equality alone remains insufficient to identify physical stacking: a closed two-input correction can change an extension, as illustrated by $\mathbb Z_2\times\mathbb Z_2$ versus $\mathbb Z_4$ with the same two graded $\mathbb Z_2$ layers. Thus physical product compatibility cannot simply be omitted. What is optional is a particular explicit coordinate dictionary once an abstract equivalence has been established by another valid method.

This result answers the narrower abstract-group question for the optional enlarged sector. Complete intrinsic outgoing operations, secondary trivializations, and product/gauge compatibility would be required for that enlarged sector. They are not missing differentials of the specified four-coordinate theory, whose required $d_2,d_3,d_4$ and stacking/gauge formulas remain the current priority. The transfer theorem is an auxiliary consistency check and abstract-group fallback; it does not supply those formulas.
