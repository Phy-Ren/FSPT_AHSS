# Comparison protocol and sector audit, 2026-10-14

The stored groups classify the supplied CI/charge/phase model. An abstract
agreement with a published group is a comparison result, not a proof that
every physical phase, equivalence, or response has been included. This note
separates exact computational statements from the remaining physical maps.
It does not change the runtime or the frozen 2026-10-13 reports.

## What the calculation and comparator actually do

The finite-group inputs specify multiplication, the independent characters
`s` and `rho`, and a real lift of the U(1) extension. Wallpaper calculations
use the full infinite affine group, not only its finite point quotient.
The crystalline catalogs have effective `s=rho=w1`, so the circle action
`s+rho` is zero. Their physical spin labels include the declared geometric
extension shift; equality of abstract groups does not validate that dictionary.

For spatial dimension d, the backend starts from integer charge cohomology
H^d(G,Z_rho), phase cohomology H^(d+1)(G,R/Z_s), and the retained CI row
H^(d-2)(G,Z_s). It computes the actual charge obstruction kernel, constructs
charge and phase completions, tests the CI integer obstruction, and tests the
CI phase obstruction modulo every allowed closed-charge adjustment. A nonzero
exact source is completed rather than rejected.

The presentation then includes the phase orders, complete charge-root powers,
complete CI-root powers, and incoming charge/CI gauges with their phase
coordinates. Smith normal form determines stacking. Integer elimination gives
the final phase, charge, and sheet filtration subquotients. Consequently raw
`phaseOrders` and `chargeOrders` are not classification answers, and the
graded pieces must not be multiplied to guess the stacking group.

`benchmarks/compare.py` reads reference data only after classification. For
2D full runs it deliberately selects `relativeUniformIQH0`. It compares final
wallpaper charge and phase quotients with the corresponding layer reference,
and the full relative stacking presentation with the stacking reference.
For free wallpaper charge, the solver supplies an actual primitive-cell
period. The comparator currently retains `requires_source_coordinate_map`:
the reference's displayed Z or 2Z is not identified with this physical period
without a Wyckoff-coordinate map. In particular, pg has abstract free group Z
and physical primitive-cell charge step two.

## Three distinct two-dimensional objects

Write A for the full group of the **supplied model**, and pi for its invariant
uniform CI coordinate. The source uses

```
pi : A -> H^0(G,Z_s),       pi(n0,n2,nu3)=n0,
A0 = ker(pi),              I = image(pi).
```

1. **n0=0:** A0 is a stacking subgroup with a vacuum and inverses. It is the
   object used in the relative literature comparisons.
2. **A fixed allowed n0=k != 0:** pi^-1(k) is an A0-torsor, or coset. Choosing
   one completed state identifies its elements with A0 as a set, but there is
   no distinguished origin. Stacking two states in this fiber lands in the
   2k fiber. It is not a stacking group. A k outside I gives an empty fiber.
3. **All allowed n0 together:** A fits into the exact sequence
   `0 -> A0 -> A -> I -> 0`. The full column of a results table refers to A,
   not to any single nonzero fiber.

The term "relative" here means the zero-coordinate subgroup. It is not the
operation of quotienting A by an unspecified IQH state. If I=mZ is nonzero,
the extension splits as an abstract abelian group because mZ is free. A
completed lift of m gives a splitting, and changing that lift by a state in
A0 changes the splitting. The abstract extra Z therefore does not identify
a canonical pure-IQH generator, its charge decoration, or its response map.
Physical product calibration still matters even when this abstract group
extension necessarily splits.

The audit [tables and witnesses](../results/calibration_20261014/two_dimensional_sectors.md)
reads all 54 independent relative runs and all 54 full runs from the immutable
archive. In every pair:

- The relative generator cochains are literally identical.
- Integer Hermite normal form gives identical relative relation lattices.
- Every full relation has zero coefficient on the possible CI generator.
- Independent Smith normal form reproduces both reported groups.

There is at most one CI generator, with nonzero integral pi. Thus the span of
the charge and phase generators is precisely ker(pi), with exactly the
relations returned by `relativeUniformIQH0`. This proves a kernel statement
inside the computed presentation, not merely an equality of group orders.

Twenty cases, the five rotation point groups and five orientation-preserving
wallpaper groups with both spin labels, have an actual completed n0=1 state.
Their image I is Z. The remaining 34 cases have s nontrivial, H^0(G,Z_s)=0,
and no nonzero uniform CI sector. All ten wallpaper CI lifts chosen by the
solver have zero additional primitive-cell charge; this is a property of
those choices, not a canonical identification of IQH with a zero-charge lift.

## Physical normalization of the 2D calculation

