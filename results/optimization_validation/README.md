# Exact output and performance comparisons

The accepted runtime is **v09**, archived at `../space_groups`. All 230 saved
mathematical outputs agree with both the generic v07 baseline and the complete
v08 configuration. The live GAP files match the accepted frozen source exactly.

| Complete uniform campaign | Classification elapsed | Full elapsed | GAP CPU | Largest task RSS |
|---|---:|---:|---:|---:|
| v09: integral bar cache, closed-CF/half-phase enabled | 783.017 s | 12699.328 s | 62963.022 s | 16.869 GiB |
| v08: mod-two bar map, closed-CF/half-phase enabled | 803.019 s | 14751.680 s | 70171.795 s | 20.063 GiB |

v09 was 2052.352 seconds (34 min 12 s) faster in observed full completion.
Both campaigns shared five PBS workers, each capped at 28 tasks, with other
candidate and control tasks. These are observed deployment timings, including
queue delays; they do not establish an exclusive-resource algorithmic speed
ratio. Neither campaign combines different configurations by group.

- `selection.json` records the decision, exact measurements and archive hashes.
- `v07_vs_v09.json` and `v08_vs_v09.json` compare all 230 outputs. Only the
  explicitly listed execution/provenance fields are excluded. Actual marked
  generator fields, phases, gauges, relation matrices, free lattices and Smith
  transforms are compared literally. This does not rerun every bar equation.
- `generic_v07_math_complete/` preserves the original result bytes, assembly
  manifest and audit from the generic baseline, plus its actual frozen source.
  It consists of 229 original v07 results and a separate same-source SG219 retry.
  It is **not** an uninterrupted campaign benchmark. The original failed
  attempt remains in the historical `runs/` records.
- `full_optimized_v08/` byte-preserves the entire second complete campaign,
  source, checkpoints, task logs, supervision ledger and timing evidence.
  Its SG219 raw worker state is `timeout`, exit zero; the independently audited
  extension was authorized before the original deadline. The original state
  was not rewritten. Completed guard/watchdog records and GNU time exit zero
  establish successful completion within the extended budget. Its portable
  strict recheck is in `audits/portable_performance.json`.

Comparison reports retain their original provenance paths. The archived result
bytes have the same hashes; no access to those original paths is required to
repeat mathematical comparisons. From the repository root:

```sh
python3 scripts/compare_witnesses.py \
  results/optimization_validation/generic_v07_math_complete results/space_groups \
  --output runs/recheck_v07_vs_v09.json
python3 scripts/compare_witnesses.py \
  results/optimization_validation/full_optimized_v08 results/space_groups \
  --output runs/recheck_v08_vs_v09.json
python3 scripts/collect_performance.py results/optimization_validation/full_optimized_v08 \
  --tasks-root results/optimization_validation/full_optimized_v08/tasks \
  --output runs/recheck_v08_performance.json
```

The same archive performance procedure applies to `results/space_groups` with
its own `tasks` directory. Original manifests and reports need not be replaced.
All five PBS allocations have been released; the exact-ID scheduler and queue
checks are in `../performance_environment/final_release.json`.
