# Computed U(1)^f insulator examples

The current catalogue contains **596 distinct backgrounds** and **664 response-sector entries in 16 tables**. Each calculation fixes the symmetry group, physical spin, extension data, and response sector. Dimensions and physical spins have separate result files.

| Collection | Backgrounds | Response-sector entries |
| --- | ---: | ---: |
| [2+1D planar point groups](2p1d/README.md) | 20 | 40 |
| [2+1D wallpaper groups](2p1d/README.md) | 34 | 68 |
| [3+1D crystallographic point groups](3p1d/README.md) | 64 | 64 |
| [3+1D space groups](3p1d/README.md) | 460 | 460 |
| [4+1D internal groups](4p1d/README.md) | 18 | 32 |

The 2+1D collections keep `n0=0` and all allowed `n0` in separate files, both with `e0=0`. The 3+1D collections include E8 in the completed four-data calculation. The 4+1D cyclic examples retain the coupled E8 and shared-phase root relations.

## Reading the tables

Each row records the final filtration in the order `(e_p,n_p,n_{p+2},nu_{p+3})`, followed by the **final stacking group**, with `p=d-2` in spatial dimension `d`. Filtration layers already include incoming identifications; multiplying their groups does not determine the stacking extensions. Wallpaper and space groups use the full infinite affine groups.

Every interacting reference source and version has its own cited column. **✓** marks the same reported group; **×** marks a different reported group. `UNVERIFIED` means no verified comparison is available; `N/A` means the source does not apply. Layer comparisons are labeled separately from full stacking comparisons. In particular, the space-group Song–Xiong–Huang column compares the neutral E8 layer only.

The results are complete calculations of the selected four-data model. Its universal identification with the full physical CI kernel remains conditional. [Calculation provenance and scope](PROVENANCE.md) explains acceptance and reference domains.

[Formula guide](../../docs/FORMULA_GUIDE.md) · [Machine-readable example index](index.json) · [Reference source ledger](../../docs/reference_ledger_20261014.md).
