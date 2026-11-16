<a id="four-dimensional"></a>
# 4+1D

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates). Every physical field and layer below belongs to this dimension.

Throughout this section the physical fields are:

| Field | Physical role | Coefficients |
|---|---|---|
| $`n_2`$ | p+ip decoration | $`\mathbb Z_{s_1}`$ |
| $`n_3`$ | Majorana decoration | $`\mathbb Z_2`$ |
| $`n_4`$ | Complex-fermion decoration (physical point-fermion occupation) | $`\mathbb Z_2`$ |
| $`\nu_5`$ | Bosonic phase | $`U(1)_{s_1}`$ |

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

### 3. Complex-fermion obstruction

<a id="eq-l2-4d"></a>

{{equation:four-dimensional--3-complex-fermion-obstruction--6}}

**Majorana contribution.**

{{equation:four-dimensional--3-complex-fermion-obstruction--7}}

**Mixed Majorana–p+ip contribution.**

{{equation:four-dimensional--3-complex-fermion-obstruction--8}}

Here $`dn_3`$ is fixed by the preceding obstruction.

**p+ip contribution.**

<a id="eq-l4"></a>

{{equation:four-dimensional--3-complex-fermion-obstruction--9}}

The second digit obeys $`d[\lfloor n_2/2\rfloor]_2=[n_2]_2\cup_1[n_2]_2+s_1[n_2]_2`$.

<a id="terminal-occupation-4d"></a>

Here $`n_4`$ is the physical point-fermion occupation of the original
pairing arrows. The directed F-move count differs from $`\mathcal{𝒪}_5`$ by
the coboundary of the fixed binary four-cochain $`B_4`$ given explicitly in
the [physical pairing comparison](FOUR_DIMENSIONAL_GEOMETRIC_REFERENCE.md#eq-r4).
That page also gives the complete F-move and P-move counts.
For $`n_2=0`$ every $`s_1`$ face term of $`B_4`$ vanishes and
$`B_4=n_3\cup_2n_3`$.

### 4. Bosonic obstruction

<a id="eq-t4"></a>
<a id="shared-terminal-source"></a>
<a id="four-dimensional-pair"></a>

{{equation:four-dimensional--4-bosonic-obstruction--10}}

The contributions are:

**Complex-fermion contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--11}}

**Complex-fermion–Majorana contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--12}}

The bracket reuses the complete Majorana parity from the preceding layer:
$`\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}=\mathrm{Sq}^2n_3
+\omega_2n_3+s_1\mathrm{Sq}^1n_3`$.
Its mixed component retains the terms proportional to $`dn_3`$;
no closed-input assumption is made. The outer superscript records the
exchanged fermion operators. Reusing their full parity does not change
that physical origin.

**Complex-fermion–p+ip contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--13}}

The terms with $`B_4`$ vanish for $`n_2=0`$, where $`B_4=n_3\cup_2n_3`$
and $`dB_4=0`$. The complex fermions are in operator order, and the
Majorana contribution is in the [compact phase convention](FOUR_DIMENSIONAL_MAJORANA_PHASE.md).

**Majorana contribution.**

<a id="majorana-phase-4d"></a>

{{equation:four-dimensional--4-bosonic-obstruction--14}}

The formula is defined for arbitrary $`n_3`$ through the open
integer carry $`\beta^-`$. It does not impose
$`dn_3=0`$. The intrinsic polynomial and the two Cartan operations
are

{{equation:four-dimensional-majorana-phase--intrinsic--1}}

The intrinsic polynomial contains **four MS terms** and one product of
the defined first squares.

{{equation:four-dimensional-majorana-phase--cartan--2}}

Each Cartan operation contains **one MS term**. The carry numerator
$`\beta^-n_3+[\beta^-n_3]_2`$ is even,
including for negative integer values. When the integer decoration is
zero, $`dn_3=0`$, $`\beta^- n_3=\beta n_3`$, and this is the
[closed-Majorana formula](MAJORANA_AND_ENDPOINTS.md#eq-m4-4d).

**Majorana–p+ip contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--15}}

