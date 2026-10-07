# Archived face expansion of the 4+1D Majorana stacking formula

This is the previous fully expanded carry, retained for exact verification.
The [current principal formula](FOUR_DIMENSIONAL.md) replaces it by an
integer-carry identity, with **482 outer addends and 624 explicit expression
leaves** after counting the interiors of four protected binary lifts.
The [derivation](FOUR_DIMENSIONAL_MAJORANA_CARRY_REDUCTION.md) and
[146 lift-interior terms](FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.md) are explicit.

The archived physical-face polynomial contains exactly **5,707 terms**. Its complete coefficient set is the array `terms` in the
[coefficient table](coefficients/FOUR_DIMENSIONAL_MAJORANA_STACKING_FACES.json).
Each row is one product. Each factor gives the mathematical cochain and
the exact ordered face on the simplex (012345). Every coefficient is one
in F2. Add all rows modulo two; there are no other rows, recursions, or
implicit summations.

The cochain names in the table are the physical notation of the principal
formula. Bars mean parity, and tildes mean the second binary digit. In
particular, the second digit of the integral open Bockstein is included
where printed. Standard Bocksteins of the Majorana differential use its
binary value; that differential is closed even when the Majorana input
itself is open.

These two standard expressions are related by the exact identities

```math
d\beta^\circ\check n_3
=-\beta\overline{d\check n_3},\qquad
d\overline{\beta^\circ\check n_3}
=\overline{\beta\overline{d\check n_3}}.
```

Thus the Bockstein-of-differential factors in this table and the
differential-of-Bockstein arguments in the MS table describe the same
open-input constraint, in integer and binary coefficients respectively.
The identities follow from the definition of the open Bockstein and
$`d^2=0`$; they do not impose $`d\check n_3=0`$.

This is the fully materialized coefficient list, not an instruction to
solve for a primitive or evaluate a higher-dimensional field. The
companion [MS table](FOUR_DIMENSIONAL_MAJORANA_STACKING_WORDS.md) contains
455 additional explicitly specified ordinary MS terms. Together with
the printed two half-valued cups and twelve quarter-valued cups, the
archived expression has **6,176 terms**. This is the former count; it
is not the count of the current principal formula.
The explicitly defined lower differentials are legitimate structured
arguments of higher cochain operations. They need not be expanded into
their lower decoration fields every time they occur. Here $`d`$ denotes
the ordinary cochain differential; it is distinct from the AHSS maps
$`d_r`$. In particular, $`d\check n_3`$ is not assumed to vanish.

## Supplemental lower-equation substitution

This optional expansion checks compatibility with the lower laws. Its
term count does not replace the count of the current principal formula;
it expands the archived 6,176-term representation.

Expanding the lower equation inside each face factor produces 119,564
raw face-product occurrences. Collecting equal products modulo two
leaves 86,682 face products. The remaining standard Bocksteins retain
the whole explicitly specified two-term binary arguments.

The [complete lower-expanded manifest](coefficients/FOUR_DIMENSIONAL_MAJORANA_STACKING_LOWER_EXPANDED.json)
contains all **87,189 terms**: 486 specified ordinary MS terms, 86,682
binary face products, six other half-valued cups, and fifteen signed
quarter-valued cups. Each face product is encoded by a hexadecimal mask
into the explicitly named physical factor alphabet; bit $`i`$ selects
entry $`i`$. The ordered cup expressions are complete expression trees,
with the cup index and both arguments written at every node. Integer
Bocksteins retain their complete binary arguments.

The four extra half-valued cups are essential: they are the integer-lift
carries when the two-term binary lower equations are substituted into
the quarter-valued expression. They cannot be dropped by distributing
binary sums as integer sums.

The [standalone verification script](coefficients/verify_majorana_lower_expansion.py)
uses only these public coefficient files. It replays every lower-equation
substitution in the original 5,707-row table, collects all binary products,
compares the full 86,682-row result, checks every count, and checks all
sixteen values in the canonical-quarter carry identity. Run it with
Python 3; it has no additional dependencies.
