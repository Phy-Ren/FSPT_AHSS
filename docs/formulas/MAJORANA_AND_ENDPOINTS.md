# Closed Majorana laws and lower-dimensional endpoints

This appendix gives the closed-Majorana obstruction and stacking laws in
$`2+1`$, $`3+1`$ and $`4+1`$ dimensions, followed by the $`1+1`$D fMPS endpoint.
It uses the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates)
and [cochain operations](OPERATIONS.md) throughout. In particular,
$`\overline{x}`$ means reduction modulo two, a tilde means the canonical
integer lift of the entire indicated binary expression, and a hat means
the additive phase of a multiplicative $`U(1)`$ quantity. Primed fields belong
to the second input; $`N_j`$ is the stacked binary field.

## Fields and operations

Let $`q=1,2,3`$, with spatial dimension $`d=q+1`$. The fields are a **closed
Majorana** cochain $`n_q`$, a complex-fermion cochain $`n_{q+1}`$, and a phase
$`\nu_{q+2}=\exp(2\pi i\widehat\nu_{q+2})`$. There is no integer decoration
layer in this appendix. The Majorana closure equation is $`dn_q=0`$.

The ordinary Bockstein $`\beta n_q`$ and second (plus) carry
$`\beta^+n_q`$ are defined in [Operations](OPERATIONS.md). Their integer
lifts and signed cup products have **untwisted integer** coefficients here.
The phase instead takes values in $`(\mathbb R/\mathbb Z)_{s_1}`$, with
differential $`d_{s_1}`$. These two coefficient conventions must stay distinct.

Only the following composite operations need names beyond the common notation.
They denote full polynomials, not alternative names for the fields.