This finite sum contains **1,897 specified MS terms** with the defined
Majorana differential retained as an input. Every word and its arguments
are given in the [relative coefficient table](FOUR_DIMENSIONAL_MAJORANA_RELATIVE_WORD_COEFFICIENTS.md).
The complete finite sum vanishes on $`dn_3=0`$; this need not hold
word by word. The [phase convention page](FOUR_DIMENSIONAL_MAJORANA_PHASE.md)
derives this relative continuation. The other displayed half-valued cups are outside the sum. The mixed
quarter phase contains the four-cup quadratic polarization and **three
additional ordered integer cups**. The binary cochain $`dn_3`$
is lifted as a whole in the last two cups.


**p+ip contribution.**

{{equation:four-dimensional--4-bosonic-obstruction--16}}

The quadratic cochain is defined once in the
[common notation](../FORMULA_GUIDE.md#integral-quadratic-cochain).
The mixed quarter phase reuses its exact addition polarization, which
expands to four ordered cups with no background remainder. Here
$`\beta_4=\beta^-n_3+\beta_4^\psi`$ is ordinary integer addition.
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
the whole polynomial enclosed in $`[\cdot]_2`$ is reduced before its integer use. The pure binary cochain $`y_6`$ has a [complete finite source definition](SOURCE_OPERATIONS.md#source-completion),
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

Consequently $`d\mathcal{ℰ}_3=[n_2]_2[n'_2]_2+[n'_2]_2[n_2]_2`$.

### 3. Complex-fermion stacking

<a id="eq-p4"></a>

{{equation:four-dimensional--3-complex-fermion-stacking--24}}

Here $`\Delta B_4=B_4[N_2,N_3]-B_4[n_2,n_3]-B_4[n'_2,n'_3]`$, evaluated on the
actual lower fields of the stacked state. The law includes the complex-fermion
gauge transformation by the explicit pairing reference of the separate states described under the bosonic
stacking law below.

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

The fields of the stacked state are those of the preceding three stacking laws, and the
phase convention is that of the obstruction above.
The cochain $`B_5[n_3]`$ is defined once in the
[phase convention page](FOUR_DIMENSIONAL_MAJORANA_PHASE.md); its backgrounds
are kept fixed in every evaluation below.

The directed pairing count of the physical P move gives the stacked field
$`N_4`$ plus the coboundary of the pairing reference of the separate states
written out in the [physical pairing comparison](FOUR_DIMENSIONAL_GEOMETRIC_REFERENCE.md#stacking).
That coboundary is not a decoration. The lower law above composes the P move
with the complex-fermion gauge transformation that removes it. If the
uncorrected stacked field $`N_4+dx`$ is used instead, with $`x`$ the written-out
reference of the separate states, add

{{equation:four-dimensional--4-bosonic-stacking--45}}

to $`\mathcal{ℰ}_5`$. For any binary three-cochain $`x`$ this is the primitive of
$`\mathcal{𝒪}_6^c[N_4+dx]-\mathcal{𝒪}_6^c[N_4]`$;
the other contributions do not depend on $`N_4`$.

#### Complex fermions

{{equation:four-dimensional--complex-fermions--30}}

#### Complex fermions and Majorana decoration

{{equation:four-dimensional--complex-fermions-and-majorana-decoration--31}}

The $`\Delta`$ has its defined three terms: the value at $`(N_4,N_2,N_3)`$ minus the values at $`(n_4,n_2,n_3)`$ and $`(n'_4,n'_2,n'_3)`$. It uses the actual stacked fields, including their p+ip carries. All parity brackets retain the cochain differential terms. The terms with $`B_4`$ come from the pairing reference of the complex fermions; $`\mathcal{𝒪}_5$ without a superscript is the complete parity obstruction of the first input.

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
to the Majorana fields of the separate states and to their lower differentials, respectively.
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
terms without the three $`B_5`$ evaluations**. The four lift interiors contain **146 explicit products**.
Counting those products in place of the four lift wrappers gives
**624 explicit term occurrences without them**, with all four reduction boundaries
retained. Defined lower
differentials, Bocksteins, and binary-addition carries remain structured
arguments; $`d`$ denotes the cochain differential.

The three displayed $`B_5`$ evaluations and the term
$`-s_1\mathcal{ℰ}_4^\gamma/2`$ put this expression in the
phase convention of the pure Majorana obstruction. Each
$`B_5[x]`$ has **44 half-valued terms and one quarter-valued term**;
the complete 32-word sum and the remaining terms are written in the
[phase-change definition](FOUR_DIMENSIONAL_MAJORANA_PHASE.md).
The inputs $`n_3+n'_3`$ are binary sums, including inside
all integer carries. These evaluations are not counted as single MS terms.

The [output-gauge relation](FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md)
and the [integer-carry derivation](FOUR_DIMENSIONAL_MAJORANA_CARRY_REDUCTION.md)
explain the coefficient part; the $`B_5`$ terms are checked separately.

#### Majorana and p+ip decoration

{{equation:four-dimensional--majorana-and-p-ip-decoration--36}}

This finite sum contains **5,684,189 explicit terms** with the defined
lower differentials, stacking twisters and integer carries retained.
The [complete coefficient table](FOUR_DIMENSIONAL_STACKING_COEFFICIENTS.md)
specifies every factor and argument. Expanding the remaining displayed
linear sums and the three quarter numerators adds **1,262 terms**, giving
**5,685,451 terms without the three $`B_5`$ evaluations**. Whole nonlinear lifts retain
their scopes; their complete interior terms are recorded separately in
the coefficient table.

The three $`B_5[\cdot]`$ evaluations supply the polarization of
$`B_5`$ between $`n_3+n'_3`$ and
$`\mathcal{ℰ}_3`$; the additional half term uses the already
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
terms add **22**, giving **2,869,220 terms without the $`B_5`$ evaluation**.
The protected whole quarter numerator has 20 interior terms, displayed
below; the other nonlinear interiors are specified in the coefficient table.

The final $`B_5`$ evaluation has 45 explicit cochain terms, with
$`\mathcal{ℰ}_3`$ as its defined input. Together with
$`-s_1\mathcal{ℰ}_4^\psi/2`$, it is the pure-integer part of the $`B_5`$
terms, not a separately chosen p+ip correction.

The final denominator-three term belongs to the integer cubic response.
All displayed integer products use the fixed signed coefficient transports.

<a id="eq-t4a"></a>

#### Carries in the quarter-valued terms

The carry already used in the full product has the exact integral split

{{equation:four-dimensional--carries-in-the-quarter-valued-terms--38}}

The products in these three definitions are integral. Binary factors use their canonical values, and the reduction modulo two of the full expression on the middle line is retained. In the same convention,

{{equation:four-dimensional--carries-in-the-quarter-valued-terms--39}}

The three binary quarter numerators are expanded below. Their sum is the original binary numerator. The identity used above is

{{equation:four-dimensional--carries-in-the-quarter-valued-terms--40}}


<a id="eq-t4b"></a>

The binary quarter numerators are denoted by $`V_5`$ and its physical
contributions below. The calligraphic $`\mathcal V_5`$ denotes the
stacked bosonic phase.

##### Majorana quarter numerator


{{equation:four-dimensional--majorana-quarter-numerator--41}}

Here $`\beta_4^\gamma=\beta^-n_3`$ is the Majorana part of the
already defined carry $`\beta_4=\beta_4^\gamma+\beta_4^\psi`$. Primes mean the lower
state. The three parts of $`\lambda_3`$ are those defined in the
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
The pair sum is written in the nine-term form given by the
[exact polarization identity](GENERAL_MIXED_QUARTER_POLARIZATION.md).
The differentials remain present; no output coboundary is discarded.

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
$`\mathcal{ℰ}_5^{\gamma\psi}`$.

The $`B_5`$ terms of the three physical contributions sum to
$`-B_5[N_3]+B_5[n_3]+B_5[n'_3]`$, evaluated on the actual lower field
$`N_3=n_3+n'_3+\mathcal{ℰ}_3`$ of the stacked state, together with
$`-s_1\mathcal{ℰ}_4/2`$ from the complex-fermion stacking law.
