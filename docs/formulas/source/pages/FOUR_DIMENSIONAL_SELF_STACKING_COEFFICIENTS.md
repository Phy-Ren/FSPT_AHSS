# Complete coefficient data for 4+1D self-stacking

The [complete self-stacking formula](FOUR_DIMENSIONAL_SELF_STACKING.md)
retains two large, fully specified binary coefficient sums. They are
specializations of the completed general stacking expression: both input
states are made equal in every physical factor and in every argument of
an existing lower operation. Internal faces of a contraction are not
identified before that contraction is completed.

| Coefficient sum | General terms | Self-stacking terms | Distinct protected numerator terms |
|---|---:|---:|---:|
| $`\mathcal I_5^{\gamma\psi}`$ | 5,684,189 | **3,613,999** | 55,901 |
| $`\mathcal I_5^\psi`$ | 2,869,198 | **793,669** | 34,243 |

The complete mathematical expressions are the
[Majorana–p+ip table](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/gamma_psi/INDEX.json)
and the [p+ip table](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/psi/INDEX.json).
The latter includes the entire pure-source and tensor contributions.
These large lists provide a reproducible restricted expression; their
size remains a target for structural simplification. The counts do not
assert optimality under other cochain identities.

Each outer row specifies an actual product of binary face values.
Every factor is either a physical cochain face, a fully defined lower
obstruction or stacking twister, a Bockstein or integer carry with all
its arguments specified, or a whole canonical lift/floor with its entire
numerator. No unspecified finite polynomial is counted as one factor.
The lower-operation domains and integer precisions are those of the
[general coefficient conventions](FOUR_DIMENSIONAL_STACKING_COEFFICIENTS.md).

All outer products are collected over $`\mathbb F_2`$ after the equal-input
substitution. This includes cancellations within argument polynomials,
identical complete lower-operation values, and normalized lower operations
with zero decorations. Identical names alone do not identify factors:
the operation, all arguments, digit, and differential convention must
also coincide.

The protected-numerator column counts each distinct nonlinear factor's
explicit interior once. It is separate from the outer count; it does not
pretend that repeated occurrences of the same lift can be distributed as
integer addition. The transformed lower-operation argument arrays contain
1,565,241 explicit argument summands in the mixed table and 911,981 in
the pure table. These argument data specify the values of already defined
operations and are not additional outer summands.

The [standalone verifier](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/verify_coefficients.py)
checks file hashes, factor references, complete reduction scopes, duplicate
outer products, and every stated table count. The independent native
readbacks for [Majorana–p+ip](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/gamma_psi/NATIVE_RESTRICTION_CHECK.json)
and [p+ip](coefficients/FOUR_DIMENSIONAL_SELF_STACKING/psi/NATIVE_RESTRICTION_CHECK.json)
evaluate the original completed formula and the specialized expression on
four signed physical towers with arbitrary Majorana root lifts. All checks
agree. These readbacks supplement the exact algebraic substitution and
coefficient collection; they are not an independent physical calibration.

The six exchange-origin contributions retain their labels throughout.
No term is assigned a new physical label from the variables left after
specialization. No obstruction, source coordinate, product coordinate,
or output gauge has been changed by these table reductions.
