# Majorana lift performance: follow-up after the current delivery

This note records a read-only code review. No runtime file was changed and
no numerical task or benchmark was started for these suggestions. The current
v07, v08 and v09 candidates do not use the optimizations described below.
Complete and deliver those existing candidates first; this note is not a
proposal to start another full campaign before measuring a specific change.

The long `stack_lift_B1` stage covers several operations, including the
degree-four F2 solve, evaluation of the degree-five phase obstruction and
its U1 solve. A stage-level elapsed time does not identify which operation
dominates. High CPU use and moderate RSS do not resolve that distinction.

## Priority 1: use the known defining coboundary inside the MC obstruction

In `gap/stacking.g`, `AFSStackLiftMC` constructs

\[
q=\operatorname{majorana\_source}(a),\qquad
c=\operatorname{AFSSolve}(4,\mathbb F_2,q),\qquad \delta c=q.
\]

The source callback remains available, but the subsequent `AFSFormula`
call receives only `a` and `c`. In the current compiled `obstruction_2_w`
program, `delta(c)` is reconstructed from alternating sums of five
degree-three face values and then reduced modulo two. The compiler already
shares common subexpressions, so this should not be described as five new
uncached evaluations on every occurrence.

For the current omega-zero CA coordinate, the supplied formula is

\[
O_5(a,c)=\frac12\bigl(c\smile_1c+c\smile_2\delta c\bigr)
          +\gamma(a)\quad\text{in }\mathbb R/\mathbb Z_s.
\]

On this actual defining tower it can be evaluated as

\[
O_5(a,c)=\frac12\bigl(c\smile_1c+c\smile_2q\bigr)
          +\gamma(a).
\]

This is equality of the cochain values at every normalized bar simplex,
not only equality of cohomology classes. `AFSSolve` includes the comparison
homotopy correction, so its successful F2 primitive satisfies the actual
bar equation. When the CF indeterminacy adjustment adds a closed H3
representative to `c`, the same equation `delta(c)=q` remains valid.
Consequently the canonical native phase solve and the marked phase can
remain exactly the same if their source values are unchanged.

The substitution must be restricted to the **binary** differential node of
this particular `c`. It must not replace the integer differential of a
canonical lift by a mod-two source, discard Bockstein terms, or simplify
the integer carries in `gamma(a)`. An arbitrary off-shell `c` does not have
this defining equation. The general obstruction evaluator should remain
available for such inputs and for independent comparisons.

Relevant locations are `AFSStackLiftMC` in `gap/stacking.g` (source creation,
CF adjustment and phase lift), `square` and `obstruction` in
`fspt/formulas.py`, and the `obstruction_2_w` program in
`gap/formula_fast.g`. The generic evaluator's differential-face loop is in
`gap/formulas.g`.

Suggested minimum controls for a later implementation:

- Compare the specialized obstruction against the unchanged general formula
  on legal local towers with `delta(c)=q`, including degenerate simplices;
  include an off-shell negative fixture where substituting an unrelated
  source must be rejected or must not be dispatched.
- In one fixed classification object, compare complete native obstruction
  vectors, native phase seeds and actual marked phase values with the
  general path. Include a nonzero Majorana source and a case with a nonzero
  closed CF adjustment.
- Check the actual bar equations and at least one complete generator
  relation. Equality of final invariant factors alone is insufficient to
  establish equality of the marked lift.

This is the most local candidate: it avoids some costly `c` evaluations
without changing the comparison-map backend. It still needs direct `c`
values for the cup products. Its net runtime benefit is unmeasured; a new
formula arrangement can lose some existing common-subexpression sharing.

## Priority 2: skip zero contributions in the existing F2 homotopy evaluator

`AFSHomotopyPullback` in `gap/backend_bar.g` already evaluates the scalar
pullback without materializing the complete bar homotopy chain. It still
uses the integer `AFSChainFromBar` and `AFSChainToBar` caches. Its scalar sum
has terms of the form

\[
(-1)^j w_1t_1\,
f(\text{prefix},w_3,\text{bar tuple}),
\]

and the F2 branch reduces the sum only at the end. For an F2-valued source,
a term with even `w_1` or even `t_1` vanishes. The smallest candidate change
is therefore to skip an even `w_1` before accessing its F image and skip an
even `t_1` before invoking the source callback. The existing integer G/F
caches can remain in use.

This deletes zero summands from the same exact formula. With the same
native primitive `b`,

