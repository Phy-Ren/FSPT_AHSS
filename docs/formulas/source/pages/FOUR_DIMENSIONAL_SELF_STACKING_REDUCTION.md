# Cochain identities in the 4+1D self-stacking formula

Two exact identities simplify the complete equal-input expression while
preserving its obstruction, stacking representative, and physical labels.
Both use existing lower-layer operations with their original domains.

## Open Majorana cochains

For every binary degree-three cochain,

{{equation:four-dimensional-self-stacking-reduction--open-majorana-cochains--1}}

These are cochain identities, including the differential terms in the
Steenrod square. They do not require $`d\check n_3=0`$.
Using these relations and the closed-background equations, the earlier
218 MS terms in the self-stacking coefficient have the following exact
pointwise replacement:

{{equation:four-dimensional-self-stacking-reduction--open-majorana-cochains--2}}

This sum has **187 individually specified operations**, all printed in
the [current word table](FOUR_DIMENSIONAL_SELF_STACKING_WORDS.md).
The two additional half-valued face products and all quarter-valued
terms are unchanged. Thus the complete open-Majorana self contribution
has **200 outer terms instead of 231**, or **302 instead of 333** when
its unchanged 106 canonical-lift interior terms replace the four lift
wrappers in the occurrence count.

The [standalone coefficient proof](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/verify_open_half_reduction.py)
checks the original 218 operations against the new 187 operations on all
thirty independent open-cochain/background face variables. The
[exact receipt](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/OPEN_HALF_UNIVERSAL_CHECK.json)
and [independent 512-case native replay](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/OPEN_HALF_NATIVE_CHECK.json)
record zero remainder. These checks establish equality of the displayed
cochains, not merely their cohomology classes. No output gauge is added.

## The lower obstruction inside the fractional correction

On the actual lower tower, the integer derivative of the existing
Majorana carry is fixed by the lower obstruction:

{{equation:four-dimensional-self-stacking-reduction--the-lower-obstruction-inside-the-fractional-correcti--3}}

Here $`\beta`$ is the ordinary integer Bockstein of a closed binary
cochain. Its input is closed because
$`\check{\mathcal{𝒪}}_4[n_2]=d\check n_3`$ on this tower.
For an arbitrary binary cochain, the defining integer identity is

{{equation:four-dimensional-self-stacking-reduction--the-lower-obstruction-inside-the-fractional-correcti--4}}

where the unbarred differential is taken over the integers on the
canonical input values, and the whole bar gives its binary reduction
before the integer subtraction. Applying $`d`$ and using $`d^2=0`$ proves the stated carry
identity. Thus the quarter-valued self-stacking term can be written

{{equation:four-dimensional-self-stacking-reduction--the-lower-obstruction-inside-the-fractional-correcti--5}}

This directly reuses the lower obstruction and introduces no new
polynomial or gauge. The term count is unchanged. The open-cochain
formula with $`dB_4^\gamma`$ remains valid without imposing the lower
tower, while its right-hand expression uses the stated physical equation.

## Reusing the integer-only carry

The integer carry was defined on arbitrary binary degree-three inputs by

{{equation:four-dimensional-self-stacking-reduction--reusing-the-integer-only-carry--6}}

Its zero-input specialization is therefore an exact integral identity:

{{equation:four-dimensional-self-stacking-reduction--reusing-the-integer-only-carry--7}}

Every binary digit of these equal integer cochains agrees. This statement
needs no separate lower-tower equation for $`x=0`$; it uses the open-domain
definition rather than an on-tower quotient with a substituted differential.

Applying this identity to every complete argument in the finite
self-stacking coefficients identifies 112 previously distinct factor values
in the Majorana–p+ip coefficient. Exact binary collection then gives
**3,613,517 outer summands instead of 3,613,999**, removing 482 summands.
The pure p+ip coefficient remains **793,669 summands**. Its 94 redundant
factor definitions are removed, but that is not a reduction in its outer
term count.

Every protected integer numerator is transformed within its original
modulus and reduction scope. The same rule is applied to ordinary
cochain differentials of the carries. No lift is distributed as integer
addition and no microscopic contribution is reassigned by variable support.
The [normalization script](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/normalize_integer_carries.py)
and [complete updated tables](FOUR_DIMENSIONAL_SELF_STACKING_COEFFICIENTS.md)
make this reduction reproducible.

These are finite improvements, not a claim that the two large remaining
coefficient sums are optimally organized. They remain explicit verification
data for further structural reduction.
