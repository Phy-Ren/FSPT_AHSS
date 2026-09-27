# Independent result reports

The accepted crystalline spin-half campaign is `results/space_groups`. Its 230 original
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

## The two physical conventions

The runner selects the physical crystalline convention with
`--crystalline-spin half` (the default) or `--crystalline-spin spinless`.
Both calculations retain the full infinite affine space group. Their internal
backgrounds and report entry points differ:

| Physical crystalline convention | Effective internal background | Result directory | Report script |
|---|---|---|---|
| Spin-half (internal spinless) | `s=w1(V)`, `omega=0` | `results/space_groups` | `scripts/report_results.py` |
| Spinless (internal spin-half) | `s=w1(V)`, `omega=w2(V)+w1(V)^2` | `results/space_groups_spinless` | `scripts/report_background_results.py` |

Here `V` is the actual three-dimensional point representation. A spinless row
can use a zero cocycle after an explicit trivialization on the affine group;
this is a fermion-extension gauge choice, not a change of physical convention.
The original Pin-minus background and its trivialization certificate remain
in `crystalline_background`.

The complete spinless archive is now `results/space_groups_spinless`, with
source ID `73e7bae91a1c02156431ddc1c072c06d32517e287b5aa6314203f416cff1b252`
and archive SHA-256
`1c2148ca95fd5245ec5a490665f784229a629e2c8745b6838c17262ba7e3aa72`.
Validate it and generate a separate report in a **new** directory:

```sh
python3 scripts/audit_background_run.py results/space_groups_spinless
python3 scripts/report_background_results.py results/space_groups_spinless \
  --output runs/spinless_report_recheck --tex
```

The second command writes `audit.json`, `space_groups.csv`,
`candidate_pages.csv`, `README.md`, and, with `--tex`, `space_groups.tex`.
It requires all 230 rows and one source snapshot unless `--allow-partial` is
explicitly supplied. It refuses an existing output directory and rejects
invalid available rows even in partial mode. It does not reuse the old
reporter's parity-only free-lattice checks: a nonzero background can require
a different finite-index surviving lattice.

Read `all_230_full_groups_determined` separately from
`all_230_marked_witnesses_complete`, and inspect `actual_marked_witnesses`
and `audit_kind` in each CSV row. The final archive certifies all 230 abstract
groups: **214 rows retain marked evidence; 16 have an abstract-only upper
extension**. Thus the first completeness flag is true and the second is false.
All 44 groups with a nonzero free p+ip rank retain an actual primitive surviving
lattice basis and complete defining towers. Missing rows in a development
snapshot remain missing; these final counts apply to the archive identified
above.

## Background quotient and saved generator evidence

For unitary groups, the new calculation first constructs the complete lower
CA stacking group and then quotients by the actual `H^0` p+ip incoming state
`X=(omega,0,F)`. The supplied unary normalization fixes the zero CF component;
the independently constructed phase and its normalization are described in
`CRYSTALLINE_SPINLESS_BACKGROUND.md`. All incoming pages are represented by
this one cyclic subgroup. The final Majorana, CF and bosonic graded factors
are obtained from integral relation intersections after the quotient, not by
independently deleting layer generators.

The JSON retains `preH0IncomingGraded`, `h0PipIncoming`, and, inside `stacking`,
`lowerBeforeH0Incoming` and `h0IncomingQuotient`. The nested
`h0IncomingQuotient.backgroundQuotient` includes the actual incoming coordinate
row, its order, its native state, the marked-basis change and the filtered
integer-lattice certificates. The final `stacking.lower.presentation` has
the incoming relation appended. It can therefore be rectangular or
nontriangular; its marked generators may be redundant, and their original
`quotientOrder` labels are not the new graded orders. Use the final Smith
certificate and `finalFiltrationCertificate` to read the quotient.

Saved generators contain either native `lift` fields or a
`nativePhase4Seed`, with `nativeCF3Seed` for the native Gu--Wen construction.
These exact vectors, rational phases, the named construction and the frozen
comparison-map/homotopy source specify their reconstruction. For nonlinear
primitives, applying the native-to-bar map to the phase seed alone is
insufficient: the recorded construction includes the obstruction's comparison
homotopy correction. `fullBarCochainsPersisted=false` states that the infinite
bar functions themselves are not serialized. It does not mean the native
lift or its reconstruction recipe is absent. Conversely, an algebraic audit
of those saved records is not a new evaluation of the bar-cochain equations
and does not imply that every group underwent a separate full-support audit.

## Stacking the saved marked generators

The same replay entry point accepts either convention after the corresponding
strict certificate audit. For example, a spinless row with an actual upper
relation can be used as follows:

```sh
python3 scripts/stack_result.py results/space_groups_spinless/sg7.json \
  --left '{"P1":1}' --right '{"P1":1}'
```

Inputs are signed integer coefficients in that result's generator names.
The output contains both canonical Smith coordinates (`stacked`) and a
representative in the original marked names (`stacked_marked`). For an H0
quotient the reduction is labelled `smith-representative`: a row `x` is mapped
to `x V`, reduced in the exact Smith coordinates, then lifted back by the
unimodular inverse `V^-1`. It is not necessarily the ordered filtration normal
form used for triangular presentations. This API performs relation algebra;
it does not reevaluate a cochain product. Names from different runs need not
denote the same physical representatives.

When `pipExtensionCertificate` is present and `fullUpperPhaseWitness=false`,
the leading MC component of `2P` and all allowed CF/bosonic carries define an
entire extension family. A single `invariantOptions` entry means that **every
allowed carry has the same abstract Smith type**. A nonzero leading MC
component alone would not establish this. No particular upper carry, upper
phase or marked `2P` relation is thereby supplied, so `stack_result.py`
explicitly refuses these rows, even when their abstract stacking group is
fully determined. The given first p+ip product normalization is a mathematical
input to this family calculation; closure alone does not derive that input.

The 16 abstract-only rows are SG
`6, 8, 28, 30, 31, 32, 34, 40, 41, 43, 156, 157, 160, 174, 188, 190`.
The other seven surviving torsion p+ip cases,
`7, 9, 29, 33, 158, 159, 161`, retain the actual upper relation; their chosen
final marked squares are zero. This does not assert that their intermediate
CF or phase twisters vanish.

An independent [archived relation replay](validation_runs/presented_stacking_spinless.json)
passed all 1,850 saved relations in the 214 marked rows, plus four signed
coefficient examples per row, including 70-bit integers. All 16 abstract-only
rows were correctly refused. The 52 H0 quotients use `smith-representative`;
the remaining 162 marked rows use `ordered-filtration`. This is a check of
saved relation algebra, not a new bar-cochain audit. A separate
[scope review](validation_runs/spinless_final_scope_review.json) matches every
diagnostic candidate and group list to the original archived bytes.

The free p+ip generators are different: the explicitly determined surviving
lattice is free abelian, so its extension splits as an abstract abelian
group. Chosen complete lifts define a section by their integer stacking
powers. This removes an abstract free-extension ambiguity; it does not assert
that every possible cochain twister involving free decorations vanishes.

## Timing and reproducibility

The accepted spin-half v09 run completed classification in 783.017 observed seconds and
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
