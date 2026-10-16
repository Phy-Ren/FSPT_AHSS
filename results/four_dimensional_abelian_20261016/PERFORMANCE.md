# Complete-run performance and bounded attempts

The main campaign ran on initially idle `n07.local`, with three workers,
16g GAP limits, 1800 seconds per case, the optimized GAP4.13.1 executable,
and the pinned Python3.13.12/SymPy1.14.0 environment. Twelve cases completed;
`C4 × C8` timed out. The entire execution interval, including the timeout,
was 2096.349 seconds. Every per-case time is in [performance.json](performance.json).

Representative complete calculations took 13.585 seconds for `C2²`,
47.132 seconds for `C3²`, 122.534 seconds for `C2³`, 171.561 seconds for
`C4²`, and 1076.733 seconds for `C3 × C9`. These times include full native
completions, incoming gauges, all non-phase pair commutators and the final
presentation, not just cohomology or associated-graded groups.

## Primary-class comparison

The optional native charge-primary path was compared with the full bar
primary calculation on the same host, `n08.local`. All other mathematics,
matrices, roots and witnesses agree literally; only the two mode flags are
excluded. The [raw comparison](verification/native_comparison.json) records
all six result hashes and points to the full raw runs in `verification/`.
An [independent replay](verification/independent_native_comparison_replay.json)
checks those hashes, equality, and every saved certificate again.

| Full calculation | Bar primary | Native primary | Both primary implementations checked |
|---|---:|---:|---:|
| C2² | 12.833 s | 13.184 s | 13.285 s |
| C2³ | 118.357 s | 119.671 s | 121.026 s |

The shortcut shows no end-to-end speedup here, so `bar` remains the default.
The rank-three comparison includes a genuinely nonzero charge differential.
The first-stage class calculation alone does not measure the cost of
completing roots or computing their stacking relations.

The separate [half-phase completion prototype](verification/half_phase/REVIEW.md)
also preserved every complete output and witness. On idle n11, C2² took
12.431/12.383 seconds and C2³ took 117.269/118.272 seconds in baseline/candidate
modes. Its 2048 pointwise source checks passed. The sub-second improvement
in the C2³ charge-completion stage did not improve the complete calculation,
so this candidate is archived as an experiment and is not in the production
engine. The portable audit and immutable source/run archive accompany the
review. [Original stage-entry CPU timestamps](verification/main_stage_timings.json)
for the main campaign identify the later root/incoming work as a scaling
issue; they are not described as stage wall times.

## Retained incomplete attempts

- [C4 × C8](raw/abelian/internal_abelian_4x8_4p1/run.json): timeout at
  1800.017 seconds. Its last logged stage was incoming-charge gauges; it
  did not reach a completed presentation.
- [C2⁴ bar pilot](failed_rank4_pilot/internal_abelian_2x2x2x2_4p1/run.json):
  timeout at 900.018 seconds, during root relations.

The complete primary obstruction matrices of the bar pilot and the separate
native rank-four attempt agree, with kernel index16; see
[the explicitly stage-limited comparison](verification/rank4_primary_parity.json).
This is not a completed `C2⁴` classification. Any later accepted rerun must
have its own full record and certificate; the timeout evidence remains.

The bottleneck therefore includes actual phase completions and their repeated
use in root/gauge reductions. Reusing certified half-valued phase completion,
or explicit completed mixed roots, is a separate optimization task requiring
full-result comparison. No speculative speedup is used in these tables.
