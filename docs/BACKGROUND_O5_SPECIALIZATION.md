# Exact specializations of the full-background p+ip O5

`fspt/formulas_background_specialize.py` reads the existing 34,198-node
`gap/pip_o5_background.json`. It does not modify the original compiler, the
provided formula, or its Alexander–Whitney edge frames. It emits separate
`AFSPipO5BackgroundEvenProgram` and `AFSPipO5BackgroundSignProgram` functions,
with independent call counters and the same `n,b,c,w,s` field interface.

The even program requires the **actual integer cochain n to be even on
every edge**. It continues calling the original n, preserving all integer
carries; it never substitutes n/2. Each evaluated n field is checked for
evenness in the generated GAP code. The dispatch proof is integral linearity
of the bar representative when every integer-H1 coefficient, including
torsion coordinates, is even. A statement merely about the free coordinate
or about the cohomology class is insufficient.

The sign program requires **n=s pointwise**, with s taking values zero or
one. It replaces only field references at the identical face. The runtime
integration checks equality of the n and s function pointers before input
normalization. Equality modulo two is insufficient.

The abstract evaluator tracks an integer's known residue modulo a power of
two and, when available, inclusive bounds. Addition, multiplication, positive
power-of-two division and floor operations propagate these facts. For
`a=r_a+2^k A`, `b=r_b+2^l B`, the product is known modulo the minimum of
`k+v2(r_b)`, `l+v2(r_a)` and `k+l`. A 32-bit precision cap only discards
information; it does not truncate runtime integers. Bounds eliminate binary
sign carries, and low-bit facts eliminate terms already forced to zero.
Negative floor and bit operations retain floor division, including the
two's-complement low-bit identity `bit(-1,k)=1`.

Reachability removes unused scalar instructions after simplification. It can
therefore remove an unused exact-division guard. Equality is asserted on the
original formula's legal complete-tower domain; this is not a new validator
of arbitrary off-shell inputs. Every retained division still checks exact
divisibility. The compiler has no space-group answer inputs or survival gates.

The resulting graphs contain 7,786 nodes for even n and 16,008 nodes for n=s.
`tests/test_background_specialize.py` checks 64 legal full-background towers
per branch against both the unchanged provided evaluator and the complete
scalar graph. The even cases include 480 negative edge values and integers
up to 84 bits. All 128 three-way equalities pass. Independent review checked
the low-bit multiplication precision, negative floors/bits and domain of
dead-code elimination.

`tests/test_background_specialize.g` replays the same oracle fixtures against
the generated complete and specialized GAP programs. A separate odd-input
test exercises the even-branch rejection. It measures scalar evaluation on
fixed callback tables, not an affine-group classification or a full campaign.
Exact source and log hashes and measured timings are archived in
`docs/validation_runs/background_o5_specialization.json`.

The original complete background evaluator remains available. The runtime
switch `AFS_USE_BACKGROUND_SPECIALIZED_O5=false` disables both specializations;
ordinary odd free candidates and unrecognized integer representatives use the
complete graph.
