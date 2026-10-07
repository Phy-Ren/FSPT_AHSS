<a id="four-dimensional"></a>
# 4+1D

Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates). Every physical field and layer below belongs to this dimension.

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
## Obstruction functions

### 1. p+ip obstruction

<a id="eq-integer-4d"></a>

```math
d_{s_1}n_2=0.
```

### 2. Majorana obstruction

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

### 3. Complex-fermion obstruction

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

### 4. Bosonic obstruction

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
\begin{aligned}
\widehat{\mathcal{𝒪}}_6^{c\gamma}
={}&\frac12\big[\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}\big]\cup_4\!\big[\\
&\qquad\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}\big].
\end{aligned}
```

The bracket reuses the complete Majorana parity from the preceding layer:
$`\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}=\mathrm{Sq}^2\check n_3
+\omega_2\check n_3+s_1\mathrm{Sq}^1\check n_3`$.
Its mixed component retains the terms proportional to $`d\check n_3`$;
no closed-input assumption is made. The outer superscript records the
exchanged fermion operators. Reusing their full parity does not change
that physical origin.

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
&+\frac14\mathcal Q_{\omega_2}[\beta^\circ\check n_3].
\end{aligned}
```

This finite sum contains **85 specified MS terms**. Its rows have no
differential argument; the other displayed half- and quarter-valued
terms are outside the sum.

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
 \mathcal Q_{\omega_2}[B_4]
 -\mathcal Q_{\omega_2}[\beta^\circ\check n_3]
 -\mathcal Q_{\omega_2}[B_4^\psi]\Big].
\end{aligned}
```

This finite sum contains **1,005 specified MS terms** with the defined
Majorana differential retained as an input. Every word and its arguments
are given in the [coefficient table](FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md).
For a supplementary check, substituting
$`d\check n_3=\bar n_2^2+\check\omega_2\bar n_2`$ gives 4,420
distributed occurrences before equal normalized operations collect to
**4,220 terms**. This substitution is not required in the reader formula. The other
displayed half- and quarter-valued terms are outside this sum.


**p+ip contribution.**

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_6^\psi
={}&\frac12y_6[n_2;\omega_2,s_1]\\
 &+\frac14\mathcal Q_{\omega_2}[B_4^\psi]\\
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

The quadratic cochain is defined once in the
[common notation](../FORMULA_GUIDE.md#integral-quadratic-cochain).
Its three defining cups occur in the pure Majorana and pure p+ip
quarter phases. The mixed quarter phase is their exact addition
polarization: it expands to four ordered cups, with no background
remainder. Here $`B_4=\beta^\circ\check n_3+B_4^\psi`$ is ordinary integer
addition. This organization preserves all three physical contributions
and their complete phases.

The polynomial $`y_6`$ contains **623,880 explicit physical-face monomials**
after its complete finite definition is expanded and equal binary
monomials are collected. The [complete physical coefficient table](FOUR_DIMENSIONAL_Y6_FACES.md)
specifies every monomial. It is not counted as one term. The remaining
displayed rational terms are additional.

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
the whole barred polynomial is reduced before its integer use. The pure binary cochain $`y_6`$ has a [complete finite source definition](SOURCE_OPERATIONS.md#source-completion),
with every coefficient listed in [Coefficients](COEFFICIENTS.md). The Majorana word coefficients are the explicit four-dimensional table linked above.

<a id="stacking-4d"></a>
## Stacking twisters

### 1. p+ip stacking

<a id="eq-p1-4d"></a>

```math
N_2=n_2+n'_2.
```

### 2. Majorana stacking

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

### 3. Complex-fermion stacking

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
 &+s_1\big[(\check n_3+\check n'_3)
                \cup_3\check{\mathcal{ℰ}}_3\big].
\end{aligned}
```

**p+ip contribution.**

