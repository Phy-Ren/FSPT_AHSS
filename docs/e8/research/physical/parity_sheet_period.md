# 4+1D parity transfer under an arbitrary sixteen-sheet shift

The complete dyadic source and dyadic stacking correction of the immutable
parity reference are unchanged when either integral sheet is shifted by an
arbitrary multiple of sixteen. This holds with arbitrary unchanged lower data,
on the legal lower-tower domain. It includes the full normalized `binary4`
recurrence, not only its local arithmetic packets.
For a direct runtime comparison use `Backend(use_specializations=False)`.
This fixes the generic publication-formula path. The optional optimization
`majorana4_product_composed`, dispatched when both input sheets are exactly
zero, is outside this certificate; a shift can cross that dispatch condition.
Its separate equivalence proof is not being silently assumed here.

The E8-first electronic tower is `(e_2, n_2, n_4, nu_5)`. In this note the parity
reference's integral sheet is called `a_2`; its second input is `b_2`. Its raw
field names `n,m,a,b,c,cp` are implementation names, not the electronic tower's
notation. The comparison is

\[
a_2\longmapsto a_2+16e_2,\qquad
b_2\longmapsto b_2+16f_2.
\]

The integers on the two sides can vary independently on every face in the
arithmetic certificate. Closedness of `e_2,f_2`, with the appropriate sign local
system, is needed when these evaluations are interpreted as legal towers. The
certificate does not waive the reference's exact-division domain conditions.

## Exact arithmetic certificate

Run `python probe_parity_sheet_period.py`. Its JSON output records the SHA-256
of each immutable arithmetic program and the following universal conclusions.

| Program | Result under the shift |
|---|---|
| Four lower source/product packets | Exactly unchanged |
| `y6`, `h6` | Exactly unchanged |
| `high6` dyadic numerator | Exactly unchanged |
| `rho4`, including all 35 upper-data outputs | Exactly unchanged |
| `tensor4` | Exactly unchanged |
| `high6` cubic numerator | Difference divisible by 16 |
| `nonbinary4` numerator modulo 48 | Difference divisible by 16 |

Each node carries a lower bound on the 2-adic valuation of its original value
and of its change. Addition takes minima; multiplication uses
`(x+dx)(y+dy)-xy=x*dy+y*dx+dx*dy`; division by `2^k` reduces the guaranteed
precision by `k`; a digit or reduction modulo `2^k` is exactly unchanged when
the input change is divisible by `2^k`. These rules hold for negative integers
and mathematical floors. Constants are simplified only when shared by the two
evaluations. This is a proof by induction on every node of each finite program,
not a selection of numerical examples.

Divisibility by 16 of a denominator-48 numerator leaves a possible third-root
phase. The cubic correction is retained. This result does not claim that the
entire stacking correction is unchanged.

## Why the normalized transfer also descends modulo sixteen

The raw local certificate alone would be insufficient: the runtime's exact
equality tests, zero-factor tests, and degeneracy tests can take different
branches after the shift. The following second certificate resolves that issue.

Run `python probe_parity_normalization.py`. It substitutes every adjacent
simplicial degeneracy into the actual raw programs. It rewrites integer
polynomials exactly. An unresolved `div`, `floor`, `mod`, or `bit` becomes a
formal atom; no value is guessed. Boolean atoms are idempotent over the
integers. It proves:

1. `y6`, `h6`, both `high6` outputs, `rho4`'s raw residual, and `tensor4` vanish
   identically on every degeneracy of their top simplex. There are 29
   program/degeneracy cases. For `rho4`, its 35 output faces also satisfy the
   same degeneracy, so the three subsequent `h6` evaluations vanish.
2. With either input factor zero, the raw tensor and residual vanish.
   `rho4`'s upper output is exactly the other factor. Consequently its two
   equal `h6` values cancel, and the zero input's `h6` value vanishes. The
   zero-sheet `y6` also vanishes. These are six symbolic reductions.
