# Completed H SG226 spinless: 3+1D

SG226 (`Fm-3c`), spinless, finished the unchanged H classifier with ordinary
exit zero in 11,628.434 seconds on `n08`. Its E8-inclusive four-data result was
accepted at `2026-10-15T22:02:38.112154+00:00`:

| E8 layer | CI/charge/phase sector | Final stacking group | Filling step |
|---|---|---|---|
| $\mathbb Z_2$ | $\mathbb Z\times\mathbb Z_2^4\times\mathbb Z_4^3$ | **$\mathbb Z\times\mathbb Z_2^5\times\mathbb Z_4^3$** | 2 |

This is the complete singleton parent selected for the full 460-case catalogue.
It uses the original H formulas with a 32g workspace limit and a 14,400-second
timeout. The separate q2 diagnostic is not selected. The earlier 12g failure
remains historical evidence and contributes no result.

`raw.tar.gz` preserves the original 97,219-byte finalized archive, SHA256
`5e10ffe764668ddc6ef8d75f029f888c22f7bcf5b594eee8263ba251eab78578`.
The archive retains exact inputs, driver, complete native roots and witnesses,
run logs, E8 cocycle and gauge witnesses, and accepted collection. Download
verification binds every original member and records exact frozen collection
replay. Launch, admission and finalizer metadata are checked against the original
captured records; compressed JSON files preserve those records byte for byte.

CI source: H commit `ea44c1f55314ddd66587cf452bbaae9331f3a1db`, source SHA256
`80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b`.
E8 and collector: G commit `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`,
E8 source SHA256
`994af05b2ab8cea90002e6c75dd2442736b3f1096bf0ceab98703f6e90dc2214`.
The verifier checks all 65 CI/E8 source files against Git and checks the recorded
VM hash and launch/input/runtime bindings.

Run with Python, SymPy and this Git checkout:

```sh
python3 results/spacegroup_campaign_20261015/completed_h_226_spinless/verify.py
```

A relocated package accepts `--repository /path/to/checkout`. Add
`--validator-root /path/to/checkout-at-c07c6e5` to repeat the frozen collector and
recompute the exact neutral section from the unchanged CI parent. The saved
`frozen_replay.json` records this additional check. Independent integer checks
recompute full and filtration Smith groups, filling relations and gcd, and the
E8-first block presentation; saved chain/completion certificates and complete
witness structures are checked. This does not recompute the nonlinear CI
classification. The existing singleton download verifier and full-parent
readiness validator were also rerun successfully.

The result is accepted for the supplied four-data model and retains
`physicalClassificationCertified: false`; the physical CI-kernel identification
is not established by this computational acceptance. Packaging launched no
classification jobs and sent no process signals.
