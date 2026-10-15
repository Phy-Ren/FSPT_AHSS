# Completed H remaining n02: twelve 3+1D space-group cases

All twelve selected cases have ordinary, exit-zero CI results, the exact
neutral E8 extension and accepted four-data output. The finalizer completed at
`2026-10-15T16:46:26.705136+00:00`. No stopped-run recovery is used.

The completed selection is SG133, SG201 and SG210 spinless; and SG140, SG142,
SG206, SG219, SG220, SG223, SG224, SG227 and SG228 spin-half. These are the exact
n02 assignments in the [immutable launch plan](../../deployment_h_remaining/README.md).
This package certifies this twelve-case shard, without asserting completion of
other campaign shards or changing the current catalogue.

`raw.tar.gz` is the byte-exact 635,312-byte finalized archive, SHA256
`8e98548743b45eb6168adbdf0dc62c712dfd63b795f8cd3a75d7222d71246e74`.
Its 144 files retain the original CI inputs, native outputs, roots, witnesses,
logs and result wrappers, plus the full E8 and accepted-output trees.
`download_verification.json` binds every original member and records a successful
frozen-collector replay before atomic publication of the local download.

CI used frozen H commit `ea44c1f55314ddd66587cf452bbaae9331f3a1db`, source SHA256
`80e0a57b1ac611b348d748da2becbfe64d4aa17f196df9ffae3addea3e22940b`.
E8 and acceptance used frozen G commit `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824`,
with E8-source SHA256
`994af05b2ab8cea90002e6c75dd2442736b3f1096bf0ceab98703f6e90dc2214`.
All 60 CI and five E8 source-file hashes are checked against Git. The runtime
manifest exactly matches the launch and records native-VM SHA256
`0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2`;
the finalizer records unchanged-source and runtime verification.

Independent review ran `check_readiness.verify_h_download` and
`validate_parent` on the complete downloaded parent. Their exact report and
validator bytes are retained. The portable verifier also checks input bytes
against the frozen catalogue, exact CI-to-E8 parent bytes, completed-root and
chain certificates, full/filtration Smith groups, filling relations and gcd,
the E8-first block presentation, and every accepted result/hash. It verifies
saved CI certificates without recomputing nonlinear CI cochains.

Run the default offline check with Python, SymPy and this Git checkout:

```sh
python3 results/spacegroup_campaign_20261015/completed_h_remaining/n02/verify.py
```

Use `--repository /path/to/checkout` for a relocated package. Add
`--validator-root /path/to/checkout-at-c07c6e5` to repeat the frozen collector
and recompute the neutral section from each complete CI parent. The recorded
`frozen_replay.json` and `frozen_replay.log` preserve this additional review:
all accepted CI/E8 results and validation bytes reproduce exactly, and all
twelve recomputed neutral sections and full presentations agree. Temporary
replay paths change provenance paths only; original bytes remain unchanged.

These are accepted computations of the supplied E8-inclusive four-data model.
Every result retains `physicalClassificationCertified: false`; the remaining
physical CI-kernel identification is not established by successful computation.
No classification jobs or process signals were issued by this review.
