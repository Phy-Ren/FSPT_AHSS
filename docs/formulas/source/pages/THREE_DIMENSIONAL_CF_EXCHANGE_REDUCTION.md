# 3+1D complex-fermion exchange terms

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

The complete complex-fermion–p+ip stacking contribution on the ordered
four-simplex is

{{equation:three-dimensional--complex-fermions-and-p-ip-decoration--30}}

The two face brackets contain **13 explicit products** after distributing
the displayed binary parentheses: eight multiply $`dn_3+dR_3`$ and five multiply
$`dn'_3+dR'_3`$, with $`R_3=n_2\cup_1n_2`$. The lower differentials are
$`dn_2=\widetilde{\omega}_2[n_1]_2`$ and $`dn'_2=\widetilde{\omega}_2[n'_1]_2`$.
On identical complete inputs, the terms proportional to $`s_1(01)`$ and
the first two products cancel between the two face brackets. The remaining
expression is exactly

{{equation:three-dimensional-cf-exchange-reduction--general-3-1d-complex-fermion-exchange-reduction--2}}

These **three face products** appear in the
[self-stacking formula](THREE_DIMENSIONAL_SELF_STACKING.md).

## Exact proof

The [standalone verifier](coefficients/verify_three_dimensional_cf_exchange.py)
compares the 13-product expression with the
[normalized MS-word form](THREE_DIMENSIONAL_PRODUCT_CF_WORDS.md) of the same
exchange. Its inputs are arbitrary degree-two Majorana cochains, arbitrary
degree-three complex-fermion differentials, and a closed sign background;
all 50 independent four-simplex bits are checked at once as exact
coefficient polynomials, and the residual is identically zero.

## The obstruction

The complex-fermion–p+ip obstruction contribution is

{{equation:three-dimensional--complex-fermions-and-p-ip-decoration--13}}

The sum has **seven MS terms**, given in the
[word table](THREE_DIMENSIONAL_WORD_INDICES.md#complex-fermion-indices); their
first input is the binary cochain $`dn_3+dR_3`$. The three cups in the first
line come from the complete lower equation
$`dn_3=\mathcal{𝒪}_4^\gamma+\mathcal{𝒪}_4^{\gamma\psi}+\mathcal{𝒪}_4^\psi`$;
the two cups with $`R_3`$ come from the pairing reference and vanish for
$`n_1=0`$.

The [standalone verifier](coefficients/verify_three_dimensional_source_cf_exchange.py)
checks the seven-word form against the full word expansion on a five-simplex:
20 free Majorana faces, 15 free complex-fermion faces, ten closed-background
bits, and five closed-sign bits, all **50 independent binary variables** at once.
