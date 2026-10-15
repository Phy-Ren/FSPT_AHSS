# Accepted local SG221 spinless result

This package preserves one ordinary completed local classification of space group 221 (`Pm-3m`, spinless), its independently computed neutral E8 extension, and the strict collector's accepted records. It can supply this case to the full 460-case catalogue without waiting for the older duplicate F job. It is a completed result with full roots and witnesses, not recovery of an unfinished native file. No running or frozen cluster campaign was changed by this packaging step.

The selected four-data model gives

- CI sector: $\mathbb Z\oplus\mathbb Z_2^{13}\oplus\mathbb Z_4^2\oplus\mathbb Z_8$.
- Independently computed neutral layer: $H^1(G,\mathbb Z_s)=\mathbb Z_2$.
- E8-inclusive selected section: $\mathbb Z\oplus\mathbb Z_2^{14}\oplus\mathbb Z_4^2\oplus\mathbb Z_8$.

The primitive-cell filling step is 1, with oriented primitive volume 1. Identification of the CI model with the full physical kernel remains a separate mathematical requirement; the archived E8 result retains `physicalClassificationCertified: false` and its original scope statement.

## Preserved artifacts

[raw_ci_e8_acceptance.tar.gz](raw_ci_e8_acceptance.tar.gz) contains 23 original files under `ci/`, `e8/` and `accepted/`. Every file's bytes are unchanged; only the enclosing archive metadata is standardized. [archive_members.json](archive_members.json) records member sizes, hashes and original directories. The archive contains the complete inputs, native/result records, run/source manifests, logs, drivers, E8-consumed CI copy, and accepted collection. It contains no executable or full source checkout.

[source_verification.json](source_verification.json) records verification of all 57 CI source files against the actual calculation source tree. Every file is exactly reconstructible from commit `d922a12` and the four already committed [source overlays](../generic_cochain_performance/sg221/overlay.json). The actual native VM was checked against the recorded SHA256 `7c3288b10176c7fe814c2f202bea4e07bcd0b71a842a80253bb222bba7a0afdc`. The five E8 source files and collector dependencies are pinned to their recorded Git commit. Existing source/equation proof artifacts are referenced by exact path and hash rather than duplicated.

CI result SHA256: `27710b7d678b4d8612b27f84791f508ec87c69bb4c744dd922cac75033d1bc33`.
E8 result SHA256: `3bbd9c882b0d015e922b54598999600c35fd562a6bbc189131ba8ee94fd7eb20`.

## Independent audit and reproduction

Run from this repository with Python, SymPy and the retained Git history:

```sh
python results/spacegroup_campaign_20261015/completed_local221/audit.py
```

The auditor verifies package/member hashes and reconstructs the exact CI/E8 source identities from Git plus the committed overlays. It checks the CI result is byte-for-byte the E8 parent, and both records are exactly those accepted by the collector. It independently recomputes all three Smith groups, the primitive filling relations and gcd, and 51 saved native linear equations: 18 phase closures, 7 charge closures, 1 sheet closure, 8 primitive equations, 8 source closures and 9 gauge-reduced phase closures. The source's 20 completed-state certificates are also retained.

The auditor then imports the pinned three-module E8 implementation in a temporary namespace and repeats its full affine finite-presentation calculation. All 39 affine relators, three primitive translation words, saturated signed cocycle kernel, principal gauge relation and combined presentation are recomputed; the entire E8 classification must equal the saved record exactly. This replays the small neutral extension, not the expensive nonlinear CI solve. [audit_result.json](audit_result.json) is the saved passing output.

For raw inspection, extract the archive to a new directory. For a full CI rerun, reconstruct the pinned base plus the four overlays and use the archived `ci/spacegroup_221_spinless/driver.g` or normal classifier with the archived input and native/cycle mode choices in `run.json`; output paths must be new. The prior [full SG221 control](../generic_cochain_performance/sg221/validation.json) separately establishes exact equality of all 37 non-timing classification fields with the original native-primary/DAG baseline. That validation, source identity and every native witness remain preserved independently of this acceptance package.
