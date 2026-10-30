# 4+1D translations: the complete integer kernel and stacking law

The calculation applies to `U(1)^f × Z^r`, `1 <= r <= 4`, with
`s=r=omega=0`. Rank four is the full translation subgroup in four spatial
dimensions. Lower ranks describe partial translations in the same spatial
dimension. Pure translations have no rotation-spin lift distinction.
The four fields are ordered `(e2,n2,n4,nu5)`, and the intrinsic pair `(n0I,n0J)`
is recorded separately. Integer atomic filling is retained.

## Finite classifying space and obstruction equations

The solver uses the simplicial set

\[
K_r=(\Delta[1]/\partial\Delta[1])^r\simeq T^r=B\mathbb Z^r.
\]

Its normalized degree-`p` simplices are sequences of `p` nonempty, pairwise
disjoint subsets of the `r` coordinates. The first and last faces remove a
subset; an inner face merges two adjacent subsets. This is a complete
finite classifying space, not a finite truncation of the group bar complex.
For rank four its nondegenerate cell counts are
`(1,15,50,60,24,0,0)` in degrees zero through six.

The solver constructs every integer coboundary matrix from these faces.
For each degree it retains a Smith factorization with unimodular left and
right matrices. It then proves, over integers, the direct decomposition

\[
\ker d_p=\langle a_{i_1}\cup\cdots\cup a_{i_p}\rangle_{\mathbb Z}
\oplus d_{p-1}\langle\text{retained integer gauge basis}\rangle_{\mathbb Z}.
\]

Here `a_i` is the integral coordinate-one-cocycle. Antisymmetrized coordinate
cycles give primitive dual periods. A second unimodular matrix gives an
explicit integer gauge correction for **every** closed cochain, not just a
rational decomposition or a cohomology rank.

The adopted obstruction equations become

\[
de_2=dn_2=0,\qquad dn_4=0,\qquad
d\nu_5=e_2^3/3+\widehat O_6^{\rm CI}(n_2,n_4).
\]

There are no degree-five or degree-six simplices when `r<=4`. Thus the
integer obstruction target, the terminal source target, and the phase
cochain module are genuinely zero on this classifying space. This is a
dimensional argument about the complete space, rather than setting an
unknown differential to zero. The degree-two and degree-four integral
cocycles still have their full, nonzero coboundary and gauge matrices.
The local source API is also evaluated on every top simplex for every
retained root.

## Stacking and its integral straightening

The phase twisters have degree five and therefore evaluate in the zero
cochain module. The integer CI product does **not** vanish:

\[
(e,n,q)\star(f,m,t)=(e+f,n+m,q+t+n\smile m).
\]

The solver evaluates the actual adopted `integer_product` on every
degree-four simplex for every ordered pair of primitive CI sheets. For
each resulting four-cocycle it retains the complete integer charge gauge
that brings it to the primitive-period representative. An independent
certificate verifier reconstructs its Alexander–Whitney values and checks
the full gauge equation, not only the resulting invariant factors.

On primitive periods the product is the exterior product. In rank four,
write `n=sum_(i<j) n_ij a_i a_j`. The nonzero transverse products give

\[
\frac{n\wedge n}{2}
=\left(n_{12}n_{34}-n_{13}n_{24}+n_{14}n_{23}\right)a_1a_2a_3a_4.
\]

In particular this half-square is integral; it is not a division of an
arbitrary integer cochain by two. The explicit new charge coordinate

\[
Q=[q]-\frac{[n]\wedge[n]}2
\]

is additive. The computed polarizer is symmetric with zero diagonal,
which proves integrality and the polarization identity for every integer
sheet, including negative coefficients. Thus `(e,n,q) -> (e,n,Q)` is an
integral bijection and group homomorphism. It proves the full stacking
group rather than assuming that the associated graded group splits.

The inverse and every integer power retain the nonlinear charge term:

\[
(e,n,q)^{-1}=(-e,-n,-q+n\wedge n),
\]
\[
(e,n,q)^k=(ke,kn,kq+\tbinom k2 n\wedge n),\quad k\in\mathbb Z.
\]

## Gauges and incoming identifications

The full lower gauge action at this background is

\[
e\mapsto e+dv_1,\quad n\mapsto n+du_1,\quad q\mapsto q+d\lambda_3.
\]

Every nonclosed unit parameter is checked with the public joint gauge API
on every top simplex. The retained unimodular decompositions quotient the
entire integer images. Closed parameters in `H1` and `H3` cannot change
primitive periods, and the possible phase correction has no degree-five
target. The independent phase gauge likewise acts on the zero phase
module. No residual finite incoming quotient is being discarded.

The resulting presentation has `2*binom(r,2)+binom(r,4)` infinite-order
generators and no relations. Their primitive coordinates give an explicit
isomorphism to a free integer lattice. The neutral E8, CI, and charge
filtration ranks are separately retained.

## Independent physical comparison and intrinsic section

The separate physical benchmark uses the stable torus splitting

\[
\Sigma^\infty T^r_+\simeq
\bigvee_{j=0}^r\binom rj S^j.
\]

Together with the interacting Spin-c coefficient groups `TP5=Z²`,
`TP3=Z²`, `TP1=Z`, and `TP4=TP2=0`, it gives full free rank
`2+2*binom(r,2)+binom(r,4)` and zero-uniform free rank
`2*binom(r,2)+binom(r,4)`. The coefficients come from
[Freed–Hopkins v6, Theorem 9.87 and Table 9.88](https://arxiv.org/abs/1604.06527v6).
The translation interpretation uses the crystalline equivalence framework
of [Thorngren–Else v6, §III.C](https://arxiv.org/abs/1612.00846v6).
This is a stable-splitting deduction from their results, not a printed
four-dimensional space-group table. See the separate
[source and structure ledger](BATCH2_TARGETS.md#translation-benchmarks).

The computed zero-intrinsic sector is:

| Translation subgroup | E8 rank | CI rank | Charge rank | Phase | Stacking |
|---|---:|---:|---:|---|---|
| Z | 0 | 0 | 0 | 0 | 0 |
| Z² | 1 | 1 | 0 | 0 | Z² |
| Z³ | 3 | 3 | 0 | 0 | Z⁶ |
| Z⁴ | 6 | 6 | 1 | 0 | Z¹³ |

The two uniform roots are pulled back along
`B(U(1)^f × Z^r) -> BU(1)^f`; forgetting translations is a retraction.
This independently gives a natural physical section with zero lower data.
Direct substitution of both unit intrinsic roots into the reviewed
background-zero equations agrees. The implementation therefore records
this physical section separately; it does not claim to implement a
general opened-intrinsic solver.

The physical comparison constrains the full free group here. It does not
prove the universal terminal CI source/product comparison, nor does a
torus calculation certify nontrivial finite holonomy or mixed
`Z^r × C_N` backgrounds.

## Reproduction and certificate scope

```bash
python scripts/classify_translation_4p1.py --output NEW_DIRECTORY
python -m unittest discover -s tests -p test_translation4p1.py
```

The runner writes immutable inputs, source hashes, exact simplicial
evidence, run timing, and the full presentation. `verify_certificate`
replays the saved unimodular identities, all primitive periods, and every
ordered CI-product gauge without computing a new Smith form or reading a
reference group. Corrupting a gauge witness or omitting a product causes
verification to fail.
