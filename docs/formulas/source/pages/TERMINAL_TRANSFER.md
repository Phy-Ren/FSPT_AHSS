# Finite binary transfer in the 4+1D product

This appendix retains the construction of the binary five-cochain $`Z_5`$ in the supplied 4+1D product. Its complete physical-face expansion and three physical parts are now given in the [coefficient appendix](FOUR_DIMENSIONAL_BINARY_COEFFICIENTS.md). The [current full stacking formula](FOUR_DIMENSIONAL.md#eq-t4c) also applies the paired complex-fermion phase map stated in [Representatives](REPRESENTATIVES.md#operator-phase-4d). The inputs are
$`(n_2,\check n_3)`$ and $`(n'_2,\check n'_3)`$, with common backgrounds
$`\omega_2,s_1`$. Primes always label the second stacking input; $`N_2,\check
N_3`$ are the output. Bars, tildes, and checks have the same meanings as in the guide. In integer
arithmetic each binary field supplies its canonical value $`0,1`$; a whole
composite binary expression is reduced first whenever a bar surrounds it.

The full formula comes first; its kernel, coordinates, and coefficients
are then defined explicitly:

| Operation | Degree and role | Definition |
|---|---|---|
| $`\rho_6`$ | Binary degree-six transfer kernel | (K3) |
| $`L^s_5,L^0_5,L_5`$ | Binary degree-five tensor coefficients, separated by background degree | (K6), (K9), (K11) |
| $`P_i^{L},P_i^{R}`$ | Binary tetrahedral polynomials | (K8) |
| $`D^0_5`$ | Binary reduction of the complete zero-background integer carry | (K10) |
| $`Z_5`$ | Binary degree-five finite transfer | (K12) |

The lower correction $`\mathcal{ℰ}_4`$, its shifted predecessor
$`\check{\mathcal{ℰ}}_3=\bar n_2\cup_1\bar n'_2`$, the carry $`B_4`$,
$`\lambda_3`$, and $`\Delta B_4=d\lambda_3-n'_2n_2`$ are already defined in
the guide. For any one-input expression the signed difference is
$`\Delta X=X[N_2,\check N_3]-X[n_2,\check n_3]-X[n'_2,\check n'_3]`$.
As elsewhere, $`B'_4=B_4[n'_2,\check n'_3]`$ and an unlabelled $`B_4`$ refers
to the first input. All products remain ordered.

<a id="transfer"></a>
## Finite formula for the stacking correction

Encode the physical input as the graded five-simplex $`S`$ specified below.
The binary five-cochain in the terminal stacking correction is

<a id="eq-k12"></a>

**(K12)**

{{equation:terminal-transfer--finite-formula-for-the-stacking-correction--1}}

Evaluation on a binary chain means the sum over its normalized simplices.
Cancel equal simplices before evaluating the source. The bound $`j\le5`$
is finite: each nonzero $`\delta\mathsf h^{(3)}`$ lowers the background
skeletal filtration, whose degree here is at most five. All face rules,
grids, polynomials, and division operations used in (K12) are specified
below; no group-dependent primitive solver is needed.

## Grid evaluation

Let $`\mathsf h^{(3)}`$ denote the three-factor grid homotopy, whose component
in degree $`D`$ is $`\mathsf h_D^{(3)}`$ from (O11). Order its factors as
$`(\text{common background},\text{first input},\text{second input})`$.
For grid vertices $`(r_i,t_i,v_i)`$, pull both $`s_1,\omega_2`$ along $`r`$,
the complete graded pair $`(n_2^{\rm gr},\check n_3^{\rm gr})`$ along $`t`$,
and $`(n_2^{{\rm gr}\prime},\check n_3^{{\rm gr}\prime})`$ along $`v`$.
After pulling back, decode (K4) before evaluating $`\rho_6`$.

## The binary kernel

The kernel is given directly below, without separate names for its
single-input and even-integer pieces. All terms before the final braces are binary. The $`\Delta`$
acts on the entire following binary bracket. The final braces form one
integer numerator; it is pointwise even, and is divided by two before the
final reduction modulo two. The binary source values
$`\mathcal{𝒪}_5[n_2,\check n_3]`$ are the complex-fermion obstruction of the
guide, not additional input fields.

<a id="eq-k1"></a>
<a id="eq-k2"></a>
<a id="eq-k3"></a>

**(K1–K3)**

{{equation:terminal-transfer--the-binary-kernel--2}}

The repeated integer quadratic expression is the same
[quadratic cochain](QUADRATIC_REFINEMENTS.md#quadratic-cochain) as in the
obstruction. Its exact [stacking variation](QUADRATIC_REFINEMENTS.md#quadratic-variation)
exhibits the differential and ordinary-cup corrections before any lift is
expanded. This rewriting leaves the kernel and its coefficient tables unchanged.

Every derivative differentiates a specified expression. In the binary
part, $`d\overline{B_4}=\overline{\beta_{s_1}\check\omega_2}\bar n_2`$ and
$`d\check{\mathcal{ℰ}}_3=\bar n_2\bar n'_2+\bar n'_2\bar n_2`$.
Inside the final integer braces, $`d_{s_1}\mathcal V_5`$ differentiates the
canonical integer representative of that binary five-cochain. Every quantity inside $`\Delta`$ is re-evaluated on the output and on both
inputs, including $`B_4^\psi,\mathcal{𝒪}^\psi_5,T_6,y_6`$. The bar on
the polynomial following the minus sign is taken **before** its signed
stacking difference. The free complex-fermion solutions $`n_4,n'_4`$ do not
enter this kernel.

## Shared-background coordinates

Use $`D`$ only for the degree of a simplex in this appendix. A graded
simplex consists of the common backgrounds and two graded inputs:

{{equation:terminal-transfer--shared-background-coordinates--3}}

The superscript $`{\rm gr}`$ denotes the untwisted coordinates relative to
the simplex's first vertex. It does not change the cochain degree. Decode
the first input by

<a id="eq-k4"></a>

**(K4)**

{{equation:terminal-transfer--shared-background-coordinates--4}}

Apply the same rule to the primed input and take $`s_1(00)=0`$. Encoding is
the inverse of (K4). Positive faces and degeneracies are factorwise. The
actual zeroth face is obtained by decoding, restricting to
$`[1,\ldots,D]`$, and re-encoding with vertex $`1`$ as root. Relative to the
factorwise zeroth face its changes are

<a id="eq-k5"></a>

**(K5)**

{{equation:terminal-transfer--shared-background-coordinates--5}}

These formulas apply for $`1\le i\lt j\lt k\lt l\le D`$ and to the primed
input as well. Let $`\delta S`$ be the binary sum of the actual and
factorwise zeroth faces, extended linearly to binary chains. The root in
(K4) is a coordinate choice on each simplex, not a global trivialization of
either background; its failure on the zeroth face is precisely (K5).

## The tensor coefficient

The complete binary coefficient is

<a id="eq-k11"></a>

**(K11)**

{{equation:terminal-transfer--the-tensor-coefficient--6}}

This notation is a finite rule: for $`(p,q)=(2,3)`$ and $`(3,2)`$, use the
front $`p`$-face and back $`q`$-face of a five-simplex, sharing vertex $`p`$.
Enumerate the ten paths from $`(0,p)`$ to $`(p,5)`$. Pull the two complete
zero-background inputs along coordinates one and two, evaluate $`D^0_5`$,
and sum modulo two. Together with $`L^0_5`$, these are the
background-degree-zero terms. The contribution $`L^s_5`$ in (K6) uses the
background-degree-one component. These prescriptions define $`L_5`$ on
every simplex in (K12).


### Background-degree-one contribution

The background-degree-one contribution $`L^s_5`$ uses $`\bar x`$ and
$`\widetilde x`$. Where the third binary digit is needed, it is written
explicitly as $`\overline{\lfloor x/4\rfloor}`$:

<a id="eq-k6"></a>

**(K6)**

{{equation:terminal-transfer--background-degree-one-contribution--7}}

These are graded integer values. Equivalently, the same scalar polynomial
can be written directly in integer binomials:

<a id="eq-k7"></a>

**(K7)**

{{equation:terminal-transfer--background-degree-one-contribution--8}}

### Background-degree-zero contribution

The ordered-cup polynomial is

<a id="eq-k9"></a>

**(K9)**

{{equation:terminal-transfer--background-degree-zero-contribution--9}}

Its tetrahedral polynomials are defined on one input at a time.

For one zero-background input $`(n_2,\check n_3)`$ on $`0123`$, define three
local integer face coordinates:

{{equation:terminal-transfer--background-degree-zero-contribution--10}}

The indices after the semicolon specify the face or difference of faces.
Applying the same bar and tilde rules gives all bits needed below.
Products in (K8) are ordinary products of bits on this tetrahedron, and
$`\check n_3(0123)`$ is the binary Majorana value on the same face:

<a id="eq-k8"></a>

**(K8)**

{{equation:terminal-transfer--background-degree-zero-contribution--11}}

Rows referenced on the right use the same input and face. In particular,
$`\widetilde n_{2;013-012}`$ is the second bit of the integer
difference; it is not the sum of the second bits of $`n_2(013)`$ and
$`n_2(012)`$.

### The balanced integer carry

Only in this subsection set $`\omega_2=s_1=0`$, so
$`dn_2=dn'_2=0`$, $`d\check n_3=\bar n_2^2`$, and
$`d\check n'_3=(\bar n'_2)^2`$. Evaluate the guide's
$`B_4,B'_4,\Delta B_4,\lambda_3`$ at these backgrounds. Form

<a id="eq-k10"></a>

**(K10)**

{{equation:terminal-transfer--the-balanced-integer-carry--12}}

The only additional face operation in this expression is the integral
polynomial

{{equation:terminal-transfer--the-balanced-integer-carry--13}}

$`\mathcal V_{5,0}`$ is the binary polynomial (T4b) at
$`\omega_2=s_1=0`$, supplying its canonical value $`0,1`$ to the integer
numerator. The same rule applies to each barred expression. In particular,
$`d`$ in the fourth line is the **integer** differential after reduction
of the expression it acts on. The stacking differences are also taken over
the integers. Assemble the complete numerator, which is pointwise even,
then divide by two and take parity. No reduction of a rational phase
modulo one is performed before these operations.
