> Public release: this document describes the complete local audit. [Private reference inputs](../PUBLIC_RELEASE.md#private-comparison-materials) are not distributed; production and independent result audits remain reproducible.

# Reproducible final archive and external comparisons

The v09 campaign has been accepted and archived at `results/space_groups`.
All 230 full AW-v2 witness outputs, their uniform source and the measured
campaign evidence passed strict auditing. Its literal mathematical witnesses
also agree with the complete v07 mathematical baseline (229 original v07
outputs plus its same-source SG219 retry).
The accepted source ID is
`9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`;
the `archive.json` SHA256 is
`60bc072c330c838a10e6a1f663eb6664e1d09e010b5081141dacf609aff33831`.
The initial archive contains 1,198 files and 15,929,682 bytes, including its
manifest and excluding subsequently generated reports. Its largest single-task
RSS is SG219's 16.869 GiB.

The independent classification freeze and the small comparison inputs have
already been archived and their original bytes verified. Their existing
directories are evidence to retain, not destinations to rebuild in place.

The accepted campaign is archived by the campaign coordinator at:

```text
results/space_groups/
  sg1.json ... sg230.json
  classification/sg1.json ... sg230.json
  source/gap/
  archive.json
  campaign.json
  observation.json
  performance.json
  tasks/
  deadline_extensions.json              # when an audited extension was used
  deadline_extensions/LEDGER_NAME/       # complete original supervision evidence
  report/
```

The completed strict archive operation has this command form. The accepted
destination already exists: do not run it again against that directory.
For an independent reconstruction, replace `results/space_groups` with a new,
nonexistent destination and keep the original run/source inputs unchanged.

```sh
python3 scripts/archive_campaign.py FINAL_RUN \
  --source FROZEN_SOURCE \
  --tasks-root runs/tasks \
  --output results/space_groups
```

It rejects an existing destination. Before creating any destination directory,
it audits all 230 complete AW-v2 witnesses, verifies the actual frozen
`gap/*.g` bytes against the uniform campaign source, checks classification
checkpoints, and runs strict performance collection. It then copies only the
original result/checkpoint JSON, campaign/observer records, frozen GAP source,
and each task's status, metrics and stdout. When a task used an explicit
deadline extension, its original `deadline_extensions.json` index and the
completed supervision ledger are also copied without changing their bytes.
`stdout.log` is stored unchanged
as `stdout.txt`; original absolute paths inside JSON are retained. A newly
computed `performance.json` and `archive.json` record the audits and the
original-to-archived path, hash and byte-count mapping. No reference is read.
The later generated human-readable report lives under `report/` and is not
part of the initial byte-preserving archive operation.

The extension ledger includes the predeadline plan, original task/status
snapshots, guard and watchdog identities/events, frozen guard source,
per-task exit observations, and completed supervision summary. The raw
worker status is retained even when it says `timeout` with `exit_code=0`.
Only an independent audit of that original reap result, GNU time and the
complete ledger can assign the separate effective state
`done_with_audited_deadline_extension`; it never rewrites the raw status to
`done`. Actual exit observations and their time intervals remain distinct
from the worker's later reap time. Ledger paths embedded in original JSON
are resolved through `archive.json` when auditing a relocated archive.

Keeping the group JSON files directly under this directory allows the
existing auditor, report generator and table utilities to read the archive
without another path adapter. Copy the selected immutable source and result
bytes; do not regenerate results from the live working tree or select a
different configuration for each group. Preserve source paths embedded in
the original outputs as historical provenance. The archived source hashes
and the archive manifest identify their new location.

Keep the independent pre-reference classification separately:

```text
results/classification_frozen/
  manifest.json
  sg1.json ... sg230.json
```

These 231 original files have already been copied from
`runs/classification_frozen` without editing any byte of the manifest or
results. The manifest SHA256 is
`42e42ce70900bf0df2dada35624198474f07e4a98dfe95770d462a69169ec438`.
Do not copy a later classification campaign over them. The timestamp, the
`external_answers_consulted=false` declaration, and all 230 result hashes
belong to that original freeze. They do not describe the later formula or
performance regression campaigns. Both comparison scripts recheck this
manifest and every frozen result hash.

The existing `results/boss_layers/reference_comparison.*` and
`parsed_reference.json` remain the historical first comparison. A later
comparison uses separate `current_reference_comparison.*` filenames.

## Small comparison inputs

The supplied inputs are already archived at
`results/external_comparison/inputs`, before the final campaign was selected.
Its manifest SHA256 is
`80d8ba92e2b495232e593445f7136a22d90161f05cdc77f01e92c4cd91c48c86`.
The following command documents reconstruction from the original supplied
sources **into a new, nonexistent directory only**. It is not a step to run
again against the existing archive; choose a new output name if such a
reconstruction is needed.

```sh
python3 scripts/archive_comparison_inputs.py \
  --boss-root /tmp/AllFSPT-inspect-boss \
  --reference-root /tmp/AllFSPT-inspect-fermionAHSS \
  --output NEW_INPUT_ARCHIVE
```

The command accepts explicit `--legacy-root`, `--pdf`, `--text` and
`--finite-controls` paths when the source files have moved. The current
inputs total 12 files and 931,809 bytes, excluding their generated manifest:

```text
results/external_comparison/inputs/
  manifest.json
  space_group_230_layers.pdf
  space_group_230_layers.txt
  finite_c2_controls.json
  boss/output/space_group_230/
    draft_table.json
    backend/FOUNDATIONS.md
    backend/hap_all230_e2.json
    backend/h1_all230.json
  fermionAHSS/data/extension-paper-results-20260926-transfer.json
  legacy_sg068.txt
  legacy_sg081.txt
  legacy_sg082.txt
  legacy_sg101.txt
```

The four `.txt` files contain the exact bytes of the original completed
SptSet logs. Their source-manifest hashes are checked before copying;
original absolute paths and hashes are retained in the input manifest.
Renaming avoids the repository's `*.log` ignore rule without changing line
endings or text. An existing destination is rejected. This archive contains
reference outputs and independently calculated finite controls, without
external implementation code or any production answer-table dependency.

## Reproduce the final comparisons

Use a modern Python environment with the report-only dependency in
`requirements-report.txt`. The exercised PDF parser version is PyMuPDF
1.28.0. The other archive and external-comparison scripts use the standard
library.

Run the strict result audit first:

```sh
python3 scripts/audit_run.py results/space_groups \
  --require-complete-witnesses \
  --require-formula-convention normalized-pip-aw-edge-transport-v2
```

Independently recompute strict performance from the
portable archive with its **archived task directory explicitly supplied**:

```sh
python3 scripts/collect_performance.py results/space_groups \
  --tasks-root results/space_groups/tasks \
  --output runs/final_performance_recheck.json
```

Do not omit `--tasks-root`: its default would select the sibling
`results/tasks`, not the archived tasks. Do not use `--allow-partial` for
final validation. The new report is written outside the archive so the
archived `performance.json` and its recorded hash remain unchanged.
The collector rechecks any archived deadline-extension evidence instead of
silently accepting a raw timeout state. These checks use the accepted archive
and do not require the original compute-node allocations to remain active.

Compare the final four layers with both the original freeze and the PDF:

```sh
python3 scripts/compare_boss.py \
  --current results/space_groups \
  --frozen results/classification_frozen \
  --pdf results/external_comparison/inputs/space_group_230_layers.pdf \
  --text results/external_comparison/inputs/space_group_230_layers.txt \
  --output results/boss_layers
```

This requires all 230 complete AW-v2 witness results. Its JSON records the
unchanged frozen hashes and the current result/source hashes separately,
with all 920 current-versus-frozen and current-versus-PDF comparisons. It
preserves the original report files. The PDF does not supply full stacking
extensions or a marked free-lattice basis.

Compare the available historical stacking, geometric and finite-group
reference results:

```sh
python3 scripts/compare_external_refs.py \
  --classification results/classification_frozen \
  --computed results/space_groups \
  --require-complete \
  --boss-root results/external_comparison/inputs/boss \
  --reference-root results/external_comparison/inputs/fermionAHSS \
  --finite-controls results/external_comparison/inputs/finite_c2_controls.json \
  --output results/external_comparison
```

`--require-complete` additionally requires one uniform source for all 230
groups. It cannot report a partial campaign as final. The output records all
original frozen hashes, current result/source hashes, and each numerical
reference input's hash. Its historical mismatch categories distinguish
changed filtration layers from disagreements about extensions with the same
four layers. The finite comparison selects only the supplied actual C2,
spatial-dimension-three, omega-zero models; no point-group replacement of an
affine space group is made.

The earlier `runs/comparison_external/comparison*.json` files remain
historical reports. The final result uses the new tracked output directory.
The reference checkout has no supplied affine-230 stacking table; the final
report must preserve that availability boundary instead of inventing a
missing comparison.

Both final comparisons have now been run against the accepted archive. All
920 four-layer entries agree with both the original freeze and the boss PDF.
The historical full-stacking references give 179 matches, 21 disagreements
with changed filtration layers and four disagreements with unchanged layers
(SG68, 81, 82, 101); 26 groups have no historical stacking reference. All nine
applicable geometric references, 687 raw mod-2 cohomology dimensions, 230
signed-H1 groups and four matching finite-C2 labels agree. Those four labels
represent two distinct finite-group inputs, not four affine-space-group tests.
SG219 has no historical full-stacking reference; its four current layers
agree with the boss PDF.

## Prepared controls

The new archive and provenance controls pass:

```sh
python3 tests/test_boss_parser.py
python3 tests/test_boss_current.py
python3 tests/test_external_comparison.py
python3 tests/test_comparison_archive.py
```

A temporary archive of the actual 12 inputs and the exact independent
freeze was also tested from outside the project directory. It reproduced
the original 920 PDF matches, the existing historical categories
179/21/4 with 26 missing references, and four matching finite-C2 labels.
The final-mode check rejected the actual partial campaign without writing
an output. This was a portability control, not a final campaign comparison;
its hashes and outcomes are in
`docs/validation_runs/comparison_archive.json`.
