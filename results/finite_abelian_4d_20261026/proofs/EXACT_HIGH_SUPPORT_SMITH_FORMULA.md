# Exact nonsplit blocks with at least two spectator factors

Derivation, 26 October 2026.
The cyclic base and one-spectator block require separate calculations.

## Scope and stable decomposition

Let the fermionic group be
\(\mathbb Z^f_{2m}\times\prod_i\mathbb Z_{N_i}\), with every order a power
of two and \(m\geq2\). The parity twist is the mod-two reduction \(y_0\) of
the degree-two integral generator of the distinguished \(\mathbb Z_m\).
Stable splitting in the spectator factors gives an actual direct sum over
spectator subsets. There are no extensions between distinct stable summands.
Only subsets of at most five spectators can contribute in spacetime degree
five.

On a chosen subset of \(r\geq2\) spectators, there is no integral degree-two
class. There is also no surviving Majorana class: the kernel of
\(\mathrm{Sq}^2+y_0\) on degree-three mod-two cohomology of the whole product
is exactly the span of \(x_i y_0\). Each such monomial involves at most one
spectator. Thus the chosen block has only complex-fermion and bosonic layers.
It can be computed without either terminal p+ip formula.

## Finite matrices, defined for all cyclic orders

Set \(N_0=m\). In degree \(n\), use the basis of tuples

\[
\alpha=(\alpha_0,\ldots,\alpha_r),\qquad
\sum_j\alpha_j=n,\quad \alpha_0\geq0,\quad\alpha_j\geq1\ (j>0).
\]

This is the cellular basis of the tensor product of the cyclic periodic
resolutions, restricted to the chosen spectator support. The integer
coboundary matrix \(D_n\) is given explicitly by

\[
D_ne_\alpha=
\sum_{j:\,\alpha_j\ {
m odd}}
(-1)^{\alpha_0+\cdots+\alpha_{j-1}}N_j e_{\alpha+e_j}.
\tag{1}
\]

Every \(D_n\) is zero mod two. Identify the mod-two basis element with
\(\prod_j x_j^{[\alpha_j]_2}y_j^{\lfloor\alpha_j/2\rfloor}\), where
\(x_j^2=\epsilon_j y_j\) and \(\epsilon_j=[N_j/2]_2\). Define the binary
matrix \(T_n\) of \(\mathrm{Sq}^2+y_0\) by

\[
T_ne_\alpha=e_{\alpha+2e_0}
+\sum_j[\lfloor\alpha_j/2\rfloor]_2e_{\alpha+2e_j}
+\sum_{i<j}\epsilon_i\epsilon_j[\alpha_i]_2[\alpha_j]_2
 e_{\alpha+e_i+e_j}.
\tag{2}
\]

Repeated entries are added mod two. These matrices depend on the number of
factors and their orders, not on a list of group elements or a bar resolution.

Take an integer Smith decomposition

\[
U D_5 V=\operatorname{diag}(s_1,\ldots,s_t,0),\qquad s_i>0.
\tag{3}
\]

The matrices \(U,V\) are unimodular. Let \(U_\perp\) denote the rows below
the nonzero diagonal. Choose binary column vectors \(f_a\) representing a
basis of

\[
\ker_{\mathbb F_2}(U_\perp T_4)\big/\operatorname{im}_{\mathbb F_2}T_2.
\tag{4}
\]

For \(r=2\), the one degree-two Majorana gauge direction is
\(x_1x_2\); its primary image \(T_2(x_1x_2)\) must be quotiented in (4).
For \(r>2\), degree two has no supported basis elements. There is no
secondary Majorana incoming contribution, since the degree-two kernel of
\(T_2\) on these supports is zero.

Define the following integer coefficients, reducing them modulo \(s_i\)
when desired:

\[
q_{ij}=\frac{s_i}{2}(V^{-1}T_3)_{ij},\qquad
p_{ia}=[(UT_4f_a)_i]_2.
\tag{5}
\]

The first expression is integral. The full block has the finite abelian
presentation with generators \(v_i\) and \(F_a\):

\[
s_i v_i=0,\qquad
\sum_iq_{ij}v_i=0,\qquad
2F_a=\sum_i p_{ia}v_i.
\tag{6}
\]

Thus (1)--(6) are a direct, finite integer-matrix formula for arbitrary
exponents. No undetermined differential or extension remains in these
blocks. The Smith form of (6) gives the full group. Its size is bounded by
the fixed spacetime dimension: for support two the presentation has at most
eight generators; for support three it has at most eight; the larger supports
are smaller still.

## Why the presentation includes the physical extension

A binary degree-four class \(f\) has obstruction
\(T_4f/2\). Equation (3) shows that it is a U(1) coboundary precisely when
\(U_\perp T_4f=0\) mod two. For such a class choose its phase primitive
\(\nu_5\), in the Smith coordinates, to have entries

\[
(V^{-1}\nu_5)_i=\frac{[(UT_4f)_i]_2}{2s_i}\quad(i\leq t).
\]

Twice this primitive has the bosonic coordinates \(p_{ia}\) in (5).
The complex-fermion self-stacking contribution is
\(\mathrm{Sq}^1f/2\). Its U(1) cohomology class is zero: it is the image
of a Bockstein reduction and is represented here by \(D_4f/4\).
Consequently the last relation in (6) gives the actual group extension.

