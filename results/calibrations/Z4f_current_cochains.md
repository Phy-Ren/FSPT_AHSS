# The current 4+1D Z4f cochain representatives

Take $`G_f=\mathbb Z_4^f`$, $`G_b=\mathbb Z_2`$, $`\omega_2=m_1^2`$, and $`s_1=0`$.
Here $`m_1(g)=g`$ for $`g\in\{0,1\}`$, and $`m_1^q`$ is the ordered cup power. It equals one precisely when all its arguments are one. Binary inputs have their canonical integer values whenever integer arithmetic is required.

The following representatives solve the [current obstruction equations](../../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4). The multiplicative phase is $`\nu_5=\exp(2\pi i\widehat\nu_5)`$.

| Root layer | $`n_2`$ | $`n_3`$ | $`n_4`$ | $`\widehat\nu_5`$ | $`\widehat{\mathcal O}_6`$ |
|---|---|---|---|---|---|
| p+ip | $`m_1^2`$ | $`0`$ | $`0`$ | $`25m_1^5/96`$ | $`25m_1^6/48`$ |
| Majorana | $`0`$ | $`m_1^3`$ | $`0`$ | $`m_1^5/8`$ | $`m_1^6/4`$ |
| Complex fermion | $`0`$ | $`0`$ | $`m_1^4`$ | $`m_1^5/4`$ | $`m_1^6/2`$ |
| Bosonic | $`0`$ | $`0`$ | $`0`$ | $`m_1^5/2`$ | $`0`$ |

All four lower solutions have $`dn_2=dn_3=dn_4=0`$. Their lower obstruction cochains vanish pointwise. Since $`dm_1^5=2m_1^6`$ over the integers, every phase in the table obeys its full terminal equation. The nonzero terminal cochains are coboundaries and do not obstruct these solutions.

For the p+ip root the fixed binary completion is $`y_6=m_1^6`$, and $`B_4^\psi=-m_1^4`$. The signed integral cup gives $`m_1^4\cup_2m_1^4=4m_1^6`$. Thus the half-valued completion, integer quadratic term, background terms, and cubic normalization give

```math
\widehat{\mathcal O}_6
=\left(\frac12+\frac34+\frac18+\frac1{16}+\frac1{12}\right)m_1^6
=\frac{25}{48}m_1^6\pmod1.
```

The Majorana row includes the [paired phase change](../../docs/formulas/FOUR_DIMENSIONAL_MAJORANA_PHASE.md). On this root $`R_5=m_1^5/4`$ modulo one, so the preceding coordinate value $`3m_1^5/8`$ becomes $`m_1^5/8`$. Keeping $`3m_1^5/8`$ with the current obstruction would leave the nonzero residual $`m_1^6/2`$. This is a change of cochain coordinates applied to the obstruction and product together; it is not an ordinary gauge transformation with the obstruction held fixed. The invertible transport preserves the established full stacking group $`\mathbb Z_{16}`$.

The [exact receipt](Z4f_current_cochains.json) checks every one of the 64 inhomogeneous six-tuples, including tuples containing the identity, for each root. All terminal residuals vanish, and all lower equations and the phase-transport identities pass. It also evaluates the complete fixed $`y_6`$ and the relative Majorana polynomial on those 64 tuples, and checks that the numerical $`y_6`$ coefficient table equals the reader table. The [standalone checker](../../scripts/check_z4f_current_cochains.py) uses exact integers and fractions. This is a concrete cochain calibration; it does not assert universal physical uniqueness of the formulas.
