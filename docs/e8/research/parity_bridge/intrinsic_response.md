# Intrinsic 4+1D Spin-c responses and their AHSS position

Date: 2026-10-15 UTC. All reduced decoration states use E8-first notation $(e_p,n_p,n_{p+2},\nu_{p+3})$, $p=d-2$. The intrinsic row below is additional data, denoted $r_0=(r_0^I,r_0^J)$; it is not hidden inside $e_2$ or $n_2$.

## 1. A primitive integral response basis

Let $c=c_1(L)$ be the determinant class of a Spin-c structure on a closed oriented six-manifold. The physical charge-one curvature has de Rham class $c/2$. Define

$$I=\int\frac{c^3-cp_1}{48},\qquad J=\int\frac{c^3}{2}.$$

$I$ is the Spin-c Dirac index, from $[\widehat A e^{c/2}]_6$. The determinant-line twist has index

$$\operatorname{Index}(D\otimes L)=\int\frac{27c^3-3cp_1}{48}=3I+J.$$

Thus **both** are integer-valued, without assuming $c$ is even or replacing a Spin-c background by a spin background. These are functions on Spin-c bordism. Freed–Hopkins v6 give $\Omega_5^{\mathrm{Spin}^c}=0$, $\Omega_6^{\mathrm{Spin}^c}=\mathbb Z^2$ and the interacting response group $\mathrm{TP}_5(\mathrm{Spin}^c)=\mathbb Z^2$; their free-fermion column is only $\mathbb Z$. We use the interacting column. Primary source: [arXiv:1604.06527v6](https://arxiv.org/abs/1604.06527v6), cached full TeX `positive.arxiv6.tex:6576–6613`, Eq. (74) and Eq. (115).

The basis is primitive, not merely a rational basis. These legitimate Spin-c manifolds give:

| Manifold and determinant | $\int c^3$ | $\int cp_1$ | $(I,J)$ |
|---|---:|---:|---|
| $A=(\mathbb{CP}^3,c=2h)$ | 8 | 8 | $(0,4)$ |
| $B=(\mathbb{CP}^2\times S^2,c=h+2u)$ | 6 | 6 | $(0,3)$ |
| $C=(\mathbb{CP}^3,c=4h)$ | 64 | 16 | $(1,32)$ |

The choices satisfy $c\bmod2=w_2$. The virtual bordism cycles $U=A-B$ and $V=C-32U$ have evaluations $(0,1)$ and $(1,0)$. Since the bordism group is torsion-free of rank two, $(I,J)$ identifies its full integral dual lattice. The inflow polynomial for the intrinsic response $(r_0^I,r_0^J)$ is

$$r_0^I\frac{c^3-cp_1}{48}+r_0^J\frac{c^3}{2}.$$

`check_intrinsic_lattice.py` records these exact evaluations and the source hash. Expressing $J$ as a difference of indices is an integrality argument; it does not turn the fixed-charge free-band classification into the interacting one or assert a particular microscopic construction.

## 2. Coefficient action and forgetting charge

The determinant class changes as $c\mapsto(-1)^{\rho_1+s_1}c$. Both six-form basis polynomials are odd in $c$. Incorporating the phase orientation/antiunitary sign $(-1)^{s_1}$ gives coefficient action $(-1)^{\rho_1}$. Hence the missing intrinsic module is

$$\mathbb Z_{\rho_1}^2.$$

For actual restriction to pure parity, take the map $\mathrm{Spin}\to\mathrm{Spin}^c$ with trivial determinant line. Both polynomials vanish at $c=0$. There is no residual torsion response: Freed–Hopkins have $\Omega_5^{\mathrm{Spin}}=\Omega_6^{\mathrm{Spin}}=0$ and $\mathrm{TP}_5(\mathrm{Spin})=0$ (`positive.arxiv6.tex:6439–6473`, Eqs. (84),(85)). Thus the intrinsic coefficient map to pure parity is zero.

This does **not** mean these responses disappear when the same symmetry is organized over $G_b=G_f/\mathbb Z_2^f$. For $G=1$, $G_f=U(1)^f$ and $G_b=U(1)_b$: the circle remains. The reduced state $(e_2,n_2,n_4,\nu_5)$ on $G=1$ is zero, but the full interacting group is still $\mathbb Z^2$. Matching the mixed gravitational term of $I$ to the p+ip anomaly $-p_1/48$ identifies its leading parity-sheet component on the circle as

$$n_2^{\rm SC}=c.$$

This is an odd circle Euler class, despite the even thermal map $2n_2+16e_2$ for pulled-back reduced decorations. $J$ has no mixed gravitational term and hence no such leading thermal component. These statements fix the indicated leading response components; they are not a completed lower/terminal cochain dictionary for the intrinsic generators. They show concretely why the complete correspondence must allow circle-dependent parity fields and a change of filtration.

The bosonic intrinsic $w_2w_3$ class is not an additional independent Spin-c coefficient: the integral lift of $w_2$ forces $w_3=0$ on ordinary Spin-c manifolds. For a nontrivial crystalline/tangential twist, its image requires a separate background-dependent analysis; it must not be appended as a universal extra $\mathbb Z_2$.

## 3. The extra AHSS row and the unknown operations

In the note's convention $d_r:(a,q)\mapsto(a+r,q-r+1)$, spacetime dimension five has total degree five. The new coefficient row is $q=5$, with initial uniform data

$$E_2^{0,5}=H^0(G,\mathbb Z_{\rho_1}^2).$$

If $\rho_1$ is nontrivial this invariant lattice is zero. If $\rho_1=0$ it begins as $\mathbb Z^2$, but invariance alone does not prove an equivariant lift. The possible outgoing slots are:

| Differential from $(0,5)$ | Target row | Status |
|---|---|---|
| $d_2$ | $(2,4)$ | Intrinsic spatial-dimension-three row is zero |
| $d_3$ | $(3,3)$, E8/CI coefficient $\mathbb Z_{s_1}^2$ | Requires the integral operation and its lift convention |
| $d_4$ | $(4,2)$ | Intrinsic spatial-dimension-one row is zero |
| $d_5$ | $(5,1)$, charge coefficient $\mathbb Z_{\rho_1}$ | Requires secondary operation after earlier trivializations |
| $d_6$ | $(6,0)$, phase coefficient $\mathbb R/\mathbb Z_{s_1}$ | Requires terminal operation after earlier trivializations |

These are page targets, subject to earlier quotients, not a claim that raw cohomology targets are unchanged on every page. There is no incoming differential to filtration zero. Nor can this new $q=5$ row introduce an incoming relation into an existing total-degree-five positive-filtration class: such an incoming source would have total degree four and therefore negative filtration in row five. Write $L=E_\infty^{0,5}\subseteq H^0(G,\mathbb Z_{\rho_1}^2)$ for the admissible intrinsic lattice. Under the full physical-spectrum identification and convergence of this filtration, the exact sequence is

$$0\longrightarrow F^1\longrightarrow E\longrightarrow L\longrightarrow0.$$

The current retained model can be identified with $F^1$ only after its own physical completeness is established. The lattice $L$ is free, so this Abelian extension splits abstractly: $E\cong F^1\oplus L$. A canonical splitting compatible with physical response coordinates does not follow. The missing outgoing operations determine the rank, index, and allowed generators of $L$; they are not an additional abstract extension obstruction. We do not infer that $L$ has rank two or finite index from invariance alone.

There is an exact **formal polynomial** transgression candidate in the unitary setting. Write $B=\beta\omega$, use the sign convention $d_3c=-2B$, and the two-dimensional response basis

$$\mathrm{IQH}=c^2/8-p_1/24,\qquad E_8=-p_1/3.$$

Differentiating the two polynomials gives

$$d_3^{\rm formal}I=-B\,\mathrm{IQH},\qquad
 d_3^{\rm formal}J=B(3E_8-24\,\mathrm{IQH}).$$

In E8-first coordinates the candidate matrix is $B\begin{pmatrix}0&3\\-1&-24\end{pmatrix}$. `check_intrinsic_lattice.py` verifies these polynomial coefficients exactly. **This is not a proved integral AHSS differential.** In particular $B$ is torsion for finite groups and disappears upon rationalization; the characteristic-form computation cannot by itself fix its integral normalization or exclude dyadic/background corrections. Signed backgrounds and higher $d_5,d_6$ require still more data. No such operation has been implemented or set to zero here.

For the user's rank-$\le4$ space-group scope, finite real cohomological dimension removes certain purely real high-degree targets, but it does not force the integral/torsion targets above to vanish. The intrinsic coefficient basis and its zero Spin restriction are settled; the full equivariant intrinsic-row operations remain an explicit mathematical work item.