| Operation | Role | Definition |
|---|---|---|
| $`\widehat{\mathcal O}^\gamma_{q+3}`$, $`\widehat{\mathcal E}^\gamma_{q+2}`$ | Pure Majorana parts of the phase obstruction and stacking correction | [M3](#eq-m3), [M4](#eq-m4), [M6](#eq-m6), [M7](#eq-m7), [M11](#eq-m11) |
| $`\zeta_{i,j}`$ | Binary word operation used in the source | [M4](#eq-m4) and its word table |
| $`\mathcal X_{q+3}`$ | Intrinsic Majorana source polynomial, indexed by output degree | [M5](#eq-m5) |
| $`z_{q+2}`$, $`z^0_{q+2}`$ | Binary completion of the product, and its symmetry-independent part | [M8](#eq-m8), [M9](#eq-m9) |
| $`\mathcal L_3`$ | Antiunitary correction at the $`q=1`$ endpoint | [M10](#eq-m10) |

The superscript $`\gamma`$ retains the paper's label for the pure Majorana
contribution; it is not another cochain. The lower
correction $`\mathcal E_{q+1}`$ follows the same degree-based naming as the
main guide. The phase formulas below fix one representative; their paired
transport to the operator representative is given in [M12](#eq-m12).
Neither is implicitly identified with
the nonzero-integer-layer coordinate of the main guide.

## Lower layers and complete phase law

For two inputs, the Majorana sum and lower stacking correction are

<a id="eq-m1"></a>

**(M1)**

```math
\begin{aligned}
N_q&=n_q+n'_q,\\
\mathcal E_{q+1}&=(n_q\cup_{q-1}n'_q)+s_1(n_q\cup_qn'_q).
\end{aligned}
```

The complex-fermion equation and its stacked field are

<a id="eq-m2"></a>

**(M2)**

```math
\begin{aligned}
dn_{q+1}=\mathcal O_{q+2}
 &=\mathrm{Sq}^2n_q+\omega_2n_q+s_1\overline{\beta n_q},\\
N_{q+1}&=n_{q+1}+n'_{q+1}+\mathcal E_{q+1}.
\end{aligned}
```

In this representative the complete phase law is

```math
d_{s_1}\widehat\nu_{q+2}=\widehat{\mathcal O}_{q+3},\qquad
\widehat\nu^{\mathrm{out}}_{q+2}
 =\widehat\nu_{q+2}+\widehat\nu'_{q+2}+\widehat{\mathcal E}_{q+2},
```

where the source and correction separate as follows:

<a id="eq-m3"></a>

**(M3)**

```math
\begin{aligned}
\widehat{\mathcal O}_{q+3}(n_q,n_{q+1})&=\frac12(\mathrm{Sq}^2n_{q+1}+\omega_2n_{q+1})+\widehat{\mathcal O}^\gamma_{q+3}(n_q),\\
\widehat{\mathcal E}_{q+2}(n_q,n_{q+1};n'_q,n'_{q+1})&=\frac12\big[n_{q+1}\cup_qn'_{q+1}\\
&\qquad+dn_{q+1}\cup_{q+1}n'_{q+1}
\\
&\qquad+(n_{q+1}+n'_{q+1})\cup_q\mathcal E_{q+1}\big]+\widehat{\mathcal E}^\gamma_{q+2}(n_q,n'_q).
\end{aligned}
```

Equivalently, the multiplicative output is
$`\nu^{\mathrm{out}}_{q+2}=\nu_{q+2}\nu'_{q+2}\exp(2\pi i\widehat{\mathcal E}_{q+2})`$.

## Pure Majorana sources

For $`q=2,3`$,

<a id="eq-m4"></a>

**(M4)**

```math
\begin{aligned}
\widehat{\mathcal O}^\gamma_{q+3}(n_q)={}&\frac12\big[
 \zeta_{2,q}(\omega_2,n_q)+\mathcal X_{q+3}(n_q)\\
&\qquad+(n_q\cup_{q-2}n_q)\cup_{q+1}(\omega_2 n_q)\\
&\qquad+(n_q\cup_{q-2}n_q)\cup_{q+1}(s_1\overline{\beta n_q})\\
&\qquad+(\omega_2 n_q)\cup_{q+1}(s_1\overline{\beta n_q})\\
&\qquad+\zeta_{1,q+1}(s_1,\overline{\beta n_q})\\
&\qquad+(\omega_2\cup_1s_1)\overline{\beta n_q}+s_1(n_q\cup_{q-2}n_q)+s_1^2\overline{\beta^+n_q}\big]\\
&+\frac14\big[\widetilde{\omega_2} \beta n_q+\beta n_q\cup_{q-1}\beta n_q\big].
\end{aligned}
```

The four word operations appearing here are

| $`q`$ | $`\zeta_{2,q}(\omega_2,n_q)`$ | $`\zeta_{1,q+1}(s_1,\overline{\beta n_q})`$ |
|---|---|---|
| 2 | $`\mathop{\mathrm{MS}}\nolimits_{1231343}(\omega_2,\omega_2,n_q,n_q)`$ | $`\mathop{\mathrm{MS}}\nolimits_{1231434}(s_1,s_1,\overline{\beta n_q},\overline{\beta n_q})`$ |
| 3 | $`\mathop{\mathrm{MS}}\nolimits_{12313434}(\omega_2,\omega_2,n_q,n_q)`$ | $`\mathop{\mathrm{MS}}\nolimits_{12314343}(s_1,s_1,\overline{\beta n_q},\overline{\beta n_q})`$ |

The intrinsic source polynomials are

<a id="eq-m5"></a>

**(M5)**

```math
\begin{aligned}
\mathcal X_5(n_2)&=(\mathop{\mathrm{MS}}\nolimits_{1213243}+\mathop{\mathrm{MS}}\nolimits_{1213431}
 +\mathop{\mathrm{MS}}\nolimits_{1232141}+\mathop{\mathrm{MS}}\nolimits_{1234321})(n_2,n_2,n_2,n_2),\\
\mathcal X_6(n_3)&=(\mathop{\mathrm{MS}}\nolimits_{1213243142}+\mathop{\mathrm{MS}}\nolimits_{1213431412}
 +\mathop{\mathrm{MS}}\nolimits_{1232431421}+\mathop{\mathrm{MS}}\nolimits_{1234314212})(n_3,n_3,n_3,n_3)
 +\overline{\beta n_3}\cup_2\overline{\beta n_3}.
\end{aligned}
```

For $`q=1`$ the source is instead

<a id="eq-m6"></a>

**(M6)**

```math
\begin{aligned}
\widehat{\mathcal O}^\gamma_4(n_1)={}&\frac12\big[
 \mathop{\mathrm{MS}}\nolimits_{123134}(\omega_2,\omega_2,n_1,n_1)\\
&\qquad+(\omega_2n_1)\cup_2(s_1\overline{\beta n_1})
\\
&\qquad+(\omega_2\cup_1s_1)\overline{\beta n_1}+s_1(s_1+n_1)\overline{\beta n_1}\big]\\
&+\frac14\big[\widetilde{\omega_2} \beta n_1+\widetilde{s_1}\,\widetilde{n_1}\,\beta n_1\big].
\end{aligned}
```

Each half-valued bracket is formed in binary cochains before taking its
canonical lift. The quarter-valued brackets use integer lifts and signed cups.

## Pure Majorana products for q=2,3

One degree-indexed expression gives the product in both dimensions:

<a id="eq-m7"></a>

**(M7)**

```math
\begin{aligned}
\widehat{\mathcal E}^\gamma_{q+2}={}&\frac12z_{q+2}
 +\frac14\big[(-1)^{q+1}\beta n_q\cup_q\beta n'_q
\\
&\qquad+(-1)^q(\beta n_q+\beta n'_q)\cup_{q-1}\widetilde{n_q\cup_qn'_q}\\
&\qquad-\widetilde{n_q\cup_qn'_q}\cup_{q-1}\beta N_q
\\
&\qquad+\widetilde{n_q\cup_qn'_q}\cup_{q-2}\widetilde{n_q\cup_qn'_q}\\
&\qquad-\widetilde{\omega_2}\,\widetilde{n_q\cup_qn'_q}\big].
\end{aligned}
```

The overlap $`n_q\cup_qn'_q`$ is a binary cochain: form this product **before**
applying its tilde. Its binary completion is

<a id="eq-m8"></a>

**(M8)**

```math
\begin{aligned}
z_{q+2}={}&z^0_{q+2}+(\omega_2N_q)\cup_{q+1}\mathcal E_{q+1}
 +d(n_q\cup_{q-1}n'_q)\cup_{q+2}(\omega_2N_q)\\
&+(n'_q\cup_{q-2}n'_q)\cup_{q+2}(\omega_2n_q)\\
&+((n'_q\cup_{q-2}n'_q)+\omega_2n'_q)\cup_{q+2}(s_1\overline{\beta n_q})\\
&+(\omega_2\cup_1s_1)(n_q\cup_qn'_q)
 +(n_q\cup_{q-1}n'_q)\cup_{q+1}[s_1(\overline{\beta n_q}+\overline{\beta n'_q})]\\
&+(N_q\cup_{q-2}N_q)\cup_{q+1}(s_1(n_q\cup_qn'_q))+(n_q\cup_{q-1}n'_q)\cup_q(s_1(n_q\cup_qn'_q))\\
&+s_1\big[\mathcal E_{q+1}+\overline{\beta n_q}\cup_{q+1}\overline{\beta n'_q}\\
&\qquad+(n_q\cup_qn'_q)\cup_{q-1}(n_q\cup_qn'_q)\\
&\qquad+(\overline{\beta n_q}+\overline{\beta n'_q})\cup_{q+1}(s_1(n_q\cup_qn'_q))\\
&\qquad+(s_1(n_q\cup_qn'_q))\cup_q(n_q\cup_qn'_q)\\
&\qquad+\overline{\beta^+N_q-\beta^+n_q-\beta^+n'_q}\big].
\end{aligned}
```

To define the intrinsic polynomial $`z^0_{q+2}`$, first sum the following word
operations on their listed inputs, using the degree rule below the table.

| Words | Ordered inputs |
|---|---|
| `12131432412`, `12343213431`, `23412342324` | $`(n_q,n'_q,n'_q,n'_q)`$ |
| `12123434123`, `12131412324`, `12134131234`, `12312412423`, `12314324123`, `12314342413`, `13242412314`, `13412321341`, `13412321413`, `13413142134`, `13432412314`, `31214124324` | $`(n_q,n_q,n'_q,n'_q)`$ |
| `12413432312` | $`(n_q,n_q,n_q,n'_q)`$ |
| `12131432412` | $`(n'_q,n_q,n_q,N_q)`$ |
| `12131432412` | $`(N_q,n_q,n_q,n'_q)`$ |
| `12131432412`, `12134341321` | $`(N_q,n'_q,n'_q,n_q)`$ |
| `1212312` | $`(N_q,n'_q,(n_q\cup_qn'_q))`$ |
| `12313123` | $`(n'_q,n_q,(n_q\cup_{q-1}n'_q))`$ |
| `12131232` | $`(\overline{\beta n_q},n'_q,n'_q)`$ |
| `123131212` | $`(n'_q\cup_{q-2}n'_q,n_q,N_q)`$ |
| `123131212` | $`(N_q\cup_{q-2}N_q,n'_q,n_q)`$ |

For $`q=3`$, use these words unchanged. For $`q=2`$, a word with $`k`$ input
labels contributes only if its final $`k`$ letters contain every label exactly
once. Remove those final $`k-1`$ letters; if a label is then missing, the term
is zero. Otherwise evaluate the shortened word on the listed inputs. This
finite desuspension rule includes words whose first input has degree greater
than $`q`$.

Add the following six cup terms to that word sum:

<a id="eq-m9"></a>

**(M9)**

```math
\begin{aligned}
z^0_{q+2}={}&\text{word sum}
 +(n_q\cup_{q-1}n'_q)\cup_{q-1}n'_q\\
&+(\overline{\beta n_q}+\overline{\beta n'_q})\cup_{q-1}(n_q\cup_qn'_q)
\\
&+(n_q\cup_qn'_q)\cup_{q-1}(\overline{\beta n_q}+\overline{\beta n'_q}+n'_q\cup_{q-1}n_q)\\
&+(n_q\cup_{q-1}n'_q)\cup_{q+1}(n_q\cup_{q-2}n_q+n'_q\cup_{q-2}n'_q)
\\
&+n'_q\cup_q(n_q\cup_{q-1}(n_q\cup_{q-1}n'_q))+\overline{\beta n'_q}\cup_q\overline{\beta n_q}.
\end{aligned}
```

At $`q=2`$ this representative is the stated desuspension of the $`q=3`$
product. The earlier manuscript's longer representative uses a stacking-move
boundary dictionary. A comparison must therefore transport the complete
product into matching coordinates, including the mixed terms in [M3](#eq-m3).

## The q=1 product

The $`2+1`$D endpoint has fractional carries that require a separate formula.
Here $`N_1=n_1+n'_1`$. Its binary
antiunitary correction is

<a id="eq-m10"></a>

**(M10)**

```math
\begin{aligned}
\mathcal L_3={}&s_1((s_1\cup_1n_1)+(s_1\cup_1n'_1)+[s_1\cup_1(n_1\cup_1n'_1)])(n_1\cup_1n'_1)\\
&+(s_1\cup_1n_1) (n_1\cup_1n'_1)N_1
\\
&+((s_1\cup_1n_1) n_1+n_1 (s_1\cup_1n'_1)+s_1n_1+n_1s_1)(n_1\cup_1n'_1)\\
&+s_1((n_1\cup_1n'_1)n_1+n_1n'_1+n'_1(n_1\cup_1n'_1)).
\end{aligned}
```

The pure Majorana phase correction is

<a id="eq-m11"></a>

**(M11)**

```math
\begin{aligned}
\widehat{\mathcal E}^\gamma_3={}&
\frac14\big[\beta n_1\cup_1\beta n'_1\\
&\qquad-(\beta n_1+\beta n'_1)(\widetilde{n_1}\cup_1\widetilde{n'_1})\\
&\qquad-(\widetilde{n_1}\cup_1\widetilde{n'_1})(\beta n_1+\beta n'_1)\\
&\qquad+(\widetilde{n_1}\cup_1\widetilde{n'_1})d(\widetilde{n_1}\cup_1\widetilde{n'_1})\big]\\
&+\frac12[n_1\cup_1(n_1n'_1)]n'_1
 -\frac18\widetilde{N_1^3}+\frac18\widetilde{n_1^3}+\frac18\widetilde{(n'_1)^3}\\
&+\frac12(\omega_2N_1)\cup_2(n_1n'_1)\\
&-\frac14\widetilde{\omega_2} (\widetilde{n_1}\cup_1\widetilde{n'_1})
 +\frac12\mathcal L_3+\frac14\widetilde{s_1n_1n'_1}\\
&+\frac12\big[(\omega_2\cup_1s_1)(n_1\cup_1n'_1)\\
&\qquad+(\omega_2N_1)\cup_2(s_1(n_1\cup_1n'_1))\\
&\qquad+(\omega_2n'_1)\cup_3(s_1n_1^2)\big]
 \pmod1.
\end{aligned}
```

The tildes on the eighth-valued terms and on $`\widetilde{s_1n_1n'_1}`$ lift
the entire displayed **binary product**. In contrast,
$`\widetilde{n_1}\cup_1\widetilde{n'_1}`$ is a signed integer cup of two lifted
inputs; its differential is also integral. These operations cannot be
interchanged. Add the mixed complex-fermion bracket in [M3](#eq-m3), at
$`q=1`$, to obtain the complete phase. Merely dropping negative cup indices
from [M7](#eq-m7) would miss the endpoint coordinate correction.

## Change of phase representative

The operator representative changes the single-state additive phase by
$`\tfrac12n_{q+1}\cup_{q+1}dn_{q+1}`$. For the same lower fields, the paired
transport is therefore

<a id="eq-m12"></a>

**(M12)**

```math
\begin{aligned}
\widehat{\mathcal O}^{\mathrm{op}}_{q+3}
 &=\widehat{\mathcal O}_{q+3}
   +d_{s_1}\!\left[\frac12n_{q+1}\cup_{q+1}dn_{q+1}\right],\\
\widehat{\mathcal E}^{\mathrm{op}}_{q+2}
 &=\widehat{\mathcal E}_{q+2}
   +\frac12N_{q+1}\cup_{q+1}dN_{q+1}\\
 &\qquad-\frac12n_{q+1}\cup_{q+1}dn_{q+1}
             -\frac12n'_{q+1}\cup_{q+1}dn'_{q+1}.
\end{aligned}
```

This states both representatives without duplicating a long polynomial. It
does not identify either with a different integer-layer convention.

## The 2+1D chiral domain

The degree-one Majorana formulas compute the zero-integer fiber. For split
unitary symmetry ($`\omega_2=s_1=0`$), an independent neutral chiral
$`\mathbb Z`$ factor can be adjoined. For the two nonsplit unitary controls in
the example catalog, the finite subgroup and its abstract infinite-cyclic
completion are reported separately; a marked minimal chiral generator is
not specified. The formulas above do not cover general nonsplit
nonzero-chiral cochain inputs. This restriction does not remove any term
from the complete $`3+1`$D or $`4+1`$D laws in the main guide.

## The 1+1D fMPS endpoint

Use the physical layer names also for the fMPS representative:
$`n_0\in Z^0(G_b,\mathbb Z_2)`$,
$`n_1\in C^1(G_b,\mathbb Z_2)`$ and
$`\widehat\nu_2\in C^2(G_b,(\mathbb R/\mathbb Z)_{s_1})`$.
There is no integer layer. This fMPS representative is a distinct choice
of phase coordinate; using the same physical layer names does not assert
an unstated coordinate transformation to the manuscript representative.
The equations are

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
