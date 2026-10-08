# Reproduce and maintain the public results

This repository contains the formula definitions, an independent exact runtime,
the group engine, symmetry inputs and completed example results. No private
archive is needed to evaluate the public formulas or run a listed input.

## Find an example

Start at the [computed-example catalogue](results/computed_examples/README.md).
Its [unique example index](results/computed_examples/unique_examples.json)
contains 1,190 reader entries and verified links to all 1,234 retained
calculation records. Equivalent backgrounds appear once in the tables;
explicit group maps and cocycle section changes justify every merge.
The original [calculation index](results/computed_examples/index.json)
retains all names, exact inputs, results, final groups and layer filtrations.

For finite internal symmetry, the input gives the bosonic quotient $G_b$, its
one-based multiplication table with identity first, a binary character $s_1$,
and a normalized binary extension cocycle $\omega_2$. Generator indices use
that same enumeration. Crystalline inputs instead specify the space-group
number or crystallographic point-group index and physical crystalline spin
convention. Their constructors and background routines are included.

Invariant-factor arrays use `[]` for the trivial group, `0` for an infinite
cyclic factor, and `n>1` for $\mathbb Z/n$. The final decoration filtration
includes incoming gauge identifications. The intermediate
`rawSurvivingLayers` field must not be substituted for it.

## Reproduce a complete calculation

Install the GAP packages and Python requirements listed in [README.md](README.md).
Set `AFS_GAP` or pass `--gap`. A numerical job should run on an allocated compute
node, with a new output path:

```sh
python3 scripts/run_complete_example.py \
  --index results/computed_examples/index.json --list
python3 scripts/run_complete_example.py \
  --index results/computed_examples/index.json \
  --case d4_D8xC2_orbit_084 --output runs/d8xc2_084.json --dry-run
```

The second command prints the exact calculation command. Remove `--dry-run` to
run it. The wrapper reads only the symmetry input and retained performance
options before solving; the expected group is compared afterward. Classification
and stacking share the same representatives in one serial calculation.

`--audit` additionally checks generator inverses and the configured selection of
commutators and triples. This can dominate the run time. The result's
`coherenceAudit.allGeneratorTriples` field states whether every generator triple
was tested. A completed configured audit must not be described as exhaustive
unless that field and its supporting evidence say so.

The runner retains the recorded resolution strategy. An optional override is:

```sh
python3 scripts/run_complete_example.py \
  --index results/computed_examples/index.json \
  --case d4_Q8_w0_s0 --resolution input-generators \
  --output runs/q8_marked.json --dry-run
```

Available finite strategies include tensor products of cyclic resolutions,
standard dihedral resolutions, the input's explicit generating set, and the
direct products `D8xC2` and `Q8xC2`. Here D8 and Q8 have order eight. All
boundaries and contractions are transported back to the exact input group;
$s_1$, $\omega_2$ and the formulas stay attached to that group. The
[resolution certificates](results/resolution_certificates/README.md) include
standalone replay data. Their timings concern resolution construction and
verification, rather than a full classification/stacking calculation.

## Verify saved data

The catalogue explicitly distinguishes two published artifact kinds:

| Artifact | What it contains | Saved-data verification |
| --- | --- | --- |
| Full numerical record | Scientific output, integer presentation and retained witnesses | Hash/input checks; independent presentation and filtration arithmetic |
| Accepted scientific summary | Exact input, final group and filtration, source and acceptance provenance, retained reproduction settings | Hash/input/acceptance-summary consistency checks |

Both identify completed calculations. A compact summary is not an independently
replayable Smith/Hermite certificate. Its background can still be recomputed
using the same public runner.

```sh
python3 scripts/verify_complete_results.py \
  --index results/computed_examples/index.json
python3 scripts/verify_complete_results.py \
  --index results/complete_formulas/index.json --arithmetic
```

The first command checks the consolidated metadata and saved bytes. The second
recomputes integer presentation and filtration arithmetic for the original full
archive; use an allocated compute node. `--arithmetic` rejects a selection that
contains accepted summaries. Select full records with `--case`, or compute a
fresh full result for a summary's input.

A nonzero obstruction cochain can be exact. Even a nonzero original cohomology
class can be removed by permitted lower-layer adjustments. Only a nontrivial
final obstruction class excludes the candidate. Cochain consistency, integer
presentation checks, and agreement with an independent physical calculation
are recorded as distinct forms of evidence.

## Formula reference and implementation

The [canonical Markdown guide](docs/FORMULA_GUIDE.md) is the common mathematical
reference. It defines the cochain conventions, source/product pair and finite
operations before linking the executable implementation. The
[implementation map](formulas/README.md) gives API and source locations.
The complete publication coordinate covers 3+1D and 4+1D. Additional
lower-dimensional endpoints have the domains stated in the formula guide.

The readable source under `formulas/publication_source` and its fixed coefficient
tables are retained verbatim. The scalar evaluator and shared-background transfer
are implemented separately. Recompile a core formula into a fresh directory:

```sh
python3 -m fspt.full_formula.compiler \
  --source formulas/publication_source --target high6 \
  --out runs/recompiled/high6.json
```

Production supports Python 3.8. Recompiling the retained readable source requires
Python 3.9 or newer. For the existing full integration suite, on an allocated
node:

```sh
python3 scripts/check_complete_release.py --gap "$AFS_GAP" \
  --output runs/release_check --recompile-formulas
```

This checks retained results, recompiles the core scalar programs and runs small
complete examples. It is a numerical validation suite, distinct from a
documentation-only update.

## Archives and publication updates

The [archive scope guide](docs/ARCHIVES.md) identifies which statements belong
to an earlier source version. In particular, the earlier finite-example
archive's graded-only 4+1D scope does not describe the current full-group engine.

The [original complete release](COMPLETE_RELEASE_MANIFEST.json),
[resolution update](RESOLUTION_UPDATE.json) and dated result archives retain
their original bytes. [ORGANIZATION_MANIFEST.json](ORGANIZATION_MANIFEST.json)
records the committed source version, public base commit and exact files of the
consolidated catalogue/documentation update. Mathematical runtime kernels were
not changed by this organization pass.

The maintained source under `docs/formulas/source/` supplies the mathematical
notation and equation blocks for subsequent manuscript editing. Run
`python docs/formulas/build_reference.py` and its `--check` mode to generate
and verify the guide, dimensional references, and programmer translation.
General and self-stacking laws have separate pages with shared navigation. Paper-specific exposition can be
adapted around those blocks; changes of a formula or its representative must
update the common definition and its implementation correspondence together.

For subsequent catalogue/documentation releases, use
`scripts/publish_organized_release.py` with separate source and public checkouts
and the expected public HEAD. It reads committed allowlisted files, preserves
earlier archives, refuses changes to published scientific payloads, and writes
the update manifest. It performs no commit or push. Review the result, run the
saved-data/documentation checks, then commit and push the public checkout.
The older `scripts/publish_snapshot.py` builds the historical archive layout;
it is not the update path for the current catalogue.
