# How the first 4+1D calculations are certified

The calculated fields are `(e2,n2,n4,nu5)`, with E8 first. The cyclic and
signed C2 algorithms below are complete for their stated backgrounds. They
do not constitute a general intrinsic-row solver or a universal physical
identification of the four-data theory. Reference targets and their precise
symmetry structures are recorded separately in [BORDISM_TARGETS.md](BORDISM_TARGETS.md).

## Internal commuting cyclic symmetry

For `U(1)^f × C_N`, set `s=rho=omega=0`. Let `a` be the integer residue
cochain and `x=da/N`. The canonical roots, in the stated field order, are

\[
X=(x,0,0,ax^2/(3N)),\qquad
Y=(0,x,0,ax^2/(6N)),
\]
\[
Q=(0,0,x^2,\zeta_{22}(x,x)/2),\qquad
b=(0,0,0,ax^2/N).
\]

Here `zeta22` is the implemented integral Cartan completion. It must be
retained even when its final cycle pairing vanishes. The identities
`da=Nx`, `dx=0` and the integral Cartan identity prove the full source
equations. Nonvacuous degree-six checks also test the implementation.
The roots and their physical dictionary are specified in the supplied
[v0.15 Appendix K](../../../formulas/v015_reference/manuscript/appendices/K_cyclic_proof.tex),
equations `v14:roots` and `v14:physicalcharacters`.

The algorithm computes each root's Nth power with the adopted coupled
product, removes exact E8/CI sheets by their actual gauges, removes the
required charge root, and applies the remaining charge gauge. All lower
fields then vanish. The residual phase is closed and is paired with

\[
\Gamma_5=\sum_{i,j=0}^{N-1}[g\mid g^i\mid g\mid g^j\mid g].
\]

Terms containing the identity vanish in the normalized complex. This
cycle generates `H5(C_N,Z)=Z_N`, and `H^5(C_N,R/Z)=Z_N`; the phase root
has pairing `1/N`. Therefore the pairing determines the **entire phase
class**, including its coefficient in each root relation. A zero pairing
proves that the residual phase is a coboundary. This method does not
produce an explicit full-bar primitive and does not claim one.

There are no additional incoming sheet/charge cohomology classes because
`H^1(C_N,Z)=H^3(C_N,Z)=0`. The terminal target `H^6(C_N,R/Z)` vanishes.
The four completed roots cover the four `Z_N` filtration layers; their
complete power relations determine the stacking group. The retained
cycle ledger contains every term, every lower gauge and its shared-phase
correction. See [the cyclic method](../../formulas/FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md)
and [cyclic4p1.py](../../../insulator/cyclic4p1.py).

## Independent physical lattice comparison

[cyclic_physical.py](../../../insulator/cyclic_physical.py) computes the
eta characters directly in the rational group ring `Q[C_N]`. It evaluates
the specified electronic anomaly theories on lens spaces and on
`S1 × CP2`. For even N, the lens structure is specified as the canonical
complex-induced Spin-c structure twisted by `lambda^p`; its determinant
alone would not specify the structure uniquely.

The code constructs the full integer kernel

\[
K=\ker\bigl(\mathbb Z^4\longrightarrow(\mathbb Q/\mathbb Z)^{N+1}\bigr)
\]

by successive exact Bezout lattice intersections. It does not use the
cochain relation matrix to construct K. Only afterward are their column
Hermite normal forms compared, in the fixed `X,Y,Q,b` dictionary. Thus
the comparison tests the actual relations and generator identification,
not merely equal abstract Smith factors.

Independently, the reduced Spin-c bordism AHSS in total degree five has
entries `(p,q)=(5,0),(3,2),(1,4)`, of total order at most `N^4` because
`Omega0=Omega2=Z`, `Omega4=Z²` and the relevant odd coefficients vanish.
The character image has exactly that order. It therefore saturates the
bordism bound and is faithful and complete. The reduced degree-six
bordism has no rational part. The project proof is
[v0.15 Appendix K](../../../formulas/v015_reference/manuscript/appendices/K_cyclic_proof.tex),
equations `v14:etamatrix` and `v14:etaD` and the following order argument.

