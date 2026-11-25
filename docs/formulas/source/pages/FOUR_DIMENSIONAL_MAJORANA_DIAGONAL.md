# Self-stacking in 4+1D with no p+ip decoration

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

Take a complete state with $`n_2=0`$, closed binary Majorana cochain
$`n_3`$, complex-fermion cochain $`n_4`$ satisfying
$`dn_4=\mathcal{𝒪}_5^\gamma[n_3]`$, and phase $`\nu_5`$
satisfying the [closed obstruction equation](MAJORANA_AND_ENDPOINTS.md#eq-m3-4d). Here
$`n_4`$ is the physical point-fermion occupation used in the
[closed-Majorana 4+1D formulas](MAJORANA_AND_ENDPOINTS.md#majorana-4d).
In all stacking corrections below the upper and lower states are the same
complete state. They are the specialization of those closed laws to equal
states, and equally the
zero-p+ip restriction of the [complete self-stacking formulas](FOUR_DIMENSIONAL_SELF_STACKING.md).

## 1. p+ip stacking

{{equation:four-dimensional-majorana-diagonal--1-p-ip-stacking--1}}

## 2. Majorana stacking

{{equation:four-dimensional-majorana-diagonal--2-majorana-stacking--2}}

## 3. Complex-fermion stacking

{{equation:four-dimensional-majorana-diagonal--3-complex-fermion-stacking--3}}

## 4. Bosonic stacking

{{equation:four-dimensional-majorana-diagonal--4-bosonic-stacking--4}}

### Complex fermions

{{equation:four-dimensional-majorana-diagonal--complex-fermions--5}}

### Complex fermions and Majorana decoration

{{equation:four-dimensional-majorana-diagonal--complex-fermions-and-majorana-decoration--6}}

The terms of the general formula on the stacked state vanish because $`N_3=0`$ and $`dN_4=0`$.
The terms after the first are the occupation bracket of the [general law](FOUR_DIMENSIONAL_SELF_STACKING.md) at $`n_2=0`$.

### Majorana decoration

This is the shared self-stacking expression with $`n_2=0`$,
$`dn_3=0`$, and $`\beta_4^\gamma=\beta n_3`$. The terms
containing $`dn_3`$ or $`\beta(\mathcal{𝒪}_4[n_2])`$
vanish and are omitted:

{{equation:four-dimensional-majorana-diagonal--majorana-decoration--7}}

## Specialization of the phase convention

The complete lower fields of the stacked state here are $`N_3=0`$ and
$`N_4=\mathcal{ℰ}_4^\gamma`$. The $`B_5`$ terms of the phase convention
consequently give $`\tfrac12[n_3\cup_1n_3-s_1\mathcal{ℰ}_4^\gamma]`$; this
half-valued cochain is unchanged by the overall sign.
Those two terms already appear in the Majorana formula above.

All integer lifts and Bocksteins have their common meanings. In particular
$`\beta n_3=dn_3/2`$ uses the integer differential of the binary cocycle,
and the whole binary lifts inside the formula retain their scopes.
The coefficient sets are the same ones used in
[complete self-stacking](FOUR_DIMENSIONAL_SELF_STACKING.md); their values
are specialized with the stated closed input rather than fitted again.
The complex-fermion completion of the separate states and their incoming phase are retained.

The [root-power presentation](ROOT_POWER_PRESENTATIONS.md) explains how
these powers determine the final abelian group.
