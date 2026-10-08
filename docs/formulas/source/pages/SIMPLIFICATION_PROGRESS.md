# Formula simplification: incorporated results and remaining work

The [guide](../FORMULA_GUIDE.md) links the current obstruction, general
stacking, and separate self-stacking references. The
[term census](TERM_COUNTS.md) gives the current counts and their exact
boundaries. This record distinguishes formulas already changed from
structural ideas whose full application remains to be derived.

## Incorporated in the general formulas

- **4+1D Majorana bosonic twister:** the integral carry identity replaces
  the former 6,176-term expression by 482 outer addends. Counting the
  146 explicit products inside its four protected lifts gives 624
  expression leaves. The [derivation](FOUR_DIMENSIONAL_MAJORANA_CARRY_REDUCTION.md)
  and every lift interior are available; the representative is unchanged.
- **3+1D complex-fermion exchange:** the former 132-word contribution is
  exactly thirteen face products. The [complete replacement and proof](THREE_DIMENSIONAL_CF_EXCHANGE_REDUCTION.md)
  are incorporated in the main formula, retaining its physical origin.
  The accompanying eight-word auxiliary polynomial is also replaced by
  the lower Majorana obstruction, eliminating its symbol. The complete
  c-psi contribution falls from 202 to 29 terms.
- **3+1D source exchange:** its 25-word correction is seven MS words,
  all using the full complex-fermion differential. Reusing that same
  lower equation also reduces five ordinary cups to three. The complete
  c-psi source contribution drops from 30 to ten terms with exact equality.
  [Proof and executable certificate](THREE_DIMENSIONAL_CF_EXCHANGE_REDUCTION.md#source-exchange-through-the-lower-differential).
- **4+1D mixed quarter numerator:** its three pairs of four cup terms
  become three pairs of three terms by the
  [higher-cup polarization identity](GENERAL_MIXED_QUARTER_POLARIZATION.md).
  Its 42 terms become 39. Distributing the associated half-valued carries
  reduces the complete mixed twister by 84 terms, without altering a lift.
- **Reuse of lower operations:** the main formulas retain their defined
  differentials, twisters, complete output fields, Delta, and integer
  carries. The [integer quadratic cochain](QUADRATIC_REFINEMENTS.md)
  supplies a reusable three-cup expression and an exact addition identity.

These are changes to the displayed formulas. Frozen expanded coefficient
archives keep their original bytes as independent verification inputs.
The production runtime remains in its documented coordinate convention;
this documentation update does not claim a new runtime benchmark.

## Separate self-stacking references

| Scope | Complete terminal twister | Reference |
|---|---:|---|
| 2+1D, zero integer decoration | 8 terms | [Formula and exact proof](TWO_DIMENSIONAL_SELF_STACKING.md) |
| 3+1D, zero p+ip | 10 terms | [Complete self-stacking](THREE_DIMENSIONAL_SELF_STACKING.md) |
| 3+1D, canonical torsion p+ip root | 1,414 terms | [All six contributions](THREE_DIMENSIONAL_SELF_STACKING.md) |
| 4+1D, zero p+ip | Restriction of the shared current self-stacking law | [Complete closed specialization](FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md) |
| 4+1D, arbitrary permitted p+ip | 4,407,587 outer terms | [Complete self-stacking](FOUR_DIMENSIONAL_SELF_STACKING.md) |

The 3+1D open-Majorana contribution now has 13 outer terms instead of
16. Its [canonical-lift identity](THREE_DIMENSIONAL_OPEN_MAJORANA_LIFT_REDUCTION.md)
reuses the lower Majorana obstruction; one whole lift has two interior terms.
The 4+1D open-Majorana word identity removes 31 terms, and identifying the
same integer carry evaluated with zero Majorana input removes 482 mixed
terms. These are exact changes in the same phase representative.
[4+1D derivation and checks](FOUR_DIMENSIONAL_SELF_STACKING_REDUCTION.md).

The full open Majorana contribution in the last row has 200 outer terms,
including four lifts with 106 interior products. Replacing only those
four wrappers in the count by their interiors gives 302 expression leaves
for that contribution. The remaining large mixed and pure coefficient
sums have 3,613,517 and 793,669 terms. All are specified explicitly; none
is counted as one term merely because it is written as a sum.

The [root-power theorem](ROOT_POWER_PRESENTATIONS.md) explains why two
copies suffice for the finite 3+1D p+ip relation, how to choose the other
roots, and how to extend the construction to the current finite 4+1D
examples. Complete gauge transport and ordinary CF/bosonic arithmetic
remain necessary. Saved-presentation replays check the group-theoretic
construction; they are distinct from implementing and timing a new
cochain backend.

## What is still a simplification target

The mixed and pure p+ip terminal blocks still dominate the general
formulas. Their large coefficient lists are exact baselines, not a claim
that the mathematical structure has been fully understood.

The [fermionic-coboundary/stacking relation](COBOUNDARY_STACKING_COMPATIBILITY.md)
provides a constraint on the cross contributions. Its full application
to the current representatives requires the corresponding section and
phase maps. It has not yet replaced all mixed coefficient blocks.
Likewise, the optional quarter-lift transport in the quadratic-cochain
appendix is a stated coordinate change, not a simplification silently
applied to every formula.

The next work is to express the remaining mixed blocks using the already
defined lower differentials and twisters, and to simplify the pure p+ip
integer response together with its stacking difference. Every replacement
must preserve the complete phase, including whole lifts and signed
integer inputs. [Specific targets](NEXT_SIMPLIFICATION_TARGETS.md) give
their current sizes and the identities to investigate.

## One maintained formula source

Edit [source/](source/README.md), then regenerate the reader pages.
Shared equations are stored once; general and restricted laws have
separate pages and explicit domains. The generator checks every page
against that source. Publish source, generated pages, proofs, and the
updated census together. Coordinate maps and numerical variable names
belong in the [programmer translation](../../formulas/CODE_NOTATION.md).
