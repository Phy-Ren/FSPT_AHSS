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

{{equation:four-dimensional--4-1d--1}}

<a id="obstructions-4d"></a>
## Obstruction functions

### 1. p+ip obstruction

<a id="eq-integer-4d"></a>

{{equation:four-dimensional--1-p-ip-obstruction--2}}

### 2. Majorana obstruction

<a id="eq-l1-4d"></a>

{{equation:four-dimensional--2-majorana-obstruction--3}}

**p+ip contribution.**

{{equation:four-dimensional--2-majorana-obstruction--4}}

Equivalently, in the shifted Majorana coordinate,

{{equation:four-dimensional--2-majorana-obstruction--5}}

### 3. Complex-fermion obstruction

<a id="eq-l2-4d"></a>

{{equation:four-dimensional--3-complex-fermion-obstruction--6}}

**Majorana contribution.**

{{equation:four-dimensional--3-complex-fermion-obstruction--7}}

**Mixed Majorana–p+ip contribution.**

{{equation:four-dimensional--3-complex-fermion-obstruction--8}}

Here $`d\check n_3`$ is fixed by the preceding obstruction.

**p+ip contribution.**

<a id="eq-l4"></a>

{{equation:four-dimensional--3-complex-fermion-obstruction--9}}

The second digit obeys $`d\widetilde n_2=\bar n_2\cup_1\bar n_2+s_1\bar n_2`$.

The [physical pairing comparison](FOUR_DIMENSIONAL_GEOMETRIC_REFERENCE.md)
gives the complete F-move count, its explicit local reference, and the
paired stacking comparison while retaining the original ordinary Majorana
graph.

### 4. Bosonic obstruction

<a id="eq-t4"></a>
<a id="shared-terminal-source"></a>
<a id="four-dimensional-pair"></a>

{{equation:four-dimensional--4-bosonic-obstruction--10}}

In the current phase coordinate the contributions are:

**Complex-fermion contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--11}}

**Complex-fermion–Majorana contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--12}}

The bracket reuses the complete Majorana parity from the preceding layer:
$`\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}=\mathrm{Sq}^2\check n_3
+\omega_2\check n_3+s_1\mathrm{Sq}^1\check n_3`$.
Its mixed component retains the terms proportional to $`d\check n_3`$;
no closed-input assumption is made. The outer superscript records the
exchanged fermion operators. Reusing their full parity does not change
that physical origin.

**Complex-fermion–p+ip contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--13}}

These terms use the paired operator phase
$`\widehat\nu_5^{\rm op}=\widehat\nu_5^{\rm raw}
+\tfrac12n_4\cup_4dn_4`$, followed by the fixed
[Majorana phase change](FOUR_DIMENSIONAL_MAJORANA_PHASE.md).
Both changes are included in the terminal stacking law. The lower fields
are unchanged. This convention retains the compact intrinsic Majorana
formula and places its differential-dependent continuation in the mixed
contribution.

**Majorana contribution.**

<a id="majorana-phase-4d"></a>

{{equation:four-dimensional--4-bosonic-obstruction--14}}

The formula is defined for arbitrary $`\check n_3`$ through the open
integer carry $`\beta^\circ`$. It does not impose
$`d\check n_3=0`$. The intrinsic polynomial and the two Cartan operations
are

{{equation:four-dimensional-majorana-phase--intrinsic--1}}

The intrinsic polynomial contains **four MS terms** and one product of
the defined first squares.

{{equation:four-dimensional-majorana-phase--cartan--2}}

Each Cartan operation contains **one MS term**. The carry numerator
$`\beta^\circ\check n_3+\overline{\beta^\circ\check n_3}`$ is even,
including for negative integer values. When the integer decoration is
zero, $`\check n_3=n_3`$ and $`\beta^\circ n_3=\beta n_3`$; this same
formula is the compact closed-Majorana expression.

**Majorana–p+ip contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--15}}

