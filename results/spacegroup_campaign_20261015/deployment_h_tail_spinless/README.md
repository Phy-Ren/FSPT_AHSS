# Two standalone spinless tail jobs

This package records the authorized launch of SG226 spinless and SG230 spinless on n08 at 2026-10-15 15:38:19 UTC (node clock). It makes no completion or final-catalogue selection claim. The existing paired H-tail and original G jobs were left running.

Each case has its own GAP process, a 12 GiB GAP workspace limit and a 14,400-second timeout. Two jobs run concurrently. The prelaunch observation found only the two existing paired H-tail GAP jobs, 28 physical cores, load 1.62 and 112.2 GiB of free memory. Both paired jobs were still on their first, spin-half member after 38.5 minutes; the two spinless calculations had not started. The additional jobs remove that scheduling dependency, without changing the mathematical source.

The source is frozen commit `ea44c1f55314ddd66587cf452bbaae9331f3a1db`, with 60-file manifest `80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b`. The launcher checked all source files, exact catalogue inputs, source archive, optional formula VM, GAP binary and finalizer before starting. The captured campaign metadata then matched those pins. Runner PID11599 and finalizer PID11605 are historical identifiers only.

`initial_metadata.tar.gz` preserves 19 exact initial files, including the launchers, source/runtime manifests, selection, both inputs/drivers/run records and initial logs. `download.json` pins every archive member. The archive was captured while the finalizer was waiting and both cases were running. The locale warnings in the local SSH launch log precede the explicit campaign `LC_ALL=C` environment; the recorded campaign environment is retained in the launch record.

`download_tool/` records a separate local downloader, PID358717, configured for this tag only. Its helper is a byte-identical copy of the already verified completion downloader. The existing downloaders and their files were unchanged. On completion it will require the ordinary finalizer, exact archive hashes and a frozen collector replay; this package does not claim that those future gates have passed.

Run the offline verifier from this repository:

```sh
python results/spacegroup_campaign_20261015/deployment_h_tail_spinless/verify.py
```

The verifier uses the shared, hash-checked helpers in `../deployment_h_remaining/` and the existing frozen-H provenance in `../deployment_h/`. It checks source and catalogue bytes against Git, exact two-case standalone configuration, resource preflight, finalizer linkage and isolated downloader pins. It does not contact the cluster, query PIDs, launch jobs or signal processes. Acceptance of either result in the final 460-case catalogue remains a separate explicit selection step.
