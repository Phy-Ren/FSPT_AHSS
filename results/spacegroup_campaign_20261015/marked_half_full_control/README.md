# Marked-half doubling: complete SG141 spin-half control

The isolated marked-half candidate preserves the complete **3+1D SG141 spin-half CI-sector result**, with six actual marked doubles, but shows **no whole-run performance improvement**. It was not adopted into production, and no marked-only SG226 run was launched. These diagnostics are not catalogue inputs and add no E8 classification.

| GNU time measurement | Baseline d3b2dcc | Marked-half candidate |
| --- | ---: | ---: |
| Actual marked-double hits | 0 | 6 |
| Wall seconds | 1359.28 | 1360.11 |
| User CPU seconds | 1247.99 | 1248.28 |
| System CPU seconds | 1.47 | 2.57 |
| Total CPU seconds | 1249.46 | 1250.85 |
| Maximum resident set size, KiB | 10212128 | 10541104 |
| Formula-worker calls | 64826 | 64826 |

Both cases ran concurrently on n08 with one standalone job, a 16g GAP workspace cap, a 2400-second limit, the same exact input, O2 GAP, VM, Python and classification modes. These are single workload observations. GNU time reports its process high-water metric, not an aggregate simultaneous process-tree peak. The candidate exercised its optimization, but wall time, CPU time and reported maximum RSS all failed to improve. Correctness and operation-count arguments alone do not establish useful whole-run performance.

All **35 scientific and certificate fields** agree literally. Formula calls and cache statistics also agree; only resolution construction timings differ among the saved native fields. Each case ran the full classifier checks. The retained original comparison includes the collector's complete-parent certificate checks and independent Smith/filling validation. The verifier below checks the preserved evidence and exact equality without rerunning those cochain calculations or importing mutable production code. This is implementation agreement, not a physical-spectrum classification claim.

The baseline is reconstructible from Git commit `d3b2dcc6fe9f4ecda3e957d74edae2012ac46198`. Only the two retained files under `candidate_overlay/` change it. Neither the q2 patch nor adjacent native-vector reuse is included. The separately retained prototype proof and peer review bind those exact file hashes; their mathematical evidence does not imply a performance gain.

The standard driver ends in uppercase `QUIT`, which bypasses `InstallAtExit`. An identical external wrapper therefore preserves each original driver and executes a separate `observed_driver.g` with exactly one read-only observer `Read` inserted immediately before the unchanged final `QUIT`. It prints the count after classification, without altering the context or native result. The archive retains the wrapper, observer, original and executed drivers, exact insertion proof, actual GAP executable/argv observation, ordinary case exits and outer exits. A count alone is never treated as completion.

`raw.tar.gz` is the unchanged 276,313-byte acquisition archive: 45 original artifacts plus its capture proof. Before/archive/after hashes, source/runtime/input bindings, admission, measurements and original comparison are retained. The full source archive is not duplicated; the portable verifier reconstructs its 1,268 baseline files from Git and applies only the two stored file replacements. No production runtime, accepted result or source snapshot was changed by this package.

Run:

```bash
python3 results/spacegroup_campaign_20261015/marked_half_full_control/verify.py
```

For a relocated package, add `--repository /path/to/FSPT_AHSS_insulator`. The offline verifier checks exact package and safe archive membership, immutable hashes, Git/overlay sources, exact catalogue bytes, original driver generation, observer insertion and actual executable bindings, both successful exits, raw counts, all 35 scientific fields, and measurements reparsed from GNU time. It does not launch GAP, workers, E8 processing or collection.
