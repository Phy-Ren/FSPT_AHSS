# Calibration audit artifacts, 2026-10-14

The active narrative and tables have been reorganized. Use the
[foundation index](../../docs/foundations/README.md) and
[per-case, per-source tables](../foundation_review_20261014/README.md).
The model and its proposed neutral extension now have separate documents.

This directory retains the reproducible audits:

- [Exact 2D kernel and relation-lattice audit](audit_2d_sectors.py), with
  [JSON](two_dimensional_sectors.json) and [CSV](two_dimensional_sectors.csv).
- [Independent 2024 wallpaper response comparison](wallpaper_2024_response_comparison.json).

The earlier `two_dimensional_sectors.md` is a historical side-by-side-spin
audit display. Active tables instead have separate files for spinless and
spin-half results, and separate files for zero and all-uniform-IQH sectors.
All current 2D tables have `e0=0`; E8-inclusive tables are deferred. No
saved calculation has been overwritten. The previous combined review is
preserved in Git at commit `8c240ec`.
