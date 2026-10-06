# FSPT obstruction functions and stacking twisters

Read each dimension on its own. In every dimension the obstruction functions
come first, followed by the complete stacking law.

| Dimension | Obstruction functions | Stacking twisters |
|---|---|---|
| 2+1D | [Obstructions](#obstructions-2d) | [Stacking](#stacking-2d) |
| 3+1D | [Obstructions](#obstructions-3d) | [Stacking](#stacking-3d) |
| 4+1D | [Obstructions](#obstructions-4d) | [Stacking](#stacking-4d) |

## Notation

The backgrounds are $`\omega_2\in Z^2(G_b,\mathbb Z_2)`$ and
$`s_1\in Z^1(G_b,\mathbb Z_2)`$, held fixed during stacking.
A subscript gives the cochain degree. Each dimension defines its own
fields; their physical roles are not inferred from another section.
The superscripts $`c,\gamma,\psi`$ retain the paper's physical labels:
complex fermion, Majorana, and p+ip. A mixed superscript identifies a
contribution involving those layers. The pieces are parts of the full
cochain equation; they need not be separately closed. In the p+ip sections they refer to the
displayed shifted Majorana field; rewriting it in native fields redistributes
some mixed terms.

<a id="conventions-and-coordinates"></a>

### Arithmetic and modifiers

A prime denotes the second stacking input. The outputs are $`N_j`$ and
$`\nu_j^{\mathrm{out}}`$. A hat denotes the additive phase,
$`\nu_j=\exp(2\pi i\widehat\nu_j)`$, with
$`\widehat\nu_j\in\mathbb R/\mathbb Z`$. The same convention applies to
phase obstructions $`\widehat{\mathcal O}`$ and corrections
$`\widehat{\mathcal E}`$.

A bar means reduction modulo two; a tilde means the second binary digit:

```math
\bar x=x\pmod2,\qquad
\widetilde x=\overline{\lfloor x/2\rfloor}.
```

Floors are mathematical floors, including for negative integers. Integer
lifts are implicit, so tilde always has the meaning above. A check denotes
an explicitly defined shift. The background shift is

<a id="eq-c1"></a>

**(C1)**

```math
\check\omega_2=\omega_2+s_1\cup s_1.
```

### Integer lifts are implicit in integer arithmetic

A named binary cochain in an integer expression means its canonical
$`0,1`$ lift. No lift symbol is needed. Sums, differences, differentials, and
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

The fixed quadratic background cochain is:

```math
\mathcal P_{s_1}(\check\omega_2)
 =\check\omega_2\check\omega_2
  +\check\omega_2\cup_1d_{s_1}\check\omega_2\quad\text{in }\mathbb Z.
```

This is a fixed integer representative of the twisted Pontryagin-square
expression; keep the displayed representative when it is multiplied by
$`1/16`$. It is not an unspecified modulo-four class.

Finite definitions of higher cups and ordered word operations are in
[Operations](formulas/OPERATIONS.md). Parameter-space constructions and
representative changes have their own files; they are not additional
physical data in the equations below.

<a id="two-dimensional"></a>
## 2+1D

The fields are the binary Majorana decoration $`n_1`$, the binary
complex-fermion decoration $`n_2`$, and the bosonic phase $`\nu_3`$.
This section is the zero-integer-decoration sector. The scope of the
chiral sector is stated with the complete formulas below.

<a id="obstructions-2d"></a>
### Obstruction functions

The phase uses the manuscript operator ordering. Its paired map to the
previous coordinate is given in the [2+1D coordinate note](formulas/MAJORANA_AND_ENDPOINTS.md#eq-m12-2d).

The lower equations are

**(M2, 2+1D)**

```math
\begin{aligned}
dn_1&=0,\\
dn_2=\mathcal O_3
 &=\mathrm{Sq}^2n_1+\omega_2n_1+s_1\overline{\beta n_1}.
\end{aligned}
```

The terminal obstruction is the sum of its three operator contributions:

**(M3, 2+1D: obstruction)**

```math
d_{s_1}\widehat\nu_3=\widehat{\mathcal O}_4
 =\widehat{\mathcal O}^{c}_4
  +\widehat{\mathcal O}^{\gamma}_4
  +\widehat{\mathcal O}^{c\gamma}_4.
```

**Complex-fermion contribution.**

**(M3c, 2+1D)**

```math
\widehat{\mathcal O}^{c}_4
 =\frac12\big[\omega_2n_2+n_2\cup n_2
   +dn_2\cup_1n_2\big].
```

**Majorana contribution.**

**(M6, 2+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}^\gamma_4(n_1)={}&\frac12\big[
 \mathop{\mathrm{MS}}\nolimits_{123134}(\omega_2,\omega_2,n_1,n_1)\\
&\qquad+(\omega_2n_1)\cup_2(s_1\overline{\beta n_1})\\
&\qquad+(\omega_2\cup_1s_1)\overline{\beta n_1}+s_1(s_1+n_1)\overline{\beta n_1}\big]\\
&+\frac14\big[{\omega_2} \beta n_1+{s_1}\,{n_1}\,\beta n_1\big].
\end{aligned}
```

**Mixed contribution.**

**(M3cγ, 2+1D)**

```math
\widehat{\mathcal O}^{c\gamma}_4
 =\frac12\big[dn_2\cup_2dn_2\big].
```


<a id="stacking-2d"></a>
### Stacking twisters

The lower stacking law is

**(M1, 2+1D)**

```math
\begin{aligned}
N_1&=n_1+n'_1,\\
\mathcal E_2&=(n_1\cup n'_1)+s_1(n_1\cup_1n'_1),\\
N_2&=n_2+n'_2+\mathcal E_2.
\end{aligned}
```

The terminal stacking law is

**(M3E, 2+1D)**

```math
\begin{aligned}
\widehat\nu_3^{\mathrm{out}}
 &=\widehat\nu_3+\widehat\nu'_3+\widehat{\mathcal E}_3,\\
\widehat{\mathcal E}_3
 &=\widehat{\mathcal E}^{c}_3
  +\widehat{\mathcal E}^{\gamma}_3
  +\widehat{\mathcal E}^{c\gamma}_3.
\end{aligned}
```

**Complex-fermion contribution.**

**(M3Ec, 2+1D)**

```math
\widehat{\mathcal E}^{c}_3
 =\frac12\big[n_2\cup_1n'_2
 +(n_2+n'_2)\cup_1\mathcal E_2\big].
```

**Majorana contribution.**
The binary antiunitary term is

**(M10, 2+1D)**

```math
\begin{aligned}
\mathcal L_3={}&s_1((s_1\cup_1n_1)+(s_1\cup_1n'_1)+[s_1\cup_1(n_1\cup_1n'_1)])(n_1\cup_1n'_1)\\
&+(s_1\cup_1n_1) (n_1\cup_1n'_1)N_1\\
&+((s_1\cup_1n_1) n_1+n_1 (s_1\cup_1n'_1)+s_1n_1+n_1s_1)(n_1\cup_1n'_1)\\
&+s_1((n_1\cup_1n'_1)n_1+n_1n'_1+n'_1(n_1\cup_1n'_1)).
\end{aligned}
```

The pure Majorana phase correction is

**(M11, 2+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}^\gamma_3={}&
\frac14\big[\beta n_1\cup_1\beta n'_1\\
&\qquad-(\beta n_1+\beta n'_1)({n_1}\cup_1{n'_1})\\
&\qquad-({n_1}\cup_1{n'_1})(\beta n_1+\beta n'_1)\\
&\qquad+({n_1}\cup_1{n'_1})d({n_1}\cup_1{n'_1})\big]\\
&+\frac12[n_1\cup_1(n_1n'_1)]n'_1
 -\frac18\overline{N_1^3}+\frac18\overline{n_1^3}+\frac18\overline{(n'_1)^3}\\
&+\frac12(\omega_2N_1)\cup_2(n_1n'_1)\\
&-\frac14{\omega_2} ({n_1}\cup_1{n'_1})
 +\frac12\mathcal L_3+\frac14\overline{s_1n_1n'_1}\\
&+\frac12\big[(\omega_2\cup_1s_1)(n_1\cup_1n'_1)\\
&\qquad+(\omega_2N_1)\cup_2(s_1(n_1\cup_1n'_1))\\
&\qquad+(\omega_2n'_1)\cup_3(s_1n_1^2)\big]
 \pmod1.
\end{aligned}
```

The bars on the eighth-valued terms and on $`\overline{s_1n_1n'_1}`$ reduce
the complete indicated product. In contrast, $`n_1\cup_1n'_1`$ in the
quarter-valued bracket is a signed integer cup; its differential is also
integral.

**Mixed contribution.**

**(M3Ecγ, 2+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}^{c\gamma}_3
 =\frac12\big[&dn_2\cup_2n'_2+N_2\cup_2dN_2\\
 &+n_2\cup_2dn_2+n'_2\cup_2dn'_2\big].
\end{aligned}
```

The formulas above cover zero integer decoration. A neutral chiral
integer factor can be adjoined for split unitary symmetry; general
nonsplit nonzero-chiral cochain inputs are outside this endpoint.
The [endpoint reference](formulas/MAJORANA_AND_ENDPOINTS.md#majorana-2d)
states the scope and phase-coordinate map.

<a id="three-dimensional"></a>
## 3+1D

Throughout this section the physical fields are:

| Field | Physical role | Coefficients |
|---|---|---|
| $`n_1`$ | p+ip decoration | $`\mathbb Z_{s_1}`$ |
| $`n_2`$ | Majorana decoration | $`\mathbb Z_2`$ |
| $`n_3`$ | Complex-fermion decoration | $`\mathbb Z_2`$ |
| $`\nu_4`$ | Bosonic phase | $`U(1)_{s_1}`$ |

The contributions below are grouped in the shifted Majorana coordinate

<a id="eq-c1-3d"></a>

**(3D coordinates)**

```math
\check n_2=n_2+s_1\widetilde n_1.
```

<a id="obstructions-3d"></a>
<a id="lower-sources"></a>
### Obstruction functions

The p+ip decoration satisfies $`d_{s_1}n_1=0`$. The next equations are binary.

#### p+ip contribution to the Majorana equation

<a id="eq-l1"></a>

**(L1)**

```math
dn_2=\mathcal O_3^\psi=\omega_2\bar n_1+s_1\bar n_1^2,\qquad d\check n_2=\check\omega_2\bar n_1.
```

#### Majorana, mixed, and p+ip contributions to the complex-fermion equation

<a id="eq-l2"></a>

**(L2)**

```math
\begin{aligned}
dn_3&=\mathcal O_4=\mathcal O_4^\gamma+\mathcal O_4^{\gamma\psi}+\mathcal O_4^\psi,\\
\mathcal O_4^\gamma&=\check n_2^2+s_1(\check n_2\cup_1\check n_2)+\omega_2\check n_2,\\
\mathcal O_4^{\gamma\psi}&=\check n_2\cup_1d\check n_2+s_1(\check n_2\cup_2d\check n_2).
\end{aligned}
```

In the mixed part, substitute $`d\check n_2=\check\omega_2\bar n_1`$.
The remaining p+ip contribution is

<a id="eq-l3"></a>

**(L3)**

```math
\begin{aligned}
{\mathcal O^\psi_4}={}&\zeta_{2,1}({\check\omega_2},{\bar n_{1}})+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\widetilde n_{1}}\\
&+\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\bar n_{1}},\\
\zeta_{2,1}({\check\omega_2},{\bar n_{1}})(01234)={}&{\check\omega_2}(012){\check\omega_2}(023){\bar n_{1}}(23){\bar n_{1}}(34).
\end{aligned}
```

Here $`d\widetilde n_1=\bar n_1^2+s_1\bar n_1`$.

#### Full bosonic obstruction

<a id="eq-t3"></a>

**(T3: obstruction)**

```math
d_{s_1}\widehat\nu_4=\widehat{\mathcal O}_5(n_1,\check n_2,n_3;\omega_2,s_1).
```

The complete finite definition is in the separate
[terminal obstruction construction](formulas/THREE_DIMENSIONAL_TERMINAL.md#eq-t3).
It retains every complex-fermion, Majorana, p+ip, and mixed term in this
phase coordinate. The parameter fields used to evaluate it are defined
only in that technical file. The three physical arguments here remain
p+ip, shifted Majorana, and complex fermion.

<a id="stacking-3d"></a>
<a id="lower-stacking"></a>
### Stacking twisters

The two inputs have the same backgrounds. First combine the decoration
fields, then add the bosonic correction.

#### p+ip contribution to Majorana stacking

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

#### Majorana contribution to complex-fermion stacking

<a id="eq-p3"></a>

**(P3)**

```math
\begin{aligned}
\mathcal E_3&=\mathcal E_3^\gamma+\mathcal E_3^{\gamma\psi}+\mathcal E_3^\psi,\\
\mathcal E_3^\gamma&=\check n_2\cup_1\check n'_2+s_1(\check n_2\cup_2\check n'_2).
\end{aligned}
```

#### Mixed Majorana–p+ip contribution

```math
\mathcal E_3^{\gamma\psi}
 =d\check n_2\cup_2\check n'_2
 +(\check n_2+\check n'_2)\cup_1\check{\mathcal E}_2
 +s_1\big[(\check n_2+\check n'_2)\cup_2\check{\mathcal E}_2\big].
```

#### p+ip contribution

```math
\begin{aligned}\mathcal E_3^\psi={}&{z^\psi_3}({\bar n_{1}},{\overline{n'_{1}}})+[{\check\omega_2}({\bar n_{1}}+{\overline{n'_{1}}})]\cup_2{\check{\mathcal E}_{2}}+(d{\widetilde n_{1}}){\widetilde{n'_{1}}}\\
&+({s_1}{\bar n_{1}})\cup_1{\overline{n'_{1}}}^2+{\bar n_{1}} {s_1} {\overline{n'_{1}}}+{(\bar n_{1}\cup_{1}\overline{n'_{1}})} {s_1}({\bar n_{1}}+{\overline{n'_{1}}})\\
&+{s_1}\big[{s_1}{(\bar n_{1}\cup_{1}\overline{n'_{1}})}+{\bar n_{1}}\cup_1d{\widetilde{n'_{1}}}+{(\bar n_{1}\cup_{1}\overline{n'_{1}})}({\bar n_{1}}+{\overline{n'_{1}}})\big]+{\Delta[(\bar n_1^2\cup_1s_1)\bar n_1]},\\
{z^\psi_3}({\bar n_{1}},{\overline{n'_{1}}})={}&\mathop{\mathrm{MS}}\nolimits_{12314}({\bar n_{1}},{\bar n_{1}},{\overline{n'_{1}}},{\overline{n'_{1}}})
 =[{\bar n_{1}}\cup_1({\bar n_{1}}{\overline{n'_{1}}})]{\overline{n'_{1}}}.
\end{aligned}
```

The $`\Delta`$ acts on the entire bracket using the lower output. The
second digit satisfies

```math
\widetilde N_1=\widetilde n_1+\widetilde{n'_1}+\bar n_1\cup_1\overline{n'_1}.
```

#### Full bosonic stacking correction

<a id="eq-t3-product"></a>

**(T3: stacking)**

```math
\widehat\nu_4^{\mathrm{out}}
 =\widehat\nu_4+\widehat\nu'_4
 +\widehat{\mathcal E}_4(n_1,\check n_2,n_3;n'_1,\check n'_2,n'_3;\omega_2,s_1).
```

Use the complete [terminal stacking construction](formulas/THREE_DIMENSIONAL_TERMINAL.md#eq-t3)
on these physical inputs and the lower output just specified. It fixes
the entire correction, including the interactions between layers.
The separately displayed [closed-Majorana factors](formulas/MAJORANA_AND_ENDPOINTS.md#majorana-3d)
use their stated phase coordinate; they must not be inserted here on an
open Majorana cochain.

<a id="four-dimensional"></a>
## 4+1D

Throughout this section the physical fields are:

| Field | Physical role | Coefficients |
|---|---|---|
| $`n_2`$ | p+ip decoration | $`\mathbb Z_{s_1}`$ |
| $`n_3`$ | Majorana decoration | $`\mathbb Z_2`$ |
| $`n_4`$ | Complex-fermion decoration | $`\mathbb Z_2`$ |
| $`\nu_5`$ | Bosonic phase | $`U(1)_{s_1}`$ |

The contributions below are grouped in the shifted Majorana coordinate

<a id="eq-c1-4d"></a>

**(4D coordinates)**

```math
\check n_3=n_3+s_1\widetilde n_2.
```

<a id="obstructions-4d"></a>
### Obstruction functions

The p+ip decoration satisfies $`d_{s_1}n_2=0`$. The next equations are binary.

#### p+ip contribution to the Majorana equation

<a id="eq-l1-4d"></a>

**(L1–4D)**

```math
d{n_{3}}=\mathcal O_4[n_{2}]={\mathrm{Sq}}^2{\bar n_{2}}+{\omega_2} {\bar n_{2}}+{s_1} {\mathrm{Sq}}^1{\bar n_{2}}.
```

The shifted equation is $`d\check n_3=\check{\mathcal O}_4=\bar n_2^2+\check\omega_2\bar n_2`$.

#### Majorana, mixed, and p+ip contributions to the complex-fermion equation

<a id="eq-l2-4d"></a>

**(L2–4D)**

```math
\begin{aligned}
dn_4&=\mathcal O_5=\mathcal O_5^\gamma+\mathcal O_5^{\gamma\psi}+\mathcal O_5^\psi,\\
\mathcal O_5^\gamma&=\check n_3\cup_1\check n_3+s_1(\check n_3\cup_2\check n_3)+\omega_2\check n_3,\\
\mathcal O_5^{\gamma\psi}&=\check n_3\cup_2d\check n_3+s_1(\check n_3\cup_3d\check n_3).
\end{aligned}
```

Substitute the displayed value of $`d\check n_3`$ in the mixed part.
The p+ip contribution is

<a id="eq-l4"></a>

**(L4)**

```math
\begin{aligned}
{\mathcal O^\psi_5}={}&\zeta_{2,2}({\bar n_{2}},{\bar n_{2}})+\zeta_{2,2}({\check\omega_2},{\bar n_{2}})
 +{\bar n_{2}}^2\cup_3({\check\omega_2}{\bar n_{2}})+\mathrm{Sq}^3{\widetilde n_{2}}+{(\bar n_2\cup_1\bar n_2)}\cup_1({s_1}{\bar n_{2}})\\
&+{s_1}\big[{\bar n_{2}}^2\cup_4({\check\omega_2}{\bar n_{2}})+({\bar n_{2}}\cup_1{s_1}){\bar n_{2}}+{\bar n_{2}}\cup_1{(\bar n_2\cup_1\bar n_2)}+{\bar n_{2}}^2\big]\\
&+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\widetilde n_{2}}
 +\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\bar n_{2}},\\
\zeta_{2,2}(x,y)={}&\mathop{\mathrm{MS}}\nolimits_{1231343}(x,x,y,y).
\end{aligned}
```

Here $`d\widetilde n_2=\bar n_2\cup_1\bar n_2+s_1\bar n_2`$.

<a id="shared-terminal-source"></a>
<a id="four-dimensional-pair"></a>
#### Contributions to the bosonic obstruction

The integer residuals used here are

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

<a id="eq-s2"></a>
<a id="eq-s3"></a>

The phase is the sum of six displayed contributions:

<a id="eq-t4"></a>

**(T4)**

```math
\begin{aligned}
d_{s_1}\widehat\nu_5=\widehat{\mathcal O}_6
={}&\widehat{\mathcal O}_6^c
 +\widehat{\mathcal O}_6^{c\gamma}
 +\widehat{\mathcal O}_6^{c\psi}\\
 &+\widehat{\mathcal O}_6^\gamma
 +\widehat{\mathcal O}_6^{\gamma\psi}
 +\widehat{\mathcal O}_6^\psi.
\end{aligned}
```

**Complex-fermion and mixed contributions.**

The terms containing the complex-fermion cochain are

```math
\begin{aligned}
\widehat{\mathcal O}_6^c
 &=\frac12\big[n_4\cup_2n_4+\omega_2n_4\big],\\
\widehat{\mathcal O}_6^{c\gamma}
 &=\frac12n_4\cup_3
      (\mathcal O_5^\gamma+\mathcal O_5^{\gamma\psi}),\\
\widehat{\mathcal O}_6^{c\psi}
 &=\frac12n_4\cup_3\mathcal O_5^\psi.
\end{aligned}
```

Thus the $`c\gamma`$ contribution includes the effect of the nonclosed
Majorana layer. In particular its $`\mathcal O_5^{\gamma\psi}`$ term is an interaction
of all three layers; the grouping does not assert that this term vanishes.
These three expressions sum to
$`[\mathrm{Sq}^2n_4+\omega_2n_4]/2`$ in the current phase convention. The
operator-ordered closed-Majorana convention uses its explicitly paired
phase change and is not silently substituted here.

**Majorana contribution.**

The remaining contributions use the already defined integer cochain
$`B_4^\psi`$ and the open carry $`\beta^\circ\check n_3`$. No closed Bockstein is applied
to the nonclosed Majorana input:

```math
\begin{aligned}
\widehat{\mathcal O}_6^\gamma
={}&\frac12\Big[
 T_6[\check n_3;\omega_2,s_1]
 +\check n_3(\overline{\beta\omega_2}+s_1\omega_2)\Big]\\
 &+\frac14\Big[
 (\beta^\circ\check n_3)\cup_2(\beta^\circ\check n_3)
 +(\beta^\circ\check n_3)\cup_3d(\beta^\circ\check n_3)
 +\omega_2\beta^\circ\check n_3\Big].
\end{aligned}
```

**Mixed Majorana–p+ip contribution.**

```math
\begin{aligned}
\widehat{\mathcal O}_6^{\gamma\psi}
={}&\frac12\Big[
 (\mathcal O_5^\gamma+\mathcal O_5^{\gamma\psi})
     \cup_4\mathcal O_5^\psi
 +\overline{\beta^\circ\check n_3}\cup_2\overline{B_4^\psi}\\
 &\qquad+s_1\big(
    \overline{\beta^\circ\check n_3}\cup_3\overline{B_4^\psi}
   \big)\Big]\\
 &+\frac14\Big[
 (\beta^\circ\check n_3)\cup_2B_4^\psi
 +B_4^\psi\cup_2(\beta^\circ\check n_3)\\
 &\qquad+(\beta^\circ\check n_3)\cup_3dB_4^\psi
 +B_4^\psi\cup_3d(\beta^\circ\check n_3)\Big].
\end{aligned}
```

**p+ip contribution.**

```math
\begin{aligned}
\widehat{\mathcal O}_6^\psi
={}&\frac12y_6[n_2;\omega_2,s_1]\\
 &+\frac14\Big[
 B_4^\psi\cup_2B_4^\psi
 +B_4^\psi\cup_3dB_4^\psi+\omega_2B_4^\psi\Big]\\
 &-\frac14\overline{\Big[
 \mathop{\mathrm{MS}}\nolimits_{12132434}
 (\overline{\beta_{s_1}\check\omega_2},
  \overline{\beta_{s_1}\check\omega_2},\bar n_2,\bar n_2)
 +\widetilde{\beta_{s_1}\check\omega_2}
       (\bar n_2\cup_1\bar n_2)
 +(s_1\overline{\beta_{s_1}\check\omega_2})\widetilde n_2
 +s_1(\overline{\beta_{s_1}\check\omega_2}\cup_1s_1)\bar n_2
 \Big]}\\
 &+\frac1{16}\mathcal P_{s_1}(\check\omega_2)n_2
   +\frac18\check\omega_2n_2^2+\frac1{12}n_2^3.
\end{aligned}
```

The half-valued brackets are binary. Every quarter-valued bracket uses
integer arithmetic; the single barred polynomial is reduced as a whole
before it supplies its integer value. This is an exact expansion of
$`B_4=\beta^\circ\check n_3+B_4^\psi`$ in the current source, including its mixed
integer terms. It does not impose closure on either summand of $`B_4`$.

The fixed operations $`T_6,y_6`$ are defined in [Source operations](formulas/SOURCE_OPERATIONS.md); all coefficients are in [Coefficients](formulas/COEFFICIENTS.md).

<a id="stacking-4d"></a>
### Stacking twisters

#### p+ip contribution to Majorana stacking

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

In these coordinates $`d\check{\mathcal E}_3=\bar n_2\overline{n'_2}+\overline{n'_2}\bar n_2`$.

#### Majorana contribution to complex-fermion stacking

<a id="eq-p4"></a>

**(P4)**

```math
\begin{aligned}
\mathcal E_4&=\mathcal E_4^\gamma+\mathcal E_4^{\gamma\psi}+\mathcal E_4^\psi,\\
\mathcal E_4^\gamma&=\check n_3\cup_2\check n'_3+s_1(\check n_3\cup_3\check n'_3).
\end{aligned}
```

#### Mixed Majorana–p+ip contribution

```math
\begin{aligned}
\mathcal E_4^{\gamma\psi}={}&d\check n_3\cup_3\check n'_3
 +(\check n_3+\check n'_3)\cup_2\check{\mathcal E}_3\\
 &+s_1\big[d\check n_3\cup_4\check n'_3
 +(\check n_3+\check n'_3)\cup_3\check{\mathcal E}_3\big].
\end{aligned}
```

#### p+ip contribution

```math
\begin{aligned}\mathcal E_4^\psi={}&{z^\psi_4}({\bar n_{2}},{\overline{n'_{2}}})+[{\check\omega_2}({\bar n_{2}}+{\overline{n'_{2}}})]\cup_3{\check{\mathcal E}_{3}}
 +{\overline{n'_{2}}}^2\cup_4({\check\omega_2}{\bar n_{2}})+d{\check{\mathcal E}_{3}}\cup_4[{\check\omega_2}({\bar n_{2}}+{\overline{n'_{2}}})]\\
&+{\widetilde n_{2}}({\widetilde{n'_{2}}}+{\overline{n'_{2}}})+{\bar n_{2}}{\widetilde{n'_{2}}}+d{\widetilde n_{2}}\cup_1{\widetilde{n'_{2}}}+({\widetilde n_{2}}+{\widetilde{n'_{2}}}){(\bar n_{2}\cup_{2}\overline{n'_{2}})}\\
&+({s_1}{\bar n_{2}})\cup_2({\overline{n'_{2}}}\cup_1{\overline{n'_{2}}})+{\bar n_{2}}\cup_1({s_1}{\overline{n'_{2}}})+{(\bar n_{2}\cup_{2}\overline{n'_{2}})}\cup_1[{s_1}({\bar n_{2}}+{\overline{n'_{2}}})]\\
&+{s_1}\big[{s_1}{(\bar n_{2}\cup_{2}\overline{n'_{2}})}+{\bar n_{2}}\cup_2d{\widetilde{n'_{2}}}+{(\bar n_{2}\cup_{2}\overline{n'_{2}})}\cup_1({\bar n_{2}}+{\overline{n'_{2}}})+\ell_3({\bar n_{2}},{\overline{n'_{2}}})\big].
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

The second digit satisfies

```math
\widetilde N_2=\widetilde n_2+\widetilde{n'_2}+\bar n_2\cup_2\overline{n'_2}.
```

#### Contributions to the bosonic stacking correction

```math
\widehat\nu_5^{\mathrm{out}}
 =\widehat\nu_5+\widehat\nu'_5+\widehat{\mathcal E}_5.
```

The integer stacking carry and the repeated binary polynomial are

<a id="eq-t4a"></a>

**(T4A)**

```math
\begin{aligned}
\lambda_3&=\frac{\check N_3-\check n_3-\check n'_3+n_2\cup_1n'_2}{2},\\
\Delta B_4&=d\lambda_3-n'_2n_2,\\
\overline{\Delta B_4}&=d\bar\lambda_3+\overline{n'_2}\bar n_2.
\end{aligned}
```

The three Majorana fields in the numerator use their canonical integer
values. The quantities $`\lambda_3,B_4,\Delta B_4`$ are untwisted integers.
Evaluate the following polynomial modulo two before either integer use:

<a id="eq-t4b"></a>

**(T4B)**

```math
\begin{aligned}
\mathcal V_5={}&{\bar B_4}\cup_3{\overline{B'_4}}+d{\bar B_4}\cup_4{\overline{B'_4}}+({\bar B_4}+{\overline{B'_4}})\cup_3{\overline{\Delta B_4}}
 +(d{\bar B_4}+d{\overline{B'_4}})\cup_4{\overline{\Delta B_4}}\\
&+{\mathrm{Sq}}^2{\bar\lambda_3}+({\overline{n'_{2}}}{\bar n_{2}})\cup_3d{\bar\lambda_3}+{\omega_2}{\bar\lambda_3}+({\widetilde{\beta_{s_1}\check\omega_2}}+{\overline{\beta_{s_1}\check\omega_2}}){(\bar n_{2}\cup_{2}\overline{n'_{2}})}\\
&+\zeta_{2,2}({\overline{n'_{2}}},{\bar n_{2}})+{\check n'_{3}}{\bar n_{2}}+{\overline{n'_{2}}}{\check n_{3}}+({\check\omega_2}\cup_1{\overline{n'_{2}}}){\bar n_{2}}
 +{\widetilde{n'_{2}}}({\bar n_{2}}\cup_1{\bar n_{2}})+{s_1}{\overline{n'_{2}}}{\widetilde n_{2}}+{s_1}({\overline{n'_{2}}}\cup_1{s_1}){\bar n_{2}}.
\end{aligned}
```

In the current phase representative, the contributions containing a free
complex-fermion input can be separated exactly as follows:

```math
\begin{aligned}
\widehat{\mathcal E}_5^c
 &=\frac12n_4\cup_3n'_4,\\
\widehat{\mathcal E}_5^{c\gamma}
 &=\frac12\Big[
    (\mathcal O_5^\gamma+\mathcal O_5^{\gamma\psi})\cup_4n'_4
   +(n_4+n'_4)\cup_3
       (\mathcal E_4^\gamma+\mathcal E_4^{\gamma\psi})\Big],\\
\widehat{\mathcal E}_5^{c\psi}
 &=\frac12\Big[
    \mathcal O_5^\psi\cup_4n'_4
   +(n_4+n'_4)\cup_3\mathcal E_4^\psi\Big].
\end{aligned}
```

The unprimed obstruction blocks in this formula are evaluated on the
first input. Their sum is $`dn_4`$. The $`c\gamma`$ block includes the
nonclosed-Majorana corrections, including interactions of all three
layers. The total of these three terms is exactly

```math
\frac12\Big[n_4\cup_3n'_4+dn_4\cup_4n'_4
                   +(n_4+n'_4)\cup_3\mathcal E_4\Big].
```

The rest of the terminal correction is independent of the freely chosen
complex-fermion cochains. The complete terminal correction is therefore:

<a id="eq-t4c"></a>
<a id="eq-t4d"></a>

**(T4D)**

```math
\begin{aligned}
\widehat{\mathcal E}_5
={}&\widehat{\mathcal E}_5^c+\widehat{\mathcal E}_5^{c\gamma}+\widehat{\mathcal E}_5^{c\psi}\\
 &+\frac12\Big[
 (\mathcal E_4+\bar n_2\overline{n'_2})
       \cup_3(\bar n_2\overline{n'_2})
 +\mathcal O_5[N_2,\check N_3]
       \cup_4(\bar n_2\overline{n'_2})\\
 &\qquad+\zeta_{2,2}(\bar n_2,\overline{n'_2})
 +\bar n_2\cup_1d\check n'_3
 +\widetilde n_2(\overline{n'_2}\cup_1\overline{n'_2})\\
 &\qquad+(\check\omega_2\cup_1\bar n_2)\overline{n'_2}
 +s_1\bar n_2\widetilde{n'_2}
 +s_1(\bar n_2\cup_1s_1)\overline{n'_2}\\
 &\qquad+\check{\mathcal E}_3(\bar n_2+\overline{n'_2})
 +\check\omega_2\check{\mathcal E}_3+Z_5\Big]\\
 &+\frac14\Big[
 \mathcal V_5+\Delta(n_2\check n_3)
 +(n_2\cup_1\check\omega_2)n'_2
 +(n'_2\cup_1\check\omega_2)n_2\Big]\\
 &+\frac18\check\omega_2(n_2\cup_1n'_2)\\
 &+\frac13\Big[
  (n'_2-n_2)(n_2\cup_1n'_2)
 -(n_2\cup_1n'_2)(n'_2-n_2)\Big]\pmod1.
\end{aligned}
```

The final display includes the full Majorana, p+ip, and mixed contribution.
Their finite transfer is kept together here; $`Z_5`$ is not a pure-p+ip
operation. Its [complete definition](formulas/TERMINAL_TRANSFER.md) fixes
every term. These formulas introduce no new phase coordinate or adjustable
primitive.

The replacement of $`dN_4`$ by $`\mathcal O_5[N_2,\check N_3]`$ uses the already verified
lower product equation and removes the apparent dependence of this
remaining term on the free complex-fermion inputs. All previous lift,
integer-order and phase conventions are unchanged.


## Finite definitions and coordinate maps

- [3+1D terminal construction](formulas/THREE_DIMENSIONAL_TERMINAL.md)
- [Source operations](formulas/SOURCE_OPERATIONS.md) and [fixed coefficients](formulas/COEFFICIENTS.md)
- [4+1D terminal transfer](formulas/TERMINAL_TRANSFER.md)
- [Closed-Majorana phase formulas](formulas/MAJORANA_AND_ENDPOINTS.md)
- [Changes of representative](formulas/REPRESENTATIVES.md)
- [Formula-to-code translation](../formulas/CODE_NOTATION.md)

A nonzero obstruction cochain may be a coboundary. Only its nontrivial
class after the allowed lower-layer changes obstructs the decoration.
