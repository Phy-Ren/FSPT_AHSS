# Two standalone spin-half jobs with larger workspace limits

This package records the authorized launch of SG226 spin-half and SG230 spin-half on n02 at 2026-10-15 15:49:50 UTC (node clock). It makes no completion or final-catalogue selection claim. All existing G, paired H-tail and standalone spinless jobs were left running.

The two new cases run independently, each with a 32 GiB GAP workspace limit and a 14,400-second timeout. The preceding n02 observation found 16 active GAP jobs, 28 physical cores, load 12.10 and 442.45 GiB of free memory. The captured G226 GAP process itself occupied 8.015 GiB under an 8g workspace limit; its Python worker was small. Prior monitoring found a sustained GAP memory plateau, which motivated this bounded fallback. CPU and RSS observations do not identify garbage collection or prove that increasing the limit improves runtime.

The mathematical source remains frozen commit `ea44c1f55314ddd66587cf452bbaae9331f3a1db`, with 60-file manifest `80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b`. Before launch, all source files, both exact catalogue inputs, source archive, optional formula VM, GAP binary and finalizer were verified. The actual campaign source/runtime/selection metadata then matched. Runner PID42816 and finalizer PID42819 are historical identifiers only.

`initial_metadata.tar.gz` preserves 19 exact initial files, including launchers, source/runtime manifests, selection and both inputs/drivers/run records/logs. `download.json` pins every archive member. This capture shows two running cases and a waiting finalizer. The locale warnings in the SSH launch log precede the explicit campaign `LC_ALL=C` setting; the recorded campaign environment is retained.

`download_tool/` records a separate local downloader, PID459428, configured for this tag only. Its helper is byte-identical to the previously verified downloader; existing downloader files and processes were unchanged. Completion will require the ordinary finalizer, exact archive hashes and frozen collector replay. None of those future completion gates is asserted here.

Run the offline verifier from this repository:

```sh
python results/spacegroup_campaign_20261015/deployment_h_tail_highmem/verify.py
```

The verifier uses the hash-checked shared helpers in `../deployment_h_remaining/` and existing frozen-H provenance in `../deployment_h/`. It checks source/catalogue bytes against Git, the exact two-case standalone configuration, the prelaunch resource sample, finalizer linkage and isolated downloader pins. It does not contact the cluster, query PIDs, launch jobs or signal processes. Inclusion in the final 460-case catalogue requires a separate explicit accepted-source selection.
