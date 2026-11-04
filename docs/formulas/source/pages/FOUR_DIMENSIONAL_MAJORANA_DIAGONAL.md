# Self-stacking in 4+1D with no p+ip decoration

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

Take a complete state with $`n_2=0`$, closed binary Majorana cochain
$`n_3`$, complex-fermion cochain $`n_4`$ satisfying
$`dn_4=\mathcal{𝒪}_5^\gamma[n_3]`$, and phase $`\nu_5`$
satisfying the [closed obstruction equation](MAJORANA_AND_ENDPOINTS.md#eq-m3-4d). Here $`\widetilde{n}_3=n_3`$, and
$`n_4`$ is the physical point-fermion occupation used in the
[closed-Majorana 4+1D formulas](MAJORANA_AND_ENDPOINTS.md#majorana-4d).
All stacking corrections below have identical complete inputs. They are the
equal-input specialization of those closed laws, that is, the negative of the
zero-p+ip restriction of the [complete self-stacking formulas](FOUR_DIMENSIONAL_SELF_STACKING.md)
evaluated at the same arguments. The complex-fermion contributions are
half-valued and unchanged in form; the quarter-valued Majorana terms change
sign. The two forms are related by the
[bridging identity](FOUR_DIMENSIONAL.md#bridging-identity-4d); on equal inputs
the polarization of $`\tfrac12n_4\cup_3\mathrm{Sq}^1n_3`$ vanishes.

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

The output term of the general formula vanishes because $`N_3=0`$, and the mixed input source is zero.

### Majorana decoration

This is the negative of the shared self-stacking expression with $`n_2=0`$,
$`d\widetilde{n}_3=0`$, and $`\beta_4^\gamma=\beta n_3`$. The terms
containing $`d\widetilde{n}_3`$ or $`\beta(\widetilde{\mathcal{𝒪}}_4[n_2])`$
vanish and are omitted:

{{equation:four-dimensional-majorana-diagonal--majorana-decoration--7}}

The phase convention is that of the closed obstruction, with quarter-valued
bracket $`-1/4`$.

## Specialization of the common phase change

The full lower output here has $`\widetilde{N}_3=0`$ and
$`N_4=\mathcal{ℰ}_4^\gamma`$. The common phase map consequently gives
$`-\Delta B_5=\tfrac12[n_3\cup_1n_3-s_1\mathcal{ℰ}_4^\gamma]`$; this
half-valued cochain is unchanged by the overall sign.
Those two terms already appear in the Majorana formula above.
No separate diagonal representative or additional output gauge is chosen.
The existing output coboundary is part of the shared general formula.

All integer lifts and Bocksteins have their common meanings. In particular
$`\beta n_3=dn_3/2`$ uses the integer differential of the binary cocycle,
and the whole binary lifts inside the formula retain their scopes.
The coefficient sets are the same ones used in
[complete self-stacking](FOUR_DIMENSIONAL_SELF_STACKING.md); their values
are specialized with the stated closed input rather than fitted again.
The input complex-fermion completion and incoming phase are retained.

The [root-power presentation](ROOT_POWER_PRESENTATIONS.md) explains how
these powers determine the final abelian group.
