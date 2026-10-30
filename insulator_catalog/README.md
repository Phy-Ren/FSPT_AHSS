# Crystalline insulator symmetry catalog

The catalog supplies 10 crystallographic planar point groups, 17 wallpaper
groups, 32 three-dimensional crystallographic point groups, and 230 space groups, each with
physical `spinless` and `spin_half` conventions. The 578 inputs contain geometry
and backgrounds only. Nothing under `benchmarks/` is read by the catalog or the
classification solver.

Run `python scripts/build_catalog.py` from the repository root. Generated JSON
and GAP records contain the same data. The GAP form binds `U1_INPUT`; group
indices in both formats start at **zero**, with the identity at index zero.
`omega` contains exact rational strings; GAP consumers should apply `Rat` to
these strings. `dimension` is the spatial dimension. The corresponding spacetime
dimension is `dimension + 1`.
Current records have `schema_version=2`, `s` for antiunitarity, `r` for charge
reversal, and `rho` for the circle action, with `r=rho XOR s`.
The retained `circle_action` metadata is a redundant copy of `rho`.
Both the generated JSON and GAP records use these definitions.
Archived run inputs retain their historical schema and must be converted
explicitly before reuse; see [notation and inputs](../docs/NOTATION_AND_INPUTS.md).
The [migration record](notation_migration.json) verifies all 578 backgrounds
against the previous revision and an independent regeneration of the JSON/GAP pairs.

For wallpaper groups, `multiplication`, `order`, `matrices`, and the three
character tables describe **finite holonomy only**. The classification group is
the full infinite affine group `SpaceGroupBBNWZ(2,catalog_number)`. Its
`affine_generators` retain fractional translations. GAP's recorded affine
matrices use row vectors and the last row for translations. Pull the finite
background back along the actual point homomorphism; computing cohomology of
the finite quotient loses translations, glides, and their extension data.

## Effective onsite convention

These inputs describe initially unitary spatial symmetries preserving electric
charge. Let `w1(g)=(1-det(R_g))/2`. Crystalline equivalence keeps the abstract
circle extension while changing the wavefunction antiunitarity:

- `s1_eff = w1`;
- `rho1_eff = 0`;
- `r1_eff = rho1_eff + s1_eff = w1`.

Thus effective orientation-reversing elements act by charge conjugation in the
onsite description. They are **not** ordinary charge-preserving time reversal,
which would instead have `r1=0, s1=1, rho1=1`. This distinction is required
for charge cohomology of wallpaper groups, including the free filling class in
`H^2(G,Z_w1)`.

The notation conversion follows Wang–Qi–Fang–Cheng–Gu,
[arXiv:2112.15533](https://arxiv.org/abs/2112.15533), equations labeled `rho1`,
`Q`, and `n2symm`: that paper's `rho1` is the circle automorphism, with the
same meaning as current `rho1`; its charge character is `rho1+s1=r1`.
The frozen v0.7 package instead called the charge character `rho1`.
Its translation is documented separately and is not a current alternative convention.
Supplement H of the paper states the
spinless/spin-half exchange under crystalline equivalence.

For the conventional physical spin-half point-group representation, inversion
acts trivially on the spin. The geometric double cover is obtained by lifting
`det(R) R` to Spin(3), as described in
[arXiv:2204.13558, Sec. I A](https://arxiv.org/abs/2204.13558), equation
`w2-proj`. Its characteristic class is `w2(V)+w1(V)^2`. Planar matrices are
embedded as `diag(R,1)` before this construction. With `p(g,h)` the normalized
binary cocycle of those lifts, use the following effective representatives:

| Physical convention | Effective omega in R/Z |
| --- | --- |
| spinless | `p/2` |
| spin-half | `0` |

The latter chooses the representative where the physical double-cover class
and the crystalline shift cancel. It is not a claim that every intermediate
choice of physical section cancels pointwise. Section/lift conversion, when
needed for externally supplied inputs, belongs to the cochain formula engine.

The implementation forms an invariant rational metric, an orthogonal rational
basis, and even lifts in the exact Clifford algebra Cl(0,3). Multiplication of
lifts differs from the selected lift by a nonzero rational scalar. Its sign
provides `p`; unit normalization and floating-point square roots are unnecessary.
For a mirror or pi rotation the chosen lift squares to minus one; inversion
lifts to plus one. All products and every cocycle triple are tested, including
the 48-element cubic point group.

## Geometry provenance

`source/wallpaper_gap_export.txt` records the actual affine generators and
finite point matrices from `SpaceGroupBBNWZ(2,n)`, `n=1..17`.
`source/point3_gap_export.txt` records generators from
`MatGroupZClass(3,representativeITNumber)` for the listed 32 representatives.
The read-only export used GAP 4.13.1 and CrystCat 1.1.10 on cluster3. The
representative IT number selects geometry, never a classification answer.
The export program is preserved as `source/export_geometry.g`.

The 3D representative list and the rational Clifford construction were
independently transcribed from generic geometry in `Phy-Ren/FSPT_AHSS`, main
commit `ac45fa7`, files `gap/point_group_backend.g` and
`gap/crystalline_background.g`. This branch has no runtime dependency on that
checkout and imports no other theory's formulas or classifications.
