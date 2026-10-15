# Preserved D campaign: 3+1D space groups

This archive preserves 250 completed CI calculations and their newly computed E8 extensions after the deliberately stopped D campaign. The three original compressed archives are stored byte for byte; extracted result directories are not duplicated here. This is calculation evidence for the selected four-data model, with `physicalClassificationCertified=false`.

| Node | Ordinary complete | Recovered complete | Preserved and E8 accepted | Retry |
|---|---:|---:|---:|---:|
| n02 | 52 | 24 | 76 | 88 |
| n03 | 46 | 28 | 74 | 90 |
| n08 | 82 | 18 | 100 | 32 |
| Total | 180 | 70 | 250 | 210 |

All 210 excluded cases lack a completed `native.json` (140 cases) or were never started and lack `input.json` (70 cases). No existing completed native result was rejected. Exact retained IDs, retry reasons and copied-file hashes are in `nodes/*/recovery.json` and `nodes/*/retry.json`.

The 70 recovered wrappers retain the distinct status `recovered_complete`. They do **not** assert a successful process exit or invent execution timestamps. Acceptance requires the saved closed-output marker, exact input/source/log bytes, native completion and chain certificates, independent presentation and filling checks, and the separately recorded verified stop evidence. Ordinary completed wrappers remain unchanged. The E8 extension and collector explicitly used `--allow-recovered`; their normal default remains strict. The original D campaign was not edited during preservation.

The CI computations retain source manifest SHA256 `63887ca47cf557f30a3a867bac16392b05c8d107a8cdb87ffbd4d47784ccdc88` from frozen snapshot C, using the optimized GAP executable for campaign D. Preservation, E8 extension and acceptance used repository commit `6065593d15a85c9e6eff57e8fcc4bb1413d5ae56` and Python 3.8.16. Per-node archives include original inputs, native results, witnesses, drivers, logs, stop/process evidence, recovery ledgers, E8 results, collector acceptance and exact postprocessing commands. `nodes/*/archive_metadata.json` records the final archive checksum; the status inside each archive accurately records the earlier `archiving` stage.

An initial orchestration attempt failed before preservation because the compute-node Git did not support `git -C`. The successful external wrapper used a subprocess working directory instead. Frozen repository sources were unchanged; the failed launch logs remain on the cluster.

Run `python results/spacegroup_campaign_20261015/preserved_d/verify.py` from the repository to verify every packaged byte, archive/manifest correspondence, all saved case identities/statuses and acceptance cross-links. This default check audits preserved evidence; it does not rerun classifications. To independently repeat the original collector checks, add `--validator-root /path/to/checkout-at-6065593`; the verifier requires the frozen helper/collector bytes and extracts only into a temporary directory. SHA256 manifests cover every package file except the manifest itself.

The optional replay was also executed successfully on all 250 cases from a fresh extraction of commit `6065593`: `frozen_collector_replay.log` preserves its output. The repeated CI results, E8 results and validation reports have exactly the original hashes. The generated provenance paths change because replay uses temporary local directories; that path change is not rewritten into the archived evidence.

The separate [G deployment record](../deployment_g/README.md) proves the disjoint coverage plan for the remaining work. It does not promote launched jobs to completed results.
