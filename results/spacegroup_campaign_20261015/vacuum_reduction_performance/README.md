# Complete vacuum-gauge zero callbacks

The isolated two-line frozen-G experiment proves and measures replacement of already-zero lower callbacks after their full integral gauges. See [the full-cochain proof and domain](proof.md). The experiment changed neither phases nor gauge parameters. The later production integration adds an explicit internal precondition, `c.vacuumReductionMode` and CLI `--vacuum-reduction canonical|reference`, with a portable signed pointwise regression.

The complete local SG221 spin-half run took 127.065 seconds versus 234.922 seconds for frozen G. All 38 classification fields are compared: all 35 mathematical fields are literally identical. Only worker/cache counts and resolution timings differ. The same native VM is used, and the 57-file runner manifests differ only in `gap/classification.g`. Independent Smith reduction, primitive filling and exact input/source/native records are revalidated by `verify.py`.

Four signed cases in each of 2+1D and 3+1D check the raw discarded callbacks before replacement, integral charge closure, complete reference/candidate phase values, and identical native gauge/final-phase witnesses. The initial out-of-domain test and its rejection are preserved and explained in the proof. `tests.log` is the unchanged frozen-G 14-test backend control; `candidate_tests.log` is the same suite on the isolated candidate. `integrated_tests.log` records the three portable signed-mode tests; `runner_tests.log` records five timing regressions. The two CLI archives retain actual paired D2 canonical/all-reference results and mode metadata.

```bash
python3 results/spacegroup_campaign_20261015/vacuum_reduction_performance/verify.py
python3 -m unittest discover -s tests -p 'test_reduction_zero_callbacks.py' -v
```

These timings describe one matched local experiment. They are not a whole-catalogue throughput estimate. The underlying CI/E8 physical scope is unchanged; no group is accepted merely because its invariant factors match.
