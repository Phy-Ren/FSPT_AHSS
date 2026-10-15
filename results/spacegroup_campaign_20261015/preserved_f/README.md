# Preserved F results: 3+1D space groups

This immutable package preserves four completed calculations from the two deliberately stopped F pilots. It includes the original result bytes, exact input/source/log/witness artifacts, cancellation identity evidence, selected neutral E8 extensions and collector acceptance. No unfinished native result is accepted.

| Node | Ordinary complete | Recovered complete | Cases requiring another result |
|---|---:|---:|---:|
| n02 | 2 | 0 | 2 |
| n03 | 0 | 2 | 4 |

The ordinary results are SG221 spin-half and spinless. The recovered results are SG214 spin-half and SG138 spin-half. A recovered result has `status: recovered_complete`: its exact driver completion marker, complete native witnesses and independently checked presentation/filling/chain certificates survived the verified process stop. Its new metadata does not invent a successful process exit, start timestamp or elapsed duration. Original source files, run metadata and logs remain unchanged inside the archives.

All four selected neutral E8 extensions and their exact CI parents passed the recovery-aware collector. This certifies computation in the selected four-data model; each extended record retains `physicalClassificationCertified: false`. No full physical-spectrum identification is inferred from preservation or acceptance.

Six original assignments lack `native.json`: SG141 both spins, SG229 both spins, SG138 spinless and SG214 spinless. They remain explicitly excluded. SG214 spinless already has an accepted independent E result. SG138 spin-half is the newly retained case needed to reduce H to five missing assignments. SG221 both spins and SG214 spin-half overlap other accepted evidence; the final catalogue must select an exact parent rather than count duplicates.

`archives/` contains the two byte-exact remote evidence tarballs and the small frozen postprocessor source archive. The former contain complete preserved CI/E8/acceptance/stop/log trees. `nodes/` mirrors only small metadata for inspection; `archive_mirrors.json` binds every mirror to its exact archive member. Original automatic finalizer reports are separately retained with state `incomplete`. They were produced before recovery, correctly rejected the stopped original batches, and are not rewritten as successful reports. The postprocessing log snapshot inside each tarball ends at `archiving`; the external `archive_metadata.json` records final completion and the resulting archive hash.

The original F runtime source manifest SHA256 is `67b361e640a9ea5b598b0e9fbde7399f2a7988285a61081684327c8870babe2d`. Preservation, E8 extension and acceptance used an isolated export of commit `5ed6b9c5e1acead350424aff7073b0c83d4d09e6` with Python 3.8.16. Its 42 file hashes and source archive are retained. No classification or process signal is performed by this package.

Run `python results/spacegroup_campaign_20261015/preserved_f/verify.py` for package, source, archive, ledger, input/run, exact CI/E8 parent and acceptance hash checks. It does not recompute the Smith/filling certificates by default. For the full frozen replay, extract `archives/f-preserve-5ed6b9c.tar.gz` to a temporary directory and pass that path as `--validator-root`. The saved local replay logs, `local_replay_verification.json` and a fresh replay directly from this package (`packaged_frozen_collector_replay.log`) record this stronger check for all four cases, including exact output and validation hashes. Temporary filesystem paths can change provenance paths, but cannot change the accepted mathematical artifacts.
