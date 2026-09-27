# Measured allocation environment

Byte-preserved observations taken inside the five campaign PBS allocations.
`summary.json` contains the relative SHA-256 inventory and separates the first
failed probe launches (missing probe script) from the successful short retries.
No GAP computation was launched by these probes.

All five nodes reported Intel Xeon E5-2680 v4 at 2.40 GHz and 56 host logical
CPUs. Each job's own PBS node file contained 28 slots: 140 allocated slots in
all. The worker limit was 28 single-threaded GAP processes per allocation.

Host MemTotal was 504.526 GiB on n01–n04 and 125.776 GiB on n05. These are
host totals, not per-job memory limits or simultaneous memory usage. Per-task
peak RSS belongs to the accepted campaign's separate performance report.
The probe also records Python, kernel, exact job IDs, and node clocks. Campaign
elapsed times use the single login-node observer, not differences between
unsynchronized node timestamps.

Original archive: `runs/hardware_20260926/` on the project working tree.