The external inputs are the structured interacting-phase and low
coefficient results of [Freed–Hopkins v6, Theorem 9.87 and Corollary 9.89](https://arxiv.org/abs/1604.06527v6),
and the lens/product eta input of [Bahri–Gilkey (1987), Lemmas 2.2–2.3](https://doi.org/10.2140/pjm.1987.128.1).
Bahri–Gilkey Theorem 0.1 also supplies a separately published cyclic
**2-power** classification. The all-N physical dictionary and complete
presentation are the supplied project's proof; they are not attributed
to an external all-N table. No free-band classification supplies a target.

For this direct product, forgetting C_N has the trivial-C_N-action
section. Consequently the full physical answer adds `Z{I} ⊕ Z{J}` to the
relative group. This independently justified section is recorded
separately from the cochain run. It is not an implemented general
intrinsic solver and does not extend automatically to signed backgrounds.

## Signed C2: complete canonical and incoming quotient

There is exactly one normalized nondegenerate C2 simplex in each degree.
A cochain is one scalar and its differential is

\[
d_\chi:C^p\longrightarrow C^{p+1},\qquad
d_\chi=(-1)^\chi+(-1)^{p+1}.
\]

[The signed solver](../../../insulator/signed_charge_conjugation_4p1.py)
evaluates the actual source, product and joint gauges on this complete
complex. It solves the integer equation before the phase equation and
retains all inequivalent phase completions. Put `k=0,1` for
`omega=k alpha²/2`. The arbitrary-integer gauge quotient is exhausted as
follows, not merely sampled with small parameters:

* For H+/H-, `s=0,rho=alpha`. The sheet gauges change `e,n` by `2v,2u`.
  Normalize both to `0,1` and solve the charge equation. Between these
  canonical representatives a residual transformation has `v=u=0`.
  The remaining closed charge parameter is any integer `w=m`, with
  `Delta nu=(k+1)m/2 mod 1`. Its unit generator includes every residual
  incoming action. H+ has k=0, obstructs odd CI and removes the phase
  root; H- has k=1 and retains the two sheets and phase.
* For AI/AII, `s=alpha,rho=0`. Closed integral sheets vanish. Every
  charge transformation is `q -> q+(k-1)u+2w`; every phase is removed by
  the surjective signed phase gauge `d4=-2`. For AI the unit CI parameter
  removes charge parity. For AII the terminal source already rejects
  odd charge. The intrinsic-zero group therefore vanishes in both cases.

Every ordered product of canonical states and every residual incoming
action on every state is retained. The solver checks quotient
compatibility, associativity, commutativity, inverses, and equality of
the presentation order with the exhaustive quotient order. It also
retains nonclosed unit and joint lower gauges. The residual formulas
above justify arbitrary integer completeness; finite probes alone would
not provide that proof.

The H- calibration in supplied
[Appendix J](../../../formulas/v015_reference/manuscript/appendices/J_physical_tests.tex),
equations `eq:Hminus-spin06` through `eq:bordism-minus06`, is a **derived**
Smith-sequence calculation. Its primary inputs are
[Smith v2, Theorem 5.1 and Corollary 5.8](https://arxiv.org/abs/2405.04649v2),
[Freed–Hopkins v6, Theorem 9.87](https://arxiv.org/abs/1604.06527v6), and
the explicit tangential twist in
[Debray–Ye–Yu v2, Proposition 6.27](https://arxiv.org/abs/2312.13341v2).
The other H+ twist gives its distinct target. AI/AII use the interacting
columns of FH Corollaries 9.95/9.93. Their full uniform responses are
separate from the intrinsic-zero calculation.

These finite calculations do not settle the unrestricted terminal
`R5/K4` comparison or justify a finite-group argument for infinite space
groups. Those scope boundaries remain explicit even when every stated
case passes its independent physical calibration.
