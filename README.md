# FSPT_AHSS

Exact classification and stacking of fermionic SPT phases, using independently
implemented cochain operations, gauge equivalences, and integer presentations.
Classification and stacking run sequentially in one process and share the same
representatives. Different symmetry inputs can run in parallel. SptSet is not
loaded.

The initial [complete-formula results](results/complete_formulas/README.md) contain
**769 completed production calculations**:

- 230 space groups in each crystalline spin convention: 460 calculations.
- 32 crystallographic point groups in each convention: 64 calculations.
- 245 finite internal-symmetry inputs: 229 in 4+1D and 16 in 3+1D.

The 4+1D finite catalog contains **202 typed physical cases**. The 229 exact
calculations also retain 27 historical coordinate representatives. An additional
63 completed controls are listed separately. These counts describe calculation
records, not 832 inequivalent physical symmetries.

The [2026-10-02 supplement](results/complete_formulas_20261002_supplement/README.md)
adds five accepted finite calculations, including two further independent
full-group checks. Its dated inventory preserves the original release unchanged.

All current production rows contain the full abstract stacking group, its
presentation, and gauge-reduction witnesses. The [formula guide](formulas/README.md)
links every obstruction and stacking operation to readable definitions and exact
executable tables. No private archive is needed to evaluate the formulas or run
the published inputs.

| Crystalline convention | Effective internal background | SG | PG |
|---|---|---:|---:|
| Spin-1/2, corresponding to internal spinless | `s=w1`, `omega2=0` | 230 | 32 |
| Spinless, corresponding to internal spin-1/2 | `s=w1`, `omega2=w2+w1^2` | 230 | 32 |

Space groups use the full infinite affine group, including translations and weak
phases. Point groups use the finite three-dimensional matrix group.

## Install and run

The computation environment used GAP 4.13.1, HAP 1.62, CrystCat 1.1.10,
Polycyclic 2.16, the GAP JSON and IO packages, and Python 3.8.16. Install SymPy for
independent integer-presentation checks. A C++11 compiler enables the optional
exact native evaluator:

```sh
python3 -m pip install -r requirements-runtime.txt
g++ -O3 -std=c++11 -shared -fPIC fspt/full_formula/native.cpp \
  -o fspt/full_formula/native.so
export AFS_GAP=/path/to/gap
python3 scripts/run_complete_example.py --list
python3 scripts/run_complete_example.py --case d3_C2_w1_s1 \
  --output runs/pin_plus_3d.json --audit
```

Run on an allocated compute node. Each result path must be new. The runner freezes
its source and records hashes before computing. The Python evaluator is exact
without the native library, but can be substantially slower.

For arbitrary published or new inputs:

```sh
python3 scripts/run_full_finite.py \
  --catalog results/complete_formulas/catalog/models.json \
  --model Q8_orbit_000 --dimension 4 --output runs/q8_4d.json
python3 scripts/run_full_space_group.py 219 --crystalline-spin spinless \
  --output runs/sg219_spinless.json
python3 scripts/run_full_point_group.py 10 --crystalline-spin half \
  --output runs/pg10_half.json
```

`--help` lists exact performance options and additional coherence/bar probes.
The [reproduction guide](PUBLIC_RELEASE.md) explains inputs, result fields and
verification. [Lower-dimensional scope](formulas/README.md#lower-dimensional-endpoints)
is stated separately from the complete 3+1D and 4+1D formulas.

## Verification and interpretation

```sh
python3 scripts/verify_complete_results.py
python3 scripts/verify_complete_results.py --arithmetic
```

The first command checks all 832 exported records and their exact inputs. The
second independently recomputes Smith normal forms, checks GAP's unimodular
certificates, and computes the final filtration by Hermite reduction, including
incoming gauge relations. It does not establish physical normalization by itself.

The canonical finite table has independent full-group targets for 49 of its 202
cases. Target provenance is explicitly labeled as published, Bott-derived, or
independently derived from primary results. The other rows remain computed
predictions; an exponent lower bound is not a full-group target. Crystalline
regression against earlier computations is also distinct from independent
physical calibration.

Earlier [crystalline archives](results/group_tables/README.md) and
[finite-example archives](results/finite_examples/README.md) remain available with
their original source versions. The new complete-formula tables are the current
results. Historical archive timings should not be interpreted as timings of the
new complete-formula engine.
