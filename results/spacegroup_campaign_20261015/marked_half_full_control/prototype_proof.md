# Exact marked half-source doubling, 3+1D

Review date: 2026-10-15 UTC. This is an isolated prototype on insulator commit `d3b2dcc6fe9f4ecda3e957d74edae2012ac46198`. It contains neither the q2-only mod-2 pullback patch nor the later immediate native-vector reuse patch. No production checkout or running campaign was changed.

## Identity and its domain

Use the original four-data order $(e_1,n_1,n_3,\nu_4)$. This optimization acts only inside the pure-charge subsection $e_1=n_1=0$ of the CI backend. Let $q=n_3$ be the actual closed integer charge cochain, and let $O_5(q)$ be its certified source with values in $\tfrac12\mathbb Z/\mathbb Z_s$. The certificate factory checks native integral closure and the half-integral background; arbitrary rational backgrounds do not enter this path.

Write $G^*$ for the unchanged native-to-bar cochain pullback and $H^*$ for the unchanged integral comparison homotopy. The actual successful solver call constructs

$$\nu_4=G^*b_4-H^*O_5(q)\pmod1.$$

This is the existing code in `baseline/gap/backend_half_phase.g:49–60`. Every term of $H^*O$ has an integer coefficient, including all orientation signs: see `baseline/gap/backend_bar.g:225–247`. Therefore, pointwise on every ordered group tuple,

$$2H^*O_5(q)=0\pmod1,\qquad 2\nu_4=2G^*b_4\pmod1.$$

This holds for nonabelian and infinite affine groups and independent coefficient actions. It uses neither averaging nor a cohomology-class identification. The signed action also preserves the subgroup of half phases. The full product is consequently

$$(0,0,q,\nu_4)^2=(0,0,2q,\;2G^*b_4+F_{\rm charge}(q,q)),$$

where the implementation calls the original `U1ChargeProduct` without simplifying or replacing it. In particular, it keeps its full cochain expression, rather than introducing a new closed-cocycle formula. The full integer charge is $2q$, including when its cohomology class is zero. Its later removal still uses the original integer primitive, full gauge correction and recorded root witness.

The native seed $b_4$ can contain quarters; $2G^*b_4$ need not vanish. Moreover, $b_4$ is not substituted for the native transfer of the original completed $\nu_4$. The single-root completion, its source, native completion checks and exported full phase remain unchanged. Only a later product of that exact marked state with itself uses the identity. Rational-valued representatives can differ by integers, as appropriate for the target $\mathbb R/\mathbb Z_s$; all saved scientific records tested here agree literally.

## Guarded implementation

Only `candidate/gap/backend_half_phase.g` and `candidate/gap/classification.g` differ from the baseline runtime. A successful `U1SolveCertifiedChargeData` call stores a context-owned entry and gives the original state an opaque handle. The entry binds the actual state, context, resolution, comparison object, dimension, action/background callbacks, charge callback, source certificate and callback, and returned phase callback. It copies the native integer charge values.

The native phase callback is constructed with `U1Bar`; that function immediately copies its vector (`baseline/gap/backend.g:193–199`). The original solver's $G^*b_4$ and the marked callback thus capture independent copies of the same values. Mutating the caller-visible `nativePrimitive` afterwards changes neither callback. The previous unused audit-vector field was removed. No extra seed-mutation rejection is needed because the original and optimized phase have the same copy semantics.

`U1TryMarkedHalfChargeDouble` accepts only spatial dimension three, literal zero CI sheet, the same state object in both factors and the still-matching entry. Missing, non-record or damaged relevant source-certificate fields return `fail`; ordinary product fallback remains available. Non-half backgrounds, unmarked states, changed callbacks, different contexts/resolutions/comparisons, shallow copies and forged handles do not select the optimization. An explicit `c.markedHalfDoubleMode="reference"` disables it. The product result is unmarked, so its next product uses the original algorithm. A genuine no-op gauge returns the same state object and legitimately retains the mark.

The registry is an internal mutable GAP record, not a security boundary against arbitrary edits to internal backend records. As elsewhere in this backend, actual cochains and contexts obey the immutable-callback contract. The guards cover supported replacement and stale-context cases; they do not claim to detect a function whose hidden captured environment is illicitly mutated while its identity stays fixed.

## Reuse provenance

The idea is the marked-source cancellation in superconducting main commit `0864495b90297d3e1a0747b77aae17980f6d1f3f`, `gap/stacking.g:85–93`. Its file SHA256 is `4a8bcd788980c1f87cf5ced70ab277562f0c3e1db73462e6ea377155305d697d`. This file was inspected through that exact Git revision; the current main working tree can advance independently.

No superconducting formula or coordinate rule was copied. In particular, its mod-2 lower charge can disappear on doubling, whereas the insulator's integral $2q$ must remain. The prototype derives the cancellation from the existing insulator solver and reuses its own complete charge twister and removal gauge.

## Validation and limits

The final candidate passes six focused tests, including three existing half-phase-transfer tests, in `focused_tests.log`. The earlier incorrect unittest import invocation is retained separately in `focused_tests_import_attempt.log`; it performed no mathematical tests.

The direct controls contain 49 full doubles, 4,696 ordered-tuple phase comparisons modulo one, 49 native vector comparisons and completed-state checks, eight genuine quarter seeds, 49 nonzero doubled integer charges, and 46 exact removal-gauge/root-witness comparisons. They include independent signed cyclic backgrounds, nonabelian D4 with independent nontrivial $s$ and $\rho$, full affine SG4 and SG6, inverse group generators and negative integer charges. The fixture compares the full doubled charge to twice the original charge's actual native transfer, without assuming a native/bar round trip is the identity on representatives.

There are 26 rejection/guard controls, including missing certificate fields, source callback mutation, rational backgrounds with a nonzero completed charge, other contexts even with a shared registry, and exported native-seed mutation. Damaged-certificate product fallback is compared to the reference product.

`complete_controls_final/comparison.json` records eleven fresh-process complete baseline/candidate classifications on the final code: eight point-group cases and three affine cases. Every output field except `resolutionBuildTimings` is literally equal, including the full presentation, roots, native certificates, incoming/gauge witnesses, filling data and worker/cache counters. Six marked-double calls occurred across the point cases. The three complete affine runs had zero hits; the direct affine cochain controls exercise the optimized branch. The portable test additionally compares four complete classifications in reference/certified modes.

These checks establish a reviewed exact optimization candidate, not an observed performance gain. A useful benchmark must report actual marked hits, full scientific equality, whole-run wall/CPU and peak memory under matched conditions. No cluster benchmark or production integration is part of this package. Existing physical-spectrum scope and the selected neutral E8 section are unchanged.
