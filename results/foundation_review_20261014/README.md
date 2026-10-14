# Interacting insulator comparisons

Choose the spacetime dimension first. Each dimension has its own directory
and index; within it, physical spins and response sectors have separate files.

- [2+1D results](2p1d/README.md)
- [3+1D results](3p1d/README.md)

**✓** means the reported classification groups match; **×** means they
differ. `UNVERIFIED` and `N/A` are separate from mismatches. A match does
not by itself identify physical generators. Sources and publication
versions retain separate columns.

E8 decoration remains deferred. Current 2+1D tables use `e0=0`; E8-inclusive
results have no classification table. See the separate dimension indexes
for the deferred scope files.

## Provenance

Markdown, CSV and JSON contain the same cases and classification values.
The [reference policy](../../docs/foundations/interacting_reference_policy.md),
[correction audit](../../docs/foundations/corrections_and_versions.md),
[version ledger](../../docs/reference_ledger_20261014.md), and
[D2/D6 grading audit](../../docs/foundations/debray_d2_grading_audit.md)
retain source qualifications. Raw references and calculation archives are
unchanged. Earlier layouts remain in Git history.

Regenerate with `python scripts/build_foundation_tables.py`.
The [validation record](table_validation.json) records input hashes and
checks that dimension, physical spin and response sectors remain separate.
