# Commuting finite abelian products in 4+1D

The new engine computes the complete original four-data model for
`U(1)^f × G`, where `G=∏ C_Ni` and `s=r=omega=0`. The ordered fields are
`(e2,n2,n4,nu5)`, with one shared phase. The calculation fixes the additional
intrinsic pair `(n0I,n0J)=(0,0)`. No physical reference group is imported by
the solver, and an additive bordism-group match is not a proof of a labelled
physical root dictionary.

The implementation is [abelian4p1.g](../../../gap/abelian4p1.g), using the
existing exact HAP resolution transfers, integer cohomology, local source,
product, and full cylinder-gauge formulas. The runner is
[classify_abelian_4p1.py](../../../scripts/classify_abelian_4p1.py).

## Obstructions and complete roots

In this background the equations reduce to

```math
de_2=dn_2=dn_4=0,\qquad
 d\nu_5=\frac13e_2^3+\frac16n_2^3+
 \frac12\operatorname{Sq}^2(\bar n_4).
```

The charge obstruction is computed on the entire integral group
`H4(G,Z)`, including mixed classes. Its exact integer kernel is retained;
a nonzero obstruction on a basis vector never discards a surviving
combination or multiple. Each kernel generator receives an actual phase
completion, obtained using the resolution-to-bar comparison and its
contracting homotopy.

For factor `C_Ni`, let `ai` be its least nonnegative residue and
`xi=dai/Ni`. The two pulled-back completed sheet roots are

```math
X_i=(x_i,0,0,a_i\cup x_i^2/(3N_i)),\qquad
Y_i=(0,x_i,0,a_i\cup x_i^2/(6N_i)).
```

Their global source equations follow from `dai=Ni xi`, not from a sample
of simplices. The engine independently transfers and checks these
identities on the complete native resolution. It verifies that the
`xi` generate all of `H2(G,Z)` by an integer Smith calculation. Consequently
every sheet class lifts through full stacking of these completed roots;
there is no unexamined sheet-obstruction combination.

The separate phase generators span `H5(G,R/Z)`. Phase coordinates use its
full native cohomology, not restrictions to individual cyclic subgroups.
This distinction retains the mixed phase classes.

## Incoming gauges are necessary

For finite unsigned `G`, `H1(G,Z)=0`, so there are no independent incoming
closed E8 or CI sheet-gauge classes. The degree-three charge gauge group
`H3(G,Z)` can be nonzero. Its incoming map is

```math
\iota:H^3(G,\mathbb Z)\longrightarrow H^5(G,\mathbb R/\mathbb Z),
\qquad [w_3]\longmapsto
\left[\frac12\operatorname{Sq}^2(\bar w_3)\right].
```

This is a fixed homomorphism on gauge classes. To see why it applies to
arbitrary completed states, set the sheet parameters to zero and take
`dw3=0`. The lower endpoint is unchanged. In the full source cylinder,
the E8 and CI cubic terms are pulled back from the base and have zero
interval integral. Only the charge-square term transgresses. Its
cohomology class is the displayed Steenrod operation; the closed base
charge contributes only a coboundary. Equivalently, the standard charge
gauge is `Sq2(w3)/2 + F(n4,dw3)` at `omega=0`, and its second term vanishes.
The adopted cylinder representative is related to this representative by
a phase coboundary, without any change of gauge-equivalence classes.

Additivity does not require checking every integer combination. For
closed binary degree-three cochains `w,z`, the polarization is
`w cup_1 z + z cup_1 w = d(w cup_2 z)`. Hence half the polarization is a
phase coboundary. The Steenrod cochain identity also sends an exact
input to an exact output. Thus the incoming map factors through integral
cohomology, is additive, and has exponent-two image. One representative
per cohomology generator therefore generates every incoming relation.

The implementation nevertheless evaluates the **full cylinder gauge**,
followed by the full inverse/product and phase reduction, at the vacuum
and at every non-phase root. It records all these images instead of
installing the cohomological formula as a shortcut.

