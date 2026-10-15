# Twelve further G/H scientific-output comparisons

All twelve frozen G/H native classifications have **34 literally equal
scientific fields**. Completed roots and native phases, obstruction/kernel
maps, gauge and root witnesses, presentations, filtration and filling agree
without a coordinate change or phase normalization. The only differences are
execution fields: `formulaCacheStats`, `formulaWorkerCalls`,
`pairedGeometryReuse` and `resolutionBuildTimings`.

The capture distinguishes two kinds of case records:

- **Both ordinary case records complete (5):** SG133, SG134, SG201, SG203 and
  SG218, all spinless. Each G and H record has its own complete, exit-zero
  `result.json` matching its saved input, run metadata and native classification.
- **H ordinary / G native-only diagnostics (7):** SG140, SG142, SG206, SG220,
  SG223, SG224 and SG227, all spin-half. H has an ordinary complete case record.
  G has a native output and the exact case-completion marker, but no
  `result.json`; its captured `run.json` is not complete. These G files remain
  diagnostic evidence and are not accepted case records.

The containing G/H campaigns were incomplete at capture. **This package does
not establish full-campaign acceptance**, including for the five comparisons
whose individual case records are complete. It adds no entries to the accepted
catalogue and makes no physical-classification claim. The earlier SG210
comparison is [archived separately](../overlap_g_h_210/README.md).

The verifier recomputes full and filtration Smith groups and checks every
presentation relation against filling, the filling gcd, primitive-cell volume,
root vector types and dimensions, and consistency of saved completion/chain
certificates. It also compares the complete saved scientific objects. It does
not rerun cochain completion or the neutral E8 stage; this is a comparison of
the CI block used within the full four-data workflow. Different hosts,
scheduling, memory budgets and G's older timing method preclude a controlled
speedup claim.

`raw.tar.gz` contains 173 byte-exact remote artifacts from the one bounded
capture recorded in `original_review/download.json`. Source manifests bind G
to `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824` (57 files) and H to
`ea44c1f55314ddd66587cf452bbaae9331f3a1db` (60 files); every listed hash is checked
against Git. Both runtime manifests record VM SHA256
`0c026ca103e9ba8b674c006d6042ca23bfe526ca62b4e96b3c1b79c4d318dec2`.
The copied inputs match the exact frozen catalogues and each other. All paired
records were stable during the read. No processes were signalled or restarted.

Run the portable offline verifier with Python, SymPy and this Git history:

```sh
python3 results/spacegroup_campaign_20261015/overlap_g_h_remaining/verify.py
```

A relocated package accepts `--repository /path/to/checkout`. Verification
reads archived bytes and Git objects only; it does not import current runtime
code, read live campaigns or perform acceptance. The independent integer
checker is the exact pinned SG210 verifier, retained in `original_review/`.

`comparison.json` uses the case-level labels above. The original review report,
scripts, logs and manifest remain byte-exact in `original_review/`, including
their earlier, imprecise `completed-parent-overlap` label. That historical label
does not mean a complete campaign. `provenance.json` records this wording-only
transformation, the original hashes and both compressed/uncompressed archive
hashes. The redundant base64 transport is omitted; all underlying files remain.
