# FSPT obstruction and stacking formulas

The input is the bosonic symmetry group $`G_b`$, the fermion-parity extension
cocycle $`\omega_2`$, and the antiunitary cocycle $`s_1`$. We retain the
physical decoration fields $`n_j`$ and phase $`\nu_j`$ throughout. The same
notation is used in every appendix.

Read the [notation](#conventions-and-coordinates) first, then the
[obstruction equations](#lower-sources), [stacking equations](#lower-stacking),
and the terminal formulas for [3+1D](#three-dimensional-pair) or
[4+1D](#four-dimensional-pair). The [closed-Majorana and lower-dimensional
formulas](formulas/MAJORANA_AND_ENDPOINTS.md) use these same rules.

<a id="conventions-and-coordinates"></a>
## Notation and operations

### Physical fields and stacking

Here $`d`$ is spatial dimension. In $`3+1`$D and $`4+1`$D the decorations are

```math
(n_{d-2},n_{d-1},n_d,\nu_{d+1})
\in C^{d-2}(G_b,\mathbb Z_{s_1})\times
 C^{d-1}(G_b,\mathbb Z_2)\times C^d(G_b,\mathbb Z_2)
 \times C^{d+1}(G_b,U(1)_{s_1}).
```

| Field | Meaning |
|---|---|
| $`n_{d-2}`$ | Integer p+ip decoration |
| $`n_{d-1}`$ | Majorana-chain decoration |
| $`n_d`$ | Complex-fermion decoration |
| $`\nu_{d+1}`$ | Bosonic phase |
| $`\omega_2,s_1`$ | Fixed symmetry background, shared by both stacking inputs |

A prime denotes the **second stacking input**, $`n'_j,\nu'_j`$; it never
means a coordinate redefinition. The output fields are $`N_j`$ and
$`\nu_{d+1}^{\mathrm{out}}`$. The subscript of a cochain records its degree.
Dummy simplex indices and the indices of finite word lists are not cochain degrees.

### Modifiers: one meaning each

| Notation | Meaning |
|---|---|
| $`\bar x`$ | Pointwise reduction modulo two |
| $`\bar x^{[k]}=\overline{\lfloor x/2^k\rfloor}`$ | Binary digit $`k`$ of an integer value; $`\bar x^{[0]}=\bar x`$ |
| $`\widetilde x`$ | Canonical integer lift of a binary value to $`0,1`$ |
| $`\widehat\nu`$ | Additive phase, $`\nu=\exp(2\pi i\widehat\nu)`$, with $`\widehat\nu\in\mathbb R/\mathbb Z`$ |
| $`\check x`$ | The explicitly defined shifted coordinate in (C1), or its corresponding source/stacking correction |

Thus the second digit of $`n_j`$ is $`\bar n_j^{[1]}`$, not a separately named
field. For the second input write $`\overline{n'_j}^{[1]}`$.
Digits are labels, not powers. Floors are mathematical floors even for
negative integers: $`\bar{(-1)}=\bar{(-1)}^{[1]}=1`$.
A lift is taken **after the entire binary expression has been formed**;
$`\widetilde{x+y}`$ and $`\widetilde x+\widetilde y`$ are different integers.

Only two field redefinitions are needed:

<a id="eq-c1"></a>

**(C1)**

```math
\check\omega_2=\omega_2+s_1\cup s_1,\qquad
\check n_{d-1}=n_{d-1}+s_1\cup\bar n_{d-2}^{[1]}.
```

The same rule defines $`\check n'_{d-1}`$ and $`\check N_{d-1}`$.
A check therefore keeps the original field visible; it does not introduce
an independent decoration. The binary reductions of a p+ip field are written
explicitly, while the field itself remains integer valued wherever an
integer cup or rational coefficient occurs.

### Differential, products, and standard operations

Ordinary $`d`$ is the untwisted differential; $`d_{s_1}`$ is the sign-twisted
differential. Juxtaposition means the **ordered cup product** $`\cup=\cup_0`$.
Cochains are not treated as commuting. Negative cup indices and
 degree-impossible operations give zero. Powers of cochains mean ordered cup powers; the bracketed superscript $`[k]`$ alone denotes a binary digit.

For a binary cochain $`x`$ of degree $`r`$, the cochain representative of the
Steenrod square is

<a id="eq-c2"></a>

**(C2)**

```math
\mathrm{Sq}^{j}x=x\cup_{r-j}x+x\cup_{r-j+1}dx.
```

This specifies the operation also for nonclosed cochains; the second term
must then be retained. On cocycles it represents the usual Steenrod square.
The standard symbol $`\mathrm{Sq}`$ is used throughout.

| Operation | Definition or reference |
|---|---|
| $`\beta x=d\widetilde x/2`$ | Ordinary integer Bockstein of a **closed** binary cochain |
| $`\beta^\circ x=(d\widetilde x-\widetilde{dx})/2`$ | Integer lift carry for a possibly open binary cochain |
| $`\beta^+x=(\beta x+\widetilde{\overline{\beta x}})/2`$ | The plus carry used in the closed-Majorana formulas |
| $`\beta_{s_1}\check\omega_2=d_{s_1}\widetilde{\check\omega_2}/2`$ | Twisted integer background carry |
| $`\Delta f=f(N)-f(n)-f(n')`$ | Change of a one-state expression under stacking, with backgrounds fixed |
| $`\zeta,\mathop{\mathrm{MS}}\nolimits`$ | Explicit cup/interval-cut polynomials; [definitions](formulas/OPERATIONS.md#interval-cuts) |
| $`\tau_I,\tau_\triangle`$ | Integration over the interval or triangle parameter; [finite signed sums](formulas/OPERATIONS.md#parameter-integration) |
| $`(\mathsf h_r^{(2)})^*,(\mathsf h_r^{(3)})^*`$ | Duals of the two- and three-factor grid homotopies; [definitions](formulas/OPERATIONS.md#parameter-base-fill) |

The $`\Delta`$ rule applies to the full expression, including any field on
which it depends. Integer signs are retained; for binary values subtraction
and addition agree. Function arguments are omitted only when the current
input is unambiguous. Thus $`B'_4`$ means the same defined function $`B_4`$
evaluated on $`(n'_2,\check n'_3)`$.

Every exact division is performed on the **complete integer numerator** before
any indicated binary reduction. A bracket multiplied by $`1/2`$ in a phase
formula is binary, then lifted and divided by two. Quarter-valued and other
integral expressions retain their explicitly stated lifts and signed cups.

### Coefficients and phase equations

Binary fields have no sign distinction. The integer p+ip field $`n_{d-2}`$
and the lift $`\widetilde{\check\omega_2}`$ in the integer-layer formulas have
coefficients $`\mathbb Z_{s_1}`$; $`\widetilde{\omega_2}`$ and canonical
Majorana lifts have ordinary integer coefficients. In particular,
$`\beta_{s_1}\check\omega_2`$ is twisted. All products include the coefficient
transport fixed in [Operations](formulas/OPERATIONS.md#eq-o7).
The closed-Majorana appendix states its ordinary integral lifts separately.

The equations are organized by their physical output:

```math
\begin{aligned}
d_{s_1}n_{d-2}&=0,&
dn_{d-1}&=\mathcal O_d,&dn_d&=\mathcal O_{d+1},&
d_{s_1}\widehat\nu_{d+1}&=\widehat{\mathcal O}_{d+2},\\
N_{d-2}&=n_{d-2}+n'_{d-2},&
N_{d-1}&=n_{d-1}+n'_{d-1}+\mathcal E_{d-1},&&&\\
N_d&=n_d+n'_d+\mathcal E_d,&
\widehat\nu_{d+1}^{\mathrm{out}}
 &=\widehat\nu_{d+1}+\widehat\nu'_{d+1}+\widehat{\mathcal E}_{d+1}.&&&
\end{aligned}
```

The hats on the terminal $`\mathcal O,\mathcal E`$ have exactly the same
meaning as on $`\nu`$: additive representatives of $`U(1)`$ phases. Equivalently,
$`\nu_{d+1}^{\mathrm{out}}=\nu_{d+1}\nu'_{d+1}
\exp(2\pi i\widehat{\mathcal E}_{d+1})`$.

### Named expressions used below

Short field aliases are unnecessary. The remaining named expressions stand
for whole cochains that are reused in a source, a product, or its finite
definition. This index gives their role before they appear.

| Expressions | Role | Definition |
|---|---|---|
| $`\mathcal O_d,\check{\mathcal O}_d,\mathcal O_{d+1}`$ | Native and shifted lower obstructions | [L1–L2](#eq-l1) |
| $`\mathcal O^\psi_4,\mathcal O^\psi_5`$ | Integer-layer contribution to the complex-fermion obstruction | [L3–L4](#eq-l3) |
| $`\mathcal E_{d-1},\check{\mathcal E}_{d-1},\mathcal E_d`$ | Lower stacking corrections in the corresponding coordinates | [P1–P4](#eq-p1) |
| $`z^\psi_3,z^\psi_4,\ell_3`$ | Finite face polynomials in the lower product | [P3–P5](#eq-p3) |
| $`B_4,B_4^\psi`$ | Full integer lift residual and its integer-layer part | [S1](#eq-s1) |
| $`\mathcal P_{s_1}(\check\omega_2)`$ | Quadratic integer background expression | [S1](#eq-s1) |
| $`\mathcal C_6,\mathcal H_6,\mathcal A_6,\mathcal Q_6`$ | Reused binary/integer terms of the terminal source | [S2](#eq-s2) |
| $`T_6,y_6`$ | Open-Majorana source operation and integer-layer completion | [Source operations](formulas/SOURCE_OPERATIONS.md) |
| $`\widehat{\mathcal O}^{\mathrm{base}}_6`$ | Shared source before its cubic term | [S3](#eq-s3) |
| $`D_3,g_2,\kappa_3`$ | Corrections defining the parameter lift and the older fermion coordinate | [T3a–T3d](#eq-t3a) |
| $`\theta_1,\theta'_1,\chi_1`$ | Fixed cochains on the parameter triangle | [T3b](#eq-t3b) |
| $`n_j^I,n_j^\triangle`$ | The explicitly constructed interval/triangle fields | [T3b–T3c](#eq-t3b) |
| $`\lambda_3`$ | Integer carry of the shifted Majorana product | [T4a](#eq-t4a) |
| $`\mathcal V_5,\Phi_5,\varepsilon_5,\Pi_5`$ | Binary and integer terms of the terminal product | [T4b–T4c](#eq-t4b) |
| $`Z_5`$ | Finite binary transfer completing that product | [Terminal transfer](formulas/TERMINAL_TRANSFER.md) |
| $`\Lambda_5`$ | Paired source/product change of representative | [T4e](#eq-t4e) |

The appendices give their own small indices of subsidiary polynomials. No
new name is used for the parity or binary digits of an already named field.

<a id="lower-sources"></a>
## Lower obstruction equations

The integer field satisfies $`d_{s_1}n_{d-2}=0`$. The Majorana equation is

<a id="eq-l1"></a>

**(L1)**

```math
d{n_{d-1}}=\mathcal O_d[n_{d-2}]={\mathrm{Sq}}^2{\bar n_{d-2}}+{\omega_2} {\bar n_{d-2}}+{s_1} {\mathrm{Sq}}^1{\bar n_{d-2}}.
```

In shifted coordinates, write $`d\check n_{d-1}=\check{\mathcal O}_d`$.
The two dimensions then read

| Dimension | $`\check{\mathcal O}_d`$ | $`d\bar n_{d-2}^{[1]}`$ |
|---|---|---|
| 3+1D | $`\check\omega_2\bar n_1`$ | $`\bar n_1^2+s_1\bar n_1`$ |
| 4+1D | $`\bar n_2^2+\check\omega_2\bar n_2`$ | $`\bar n_2\cup_1\bar n_2+s_1\bar n_2`$ |

The complex-fermion equation, expressed in these shifted inputs, is

<a id="eq-l2"></a>

**(L2)**

```math
d{n_{d}}={\mathcal O_{d+1}}({n_{d-2}},{\check n_{d-1}})={\mathrm{Sq}}^2{\check n_{d-1}}+{s_1}{\mathrm{Sq}}^1{\check n_{d-1}}+{\omega_2}{\check n_{d-1}}+{\mathcal O^\psi_{d+1}}({n_{d-2}}).
```

For 3+1D,

<a id="eq-l3"></a>

**(L3)**

```math
\begin{aligned}
{\mathcal O^\psi_4}={}&\zeta_{2,1}({\check\omega_2},{\bar n_{1}})+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\bar n_{1}^{[1]}}\\
&+\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\bar n_{1}},\\
\zeta_{2,1}({\check\omega_2},{\bar n_{1}})(01234)={}&{\check\omega_2}(012){\check\omega_2}(023){\bar n_{1}}(23){\bar n_{1}}(34).
\end{aligned}
```

For 4+1D,

<a id="eq-l4"></a>

**(L4)**

```math
\begin{aligned}
{\mathcal O^\psi_5}={}&\zeta_{2,2}({\bar n_{2}},{\bar n_{2}})+\zeta_{2,2}({\check\omega_2},{\bar n_{2}})
 +{\bar n_{2}}^2\cup_3({\check\omega_2}{\bar n_{2}})+{\bar n_{2}^{[1]}}\,d{\bar n_{2}^{[1]}}+{(\bar n_2\cup_1\bar n_2)}\cup_1({s_1}{\bar n_{2}})\\
&+{s_1}\big[{\bar n_{2}}^2\cup_4({\check\omega_2}{\bar n_{2}})+({\bar n_{2}}\cup_1{s_1}){\bar n_{2}}+{\bar n_{2}}\cup_1{(\bar n_2\cup_1\bar n_2)}+{\bar n_{2}}^2\big]\\
&+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\bar n_{2}^{[1]}}
 +\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\bar n_{2}},\\
\zeta_{2,2}(x,y)={}&\mathop{\mathrm{MS}}\nolimits_{1231343}(x,x,y,y).
\end{aligned}
```

These are explicit cochains. The $`\zeta`$ and interval-cut definitions
are part of the formulas; no unspecified primitive is being chosen.

<a id="lower-stacking"></a>
## Lower stacking equations

In shifted coordinates the Majorana correction is

<a id="eq-p1"></a>

**(P1)**

```math
\begin{aligned}
\check{\mathcal E}_{d-1}
 &=\bar n_{d-2}\cup_{d-3}\overline{n'_{d-2}},\\
N_{d-2}&=n_{d-2}+n'_{d-2},\\
\check N_{d-1}
 &=\check n_{d-1}+\check n'_{d-1}+\check{\mathcal E}_{d-1}.
\end{aligned}
```

The native output and the complex-fermion output are

<a id="eq-p2"></a>

**(P2)**

```math
\begin{aligned}
\mathcal E_{d-1}
 &=\check{\mathcal E}_{d-1}
   +s_1(\bar n_{d-2}\cup_{d-2}\overline{n'_{d-2}}),\\
N_{d-1}&=n_{d-1}+n'_{d-1}+\mathcal E_{d-1},\\
N_d&=n_d+n'_d+\mathcal E_d.
\end{aligned}
```

The check on a correction denotes the correction in shifted coordinates,
not a different operation. The bit identity behind (P2) is

```math
\bar N_{d-2}^{[1]}=\bar n_{d-2}^{[1]}+\overline{n'_{d-2}}^{[1]}
 +\bar n_{d-2}\cup_{d-2}\overline{n'_{d-2}}.
```

### The 3+1D complex-fermion correction

Here $`\check{\mathcal E}_2=\bar n_1\overline{n'_1}`$.

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

The $`\Delta`$ in the last line uses the stacking rule stated at the start;
its argument is written out, so no additional one-state symbol is needed.

### The 4+1D complex-fermion correction

Here $`\check{\mathcal E}_3=\bar n_2\cup_1\overline{n'_2}`$ and
$`d\check{\mathcal E}_3=\bar n_2\overline{n'_2}+\overline{n'_2}\bar n_2`$.

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

The finite polynomials in this correction are

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

The digit terms in (P4) include its closed $`\bar n_2\overline{n'_2}`$
contribution once.

<a id="shared-terminal-source"></a>
## Shared terminal source

This section is a function of a degree-two integer field $`n_2`$, a
shifted degree-three Majorana field $`\check n_3`$, and a degree-four fermion
field $`n_4`$. In 4+1D these are the physical fields. In the 3+1D formulas
below they will be the explicitly constructed parameter fields of the
same degrees. This lets the long source be written once.

The integer residuals are

<a id="eq-s1"></a>

**(S1)**

```math
\begin{aligned}
\mathcal P_{s_1}(\check\omega_2)
 &=\widetilde{\check\omega_2}\,\widetilde{\check\omega_2}
   +\widetilde{\check\omega_2}\cup_1d_{s_1}\widetilde{\check\omega_2},\\
B_4^\psi
 &=\frac{\widetilde{\check{\mathcal O}_4}-n_2^2
   -\widetilde{\check\omega_2}n_2}{2},\\
B_4&=\beta^\circ\check n_3+B_4^\psi
 =\frac{d\widetilde{\check n_3}-n_2^2
   -\widetilde{\check\omega_2}n_2}{2},\\
dB_4&=-(\beta_{s_1}\check\omega_2)n_2.
\end{aligned}
```

All three integer expressions $`B_4,B_4^\psi,\mathcal P_{s_1}`$ are
untwisted. In particular, $`B_4`$ is generally not closed; its differential
is part of the formula. The binary background carry is simply
$`\overline{\beta_{s_1}\check\omega_2}`$, and its next digit is
$`\overline{\beta_{s_1}\check\omega_2}^{[1]}`$.

The reused source terms are

<a id="eq-s2"></a>

**(S2)**

```math
\begin{aligned}
\mathcal C_6={}&\mathop{\mathrm{MS}}\nolimits_{12132434}({\overline{\beta_{s_1}\check\omega_2}},{\overline{\beta_{s_1}\check\omega_2}},{\bar n_{2}},{\bar n_{2}})
 +{\overline{\beta_{s_1}\check\omega_2}^{[1]}}({\bar n_{2}}\cup_1{\bar n_{2}})+({s_1}{\overline{\beta_{s_1}\check\omega_2}}){\bar n_{2}^{[1]}}+{s_1}({\overline{\beta_{s_1}\check\omega_2}}\cup_1{s_1}){\bar n_{2}},\\
\mathcal H_6({n_{2}},{\check n_{3}})={}&T_6({\check n_{3}};{\omega_2},{s_1})+{\check n_{3}}{(\overline{\beta\omega_2}+s_1\omega_2)}
 +({\mathrm{Sq}}^2{\check n_{3}}+{s_1}{\mathrm{Sq}}^1{\check n_{3}}+{\omega_2}{\check n_{3}})\cup_4{\mathcal O^\psi_5}+y_6({n_{2}};{\omega_2},{s_1})\\
&+{\overline{\beta^\circ\check n_3}}\cup_2{\overline{B_4^\psi}}+{s_1}\big({\overline{\beta^\circ\check n_3}}\cup_3{\overline{B_4^\psi}}\big),\\
\mathcal A_6({n_{2}},{\check n_{3}},{n_{4}})={}&{\mathrm{Sq}}^2{n_{4}}+{\omega_2}{n_{4}}+\mathcal H_6({n_{2}},{\check n_{3}}),\\
\mathcal Q_6({n_{2}},{\check n_{3}})={}&{B_4}\cup_2{B_4}+{B_4}\cup_3d{B_4}
 +\widetilde {\omega_2} {B_4}-\widetilde{\mathcal C_6}.
\end{aligned}
```

Here $`T_6`$ and $`y_6`$ are the complete finite operations in
[Source operations](formulas/SOURCE_OPERATIONS.md); all their fixed
coefficients appear in [Coefficients](formulas/COEFFICIENTS.md).
The shared additive source is

<a id="eq-s3"></a>

**(S3)**

```math
{\widehat{\mathcal O}_6^{\rm base}}({n_{2}},{\check n_{3}},{n_{4}})=\frac12\mathcal A_6
 +\frac14\mathcal Q_6
 +\frac1{16}\mathcal P_{s_1}({\check\omega_2}){n_{2}}+\frac18\widetilde {\check\omega_2} {n_{2}}^2
 \pmod1.
```

<a id="three-dimensional-pair"></a>
## The 3+1D terminal pair

The physical fields here are $`n_1,n_2,n_3`$. In the following formula,
$`\mathcal A_6,\mathcal Q_6`$ are evaluated on the parameter fields specified
just below; they are not evaluated on fields of the wrong degree.

<a id="eq-t3"></a>

**(T3)**

```math
\boxed{\begin{aligned}
{\widehat{\mathcal O}}_5({n_{1}},{\check n_{2}},{n_{3}})&=\frac12\tau_I\mathcal A_6
 +\frac14\tau_I\mathcal Q_6+\frac1{16}\mathcal P_{s_1}({\check\omega_2}){n_{1}},\\
{\widehat{\mathcal E}}_4({n_{1}},{\check n_{2}},{n_{3}};{n'_{1}},{\check n'_{2}},{n'_{3}})&=\frac12\tau_\triangle\mathcal A_6
 +\frac14\tau_\triangle\mathcal Q_6-\frac18\widetilde {\check\omega_2} {n_{1}} {n'_{1}}.
\end{aligned}}
```

The output phase is
$`\nu_4^{\mathrm{out}}=\nu_4\nu'_4\exp(2\pi i\widehat{\mathcal E}_4)`$.
The lower output is (P2),(P3). First define the two parameter corrections

<a id="eq-t3a"></a>

**(T3a)**

```math
\begin{aligned}
{D_3}({n_{1}},{\check n_{2}})&={\check\omega_2}{\bar n_{1}^{[1]}}+{\check n_{2}}\cup_2d{\check n_{2}}+({s_1}\cup_1{\omega_2}){\bar n_{1}},\\
g_2&={\bar n_{1}^{[1]}}{\overline{n'_{1}}}+({\bar n_{1}}+{\bar n_{1}^{[1]}}){\overline{n'_{1}}^{[1]}}+{\check{\mathcal E}_{2}}\cup_2({\check n_{2}}+{\check n'_{2}})+{\check{\mathcal E}_{2}}
 +({s_1}\cup_1{\bar n_{1}}){(\bar n_{1}\cup_{1}\overline{n'_{1}})}+({s_1}\cup_1{(\bar n_{1}\cup_{1}\overline{n'_{1}})})({\bar n_{1}}+{\overline{n'_{1}}}).
\end{aligned}
```

On the oriented triangle $`012`$, the integer one-cocycles
$`\theta_1,\theta'_1`$ have edge values $`(01,12,02)=(1,0,1),(0,1,1)`$.
The binary one-cochain $`\chi_1`$ has values $`(0,0,1)`$, so
$`d\chi_1=\bar\theta_1\overline{\theta'_1}`$.
Backgrounds and physical fields are pulled from the base; the three
parameter cochains are pulled from the triangle. In binary expressions, the integer parameter cocycles act through their reductions modulo two; the integer field retains their integer values. Define

<a id="eq-t3b"></a>

**(T3b)**

```math
\begin{aligned}
{n_2^\triangle}&={\theta_1} {n_{1}}+{\theta'_1} {n'_{1}},\\
{\check n_3^\triangle}&={\theta_1} {\check n_{2}}+{\theta'_1} {\check n'_{2}}+({\check\omega_2}\cup_1{\theta_1}){\bar n_{1}}
 +({\check\omega_2}\cup_1{\theta'_1}){\overline{n'_{1}}}+{\chi_1} {\check{\mathcal E}_{2}}+{\theta_1}({\bar n_{1}}\cup_1{\theta'_1}){\overline{n'_{1}}},\\
{n_4^\triangle}&={(\mathsf h_4^{(2)})^*}{\mathcal O_5[n_2^\triangle,\check n_3^\triangle]}+{\theta_1}({n_{3}}+{D_3}({n_{1}},{\check n_{2}}))
 +{\theta'_1}({n'_{3}}+{D_3}({n'_{1}},{\check n'_{2}}))\\
&\quad+{\chi_1}\big({\mathcal E_3}+{D_3}({N_{1}},{\check N_{2}})+{D_3}({n_{1}},{\check n_{2}})+{D_3}({n'_{1}},{\check n'_{2}})\big)
 +(d{\chi_1})g_2.
\end{aligned}
```

For the interval use $`\theta_1(01)=1`$ and omit the second input:

<a id="eq-t3c"></a>

**(T3c)**

```math
{n_2^I}={\theta_1} {n_{1}},\qquad
{\check n_3^I}={\theta_1} {\check n_{2}}+({\check\omega_2}\cup_1{\theta_1}){\bar n_{1}},\qquad
{n_4^I}={(\mathsf h_4^{(2)})^*}{\mathcal O_5}({n_2^I},{\check n_3^I})
 +{\theta_1}({n_{3}}+{D_3}({n_{1}},{\check n_{2}})).
```

The two- and three-factor grid definitions use the same notation as the
corresponding appendix. The interval sum has six paths and the triangle
sum fifteen. Apply coefficient transports before taking either sum.

For comparison with the older direct fermion coordinate, the change is

<a id="eq-t3d"></a>

**(T3d)**

```math
{n_3^{\mathrm{old}}}={n_{3}}+\kappa_3({n_{1}},{\check n_{2}}),\qquad
\kappa_3=({\bar n_{1}}+{s_1}){\check n_{2}}+{\check\omega_2}{\bar n_{1}^{[1]}}+[{\check\omega_2}\cup_1({\bar n_{1}}+{s_1})]{\bar n_{1}}.
```

The corresponding stacking correction must change with it:

```math
\mathcal E_{3,\mathrm{old}}=\mathcal E_3+\Delta\kappa_3.
```

In particular, $`n_1=0`$ does not by itself remove this change if $`s_1\ne0`$.

<a id="four-dimensional-pair"></a>
## The 4+1D terminal pair

The fields $`n_2,\check n_3,n_4`$ now have their physical degrees. The source is

<a id="eq-t4"></a>

**(T4)**

```math
\boxed{{\widehat{\mathcal O}}_6({n_{2}},{\check n_{3}},{n_{4}})={\widehat{\mathcal O}_6^{\rm base}}({n_{2}},{\check n_{3}},{n_{4}})+\frac1{12}{n_{2}}^3\pmod1.}
```

The cubic term is retained in 4+1D. It vanishes on the interval and
triangle fields used above. The lower output is fixed by (P2),(P4).
Only one new integer carry is needed for the product:

<a id="eq-t4a"></a>

**(T4a)**

```math
\begin{aligned}
\lambda_3&=\frac{\widetilde{\check N_3}-\widetilde{\check n_3}
 -\widetilde{\check n'_3}+n_2\cup_1n'_2}{2},\\
\Delta B_4&=d\lambda_3-n'_2n_2,\\
\overline{\Delta B_4}&=d\bar\lambda_3+\overline{n'_2}\bar n_2.
\end{aligned}
```

The quantities $`\lambda_3,B_4,\Delta B_4`$ are untwisted integers.
A bar on any of them has the same mod-two meaning as everywhere else.
There are no separate symbols for their parities.

The binary terms of the phase correction are

<a id="eq-t4b"></a>

**(T4b)**

```math
\begin{aligned}
\mathcal V_5={}&{\bar B_4}\cup_3{\overline{B'_4}}+d{\bar B_4}\cup_4{\overline{B'_4}}+({\bar B_4}+{\overline{B'_4}})\cup_3{\overline{\Delta B_4}}
 +(d{\bar B_4}+d{\overline{B'_4}})\cup_4{\overline{\Delta B_4}}\\
&+{\mathrm{Sq}}^2{\bar\lambda_3}+({\overline{n'_{2}}}{\bar n_{2}})\cup_3d{\bar\lambda_3}+{\omega_2}{\bar\lambda_3}+({\overline{\beta_{s_1}\check\omega_2}^{[1]}}+{\overline{\beta_{s_1}\check\omega_2}}){(\bar n_{2}\cup_{2}\overline{n'_{2}})}\\
&+\zeta_{2,2}({\overline{n'_{2}}},{\bar n_{2}})+{\check n'_{3}}{\bar n_{2}}+{\overline{n'_{2}}}{\check n_{3}}+({\check\omega_2}\cup_1{\overline{n'_{2}}}){\bar n_{2}}
 +{\overline{n'_{2}}^{[1]}}({\bar n_{2}}\cup_1{\bar n_{2}})+{s_1}{\overline{n'_{2}}}{\bar n_{2}^{[1]}}+{s_1}({\overline{n'_{2}}}\cup_1{s_1}){\bar n_{2}},\\
\Phi_5={}&\zeta_{2,2}({\bar n_{2}},{\overline{n'_{2}}})+{\bar n_{2}}\cup_1d{\check n'_{3}}+{\bar n_{2}^{[1]}}({\overline{n'_{2}}}\cup_1{\overline{n'_{2}}})
 +({\check\omega_2}\cup_1{\bar n_{2}}){\overline{n'_{2}}}+{s_1}{\bar n_{2}}{\overline{n'_{2}}^{[1]}}+{s_1}({\bar n_{2}}\cup_1{s_1}){\overline{n'_{2}}}+{\check{\mathcal E}_{3}}({\bar n_{2}}+{\overline{n'_{2}}})+{\check\omega_2}{\check{\mathcal E}_{3}},\\
\varepsilon_5={}&{n_{4}}\cup_3{n'_{4}}+d{n_{4}}\cup_4{n'_{4}}+({n_{4}}+{n'_{4}})\cup_3{\mathcal E_4}
 +({\mathcal E_4}+{(\bar n_{2}\overline{n'_{2}})})\cup_3{(\bar n_{2}\overline{n'_{2}})}+d{N_{4}}\cup_4{(\bar n_{2}\overline{n'_{2}})},
\end{aligned}
```

The integral term is

<a id="eq-t4c"></a>

**(T4c)**

```math
\Pi_5={N_{2}}\widetilde {\check N_{3}}-{n_{2}}\widetilde {\check n_{3}}-{n'_{2}}\widetilde {\check n'_{3}}
 +({n_{2}}\cup_1\widetilde {\check\omega_2}){n'_{2}}+({n'_{2}}\cup_1\widetilde {\check\omega_2}){n_{2}}.
```

Together they give the complete additive phase correction

<a id="eq-t4d"></a>

**(T4d)**

```math
\boxed{\begin{aligned}
{\widehat{\mathcal E}}_5={}&\frac12[\varepsilon_5+\Phi_5+Z_5]
 +\frac14[\widetilde{\mathcal V_5}+\Pi_5]
 +\frac18\widetilde {\check\omega_2}({n_{2}}\cup_1{n'_{2}})\\
&+\frac13\big[({n'_{2}}-{n_{2}})({n_{2}}\cup_1{n'_{2}})-({n_{2}}\cup_1{n'_{2}})({n'_{2}}-{n_{2}})\big]\pmod1.
\end{aligned}}
```

The output is
$`(N_2,N_3,N_4,\nu_5\nu'_5\exp(2\pi i\widehat{\mathcal E}_5))`$.
The binary term $`Z_5`$ is the explicit finite transfer defined in
[Terminal transfer](formulas/TERMINAL_TRANSFER.md). Its kernel, face rule,
coefficient polynomials, and finite sum are all specified there.
The ordered $`1/3`$ term is retained; its cup products do not commute.

For comparison with the earlier source convention, denote its additive source by $`\widehat{\mathcal O}_{6,\mathrm{raw}}`$. The exact change, together with the displayed cubic contribution, is

<a id="eq-t4e"></a>

**(T4e)**

```math
{\widehat{\mathcal O}}_6=\widehat{\mathcal O}_{6,\mathrm{raw}}+d_{s_1}\Lambda_5+\frac1{12}{n_{2}}^3,
\qquad \Lambda_5=\frac14{\beta^\circ\check n_3}\cup_3{B_4^\psi}.
```

The source and stacking product in this guide use the same representative.
A change of source coordinates must be accompanied by the corresponding
change of product coordinates.

## Classification and comparison of conventions

For fixed lower decorations, solve the obstruction equations modulo the
allowed gauge and lower-layer changes. A nonzero obstruction cochain can
be exact, or can become exact after those changes. Only a nontrivial final
class obstructs the decoration. Apply the full stacking law to accepted
representatives and reduce by those same equivalences. The resulting
extensions determine the full stacking group.

Some earlier manuscript drafts used a bar or prime for the shifted
Majorana field and a prime for $`\omega_2+s_1^2`$. Here these two shifts
always carry a check. A bar always means binary reduction, and a prime
always identifies the second input. This is a notation change, not a
change of cochain representative.

The readable formulas are independent of programming variable names. The
separate [implementation translation](../formulas/CODE_NOTATION.md) connects
this notation to the executable definitions. Fixed source coefficients and
previous computed results are unchanged by this notation organization.
