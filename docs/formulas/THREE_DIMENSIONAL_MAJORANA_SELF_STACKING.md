# Self-stacking in 3+1D with no p+ip decoration

Take a complete state with $`n_1=0`$, closed binary Majorana cochain
$`n_2`$, binary complex-fermion cochain $`n_3`$, and additive phase
$`\widehat\nu_4`$. The input satisfies the obstruction equations in the
[3+1D formula section](THREE_DIMENSIONAL.md), including
$`dn_3=\mathcal{𝒪}_4^\gamma[n_2]`$. The backgrounds are shared by both
copies. The restriction is **zero p+ip decoration**, not merely a closed
Majorana cochain inside a state with nonzero p+ip decoration.

All corrections below are evaluated on two identical complete states.
The separate output layers are as follows.

## 1. p+ip stacking

```math
N_1=0.
```

## 2. Majorana stacking

```math
N_2=0.
```

## 3. Complex-fermion stacking

```math
N_3=\mathcal{ℰ}_3^\gamma=\mathrm{Sq}^1n_2+s_1n_2.
```

## 4. Bosonic stacking

```math
\begin{aligned}
\widehat\nu_4^{\mathrm{out}}&=2\widehat\nu_4+\widehat{\mathcal{ℰ}}_4,\\
\widehat{\mathcal{ℰ}}_4
 &=\widehat{\mathcal{ℰ}}_4^c
  +\widehat{\mathcal{ℰ}}_4^{c\gamma}
  +\widehat{\mathcal{ℰ}}_4^\gamma.
\end{aligned}
```

In the same phase representative as the main formulas, the three
contributions are as follows.

### Complex fermions

```math
\widehat{\mathcal{ℰ}}_4^c
 =\frac12n_3\cup_2n_3.
```

### Complex fermions and Majorana decoration

```math
\widehat{\mathcal{ℰ}}_4^{c\gamma}
 =\frac12\mathcal{𝒪}_4^\gamma[n_2]\cup_3n_3.
```

### Majorana decoration

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}_4^\gamma
={}&\frac12\Big[
 (\omega_2\cup_1s_1)n_2
 +\overline{\beta n_2}\cup_2(s_1n_2)
 +s_1N_3\\
&\qquad+s_1\big[(s_1n_2)\cup_2n_2\big]+n_2^2\Big]\\
&+\frac14\Big[
 (\beta n_2)\cup_2(\beta n_2)
 +s_1\overline{\beta n_2}
 -\mathcal{𝒪}_4^\gamma[n_2]\Big]\pmod1.
\end{aligned}
```

The already defined lower obstruction is

```math
\mathcal{𝒪}_4^\gamma[n_2]
 =n_2^2+\omega_2n_2+s_1\overline{\beta n_2},
\qquad
\beta n_2=\frac{dn_2}{2}\quad\text{over }\mathbb Z.
```

The lower obstruction is evaluated in binary arithmetic before its
canonical integer value enters the quarter bracket. In particular,
$`-\mathcal{𝒪}_4^\gamma/4`$ is not the negative quarter of the integer sum
of its three displayed binary components. The Bockstein and its higher
cup instead use their actual integer values and the signed cup convention.
The half bracket is binary. These conventions also apply when the
Bockstein takes negative values.

The complete self-stacking correction has **ten specified terms**:
seven in the half brackets and three in the quarter bracket. This count
reuses the previously computed lower output $`N_3`$ and the defined
lower obstruction. Expanding $`s_1N_3`$ into its two terms gives eleven.
There is no finite coefficient sum or unspecified polynomial in this
formula. The input complex-fermion completion and the incoming phase
remain present; the formula does not set either one to zero.

This is an exact specialization and simplification of the main product,
with no change of its phase representative. The output may still require
its usual lower-layer gauge reductions when a group relation is read
from it.

## Why the intrinsic word terms disappear

For a closed binary degree-two cochain $`x`$, the seven intrinsic terms
in the main formula obey

```math
\sum_{v\in\{12123434,12134131,12314324,12314342,
13242412,13413142,13432412\}}
 \mathop{\mathrm{MS}}\nolimits_v(x,x,x,x)=0.
```

This is the exact cancellation of **seven MS terms**, with no coboundary
removed. The remaining intrinsic binary terms reduce using

```math
\mathop{\mathrm{MS}}\nolimits_{123131}
 (x,x,\overline{\beta x})
 +x\cup_1\overline{\beta x}
 +x\cup_2\big(x\cup_1\overline{\beta x}\big)=0.
```

This identity has **three specified terms**. The other copy of
$`\overline{\beta x}\cup_1x/2`$ cancels the half-valued reduction of
$`(\beta x)\cup_1x/2`$ in the integer part.

Finally, for three binary degree-four cochains, their three pairwise
pointwise products give exactly the carry between the integer sum of
individual values and the canonical value of their binary sum, modulo
one after division by two. Apply this to
$`n_2^2`$, $`\omega_2n_2`$, and
$`s_1\overline{\beta n_2}`$. Their binary sum is the already defined
$`\mathcal{𝒪}_4^\gamma`$. This accounts for the whole obstruction in the
quarter bracket without dropping its carry.

The [standalone symbolic verifier](coefficients/verify_three_dimensional_majorana_self_stacking.py)
checks these identities and the complete formula using exact Boolean and
integer coefficient polynomials, rather than selected group examples.
It treats all closed Majorana and background inputs on an ordered
four-simplex and every compatible complex-fermion completion.
