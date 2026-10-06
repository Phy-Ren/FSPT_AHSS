# Finite construction of the 3+1D terminal phase

This file defines the terminal obstruction and stacking correction in the
publication coordinate. Physical fields, obstruction equations, and products
are listed in the [3+1D formula section](../FORMULA_GUIDE.md#three-dimensional).
All parameter fields below are auxiliary mathematical cochains. Their degrees
do not change the physical roles of the fields in that section.

<a id="three-dimensional-pair"></a>

## Bosonic obstruction

The physical phase equation is

```math
d_{s_1}\widehat\nu_4=\widehat{\mathcal{𝒪}}_5.
```

Its obstruction is the following fixed finite sum, with the
[integration rule specified in Operations](OPERATIONS.md#parameter-integration):

<a id="eq-t3"></a>

**(T3)**

```math
\boxed{\widehat{\mathcal{𝒪}}_5=\tau_I\widehat{\mathcal{𝒪}}_6^I.}
```

## Bosonic stacking correction

The physical phase stacks as

```math
\widehat\nu_4^{\mathrm{out}}=\widehat\nu_4+\widehat\nu'_4+\widehat{\mathcal{ℰ}}_4.
```

The correction evaluates the same polynomial on the triangle fields:

<a id="eq-t3-product"></a>

**(T3 product)**

```math
\boxed{\widehat{\mathcal{ℰ}}_4=\tau_\triangle\widehat{\mathcal{𝒪}}_6^\triangle.}
```

## Polynomial evaluated in both formulas

The same degree-six polynomial is evaluated on the interval fields for
the obstruction and on the triangle fields for stacking:

<a id="eq-aux-terminal-source"></a>

**(Auxiliary phase source)**

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_6^J={}&\frac12\Big[\mathrm{Sq}^2 {n_4^J}+\omega_2 {n_4^J}+T_6[\check n_3^J;\omega_2,s_1]+\check n_3^J(\overline{\beta\omega_2}+s_1\omega_2)\\
 &\qquad +(\mathrm{Sq}^2\check n_3^J+s_1\mathrm{Sq}^1\check n_3^J+\omega_2\check n_3^J)
 \cup_4\mathcal{𝒪}_5^{\psi,J}+y_6[{n_2^J};\omega_2,s_1]\\
 &\qquad +\overline{\beta^\circ\check n_3^J}\cup_2\overline{B_4^{\psi,J}}
 +s_1(\overline{\beta^\circ\check n_3^J}\cup_3\overline{B_4^{\psi,J}})\Big]\\
 &+\frac14\big[B_4^J\cup_2B_4^J+B_4^J\cup_3dB_4^J+\omega_2 B_4^J\big]\\
 &-\frac14\overline{\big[\mathop{\mathrm{MS}}\nolimits_{12132434}
 (\overline{\beta_{s_1}\check\omega_2},\overline{\beta_{s_1}\check\omega_2},\overline{n_2^J},\overline{n_2^J})
 +\widetilde{\beta_{s_1}\check\omega_2}(\overline{n_2^J}\cup_1\overline{n_2^J})
 +(s_1\overline{\beta_{s_1}\check\omega_2})\widetilde{n_2^J}
 +s_1(\overline{\beta_{s_1}\check\omega_2}\cup_1s_1)\overline{n_2^J}\big]}\\
 &+\frac1{16}\mathcal P_{s_1}(\check\omega_2){n_2^J}
 +\frac18\check\omega_2 {n_2^J}^2+\frac1{12}{n_2^J}^3.
\end{aligned}
```

Its fields, residuals, and finite constituent formulas are specified below.

<a id="physical-field-evaluation"></a>
## Evaluation notation in the physical formulas

The main guide writes the same two fixed sums as
$`\mathop{\mathrm{ev}}\nolimits_5=\tau_I`$ for the obstruction and
$`\mathop{\mathrm{ev}}\nolimits_4=\tau_\triangle`$ for stacking. Both act on
a degree-six cochain. The subscript gives the output degree: the first
uses the six signed paths on an interval times a five-simplex; the second
uses the fifteen signed paths on a triangle times a four-simplex. Their
orientations and coefficient transports are exactly (O8).

The upward marks identify components of the **fixed lift of the complete
physical input**. The obstruction lift uses one input, whereas the stacking
lift uses both inputs and their displayed lower stacking corrections:

| Symbol in the physical formula | Obstruction evaluation | Stacking evaluation |
|---|---|---|
| $`\uparrow n_1`$ | $`n_2^I`$ | $`n_2^\triangle`$ |
| $`\uparrow\check n_2`$ | $`\check n_3^I`$ | $`\check n_3^\triangle`$ |
| $`\uparrow n_3`$ | $`n_4^I`$ | $`n_4^\triangle`$ |
| $`B_4^\uparrow`$ | $`B_4^I`$ | $`B_4^\triangle`$ |
| $`B_4^{\psi,\uparrow}`$ | $`B_4^{\psi,I}`$ | $`B_4^{\psi,\triangle}`$ |
| $`\mathcal{𝒪}_5^\psi[\uparrow n_1]`$ | $`\mathcal{𝒪}_5^{\psi,I}`$ | $`\mathcal{𝒪}_5^{\psi,\triangle}`$ |

Every entry on the right is defined explicitly below. In particular,
$`\uparrow\check n_2`$ and $`\uparrow n_3`$ include the mixed terms and
fixed cochain fills in those definitions. They are not independently
chosen linear suspensions of the individual fields. Backgrounds are pulled
from the physical base throughout.

This notation changes neither the cochains nor their representative. It
introduces no physical decoration or integer-lift convention. The arrow
components have degrees two, three, and four, with coefficients
$`\mathbb Z_{s_1},\mathbb Z_2,\mathbb Z_2`$, respectively. Products,
Bocksteins, and reductions inside the evaluation are formed before the
signed sum, using the arithmetic of the shared degree-six polynomial.
The fractional terms written outside the main guide's evaluation brackets
are precisely the signed identities in the final section below.

## Auxiliary integer residuals

The following residuals are untwisted integer cochains on the parameter
space. The definitions are local to the auxiliary fields:

<a id="eq-aux-residual"></a>

**(Auxiliary integer residuals)**

```math
\begin{aligned}
\check{\mathcal{𝒪}}_4^J&=\overline{n_2^J}^2+\check\omega_2\overline{n_2^J}
 \quad\text{in }\mathbb Z_2,\\
B_4^{\psi,J}&=\frac{\check{\mathcal{𝒪}}_4^J-{n_2^J}^2-\check\omega_2{n_2^J}}{2},\\
B_4^J&=\beta^\circ\check n_3^J+B_4^{\psi,J}
 =\frac{d\check n_3^J-{n_2^J}^2-\check\omega_2{n_2^J}}{2},\\
dB_4^J&=-(\beta_{s_1}\check\omega_2){n_2^J}.
\end{aligned}
```

## Auxiliary parameter fields

This construction uses cochains on an interval or triangle times the
physical base. They are **auxiliary**, not additional physical decorations.
A superscript $`J\in\{I,\triangle\}`$ always marks them: $`n_2^J`$ is
integer, while $`\check n_3^J,n_4^J`$ are binary. The physical $`n_2`$ in
this section remains Majorana decoration.

On the oriented triangle $`012`$, the integer one-cocycles
$`\theta_1,\theta'_1`$ have edge values $`(01,12,02)=(1,0,1),(0,1,1)`$.
The binary $`\chi_1`$ has values $`(0,0,1)`$ and satisfies
$`d\chi_1=\bar\theta_1\bar\theta'_1`$. Backgrounds and physical
fields are pulled from the base; parameter cochains are pulled from the
triangle. Integer parameter cochains act through their reductions inside
binary expressions.

<a id="eq-t3b"></a>

**(T3B)**

```math
\begin{aligned}
{n_2^\triangle}&={\theta_1} {n_{1}}+{\theta'_1} {n'_{1}},\\
{\check n_3^\triangle}&={\theta_1} {\check n_{2}}+{\theta'_1} {\check n'_{2}}+({\check\omega_2}\cup_1{\theta_1}){\bar n_{1}}
 +({\check\omega_2}\cup_1{\theta'_1}){\bar n'_{1}}+{\chi_1} {\check{\mathcal{ℰ}}_{2}}+{\theta_1}({\bar n_{1}}\cup_1{\theta'_1}){\bar n'_{1}},
\end{aligned}
```

For the interval, $`\theta_1(01)=1`$ and the second input is absent:

```math
n_2^I=\theta_1 n_1,\qquad
\check n_3^I=\theta_1\check n_2+(\check\omega_2\cup_1\theta_1)\bar n_1.
```

The following binary degree-five source is evaluated on these auxiliary
fields. Its superscript keeps it separate from the physical terminal
phase obstruction $`\widehat{\mathcal{𝒪}}_5`$:

<a id="eq-aux-o5"></a>

**(Auxiliary source)**

```math
\mathcal{𝒪}_5^J=\mathrm{Sq}^2\check n_3^J+s_1\mathrm{Sq}^1\check n_3^J
 +\omega_2\check n_3^J+\mathcal{𝒪}_5^{\psi,J}.
```

<a id="eq-aux-pip5"></a>

**(Auxiliary p+ip source)**

```math
\begin{aligned}
{\mathcal{𝒪}_5^{\psi,J}}={}&\zeta_{2,2}({\overline{n_2^J}},{\overline{n_2^J}})+\zeta_{2,2}({\check\omega_2},{\overline{n_2^J}})
 +{\overline{n_2^J}}^2\cup_3({\check\omega_2}{\overline{n_2^J}})+\mathrm{Sq}^3{\widetilde{n_2^J}}+{(\overline{n_2^J}\cup_1\overline{n_2^J})}\cup_1({s_1}{\overline{n_2^J}})\\
&+{s_1}\big[{\overline{n_2^J}}^2\cup_4({\check\omega_2}{\overline{n_2^J}})+({\overline{n_2^J}}\cup_1{s_1}){\overline{n_2^J}}+{\overline{n_2^J}}\cup_1{(\overline{n_2^J}\cup_1\overline{n_2^J})}+{\overline{n_2^J}}^2\big]\\
&+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\widetilde{n_2^J}}
 +\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\overline{n_2^J}},\\
\zeta_{2,2}(x,y)={}&\mathop{\mathrm{MS}}\nolimits_{1231343}(x,x,y,y).
\end{aligned}
```

The auxiliary complex-fermion fields now follow. Their complete
corrections are written directly, without additional named sum wrappers.

<a id="eq-t3a"></a>

**(T3A)**

```math
\begin{aligned}
n_4^\triangle={}&(\mathsf h_4^{(2)})^*\mathcal{𝒪}_5^\triangle\\
 &+\theta_1\big[n_3+\check\omega_2\widetilde n_1+\check n_2\cup_2d\check n_2+(s_1\cup_1\omega_2)\bar n_1\big]\\
 &+\theta'_1\big[n'_3+\check\omega_2\widetilde n'_1+\check n'_2\cup_2d\check n'_2+(s_1\cup_1\omega_2)\bar n'_1\big]\\
 &+\chi_1\Big(\mathcal{ℰ}_3+\Delta\big[\check\omega_2\widetilde n_1+\check n_2\cup_2d\check n_2+(s_1\cup_1\omega_2)\bar n_1\big]\Big)\\
 &+(d\chi_1)\Big[\widetilde n_1\bar n'_1+(\bar n_1+\widetilde n_1)\widetilde n'_1
 +\check{\mathcal{ℰ}}_2\cup_2(\check n_2+\check n'_2)+\check{\mathcal{ℰ}}_2\\
 &\qquad +(s_1\cup_1\bar n_1)(\bar n_1\cup_1\bar n'_1)
 +[s_1\cup_1(\bar n_1\cup_1\bar n'_1)](\bar n_1+\bar n'_1)\Big].
\end{aligned}
```

<a id="eq-t3c"></a>

**(T3C)**

```math
n_4^I=(\mathsf h_4^{(2)})^*\mathcal{𝒪}_5^I
 +\theta_1\big[n_3+\check\omega_2\widetilde n_1+\check n_2\cup_2d\check n_2+(s_1\cup_1\omega_2)\bar n_1\big].
```

All brackets defining these binary fields are evaluated modulo two.
The interval and triangle sums and their coefficient transports are fixed
in [Operations](OPERATIONS.md#parameter-integration).

## Signed fractional terms

The extra integer terms have the exact signed transgressions

| Auxiliary term | $`\tau_I`$ | $`\tau_\triangle`$ |
|---|---|---|
| $`\mathcal P_{s_1}(\check\omega_2)n_2^J`$ | $`\mathcal P_{s_1}(\check\omega_2)n_1`$ | $`0`$ |
| $`\check\omega_2(n_2^J)^2`$ | $`0`$ | $`-\check\omega_2 n_1n'_1`$ |
| $`(n_2^J)^3`$ | $`0`$ | $`0`$ |

These identities use the displayed interval/triangle fields and the fixed
coefficient transport, so the compact pair includes all fractional terms.

The operations $`T_6,y_6`$ are the finite operations of
[Finite cochain formulas for the bosonic obstruction](SOURCE_OPERATIONS.md), applied to the displayed
auxiliary fields. Each $`1/2`$ bracket is binary. Each $`1/4`$ bracket is
integer, with the barred polynomial reduced as a whole before its
implicit lift. The parameter integration then gives phases modulo one.
