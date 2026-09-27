# Spinless campaign compute environment

These are exact allocation, resource-probe and release records for the five
PBS workers used by the spinless baseline, optimization controls and accepted
campaign. Both conventions' small regression controls shared the workers.
Per-campaign timings and maximum single-task RSS are recorded separately in
their own campaign archives; these observations are not exclusive-node tests.

The initial five resource probes failed because this older system's ps does
not support the requested etimes field. Their original failures are retained.
They are monitoring failures, not failed space-group computations. Subsequent
probes use /proc and are preserved with the corrected probe source.

Scheduler stdout files are included only when actually available. Availability
is listed explicitly in archive.json. Some completed PBS jobs report a failed
stdout transfer because the old compute-node SSH client rejects options in the
account's SSH configuration; the exact scheduler diagnostics remain in the
release record. Missing scheduler stdout is not reconstructed. Numerical task
stdout, exit status and timing files are written independently to shared storage
and are archived separately with the numerical campaigns.

The summary excludes the short monitoring process itself from numerical task
counts. Summed process-tree RSS can double-count shared pages and is not actual
physical memory consumption. CPU percentages average over each process's age;
they are not instantaneous samples. MemTotal is installed host RAM. Missing
MemAvailable on these older kernels is not interpreted as zero or reconstructed.

All original files have SHA-256 entries in archive.json. stdout.log is retained
byte-for-byte under the name stdout.txt. The release record binds each STOP to
its original worker, queue and exact PBS job; no other user's job is modified.
