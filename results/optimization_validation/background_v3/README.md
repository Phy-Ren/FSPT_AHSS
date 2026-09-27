# Background optimization validation

Both full campaigns completed all 230 groups successfully. The [complete comparison](comparisons/v1_vs_v3_complete.json) finds exact equality of every retained mathematical field and native witness after the listed metadata/export normalizations. Each full campaign contains 214 results with complete marked evidence and 16 uniquely determined abstract upper extensions; those 16 retain their explicit missing upper-phase-witness scope.

| Comparison | Completed comparisons | Result |
|---|---:|---|
| v1 baseline vs accepted v3 | 230 / 230 | Literal equality |
| v1 baseline vs cup-zero pilot | 13 / 13 | Literal equality |
| Original small controls vs cup-zero pilot | 12 common groups | Literal equality; original controls lack SG219 |
| v1 baseline vs integrated pilot | 6 / 7 planned | Six equal; SG219 hit its unchanged 3-hour budget |
| Accepted spin-half vs background-source regression | 7 / 7 | Existing fields/witnesses equal |
| Accepted spin-half vs diagnostic supplement | 2 / 2 | Existing fields/witnesses equal; new diagnostics identified |

The integrated pilot's SG219 is retained as raw `timeout`, exit `-9`, elapsed `10800.999019145966` seconds. Its original GNU metrics file is empty and stays empty. The independently completed formal v3 SG219 is separate evidence, never substituted for that pilot.

The [whole-campaign performance comparison](comparisons/performance_v1_vs_v3.json) gives:

| Measurement | v1 baseline | v3 accepted | Change |
|---|---:|---:|---:|
| Observer elapsed, seconds | 14030.195089 | 13654.803966 | −2.6756% |
| Total GAP CPU, seconds | 154544.508 | 148463.701 | −3.9347% |
| Total GNU process CPU, seconds | 154638.18 | 148558.07 | −3.9318% |
| Maximum final single-task RSS, GiB | 22.949142 | 21.574188 | −5.9913% |

These are measured complete-campaign values, with queue delays and overlapping development workloads. They are not an isolated hardware comparison. GAP CPU differences use exact integer-millisecond input sums; original reported floating totals are retained separately. The nonzero-background checkpoint follows the integrated background stacking routine and is not a standalone classification timing. Local cup-zero speedups are not extrapolated to the full run.

The 460-row table passes the odd-primary check for all 230 bosonic layers and full-group options. All nine designated oriented torsion-free examples have exact native background trivializations and equal graded/full groups across the two conventions. [Portable fixture tests](comparisons/portable_fixture_tests.json) pass all 15 controls with all eight fixture types available and zero skips while development `runs/` inputs are excluded.

This archive compares the same spinless crystalline problem before and after the cup-zero and integer-layer specializations. It retains full numerical trees and native witnesses, rather than only abstract group types. Production acceptance and timing belong to the [accepted v3 archive](../../space_groups_spinless/); this directory retains the independent baseline and smaller controls.

The comparison removes only individually documented runtime metadata. Earlier display labels and omitted redundant aliases are normalized explicitly. New native background certificates or diagnostic vectors that were absent in an early export are reported as added evidence; their absence is not called a literal match. Abstract upper extension certificates remain distinct from actual marked-generator witnesses.

The [input manifest](archive.json) records every original path, exact byte count and SHA256. Raw result JSON, classification checkpoints, campaign manifests and task records remain unchanged. Original absolute provenance paths are retained inside those files. Frozen GAP sources are deduplicated under `sources/<source_id>/gap/`, with their complete file sets and contents checked against every campaign. `stdout.txt` contains the original `stdout.log` bytes.

The full comparisons and their result hashes are listed in `validation.json`. Incremental audit history is retained by exact input hash; unchanged inputs were not repeatedly re-audited while waiting for new results. The portable commands below repeat the final independent audit and comparison from the archived inputs. Each output path must be new.

