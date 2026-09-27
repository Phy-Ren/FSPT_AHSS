# What a stacking result certifies

`gap/stacking.g` uses the delivered manuscript **CA** phase coordinate. Its
three-layer states are actual lazy bar cochains `(a2,c3,nu4)` on the full affine
group. Native HAP cochains are only the finite linear-algebra model. Primitive
solutions include the chain-comparison homotopy correction, so projecting a
cochain and lifting its coordinates is never assumed to be the identity.

For the general three-layer calculation, the engine stores one full flat lift
for every final complex-fermion and Majorana generator and uses that same lift
for its power relation. The reduction
uses the common marked lower basis, incoming-differential boundary states, and
ordinary cochain gauges. It retains integral lower coordinates until forming
one joint presentation. Smith reduction is performed on that joint matrix;
the orders of generators considered individually are insufficient.

Bosonic order relations already follow from the final cohomology quotient's
Smith presentation. They do not need to be remeasured through the nonlinear
stacking engine. When the bosonic layer is the only nonzero lower layer, this
quotient itself is the complete lower group.

When the Majorana layer is zero, a native Gu–Wen calculation computes the CF
power relations without expanding high-dimensional bar comparisons. For a
native binary cocycle c3, solve

    delta_s nu4 = (c3 cup1 c3)/2.

The marked doubled phase class is

    2 nu4 + (ordinary integral Bockstein(c3) mod2)/2.

The ordinary Bockstein represents Sq1(c3), so this is exactly the diagonal
CF correction. A full marked bar lift is reconstructible: lift the native nu
by the chain comparison, solve the binary equation
`delta h4 = 2[O5(c_bar)-delta_s(nu_bar)]`, then use `nu_bar+h4/2`.
The correction disappears pointwise under doubling. Replacing the bar Sq1
representative by the ordinary Bockstein changes the doubled phase only by
an exact half-integral gauge. This shortcut is restricted to the case with no
Majorana generators; its chosen CF lifts therefore cannot inconsistently alter
later Majorana relation coordinates. The export identifies these as native
Gu–Wen witnesses and records their exact primitive, residual, doubled phase,
and bosonic coordinates, rather than claiming stored full bar witnesses.

The comparison-support flatness checks are available under `AFS_STACK_AUDIT`.
Production relies on the exact primitive equations and the separately tested
comparison-homotopy and universal cochain identities; repeated expansion of
those same identities is not part of the per-group calculation.

The exact phase of a pure complex-fermion gauge beta2 is

    Q4(beta) = (beta cup beta + beta cup1 delta beta)/2.

For a closed degree-one Majorana gauge a1, the incoming boundary is
`(0, P(a1), O4(a1,0))`. If `delta c2=P(a1)`, the ordered product of this
boundary with the pure-complex boundary differs from `O4(a1,c2)` by

    delta_s [(c2 cup1 c2 + c2 cup2 delta c2)/2].

This top gauge is kept explicitly; an incoming image rank alone would not
suffice to compare representatives.

## A p+ip torsion square modulo the bosonic layer

For the physical spin-half problem, omega_eff=0 and the coefficient sign is
the orientation character s. The torsion class of H1(G,Z_s) has representative
`n=c_s=(1-(-1)^s)/2`, whose binary reduction is s. Write B for its degree-two
Majorana defining cochain, so `delta B=s^3`.

The calibrated reference product has diagonal second-layer correction

    alpha(s,s)=s cup s + s cup (s cup1 s)=0.

Its third-layer correction reduces, modulo cochains depending only on s, to

    K = S1(B) + s cup B,
    S1(B) = B cup1 B + B cup2 delta B.

Here S1 is the operation on an arbitrary cochain, including its differential
term. The identity `delta K=Sq1(s^3)+s^4=0` is essential. Omitting the second
term in S1 would be incorrect. The explicit unary coordinate dictionary
between the supplied p+ip source and the reference secondary source is
independently derived in `tests/derive_pip_coordinate.py`; on the diagonal the
remaining change is a multiple of s^3.

Removing the exact integer cochain `2c_s` uses a constant integer zero-cochain.
Its second-layer curvature is zero at omega=0. Its third component depends
only on s, hence is a normalized degree-three cochain pulled back from C2,
and is again a multiple of s^3. This is an incoming Majorana boundary because
`P(s)=s^3`. Consequently the final CF coordinate of the torsion square is the
class of K, independent of those choices. Its bosonic coordinate is not
determined by this argument.

