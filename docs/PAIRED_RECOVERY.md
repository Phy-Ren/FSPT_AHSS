# Preserving completed cases after a paired campaign stops

`scripts/recover_paired_campaign.py` is an offline preservation and validation
tool. It does not inspect a live process, issue a signal, restart a calculation,
or modify an original campaign. Its supported scope is the paired 3+1D
space-group runner. The original CI calculation and E8 physical-scope caveats
remain unchanged.

A pair can finish its first native calculation while its second spin is still
running. GAP closes the first `native.json` stream and emits
`U1_PAIR_CASE_DONE <case-id>`. If the Python parent is externally terminated
before materializing result wrappers, the first calculation can be complete
although its original `run.json` still says `running`. Neither a JSON file by
itself nor elapsed wall time is a sufficient completion certificate.

## What is accepted

The tool requires a separately captured stopped-campaign report. It verifies
that all used original bytes match the report's post-stop hashes. It then
checks, for each case:

1. Original input and source identities, the exact ordered paired IDs, the
   immutable driver/source path, and a complete, unique marker line. The
   driver must emit that marker after closing the native output stream.
2. Well-formed native JSON, complete root vectors in the recorded resolution
   dimensions, exact integer/rational values, root/gauge witness lists, a
   positive completed-state check count, and true saved chain/character flags.
3. Independent Smith reduction of the complete integer presentation, and
   independent primitive-cell filling checks against every relation, the
   generator gcds, the root decomposition and the primitive-cell volume.
4. For a missing result wrapper, a captured GAP identity with exact node,
   PID, UID, PGID, Linux start ticks, executable path/hash and argv; an owned
   parent chain to the captured runner; matching immutable launch arguments;
   and a post-stop report showing no active owned descendants.

Checking saved chain flags does not re-run the chain-map proof or the full
classification. The independent arithmetic checks are Smith/filling checks;
the original solver's completed-state and chain certificates are retained as
such, with their complete native witness bytes.

The preserved first result gets status **`recovered_complete`**. It does not get
an invented `exitCode=0`, elapsed time, start/completion time, or batch exit code.
Its original execution metadata is retained byte for byte under `_recovery/`.
The recovery preparation time is a separate, accurately recorded event.
Already materialized ordinary complete results keep their original `run.json`
and `result.json` bytes, including any original batch exit status. They do not
need a still-live GAP identity to be reconstructed.

Missing markers, incomplete JSON, failed certificates, uncaptured process
identities, or inconsistent case evidence put that case in `retry.json`. A
malformed or unconfirmed stop report rejects preservation before creating any
output. Only accepted native calculations appear in the new subset; incomplete
native outputs are not copied into accepted case directories. The original
campaign remains unchanged. An existing destination is always rejected.

## Stop-report contract

The caller supplies `cancellation.json`, schema `u1-paired-stop-v1`, plus its raw
process-observation files. This is an explicit external attestation: an offline
program can check its identities, hashes and consistency, but cannot itself
establish that a remote process has stopped. The stopping procedure must capture
identities before stopping and check them again before signaling; PID reuse
must never authorize a signal or a recovery.

Required top-level fields:

- `originalCampaignRoot`, `sourceSnapshotPath`: absolute original paths, which
  can differ from a later local download location.
- `sourceSHA256`: the original source manifest's content digest;
  `sourceSnapshotVerified: true` and `verifiedSourceSHA256`: the same digest
  after independently rehashing **the original recorded file list** under the
  snapshot after stopping. Cancellation skips the runner's normal final source
  check, so a pathname alone cannot replace this verification.
- `stoppedObservedUTC`: the actual UTC stop-observation time;
  `allOwnedProcessesStopped: true`.
- `processes`: captured complete identities with `host`, `pid`, `ppid`, `pgid`,
  `uid`, `startTicks`, `argv`, `role`, `executablePath`, `executableSHA256`, and
  `observedState` equal to `absent` or `zombie`. The runner argv must identify
  this exact campaign and snapshot's `scripts/classify.py`.
- `batches`: captured active paired groups. Each entry has ordered `caseIDs`,
  `host`, `gapPID`, `runnerPID`, `launchedCommand`, `launcherPath`,
  `launcherSHA256`, `allOwnedDescendantsStopped: true`, and
  `remainingOwnedPIDs: []`.
- `artifactsSHA256`: paths relative to the original campaign and hashes of
  post-stop bytes. Include source/selection, all selected case inputs, runs,
  existing results/native files, drivers/logs, and any existing root
  `summary.json`, `formula_runtime.json` or `runtime_plan.json`.
- `evidence`: nonempty `{path, sha256}` records for the raw before/after process
  observations. Paths are relative to `cancellation.json`'s parent and are
  preserved with the report.

The actual GAP executable may differ from the launcher in `run.command`.
`batch.launchedCommand` must equal that original vector. Actual captured GAP
argv must end with **exactly `launchedCommand[1:]`**, including the immutable
driver path; launcher-added arguments such as `-l` may precede that suffix.
Both the launcher and actual executable identities are recorded separately.

Initially defunct processes without a durable argv/executable identity can be
kept in raw evidence or a separate `uncapturedExitedProcesses` field. They
cannot serve as the captured GAP/runner identity for a recovered case. Missing
captures cause retries, not an inferred process identity.

If the original campaign has `formula_runtime.json`, the stopper must also
confirm its recorded optional library hash or absence and set
`formulaRuntimeVerified: true`. The recovery copies this original runtime
record without alteration.

## Output and explicit opt-in

Preparation, after a separately authorized stop has actually completed:

```sh
python scripts/recover_paired_campaign.py \
  --campaign /download/original-campaign \
  --stop-report /download/stop-evidence/cancellation.json \
  --output /new/recovered-subset
```

`--case` can be repeated to restrict the requested cases. The output contains a
new filtered selection, accepted raw case files, a retry list, original report
and evidence, original run/selection metadata, and `recovery.json` with copy
mappings, hashes and independent check results. No operation in this command
stops or accepts a production campaign implicitly.

Both downstream programs remain strict by default. Recovery requires an
explicit opt-in and full revalidation of the copied proof:

```sh
python scripts/extend_e8_3p1.py --ci-root /new/recovered-subset \
  --allow-recovered --output /new/e8-subset
python scripts/collect_expansion.py --ci-root /new/recovered-subset \
  --e8-root /new/e8-subset --allow-recovered --output /new/accepted-subset
```

The E8 API's optional `recovery_root` is bound to the exact result stored under
that validated root. It does not accept a caller-supplied success Boolean or a
modified `complete` copy. Its normal result is a newly executed E8 extension,
with the original recovered CI run and proof identity retained explicitly.
The collector checks that its E8 parent bytes are the same validated CI artifact.
No group classification or witness value is altered to accommodate recovery.

`tests/test_paired_recovery.py` uses copied immutable SG19 fixtures and synthetic
process records; it sends no signals. It tests recovery and retry separation,
raw-byte preservation, strict defaults, the full CI-to-E8-to-collector path,
missing identity fields, mismatched argv/parent/source evidence, incomplete
output, invalid presentations/filling/chain certificates, and post-recovery
mutation or fabricated exit status. A separate owned local process fixture can
test a stopping procedure; it must never target a real campaign merely to test
this offline tool.
