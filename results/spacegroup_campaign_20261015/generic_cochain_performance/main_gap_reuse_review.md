# Current main versus the insulator GAP path

Reviewed 2026-10-15 UTC. This is a call-path and exact-arithmetic review, not a comparison of the two physical classifications.

The main reference is commit `0864495b90297d3e1a0747b77aae17980f6d1f3f` in `/home/xingyu/FSPT_AHSS_public`. The live cluster source `/home/user/xyren/AllFSPT` was checked read-only through the persistent cluster3 SSH connection. Nine of ten examined generic/entry files are byte-identical. The tenth, `finite_full.g`, adds two explicitly nonproduction 4D diagnostic coordinate names; its 3D primary/class-transfer path agrees. Exact hashes are in `main_gap_source_identity.json`; the differing cluster file is retained outside the repository in the original review directory as `cluster_main_finite_full.g`; no superconducting theory file is copied into this package.

## The production path that matters

The main full-space-group entry is `gap/run_full_space_group.g:4–20`. It loads the native mod-two contraction, higher diagonals and closed-phase coordinate module, then calls `AFSFullClassify` and `AFSFullStackingClassification`. The Python CLI defaults both primary evaluation modes to native. Looking only at the older `AFSClassify` path misses these optimizations.

| Stage | Current main | Insulator before this review | Reusable part |
| --- | --- | --- | --- |
| Primary charge obstruction class | `finite_full.g:507–520,749–764`: native higher cup/Sq2 followed by signed phase class projection | Evaluates every degree-five bar-image native cell, then projects | Native diagonal/contraction and coefficient maps; derive the U1 charge combination separately |
| Closed phase class only | `finite_full.g:30–38` calls `AFSU1BarCoordinates` | Full `U1Native`, then `H.coordinates` | Smith dual-cycle projection, including odd orders and signed action |
| Completed phase primitive | Full matched bar source and comparison homotopy | Full matched bar source and comparison homotopy | Preserve this path and its representative |
| Certified closed lower input | `finite_full.g:829–842`, `full_stacking.g:143–172`: certificate tied to the actual cochain | Generic coboundary callback even for a known native cocycle | Generic certificate pattern; not the SC source expression |

The SG221 spin-half 120-second baseline profile stopped inside the initial charge-source map, before any Python worker call. Resolution construction and the initial cohomology/Smith work were short. Its stack was `sourceMap -> U1Native -> U1ChargeSource -> U1Cup/U1Coboundary -> U1Bar -> U1ChainFromBar`. This directly motivates the first two transfers in the table; Python compilation alone cannot remove that GAP work.

Some files that look promising are not loaded by the current full-space-group entry: `backend_hash_cache.g`, `backend_cup_cycle.g`, `backend_cup_slant.g`, `backend_smith_transfer.g`, and `backend_half_phase.g`. `AFS_USE_MOD2_BAR` is explicitly false. The main F2 parity filter is optional, not a default explanation of the speed difference. Main also does not enable the optional Koszul resolution by default; the insulator already enables it for its space-group runner. These should not be confused with missing active fast paths.

## Exact closed-phase transfer implemented here

The new insulator `gap/class_coordinates.g` adapts only main's generic Smith-period routine. Write the signed integral differential as `D`, with `U D V = S`. For a nonunit diagonal entry `d_j`, set `z_j = sign(d_j) column_j(U^{-1})`. Then `D_previous z_j = 0`, checked exactly, and the required class coordinate is

`|d_j| <f, F(z_j)> mod |d_j|`.

The implementation combines the group-ring boundary of `z_j` before applying the bar contraction; it does not separately expand all top native basis cells. This formula follows from `D V_j = d_j U^{-1}_j`, so its coordinates agree exactly with the original Smith convention, not merely up to an automorphism of the finite group. Leading group elements act through the actual `U1s` coefficient action. The cache is private to a context and checks the resolution, signed action and canonical cohomology object.

The first production call site is only the initial charge obstruction map. Its adapter constructs the bar charge from the given native integer vector after verifying its signed integral coboundary is zero. A validated background has integral `delta_(rho+s) omega`; therefore `omega cup q + Sq2(q mod 2)/2` is closed modulo one. The background certificate is bound to the exact `s`, `rho`, and `omega` functions. Uncertified contexts fall back to the previous native cocycle check. The generic fallback tests native closure; it does not claim to inspect every bar tuple of an infinite group. A missing or mismatched certificate is rejected by the period-only API.

`phaseClassMode="native"` selects the original full-native reference route; `"compare"` checks its coordinates against the cycle route. The separate native F2-primary adapter is under independent review and retains an explicit half-integral-background guard. No full primitive, completed root, integer gauge, incoming relation, or saved phase representative is replaced by a class-only value.

## Bounded validation and limits

The initial implementation passed all 14 existing backend tests and three new period/domain/comparison tests. The latter cover torsion orders 2, 3, 4, 6, 8, 9, independent sign characters, rational exact perturbations, both D2 backgrounds, a glide group and the rank-three translation group. A nonclosed native phase, a nonclosed integral charge, and mismatched certificates are rejected. Sibling spin contexts keep distinct background certificates and do not inherit the cycle cache.

The isolated SG195 pair completed with all 33 nonperformance mathematical fields per case literally equal to the actual full-D cluster results, including presentations, completed roots, gauge witnesses and primitive filling. See `closed_phase_candidate/sg195_comparison.json`. Its local 42.787-second pair time is not a same-node speed ratio against those cluster references; it also includes the previously validated Python simplex optimization.

The isolated SG221 cycle-only control remained unfinished at 120 seconds. Two class evaluations completed, with 18.842 CPU seconds combined in the profiler; another remained in bar source evaluation. The incomplete profiler does not measure the full time of pending calls. This demonstrates that cycle projection alone does not eliminate the expensive bar evaluation of the charge source. The next justified generic reuse is the native primary operation, with the U1 formula and integral input lattice kept intact.

All review and bounded-run evidence is outside the earlier committed immutable performance archive. No active campaign source or main-branch file was modified.
