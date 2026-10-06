# FSPT obstruction and stacking formulas

Read the conventions once, then use the complete section for the desired
spacetime dimension: [3+1D](#three-dimensional) or [4+1D](#four-dimensional).
The notation is deliberately local to each dimension. A subscript records
a cochain's degree; its physical meaning is fixed by that section's field
table. In particular, the two sections do not share a physical field named
$`n_2`$.

The input backgrounds are $`\omega_2\in Z^2(G_b,\mathbb Z_2)`$ and
$`s_1\in Z^1(G_b,\mathbb Z_2)`$. They are fixed during stacking.
[Closed-Majorana formulas and lower-dimensional endpoints](formulas/MAJORANA_AND_ENDPOINTS.md)
also have separate dimensional sections.

<a id="conventions-and-coordinates"></a>
## Common notation and arithmetic

A prime denotes the second stacking input. The outputs are $`N_j`$ and
$`\nu_j^{\mathrm{out}}`$. A hat denotes the additive phase,
$`\nu_j=\exp(2\pi i\widehat\nu_j)`$, with
$`\widehat\nu_j\in\mathbb R/\mathbb Z`$. The same convention applies to
phase obstructions $`\widehat{\mathcal O}`$ and corrections
$`\widehat{\mathcal E}`$.

A bar means pointwise reduction modulo two. Binary digits use this same
operation:

```math
\bar x^{[k]}=\overline{\lfloor x/2^k\rfloor},\qquad
\bar x^{[0]}=\bar x.
```

The bracketed superscript labels a digit, not a power. Floors are
mathematical floors, including for negative integers. A check denotes an
explicitly defined shifted field or its corresponding source/product.
The common background shift is binary:

<a id="eq-c1"></a>

**(C1)**

```math
\check\omega_2=\omega_2+s_1\cup s_1.
```

### Integer lifts are implicit in integer arithmetic

A named binary cochain in an integer expression means its canonical
$`0,1`$ lift. No tilde is needed. Sums, differences, differentials, and
higher cups in such an expression use integer arithmetic and its stated
coefficient transport. If an entire compound expression must first be
reduced, its bar stays explicit. For binary values, for example,

```math
\overline{x+y}=x+y-2xy\quad\text{in }\mathbb Z.
```

Thus $`(x+y)/4`$ and $`\overline{x+y}/4`$ need not be the same phase. A
previously defined binary polynomial is first evaluated as that binary
polynomial, then lifted when used in an integer expression. Integer
numerators are assembled completely before exact division.
A phase bracket with coefficient $`1/2`$ is binary before its implicit
lift; the integral $`1/4,1/8,1/16`$ terms state their arithmetic separately.

All products are ordered: juxtaposition means $`\cup=\cup_0`$. Powers are
ordered cup powers. Ordinary $`d`$ and $`d_{s_1}`$ are the untwisted and
sign-twisted differentials. Their coefficient domain follows the equation.
In particular, the differential inside an integer Bockstein is taken
before reduction.

For a binary cochain $`x`$ of degree $`r`$, use the standard Steenrod symbol:

<a id="eq-c2"></a>

**(C2)**

```math
\mathrm{Sq}^j x=x\cup_{r-j}x+x\cup_{r-j+1}dx.
```

The second term is retained for a nonclosed cochain. Negative or
otherwise degree-impossible higher cups are zero in the explicit
[interval-cut definition](formulas/OPERATIONS.md#interval-cuts).

| Operation | Definition and domain |
|---|---|
| $`\beta x=dx/2`$ | Integer Bockstein, for binary $`dx=0`$; numerator is the **integer** differential |
| $`\beta^\circ x=(dx-\overline{dx})/2`$ | Integer carry for a possibly open binary cochain |
| $`\beta^+x=(\beta x+\overline{\beta x})/2`$ | The plus carry of a closed binary cochain |
| $`\beta_{s_1}\check\omega_2=d_{s_1}\check\omega_2/2`$ | Twisted integer background carry |
| $`\Delta f=f(N)-f(n)-f(n')`$ | Full change under the displayed lower stacking law, with fixed backgrounds |

The integer lifts of $`\check\omega_2`$ and the p+ip field have coefficients
$`\mathbb Z_{s_1}`$; those of $`\omega_2`$ and the Majorana field have ordinary
integer coefficients. [Operations](formulas/OPERATIONS.md#eq-o7) specifies
all coefficient transports. A check is never an instruction to change
those coefficient systems.

The standard quadratic background cochain will be useful in both sections:

```math
\mathcal P_{s_1}(\check\omega_2)
 =\check\omega_2\check\omega_2
  +\check\omega_2\cup_1d_{s_1}\check\omega_2\quad\text{in }\mathbb Z.
```

This is a fixed integer representative of the twisted Pontryagin-square
expression; keep the displayed representative when it is multiplied by
$`1/16`$. It is not an unspecified modulo-four class.

The non-elementary operations are the explicit interval-cut polynomials
$`\zeta,\mathop{\mathrm{MS}}\nolimits`$, the signed parameter sums
$`\tau_I,\tau_\triangle`$, and the grid homotopies
$`(\mathsf h_r^{(2)})^*,(\mathsf h_r^{(3)})^*`$ in
[Operations](formulas/OPERATIONS.md). Their finite definitions fix all
signs and choices.

<a id="three-dimensional"></a>
## 3+1D

Throughout this section the physical fields are:

| Field | Physical role | Coefficients |
|---|---|---|
| $`n_1`$ | p+ip decoration | $`\mathbb Z_{s_1}`$ |
| $`n_2`$ | Majorana decoration | $`\mathbb Z_2`$ |
| $`n_3`$ | Complex-fermion decoration | $`\mathbb Z_2`$ |
| $`\nu_4`$ | Bosonic phase | $`U(1)_{s_1}`$ |

The shifted Majorana field is

<a id="eq-c1-3d"></a>

**(3D coordinates)**

```math
\check n_2=n_2+s_1\bar n_1^{[1]}.
```

<a id="lower-sources"></a>
### Obstructions

The integer field satisfies $`d_{s_1}n_1=0`$. The next equations are binary:

<a id="eq-l1"></a>

**(L1)**

```math
dn_2=\mathcal O_3=\omega_2\bar n_1+s_1\bar n_1^2,\qquad d\check n_2=\check\omega_2\bar n_1.
```

<a id="eq-l2"></a>

**(L2)**

```math
d{n_{3}}={\mathcal O_{4}}({n_{1}},{\check n_{2}})={\mathrm{Sq}}^2{\check n_{2}}+{s_1}{\mathrm{Sq}}^1{\check n_{2}}+{\omega_2}{\check n_{2}}+{\mathcal O^\psi_{4}}({n_{1}}).
```

<a id="eq-l3"></a>

**(L3)**

```math
\begin{aligned}
{\mathcal O^\psi_4}={}&\zeta_{2,1}({\check\omega_2},{\bar n_{1}})+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\bar n_{1}^{[1]}}\\
&+\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\bar n_{1}},\\
\zeta_{2,1}({\check\omega_2},{\bar n_{1}})(01234)={}&{\check\omega_2}(012){\check\omega_2}(023){\bar n_{1}}(23){\bar n_{1}}(34).
\end{aligned}
```

Here $`d\bar n_1^{[1]}=\bar n_1^2+s_1\bar n_1`$. The final phase equation
$`d_{s_1}\widehat\nu_4=\widehat{\mathcal O}_5`$ is given below, after its
auxiliary parameter fields have been specified.

<a id="lower-stacking"></a>
### Stacking of the decoration fields

<a id="eq-p1"></a>

**(P1)**

```math
\begin{aligned}
\check{\mathcal E}_{2}
 &=\bar n_{1}\cup\overline{n'_{1}},\\
N_{1}&=n_{1}+n'_{1},\\
\check N_{2}
 &=\check n_{2}+\check n'_{2}+\check{\mathcal E}_{2}.
\end{aligned}
```

<a id="eq-p2"></a>

**(P2)**

```math
\begin{aligned}
\mathcal E_{2}
 &=\check{\mathcal E}_{2}
   +s_1(\bar n_{1}\cup_{1}\overline{n'_{1}}),\\
N_{2}&=n_{2}+n'_{2}+\mathcal E_{2},\\
N_3&=n_3+n'_3+\mathcal E_3.
\end{aligned}
```

<a id="eq-p3"></a>

**(P3)**

```math
\begin{aligned}
{\mathcal E_3}={}&{\check n_{2}}\cup_1{\check n'_{2}}+d{\check n_{2}}\cup_2{\check n'_{2}}+({\check n_{2}}+{\check n'_{2}})\cup_1{\check{\mathcal E}_{2}}
 +{s_1}\big[{\check n_{2}}\cup_2{\check n'_{2}}+({\check n_{2}}+{\check n'_{2}})\cup_2{\check{\mathcal E}_{2}}\big]\\
&+{z^\psi_3}({\bar n_{1}},{\overline{n'_{1}}})+[{\check\omega_2}({\bar n_{1}}+{\overline{n'_{1}}})]\cup_2{\check{\mathcal E}_{2}}+(d{\bar n_{1}^{[1]}}){\overline{n'_{1}}^{[1]}}\\
&+({s_1}{\bar n_{1}})\cup_1{\overline{n'_{1}}}^2+{\bar n_{1}} {s_1} {\overline{n'_{1}}}+{(\bar n_{1}\cup_{1}\overline{n'_{1}})} {s_1}({\bar n_{1}}+{\overline{n'_{1}}})\\
&+{s_1}\big[{s_1}{(\bar n_{1}\cup_{1}\overline{n'_{1}})}+{\bar n_{1}}\cup_1d{\overline{n'_{1}}^{[1]}}+{(\bar n_{1}\cup_{1}\overline{n'_{1}})}({\bar n_{1}}+{\overline{n'_{1}}})\big]+{\Delta[(\bar n_1^2\cup_1s_1)\bar n_1]},\\
{z^\psi_3}({\bar n_{1}},{\overline{n'_{1}}})={}&\mathop{\mathrm{MS}}\nolimits_{12314}({\bar n_{1}},{\bar n_{1}},{\overline{n'_{1}}},{\overline{n'_{1}}})
 =[{\bar n_{1}}\cup_1({\bar n_{1}}{\overline{n'_{1}}})]{\overline{n'_{1}}}.
\end{aligned}
```

The $`\Delta`$ acts on the entire bracket using the output above. The
binary digit identity used in the native Majorana product is

```math
\bar N_1^{[1]}=\bar n_1^{[1]}+\overline{n'_1}^{[1]}
 +\bar n_1\cup_1\overline{n'_1}.
```

<a id="three-dimensional-pair"></a>
### Bosonic phase: auxiliary parameter fields

This construction uses cochains on an interval or triangle times the
physical base. They are **auxiliary**, not additional physical decorations.
A superscript $`J\in\{I,\triangle\}`$ always marks them: $`n_2^J`$ is
integer, while $`\check n_3^J,n_4^J`$ are binary. The physical $`n_2`$ in
this section remains Majorana decoration.

On the oriented triangle $`012`$, the integer one-cocycles
$`\theta_1,\theta'_1`$ have edge values $`(01,12,02)=(1,0,1),(0,1,1)`$.
The binary $`\chi_1`$ has values $`(0,0,1)`$ and satisfies
$`d\chi_1=\bar\theta_1\overline{\theta'_1}`$. Backgrounds and physical
fields are pulled from the base; parameter cochains are pulled from the
triangle. Integer parameter cochains act through their reductions inside
binary expressions.

<a id="eq-t3b"></a>

**(T3B)**

```math
\begin{aligned}
{n_2^\triangle}&={\theta_1} {n_{1}}+{\theta'_1} {n'_{1}},\\
{\check n_3^\triangle}&={\theta_1} {\check n_{2}}+{\theta'_1} {\check n'_{2}}+({\check\omega_2}\cup_1{\theta_1}){\bar n_{1}}
 +({\check\omega_2}\cup_1{\theta'_1}){\overline{n'_{1}}}+{\chi_1} {\check{\mathcal E}_{2}}+{\theta_1}({\bar n_{1}}\cup_1{\theta'_1}){\overline{n'_{1}}},
\end{aligned}
```

For the interval, $`\theta_1(01)=1`$ and the second input is absent:

```math
n_2^I=\theta_1 n_1,\qquad
\check n_3^I=\theta_1\check n_2+(\check\omega_2\cup_1\theta_1)\bar n_1.
```

The following binary degree-five source is evaluated on these auxiliary
fields. Its superscript keeps it separate from the physical terminal
phase obstruction $`\widehat{\mathcal O}_5`$:

<a id="eq-aux-o5"></a>

**(Auxiliary source)**

```math
\mathcal O_5^J=\mathrm{Sq}^2\check n_3^J+s_1\mathrm{Sq}^1\check n_3^J
 +\omega_2\check n_3^J+\mathcal O_5^{\psi,J}.
```

<a id="eq-aux-pip5"></a>

**(Auxiliary p+ip source)**

```math
\begin{aligned}
{\mathcal O_5^{\psi,J}}={}&\zeta_{2,2}({\overline{n_2^J}},{\overline{n_2^J}})+\zeta_{2,2}({\check\omega_2},{\overline{n_2^J}})
 +{\overline{n_2^J}}^2\cup_3({\check\omega_2}{\overline{n_2^J}})+\mathrm{Sq}^3{\overline{n_2^J}^{[1]}}+{(\overline{n_2^J}\cup_1\overline{n_2^J})}\cup_1({s_1}{\overline{n_2^J}})\\
&+{s_1}\big[{\overline{n_2^J}}^2\cup_4({\check\omega_2}{\overline{n_2^J}})+({\overline{n_2^J}}\cup_1{s_1}){\overline{n_2^J}}+{\overline{n_2^J}}\cup_1{(\overline{n_2^J}\cup_1\overline{n_2^J})}+{\overline{n_2^J}}^2\big]\\
&+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\overline{n_2^J}^{[1]}}
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
n_4^\triangle={}&(\mathsf h_4^{(2)})^*\mathcal O_5^\triangle\\
 &+\theta_1\big[n_3+\check\omega_2\bar n_1^{[1]}+\check n_2\cup_2d\check n_2+(s_1\cup_1\omega_2)\bar n_1\big]\\
 &+\theta'_1\big[n'_3+\check\omega_2\overline{n'_1}^{[1]}+\check n'_2\cup_2d\check n'_2+(s_1\cup_1\omega_2)\overline{n'_1}\big]\\
 &+\chi_1\Big(\mathcal E_3+\Delta\big[\check\omega_2\bar n_1^{[1]}+\check n_2\cup_2d\check n_2+(s_1\cup_1\omega_2)\bar n_1\big]\Big)\\
 &+(d\chi_1)\Big[\bar n_1^{[1]}\overline{n'_1}+(\bar n_1+\bar n_1^{[1]})\overline{n'_1}^{[1]}
 +\check{\mathcal E}_2\cup_2(\check n_2+\check n'_2)+\check{\mathcal E}_2\\
 &\qquad +(s_1\cup_1\bar n_1)(\bar n_1\cup_1\overline{n'_1})
 +[s_1\cup_1(\bar n_1\cup_1\overline{n'_1})](\bar n_1+\overline{n'_1})\Big].
\end{aligned}
```

<a id="eq-t3c"></a>

**(T3C)**

```math
n_4^I=(\mathsf h_4^{(2)})^*\mathcal O_5^I
 +\theta_1\big[n_3+\check\omega_2\bar n_1^{[1]}+\check n_2\cup_2d\check n_2+(s_1\cup_1\omega_2)\bar n_1\big].
```

All brackets defining these binary fields are evaluated modulo two.
The interval and triangle sums and their coefficient transports are fixed
in [Operations](formulas/OPERATIONS.md#parameter-integration).

### Bosonic phase: source and product

The following residuals are untwisted integer cochains on the parameter
space. The definitions are local to the auxiliary fields:

<a id="eq-aux-residual"></a>

**(Auxiliary integer residuals)**

```math
\begin{aligned}
\check{\mathcal O}_4^J&=\overline{n_2^J}^2+\check\omega_2\overline{n_2^J}
 \quad\text{in }\mathbb Z_2,\\
B_4^{\psi,J}&=\frac{\check{\mathcal O}_4^J-{n_2^J}^2-\check\omega_2{n_2^J}}{2},\\
B_4^J&=\beta^\circ\check n_3^J+B_4^{\psi,J}
 =\frac{d\check n_3^J-{n_2^J}^2-\check\omega_2{n_2^J}}{2},\\
dB_4^J&=-(\beta_{s_1}\check\omega_2){n_2^J}.
\end{aligned}
```

<a id="eq-aux-terminal-source"></a>

**(Auxiliary phase source)**

```math
\begin{aligned}
\widehat{\mathcal O}_6^J={}&\frac12\Big[\mathrm{Sq}^2 {n_4^J}+\omega_2 {n_4^J}+T_6[\check n_3^J;\omega_2,s_1]+\check n_3^J(\overline{\beta\omega_2}+s_1\omega_2)\\
 &\qquad +(\mathrm{Sq}^2\check n_3^J+s_1\mathrm{Sq}^1\check n_3^J+\omega_2\check n_3^J)
 \cup_4\mathcal O_5^{\psi,J}+y_6[{n_2^J};\omega_2,s_1]\\
 &\qquad +\overline{\beta^\circ\check n_3^J}\cup_2\overline{B_4^{\psi,J}}
 +s_1(\overline{\beta^\circ\check n_3^J}\cup_3\overline{B_4^{\psi,J}})\Big]\\
 &+\frac14\big[B_4^J\cup_2B_4^J+B_4^J\cup_3dB_4^J+\omega_2 B_4^J\big]\\
 &-\frac14\overline{\big[\mathop{\mathrm{MS}}\nolimits_{12132434}
 (\overline{\beta_{s_1}\check\omega_2},\overline{\beta_{s_1}\check\omega_2},\overline{n_2^J},\overline{n_2^J})
 +\overline{\beta_{s_1}\check\omega_2}^{[1]}(\overline{n_2^J}\cup_1\overline{n_2^J})
 +(s_1\overline{\beta_{s_1}\check\omega_2})\overline{n_2^J}^{[1]}
 +s_1(\overline{\beta_{s_1}\check\omega_2}\cup_1s_1)\overline{n_2^J}\big]}\\
 &+\frac1{16}\mathcal P_{s_1}(\check\omega_2){n_2^J}
 +\frac18\check\omega_2 {n_2^J}^2+\frac1{12}{n_2^J}^3.
\end{aligned}
```

The complete physical source and product are the two signed transgressions
of this one auxiliary source, each on its own parameter fields:

<a id="eq-t3"></a>

**(T3)**

```math
\boxed{\widehat{\mathcal O}_5=\tau_I\widehat{\mathcal O}_6^I,\qquad
\widehat{\mathcal E}_4=\tau_\triangle\widehat{\mathcal O}_6^\triangle.}
```

The extra integer terms have the exact signed transgressions

```math
\begin{array}{c|cc}
 &\tau_I&\tau_\triangle\\ \hline
\mathcal P_{s_1}(\check\omega_2)n_2^J
 &\mathcal P_{s_1}(\check\omega_2)n_1&0\\
\check\omega_2(n_2^J)^2&0&-\check\omega_2 n_1n'_1\\
(n_2^J)^3&0&0.
\end{array}
```

These identities use the displayed interval/triangle fields and the fixed
coefficient transport, so the compact pair includes all fractional terms.

The operations $`T_6,y_6`$ are the finite operations of
[Source operations](formulas/SOURCE_OPERATIONS.md), applied to the displayed
auxiliary fields. Each $`1/2`$ bracket is binary. Each $`1/4`$ bracket is
integer, with the barred polynomial reduced as a whole before its
implicit lift. The parameter integration then gives phases modulo one.
The physical equations and product are

```math
d_{s_1}\widehat\nu_4=\widehat{\mathcal O}_5,\qquad
\widehat\nu_4^{\mathrm{out}}=\widehat\nu_4+\widehat\nu'_4+\widehat{\mathcal E}_4.
```

### Relation to the older fermion coordinate

<a id="eq-t3d"></a>

**(T3D)**

```math
{n_3^{\mathrm{old}}}={n_{3}}+\kappa_3({n_{1}},{\check n_{2}}),\qquad
\kappa_3=({\bar n_{1}}+{s_1}){\check n_{2}}+{\check\omega_2}{\bar n_{1}^{[1]}}+[{\check\omega_2}\cup_1({\bar n_{1}}+{s_1})]{\bar n_{1}}.
```

Its stacking correction changes at the same time:

```math
\mathcal E_{3,\mathrm{old}}=\mathcal E_3+\Delta\kappa_3.
```

The obstruction is transported by the same substitution and $`d\kappa_3`$.
In particular, $`n_1=0`$ alone does not remove this coordinate change when
$`s_1\ne0`$.

<a id="four-dimensional"></a>
## 4+1D

Throughout this section the physical fields are:

| Field | Physical role | Coefficients |
|---|---|---|
| $`n_2`$ | p+ip decoration | $`\mathbb Z_{s_1}`$ |
| $`n_3`$ | Majorana decoration | $`\mathbb Z_2`$ |
| $`n_4`$ | Complex-fermion decoration | $`\mathbb Z_2`$ |
| $`\nu_5`$ | Bosonic phase | $`U(1)_{s_1}`$ |

The shifted Majorana field is

<a id="eq-c1-4d"></a>

**(4D coordinates)**

```math
\check n_3=n_3+s_1\bar n_2^{[1]}.
```

### Obstructions

The integer field satisfies $`d_{s_1}n_2=0`$. The next equations are binary:

<a id="eq-l1-4d"></a>

**(L1–4D)**

```math
d{n_{3}}=\mathcal O_4[n_{2}]={\mathrm{Sq}}^2{\bar n_{2}}+{\omega_2} {\bar n_{2}}+{s_1} {\mathrm{Sq}}^1{\bar n_{2}}.
```

The shifted equation is $`d\check n_3=\check{\mathcal O}_4
=\bar n_2^2+\check\omega_2\bar n_2`$.

<a id="eq-l2-4d"></a>

**(L2–4D)**

```math
d{n_{4}}={\mathcal O_{5}}({n_{2}},{\check n_{3}})={\mathrm{Sq}}^2{\check n_{3}}+{s_1}{\mathrm{Sq}}^1{\check n_{3}}+{\omega_2}{\check n_{3}}+{\mathcal O^\psi_{5}}({n_{2}}).
```

<a id="eq-l4"></a>

**(L4)**

```math
\begin{aligned}
{\mathcal O^\psi_5}={}&\zeta_{2,2}({\bar n_{2}},{\bar n_{2}})+\zeta_{2,2}({\check\omega_2},{\bar n_{2}})
 +{\bar n_{2}}^2\cup_3({\check\omega_2}{\bar n_{2}})+\mathrm{Sq}^3{\bar n_{2}^{[1]}}+{(\bar n_2\cup_1\bar n_2)}\cup_1({s_1}{\bar n_{2}})\\
&+{s_1}\big[{\bar n_{2}}^2\cup_4({\check\omega_2}{\bar n_{2}})+({\bar n_{2}}\cup_1{s_1}){\bar n_{2}}+{\bar n_{2}}\cup_1{(\bar n_2\cup_1\bar n_2)}+{\bar n_{2}}^2\big]\\
&+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\bar n_{2}^{[1]}}
 +\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\bar n_{2}},\\
\zeta_{2,2}(x,y)={}&\mathop{\mathrm{MS}}\nolimits_{1231343}(x,x,y,y).
\end{aligned}
```

Here $`d\bar n_2^{[1]}=\bar n_2\cup_1\bar n_2+s_1\bar n_2`$.
The final phase equation is given after the integer residuals below.

### Stacking of the decoration fields

<a id="eq-p1-4d"></a>

**(P1–4D)**

```math
\begin{aligned}
\check{\mathcal E}_{3}
 &=\bar n_{2}\cup_{1}\overline{n'_{2}},\\
N_{2}&=n_{2}+n'_{2},\\
\check N_{3}
 &=\check n_{3}+\check n'_{3}+\check{\mathcal E}_{3}.
\end{aligned}
```

<a id="eq-p2-4d"></a>

**(P2–4D)**

```math
\begin{aligned}
\mathcal E_{3}
 &=\check{\mathcal E}_{3}
   +s_1(\bar n_{2}\cup_{2}\overline{n'_{2}}),\\
N_{3}&=n_{3}+n'_{3}+\mathcal E_{3},\\
N_4&=n_4+n'_4+\mathcal E_4.
\end{aligned}
```

In these coordinates $`d\check{\mathcal E}_3=
\bar n_2\overline{n'_2}+\overline{n'_2}\bar n_2`$.

<a id="eq-p4"></a>

**(P4)**

```math
\begin{aligned}
{\mathcal E_4}={}&{\check n_{3}}\cup_2{\check n'_{3}}+d{\check n_{3}}\cup_3{\check n'_{3}}+({\check n_{3}}+{\check n'_{3}})\cup_2{\check{\mathcal E}_{3}}\\
&+{s_1}\big[{\check n_{3}}\cup_3{\check n'_{3}}+d{\check n_{3}}\cup_4{\check n'_{3}}+({\check n_{3}}+{\check n'_{3}})\cup_3{\check{\mathcal E}_{3}}\big]\\
&+{z^\psi_4}({\bar n_{2}},{\overline{n'_{2}}})+[{\check\omega_2}({\bar n_{2}}+{\overline{n'_{2}}})]\cup_3{\check{\mathcal E}_{3}}
 +{\overline{n'_{2}}}^2\cup_4({\check\omega_2}{\bar n_{2}})+d{\check{\mathcal E}_{3}}\cup_4[{\check\omega_2}({\bar n_{2}}+{\overline{n'_{2}}})]\\
&+{\bar n_{2}^{[1]}}({\overline{n'_{2}}^{[1]}}+{\overline{n'_{2}}})+{\bar n_{2}}{\overline{n'_{2}}^{[1]}}+d{\bar n_{2}^{[1]}}\cup_1{\overline{n'_{2}}^{[1]}}+({\bar n_{2}^{[1]}}+{\overline{n'_{2}}^{[1]}}){(\bar n_{2}\cup_{2}\overline{n'_{2}})}\\
&+({s_1}{\bar n_{2}})\cup_2({\overline{n'_{2}}}\cup_1{\overline{n'_{2}}})+{\bar n_{2}}\cup_1({s_1}{\overline{n'_{2}}})+{(\bar n_{2}\cup_{2}\overline{n'_{2}})}\cup_1[{s_1}({\bar n_{2}}+{\overline{n'_{2}}})]\\
&+{s_1}\big[{s_1}{(\bar n_{2}\cup_{2}\overline{n'_{2}})}+{\bar n_{2}}\cup_2d{\overline{n'_{2}}^{[1]}}+{(\bar n_{2}\cup_{2}\overline{n'_{2}})}\cup_1({\bar n_{2}}+{\overline{n'_{2}}})+\ell_3({\bar n_{2}},{\overline{n'_{2}}})\big].
\end{aligned}
```

<a id="eq-p5"></a>

**(P5)**

```math
\begin{aligned}
{z^\psi_4}({\bar n_{2}},{\overline{n'_{2}}})={}&\mathop{\mathrm{MS}}\nolimits_{12413423}({\bar n_{2}},{\bar n_{2}},{\bar n_{2}},{\overline{n'_{2}}})\\
&+(\mathop{\mathrm{MS}}\nolimits_{12314132}+\mathop{\mathrm{MS}}\nolimits_{12314324}
 +\mathop{\mathrm{MS}}\nolimits_{12341321})({\bar n_{2}},{\bar n_{2}},{\overline{n'_{2}}},{\overline{n'_{2}}})\\
&+(\mathop{\mathrm{MS}}\nolimits_{12132413}+\mathop{\mathrm{MS}}\nolimits_{12324214})({\bar n_{2}},{\overline{n'_{2}}},{\overline{n'_{2}}},{\overline{n'_{2}}}),\\
\ell_3({\bar n_{2}},{\overline{n'_{2}}})(0123)={}&{\bar n_{2}}(023){\overline{n'_{2}}}(012)[1+{\bar n_{2}}(013){\overline{n'_{2}}}(123)].
\end{aligned}
```

The digit terms retain the closed $`\bar n_2\overline{n'_2}`$
contribution once. The native Majorana rule uses

```math
\bar N_2^{[1]}=\bar n_2^{[1]}+\overline{n'_2}^{[1]}
 +\bar n_2\cup_2\overline{n'_2}.
```

<a id="shared-terminal-source"></a>
<a id="four-dimensional-pair"></a>
### Bosonic obstruction

The integral residual $`B_4`$ is useful independently of the phase formula:
its differential and its stacking carry will both occur below. Keep its
integer-layer part $`B_4^\psi`$ separately because the source completion
uses it before any Majorana field has been chosen.

<a id="eq-s1"></a>

**(S1)**

```math
\begin{aligned}
\check{\mathcal O}_4&=\bar n_2^2+\check\omega_2\bar n_2
 \quad\text{in }\mathbb Z_2,\\
B_4^\psi&=\frac{\check{\mathcal O}_4-n_2^2-\check\omega_2n_2}{2},\\
B_4&=\beta^\circ\check n_3+B_4^\psi
 =\frac{d\check n_3-n_2^2-\check\omega_2n_2}{2},\\
dB_4&=-(\beta_{s_1}\check\omega_2)n_2.
\end{aligned}
```

The complete source is written directly below. The subtracted binary polynomial is reduced as a whole before its
quarter-valued integer use.

<a id="eq-s2"></a>
<a id="eq-s3"></a>

<a id="eq-t4"></a>

**(T4)**

```math
\begin{aligned}
\widehat{\mathcal O}_6={}&\frac12\Big[\mathrm{Sq}^2 n_4+\omega_2 n_4+T_6[\check n_3;\omega_2,s_1]+\check n_3(\overline{\beta\omega_2}+s_1\omega_2)\\
 &\qquad +(\mathrm{Sq}^2\check n_3+s_1\mathrm{Sq}^1\check n_3+\omega_2\check n_3)
 \cup_4\mathcal O^\psi_5+y_6[n_2;\omega_2,s_1]\\
 &\qquad +\overline{\beta^\circ\check n_3}\cup_2\overline{B_4^\psi}
 +s_1(\overline{\beta^\circ\check n_3}\cup_3\overline{B_4^\psi})\Big]\\
 &+\frac14\big[B_4\cup_2B_4+B_4\cup_3dB_4+\omega_2 B_4\big]\\
 &-\frac14\overline{\big[\mathop{\mathrm{MS}}\nolimits_{12132434}
 (\overline{\beta_{s_1}\check\omega_2},\overline{\beta_{s_1}\check\omega_2},\bar n_2,\bar n_2)
 +\overline{\beta_{s_1}\check\omega_2}^{[1]}(\bar n_2\cup_1\bar n_2)
 +(s_1\overline{\beta_{s_1}\check\omega_2})\bar n_2^{[1]}
 +s_1(\overline{\beta_{s_1}\check\omega_2}\cup_1s_1)\bar n_2\big]}\\
 &+\frac1{16}\mathcal P_{s_1}(\check\omega_2)n_2
 +\frac18\check\omega_2 n_2^2+\frac1{12}n_2^3\pmod1.
\end{aligned}
```

Here $`T_6[\check n_3;\omega_2,s_1]`$ is the fixed continuation of the
closed-Majorana source and $`y_6[n_2;\omega_2,s_1]`$ its integer-layer
completion. [Source operations](formulas/SOURCE_OPERATIONS.md) gives their
full finite definitions, and [Coefficients](formulas/COEFFICIENTS.md) gives
every fixed coefficient. The $`1/2`$ bracket is binary; all other brackets
and products in this source are integer before division. The phase equation
is $`d_{s_1}\widehat\nu_5=\widehat{\mathcal O}_6`$.

### Bosonic stacking correction

The product requires one integer carry:

<a id="eq-t4a"></a>

**(T4A)**

```math
\begin{aligned}
\lambda_3&=\frac{\check N_3-\check n_3-\check n'_3+n_2\cup_1n'_2}{2},\\
\Delta B_4&=d\lambda_3-n'_2n_2,\\
\overline{\Delta B_4}&=d\bar\lambda_3+\overline{n'_2}\bar n_2.
\end{aligned}
```

The numerator uses the canonical integer values of the three named
binary Majorana fields. The quantities $`\lambda_3,B_4,\Delta B_4`$ are
untwisted integers. Only one binary polynomial needs to retain a name:
$`\mathcal V_5`$ is used both in its quarter-valued phase and in the finite
transfer. Its full reduction must precede either integer use.

<a id="eq-t4b"></a>

**(T4B)**

```math
\begin{aligned}
\mathcal V_5={}&{\bar B_4}\cup_3{\overline{B'_4}}+d{\bar B_4}\cup_4{\overline{B'_4}}+({\bar B_4}+{\overline{B'_4}})\cup_3{\overline{\Delta B_4}}
 +(d{\bar B_4}+d{\overline{B'_4}})\cup_4{\overline{\Delta B_4}}\\
&+{\mathrm{Sq}}^2{\bar\lambda_3}+({\overline{n'_{2}}}{\bar n_{2}})\cup_3d{\bar\lambda_3}+{\omega_2}{\bar\lambda_3}+({\overline{\beta_{s_1}\check\omega_2}^{[1]}}+{\overline{\beta_{s_1}\check\omega_2}}){(\bar n_{2}\cup_{2}\overline{n'_{2}})}\\
&+\zeta_{2,2}({\overline{n'_{2}}},{\bar n_{2}})+{\check n'_{3}}{\bar n_{2}}+{\overline{n'_{2}}}{\check n_{3}}+({\check\omega_2}\cup_1{\overline{n'_{2}}}){\bar n_{2}}
 +{\overline{n'_{2}}^{[1]}}({\bar n_{2}}\cup_1{\bar n_{2}})+{s_1}{\overline{n'_{2}}}{\bar n_{2}^{[1]}}+{s_1}({\overline{n'_{2}}}\cup_1{s_1}){\bar n_{2}}.
\end{aligned}
```

<a id="eq-t4c"></a>

All remaining sums are inserted directly into the product. The first
bracket is binary. The signed $`\Delta(n_2\check n_3)`$ and all terms with
coefficient $`1/4,1/8,1/3`$ use integer arithmetic:

<a id="eq-t4d"></a>

**(T4D)**

```math
\begin{aligned}
\widehat{\mathcal E}_5={}&\frac12\Big[{n_{4}}\cup_3{n'_{4}}+d{n_{4}}\cup_4{n'_{4}}+({n_{4}}+{n'_{4}})\cup_3{\mathcal E_4}
 +({\mathcal E_4}+{(\bar n_{2}\overline{n'_{2}})})\cup_3{(\bar n_{2}\overline{n'_{2}})}+d{N_{4}}\cup_4{(\bar n_{2}\overline{n'_{2}})}\\
 &\qquad +\zeta_{2,2}({\bar n_{2}},{\overline{n'_{2}}})+{\bar n_{2}}\cup_1d{\check n'_{3}}+{\bar n_{2}^{[1]}}({\overline{n'_{2}}}\cup_1{\overline{n'_{2}}})
 +({\check\omega_2}\cup_1{\bar n_{2}}){\overline{n'_{2}}}+{s_1}{\bar n_{2}}{\overline{n'_{2}}^{[1]}}+{s_1}({\bar n_{2}}\cup_1{s_1}){\overline{n'_{2}}}+{\check{\mathcal E}_{3}}({\bar n_{2}}+{\overline{n'_{2}}})+{\check\omega_2}{\check{\mathcal E}_{3}}+Z_5\Big]\\
 &+\frac14\Big[\mathcal V_5+\Delta(n_2\check n_3)+(n_2\cup_1\check\omega_2)n'_2
 +(n'_2\cup_1\check\omega_2)n_2\Big]
 +\frac18\check\omega_2(n_2\cup_1n'_2)\\
 &+\frac13\big[(n'_2-n_2)(n_2\cup_1n'_2)
 -(n_2\cup_1n'_2)(n'_2-n_2)\big]\pmod1.
\end{aligned}
```

The full output is

```math
(N_2,N_3,N_4,\nu_5^{\mathrm{out}}),\qquad
\widehat\nu_5^{\mathrm{out}}
 =\widehat\nu_5+\widehat\nu'_5+\widehat{\mathcal E}_5.
```

$`Z_5`$ is the finite binary operation in
[Terminal transfer](formulas/TERMINAL_TRANSFER.md). Its kernel, face rule,
coefficient polynomials, and finite sum are specified there. It is retained
as a defined operation, rather than replacing it by a list of implementation
intermediates. The ordered integer $`1/3`$ products do not commute.

### Relation to the earlier source representative

Write $`\widehat{\mathcal O}_{6,\mathrm{raw}}`$ for the earlier source.
The displayed change is paired with the product change in the same
coordinates:

<a id="eq-t4e"></a>

**(T4E)**

```math
{\widehat{\mathcal O}}_6=\widehat{\mathcal O}_{6,\mathrm{raw}}+d_{s_1}\Lambda_5+\frac1{12}{n_{2}}^3,
\qquad \Lambda_5=\frac14{\beta^\circ\check n_3}\cup_3{B_4^\psi}.
```

The corresponding terminal redefinition contributes
$`\Delta\Lambda_5`$ to the stacking correction. The separate cubic term
shown in (T4e) is retained in (T4); it is not being called a coboundary.

## Classification and changes of representative

For fixed lower decorations, solve each obstruction modulo the permitted
gauge and lower-layer changes. A nonzero cochain may be exact; only a
nontrivial final obstruction class rules out the decoration. Stack accepted
representatives using the paired product and reduce by the same equivalences.

For a terminal phase change $`\widehat\nu\mapsto\widehat\nu+f`$, with
lower fields and their product fixed, the source and correction transform
together:

```math
\widehat{\mathcal O}\longmapsto\widehat{\mathcal O}+d_{s_1}f,\qquad
\widehat{\mathcal E}\longmapsto\widehat{\mathcal E}+\Delta f.
```

A change of a lower decoration must also be substituted into every higher
source and product. These coordinate rules concern the full equations,
not only the abstract group obtained in an example.

The separate [programmer translation](../formulas/CODE_NOTATION.md) records
how the formulas correspond to existing variables and compiled operations.
