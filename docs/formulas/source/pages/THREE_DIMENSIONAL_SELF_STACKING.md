# Complete root self-stacking in 3+1D

This page stacks two identical **complete states**, including the complex-fermion
completion and bosonic phase. The lower fields obey the obstruction equations
in [the 3+1D reference](THREE_DIMENSIONAL.md). The coordinate convention is
$`\check n_2=n_2+s_1\widetilde n_1`$ and
$`\check\omega_2=\omega_2+s_1^2`$.
The formulas use the same phase representative as that reference.

The terminal formulas below cover $`n_1=0`$ and the canonical signed torsion
representative $`n_1=s_1`$. These are the two branches required for finite root
power relations in 3+1D, as explained in the
[root-power presentation theorem](ROOT_POWER_PRESENTATIONS.md).
The first three stacking laws hold for every signed integer cocycle $`n_1`$.
A nonzero free integer root has no finite power relation.

## 1. p+ip self-stacking

{{equation:three-dimensional-self-stacking--1-p-ip-self-stacking--1}}

The value $`2n_1`$ is retained as a cochain, even when its cohomology class is zero.

## 2. Majorana self-stacking

{{equation:three-dimensional-self-stacking--2-majorana-self-stacking--2}}

This is the output before removing the integer decoration. The corresponding
integer gauge can change the Majorana output.

## 3. Complex-fermion self-stacking

{{equation:three-dimensional-self-stacking--3-complex-fermion-self-stacking--3}}

**Majorana contribution.**

{{equation:three-dimensional-self-stacking--3-complex-fermion-self-stacking--4}}

**Majorana–p+ip contribution.**

{{equation:three-dimensional-self-stacking--3-complex-fermion-self-stacking--5}}

**p+ip contribution.**

{{equation:three-dimensional-self-stacking--3-complex-fermion-self-stacking--6}}

There are **seven terms**. Their total can also be written as
$`\mathrm{Sq}^1\check n_2+d\check n_2+s_1\check n_2+
\mathcal{ℰ}_{3}^\psi`$ using the open-cochain Steenrod square.
The term $`d\check n_2`$ must be retained.

## 4. Bosonic self-stacking with zero p+ip input

For $`n_1=0`$, the complete bosonic output is

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--7}}

The earlier lower equations specialize to

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--8}}

Here $`dn_2=0`$ and $`dn_3=\mathcal{𝒪}_4^\gamma[n_2]`$. The three physical
contributions are

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--9}}

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--10}}

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--11}}

The complete formula has **ten terms: seven half terms and three quarter
terms**, retaining the already defined lower output and obstruction.
The quarter-valued obstruction is the canonical integer lift of its
**whole binary value**. It must not be distributed into separately lifted
summands. This is an exact simplification with no additional gauge;
[a self-contained coefficient proof](coefficients/verify_three_dimensional_majorana_self_stacking.py)
also checks the complex-fermion completion.

## 5. Bosonic self-stacking of the canonical p+ip torsion root

For $`n_1=s_1`$, retain every allowed Majorana and complex-fermion completion.
The complete bosonic output, before the integer gauge, is

{{equation:three-dimensional-self-stacking--5-bosonic-self-stacking-of-the-canonical-p-ip-torsio--12}}

The earlier lower outputs specialize to

{{equation:three-dimensional-self-stacking--5-bosonic-self-stacking-of-the-canonical-p-ip-torsio--13}}

{{equation:three-dimensional-self-stacking--5-bosonic-self-stacking-of-the-canonical-p-ip-torsio--14}}

In particular,
$`d\check n_2=\check\omega_2s_1`$ and
$`dn_3=(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[\check n_2]
+\mathcal{𝒪}_4^\psi[s_1]`$.
The six labels below retain their fermionic exchange origins.

### Complex fermions

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--9}}

### Complex fermions and Majorana decoration

{{equation:three-dimensional-self-stacking--complex-fermions-and-majorana-decoration--15}}

These are **three terms** after distributing the input parity bracket.
The output mixed part vanishes exactly because $`d(s_1^2)=0`$, so
$`\mathcal{𝒪}_4^{\gamma\psi}[s_1^2]=0`$. The individual lower differential
representatives remain defined structures.

### Complex fermions and p+ip decoration

On the ordered four-simplex,

{{equation:three-dimensional-self-stacking--complex-fermions-and-p-ip-decoration--16}}