\[
c=G^*b-h^*f
\]

is unchanged pointwise in F2. This argument does not replace a cochain by
a cohomologous representative. It also does not remove the cost of building
the integer G/F words themselves.

Dispatch must be restricted to `coeff="F2"`. A general MC U1 obstruction
has quarter-valued and other phase terms, so the same parity deletion is
not valid there. The separate half-valued CF optimization has its own
restricted source domain; it is not a justification for reducing arbitrary
U1 homotopy sums modulo two.

Suggested minimum controls are exact old/new F2 homotopy values on the
complete comparison support and on translated/degenerate tuples; unchanged
native primitive coordinates and bar primitive values; and direct
`delta(primitive)=source` checks. The chain-valued
`AFSChainHomotopy` remains an independent evaluator for small controls.
Existing scalar-homotopy tests establish the current scalar formula, but
have not tested the proposed early skips.

## Larger option: evaluate F2 homotopy using the binary G map

The optional `AFSBarMod2` backend replaces G when `AFSBar` creates an F2
cochain. It does not dispatch `AFSHomotopyPullback` to a binary path.
That function directly calls the integer map even when
`AFS_USE_MOD2_BAR=true`. The half-phase solver also retains the same
integer homotopy evaluator.

`AFSChainFromBarMod2` was constructed as the literal reduction of the same
integer recurrence. Its existing controls compare translated native words
modulo two, rather than merely their cohomology classes. A later F2
homotopy specialization could therefore use this G reduction together with
the odd-coefficient support of the same F image. Preserving those exact
maps, prefix insertions and normalization would preserve `h* f` pointwise.
An independently chosen native diagonal or homotopy is not interchangeable
without an explicit comparison correction.

This option is larger because it changes cache use. It requires complete
old/new homotopy and marked-lift comparisons in addition to the existing G
map controls. Binary and integer caches may duplicate work or fail to warm
each other. The observed CF-versus-MC tradeoff between current configurations
already shows why a local improvement need not improve a full pipeline.

## SG219: exact torsion-pip phase construction and its doubled source

The saved SG219 classification has torsion p+ip order two, one Majorana
factor, two CF factors and no final bosonic factor. Its remaining d4 target
is odd of order three. This certifies survival in the incoming-image
quotient; it is not a native phase seed or an explicit primitive of the
unadjusted top obstruction. In particular, a zero final bosonic quotient
does not permit setting the phase cochain or its gauges to zero.

There are two distinct costs inside the generic, non-C4 route. In
`AFSStackPipLift`, the `stack_pip_phase_lift` marker precedes transfer of
the full obstruction, its incoming-image adjustments, and the final native
solve. `AFSSolve` constructs the top homotopy correction as a lazy callback;
it does not evaluate that callback before returning. Its consumers occur
after the subsequent `stack_pip_square` marker. Therefore a run that still
shows `stack_pip_phase_lift` has not yet begun evaluating the newly defined
top phase's homotopy. Its obstruction evaluations can already be expensive
because the *lower* defining cochain C itself contains a homotopy correction.
The single stage marker does not distinguish its initial transfer from
transfers after lower-choice adjustments.

For the current omega-zero, canonical integer representative n=s, write

\[
\beta(B)=\frac{d\widetilde B-\widetilde{\delta B}}2,\qquad
J(B)=\beta(B)\smile_1\beta(B)
       +\beta(B)\smile_2d\beta(B).
\]

Here d is the ordinary integral differential, a tilde is the canonical
binary lift, and delta is the binary differential. The supplied
`explicit_pip.gamma_terms16` and the exact sign specialization give

\[
O_5(s,B,C)=\frac12 S^2(C)+\frac12 T(B,s)
             +\frac14J(B)+\frac9{16}s^5 \pmod1,
\]

where T is the binary prism-transgression term. The background-order term
vanishes at omega=0. Hence the following is a literal cochain identity:

\[
\boxed{\;2O_5(s,B,C)=\frac12J(B)+\frac98s^5\pmod1.\;}
\]

This identity requires the omega-zero sign representative and its genuine
sign cocycle, but does not require replacing the open Bockstein by a
closed-input one. It eliminates all C evaluations from the **doubled**
source. On a legal torsion tower, delta B=s^3, so additionally

\[
d\beta(B)=-s^4,
\qquad
2O_5=\frac12\bigl(\bar\beta\smile_1\bar\beta
                         +\bar\beta\smile_2s^4\bigr)
                       +\frac18s^5 \pmod1,
\]