3. The runtime's five-dimensional Eilenberg–Zilber homotopy has 291 retained
   projection triples. Composing these triples with each of the five input
   degeneracies, and reducing the resulting formal chains over `F_2`, gives
   zero in every case. Only a simultaneous repeated adjacent vertex or a
   fiber projection with fewer than three vertices is discarded. No field
   values are substituted in this combinatorial calculation.

The remaining runtime terms have direct short proofs. The extra tensor
negation term is `s(01)` times a polynomial in the first three binary digits
of the two triangle values. It has period eight, vanishes if either triangle
is zero, and is normalized: a repeated first edge kills `s(01)`, while any
other repeated edge kills one of the two triangles.

The chart encoding/decoding multiplies integral sheets by signs and changes
binary upper fields using only the parity of the integral sheet. Thus it
commutes with reduction modulo sixteen. Pullback selects faces or inserts
zero, so it also commutes with that reduction. The preliminary native-coordinate
shift uses only the second binary digit and is unchanged.

The first-face perturbation `delta` is the difference of the twisted and plain
first faces. It preserves the degenerate-chain ideal. For a degeneracy away
from the first edge, both faces retain that degeneracy. For a repeated first
edge, the initial background edge and triangle vanish, making the two faces
equal. Zero factors remain zero under all these operations.
The runtime additionally omits homotopy cuts whose first two background
vertices agree before applying `delta`. On precisely those cuts,
`s(01)=0` and every `w(01i)=0`, so `delta` vanishes even when the two fiber
projections have distinct initial vertices. This pruning is therefore also
compatible with the quotient; it is not a value-dependent extra assumption.

Therefore all local cochains, the homotopy, and the first-face perturbation
descend to the same reduced normalized chain complex with integral sheets
read modulo sixteen. If a reduced state becomes degenerate only after reducing
modulo sixteen, its exact degenerate face/degeneracy lift has the same residue;
the raw normalization identities and period certificate give zero on it.
For zero factors, use the exact zero-factor lift instead. This also explains
why deleting an exactly degenerate state in one evaluation but retaining its
congruent representative in the other does not change the answer.

The full binary recurrence is a finite sum of the descended tensor and
residual cochains over iterated homotopy/perturbation chains. Exact duplicate
elimination merely sums those chains over `F_2`. Every summand therefore
depends only on the residue state. The existing six-step termination condition
is preserved as a condition of the legal reference transfer; no new
termination claim is inferred from a sample run.

## Consequence and scope

The dyadic and lower components required by the mixed electronic/E8 comparison
are invariant, including legal cylinder/prism inputs. The remaining mixed
source and stacking change is the explicitly retained odd-primary cubic
change. The actual cubic source/product/gauge comparison is proved separately
in [the mixed bridge note](../general_groups/mixed_bridge_4p1.md).

This theorem concerns the four-tuple tower through 4+1D and its fixed parity
reference coordinate. It does not introduce an intrinsic filtration-zero
4+1D response row, and does not prove an unspecified universal physical
classification theorem beyond that tower.

## Reproducible provenance

The reference is `/home/xingyu/FSPT_AHSS_public`, revision
`ac45fa7ed0acd992a2f3a69273762dc9dceb2a97`. The scripts read it without modifying
or importing executable formula sources. The normalization certificate imports
only the standalone runtime's finite projection combinatorics, with bytecode
writing disabled. JSON outputs pin every tested DAG and the relevant source
files.

Runtime locations: `fspt/full_formula/runtime.py` lines 158–179 (homotopy cuts),
205–299 (pullback, normalization, chart and perturbation), 350–375 (native shift
and source), and 391–428 (full binary stacking recurrence). The corresponding
displayed construction is `formulas/publication_source/full4/graded_full.py`
lines 36–89 and `product_full.py` lines 17–44. These are implementation sources,
not independent literature classifications.
