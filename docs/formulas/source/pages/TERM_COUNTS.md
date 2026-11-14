# Term counts with defined lower structures

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

These counts refer to fully specified cochain expressions. A summation
sign, a named y polynomial, or a factored coefficient-table row is never counted
as one term. Every specified MS word counts once; every explicit scalar
face monomial counts once.

The primary reader-facing count retains fully defined standard lower-layer
differentials and stacking twisters as structured inputs. Each is written
completely at its own layer; higher formulas need not expand it again. A specified MS or cup term
may therefore contain those defined inputs and still count once.
This convention also retains the explicitly defined Steenrod squares and
Bocksteins. It does not turn an arbitrary y polynomial or finite sum into
one term. Every reused lower operation keeps its fully specified earlier
definition and physical contribution.

Standard Bocksteins and whole canonical lifts retain their complete
scopes; interior counts are recorded explicitly. A binary lift cannot be
distributed as an integer-linear operation. No count is asserted to be
globally minimal.
Expanded counts audit the explicit formulas; they do not measure the quality of their mathematical organization.

## Primary count with defined lower structures retained

The formulas use the common Cartan–Adem phase and its
[Majorana phase convention](FOUR_DIMENSIONAL_MAJORANA_PHASE.md).
The pure Majorana O6 has **16 terms**: 12 half-valued and four
quarter-valued terms. Its intrinsic operation contains four MS words
and one product of standard squares. The mixed source contains
**1,897 MS terms**, four other half terms, and six quarter terms,
for **1,907** in total. The pure p+ip contribution has **623,886** terms.
The complete O6 therefore has **625,828 terms** at this boundary.

For the general 4+1D Majorana twister the count is
**760 explicit expression leaves**, or **618 outer addends**.
There are 592 half-valued occurrences, 22 ordinary quarter occurrences,
and four separately reduced lifts with 5, 15, 10 and 116 interior
products. Thus 592 + 22 + 146 = 760, while 592 + 22 + 4 = 618.
The lift interiors remain inside their nonlinear scopes.

These are **uncollected expression occurrences**. Each displayed
phase-map evaluation is expanded into its complete finite expression;
its actual binary lower-output argument remains a field, just as in
other higher formulas. We do not expand that output into all of its
face coordinates or cancel terms across physical contributions.
The same boundary is used for the source and product tables below.

Physical contributions remain in the manuscript order c, c gamma,
c psi, gamma, gamma psi, psi. These labels track fermionic exchange
origins. Substituting a differential does not reassign its microscopic
origin according to the variables appearing afterward.


### Counts by layer

These primary counts retain the already defined lower obstruction and
stacking operations, their actual output fields, the standard differential,
Sq and Bockstein operations, Delta, the existing integer carries, the
defined integral quadratic cochain and the fixed integer Pontryagin
representative. Explicit linear parentheses and
arbitrary coefficient polynomials are expanded. The counts describe this
stated expression, not a normal form obtained by flattening all operations.
Whole nonlinear lifts retain their scopes; their interior terms are
listed in the [structured count ledger](term_census/STRUCTURED_TERM_COUNTS.json).

| Dimension | Law | c | c gamma | c psi | gamma | gamma psi | psi | Total |
|---|---|---:|---:|---:|---:|---:|---:|---:|
| 2+1D | O2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2+1D | O3 | 0 | 0 | 0 | 2 | 0 | 0 | 2 |
| 2+1D | O4 | 3 | 1 | 0 | 7 | 0 | 0 | 11 |
| 2+1D | E1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 2+1D | E2 | 0 | 0 | 0 | 2 | 0 | 0 | 2 |
| 2+1D | E3 | 3 | 2 | 0 | 20 | 0 | 0 | 25 |
| 3+1D | O2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3+1D | O3 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 3+1D | O4 | 0 | 0 | 0 | 3 | 2 | 5 | 10 |
| 3+1D | O5 | 3 | 4 | 15 | 15 | 2,281 | 11,416 | 13,734 |
| 3+1D | E1 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 3+1D | E2 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 3+1D | E3 | 0 | 0 | 0 | 2 | 5 | 13 | 20 |
| 3+1D | E4 | 3 | 4 | 73 | 43 | 16,059 | 10,583 | 26,765 |
| 4+1D | O3 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4+1D | O4 | 0 | 0 | 0 | 0 | 0 | 2 | 2 |
| 4+1D | O5 | 0 | 0 | 0 | 3 | 2 | 13 | 18 |
| 4+1D | O6 | 3 | 4 | 12 | 16 | 1,907 | 623,886 | 625,828 |
| 4+1D | E2 | 0 | 0 | 0 | 0 | 0 | 0 | 0 |
| 4+1D | E3 | 0 | 0 | 0 | 0 | 0 | 1 | 1 |
| 4+1D | E4 | 0 | 0 | 0 | 2 | 5 | 27 | 34 |
| 4+1D | E5 | 3 | 13 | 2 | 760† | 5,685,587 | 2,869,266 | 8,555,631† |

