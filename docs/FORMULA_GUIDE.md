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
absent contributions are omitted. A mixed superscript identifies an interaction between the indicated physical layers. The pieces are parts of the full
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
[Operations](formulas/OPERATIONS.md). The terminal formulas below use physical cochains. Long numerical coefficient lists and proofs of the paired representative changes are kept in separate appendices.

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
\frac12\Big[[n_1\cup_1(n_1n'_1)]n'_1
 +(\omega_2N_1)\cup_2(n_1n'_1)+\mathcal L_3\\
&\qquad+(\omega_2\cup_1s_1)(n_1\cup_1n'_1)\\
&\qquad+(\omega_2N_1)\cup_2(s_1(n_1\cup_1n'_1))\\
&\qquad+(\omega_2n'_1)\cup_3(s_1n_1^2)\Big]\\
&+\frac14\Big[\beta n_1\cup_1\beta n'_1\\
&\qquad-(\beta n_1+\beta n'_1)({n_1}\cup_1{n'_1})\\
&\qquad-({n_1}\cup_1{n'_1})(\beta n_1+\beta n'_1)\\
&\qquad+({n_1}\cup_1{n'_1})d({n_1}\cup_1{n'_1})
 -\omega_2(n_1\cup_1n'_1)+\overline{s_1n_1n'_1}\Big]\\
&+\frac18\Big[-\overline{N_1^3}+\overline{n_1^3}+\overline{(n'_1)^3}\Big]
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
d_{s_1}\widehat\nu_4=\widehat{\mathcal{𝒪}}_5
 =\widehat{\mathcal{𝒪}}_5^c
  +\widehat{\mathcal{𝒪}}_5^{c\gamma}
  +\widehat{\mathcal{𝒪}}_5^{c\psi}
  +\widehat{\mathcal{𝒪}}_5^\gamma
  +\widehat{\mathcal{𝒪}}_5^{\gamma\psi}
  +\widehat{\mathcal{𝒪}}_5^\psi.
```

##### Complex fermions

```math
\widehat{\mathcal{𝒪}}_5^c
 =\frac12[\omega_2n_3+n_3\cup_1n_3+dn_3\cup_2n_3].
```

##### Complex fermions and Majorana decoration

```math
\widehat{\mathcal{𝒪}}_5^{c\gamma}
 =\frac12(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})\cup_3(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}).
```

##### Complex fermions and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_5^{c\psi}
 =\frac12\Big[&\mathcal{𝒪}_4^\psi\cup_3\mathcal{𝒪}_4^\psi
  +(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})\cup_3\mathcal{𝒪}_4^\psi
  +\mathcal{𝒪}_4^\psi\cup_3(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})\\
 &+\sum_{(v;\mathbf x)\in\mathcal I_5^{c\psi}}
       \mathop{\mathrm{MS}}\nolimits_v(\mathbf x)\Big].
\end{aligned}
```

Every term of the last sum contains
$`d\check n_2=\check\omega_2\bar n_1`$. Its 25 coefficients are
[listed explicitly](formulas/THREE_DIMENSIONAL_WORD_INDICES.md#complex-fermion-indices).

##### Majorana decoration

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_5^\gamma
={}&\frac12\Big[
 \zeta_{2,2}(\omega_2,\check n_2)\\
&\qquad+(\mathop{\mathrm{MS}}\nolimits_{1213243}
 +\mathop{\mathrm{MS}}\nolimits_{1213431}
 +\mathop{\mathrm{MS}}\nolimits_{1232141}
 +\mathop{\mathrm{MS}}\nolimits_{1234321})
       (\check n_2,\check n_2,\check n_2,\check n_2)
 +(\check n_2^2)\cup_3(\omega_2\check n_2)\\
&\qquad+(\check n_2^2)\cup_3(s_1\overline{\beta^\circ\check n_2})
 +(\omega_2\check n_2)\cup_3(s_1\overline{\beta^\circ\check n_2})\\
&\qquad+\zeta_{1,3}(s_1,\overline{\beta^\circ\check n_2})
 +(\omega_2\cup_1s_1)\overline{\beta^\circ\check n_2}
 +s_1\check n_2^2\Big]\\
&+\frac14\Big[
 \omega_2\beta^\circ\check n_2
 +(\beta^\circ\check n_2)\cup_1(\beta^\circ\check n_2)
 +s_1^2(\beta^\circ\check n_2+
             \overline{\beta^\circ\check n_2})\Big].
\end{aligned}
```

Here $`\beta^\circ x=(dx-\overline{dx})/2`$, with the first differential
formed in integers. It agrees with the ordinary Bockstein on a cocycle.
The word operations are

```math
\begin{aligned}
\zeta_{2,2}(x,y)&=\mathop{\mathrm{MS}}\nolimits_{1231343}(x,x,y,y),\\
\zeta_{1,3}(x,y)&=\mathop{\mathrm{MS}}\nolimits_{1231434}(x,x,y,y).
\end{aligned}
```

##### Majorana and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_5^{\gamma\psi}
={}&\frac12\sum_{(v;\mathbf x)\in\mathcal I_5^{\gamma\psi}}
       \mathop{\mathrm{MS}}\nolimits_v(\mathbf x)\\
&+\frac14\Big[
 (\beta^\circ\check n_2)\cup_1B_3^\psi
 +B_3^\psi\cup_1(\beta^\circ\check n_2)
 -[(\beta_{s_1}\check\omega_2)n_1]\cup_2(\beta^\circ\check n_2)\\
&\qquad-(\check\omega_2\bar n_1)\check n_2
        -\check n_2(\check\omega_2\bar n_1)\Big].
\end{aligned}
```

The integer carry and the twisted Bockstein are

```math
B_3^\psi
 =\frac{\overline{\check\omega_2\bar n_1}
                  +\check\omega_2 n_1}{2},
\qquad
\beta_{s_1}\check\omega_2=\frac{d_{s_1}\check\omega_2}{2}.
```

Both divisions are exact. The product $`\check\omega_2n_1`$ has the
local-coefficient transport of its two signed integer factors.
The finite index set $`\mathcal I_5^{\gamma\psi}`$ is defined in the
[coefficient appendix](formulas/THREE_DIMENSIONAL_WORD_INDICES.md#final-physical-index-sets).

##### p+ip decoration

<a id="three-dimensional-pip-source"></a>

On the ordered five-simplex $`(012345)`$, the complete contribution is

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_5^\psi(012345)
={}&\frac12\Bigg[
 \sum_{(v;\mathbf x)\in\mathcal I_5^\psi}
       \mathop{\mathrm{MS}}\nolimits_v(\mathbf x)
 +\sum_{(f,g)\in\mathcal C_5^\psi}f\,g
 \Bigg]\\
&+\frac14\left\{\begin{aligned}
&B_3^\psi\cup_1B_3^\psi
 -[(\beta_{s_1}\check\omega_2)n_1]\cup_2B_3^\psi
 -\omega_2B_3^\psi\\
&+(-1)^{s_1(34)}(\beta_{s_1}\check\omega_2)(0123)
  [(\beta_{s_1}\check\omega_2)(0124)
   +(\beta_{s_1}\check\omega_2)(0234)]n_1(34)n_1(45)\\
&-\overline{[\mathrm{Sq}^1\overline{\beta_{s_1}\check\omega_2}]\bar n_1
 +s_1\overline{\beta_{s_1}\check\omega_2}\widetilde n_1
 +s_1(s_1\cup_1\overline{\beta_{s_1}\check\omega_2})\bar n_1}
 +\overline{\widetilde{\beta_{s_1}\check\omega_2}\bar n_1^2}
\end{aligned}\right\}
 +\frac1{16}[\mathcal P_{s_1}(\check\omega_2)\cup n_1](012345).
\end{aligned}
```

Every cochain expression without explicit arguments is evaluated on
$`(012345)`$. The [word indices](formulas/THREE_DIMENSIONAL_WORD_INDICES.md#final-physical-index-sets)
fix $`\mathcal I_5^\psi`$, and the
[physical-face coefficient table](formulas/THREE_DIMENSIONAL_INTEGER_SOURCE_FACES.md#physical-integer-source-coefficients)
prints every pair in $`\mathcal C_5^\psi`$. Its factors involve only the
physical values of $`n_1`$, $`s_1`$, and $`\omega_2`$ on faces of this same
five-simplex. The table is finite and complete; no auxiliary simplex or
lifted-field evaluation is part of this formula.

The Pontryagin-square convention in the last term is

```math
\mathcal P_{s_1}(\check\omega_2)
=\check\omega_2^2
 +\check\omega_2\cup_1d_{s_1}\check\omega_2.
```

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

<a id="eq-t3b"></a>


```math
\begin{aligned}
\widehat\nu_4^{\mathrm{out}}
 &=\widehat\nu_4+\widehat\nu'_4+\widehat{\mathcal{ℰ}}_4,\\
\widehat{\mathcal{ℰ}}_4
 &=\widehat{\mathcal{ℰ}}^{c}_4
  +\widehat{\mathcal{ℰ}}^{c\gamma}_4
  +\widehat{\mathcal{ℰ}}^{c\psi}_4
  +\widehat{\mathcal{ℰ}}^{\gamma}_4
  +\widehat{\mathcal{ℰ}}^{\gamma\psi}_4
  +\widehat{\mathcal{ℰ}}^{\psi}_4.
\end{aligned}
```

##### Complex fermions

```math
\widehat{\mathcal{ℰ}}^{c}_4
 =\frac12\big[n_3\cup_2n'_3
 +(n_3+n'_3)\cup_2\mathcal{ℰ}_3\big].
```

##### Complex fermions and Majorana decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{c\gamma}_4=\frac12\big[&
 (\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check n_2]\cup_3n'_3
 +N_3\cup_3(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check N_2]\\
 &+n_3\cup_3(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check n_2]
 +n'_3\cup_3(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check n'_2]\big].
\end{aligned}
```

The output is the actual stacked Majorana field, including its p+ip carry.

##### Complex fermions and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{c\psi}_4=\frac12\big[&
 \mathcal{𝒪}_4^\psi[n_1]\cup_3n'_3
 +N_3\cup_3\mathcal{𝒪}_4^\psi[N_1]\\
 &+n_3\cup_3\mathcal{𝒪}_4^\psi[n_1]
 +n'_3\cup_3\mathcal{𝒪}_4^\psi[n'_1]\\
 &+\sum_{(v;\boldsymbol x)\in\mathcal I_{4,A}}
       \mathop{\mathrm{MS}}\nolimits_v(\boldsymbol x)\\
 &+P_4[\check N_2,n_3+n'_3]
  +P_4[\check n_2+\check n'_2,n_3+n'_3]\big].
\end{aligned}
```

The [186 open-Majorana words](formulas/THREE_DIMENSIONAL_PRODUCT_CF_WORDS.md) contain
$`d\check n_2=\check\omega_2\bar n_1`$ or its primed counterpart.
The two displayed $`P_4`$ terms differ by inserting the actual p+ip Majorana
stacking carry $`\bar n_1\bar n'_1`$; their eight-row definition is below. These terms retain the physical complex-fermion operator ordering. The accompanying 58 words with
$`dn_3`$ or $`dn'_3`$ are retained in the lower-sector index set.

##### Majorana decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{\gamma}_4={}&\frac12z_4^\gamma
 +\frac14\big[
 -\beta^\circ\check n_2\cup_2\beta^\circ\check n'_2\\
 &+(\beta^\circ\check n_2+\beta^\circ\check n'_2)
       \cup_1\lambda_2^\gamma
 -\lambda_2^\gamma\cup_1
       \beta^\circ\overline{\check n_2+\check n'_2}\\
 &+(\lambda_2^\gamma)^2-\omega_2\lambda_2^\gamma\big].
\end{aligned}
```

The binary completion is

```math
\begin{aligned}
z_4^\gamma={}&z^0_4(\check n_2,\check n'_2)
 +(\omega_2\overline{\check n_2+\check n'_2})\cup_3\mathcal{ℰ}_3^\gamma
 +d(\check n_2\cup_1\check n'_2)\cup_4
       (\omega_2\overline{\check n_2+\check n'_2})\\
&+(\check n'_2)^2\cup_4(\omega_2\check n_2)
 +[(\check n'_2)^2+\omega_2\check n'_2]\cup_4
                     (s_1\overline{\beta^\circ\check n_2})\\
&+(\omega_2\cup_1s_1)\lambda_2^\gamma
 +(\check n_2\cup_1\check n'_2)\cup_3
       [s_1(\overline{\beta^\circ\check n_2}
                       +\overline{\beta^\circ\check n'_2})]\\
&+\overline{\check n_2+\check n'_2}^{\,2}\cup_3(s_1\lambda_2^\gamma)
 +(\check n_2\cup_1\check n'_2)\cup_2(s_1\lambda_2^\gamma)\\
&+s_1\Big[\mathcal{ℰ}_3^\gamma
 +\overline{\beta^\circ\check n_2}\cup_3
                     \overline{\beta^\circ\check n'_2}
 +\lambda_2^\gamma\cup_1\lambda_2^\gamma\\
&\qquad+(\overline{\beta^\circ\check n_2}
                      +\overline{\beta^\circ\check n'_2})
                    \cup_3(s_1\lambda_2^\gamma)
 +(s_1\lambda_2^\gamma)\cup_2\lambda_2^\gamma\\
&\qquad+\overline{
 \beta^{\circ+}\overline{\check n_2+\check n'_2}
 -\beta^{\circ+}\check n_2-\beta^{\circ+}\check n'_2}\Big].
\end{aligned}
```

Here $`\mathcal{ℰ}_3^\gamma=\check n_2\cup_1\check n'_2
+s_1(\check n_2\cup_2\check n'_2)`$ and
$`\beta^{\circ+}x=(\beta^\circ x+\overline{\beta^\circ x})/2`$.
Its intrinsic binary polynomial is

```math
\begin{aligned}
z^0_4(x,y)={}&\sum_{v\in\mathcal V_4}\mathop{\mathrm{MS}}\nolimits_v(x,x,y,y)
 +\mathop{\mathrm{MS}}\nolimits_{12123}(x+y,y,x\cup_2y)
 +\mathop{\mathrm{MS}}\nolimits_{123131}(y,x,x\cup_1y)\\
&+(x\cup_1y)\cup_1y
 +(\overline{\beta^\circ x}+\overline{\beta^\circ y})\cup_1(x\cup_2y)\\
&+(x\cup_2y)\cup_1
  (\overline{\beta^\circ x}+\overline{\beta^\circ y}+y\cup_1x)\\
&+(x\cup_1y)\cup_3(x^2+y^2)
 +y\cup_2[x\cup_1(x\cup_1y)]
 +\overline{\beta^\circ y}\cup_2\overline{\beta^\circ x},\\
\mathcal V_4={}&\{12123434,12134131,12314324,12314342,
                13242412,13413142,13432412\}.
\end{aligned}
```

##### Majorana and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{\gamma\psi}_4={}&
 \frac12\left[z_4^\gamma+
   \sum_{(v;\boldsymbol x)\in\mathcal I_{4,\neg\psi}}
          \mathop{\mathrm{MS}}\nolimits_v(\boldsymbol x)\right]\\
&+\frac14\Big[
 -\beta^\circ\check n_2\cup_2 B_3^{\psi\prime}
 -B_3^\psi\cup_2\beta^\circ\check n'_2
 +\beta^\circ\check n_2\cup_3
       [ (\beta_{s_1}\check\omega_2)n'_1]\\
&\quad+(\beta^\circ\check n_2+\beta^\circ\check n'_2)
       \cup_2d\lambda_2
 +(B_3^\psi+B_3^{\psi\prime})
       \cup_2d(\lambda_2^\gamma+\lambda_2^{\gamma\psi})\\
&\quad+\sum_{\substack{i,j\in\{\gamma,\gamma\psi,\psi\}\\
                         (i,j)\ne(\psi,\psi)}}
       [\lambda_2^i\cup_1d\lambda_2^j-\lambda_2^i\lambda_2^j]
 +\omega_2(\lambda_2^\gamma+\lambda_2^{\gamma\psi})\\
&\quad-\big[\check N_2^2-\check n_2^2-(\check n'_2)^2
                      -(\bar n_1\bar n'_1)^2\big]\\
&\quad+d_{s_1}\Big[
 2\lambda_2^\gamma\cup_1\lambda_2^\gamma
 +(\beta^\circ\check n_2+\beta^\circ\check n'_2)
                     \cup_2\lambda_2^\gamma
 +(d\lambda_2^\gamma)\cup_3d\lambda_2^\gamma
 -\overline{\check n_2\cup_1\check n'_2}\Big]\\
&\quad-(\beta^\circ\check n_2+\beta^\circ\check n'_2)
                  \cup_1\lambda_2^\gamma
 +\lambda_2^\gamma\cup_1
        \beta^\circ\overline{\check n_2+\check n'_2}
 -(\lambda_2^\gamma)^2+\omega_2\lambda_2^\gamma
 \Big].
\end{aligned}
```

This explicitly continued relative phase is zero on the closed-Majorana
physical tower by the proved paired coordinate map. Its half and quarter
brackets need not separately vanish. The integer derivatives and whole
binary lifts displayed here are part of that exact statement. The formula
can be simplified further only while retaining both coefficients and its
paired source map; canceling the binary parity of a quarter term is not
sufficient.

##### p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{\psi}_4={}&
 \frac12\left[
 \sum_{(v;\boldsymbol x)\in\mathcal I_{4,\psi}}
         \mathop{\mathrm{MS}}\nolimits_v(\boldsymbol x)+\sum_{(f,g)\in\mathcal C_4^\psi}f\,g\right]\\
&+\frac14\Big[
 -B_3^\psi\cup_2B_3^{\psi\prime}
 +B_3^\psi\cup_3[(\beta_{s_1}\check\omega_2)n'_1]
 +(B_3^\psi+B_3^{\psi\prime})\cup_2d\lambda_2^\psi\\
&\quad+\lambda_2^\psi\cup_1d\lambda_2^\psi
       -(\lambda_2^\psi)^2+\omega_2\lambda_2^\psi
       -(\bar n_1\bar n'_1)^2
 -\overline{\widetilde{\beta_{s_1}\check\omega_2}
                   (\bar n_1\cup_1\bar n'_1)}\Big]\\
&-\frac18\check\omega_2 n_1n'_1.
\end{aligned}
```

###### Physical-face coefficients

On an ordered four-simplex the remaining half-valued term is the following
finite polynomial in the physical integer digits and background faces:

```math
\frac12\sum_{(f,g)\in\mathcal C_4^\psi}f\,g.
```

Every pair $`(f,g)`$ is printed in the
[physical-face coefficient table](formulas/THREE_DIMENSIONAL_INTEGER_PRODUCT_FACES.md).
Its 173 rows contain all 306 integer-digit monomials, grouped only when
their background coefficients are identical. Each table entry contains
only $`\bar n_1`$, $`\widetilde n_1`$, their primed counterparts, the
explicit third digit $`\overline{\lfloor n_1/4\rfloor}`$, and the
physical faces of $`s_1`$, $`\omega_2`$, and $`\check\omega_2`$.

##### Physical fields, carries, and arithmetic

The lower product and source in these displays are the already fixed laws

```math
\begin{aligned}
N_1&=n_1+n'_1,\qquad
\check N_2=\check n_2+\check n'_2+\bar n_1\bar n'_1,\\
N_3&=n_3+n'_3+\mathcal{ℰ}_3,\qquad
 dn_3=(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check n_2]+\mathcal{𝒪}_4^\psi[n_1],\\
\mathcal{𝒪}_4^\gamma[x]&=x^2+s_1(x\cup_1x)+\omega_2x,\\
\mathcal{𝒪}_4^{\gamma\psi}[x]&=x\cup_1dx+s_1(x\cup_2dx).
\end{aligned}
```

All cochain Steenrod squares include their differential terms. The integer carries appearing in the formulas are:

```math
\begin{aligned}
\beta^\circ x&=(dx-\overline{dx})/2,\\
B_3&=\beta^\circ\check n_2+B_3^\psi
 =\frac{d\check n_2+\check\omega_2n_1}{2},\\
B_3^\psi&=(\overline{\check\omega_2\bar n_1}
                         +\check\omega_2n_1)/2,\\
\lambda_2^\gamma&=\check n_2\cup_2\check n'_2,\\
\lambda_2^{\gamma\psi}
 &=\overline{\check n_2+\check n'_2}
                  \cup_2(\bar n_1\bar n'_1),\\
\lambda_2^\psi&=(n_1n'_1-\overline{\bar n_1\bar n'_1})/2,\\
\lambda_2&=\lambda_2^\gamma+\lambda_2^{\gamma\psi}
            +\lambda_2^\psi
 =\frac{\check n_2+\check n'_2+n_1n'_1-\check N_2}{2}.
\end{aligned}
```

Every binary field in an integer expression means its canonical zero-or-one
lift. Bars on full sums retain their complete reduction boundary. The
integer products in $`\check\omega_2n_1`$ and $`n_1n'_1`$ use the inherited
local systems; the latter is closed and untwisted. In particular the full
residual satisfies $`dB_3=(\beta_{s_1}\check\omega_2)n_1`$, whereas differentiating
$`B_3^\psi`$ alone need not give that expression. The origin selection uses the
full legal derivative before selecting its p+ip descendant.

##### The finite phase polynomials

For a binary degree-two argument $`x`$ and degree-three argument $`z`$,
the phase numerator $`P_4[x,z]`$ is the sum of these eight ordinary words:

| Word | Inputs |
|---|---|
| 121231 | $`(z,\omega_2,x)`$ |
| 121323 | $`(\omega_2,z,x)`$ |
| 12134243 | $`(s_1,z,x,x)`$ |
| 12134323 | $`(s_1,z,x,x)`$ |
| 123131 | $`(z,\omega_2,x)`$ |
| 12313431 | $`(z,s_1,x,x)`$ |
| 12341431 | $`(z,s_1,x,x)`$ |
| 12342432 | $`(s_1,z,x,x)`$ |

The [lower word indices](formulas/THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md) also use the nine-term phase numerator

```math
\begin{aligned}
H_4[x]={}&x\cup_1\mathrm{Sq}^1\omega_2
 +\mathop{\mathrm{MS}}\nolimits_{1321}(x,\omega_2,s_1)
 +\mathop{\mathrm{MS}}\nolimits_{12131}(x,x,x)\\
&+\mathop{\mathrm{MS}}\nolimits_{132123}(x,x,\mathrm{Sq}^1x)
 +\mathop{\mathrm{MS}}\nolimits_{2321232}(x,\mathrm{Sq}^1x,\mathrm{Sq}^1x)\\
&+(\mathop{\mathrm{MS}}\nolimits_{34123121}+\mathop{\mathrm{MS}}\nolimits_{34123212})
      (x,\mathrm{Sq}^1x,\omega_2,s_1)\\
&+\mathop{\mathrm{MS}}\nolimits_{41231231}(x,x,\mathrm{Sq}^1x,s_1)
 +\mathop{\mathrm{MS}}\nolimits_{12131243}(x,x,x,x).
\end{aligned}
```

The derivative of its integer quarter partner, the literal square of $`x`$,
is already displayed in the mixed and pure quarter formulas. It has not
been absorbed into a binary word table.

The obstruction and stacking law use the same [paired phase convention](formulas/THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md), including the explicit output gauge.

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
\widehat{\mathcal{𝒪}}_6^c
=\frac12\big[
 \omega_2n_4+n_4\cup_2n_4+dn_4\cup_3n_4\big].
```

**Complex-fermion–Majorana contribution.**

```math
\widehat{\mathcal{𝒪}}_6^{c\gamma}
=\frac12(\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})
        \cup_4(\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}).
```

**Complex-fermion–p+ip contribution.**

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_6^{c\psi}
=\frac12\Big[&
 (\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})
                                      \cup_4\mathcal{𝒪}_5^\psi\\
 &+\mathcal{𝒪}_5^\psi\cup_4
           (\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})
 +\mathcal{𝒪}_5^\psi\cup_4\mathcal{𝒪}_5^\psi\Big].
\end{aligned}
```

These terms use the paired operator phase
$`\widehat\nu_5^{\rm op}=\widehat\nu_5^{\rm raw}
+\tfrac12n_4\cup_4dn_4`$. The same change is included in the terminal
stacking law. The following three lower-layer contributions retain their
specified cochain representatives.

**Majorana contribution.**

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_6^\gamma
={}&\frac12\Big[
 \sum_{(\vartheta;x_1,\ldots,x_q)\in\mathcal I_6^\gamma}
       \mathop{\mathrm{MS}}\nolimits_\vartheta(x_1,\ldots,x_q)
 +s_1^2\widetilde{\beta^\circ\check n_3}\\
&\qquad+\check n_3(\overline{\beta\omega_2}+s_1\omega_2)\Big]\\
&+\frac14\Big[
 (\beta^\circ\check n_3)\cup_2(\beta^\circ\check n_3)
 +(\beta^\circ\check n_3)\cup_3d(\beta^\circ\check n_3)
 +\omega_2\beta^\circ\check n_3\Big].
\end{aligned}
```

**Majorana–p+ip contribution.**

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_6^{\gamma\psi}
={}&\frac12\Big[
 \sum_{(\vartheta;x_1,\ldots,x_q)\in\mathcal I_6^{\gamma\psi}}
       \mathop{\mathrm{MS}}\nolimits_\vartheta(x_1,\ldots,x_q)\\
&\qquad+(\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})
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

The [ordinary 4D coefficient table](formulas/FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md)
defines both finite sets. The 101 rows in $`\mathcal I_6^\gamma`$
have no differential argument. The 1,075 rows in
$`\mathcal I_6^{\gamma\psi}`$ contain both $`\check n_3`$
and $`d\check n_3`$; substitute the actual lower equation
$`d\check n_3=\bar n_2^2+\check\omega_2\bar n_2`$
in those arguments. Every row contains a Majorana argument, so this
word sum adds no pure-p+ip source term. The single second-digit term
retains the specified open-Bockstein continuation. This is a literal
regrouping of the cochain terms in the same phase coordinate.


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
 &+\frac18\check\omega_2n_2^2
   +\frac1{16}\mathcal P_{s_1}(\check\omega_2)n_2+\frac1{12}n_2^3.
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
the whole barred polynomial is reduced before its integer use. The pure binary cochain $`y_6`$ has a [complete finite source definition](formulas/SOURCE_OPERATIONS.md#source-completion),
with every coefficient listed in [Coefficients](formulas/COEFFICIENTS.md). The Majorana word coefficients are the explicit four-dimensional table linked above.

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

<a id="eq-t4c"></a>
<a id="eq-t4d"></a>

```math
\begin{aligned}
\widehat\nu_5^{\mathrm{out}}
 &=\widehat\nu_5+\widehat\nu'_5+\widehat{\mathcal{ℰ}}_5,\\
\widehat{\mathcal{ℰ}}_5
 &=\widehat{\mathcal{ℰ}}_5^c
  +\widehat{\mathcal{ℰ}}_5^{c\gamma}
  +\widehat{\mathcal{ℰ}}_5^{c\psi}
  +\widehat{\mathcal{ℰ}}_5^\gamma
  +\widehat{\mathcal{ℰ}}_5^{\gamma\psi}
  +\widehat{\mathcal{ℰ}}_5^\psi.
\end{aligned}
```

The output fields are those of the preceding three stacking laws. The
following formulas use the operator ordering of the complex-fermion
contribution. Its paired phase convention is stated after the formulas.

##### Complex fermions

```math
\widehat{\mathcal{ℰ}}_5^c
=\frac12\big[n_4\cup_3n'_4
 +(n_4+n'_4)\cup_3\mathcal{ℰ}_4\big].
```

##### Complex fermions and Majorana decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5^{c\gamma}
=\frac12\Big[&
 (\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})\cup_4n'_4\\
 &+N_4\cup_4(\mathcal{𝒪}_5^\gamma
                 +\mathcal{𝒪}_5^{\gamma\psi})[N_2,\check N_3]\\
 &+n_4\cup_4(\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})
 +n'_4\cup_4(\mathcal{𝒪}_5^{\gamma\prime}
                      +\mathcal{𝒪}_5^{\gamma\psi\prime})\Big].
\end{aligned}
```

Each Majorana obstruction includes its known differential terms. In
particular the output uses the actual $`\check N_3`$, including the
$`p+ip`$ contribution to Majorana stacking.

##### Complex fermions and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5^{c\psi}
=\frac12\Big[&\mathcal{𝒪}_5^\psi\cup_4n'_4
 +N_4\cup_4\mathcal{𝒪}_5^\psi[N_2]\\
 &+n_4\cup_4\mathcal{𝒪}_5^\psi
 +n'_4\cup_4\mathcal{𝒪}_5^{\psi\prime}\Big].
\end{aligned}
```

##### Majorana decoration

```math
\widehat{\mathcal{ℰ}}_5^\gamma
=\frac12\sum_{\eta\in\mathcal I_5^\gamma}
       \prod_{(x,f)\in\eta}x(f)
 +\frac14\overline{\mathcal V_5^\gamma}.
```

The finite sums in this subsection and the next two are evaluated on
$`(012345)`$. Their factors are original physical face values, and their
complete coefficient indices are specified in the
[physical coefficient appendix](formulas/FOUR_DIMENSIONAL_BINARY_COEFFICIENTS.md). They do not introduce higher-dimensional input fields.

##### Majorana and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5^{\gamma\psi}
={}&\frac12\Big[
 \sum_{\eta\in\mathcal I_5^{\gamma\psi}}
       \prod_{(x,f)\in\eta}x(f)
 +(\mathcal{ℰ}_4^\gamma+\mathcal{ℰ}_4^{\gamma\psi})
                   \cup_3(\bar n_2\bar n'_2)\\
&\quad+(\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi})
                  [N_2,\check N_3]\cup_4(\bar n_2\bar n'_2)\\
&\quad+\bar N_2\big[
  \check n_3\cup_3\check n'_3
  +(\check n_3+\check n'_3)\cup_3\check{\mathcal{ℰ}}_3\big]\\
&\quad+\mathcal V_5^\gamma\cup_5\mathcal V_5^{\gamma\psi}
 +\mathcal V_5^\gamma\cup_5\mathcal V_5^\psi
 +\mathcal V_5^{\gamma\psi}\cup_5\mathcal V_5^\psi\Big]\\
&+\frac14\Big[
 \overline{\mathcal V_5^{\gamma\psi}}
 +n_2\check n'_3+n'_2\check n_3\Big].
\end{aligned}
```

The three products of $`\mathcal V`$ retain the carry from the canonical
integer lift of their binary sum. They cannot be dropped when splitting a
quarter-valued contribution into physical parts.

##### p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5^\psi
={}&\frac12\Big[
 \sum_{\eta\in\mathcal I_5^\psi}\prod_{(x,f)\in\eta}x(f)
 +(\mathcal{ℰ}_4^\psi+\bar n_2\bar n'_2)
                    \cup_3(\bar n_2\bar n'_2)\\
&\quad+\mathcal{𝒪}_5^\psi[N_2]\cup_4(\bar n_2\bar n'_2)
 +\zeta_{2,2}(\bar n_2,\bar n'_2)
 +\bar n_2\cup_1[(\bar n'_2)^2+\check\omega_2\bar n'_2]\\
&\quad+\widetilde n_2(\bar n'_2\cup_1\bar n'_2)
 +(\check\omega_2\cup_1\bar n_2)\bar n'_2
 +s_1\bar n_2\widetilde n'_2
 +s_1(\bar n_2\cup_1s_1)\bar n'_2\\
&\quad+\check{\mathcal{ℰ}}_3(\bar n_2+\bar n'_2)
 +\check\omega_2\check{\mathcal{ℰ}}_3\Big]\\
&+\frac14\Big[
 \overline{\mathcal V_5^\psi}
 +N_2\check{\mathcal{ℰ}}_3
 +(n_2\cup_1\check\omega_2)n'_2
 +(n'_2\cup_1\check\omega_2)n_2\Big]\\
&+\frac18\check\omega_2(n_2\cup_1n'_2)\\
&+\frac13\Big[
 (n'_2-n_2)(n_2\cup_1n'_2)
 -(n_2\cup_1n'_2)(n'_2-n_2)\Big]\pmod1.
\end{aligned}
```

The final denominator-three term belongs to the integer cubic response.
All displayed integer products use the fixed signed coefficient transports.

<a id="eq-t4a"></a>

##### Carries in the quarter-valued terms

The carry already used in the full product has the exact integral split

```math
\begin{aligned}
\lambda_3&=\frac{\check N_3-\check n_3-\check n'_3+n_2\cup_1n'_2}{2}\\
 &=\lambda_3^\gamma
           +\lambda_3^{\gamma\psi}+\lambda_3^\psi,\\
\lambda_3^\gamma&=-\check n_3\cup_3\check n'_3,\\
\lambda_3^{\gamma\psi}
 &=-\overline{\check n_3+\check n'_3}
                        \cup_3\check{\mathcal{ℰ}}_3,\\
\lambda_3^\psi&=\frac{\check{\mathcal{ℰ}}_3+n_2\cup_1n'_2}{2}.
\end{aligned}
```

The products in these three definitions are integral. Binary factors use their canonical values, and the full bar on the middle line is retained. In the same convention,

```math
\Delta B_4=d\lambda_3-n'_2n_2,\qquad
\overline{\Delta B_4}=d\bar\lambda_3+\bar n'_2\bar n_2.
```

The three binary quarter numerators are expanded below. Their sum is the original binary numerator. The identity used above is

```math
\begin{aligned}
\frac14\overline{\mathcal V_5^\gamma
                  +\mathcal V_5^{\gamma\psi}+\mathcal V_5^\psi}
={}&\frac14\big[
 \overline{\mathcal V_5^\gamma}
 +\overline{\mathcal V_5^{\gamma\psi}}
 +\overline{\mathcal V_5^\psi}\big]\\
&+\frac12\big[
 \mathcal V_5^\gamma\cup_5\mathcal V_5^{\gamma\psi}
 +\mathcal V_5^\gamma\cup_5\mathcal V_5^\psi
 +\mathcal V_5^{\gamma\psi}\cup_5\mathcal V_5^\psi\big]
 \pmod1.
\end{aligned}
```


<a id="eq-t4b"></a>

###### Majorana quarter numerator


```math
\begin{aligned}
\mathcal V_5^\gamma={}&
 \bar B_4^\gamma\cup_3\bar B_4^{\gamma\prime}
 +d\bar B_4^\gamma\cup_4\bar B_4^{\gamma\prime}\\
&+(\bar B_4^\gamma+\bar B_4^{\gamma\prime})\cup_3d\bar\lambda_3^\gamma
 +(d\bar B_4^\gamma+d\bar B_4^{\gamma\prime})\cup_4d\bar\lambda_3^\gamma\\
&+\mathrm{Sq}^2\bar\lambda_3^\gamma
 +\omega_2\bar\lambda_3^\gamma.
\end{aligned}
```

Here $`B_4^\gamma=\beta^\circ\check n_3`$ is the Majorana part of the
already defined carry $`B_4=B_4^\gamma+B_4^\psi`$. Primes mean the second
stacking input. The three parts of $`\lambda_3`$ are those defined in the
main stacking formula.

###### Majorana–p+ip quarter numerator

```math
\begin{aligned}
\mathcal V_5^{\gamma\psi}={}&
 \bar B_4^\gamma\cup_3\bar B_4^{\psi\prime}
 +d\bar B_4^\gamma\cup_4\bar B_4^{\psi\prime}
 +\bar B_4^\psi\cup_3\bar B_4^{\gamma\prime}
 +d\bar B_4^\psi\cup_4\bar B_4^{\gamma\prime}\\
&+(\bar B_4^\gamma+\bar B_4^{\gamma\prime})
       \cup_3[d(\bar\lambda_3^{\gamma\psi}+\bar\lambda_3^\psi)
                       +\bar n'_2\bar n_2]\\
&+(d\bar B_4^\gamma+d\bar B_4^{\gamma\prime})
       \cup_4[d(\bar\lambda_3^{\gamma\psi}+\bar\lambda_3^\psi)
                       +\bar n'_2\bar n_2]\\
&+(\bar B_4^\psi+\bar B_4^{\psi\prime})
                      \cup_3d(\bar\lambda_3^\gamma+\bar\lambda_3^{\gamma\psi})\\
&+(d\bar B_4^\psi+d\bar B_4^{\psi\prime})
                      \cup_4d(\bar\lambda_3^\gamma+\bar\lambda_3^{\gamma\psi})\\
&+\mathrm{Sq}^2\bar\lambda_3^{\gamma\psi}
 +(\bar n'_2\bar n_2)\cup_3d(\bar\lambda_3^\gamma+\bar\lambda_3^{\gamma\psi})
 +\omega_2\bar\lambda_3^{\gamma\psi}
 +\check n'_3\bar n_2+\bar n'_2\check n_3\\
&+\sum_{i\lt j}\Big[
 \bar\lambda_3^i\cup_1\bar\lambda_3^j
 +\bar\lambda_3^j\cup_1\bar\lambda_3^i
 +\bar\lambda_3^i\cup_2d\bar\lambda_3^j
 +\bar\lambda_3^j\cup_2d\bar\lambda_3^i\Big].
\end{aligned}
```

The last sum contains the three pairs
$`(i,j)=(\gamma,\gamma\psi),(\gamma,\psi),(\gamma\psi,\psi)`$.
It is the ordinary polarization of the cochain Steenrod square, including
its differential terms.

###### p+ip quarter numerator

```math
\begin{aligned}
\mathcal V_5^\psi={}&
 \bar B_4^\psi\cup_3\bar B_4^{\psi\prime}
 +d\bar B_4^\psi\cup_4\bar B_4^{\psi\prime}\\
&+(\bar B_4^\psi+\bar B_4^{\psi\prime})
          \cup_3(d\bar\lambda_3^\psi+\bar n'_2\bar n_2)\\
&+(d\bar B_4^\psi+d\bar B_4^{\psi\prime})
          \cup_4(d\bar\lambda_3^\psi+\bar n'_2\bar n_2)\\
&+\mathrm{Sq}^2\bar\lambda_3^\psi
 +(\bar n'_2\bar n_2)\cup_3d\bar\lambda_3^\psi
 +\omega_2\bar\lambda_3^\psi\\
&+(\widetilde{\beta_{s_1}\check\omega_2}
       +\overline{\beta_{s_1}\check\omega_2})
                        (\bar n_2\cup_2\bar n'_2)\\
&+\zeta_{2,2}(\bar n'_2,\bar n_2)
 +(\check\omega_2\cup_1\bar n'_2)\bar n_2
 +\widetilde n'_2(\bar n_2\cup_1\bar n_2)\\
&+s_1\bar n'_2\widetilde n_2
 +s_1(\bar n'_2\cup_1s_1)\bar n_2.
\end{aligned}
```

Their sum is exactly the original binary numerator
$`\mathcal V_5=\mathcal V_5^\gamma+\mathcal V_5^{\gamma\psi}
+\mathcal V_5^\psi`$. Splitting its canonical integer lift produces the
three half-valued carry terms already included in
$`\widehat{\mathcal{ℰ}}_5^{\gamma\psi}`$.

The [paired operator phase map](formulas/REPRESENTATIVES.md#operator-phase-4d) is applied to both the obstruction and the stacking law.

## Finite definitions and coordinate maps

- 3+1D: [obstruction word coefficients](formulas/THREE_DIMENSIONAL_WORD_INDICES.md), [stacking word coefficients](formulas/THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md), [complex-fermion stacking coefficients](formulas/THREE_DIMENSIONAL_PRODUCT_CF_WORDS.md).
- 3+1D pure p+ip face coefficients: [obstruction](formulas/THREE_DIMENSIONAL_INTEGER_SOURCE_FACES.md), [stacking](formulas/THREE_DIMENSIONAL_INTEGER_PRODUCT_FACES.md).
- 4+1D: [Majorana word coefficients](formulas/FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md), [stacking coefficients](formulas/FOUR_DIMENSIONAL_BINARY_COEFFICIENTS.md), [physical face indices](formulas/FOUR_DIMENSIONAL_PHYSICAL_PATHS.md), [tensor coefficients](formulas/FOUR_DIMENSIONAL_TENSOR_COEFFICIENTS.md).
- [4+1D pure-source construction](formulas/SOURCE_OPERATIONS.md#source-completion).
- [Closed-Majorana formulas](formulas/MAJORANA_AND_ENDPOINTS.md)
- [Higher cups and finite sums](formulas/OPERATIONS.md), [fixed coefficients](formulas/COEFFICIENTS.md)
- [Changes of representative](formulas/REPRESENTATIVES.md)
- [Formula-to-code translation](../formulas/CODE_NOTATION.md)

A nonzero obstruction cochain may be a coboundary. Only its nontrivial
class after the permitted lower-layer changes obstructs the decoration.
