# Complete 4+1D self-stacking, including p+ip decoration

These formulas give the square of a complete lifted state
$`(n_2,\check n_3,n_4,\widehat\nu_5)`$. Every stacking twister and
coefficient set on this page is specialized to two copies of that same
input; no extra input label is needed.

These formulas specialize the complete two-input law. In particular the
input includes the upper decorations required by
$`d_{s_1}n_2=0`$,
$`d\check n_3=\check{\mathcal{𝒪}}_4[n_2]
 =\bar n_2^2+\check\omega_2\bar n_2`$, and
$`dn_4=\mathcal{𝒪}_5^\gamma+\mathcal{𝒪}_5^{\gamma\psi}
 +\mathcal{𝒪}_5^\psi`$. The bosonic obstruction is the unchanged
[4+1D obstruction](FOUR_DIMENSIONAL.md). Neither $`\check n_3`$ nor
$`n_4`$ is set to zero. The output Majorana cochain shown below is closed and need not vanish.

Bars, second digits, canonical lifts, and signed integer products have
the conventions of the general formula. Every $`d\check n_3`$ in a
binary expression below means the binary differential. Integer
differentials appear explicitly inside Bocksteins or integer-carry
identities.

The [root-power construction](ROOT_POWER_PRESENTATIONS.md) explains how
relative self-power relations determine a finite abelian extension and how
odd orders are handled. The complete two-input law remains available; this
page specifies its exact equal-input specialization.

## 1. Integer decoration

{{equation:four-dimensional-self-stacking--1-integer-decoration--1}}

## 2. Majorana decoration

{{equation:four-dimensional-self-stacking--2-majorana-decoration--2}}

The native output is $`N_3=\check N_3+s_1\bar n_2`$.

## 3. Complex-fermion decoration

{{equation:four-dimensional-self-stacking--3-complex-fermion-decoration--3}}

### Majorana decoration

{{equation:four-dimensional-self-stacking--majorana-decoration--4}}

This contribution has **two terms**.

### Majorana and p+ip decoration

{{equation:four-dimensional-self-stacking--majorana-and-p-ip-decoration--5}}

This contribution has **one term**. The sum of the two is $`\mathrm{Sq}^1\check n_3+d\check n_3+s_1\check n_3`$.


### p+ip decoration

The intrinsic p+ip contribution is

{{equation:four-dimensional-self-stacking--p-ip-decoration--6}}

In the last line the bracket is a degree-three face polynomial, multiplied
by $`s_1`$ by the ordinary cup product. This formula has **11 terms**.
The six intrinsic MS terms of the general p+ip lower twister cancel
identically when its two closed inputs $`\bar n_2`$ coincide.

## 4. Bosonic phase

{{equation:four-dimensional-self-stacking--4-bosonic-phase--7}}

### Complex fermions

{{equation:four-dimensional-majorana-diagonal--complex-fermions--5}}

### Complex fermions and Majorana decoration

{{equation:four-dimensional-self-stacking--complex-fermions-and-majorana-decoration--8}}

### Complex fermions and p+ip decoration

{{equation:four-dimensional-self-stacking--complex-fermions-and-p-ip-decoration--9}}

These have respectively **one, three, and two structured terms**, retaining
the already defined lower obstructions. In particular
$`\mathcal{𝒪}_5^\psi[2n_2]
 =\overline{\beta_{s_1}\check\omega_2}\,\bar n_2`$.
The actual output $`N_4`$ is used in both formulas; replacing it by zero
would discard an upper-layer correction.

### Majorana decoration

With the existing integer carry $`B_4^\gamma=\beta^\circ\check n_3`$,

{{equation:four-dimensional-self-stacking--majorana-decoration--10}}

The first sum contains **187 specified MS terms** in the
[self-stacking word table](FOUR_DIMENSIONAL_SELF_STACKING_WORDS.md).
The final sum contains **four whole binary lifts**, with signs
$`+,-,-,+`$ and respectively **5, 15, 10, and 76 interior terms** in the
[self-stacking lift table](FOUR_DIMENSIONAL_SELF_STACKING_LIFTS.md).
The complete contribution has **200 outer terms**, or **302 explicit
occurrences** when the four lift wrappers are replaced in the count by
their 106 interior products. Every lift boundary is retained.

The [exact cochain-identity reduction](FOUR_DIMENSIONAL_SELF_STACKING_REDUCTION.md)
collects the earlier 218 MS terms into 187, without changing any quarter phase. The derivative in the quarter bracket
uses the exact lower-obstruction identity
$`dB_4^\gamma=-\beta(\check{\mathcal{𝒪}}_4[n_2])`$
on the stated input tower.
This is the same open-cochain representative as the general formula.
No cocycle hypothesis on $`\check n_3`$ has been imposed. If p+ip
vanishes and $`d\check n_3=0`$, the further closed-Majorana reduction
and its explicitly stated output gauge remain available separately.

### Majorana and p+ip decoration

{{equation:four-dimensional-self-stacking--majorana-and-p-ip-decoration--11}}

This is the complete restricted coefficient sum: **3,613,517 terms**.
The [explicit coefficient files](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/gamma_psi/INDEX.json)
include the completed transfer and tensor contributions before the two
external inputs are identified. The remaining terms give **181 outer
terms** after the three displayed quarter numerators are substituted and
their linear sums distributed, retaining standard lower operations.
Thus this contribution currently has **3,613,698 outer terms**; the
protected mixed lift has eight interior terms. This large residual is
preserved as exact verification data and remains a target for structural
simplification.

### p+ip decoration

{{equation:four-dimensional-self-stacking--p-ip-decoration--12}}

This finite sum contains **793,669 terms**, including the complete
integer-decoration and tensor contributions. Its
[explicit coefficient files](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/psi/INDEX.json)
use the same lower-operation conventions as the general formula. The
remaining displayed terms add **14 outer terms**, giving **793,683**.
The protected pure lift has twelve interior terms. The denominator-three
term of the general law vanishes identically on equal inputs.

The two large coefficient lists are exact specializations of completed
cochain expressions, not of their input kernels. The
[coefficient appendix](FOUR_DIMENSIONAL_SELF_STACKING_COEFFICIENTS.md)
records the arguments, scopes, checks, and remaining complexity.

## 5. Integer carries and binary quarter numerators

{{equation:four-dimensional-self-stacking--5-integer-carries-and-binary-quarter-numerators--13}}

The quotient is integral with the fixed signed higher cup. The closed-input
Bockstein on its last line is legal because $`d\check N_3=0`$.
The already defined carries are
$`B_4^\gamma=\beta^\circ\check n_3`$ and
$`B_4^\psi=B_4-B_4^\gamma`$, with the exact integer-only definition
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
