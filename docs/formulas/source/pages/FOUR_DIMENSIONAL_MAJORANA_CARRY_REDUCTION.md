# Why the complete Majorana carry becomes smaller

The revised four-dimensional formula is exactly the previous open-cochain
representative. Its 5,707-term binary carry can be replaced before expanding
the second binary digit. The result has two half-valued face products,
seven additional ordinary quarter-valued terms, and four separately lifted
binary polynomials. Their interiors contain 146 terms.

The following notation is local to this proof. Write

{{equation:four-dimensional-majorana-carry-reduction--why-the-complete-majorana-carry-becomes-smaller--1}}

Here $`A,A'`$ are binary differentials, canonically lifted in integer
arithmetic. Thus $`dB=-r`$, $`dB'=-r'`$, and $`dX=-(r+r')`$.
All higher cups below are signed integer cups.

The old integer numerator before taking its second digit is

{{equation:four-dimensional-majorana-carry-reduction--why-the-complete-majorana-carry-becomes-smaller--2}}

A signed cup identity gives

{{equation:four-dimensional-majorana-carry-reduction--why-the-complete-majorana-carry-becomes-smaller--3}}

This is an integer identity, including the canonical carry
$`\beta(A+A')=r+r'-dJ`$. It has been verified by complete integer
coefficient comparison, not only modulo two.

Let $`H_{\mathbb Z}`$ be the signed integer version of the fixed normalized
Eilenberg–Zilber homotopy used to construct the original coefficient. It
satisfies $`dH_{\mathbb Z}+H_{\mathbb Z}d=1-\mathrm{AW}`$ and reduces to
the original binary homotopy, denoted below by $`H`$. Here $`\mathrm{AW}`$
denotes the full shuffle–Alexander–Whitney projection onto the tensor
model and back. For these particular cochains,

{{equation:four-dimensional-majorana-carry-reduction--why-the-complete-majorana-carry-becomes-smaller--4}}

The first equality follows by evaluating every normalized contribution;
each vanishes. The second also follows from normalization on the two
original degree-three input axes: their relative tensor starts in degree
six, above the degree-five cochain $`F`$. Consequently no new output gauge,
ordinary or twisted, remains in this reduction.

For every integer $`P`$,
$`\widetilde P/2=(P-\bar P)/4\pmod1`$. The preceding identity therefore
gives

{{equation:four-dimensional-majorana-carry-reduction--why-the-complete-majorana-carry-becomes-smaller--5}}

In $`HQ`$, the integer $`Q`$ is first reduced modulo two; the following
identity is an identity of binary cochains. Its terms are explicit:

{{equation:four-dimensional-majorana-carry-reduction--why-the-complete-majorana-carry-becomes-smaller--6}}

{{equation:four-dimensional-majorana-carry-reduction--why-the-complete-majorana-carry-becomes-smaller--7}}

Finally, $`-H_{\mathbb Z}\bar P`$ is exactly the four signed canonical
lifts in the [complete coefficient table](FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.md).
Substituting $`L=-\lambda_3^\gamma`$ and $`J=-\lambda_4^\gamma`$ yields
the revised physical formula. Whole binary lifts are retained throughout;
$`P`$ itself need not be even.

The [standalone integer-chain certificate](coefficients/verify_majorana_signed_transfer.py)
checks the signed chain identity and normalization exactly through the
required degrees. The complete phase passes 1,024 arbitrary open-input
checks against the original frozen formula and its existing gauge. An
independent native-cochain implementation checks the signed reduction
without using its scalar compiler. The public
[standalone replay](coefficients/verify_majorana_carry_reduction.py) compares
the new expression with the archived 5,707-term table on 512 arbitrary open
inputs, exercises all sixteen lift patterns, and covers all four quarter
residues with the unchanged terms. The
[public receipt](coefficients/FOUR_DIMENSIONAL_MAJORANA_CARRY_REPLAY.json)
records the coefficient-file hashes and counts.
