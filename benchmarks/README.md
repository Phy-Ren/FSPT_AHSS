# Published insulator comparison data

These files are comparison references, never solver inputs. They are extracted
from cached primary-source LaTeX by `extract_sources.py`. Each file records the
source URL, exact file SHA-256, table location, source row or cells, and whether
it describes graded layers or a stacking group. Zero in a factor list denotes
a free integer summand. Factors are direct cyclic factors, not necessarily
invariant-factor order.

| File | Source content | Permitted comparison |
| --- | --- | --- |
| `wallpaper_layers_2112.15533.json` | Wang et al., Supplement H, both wallpaper tables | Charge layer and bosonic layer after incoming identifications, with uniform IQH `n0=0` |
| `wallpaper_stacking_2012.15657.json` | Zhang et al., Table III | Full stacking of the nonchiral wallpaper SPT sector, with uniform IQH `n0=0` |
| `point2_stacking_2012.15657.json` | Zhang et al., supplemental Table `point` | Published point-group statements, subject to the discrepancy below |
| `point3_full_2204.13558.json` | Zhang et al., Table II | Full physical classification including independent neutral E8 states; requires sector matching |

The first source labels **onsite** spin, and says explicitly to exchange that
label when interpreting the symmetry as spatial. Our JSON uses the resulting
physical crystalline labels: its first table, onsite omega zero, is physical
spin-half; its second table is physical spinless. The real-space sources already
use physical spin labels. Historical code comments occasionally use onsite
`EZ/s12` and physical `spinless/spinful` interchangeably; those comments are not
accepted as convention definitions.

The 2D comparisons keep the uniform IQH index fixed to zero. They do not remove
the free wallpaper filling class. Where the real-space table prints `2Z`, the
JSON retains that physical charge step separately; its abstract additive group
still has one free summand. The charge and phase layers in the first source
must not be concatenated to infer a final stacking group: nontrivial extensions
are precisely what the twister calculation must recover.

## Source discrepancies and scope

Supplemental Table `point` of
[arXiv:2012.15657](https://arxiv.org/abs/2012.15657) prints
`C_(2m) -> Z_(2m) x Z_(2m)` for both spins. In particular it prints `Z2 x Z2`
for planar `C2`. The onsite `U(1)^f x C2` example of
[arXiv:2112.15533](https://arxiv.org/abs/2112.15533), main text following the
classification equations, instead explicitly gives `Z4`. The supplied v0.7
formula package also uses the latter as a complete-root calibration. These
statements are stored separately. The present source audit has not reconciled
the point-group table with the onsite root relation; do not change a calculation
to fit one table, and do not report this row as a verified agreement.

[arXiv:2204.13558](https://arxiv.org/abs/2204.13558) treats the neutral E8 phase
as an independent two-dimensional root for insulators (introduction and block
state decoration section). Its real-space `E^(2D), E^(1D), E^(0D)` filtration is
also not identical by label to the onsite CI/charge/phase filtration. The current
branch implements the latter tower without an independent E8 sector. Full-group
equality is not an appropriate blanket pass criterion. For orientation-reversing
finite point groups, a missing neutral direction must be identified by a map or
explicit generator before forming a quotient; deleting an arbitrary `Z2` factor
from a published answer is not an implementation of that map.

Historical cluster3 inspection found
`/home/user/xyren/gap-insulator/pkg/SptSet/debug/exp_3d_point_groups_insulator_ez_diag.log`
to be an incomplete run: it stops during the D2h differential computation with a
fractional inverse diagnostic. The neighboring 2D diagnostic contains useful
historical stacking values, but neither file is an independent mathematical
oracle. They are not imported into these benchmark tables.

## Reproduction

Acquire the three primary sources with the arxiv skill, then run:

```bash
python benchmarks/extract_sources.py --cache /home/arxiv
python -m unittest discover -s tests -p 'test_catalog*.py'
```

The source extractor derives tables from their LaTeX boundaries, keeps provenance,
and fails if the 3D table does not contain 64 physical-spin rows. It does not
supply any classified group to the runtime symmetry catalog.
