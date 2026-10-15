# Completed H high-memory tail: 3+1D spin-1/2

SG226 and SG230 both have ordinary exit-zero CI results, the exact neutral
E8 extension, and accepted four-data output. The full two-case parent finished
finalization at `2026-10-15T18:09:21.458364+00:00`. No stopped-run recovery is used.
These are the two standalone cases in the
[32g launch record](../deployment_h_tail_highmem/README.md).
This package certifies that parent; it makes no completion claim for other
campaigns and does not change the current catalogue.

`raw.tar.gz` preserves the original 162,465-byte finalized archive, SHA256
`502fc8044a4bf0cd92aa59e3d9d634a09e98e9eaf3b7c5366cb7533e986c374f`.
Its original CI inputs, native results, complete roots and witnesses, logs,
result wrappers, E8 output and accepted collection remain unchanged.
`download_verification.json` binds every member and records an exact frozen
collector replay before publication of the local download.

CI used H commit `ea44c1f55314ddd66587cf452bbaae9331f3a1db`, with source SHA256
`80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b`.
E8 and acceptance used G commit `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`,
with E8 source SHA256
`994af05b2ab8cea90002e6c75dd2442736b3f1096bf0ceab98703f6e90dc2214`.
All 60 CI and five E8 source hashes are checked against Git. The runtime
manifest agrees with the launch and records VM SHA256
`0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2`;
the finalizer records unchanged-source and runtime verification. Both jobs
used a 32g GAP workspace limit and a 14,400-second individual timeout.

Independent review reran `verify_h_download` and `validate_parent` on this
complete parent. Their report and exact validator bytes are retained. The
portable verifier checks the launch linkage, frozen catalogue inputs, exact
CI-to-E8 parent bytes, saved completed-root and chain certificates, full and
filtration Smith groups, primitive filling relations and gcd, the E8-first
block presentation, and accepted result hashes. It does not recompute the
nonlinear CI classification.

Run the offline check with Python, SymPy and this Git checkout:

```sh
python3 results/spacegroup_campaign_20261015/completed_h_tail_highmem/verify.py
```

For a relocated package, pass `--repository /path/to/checkout`. Add
`--validator-root /path/to/checkout-at-c07c6e5` to repeat the frozen collector
and recompute the neutral section from both saved CI parents. The recorded
`frozen_replay.json` and log retain this additional check: accepted CI/E8 and
validation bytes reproduce exactly, and both neutral sections agree.

The outputs are accepted computations of the supplied four-data model.
They retain `physicalClassificationCertified: false`; successful computation
does not establish the remaining physical CI-kernel identification. This
review launched no classification jobs and sent no process signals.
