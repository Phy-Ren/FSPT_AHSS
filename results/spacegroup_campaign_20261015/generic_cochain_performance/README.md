# Generic cochain performance evidence

This package records two independently checked exact optimizations, followed
by their combined hard-case comparison. It is a new evidence package; the
earlier `performance/archive_manifest.json` remains unchanged.

`closed_charge/proof.md` proves the full charge-source specialization for an
actual closed integer native charge and half-integral extension. It is an
equality of cochains modulo one, preserving the selected phase primitive.
The old unrestricted source remains available through
`c.closedChargeSourceMode := "reference"`; `"compare"` checks each queried
simplex. Integer charge, nonzero source homotopies, root relations and gauges
are retained.

`cup/peer_review/review.md` proves the ordered-edge replacement without
assuming commutativity, including degree-zero factors. Its original executable
structural check and pinned generic cochain/cut files are included.

| Isolated check | Exact mathematical comparison | Observed local time |
| --- | --- | --- |
| Closed full source, SG195 pair | All 35 nonperformance fields per spin literally equal; 9,664 pointwise checks and 60 even-native zero checks | 41.037 to 33.919 seconds, 1.21 times |
| Ordered edges, SG195 pair | Complete generators, presentation, gauge and filling witnesses literally equal; 19,440 signed/nonabelian comparisons | 63.224 to 39.025 seconds, 1.62 times |
| Native primary, SG221 spin-half | Actual seven-row obstruction map retained in `native_primary_stage/` | 0.547 CPU seconds for this stage only |
| Closed source plus ordered edges, full SG221 spinless | 37 of 38 classification fields literally identical; only resolution timing differs | 429.263 to 268.854 seconds, 1.597 times; peak RSS 2,583,856 to 1,827,896 KiB |

The two SG195 timings use different baseline revisions and are not additive
or directly comparable with each other. Each before/after pair uses the same
host, runtime and inputs. They are observed end-to-end timings, not controlled
microbenchmarks or estimates for every space group. The native-primary timing
does not claim a full-classification speedup.

The full SG221 comparison changes only four GAP files on the exact same
`d922a12` source/runtime baseline and preserves the same native VM binary.
No phase normalization is needed: all completed phase representatives,
obstruction maps, presentation rows, gauge witnesses, sheet lattices and
primitive filling values are literally equal. The baseline's independent
27-by-26 Smith calculation, filling audit and 51 saved native linear-equation
checks are retained under `sg221/baseline/`; their mathematical inputs are
unchanged in the candidate. The computed CI-sector group is
`Z × Z2^13 × Z4^2 × Z8`. This numerical agreement does not enlarge the declared
physical scope of that sector.

The closed-source baseline runtime files match commit `d922a12` exactly. The
earlier ordered-edge baseline is commit
`80d565de744bbd5ef6ac4cca3530511f549547f4`. Every run retains its input/source
hashes and complete result, and each pair retains the full runtime source
manifest. `main_gap_reuse_review.md` documents the actual main-branch path and
the read-only cluster source checks; no superconducting theory engine or
runtime dependency is included here.

Run `python3 check_evidence.py` to verify the archived literal comparisons and
package hashes. The current mathematical regressions are
`tests/test_closed_charge_source.py` and `tests/test_cup_geometry.py` at the
repository root. `focused_tests.json` records their observed passing runs
and the subsequent 14 backend regressions. Original result files intentionally
retain historical absolute paths as provenance.

The original independent SG221 audit driver also verifies its unpacked source
tree and VM binary at those historical paths. They are omitted from this small
package; reproduce the archived record comparison with `check_evidence.py`,
or restore the pinned source snapshot to rerun the original complete audit.
