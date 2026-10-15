# E8 integration and mathematical closure status

Date: 2026-10-15. The formal group domain is a discrete finite-holonomy
extension `1 -> Z^r -> G -> P -> 1`, with finite `P` and `r` no greater
than the spatial dimension, at most four. Infinite translations and
nonsymmorphic relations are retained. Continuous groups are exploratory
and are not a completion condition for this work.

All extended states use **E8 first**:
`(e_p,n_p,n_{p+2},nu_{p+3})`, `p=d-2`.
This specified tower has coefficient rows `q=3,1,0`; its potentially
nonzero AHSS operations end at **d4**. See [the page-index convention](notation.md).
Extra uniform intrinsic 4+1D responses are a separate enlargement, not a
missing layer or `d5/d6` operation of this four-coordinate tower.

## Separate dimensional specifications

- [The four-data theory and the final-group procedure](four_data_theory.md).
- [Notation and coefficient actions](notation.md).
- [2+1D uniform coordinates](2p1.md).
- [3+1D neutral section and integer cocycles](3p1.md).
- [4+1D source, stacking, and full gauge](4p1.md).

The `insulator.E8State` API implements these local completed-state operations,
with exact integers/rationals, one phase, complete inverses and integer powers.
It validates the degree and coefficient action of every phase. The existing
base CLI still uses the CI-only model. The separate
`scripts/extend_e8_3p1.py` computes the selected 3+1D E8 section for finite
point groups from integer H1, principal gauges, and the combined
presentation. Its output retains the physical CI-kernel caveat; it is
not a general space-group or coupled 4+1D global classifier.

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

The [relative mixed E8–CI bridge](research/general_groups/mixed_bridge_4p1.md)
now supplies explicit single-state, product, and gauge corrections.
Arbitrary-base sixteen-sheet periodicity is proved for the generic
publication formula, including its normalized binary transfer; it is not
inferred from the pure-neutral test. The executable E8-first helpers are
in `insulator/parity_bridge.py`. The [2+1D endpoint](2p1.md) also now
includes the finite source-cylinder background transport and its proof.

## Still open within the specified four-coordinate tower

1. The universal nonzero-CI terminal comparison `R_{p+3}` and its paired
   two-input correction `K_{p+2}` are not yet constructed on the full circle
   quotient. The relative E8 bridge and closed-charge result do not supply
   the remaining pure-CI map.
2. Identification of the retained CI cochain model with the complete
   physical kernel remains unproved for the entire stated group domain.
   The nonzero-uniform-IQH microscopic product-coordinate dictionary also
   remains distinct from the proved free-quotient abstract splitting.
3. A general global E8 classifier must implement the common phase presentation,
   incoming identifications, resolution transfers, and actual root powers.
   The selected 3+1D finite-point-group postprocessor is now implemented;
   the general space-group and coupled 4+1D computations remain open.

The required deliverable is the complete `d2,d3,d4`, stacking twisters,
and equivalences for this tower. Knowing only an isomorphic final group
does not replace those formulas. Abstract splitting and transfer arguments
are auxiliary checks or an explicitly identified fallback.

Consequently the supplied neutral cochain block is substantially closed and
implemented locally, while the universal physical identification and the
global coupled classifier are not yet certified complete.

## Deferred research

The user has deferred the separate intrinsic `r0` enlargement until the
four-data theory is complete. Existing calculations remain in the
[separate intrinsic-response notes](research/parity_bridge/intrinsic_response.md).
They do not enter the active dimensional specifications or runtime.

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
