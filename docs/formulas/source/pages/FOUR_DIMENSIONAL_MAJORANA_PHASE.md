# The Majorana phase convention in 4+1D

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

The pure Majorana contribution has one formula for arbitrary binary
three-cochain input. Turning on the integer decoration changes its lower
differential and introduces the accompanying mixed contribution; it does
not require a different intrinsic Majorana formula.

The obstruction and the stacking law use one phase convention. It is
fixed by the five-cochain $`B_5[n_3]`$ below together with the half term
$`\tfrac12s_1n_4`$. The obstruction contains their differential:
the relative Majorana–p+ip terms and the term $`s_1\mathcal{𝒪}_5^\psi/2`$.
The stacking law contains their values on the stacked state minus the values
on the upper and lower states: the three $`B_5`$ evaluations and the terms
$`-s_1\mathcal{ℰ}_4/2`$. The $`B_5`$ evaluations use the actual lower fields
of the stacked state, whose $`N_3`$ contains the integer-layer twister and is
not simply $`n_3+n'_3`$.

## The five-cochain $`B_5`$

{{equation:four-dimensional-majorana-phase--phase-change--1}}

The finite sum has **32 MS terms**. The full half-valued bracket has
**44 terms**, and the last integer cup is one additional quarter-valued
term. That quarter cup is formed over the integers from the individual
binary field values; it is not the lift of a reduced whole cup.

Every word in $`\mathcal W_5`$ has the same four ordered inputs displayed
above, and coefficient one modulo two:

```text
12131412324 12131412343 12131434241 12134313234
12134313242 12134341423 12321414232 12321414342
12323431412 12324214131 12324241314 12343232141
12123412343 12123431243 12131242341 12131423241
12134121343 12134121434 12134312143 12134312343
12134312423 12321242341 12324213431 12324231342
12324241341 12343121234 12343121343 12343132341
12343134321 12134132341 12324214231 12341343231
```

## Why the pure contribution stays compact

For an arbitrary binary cochain, $`\beta^- x=(dx-[dx]_2)/2`$
uses integer arithmetic in the numerator. Its parity is the specified
open-cochain operation $`\mathrm{Sq}^1x`$. Thus every Bockstein and carry
in the compact [Majorana formula](FOUR_DIMENSIONAL.md#majorana-phase-4d)
is defined even when $`dn_3\ne0`$.

Its intrinsic and Cartan polynomials are fixed operations:

{{equation:four-dimensional-majorana-phase--intrinsic--1}}

The first line contains **four MS terms**; the last line is the product
of the already defined first squares.

{{equation:four-dimensional-majorana-phase--cartan--2}}

Each Cartan operation contains **one MS term**. The cochains need not be
cocycles for these evaluation formulas to make sense. Their familiar
closed-input identities acquire the required differential corrections
when the input becomes open.

## The relative correction and its proof

Differentiate the displayed five-cochain using the signed integral cup
identity. On writing the original binary field differential as its binary
value plus twice the open Bockstein, its quarter part contributes exactly
the two ordered cups involving $`dn_3`$ in the mixed obstruction.
The derivative term of the preceding integer quadratic cochain contributes
the third quarter cup. Their sum is

```math
\frac14\Big[
 -(\beta^-n_3)\cup_3\beta(dn_3)
 -(dn_3)\cup_1n_3
 +n_3\cup_1(dn_3)\Big].
```

All three cups vanish when the lower Majorana differential is zero.
In the last two cups the binary cochain $`dn_3`$ is lifted as a
whole; it is not the unreduced integer differential of $`n_3`$.
The Bockstein is defined because the binary differential is closed.

The remaining binary derivative is expanded by the ordinary differential
and composition of the MS operations. Collecting equal words gives the
**1,897-term relative polynomial** in the
[complete coefficient table](FOUR_DIMENSIONAL_MAJORANA_RELATIVE_WORD_COEFFICIENTS.md).
It is evaluated directly from that table; no old obstruction formula or
unspecified primitive is needed to define it. Its zero restriction to
$`dn_3=0`$ follows from the same exact closed-input dictionary.
Individual terms need not display the differential explicitly.

The half term $`\tfrac12s_1n_4`$ is essential. Its derivative is
$`\tfrac12s_1\mathcal{𝒪}_5`$ by the lower equation $`dn_4=\mathcal{𝒪}_5`$, so it
enters both the Majorana continuation and the pure integer contribution. The
latter therefore contains $`s_1\mathcal{𝒪}_5^\psi/2`$ in addition to $`y_6/2`$.

The [exact verification receipt](data/four_dimensional_majorana_relative_verification.json)
checks every coefficient modulo four on 56 independent simplex variables,
with arbitrary open Majorana input and both closed backgrounds, and gives
zero residual. The signed quarter cups and complete binary lifts are kept
before reduction. It does not infer a physical normalization from cochain closure.

The standalone [coefficient verifier](../../scripts/verify_majorana_phase_transport.py)
uses only the retained public cochain operations and coefficient files.
It also checks the 41-variable closed restriction and the literal
open-Bockstein/first-square identity. No symmetry group or numerical
classification is used in these checks.

<a id="microscopic-heptagon-table"></a>

## Comparison with the microscopic phase tables

The cochain $`B_5`$ above is distinct from the local phase-reference cochain
$`B_5^\gamma`$ of this section.

With the moves and insertions of the
[phase convention](../FORMULA_GUIDE.md#phase-convention), the forward F move
carries $`\nu_5`$, the heptagon loop runs forward along the three moves with odd
omitted vertex ($`012346,012456,023456`$) and back along the four moves with
even omitted vertex, and the inserted Majoranas act as $`X=P\Gamma`$ on forward
moves and $`\bar X=\bar P\Gamma^\dagger`$ on inverse moves, with
$`\Gamma=g_{1235A}^{\,d}g_{0123B}^{\,c}g_{1234B}^{\,b}g_{2345B}^{\,a}`$. On every
parity-changing transition loop the first of $`g_{2345B},g_{1234B},g_{0123B},g_{1235A}`$
lying on the loop is inserted; the rule covers every loop. The microscopic
heptagon phase then satisfies, pointwise,

```math
\mathcal O_6^\gamma=\mathcal O_{\mathrm{CA}}+d_{s_1}B_5^\gamma,
```

where $`\mathcal O_{\mathrm{CA}}`$ is the
[closed-Majorana Cartan–Adem polynomial](MAJORANA_AND_ENDPOINTS.md#eq-m4-4d),
with quarter-valued bracket $`-1/4`$, and $`B_5^\gamma`$ is the explicit local
phase-reference cochain obtained with the microscopic tables. The microscopic
table has 33,554,432 rows ($`n_3`$ with general closed $`\omega_2,s_1`$). The
identity holds on all of them: it is checked directly on 30,000 random
configurations and holds row by row through the exact rephasing of the F move
relative to the earlier table.

The stacking amplitudes use the same F moves. The $`\mathcal P`$ moves use the same
rule with the candidates $`g'_{1234B},g'_{0134B},g'_{0124A}`$, acting in this
order. With the root complex-fermion twisters,
$`d_{s_1}(\mathcal{ℰ}^c+\mathcal{ℰ}^{c\gamma}+\mathcal{ℰ}^\gamma)
=\mathcal O_6[N]-\mathcal O_6[n]-\mathcal O_6[n']`$ holds pointwise for every one
of the 8,388,608 stacking rows with general closed $`\omega_2,s_1`$. Each row is
checked on its own six-simplex. The microscopic tables themselves are not part
of this repository.
