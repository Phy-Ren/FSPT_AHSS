# Fresh four-data campaign — 2026-10-15

All 108 new CI calculations and 64 selected-model E8 extensions completed.
The CI runs used immutable source `f572a98` on `n02.local` and `n03.local`,
reached through the persistent cluster3 connection. E8 extensions used source
`442a2cd` locally and consumed those exact new CI results. None of the new
tables substitutes a historical calculation for a rerun.

Select a dimension first; each directory then separates physical spin and
response sector. Each literature source and version has a separate column.

- [3+1D: all 32 point groups for each spin](3p1d/README.md).
- [2+1D: selected point and wallpaper diagnostics](2p1d/README.md).

All 108 CI final groups agree with their saved predecessors. The E8 extensions
compute the specified four-data model with independent neutral cocycles, gauge
witnesses and combined integer presentations. Identifying the CI model with
the complete physical kernel is still unresolved; the result records explicitly
retain `physicalClassificationCertified: false`.

The report independently checks 108 Smith forms, 22 all-n0 relative kernels
against standalone n0=0 calculations, and 20 wallpaper filling relations.
All 108 CI records carry native chain-equation certificates. The source/input
hashes and extension-to-CI links pass verification. The recorded
[69-test run](../../docs/e8/research/campaign_20261015/wiring_audit/unittest.log)
also passed.

- [Validation totals](validation.json), [per-case checks](computation_checks.json),
  and [old/new CI comparison](old_new_comparison.json).
- [Raw evidence and reproduction commands](../evidence/four_data_20261015/README.md).
- [CI provenance](run_provenance.json), [E8 provenance](extension_provenance.json),
  and [pinned reference provenance](reference_provenance.json).
- [Formula and source audits](../../docs/e8/research/campaign_20261015/benchmark_audit.md).

Only interacting electronic classifications enter the main comparisons. No
intrinsic 4+1D r0 calculation or general space-group E8 classification is claimed.