where bar beta is beta modulo two. The sign in the second cup product is
immaterial only after multiplication by one half modulo one. The identity
d beta=-s^4 follows from d(tilde(s^3))=2s^4; it does not set beta to zero or
discard the integer carry in d(tilde B).

To use the doubled identity without changing the marked primitive, retain
the **same already computed native seed** u that solves

\[
\delta_s u=F^*O_5,\qquad
\nu=G^*u-h^*O_5.
\]

The fixed comparison homotopy satisfies dh+hd=FG-id. On the legal, adjusted
tower O5 is closed, so this formula defines an actual global bar primitive
with delta_s nu=O5. By linearity its square contribution can be evaluated as

\[
2\nu=G^*(2u)-h^*(2O_5).
\]

Thus subsequent square evaluation can use a B-only homotopy source.
Solving a new native problem for 2O5 and calling its answer 2u is not
automatically equivalent: canonical Smith division and representative
reduction can select a different closed torsion cochain. The same seed is
what preserves the marked phase, rather than just the existence of a lift.

A finite record of u, the adjusted lower-cochain construction and seeds,
the obstruction formula, and the fixed F/G/h recurrences is also an explicit
recursive definition of nu. Each requested simplex evaluation terminates;
one need not expand its entire bar support just to *define* the generator.
This is valid only after the native obstruction, all required lower-choice
adjustments and the actual seed have been computed and checked. A record
that merely promises to run an unresolved solve later is not such a witness.
Also, u must not be written into the current `phase4` field as if it were
F*nu: those vectors are not identified by the comparison-map identities.
An expression-backed export would require an explicit schema and verifier
that retain the correction, with no claim of an already performed support
audit. The current candidates and output format are unchanged.

The **first** full O5 transfer has a separate exact local simplification.
For the actual defining tower one knows

\[
\delta C=Q(B),\qquad
Q(B)=S^2(B)+s\smile S^1(B)
=B\smile B+B\smile_1s^3
  +s\smile(B\smile_1B+B\smile_2s^3)\quad\text{in }\mathbb F_2.
\]

Consequently its C-dependent term may be evaluated as
one half of (C cup1 C + C cup2 Q(B)), instead of reconstructing delta C
from C face values. This remains true after adding a closed CF adjustment;
after a Majorana adjustment one must use the recomputed B and its Q.
Substitution is inside the binary operation, before taking its canonical
lift. It does not replace an integral differential by a binary value.
Likewise, using delta B=s^3 in beta retains the full expression
(d(tilde B)-tilde(s^3))/2 and its integer carries. No further integer
transport disappears by assumption; the exact n=s specialization already
accounts for those terms.

This can remove some repeated C calls while retaining every phase carry,
but cannot remove C altogether from the original O5. SG219 itself has
nonzero CF-primary image (recorded rank two): closed CF changes can change
the top obstruction class even though delta C is unchanged. The quadratic
C cup1 C term therefore carries information that Q(B) alone does not give.
Net speed benefit remains unmeasured, and neither this substitution nor
the doubled identity supplies the still-needed first native phase seed.

For a future implementation, the existing sign fixtures and their unchanged
scalar-oracle outputs supply direct exact checks. If N is the original
numerator modulo 16, doubling must obey

\[
2N\equiv8J(B)+18s^5\pmod{16}.
\]

Use the unsimplified J for arbitrary B fixtures and the bar-beta version
only when delta B=s^3 has been verified on every relevant face. For the
first-transfer substitution additionally verify delta C=Q(B), then compare
the full numerator before and after substitution on all legal fixtures;
retain off-shell negative fixtures. Existing direct-oracle agreement of the
full sign formula establishes the source convention, but these proposed
runtime callbacks have not been implemented or numerically tested here.
Complete native vectors, the retained seed, and marked doubled phase values
must subsequently agree in one fixed context before adopting either path.

## Measurement and delivery boundary

No speedup is claimed for any suggestion in this note. A later evaluation
should first time the smallest change in fresh contexts with identical
classification settings, preserve the exact marked outputs, and distinguish
obstruction evaluation from solving and subsequent reduction. A same-context
old-then-new comparison is useful for equality but is not an independent
performance benchmark. Only a complete pipeline measurement can establish
an overall gain.

The existing candidate source snapshots, running tasks, accepted-result
criteria and pending final comparison workflow remain unchanged.
