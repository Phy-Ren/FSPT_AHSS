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
The physical labels $`c,\gamma,\psi`$ mean, respectively,
complex fermion, Majorana, and p+ip. The fixed order for resolved
contributions is $`c,c\gamma,c\psi,\gamma,\gamma\psi,\psi`$;
absent contributions are omitted. A combined finite contribution is
identified explicitly and is not labeled as a pure physical layer. A mixed superscript identifies a
contribution involving those layers. The pieces are parts of the full
cochain equation; they need not be separately closed. In the p+ip sections they refer to the
displayed shifted Majorana field; rewriting it in native fields redistributes
some mixed terms.

<a id="conventions-and-coordinates"></a>

### Arithmetic and modifiers

A prime denotes the second stacking input. On an individual field it is
placed outside the modifier: $`\bar n'_j,\widetilde n'_j,\check n'_j`$. The outputs are $`N_j`$ and
$`\nu_j^{\mathrm{out}}`$. A hat denotes the additive phase,
$`\nu_j=\exp(2\pi i\widehat\nu_j)`$, with
$`\widehat\nu_j\in\mathbb R/\mathbb Z`$. The same convention applies to
phase obstructions $`\widehat{\mathcal{𝒪}}`$ and corrections
$`\widehat{\mathcal{ℰ}}`$.

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

Finite definitions of higher cups and ordered word operations are in
[Operations](formulas/OPERATIONS.md). The terminal formulas below are complete finite expressions; their
parameter evaluation rules and representative maps are in separate files.

<a id="two-dimensional"></a>

## 2+1D

The physical fields are the binary Majorana cochain $`n_1`$,
the binary complex-fermion cochain $`n_2`$, and the phase $`\nu_3`$.
This is the zero-integer-decoration sector, in the manuscript operator
phase coordinate. Its [paired coordinate map](formulas/MAJORANA_AND_ENDPOINTS.md#eq-m12-2d)
is stated separately.

<a id="obstructions-2d"></a>
### Obstruction functions

#### 1. Majorana obstruction

```math
dn_1=\mathcal{𝒪}_2=0.
```

#### 2. Complex-fermion obstruction

```math
dn_2=\mathcal{𝒪}_3=\mathcal{𝒪}^{\gamma}_3.
```

##### Majorana contribution

```math
\mathcal{𝒪}^{\gamma}_3
 =\mathrm{Sq}^2n_1+\omega_2n_1+s_1\overline{\beta n_1}.
```

#### 3. Bosonic obstruction

```math
d_{s_1}\widehat\nu_3=\widehat{\mathcal{𝒪}}_4
 =\widehat{\mathcal{𝒪}}^{c}_4
  +\widehat{\mathcal{𝒪}}^{c\gamma}_4
  +\widehat{\mathcal{𝒪}}^{\gamma}_4.
```

##### Complex-fermion contribution

```math
\widehat{\mathcal{𝒪}}^{c}_4
 =\frac12\big[\omega_2n_2+n_2\cup n_2
   +dn_2\cup_1n_2\big].
```

##### Complex-fermion–Majorana contribution

```math
\widehat{\mathcal{𝒪}}^{c\gamma}_4
 =\frac12\big[dn_2\cup_2dn_2\big].
```

##### Majorana contribution

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}^\gamma_4(n_1)={}&\frac12\big[
 \mathop{\mathrm{MS}}\nolimits_{123134}(\omega_2,\omega_2,n_1,n_1)\\
&\qquad+(\omega_2n_1)\cup_2(s_1\overline{\beta n_1})\\
&\qquad+(\omega_2\cup_1s_1)\overline{\beta n_1}+s_1(s_1+n_1)\overline{\beta n_1}\big]\\
&+\frac14\big[{\omega_2} \beta n_1+{s_1}\,{n_1}\,\beta n_1\big].
\end{aligned}
```

<a id="stacking-2d"></a>
### Stacking twisters

#### 1. Majorana stacking

```math
N_1=n_1+n'_1.
```

There is no stacking correction in this layer.

#### 2. Complex-fermion stacking

```math
N_2=n_2+n'_2+\mathcal{ℰ}_2,\qquad
\mathcal{ℰ}_2=\mathcal{ℰ}^{\gamma}_2.
```

##### Majorana contribution

```math
\mathcal{ℰ}^{\gamma}_2=(n_1\cup n'_1)+s_1(n_1\cup_1n'_1).
```

#### 3. Bosonic stacking

```math
\begin{aligned}
\widehat\nu_3^{\mathrm{out}}
 &=\widehat\nu_3+\widehat\nu'_3+\widehat{\mathcal{ℰ}}_3,\\
\widehat{\mathcal{ℰ}}_3
 &=\widehat{\mathcal{ℰ}}^{c}_3
  +\widehat{\mathcal{ℰ}}^{c\gamma}_3
  +\widehat{\mathcal{ℰ}}^{\gamma}_3.
