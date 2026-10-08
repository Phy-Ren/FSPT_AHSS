# Cartan–Adem Majorana phase in 4+1D

The pure Majorana contribution has one formula for arbitrary binary
three-cochain input. Turning on the integer decoration changes its lower
differential and introduces the accompanying mixed contribution; it does
not require a different intrinsic Majorana formula.

The current obstruction and stacking correction use the same phase
coordinate. The following fixed change relates them to the preceding
coordinate without changing the lower decorations:

{{equation:four-dimensional-majorana-phase--paired-transport--3}}

Here $`\Delta R_5`$ is evaluated on the actual lower stacking output and
then subtracts its values on the two inputs. In particular, the shifted
Majorana output contains the integer-layer correction; it is not simply
$`\check n_3+\check n'_3`$. This transport is invertible by adding the same
five-cochain. It is applied to the source and product together.

## The fixed change of phase

{{equation:four-dimensional-majorana-phase--phase-change--1}}

The finite sum has **32 MS terms**. The full half-valued bracket has
**45 terms**, and the last integer cup is one additional quarter-valued
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

For an arbitrary binary cochain, $`\beta^\circ x=(dx-\overline{dx})/2`$
uses integer arithmetic in the numerator. Its parity is the specified
open-cochain operation $`\mathrm{Sq}^1x`$. Thus every Bockstein and carry
in the compact [Majorana formula](FOUR_DIMENSIONAL.md#majorana-phase-4d)
is defined even when $`d\check n_3\ne0`$.

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
the two ordered cups involving $`d\check n_3`$ in the mixed obstruction.
The derivative term of the preceding integer quadratic cochain contributes
the third quarter cup. Their sum is

```math
\frac14\Big[
 -(\beta^\circ\check n_3)\cup_3\beta(d\check n_3)
 -(d\check n_3)\cup_1\check n_3
 +\check n_3\cup_1(d\check n_3)\Big].
```

All three cups vanish when the lower Majorana differential is zero.
In the last two cups the binary cochain $`d\check n_3`$ is lifted as a
whole; it is not the unreduced integer differential of $`\check n_3`$.
The Bockstein is defined because the binary differential is closed.

The remaining binary derivative is expanded by the ordinary differential
and composition of the MS operations. Collecting equal words gives the
**1,897-term relative polynomial** in the
[complete coefficient table](FOUR_DIMENSIONAL_MAJORANA_RELATIVE_WORD_COEFFICIENTS.md).
It is evaluated directly from that table; no old obstruction formula or
unspecified primitive is needed to define it. Its zero restriction to
$`d\check n_3=0`$ follows from the same exact closed-input dictionary.
Individual terms need not display the differential explicitly.

The term $`s_1n_4/2`$ in the phase change is essential. Its derivative
uses the complete lower equation for $`dn_4`$, so it changes both the
Majorana continuation and the pure integer contribution. The latter
therefore contains $`s_1\mathcal{𝒪}_5^\psi/2`$ in addition to $`y_6/2`$.
The fixed polynomial $`y_6`$ is unchanged. Likewise the terminal product
retains the contribution of the full lower twister through $`\Delta R_5`$.

The [exact verification receipt](data/four_dimensional_majorana_relative_verification.json)
checks every coefficient modulo four on 56 independent simplex variables,
with arbitrary open Majorana input and both closed backgrounds, and gives
zero residual. The signed quarter cups and complete binary lifts are kept
before reduction. This verifies a representative change; it does not infer
a new physical normalization from cochain closure.

The standalone [coefficient verifier](../../scripts/verify_majorana_phase_transport.py)
uses only the retained public cochain operations and coefficient files.
It also checks the 41-variable closed restriction and the literal
open-Bockstein/first-square identity. No symmetry group or numerical
classification is used in these checks.