```math
\begin{aligned}\mathcal{ℰ}_4^\psi={}&{z^\psi_4}({\bar n_{2}},{\bar n'_{2}})+[{\check\omega_2}({\bar n_{2}}+{\bar n'_{2}})]\cup_3{\check{\mathcal{ℰ}}_{3}}
 +(\check\omega_2\cup_2\bar n_2)
       [\bar n'_2+(\bar n_2\cup_2\bar n'_2)]
 +(\check\omega_2\cup_2\bar n'_2)\bar n_2\\
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

### 4. Bosonic stacking

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

#### Complex fermions

```math
\widehat{\mathcal{ℰ}}_5^c
=\frac12\big[n_4\cup_3n'_4
 +(n_4+n'_4)\cup_3\mathcal{ℰ}_4\big].
```

#### Complex fermions and Majorana decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5^{c\gamma}
={}&\frac12\Big[
 \big[\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}\big]\cup_4n'_4\\
&\qquad+\Delta\Big[
 n_4\cup_4\big[\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}\big]\Big]\Big].
\end{aligned}
```

The $`\Delta`$ has its defined three terms: the value at $`(N_4,\check N_3)`$ minus the values at $`(n_4,\check n_3)`$ and $`(n'_4,\check n'_3)`$. It uses the actual stacked fields, including their p+ip carries. All three parity brackets retain the cochain differential terms. This is an exact rewriting of the same contribution.

#### Complex fermions and p+ip decoration

```math
\widehat{\mathcal{ℰ}}_5^{c\psi}
=\frac12\Big[\mathcal{𝒪}_5^\psi\cup_4n'_4
 +\Delta\big(n_4\cup_4\mathcal{𝒪}_5^\psi\big)\Big].
```

#### Majorana decoration

On an ordered five-simplex, the complete Majorana contribution is

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5^\gamma
={}&\frac12\Big[
 \sum_{(\vartheta;x_1,\ldots,x_q)\in\mathcal I_5^\gamma}
       \mathop{\mathrm{MS}}\nolimits_{\vartheta}(x_1,\ldots,x_q)
 +s_1\big[(\bar B_4^\gamma+\bar B_4^{\gamma\prime})
                         \cup_3\bar\lambda_3^\gamma\big]\\
&\qquad+(\bar\lambda_4^\gamma)_{12345}
                  (\bar\lambda_3^\gamma)_{0145}
 +(\bar\lambda_4^\gamma)_{01235}
                  (\bar\lambda_3^\gamma)_{0345}\Big]\\
&+\frac14\Big[
 B_4^\gamma\cup_3B_4^{\gamma\prime}
 -(B_4^\gamma+B_4^{\gamma\prime})\cup_2\lambda_3^\gamma\\
&\qquad+\lambda_3^\gamma\cup_2\beta^\circ(\check n_3+\check n'_3)
 +\lambda_3^\gamma\cup_1\lambda_3^\gamma+\omega_2\lambda_3^\gamma\\
&\qquad-(dB_4^\gamma+dB_4^{\gamma\prime})\cup_3\lambda_3^\gamma
 +\lambda_3^\gamma\cup_2\lambda_4^\gamma
 +dB_4^\gamma\cup_4B_4^{\gamma\prime}\\
&\qquad+(dB_4^\gamma+dB_4^{\gamma\prime})\cup_4d\lambda_3^\gamma
 -(B_4^\gamma+B_4^{\gamma\prime}+d\lambda_3^\gamma)
                                      \cup_3\lambda_4^\gamma\\
&\qquad-(\lambda_4^\gamma)_{01235}(\lambda_4^\gamma)_{01345}
 +(\lambda_4^\gamma)_{02345}(\lambda_4^\gamma)_{01245}\\
&\qquad-(\lambda_4^\gamma)_{01235}(\lambda_4^\gamma)_{12345}
 -(\lambda_4^\gamma)_{01345}(\lambda_4^\gamma)_{12345}\\
&\qquad+\sum_{(\epsilon,\mathcal P)\in\mathcal J_5^\gamma}
 \epsilon\;\overline{
       \sum_{\eta\in\mathcal P}\prod_{(x,f)\in\eta}x_f}
 \Big]\pmod1.
\end{aligned}
```

Every unindexed cochain on the right is evaluated on the same simplex
$`012345`$. The face products are ordinary products of the indicated values.
The integer carries are

```math
\begin{aligned}
B_4^\gamma&=\beta^\circ\check n_3,
& B_4^{\gamma\prime}&=\beta^\circ\check n'_3,\\
\lambda_3^\gamma&=-\check n_3\cup_3\check n'_3,
&\lambda_4^\gamma&=-\overline{d\check n_3}
                         \cup_4\overline{d\check n'_3}.
\end{aligned}
```

The two $`\lambda`$ cochains are the same binary-addition carry, applied
to the Majorana inputs and to their lower differentials, respectively.
For any pair of binary degree-$`k`$ cochains, that carry is the integer
cochain $`-x\cup_kx'`$: the canonical integer value of their binary sum
is $`x+x'-2(x\cup_kx')`$. Thus $`\lambda_4^\gamma`$ introduces no new
polynomial or choice. Its factors are the **canonical binary
differentials**, not the integer differentials of the lifted fields.

The compatibility of the two carries is

```math
\beta^\circ(\check n_3+\check n'_3)
=B_4^\gamma+B_4^{\gamma\prime}
 +d\lambda_3^\gamma-\lambda_4^\gamma.
```

The first sum contains **455 individually specified MS terms**, unchanged
in the [ordinary coefficient table](FOUR_DIMENSIONAL_MAJORANA_STACKING_WORDS.md).
The last sum has **four separately lifted binary polynomials**, with signs
$`+,-,-,+`$. Their complete interiors contain **5, 15, 10, and 116 terms**,
respectively, listed in the
[canonical-lift coefficient table](FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.md).
Each whole binary sum is reduced before its integer value enters the
quarter bracket. Distributing those lifts would lose their carries.

After distributing the displayed linear additions, the formula has
**459 half-valued terms and 23 outer quarter-valued terms: 482 outer
terms**. The four lift interiors contain **146 explicit products**.
Counting those products in place of the four lift wrappers gives
**624 explicit term occurrences**, with all four reduction boundaries
retained. This replaces the previous 6,176-term expansion. Defined lower
differentials, Bocksteins, and binary-addition carries remain structured
arguments; $`d`$ denotes the cochain differential.

This is an exact rewriting of the same complete open-cochain
representative. No Majorana cocycle condition is imposed, and no term is
moved to another physical contribution. The obstruction and the
[existing output-gauge relation](FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md)
are unchanged. The [standalone replay](coefficients/verify_majorana_carry_reduction.py)
checks the replacement against the archived 5,707-term face polynomial,
using only public coefficient files and Python's standard library.

The [integer-carry derivation](FOUR_DIMENSIONAL_MAJORANA_CARRY_REDUCTION.md) explains the reduction before binary expansion. For closed Majorana self-stacking, a further [28-term formula](FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md) includes its explicit output-coboundary relation.

#### Majorana and p+ip decoration

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

This finite sum contains **5,684,189 explicit terms** with the defined
lower differentials, stacking twisters and integer carries retained.
The [complete coefficient table](FOUR_DIMENSIONAL_STACKING_COEFFICIENTS.md)
specifies every factor and argument. Expanding the remaining displayed
linear sums and the three quarter numerators adds **1,346 terms**, giving
**5,685,535 terms** for this contribution. Whole nonlinear lifts retain
their scopes; their complete interior terms are recorded separately in
the coefficient table.

The three products of $`\mathcal V`$ retain the carry from the canonical
integer lift of their binary sum. They cannot be dropped when splitting a
quarter-valued contribution into physical parts.

#### p+ip decoration

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

This finite sum contains **2,869,198 explicit terms**, including the entire
pure-source and tensor contributions. The
[complete coefficient table](FOUR_DIMENSIONAL_STACKING_COEFFICIENTS.md)
lists them with the same lower-operation convention. The other displayed
terms add **22**, giving **2,869,220 terms** for this contribution.
The protected whole quarter numerator has 20 interior terms, displayed
below; the other nonlinear interiors are specified in the coefficient table.

The final denominator-three term belongs to the integer cubic response.
All displayed integer products use the fixed signed coefficient transports.

<a id="eq-t4a"></a>

#### Carries in the quarter-valued terms

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

##### Majorana quarter numerator


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

With these defined carries and the standard Steenrod square retained,
this numerator contains **eight terms** after distributing the explicit
linear sums.

##### Majorana–p+ip quarter numerator

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
$`(i,j)=(\gamma,\gamma\psi),(\gamma,\psi),(\gamma\psi,\psi)`$,
and contains **twelve cup terms** with the defined stacking carries
retained. The entire mixed numerator contains **42 terms** at this boundary.
For a supplementary substitution check, inserting the lambda definitions and
expanding the cochain differentials of $`\bar\lambda_3^\gamma`$ and
$`\bar\lambda_3^{\gamma\psi}`$ gives **55 nested-cup terms** after
the lower Majorana equations are inserted. The entire binary reduction
of the exact quotient in $`\bar\lambda_3^\psi`$, and the differential
of that explicit quotient, remain intact; its numerator has two terms.
Distributing those two integer numerator terms inside a binary cup would
be invalid. The count 55 applies to this last sum alone, in that protected
quotient convention.

##### p+ip quarter numerator

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

The p+ip numerator contains **20 terms** with the defined lower carries
and standard operations retained. A canonical lift of a whole numerator
retains its scope: the mixed and pure lifts have respectively 42 and 20
terms inside them, and cannot be replaced by sums of individual lifts.

Their sum is exactly the original binary numerator
$`\mathcal V_5=\mathcal V_5^\gamma+\mathcal V_5^{\gamma\psi}
+\mathcal V_5^\psi`$. Splitting its canonical integer lift produces the
three half-valued carry terms already included in
$`\widehat{\mathcal{ℰ}}_5^{\gamma\psi}`$.

The [paired operator phase map](REPRESENTATIVES.md#operator-phase-4d) is applied to both the obstruction and the stacking law.