This finite sum contains **1,897 specified MS terms** with the defined
Majorana differential retained as an input. Every word and its arguments
are given in the [relative coefficient table](FOUR_DIMENSIONAL_MAJORANA_RELATIVE_WORD_COEFFICIENTS.md).
The complete finite sum vanishes on $`d\check n_3=0`$; this need not hold
word by word. The [phase construction](FOUR_DIMENSIONAL_MAJORANA_PHASE.md)
derives this relative continuation and transports the stacking law with
it. The other displayed half-valued cups are outside the sum. The mixed
quarter phase contains the four-cup quadratic polarization and **three
additional ordered integer cups**. The binary cochain $`d\check n_3`$
is lifted as a whole in the last two cups.


**p+ip contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--16}}

The quadratic cochain is defined once in the
[common notation](../FORMULA_GUIDE.md#integral-quadratic-cochain).
The mixed quarter phase reuses its exact addition polarization, which
expands to four ordered cups with no background remainder. Here
$`B_4=\beta^\circ\check n_3+B_4^\psi`$ is ordinary integer addition.
The explicit $`s_1\mathcal{𝒪}_5^\psi/2`$ is required by the same phase
change that fixes the compact Majorana formula; it does not redefine
the fixed binary completion $`y_6`$.

The polynomial $`y_6`$ contains **623,880 explicit physical-face monomials**
after its complete finite definition is expanded and equal binary
monomials are collected. The [complete physical coefficient table](FOUR_DIMENSIONAL_Y6_FACES.md)
specifies every monomial. It is not counted as one term. The remaining
displayed rational terms are additional.

**Cochains appearing in these contributions.**

<a id="eq-s1"></a>
<a id="eq-s2"></a>
<a id="eq-s3"></a>

{{equation:four-dimensional--4-bosonic-obstruction--17}}

The fixed quadratic background cochain is:

{{equation:four-dimensional--4-bosonic-obstruction--18}}

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

{{equation:four-dimensional--1-p-ip-stacking--19}}

### 2. Majorana stacking

<a id="eq-p2-4d"></a>

{{equation:four-dimensional--2-majorana-stacking--20}}

**p+ip contribution.**

{{equation:four-dimensional--2-majorana-stacking--21}}

The same product in the shifted coordinate is

{{equation:four-dimensional--2-majorana-stacking--22}}

Its integer digit carry is

{{equation:four-dimensional--2-majorana-stacking--23}}

Consequently $`d\check{\mathcal{ℰ}}_3=\bar n_2\bar n'_2+\bar n'_2\bar n_2`$.

### 3. Complex-fermion stacking

<a id="eq-p4"></a>

{{equation:four-dimensional--3-complex-fermion-stacking--24}}

**Majorana contribution.**

{{equation:four-dimensional--3-complex-fermion-stacking--25}}

**Mixed Majorana–p+ip contribution.**

{{equation:four-dimensional--3-complex-fermion-stacking--26}}

**p+ip contribution.**

{{equation:four-dimensional--3-complex-fermion-stacking--27}}

The two finite polynomials in this contribution are

<a id="eq-p5"></a>

{{equation:four-dimensional--3-complex-fermion-stacking--28}}

### 4. Bosonic stacking

<a id="eq-t4c"></a>
<a id="eq-t4d"></a>

{{equation:four-dimensional--4-bosonic-stacking--29}}

The output fields are those of the preceding three stacking laws. The
following formulas use the operator ordering of the complex-fermion
contribution. The terminal phase is the same compact-Majorana coordinate as the obstruction above.
The cochain $`R_5[\check n_3,n_4]`$ is defined once in the
[paired phase change](FOUR_DIMENSIONAL_MAJORANA_PHASE.md); its backgrounds
are kept fixed in every evaluation below. Setting its second argument
to zero removes only the term $`s_1n_4/2`$.

#### Complex fermions

{{equation:four-dimensional--complex-fermions--30}}

#### Complex fermions and Majorana decoration

{{equation:four-dimensional--complex-fermions-and-majorana-decoration--31}}

The $`\Delta`$ has its defined three terms: the value at $`(N_4,\check N_3)`$ minus the values at $`(n_4,\check n_3)`$ and $`(n'_4,\check n'_3)`$. It uses the actual stacked fields, including their p+ip carries. All three parity brackets retain the cochain differential terms. This is an exact rewriting of the same contribution.

#### Complex fermions and p+ip decoration

{{equation:four-dimensional--complex-fermions-and-p-ip-decoration--32}}

#### Majorana decoration

On an ordered five-simplex, the complete Majorana contribution is

{{equation:four-dimensional--majorana-decoration--33}}

Every unindexed cochain on the right is evaluated on the same simplex
$`012345`$. The face products are ordinary products of the indicated values.
The integer carries are

{{equation:four-dimensional--majorana-decoration--34}}

The two $`\lambda`$ cochains are the same binary-addition carry, applied
to the Majorana inputs and to their lower differentials, respectively.
For any pair of binary degree-$`k`$ cochains, that carry is the integer
cochain $`-x\cup_kx'`$: the canonical integer value of their binary sum
is $`x+x'-2(x\cup_kx')`$. Thus $`\lambda_4^\gamma`$ introduces no new
polynomial or choice. Its factors are the **canonical binary
differentials**, not the integer differentials of the lifted fields.

The compatibility of the two carries is

{{equation:four-dimensional--majorana-decoration--35}}

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
terms before the compact-phase transport**. The four lift interiors contain **146 explicit products**.
Counting those products in place of the four lift wrappers gives
**624 explicit term occurrences before that transport**, with all four reduction boundaries
retained. This replaces the previous 6,176-term expansion. Defined lower
differentials, Bocksteins, and binary-addition carries remain structured
arguments; $`d`$ denotes the cochain differential.

The three displayed $`R_5`$ evaluations and the term
$`-s_1\mathcal{ℰ}_4^\gamma/2`$ transport this expression to the same
phase coordinate as the compact pure Majorana obstruction. Each
$`R_5[x,0]`$ has **44 half-valued terms and one quarter-valued term**;
the complete 32-word sum and the remaining terms are written in the
[phase-change definition](FOUR_DIMENSIONAL_MAJORANA_PHASE.md).
The inputs $`\check n_3+\check n'_3`$ are binary sums, including inside
all integer carries. These evaluations are not counted as single MS terms.

The existing [output-gauge relation](FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md)
precedes this terminal coordinate change and is retained in it. The
[integer-carry derivation](FOUR_DIMENSIONAL_MAJORANA_CARRY_REDUCTION.md)
explains the unchanged coefficient part. Its replay verifies that part;
the additional paired phase change is proved separately.

#### Majorana and p+ip decoration

{{equation:four-dimensional--majorana-and-p-ip-decoration--36}}

This finite sum contains **5,684,189 explicit terms** with the defined
lower differentials, stacking twisters and integer carries retained.
The [complete coefficient table](FOUR_DIMENSIONAL_STACKING_COEFFICIENTS.md)
specifies every factor and argument. Expanding the remaining displayed
linear sums and the three quarter numerators adds **1,262 terms**, giving
**5,685,451 terms before the displayed compact-phase correction**. Whole nonlinear lifts retain
their scopes; their complete interior terms are recorded separately in
the coefficient table.

The three $`R_5[\cdot,0]`$ evaluations supply the polarization of the
same phase map between $`\check n_3+\check n'_3`$ and
$`\check{\mathcal{ℰ}}_3`$; the additional half term uses the already
defined mixed lower twister. Each evaluation contains 45 explicit
cochain terms before argument expansion and cancellations. In particular
this correction vanishes when the p+ip carry and mixed lower twister vanish.

The three products of the binary numerators retain the carry from the canonical
integer lift of their binary sum. They cannot be dropped when splitting a
quarter-valued contribution into physical parts.

#### p+ip decoration

{{equation:four-dimensional--p-ip-decoration--37}}

This finite sum contains **2,869,198 explicit terms**, including the entire
pure-source and tensor contributions. The
[complete coefficient table](FOUR_DIMENSIONAL_STACKING_COEFFICIENTS.md)
lists them with the same lower-operation convention. The other displayed
terms add **22**, giving **2,869,220 terms before the displayed compact-phase correction**.
The protected whole quarter numerator has 20 interior terms, displayed
below; the other nonlinear interiors are specified in the coefficient table.

The final phase-map evaluation has 45 explicit cochain terms, with
$`\check{\mathcal{ℰ}}_3`$ as its defined input. Together with
$`-s_1\mathcal{ℰ}_4^\psi/2`$, it is the pure-integer part of the same
terminal coordinate change, not a separately chosen p+ip correction.

The final denominator-three term belongs to the integer cubic response.
All displayed integer products use the fixed signed coefficient transports.

<a id="eq-t4a"></a>

#### Carries in the quarter-valued terms

The carry already used in the full product has the exact integral split

{{equation:four-dimensional--carries-in-the-quarter-valued-terms--38}}

The products in these three definitions are integral. Binary factors use their canonical values, and the full bar on the middle line is retained. In the same convention,

{{equation:four-dimensional--carries-in-the-quarter-valued-terms--39}}

The three binary quarter numerators are expanded below. Their sum is the original binary numerator. The identity used above is

{{equation:four-dimensional--carries-in-the-quarter-valued-terms--40}}


<a id="eq-t4b"></a>

The binary quarter numerators are denoted by $`V_5`$ and its physical
contributions below. The calligraphic $`\mathcal V_5`$ denotes the
stacked bosonic phase.

##### Majorana quarter numerator


{{equation:four-dimensional--majorana-quarter-numerator--41}}

Here $`B_4^\gamma=\beta^\circ\check n_3`$ is the Majorana part of the
already defined carry $`B_4=B_4^\gamma+B_4^\psi`$. Primes mean the second
stacking input. The three parts of $`\lambda_3`$ are those defined in the
main stacking formula.

With these defined carries and the standard Steenrod square retained,
this numerator contains **eight terms** after distributing the explicit
linear sums.

##### Majorana–p+ip quarter numerator

{{equation:four-dimensional--majorana-p-ip-quarter-numerator--42}}

The last sum contains the three pairs
$`(i,j)=(\gamma,\gamma\psi),(\gamma,\psi),(\gamma\psi,\psi)`$,
and contains **nine cup terms** with the defined stacking carries
retained. The entire mixed numerator contains **39 terms** at this boundary.
The [exact polarization identity](GENERAL_MIXED_QUARTER_POLARIZATION.md)
reduces the former twelve-term pair sum to these nine terms without
changing its binary value or whole lift. The differentials remain present;
no output coboundary is discarded. The archived 55-term substitution
count refers to the preceding twelve-term expression and its stated
protected-quotient convention.

##### p+ip quarter numerator

{{equation:four-dimensional--p-ip-quarter-numerator--43}}

The p+ip numerator contains **20 terms** with the defined lower carries
and standard operations retained. A canonical lift of a whole numerator
retains its scope: the mixed and pure lifts have respectively 39 and 20
terms inside them, and cannot be replaced by sums of individual lifts.

Their sum is exactly the original binary numerator
$`V_5=V_5^\gamma+V_5^{\gamma\psi}
+V_5^\psi`$. Splitting its canonical integer lift produces the
three half-valued carry terms already included in
$`\widehat{\mathcal{ℰ}}_5^{\gamma\psi}`$.

The [paired phase map](FOUR_DIMENSIONAL_MAJORANA_PHASE.md) is applied to
both the obstruction and the stacking law. To check the sum of its three
physical contributions, use the actual lower output
$`\check N_3=\check n_3+\check n'_3+\check{\mathcal{ℰ}}_3`$ and
$`N_4=n_4+n'_4+\mathcal{ℰ}_4`$. The displayed corrections sum exactly to
$`-R_5[\check N_3,N_4]+R_5[\check n_3,n_4]+R_5[\check n'_3,n'_4]`$.
The lower twisters, finite coefficient sets, and existing output coboundary
are unchanged; the full terminal formula uses this one transported phase.
