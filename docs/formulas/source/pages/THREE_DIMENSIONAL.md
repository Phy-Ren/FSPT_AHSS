<a id="three-dimensional"></a>
# 3+1D

Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates). Every physical field and layer below belongs to this dimension.

Throughout this section the physical fields are:

| Field | Physical role | Coefficients |
|---|---|---|
| $`n_1`$ | p+ip decoration | $`\mathbb Z_{s_1}`$ |
| $`n_2`$ | Majorana decoration | $`\mathbb Z_2`$ |
| $`n_3`$ | Complex-fermion decoration | $`\mathbb Z_2`$ |
| $`\nu_4`$ | Bosonic phase | $`U(1)_{s_1}`$ |

The contributions below are grouped in the shifted Majorana coordinate

<a id="eq-c1-3d"></a>

{{equation:three-dimensional--3-1d--1}}

<a id="obstructions-3d"></a>
<a id="lower-sources"></a>
## Obstruction functions

### 1. p+ip obstruction

<a id="eq-integer-3d"></a>

{{equation:three-dimensional--1-p-ip-obstruction--2}}

### 2. Majorana obstruction

<a id="eq-l1"></a>

{{equation:three-dimensional--2-majorana-obstruction--3}}

**p+ip contribution.**

{{equation:three-dimensional--2-majorana-obstruction--4}}

Equivalently, in the shifted Majorana coordinate,

{{equation:three-dimensional--2-majorana-obstruction--5}}

### 3. Complex-fermion obstruction

<a id="eq-l2"></a>

{{equation:three-dimensional--3-complex-fermion-obstruction--6}}

**Majorana contribution.**

{{equation:three-dimensional--3-complex-fermion-obstruction--7}}

**Mixed Majorana–p+ip contribution.**

{{equation:three-dimensional--3-complex-fermion-obstruction--8}}

Here $`d\check n_2=\check\omega_2\bar n_1`$ is fixed by the preceding obstruction.

**p+ip contribution.**

<a id="eq-l3"></a>

{{equation:three-dimensional--3-complex-fermion-obstruction--9}}

The second digit obeys $`d\widetilde n_1=\bar n_1^2+s_1\bar n_1`$.

### 4. Bosonic obstruction

<a id="eq-t3"></a>


{{equation:three-dimensional--4-bosonic-obstruction--10}}

#### Complex fermions

{{equation:three-dimensional--complex-fermions--11}}

#### Complex fermions and Majorana decoration

{{equation:three-dimensional--complex-fermions-and-majorana-decoration--12}}

The bracket reuses the complete Majorana parity from the preceding layer:
$`\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}=\mathrm{Sq}^2\check n_2
+\omega_2\check n_2+s_1\mathrm{Sq}^1\check n_2`$.
Its mixed component retains the terms proportional to $`d\check n_2`$;
no closed-input assumption is made. The outer superscript records the
exchanged fermion operators. Reusing their full parity does not change
that physical origin.

#### Complex fermions and p+ip decoration

{{equation:three-dimensional--complex-fermions-and-p-ip-decoration--13}}

