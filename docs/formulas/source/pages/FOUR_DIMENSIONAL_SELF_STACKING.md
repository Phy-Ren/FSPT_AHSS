# Complete 4+1D self-stacking, including p+ip decoration

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

These formulas give the square of a complete lifted state
$`(n_2,n_3,n_4,\nu_5)`$ in the [general formulas](FOUR_DIMENSIONAL.md). Every stacking twister and
coefficient set on this page is specialized to upper and lower states that
are both this same state; no extra state label is needed.

These formulas specialize the complete stacking law for two separate states.
In particular the state includes the higher decorations required by
$`d_{s_1}n_2=0`$,
$`dn_3=\mathcal{𝒪}_4[n_2]
 =[n_2]_2^2+\widetilde{\omega}_2[n_2]_2`$, and
$`dn_4=\mathcal{𝒪}_5`$. The bosonic obstruction is the same
[4+1D obstruction](FOUR_DIMENSIONAL.md). Neither $`n_3`$ nor
$`n_4`$ is set to zero. The Majorana cochain of the stacked state shown below is closed and need not vanish.

Bars, second digits, canonical lifts, and signed integer products have
the conventions of the general formula. Every $`dn_3`$ in a
binary expression below means the binary differential. Integer
differentials appear explicitly inside Bocksteins or integer-carry
identities.

The [root-power construction](ROOT_POWER_PRESENTATIONS.md) explains how
relative self-power relations determine a finite abelian extension and how
odd orders are handled. The complete law for two different states remains available; this
page specifies its exact specialization to equal upper and lower states. The
[phase convention](FOUR_DIMENSIONAL_MAJORANA_PHASE.md) is specialized at
the same time. Since the binary sum of two equal Majorana fields is zero,
$`2B_5[n_3]=\tfrac12(n_3\cup_1n_3)`$ modulo
one; the half-valued part doubles to an integer. This gives the short
extra terms below directly from the general law.

## 1. Integer decoration

{{equation:four-dimensional-self-stacking--1-integer-decoration--1}}

## 2. Majorana decoration

{{equation:four-dimensional-self-stacking--2-majorana-decoration--2}}

In the lift variable of the code input, this stacked field is $`N_3+s_1[n_2]_2`$.

## 3. Complex-fermion decoration

{{equation:four-dimensional-self-stacking--3-complex-fermion-decoration--3}}

### Majorana decoration

{{equation:four-dimensional-self-stacking--majorana-decoration--4}}

This contribution has **two terms**.

### Majorana and p+ip decoration

{{equation:four-dimensional-self-stacking--majorana-and-p-ip-decoration--5}}

This contribution has **one term**. The sum of the two is $`\mathrm{Sq}^1n_3+s_1n_3`$, with $`\mathrm{Sq}^1n_3=n_3\cup_2n_3+n_3\cup_3dn_3`$.


### p+ip decoration

The intrinsic p+ip contribution is

{{equation:four-dimensional-self-stacking--p-ip-decoration--6}}

In the last line the bracket is a degree-three face polynomial, multiplied
by $`s_1`$ by the ordinary cup product. This formula has **12 terms**; the last one,
$`N_3\cup_2N_3`$, is the specialization of $`\mathcal{ℰ}_3\cup_2\mathcal{ℰ}_3`$, and the polarization term
$`\Delta[\cdots]`$ of the general law vanishes for equal states.
The six intrinsic MS terms of the general p+ip lower twister cancel
identically when the closed fields $`[n_2]_2`$ of the two separate states coincide.

## 4. Bosonic phase

{{equation:four-dimensional-self-stacking--4-bosonic-phase--7}}

### Complex fermions

{{equation:four-dimensional-self-stacking--complex-fermions--17}}

### Complex fermions and Majorana decoration

{{equation:four-dimensional-self-stacking--complex-fermions-and-majorana-decoration--8}}

### Complex fermions and p+ip decoration

{{equation:four-dimensional-self-stacking--complex-fermions-and-p-ip-decoration--9}}

These have respectively **one, ten, and two structured terms**, retaining
the already defined lower obstructions. In particular
$`\mathcal{𝒪}_5^\psi[2n_2]
 =[\beta_{s_1}\widetilde{\omega}_2]_2\,[n_2]_2`$.
The actual stacked field $`N_4`$ of the lower self-stacking law is used in these formulas; replacing it by zero
would discard an upper-layer correction. The second bracket of
$`\mathcal{ℰ}_5^{c\gamma}`$ is the specialization of the corresponding bracket of
the general law: $`y=n_3\cup_2n_3+x`$ with $`x`$ the polynomial of
$`\mathcal{𝒪}_6^\psi`$, and $`\mathcal{𝒪}_5[N]`$ is evaluated on the stacked state.

### Majorana decoration

