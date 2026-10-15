# G deployment evidence: 3+1D space groups

This package records the immutable launch plan, exact commands, source manifests and formula-runtime provenance for campaign G. Launch evidence is not evidence that a calculation has completed. Accepted results are collected separately.

| Node | Cases | Group tasks | Maximum workers | Memory per worker | Recorded runner PID |
|---|---:|---:|---:|---|---:|
| n02 | 56 | 44 | 48 | 8g | 40405 |
| n03 | 60 | 47 | 48 | 8g | 38671 |
| n08 | 85 | 43 | 24 | 4g | 9271 |

All 201 launched cases are disjoint from the D preserved results and the reserved E/F controls. `coverage_partition.json` proves exact coverage of both spins for all 230 space groups: 250 preserved D cases, 8 F-pilot assignments beyond D, 1 completed E-only case (`spacegroup_014_spinless`), and 201 G cases. Assignment gives D precedence, then F, then E, so repeated controls are counted once. In particular, `spacegroup_214_spinless` appears in both E and F and is assigned to F here. This partition records coverage at launch, not the later completion status of F or G.

The frozen G snapshot is commit `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`, source manifest SHA256 `17150f175fffd703f2d1008ec0066f53f25d23abfc63dbb15dd71440243a08fc`, and original snapshot archive SHA256 `307a554bb6ceb3126223a97263103cfcd21715d61fef2f1a75cbcd92e6795279`. Launches use the separately built GAP 4.13.1 `gap-o2`, the native charge-primary path, cycle-based phase-class transfer, certified closed-charge source, and paired-spin execution where both cases remain selected. Each recorded command sets a 14,400-second timeout. These are exact infrastructure optimizations; they do not replace obstruction, gauge or stacking calculations.

The optional integer DAG VM is copied unchanged from F after comparing its C++ source and both generated U1 DAG files. `vm_reuse.json` and `original_vm_build.json` record that proof, the compiler/options and binary SHA256 `0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2`. Mode `auto` retains the exact Python fallback. No compiled binary is duplicated in this package.

`metadata_origins.json` maps the byte-exact files to their cluster paths. `remote_verification.json` records a read-only check of every declared snapshot source file, the original source archive, and the chosen formula library. `nodes/*/source.json` retains the source hashes and `nodes/*/formula_runtime.json` retains the selected runtime. The original snapshot archive remains at `/home/user/xyren/AllFSPT_insulator/snapshots/sgfull-20261015-g.tar.gz`; its source is also preserved by the recorded Git commit.

`finalizers/` separately preserves the two external postprocessing scripts and their five launch records for G's three shards and F's two pilots. These processes wait for their recorded classifier runner, then perform ordinary E8 extension and acceptance using the appropriate frozen snapshot. Their launch records do not assert that postprocessing has finished. The separate E-smoke finalization and its failed initial attempt belong to the E evidence, not this G launch package.

Run `python results/spacegroup_campaign_20261015/deployment_g/verify.py` from this repository. It checks package hashes, the exact 460-case partition, D ledger links, launch/plan/selection correspondence, all VM provenance links, and each source file against the recorded Git commit. It does not query or signal the recorded PIDs, launch jobs, or accept unfinished cases. See the separate [D preservation package](../preserved_d/README.md) for the accepted 250-case evidence.
