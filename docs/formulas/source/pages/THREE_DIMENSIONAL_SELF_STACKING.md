# Complete root self-stacking in 3+1D

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

This page stacks two identical **complete states**, including the complex-fermion
completion and bosonic phase. The lower fields obey the obstruction equations
in [the 3+1D reference](THREE_DIMENSIONAL.md). The background is
$`\widetilde{\omega}_2=\omega_2+s_1^2`$.
The formulas are the general laws of that reference with equal upper and lower states,
with $`B_3=n_2\cup_1n_2`$.

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

This is the stacked field before removing the integer decoration. The corresponding
integer gauge can change the Majorana field of the stacked state.

## 3. Complex-fermion self-stacking

{{equation:three-dimensional-self-stacking--3-complex-fermion-self-stacking--3}}

**Majorana contribution.**

{{equation:three-dimensional-self-stacking--3-complex-fermion-self-stacking--4}}

**Majorana–p+ip contribution.**

{{equation:three-dimensional-self-stacking--3-complex-fermion-self-stacking--5}}

**p+ip contribution.**

{{equation:three-dimensional-self-stacking--3-complex-fermion-self-stacking--6}}

There are **five terms**. Their total is
$`\mathrm{Sq}^1n_2+s_1n_2+\mathcal{ℰ}_3^\psi`$,
with the open-cochain square. The changed cup order is essential.
The diagonal Cartan term vanishes because the parity of the state is closed.

For both finite-root branches below, the two-cochain $`\mathcal B_2`$ of the
general formula equals $`n_2`$, and $`N_2\cup_1N_2=0`$.

## 4. Bosonic self-stacking with zero p+ip input

For $`n_1=0`$, the complete bosonic result is

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--7}}

The earlier lower equations specialize to

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--8}}

Here $`dn_2=0`$ and $`dn_3=\mathcal{𝒪}_4^\gamma[n_2]`$. The three physical
contributions are

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--9}}

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--10}}

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--11}}

On this closed branch the last two derivative terms of the point-fermion block vanish.
The complete phase has **seven half terms and three quarter terms**,
retaining the defined lower fields of the stacked state and the obstruction.
The quarter-valued obstruction is the canonical integer lift of its
**whole binary value**. It must not be distributed into separately lifted
summands. The [coefficient proof](coefficients/verify_three_dimensional_majorana_self_stacking.py)
also checks the complex-fermion completion.

## 5. Bosonic self-stacking of the canonical p+ip torsion root

For $`n_1=s_1`$, retain every allowed Majorana and complex-fermion completion.
The complete bosonic result, before the integer gauge, is

{{equation:three-dimensional-self-stacking--5-bosonic-self-stacking-of-the-canonical-p-ip-torsio--12}}

The lower fields of the stacked state specialize to

{{equation:three-dimensional-self-stacking--5-bosonic-self-stacking-of-the-canonical-p-ip-torsio--13}}

{{equation:three-dimensional-self-stacking--5-bosonic-self-stacking-of-the-canonical-p-ip-torsio--14}}

In particular,
$`dn_2=\widetilde{\omega}_2s_1`$ and
$`dn_3=(\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi})[n_2]
+\mathcal{𝒪}_4^\psi[s_1]`$.
The six labels retain their fermionic exchange origins.

### Complex fermions

{{equation:three-dimensional-self-stacking--4-bosonic-self-stacking-with-zero-p-ip-input--9}}

### Complex fermions and Majorana decoration

{{equation:three-dimensional-self-stacking--complex-fermions-and-majorana-decoration--15}}

The mixed part on the stacked state vanishes exactly because $`d(s_1^2)=0`$, so
$`\mathcal{𝒪}_4^{\gamma\psi}[s_1^2]=0`$. The individual lower differential
representatives remain defined structures.

### Complex fermions and p+ip decoration

On the ordered four-simplex,

{{equation:three-dimensional-self-stacking--complex-fermions-and-p-ip-decoration--16}}

