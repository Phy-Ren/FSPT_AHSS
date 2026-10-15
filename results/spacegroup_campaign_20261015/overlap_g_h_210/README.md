# SG210 spinless: completed G/H overlap

The frozen G paired calculation and H standalone calculation have identical
input bytes and **34 literally equal scientific classification fields**.
Completed roots, native phases, obstruction/kernel matrices, root and gauge
witnesses, integer relations, filtration presentations and filling all agree.
No coordinate change or cochain normalization was needed. The full native
objects differ in exactly four execution fields: cache statistics, worker-call
count, paired geometry reuse and resolution timings.

Independent Smith calculations give the CI-tower stacking group `Z x Z4`,
with sheet `0`, charge `Z x Z2` and phase `Z2` layers. The primitive filling
image is `2Z`; every relation preserves filling. Both records retain nine
native completion checks and the same chain certificate. This check does not
repeat cochain completion, the E8 extension, or physical-spectrum identification.

`raw.tar.gz` preserves 20 exact remote artifacts from
`sgfull-20261015-g-n03/spacegroup_210_spinless` and
`sgfull-20261015-h-remaining-n02/spacegroup_210_spinless`, including their
source/runtime/selection manifests. All 57 G and 60 H source hashes match
commits `c07c6e5d4a69d79c9c2aeb0739ae1e189029f824` and
`ea44c1f55314ddd66587cf452bbaae9331f3a1db`. Both use the same optional VM hash.
The records were stable across the read; original campaign files were unchanged.

The recorded times are G 2361.523 s and H 844.399 s. Different nodes,
paired/standalone scheduling, memory limits and G's older NFS-derived timing
prevent a **controlled speedup claim**. Worker calls decreased from 229681 to
44120; this is an execution counter, not a scientific result.

Run the portable offline verifier, requiring Python, SymPy and this Git history:

```sh
python3 results/spacegroup_campaign_20261015/overlap_g_h_210/verify.py
```

It checks every package/member hash, input/source identity, all field
comparisons, saved certificate consistency, and independent Smith/filling
calculations. It reads archived bytes and Git objects only. A relocated
package accepts `--repository /path/to/checkout`; it does not depend on the
original review directory or current runtime implementations.

`comparison.json`, `download.json`, and `original_scripts/` retain the original
review bytes and recorded validator hashes. The original validator checkout
was evolving; the new portable verifier independently repeats the integer
checks without relying on that checkout. `provenance.json` links the external
original manifest and records compressed/uncompressed archive hashes. The
redundant base64 transport was omitted; all underlying raw files are retained.
