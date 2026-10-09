# Current cochain representatives for the 3+1D time-reversal example

Take $`G_b=\mathbb Z_2^T`$, $`s_1=m_1`$, and
$`\omega_2=m_1^2`$, where the normalized bar cochain is
$`m_1(g)=g`$ for $`g\in\{0,1\}`$.
Its ordered cup powers are
$`m_1^q(g_1,\ldots,g_q)=\prod_j g_j`$.
The additive phase is defined by
$`\nu_4=\exp(2\pi i\widehat\nu_4)`$.

These representatives use the [current 3+1D formulas](../../docs/formulas/THREE_DIMENSIONAL.md)
in the geometric pairing coordinate.

| Decoration | $`n_1`$ | $`n_2`$ | $`n_3`$ | $`\widehat{\mathcal O}_5`$ | $`\widehat\nu_4`$ |
|---|---|---|---|---|---|
| p+ip | $`m_1`$ | $`0`$ | $`0`$ | $`\tfrac12m_1^5`$ | $`\tfrac14m_1^4`$ |
| Majorana | $`0`$ | $`m_1^2`$ | $`0`$ | $`\tfrac12m_1^5`$ | $`\tfrac14m_1^4`$ |
| Complex fermion | $`0`$ | $`0`$ | $`m_1^3`$ | $`0`$ | $`0`$ |
| Bosonic | $`0`$ | $`0`$ | $`0`$ | $`0`$ | $`\tfrac12m_1^4`$ |

Every row satisfies all lower obstruction equations. In particular,
$`\check\omega_2=\omega_2+s_1^2=0`$ and the second integer digit
$`\widetilde n_1`$ vanishes on the p+ip representative.
These facts do **not** make its terminal obstruction vanish: the complete
binary physical-face contribution evaluates to $`m_1^5`$, while its MS sum
and all higher-denominator terms vanish. Thus its required phase is
$`\nu_4=i^{m_1^4}`$.

For the Majorana row, the integral Bockstein of $`m_1^2`$ vanishes;
the half-valued part gives the displayed source. In the complex-fermion
row, $`\mathrm{Sq}^2(m_1^3)=\omega_2m_1^3=m_1^5`$, so the two terms cancel.
The twisted differential is

```math
d_{s_1}(q\,m_1^4)=-2q\,m_1^5.
```

Consequently, the nonzero sources in the first two rows are coboundaries
in $`U(1)_{s_1}`$: they require the displayed phase and do not obstruct
the states. Adding $`m_1^4/2`$ gives the alternative solution differing
by the bosonic root.

The [exact checker](../../scripts/check_z4ft_current_cochains.py) evaluates
all six physical contributions on **all 32 bar five-tuples**, including
tuples containing the identity. It verifies the lower equations on all
four pairs, eight triples, and sixteen four-tuples. The
[receipt](Z4fT_current_cochains.json) also records the established
self-stacking laws on all sixteen four-tuples, before removing the
integer output by its fermionic coboundary. This verifies concrete
representatives; it is not a repeated classification calculation.

The reference change is also evaluated explicitly. All four roots have
$`\mathcal B_3=\check n_2\cup_1\check n_2=0`$. The p+ip square has
$`\mathcal B_2=0`$, while the Majorana square has $`\mathcal B_2=m_1^2`$;
in the latter case $`d\mathcal B_2=0`$ and
$`(\omega_2\mathcal B_2+\mathcal B_2^2)/2=0\mod1`$.
Their complete products before the integer gauge are

| Input root | $`N_1`$ | $`N_2`$ | $`N_3`$ | $`\mathcal V_4`$ |
|---|---|---|---|---|
| p+ip | $`2m_1`$ | $`0`$ | $`0`$ | $`(-i)^{m_1^4}`$ |
| Majorana | $`0`$ | $`0`$ | $`m_1^3`$ | $`1`$ |
| Complex fermion | $`0`$ | $`0`$ | $`0`$ | $`(-1)^{m_1^4}`$ |
| Bosonic | $`0`$ | $`0`$ | $`0`$ | $`1`$ |

Removing $`N_1=2m_1`$ uses the full integer coboundary, including its phase.
These are the same root relations in $`\mathbb Z_{16}`$, checked as cochains
in the current coordinate, rather than inferred from the group order.
