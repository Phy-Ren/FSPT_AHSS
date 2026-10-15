# Immutable campaign evidence

The [2026-10-15 evidence](four_data_20261015/README.md) separately preserves
108 new CI calculations, 64 selected-model E8 extensions, launchers, logs and
source-commit checks. The archives described below belong to the earlier runs.

`two_dimensional_runs.tar.gz` contains the four 2D campaigns (108 calculations).
`three_dimensional_runs.tar.gz` contains the 3D campaign (64 calculations).
The [manifest](manifest.json) records archive hashes and a SHA-256 for every
saved run file. All 172 classifications completed successfully on `n01.local`.

Every case retains its symmetry input, generated GAP driver, stdout/stderr,
runner metadata, native result, and complete result with root witnesses and
integer presentation. Each campaign retains the selected cases and its runtime
source manifest. Git commits `23f9d9c` and `cd8b24d` preserve the source snapshots.
Absolute paths inside recorded commands describe the actual remote run.

To inspect and regenerate the saved summaries in a new directory:

```bash
mkdir -p /tmp/insulator-evidence
tar -xzf results/evidence/two_dimensional_runs.tar.gz -C /tmp/insulator-evidence
tar -xzf results/evidence/three_dimensional_runs.tar.gz -C /tmp/insulator-evidence
python3 scripts/report_campaign.py \
  /tmp/insulator-evidence/cd8b24d-uniform-point2 \
  /tmp/insulator-evidence/cd8b24d-uniform-wallpaper \
  /tmp/insulator-evidence/23f9d9c-point3 \
  --output /tmp/insulator-report
python3 scripts/summarize_results.py /tmp/insulator-report \
  --output /tmp/insulator-summary
```

The source-hash checks concern the archived runtime manifests and saved inputs;
comparison reports also record the independently versioned benchmark files.
Later audit scripts and diagnostic fields do not retroactively modify an older
run. In particular, the original 3D records predate the additional
`nativeChainIdentitiesVerified` field in the full-IQH 2D snapshot. Independent
audits in [../audits](../audits) retain their own provenance and scope.