The authoritative v0.7 note distinguishes these issues explicitly.
`note/sections/03_two_dimensional.tex`, first paragraph and Eq. `2d-product`,
give an explicit consistent nonzero-IQH product while leaving its universal
identification with a specified physical P-move convention open.
`11_reproducibility.tex`, scope table, repeats that qualification. Testing
local identities, constructing completions, or observing A0 plus Z does not
finish that physical comparison. The new tables label these rows **I**;
rows with only the relative construction are labeled **R**.

The same note's `01_symmetry.tex`, Eq. `neutral-coefficient`, specifies two
independent symmetry-free 2D response coordinates:

```
(n0,e0) in Z^2,       sigma_xy = n0,       c_minus = n0 + 8 e0.
```

The present runtime retains n0 and sets aside the independent neutral E8
coordinate e0. A physical relative 2D SPT comparison sets both n0=0 and e0=0.
Setting n0=0 alone only sets electric Hall response to zero; a separately
added E8 phase would still have thermal response. Conversely c_minus=0 alone
does not force n0=0: the pair (8,-1) in the stated normalization is an example.
There is no E8 source, product, or gauge implementation in this runtime.
Its omission must not be interpreted as assigning those operations zero.

## What the 3D E8 comparison can and cannot establish

The frozen `neutralE8AbsentByCohomology` field tests only whether
H^1(G,Z_s) is zero. Its name must be read literally as a statement about that
leading decoration group. By itself it does not examine incoming operations
or establish the full physical spectrum.

There is a useful additional argument in this specific 3D setting, with
explicit hypotheses. Assume the usual full invertible-phase AHSS with the
neutral E8 coefficient row and its natural physical interpretation. The
potential E8 incoming source for total degree three is H^0(G,Z_s), in total
degree two. Its relevant outgoing operations have the degrees of a d3 into
charge H^3(G,Z_rho), then a d4 into phase H^4(G,R/Z_s), interpreted in the
successive quotients. For nontrivial s that source is zero. For s=0, a neutral
E8 layer with trivial internal G_f action, stacked with a trivial electronic
vacuum, is a genuine symmetric 2D phase for any extension. Pullback of this
phase gives a lift of the H^0 E8 generator to the full degree-two theory.
It is therefore a permanent cycle, so these outgoing differentials vanish
in their proper successive quotients. This excludes an additional incoming
E8 differential of this kind under those hypotheses; it is stronger than the
stored H^1 test, and is a physical/naturality argument rather than a runtime
calculation of an omitted operation.

This argument does not identify the nonzero H^1 E8 sector for improper
groups, compute its mixed extensions, prove an E8 direct product, or extend
automatically to 4D. It also does not certify that every other physical
response coefficient has been included.

Suppose a reference presentation really specifies a physical group F and a
named independent neutral subgroup E generated by an E8 root. The arithmetic
quotient F/E is then well defined within that source presentation. Removing
a factor of two merely because it improves a match is not a substitute for
identifying E. Even after the source identifies it, comparing A with F/E
still requires a model-to-physical map j and the composite

```
A --j--> F --q--> F/E.
```

To claim equality, qj must be an isomorphism. Its kernel tests whether a
retained-model state becomes trivial or lands in the physical E8 subgroup;
surjectivity tests whether the retained model covers every class modulo E8.
An independent E8 coefficient at a point does not by itself establish that
its decorated/gauged image has zero intersection with the other sector.
Equal invariant factors, and even a source-side direct-product root list,
do not supply j. Existing `stacking_mod_named_neutral_E8` matches are therefore
abstract quotient controls with their recorded map limitation.

## Calibration steps required for stronger claims

Keep a reference-version ledger: journal and preprint tables must be checked
independently, including named roots and extensions. Preserve existing
results while issuing a new comparison report for a changed source version.
For each comparison, record physical symmetry, spin convention, coefficient
actions, extension class, uniform electric and thermal responses, and which
group or fiber is being compared.

For nonzero 2D IQH, construct the physical product/coordinate bridge with its
lower charge and phase shifts, and test it on completed roots and incoming
gauges. For 3D E8 quotients, construct the actual map on named generators and
relations; check kernel, image, and mixed extensions rather than only Smith
orders. For wallpaper free charge, complete the source-to-primitive-cell
coordinate map. Source arithmetic inconsistencies, model discrepancies, and
missing comparison maps should remain separate statuses until those checks
resolve them.

The authoritative input is `U1f_AHSS_Consolidated_v0_7_complete.zip`, SHA256
`a1410f854828f012dc9be56cfd62dc0eb4a195779c09eed273e6a70f2ca97a4a`.
The new sector audit records hashes of the frozen archive, full results and
its reproduction script. No original campaign output is modified.
