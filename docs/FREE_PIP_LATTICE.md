# Free p+ip generators and their surviving lattice

This note concerns the physical spin-half convention with `omega=0`. It gives a
primitive-generator strategy beyond the abstract free rank recorded in the
initial result files. It does not change those immutable files or assert that
the additional target-group computations have already been performed.

Write `H = H^1(G,Z_s)`, where `s` is the orientation character. Let `S` be the
subgroup of integer-layer classes surviving all higher obstructions, including
all lower defining choices. Its free projection is a finite-index sublattice
`L_surv` of the free part `L` of `H`. Finite index preserves the rank, so the
abstract group type alone cannot determine this embedding.

## Orientation-preserving groups

When `s=0`, an integral 1-cocycle is an ordinary homomorphism `n:G->Z`. The actual
defining tower

```text
(n, B, C, nu) = (n, 0, 0, 0)
```

is flat in the supplied normalized coordinate. The first source is `Sq^2(a)=0`
for the closed degree-one cochain `a=n mod2`. The second source vanishes with
zero Majorana field and zero background. In the full upper formula, `W`, its
Bockstein, the integral carry `K`, and the Cartan terms vanish. Every block in
the fixed `Y5_word_total` has a positive sign degree or a positive extension
degree, so the remaining binary completion also vanishes.

There is an exact executable check: substituting `s=B=C=0` into the complete
7239-operation O5 expression and leaving every `n` evaluation symbolic reduces
its output to the constant zero. Thus `L_surv=L`. Each native integral H1 basis
vector, converted by the independent bar comparison map, gives an explicit
primitive free generator with the three lower fields zero.

## A universal bound for signed groups

Every signed integral cocycle satisfies

```text
n(gh) = n(g) + (-1)^s(g) n(h).
```

It therefore defines an actual homomorphism
`G -> D_infinity = Z semidirect C2`, `g -> (n(g),s(g))`. Denote the universal
signed integer coordinate on this group by `x`. The class `2x` survives all
three obstruction stages:

1. Its mod-two reduction is zero, so its first source vanishes and `B=0` is a
   legitimate choice.
2. View the infinite dihedral group as the free product `C2 * C2`. In degrees
   at least two, restriction to the two vertex groups gives an isomorphism on
   group cohomology with any fixed coefficient module. This follows from its
   action on the Bass-Serre tree, whose edge stabilizers are trivial. The two
   restrictions of `2x` are `0` and `2s`. The supplied parity formula gives
   `Q(0,0)=Q(2s,0)=0` pointwise. Consequently its degree-four obstruction class
   is zero, and a degree-three primitive `C` exists on the actual infinite
   dihedral group.
3. On either reflection subgroup the phase coefficient module has the sign
   action. Its cyclic cochain complex alternates multiplication by `-2` and
   zero. Since multiplication by two on `R/Z` is surjective,
   `H^5(C2,U1_s)=0`. The same restriction isomorphism gives
   `H^5(D_infinity,U1_s)=0`. Thus the closed full O5 phase has a degree-four
   primitive `nu`.

Pullback of this universal complete tower proves `2H <= S`, and hence
`2L <= L_surv`. This assertion uses the full higher obstruction problem, not
only a first-page rank argument. Constructing the universal primitives with an
actual infinite-group resolution gives reusable bar-cochain representatives.
The optional factory in `gap/pip_free.g` now constructs these primitives on an
actual infinite dihedral Pcp group, using a resolution with dimensions
`[1,2,2,2,2,2,2]`. `tests/test_dihedral_pip_lift.g` passed the native cohomology,
signed-character, pair-coordinate, and complete defining-tower checks on bar
supports in task `f8c23e63`. Its primitives use the independent comparison-map
homotopy correction. This universal test does not yet assert that every target
space group's primitive lattice has been exported. A second independent audit,
`tests/test_dihedral_pip_extra.g` (task `af3534f2`), checks the complete tower on
four actual degree-five bar tuples beyond the comparison supports, including
negative translations, mixed reflections, and an identity degeneracy. It also
verifies the signed character law on these group elements.

The bound two is sharp universally. Assign reflection values `(u,v)` to a
signed integer cocycle. Then
`H^1(D_infinity,Z_s) = Z^2 / <(2,2)>`, with free representative `(0,1)` and
torsion representative `(1,1)`. Either parity of an odd free class, even after
adding the torsion class, restricts to an odd integer on one reflection. Its
first source restricts to the nonzero class `s^3`. Therefore the surviving
free projection for this universal group is exactly `2Z`.

## Recovering a primitive target-group basis

Once the universal tower is implemented, only the joint parity quotient
`H/2H = (L/2L) + Tor(H)` remains to be tested for a given space group. The
torsion coordinate must be included: a free class plus the torsion class can
survive even when a chosen unshifted free representative does not.

For every surviving parity class retain its actual lower choices and phase
primitive. Let `V` be the projection of these classes to `L/2L`. Then

```text
L_surv = {v in L : v mod2 belongs to V}.
```

A particularly useful primitive basis needs no general binary stacking rule
for the integer layer. Put a binary basis of `V` in reduced row-echelon form,
and test each resulting row directly to obtain its torsion shift and flat
tower. Add `2e_j` for every nonpivot column, using the universal doubled tower.
These `rank(L)` rows have determinant `2^(rank(L)-dim(V))`. They generate every
row of `2I`, since for each pivot `p` one has
`2e_p = 2v_p - sum_j 2(v_p)_j e_j`, with `j` ranging over nonpivot columns.
They therefore form a basis of the full inverse-image lattice. This records
the actual integer H1 coordinate of every marked free generator without
combining cochains through an unimplemented general p+ip product. A
stage-by-stage integer-kernel calculation is another option. The largest
observed free rank among the current space groups is three; this procedure
never enumerates lower FSPT states.

No finite-order relation is imposed on the resulting free generators. As an
abstract abelian extension, the free quotient splits after choosing these
lifts. Their native H1 coordinates and flat defining towers make that split
explicit. Until these target computations and witnesses are exported, the
initial `Pfree` names retain the abstract scope stated in `RESULTS_REPORT.md`.

The optional adapter has now passed complete selected-generator equation checks
for SG1, SG2, SG6 and SG7. Subsequent controls in `runs/free_integration_v05`
export explicit lattices for SG1, SG2, SG6, SG7, SG9 and SG174, of indices
`1, 8, 2, 1, 1, 2` respectively. SG2 has basis `2I3`; the rank-one index-two
cases have basis `[2]`. These are independently computed controls, not a claim
that every accepted result already contains the additional free export.

## Checks

`tests/test_free_pip_universal.py` checks symbolic vanishing of the entire
unitary O5 expression, lower sources on ordinary integral cocycles, and all
homogeneous reflection simplices for the even dihedral lower sources. These
are exact formula checks. The cohomological restriction argument above is an
algebraic proof; it is not inferred from random tests or external answer tables.