The finite sum contains **25 specified MS terms**, [listed explicitly](THREE_DIMENSIONAL_WORD_INDICES.md#complex-fermion-indices). Every term contains
$`d\check n_2=\check\omega_2\bar n_1`$; this lower source has one cup term.

#### Majorana decoration

{{equation:three-dimensional--majorana-decoration--14}}

Here $`\beta^\circ x=(dx-\overline{dx})/2`$, with the first differential
formed in integers. It agrees with the ordinary Bockstein on a cocycle.
The word operations are

{{equation:three-dimensional--majorana-decoration--15}}

#### Majorana and p+ip decoration

{{equation:three-dimensional--majorana-and-p-ip-decoration--16}}

The sum contains **2,276 ordinary MS terms** after substituting its finite
definitions and collecting equal normalized cochains. This counts the
complete half-valued sum; the quarter-valued terms are separate.

The integer carry and the twisted Bockstein are

{{equation:three-dimensional--majorana-and-p-ip-decoration--17}}

Both divisions are exact. The product $`\check\omega_2n_1`$ has the
local-coefficient transport of its two signed integer factors.
The finite index set $`\mathcal I_5^{\gamma\psi}`$ is defined in the
[coefficient appendix](THREE_DIMENSIONAL_WORD_INDICES.md#final-physical-index-sets).

#### p+ip decoration

<a id="three-dimensional-pip-source"></a>

On the ordered five-simplex $`(012345)`$, the complete contribution is

{{equation:three-dimensional--p-ip-decoration--18}}

The two sums contain **583 ordinary MS terms** and **10,825 physical-face
monomials**, respectively, after their coefficient polynomials are fully
expanded and collected. The latter count includes the background factors;
a coefficient-table row is not counted as a single term.

Every cochain expression without explicit arguments is evaluated on
$`(012345)`$. The [word indices](THREE_DIMENSIONAL_WORD_INDICES.md#final-physical-index-sets)
fix $`\mathcal I_5^\psi`$, and the
[physical-face coefficient table](THREE_DIMENSIONAL_INTEGER_SOURCE_FACES.md#physical-integer-source-coefficients)
prints every pair in $`\mathcal C_5^\psi`$. Its factors involve only the
physical values of $`n_1`$, $`s_1`$, and $`\omega_2`$ on faces of this same
five-simplex. The table is finite and complete; no auxiliary simplex or
lifted-field evaluation is part of this formula.

The Pontryagin-square convention in the last term is

{{equation:three-dimensional--p-ip-decoration--19}}

<a id="stacking-3d"></a>
<a id="lower-stacking"></a>
## Stacking twisters

### 1. p+ip stacking

<a id="eq-p1"></a>

{{equation:majorana-and-endpoints--majorana-stacking--8}}

### 2. Majorana stacking

<a id="eq-p2"></a>

{{equation:three-dimensional--2-majorana-stacking--20}}

**p+ip contribution.**

{{equation:three-dimensional--2-majorana-stacking--21}}

The same product in the shifted coordinate is

{{equation:three-dimensional--2-majorana-stacking--22}}

Its integer digit carry is

{{equation:three-dimensional--2-majorana-stacking--23}}

### 3. Complex-fermion stacking

<a id="eq-p3"></a>

{{equation:three-dimensional--3-complex-fermion-stacking--24}}

**Majorana contribution.**

{{equation:three-dimensional--3-complex-fermion-stacking--25}}

**Mixed Majorana–p+ip contribution.**

{{equation:three-dimensional--3-complex-fermion-stacking--26}}

**p+ip contribution.**

{{equation:three-dimensional--3-complex-fermion-stacking--27}}

The $`\Delta`$ acts on the entire displayed bracket with the p+ip output $`N_1`$.

### 4. Bosonic stacking

<a id="eq-t3b"></a>


{{equation:three-dimensional--4-bosonic-stacking--28}}

For two identical complete states with $`n_1=0`$, the entire correction
reduces to the [ten-term self-stacking formula](THREE_DIMENSIONAL_MAJORANA_SELF_STACKING.md).
It retains the complex-fermion completion and uses the same phase representative.

#### Complex fermions

{{equation:majorana-and-endpoints--complex-fermion-contribution--28}}

#### Complex fermions and Majorana decoration

{{equation:three-dimensional--complex-fermions-and-majorana-decoration--29}}

The $`\Delta`$ has its defined three terms: the value at $`(N_3,\check N_2)`$ minus the values at $`(n_3,\check n_2)`$ and $`(n'_3,\check n'_2)`$. It uses the actual stacked fields, including their p+ip carries. All three parity brackets retain the cochain differential terms. This is an exact rewriting of the same contribution.

#### Complex fermions and p+ip decoration

{{equation:three-dimensional--complex-fermions-and-p-ip-decoration--30}}

The two face brackets contain **13 products** after distributing the
binary parentheses: eight multiply $`dn_3`$ and five multiply $`dn'_3`$.
They replace the former 132-word sum exactly, as proved in the
[exchange reduction](THREE_DIMENSIONAL_CF_EXCHANGE_REDUCTION.md).
The lower Majorana differentials retain their physical meanings.

The former auxiliary eight-word phase polynomial has been eliminated in
favor of the lower obstruction. Its two evaluations give **14 terms**:
two derivatives multiply two retained obstruction evaluations, one output
square, and the four products in the displayed input square. Together with
the two initial lower-operation terms and thirteen face products, this
contribution has **29 terms**. The lower obstruction acts on its whole
binary argument; it must not be linearized.

#### Majorana decoration

{{equation:three-dimensional--majorana-decoration--31}}

The binary completion is

{{equation:three-dimensional--majorana-decoration--32}}

Here $`\mathcal{ℰ}_3^\gamma=\check n_2\cup_1\check n'_2
+s_1(\check n_2\cup_2\check n'_2)`$ and
$`\beta^{\circ+}x=(\beta^\circ x+\overline{\beta^\circ x})/2`$.
Its intrinsic binary polynomial is

{{equation:three-dimensional--majorana-decoration--33}}

The sum over $`\mathcal V_4`$ contains **seven specified MS terms**.
The other displayed terms of $`z_4^0`$ are outside this sum. The complete
$`z_4^0`$ has **20 distributed terms**; the complete $`z_4^\gamma`$ has
**37**, retaining the defined lower twister, integer carries, and whole
lift scopes.

#### Majorana and p+ip decoration

{{equation:three-dimensional--majorana-and-p-ip-decoration--34}}

The MS sum over $`\mathcal I_{4,\neg\psi}`$ contains **15,994 terms**
after exact collection; $`z_4^\gamma`$ is outside that sum. The quarter-valued
quadratic expression uses the total integer carry $`\lambda_2`$ and
subtracts the same expression in $`\lambda_2^\psi`$. These **four terms**
are exact because
$`\lambda_2=\lambda_2^\gamma+\lambda_2^{\gamma\psi}+\lambda_2^\psi`$
is an equality of integer cochains. Expanding this split recovers the
eight ordered pairs other than $`(\psi,\psi)`$, or **16 cup terms**.
Further inserting the three carry definitions gives **24 distributed
integer-cup terms**. These are supplementary expansions; the whole
binary lift in the mixed carry retains its two-term interior and is not
distributed as an integer sum.

The two repeated quarter-valued copies of $`\omega_2\lambda_2^\gamma`$
have been combined in the half-valued bracket. The integer differential of
$`2\lambda_2^\gamma\cup_1\lambda_2^\gamma`$ is likewise half-valued.
These are exact coefficient combinations, with no change of phase
coordinate or reassignment of physical contributions.

This explicitly continued relative phase is zero on the closed-Majorana
physical tower by the proved paired coordinate map. Its half and quarter
brackets need not separately vanish. The integer derivatives and whole
binary lifts displayed here are part of that exact statement. The formula
can be simplified further only while retaining both coefficients and its
paired source map; canceling the binary parity of a quarter term is not
sufficient.

#### p+ip decoration

{{equation:three-dimensional--p-ip-decoration--35}}

The sums contain **6,479 ordinary MS terms** and **4,094 physical-face
monomials**, respectively. These are the expanded sums themselves; the
following quarter- and eighth-valued terms are additional.

##### Physical-face coefficients

On an ordered four-simplex the remaining half-valued term is the following
finite polynomial in the physical integer digits and background faces:

{{equation:three-dimensional--physical-face-coefficients--36}}

This sum contains **4,094 physical-face monomials** after every background
coefficient is multiplied out and identical monomials are collected.
Every pair $`(f,g)`$ is printed in the
[physical-face coefficient table](THREE_DIMENSIONAL_INTEGER_PRODUCT_FACES.md).
Its 173 factored rows group 306 integer-digit monomials by common
background coefficients; neither of those two row counts is the expanded
term count. Each table entry contains
only $`\bar n_1`$, $`\widetilde n_1`$, their primed counterparts, the
explicit third digit $`\overline{\lfloor n_1/4\rfloor}`$, and the
physical faces of $`s_1`$, $`\omega_2`$, and $`\check\omega_2`$.

#### Physical fields, carries, and arithmetic

The lower product and source in these displays are the already fixed laws

{{equation:three-dimensional--physical-fields-carries-and-arithmetic--37}}

All cochain Steenrod squares include their differential terms. The integer carries appearing in the formulas are:

{{equation:three-dimensional--physical-fields-carries-and-arithmetic--38}}

Every binary field in an integer expression means its canonical zero-or-one
lift. Bars on full sums retain their complete reduction boundary. The
integer products in $`\check\omega_2n_1`$ and $`n_1n'_1`$ use the inherited
local systems; the latter is closed and untwisted. In particular the full
residual satisfies $`dB_3=(\beta_{s_1}\check\omega_2)n_1`$, whereas differentiating
$`B_3^\psi`$ alone need not give that expression. The origin selection uses the
full legal derivative before selecting its p+ip descendant.

#### The finite phase polynomials

The [lower word indices](THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md) also use the nine-term phase numerator

{{equation:three-dimensional--the-finite-phase-polynomials--39}}

The derivative of its integer quarter partner, the literal square of $`x`$,
is already displayed in the mixed and pure quarter formulas. It has not
been absorbed into a binary word table.

The obstruction and stacking law use the same [paired phase convention](THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md), including the explicit output gauge.