The implementation requires that all primary Majorana cycles survive before
using an unfinished p+ip top lift in this argument. Otherwise a nonpermanent
Majorana adjustment could affect the proposed relation and the engine keeps
the result unresolved. No p+ip phase witness is claimed by this quotient
calculation.

The mathematical product reference is `fermionAHSS` revision
`c2961a2d6ee9465a7b634a31b6c095e607972966`, especially
`python/stacking_model/v1_pair_shared.py` and `off_shell_beta.py`.
Those files are mathematical references; this engine neither imports them
nor reads a space-group answer table.

## When the missing bosonic carry cannot affect the answer

Let H be the already measured lower stacking group and F its bosonic subgroup.
For a torsion p+ip quotient Z2, abelian extensions are classified by

    Ext1_Z(Z2,H) = H/2H.

The CF calculation fixes an affine family `z + image(F)` in H/2H. It does not
select zero for an unknown bosonic carry. The code maps both z and every
bosonic generator through the lower presentation's Smith column transform.

There is an efficient exact classification of this affine family. For a
nonzero element in H/2H, let h be the largest 2-adic cyclic height on which it
has a nonzero coordinate. The corresponding extension doubles one cyclic
factor at height h. Smaller-height components can be removed by a change of
generators. A nonzero free coordinate has the separate free-height case;
the zero class gives the split extension. Odd torsion contributes no Ext
coordinate.

For each possible height, affine F2 equations decide whether higher
coordinates can vanish while a coordinate at that height remains nonzero.
This determines all possible abstract groups with no enumeration of physical
phases or of extension classes. The calculation is checked against direct
integer Smith presentations under independent changes of basis in
`tests/test_extension_algebra.g`.

If every compatible extension has the same invariant factors, those factors
are a complete **abstract-group** result. The export records
`upperCompletion="abstract-group-independent-of-every-bosonic-carry"` and
`fullUpperPhaseWitness=false`. If possible groups differ, it preserves the
entire list and reports the upper extension as unresolved.

Free p+ip quotient factors split abstractly because Ext1_Z(Z^r,H)=0. This does
not assert that a particular geometric weak generator is a primitive cochain
representative or that the splitting is canonical.

## Persisted data

`AFSStackExport` saves integer matrices, Smith transformations, native seeds
for cochain lifts, native ordinary gauges, incoming-boundary coordinates, and
the reconstruction method. Rational cochains are pairs `[numerator,denominator]`.
The full lazy bar functions remain in memory; persisted native seeds alone are
not mislabeled as full bar-cochain witnesses. Replay must use the recorded
formula version and comparison-homotopy construction.

## Full marked p+ip square

`gap/pip_stacking.g` completes the torsion generator's actual phase and power
relation. It first evaluates the full normalized O5 on the defining tower kept
by classification. It solves the full incoming image, including any
nonpermanent Majorana secondary classes. A Majorana adjustment changes B, after
which the CF primitive and full O5 are recomputed. A final CF adjustment then
removes the remaining raw obstruction. The phase primitive uses the same
comparison homotopy as the lower lifts.

The diagonal product uses a universal local formula derived from the calibrated
reference product. Its inputs have n=s and omega=0. A legal four-simplex has
four sign bits, six independent Majorana cone-face bits, and four independent
CF cone-face bits. The derivation evaluates all 16,384 such inputs with exact
rational arithmetic; it never enumerates elements of a space-group FSPT
classification. The resulting 579-term multilinear polynomial over Z/16
reconstructs all entries exactly. Runtime uses a packed 14-bit lookup of this
universal cochain formula, without importing the reference checkout. The exact
CF correction `beta_ref=S1(B)+sB+s^3` is also independently checked on all
1,024 restrictions used in those derivations.

Write K=S1(B)+sB. Let T1 denote the exact unary phase-coordinate change from the
normalized input to the reference input, T2 the corresponding change on the
doubled output (2s,0,K), and g the canonical integer-layer gauge that removes
2s. The actual square is the lower state

    Majorana = 0,
    CF = K+s^3,
    phase = 2 nu + 2 T1 + Gamma_ref - T2 + g.

