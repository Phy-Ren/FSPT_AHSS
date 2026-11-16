<a id="three-dimensional"></a>
# 3+1D

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

Use the [common notation](../FORMULA_GUIDE.md#conventions-and-coordinates). Every physical field and layer below belongs to this dimension.

Throughout this section the physical fields are:

| Field | Physical role | Coefficients |
|---|---|---|
| $`n_1`$ | p+ip decoration | $`\mathbb Z_{s_1}`$ |
| $`n_2`$ | Majorana decoration | $`\mathbb Z_2`$ |
| $`n_3`$ | Complex-fermion decoration | $`\mathbb Z_2`$ |
| $`\nu_4`$ | Bosonic phase | $`U(1)_{s_1}`$ |

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

### 3. Complex-fermion obstruction

<a id="eq-l2"></a>

{{equation:three-dimensional--3-complex-fermion-obstruction--6}}

**Majorana contribution.**

{{equation:three-dimensional--3-complex-fermion-obstruction--7}}

**Mixed Majorana–p+ip contribution.**

{{equation:three-dimensional--3-complex-fermion-obstruction--8}}

Here $`dn_2=\widetilde{\omega}_2[n_1]_2`$ is fixed by the preceding obstruction.

**p+ip contribution.**

<a id="eq-l3"></a>

{{equation:three-dimensional--3-complex-fermion-obstruction--9}}

Here $`\zeta_{2,1}(x,y)(01234)=x(012)\,x(023)\,y(23)\,y(34)`$.
The second digit obeys $`d[\lfloor n_1/2\rfloor]_2=[n_1]_2^2+s_1[n_1]_2`$.

### 4. Bosonic obstruction

<a id="eq-t3"></a>

{{equation:three-dimensional--4-bosonic-obstruction--10}}

The decoration $`n_3`$ is the occupation of the point fermions. The formulas
below abbreviate

```math
B_3=n_2\cup_1n_2.
```

All phases are in the physical
convention of the [guide](../FORMULA_GUIDE.md#phase-convention). For $`n_1=0`$
every contribution reduces to the
[closed-sector formulas](MAJORANA_AND_ENDPOINTS.md#majorana-3d).

#### Complex fermions

{{equation:three-dimensional--complex-fermions--11}}

#### Complex fermions and Majorana decoration

{{equation:three-dimensional--complex-fermions-and-majorana-decoration--12}}

The bracket is the Majorana part of the complex-fermion parity:
$`\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}=\mathrm{Sq}^2n_2
+\omega_2n_2+s_1\mathrm{Sq}^1n_2+d(n_2\cup_1n_2)`$.
Its mixed component retains the terms proportional to $`dn_2`$;
no closed-input assumption is made. The outer superscript records the
exchanged fermion operators. Reusing their full parity does not change
that physical origin.

#### Complex fermions and p+ip decoration

{{equation:three-dimensional--complex-fermions-and-p-ip-decoration--13}}

{{equation:three-dimensional-geometric-reference--O5-cpsi-words}}

The finite sum contains **seven specified MS terms**,
[listed explicitly](THREE_DIMENSIONAL_WORD_INDICES.md#complex-fermion-indices).
The displayed cups give eight terms after distributing their sums, so the contribution has **fifteen terms**.
Every MS term contains $`dn_2=\widetilde{\omega}_2[n_1]_2`$ and
$`dn_3+dB_3=\mathcal{𝒪}_4+dB_3`$, so the complex-fermion exchange correction
depends on the full lower parity differential. The terms with $`B_3`$ vanish
for $`n_1=0`$. The
[exact reduction](THREE_DIMENSIONAL_CF_EXCHANGE_REDUCTION.md#the-obstruction)
gives the seven-word form.

#### Majorana decoration

{{equation:three-dimensional--majorana-decoration--14}}

Here $`\beta^- x=(dx-[dx]_2)/2`$, with the first differential
formed in integers. It agrees with the ordinary Bockstein on a cocycle.
The word operations are

{{equation:three-dimensional--majorana-decoration--15}}

The intrinsic Adem cochain of a binary two-cochain $`x`$ is

{{equation:majorana-and-endpoints--majorana-contribution--24}}

This operation has four word terms. For $`n_1=0`$ one has $`\beta^-=\beta`$, and the
contribution is the closed-Majorana formula.

#### Majorana and p+ip decoration

{{equation:three-dimensional--majorana-and-p-ip-decoration--16}}

The sum contains **2,276 ordinary MS terms** after substituting its finite
definitions and collecting equal normalized cochains. The four further
half-valued cup terms contain $`n_2\cup_2dn_2`$, the difference
$`[\beta^-n_2]_2-n_2\cup_1n_2`$ of the two binary carries of an open
Majorana decoration; they vanish for $`n_1=0`$. The quarter-valued terms are separate.

The integer carry and the twisted Bockstein are

{{equation:three-dimensional--majorana-and-p-ip-decoration--17}}

Both divisions are exact. The product $`\widetilde{\omega}_2n_1`$ has the
local-coefficient transport of its two signed integer factors.
The integer terms are read with the following twists. In
$`\widetilde{\omega}_2[n_1]_2`$ the factor is the untwisted canonical
zero-or-one lift of the binary product. Inside $`\widetilde{\omega}_2n_1`$,
for example in $`(\beta_{s_1}\widetilde{\omega}_2)n_1`$, and in the
Pontryagin term $`\mathfrak P_{s_1}(\widetilde{\omega}_2)\cup n_1`$, the cochain
$`\widetilde{\omega}_2`$ carries $`\mathbb Z_{s_1}`$ coefficients.
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
prints every pair in $`\mathcal I_5^{\psi,\mathrm{face}}`$. Its factors involve only the
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

### 3. Complex-fermion stacking

<a id="eq-p3"></a>

{{equation:three-dimensional--3-complex-fermion-stacking--24}}

**Majorana contribution.**

{{equation:three-dimensional--3-complex-fermion-stacking--25}}

**Mixed Majorana–p+ip contribution.**

{{equation:three-dimensional--3-complex-fermion-stacking--26}}

**p+ip contribution.**

{{equation:three-dimensional--3-complex-fermion-stacking--27}}

The p+ip contribution has three terms. The signed floor is taken before reduction. The parity of a lattice P move equals this formula for both backgrounds.

### 4. Bosonic stacking

<a id="eq-t3b"></a>

{{equation:three-dimensional--4-bosonic-stacking--28}}

The formulas below use $`B_3=n_2\cup_1n_2`$, $`B'_3=n'_2\cup_1n'_2`$ and
$`B_3[N]=N_2\cup_1N_2`$,
$`\Delta B_3=B_3[N]-B_3-B'_3`$,
$`B_3^+=[n_2+n'_2]_2\cup_1[n_2+n'_2]_2`$, $`\lambda_2^\gamma=n_2\cup_2n'_2`$,
and the fixed two-cochain

{{equation:three-dimensional-geometric-reference--pair-cochain}}

The $`\Delta`$ below always uses the actual stacked state.
For two identical complete states with $`n_1=0`$, the entire correction
reduces to the [zero-p+ip self-stacking formula](THREE_DIMENSIONAL_MAJORANA_SELF_STACKING.md).

#### Complex fermions

{{equation:majorana-and-endpoints--complex-fermion-contribution--28}}

#### Complex fermions and Majorana decoration

{{equation:three-dimensional--complex-fermions-and-majorana-decoration--29}}

The $`\Delta`$ has its defined three terms: the value at $`(N_3,N_2)`$ minus the values at $`(n_3,n_2)`$ and $`(n'_3,n'_2)`$. It uses the actual stacked fields, including their p+ip carries. Both parity brackets retain the cochain differential terms.

#### Complex fermions and p+ip decoration

{{equation:three-dimensional--complex-fermions-and-p-ip-decoration--30}}

The two face brackets contain **13 products** after distributing the
binary parentheses: eight multiply $`dn_3+dB_3`$ and five multiply $`dn'_3+dB'_3`$.
The [exchange reduction](THREE_DIMENSIONAL_CF_EXCHANGE_REDUCTION.md) proves
that these products equal the complex-fermion exchange words. The lower obstruction acts on its whole
binary argument; it must not be linearized.
The terms with $`\mathcal B_2`$ are the phase of the shift
$`N_3\mapsto N_3+d\mathcal B_2`$ of the stacked point-fermion occupation.
The terms with $`[\beta^-n_2]_2`$ and $`\lambda_2^\gamma`$ compensate the
quarter-valued Majorana terms; the derivative term is a rephasing of the
stacking move. Together with the terms in $`B_3`$ they vanish for
$`n_1=n'_1=0`$, so that the whole contribution vanishes there.

#### Majorana decoration

{{equation:three-dimensional--majorana-decoration--31}}

The binary completion is

{{equation:three-dimensional--majorana-decoration--32}}

Here $`\mathcal{ℰ}_3^\gamma=n_2\cup_1n'_2
+s_1(n_2\cup_2n'_2)`$ and
$`\beta^{-+}x=(\beta^- x+[\beta^- x]_2)/2=\lfloor(dx+2)/4\rfloor`$.
Its intrinsic binary polynomial is

{{equation:three-dimensional--majorana-decoration--33}}

The finite word sum contains **seven specified MS terms**.
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
have been combined in the half-valued bracket.

These are exact coefficient combinations, with no change of phase
coordinate or reassignment of physical contributions.

On the closed-Majorana tower, $`n_1=n'_1=0`$, this mixed Majorana–p+ip
contribution vanishes. Its half and quarter brackets need not separately
vanish; canceling the binary parity of a quarter term is not sufficient.

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
only $`[n_1]_2`$, $`[\lfloor n_1/2\rfloor]_2`$, their primed counterparts, the
explicit third digit $`[\lfloor n_1/4\rfloor]_2`$, and the
physical faces of $`s_1`$, $`\omega_2`$, and $`\widetilde{\omega}_2`$.

#### Physical fields, carries, and arithmetic

The lower product and source in these displays are the already fixed laws

{{equation:three-dimensional--physical-fields-carries-and-arithmetic--37}}

All cochain Steenrod squares include their differential terms. The integer carries appearing in the formulas are:

{{equation:three-dimensional--physical-fields-carries-and-arithmetic--38}}

Every binary field in an integer expression means its canonical zero-or-one
lift. Bars on full sums retain their complete reduction boundary. The
integer products in $`\widetilde{\omega}_2n_1`$ and $`n_1n'_1`$ use the inherited
local systems; the latter is closed and untwisted. In particular the full
residual satisfies $`d\beta_3=(\beta_{s_1}\widetilde{\omega}_2)n_1`$, whereas differentiating
$`\beta_3^\psi`$ alone need not give that expression. The origin selection uses the
full legal derivative before selecting its p+ip descendant.

#### The finite phase polynomials

The [lower word indices](THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md) also use the nine-term phase numerator

{{equation:three-dimensional--the-finite-phase-polynomials--39}}

The derivative of its integer quarter partner, the literal square of $`x`$,
is already displayed in the mixed and pure quarter formulas. It has not
been absorbed into a binary word table.


<a id="closed-sector"></a>

## Closed sector

For $`n_1=n'_1=0`$ one has $`\beta^-=\beta`$, $`B_3`$ is closed, and every
contribution on this page reduces to the
[closed-sector formulas](MAJORANA_AND_ENDPOINTS.md#majorana-3d); the
contributions $`\mathcal{𝒪}_5^{c\psi},\mathcal{𝒪}_5^{\gamma\psi},\mathcal{𝒪}_5^\psi,
\mathcal{ℰ}_4^{c\psi},\mathcal{ℰ}_4^{\gamma\psi},\mathcal{ℰ}_4^\psi`$ vanish.
