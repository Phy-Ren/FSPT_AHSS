# Certified full charge-source evaluation

Reviewed 2026-10-15 UTC. This specializes the existing U(1)^f source; it does not import superconducting operations. The reusable implementation pattern is main commit `0864495b90297d3e1a0747b77aae17980f6d1f3f`, `gap/full_stacking.g:143–172`, where a checked native cocycle certifies an exact closed-input formula.

Let `q` be the comparison-map pullback of an actual integral native degree-`d` cocycle with charge action `rho`, for `d=2` or `3`. Its exact native coboundary is checked before constructing the callback. Since the comparison is a chain map, `delta_rho(q)=0` on every bar tuple. Reduction modulo two removes the signs, so `qbar=q mod2` is a closed binary cochain.

The existing insulator source is

`O(q) = omega cup q + (qbar cup_(d-2) qbar + qbar cup_(d-1) delta(qbar))/2`.

Assume the validated extension lift is half integral and set `w=2 omega mod2`. The last term vanishes **pointwise**, and the first term is `w cup qbar /2` modulo one. Thus

`O(q) = (w cup qbar + qbar cup_(d-2) qbar)/2 mod1`.

The signed transports are respected: an integer difference in the original cup product disappears modulo one, and multiplication by a sign fixes every half-valued phase. This is not merely a cohomology identity, so no new phase primitive or gauge coordinate change is introduced.

If the actual native integer vector is even, linearity of the comparison map makes its entire bar pullback even. Then `qbar` is literally zero and the source is literally zero as a U1 cochain. This does **not** discard the integer charge: its native vector and bar callback remain in the complete state, and all existing root powers and integer gauge reductions still act on it. A vector that is only cohomologically zero, or only has an exact source, is not eligible for this zero-source conclusion.

For nonzero sources the unchanged `U1SolveData` still evaluates the full native obstruction, chooses the same Smith primitive, and applies the full bar/native homotopy correction. Replacing the raw rational source by a pointwise equal modulo-one source preserves this chosen phase representative: both transfer and homotopy have signed integer coefficients, so the difference contributes only integers before the existing modulo-one normalization. The same statement covers the even-vector case, whose old primitive was pointwise zero although represented by a nonconstant callback.

The certificate is created only while constructing initial charge-kernel lifts from explicit native integer vectors. It binds the exact context, dimension, charge callback, native vector and `s/rho/omega` callbacks. `U1Source` uses it only at zero CI sheet and only while those identities match. An absent, changed or non-half-integral background retains the original source route. Product and gauge formulas are unchanged, and states whose charge callback changes lose eligibility unless independently recertified.

## Evidence

The archived initial driver, reproduced by `tests/test_closed_charge_source.py`, performed 9,664 exact pointwise modulo-one comparisons against the existing unrestricted `U1ChargeSource`. Inputs include independent nontrivial `s/rho`, half-valued extensions, negative charges, cyclic orders 2/3/4, nonzero exact integer cocycles, and 60 even-native literal-zero checks. The checks compare actual cochain values, not only final groups or native classes.

`validation.json` compares the full SG195 paired run against a separately frozen baseline containing the native-primary, Smith-cycle and compiled-formula changes. Only `gap/charge_source.g`, its load line, and the two certificate call sites differ. All 35 nonperformance fields per spin agree literally, including completed generators, root relations, incoming/gauge witnesses, filtration and primitive filling. The sequential local pair times were 41.037 and 33.919 seconds, an observed 1.21-fold improvement. This is not a cluster speed claim or an estimate for all 230 geometries.
