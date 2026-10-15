# Fresh campaign evidence — 2026-10-15

The [manifest](manifest.json) records archive hashes, every saved run-file hash,
source commits, hosts and runtime metadata. All recorded source files were
independently checked against their Git commits: 37 files for each CI campaign
at `f572a98`, and 4 files for each E8 extension at `442a2cd`.

- `allfspt_f572a98_point3.tar.gz`: 64 fresh 3+1D CI calculations, split by spin.
- `allfspt_f572a98_special2.tar.gz`: 44 fresh 2+1D diagnostic calculations,
  split into n0=0 and all allowed n0. Both fix e0=0.
- `allfspt_442a2cd_e8_extensions.tar.gz`: 64 selected 3+1D E8 extensions,
  split by spin, including the exact consumed CI results and parent hashes.
- `allfspt_f572a98_launchers.tar.gz`: remote launch scripts and campaign logs.

CI calculations ran on n02.local and n03.local through persistent cluster3
and compute-node SSH masters. Each node ran at most 12 point-group workers
and 6 diagnostic workers concurrently, with 8 GB workspace caps and 7200-second
per-case timeouts. The slowest case was spin-1/2 D6h, at 1577.506 seconds.
The E8 postprocessing ran locally after all new CI calculations completed.
All 108 CI runs and 64 extensions succeeded. The E8 results explicitly retain
the unresolved physical CI-kernel identification caveat.

To regenerate the numerical comparisons in a new directory, run from the
repository root:

```bash
mkdir -p /tmp/insulator-fresh-20261015
tar -xzf results/evidence/four_data_20261015/allfspt_f572a98_point3.tar.gz -C /tmp/insulator-fresh-20261015
tar -xzf results/evidence/four_data_20261015/allfspt_f572a98_special2.tar.gz -C /tmp/insulator-fresh-20261015
tar -xzf results/evidence/four_data_20261015/allfspt_442a2cd_e8_extensions.tar.gz -C /tmp/insulator-fresh-20261015
python3 scripts/report_four_data_campaign.py \
  --ci-root /tmp/insulator-fresh-20261015/f572a98-point3-spinless \
  --ci-root /tmp/insulator-fresh-20261015/f572a98-point3-spin_half \
  --ci-root /tmp/insulator-fresh-20261015/f572a98-special2-n0-zero \
  --ci-root /tmp/insulator-fresh-20261015/f572a98-special2-n0-all \
  --e8-root /tmp/insulator-fresh-20261015/f572a98-e8-point3-spinless \
  --e8-root /tmp/insulator-fresh-20261015/f572a98-e8-point3-spin_half \
  --output /tmp/insulator-fresh-report-20261015
```

The command regenerates tables and numerical/provenance checks. The published
index pages additionally contain the reviewed scientific interpretation.
Original absolute paths in run metadata describe where the calculations
actually executed and are retained unchanged.
