# E8-first theory: research and physical comparison

The active specification is the [formula guide](../FORMULA_GUIDE.md).
It presents one current set of E8-first obstruction functions, stacking
twisters, and gauges in separate dimensional pages. This directory retains
the research proofs and physical-comparison record; its short dimensional
links do not maintain duplicate formula versions.

The formal group domain is a discrete finite-holonomy extension
`1 -> Z^r -> G -> P -> 1`, with finite `P` and translation rank no greater
than the spatial dimension, at most four. Continuous groups remain
exploratory. Every state has one shared phase and is ordered
`(e_p,n_p,n_{p+2},nu_{p+3})`, with `p=d-2`.

## Current formulas and global computations

- [2+1D](../formulas/TWO_DIMENSIONAL.md): uniform E8 and IQH, charge, and phase.
- [3+1D](../formulas/THREE_DIMENSIONAL.md): integer signed walls and the selected neutral section.
- [4+1D](../formulas/FOUR_DIMENSIONAL.md): both sheet rows, coupled charge, and shared phase.
- [Full root presentations](../formulas/ROOT_POWER_PRESENTATIONS.md) and
  [computed 4+1D cyclic examples](../formulas/FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md).

`insulator.E8State` implements the exact local source/product/gauge triple,
inverses, powers, and background transport. The 3+1D extension routines
compute signed integer H1 from finite point-group presentations or full
rank-three affine space-group presentations, and combine its selected
section with actual CI root presentations. They retain free weak layers
and principal gauge relations. The separate 4+1D cyclic pilot computes
all four layers and their coupled powers for its explicit internal
backgrounds. It does not constitute a general 4+1D group classifier.

## Mathematical and physical evidence

The [general-group proof](research/general_groups/general_groups.md) gives
a rational primitive for the neutral cubic for translation rank at most
four; it does not require the neutral sheet itself to be exact. The
[eta dictionary](research/physical/eta_dictionary.md) fixes orientation,
flat-line convention, and the phase shift of the selected neutral lens
root. These statements have different roles and are not substituted for
a global root computation.

The [parity bridge](research/parity_bridge/parity_bridge.md) records the
closed-charge comparison and the pure sixteen-sheet calculation. The
[mixed 4+1D bridge](research/general_groups/mixed_bridge_4p1.md) supplies
paired source, product, and gauge corrections relative to the pure-CI
comparison. Its arbitrary-base sixteen-sheet periodicity certificate
covers the generic publication path, with
`Backend(use_specializations=False)`.

The outstanding physical inputs are the universal nonzero-CI terminal
map and its paired product map on the circle quotient, identification
of the retained CI presentation with the complete physical kernel, and
the nonzero-uniform-IQH physical product-coordinate comparison. The
explicit cochain operations are fixed; a remaining physical comparison
is not an omitted runtime coefficient. Matching abstract groups or
local identities alone does not prove the complete physical dictionary.

## Preserved research

The [research index](research/README.md) separates dimensional proofs,
exact certificates, and primary-source provenance. The user has deferred
the distinct intrinsic uniform 4+1D enlargement; its existing work remains
in [separate research notes](research/parity_bridge/intrinsic_response.md)
and does not enter the four-data formulas or calculated examples.

The [CI provenance](../../formulas/provenance.json) and
[E8 provenance](../../formulas/e8_provenance.json) pin the supplied input
archives. Runtime tests use only this branch; historical-source audits
retain their own explicitly recorded reference inputs.
