# Frozen G point-group validation: 3+1D

All 64 physical point-group backgrounds completed at commit
`c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`: 32 spinless and 32 spin-1/2.
Every complete CI presentation and final stacking group exactly matches the
accepted CI sector in the earlier E8 records. Input hashes, source hashes,
native completion certificates and independent Smith reductions pass for all
64 cases. This archive supplies CI records for a subsequent E8 extension; it
does not perform that extension or change active classification tables.

The local run used GAP 4.12.1, HAP 1.62, four paired-spin workers and the
separately hash-checked native integer VM. It finished in 56.08 seconds wall
time. All 99 tests passed on the same frozen source in 54.088 seconds. These
are local observations, without a cluster-wide performance extrapolation.

## Preserved records

- [point3_g_raw.tar.gz](point3_g_raw.tar.gz) contains all 64 complete runner
  records, immutable inputs, native outputs, source manifest, selected VM
  metadata, drivers and logs under `run/`.
- [comparison/spinless.json](comparison/spinless.json) and
  [comparison/spin_half.json](comparison/spin_half.json) compare every
  preexisting native field against the accepted `classification.ciSector`.
  They retain every raw difference and apply no normalization.
- [representative_controls.tar.gz](representative_controls.tar.gz) contains
  the separate and paired optimized/reference controls and original-source
  local replays for O and Td.
- [control_audit.json](control_audit.json) records the exact control checks
  and the two serialization rules proved below.
- [committed_source_validation.json](committed_source_validation.json)
  verifies all 57 runtime source files against the committed G tree.
  [native_build_origin.json](native_build_origin.json) records the reused
  VM's compiler, source and binary hashes; its source and generated integer
  expressions match this commit exactly.
- [tests.log](tests.log), [summary.json](summary.json) and
  [package_manifest.json](package_manifest.json) retain test output,
  machine-readable counts and artifact hashes.

## Exact comparison levels

Only three cases match every old native field literally. The other 61 are
preserved as differences in the raw reports. Two explicit serialization
changes account for all differences in 62 of the 64 cases:

1. Thirty-one CI-root witnesses now include `sheetCoefficients`. Each is
   checked to equal the already recorded root order times its indexed
   basis vector. The original order and phase/charge coordinates remain
   identical. This records the finite relation in the general relation
   format introduced for affine groups.
2. Sixty-two zero sheet-gauge records use `[]` instead of `[0]`. In
   `U1ReduceVacuum`, the empty field records that the literal-zero sheet
   needs no correction; `[0]` records the explicit zero correction.
   `U1Bar` returns `U1Zero` for an all-zero vector, and the zero gauge is the
   identity. Only this exact `[0]` to `[]` change is identified in the audit;
   no nonzero gauge is removed.

O spinless and Td spinless retain additional native representative
differences from the earlier cluster records. The controls establish:

- Current optimized and all-reference G runs have literally identical
  mathematical fields; only primary-call counters differ.
- Separate and paired G runs have literally identical mathematical fields;
  only reuse metadata differs.
- The original `f572a98` source, rerun locally with the exact same source
  hash as the archived cluster run, reproduces current G's phase, source and
  generator representatives. Its only difference from current local G is
  the explicit zero-gauge serialization above.

Thus these differences were not introduced by the optimizations. They occur
between environments using the same original source. The old cluster used
GAP 4.13.1 and this local run uses GAP 4.12.1, both with HAP 1.62. The existing
S4 resolution transport calls `IsomorphismGroups`, which is a possible source
of different native coordinates, but its actual old/new transport maps were
not reconstructed. No claimed cochain equality or physical root map is
inferred merely from equal groups. Both complete presentations already agree
literally, and all raw source/phase differences remain available for review.

## Reproduction

Extract both archives into a new review directory and restore the committed
source with `git archive c07c6e5` into its `source/` subdirectory. Copy
`compare_results.py` and `audit_controls.py` there. The first script reproduces
the intentionally retained raw differences and returns a nonzero status for
them; the second verifies the stated controls and serialization rules and
returns success. Neither script rewrites calculation records or reference
values. The frozen source checkout and git archive are omitted here because
the exact commit is retained in the repository.
