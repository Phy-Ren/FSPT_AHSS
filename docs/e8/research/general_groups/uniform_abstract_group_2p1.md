# 2+1D: the uniform response image has full rank when s is trivial

This is an auxiliary existence and abstract-group argument. It does not
replace the explicit terminal source, product, gauge, or coordinate
comparison required for the cochain implementation. States are ordered
`(e_0,n_0,n_2,nu_3)`.

Assume the physical classification is the specified charge-conserving
topological symmetry theory, with finite-cover transfer for its actual
twisted tangential Thom spectrum. Let
`1 -> T=Z^r -> G -> F -> 1`, with finite `F`, and let the extension by
the physical charge circle be specified, including magnetic translations.
No filling or other nonadditive response fiber is fixed externally.

## A translation cover carries both coefficient generators

Choose a normal finite-index sublattice `K` of `T` on which both sign
characters vanish, for example `2T`. Its spatial linear representation is
trivial. The bosonic charge-circle quotient over `K` has a fibration

`BU(1)_b -> BG_b^K -> BK`.

If the fermionic extension is represented by `omega`, the transgression
of the fiber generator `u` is the integral Bockstein `beta(2 omega)`.
It vanishes because `BK` is a torus and
`H3(BK,Z) -> H3(BK,R)` is injective. Therefore `u` extends to an integral
class `c0` on `BG_b^K`. This uses the classifying-space fibration, not a
splitting of the magnetic projective group extension.

Let `w` classify its fermion-parity extension. The restrictions of `w`
and `c0 mod 2` to the charge-circle fiber agree. Their difference is
pulled back from `a in H2(BK,Z2)`. Since `H3(BK,Z)` has no two-torsion,
`a` has an integral lift. Correcting `c0` by that lift produces `c` with
`c mod 2=w`.

The restricted tangential structure consequently admits a map of
classifying spaces to `BSpin^c`, over `BSO`, which is the identity on the
coefficient fiber. A group homomorphism to `Spin^c` is neither required
nor asserted. In particular, irrational magnetic commutators do not
invalidate this argument. Pulling back the physical IQH and neutral E8
coefficient phases gives completed classes over `K` with responses
`(e_0,n_0)=(0,1)` and `(1,0)`.

## Transfer and its precise conclusion

The full finite-index symmetry inclusion induces a finite cover of the
actual tangential classifying spaces, with the tangent bundle pulled
back. Its Thom transfer has zero-dimensional vertical tangent, so it
requires no additional orientation. Transfer phases along this cover.
On the filtration-zero coefficient it is the sum of the coset actions.

In 2+1D both coefficient generators have action `s`. Thus, when `s=0`,
the transferred classes have leading responses
`(0,N)` and `(N,0)`, where `N=[G:K]`. This edge statement does not require
the generally stronger assertion that transfer after restriction is
globally multiplication by `N` on every twisted phase.

In addition, a uniform neutral E8 layer with trivial internal action
already gives `(1,0)` for trivial `s`. Consequently the actual physical
response image is

`Z_e0 direct-sum m Z_n0`, with `m>0` and `m` dividing `N`.

The exact value of `m`, and the completed cochain representative realizing
it, are not determined by transfer. The integral differential operations
and terminal completion remain necessary for those tasks. The argument
also assumes the actual physical theory; it does not certify that the
currently retained CI evaluator already realizes every transferred class.

If `s` is nontrivial, the invariant uniform coefficient group is zero,
so neither uniform integer response is allowed. The criterion here is
`s`, not the `rho` criterion for intrinsic 4+1D responses.

## Consequences within each response sector

Let `K00` be the physical stacking group with both uniform responses zero.
An abelian extension by a free response lattice splits after completed
generators are chosen. The following are separate abstract statements,
not a combined classification table:

- With `e_0=0` and all allowed `n_0`, the group is noncanonically
  `K00 direct-sum Z` for trivial `s`.
- With `n_0=0` and all allowed `e_0`, it is noncanonically
  `K00 direct-sum Z` for trivial `s`.
- With both uniform responses allowed, it is noncanonically
  `K00 direct-sum Z^2` for trivial `s`.

The zero-response kernel itself is unchanged by this algebraic argument.
A fixed nonzero-response fiber is not a stacking group. These facts do
not determine the microscopic product rephasing or justify setting any
missing differential or twister to zero. Keep numerical result files
separated by their response restrictions and spin conventions.
