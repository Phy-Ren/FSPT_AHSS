# Closed Majorana laws and lower-dimensional endpoints

The formulas are separated by physical dimension:
[3+1D](#majorana-3d), [4+1D](#majorana-4d), and the
[2+1D](#majorana-2d) and [1+1D](#fmps-1d) endpoints.
Each section gives its own fields, source, and product. There is no integer
decoration in this appendix. All sections use the
[common notation](../FORMULA_GUIDE.md#conventions-and-coordinates).

## Arithmetic and operations

Lower-layer equations and half-valued brackets are binary. In integer
expressions, each named binary cochain means its canonical zero-or-one
representative; all sums, differentials, and cups are then integral.
An outer bar on a composite expression means first reduce that entire
expression modulo two. Thus $`x\cup_i y`$ in a quarter-valued term is a
signed integer cup, while $`\overline{x\cup_i y}`$ is its binary value.
[Operations](OPERATIONS.md#arithmetic-and-carries) gives the complete rule.

The Bockstein $`\beta`$, its second carry $`\beta^+`$, and their signed
products have **untwisted integer** coefficients here. The additive phase
has coefficients $`(\mathbb R/\mathbb Z)_{s_1}`$ and differential $`d_{s_1}`$.
These coefficient lines remain distinct even though binary values do not
carry a sign. A hat denotes an additive phase; a prime always labels the
second input, and $`N_j`$ is its stacked binary output.

The named expressions below are full operations, not aliases for fields.

| Expression | Meaning |
|---|---|
| $`\widehat{\mathcal O}^\gamma_j,\widehat{\mathcal E}^\gamma_j`$ | Pure Majorana contribution to a source or phase correction; $`\gamma`$ retains the paper's role label |
| $`\mathcal X_5,\mathcal X_6`$ | Intrinsic binary source polynomials of the indicated output degree |
| $`z_4,z_5`$ | Binary completion of the Majorana phase product |
| $`z^0_4,z^0_5`$ | Their intrinsic word-polynomial parts, [defined once](#intrinsic-word-products) on mathematical input cochains |
| $`\mathcal L_3`$ | Binary antiunitary correction at the 2+1D endpoint |

These formulas fix a phase representative in each dimension. Its explicit
change to the operator representative is given in the same section, with
source and product transported together. Neither is implicitly identified
with a nonzero-integer-layer representative in the main guide.

<a id="majorana-3d"></a>
## 3+1D closed Majorana formulas

The fields in 3+1D are the closed Majorana cochain $`n_2`$,
the complex-fermion cochain $`n_3`$, and the phase $`\nu_4`$.
Both lower fields are binary, and $`dn_2=0`$.

### Lower layers and full phase law

The lower product and source are

<a id="eq-m1"></a>

**(M1, 3+1D)**

```math
\begin{aligned}
N_2&=n_2+n'_2,\\
\mathcal E_3&=(n_2\cup_1n'_2)+s_1(n_2\cup_2n'_2).
\end{aligned}
```

<a id="eq-m2"></a>

**(M2, 3+1D)**

```math
\begin{aligned}
dn_3=\mathcal O_4
 &=\mathrm{Sq}^2n_2+\omega_2n_2+s_1\overline{\beta n_2},\\
N_3&=n_3+n'_3+\mathcal E_3.
\end{aligned}
```

The phase satisfies

```math
\begin{aligned}
d_{s_1}\widehat\nu_4&=\widehat{\mathcal O}_5,\\
\widehat\nu_4^{\mathrm{out}}
 &=\widehat\nu_4+\widehat\nu'_4+\widehat{\mathcal E}_4.
\end{aligned}
```

with the full source and product correction

<a id="eq-m3"></a>

**(M3, 3+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}_5(n_2,n_3)&=\frac12(\mathrm{Sq}^2n_3+\omega_2n_3)+\widehat{\mathcal O}^\gamma_5(n_2),\\
\widehat{\mathcal E}_4(n_2,n_3;n'_2,n'_3)&=\frac12\big[n_3\cup_2n'_3\\
&\qquad+dn_3\cup_3n'_3\\
&\qquad+(n_3+n'_3)\cup_2\mathcal E_3\big]+\widehat{\mathcal E}^\gamma_4(n_2,n'_2).
\end{aligned}
```

### Pure Majorana source

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

Here the two word operations are

```math
\begin{aligned}
\zeta_{2,2}(\omega_2,n_2)
 &=\mathop{\mathrm{MS}}\nolimits_{1231343}(\omega_2,\omega_2,n_2,n_2),\\
\zeta_{1,3}(s_1,\overline{\beta n_2})
 &=\mathop{\mathrm{MS}}\nolimits_{1231434}(s_1,s_1,\overline{\beta n_2},\overline{\beta n_2}).
\end{aligned}
```

The intrinsic source is

<a id="eq-m5"></a>

**(M5, 3+1D)**

```math
\begin{aligned}
\mathcal X_5(n_2)&=(\mathop{\mathrm{MS}}\nolimits_{1213243}+\mathop{\mathrm{MS}}\nolimits_{1213431}
 +\mathop{\mathrm{MS}}\nolimits_{1232141}+\mathop{\mathrm{MS}}\nolimits_{1234321})(n_2,n_2,n_2,n_2).
\end{aligned}
```

### Pure Majorana product

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

Every barred higher cup in the quarter-valued bracket is reduced before
entering the integer arithmetic. The binary completion is

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

The intrinsic term $`z^0_4(n_2,n'_2)`$ is given by the
[finite word definition](#intrinsic-word-products) below.
This representative is the stated desuspension of the 4+1D product.
The earlier manuscript representative uses a stacking-move boundary
dictionary; compare the complete products, including their mixed terms,
after placing them in matching coordinates.

### Change of phase representative

The operator representative changes the single-state phase by
$`\tfrac12n_3\cup_3dn_3`$. Therefore

<a id="eq-m12"></a>

**(M12, 3+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}^{\mathrm{op}}_5
 &=\widehat{\mathcal O}_5
   +d_{s_1}\!\left[\frac12n_3\cup_3dn_3\right],\\
\widehat{\mathcal E}^{\mathrm{op}}_4
 &=\widehat{\mathcal E}_4
   +\frac12N_3\cup_3dN_3\\
 &\qquad-\frac12n_3\cup_3dn_3
             -\frac12n'_3\cup_3dn'_3.
\end{aligned}
```

<a id="majorana-4d"></a>
## 4+1D closed Majorana formulas

The fields in 4+1D are the closed Majorana cochain $`n_3`$,
the complex-fermion cochain $`n_4`$, and the phase $`\nu_5`$.
Both lower fields are binary, and $`dn_3=0`$.

### Lower layers and full phase law

The lower product and source are

<a id="eq-m1-4d"></a>

**(M1, 4+1D)**

```math
\begin{aligned}
N_3&=n_3+n'_3,\\
\mathcal E_4&=(n_3\cup_2n'_3)+s_1(n_3\cup_3n'_3).
\end{aligned}
```

<a id="eq-m2-4d"></a>

**(M2, 4+1D)**

```math
\begin{aligned}
dn_4=\mathcal O_5
 &=\mathrm{Sq}^2n_3+\omega_2n_3+s_1\overline{\beta n_3},\\
N_4&=n_4+n'_4+\mathcal E_4.
\end{aligned}
```

The phase satisfies

```math
\begin{aligned}
d_{s_1}\widehat\nu_5&=\widehat{\mathcal O}_6,\\
\widehat\nu_5^{\mathrm{out}}
 &=\widehat\nu_5+\widehat\nu'_5+\widehat{\mathcal E}_5.
\end{aligned}
```

with the full source and product correction

<a id="eq-m3-4d"></a>

**(M3, 4+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}_6(n_3,n_4)&=\frac12(\mathrm{Sq}^2n_4+\omega_2n_4)+\widehat{\mathcal O}^\gamma_6(n_3),\\
\widehat{\mathcal E}_5(n_3,n_4;n'_3,n'_4)&=\frac12\big[n_4\cup_3n'_4\\
&\qquad+dn_4\cup_4n'_4\\
&\qquad+(n_4+n'_4)\cup_3\mathcal E_4\big]+\widehat{\mathcal E}^\gamma_5(n_3,n'_3).
\end{aligned}
```

### Pure Majorana source

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

Here the two word operations are

```math
\begin{aligned}
\zeta_{2,3}(\omega_2,n_3)
 &=\mathop{\mathrm{MS}}\nolimits_{12313434}(\omega_2,\omega_2,n_3,n_3),\\
\zeta_{1,4}(s_1,\overline{\beta n_3})
 &=\mathop{\mathrm{MS}}\nolimits_{12314343}(s_1,s_1,\overline{\beta n_3},\overline{\beta n_3}).
\end{aligned}
```

The intrinsic source is

<a id="eq-m5-4d"></a>

**(M5, 4+1D)**

```math
\begin{aligned}
\mathcal X_6(n_3)&=(\mathop{\mathrm{MS}}\nolimits_{1213243142}+\mathop{\mathrm{MS}}\nolimits_{1213431412}
 +\mathop{\mathrm{MS}}\nolimits_{1232431421}+\mathop{\mathrm{MS}}\nolimits_{1234314212})(n_3,n_3,n_3,n_3)
 +\overline{\beta n_3}\cup_2\overline{\beta n_3}.
\end{aligned}
```

### Pure Majorana product

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

Every barred higher cup in the quarter-valued bracket is reduced before
entering the integer arithmetic. The binary completion is

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

The intrinsic term $`z^0_5(n_3,n'_3)`$ is given by the
[finite word definition](#intrinsic-word-products) below.

### Change of phase representative

The operator representative changes the single-state phase by
$`\tfrac12n_4\cup_4dn_4`$. Therefore

<a id="eq-m12-4d"></a>

**(M12, 4+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}^{\mathrm{op}}_6
 &=\widehat{\mathcal O}_6
   +d_{s_1}\!\left[\frac12n_4\cup_4dn_4\right],\\
\widehat{\mathcal E}^{\mathrm{op}}_5
 &=\widehat{\mathcal E}_5
   +\frac12N_4\cup_4dN_4\\
 &\qquad-\frac12n_4\cup_4dn_4
             -\frac12n'_4\cup_4dn'_4.
\end{aligned}
```

<a id="intrinsic-word-products"></a>
## Intrinsic word products

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

<a id="majorana-2d"></a>
## 2+1D endpoint

The binary fields are the closed Majorana cochain $`n_1`$ and the
complex-fermion cochain $`n_2`$, with phase $`\nu_3`$. Their Majorana closure
is $`dn_1=0`$. The lower product and source are

<a id="eq-m1-2d"></a>

**(M1, 2+1D)**

```math
\begin{aligned}
N_1&=n_1+n'_1,\\
\mathcal E_2&=(n_1\cup n'_1)+s_1(n_1\cup_1n'_1).
\end{aligned}
```

<a id="eq-m2-2d"></a>

**(M2, 2+1D)**

```math
\begin{aligned}
dn_2=\mathcal O_3
 &=\mathrm{Sq}^2n_1+\omega_2n_1+s_1\overline{\beta n_1},\\
N_2&=n_2+n'_2+\mathcal E_2.
\end{aligned}
```

The phase law is

```math
\begin{aligned}
d_{s_1}\widehat\nu_3&=\widehat{\mathcal O}_4,\\
\widehat\nu_3^{\mathrm{out}}
 &=\widehat\nu_3+\widehat\nu'_3+\widehat{\mathcal E}_3.
\end{aligned}
```

with

<a id="eq-m3-2d"></a>

**(M3, 2+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}_4(n_1,n_2)&=\frac12(\mathrm{Sq}^2n_2+\omega_2n_2)+\widehat{\mathcal O}^\gamma_4(n_1),\\
\widehat{\mathcal E}_3(n_1,n_2;n'_1,n'_2)&=\frac12\big[n_2\cup_1n'_2\\
&\qquad+dn_2\cup_2n'_2\\
&\qquad+(n_2+n'_2)\cup_1\mathcal E_2\big]+\widehat{\mathcal E}^\gamma_3(n_1,n'_1).
\end{aligned}
```

### Pure Majorana source

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

### Pure Majorana product

The binary antiunitary correction is

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

The pure phase correction is

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
the entire indicated product. In contrast, $`n_1\cup_1n'_1`$ inside the
quarter-valued bracket is a signed integer cup, and its differential is
also integral. These operations cannot be interchanged.
The mixed complex-fermion terms are already included in the full phase
formula above. Simply discarding negative cup indices in a higher-dimensional
product would miss this endpoint's coordinate correction.

### Change of phase representative

The operator representative shifts the single-state phase by
$`\tfrac12n_2\cup_2dn_2`$. The paired changes are

<a id="eq-m12-2d"></a>

**(M12, 2+1D)**

```math
\begin{aligned}
\widehat{\mathcal O}^{\mathrm{op}}_4
 &=\widehat{\mathcal O}_4
   +d_{s_1}\!\left[\frac12n_2\cup_2dn_2\right],\\
\widehat{\mathcal E}^{\mathrm{op}}_3
 &=\widehat{\mathcal E}_3
   +\frac12N_2\cup_2dN_2\\
 &\qquad-\frac12n_2\cup_2dn_2
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
inputs. This restriction removes no term from the complete 3+1D or 4+1D laws.

<a id="fmps-1d"></a>
## 1+1D fMPS endpoint

The fields are $`n_0\in Z^0(G_b,\mathbb Z_2)`$,
$`n_1\in C^1(G_b,\mathbb Z_2)`$, and
$`\widehat\nu_2\in C^2(G_b,(\mathbb R/\mathbb Z)_{s_1})`$.
There is no integer layer. This fMPS representative is a distinct phase
coordinate; the physical field names do not imply an unstated coordinate
transformation to the manuscript representative. Its equations are

<a id="eq-m13"></a>

**(M13)**

```math
dn_0=0,\qquad dn_1=n_0\omega_2,\qquad
d_{s_1}\widehat\nu_2=\frac12n_1\omega_2.
```

The nonzero $`n_0`$ sector requires $`\omega_2=0`$ pointwise in this
representative. If the extension cocycle is nonzero but exact, trivialize
it explicitly before using that sector. For two admissible inputs,

<a id="eq-m14"></a>

**(M14)**

```math
\begin{aligned}
N_0&=n_0+n'_0,\\
N_1&=n_1+n'_1+n_0n'_0s_1,\\
\widehat\nu^{\mathrm{out}}_2
 &=\widehat\nu_2+\widehat\nu'_2+\frac12n_1n'_1
 +\begin{cases}\frac12(n_1^{\mathrm{even}})^2,&n_0\ne n'_0,\\
 0,&n_0=n'_0.\end{cases}
\end{aligned}
```

Here $`n_1^{\mathrm{even}}`$ is the degree-one cochain of the input whose
$`n_0=0`$. Classification also quotients by the residual parity gauge
$`\widehat\nu_2\sim\widehat\nu_2+\omega_2/2`$; this is part of the
equivalence relation, not an optional modification of [M14](#eq-m14).
