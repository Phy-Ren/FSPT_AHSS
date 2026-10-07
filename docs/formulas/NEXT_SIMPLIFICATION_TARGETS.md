# Further formula simplification

The [Majorana carry reduction](FOUR_DIMENSIONAL_MAJORANA_CARRY_REDUCTION.md)
is an exact replacement in the existing representative. The
[28-term closed diagonal](FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md) has an
explicit output coboundary relating it to that representative. The
[quadratic cochain](QUADRATIC_REFINEMENTS.md) organizes repeated fractional
terms and supplies an exact variation law. These are established results;
the targets below are proposed further reductions.

## Current targets in 4+1D

| Contribution | Current terms |
| --- | ---: |
| $`\widehat{\mathcal O}_6^{\gamma\psi}`$ | 1,012, including 1,005 MS terms |
| $`\widehat{\mathcal O}_6^\psi`$ | 623,885 |
| $`\widehat{\mathcal E}_5^{\gamma\psi}`$ | 5,685,535 |
| $`\widehat{\mathcal E}_5^\psi`$ | 2,869,220 |

## Current targets in 3+1D

| Contribution | Current terms |
| --- | ---: |
| $`\widehat{\mathcal O}_5^{\gamma\psi}`$ | 2,281 |
| $`\widehat{\mathcal O}_5^\psi`$ | 11,416 |
| $`\widehat{\mathcal E}_4^{\gamma\psi}`$ | 16,059 |
| $`\widehat{\mathcal E}_4^\psi`$ | 10,583 |

These use the current [displayed-expression counting boundary](TERM_COUNTS.md):
defined lower operations and the quadratic cochain remain structured
inputs, while finite coefficient sets are fully enumerated. Whole
canonical lifts have separately recorded interior counts. Thus the
4+1D pure-source total includes the quadratic cochain as a structured
operation with its three defining terms stated explicitly; it does not
treat its 623,880-term finite completion as one term.

## A smaller target for group reconstruction

The [root-power presentation theorem](ROOT_POWER_PRESENTATIONS.md)
identifies which products determine the abstract abelian group. In 3+1D,
a basis adapted to the single possible distinguished Majorana target
allows all Majorana and p+ip terminal products in that reconstruction to
be self-stacking specializations. Complete gauges and CF/bosonic reduction
remain part of the algorithm. The full two-input formulas remain available.

The complete [zero-p+ip 3+1D self-stack](THREE_DIMENSIONAL_MAJORANA_SELF_STACKING.md)
now has ten terms in the current phase representative. The remaining
finite p+ip root, when present, can be chosen with $`n_1=s_1`$. This fixes
a much smaller specialization to simplify next, while retaining the
actual open Majorana field, CF completion, and integer-output gauge.

In 4+1D, general cyclic p+ip orders and several lower target vectors
require a broader construction. The closed-Majorana diagonal is already
small, but it does not replace cyclic powers with nonzero p+ip decoration.

## Proposed reductions

1. **The 4+1D Majorana–p+ip source and product.** The source still contains
   1,005 specified MS terms, and its stacking coefficient set is the
   largest remaining block. Separate the already determined integral
   quadratic polarization from the binary correction. Then seek a direct
   polarization of that binary correction in the defined lower
   obstructions and stacking twisters. The required result is a coupled
   source/product identity, including the open Majorana differential;
   a formula valid only for closed Majorana inputs would not replace this
   block.

2. **The pure p+ip completion and its stacking difference.** The expanded
   obstruction completion contains 623,880 physical-face monomials.
   Work with its integer polynomial structure before taking binary
   digits: use generalized binomial identities, signed cup identities,
   and the existing integer carries. Simplify the source together with
   its stacking difference so that canonical-lift carries remain
   accounted for. A candidate must preserve the complete fractional
   phase, including negative integer decorations, rather than only its
   binary derivative.

3. **The four remaining Majorana lift interiors.** Their 146 explicit
   products provide a small, bounded target. Test factorization into
   the already defined differential, Bockstein, and overlap carries
   before expanding the whole binary lifts. Any factorization must
   reproduce each lift separately with its stated integer sign.

4. **Cross-dimensional reuse.** Apply the
   [coboundary/stacking compatibility](COBOUNDARY_STACKING_COMPATIBILITY.md)
   to related 3+1D and 4+1D expressions with their actual lower fields,
   sections, and inverse carries. Such comparisons can identify common
   operations. A changed cochain representative must come with the
   explicit phase map and the transported product.

The two 4+1D stacking blocks are the largest numerical targets. The
cross-dimensional route is also promising for the 3+1D mixed blocks:
it can relate their exchange corrections to already defined bulk
obstructions and stacking laws. The compatibility identity constrains
such a reduction; it does not itself establish the required map between
the current cochain representatives. That map and its paired phase
corrections must be derived before any of these counts is replaced.

The coefficient tables remain exact reference formulas during this work.
A proposed reduction replaces them only after an exact identity or a
specified paired coboundary is established. Physical contribution labels
continue to record fermion-exchange origin, not polynomial variable
support.
