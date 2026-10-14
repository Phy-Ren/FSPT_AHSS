# Interacting insulator comparisons

Each table file contains one physical spin convention, one catalog family,
and one response sector. Sources and publication versions have separate
columns. Markdown, CSV and JSON copies contain the same cases and values.

All active tables omit independent E8 decoration. In 2+1D this means
`e0=0`. The `n0=0` and all-allowed-`n0` results are different files, even
when a symmetry forces all allowed `n0` to vanish.

## Spinless tables

| Scope | Separate result file | Cases |
|---|---|---:|
| 2+1D point groups, n0=0, e0=0 | [Spinless point groups, n0=0](e0_zero/n0_zero_point2_spinless.md) | 10 |
| 2+1D wallpaper groups, n0=0, e0=0 | [Spinless wallpaper groups, n0=0](e0_zero/n0_zero_wallpaper_spinless.md) | 17 |
| 2+1D point groups, all allowed n0, e0=0 | [Spinless point groups, all n0](e0_zero/n0_all_point2_spinless.md) | 10 |
| 2+1D wallpaper groups, all allowed n0, e0=0 | [Spinless wallpaper groups, all n0](e0_zero/n0_all_wallpaper_spinless.md) | 17 |
| 3+1D point groups, current model without independent E8 | [Spinless 3D point groups](without_e8/point3_spinless.md) | 32 |

## Spin-half tables

| Scope | Separate result file | Cases |
|---|---|---:|
| 2+1D point groups, n0=0, e0=0 | [Spin-half point groups, n0=0](e0_zero/n0_zero_point2_spin_half.md) | 10 |
| 2+1D wallpaper groups, n0=0, e0=0 | [Spin-half wallpaper groups, n0=0](e0_zero/n0_zero_wallpaper_spin_half.md) | 17 |
| 2+1D point groups, all allowed n0, e0=0 | [Spin-half point groups, all n0](e0_zero/n0_all_point2_spin_half.md) | 10 |
| 2+1D wallpaper groups, all allowed n0, e0=0 | [Spin-half wallpaper groups, all n0](e0_zero/n0_all_wallpaper_spin_half.md) | 17 |
| 3+1D point groups, current model without independent E8 | [Spin-half 3D point groups](without_e8/point3_spin_half.md) | 32 |

The all-`n0` tables use the current supplied product convention; its
universal nonzero-`n0` physical calibration remains open. A fixed nonzero
`n0` fiber is not another stacking group. See the
[sector definitions](../../docs/foundations/two_dimensional_sectors.md)
and [current model status](../../docs/foundations/ci_sector.md).
The 3D tables retain explicitly labelled source-side quotients where
applicable; they do not claim a computed full-E8 classification.

## E8-inclusive results are deferred

The current [e0=0 scope](e0_zero/README.md) and the
[deferred e0-inclusive status](e0_included/README.md) have separate files.
There is no active E8-inclusive classification table. E8 decoration has
not been implemented; complete tables will be produced separately after
that work. The earlier reference-only full tables are preserved in Git
history at `f918528`, and their raw reference fixtures remain available.
[Extension notes](../../docs/foundations/e8_extension.md) are deferred
research notes, not current calculation results.

## Separate diagnostics and provenance

The interacting reduction of band-generated phases is only a diagnostic:
[spinless](diagnostics/point2_band_generated_interacting_reduction_spinless.md)
and [spin-half](diagnostics/point2_band_generated_interacting_reduction_spin_half.md)
have separate files. Raw free-fermion classifications are not used in
main tables. See the
[interacting-reference policy](../../docs/foundations/interacting_reference_policy.md).

The [D2/D6 grading audit](../../docs/foundations/debray_d2_grading_audit.md)
remains distinct from printed source values. The
[correction audit](../../docs/foundations/corrections_and_versions.md)
and [version ledger](../../docs/reference_ledger_20261014.md) record source
provenance. Splitting files changes no classification or reference value.

Regenerate the active tables with:

```bash
python scripts/build_foundation_tables.py
```

The generator reads frozen campaign results and reference fixtures only.
The [validation record](table_validation.json) records input hashes,
coverage and separation checks. Raw calculation archives remain unchanged;
these presentation checks do not certify physical completeness.
