# All-exponent Smith proof for nonsplit supports two and three

This proves the closed factors for arbitrary powers of two.
Finite exponent sweeps are only implementation checks and are not used to
extend the result beyond the tested orders.

## 1. An explicit simultaneous Koszul basis

In the tensor periodic resolution, the integer differential preserves
\(k_i=\lceil\alpha_i/2\rceil\). For a fixed tuple \(k\), let \(I\) be its
positive coordinates. The corresponding cochain block is an exterior Koszul
complex on symbols \(e_i\), with \(de_i=N_i\). A wedge of \(q\) such symbols
has cochain degree \(2\sum_i k_i-q\).

Choose an index \(j\in I\) of minimum order \(h=N_j\), taking the first
such index when tied. The integral basis change

\[
z_i=e_i-(N_i/h)e_j\quad(i\ne j),\qquad de_j=h,\quad dz_i=0
\]

is unimodular. Thus every nonzero differential in this block is exactly
multiplication by \(h\), between \(e_j\wedge z_A\) and \(z_A\).
This is an explicit Smith basis for all orders, with no numerical Smith
decomposition or conjectured stabilization needed.

Modulo two, \(N_i/h\) is one precisely at the minimum-order indices.
Consequently every binary basis-change matrix depends only on the weak
ordering of the cyclic orders. The Steenrod operation adds only the flags
\(N_i=2\), through \([N_i/2]_2\).
There is no dependence on the size of a positive gap between exponents.

The code `../koszul_stabilization.py` computes these basis changes directly.
Its degree-five projection is contraction with the vector \(N_i/h\),
followed by deletion of the pivot index. Its degree-six zero-row projection
is the same contraction. The degree-six image coordinates are the original
wedge coefficients whose odd set does not contain the pivot.
These are exactly the three pieces needed for the bosonic incoming
relations, the complex-fermion obstruction, and the doubling relation.

## 2. Exhaustive signatures

A signature consists of all comparisons between the cyclic orders and the
flags indicating which are two. This is a finite logical partition of all
positive exponents, not a bounded numerical sample.

With \(r\) spectators, every signature has a representative using the
orders \(2,4,\ldots,2^{r+2}\): there are at most \(r+1\) distinct orders,
and one extra level allows the minimum to be greater than two.
The code deduplicates these representatives by their full signatures.
There are 16 signatures for two spectators and 40 for three spectators.
The representative values are used only to choose binary matrices; the
generator orders remain symbolic in the following reduction.

## 3. Removing the primitive lift relations

Let \(g\) be the smallest spectator order and \(h=\min(m,g)\).
For two spectators, the six raw bosonic factors have orders
\(g,g,h,h,h,h\). For three spectators, the seven raw factors have orders
\(g,g,g,g,h,h,h\).

The incoming bosonic relations have coefficients either zero or half of
the corresponding factor order. The complex-fermion doubling rows have
binary bosonic coefficients and a coefficient two on their own lift.
Their independent primitive bosonic entries permit ordinary unit row and
column elimination. This removes the lift rows and the same number of
bosonic columns, retaining six or seven generators respectively.
These operations are unimodular for all orders.

## 4. Two spectators: constant and polynomial identities

If \(g\leq m\), all six bosonic orders are \(g\). The reduced matrix is
\(g/2\) times a constant integer matrix determined by the signature.
Its normalized Smith diagonals are

\[
\begin{array}{c|c}
N_1=N_2=g\leq m &(1,1,1,2,2,4)\\
g<N_2,\ g<m &(1,1,2,2,4,4)\\
g<N_2,\ g=m &(1,1,2,2,2,4).
\end{array}
\]

If \(g>m\), write \(g/m=2t\). After extracting \(m/2\), the reduced
matrix is over \(\mathbb Z[t]\). Exact polynomial unimodular transformations
give the diagonals

\[
\begin{array}{c|c}
N_1=N_2=g &(1,2,2,2,2t,4t)\\
N_1=g<N_2 &(1,2,2,2,2t,8t).
\end{array}
\]

The matrices \(L(t),R(t)\) have determinant \(\pm1\) identically and obey
\(L(t)A(t)R(t)=\operatorname{diag}(d_i(t))\), with any extra rows zero.
The displayed diagonal entries divide the next entries for every positive
integer \(t\). Specializing to any power-of-two ratio is therefore valid.
This proves all five cases of the two-spectator formula for unbounded
exponents.

## 5. Three spectators

The binary kernel has one complex-fermion lift precisely when the minimum
spectator order occurs once. Write this indicator as \(\delta\).
For \(g\leq m\), factoring out \(g/2\) gives the constant Smith diagonal

\[
(1,\underbrace{2,\ldots,2}_{6-\delta},
 \underbrace{4}_{\delta}).
\]

For \(g>m\), the incoming bosonic row is zero. Put \(g/m=2t\) and factor
out \(m\). Polynomial unimodular transformations give

\[
(1,1,1,\underbrace{2t,\ldots,2t}_{4-\delta},
 \underbrace{4t}_{\delta}).
\]

These identities prove the three-spectator closed factors for every order.

## 6. Independently checkable receipts

`../data/support2_symbolic_certificates.json` and
`../data/support3_symbolic_certificates.json` contain the reduced matrix and its
left and right unimodular transformations for every exhaustive signature.
The script verifies the identities symbolically over \(\mathbb Z[t]\),
including determinant \(\pm1\), before writing the files.
No exponent bound enters these identities.

The certificates supplement the cochain derivation of the exact relation
matrix; they are not a substitute for that derivation.
The separate archived-result and exponent-grid checks remain useful for
detecting transcription or implementation errors.