† The Majorana entry counts the 146 explicit products inside its four
canonical lifts, as explained above: 760 expression leaves, not 760
linearly distributed phase addends. Counting those four lifts as outer
addends instead gives 618 for this contribution and 8,555,489 for E5.
Other entries retain their declared standard-operation and whole-lift
boundaries, with their interior counts separately listed in the ledger.

The integral quadratic cochain has three defining cups and a four-cup
addition polarization. Reusing it in the O6 quarter phases contributes one operation
in the pure p+ip part and three in the mixed difference. The compact
Majorana quarter phase instead displays its four terms explicitly.
Its complete definition and exact identities appear in the
[quadratic-cochain appendix](QUADRATIC_REFINEMENTS.md).

Every defined lower operation is specified at its own layer; reuse does
not make its definition disappear from this ledger. A finite MS or face
sum still contributes every listed term. The expanded 4+1D stacking
counts below use further lower-law substitutions and collect equal
normalized operations. Their numbers are not substitutes for this primary
boundary.

## Counting the phase-convention terms

The five-cochain $`B_5[n_3]`$ has 44 half-valued terms and one
quarter-valued term, **45** in total. It and its 32-word index set are
printed on the
[Majorana phase page](FOUR_DIMENSIONAL_MAJORANA_PHASE.md#the-five-cochain-b_5).
It is not counted as one term.

| General contribution | $`B_5`$ evaluations | Additional lower twister terms | Occurrences |
|---|---:|---:|---:|
| gamma | 3 | 1 | 136 |
| gamma psi | 3 | 1 | 136 |
| psi | 1 | 1 | 46 |

The $`B_5`$ arguments are the actual complete lower outputs specified in
[the general product](FOUR_DIMENSIONAL.md#eq-t4c). A binary sum used as an
output is retained as that field before a word is evaluated. Consequently
these counts mean 3 × 45 + 1, 3 × 45 + 1, and 45 + 1 occurrences in the
printed expressions; they are not a fully distributed or collected
polynomial in independent input bits. They include every $`B_5`$ term.
The carry reduction is retained inside this product,
with its four protected lift interiors counted separately.

The shared 3+1D Adem expression contributes **four MS terms**;
its reuse does not change the **15-term** pure Majorana O5 count.

## Self-stacking counts (separate domains)

These restrictions have their own pages and do not replace the general
counts above. Every input is a complete state with its allowed upper
completions. The integer output is retained before full gauge reduction.

| Dimension and scope | c | c gamma | c psi | gamma | gamma psi | psi | Complete terminal twister |
|---|---:|---:|---:|---:|---:|---:|---:|
| 2+1D, zero integer decoration | 1 | 1 | 0 | 6 | 0 | 0 | **8** |
| 3+1D, zero p+ip | 1 | 1 | 0 | 8 | 0 | 0 | **10** |
| 3+1D, canonical torsion p+ip | 1 | 3 | 16 | 14 | 1,144 | 250 | **1,428** |
| 4+1D, arbitrary permitted p+ip | 1 | 10 | 2 | 202 | 3,613,699 | 793,729 | **4,407,643 outer terms** |

The 3+1D open-Majorana entry has one whole lift with two interior terms;
counting that interior gives 14 leaves for the contribution and 1,415 for
the complete canonical torsion twister. The outer count remains 1,428.

The 4+1D Majorana entry has four protected lifts containing 106 products.
Replacing only those four wrappers by their interiors gives 304 expression
leaves for that contribution and 4,407,745 for the corresponding total.
The full restricted mixed and pure finite sums contain 3,613,517 and
793,669 terms. Their nonlinear interiors and lower-operation argument
arrays are recorded separately in the coefficient indices. The zero-p+ip 4+1D sector uses the restriction of this same
expression, written in the physical occupation $`n_4`$, with the lower fields specified on its
[dedicated page](FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md); there only the quarter-valued
terms carry the opposite sign.
No alternative closed-diagonal formula is counted as another law.
For the full self-stack, the $`B_5`$ terms add two Majorana terms,
one mixed term, and 46 pure p+ip occurrences at the same boundary.

The complete lower self-twister counts are: 2+1D E2 has two terms;
3+1D E2 has one, and E3 has seven for a general signed integer input;
4+1D E3 has one term, and E4 has
fourteen terms. The 3+1D canonical torsion branch has a vanishing pure
p+ip E3 contribution and retains its open-Majorana differential.

See the separate [2+1D](TWO_DIMENSIONAL_SELF_STACKING.md),
[3+1D](THREE_DIMENSIONAL_SELF_STACKING.md), and
[4+1D](FOUR_DIMENSIONAL_SELF_STACKING.md) laws and their exact certificates.

## 4+1D bosonic stacking: expanded boundaries

The c, c gamma and c psi contributions have respectively **75**, **2,216**
and **3,262** terms after substituting their actual lower laws and output
fields and collecting equal typed operations.

The carry-reduced Majorana coefficient part preserves its four whole
lifts and contributes 624 leaves before the $`B_5`$ terms. The
$`B_5`$ terms add 136 explicit occurrences, giving the 760-leaf entry
above.

The complete mixed finite sum has **5,684,189 terms**,
and the complete pure p+ip finite sum has **2,869,198 terms**.
Including the other displayed contributions and the explicitly expanded $`B_5`$ terms give **8,555,631 expression
occurrences** for E5, with the Majorana lift-interior convention
marked by † in the table. Every coefficient
is supplied in the [stacking coefficient appendix](FOUR_DIMENSIONAL_STACKING_COEFFICIENTS.md).
The exact collection includes all source and tensor contributions; these
are term lists, not counts of construction steps.

The mixed and pure sums respectively have 58,547 and 35,550 distinct
nonlinear-interior terms, with 448,864 and 54,840 appearances when those
interiors and the explicit operation arguments are written inline. The
definitions of the reused lower operations remain intact. The interiors
are listed separately because a whole
canonical lift or exact quotient cannot be distributed as an ordinary
linear sum. Reused lower differentials and twisters retain their full
earlier definitions.

## Self-stacking is counted separately

These formulas take two identical complete input states. Their restricted
counts do not replace the general two-input totals above. Both retain the
complex-fermion completion and the incoming bosonic phase.

| Dimension and input | c | c gamma | gamma | Complete phase correction |
| --- | ---: | ---: | ---: | ---: |
| [3+1D, zero p+ip decoration](THREE_DIMENSIONAL_MAJORANA_SELF_STACKING.md) | 1 | 1 | 8 | **10** |

The 3+1D correction has seven half-valued and three quarter-valued
terms. It is in exactly the same representative as the general formula.
The 4+1D zero-p+ip case instead uses the restriction of the common
self-stacking law counted above, written in the physical occupation $`n_4`$. Its lower equation and full
phase convention are given on the [restriction page](FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md).

## Representation and verification

The c gamma expressions reuse the complete lower Majorana parity, and
the c psi products reuse the existing Delta. Both reuses preserve the
complete contributions exactly, including open-cochain differential and
actual output terms. The quadratic-cochain reuse is also an exact identity.

The Majorana stacking coefficient uses the
[output gauge](FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md).
The carry reduction rewrites that coefficient part exactly. The
Cartan–Adem presentation then applies the explicit terminal phase change
to the complete obstruction and product together; its contribution is
included in every count above.

Standard integer lifts and divisions retain their scopes throughout.
In particular, a binary numerator with two summands has canonical integer
value x+y-2xy; using x+y in a quarter-valued expression would lose a
half-valued contribution. The face-expansion Majorana replay explicitly checks
all sixteen local carry cases. Its independent comparison passed for
512 arbitrary open input pairs and 128 valid lower physical towers.
The [carry replay](coefficients/verify_majorana_carry_reduction.py)
compares the reduced expression with the 5,707-term face
polynomial while retaining all four nonlinear lift boundaries. The
independent 1,024-input readback passed; these input checks corroborate
the exact signed-carry identity rather than replacing its derivation.
