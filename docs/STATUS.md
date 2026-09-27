# Completed campaign

Accepted on 2026-09-26: **all 230 space groups have complete classification,
actual generators and stacking relations**. The uniform `full_closed_cf_v09`
run is archived at `results/space_groups`. Its source ID is
`9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`;
all 30 live GAP files match the frozen source exactly. The original archive
manifest SHA-256 is
`60bc072c330c838a10e6a1f663eb6664e1d09e010b5081141dacf609aff33831`.

The local Git repository is `/home/xingyu/FSPT_AHSS`; the cluster working
directory is `/home/user/xyren/AllFSPT`. There is no published GitHub remote.
Each space group uses one sequential classification-to-stacking GAP process,
with parallelism across groups. SptSet is never loaded. Runtime formulas are
compiled independently from the delivered mathematical inputs; no external
answer table or collaborator calculation engine is a production dependency.

## Results and performance

| Measure | Accepted run |
|---|---:|
| All 230 classification checkpoints | 783.017 seconds |
| First 229 complete stacking results | 3657.307 seconds |
| All 230 complete results | 12699.328 seconds (3 h 31 min 39 s) |
| Summed GAP CPU time | 62963.022 seconds |
| GNU time process-tree CPU | 63036.050 seconds |
| Largest single-task RSS | 17688448 KiB (16.869 GiB), SG219 |

Five shared PBS workers each allowed at most 28 single-threaded tasks. The
observed elapsed times include queueing, competing candidate/control tasks,
and a 10-second observer interval. They are not exclusive-140-core benchmarks.
The SG219 tail dominates completion: 12689.769 GAP CPU seconds, including
4288.262 seconds in the B1 lift and 4041.885 seconds in the p+ip phase lift.
The saved group is `Z2 + Z2 + Z4`, with `2P1=C1` and `2C1=2C2=2B1=0`.

The result table is `results/space_groups/report/space_groups.pdf` (six pages),
with CSV, Markdown and JSON reports beside it. The seven-page formula note is
`notes/independent_space_group_formulas.pdf`. Both PDFs passed layout checks.
See `PROJECT_REPORT_ZH.md` for the Chinese report and `CLUSTER_RUN.md` for a
fresh five-node rerun with persistent SSH reuse.

## Correctness and independent comparisons

All 230 accepted results pass the complete-stored-witness, exact Smith,
formula-convention and source audits. All 44 groups with nonzero free p+ip
rank contain an actual surviving lattice basis and complete generator towers.
Their indices are 1 for 29 groups, 2 for 14 groups, and 8 for SG2. All 32
surviving torsion p+ip cases include the upper phase relation.

Every saved mathematical field agrees literally with the complete generic
v07 baseline for all 230 groups. Only explicitly listed execution/provenance
fields are excluded. The baseline preserves 229 original outputs plus a
same-source SG219 retry; it is a mathematical comparison set, not an
uninterrupted campaign benchmark. The data and comparison are under
`results/optimization_validation`.

The other complete configuration, v08, reached all results in 14751.680
observed seconds, used 70171.795 GAP CPU seconds and peaked at 20.063 GiB.
Its mathematical fields also agree with v09 for all 230 groups. Thus v09 was
2052.352 seconds faster in this deployment. Both complete uniform runs and
their original task evidence are archived; see `selection.json` in that
directory. No per-group source selection was used.

All 920 graded-layer entries agree with both the independent pre-reference
freeze and the current supplied boss PDF. That PDF does not provide complete
stacking extensions. Of 204 nonempty historical stacking answers, 179 agree,
21 already differ in graded layers, and four have equal layers but different
extensions (SG68, SG81, SG82, SG101). Those four pass targeted relation and
cochain controls; no specific old implementation line has been established
as their cause. Another 26 historical full-group entries are empty. The
provided Weicheng checkout has no affine-230 stacking table; its four relevant
finite C2 labels correspond to two distinct models and all agree.

The final comparisons also reproduce the nine geometric examples, all 687
supplied initial F2 dimensions and all 230 signed-H1 entries. Original
pre-reference hashes and historical reports are unchanged. See
`results/boss_layers/current_reference_comparison.md`,
`results/external_comparison/comparison.json`, and
`HISTORICAL_STACKING_REVIEW.md`.

The AW transport compiler correction is checked against the unchanged supplied
scalar oracle on 84 legal signed-integer towers and all 1024 C4 tuples.
Corrected full-support controls on SG7, SG81, SG82 and finite C4 pass.
The accepted closed-CF/half-phase optimization has additional exhaustive
local, translated-primitive and complete SG87 marked-lift controls. Native
mod-two classification contraction is enabled; mod-two **bar comparison** is
disabled so later lifts retain integral-cache reuse.

All 98 Python tests passed after the scheduling/archive changes; the later
budget-default edit also passed its three submission tests. These checks and
stored-output audits do not replace cochain controls or extend them to every
support tuple in every space group. Exact assumptions and coverage remain in
`VALIDATION.md` and the individual validation records.

## Provenance and scheduling

The accepted archive contains 1198 original/generated-manifest files and
15929682 bytes before the later human-readable reports. All 1197 payload
hashes were verified after transfer. Strict performance collection was also
repeated using only archived task/guard evidence; its record is
`results/space_groups/audits/portable_performance.json`.

Three healthy SG219 tasks received explicit predeadline scheduling extensions
within their original PBS allocations. Complete guard/watchdog ledgers and
original worker states are preserved; no failed status was rewritten. The
accepted v09 task actually finished before its original four-hour limit and
was reaped as `done`, exit zero. The generic retry finished earlier but was
reaped later as `timeout`, exit zero; its real exit interval and GNU time are
separate evidence. See `SCHEDULING_EXTENSIONS.md`.

Earlier v04/v06 and the original v07 campaign retain their 229-result plus
SG219-timeout histories and stopped observers. They are not full-230 timing
benchmarks. Resource measurements are in `results/performance_environment`;
PBS host memory totals are distinct from task RSS. All five allocations have
been released, and their queues have no active, pending or running tasks.
The exact-ID scheduler checks are in `results/performance_environment/final_release.json`.
Workers drained through their own STOP files, leaving historical queues intact.

The model is three spatial dimensions, physical spin-half superconducting
fermions, no extra onsite symmetry, determinant sign action and effective
omega zero. The complete infinite affine space group is used, including
translations, weak phases and atomic fermion parity. The supplied calibrated
product and the finite-group normalization assumptions remain mathematical
inputs; these computations do not claim a new general coherence theorem.