This contribution has **five terms**. The three face products replace the
entire 132-word open-Majorana correction on identical inputs. This is an
exact cochain identity; the two other open-Majorana product terms vanish
because their complex-fermion argument is $`n_3+n_3=0`$.
The output evaluation $`\mathcal{𝒪}_4^\psi[2s_1]`$ retains the second digit:
$`\widetilde{2s_1}=s_1`$.

### Majorana decoration

{{equation:three-dimensional-self-stacking--majorana-decoration--17}}

This is **13 outer terms: ten half terms and three quarter terms**,
valid also for an arbitrary open $`\check n_2`$. The whole lift contains
**two terms**, retaining the existing lower obstruction. Replacing its
wrapper by those two interior terms in the count gives **14 leaves**.
The [lower-obstruction carry identity](THREE_DIMENSIONAL_OPEN_MAJORANA_LIFT_REDUCTION.md)
replaces six former terms by three with exact equality modulo one.
The first face product is the exact diagonal of seven intrinsic Majorana
MS terms. Integer cups and the whole binary lift retain their scopes;
$`\beta^\circ x=(dx-\overline{dx})/2`$ uses the integer differential
in its first term.

### Majorana and p+ip decoration

{{equation:three-dimensional-self-stacking--majorana-and-p-ip-decoration--18}}

The finite sum contains **1,130 explicitly listed physical-face products**
in the [coefficient table](THREE_DIMENSIONAL_SELF_STACKING_FACES.md#majoranapip-half-contribution).
It includes the entire current half-valued contribution. The three ordinary
half terms and nine distributed quarter terms are additional, giving
**1,142 terms** in this contribution. Every differential in these fractional
brackets acts on the indicated integer cochain; a whole bar selects a
binary value before its integer lift.

The existing lower integer carries specialize to

{{equation:three-dimensional-self-stacking--majorana-and-p-ip-decoration--19}}

Here $`d\lambda_2^\psi=0`$ as an integer identity. The signed product in
$`(\beta_{s_1}\check\omega_2)s_1`$ keeps both inherited sign coefficient
systems; its value must not be replaced by an unsigned product.

### p+ip decoration

{{equation:three-dimensional-self-stacking--p-ip-decoration--20}}

The finite sum contains **244 explicitly listed physical-face products**
in the [coefficient table](THREE_DIMENSIONAL_SELF_STACKING_FACES.md#pure-pip-half-contribution).
The six remaining ordinary terms give **250 terms** in this contribution.
The eighth-valued sign follows from the signed integer identity
$`s_1s_1=-\overline{s_1^2}`$ when both factors are copies of the p+ip
integer decoration. The binary square $`s_1^2`$ elsewhere keeps its stated
canonical integer lift.

### Completeness and use in root relations

| Physical contribution | Explicit terms |
|---|---:|
| c | 1 |
| c-gamma | 3 |
| c-psi | 5 |
| gamma | 13 |
| gamma-psi | 1,142 |
| psi | 250 |
| Complete canonical torsion self-twister | **1,414** |

The count retains the already defined lower differential representatives,
Bocksteins and integer carries, while counting every finite coefficient
product separately. The Majorana whole lift has two interior terms;
counting its interior gives 1,415 leaves instead of 1,414 outer terms.
It is not a claim of minimality.
The [standalone exact verifier](coefficients/verify_three_dimensional_canonical_self_stacking.py)
checks every physical sector and the total against the frozen baseline
on all 20 independent valid-tower bits. All seven residuals are zero.
The [additional lift-identity verifier](coefficients/verify_three_dimensional_open_gamma_lift_reduction.py)
checks the current 13-term Majorana expression against that same baseline.
The fully collected scalar phase has 2,652 coefficients modulo 16; that
supplementary coefficient count uses a different expansion boundary.

These are complete **self-stacking twisters before gauge reduction**.
To obtain a root relation, subsequently remove $`N_1=2s_1`$ with the complete
integer gauge, then reduce all induced lower decorations and the phase.
In the normalized lower cylinder the parameter $`+1`$ removes $`2s_1`$ and
changes the native Majorana field from zero to $`\omega_2`$. Thus the initial
$`N_2=0`$ must not be read as the final Majorana coordinate of the relation.
The full gauge descent and its bosonic correction are retained when forming
the group presentation.