The gauge changes CF by s^3; it is retained rather than silently discarded.
Reduction through the same marked lower generators keeps its incoming MC1
boundary phase and every induced CF cross-term. One joint integer presentation
then contains all lower relations and this measured p+ip relation. The export
retains the upper generator's native defining tower, every phase-coordinate
shift, the integer gauge, the lower reduction gauges, and the joint Smith
transformations. `fullUpperPhaseWitness=true` is used only for this actual
cochain relation; the earlier affine-family calculation keeps its weaker flag.

For a pure-CF marked lift obtained by the backend primitive solver, the
comparison correction is a half-integral cochain. It therefore vanishes
pointwise modulo one when doubled. The engine can evaluate its exact square as
`2 Bar(native_primitive) + (c cup2 c)/2`, without expanding the degree-five
homotopy. This preserves the chosen marked lift and applies even when
Majorana generators are present in the same joint presentation.

## Replaying marked-generator stacking

The persisted integer presentation can be used without GAP:

```sh
python3 scripts/stack_result.py runs/full_v01/sg11.json \
  --left '{"C1":1}' --right '{"C1":1}'
```

`PresentedStackingGroup` maps marked integer combinations through the saved
Smith column transformation and reduces cyclic coordinates. It retains free
coordinates as integers, accepts negative powers, and reports actual phase
orders. The additional `stacked_marked` output reduces higher layers first,
applying every saved lower carry, so `C1+C1` is displayed directly as `D1`. For SG11 both C1 and C2 have order4, but their doubles are the same
D1; the resulting lower group is Z2×Z4. This is a direct replay of the joint
relations, not an inference from separate generator orders. In initial result
files, Pfree1, Pfree2, ... refer to the noncanonical abstract splitting already
certified by the free-quotient argument. Files containing
`pip.free_lattice.fullFreePhaseWitness=true` instead bind those names to their
explicit primitive surviving lattice vectors and complete flat towers. The
CLI reports this scope and the actual integer H1 coordinates. For example,
SG2 requires the lattice `2I3`, so one marked free generator has twice the
corresponding primitive unconstrained H1 character. The optional construction
is documented in `docs/FREE_PIP_LATTICE.md`. An abstract-only torsion upper
extension result is rejected by this marked-generator interface.

Validation includes actual infinite-SG native/full-bar comparisons for SG2,
11, 15, and87. Their entire joint presentations agree, including the Z8 factor
and bosonic Z4 subgroup in SG87. The shortcut for twice the same pure-CF lift
is also compared directly, pointwise on all native comparison-support faces,
against the literal cochain product in SG11 with its nonzero bosonic carry.

## Universal C4 pullback lift

For an orientation character that lifts to an actual homomorphism G→C4, an
independently solved universal flat tower gives an efficient marked p+ip lift.
The character is derived from native degree-one cochains, without a list of
space-group numbers: solve `delta u = delta(s_native)/2 mod2`, then
`t_native=s_native+2u` is closed modulo4. Its ordinary bar lift defines the
global C4 homomorphism. Reduction modulo2 equals s pointwise because
untwisted degree-one coboundaries vanish.

On C4 choose n(t)=t mod2 and B(g,h)=(g mod2) floor(h/2). An independently
computed normalized 27-entry CF cochain and 81-entry rational phase cochain
complete the tower. The derivation verifies all256 CF equations, all4096
top-obstruction closure equations, and all1024 phase primitive equations,
including degenerate bar tuples. No fixed phase denominator is assumed in
the Smith solve; this particular solution has denominators dividing16.

Pullback produces full cochains on the infinite affine group. Classification
and all lower generators still use that full group. The export records the
actual native character, its integer differential divisible by4, the universal
flat-tower version, and that this upper lift may differ from classification's
initial primitive choices. Direct SG7 checks verify the character equations
and the complete pulled-back tower on every comparison-support face.

A same-context SG112 check constructs both the C4 lift and the generic full
phase-primitive lift while retaining one classification object and one marked
lower basis. Their measured square coordinates agree exactly:
`[0,1,0,0,0,1,0,1,1,0]`. The lower group has exponent two, so changing the upper
lift cannot change its square; this test checks that requirement at the level
of the actual joint relation, including the nonzero bosonic carry. Comparing
named coordinates from different Smith bases would not test this property.
The reproducible check is `tests/test_pip_lift_choice.g` with `AFS_TEST_SG=112`.