The three face products equal the
entire 132-word complex-fermion exchange on equal upper and lower states. This is an
exact cochain identity; the two other open-Majorana product terms vanish
because their complex-fermion argument is $`n_3+n_3=0`$.
The evaluation $`\mathcal{𝒪}_4^\psi[2s_1]`$ on the stacked state retains the second digit:
$`[\lfloor 2s_1/2\rfloor]_2=s_1`$. The three terms with $`n_2\cup_2dn_2`$ come from
$`[\beta^-n_2]_2=n_2\cup_1n_2+n_2\cup_2dn_2`$; they vanish for a closed $`n_2`$.
This contribution has **19 terms**.

### Majorana decoration

{{equation:three-dimensional-self-stacking--majorana-decoration--17}}

This is **18 terms: fifteen half terms and three quarter terms**,
valid also for an arbitrary open $`n_2`$. It is the general Majorana
contribution with equal upper and lower states.
The first face product is the exact diagonal of seven intrinsic Majorana
MS terms. The quarter-valued terms are integer cups of $`\beta^-n_2`$ and of the
canonical integer lift of $`n_2`$;
$`\beta^- x=(dx-[dx]_2)/2`$ uses the integer differential
in its first term.

### Majorana and p+ip decoration

{{equation:three-dimensional-self-stacking--majorana-and-p-ip-decoration--18}}

The finite sum contains **1,130 explicitly listed physical-face products**
in the [coefficient table](THREE_DIMENSIONAL_SELF_STACKING_FACES.md#majoranapip-half-contribution).
It includes the entire half-valued contribution. The three ordinary
half terms, the two terms of the displayed coboundary, and nine distributed
quarter terms are additional, giving **1,144 terms** in this contribution. Every differential in these fractional
brackets acts on the indicated integer cochain; $`[\cdot]_2`$ selects a
binary value before its integer lift.

The existing lower integer carries specialize to

{{equation:three-dimensional-self-stacking--majorana-and-p-ip-decoration--19}}

Here $`d\lambda_2^\psi=0`$ as an integer identity. The signed product in
$`(\beta_{s_1}\widetilde{\omega}_2)s_1`$ keeps both inherited sign coefficient
systems; its value must not be replaced by an unsigned product.

### p+ip decoration

{{equation:three-dimensional-self-stacking--p-ip-decoration--20}}

The finite sum contains **244 explicitly listed physical-face products**
in the [coefficient table](THREE_DIMENSIONAL_SELF_STACKING_FACES.md#pure-pip-half-contribution).
The six remaining ordinary terms give **250 terms** in this contribution.
The eighth-valued sign follows from the signed integer identity
$`s_1s_1=-[s_1^2]_2`$ when both factors are copies of the p+ip
integer decoration. The binary square $`s_1^2`$ elsewhere keeps its stated
canonical integer lift.

### Completeness and use in root relations

| Physical contribution | Explicit terms |
|---|---:|
| c | 1 |
| c-gamma | 3 |
| c-psi | 19 |
| gamma | 18 |
| gamma-psi | 1,144 |
| psi | 250 |
| Complete canonical torsion self-twister | **1,435** |

The count retains the already defined lower differential representatives,
Bocksteins and integer carries, while counting every finite coefficient
product separately. It is not a claim of minimality.
The [3+1D verification](verification/three_dimensional/README.md) checks every
contribution of both branches pointwise against the general law with equal
upper and lower states, and regenerates the two face tables from the general law.

These are complete **self-stacking twisters before gauge reduction**.
To obtain a root relation, subsequently remove $`N_1=2s_1`$ with the complete
integer gauge, then reduce all induced lower decorations and the phase.
In the normalized lower cylinder the parameter $`+1`$ removes $`2s_1`$ and
changes the Majorana decoration from $`s_1^2`$ to $`\omega_2`$. Thus the initial
$`N_2=s_1^2`$ must not be read as the final Majorana decoration of the relation.
The full gauge descent and its bosonic correction are retained when forming
the group presentation.
