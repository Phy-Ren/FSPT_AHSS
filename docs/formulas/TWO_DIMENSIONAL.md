<a id="two-dimensional"></a>

# 2+1D

Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates). Every physical field and layer below belongs to this dimension.

The physical fields are the binary Majorana cochain $`n_1`$,
the binary complex-fermion cochain $`n_2`$, and the phase $`\nu_3`$.
This is the zero-integer-decoration sector, in the manuscript operator
phase coordinate. Its [paired coordinate map](MAJORANA_AND_ENDPOINTS.md#eq-m12-2d)
is stated separately.

<a id="obstructions-2d"></a>
## Obstruction functions

### 1. Majorana obstruction

```math
dn_1=\mathcal{𝒪}_2=0.
```

### 2. Complex-fermion obstruction

```math
dn_2=\mathcal{𝒪}_3=\mathcal{𝒪}^{\gamma}_3.
```

#### Majorana contribution

```math
\mathcal{𝒪}^{\gamma}_3
 =\mathrm{Sq}^2n_1+\omega_2n_1+s_1\overline{\beta n_1}.
```

### 3. Bosonic obstruction

```math
d_{s_1}\widehat\nu_3=\widehat{\mathcal{𝒪}}_4
 =\widehat{\mathcal{𝒪}}^{c}_4
  +\widehat{\mathcal{𝒪}}^{c\gamma}_4
  +\widehat{\mathcal{𝒪}}^{\gamma}_4.
```

#### Complex-fermion contribution

```math
\widehat{\mathcal{𝒪}}^{c}_4
 =\frac12\big[\omega_2n_2+n_2\cup n_2
   +dn_2\cup_1n_2\big].
```

#### Complex-fermion–Majorana contribution

```math
\widehat{\mathcal{𝒪}}^{c\gamma}_4
 =\frac12\big[dn_2\cup_2dn_2\big].
```

#### Majorana contribution

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
## Stacking twisters

### 1. Majorana stacking

```math
N_1=n_1+n'_1.
```

There is no stacking correction in this layer.

### 2. Complex-fermion stacking

```math
N_2=n_2+n'_2+\mathcal{ℰ}_2,\qquad
\mathcal{ℰ}_2=\mathcal{ℰ}^{\gamma}_2.
```

#### Majorana contribution

```math
\mathcal{ℰ}^{\gamma}_2=(n_1\cup n'_1)+s_1(n_1\cup_1n'_1).
```

### 3. Bosonic stacking

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

#### Complex-fermion contribution

```math
\widehat{\mathcal{ℰ}}^{c}_3
 =\frac12\big[n_2\cup_1n'_2
 +(n_2+n'_2)\cup_1\mathcal{ℰ}_2\big].
```

#### Complex-fermion–Majorana contribution

```math
\begin{aligned}
\widehat{\mathcal{ℰ}}^{c\gamma}_3
 =\frac12\big[&dn_2\cup_2n'_2+N_2\cup_2dN_2\\
 &+n_2\cup_2dn_2+n'_2\cup_2dn'_2\big].
\end{aligned}
```

#### Majorana contribution

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
