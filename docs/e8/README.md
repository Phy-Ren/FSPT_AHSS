# E8 integration and mathematical closure status

Date: 2026-10-15. The formal group domain is a discrete finite-holonomy
extension `1 -> Z^r -> G -> P -> 1`, with finite `P` and `r` no greater
than the spatial dimension, at most four. Infinite translations and
nonsymmorphic relations are retained. Continuous groups are exploratory
and are not a completion condition for this work.

All extended states use **E8 first**:
`(e_p,n_p,n_{p+2},nu_{p+3})`, `p=d-2`.

## Separate dimensional specifications

- [Notation and coefficient actions](notation.md).
- [2+1D uniform coordinates](2p1.md).
- [3+1D neutral section and integer cocycles](3p1.md).
- [4+1D source, stacking, and full gauge](4p1.md).

The `insulator.E8State` API implements these local completed-state operations,
with exact integers/rationals, one phase, complete inverses and integer powers.
It validates the degree and coefficient action of every phase. The existing
CLI/global campaigns still use the CI-only model. No full E8-inclusive
classification table is being claimed or released by this change.

## Gaps closed in this work

The [space-group proof](research/general_groups/general_groups.md) replaces
the finite-group primitive argument. Rational cohomology vanishes above
translation rank. For the neutral cubic, a cellular-to-bar comparison
homotopy supplies the explicit construction `nu5=(e2^3) H5/3`. A primitive
of the possibly free class `e2` is unnecessary. The examples retain
translations, a glide, a screw, and magnetic sign characters, with
dimension-specific reports.

The [physical lens dictionary](research/physical/eta_dictionary.md) resolves
the eta normalization identified in the v0.9 review. With specified
orientation and flat line, `b(L)=1/3`, `X_geom(L)=7/9`, and the inverse
STZ eta has value `1/9=X_geom+b`. This is an ordinary-phase shift of the
chosen lift, not a change to `3X=b` or the `Z9` group. Exact cyclotomic
eta sums and independent relative characteristic integrals agree. Two
manifold detectors distinguish the full generated neutral/DW cyclic sector
and remain admissible Spin-c backgrounds.

The [parity bridge](research/parity_bridge/parity_bridge.md) now includes
the pure sixteen-sheet **source and product**, and a compatible source-prism
gauge. A conservative valuation proof covers the large binary transfer;
explicit source/nonbinary-face calculations are separate controls. The
closed-charge bridge is exact through source, short product, and gauge:
`R=X1 cup n_{p+2}/2`, with gauge comparison primitive `-X1 cup u/2`.
The executable comparison helpers are in `insulator/parity_bridge.py`.
They reject the open-charge case rather than omit its residual term.

The [intrinsic coefficient calculation](research/parity_bridge/intrinsic_response.md)
fixes a primitive integral 4+1D interacting response basis
`I=(c^3-c p1)/48`, `J=c^3/2`. It also establishes their restriction to
pure Spin/parity as zero. Reorganizing the same U1f symmetry over its parity
quotient retains the charge circle and therefore retains these responses;
actual symmetry breaking is a different map.

## Still open; not replaced by zero

1. The universal nonzero-CI terminal comparison `R_{p+3}` and its paired
   two-input correction `K_{p+2}` are not yet constructed on the full circle
   quotient. Pure E8 and closed-charge results do not prove this mixed map.
2. The additional intrinsic row `r0 in H0(G,Z_rho^2)` has possible integral
   `d3`, `d5`, and `d6` operations. A formal characteristic-polynomial
   transgression fixes a candidate rational expression, not its torsion
   normalization. Those differentials are not implemented.
3. Identification of the retained CI cochain model with the complete
   physical kernel remains unproved for the entire stated group domain.
   The nonzero-uniform-IQH microscopic product-coordinate dictionary also
   remains distinct from the proved free-quotient abstract splitting.
4. A global E8 classifier must implement the common phase presentation,
   incoming identifications, resolution transfers, and actual root powers.
   The new local API and existence theorem do not constitute that campaign.

Consequently the supplied neutral cochain block is substantially closed and
implemented locally, while **the entire physical AHSS is not yet certified
closed**. The four-coordinate state is the reduced decoration tower; full
intrinsic 4+1D responses require the extra `r0` data. This boundary persists
even with the user's narrower space-group scope.

## Evidence and source discipline

The [research directory](research/README.md) contains dimension-separated
proofs, exact audit programs, data, and primary-reference provenance.
Interacting bordism and independent physical constructions provide the
calibrations. No validation here uses Jian-Hao Zhang's disputed tables or
free-band groups as a substitute for interacting classifications.

Run the branch-local checks with `python3 -m unittest discover -s tests -v`.
These tests do not import another checkout. Historical-reference audit
programs are separate, preserve their recorded input paths or explicit
reference arguments, and may require the pinned source bundles/checkouts.
Supplied archives are unchanged, and superconducting runtime code remains
outside this branch.
