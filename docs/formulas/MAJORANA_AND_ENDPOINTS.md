# Closed Majorana obstructions and stacking twisters

Read the complete section for the physical dimension:
[2+1D](#majorana-2d), [3+1D](#majorana-3d), or [4+1D](#majorana-4d).
The [1+1D fMPS endpoint](#fmps-1d) is stated separately.
Each section presents all obstruction functions first, followed by all
stacking twisters. There is no integer decoration in this appendix.

The superscripts follow the manuscript's operator factorization:
$`c`$ labels the complex-fermion part, $`\gamma`$ the Majorana part, and
$`c\gamma`$ their mixed part. They label contributions, not additional
cochains. In particular, $`dn_j`$ in a mixed term is fixed by the lower
obstruction equation of that dimension.

## Arithmetic and operations

Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates).
Lower-layer equations and half-valued brackets are binary. In integer
expressions, each named binary cochain means its canonical zero-or-one
representative; sums, differentials, and cups are then integral.
An outer bar first reduces the entire indicated expression modulo two.
Thus an integer $`x\cup_i y`$ and $`\overline{x\cup_i y}`$ are different
operations in a quarter-valued phase. Their complete evaluation rules are
in [Operations](OPERATIONS.md#arithmetic-and-carries).

The Bockstein $`\beta`$, its second carry $`\beta^+`$, and their signed
products have untwisted integer coefficients here. The phase instead has
coefficients $`(\mathbb R/\mathbb Z)_{s_1}`$ and differential $`d_{s_1}`$.
A hat denotes an additive phase, a prime the second input, and $`N_j`$ the
stacked binary field. The lower fields and all subscripts are fixed anew
at the start of each dimensional section.

The long polynomial names have the following roles:

| Expression | Meaning |
|---|---|
| $`\mathcal X_5,\mathcal X_6`$ | Intrinsic binary polynomials in the Majorana obstruction |
| $`z_4,z_5`$ | Binary completions of the Majorana stacking twisters |
| $`z^0_4,z^0_5`$ | Their [intrinsic word-polynomial parts](#intrinsic-word-products) |
| $`\mathcal L_3`$ | Binary antiunitary term in the 2+1D Majorana twister |

The reader's phase coordinate below uses the manuscript operator ordering.
Its explicit map from the previous representative is given in each
dimension, with both obstruction and stacking laws transported. It is
not implicitly identified with the full integer-layer phase coordinate
of the main guide.

<a id="majorana-2d"></a>
## 2+1D

The physical fields are the binary Majorana cochain $`n_1`$,
the binary complex-fermion cochain $`n_2`$, and the phase $`\nu_3`$.
The Majorana cochain is closed. We use the following phase coordinate
and its inverse, with the lower fields unchanged:

<a id="eq-m12-2d"></a>

**(M12, 2+1D: phase coordinate)**

```math
\begin{aligned}
\widehat\nu_3
 &=\widehat\nu^{\mathrm{old}}_3+\frac12n_2\cup_2dn_2,\\
\widehat\nu^{\mathrm{old}}_3
 &=\widehat\nu_3-\frac12n_2\cup_2dn_2.
\end{aligned}
```

### Obstruction functions

The lower equations are

<a id="eq-m2-2d"></a>

**(M2, 2+1D)**

```math
\begin{aligned}
dn_1&=0,\\
dn_2=\mathcal O_3
 &=\mathrm{Sq}^2n_1+\omega_2n_1+s_1\overline{\beta n_1}.
\end{aligned}
```

The terminal obstruction is the sum of its three operator contributions:

<a id="eq-m3-2d"></a>

**(M3, 2+1D: obstruction)**

```math
d_{s_1}\widehat\nu_3=\widehat{\mathcal O}_4
 =\widehat{\mathcal O}^{c}_4
  +\widehat{\mathcal O}^{\gamma}_4
  +\widehat{\mathcal O}^{c\gamma}_4.
```

**Complex-fermion contribution.**

<a id="eq-m3-c-2d"></a>

**(M3c, 2+1D)**

```math
\widehat{\mathcal O}^{c}_4
 =\frac12\big[\omega_2n_2+n_2\cup n_2
   +dn_2\cup_1n_2\big].
```

**Majorana contribution.**

<a id="eq-m6"></a>

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

<a id="eq-m3-cgamma-2d"></a>

**(M3cγ, 2+1D)**

```math
\widehat{\mathcal O}^{c\gamma}_4
 =\frac12\big[dn_2\cup_2dn_2\big].
```

The obstruction transforms with the stated phase coordinate:

<a id="eq-m12-source-2d"></a>

**(M12O, 2+1D)**

```math
\widehat{\mathcal O}_4
 =\widehat{\mathcal O}^{\mathrm{old}}_4
 +d_{s_1}\!\left[\frac12n_2\cup_2dn_2\right].
```

### Stacking twisters

The lower stacking law is

<a id="eq-m1-2d"></a>

**(M1, 2+1D)**

```math
\begin{aligned}
N_1&=n_1+n'_1,\\
\mathcal E_2&=(n_1\cup n'_1)+s_1(n_1\cup_1n'_1),\\
N_2&=n_2+n'_2+\mathcal E_2.
\end{aligned}
```

The terminal stacking law is

<a id="eq-m3-stacking-2d"></a>

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

<a id="eq-m3-stacking-c-2d"></a>

**(M3Ec, 2+1D)**

```math
\widehat{\mathcal E}^{c}_3
 =\frac12\big[n_2\cup_1n'_2
 +(n_2+n'_2)\cup_1\mathcal E_2\big].
```

**Majorana contribution.**
The binary antiunitary term is

<a id="eq-m10"></a>

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

<a id="eq-m11"></a>

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

<a id="eq-m3-stacking-cgamma-2d"></a>

**(M3Ecγ, 2+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}^{c\gamma}_3
 =\frac12\big[&dn_2\cup_2n'_2+N_2\cup_2dN_2\\
 &+n_2\cup_2dn_2+n'_2\cup_2dn'_2\big].
\end{aligned}
```

The stacking twister transforms with the same phase coordinate:

<a id="eq-m12-stacking-2d"></a>

**(M12E, 2+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}_3
 =\widehat{\mathcal E}^{\mathrm{old}}_3
 &+\frac12N_2\cup_2dN_2\\
 &-\frac12n_2\cup_2dn_2
  -\frac12n'_2\cup_2dn'_2.
\end{aligned}
```

### Chiral domain

These formulas compute the zero-integer fiber. For split unitary symmetry
($`\omega_2=s_1=0`$), an independent neutral chiral $`\mathbb Z`$ factor can
be adjoined. For the two nonsplit unitary controls in the example catalog,
the finite subgroup and its abstract infinite-cyclic completion are
reported separately; a marked minimal chiral generator is not specified.
The endpoint formulas do not cover general nonsplit nonzero-chiral cochain
inputs.

<a id="majorana-3d"></a>
## 3+1D

The physical fields are the binary Majorana cochain $`n_2`$,
the binary complex-fermion cochain $`n_3`$, and the phase $`\nu_4`$.
The Majorana cochain is closed. We use the following phase coordinate
and its inverse, with the lower fields unchanged:

<a id="eq-m12"></a>

**(M12, 3+1D: phase coordinate)**

```math
\begin{aligned}
\widehat\nu_4
 &=\widehat\nu^{\mathrm{old}}_4+\frac12n_3\cup_3dn_3,\\
\widehat\nu^{\mathrm{old}}_4
 &=\widehat\nu_4-\frac12n_3\cup_3dn_3.
\end{aligned}
```

### Obstruction functions

The lower equations are

<a id="eq-m2"></a>

**(M2, 3+1D)**

```math
\begin{aligned}
dn_2&=0,\\
dn_3=\mathcal O_4
 &=\mathrm{Sq}^2n_2+\omega_2n_2+s_1\overline{\beta n_2}.
\end{aligned}
```

The terminal obstruction is the sum of its three operator contributions:

<a id="eq-m3"></a>

**(M3, 3+1D: obstruction)**

```math
d_{s_1}\widehat\nu_4=\widehat{\mathcal O}_5
 =\widehat{\mathcal O}^{c}_5
  +\widehat{\mathcal O}^{\gamma}_5
  +\widehat{\mathcal O}^{c\gamma}_5.
```

**Complex-fermion contribution.**

<a id="eq-m3-c"></a>

**(M3c, 3+1D)**

```math
\widehat{\mathcal O}^{c}_5
 =\frac12\big[\omega_2n_3+n_3\cup_1n_3
   +dn_3\cup_2n_3\big].
```

**Majorana contribution.**

<a id="eq-m4"></a>

**(M4, 3+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}^\gamma_5(n_2)={}&\frac12\big[
 \zeta_{2,2}(\omega_2,n_2)+\mathcal X_5(n_2)\\
&\qquad+(n_2\cup n_2)\cup_3(\omega_2 n_2)\\
&\qquad+(n_2\cup n_2)\cup_3(s_1\overline{\beta n_2})\\
&\qquad+(\omega_2 n_2)\cup_3(s_1\overline{\beta n_2})\\
&\qquad+\zeta_{1,3}(s_1,\overline{\beta n_2})\\
&\qquad+(\omega_2\cup_1s_1)\overline{\beta n_2}+s_1(n_2\cup n_2)+s_1^2\overline{\beta^+n_2}\big]\\
&+\frac14\big[{\omega_2} \beta n_2+\beta n_2\cup_1\beta n_2\big].
\end{aligned}
```

Its word operations are

```math
\begin{aligned}
\zeta_{2,2}(\omega_2,n_2)
 &=\mathop{\mathrm{MS}}\nolimits_{1231343}(\omega_2,\omega_2,n_2,n_2),\\
\zeta_{1,3}(s_1,\overline{\beta n_2})
 &=\mathop{\mathrm{MS}}\nolimits_{1231434}(s_1,s_1,\overline{\beta n_2},\overline{\beta n_2}).
\end{aligned}
```

The intrinsic polynomial is

<a id="eq-m5"></a>

**(M5, 3+1D)**

```math
\begin{aligned}
\mathcal X_5(n_2)&=(\mathop{\mathrm{MS}}\nolimits_{1213243}+\mathop{\mathrm{MS}}\nolimits_{1213431}
 +\mathop{\mathrm{MS}}\nolimits_{1232141}+\mathop{\mathrm{MS}}\nolimits_{1234321})(n_2,n_2,n_2,n_2).
\end{aligned}
```

**Mixed contribution.**

<a id="eq-m3-cgamma"></a>

**(M3cγ, 3+1D)**

```math
\widehat{\mathcal O}^{c\gamma}_5
 =\frac12\big[dn_3\cup_3dn_3\big].
```

The obstruction transforms with the stated phase coordinate:

<a id="eq-m12-source"></a>

**(M12O, 3+1D)**

```math
\widehat{\mathcal O}_5
 =\widehat{\mathcal O}^{\mathrm{old}}_5
 +d_{s_1}\!\left[\frac12n_3\cup_3dn_3\right].
```

### Stacking twisters

The lower stacking law is

<a id="eq-m1"></a>

**(M1, 3+1D)**

```math
\begin{aligned}
N_2&=n_2+n'_2,\\
\mathcal E_3&=(n_2\cup_1n'_2)+s_1(n_2\cup_2n'_2),\\
N_3&=n_3+n'_3+\mathcal E_3.
\end{aligned}
```

The terminal stacking law is

<a id="eq-m3-stacking"></a>

**(M3E, 3+1D)**

```math
\begin{aligned}
\widehat\nu_4^{\mathrm{out}}
 &=\widehat\nu_4+\widehat\nu'_4+\widehat{\mathcal E}_4,\\
\widehat{\mathcal E}_4
 &=\widehat{\mathcal E}^{c}_4
  +\widehat{\mathcal E}^{\gamma}_4
  +\widehat{\mathcal E}^{c\gamma}_4.
\end{aligned}
```

**Complex-fermion contribution.**

<a id="eq-m3-stacking-c"></a>

**(M3Ec, 3+1D)**

```math
\widehat{\mathcal E}^{c}_4
 =\frac12\big[n_3\cup_2n'_3
 +(n_3+n'_3)\cup_2\mathcal E_3\big].
```

**Majorana contribution.**

<a id="eq-m7"></a>

**(M7, 3+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}^\gamma_4={}&\frac12z_4
 +\frac14\big[-\beta n_2\cup_2\beta n'_2\\
&\qquad+(\beta n_2+\beta n'_2)\cup_1\overline{n_2\cup_2n'_2}\\
&\qquad-\overline{n_2\cup_2n'_2}\cup_1\beta N_2\\
&\qquad+\overline{n_2\cup_2n'_2}\cup \overline{n_2\cup_2n'_2}\\
&\qquad-{\omega_2}\,\overline{n_2\cup_2n'_2}\big].
\end{aligned}
```

The binary completion is

<a id="eq-m8"></a>

**(M8, 3+1D)**

```math
\begin{aligned}
z_4={}&z^0_4(n_2,n'_2)+(\omega_2N_2)\cup_3\mathcal E_3
 +d(n_2\cup_1n'_2)\cup_4(\omega_2N_2)\\
&+(n'_2\cup n'_2)\cup_4(\omega_2n_2)\\
&+((n'_2\cup n'_2)+\omega_2n'_2)\cup_4(s_1\overline{\beta n_2})\\
&+(\omega_2\cup_1s_1)(n_2\cup_2n'_2)
 +(n_2\cup_1n'_2)\cup_3[s_1(\overline{\beta n_2}+\overline{\beta n'_2})]\\
&+(N_2\cup N_2)\cup_3(s_1(n_2\cup_2n'_2))+(n_2\cup_1n'_2)\cup_2(s_1(n_2\cup_2n'_2))\\
&+s_1\big[\mathcal E_3+\overline{\beta n_2}\cup_3\overline{\beta n'_2}\\
&\qquad+(n_2\cup_2n'_2)\cup_1(n_2\cup_2n'_2)\\
&\qquad+(\overline{\beta n_2}+\overline{\beta n'_2})\cup_3(s_1(n_2\cup_2n'_2))\\
&\qquad+(s_1(n_2\cup_2n'_2))\cup_2(n_2\cup_2n'_2)\\
&\qquad+\overline{\beta^+N_2-\beta^+n_2-\beta^+n'_2}\big].
\end{aligned}
```

The complete intrinsic term $`z^0_4(n_2,n'_2)`$ is given by the
[finite word definition](#intrinsic-word-products).

**Mixed contribution.**

<a id="eq-m3-stacking-cgamma"></a>

**(M3Ecγ, 3+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}^{c\gamma}_4
 =\frac12\big[&dn_3\cup_3n'_3+N_3\cup_3dN_3\\
 &+n_3\cup_3dn_3+n'_3\cup_3dn'_3\big].
\end{aligned}
```

The stacking twister transforms with the same phase coordinate:

<a id="eq-m12-stacking"></a>

**(M12E, 3+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}_4
 =\widehat{\mathcal E}^{\mathrm{old}}_4
 &+\frac12N_3\cup_3dN_3\\
 &-\frac12n_3\cup_3dn_3
  -\frac12n'_3\cup_3dn'_3.
\end{aligned}
```

<a id="majorana-4d"></a>
## 4+1D

The physical fields are the binary Majorana cochain $`n_3`$,
the binary complex-fermion cochain $`n_4`$, and the phase $`\nu_5`$.
The Majorana cochain is closed. We use the following phase coordinate
and its inverse, with the lower fields unchanged:

<a id="eq-m12-4d"></a>

**(M12, 4+1D: phase coordinate)**

```math
\begin{aligned}
\widehat\nu_5
 &=\widehat\nu^{\mathrm{old}}_5+\frac12n_4\cup_4dn_4,\\
\widehat\nu^{\mathrm{old}}_5
 &=\widehat\nu_5-\frac12n_4\cup_4dn_4.
\end{aligned}
```

### Obstruction functions

The lower equations are

<a id="eq-m2-4d"></a>

**(M2, 4+1D)**

```math
\begin{aligned}
dn_3&=0,\\
dn_4=\mathcal O_5
 &=\mathrm{Sq}^2n_3+\omega_2n_3+s_1\overline{\beta n_3}.
\end{aligned}
```

The terminal obstruction is the sum of its three operator contributions:

<a id="eq-m3-4d"></a>

**(M3, 4+1D: obstruction)**

```math
d_{s_1}\widehat\nu_5=\widehat{\mathcal O}_6
 =\widehat{\mathcal O}^{c}_6
  +\widehat{\mathcal O}^{\gamma}_6
  +\widehat{\mathcal O}^{c\gamma}_6.
```

**Complex-fermion contribution.**

<a id="eq-m3-c-4d"></a>

**(M3c, 4+1D)**

```math
\widehat{\mathcal O}^{c}_6
 =\frac12\big[\omega_2n_4+n_4\cup_2n_4
   +dn_4\cup_3n_4\big].
```

**Majorana contribution.**

<a id="eq-m4-4d"></a>

**(M4, 4+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}^\gamma_6(n_3)={}&\frac12\big[
 \zeta_{2,3}(\omega_2,n_3)+\mathcal X_6(n_3)\\
&\qquad+(n_3\cup_1n_3)\cup_4(\omega_2 n_3)\\
&\qquad+(n_3\cup_1n_3)\cup_4(s_1\overline{\beta n_3})\\
&\qquad+(\omega_2 n_3)\cup_4(s_1\overline{\beta n_3})\\
&\qquad+\zeta_{1,4}(s_1,\overline{\beta n_3})\\
&\qquad+(\omega_2\cup_1s_1)\overline{\beta n_3}+s_1(n_3\cup_1n_3)+s_1^2\overline{\beta^+n_3}\big]\\
&+\frac14\big[{\omega_2} \beta n_3+\beta n_3\cup_2\beta n_3\big].
\end{aligned}
```

Its word operations are

```math
\begin{aligned}
\zeta_{2,3}(\omega_2,n_3)
 &=\mathop{\mathrm{MS}}\nolimits_{12313434}(\omega_2,\omega_2,n_3,n_3),\\
\zeta_{1,4}(s_1,\overline{\beta n_3})
 &=\mathop{\mathrm{MS}}\nolimits_{12314343}(s_1,s_1,\overline{\beta n_3},\overline{\beta n_3}).
\end{aligned}
```

The intrinsic polynomial is

<a id="eq-m5-4d"></a>

**(M5, 4+1D)**

```math
\begin{aligned}
\mathcal X_6(n_3)&=(\mathop{\mathrm{MS}}\nolimits_{1213243142}+\mathop{\mathrm{MS}}\nolimits_{1213431412}
 +\mathop{\mathrm{MS}}\nolimits_{1232431421}+\mathop{\mathrm{MS}}\nolimits_{1234314212})(n_3,n_3,n_3,n_3)
 +\overline{\beta n_3}\cup_2\overline{\beta n_3}.
\end{aligned}
```

**Mixed contribution.**

<a id="eq-m3-cgamma-4d"></a>

**(M3cγ, 4+1D)**

```math
\widehat{\mathcal O}^{c\gamma}_6
 =\frac12\big[dn_4\cup_4dn_4\big].
```

The obstruction transforms with the stated phase coordinate:

<a id="eq-m12-source-4d"></a>

**(M12O, 4+1D)**

```math
\widehat{\mathcal O}_6
 =\widehat{\mathcal O}^{\mathrm{old}}_6
 +d_{s_1}\!\left[\frac12n_4\cup_4dn_4\right].
```

### Stacking twisters

The lower stacking law is

<a id="eq-m1-4d"></a>

**(M1, 4+1D)**

```math
\begin{aligned}
N_3&=n_3+n'_3,\\
\mathcal E_4&=(n_3\cup_2n'_3)+s_1(n_3\cup_3n'_3),\\
N_4&=n_4+n'_4+\mathcal E_4.
\end{aligned}
```

The terminal stacking law is

<a id="eq-m3-stacking-4d"></a>

**(M3E, 4+1D)**

```math
\begin{aligned}
\widehat\nu_5^{\mathrm{out}}
 &=\widehat\nu_5+\widehat\nu'_5+\widehat{\mathcal E}_5,\\
\widehat{\mathcal E}_5
 &=\widehat{\mathcal E}^{c}_5
  +\widehat{\mathcal E}^{\gamma}_5
  +\widehat{\mathcal E}^{c\gamma}_5.
\end{aligned}
```

**Complex-fermion contribution.**

<a id="eq-m3-stacking-c-4d"></a>

**(M3Ec, 4+1D)**

```math
\widehat{\mathcal E}^{c}_5
 =\frac12\big[n_4\cup_3n'_4
 +(n_4+n'_4)\cup_3\mathcal E_4\big].
```

**Majorana contribution.**

<a id="eq-m7-4d"></a>

**(M7, 4+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}^\gamma_5={}&\frac12z_5
 +\frac14\big[\beta n_3\cup_3\beta n'_3\\
&\qquad-(\beta n_3+\beta n'_3)\cup_2\overline{n_3\cup_3n'_3}\\
&\qquad-\overline{n_3\cup_3n'_3}\cup_2\beta N_3\\
&\qquad+\overline{n_3\cup_3n'_3}\cup_1\overline{n_3\cup_3n'_3}\\
&\qquad-{\omega_2}\,\overline{n_3\cup_3n'_3}\big].
\end{aligned}
```

The binary completion is

<a id="eq-m8-4d"></a>

**(M8, 4+1D)**

```math
\begin{aligned}
z_5={}&z^0_5(n_3,n'_3)+(\omega_2N_3)\cup_4\mathcal E_4
 +d(n_3\cup_2n'_3)\cup_5(\omega_2N_3)\\
&+(n'_3\cup_1n'_3)\cup_5(\omega_2n_3)\\
&+((n'_3\cup_1n'_3)+\omega_2n'_3)\cup_5(s_1\overline{\beta n_3})\\
&+(\omega_2\cup_1s_1)(n_3\cup_3n'_3)
 +(n_3\cup_2n'_3)\cup_4[s_1(\overline{\beta n_3}+\overline{\beta n'_3})]\\
&+(N_3\cup_1N_3)\cup_4(s_1(n_3\cup_3n'_3))+(n_3\cup_2n'_3)\cup_3(s_1(n_3\cup_3n'_3))\\
&+s_1\big[\mathcal E_4+\overline{\beta n_3}\cup_4\overline{\beta n'_3}\\
&\qquad+(n_3\cup_3n'_3)\cup_2(n_3\cup_3n'_3)\\
&\qquad+(\overline{\beta n_3}+\overline{\beta n'_3})\cup_4(s_1(n_3\cup_3n'_3))\\
&\qquad+(s_1(n_3\cup_3n'_3))\cup_3(n_3\cup_3n'_3)\\
&\qquad+\overline{\beta^+N_3-\beta^+n_3-\beta^+n'_3}\big].
\end{aligned}
```

The complete intrinsic term $`z^0_5(n_3,n'_3)`$ is given by the
[finite word definition](#intrinsic-word-products).

**Mixed contribution.**

<a id="eq-m3-stacking-cgamma-4d"></a>

**(M3Ecγ, 4+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}^{c\gamma}_5
 =\frac12\big[&dn_4\cup_4n'_4+N_4\cup_4dN_4\\
 &+n_4\cup_4dn_4+n'_4\cup_4dn'_4\big].
\end{aligned}
```

The stacking twister transforms with the same phase coordinate:

<a id="eq-m12-stacking-4d"></a>

**(M12E, 4+1D)**

```math
\begin{aligned}
\widehat{\mathcal E}_5
 =\widehat{\mathcal E}^{\mathrm{old}}_5
 &+\frac12N_4\cup_4dN_4\\
 &-\frac12n_4\cup_4dn_4
  -\frac12n'_4\cup_4dn'_4.
\end{aligned}
```

<a id="intrinsic-word-products"></a>
## Shared mathematical word operation

This section defines a mathematical operation on two closed binary cochains
$`x,y`$ of the same degree $`q=2`$ or $`q=3`$. Substituting the fields from
3+1D gives $`z^0_4(n_2,n'_2)`$; substituting those from 4+1D gives
$`z^0_5(n_3,n'_3)`$. All sums and word evaluations in this section are binary.

First sum the word operations in the following table on the listed inputs.

| Words | Ordered inputs |
|---|---|
| `12131432412`, `12343213431`, `23412342324` | $`(x,y,y,y)`$ |
| `12123434123`, `12131412324`, `12134131234`, `12312412423`, `12314324123`, `12314342413`, `13242412314`, `13412321341`, `13412321413`, `13413142134`, `13432412314`, `31214124324` | $`(x,x,y,y)`$ |
| `12413432312` | $`(x,x,x,y)`$ |
| `12131432412` | $`(y,x,x,(x+y))`$ |
| `12131432412` | $`((x+y),x,x,y)`$ |
| `12131432412`, `12134341321` | $`((x+y),y,y,x)`$ |
| `1212312` | $`((x+y),y,(x\cup_qy))`$ |
| `12313123` | $`(y,x,(x\cup_{q-1}y))`$ |
| `12131232` | $`(\overline{\beta x},y,y)`$ |
| `123131212` | $`(y\cup_{q-2}y,x,(x+y))`$ |
| `123131212` | $`((x+y)\cup_{q-2}(x+y),y,x)`$ |

For input degree three, use the words as written. For input degree two, a
word with $`k`$ input labels contributes only if its final $`k`$ letters
contain every label exactly once. Remove those final $`k-1`$ letters; if a
label is then missing, the term is zero. Otherwise evaluate the shortened
word on the listed inputs. This finite desuspension rule includes words
whose first input has degree greater than $`q`$.

Add the following six cup terms to obtain the complete intrinsic polynomial:

<a id="eq-m9"></a>

**(M9)**

```math
\begin{aligned}
z^0_{q+2}(x,y)={}&\text{word sum}
 +(x\cup_{q-1}y)\cup_{q-1}y\\
&+(\overline{\beta x}+\overline{\beta y})\cup_{q-1}(x\cup_qy)
\\
&+(x\cup_qy)\cup_{q-1}(\overline{\beta x}+\overline{\beta y}+y\cup_{q-1}x)\\
&+(x\cup_{q-1}y)\cup_{q+1}(x\cup_{q-2}x+y\cup_{q-2}y)
\\
&+y\cup_q(x\cup_{q-1}(x\cup_{q-1}y))+\overline{\beta y}\cup_q\overline{\beta x}.
\end{aligned}
```


<a id="fmps-1d"></a>
## 1+1D fMPS endpoint

The physical fields are $`n_0\in Z^0(G_b,\mathbb Z_2)`$,
$`n_1\in C^1(G_b,\mathbb Z_2)`$, and
$`\widehat\nu_2\in C^2(G_b,(\mathbb R/\mathbb Z)_{s_1})`$.
There is no integer layer. This fMPS representative is a distinct phase
coordinate; its physical field names do not imply an unstated coordinate
transformation to another manuscript representative.

### Obstruction functions

The lower and phase equations are

<a id="eq-m13"></a>

**(M13, 1+1D)**

```math
dn_0=0,\qquad dn_1=n_0\omega_2,\qquad
d_{s_1}\widehat\nu_2=\frac12n_1\omega_2.
```

The phase obstruction is entirely its complex-fermion contribution:

```math
\widehat{\mathcal O}^{c}_3=\frac12n_1\omega_2,\qquad
\widehat{\mathcal O}^{\gamma}_3=\widehat{\mathcal O}^{c\gamma}_3=0.
```

The nonzero $`n_0`$ sector requires $`\omega_2=0`$ pointwise in this
representative. If the extension cocycle is nonzero but exact, trivialize
it explicitly before using that sector.

### Stacking twisters

For two admissible inputs, the lower law is

<a id="eq-m14"></a>

**(M14, 1+1D)**

```math
\begin{aligned}
N_0&=n_0+n'_0,\\
N_1&=n_1+n'_1+n_0n'_0s_1.
\end{aligned}
```

The terminal phase law is

```math
\widehat\nu_2^{\mathrm{out}}
 =\widehat\nu_2+\widehat\nu'_2
  +\widehat{\mathcal E}^{c}_2+\widehat{\mathcal E}^{c\gamma}_2.
```

**Complex-fermion contribution.**

```math
\widehat{\mathcal E}^{c}_2=\frac12n_1n'_1.
```

**Majorana contribution.** The pure Majorana phase twister is zero.

**Mixed contribution.**

```math
\widehat{\mathcal E}^{c\gamma}_2
 =\begin{cases}
 \frac12(n_1^{\mathrm{even}})^2,&n_0\ne n'_0,\\
 0,&n_0=n'_0.
 \end{cases}
```

Here $`n_1^{\mathrm{even}}`$ is the degree-one cochain of the input whose
$`n_0=0`$. Classification also quotients by the residual parity gauge
$`\widehat\nu_2\sim\widehat\nu_2+\omega_2/2`$; this remains part of the
equivalence relation.
