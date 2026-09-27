# Exact native cup-zero evaluation

`gap/background_native_cup.g` exports
`AFSBackgroundNativeCup0(ctx,p,a,q,b)` for native cochains with trivial
F2 coefficients. The module itself does not replace any existing global
function. The frozen v1 and v2 sources remain unchanged. The v3 spinless
source `73e7bae9` enables this evaluator by default through the
`background_operations.g` dispatcher; setting
`AFS_USE_BACKGROUND_NATIVE_CUP=false` disables that dispatch. The control
results below retain their original frozen source and measured values.

The implementation uses `AFSDiagonalRightComponent(ctx,p,q,i)` from the
existing backend. A component term has the form
`[left_basis,left_group,right_basis]`: the right group label has already
been quotiented out. The final F2 pairing is therefore
`a[left_basis]*b[right_basis]`; the remaining left label acts trivially.
Pairs occurring an even number of times cancel. The resulting complete
bilinear forms are cached separately in `ctx.backgroundCup0PairCache`.
The existing component cache is shared with the projected cup-one
calculation, including its frequently used `(p,q)=(2,3)` marginal.

This computes the same native D0 as `AFSNativeCupIFull`, not merely a
homotopic diagonal. In the tensor contraction, an output with positive
left degree receives only the contraction of the left factor. Quotienting
the right group label commutes with that contraction and with the
equivariant boundary sum. Induction on the left degree proves equality
with the right-coinvariant component of the full recursion. At left
degree zero, both use the existing augmented map `T=h T d`, followed by
augmentation of the remaining right group label. The full implementation's
cap cannot remove a term contributing to the requested `(p,q)` component:
the cap is at least both p and q, and contractions only increase degrees.
Finally forgetting the left label commutes with pairing with a trivial
F2 cochain. No cocycle assumption is needed for this equality.

The function is not an integral or signed-coefficient cup product. A
binary result divided by two may subsequently be interpreted in U1_s;
the signed target differential and cohomology coordinates must still be
used. Equality with an independently constructed bar cup is asserted
only in cohomology, not as an equality of native vectors.

`tests/test_background_native_cup.g` compares the entire bilinear pair
form on every native cell against the full tensor implementation. This
proves equality for all cochain pairs in each tested bidegree, beyond the
included arbitrary signed-integer test vectors. It separately compares
actual omega-times-cohomology-generator vectors, and checks their F2
and signed U1 cohomology classes against the bar cup.

The first controls use SG3, 6 and 16 in eight bidegrees, and SG219 in
bidegree `(2,3)`. They run in the immutable snapshot
`runs/background_native_cup_v1_source`. All four controls passed. SG3, SG6 and SG16 each cover eight bidegrees;
SG219 covers `(2,3)`. Together they check complete bilinear-form equality
in 25 group/bidegree cases and 63 background products against both F2
and signed U1 bar-cohomology coordinates. In SG219 the projected
construction took 59.487 CPU seconds and the old full construction
468.371 CPU seconds; the complete control took 1020.639 wall seconds. Source, output and log hashes are recorded in
`docs/validation_runs/background_native_cup.json`. Within each control the projected
calculation runs first and the full calculation follows on the same
context, sharing contraction caches; these timings must not be described
as two independent cold-start benchmarks or as a full-campaign speedup.
