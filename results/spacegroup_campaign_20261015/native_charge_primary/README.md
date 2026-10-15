# Exact native primary charge classes

This archive records the primary obstruction optimization introduced on
2026-10-15. It contains 16 affine backgrounds and 70 actual integral charge
generators, including 16 nonzero obstruction classes. All native/bar classes
agree and every saved difference primitive bounds the difference exactly.
This is a class-level check; it does not measure a complete classification.

## Mathematical domain

Let the CI sheet vanish and let `q` be an integral `rho`-twisted cocycle.
Assume `omega` is half integral and its `(rho+s)`-twisted coboundary is
integral. Then `qbar=q mod 2` and `w=2 omega mod 2` are binary cocycles.
The coefficient homomorphism `j:F2 -> (Q/Z)_s`, `j(1)=1/2`, is equivariant
because `-1/2=1/2 mod Z`. Reduction modulo two removes both sign actions.
Therefore the original primary obstruction satisfies

```
[omega cup q + Sq2(q)/2] = j([w cup qbar + Sq2(qbar)]).
```

The bar `Sq2` includes its open-cochain correction. That correction vanishes
modulo two for the present closed integral `q`, even when `rho` is nontrivial.
The native higher diagonal gives the same cohomology operation by the
comparison theorem for free resolutions. This identifies classes, without
assuming that the native and bar representatives are identical cochains.
The signed target's exact `coordinates` map is still used. In particular,
`j` need not be injective on cohomology and odd torsion is not reinterpreted
as binary cohomology.

The runtime checks the actual integral charge vector and its signed
differential, the canonical target cohomology, the callback-bound background
certificate, and native closure of `w`. General rational extensions and
uncertified contexts use the original bar class route. All charge lattices,
free CI sheets, phase completions, stacking products and incoming gauge
relations retain their exact original data. No full classifier is reduced
modulo two.

## Evidence and reproduction

- [independent_summary.json](independent_summary.json) records the 70-root
  checks. Full vectors and primitives are in
  [independent/result.json](independent/result.json) and
  [independent/result_extra.json](independent/result_extra.json).
- [independent/source_manifest.json](independent/source_manifest.json) pins
  the untouched U1 reference `ce152c6` and generic main `0864495` modules.
  Only their public symbol prefix was renamed. The earlier harness's empty
  matrix setup failure is preserved; the corrected helper treats the unique
  map into a zero-dimensional group exactly.
- [focused_tests.json](focused_tests.json) records the integrated adapter's
  three focused tests, including 32 affine roots, independent signs,
  rational coefficients, certificate invalidation and rejected invalid input.
- [main_provenance/remote_main_hash_check.json](main_provenance/remote_main_hash_check.json)
  compares the actual nongit cluster checkout with local main. Both recorded
  differences are retained; neither changes the ordinary production formula
  path. No remote source file was silently assumed identical.

Replay the independent checks with GAP/HAP and the pinned U1 commit available:

```
python3 results/spacegroup_campaign_20261015/native_charge_primary/replay_independent.py --output /tmp/u1-primary-replay-output
```

The replay restores hash-checked source files into a temporary directory and
leaves this archive unchanged. `package_manifest.json` hashes all archived
artifacts. The generic contraction and diagonal modules are reusable exact
resolution code; no other theory's formula engine is included in the runtime.
