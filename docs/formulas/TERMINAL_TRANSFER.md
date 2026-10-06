# Finite binary transfer in the 4+1D product

This appendix defines the binary five-cochain $`Z_5`$ in (T4d) of the
[formula guide](../FORMULA_GUIDE.md#four-dimensional-pair). The inputs are
$`(n_2,\check n_3)`$ and $`(n'_2,\check n'_3)`$, with common backgrounds
$`\omega_2,s_1`$. Primes always label the second stacking input; $`N_2,\check
N_3`$ are the output. Bars, digit superscripts, tildes, and checks have the
same meanings as in the guide.

The definitions below are in evaluation order. The only additional named
operations are substantial polynomials or geometric sums:

| Operation | Degree and role | Definition |
|---|---|---|
| $`\mathcal J_6`$ | Binary degree-six correction to the shared $`\mathcal H_6`$ | (K1) |
| $`I_6`$ | Even integral degree-six numerator | (K2) |
| $`\rho_6`$ | Binary degree-six transfer kernel | (K3) |
| $`L^s_5,L^0_5,L^\star_5,L_5`$ | Binary degree-five tensor coefficients, separated by background degree | (K6), (K9), (K11) |
| $`P_i^{L},P_i^{R}`$ | Binary tetrahedral polynomials | (K8) |
| $`\mathcal Q^{\rm int}_5,K^-_5,A^{\rm pair}_4,G^0_5,D^0_5`$ | Degree-indexed pieces of the zero-background integer carry | (K10) |
| $`Z_5`$ | Binary degree-five finite transfer | (K12) |

The lower correction $`\mathcal E_4`$, its shifted predecessor
$`\check{\mathcal E}_3=\bar n_2\cup_1\overline{n'_2}`$, the carry $`B_4`$,
$`\lambda_3`$, and $`\Delta B_4=d\lambda_3-n'_2n_2`$ are already defined in
the guide. For any one-input expression the signed difference is
$`\Delta X=X[N_2,\check N_3]-X[n_2,\check n_3]-X[n'_2,\check n'_3]`$.
As elsewhere, $`B'_4=B_4[n'_2,\check n'_3]`$ and an unlabelled $`B_4`$ refers
to the first input. All products remain ordered.

## The binary kernel

Define

<a id="eq-k1"></a>

**(K1)**

```math
\mathcal J_6[n_2,\check n_3]
 =\mathcal H_6[n_2,\check n_3]
 +\bar n_2\overline{B_4}
 +(\bar n_2\cup_1\overline{\beta_{s_1}\check\omega_2})\bar n_2.
```

First form the entire integer expression

<a id="eq-k2"></a>

**(K2)**

```math
\begin{aligned}
I_6={}&\Delta(B_4\cup_2B_4+B_4\cup_3dB_4)
 +\widetilde{\omega_2}\,\Delta B_4-\Delta\widetilde{\mathcal C_6}\\
&+\widetilde{\check\omega_2}(n'_2n_2)
 +(\beta_{s_1}\check\omega_2)(n_2\cup_1n'_2)
 -d_{s_1}\widetilde{\mathcal V_5}.
\end{aligned}
```

It is pointwise even. The kernel is

<a id="eq-k3"></a>

**(K3)**

```math
\begin{aligned}
\rho_6={}&
 \mathrm{Sq}^2(\mathcal E_4+\bar n_2\overline{n'_2})
 +\omega_2(\mathcal E_4+\bar n_2\overline{n'_2})\\
&+\mathcal O_5[n_2,\check n_3]\cup_4
 \mathcal O_5[n'_2,\check n'_3]\\
&+\big(\mathcal O_5[n_2,\check n_3]
 +\mathcal O_5[n'_2,\check n'_3]\big)
 \cup_3(\mathcal E_4+\bar n_2\overline{n'_2})\\
&+(\mathcal E_4+\bar n_2\overline{n'_2})\cup_3
 \big(\mathcal O_5[n_2,\check n_3]
 +\mathcal O_5[n'_2,\check n'_3]\big)\\
&+\mathcal J_6[N_2,\check N_3]
 +\mathcal J_6[n_2,\check n_3]
 +\mathcal J_6[n'_2,\check n'_3]\\
&+\overline{I_6/2}
 +\check\omega_2\,d\check{\mathcal E}_3
 +\overline{\beta_{s_1}\check\omega_2}\,\check{\mathcal E}_3.
\end{aligned}
```

Every derivative differentiates a specified expression. In particular,
$`d\overline{B_4}=\overline{\beta_{s_1}\check\omega_2}\bar n_2`$ and
$`d\check{\mathcal E}_3=\bar n_2\overline{n'_2}+\overline{n'_2}\bar n_2`$.
The free complex-fermion solutions $`n_4,n'_4`$ do not enter this kernel.

## Shared-background coordinates

Use $`D`$ only for the degree of a simplex in this appendix. A graded
simplex consists of the common backgrounds and two graded inputs:

```math
\begin{gathered}
S=(s_1,\omega_2;
 n_2^{\rm gr},\check n_3^{\rm gr};
 n_2^{{\rm gr}\prime},\check n_3^{{\rm gr}\prime}),\\
dn_2^{\rm gr}=dn_2^{{\rm gr}\prime}=0,\qquad
d\check n_3^{\rm gr}=(\overline{n_2^{\rm gr}})^2,\qquad
d\check n_3^{{\rm gr}\prime}=(\overline{n_2^{{\rm gr}\prime}})^2.
\end{gathered}
```

The superscript $`{\rm gr}`$ denotes the untwisted coordinates relative to
the simplex's first vertex. It does not change the cochain degree. Decode
the first input by

<a id="eq-k4"></a>

**(K4)**

```math
\begin{aligned}
n_2(ijk)&=(-1)^{s_1(0i)}n_2^{\rm gr}(ijk),\\
\check n_3(ijkl)&=\check n_3^{\rm gr}(ijkl)
 +\begin{cases}
 0,&i=0,\\
 \check\omega_2(0ij)\bar n_2(jkl),&i\gt0.
 \end{cases}
\end{aligned}
```

Apply the same rule to the primed input and take $`s_1(00)=0`$. Encoding is
the inverse of (K4). Positive faces and degeneracies are factorwise. The
actual zeroth face is obtained by decoding, restricting to
$`[1,\ldots,D]`$, and re-encoding with vertex $`1`$ as root. Relative to the
factorwise zeroth face its changes are

<a id="eq-k5"></a>

**(K5)**

```math
\begin{aligned}
n_2^{\rm gr}&\longmapsto(-1)^{s_1(01)}n_2^{\rm gr},\\
\check n_3^{\rm gr}(ijkl)&\longmapsto\check n_3^{\rm gr}(ijkl)
 +[\check\omega_2(01i)+\check\omega_2(01j)]\bar n_2(jkl).
\end{aligned}
```

These formulas apply for $`1\le i\lt j\lt k\lt l\le D`$ and to the primed
input as well. Let $`\delta S`$ be the binary sum of the actual and
factorwise zeroth faces, extended linearly to binary chains. The root in
(K4) is a coordinate choice on each simplex, not a global trivialization of
either background; its failure on the zeroth face is precisely (K5).

## The tensor coefficient

Write $`L_5=L^\star_5+L^s_5`$. Its antiunitary term uses the integer digit
rule from the guide, $`\bar x^{[j]}=\overline{\lfloor x/2^j\rfloor}`$:

<a id="eq-k6"></a>

**(K6)**

```math
\begin{aligned}
f(x,y)={}&(\bar x+\bar x^{[1]})\bar y^{[1]}(1+\bar y)
 +\bar x^{[1]}(\bar y+\bar y^{[2]})
 +\bar x^{[2]}\bar y(1+\bar y^{[1]}),\\
L^s_5(S)={}&s_1(01)
 f(n_2^{\rm gr}(123),n_2^{{\rm gr}\prime}(345)).
\end{aligned}
```

These are graded integer values. Equivalently, the same scalar polynomial
can be written directly in integer binomials:

<a id="eq-k7"></a>

**(K7)**

```math
\begin{aligned}
f(x,y)={}&
 \left(\overline{\binom x1}+\overline{\binom x2}\right)
 \left(\overline{\binom y2}+\overline{\binom y3}\right)\\
&+\overline{\binom x2}
 \left(\overline{\binom y1}+\overline{\binom y4}\right)\\
&+\overline{\binom x4}
 \left(\overline{\binom y1}+\overline{\binom y3}\right).
\end{aligned}
```

### Eight tetrahedral polynomials

For one zero-background input $`(n_2,\check n_3)`$ on $`0123`$, define three
local integer face coordinates:

```math
n_{2;012}=n_2(012),\qquad
n_{2;013-012}=n_2(013)-n_2(012),\qquad
n_{2;123}=n_2(123).
```

The indices after the semicolon specify the face or difference of faces.
Applying the same bar and digit rules gives all bits needed below.
Products in (K8) are ordinary products of bits on this tetrahedron, and
$`\check n_3(0123)`$ is the binary Majorana value on the same face:

<a id="eq-k8"></a>

**(K8)**

```math
\begin{aligned}
P^L_1={}&
 (\bar n_{2;012}+\bar n_{2;013-012})
 (\bar n_{2;123}+\bar n_{2;123}^{[1]})\\
&+\check n_3(0123)\big[
 1+\bar n_{2;012}+\bar n_{2;013-012}+\bar n_{2;123}
 +\bar n_{2;013-012}\bar n_{2;123}(1+\bar n_{2;012})\\
&\qquad+(\bar n_{2;012}+\bar n_{2;013-012})
 (\bar n_{2;012}^{[1]}+\bar n_{2;013-012}^{[1]}+\bar n_{2;123}^{[1]})
 +\bar n_{2;123}\bar n_{2;123}^{[1]}\big],\\
P^L_2={}&
 (\bar n_{2;013-012}+\bar n_{2;013-012}^{[1]})
 (\bar n_{2;012}+\bar n_{2;123})\\
&+\bar n_{2;013-012}\big[
 \bar n_{2;012}^{[1]}(1+\bar n_{2;123})
 +\bar n_{2;123}^{[1]}(1+\bar n_{2;012})\big],\\
P^L_3={}&P^L_2
 +\bar n_{2;013-012}^{[1]}(\bar n_{2;012}^{[1]}+\bar n_{2;123}^{[1]})\\
&+\check n_3(0123)\big[
 \bar n_{2;012}+\bar n_{2;013-012}+\bar n_{2;123}
 +\bar n_{2;123}(\bar n_{2;012}+\bar n_{2;013-012})\\
&\qquad+(\bar n_{2;012}+\bar n_{2;013-012})
 (\bar n_{2;012}^{[1]}+\bar n_{2;013-012}^{[1]}+\bar n_{2;123}^{[1]})
 +\bar n_{2;123}\bar n_{2;123}^{[1]}\big],\\
P^L_4={}&
 \bar n_{2;013-012}^{[1]}(\bar n_{2;012}^{[1]}+\bar n_{2;123}^{[1]})\\
&+\bar n_{2;013-012}\big[
 \bar n_{2;012}(1+\bar n_{2;123}+\bar n_{2;012}^{[1]}+\bar n_{2;013-012}^{[1]})
 +\bar n_{2;123}(\bar n_{2;013-012}^{[1]}+\bar n_{2;123}^{[1]})\big],\\
P^R_4={}&\bar n_{2;013-012}\bar n_{2;123}(1+\bar n_{2;012}),\\
P^R_2={}&P^R_4
 +\bar n_{2;013-012}^{[1]}(\bar n_{2;012}^{[1]}+\bar n_{2;123}^{[1]}),\\
P^R_3={}&
 \bar n_{2;013-012}^{[1]}(\bar n_{2;012}^{[1]}+\bar n_{2;123}^{[1]})
 +\bar n_{2;012}\bar n_{2;123}(\bar n_{2;013-012}^{[1]}+\bar n_{2;123}^{[1]})\\
&+\bar n_{2;013-012}(
 \bar n_{2;012}\bar n_{2;013-012}^{[1]}+\bar n_{2;012}^{[1]}\bar n_{2;123})\\
&+\check n_3(0123)\big[
 \bar n_{2;012}+\bar n_{2;013-012}+\bar n_{2;123}\\
&\qquad+(\bar n_{2;012}+\bar n_{2;013-012}+\bar n_{2;123})
 (\bar n_{2;012}^{[1]}+\bar n_{2;013-012}^{[1]}+\bar n_{2;123}^{[1]})
 +\bar n_{2;012}\bar n_{2;013-012}\bar n_{2;123}\big],\\
P^R_1={}&P^R_3+\bar n_{2;012}\bar n_{2;123}(1+\bar n_{2;013-012})\\
&+\check n_3(0123)\big[
 1+\bar n_{2;012}+\bar n_{2;013-012}+\bar n_{2;123}
 +\bar n_{2;012}\bar n_{2;123}(1+\bar n_{2;013-012})\big].
\end{aligned}
```

Rows referenced on the right use the same input and face. In particular,
$`\bar n_{2;013-012}^{[1]}`$ is the second bit of the integer
difference; it is not the sum of the second bits of $`n_2(013)`$ and
$`n_2(012)`$. Define the ordered-cup polynomial

<a id="eq-k9"></a>

**(K9)**

```math
L^0_5[n_2,\check n_3;n'_2,\check n'_3]
 =\sum_{i=1}^4\left[
 \overline{\binom{n_2}{i}}\,P^L_i[n'_2,\check n'_3]
 +P^R_i[n_2,\check n_3]\,\overline{\binom{n'_2}{i}}
 \right].
```

### The balanced integer carry

Only in this subsection set $`\omega_2=s_1=0`$, so
$`dn_2=dn'_2=0`$, $`d\check n_3=\bar n_2^2`$, and
$`d\check n'_3=(\overline{n'_2})^2`$. Evaluate the guide's
$`B_4,B'_4,\Delta B_4,\lambda_3`$ at these backgrounds. Form

<a id="eq-k10"></a>

**(K10)**

```math
\begin{aligned}
\mathcal Q^{\rm int}_5={}&
 B_4\cup_3B'_4+(B_4+B'_4)\cup_3\Delta B_4
 +\lambda_3\cup_1\lambda_3+\lambda_3\cup_2d\lambda_3
 +(n'_2n_2)\cup_3d\lambda_3\\
&+\zeta^{\mathbb Z}_{2,2}(n'_2,n_2)
 -\binom{n'_2}2(n_2\cup_1n_2),\\
K^-_5={}&(n_2+2n'_2)(n_2\cup_1n'_2)
 +(n_2\cup_1n'_2)(2n_2+n'_2),\\
A^{\rm pair}_4={}&
 \check n'_3\cup_1\bar n_2
 +\overline{n'_2}\cup_1\check{\mathcal E}_3
 +\mathop{\mathrm{MS}}\nolimits_{23123}
 (\bar n_2,\overline{n'_2},\overline{n'_2}),\\
G^0_5[n_2,\check n_3]={}&
 \frac12\widetilde{\check n_3\bar n_2}
 +\frac14n_2\widetilde{\check n_3},\\
D^0_5={}&\overline{\frac{
 \mathcal Q^{\rm int}_5-3K^-_5
 -\widetilde{\mathcal V_{5,0}}-d\widetilde{A^{\rm pair}_4}
 -4\Delta G^0_5}{2}}.
\end{aligned}
```

The integer face polynomial is

```math
\zeta^{\mathbb Z}_{2,2}(n'_2,n_2)(012345)
 =n'_2(012)n'_2(023)n_2(235)n_2(345).
```

$`\mathcal V_{5,0}`$ means (T4b) evaluated at $`\omega_2=s_1=0`$.
The difference $`\Delta G^0_5`$ uses the zero-background output
$`(N_2,\check N_3)`$ and the two inputs, in that order. The whole numerator
defining $`D^0_5`$ is even. Retain the displayed integer lift of
$`\check n_3\bar n_2`$ when forming $`4\Delta G^0_5`$; taking a phase modulo
one earlier would discard the required carry.

Now define

<a id="eq-k11"></a>

**(K11)**

```math
L^\star_5=L^0_5+\mathop{\mathrm{AW}}\nolimits^*
\big[(\mathop{\mathrm{sh}}\nolimits^*D^0_5)_{2,3}
 +(\mathop{\mathrm{sh}}\nolimits^*D^0_5)_{3,2}\big].
```

This notation is a finite rule: for $`(p,q)=(2,3)`$ and $`(3,2)`$, use the
front $`p`$-face and back $`q`$-face of a five-simplex, sharing vertex $`p`$.
Enumerate the ten paths from $`(0,p)`$ to $`(p,5)`$. Pull the two complete
zero-background inputs along coordinates one and two, evaluate $`D^0_5`$,
and sum modulo two. Add the two sums to $`L^0_5`$. On a graded simplex,
$`L^\star_5`$ uses its two graded inputs at background degree zero, while
(K6) uses the background-degree-one component. These prescriptions define
$`L_5`$ on every simplex appearing below.

<a id="transfer"></a>
## The six-slot formula

Let $`\mathsf h^{(3)}`$ denote the three-factor grid homotopy, whose component
in degree $`D`$ is $`\mathsf h_D^{(3)}`$ from (O11). Order its factors as
$`(\text{common background},\text{first input},\text{second input})`$.
For grid vertices $`(r_i,t_i,v_i)`$, pull both $`s_1,\omega_2`$ along $`r`$,
the complete graded pair $`(n_2^{\rm gr},\check n_3^{\rm gr})`$ along $`t`$,
and $`(n_2^{{\rm gr}\prime},\check n_3^{{\rm gr}\prime})`$ along $`v`$.
After pulling back, decode (K4) before evaluating $`\rho_6`$.

Encode the physical input as a graded five-simplex $`S`$. The required term is

<a id="eq-k12"></a>

**(K12)**

```math
\boxed{Z_5(S)=\sum_{j=0}^{5}\left[
 \rho_6\big(\mathsf h^{(3)}(\delta\mathsf h^{(3)})^jS\big)
 +L_5\big((\delta\mathsf h^{(3)})^jS\big)
 \right]\pmod2.}
```

Evaluation on a binary chain means the sum over its normalized simplices.
Cancel equal simplices before evaluating the source. The bound $`j\le5`$
is finite: each nonzero $`\delta\mathsf h^{(3)}`$ lowers the background
skeletal filtration, whose degree here is at most five. All face rules,
grids, polynomials, and division operations used in (K12) have been specified
above; no group-dependent primitive solver is needed.