\end{aligned}
```

##### Complex-fermion contribution

```math
\widehat{\mathcal{ℰ}}^{c}_3
 =\frac12\big[n_2\cup_1n'_2
 +(n_2+n'_2)\cup_1\mathcal{ℰ}_2\big].
```

##### Complex-fermion–Majorana contribution

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{c\gamma}_3
 =\frac12\big[&dn_2\cup_2n'_2+N_2\cup_2dN_2\\
 &+n_2\cup_2dn_2+n'_2\cup_2dn'_2\big].
\end{aligned}
```

##### Majorana contribution

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^\gamma_3={}&
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

The binary antiunitary term is

```math
\begin{aligned}
\mathcal L_3={}&s_1((s_1\cup_1n_1)+(s_1\cup_1n'_1)+[s_1\cup_1(n_1\cup_1n'_1)])(n_1\cup_1n'_1)\\
&+(s_1\cup_1n_1) (n_1\cup_1n'_1)N_1\\
&+((s_1\cup_1n_1) n_1+n_1 (s_1\cup_1n'_1)+s_1n_1+n_1s_1)(n_1\cup_1n'_1)\\
&+s_1((n_1\cup_1n'_1)n_1+n_1n'_1+n'_1(n_1\cup_1n'_1)).
\end{aligned}
```

**Chiral scope.**

These formulas compute the zero-integer fiber. For split unitary symmetry
($`\omega_2=s_1=0`$), an independent neutral chiral $`\mathbb Z`$ factor can
be adjoined. For the two nonsplit unitary controls in the example catalog,
the finite subgroup and its abstract infinite-cyclic completion are
reported separately; a marked minimal chiral generator is not specified.
The endpoint formulas do not cover general nonsplit nonzero-chiral cochain
inputs.

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

```math
\check n_2=n_2+s_1\widetilde n_1.
```

<a id="obstructions-3d"></a>
<a id="lower-sources"></a>
### Obstruction functions

#### 1. p+ip obstruction

<a id="eq-integer-3d"></a>

```math
d_{s_1}n_1=0.
```

#### 2. Majorana obstruction

<a id="eq-l1"></a>

```math
dn_2=\mathcal{𝒪}_3=\mathcal{𝒪}_3^\psi.
```

**p+ip contribution.**

```math
\mathcal{𝒪}_3^\psi=\omega_2\bar n_1+s_1\bar n_1^2.
```

Equivalently, in the shifted Majorana coordinate,

```math
d\check n_2=\check\omega_2\bar n_1.
```

#### 3. Complex-fermion obstruction

<a id="eq-l2"></a>

```math
dn_3=\mathcal{𝒪}_4=\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}+\mathcal{𝒪}_4^\psi.
```

**Majorana contribution.**

```math
\mathcal{𝒪}_4^\gamma=\check n_2^2+s_1(\check n_2\cup_1\check n_2)+\omega_2\check n_2.
```

**Mixed Majorana–p+ip contribution.**

```math
\mathcal{𝒪}_4^{\gamma\psi}=\check n_2\cup_1d\check n_2+s_1(\check n_2\cup_2d\check n_2).
```

Here $`d\check n_2=\check\omega_2\bar n_1`$ is fixed by the preceding obstruction.

**p+ip contribution.**

<a id="eq-l3"></a>

```math
\begin{aligned}
{\mathcal{𝒪}^\psi_4}={}&\zeta_{2,1}({\check\omega_2},{\bar n_{1}})+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\widetilde n_{1}}\\
&+\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\bar n_{1}},\\
\zeta_{2,1}({\check\omega_2},{\bar n_{1}})(01234)={}&{\check\omega_2}(012){\check\omega_2}(023){\bar n_{1}}(23){\bar n_{1}}(34).
\end{aligned}
```

The second digit obeys $`d\widetilde n_1=\bar n_1^2+s_1\bar n_1`$.

#### 4. Bosonic obstruction

<a id="eq-t3"></a>

```math
d_{s_1}\widehat\nu_4=\widehat{\mathcal{𝒪}}_5.
```

<a id="eq-t3-expanded"></a>

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_5
={}&\mathop{\mathrm{ev}}\nolimits_5\Bigg\{
\frac12\Big[\mathrm{Sq}^2 (\uparrow n_3)+\omega_2 (\uparrow n_3)+T_6[(\uparrow\check n_2);\omega_2,s_1]+(\uparrow\check n_2)(\overline{\beta\omega_2}+s_1\omega_2)\\
 &\qquad +(\mathrm{Sq}^2(\uparrow\check n_2)+s_1\mathrm{Sq}^1(\uparrow\check n_2)+\omega_2(\uparrow\check n_2))
 \cup_4\mathcal{𝒪}_5^\psi[\uparrow n_1]+y_6[(\uparrow n_1);\omega_2,s_1]\\
 &\qquad +\overline{\beta^\circ(\uparrow\check n_2)}\cup_2\overline{B_4^{\psi,\uparrow}}
 +s_1(\overline{\beta^\circ(\uparrow\check n_2)}\cup_3\overline{B_4^{\psi,\uparrow}})\Big]\\
 &+\frac14\big[B_4^\uparrow\cup_2B_4^\uparrow+B_4^\uparrow\cup_3dB_4^\uparrow+\omega_2 B_4^\uparrow\big]\\
 &-\frac14\overline{\big[\mathop{\mathrm{MS}}\nolimits_{12132434}
 (\overline{\beta_{s_1}\check\omega_2},\overline{\beta_{s_1}\check\omega_2},\overline{\uparrow n_1},\overline{\uparrow n_1})
 +\widetilde{\beta_{s_1}\check\omega_2}(\overline{\uparrow n_1}\cup_1\overline{\uparrow n_1})
 +(s_1\overline{\beta_{s_1}\check\omega_2})\widetilde{\uparrow n_1}
 +s_1(\overline{\beta_{s_1}\check\omega_2}\cup_1s_1)\overline{\uparrow n_1}\big]}\Bigg\}\\
 &+\frac1{16}\mathcal P_{s_1}(\check\omega_2)n_1\pmod1.
\end{aligned}
```

Every summand is displayed above. Here $`\mathop{\mathrm{ev}}\nolimits_5`$
means the fixed signed sum over six simplices, and an upward mark selects
a component of the fixed lift of the **whole input tower**. It does not
mean an integer lift or an extra physical decoration. The marked
$`\uparrow n_1,\uparrow\check n_2,\uparrow n_3`$ have degrees two, three,
and four. The physical fields retain their degrees one, two, and three.
The [six-term rule and every lifted component](formulas/THREE_DIMENSIONAL_TERMINAL.md#physical-field-evaluation)
are fully specified; no primitive or gauge is chosen during evaluation.

**Cochains appearing in the formula.**

```math
\begin{aligned}
B_4^{\psi,\uparrow}
 &=\frac{
   \overline{\big[(\overline{\uparrow n_1})^2
                  +\check\omega_2\overline{\uparrow n_1}\big]}
   -(\uparrow n_1)^2-\check\omega_2(\uparrow n_1)}{2},\\
B_4^\uparrow
 &=\beta^\circ(\uparrow\check n_2)+B_4^{\psi,\uparrow}.
\end{aligned}
```

The binary degree-five cochain in the evaluation is

<a id="eq-t3-pip-polynomial"></a>

```math
\begin{aligned}
{\mathcal{𝒪}_5^\psi[\uparrow n_1]}={}&\zeta_{2,2}({\overline{\uparrow n_1}},{\overline{\uparrow n_1}})+\zeta_{2,2}({\check\omega_2},{\overline{\uparrow n_1}})
 +{\overline{\uparrow n_1}}^2\cup_3({\check\omega_2}{\overline{\uparrow n_1}})+\mathrm{Sq}^3{\widetilde{\uparrow n_1}}+{(\overline{\uparrow n_1}\cup_1\overline{\uparrow n_1})}\cup_1({s_1}{\overline{\uparrow n_1}})\\
&+{s_1}\big[{\overline{\uparrow n_1}}^2\cup_4({\check\omega_2}{\overline{\uparrow n_1}})+({\overline{\uparrow n_1}}\cup_1{s_1}){\overline{\uparrow n_1}}+{\overline{\uparrow n_1}}\cup_1{(\overline{\uparrow n_1}\cup_1\overline{\uparrow n_1})}+{\overline{\uparrow n_1}}^2\big]\\
&+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\widetilde{\uparrow n_1}}
 +\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\overline{\uparrow n_1}},\\
