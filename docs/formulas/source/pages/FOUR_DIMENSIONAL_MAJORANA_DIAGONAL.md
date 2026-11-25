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

### Majorana decoration

Here $`\beta n_3=dn_3/2`$ uses the integer differential of the canonical
lift of the closed $`\mathbb Z_2`$ cochain $`n_3`$, $`\mathrm{Sq}^1n_3=[\beta n_3]_2=n_3\cup_2n_3`$,
and the products in the quarter bracket are signed integer higher cups of
canonical lifts:

{{equation:four-dimensional-majorana-diagonal--majorana-decoration--7}}

This is the closed-Majorana self-stacking law of the thesis, the
specialization of [(M3E)](MAJORANA_AND_ENDPOINTS.md#eq-m3-stacking-4d) to equal
upper and lower states. The [complete self-stacking formulas](FOUR_DIMENSIONAL_SELF_STACKING.md)
at $`n_2=0`$ equal it as cochains. The complex-fermion completion of the
separate states and their incoming phase are retained.

The [root-power presentation](ROOT_POWER_PRESENTATIONS.md) explains how
these powers determine the final abelian group.