With the existing integer carry $`\beta_4^\gamma=\beta^-n_3`$,

{{equation:four-dimensional-self-stacking--majorana-decoration--10}}

The first sum contains **187 specified MS terms** in the
[self-stacking word table](FOUR_DIMENSIONAL_SELF_STACKING_WORDS.md).
The final sum contains **four whole binary lifts**, with signs
$`+,-,-,+`$ and respectively **5, 15, 10, and 76 interior terms** in the
[self-stacking lift table](FOUR_DIMENSIONAL_SELF_STACKING_LIFTS.md).
The complete contribution has **200 outer terms without the two $`B_5`$ half terms**, or **302 explicit
occurrences without them** when the four lift wrappers are replaced in the count by
their 106 interior products. Every lift boundary is retained.

The [exact cochain-identity reduction](FOUR_DIMENSIONAL_SELF_STACKING_REDUCTION.md)
gives this 187-term MS sum, without changing any quarter phase. The derivative in the quarter bracket
uses the exact lower-obstruction identity
$`d\beta_4^\gamma=-\beta(\mathcal{𝒪}_4[n_2])`$
on the stated input tower.
This is the same open-cochain representative as the general formula.
No cocycle hypothesis on $`n_3`$ has been imposed. The phase
convention contributes the two displayed half terms
$`[n_3\cup_1n_3-s_1\mathcal{ℰ}_4^\gamma]/2`$. The
[zero-p+ip self-stacking page](FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md)
is the restriction $`n_2=0`$ of these formulas.

### Majorana and p+ip decoration

{{equation:four-dimensional-self-stacking--majorana-and-p-ip-decoration--11}}

This is the complete restricted coefficient sum: **3,613,517 terms**.
The [explicit coefficient files](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/gamma_psi/INDEX.json)
include the completed transfer and tensor contributions before the upper
and lower states are identified. The remaining terms give **181 outer
terms** after the three displayed quarter numerators are substituted and
their linear sums distributed, retaining standard lower operations.
Thus this contribution has **3,613,698 outer terms without the phase-convention term**; the
protected mixed lift has eight interior terms. The additional term
$`-s_1\mathcal{ℰ}_4^{\gamma\psi}/2`$ is its entire phase-convention
term on equal upper and lower states: the three general $`B_5`$ evaluations cancel
exactly here.

### p+ip decoration

{{equation:four-dimensional-self-stacking--p-ip-decoration--12}}

This finite sum contains **793,669 terms**, including the complete
integer-decoration and tensor contributions. Its
[explicit coefficient files](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/psi/INDEX.json)
use the same lower-operation conventions as the general formula. The
remaining displayed terms add **14 outer terms**, giving **793,683 without the phase-convention terms**.
The protected pure lift has twelve interior terms. The denominator-three
term of the general law vanishes identically on equal upper and lower states.
The extra half term and $`-B_5[N_3]`$ are the remaining
pure-integer phase-convention terms; the latter has 45 explicit terms
with the defined stacked field as its argument. Its complete coefficient list
is shared with the general formula rather than fitted on the diagonal.

The two large coefficient lists are exact specializations of completed
cochain expressions, not of their input kernels. The
[coefficient appendix](FOUR_DIMENSIONAL_SELF_STACKING_COEFFICIENTS.md)
records the arguments, scopes, and checks.

## 5. Integer carries and binary quarter numerators

{{equation:four-dimensional-self-stacking--5-integer-carries-and-binary-quarter-numerators--13}}

The quotient is integral with the fixed signed higher cup. The closed-input
Bockstein on its last line is legal because $`dN_3=0`$.
The already defined carries are
$`\beta_4^\gamma=\beta^-n_3`$ and
$`\beta_4^\psi=\beta_4-\beta_4^\gamma`$, with the exact integer-only definition
[used in the general source and product](FOUR_DIMENSIONAL.md#eq-s1).
In the following expressions all the $`\lambda_3^\psi`$ refer to their
value just displayed.

{{equation:four-dimensional-self-stacking--5-integer-carries-and-binary-quarter-numerators--14}}

This has **four terms**. The mixed numerator has **eight terms**:

{{equation:four-dimensional-self-stacking--5-integer-carries-and-binary-quarter-numerators--15}}

The differential of the four-term bracket contributes four of these
terms. It remains inside the whole binary lift where that lift occurs.
The p+ip numerator has **twelve terms**:

{{equation:four-dimensional-self-stacking--5-integer-carries-and-binary-quarter-numerators--16}}

The three binary numerators are the existing quarter-valued corrections,
not newly fitted coefficients. Their pairwise products in the mixed phase
are the canonical-lift carries of their sum; they have not been discarded
or reassigned by variable support. Integer cups in fractional brackets
use the signed transports of the general law.
