# Symmetry-notation migration verification

The current convention is `s` for antiunitarity, `r` for charge reversal, and `rho = r XOR s` for the circle action. The Python API stores `s1,r1` and derives `rho1`. Explicit `s,r` requests default to schema version 2; generated inputs include the version tag. A supplied circle character is checked. Historical `rho = charge` inputs require the named legacy adapter or an explicit legacy version/tag.

The unmodified commit `45c37e9` was executed in a separate checkout to obtain 60 exact reference evaluations. These cover spatial dimensions 2, 3, and 4, all four independent sign choices, and source, integer obstruction, product, integer product, and gauge operations on completed lower towers. In two dimensions, antiunitarity enforces zero uniform CI decoration. Both canonical and explicitly migrated requests reproduce every reference output. The baseline fixture records the old convention and was not derived from the renamed implementation.

The regenerated source and product DAGs retain all 1,876 and 3,391 arithmetic instructions, respectively, including their operand indices and final denominators. Only the charge input label changes. The generic native VM source is unchanged; native, exact fallback, overflow, and source-hash checks ran in the existing test suite.

The full suite passed **196 tests in 109.772 seconds**, with no skips. A final guard rejects invalid schema versions before control operations return; the five focused migration tests were then rerun successfully. Those tests also distinguish ordinary time reversal from the effective crystalline mirror in GAP, check both characters at the API boundary, exercise explicit legacy conversion, and verify file immutability. Commands, durations and fixture hashes are in [the JSON report](notation_v2_migration.json); the [full-suite log](notation_v2_full_suite.log) and [final focused log](notation_v2_focused_final.log) are retained.

All 578 current catalogue backgrounds were regenerated with the new fields. The 20 current tables retain all 4,878 displayed group values across 742 rows; see [the catalogue audit](../../insulator_catalog/notation_migration.json). Historical inputs, raw results, source fixtures, logs, and witnesses remain unchanged. Collectors translate only identified background and coefficient metadata in memory.

This verifies the notation and interface migration. It does not enlarge the physical classification domains or resolve the pre-existing higher-dimensional proof boundaries.
