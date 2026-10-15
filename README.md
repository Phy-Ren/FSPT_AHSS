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

## Computed examples

The current catalogue covers **118 crystalline backgrounds and six internal
cyclic backgrounds**, with 178 response-sector entries:

- [2+1D](results/current/2p1d/README.md): all 10 planar point groups and 17
  wallpaper groups, for spinless and spin-1/2 electrons. Each background has
  separate `n0=0` and all-allowed-`n0` tables; both fix `e0=0`.
- [3+1D](results/current/3p1d/README.md): all 32 crystallographic point groups,
  for both physical spins, with the computed neutral E8 data included.
- [4+1D](results/current/4p1d/README.md): internal unitary `C1` through `C6`,
  with `s=rho=omega=0`, including the shared-phase E8 stacking relations.

Each row records the four final filtration groups
`(e_p,n_p,n_(p+2),nu_(p+3))`, with `p=d−2`, and the final stacking group.
The layers include incoming identifications; their direct product need not
equal the stacking group. Wallpaper calculations use the full infinite
affine group, including translations and glides.

Interacting literature classifications have separate, versioned columns.
**✓** marks the same reported group; **×** marks a different reported group.
Layer comparisons remain distinct from stacking comparisons. The 3+1D result
is the selected four-data model; its identification with the complete physical
CI kernel remains conditional. Matching group types alone do not establish
that identification.

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
python3 scripts/classify.py --family point3 --jobs 4 --output runs/point3
python3 scripts/extend_e8_3p1.py --ci-root runs/point3 --output runs/point3_e8
python3 scripts/classify.py --family spacegroup --pair-spins --largest-first --jobs 4 --output runs/spacegroup
python3 scripts/extend_e8_3p1.py --ci-root runs/spacegroup --output runs/spacegroup_e8
```

Use `--case point2_02_spin_half` for one input or `--spin spinless` for one
physical spin. A separate 2+1D run with `--uniform-iqh` includes all allowed
uniform Hall responses. Each output directory must be new. Run classification
campaigns on compute nodes with immutable source snapshots.

`--pair-spins` reuses geometry, the resolution, and linear algebra with
identical coefficient actions, while keeping independent extension inputs
and classification states. `--largest-first` starts larger holonomy groups
first. Set concurrency and memory limits from the available compute node;
each GAP process has one persistent exact-arithmetic Python worker.

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
