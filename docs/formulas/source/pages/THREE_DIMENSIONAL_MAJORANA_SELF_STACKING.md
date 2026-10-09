# Self-stacking in 3+1D with no p+ip decoration

The current complex-fermion coordinate is the geometric pairing occupation.
Use $`\check n_3=n_3+n_2\cup_1n_2`$ in the phase blocks below.
The point-fermion phase includes $`(\omega_2n_2+n_2^2)/2`$ from the output reference conversion.
The old ten-term coefficient certificate is a retained kernel, not the complete current phase.

Take a complete state with $`n_1=0`$, closed binary Majorana cochain
$`n_2`$, binary complex-fermion cochain $`n_3`$, and additive phase
$`\widehat\nu_4`$. The input satisfies the obstruction equations in the
[3+1D formula section](THREE_DIMENSIONAL.md), including
$`dn_3=\mathcal{𝒪}_4^\gamma[n_2]`$. The backgrounds are shared by both
copies. The restriction is **zero p+ip decoration**, not merely a closed
Majorana cochain inside a state with nonzero p+ip decoration.

The maintained transported formula is in the
[complete self-stacking reference](THREE_DIMENSIONAL_SELF_STACKING.md#4-bosonic-self-stacking-with-zero-pip-input).
This appendix proves that specialization. Its output includes the complete
complex-fermion completion and phase; subsequent root relations still use
all lower gauge corrections. The quarter-valued obstruction always means
the lift of its whole binary value.

## Why the intrinsic word terms disappear

For a closed binary degree-two cochain $`x`$, the seven intrinsic terms
in the main formula obey

{{equation:three-dimensional-majorana-self-stacking--why-the-intrinsic-word-terms-disappear--8}}

This is the exact cancellation of **seven MS terms**, with no coboundary
removed. The remaining intrinsic binary terms reduce using

{{equation:three-dimensional-majorana-self-stacking--why-the-intrinsic-word-terms-disappear--9}}

This identity has **three specified terms**. The other copy of
$`\overline{\beta x}\cup_1x/2`$ cancels the half-valued reduction of
$`(\beta x)\cup_1x/2`$ in the integer part.

Finally, for three binary degree-four cochains, their three pairwise
pointwise products give exactly the carry between the integer sum of
individual values and the canonical value of their binary sum, modulo
one after division by two. Apply this to
$`n_2^2`$, $`\omega_2n_2`$, and
$`s_1\overline{\beta n_2}`$. Their binary sum is the already defined
$`\mathcal{𝒪}_4^\gamma`$. This accounts for the whole obstruction in the
quarter bracket without dropping its carry.

The [standalone symbolic verifier](coefficients/verify_three_dimensional_majorana_self_stacking.py)
checks these identities and the retained ten-term kernel using exact Boolean and
integer coefficient polynomials, rather than selected group examples.
It treats all closed Majorana and background inputs on an ordered
four-simplex and every compatible complex-fermion completion.
