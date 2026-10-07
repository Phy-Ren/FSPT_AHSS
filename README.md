# FSPT_AHSS

Exact classification and stacking of fermionic SPT phases with crystalline or
finite internal symmetries. A calculation first constructs the allowed
decoration layers, then determines their stacking extensions using the same
representatives. Independent symmetry backgrounds can run in parallel.

- **[Computed examples](results/computed_examples/README.md):** all completed
  examples in one catalogue, organized by dimension, symmetry family and use.
- **[Formula guide](docs/FORMULA_GUIDE.md):** one notation system for the complete
  3+1D and 4+1D obstruction and stacking formulas, with explicit definitions of
  the operations and coefficients.
- **[Run and verify](PUBLIC_RELEASE.md):** exact inputs, reproduction commands,
  saved-result checks and the scope of each kind of evidence.

## Computed examples

The consolidated catalogue contains **1,231 completed calculation records**:

| Collection | Records |
| --- | ---: |
| 3+1D space groups, both crystalline spin conventions | 460 |
| 3+1D crystallographic point groups, both conventions | 64 |
| 1+1D finite internal symmetries and controls | 6 |
| 2+1D finite internal symmetries and controls | 17 |
| 3+1D finite internal symmetries and controls | 78 |
| 4+1D finite internal symmetries and controls | 606 |

Historical names, coordinate representatives and independently repeated controls
remain identifiable. These records have 1,226 distinct literal input/scope keys;
this is not a count of inequivalent physical symmetries. The catalogue also links
the earlier cochain and geometric calibration examples. Three unfinished
backgrounds are listed separately and have no asserted final result.

Every finite background specifies the bosonic quotient group, its multiplication
table, antiunitary grading $s_1$, and normalized fermion-parity cocycle
$\omega_2$. The group order always refers to $G_b$. Dihedral and quaternion
names are accompanied by exact group data. The final stacking group and final
decoration filtration are recorded separately.

| Crystalline convention | Effective internal background | SG | PG |
| --- | --- | ---: | ---: |
| Spin-1/2, corresponding to internal spinless | $s_1=w_1$, $\omega_2=0$ | 230 | 32 |
| Spinless, corresponding to internal spin-1/2 | $s_1=w_1$, $\omega_2=w_2+w_1^2$ | 230 | 32 |

Space groups use the full infinite affine group, including translations and weak
phases. Point groups use the finite three-dimensional matrix group.

## Formulas

Start with the [canonical formula guide](docs/FORMULA_GUIDE.md). It introduces
the decoration fields once, then gives the obstruction tower and stacking law
in their order of evaluation. Shared expressions are defined once and reused;
the appendices specify the finite operations and fixed coefficients needed to
expand every term. The [implementation map](formulas/README.md) connects these
definitions to the independently implemented runtime.

The guide links obstructions, general twisters, and separate self-stacking
references in that order for each dimension. The
[simplification record](docs/formulas/SIMPLIFICATION_PROGRESS.md) identifies
reductions already incorporated and remaining large blocks; the
[term census](docs/formulas/TERM_COUNTS.md) gives exact counts. All reader
pages are generated from [one maintained source](docs/formulas/source/README.md),
including shared equations and the programmer translation.

Integer lifts, negative carries, local coefficients and cochain representative
changes are explicit. Source and stacking coordinates must be transported
together. The complete publication-coordinate implementation covers 3+1D and
4+1D; the guide states the domains of the additional lower-dimensional endpoints.

## Install and run

The retained computation environment used GAP 4.13.1, HAP 1.62, CrystCat 1.1.10,
Polycyclic 2.16, the GAP JSON and IO packages, and Python 3.8.16. SymPy is used
for independent integer-presentation checks. A C++11 compiler enables the
optional exact native evaluator:

```sh
python3 -m pip install -r requirements-runtime.txt
g++ -O3 -std=c++11 -shared -fPIC fspt/full_formula/native.cpp \
  -o fspt/full_formula/native.so
export AFS_GAP=/path/to/gap
python3 scripts/run_complete_example.py \
  --index results/computed_examples/index.json --list
python3 scripts/run_complete_example.py \
  --index results/computed_examples/index.json \
  --case d3_C2_w1_s1 --output runs/pin_plus_3d.json --audit
```

Run numerical jobs on an allocated compute node. Each output path must be new.
The runner reads the exact symmetry input and retained performance options;
expected answer groups are used only after the calculation for comparison.
The Python evaluator remains exact without the native library.

For new finite inputs or a crystalline group:

```sh
python3 scripts/run_full_finite.py \
  --catalog results/complete_formulas/catalog/models.json \
  --model Q8_orbit_000 --dimension 4 --output runs/q8_4d.json
python3 scripts/run_full_space_group.py 219 --crystalline-spin spinless \
  --output runs/sg219_spinless.json
python3 scripts/run_full_point_group.py 10 --crystalline-spin half \
  --output runs/pg10_half.json
```

## Verification and archives

The result catalogue distinguishes full numerical records from compact accepted
scientific summaries. Both provide exact inputs and completed groups. Full
records additionally retain the integer presentations and witnesses needed for
independent saved-result arithmetic checks. Verification commands and evidence
definitions are in the [reproduction guide](PUBLIC_RELEASE.md).

A computed prediction, a cochain consistency check, and agreement with an
independent physical calculation are different kinds of evidence. Each example
retains its actual validation scope. Only a nontrivial obstruction class after
the permitted lower-layer adjustments excludes a candidate decoration.

Earlier [complete-formula results](results/complete_formulas/README.md), the
[October 2 supplement](results/complete_formulas_20261002_supplement/README.md),
[crystalline archives](results/group_tables/README.md), and
[finite-example archives](results/finite_examples/README.md) retain their
original bytes and source versions. The consolidated catalogue connects these
collections to the subsequent completed examples.
The [archive scope guide](docs/ARCHIVES.md) distinguishes their historical
documentation from the current formula and result references.
