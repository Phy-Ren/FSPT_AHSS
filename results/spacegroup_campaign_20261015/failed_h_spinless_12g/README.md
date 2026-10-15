# Historical SG226 spinless workspace failure, 3+1D

The original standalone 12g SG226 spinless run ended with exit code 1 after
11,708.782 seconds. Its stderr reports GAP workspace exhaustion at
`gasman.c:1379`. It produced neither `native.json` nor `result.json`; it has
no accepted classification. The two-case parent's finalizer is incomplete
and identifies only SG226 spinless for retry.

`raw.tar.gz` preserves all 21 stable original files, including both cases,
source/runtime/selection manifests, launch/finalizer records and logs. Its
SHA256 is `69f2fdfde8c2b17b28b2d8405660bc437aee3c63d69b1056a607a7bfe8ba492f`.
The ordinary-complete SG230 companion is retained unchanged and matches
every case file in the [separately approved singleton](../preserved_h_230_spinless/README.md).
Approval of that singleton does not accept this failed parent.

`gc_evidence.tar.gz` retains the earlier read-only profile and monitoring
package, including raw `perf.data`. The direct five-second user-CPU profile
has 244 samples, predominantly `CollectBags` and GC marking functions.
The separate 198.180-second observation shows constant endpoint RSS and no
formula-worker IPC. These are distinct evidentiary intervals; the short
profile does not identify every instruction in the longer interval. Both
refer to PID11603/startTicks2689930714 and this exact H driver. The eventual
workspace-exhaustion error is retained separately.

The focused offline verifier checks archive/member hashes, all 60 H source
hashes against Git, both frozen catalogue inputs, the original 12g standalone
launch, strict failed status/exit/error and absent native output, unchanged
ordinary SG230 bytes, finalizer state, and GC-evidence linkage. It launches
no classification and performs no new profiling or process actions.

```sh
python3 results/spacegroup_campaign_20261015/failed_h_spinless_12g/verify.py
```

For a relocated copy, pass `--repository /path/to/checkout`. Original records
were not rewritten. The distinct 32g H shadow and q2 diagnostic are outside
this historical evidence package and retain their own acceptance requirements.
