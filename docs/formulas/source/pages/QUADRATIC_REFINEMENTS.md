# Integral quadratic cochains and their stacking polarization

The fractional Majorana and p+ip obstructions repeatedly contain the same
quadratic expression in an integer lift carry. Defining this expression
once exposes the relation between the obstruction and its stacking
correction. The construction below is an integral **cochain** formula;
it is not a Pontryagin square or a cohomology operation on arbitrary open
inputs.

## The quadratic cochain

For an untwisted integer cochain $`x\in C^q(X;\mathbb Z)`$, $`q\ge2`$,
define

<a id="quadratic-cochain"></a>

{{equation:quadratic-refinements--the-quadratic-cochain--1}}

The output has degree $`q+2`$ and integer coefficients. The background
$`\omega_2`$ in this formula is its canonical integer representative;
$`d\omega_2=2\beta\omega_2`$, rather than zero. Integer cups use the
[signed convention](OPERATIONS.md#eq-o6). In particular no binary
reduction is performed inside this definition. It contains **three
specified cup terms**.

Its binary reduction is the familiar open-cochain Steenrod expression:

{{equation:quadratic-refinements--the-quadratic-cochain--2}}

The second identity assumes the stated closed binary background. The
definition is degree-parametric; the integer stacking variation below
is established for degree four, which is the degree needed in $`4+1`$D.
No additional degree-independent integer identity is assumed.

## Exact addition and lift dependence

For integer cochains $`x,y`$ of the same degree $`q`$, ordinary addition
gives the exact polarization

<a id="addition-polarization"></a>

{{equation:quadratic-refinements--exact-addition-and-lift-dependence--3}}

These are **four specified cup terms**. This equation holds over the
integers, with no closure hypothesis on either input.

Changing the integer representative from $`x`$ to $`x+2z`$ preserves its
parity but changes the quarter-valued phase by

<a id="lift-dependence"></a>

{{equation:quadratic-refinements--exact-addition-and-lift-dependence--4}}

The omitted integral part is exactly
$`z\cup_{q-2}z+z\cup_{q-1}dz`$. Thus the integer lift is part of the
definition. A parity-preserving change is not silently identified with
the same phase. Changing the background lift by $`2z_2`$ likewise adds
$`z_2x/2`$ to the quarter-valued phase.

## The quadratic part of the 4+1D obstruction

The [integer carries](FOUR_DIMENSIONAL.md#eq-s1) are already fixed:
$`B_4^\gamma=\beta^\circ\check n_3`$ and
$`B_4=B_4^\gamma+B_4^\psi`$. The quadratic quarter-valued terms in the
three physical contributions are, respectively,

<a id="obstruction-specialization"></a>

{{equation:quadratic-refinements--the-quadratic-part-of-the-4-1d-obstruction--5}}

This is exactly the previous three-, four-, and three-term division into
physical contributions. All other terms of those obstructions retain
their existing values and physical labels. The same operation occurs
in the product: the characteristic part of the integer kernel is
$`\Delta\mathcal Q_{\omega_2}[B_4]`$, where $`\Delta`$ uses the actual
lower stacking output. This reuse changes neither representative nor
coefficients. It reduces repeated definitions; it does not reduce the
number of scalar monomials obtained by expanding them.

## Degree-four variation on the physical lower tower

Use the two $`4+1`$D inputs with their common backgrounds. The already
defined integer stacking carry $`\lambda_3`$ obeys

{{equation:quadratic-refinements--degree-four-variation-on-the-physical-lower-tower--6}}

The integer $`B_4,B'_4,\lambda_3`$ are untwisted; $`n_2,n'_2`$ have
coefficients $`\mathbb Z_{s_1}`$. Products of the twisted inputs include
their local coefficient transports. In particular $`d(n'_2n_2)=0`$.

The integer transgression of the quadratic cochain is

<a id="quadratic-transgression"></a>

{{equation:quadratic-refinements--degree-four-variation-on-the-physical-lower-tower--7}}

It has degree five and integer coefficients. This is a transgression of
the stated quadratic cochain, not the complete bosonic stacking phase.
Its name records that role. There are **ten ordinary cup terms** after
distributing sums of input carries; expanding
$`\Delta B_4=d\lambda_3-n'_2n_2`$ gives fourteen terms.

The complete variation law is

<a id="quadratic-variation"></a>

{{equation:quadratic-refinements--degree-four-variation-on-the-physical-lower-tower--8}}

This is exact over the integers. The bracket multiplying two contains
ten cups plus $`s_1\mathcal{ℰ}^{\mathcal Q}_5`$; substituting the latter's
complete definition gives twenty cups. The final line and the preceding
line together contain three terms. This separates the derivative of the
stacking transgression, its half-valued correction, and the remaining
integer/background contribution before any binary-lift expansion.

## An integer lift compatible with the polarization

The integer transgression provides an explicit lift of the current
binary quarter correction:

<a id="compatible-quarter-lift"></a>

{{equation:quadratic-refinements--an-integer-lift-compatible-with-the-polarization--9}}

The equality is literal binary reduction of the integer expression,
using the existing definitions of $`B_4,\lambda_3,\Delta B_4`$.
There are thirteen outer terms after the ten-term transgression is
substituted, with **seven binary terms inside the protected whole lift**.
The two mixed cups outside that lift are ordinary integer products.

## Changing the lift in the terminal product

The displayed lift can be used in a coupled change of the terminal
stacking representative. More generally, the following identity holds
for any explicitly chosen integer lift of the existing binary
$`\mathcal V_5`$ in the [terminal formula](TERMINAL_TRANSFER.md#eq-k3).
Define its integral
lift difference

{{equation:quadratic-refinements--changing-the-lift-in-the-terminal-product--10}}

Suppose the existing normalized contraction is written
$`Z_5=(\mathsf h^{\rm tw})^*\rho_6+(\mathrm{AW}^{\rm tw})^*L_5`$, with
$`dL_5=(\mathsf{sh}^{\rm tw})^*\rho_6`$. The superscript labels the
twisted contraction, not a stacking input. It is the fully specified contraction
of the terminal appendix. The lift change must transport **both** data:

{{equation:quadratic-refinements--changing-the-lift-in-the-terminal-product--11}}

Replacing $`\overline{\mathcal V_5}/4+Z_5/2`$ by
$`V_5^{\mathbb Z}/4+Z_5^{\rm new}/2`$ then gives exactly

<a id="paired-lift-transport"></a>

{{equation:quadratic-refinements--changing-the-lift-in-the-terminal-product--12}}

The source and lower multiplication laws stay in the same representative.
The inverse subtracts this output coboundary. The homotopy here is an
explicit equivalence witness; choosing a different quarter lift without
the displayed binary and tensor transports is not this identity.

## Algebraic proof of the variation

For untwisted integer four-cochains $`x,y`$, an integer three-cochain
$`r`$, and an integer two-cochain $`w`$, put $`z=dr+y`$ in this proof.
The signed cup differential identity gives

{{equation:quadratic-refinements--algebraic-proof-of-the-variation--13}}

This holds without closure hypotheses. Apply its $`r=0`$ case to
$`B_4+B'_4`$, and then apply it with
$`x=B_4+B'_4`$, $`r=\lambda_3`$, $`y=-n'_2n_2`$.
Use $`d\omega_2=2\beta\omega_2`$ and
$`d=d_{s_1}+2s_1\cup`$. The result is precisely the variation above.
All canonical lift boundaries are preserved throughout.
