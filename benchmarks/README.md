# Published insulator comparison data

For active per-case comparisons use the
[rebuilt tables](../results/foundation_review_20261014/README.md) and
[interacting-reference policy](../docs/foundations/interacting_reference_policy.md).
The list below also preserves the first campaign's historical fixtures.
New version-pinned references include `debray_class_a_2102.02941v3.json`,
`mirror_interacting_2105.02682.json`, and the separate 2025 journal table and
named-E8 ledgers. No reference is a solver input.

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
| `point2_rotation_reduction_1809.01636.json` | Liu et al., Table VI class A and Sec VI B | Diagnostic interacting reduction of band-generated phases; excluded from complete-classification comparison columns |
| `point3_full_2204.13558.json` | Zhang et al., Table II | Full physical classification including independent neutral E8 states; requires sector matching |
| `point3_named_e8_quotient_2204.13558.json` | Explicit TI root lists for all 21 improper point groups | Quotient by the named independent neutral E8 root, with per-spin source locations |

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
still has one free summand. This is the source's decoration-coordinate step;
conversion to electron charge per primitive translation cell also needs orbit
multiplicities. In particular, the `pg` subsection identifies its Z with the
charge on one representative of a glide orbit, which has two sites per cell.
The charge and phase layers in the first source
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
statements are stored separately. The [detailed source audit](point2_discrepancy.md)
finds independent primary support for Z_(2N) x Z_(N/2) at even rotation N,
with the same center-state adjoining convention and both spins. It also records
changes between v1, the published supplement, and v2 of the real-space paper.
The evidence supports a missing extension in the printed even-cyclic table;
no author-confirmed explanation was located. The original discrepancy remains
visible alongside the qualified independent-reference check. Do not change a
calculation to fit a printed table.

[arXiv:2204.13558](https://arxiv.org/abs/2204.13558) treats the neutral E8 phase
as an independent two-dimensional root for insulators (introduction and block
state decoration section). Its real-space `E^(2D), E^(1D), E^(0D)` filtration is
also not identical by label to the onsite CI/charge/phase filtration. The current
branch implements the latter tower without an independent E8 sector. Full-group
equality is not an appropriate blanket pass criterion. For orientation-reversing
finite point groups, a missing neutral direction must be identified by a map or
explicit generator before forming a quotient; deleting an arbitrary `Z2` factor
from a published answer is not an implementation of that map.

A further audit identifies the named independent neutral root for all 21
orientation-reversing point groups, for both physical spins. The dedicated
quotient file records each physical generator, order, source root-list line and
source table line. For example, the mirror subsection identifies three roots:
CI decoration, a 2D charge-conserving SPT, and neutral E8 decoration; only the
first two extend to Z8, while the E8 generator is an independent Z2. Its named
quotient is therefore Z8. The comparator reports this quotient check separately
from the full physical group, whose scope mismatch remains visible. This is an
abstract reference-side quotient comparison; it does not claim an implemented
E8 cochain map or identify individual solver roots with real-space generators.
For proper rotations, a solver certificate that H1(G,Z)=0 permits direct
comparison to the full reference group because that neutral decoration is absent.

[The point-group discrepancy audit](point3_discrepancies.md) records the named
physical roots behind D2, S4 and D2d disagreements. In particular, the source's
odd-charge spin-half D2 center root violates its SU(2) double-group convention.
An independent physical site-representation induction audit supplies exact
induced atomic characters for D2 and D2d. Its quotient is conditional on
realizing the orbit rows by allowed inverse-paired creation and adjoining paths.
These audits preserve comparison failures
and do not replace the full source tables with inferred corrections.

Historical cluster3 inspection found
`/home/user/xyren/gap-insulator/pkg/SptSet/debug/exp_3d_point_groups_insulator_ez_diag.log`
to be an incomplete run: it stops during the D2h differential computation with a
fractional inverse diagnostic. The neighboring 2D diagnostic contains useful
historical stacking values, but neither file is an independent mathematical
oracle. They are not imported into these benchmark tables.

## Reproduction

Acquire the primary sources with the arxiv skill, then run:

```bash
python benchmarks/extract_sources.py --cache /home/arxiv
python benchmarks/extract_e8_projection.py
python benchmarks/extract_rotation_control.py
python -m unittest discover -s tests -p 'test_catalog*.py'
```

The source extractor derives tables from their LaTeX boundaries, keeps provenance,
and fails if the 3D table does not contain 64 physical-spin rows. It does not
supply any classified group to the runtime symmetry catalog.

The comparison CLI accepts the runner format `{input, classification, run}`
or an enriched flat result:

```bash
python benchmarks/compare.py runs/CASE/result.json --output runs/CASE/comparison.json
```

It combines finite filtration orders with their separate free ranks. Raw
cohomology is never substituted for final obstruction kernels or incoming
quotients. A missing result stays `not_computed`.

For full uniform-IQH runs, the comparator uses the certified
`relativeUniformIQH0` subresult and labels that comparison scope. It does not
compare the full chiral group to a nonchiral source. A wallpaper filling check
requires `wallpaperFilling` with the primitive translation vectors, cell area,
actual generator periods and their gcd; the subgroup's witness takes precedence
over full-IQH filling data. The computed primitive-cell step is reported with
`requires_source_coordinate_map` until the source's Wyckoff multiplicities are
explicitly matched. No witness is inferred from the abstract free rank, and
the printed Z or 2Z is not directly equated to electrons per primitive cell.
