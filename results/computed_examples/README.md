# Computed classification and stacking examples

This catalog contains **1,190 distinct computed examples** and retains all
**1,234 accepted calculation records** as their provenance. Repeated runs,
group relabelings and equivalent cocycle representatives do not create new
reader rows. The acceptance cutoff is **7 October 2026, 15:11 UTC**.

| Collection | Distinct examples | Tables |
|---|---:|---|
| 3+1D space groups, crystalline spin-1/2 | 230 | [Markdown](tables/space_groups_spin_half.md) / [CSV](tables/space_groups_spin_half.csv) |
| 3+1D space groups, crystalline spinless | 230 | [Markdown](tables/space_groups_spinless.md) / [CSV](tables/space_groups_spinless.csv) |
| 3+1D point groups, both crystalline conventions | 64 | [Markdown](tables/point_groups.md) / [CSV](tables/point_groups.csv) |
| 1+1D finite internal controls | 6 | [Markdown](tables/internal_1d.md) / [CSV](tables/internal_1d.csv) |
| 2+1D finite internal controls | 16 | [Markdown](tables/internal_2d.md) / [CSV](tables/internal_2d.csv) |
| 3+1D finite internal symmetries | 72 | [Markdown](tables/internal_3d.md) / [CSV](tables/internal_3d.csv) |
| 4+1D finite internal symmetries | 572 | [Seven family tables](tables/internal_4d.md) / [CSV](tables/internal_4d.csv) |

The [4+1D family tables](tables/internal_4d.md) place every background in
exactly one family. The lower-dimensional [family views](tables/families.md)
and [control view](tables/calibration_controls.md) are alternative ways to
browse the same examples; their counts are not added to the table above.
The [unique example index](unique_examples.json) connects each reader entry to
its saved calculations. The original [calculation index](index.json) retains
all names and numerical provenance, including 44 additional records of
backgrounds already represented.

All **398/398 planned finite-campaign inputs** have complete acceptance;
[no pending input remains](PENDING.md). The original 832-record release,
398-input campaign and four separately completed controls are all covered.
The October 2 supplement belongs to the campaign and is counted once.
Cochain and geometric checks have a different scope; the
[4+1D calibration guide](CALIBRATIONS_4D.md) lists them separately, including
the current exact check of the handwritten $\mathbb Z_4^f$ representatives.

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

The unique index groups finite examples at fixed dimension and calculation
scope by a verified isomorphism of $(G_b,s_1,[\omega_2])$. Every merge has an
explicit group map and a section one-cochain; multiplication, grading and
cocycle transport are checked on all group-element pairs. Stacking groups
and final filtrations agree across every merged set. The
[4+1D coverage ledger](COVERAGE_4D.json) also verifies that the 572 retained
backgrounds are pairwise distinct. The numbered crystalline inputs and
physical spin conventions are preserved separately.

The 78 named finite 3+1D records become **72 distinct backgrounds**. The
[symbolic table](tables/internal_3d_symbolic.csv),
[section witnesses](tables/internal_3d_symbolic.json) and
[background definitions](SYMBOLIC_3D_BACKGROUNDS.md) give short explicit
cocycles for manuscript use. One row is the handwritten
$\mathbb Z_4^{f,T}$ example; the other 71 are additional backgrounds.
The 609 named 4+1D records become **572 backgrounds**, with their symbols
specified in the [4+1D background definitions](FOUR_DIMENSIONAL_BACKGROUNDS.md).

The earlier [literal-input alias list](exact_input_aliases.json),
[historical aliases](../complete_formulas/catalog/historical_aliases.json)
and [transformations](../complete_formulas/catalog/historical_transformations.json)
remain provenance. Literal-array equality is a weaker deduplication criterion
than the background equivalence used in the current tables.

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

Verify the readable tables and cochain check without GAP (omit `--check` on
the table builders to regenerate in the same order):

```sh
python3 results/computed_examples/rebuild_symbolic_4d.py --check
python3 results/computed_examples/rebuild_unique_examples.py --check
python3 results/computed_examples/rebuild_tables.py --check
python3 results/computed_examples/rebuild_symbolic_3d.py --check
python3 results/computed_examples/validate_catalog.py
python3 scripts/check_z4f_current_cochains.py
python3 results/computed_examples/rebuild_manifest.py --check
```

Acceptance means that the recorded complete calculation and its configured
checks succeeded. It does not state that every possible generator triple was
tested or that every prediction has an independent physical comparison.
Historical numerical provenance is retained as hashes; machine directories,
cluster identifiers and private working notes are not dependencies of this
catalog.
