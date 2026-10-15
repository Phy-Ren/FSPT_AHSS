# Completed G evidence: 3+1D space groups

This package contains completed shards only. The original [G launch package](../deployment_g/README.md) remains unchanged.

| Node | CI cases completed | E8 extensions accepted | Finalization finished (UTC) |
|---|---:|---:|---|
| n08 | 85 | 85 | 2026-10-15 14:08:08 |

The byte-exact compressed archive includes all original CI inputs, completed wrappers, native outputs, witnesses and logs, plus E8 extensions and collector acceptance. The external `finalization.json` records the exact commands, verified source/runtime, selection hash, finalization time and archive checksum. The archive SHA256 is `9c1b4ebd39d20d0f9b846f132fb8809c4c5ff4ed7509297b26fecaaa3b1228fd` (1,907,076 bytes). It was downloaded only after the finalizer reported `complete`; that report was unchanged across the download.

All 85 CI wrappers have ordinary `complete` status and exit code zero. No stopped-run recovery is used here. Their selected IDs exactly match the n08 G launch and remain disjoint from the preserved D results. Both computation and postprocessing use frozen source G (`c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`), source manifest SHA256 `17150f175fffd703f2d1008ec0066f53f25d23abfc63dbb15dd71440243a08fc`. VM and source identities agree with the launch evidence. These are accepted calculations of the selected E8-inclusive four-data model; `physicalClassificationCertified` remains false.

Some raw per-case elapsed times are negative and must not be used for speed comparisons; `nodes/n08/timing_caveat.json` lists them. The paired runner derives the first duration by subtracting the compute-node start time from the shared-file modification timestamp, which can use a different clock. The archive retains these values exactly. Separately measured batch elapsed times remain available; this timing issue does not change native results or acceptance.

Run `python results/spacegroup_campaign_20261015/completed_g/verify.py` to check package and archive hashes, original-byte manifest copies, launch links, all native/result/run identities, and collector provenance. Add `--validator-root /path/to/checkout-at-c07c6e5` to repeat the exact frozen collector in temporary directories. The recorded replay also checks that CI results, E8 results and validation hashes reproduce exactly; provenance paths differ only because replay uses local temporary directories. Other G and F shards are not claimed complete by this package.
