# General 3+1D complex-fermion exchange reduction

The complete complex-fermion–p+ip contribution can be written as follows
on the ordered four-simplex, with the already defined lower outputs and
obstruction representatives:

{{equation:three-dimensional--complex-fermions-and-p-ip-decoration--30}}

The two face brackets contain **13 explicit products** after distributing
the displayed binary parentheses: eight multiply $`dn_3`$ and five multiply
$`dn'_3`$. They replace the entire previous **132-term MS sum** exactly.
The lower differential arguments retain their meanings:
$`d\check n_2=\check\omega_2\bar n_1`$ and
$`d\check n'_2=\check\omega_2\bar n'_1`$.
The two former $`P_4`$ terms have also been eliminated. Their eight-word
operation satisfies the exact identity

{{equation:three-dimensional-cf-exchange-reduction--general-3-1d-complex-fermion-exchange-reduction--4}}

Thus the rewritten contribution uses the already defined lower obstruction
rather than an additional polynomial operation. This identity holds for
arbitrary binary $`x`$ and $`z`$ of degrees two and three.
The argument $`\check n_2+\check n'_2`$ inside
$`\mathcal{𝒪}_4^\gamma`$ is the **complete binary sum**. The nonlinear
obstruction must not be replaced by the sum of its values on the two inputs.

This is an identity of binary cochains, so multiplying it by $`1/2`$ changes
neither the phase representative nor the obstruction. The physical
$`c\psi`$ assignment is unchanged. No lower-field substitution is made in
$`dn_3`$ or $`dn'_3`$; these are the complete parity obstructions for their
respective states.

On identical complete inputs, the terms proportional to $`s_1(01)`$ and
the first two products cancel between the two brackets. The remaining
expression is exactly

{{equation:three-dimensional-cf-exchange-reduction--general-3-1d-complex-fermion-exchange-reduction--2}}

These **three face products** are the self-stacking correction already
used in the separate self-stacking formula.

## Exact proof and count impact

The [standalone verifier](coefficients/verify_three_dimensional_cf_exchange.py)
embeds all 132 original normalized MS words and compares them with the
13-product expression. The inputs are arbitrary degree-two Majorana
cochains, arbitrary degree-three complex-fermion cochains, and a closed
sign background. The complete combined check includes all 50 independent four-simplex bits
for both inputs, both backgrounds, and an arbitrary lower stacking carry,
and checks both $`P_4`$ evaluations on the actual output. These are checked at once
as exact coefficient polynomials; the residual is identically zero.
No group sampling, new cocycle choice, gauge, or coefficient fit is used.
The original [132-word table](THREE_DIMENSIONAL_PRODUCT_CF_WORDS.md) remains
a verification record.

With the same declared structured counting boundary as the general
reference, this reduces the complete $`c\psi`$ contribution from **202 to
29 terms** and the complete 3+1D bosonic twister from **26,894 to 26,721
terms**. The reduction is 173 terms. The count is two initial lower/Delta terms,
13 physical-face products, and 14 terms in the retained lower-obstruction
part. In that last part the two individual lower-obstruction evaluations
count once each, $`\check N_2^2`$ contributes one term, and
$`(\check n_2+\check n'_2)^2`$ contributes four; the two derivatives
$`dn_3+dn'_3`$ give $`2(2+1+4)=14`$. The nonlinear obstruction
evaluations keep their complete arguments. No linearization is used. This product reduction leaves the source and every other physical
contribution unchanged. The additional source reduction is given below. Fully substituted archival counts remain
records of their original expression basis and must not be relabeled as
new minimal counts.


## Source exchange through the lower differential

The complete source contribution is

{{equation:three-dimensional--complex-fermions-and-p-ip-decoration--13}}

The sum has **seven MS terms**, given in the
[word table](THREE_DIMENSIONAL_WORD_INDICES.md#complex-fermion-indices).
Together with the three displayed cups, the complete contribution has
**ten terms**, reduced from 30. The two independent reductions are:

- The former 25-word correction equals seven MS words whose arguments
  contain $`dn_3`$, $`d\check n_2`$, and the backgrounds. This identity
  holds for arbitrary binary $`\check n_2`$ and $`n_3`$ with closed
  $`\omega_2`$ and $`s_1`$; no lower source equation is imposed.
- The remaining five cups become three by substituting the complete
  lower equation $`dn_3=\mathcal{𝒪}_4^\gamma+
  \mathcal{𝒪}_4^{\gamma\psi}+\mathcal{𝒪}_4^\psi`$ and cancelling two
  identical binary terms. The separate pure-p+ip cup must remain.

This expresses the fermionic exchange through the lower parity
obstructions. Its physical $`c\psi`$ origin is unchanged even though
substituting $`dn_3`$ introduces other lower decorations.

The [standalone verifier](coefficients/verify_three_dimensional_source_cf_exchange.py)
embeds both word lists and compares every coefficient on a five-simplex:
20 free Majorana faces, 15 free complex-fermion faces, ten closed-background
bits, and five closed-sign bits. Both the $`\omega_2`$ and $`s_1`$
parts agree identically on all **50 independent binary variables**.
Multiplication by $`1/2`$ therefore preserves the entire phase, not only
its cohomology class. No paired coordinate transport is needed.

The general 3+1D bosonic obstruction consequently falls from **13,749 to
13,729 terms**. This source count is independent of the product reduction
above; the large mixed and pure p+ip blocks are still separate targets.
