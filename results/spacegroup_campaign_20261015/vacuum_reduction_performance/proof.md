# Exact zero callbacks after vacuum reduction

This isolated experiment changes only two assignments inside frozen G's `U1ReduceVacuum`. It does not alter any formula, gauge parameter, cochain primitive or stored native witness. Production source was not changed by this experiment.

## Domain and full-cochain proof

`U1ReduceVacuum(c,d,state)` is an internal operation on a completed state whose sheet and subsequent charge classes can be removed. Its two production call sites in `gap/classification.g` use combinations of completed charge roots, or the difference between a completed CI-root reduction and its completed charge representative. Closure follows from the root construction and the exact product/gauge identities. A solvable *native image alone* is not a sufficient precondition for an arbitrary off-shell bar cochain.

Write F:C→B and G:B→C for the signed integral native/bar chain comparison maps. `gap/backend_bar.g` constructs h with dh+hd=FG−id. For a closed bar cochain f, `U1Solve` computes a=F*f, solves δb=a over the requested integral coefficient module, and returns G*b−h*f. Therefore

δ(G*b−h*f) = f + h*(δf) = f.

This is an equality of full signed integral bar cochains, not only a statement about native vectors or cohomology. Without δf=0 the h*(δf) remainder need not vanish; the shortcut is not asserted for arbitrary direct debug inputs.

For a completed state (n,q,ν), δ_s n=0 and δ_r q=I(n). If u solves δ_s u=−n, the existing full gauge produces n′=n+δ_s u=0 pointwise. Replacing the *returned* sheet callback by `U1Zero` therefore preserves the full state. The full gauge's charge and phase callbacks have already been constructed from the original state and original u. Gauge covariance gives δ_r q′=I(0)=0. If v solves δ_r v=−q′, the existing charge gauge with sheet parameter zero produces q″=q′+δ_r v=0 pointwise. Only this returned charge callback is replaced by `U1Zero`.

The phase gauges remain unchanged. Their callbacks refer to the original state passed to each gauge, rather than the subsequently returned record. The existing `U1CheckCompletedState` is still called after canonicalization; in particular, the complete native phase and its coboundary are still calculated and checked. The two simplified lower identities have been established by the exact solve/gauge construction above. All gauge parameters and `nativeFinalPhase` witnesses remain identical.

The local user-facing formula API and off-shell polynomial operations are outside this experiment and remain unchanged. A production integration should state this internal precondition and retain an explicit reference mode for direct debugging.

## 2+1D check

The signed finite-bar check starts from exact charge gauges of the vacuum. For each of four independent sign choices it checks the raw residual charge pointwise, its integral closure, and equality of the complete reference/candidate phase. No uniform IQH sheet is gauged away. Existing backend tests retain the nonzero-IQH, wallpaper filling and nonbinary-root controls.

## 3+1D check

The finite-bar check additionally uses nonzero signed exact sheet gauges, with negative integral parameters. It checks the raw sheet callback before replacement, the closed charge after that gauge, the raw charge after its full primitive gauge, and reference/candidate phase equality on all tested nondegenerate tuples. Saved native sheet/charge gauge parameters and native final phase are identical.

An initial probe used a nonzero *closed* degree-zero sheet parameter with trivial s. Such a gauge can leave a nonexact incoming charge class, so a direct vacuum reduction correctly refused its charge solve. That probe was outside the required charge-exact domain; its script and failure log are retained as `initial_probe_*`. The final probe uses a zero sheet parameter when s is trivial. This changes test construction only; the candidate was not changed to fit a test.

The full affine SG221 spin-half run compares all 38 output fields against saved frozen G. All 35 mathematical fields are literally identical, including the entire presentation, root completions, incoming relations, gauge parameters, primitive filling and final phase witnesses. Only `formulaWorkerCalls`, `formulaCacheStats` and `resolutionBuildTimings` differ. Independent source/input, native/result, Smith and primitive-filling checks pass. The candidate uses the identical optional native VM and changes only `gap/classification.g` in the 57-file runner manifest.

Observed local wall time is 234.922→127.065 seconds (1.849×); peak RSS is 1,823,532→1,301,088 KiB. Worker requests are 122,445→25,330. These are one complete matched-input experiment, not a whole-catalogue or cluster throughput estimate. The existing 14 backend tests pass on both frozen G and the isolated candidate.