\zeta_{2,2}(x,y)={}&\mathop{\mathrm{MS}}\nolimits_{1231343}(x,x,y,y).
\end{aligned}
```

The fixed quadratic background cochain is:

```math
\mathcal P_{s_1}(\check\omega_2)
 =\check\omega_2\check\omega_2
  +\check\omega_2\cup_1d_{s_1}\check\omega_2\quad\text{in }\mathbb Z.
```

This is a fixed integer representative of the twisted Pontryagin-square
expression; keep the displayed representative when it is multiplied by
$`1/16`$. It is not an unspecified modulo-four class.

The half-valued bracket is binary. The quarter-valued cups are signed
integer cups, with the whole barred polynomial reduced before its
integer use. The cochains $`T_6,y_6`$ have their
[complete finite definitions](formulas/SOURCE_OPERATIONS.md) and
[fixed coefficient lists](formulas/COEFFICIENTS.md).

The marked fermion component includes lower-layer corrections. Consequently
its terms cannot be labeled as pure complex-fermion contributions merely
because they contain $`\uparrow n_3`$. This full finite expression retains
all physical contributions; their separate local factorization in the
current phase coordinate is not asserted here.

<a id="stacking-3d"></a>
<a id="lower-stacking"></a>
### Stacking twisters

#### 1. p+ip stacking

<a id="eq-p1"></a>

```math
N_1=n_1+n'_1.
```

#### 2. Majorana stacking

<a id="eq-p2"></a>

```math
N_2=n_2+n'_2+\mathcal{ℰ}_2,\qquad \mathcal{ℰ}_2=\mathcal{ℰ}_2^\psi.
```

**p+ip contribution.**

```math
\mathcal{ℰ}_2^\psi=\bar n_1\bar n'_1+s_1(\bar n_1\cup_1\bar n'_1).
```

The same product in the shifted coordinate is

```math
\check N_2=\check n_2+\check n'_2+\check{\mathcal{ℰ}}_2,\qquad\check{\mathcal{ℰ}}_2=\bar n_1\bar n'_1.
```

Its integer digit carry is

```math
\widetilde N_1=\widetilde n_1+\widetilde n'_1+\bar n_1\cup_1\bar n'_1.
```

#### 3. Complex-fermion stacking

<a id="eq-p3"></a>

```math
\begin{aligned}
N_3&=n_3+n'_3+\mathcal{ℰ}_3,\\
\mathcal{ℰ}_3&=\mathcal{ℰ}_3^\gamma+\mathcal{ℰ}_3^{\gamma\psi}+\mathcal{ℰ}_3^\psi.
\end{aligned}
```

**Majorana contribution.**

```math
\mathcal{ℰ}_3^\gamma=\check n_2\cup_1\check n'_2+s_1(\check n_2\cup_2\check n'_2).
```

**Mixed Majorana–p+ip contribution.**

```math
\mathcal{ℰ}_3^{\gamma\psi}
 =d\check n_2\cup_2\check n'_2
 +(\check n_2+\check n'_2)\cup_1\check{\mathcal{ℰ}}_2
 +s_1\big[(\check n_2+\check n'_2)\cup_2\check{\mathcal{ℰ}}_2\big].
```

**p+ip contribution.**

```math
\begin{aligned}\mathcal{ℰ}_3^\psi={}&{z^\psi_3}({\bar n_{1}},{\bar n'_{1}})+[{\check\omega_2}({\bar n_{1}}+{\bar n'_{1}})]\cup_2{\check{\mathcal{ℰ}}_{2}}+(d{\widetilde n_{1}}){\widetilde n'_{1}}\\
&+({s_1}{\bar n_{1}})\cup_1{\bar n'_{1}}^2+{\bar n_{1}} {s_1} {\bar n'_{1}}+{(\bar n_{1}\cup_{1}\bar n'_{1})} {s_1}({\bar n_{1}}+{\bar n'_{1}})\\
&+{s_1}\big[{s_1}{(\bar n_{1}\cup_{1}\bar n'_{1})}+{\bar n_{1}}\cup_1d{\widetilde n'_{1}}+{(\bar n_{1}\cup_{1}\bar n'_{1})}({\bar n_{1}}+{\bar n'_{1}})\big]+{\Delta[(\bar n_1^2\cup_1s_1)\bar n_1]},\\
{z^\psi_3}({\bar n_{1}},{\bar n'_{1}})={}&\mathop{\mathrm{MS}}\nolimits_{12314}({\bar n_{1}},{\bar n_{1}},{\bar n'_{1}},{\bar n'_{1}})
 =[{\bar n_{1}}\cup_1({\bar n_{1}}{\bar n'_{1}})]{\bar n'_{1}}.
\end{aligned}
```

The $`\Delta`$ acts on the entire displayed bracket with the p+ip output $`N_1`$.

#### 4. Bosonic stacking

<a id="eq-t3-product"></a>

```math
\widehat\nu_4^{\mathrm{out}}=\widehat\nu_4+\widehat\nu'_4+\widehat{\mathcal{ℰ}}_4.
```

<a id="eq-t3-product-expanded"></a>

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_4
={}&\mathop{\mathrm{ev}}\nolimits_4\Bigg\{
\frac12\Big[\mathrm{Sq}^2 (\uparrow n_3)+\omega_2 (\uparrow n_3)+T_6[(\uparrow\check n_2);\omega_2,s_1]+(\uparrow\check n_2)(\overline{\beta\omega_2}+s_1\omega_2)\\
 &\qquad +(\mathrm{Sq}^2(\uparrow\check n_2)+s_1\mathrm{Sq}^1(\uparrow\check n_2)+\omega_2(\uparrow\check n_2))
 \cup_4\mathcal{𝒪}_5^\psi[\uparrow n_1]+y_6[(\uparrow n_1);\omega_2,s_1]\\
 &\qquad +\overline{\beta^\circ(\uparrow\check n_2)}\cup_2\overline{B_4^{\psi,\uparrow}}
 +s_1(\overline{\beta^\circ(\uparrow\check n_2)}\cup_3\overline{B_4^{\psi,\uparrow}})\Big]\\
 &+\frac14\big[B_4^\uparrow\cup_2B_4^\uparrow+B_4^\uparrow\cup_3dB_4^\uparrow+\omega_2 B_4^\uparrow\big]\\
 &-\frac14\overline{\big[\mathop{\mathrm{MS}}\nolimits_{12132434}
 (\overline{\beta_{s_1}\check\omega_2},\overline{\beta_{s_1}\check\omega_2},\overline{\uparrow n_1},\overline{\uparrow n_1})
 +\widetilde{\beta_{s_1}\check\omega_2}(\overline{\uparrow n_1}\cup_1\overline{\uparrow n_1})
 +(s_1\overline{\beta_{s_1}\check\omega_2})\widetilde{\uparrow n_1}
 +s_1(\overline{\beta_{s_1}\check\omega_2}\cup_1s_1)\overline{\uparrow n_1}\big]}\Bigg\}\\
 &-\frac18\check\omega_2n_1n'_1\pmod1.
\end{aligned}
```

Here $`\mathop{\mathrm{ev}}\nolimits_4`$ is the fixed signed sum over fifteen
simplices. The upward marks now select the lifted components of the **two
inputs and their displayed lower stacking law**. The integer residuals
and binary polynomial have the definitions printed after $`\widehat{\mathcal{𝒪}}_5`$,
evaluated on these two-input components. The
[fifteen-term rule](formulas/THREE_DIMENSIONAL_TERMINAL.md#physical-field-evaluation)
fixes every sign and coefficient transport.

The complete correction depends on the complex-fermion, Majorana and
p+ip inputs and their interactions. Its lifted cochain terms are not
individually identified with pure physical layers. In particular this
expression is not replaced by a closed-Majorana twister on an open
Majorana input.

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

```math
\check n_3=n_3+s_1\widetilde n_2.
```

<a id="obstructions-4d"></a>
### Obstruction functions

#### 1. p+ip obstruction

<a id="eq-integer-4d"></a>

```math
d_{s_1}n_2=0.
```

#### 2. Majorana obstruction

<a id="eq-l1-4d"></a>

```math
dn_3=\mathcal{𝒪}_4=\mathcal{𝒪}_4^\psi.
```

**p+ip contribution.**

```math
\mathcal{𝒪}_4^\psi=\mathrm{Sq}^2\bar n_2+\omega_2\bar n_2+s_1\mathrm{Sq}^1\bar n_2.
```

Equivalently, in the shifted Majorana coordinate,

```math
d\check n_3=\check{\mathcal{𝒪}}_4=\bar n_2^2+\check\omega_2\bar n_2.
```

#### 3. Complex-fermion obstruction

<a id="eq-l2-4d"></a>

```math
dn_4=\mathcal{𝒪}_5=\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}+\mathcal{𝒪}_5^\psi.
```

**Majorana contribution.**

```math
\mathcal{𝒪}_5^\gamma=\check n_3\cup_1\check n_3+s_1(\check n_3\cup_2\check n_3)+\omega_2\check n_3.
```

**Mixed Majorana–p+ip contribution.**

```math
\mathcal{𝒪}_5^{\gamma\psi}=\check n_3\cup_2d\check n_3+s_1(\check n_3\cup_3d\check n_3).
```

Here $`d\check n_3`$ is fixed by the preceding obstruction.

**p+ip contribution.**

<a id="eq-l4"></a>

```math
\begin{aligned}
{\mathcal{𝒪}^\psi_5}={}&\zeta_{2,2}({\bar n_{2}},{\bar n_{2}})+\zeta_{2,2}({\check\omega_2},{\bar n_{2}})
 +{\bar n_{2}}^2\cup_3({\check\omega_2}{\bar n_{2}})+\mathrm{Sq}^3{\widetilde n_{2}}+{(\bar n_2\cup_1\bar n_2)}\cup_1({s_1}{\bar n_{2}})\\
&+{s_1}\big[{\bar n_{2}}^2\cup_4({\check\omega_2}{\bar n_{2}})+({\bar n_{2}}\cup_1{s_1}){\bar n_{2}}+{\bar n_{2}}\cup_1{(\bar n_2\cup_1\bar n_2)}+{\bar n_{2}}^2\big]\\
&+({\check\omega_2}\cup_1{\check\omega_2}+{s_1}{\check\omega_2}){\widetilde n_{2}}
 +\big[({\check\omega_2}\cup_1{\check\omega_2})\cup_1{s_1}+{s_1}({s_1}\cup_1{\check\omega_2})\big]{\bar n_{2}},\\
\zeta_{2,2}(x,y)={}&\mathop{\mathrm{MS}}\nolimits_{1231343}(x,x,y,y).
\end{aligned}
```

The second digit obeys $`d\widetilde n_2=\bar n_2\cup_1\bar n_2+s_1\bar n_2`$.

#### 4. Bosonic obstruction

<a id="eq-t4"></a>
<a id="shared-terminal-source"></a>
<a id="four-dimensional-pair"></a>

```math
\begin{aligned}
d_{s_1}\widehat\nu_5=\widehat{\mathcal{𝒪}}_6
={}&\widehat{\mathcal{𝒪}}_6^c
 +\widehat{\mathcal{𝒪}}_6^{c\gamma}
 +\widehat{\mathcal{𝒪}}_6^{c\psi}\\
 &+\widehat{\mathcal{𝒪}}_6^\gamma
 +\widehat{\mathcal{𝒪}}_6^{\gamma\psi}
 +\widehat{\mathcal{𝒪}}_6^\psi.
\end{aligned}
```

In the current phase coordinate the contributions are:

**Complex-fermion contribution.**

```math
\widehat{\mathcal{𝒪}}_6^c=\frac12\big[n_4\cup_2n_4+\omega_2n_4\big].
```

**Mixed complex-fermion–Majorana contribution.**

```math
\widehat{\mathcal{𝒪}}_6^{c\gamma}=\frac12n_4\cup_3(\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}).
```

This includes the displayed interaction induced by the nonclosed
Majorana layer, through $`\mathcal{𝒪}_5^{\gamma\psi}`$.

**Mixed complex-fermion–p+ip contribution.**

```math
\widehat{\mathcal{𝒪}}_6^{c\psi}=\frac12n_4\cup_3\mathcal{𝒪}_5^\psi.
```

**Majorana contribution.**

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_6^\gamma
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
\widehat{\mathcal{𝒪}}_6^{\gamma\psi}
={}&\frac12\Big[
 (\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})
     \cup_4\mathcal{𝒪}_5^\psi
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
\widehat{\mathcal{𝒪}}_6^\psi
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

**Cochains appearing in these contributions.**

<a id="eq-s1"></a>
<a id="eq-s2"></a>
<a id="eq-s3"></a>

```math
\begin{aligned}
\check{\mathcal{𝒪}}_4&=\bar n_2^2+\check\omega_2\bar n_2
 \quad\text{in }\mathbb Z_2,\\
B_4^\psi&=\frac{\check{\mathcal{𝒪}}_4-n_2^2-\check\omega_2n_2}{2},\\
B_4&=\beta^\circ\check n_3+B_4^\psi
 =\frac{d\check n_3-n_2^2-\check\omega_2n_2}{2},\\
dB_4&=-(\beta_{s_1}\check\omega_2)n_2.
\end{aligned}
```

The fixed quadratic background cochain is:

```math
\mathcal P_{s_1}(\check\omega_2)
 =\check\omega_2\check\omega_2
  +\check\omega_2\cup_1d_{s_1}\check\omega_2\quad\text{in }\mathbb Z.
```

This is a fixed integer representative of the twisted Pontryagin-square
expression; keep the displayed representative when it is multiplied by
$`1/16`$. It is not an unspecified modulo-four class.

The half-valued brackets are binary. Quarter-valued brackets are integer;
the whole barred polynomial is reduced before its integer use. The fixed
cochains $`T_6,y_6`$ have [explicit finite definitions](formulas/SOURCE_OPERATIONS.md),
with every coefficient listed in [Coefficients](formulas/COEFFICIENTS.md).

<a id="stacking-4d"></a>
### Stacking twisters

#### 1. p+ip stacking

<a id="eq-p1-4d"></a>

```math
N_2=n_2+n'_2.
```

#### 2. Majorana stacking

<a id="eq-p2-4d"></a>

```math
N_3=n_3+n'_3+\mathcal{ℰ}_3,\qquad\mathcal{ℰ}_3=\mathcal{ℰ}_3^\psi.
```

**p+ip contribution.**

```math
\mathcal{ℰ}_3^\psi=\bar n_2\cup_1\bar n'_2+s_1(\bar n_2\cup_2\bar n'_2).
```

The same product in the shifted coordinate is

```math
\check N_3=\check n_3+\check n'_3+\check{\mathcal{ℰ}}_3,\qquad\check{\mathcal{ℰ}}_3=\bar n_2\cup_1\bar n'_2.
```

Its integer digit carry is

```math
\widetilde N_2=\widetilde n_2+\widetilde n'_2+\bar n_2\cup_2\bar n'_2.
```

Consequently $`d\check{\mathcal{ℰ}}_3=\bar n_2\bar n'_2+\bar n'_2\bar n_2`$.

#### 3. Complex-fermion stacking

<a id="eq-p4"></a>

```math
\begin{aligned}
N_4&=n_4+n'_4+\mathcal{ℰ}_4,\\
\mathcal{ℰ}_4&=\mathcal{ℰ}_4^\gamma+\mathcal{ℰ}_4^{\gamma\psi}+\mathcal{ℰ}_4^\psi.
\end{aligned}
```

**Majorana contribution.**

```math
\mathcal{ℰ}_4^\gamma=\check n_3\cup_2\check n'_3+s_1(\check n_3\cup_3\check n'_3).
```

**Mixed Majorana–p+ip contribution.**

```math
\begin{aligned}
\mathcal{ℰ}_4^{\gamma\psi}={}&d\check n_3\cup_3\check n'_3
 +(\check n_3+\check n'_3)\cup_2\check{\mathcal{ℰ}}_3\\
 &+s_1\big[d\check n_3\cup_4\check n'_3
 +(\check n_3+\check n'_3)\cup_3\check{\mathcal{ℰ}}_3\big].
\end{aligned}
```

**p+ip contribution.**

```math
\begin{aligned}\mathcal{ℰ}_4^\psi={}&{z^\psi_4}({\bar n_{2}},{\bar n'_{2}})+[{\check\omega_2}({\bar n_{2}}+{\bar n'_{2}})]\cup_3{\check{\mathcal{ℰ}}_{3}}
 +{\bar n'_{2}}^2\cup_4({\check\omega_2}{\bar n_{2}})+d{\check{\mathcal{ℰ}}_{3}}\cup_4[{\check\omega_2}({\bar n_{2}}+{\bar n'_{2}})]\\
&+{\widetilde n_{2}}({\widetilde n'_{2}}+{\bar n'_{2}})+{\bar n_{2}}{\widetilde n'_{2}}+d{\widetilde n_{2}}\cup_1{\widetilde n'_{2}}+({\widetilde n_{2}}+{\widetilde n'_{2}}){(\bar n_{2}\cup_{2}\bar n'_{2})}\\
&+({s_1}{\bar n_{2}})\cup_2({\bar n'_{2}}\cup_1{\bar n'_{2}})+{\bar n_{2}}\cup_1({s_1}{\bar n'_{2}})+{(\bar n_{2}\cup_{2}\bar n'_{2})}\cup_1[{s_1}({\bar n_{2}}+{\bar n'_{2}})]\\
&+{s_1}\big[{s_1}{(\bar n_{2}\cup_{2}\bar n'_{2})}+{\bar n_{2}}\cup_2d{\widetilde n'_{2}}+{(\bar n_{2}\cup_{2}\bar n'_{2})}\cup_1({\bar n_{2}}+{\bar n'_{2}})+\ell_3({\bar n_{2}},{\bar n'_{2}})\big].
\end{aligned}
```

The two finite polynomials in this contribution are

<a id="eq-p5"></a>

```math
\begin{aligned}
{z^\psi_4}({\bar n_{2}},{\bar n'_{2}})={}&\mathop{\mathrm{MS}}\nolimits_{12413423}({\bar n_{2}},{\bar n_{2}},{\bar n_{2}},{\bar n'_{2}})\\
&+(\mathop{\mathrm{MS}}\nolimits_{12314132}+\mathop{\mathrm{MS}}\nolimits_{12314324}
 +\mathop{\mathrm{MS}}\nolimits_{12341321})({\bar n_{2}},{\bar n_{2}},{\bar n'_{2}},{\bar n'_{2}})\\
&+(\mathop{\mathrm{MS}}\nolimits_{12132413}+\mathop{\mathrm{MS}}\nolimits_{12324214})({\bar n_{2}},{\bar n'_{2}},{\bar n'_{2}},{\bar n'_{2}}),\\
\ell_3({\bar n_{2}},{\bar n'_{2}})(0123)={}&{\bar n_{2}}(023){\bar n'_{2}}(012)[1+{\bar n_{2}}(013){\bar n'_{2}}(123)].
\end{aligned}
```

#### 4. Bosonic stacking

```math
\widehat\nu_5^{\mathrm{out}}=\widehat\nu_5+\widehat\nu'_5+\widehat{\mathcal{ℰ}}_5.
```

<a id="eq-t4d"></a>
<a id="eq-t4c"></a>

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5
={}&\widehat{\mathcal{ℰ}}_5^c+\widehat{\mathcal{ℰ}}_5^{c\gamma}+\widehat{\mathcal{ℰ}}_5^{c\psi}\\
 &+\frac12\Big[
 (\mathcal{ℰ}_4+\bar n_2\bar n'_2)
       \cup_3(\bar n_2\bar n'_2)
 +\mathcal{𝒪}_5[N_2,\check N_3]
       \cup_4(\bar n_2\bar n'_2)\\
 &\qquad+\zeta_{2,2}(\bar n_2,\bar n'_2)
 +\bar n_2\cup_1d\check n'_3
 +\widetilde n_2(\bar n'_2\cup_1\bar n'_2)\\
 &\qquad+(\check\omega_2\cup_1\bar n_2)\bar n'_2
 +s_1\bar n_2\widetilde n'_2
 +s_1(\bar n_2\cup_1s_1)\bar n'_2\\
 &\qquad+\check{\mathcal{ℰ}}_3(\bar n_2+\bar n'_2)
 +\check\omega_2\check{\mathcal{ℰ}}_3+Z_5\Big]\\
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

The explicit complex-fermion terms are, in order:

**Complex-fermion contribution.**

```math
\widehat{\mathcal{ℰ}}_5^c=\frac12n_4\cup_3n'_4.
```

**Mixed complex-fermion–Majorana contribution.**

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5^{c\gamma}=\frac12\Big[&
 (\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})\cup_4n'_4\\
 &+(n_4+n'_4)\cup_3(\mathcal{ℰ}_4^\gamma+\mathcal{ℰ}_4^{\gamma\psi})\Big].
\end{aligned}
```

**Mixed complex-fermion–p+ip contribution.**

```math
\widehat{\mathcal{ℰ}}_5^{c\psi}=\frac12\Big[
 \mathcal{𝒪}_5^\psi\cup_4n'_4+(n_4+n'_4)\cup_3\mathcal{ℰ}_4^\psi\Big].
```

**Majorana, mixed Majorana–p+ip, and p+ip terms.**

These are the remaining terms explicitly printed in the full equation
above. The finite term $`Z_5`$ contains both lower layers and their
interaction; it is not assigned to a pure-p+ip contribution. In this
representative their allocation inside the finite transfer remains
combined. The equation is complete, and its [finite evaluation](formulas/TERMINAL_TRANSFER.md)
fixes every term.

The repeated binary polynomial is

<a id="eq-t4b"></a>

```math
\begin{aligned}
\mathcal V_5={}&{\bar B_4}\cup_3{\bar B'_4}+d{\bar B_4}\cup_4{\bar B'_4}+({\bar B_4}+{\bar B'_4})\cup_3{\overline{\Delta B_4}}
 +(d{\bar B_4}+d{\bar B'_4})\cup_4{\overline{\Delta B_4}}\\
&+{\mathrm{Sq}}^2{\bar\lambda_3}+({\bar n'_{2}}{\bar n_{2}})\cup_3d{\bar\lambda_3}+{\omega_2}{\bar\lambda_3}+({\widetilde{\beta_{s_1}\check\omega_2}}+{\overline{\beta_{s_1}\check\omega_2}}){(\bar n_{2}\cup_{2}\bar n'_{2})}\\
&+\zeta_{2,2}({\bar n'_{2}},{\bar n_{2}})+{\check n'_{3}}{\bar n_{2}}+{\bar n'_{2}}{\check n_{3}}+({\check\omega_2}\cup_1{\bar n'_{2}}){\bar n_{2}}
 +{\widetilde n'_{2}}({\bar n_{2}}\cup_1{\bar n_{2}})+{s_1}{\bar n'_{2}}{\widetilde n_{2}}+{s_1}({\bar n'_{2}}\cup_1{s_1}){\bar n_{2}}.
\end{aligned}
```

Evaluate $`\mathcal V_5`$ modulo two before its integer use. Its integer
carry is

<a id="eq-t4a"></a>

```math
\begin{aligned}
\lambda_3&=\frac{\check N_3-\check n_3-\check n'_3+n_2\cup_1n'_2}{2},\\
\Delta B_4&=d\lambda_3-n'_2n_2,\\
\overline{\Delta B_4}&=d\bar\lambda_3+\bar n'_2\bar n_2.
\end{aligned}
```

The three named Majorana fields in the numerator use their canonical
integer values. The unprimed obstruction in the mixed terms is evaluated
on the first input; $`\mathcal{𝒪}_5[N_2,\check N_3]=dN_4`$ uses the stacked
output. The $`1/4,1/8,1/3`$ products in the full correction are ordered
integer products before reduction modulo one.

## Finite definitions and coordinate maps

- [3+1D terminal evaluation](formulas/THREE_DIMENSIONAL_TERMINAL.md)
- [Finite cochain formulas for the bosonic obstruction](formulas/SOURCE_OPERATIONS.md)
- [4+1D terminal twister](formulas/TERMINAL_TRANSFER.md)
- [Closed-Majorana formulas](formulas/MAJORANA_AND_ENDPOINTS.md)
- [Higher cups and finite sums](formulas/OPERATIONS.md), [fixed coefficients](formulas/COEFFICIENTS.md)
- [Changes of representative](formulas/REPRESENTATIVES.md)
- [Formula-to-code translation](../formulas/CODE_NOTATION.md)

A nonzero obstruction cochain may be a coboundary. Only its nontrivial
class after the permitted lower-layer changes obstructs the decoration.
