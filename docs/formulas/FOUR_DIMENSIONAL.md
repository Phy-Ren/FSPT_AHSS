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

The [ordinary 4D coefficient table](FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md)
defines both finite sets. The 85 rows in $`\mathcal I_6^\gamma`$
have no differential argument. The 1,005 rows in
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

#### Complex fermions and p+ip decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_5^{c\psi}
=\frac12\Big[&\mathcal{𝒪}_5^\psi\cup_4n'_4
 +N_4\cup_4\mathcal{𝒪}_5^\psi[N_2]\\
 &+n_4\cup_4\mathcal{𝒪}_5^\psi
 +n'_4\cup_4\mathcal{𝒪}_5^{\psi\prime}\Big].
\end{aligned}
```

#### Majorana decoration

```math
\widehat{\mathcal{ℰ}}_5^\gamma
=\frac12\sum_{\eta\in\mathcal I_5^\gamma}
       \prod_{(x,f)\in\eta}x(f)
 +\frac14\overline{\mathcal V_5^\gamma}.
```

The finite sums in this subsection and the next two are evaluated on
$`(012345)`$. Their factors are original physical face values, and their
complete coefficient indices are specified in the
[physical coefficient appendix](FOUR_DIMENSIONAL_BINARY_COEFFICIENTS.md). They do not introduce higher-dimensional input fields.

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
$`(i,j)=(\gamma,\gamma\psi),(\gamma,\psi),(\gamma\psi,\psi)`$.
It is the ordinary polarization of the cochain Steenrod square, including
its differential terms.

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

Their sum is exactly the original binary numerator
$`\mathcal V_5=\mathcal V_5^\gamma+\mathcal V_5^{\gamma\psi}
+\mathcal V_5^\psi`$. Splitting its canonical integer lift produces the
three half-valued carry terms already included in
$`\widehat{\mathcal{ℰ}}_5^{\gamma\psi}`$.

The [paired operator phase map](REPRESENTATIVES.md#operator-phase-4d) is applied to both the obstruction and the stacking law.
