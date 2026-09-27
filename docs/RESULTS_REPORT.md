# Independent result reports

The accepted complete campaign is `results/space_groups`. Its 230 original
results, classification checkpoints, immutable source, task logs and timing
evidence are byte-preserved by `archive.json`. Generate its report with:

```sh
python3 scripts/report_results.py results/space_groups --require-full-stacking \
  --require-complete-witnesses \
  --require-formula-convention normalized-pip-aw-edge-transport-v2
```

For a release with explicit generators, add `--require-complete-witnesses`.
This also requires the actual torsion p+ip phase relation and every primitive
free-lattice defining tower. `--require-formula-convention NAME` additionally
rejects results from a different or unversioned formula convention; it implies
the complete-witness checks. These stricter checks are also available in
`scripts/audit_run.py`.

For this input the default output directory is `results/space_groups/report`. The command requires all
230 classification results; `--require-full-stacking` also requires all final
stacking groups. Use `--allow-partial` only for a development report. Missing
groups then appear as missing rows, and the report is prominently marked partial.
An invalid source digest, certificate, factor list, or timing is rejected even in
partial mode. Input validation finishes before any output is replaced.

The three outputs are:

* `independent_results.csv`: all 230 group numbers, exact cyclic-factor lists,
  readable groups, witnesses, source hashes, and timing fields.
* `independent_results.md`: the four surviving graded layers alongside the final
  stacking group, upper-relation witness scope, timings, and source cohorts.
* `independent_report.json`: completeness, histograms, input-file hashes, the
  digest of the input set, assembly-manifest digest, and complete source-file
  hashes for every cohort.

The script does not select among conflicting runs and does not read an external
answer table. It records assembly origins as provenance strings without opening
those paths. Each input passes the existing `audit_run.check_result` checks,
including exact Smith identities where supplied. This checks the persisted
certificates; it does not rerun the cochain computations.

## Interpretation

`pip`, `majorana`, `complex_fermion`, and `bosonic` are associated-graded layers.
Their direct sum need not equal the final stacking group. The latter comes from
the generator relations and Smith reduction in the selected result.

In a JSON cyclic-factor list, `0` means an infinite cyclic factor and `[]` means
the trivial group. Thus `[0,2,2]` means `Z + Z2 + Z2`. In the human-readable group
columns, `0` means the trivial group. Blank fields denote unavailable data rather
than a trivial group.

`torsion_upper_witness=actual-phase-witness` means the result includes the actual
p+ip torsion generator relation obtained with the upper phase. An
`abstract-certificate` records an abstract extension without claiming that
explicit phase witness. `not-needed` means there is no torsion p+ip relation to
compute. Persisted witness fields separately distinguish finite native relation
certificates from complete bar-cochain functions.

For a free p+ip part, let `L` be the free part of the original signed integral
cohomology `H^1(G,Z_s)`. Its surviving subgroup `L_surv` has finite index in `L`
because the relevant obstruction targets are finite. Consequently
`rank(L_surv)=rank(L)`. The extension by a free abelian quotient splits as an
abstract abelian group, so the final abstract group type contains `Z^rank(L)`.
This statement alone does not identify the embedding `L_surv -> L`, its index,
or a basis of primitive surviving geometric decorations. Results without the
optional `pip.free_lattice` export retain that limitation and a dagger in the
table. In particular, a formal generator named `Pfree1` in a legacy result is
not a claim that the first raw cohomology basis vector survives. The abstract
classification group can be complete while those marked geometric generators
remain unspecified.

When a computed `pip.free_lattice` is present, the report checks its square
integer basis, determinant/index, surviving parity dimension and span, and
each generator's original H1 coordinates against the corresponding lattice
row. It also checks the shapes of native cochains and exact rational phases.
The free-lattice column then displays its index and whether complete phase
witnesses were constructed. CSV fields retain the basis, H1 coordinates and
certificate; the linked result retains the actual native cochains. These
structural checks do not rerun the defining equations. The construction and
independent equation tests are described in `FREE_PIP_LATTICE.md`.

## Timing and reproducibility

The accepted run completed classification in 783.017 observed seconds and
complete stacking in 12699.328 seconds. Its total GAP CPU counter is 62963.022
seconds; GNU time reports 63036.050 process-tree CPU seconds. The largest
single-task RSS is 17688448 KiB (16.869 GiB), on SG219. The full measurements
are in `results/space_groups/performance.json`, with a plot in `performance.pdf`.
The observer elapsed times include queueing on five shared workers, each capped
at 28 tasks; CPU counters exclude queue waits.

`audits/portable_performance.json` was recomputed strictly from the archived
task and supervision files, using `--tasks-root results/space_groups/tasks`.
The original archived `performance.json` was not overwritten. No original
remote runtime files are needed for this recheck. Its floating-point summed
timings can differ in the last decimal place because task iteration order
differs; the original per-task measurements are unchanged.

`classification_cpu_ms` is the GAP `Runtime()` classification CPU counter, and
`total_cpu_ms` includes stacking when the runner supplied that field. Their
difference is reported separately. The separate GNU time user+system counters
cover the complete task process tree and are collected in `performance.json`;
they must not be confused with GAP's counter. Classification-only fallback is marked with
an asterisk in Markdown. `wall_seconds` is the recorded invocation wall time;
neither the sum of CPU counters nor the sum of wall times is parallel campaign
elapsed time. Different source cohorts are retained and are not presented as one
uniform performance benchmark.

The report script was checked on a 225-result development snapshot and with
temporary fixtures verifying rejection of incomplete strict runs, visible
partial reporting, and rejection of a modified source digest before replacing
existing report files. These are report integrity checks, not additional
mathematical validation. Formula and cochain validation is documented in
`VALIDATION.md`.

The optional free-lattice path also passes on the six actual
`runs/free_integration_v05` controls. `tests/test_report_results.py` checks
legacy scope, marked lattice formatting, and rejection of inconsistent index,
H1 coordinates, parity span, and rational phase encodings.