The bosonic generators from (3) have orders \(s_i\), and the incoming
complex-fermion obstruction on a degree-three gauge cochain is
\(T_3/2\). Its Smith coordinates are exactly \(q_{ij}\), producing the
middle relation in (6). Transporting the cochain operation from a bar
resolution can add half of a binary coboundary; this changes the primitive
by a half-valued cochain and cannot change its doubled U(1) class.

The implementation is `../supercohomology_blocks.py`. It checks the chain
identities, exactness over the rationals, integrality of (5), and containment
of the Majorana primary image in the complex-fermion kernel.

## Closed factors for two spectators

Write \(N_1\leq N_2\), \(g=N_1\), and omit factors of order one. The
Smith reduction of (6) gives the following compact cases:

\[
\begin{array}{c|c}
\text{Condition}&\text{Full support-two block}\\\hline
g=N_2\leq m&
\mathbb Z_{g/2}^{\,3}\oplus\mathbb Z_g^{\,2}\oplus\mathbb Z_{2g}\\
g<N_2,\ g<m&
\mathbb Z_{g/2}^{\,2}\oplus\mathbb Z_g^{\,2}\oplus\mathbb Z_{2g}^{\,2}\\
g<N_2,\ g=m&
\mathbb Z_{g/2}^{\,2}\oplus\mathbb Z_g^{\,3}\oplus\mathbb Z_{2g}\\
m<g=N_2&
\mathbb Z_{m/2}\oplus\mathbb Z_m^{\,3}\oplus\mathbb Z_{g/2}\oplus\mathbb Z_g\\
m<g<N_2&
\mathbb Z_{m/2}\oplus\mathbb Z_m^{\,3}\oplus\mathbb Z_{g/2}\oplus\mathbb Z_{2g}.
\end{array}
\tag{7}
\]

The raw bosonic group is \(\mathbb Z_g^2\oplus\mathbb Z_h^4\), with
\(h=\min(m,g)\). For \(g\leq m\), its incoming quotient is
\(\mathbb Z_{g/2}^3\oplus\mathbb Z_g^3\) when the spectator orders agree,
or \(\mathbb Z_{g/2}^2\oplus\mathbb Z_g^4\) otherwise. For \(g>m\), it
is \(\mathbb Z_{m/2}\oplus\mathbb Z_m^3\oplus\mathbb Z_{g/2}^2\) when
they agree, or
\(\mathbb Z_{m/2}\oplus\mathbb Z_m^3\oplus\mathbb Z_{g/2}\oplus\mathbb Z_g\)
otherwise. There is one complex-fermion generator, and a second precisely
when \(g<N_2\) and \(g<m\). Their doubling relations give (7).

## Closed factors for three spectators

Let \(g=\min_iN_i\) and let \(\delta=1\) if this minimum occurs exactly
once, or zero otherwise. Then

\[
\begin{cases}
\mathbb Z_{g/2}\oplus\mathbb Z_g^{\,6-\delta}
 \oplus\mathbb Z_{2g}^{\,\delta},&g\leq m,\\
\mathbb Z_m^{\,3}\oplus\mathbb Z_g^{\,4-\delta}
 \oplus\mathbb Z_{2g}^{\,\delta},&g>m.
\end{cases}
\tag{8}
\]

The raw bosonic group is \(\mathbb Z_g^4\oplus\mathbb Z_h^3\),
\(h=\min(m,g)\). The only incoming degree-three direction is
\(x_1x_2x_3\). Its obstruction has order two exactly when \(g\leq m\),
and is zero when \(g>m\). In the former case the quotient halves one of
the seven order-g factors.

The degree-four kernel is zero unless one spectator order is uniquely
smallest. If \(N_i=g<N_j,N_k\), its generator is \(y_i x_jx_k\).
An explicit primitive is

\[
\nu_5=\frac{X_i(Y_i+Y_0)X_jX_k}{2g}.
\]

Here capitals denote the integral cellular representatives with
\(dX_i=N_iY_i\). The remaining coefficients in its differential are
integers because \(N_j,N_k\) are divisible by \(2g\). Its double contains
a primitive spectator bosonic class of order g, so it replaces one
\(\mathbb Z_g\) by \(\mathbb Z_{2g}\). The other candidate
\(x_0x_1x_2x_3\) is excluded by the full Bockstein constraint in (4).

## Checks and status

The matrix formula independently reproduces every archived nonsplit
support-two and support-three result in
`../data/archived_51.json`, including
the extra \(\mathbb Z_4\) in the \(m=4,N_1=2,N_2=4\) block that the
cubic charge-only presentation misses.
The closed factors (7)--(8) also agree with the full matrix formula on
all exponent patterns from one through four; broader parameter checks
are maintained in the accompanying verification script.

The general result is the explicit matrix presentation (1)--(6). The closed
forms (7)--(8) are its compact evaluation. Neither is inferred from the old
finite-group classification tables; those tables are independent checks.

The all-exponent reduction of (7)--(8) is certified separately in
`ALL_EXPONENT_SMITH_CERTIFICATE.md`. The integral Koszul basis reduces every
input to one of 16 or 40 exhaustive order signatures. Exact constant or
polynomial unimodular identities then establish the displayed Smith factors
for arbitrary exponent gaps. Thus the unbounded claim does not rely on the
finite parameter sweep.
