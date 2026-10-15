# Certified half-valued charge source: exact transfer and lazy cup-one

Date: 2026-10-15 UTC. Scope: the existing insulator model's initial completed charge roots in the original four-data tower `(e_1,n_1,n_3,nu_4)`, with `e_1=n_1=0`. This is an exact evaluation change. It adds no physical identification, incoming relation, or approximation.

The generic transfer is copied, with symbol-prefix changes, from main commit `0864495b90297d3e1a0747b77aae17980f6d1f3f`, `gap/backend_half_phase.g`. The lazy source uses the normalized three-term interval-cut formula in the same commit's `gap/stacking_closed_cf.g`, extended by the existing U1 extension term. No superconducting formulas or runtime dependencies are loaded.

## Certificate and exact source

The existing constructor checks that the actual integer native `n_3` satisfies `delta_rho n_3=0`. Its bar comparison pullback is therefore closed and normalized. With certified half-integral omega, write `q=n_3 mod 2` and `w=2 omega mod 2`. The existing phase source is exactly the canonical half-valued representative

`f = (w cup q + q cup_1 q mod 2)/2`.

The integral term and the extra term involving `delta q` have already vanished under this existing, reviewed closed-input specialization. This candidate does not extend its domain. Independent `s` and `rho`, negative integer charges, and nonzero half-integral backgrounds remain allowed. Non-half-integral or uncertified backgrounds retain the reference route.

For normalized increments `(g,h,j,l,m)`, the generic cup table gives

```
2f = w(g,h) q(j,l,m)
   + q(ghj,l,m) q(g,h,j)
   + q(g,hjl,m) q(h,j,l)
   + q(g,h,jlm) q(j,l,m)                  mod 2.
```

Products preserve their nonabelian order. A zero short-face factor removes its partner evaluation. If a composed increment is the identity, normalization makes its cochain value zero. Any identity among the original five increments makes the entire normalized source zero. The implementation uses exactly these identities; it does not recognize cohomological zero or erase a nonzero exact cochain. Arbitrary integer callback values can be reduced modulo two, including negative values.

## Half-valued transfer

Let an integral comparison chain be `sum a_t h_t [x_t]`. Since `f(x_t)` lies in `(1/2)Z/Z`, an even `a_t` contributes zero modulo one. For odd `a_t`, both its integer sign and the signed coefficient action of `h_t` can be omitted modulo one. Therefore

```
sum a_t (-1)^s(h_t) f(x_t) = sum_(a_t odd) f(x_t)     mod 1.
```

The optional generic evaluator checks that every evaluated value is half-integral. The production proposal reaches it only through a certificate tied to the exact context, dimension, charge callback, source callback and background actions, plus the explicit half-valued-source property. It does not infer this property from a cohomology class.

The resulting native source vector is identical to the reference `U1Native` result. The same native Smith solver therefore selects the same native primitive. The full integral comparison homotopy remains `U1HomotopyPullback(c.bar,"U1s",f)`; it is neither reduced modulo two nor replaced by a class-only operation. Thus the completed bar primitive is unchanged pointwise modulo one, including its possible quarter-valued entries. The literal source `U1Zero` must delegate to the existing `U1SolveData` zero branch so the primitive remains literally `U1Zero`.

## Measured checks

- 98,304 exhaustive D4 nonabelian source comparisons, including degenerate simplices and negative integer normalized cochains, agree with the existing generic cup implementation.
- 32 exact native/Smith transfer comparisons agree with the full signed evaluator.
- 42 solvable signed finite controls have identical native source and primitive vectors. All 1,005 tested complete primitive values agree, including two controls with quarter-valued native primitives.
- The existing 9,664 closed-charge pointwise comparisons, even-vector checks, stale-context checks and nonclosed rejection tests pass.
- SG141 and SG229 spin-half have respectively five and six completed charge roots. Every saved native root witness, all differentials, source-map entries and kernel matrices agree literally with frozen G, excluding timing fields only.

The full SG221 spin-half control subsequently passed: all 38 classification fields were compared; 37 are literally identical and only resolutionBuildTimings differs. The full presentation, completed root/gauge witnesses, primitive filling and operation statistics are unchanged. Its wall time was 224.534 seconds versus the saved G baseline 234.922 seconds; the modest difference is an observation, not a robust whole-campaign speedup claim. That full run used the preserved candidate_v1_overlay. The final overlay additionally restores the original literal U1Zero primitive fast path; the focused zero/complete-primitive regressions pass. Production G remains frozen throughout this review.
