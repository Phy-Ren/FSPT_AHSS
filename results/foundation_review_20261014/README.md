# Interacting insulator comparisons, rebuilt 2026-10-14

Every row is one group and one physical spin. Each source has its own
column, with separate versions where the published values differ.
The adjacent CSV and JSON retain the same rows, exact invariant factors,
scope, unavailable-value reasons and source locations.

## Present model without an independent E8 field

| Table | Rows | Object |
|---|---:|---|
| [2D point groups](relative_point2.md) | 20 | Relative subgroup, n0=e0=0 |
| [2D wallpaper groups](relative_wallpaper.md) | 34 | Relative subgroup, n0=e0=0; charge and phase layers distinguished from stacking |
| [All allowed n0 in 2D](all_n0_retained_model_2d.md) | 54 | Current model with no independent e0; physical nonzero-n0 product calibration remains open |
| [3D point groups](retained_model_point3.md) | 64 | Current CI/charge/phase model; source-side quotients individually labelled |

A fixed nonzero n0 fiber is a torsor, not another stacking group. The
all-n0 table does not silently include the independent neutral response.
See the separate [sector definition](../../docs/foundations/two_dimensional_sectors.md)
and [model status](../../docs/foundations/ci_sector.md).

## Full physical references including the neutral response

| Reference-only table | Rows | Coverage |
|---|---:|---|
| [2D full-response references](full_E8_reference_2d.md) | 54 | Verified source cells only; unextracted cells explicitly marked |
| [3D full physical references](full_E8_reference_point3.md) | 64 | Full source groups; current full-theory calculation marked not computed |

These files do not append a factor to a model result and call that a
calculation. The additional fields and missing operations are specified
on the separate [E8 extension page](../../docs/foundations/e8_extension.md).

## Diagnostics and provenance

The [band-generated interacting reduction](diagnostics/point2_band_generated_interacting_reduction.md)
is a separate diagnostic. It is not a column in the complete interacting
classification table. Raw free-fermion classifications are not used.
Other candidate papers with different symmetry or atomic equivalence are
assessed in the [interacting reference policy](../../docs/foundations/interacting_reference_policy.md).

The [D2/D6 bordism grading audit](../../docs/foundations/debray_d2_grading_audit.md)
is separate from the printed-reference columns. It uses an independently
published connective-homology splitting, reads no program classifications,
and records the source theorem and the derived result separately. The
printed values have not been overwritten to improve a match.

The [correction audit](../../docs/foundations/corrections_and_versions.md)
distinguishes formal errata, arXiv replacements and changed journal tables.
The [earlier version ledger](../../docs/reference_ledger_20261014.md)
retains the original reference provenance. Debray's printed 2026 values
remain labelled as printed values; a proof audit must not silently replace
a reference cell.

Reproduce the reference transcription and tables with:

```bash
python benchmarks/extract_debray_2026.py --output benchmarks/debray_class_a_2102.02941v3.json
python scripts/build_foundation_tables.py
```

The first command requires the pinned primary source cache documented in
the script. It reads no classifier outputs. The second command reads
immutable campaign results and reference fixtures only. The
[validation record](table_validation.json) checks row uniqueness, expected
coverage, exact source values and source hashes. It does not certify
physical completeness.
