# Computed classification and stacking examples

This catalog collects **1,234 accepted named calculations** with their exact
inputs, final layer quotients and full stacking groups. It combines the existing
832-record complete-formula release with all 398 accepted inputs from the subsequent
398-input campaign and four separately completed controls. The five examples in
the October 2 supplement are part of the 398 and are counted once.
The acceptance cutoff for this catalog is **7 October 2026, 15:11 UTC**.

| Collection | Named calculations | Tables |
|---|---:|---|
| 3+1D space groups, crystalline spin-1/2 | 230 | [Markdown](tables/space_groups_spin_half.md) / [CSV](tables/space_groups_spin_half.csv) |
| 3+1D space groups, crystalline spinless | 230 | [Markdown](tables/space_groups_spinless.md) / [CSV](tables/space_groups_spinless.csv) |
| 3+1D point groups, both crystalline conventions | 64 | [Markdown](tables/point_groups.md) / [CSV](tables/point_groups.csv) |
| 1+1D finite internal controls | 6 | [Markdown](tables/internal_1d.md) / [CSV](tables/internal_1d.csv) |
| 2+1D finite internal controls | 17 | [Markdown](tables/internal_2d.md) / [CSV](tables/internal_2d.csv) |
| 3+1D finite internal symmetries | 78 | [Markdown](tables/internal_3d.md) / [CSV](tables/internal_3d.csv) |
| 4+1D finite internal symmetries | 609 | [Markdown](tables/internal_4d.md) / [CSV](tables/internal_4d.csv) |

Browse the [finite group families](tables/families.md), the overlapping
[symmetry calibration controls](tables/calibration_controls.md), or the
[machine-readable index](index.json). All **398/398 planned finite-campaign inputs** have complete acceptance.
The [campaign status](PENDING.md) records that no pending input remains.
The final additions are 4+1D `D8xC2_orbit_074`, `_091`, and `_092`.

The separate completed controls are signed split C8 in 3+1D, split SD16 in
3+1D and 4+1D, and Pin+ times C16 in 4+1D. The earlier release already includes
the Bott-family controls and lower-dimensional endpoints. Computed cochain and
geometric checks remain available in the [calibration collection](../finite_examples/calibrations/README.md).

## Exact inputs and conventions

Every finite internal record links to a standalone catalog specifying
`(G_b, s1, omega2)` through its multiplication table, binary antiunitary grading,
binary fermion-parity extension cocycle and generator indices. Tables and
generator indices are **one-based**, and element 1 is the identity. The group
order is the order of `G_b`, not its central extension by fermion parity.
Thus an input named Q16 with `G_b=Q16` is distinct from an input with
`G_f=Q16` and a smaller bosonic quotient.
The tables display whether the literal `omega2` representative is zero or
pointwise nonzero and link to its exact array. A pointwise nonzero cocycle
can be a coboundary; this column does not assert a nontrivial cohomology class.

For crystalline records the input recipe specifies the numbered space or
point group and physical spin convention. Crystalline spin-1/2 corresponds to
effective internal `s1=w1, omega2=0`; crystalline spinless corresponds to
`s1=w1, omega2=w2+w1 cup w1`. Space-group calculations include translations;
point-group calculations use the finite matrix group without translations.
The existing reproduction scripts retain the repository's crystallographic
numbering and group construction.

`[]` denotes the trivial group, `0` inside an invariant-factor array denotes
an infinite cyclic factor, and `n>1` denotes Z/n. The four layer columns are
the **final filtration quotients**, after incoming identifications. Their
direct product need not be the full stacking group. For the two explicitly
labelled zero-chiral 2+1D controls, the main result is the zero-chiral fiber;
the index separately records its abstract chiral completion.

The 1,234 records contain **1,229 distinct literal input/scope keys**. Five
identical-input pairs are linked in [exact_input_aliases.json](exact_input_aliases.json).
Historical names and calculations are retained. The 78 finite 3+1D named
records contain 77 literal backgrounds; the corresponding [symbolic background
table](tables/internal_3d_symbolic.csv) and [complete section witnesses](tables/internal_3d_symbolic.json)
provide short explicit cocycles, final layers and groups for manuscript use.
The [background definitions](SYMBOLIC_3D_BACKGROUNDS.md) explain those symbols.
This count does not identify
all isomorphic groups, automorphism-related backgrounds or cocycles differing
by a section change. Previously certified coordinate dictionaries remain in
the [historical aliases](../complete_formulas/catalog/historical_aliases.json)
and [transformations](../complete_formulas/catalog/historical_transformations.json).

## Saved results and reproduction

The original 832 complete raw results and their validation records remain
unchanged. The 402 additional records are explicitly tagged
`accepted-scientific-summary`. Each summary supplies the exact input, accepted
full group, final filtration, formula-source identity and saved acceptance
hashes. When available it also retains the complete numerical presentation.
These summaries are not represented as complete raw cochain traces or as
independent arithmetic replays. All completed inputs have a retained result
record.

Run from the repository root on an allocated compute node:

```sh
python3 scripts/run_complete_example.py --index results/computed_examples/index.json --list
python3 scripts/run_complete_example.py --index results/computed_examples/index.json \
  --case d4_D32_orbit_019 --output runs/D32_019.json --audit
python3 scripts/run_complete_example.py --index results/computed_examples/index.json \
  --case d4_Pin_plus_times_C16 --output runs/PinPlus_C16.json --audit
```

The runner uses the saved input and resolution strategy. Formula and runtime
choices are recorded separately from expected answers; the group comparison
occurs after the new calculation. Add `--dry-run` to inspect the command without
calculating. Runtime depends strongly on the group, resolution and configured
coherence checks.

Rebuild or verify the readable tables without GAP:

```sh
python3 results/computed_examples/rebuild_tables.py
python3 results/computed_examples/rebuild_tables.py --check
python3 results/computed_examples/rebuild_symbolic_3d.py --check
python3 results/computed_examples/validate_catalog.py
python3 results/computed_examples/rebuild_manifest.py --check
```

Acceptance means that the recorded complete calculation and its configured
checks succeeded. It does not state that every possible generator triple was
tested or that every prediction has an independent physical comparison.
Historical numerical provenance is retained as hashes; machine directories,
cluster identifiers and private working notes are not dependencies of this
catalog.
