# Optimized cluster GAP compatibility result

**PASS: 15 tests, no skips, errors or failures.** The suite ran serially on `n08.local` in 41.70 seconds on 2026-10-15 UTC. The maximum recorded child resident set was 278688 KiB. This validates the selected runtime paths on the optimized executable; it is not a production campaign or a new physical-classification claim.

The full source archive is commit `80d565de744bbd5ef6ac4cca3530511f549547f4`, archive SHA256 `cea5836a0bb9d447c7f99bea66fa3c46c16bef72276f69a7bb417cebcf3edd95`. All 1610 archived files were checked before and after the tests and remained unchanged. Its 45 runtime/reporting hashes exactly match the source-C campaign, with source-manifest SHA256 `63887ca47cf557f30a3a867bac16392b05c8d107a8cdb87ffbd4d47784ccdc88`.

The optimized GAP executable SHA256 is `873e902ee797706160601846c1ad6582c05e0aebd069bdd7efcff3d081f96fea`. The executed environment was GAP 4.13.1, Python 3.8.16, HAP 1.62, Cryst 4.1.27, CrystCat 1.1.10 and Polycyclic 2.16. Package paths point to the existing GAP installation. The independently prepared build evidence records identical before/after hashes for that original installation and its selected package files; no package was rebuilt for this validation.

Complete-root/incoming/IQH controls, signed bar transport, exact cache isolation and eviction, the free-sheet integer kernel, paired versus independent full-affine P1 witnesses and filling, and neutral E8/free-torsion/screw-period tests all passed. An additional independent SymPy inspection confirms the Smith invariants of all ten saved backend presentations and checks both saved wallpaper filling maps against every presentation relation and the positive primitive-cell area.

The P1 test compares the complete presentations, root generators, phase/gauge witnesses, sheet-kernel lattice and filling records between paired and independent runs. It does more than compare the final abstract group. The two wallpaper filling checks independently retain image steps 2 and 1 for the actual pg and p1 controls. These are the only primitive-filling homomorphisms saved in the common ten-record backend artifact; the P1 exact comparison is recorded by the passed frozen test. SG14/SG19 production-style optimized comparisons are separate work and are not claimed by this report.

The shared validation directory is `/home/user/xyren/AllFSPT_insulator/validations/gap_o2_80d565d_20261015`; the local copy is `/home/xingyu/AllFSPT_reviews/gap_o2_80d565d_20261015`.

- [Exact invocation, selected tests and scope](validation_plan.md).
- [Test result](validation_o2/result.json), [individual test log](validation_o2/tests.log), [binary/package/environment metadata](validation_o2/metadata.json).
- [Same-source comparison](same_source_verification.json), [complete archive verification](archive_verification.json).
- [Independent saved-presentation audit](saved_presentation_audit.json), [executable inspection](inspect_saved_presentations.py).
- [Optimized build evidence manifest](../gap_o2_build/review_manifest.json).

Two setup attempts stopped before any test: one used the node's unsupported default Python 3.5, and one encountered a relative-path error in the external metadata harness after its GAP version probe. Both are preserved with their scripts and logs in `setup_attempt_01/` and `setup_attempt_02/`. They did not change the archived source, formula implementation, package tree or production jobs.

## Repository packaging

This compact package preserves the source tree/archive identity, exact runtime comparison, commands, test results, setup attempts and independent presentation audit. The duplicate full source archive and extracted checkout remain in the external validation directory; commit `80d565de744bbd5ef6ac4cca3530511f549547f4` identifies the source. The optimized build evidence is shared at [../gap_o2_build](../gap_o2_build/README.md).

Run `python3 inspect_saved_presentations.py` here to reproduce the saved-matrix inspection. Re-running the cluster suite requires restoring the full commit into a fresh external validation directory as `source/`, with the pinned archive manifest and the recorded cluster runtime environment. The original runner refuses to overwrite an existing validation output. `package_manifest.json` records copied-file hashes and the sole documentation-link adaptation.