For `C2 × C2`, the calculation has pre-incoming order `2048`. Its one
`H3(G,Z)=Z2` generator removes a nonzero phase of order two, giving order
`1024`. The final phase layer is `Z2³`, whereas the raw phase group is
`Z2⁴`. Omitting this incoming relation would produce a wrong final
classification despite correctly computed individual sheet roots.

## Stacking and completeness of the presentation

The charge correction is the actual integer `n2 cup n2'`; all CI and E8
phase twisters are evaluated with the adopted coefficients. For each
finite sheet root, the engine computes its `Ni`-fold stack, applies the
full integer sheet-removing gauge, subtracts completed charge roots, and
removes the remaining exact charge by a full charge gauge. The residual
shared phase supplies the integer relation. Charge-kernel relations are
reduced in the same way. Every residual phase retains its primitive
witness in the native resolution.

The model's class-level associativity, commutativity, inverse, and
product/gauge compatibility are proved in
[the fixed-model coherence argument](../../../formulas/06_equivalence.tex).
Neutral coherence is explicit in
[the E8 runtime](../../../insulator/_engine/e8_4p1.py). These identities,
together with generation of the full successive cohomology layers,
justify an abelian integer presentation; arbitrary triple products do
not introduce an extra unchecked relation. In addition, this campaign
computes every pairwise commutator of non-phase roots and exhibits its
coordinates in the already constructed relation lattice. It does not
add an unexplained commutator relation to force the expected answer.

Before the incoming quotient, the presentation order is checked against

```math
|H^5(G,\mathbb R/\mathbb Z)|\,
|\ker(d_2:H^4(G,\mathbb Z)\to H^6(G,\mathbb R/\mathbb Z))|\,
|H^2(G,\mathbb Z)|^2.
```

The final E8, CI, charge, and phase layers are obtained by integer
elimination from the completed presentation. They are not multiplied to
guess the extension. The source and full mathematical witnesses are
retained per case, including the native differential matrices needed to
check stored primitives independently.

## Independent calibration and intrinsic scope

The [bordism target ledger](BORDISM_TARGETS.md) and its additional batch
references specify the physical comparison separately. The solver's
`physicalClassificationCertified` remains false: a matching additive
group is useful calibration, while a universal physical-spectrum
identification and a labelled root-character comparison require more.

For any of these direct products, a symmetry-independent physical
intrinsic root can be given trivial `G` action. Forgetting `G` composed
with this section is the identity. Therefore the **physical** full
classification splits as its relative kernel plus `Z{I} ⊕ Z{J}`. This is
a natural-section statement independent of the cochain campaign, not an
implementation of an unrestricted intrinsic-row solver.

## Native charge-class accelerator

The optional `--charge-primary native` path uses the existing contracted
higher diagonal to compute only the class
`[Sq2(n4 mod 2)/2]` in the signed phase cohomology. It validates the exact
trivial background, the integral native cocycle, and the identity of the
target cohomology object before evaluating the operation. The
`--charge-primary compare` path also computes the full bar source class
and requires equality on every integral cohomology generator.

Neither path returns a phase primitive. All subsequent charge and sheet
completions, root powers, cylinder gauges, incoming images, commutators,
and residual primitives still use the full cochain formulas. Full runs
for `C2²` and `C2³` have identical mathematical fields and witnesses in
native and compare modes. The `C2³` comparison includes a nonzero charge
obstruction map. The default remains `bar`; measured end-to-end speed,
not the isolated primary operation, determines whether the optional path
is useful for a subsequent campaign.

## Reproduction

```bash
python scripts/classify_abelian_4p1.py \
  --factors 2x2 --factors 2x4 --factors 3x3 \
  --jobs 3 --timeout 1800 --memory 16g --output NEW_DIRECTORY
```

Use an immutable source snapshot and an idle compute node for campaigns.
The runner never overwrites an existing output directory. A failed or
timed-out case retains its logs and run metadata and cannot be presented
as complete. It records the formula-runtime artifact hash as well as the
source and input hashes. The bounded end-to-end tests independently
reduce the presentation with SymPy and reconstruct all commutator,
sheet-removal, and residual-phase primitive witnesses for `C2 × C2`.
