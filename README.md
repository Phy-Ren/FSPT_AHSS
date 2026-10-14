# U(1)^f insulator AHSS

The `insulator` branch implements the supplied U(1)^f cochain tower independently
of the superconducting implementation on `main`. It has its own formula package,
GAP classification backend, group inputs, tests, results and documentation.

The formula authority is `U1f_AHSS_Consolidated_v0_7_complete.zip`, SHA-256
`a1410f854828f012dc9be56cfd62dc0eb4a195779c09eed273e6a70f2ca97a4a`.
The implementation uses its calibrated sheet-linear convention throughout:
cubic coefficient `1/6`, additional product coefficient `epsilon=0`, and matched
source, stacking and gauge representatives. See [the formula reference](formulas/README.md)
for equations, provenance and coverage.

**Start with the [foundation review](docs/foundations/README.md) and
[rebuilt comparison tables](results/foundation_review_20261014/README.md).**
Spinless and spin-half results have separate table files. In 2+1D, the
`n0=0` and all-allowed-`n0` tables are also separate; all current tables
exclude independent E8 decoration (`e0=0` in 2+1D). Each source has its own
column. E8 decoration and full E8-inclusive tables are deferred.
Main comparison tables use interacting classifications; band-generated
interacting reductions appear only in separate diagnostic tables.

The first campaigns are complete: **172 successful calculations** across both
physical spin conventions, including independent `n0=0` and all-allowed-`n0`
2D runs, both with `e0=0`.
The [original campaign report](results/README.md) preserves computation
provenance. Its first summary is historical; use the rebuilt per-case tables
for current comparisons, source versions, bordism evidence and unresolved
physical maps. Successful runs and abstract group matches do not certify
complete physical calibration.

## Mathematical scope

For spatial dimension `d`, a complete state has an integer CI sheet `n_(d-2)`
with sign `s1`, an integer charge `n_d` with sign `rho1`, and a phase `nu_(d+1)`
with sign `s1`. The extension lift has sign `rho1+s1`. These coefficient actions
are independent in the formula engine and in the global backend.

The local engine covers **2+1D, 3+1D and 4+1D** obstruction sources, stacking
twisters, complete-state gauges and inverses. The current global campaigns cover
the **10 planar point groups, 17 full affine wallpaper groups, and 32 spatial
point groups**, each for physical spinless and spin-half electrons. Wallpaper
cohomology uses the infinite affine group, including translations and glides.

The computed sector is CI-generated, localized-charge and group-cohomological
phase data. The independent neutral E8 sector and intrinsic higher-response
sectors are outside the supplied tower. No missing operation is installed as zero.
The default 2+1D comparison fixes the uniform IQH index to zero; the optional
`--uniform-iqh` calculation solves its obstruction and supplies a completed lift.
Free filling classes remain present.

Global classifications retain the complete charge/CI lifts, incoming gauge
identifications, root relations and an integer presentation. Smith normal form
determines arbitrary torsion invariant factors and free rank. Graded layers
are not multiplied together to guess the final stacking group.

## Run

The formula worker and campaign runner require Python 3.8 or newer. The GAP
backend requires GAP with HAP, Polycyclic, Cryst and CrystCat. SymPy is required
only to rebuild catalogs and perform literature comparisons. Precomputed catalogs
contain exact symmetry geometry and backgrounds, never classification answers.

```bash
python3 -m unittest discover -s tests
python3 scripts/classify.py --family point2 --jobs 4 --output runs/point2
python3 scripts/classify.py --family wallpaper --jobs 4 --output runs/wallpaper
python3 scripts/classify.py --family point3 --jobs 4 --output runs/point3
python3 scripts/report_campaign.py runs/point2 runs/wallpaper runs/point3 --output results/campaign
```

Select one case with `--case point2_02_spin_half`, or one physical spin convention
with `--spin spinless`. Use `--uniform-iqh` in a separate 2+1D run to include the
uniform Hall layer. `--gap` selects the GAP executable, `--timeout` bounds each
case, and `--memory` caps each GAP workspace. Output directories must be new.

Every case records the exact input, generated GAP driver, stdout/stderr, source
and input hashes, host, timing, classification, integer presentation and witnesses.
A missing or failed result is reported explicitly. Run large campaigns on compute
nodes using immutable source snapshots.

## Validation and comparisons

Tests check cochain closure, source/product compatibility, gauge compatibility,
inverses, independent coefficient actions, coefficient-level universal certificates,
and completed root orders. Global internal-symmetry controls include the 2+1D
`U(1)^f x C2` root `Z4` and the 3+1D AIII/AII/AI CI-sector values `Z8`, `Z2^2`, `0`.

[Independent primary-source benchmark tables](benchmarks/README.md) distinguish
final stacking groups from graded layers and record published-source discrepancies.
Full classifications containing a neutral E8 sector require a justified sector
comparison; the comparison script never deletes a factor to manufacture a match.

The generic resolution and Smith-normal-form infrastructure was adapted from
`main` commit `ac45fa7ed0acd992a2f3a69273762dc9dceb2a97`. No runtime import or filesystem
dependency on that branch remains.
