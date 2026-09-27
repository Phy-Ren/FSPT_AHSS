> Public release: this document describes the complete local audit. [Private reference inputs](../PUBLIC_RELEASE.md#private-comparison-materials) are not distributed; production and independent result audits remain reproducible.

# Optional bar comparison modulo two

`gap/backend_bar_mod2.g` implements the normalized bar-to-native comparison
map directly over F2. It exposes separate `AFSChainFromBarMod2` and
`AFSBarMod2` functions. Loading the file alone changes no production
dispatch. `AFSBar` opts into this path only for coefficient `"F2"` when
`AFS_USE_MOD2_BAR := true` is explicitly set and the module is loaded.

For the integral native contraction `h`, the original comparison map is
defined by `G_0([]) = e_0` and `G_k = h G_(k-1) d_bar`. Reduction modulo two
commutes with every sum, signed boundary term and group-ring translate.
The modular contraction was independently verified to be exactly `h mod2`.
Induction on `k` therefore proves equality of complete native words after
reduction. Cancellation before applying `h` uses its Z-linearity; it does
not assume that a contracting homotopy is linear over the group ring.

The new recurrence retains the exact multiplication order of translated
cells. It returns zero on degenerate normalized bar tuples, uses a separate
`Gmod2Cache`, and keeps the integral G, HG and homotopy caches intact. For
any native F2 vector, `AFSBarMod2` consequently returns the same 0 or 1 on
every tuple as `AFSBar(...,"F2",...)`. This pointwise identity preserves
rational nonlinear formulas subsequently evaluated on that callback; the
claim is stronger than agreement of cohomology classes.

Integer and U1-valued native cochains must continue to use the integral
comparison map. The exact bar primitive correction also keeps the integral
homotopy. A primitive with an F2 native seed may use the new pullback for
that seed because it is pointwise identical to the previous pullback.

`tests/test_backend_bar_mod2.g` compares complete comparison words on
translated and inverse tuples through degree four, entire native pullback
vectors through degree three, and an exact arbitrary-bar primitive
equation. SG29, SG47 and SG219 pass all these controls. The SG47 test in
`tests/bench_backend_bar_mod2.g` also confirms equality of every entry of
the degree-five U1 obstruction vector for the same native H3 generator.
These controls establish exact transfer semantics; full-pipeline timing is
measured separately, because earlier classification stages warm different
contraction caches.

Completed task outputs, hashes and exact source-file hashes are recorded in
[backend_bar_mod2.json](validation_runs/backend_bar_mod2.json).

## Closed CF phase specialization

The separate optional `AFSClosedCFObstruction(C)` helper evaluates
`(C cup_1 C)/2`. This requires a closed degree-three F2 cochain and zero
Majorana/omega layers. The full formula differs by `(C cup_2 delta C)/2`,
which vanishes pointwise on this domain, including the sign-twisted phase
module. Native H3 representatives pulled back along G are globally closed.
The Majorana lift's C primitive need not be closed and must keep the full
formula.

An explicit nonclosed normalized C on the finite cyclic group of order
three gives six disagreeing five-tuples; `tests/test_closed_cf_domain.g`
checks this intentional domain failure. The SG47 and SG228 comparisons
against the full compiled formula pass both translated tuples and the
entire native phase vector. SG228 compares all 231 entries for the same
first H3 basis vector. These are exact cochain equalities, not only
phase-group comparisons. The older generic cup helper runs first in these
controls, so their timings include different cache states; they are
correctness controls, not paired production benchmarks.

The optional `AFSSolveData` API returns the same exact primitive recurrence
as `AFSSolve`, together with its native primitive and native obstruction
vectors. This allows a caller to retain an existing phase seed without
evaluating the native transfer twice. The ordinary `AFSSolve` implementation
is unchanged.

`AFSClosedCFObstructionDirect` evaluates the three cup products without
generic face construction. `AFSClosedCFObstructionLazy` first evaluates
each consecutive three-face and omits its composed-face factor when the
first factor is even. Both retain normalized identity guards. They agree
with the reference cup operation in 12,080 exact comparisons, including
negative, nonnormalized callbacks and tuples containing identity elements.

## Half-valued sources and unchanged primitives

`AFSNativeHalfPhase` applies only to sources taking values in
`(1/2)Z/Z`. Even integer chain coefficients then contribute zero modulo one;
odd coefficients and orientation signs all act identically. Skipping even
coefficients before calling the source gives exactly the original canonical
native vector. The helper checks the half-integrality of every evaluated
value; its explicit domain remains a caller precondition for skipped terms.
The closed CF source satisfies that precondition by construction.

`AFSSolveHalfPhaseData` uses that native vector with the unchanged canonical
native solver and the original integral bar homotopy correction. It does
not substitute the independently constructed native higher diagonal for the
transferred bar cup: those diagonals are known to agree in cohomology, and
that alone would not justify replacing the marked primitive. Native-vector,
canonical-seed and translated exact-bar-primitive comparisons pass on SG7
and SG47. A separate SG87 same-classification comparison is recorded by the
stacking validation suite.

An immutable actual-survivor trial on SG228 first runs modular native
classification, then constructs its surviving C1 lift using modular G,
the lazy closed CF source and the half-phase transfer. Classification took
333.677 CPU seconds and lift creation took 341.878 CPU seconds; actual phase
samples were then evaluated. In the corrected v07 production task
`full_corrected_v07-p002-sg228`, C1 starts at CPU timestamp 335.587 seconds
and B1 starts at 1667.728 seconds, giving 1332.141 CPU seconds for C1.
Thus the observed C1-stage ratio is 3.8965, comparing 1332.141 with 341.878.
This combines G2, the lazy closed formula, half-phase transfer and retained
native seed; it does not isolate the contribution of any one change.
The runs have different driver work and cache histories, although both run
modular native classification first. This is a stage comparison, not a
whole-group speedup or a controlled same-process A/B benchmark. The
230-group campaign records provide the final performance comparison.

The same immutable development source completes SG219 classification in
789.109 CPU seconds, then constructs its two surviving CF lifts in 746.792
and 186.948 CPU seconds, respectively. Four marked phase samples for each
lift also evaluate successfully. In corrected v07 task
`full_corrected_v07-p001-sg219`, C1 begins at CPU timestamp 763.202 seconds
and C2 begins at 3104.317 seconds: the old C1 stage takes 2341.115 seconds.
The corresponding observed C1-stage ratio is 3.1349. The same differences
in context and cache history apply. The development trial stops after the
CF lifts and does not measure bosonic lift construction or stacking
relations, so its total duration is not a complete SG219 calculation.

## Experiments not selected

All-column Smith-basis transfer is mathematically exact even for nonclosed
phase cochains: for `U D V = S`, evaluate every transformed column, then
recover the original canonical vector as `mod1(w V^-1)` before solving.
Dividing the already reduced `w` directly would choose a different torsion
branch. Exact arbitrary-cochain tests pass, but no speed benefit was found.

On SG219, ordinary degree-five F construction took 52.959 CPU seconds for
416,625 bar terms; a zero-callback traversal took another 5.403 seconds.
Only 1,560 of these terms have even coefficients, so filtering parity alone
cannot explain a large improvement. Smith-basis chain construction was
slower and remains optional.

A separate exact hash-cache prototype preserves collision equality,
replacement, stored failure values and immutable keys, including signed
large integers and non-Pcp inputs. Its initial direct sparse-hash memo
variant took 71.287 CPU seconds on the actual 416,625-access SG219 F5
sequence, compared with 50.114 seconds for the existing sorted dictionary.
Both had 306,871 misses and exactly equal outputs: the initial hash variant
uses 1.4225 times the CPU time, a 42.25% regression on this access sequence.
Hash caching was not selected. The later replacement-capable wrapper has
correctness tests but is not represented by that timing. Its byte-level
hash relies on GAP's deployed representation; exact key-representation
tests are a portability precondition when changing GAP versions.

Completed logs, hashes, source manifests and the explicitly partial F5
profile are preserved in
[cf_backend_optimizations.json](validation_runs/cf_backend_optimizations.json).
Cancelled development probes are distinguished from passing checks.
The older SG219 arbitrary-H3 compiled-formula probe reached its preset
3600-second wall timeout before the original integral-G branch finished;
it provides no paired equality result or speed ratio. The completed actual
survivor bundle is a separate experiment. No backend development probes
remain running.
