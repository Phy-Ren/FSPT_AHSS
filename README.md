# U(1)^f insulator AHSS

Exact obstruction equations, decoration layers, and stacking for interacting
U(1)^f insulators with crystalline or discrete internal symmetries. The
`insulator` branch has its own formula engine, group inputs, classifier, and
results.

- **[Computed examples](results/current/README.md):** one current catalogue,
  organized by spacetime dimension, physical spin, and response sector.
- **[Formula guide](docs/FORMULA_GUIDE.md):** the E8-first four-data tower,
  obstruction equations, stacking twisters, and gauge transformations.
- **[Provenance and scope](results/current/PROVENANCE.md):** accepted inputs,
  source versions, calculation records, and the limits of each comparison.
- **[3+1D mismatch audit](benchmarks/point3_mismatch_audit_20261016/README.md):**
  independent bordism checks, specific source errors, and separate spin tables.

## Computed examples

The current catalogue contains **584 distinct backgrounds**: 578 crystalline
backgrounds and six internal cyclic backgrounds. Their **638 response-sector
entries** are organized into 13 tables:

- [2+1D](results/current/2p1d/README.md): all 10 planar point groups and 17
  wallpaper groups, for spinless and spin-1/2 electrons. Each background has
  separate `n0=0` and all-allowed-`n0` tables; both fix `e0=0`.
- [3+1D](results/current/3p1d/README.md): all 32 crystallographic point groups
  and all **230 space groups**, for spinless and spin-1/2 electrons, with
  E8 included in the four-data calculation.
- [4+1D](results/current/4p1d/README.md): internal unitary `C1` through `C6`,
  with `s=rho=omega=0`, including the shared-phase E8 stacking relations.

Each row records the four final filtration groups
`(e_p,n_p,n_{p+2},nu_{p+3})`, with `p=d−2`, and the final stacking group.
The layers include incoming identifications; their direct product need not
equal the stacking group. Wallpaper and space-group calculations use the
full infinite affine groups, including translations and nonsymmorphic
operations. A background means a group with its physical spin and extension
data fixed. The two 2+1D response sectors produce separate entries for the
same background.

Interacting literature classifications have separate, versioned columns.
**✓** marks the same reported group; **×** marks a different reported group.
Layer comparisons remain distinct from stacking comparisons. In the
space-group tables, the Song–Xiong–Huang comparison tests the neutral E8
layer; a full interacting electronic benchmark remains unverified. The
catalogue computes the selected four-data model. Its identification with
the complete physical CI kernel remains conditional; agreement of final
group types alone does not establish that identification.

## Formulas

The [formula guide](docs/FORMULA_GUIDE.md) uses one notation throughout
2+1D, 3+1D, and 4+1D. It presents obstruction equations before stacking,
then specifies gauge transformations and the operations needed to evaluate
the formulas. The [implementation reference](formulas/README.md) records
the supplied formula packages and their normalization.

The local API uses `E8State(e_p,n_p,n_p2,nu_p3)`, with one shared phase.
Integer lifts, signed coefficients, source terms, stacking corrections, and
changes of representatives are transported together. Independent actions
`s1`, `rho1`, and `rho1+s1` remain explicit.

The global CI classifier retains completed states, incoming gauge
identifications, arbitrary root relations, and an integer presentation.
The 3+1D E8 extension computes signed integer `H1(G,Z_s)` for finite point
groups or full affine space groups and combines its section with that
presentation. Affine CI roots retain the full integer obstruction kernels;
free translations are not replaced by finite holonomy. The 4+1D cyclic pilot
computes all four layers together. Intrinsic higher-response sectors and a
general global 4+1D classification remain outside the current catalogue.
Missing operations are not assigned zero.

## Install and run

Python 3.8 or newer and GAP with HAP, Polycyclic, Cryst, and CrystCat are
required. SymPy supports exact presentation checks and the E8 extension.

```bash
python3 -m unittest discover -s tests
python3 scripts/classify.py --family point2 --jobs 4 --output runs/point2
python3 scripts/classify.py --family wallpaper --jobs 4 --output runs/wallpaper
python3 scripts/classify_3p1d.py --family point3 --jobs 4 --output runs/point3
python3 scripts/classify_3p1d.py --family spacegroup --pair-spins --largest-first --jobs 4 --memory 32g --timeout 14400 --output runs/spacegroup
```

For 3+1D, the unified command runs CI classification, the exact neutral E8
section, and final acceptance. It reports `complete` only when all selected
four-data results pass acceptance. The new output root contains `ci/`, `e8/`,
`accepted/`, stage logs and `workflow.json` with commands, exit status and
source provenance. Accepted point-group and space-group results reside under
`accepted/3p1d/point_groups/` and `accepted/3p1d/space_groups/`, respectively.
This implements the [proved factorization of the supplied 3+1D model](docs/formulas/THREE_DIMENSIONAL.md#why-the-global-calculation-can-be-factored).

Use `--case point3_04_spin_half` for one 3+1D input or `--spin spinless` for
one physical spin. Each output directory must be new; there is no automatic
resume or overwrite. Run classification campaigns on compute nodes with
immutable source snapshots. The unified entrypoint accepts only `point3`
and `spacegroup`; it does not offer a general 4+1D solver.

The full-space-group example sets a `32g` workspace cap per GAP process and
14,400 seconds per case; a paired process shares twice that time budget.
Choose `--jobs` so all concurrent GAP processes and their Python workers fit
the compute node's memory. The [recorded 8g failure](docs/PERFORMANCE.md)
explains the larger workspace allowance.

The separate 2+1D `classify.py` command supports `--uniform-iqh` for all
allowed uniform Hall responses. For advanced staged 3+1D workflows,
`classify.py`, `extend_e8_3p1.py` and `collect_expansion.py` remain available
individually with their existing immutable output conventions.

`--pair-spins` reuses geometry, the resolution, and linear algebra with
identical coefficient actions, while keeping independent extension inputs
and classification states. `--largest-first` starts larger holonomy groups
first. Set concurrency and memory limits from the available compute node;
each GAP process has one persistent exact-arithmetic Python worker.
The unified command forwards the native/reference mode options and accepts
`--formula-mode auto|python|reference` for exact formula dispatch.
The [performance guide](docs/PERFORMANCE.md) documents the reused native
cohomology operations, generated U1 formulas, reference-comparison switches,
and measured complete-run checks.

Every calculation retains its exact symmetry input, source and input hashes,
integer presentation, witnesses, and execution logs. Literature answers are
read only after classification. Rebuild or verify the active catalogue with:

```bash
python3 scripts/build_current_tables.py
python3 scripts/build_current_tables.py --check
```

## Verification

Checks cover source closure, product and gauge compatibility, inverse and
root relations, signed coefficient actions, integer presentations, and the
actual uniform-response kernel. The catalogue's
[provenance guide](results/current/PROVENANCE.md) links the source audits and
immutable records without introducing duplicate reader tables.

The insulator implementation has no runtime dependency on the superconducting
branch. Generic geometry and integer-resolution infrastructure retain their
source attribution in the implementation documentation.
