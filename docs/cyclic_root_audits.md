# Cyclic CI-root and gauge audits

These checks address the `S4` and `S6=C3i` point-group discrepancies without
using the GAP classification backend or changing a formula coefficient. They
establish the stacking groups of the supplied calibrated CI/charge/phase model.
They do not by themselves prove its microscopic identification with every
real-space block root in the comparison paper.

Run the independent certificate generator with:

```sh
python formulas/audits/cyclic_roots.py --output /tmp/cyclic-root-audit.json
python -m unittest discover -s tests -p 'test_formulas_cyclic_audits.py' -v
python -m unittest discover -s tests -p 'test_formulas_certificates.py' -v
```

The first command records the explicit charge primitive, phase completion,
periodic-cycle values and root relations. It uses only normalized bar cochains,
exact rationals, the calibrated local kernels and a small binary linear solve.

## Universal charge-gauge identity

For a closed integer charge cochain (n_p), a charge gauge (v_{p-1}), and
zero CI sheet, the joint cylinder representative and shorter CF representative
obey, for (p=3,4),

\[
 G^{\mathrm{cyl}}_{p+1}-G^{\mathrm{CF}}_{p+1}
 =d_{s_1}\left[\frac12\bar n_p\cup_{p-1}\bar v_{p-1}\right]
 \pmod1.
\]

This is an explicit coboundary, rather than merely a closed difference or an
assumed incoming identification. It applies after a root's CI sheet has been
removed. The assertion here is restricted to closed charge and zero sheet.

For the rational part, parameter-first prism integration of
(\omega_2(n_p+d(\eta v_{p-1}))) gives (\omega_2v_{p-1}): normalization and
the Alexander–Whitney cuts leave the single path with the height jump between
the two factors. The coefficient transport agrees with the cup product.
For the half-valued part all sign actions disappear modulo two. On the cylinder,
(\bar n^I=\bar n+d(\eta\bar v)), so the required identity is

\[
 \mathcal I_1 Sq^2(\bar n^I)
 =Sq^2(\bar v)+\bar n\cup_{p-1}d\bar v
   +d(\bar n\cup_{p-1}\bar v).
\]

`test_closed_charge_cylinder_gauge_has_explicit_exact_difference` verifies this
identity coefficient by coefficient in the universal Boolean polynomial ring,
with 14 independent bits for (p=3) and 20 for (p=4). The charge is a universal
closed cochain and the gauge parameter is arbitrary. This proof uses no random
fitting. Separate local tests retain independent signs and rational extensions.

## C4: the CI root squares to the nonzero phase root

Write group elements as (a\in\{0,1,2,3\}), with addition modulo four, and set

\[
 \alpha(a)=a\bmod2,\qquad
 \beta(a,b)=\left\lfloor\frac{a+b}{4}\right\rfloor,
 \qquad s_1=r_1=\alpha,\quad\omega_2=0.
\]

All products of displayed scalar functions below are ordinary products of their
inhomogeneous values. A complete CI root is the parity pullback of the certified
C2 AIII root:

\[
 x=(n_1,n_3,\widehat\nu_4)
   =\left(\alpha,0,-\frac{\alpha(a)\alpha(b)\alpha(c)\alpha(d)}{16}\right).
\]

Its calibrated square, followed by sheet gauge (u_0=1), has

\[
 n_1=0,\qquad n_3=\alpha(a)\alpha(b)\alpha(c),\qquad
 \widehat\nu_4=\frac{\alpha(a)\alpha(b)\alpha(c)\alpha(d)}4.
\]

The charge is exact on C4. The normalized integer gauge below has rows and
columns indexed by (a,b=1,2,3):

\[
 v_2=\begin{pmatrix}0&-1&0\\0&1&1\\1&0&0\end{pmatrix},
 \qquad d_{r_1}v_2=-\alpha(a)\alpha(b)\alpha(c).
\]

The last identity is checked on all 27 normalized triples. After this gauge the
lower decorations vanish. Evaluate the remaining phase on the standard cyclic
periodic generator

\[
 F_4=\sum_{i,j=1}^{3}[g^i\mid g\mid g^j\mid g].
\]

The result is (1/2\pmod1) for each of the following paths:

1. Full sheet cylinder followed by full charge cylinder.
2. Full sheet cylinder followed by the shorter CF charge gauge.
3. One joint cylinder with parameters ((u_0,v_2)=(1,v_2)).

For sign coefficients, the cyclic periodic differentials alternate between
(-2) and zero. Thus (H^4(C_4;U(1)_{s_1})=\mathbb Z_2), detected faithfully by
this period. The closed differences between the three paths are exact. There
are no incoming classes available to erase the nonzero period:

\[
 H^2(C_4;\mathbb Z_{r_1})=0,
 \qquad H^0(C_4;\mathbb Z_{s_1})=0.
\]

An independent charge generator is (q_3(a,b,c)=\alpha(a)\beta(b,c)). The audit
constructs its exact quarter-valued phase completion and checks its source
equation on all 243 normalized five-tuples. Its square is removed with
(v_2=\beta), since (d_{r_1}\beta=-2q_3); the residual phase period is zero.
Taking (b) as the nonzero pure phase root gives

\[
 2b=0,\qquad 2q=0,\qquad 2x=b,
 \qquad\mathcal G_{\mathrm{retained}}=\mathbb Z_2\oplus\mathbb Z_4.
\]

The discrepancy with the paper is therefore an extension relation, not a
different count of surviving layers. Its S4 discussion labels the CI root as
order two; the present audit finds its nonzero completed square. Gauge-path
choice and the GAP resolution do not account for this difference.

## C6: a split restriction forces an order-eight root

For (C_6=\langle g\rangle), again take (s_1=r_1=\mathrm{parity}) and
(\omega_2=0). The homomorphisms

\[
 p:C_6\longrightarrow C_2,\quad p(g)=t,
 \qquad j:C_2\longrightarrow C_6,\quad j(t)=g^3
\]

preserve the complete symmetry background and satisfy (p\circ j=\mathrm{id}).
Naturality of the source, product and gauge formulas gives
(j^*p^*=\mathrm{id}) on complete state classes. Consequently the parity
pullback of the certified C2 AIII root of order eight still has order eight.

The signed periodic maps are (-2) and (1-1+1-1+1-1=0). The three retained
coefficient groups are (H^1(\mathbb Z_{s_1})=\mathbb Z_2),
(H^3(\mathbb Z_{r_1})=\mathbb Z_2), and
(H^4(U(1)_{s_1})=\mathbb Z_2), with zero incoming gauge groups in degrees zero
and two. Their total order is eight. Together with the injected complete root,
this forces (\mathcal G_{\mathrm{retained}}=\mathbb Z_8).

The comparison source is [arXiv:2204.13558](https://arxiv.org/abs/2204.13558),
Table II and its S4/S6 root discussions. The exact conclusions above leave a
disagreement with the published extension assignments. Resolving the physical
root correspondence is separate from reproducing that table; no coefficient
or equivalence relation has been changed to fit it.