```bash
python3 scripts/compare_background_runs.py \
  --baseline results/optimization_validation/background_v3/runs/v1_baseline \
  --candidate results/space_groups_spinless \
  --expected-groups {1..230} --output /tmp/fspt_v1_vs_v3.json

python3 scripts/compare_background_runs.py \
  --baseline results/optimization_validation/background_v3/runs/v1_initial_controls \
  --candidate results/optimization_validation/background_v3/runs/v2_cup0_pilot \
  --allow-legacy-baseline --expected-groups 1 2 3 6 7 16 19 75 81 84 103 146 219 \
  --output /tmp/fspt_initial_vs_cup0.json

python3 scripts/compare_background_runs.py \
  --baseline results/optimization_validation/background_v3/runs/v1_baseline \
  --candidate results/optimization_validation/background_v3/runs/v2_cup0_pilot \
  --expected-groups 1 2 3 6 7 16 19 75 81 84 103 146 219 \
  --output /tmp/fspt_v1_vs_cup0.json

python3 scripts/compare_background_runs.py \
  --baseline results/optimization_validation/background_v3/runs/v1_baseline \
  --candidate results/optimization_validation/background_v3/runs/v3_integrated_pilot \
  --expected-groups 3 6 84 86 87 88 219 --output /tmp/fspt_v1_vs_v3_pilot.json

python3 scripts/compare_background_runs.py \
  --baseline results/space_groups \
  --candidate results/optimization_validation/background_v3/runs/half_regression_v3 \
  --crystalline-spin half --expected-groups 1 2 6 19 81 103 146 \
  --output /tmp/fspt_half_regression.json

python3 scripts/compare_background_runs.py \
  --baseline results/space_groups \
  --candidate results/optimization_validation/background_v3/runs/half_diagnostic_completion_v3 \
  --crystalline-spin half --expected-groups 84 104 --output /tmp/fspt_half_diagnostics.json

python3 scripts/report_physical_conventions.py \
  --half results/space_groups --spinless results/space_groups_spinless \
  --output /tmp/fspt_physical_conventions
```

The initial control campaign contains 12 groups and no SG219. Its comparison with the intended 13-group cup-zero pilot cannot compare SG219. If that pilot completes SG219, this result appears as candidate-only here and is checked against the complete baseline separately; if it times out, both auxiliary comparisons explicitly retain the missing SG219. Small control campaigns are not whole-campaign timing benchmarks.

The [460-row physical table](physical_conventions/physical_conventions_460.csv) contrasts two different physical symmetry problems. It is not an external validation: spin-half crystalline uses effective internal `s=w1(V), omega=0`, while spinless crystalline uses `s=w1(V), omega=w2(V)+w1(V)^2`. The table keeps four graded layers, full group or certified options, free-lattice index and actual marked status separate. Its odd-primary consistency check uses the unchanged sign action and 2-primary nature of the changed operations.

Auxiliary SG219 attempts retain their original budgets. If a development attempt times out, `archive.json` records its original terminal status, exit code and intended/completed group sets; raw task evidence is retained unchanged. Any late partial artifact is placed under `failed_attempts/`, outside the completed `sg*.json` inputs. A 6/7 integrated pilot is not relabeled 7/7. The formal v3 SG219 result has the same numerical source and supplies separate complete mathematical evidence, but is never copied into the pilot directory. An incomplete isolated cup-zero pilot remains incomplete: [direct native bilinear controls](../../../docs/validation_runs/background_native_cup.json) and the formal full-230 comparison are supplementary evidence, not a fabricated pilot result. The native bilinear control distinguishes full native-form equality from its cohomology-only bar comparison.

The two main campaigns are held to the stronger condition: both must contain all 230 successful complete results, and every existing mathematical field/native witness must pass the exact v1-versus-v3 comparison before final acceptance. Auxiliary timeout history does not relax this requirement. `all_expected_groups_compared_and_equal` may be false for an explicitly incomplete auxiliary comparison; consult the recorded missing group list and final validation summary.

To recompute the baseline performance from only portable inputs, run this from the repository root with a new output filename. Its final floating sum can differ in the last bit across Python versions; compare the original per-group integer milliseconds and GNU decimal values for exact CPU aggregates.

```bash
python3 - <<'PY'
import json, sys
from pathlib import Path
sys.path.insert(0, 'scripts')
from audit_background_run import check_background_result
from background_performance import collect_background_performance
run = Path('results/optimization_validation/background_v3/runs/v1_baseline')
audits = {n: check_background_result(json.loads((run / ('sg%d.json' % n)).read_bytes()))
          for n in range(1, 231)}
performance = collect_background_performance(run, run / 'tasks', audits)
output = Path('/tmp/fspt_v1_performance.json')
assert not output.exists()
output.write_text(json.dumps(performance, indent=2, sort_keys=True) + '\n')
PY
```
