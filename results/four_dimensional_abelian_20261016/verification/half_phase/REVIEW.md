# Isolated degree-four closed-charge completion prototype

The prototype preserves every saved classification and witness field for both tested groups, but it does not improve complete-run wall time. Do not adopt this shortcut alone on the strength of these measurements. All changes are confined to this review snapshot; repository sources and running scientific campaigns were left intact.

The experiment ran on idle n11 with two independent single-worker campaigns, each capped at 300 seconds per case and 8 GB GAP memory. The baseline and candidate used the same immutable source, runtime and bar primary-classification mode. Only three candidate snapshot files changed: `gap/charge_source.g`, `gap/abelian4p1.g`, and `scripts/classify_abelian_4p1.py`.

| Configured group | Baseline full wall time | Candidate full wall time | Candidate/baseline | Baseline charge-completion GAP CPU | Candidate charge-completion GAP CPU |
|---|---:|---:|---:|---:|---:|
| C2 × C2 | 12.431406 s | 12.382645 s | 0.9961 | 182 ms | 209 ms |
| C2 × C2 × C2 | 117.269257 s | 118.271504 s | 1.0085 | 4509 ms | 3631 ms |

Charge-completion CPU is the difference between the existing `charge_lifts` and `root_relations` entry timestamps. It includes the complete charge-lift loop, not just source evaluation. The 19.5% reduction in that stage for C2³ is less than one second; subsequent root, incoming and commutator work dominates this test. A single paired run does not resolve sub-percent wall-time differences. Formula-worker calls remain exactly 842 and 2314, respectively.

## Mathematical domain and retained witnesses

The extension is guarded by degree four, a closed integral native charge vector, exact `s=rho=omega=0`, and finite-group `vcd=0`. The state retains the full integral charge `q`, rather than replacing the charge state with its parity. For this domain the phase source is the half-valued `Sq²(q mod 2)/2`. The existing source certificate checks the context, actions, dimension, exact charge object and closure certificate before selecting the existing half-phase transfer.

Only the native evaluation of this certified half-valued source discards even bar-chain coefficients. The canonical rational native primitive and full integral comparison-homotopy correction remain unchanged. In particular, this does not replace the primitive by a parity lift and does not discard quarter-valued completions. Root products, lower gauges, incoming relations, commutators and their reductions run through the original complete code paths.

A source comparison control checked 2048 deterministic pointwise evaluations against the original formula over 32 integral charge vectors, including negative multiples, even multiples and mixed vectors. It also verified preservation of the full integral charge. These controls supplement the algebraic closed-source identity; they are not an exhaustive enumeration of all cochains.

The full-run audit compares every classification/native field after removing only the candidate's extra execution selector `closedChargeCompletionMode`. Presentations, differential matrices, charge kernels, filtration, all root/incoming/commutator witnesses, completion checks, generators, runtime versions and formula-worker counts are identical. Both newly measured baseline classifications also exactly match the previously completed immutable bar campaign. This is equality of the complete saved output, not merely equality of Smith factors.

## Reproduction and provenance

Run `python3 verify_experiment.py` in this directory with Python 3.12 or newer. The portable audit unpacks the pinned source/run archive into a temporary directory and reads the earlier bar controls from the adjacent `native_benchmark/bar` evidence. `parity_and_timings.json` records all raw file hashes and the comparison results. It verifies 73 source-file hashes in each snapshot, the canonical source-manifest hash, input/run/result binding, all successful statuses, and the expected two-case selection.

- Baseline source SHA256: `a5df31562ea0e8e1f19dba8cf304256d5ca658c0ec8bbba6ff6e0ccef7550fc4`.
- Candidate source SHA256: `3414eeaeb8162f29266dadd9582c54cc7f02e7cc66ef430b60300dc6a484a53c`.
- Transferred snapshot-and-runs archive SHA256: `d3429db6ccc77586c88a1c610cb7cc1cf24b1b40334d06f6db6729562105af80`.
- Remote immutable experiment: `/home/user/xyren/AllFSPT_insulator/runs/abelian_half_phase_review_20261016`.
- Source donor: `/home/user/xyren/AllFSPT_insulator/runs/abelian4p1_batch2_20261016/native_rank4/source`.
- Python: `/home/user/xyren/AllFSPT_insulator/runtime4p1-v015/bin/python3`.
- GAP: `/home/user/xyren/software/gap-4.13.1-o2-20261015/gap-o2`.

The bounded experiment is complete. No larger case or additional benchmark was launched. The next optimization should target repeated complete source/comparison transfers, fresh wrapper caches in `U1FourCILower`/`U1FourCheck`, and repeated Smith decomposition during commutator relation solving. Each requires preservation of the complete cochain/gauge witness outputs and an end-to-end timing comparison; primary-class evaluation alone does not address the slow root/incoming stages observed in larger cases.
