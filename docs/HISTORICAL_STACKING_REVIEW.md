> Public release: this document describes the complete local audit. [Private reference inputs](../PUBLIC_RELEASE.md#private-comparison-materials) are not distributed; production and independent result audits remain reproducible.

# Four historical stacking differences with identical graded layers

The new boss PDF agrees with all 920 independently computed graded entries and
expressly does not compute stacking extensions. A separate historical source,
`draft_table.json`, transcribes the old manuscript's Extension column. Four of
its stacking groups disagree even though their four graded layers agree:

| SG | Historical Extension | Independent stacking |
|---:|---|---|
| 68, Ccca | `Z2^3 + Z4` | `Z2^5` |
| 81, P-4 | `Z + Z2^4 + Z8^3` | `Z + Z2^2 + Z4 + Z8^3` |
| 82, I-4 | `Z + Z2^4 + Z8^2` | `Z + Z2^2 + Z4 + Z8^2` |
| 101, P4_2cm | `Z2 + Z4` | `Z2^3` |

Here `+` denotes direct sum and powers denote multiplicities. The inspected
independent presentations, generator names, source IDs, result hashes, and
historical transcription hash are recorded in
`results/boss_layers/stacking_context_review.json`. No solver formula or saved
classification was changed to obtain agreement.

## What the manuscript actually claims

The supplied `tables_classification.tex` contains these exact four old values,
at lines 18, 31, 32 and 51. Its caption at line 71 identifies the Extension
column as existing GAP SptSet results and says entries with nonzero p+ip use
additional input beyond the stacking law derived in that manuscript. The
space-group discussion in `sections/06_examples.tex`, lines 87–93, gives the
same sector limitation. The separate p+ip discussion at
`sections/05b_pip.tex:137` labels the first proposed integer-layer stacking twist
as a conjecture. This does not establish that each numerical Extension entry
was itself explicitly conjectured.

The supplied cross-check note lists corrections at SG17, SG75, SG159 and
SG176; it does not identify any of these four extension discrepancies as a
known typo. There is also no supplied row-level derivation explaining the old
four extension values. They should therefore be described as legacy
computational claims, not silently dismissed as transcription errors.

This provenance is now confirmed directly in four original completed SptSet
logs. Their `Group structure` lines reproduce the historical values exactly:
`sg068.log:213`, `sg081.log:247`, `sg082.log:259`, and `sg101.log:207`.
The logs also contain the matching four graded layers and successful exits,
dated March 7, 9, 17 and 18, respectively. Read-only copies and source hashes
are in `reference/legacy_stacking_context/`; the small parsed record is
`results/boss_layers/historical_log_evidence.json`. These establish actual
legacy computations, without exposing a row-level mathematical derivation.
Their recorded elapsed times are not a controlled performance benchmark.

The current manuscript's discussion of a disputed S4 point-group value in the
spinful **internal** sector concerns nonzero effective omega. That paragraph
does not explain these space-group differences, which use effective omega=0.
Read-only copies of the relevant supplied sources and their hashes are in
`reference/legacy_stacking_context/`.

## Relations that distinguish the answers

For SG68 and SG101 there is one surviving Majorana generator `B`, no surviving
CF or p+ip generator, and a bosonic kernel `(Z2)^k`, with `k=4` and `k=2`
respectively. The independent complete reduction gives `2B=0`, using nonzero
incoming fermionic and bosonic gauges with an explicit phase primitive. It
does not claim that the raw product cochain vanishes pointwise. Thus the
presentation is `(Z2)^(k+1)`. A nonzero bosonic value of `2B` would instead give
`Z4 + (Z2)^(k-1)`, exactly the historical alternatives. This is a precise
extension discrepancy. Changing the lift by a bosonic element cannot explain
it: `2(B+D)=2B` because every bosonic element has order two.

For SG81 and SG82 the inspected complete presentations have

```text
2P = C1,     2C1 = 0,
```

where `P` is the torsion p+ip generator. `C1` appears in no other lower relation.
These two generators therefore give a direct summand `Z4`. The historical
total is exactly the independently computed lower group with a separate
`Z2` appended, which replaces this `Z4` by `Z2 + Z2`. This describes the
algebraic difference; it does not prove which operation the old program used.

There is a useful independent check of the CF part of this square. On C4 write
`s(g)=g mod2`, `eta(g)=floor(g/2)` and `B(g,h)=s(g)eta(h)`. Then `dB=s^3` and

```text
K = B cup1 B + B cup2 dB + s cup B
```

is closed. Its values on `(1,i,1)`, for `i=0,1,2,3`, are `[0,0,0,1]`. The sum
of these normalized bar simplices is a mod-two 3-cycle, so `K` represents a
nonzero cohomology class. In contrast, `s^3` has zero period on the same cycle.
`tests/test_c4_pip_square_cf.py` checks all 64 lower equations, all 256 closure
equations, the actual cycle boundary, and this period exactly. In fact it also
checks the pointwise identity `K(a,b,c)=(a mod2)*floor((b+c)/4) mod2` on all
64 triples, identifying the standard nonzero C4 3-cocycle. This detects
the nonzero CF square without assuming a choice of the upper phase.

The supplied point-group table independently lists the omega=0 S4 result as
`Z4` (`tables_point_groups.tex:17`). A space-group projection to this C4 point
group with a section forces its classification to occur as a direct summand,
by pullback and restriction. SG81 and SG82 are the symmorphic P-4 and I-4
cases. Task `743cdd72` verified their actual quotient maps, order-four affine
sections, and the identity of projection composed with section on all four
elements. It also computed the finite C4 complete stacking group independently,
obtaining the presentation `[[2,0],[-1,2]]`, with exact Smith factor `4`.
The saved artifact is `runs/finite_c4_retraction_controls.json`; its affine
matrix orders and full Smith identities were independently rechecked locally.
A group
`Z + Z2^4 + Z8^k` has no `Z4` direct summand, whereas the newly computed group
does. This is an additional consistency test, not a replacement of the full
affine calculation by point-group cohomology.

## Current evidence boundary

The displayed relations are extracted from actual independent presentations,
whose Smith identities are checked. Full support and literal CA-formula
audits for all four groups passed. SG68 took 868.55 seconds and returned
five order-two factors. A same-model SG82 changed-lift check also passed:
the square coordinates changed from `[0,0,1,0,0,0]` to `[0,3,1,0,0,0]`,
and their nonzero difference has an explicit witness in `2H`.

Those initial upper-phase numerical runs used the previous AW transport
coordinate. Their stored cochains are superseded as current-coordinate
witnesses. Fresh full support audits of SG81 and SG82 now pass in the
corrected immutable source, returning the same displayed abstract groups.
The finite C4 stacking and both affine retractions also pass again; exact
tasks, hashes and results are in
`docs/validation_runs/corrected_pip_transport.json`. The exact rephasing and square gauge in
[AW_TRANSPORT_CORRECTION.md](AW_TRANSPORT_CORRECTION.md) preserve the torsion
relation classes. The closed-Majorana SG68/101 audits, affine retractions,
and exact C4 CF period are unaffected pointwise. This note identifies the
conflicting relations and the provenance of the historical claims. It does not assert a diagnosed
bug in the legacy implementation or a general physical-coherence theorem
beyond the formula scope documented in `VALIDATION.md`.
