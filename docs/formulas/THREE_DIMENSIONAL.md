<a id="three-dimensional"></a>
# 3+1D

Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates). Every physical field and layer below belongs to this dimension.

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
## Obstruction functions

### 1. p+ip obstruction

<a id="eq-integer-3d"></a>

```math
d_{s_1}n_1=0.
```

### 2. Majorana obstruction

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

### 3. Complex-fermion obstruction

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

### 4. Bosonic obstruction

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

#### Complex fermions

```math
\widehat{\mathcal{𝒪}}_5^c
 =\frac12[\omega_2n_3+n_3\cup_1n_3+dn_3\cup_2n_3].
```

#### Complex fermions and Majorana decoration

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_5^{c\gamma}
={}&\frac12\big[\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}\big]\cup_3\!\big[\\
&\qquad\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}\big].
\end{aligned}
```

The bracket reuses the complete Majorana parity from the preceding layer:
$`\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}=\mathrm{Sq}^2\check n_2
+\omega_2\check n_2+s_1\mathrm{Sq}^1\check n_2`$.
Its mixed component retains the terms proportional to $`d\check n_2`$;
no closed-input assumption is made. The outer superscript records the
exchanged fermion operators. Reusing their full parity does not change
that physical origin.

#### Complex fermions and p+ip decoration

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

The finite sum contains **25 specified MS terms**, [listed explicitly](THREE_DIMENSIONAL_WORD_INDICES.md#complex-fermion-indices). Every term contains
$`d\check n_2=\check\omega_2\bar n_1`$; this lower source has one cup term.

#### Majorana decoration

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

#### Majorana and p+ip decoration

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

The sum contains **2,276 ordinary MS terms** after substituting its finite
definitions and collecting equal normalized cochains. This counts the
complete half-valued sum; the quarter-valued terms are separate.

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
[coefficient appendix](THREE_DIMENSIONAL_WORD_INDICES.md#final-physical-index-sets).

#### p+ip decoration

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

The two sums contain **583 ordinary MS terms** and **10,825 physical-face
monomials**, respectively, after their coefficient polynomials are fully
expanded and collected. The latter count includes the background factors;
a coefficient-table row is not counted as a single term.

Every cochain expression without explicit arguments is evaluated on
$`(012345)`$. The [word indices](THREE_DIMENSIONAL_WORD_INDICES.md#final-physical-index-sets)
fix $`\mathcal I_5^\psi`$, and the
[physical-face coefficient table](THREE_DIMENSIONAL_INTEGER_SOURCE_FACES.md#physical-integer-source-coefficients)
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
## Stacking twisters

### 1. p+ip stacking

<a id="eq-p1"></a>

```math
N_1=n_1+n'_1.
```

### 2. Majorana stacking

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

### 3. Complex-fermion stacking

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

### 4. Bosonic stacking

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

For two identical complete states with $`n_1=0`$, the entire correction
reduces to the [ten-term self-stacking formula](THREE_DIMENSIONAL_MAJORANA_SELF_STACKING.md).
It retains the complex-fermion completion and uses the same phase representative.

#### Complex fermions

```math
\widehat{\mathcal{ℰ}}^{c}_4
 =\frac12\big[n_3\cup_2n'_3
 +(n_3+n'_3)\cup_2\mathcal{ℰ}_3\big].
```

#### Complex fermions and Majorana decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_4^{c\gamma}
={}&\frac12\Big[
 \big[\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}\big]\cup_3n'_3\\
&\qquad+\Delta\Big[
 n_3\cup_3\big[\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}\big]\Big]\Big].
\end{aligned}
```

The $`\Delta`$ has its defined three terms: the value at $`(N_3,\check N_2)`$ minus the values at $`(n_3,\check n_2)`$ and $`(n'_3,\check n'_2)`$. It uses the actual stacked fields, including their p+ip carries. All three parity brackets retain the cochain differential terms. This is an exact rewriting of the same contribution.

#### Complex fermions and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{c\psi}_4=\frac12\big[&
 \mathcal{𝒪}_4^\psi[n_1]\cup_3n'_3
 +\Delta\big(n_3\cup_3\mathcal{𝒪}_4^\psi\big)\\
 &+\sum_{(v;\boldsymbol x)\in\mathcal I_{4,A}}
       \mathop{\mathrm{MS}}\nolimits_v(\boldsymbol x)\\
 &+P_4[\check N_2,n_3+n'_3]
  +P_4[\check n_2+\check n'_2,n_3+n'_3]\big].
\end{aligned}
```

The finite MS sum contains **132 terms**, [listed explicitly](THREE_DIMENSIONAL_PRODUCT_CF_WORDS.md). They contain
$`d\check n_2=\check\omega_2\bar n_1`$ or its primed counterpart.
The two displayed $`P_4`$ terms differ by inserting the actual p+ip Majorana
stacking carry $`\bar n_1\bar n'_1`$; their eight-row definition is below. These terms retain the physical complex-fermion operator ordering. The accompanying 22 words with
$`dn_3`$ or $`dn'_3`$ are retained in the lower-sector index set.

Expanding that eight-word definition gives **16 and 52 specified MS
occurrences** in the two displayed evaluations, respectively, with the
defined output $`\check N_2`$ retained. Together they contribute **68
terms**, in addition to the 132-term sum.

#### Majorana decoration

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

The sum over $`\mathcal V_4`$ contains **seven specified MS terms**.
The other displayed terms of $`z_4^0`$ are outside this sum. The complete
$`z_4^0`$ has **20 distributed terms**; the complete $`z_4^\gamma`$ has
**37**, retaining the defined lower twister, integer carries, and whole
lift scopes.

#### Majorana and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{\gamma\psi}_4={}&
 \frac12\Big[z_4^\gamma+
   \sum_{(v;\boldsymbol x)\in\mathcal I_{4,\neg\psi}}
          \mathop{\mathrm{MS}}\nolimits_v(\boldsymbol x)\\
&\qquad+\omega_2\lambda_2^\gamma
 +d_{s_1}(\lambda_2^\gamma\cup_1\lambda_2^\gamma)\Big]\\
&+\frac14\Big[
 -\beta^\circ\check n_2\cup_2 B_3^{\psi\prime}
 -B_3^\psi\cup_2\beta^\circ\check n'_2
 +\beta^\circ\check n_2\cup_3
       [ (\beta_{s_1}\check\omega_2)n'_1]\\
&\quad+(\beta^\circ\check n_2+\beta^\circ\check n'_2)
       \cup_2d\lambda_2
 +(B_3^\psi+B_3^{\psi\prime})
       \cup_2d(\lambda_2^\gamma+\lambda_2^{\gamma\psi})\\
&\quad+\lambda_2\cup_1d\lambda_2-\lambda_2^2
 -\lambda_2^\psi\cup_1d\lambda_2^\psi+(\lambda_2^\psi)^2
 +\omega_2\lambda_2^{\gamma\psi}\\
&\quad-\big[\check N_2^2-\check n_2^2-(\check n'_2)^2
                      -(\bar n_1\bar n'_1)^2\big]\\
&\quad+d_{s_1}\Big[
 (\beta^\circ\check n_2+\beta^\circ\check n'_2)
                     \cup_2\lambda_2^\gamma
 +(d\lambda_2^\gamma)\cup_3d\lambda_2^\gamma
 -\overline{\check n_2\cup_1\check n'_2}\Big]\\
&\quad-(\beta^\circ\check n_2+\beta^\circ\check n'_2)
                  \cup_1\lambda_2^\gamma
 +\lambda_2^\gamma\cup_1
        \beta^\circ\overline{\check n_2+\check n'_2}
 -(\lambda_2^\gamma)^2
 \Big].
\end{aligned}
```

The MS sum over $`\mathcal I_{4,\neg\psi}`$ contains **15,994 terms**
after exact collection; $`z_4^\gamma`$ is outside that sum. The quarter-valued
quadratic expression uses the total integer carry $`\lambda_2`$ and
subtracts the same expression in $`\lambda_2^\psi`$. These **four terms**
are exact because
$`\lambda_2=\lambda_2^\gamma+\lambda_2^{\gamma\psi}+\lambda_2^\psi`$
is an equality of integer cochains. Expanding this split recovers the
eight ordered pairs other than $`(\psi,\psi)`$, or **16 cup terms**.
Further inserting the three carry definitions gives **24 distributed
integer-cup terms**. These are supplementary expansions; the whole
binary lift in the mixed carry retains its two-term interior and is not
distributed as an integer sum.

The two repeated quarter-valued copies of $`\omega_2\lambda_2^\gamma`$
have been combined in the half-valued bracket. The integer differential of
$`2\lambda_2^\gamma\cup_1\lambda_2^\gamma`$ is likewise half-valued.
These are exact coefficient combinations, with no change of phase
coordinate or reassignment of physical contributions.

This explicitly continued relative phase is zero on the closed-Majorana
physical tower by the proved paired coordinate map. Its half and quarter
brackets need not separately vanish. The integer derivatives and whole
binary lifts displayed here are part of that exact statement. The formula
can be simplified further only while retaining both coefficients and its
paired source map; canceling the binary parity of a quarter term is not
sufficient.

#### p+ip decoration

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

The sums contain **6,479 ordinary MS terms** and **4,094 physical-face
monomials**, respectively. These are the expanded sums themselves; the
following quarter- and eighth-valued terms are additional.

##### Physical-face coefficients

On an ordered four-simplex the remaining half-valued term is the following
finite polynomial in the physical integer digits and background faces:

```math
\frac12\sum_{(f,g)\in\mathcal C_4^\psi}f\,g.
```

This sum contains **4,094 physical-face monomials** after every background
coefficient is multiplied out and identical monomials are collected.
Every pair $`(f,g)`$ is printed in the
[physical-face coefficient table](THREE_DIMENSIONAL_INTEGER_PRODUCT_FACES.md).
Its 173 factored rows group 306 integer-digit monomials by common
background coefficients; neither of those two row counts is the expanded
term count. Each table entry contains
only $`\bar n_1`$, $`\widetilde n_1`$, their primed counterparts, the
explicit third digit $`\overline{\lfloor n_1/4\rfloor}`$, and the
physical faces of $`s_1`$, $`\omega_2`$, and $`\check\omega_2`$.

#### Physical fields, carries, and arithmetic

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

#### The finite phase polynomials

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

The [lower word indices](THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md) also use the nine-term phase numerator

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

The obstruction and stacking law use the same [paired phase convention](THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md), including the explicit output gauge.
