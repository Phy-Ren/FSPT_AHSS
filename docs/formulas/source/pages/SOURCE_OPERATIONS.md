# Finite cochain formulas for the bosonic obstruction

The two degree-six cochains used in the 4+1D source are defined here. The ordinary Majorana word coefficients are also printed in the [physical coefficient table](FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md), with their pure and mixed source parts separated. This file retains the construction and the complete pure p+ip coefficient rule.

The backgrounds are $`\omega_2,s_1`$. A bar takes parity and a tilde takes
the second binary digit, as in [Operations](OPERATIONS.md). In integer
arithmetic a binary field means its canonical value $`0,1`$. A bar around
a composite expression means: form that entire binary expression first,
then use its value $`0,1`$. In particular it cannot be replaced by the
unreduced sum of its integer-valued terms. The coefficient transports are
fixed in [Operations](OPERATIONS.md).

The shifted background is $`\check\omega_2=\omega_2+s_1\cup s_1`$ and the
closed degree-four source is
$`\check{\mathcal{𝒪}}_4=\bar n_2^2+\check\omega_2\bar n_2`$.
The source $`\mathcal{𝒪}^\psi_5`$, the residual $`B_4^\psi`$, and the
Pontryagin-square representative $`\mathcal P_{s_1}`$ have the definitions
in the guide. The Bocksteins $`\beta,\beta_{s_1},\beta^+`$ and finite cup
operations have the definitions in [Operations](OPERATIONS.md).

The two required formulas and their constituent polynomials are:

| Operation | Purpose | Definition |
|---|---|---|
| $`T_6`$ | Degree-six formula on an open three-cochain | (S5) |
| $`y_6`$ | Integer-layer completion by the fixed grid and coefficient sums | (S7)–(S8) |
| $`M_7`$ | Binary degree-seven operation on a closed four-cochain, shared by the two constructions | (S4) |
| $`R_7`$ | The binary remainder evaluated on the three-factor grids | (S6) |

## Continuation to an open degree-three cochain

For a binary three-cochain $`z`$, the required degree-six formula is

<a id="eq-s5"></a>

**(S5)**

{{equation:source-operations--continuation-to-an-open-degree-three-cochain--1}}

Here $`(\mathrm{Sq}^2+\omega_2\cup)x`$ means
$`\mathrm{Sq}^2x+\omega_2\cup x`$. The integration is the seven-path binary
sum (O8). The input to the Bockstein inside $`M_7`$ is the **closed**
four-cochain $`dz^J`$, not the open three-cochain $`z`$.

Use the height interval $`J=[0,1]`$ and define the cochain in (S5) by

{{equation:source-operations--continuation-to-an-open-degree-three-cochain--2}}

Backgrounds are pulled from the base. The expression
$`\mathrm{Sq}^2z^J+s_1\mathrm{Sq}^1z^J+\omega_2z^J`$ is binary of degree
five. The remaining degree-seven polynomial in (S5) is given next.

## Closed degree-four polynomial

For a closed binary four-cochain $`z`$, define

<a id="eq-s4"></a>

**(S4)**

{{equation:source-operations--closed-degree-four-polynomial--3}}

All **453 words** of $`\mathcal W_4`$ are printed in
[Coefficients](COEFFICIENTS.md#adem-words). The subscript of the word set $`\mathcal W_4`$ is the input degree. No coefficient is fitted or chosen during evaluation.

<a id="source-completion"></a>
## Integer-layer contribution

For a twisted integer two-cocycle $`n_2`$, the degree-six formula is

<a id="eq-s7"></a>

**(S7)**

{{equation:source-operations--integer-layer-contribution--4}}

Its binary remainder is specified by the following expression. No
Majorana or complex-fermion decoration is chosen here. Assemble the
**entire integer numerator**, divide by eight, and then take parity.

<a id="eq-s6"></a>

**(S6)**

{{equation:source-operations--integer-layer-contribution--5}}

The numerator is pointwise divisible by eight. All operations inside the
outer braces are integer operations, including the differential on the
square bracket. Each barred subexpression supplies its canonical binary
value before that integer assembly. In particular no fraction is reduced
modulo one partway through the calculation. The ordinary Bockstein of
$`\check{\mathcal{𝒪}}_4`$ is defined because that source is closed.

For the first term use the three-factor grid (O11), ordered
$`(s_1,n_2,\omega_2)`$. On grid vertices $`(r_i,t_i,v_i)`$, pull $`s_1`$ along
$`r`$ and $`\omega_2`$ along $`v`$. Pull the integer field along $`t`$ with
first-vertex transport:

<a id="eq-s8"></a>

**(S8)**

{{equation:source-operations--integer-layer-contribution--6}}

Evaluate the entire expression (S6) on each pulled-back input and sum over
$`\mathsf h^{(3)}_6`$. This defines $`(\mathsf h^{(3)}_6)^*R_7`$.

The second term is the finite numerical polynomial specified in
[Coefficients](COEFFICIENTS.md#numerical-polynomial). It has eleven
tridegrees, uses explicit generalized integer binomials and first-vertex
transport, and contains no implicit primitive. That appendix prints every
coefficient, together with a lossless machine-readable copy.

The three-factor formulas here and in the terminal stacking correction
assign fields differently to the same grid. Here $`s_1`$ and $`\omega_2`$
occupy separate factors; in the terminal product they share one background
factor. These assignments fix the coefficient transports.
