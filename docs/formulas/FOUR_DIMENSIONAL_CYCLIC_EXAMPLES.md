# 4+1D computed examples: internal cyclic symmetry

The accepted calculations cover the orders listed in the
[current cyclic tables](../../results/current/4p1d/internal_cyclic/intrinsic_zero.md)
for a unitary internal `C_N` commuting with `U(1)^f`.
Their backgrounds are exactly `s=rho=omega=0`.
The original four-data model is ordered `(e_2,n_2,n_4,nu_5)`. A cyclic
label here does not specify a crystalline rotation or physical spin lift.

The results are separated into [zero intrinsic response](../../results/current/4p1d/internal_cyclic/intrinsic_zero.md)
and [all intrinsic responses](../../results/current/4p1d/internal_cyclic/intrinsic_all.md).
The [accepted calculation lineage](../../results/current/4p1d/README.md#accepted-calculation-lineage)
retains the complete presentations and physical comparisons. The accepted
nontrivial cases agree with the entire independent eta
character kernel in the specified physical-root dictionary, not just its
Smith factors. The all-intrinsic table additionally uses the uniform
section proved below.

## Cohomology, obstructions, and incoming completeness

For `N>1`,

```math
H^2(C_N,\mathbb Z)=H^4(C_N,\mathbb Z)
 =H^5(C_N,\mathbb R/\mathbb Z)=\mathbb Z_N,
\qquad H^6(C_N,\mathbb R/\mathbb Z)=0.
```

The integer source vanishes identically because `B3=rho=0`. The terminal
target vanishes, so both sheet roots and the charge root admit phase
completions. Closed incoming sheet and charge parameters are classified
by `H^1(C_N,Z)=H^3(C_N,Z)=0`; there is no additional incoming
cohomology class to quotient. Their exact representatives are covered by
the full cochain gauges. The four filtration layers each have order `N`,
so the completed presentation has order `N^4`. This order alone does not
determine the stacking extensions. For `N=1` the relative group is zero.

## Canonical completed roots

Write group elements as `g^j`, `0<=j<N`, and use the integer cochains

```math
a(g^j)=j,\qquad
x(g^i,g^j)=\left\lfloor\frac{i+j}{N}\right\rfloor,
\qquad da=Nx,\qquad dx=0.
```

In E8, CI, charge, phase order the roots are

```math
\begin{aligned}
X&=\left(x,0,0,\frac{a x^2}{3N}\right),&
Y&=\left(0,x,0,\frac{a x^2}{6N}\right),\\
Q&=\left(0,0,x^2,\frac12\zeta^{\mathbb Z}_{2,2}(x,x)\right),&
b&=\left(0,0,0,\frac{a x^2}{N}\right).
\end{aligned}
```

The Cartan identity supplies the phase completion of `Q`: its differential
is the charge source, with the two `x^3` terms cancelling modulo two.
The integer identities `da=Nx`, `dx=0`, the Cartan identity, and the full
source/product/gauge identities justify these constructions globally.
The retained six-simplex checks test the implementations of those identities;
they are not presented as an enumeration of all bar six-simplices.

The calculation forms every `N`th power using the complete product,
removes its sheets by the actual joint gauge, extracts and removes the
charge root, and evaluates the remaining closed phase. Every step retains
its induced higher fields and phase correction.

## Complete powers and detection of the shared phase

The normalized cyclic five-cycle is

```math
\tau_5=\sum_{i,j=0}^{N-1}[g\mid g^i\mid g\mid g^j\mid g].
```

Terms containing an identity vanish, leaving `(N-1)^2` evaluations.
This cycle generates `H_5(C_N,Z)=Z_N`. Since `R/Z` is divisible,
the pairing identifies `H^5(C_N,R/Z)` with its character group;
`b(tau5)=1/N`. Thus evaluation on the **whole cycle** determines the
remaining phase class exactly.

For each cycle term the solver constructs the canonical cochains,
computes the complete powers, removes sheets with `v=-a` or `u=-a`,
and removes a remaining charge multiple `kN x^2` with `w=-k a x`.
It checks that all lower fields vanish before taking the final pairing.
The raw case records, identified by the provenance paths in the
[machine-readable index](../../results/current/index.json),
retain the intermediate states, actual gauges, phase corrections, source
checks, and cycle contributions. A zero pairing proves a phase boundary
here; the cycle method does not claim to construct a full bar primitive.

With `r_N=binom(N,2) mod N`, the computed relations have the form

```math
NX=q_Xb,\qquad NY=r_NQ+q_Yb,\qquad NQ=r_Nb,\qquad Nb=0.
```

Here `q_X,q_Y` are measured after the complete reductions just described.
In the generator order `(X,Y,Q,b)`, the retained row lattice is

```math
L_N=\operatorname{rowspan}_{\mathbb Z}
\begin{pmatrix}
N&0&0&-q_X\\
0&N&-r_N&-q_Y\\
0&0&N&-r_N\\
0&0&0&N
\end{pmatrix}.
```

For `C2`, `2X=0`, `2Y=Q+b`, and `2Q=b`: the CI root has order eight,
giving `Z2 × Z8`. For `C3`, `3X=b`, `3Y=2b`, and `3Q=0`, giving
`Z3² × Z9`. For `C15`, `15X=5b`, `15Y=10b`, and `15Q=0`, giving
`Z5 × Z15² × Z45`. The two sheet sectors share `b`; multiplying
independently classified E8 and CI sectors would lose these relations.

There is also an analytic neutral check. The carry cocycle `x` is binary,
and `x cup_1 x=0` over integers: closure equates the sums of the two
binary pairs in `x(023)x(012)-x(013)x(123)`, hence their products.
The neutral self-products therefore have no twister. After removing
`Nx` with `v=-a`, the phase is

```math
\frac{a x^2-N^2x^2a}{3}.
```

Both ordered monomials pair to one with `tau5`, so

```math
q_X=\frac{N(1-N^2)}3\bmod N
 =\begin{cases}N/3,&3\mid N,\\0,&3\nmid N.\end{cases}
```

The independent GAP resolution implementation and its native phase
primitives provide a further control at `C2,C3,C4`. A valid relation
requires its residual phase to be exact, not to vanish as a cochain.

## Independent physical generators and the complete relation kernel

The reviewed [v0.15 Appendix K](../../formulas/v015_reference/manuscript/appendices/K_cyclic_proof.tex)
gives a physical calculation using Spin-c bordism and electronic anomaly
theories. In this paragraph only, let `R=lambda-1` in the representation
ring of an auxiliary circle. Let `A_q(V)` denote the anomaly theory of
odd-charge `q` Weyl fermions in a virtual auxiliary representation `V`;
negative coefficients denote inverse phases. Its physical roots are

```math
\begin{aligned}
X_\eta&=\mathcal A_1(9R-3R^2+2R^3)-\mathcal A_3(R),\\
Y_\eta&=\mathcal A_1(R-R^2+R^3),\\
Q_\eta&=\mathcal A_1(R^2-R^3),\qquad
b_\eta=\mathcal A_1(R^3).
\end{aligned}
```

The auxiliary circle is restricted to `C_N`. The charge-three term is
an allowed composite-electron response; these generators do not assert
a free-band classification. Their index polynomials, in this order, are

```math
\frac{x^3-xp_1}{3},\qquad
x\left(\frac{f^2}{2}-\frac{p_1}{24}\right)-\frac{fx^2}{2}+\frac{x^3}{6},
\qquad fx^2,\qquad x^3.
```

Here `f` is the electric curvature class, `x` the auxiliary first Chern
class, and `p1` the tangent first Pontryagin class.
These fix the electric and thermal leading responses and the chosen
lower-layer convention independently of the cochain calculation.

Let `L_p=L^5(N;1,1,1)` carry the canonical complex-induced Spin-c
structure twisted by `lambda^p`. Its determinant is `(3+2p)x`; the
determinant alone would not specify the structure for even `N`.
Let `P=S^1 × CP^2` have unit cyclic holonomy and determinant `h` on
`CP^2`. In the common anomaly sign, their eta evaluations are

```math
\begin{array}{c|cccc}
 &X_\eta&Y_\eta&Q_\eta&b_\eta\\\hline
L_p&\dfrac{2(N^2-1)}{3N}
 &\dfrac{N^2-6N+5+6p(p+2-N)}{12N}
 &\dfrac{2p+N+3}{2N}&\dfrac1N\\[5pt]
P&-\dfrac1N&0&0&0
\end{array}\pmod1.
```

The [physical evaluator](../../insulator/cyclic_physical.py) independently
reconstructs the lens entries using exact arithmetic in `Q[t]/(t^N-1)`:

```math
D_N(t)=\sum_{j=0}^{N-1}\frac{N-1-2j}{2N}t^j,\qquad
(1-t)D_N=1-\frac1N\sum_{j=0}^{N-1}t^j.
```

For odd charge `q`, auxiliary weight `z`, and structure `p`, it takes the
constant coefficient of `t^((3q+3)/2+qp+z) D_N^3`, then forms the stated
virtual representations. No cochain root relations or expected Smith
factors enter this calculation. It finds the exact integral kernel

```math
K_N=\ker\left[\mathbb Z^4\xrightarrow{(L_0,\ldots,L_{N-1},P)}
 (\mathbb Q/\mathbb Z)^{N+1}\right]
```

and compares its Hermite normal form with `L_N`. Every accepted nontrivial
case satisfies **`L_N=K_N`**.

Completeness has an independent order certificate. The low Spin-c
coefficients are `Omega_0=Z`, `Omega_2=Z`, `Omega_4=Z²`, and zero in
odd degrees through five. The total-degree-five bordism AHSS therefore
bounds the relative group order by `N^4`, from bidegrees `(5,0)`, `(3,2)`,
and `(1,4)`. The four rational eta rows `(L_0,L_1,L_2,P)` have determinant
magnitude `N^-4`, forcing the character image to have order at least
`N^4`. The bounds coincide. Reduced degree-six bordism has no rational
part, so there is no additional relative free response.

The physical proof holds for every positive `N`. With
`g2=gcd(N,2)` and `g3=gcd(N,3)`, its relative group is

```math
\mathbb Z_{N/(g_2g_3)}\oplus\mathbb Z_{N/g_2}
\oplus\mathbb Z_N\oplus\mathbb Z_{g_2^2g_3N},
```

omitting `Z1`. Its all-`N` presentation follows from the integral
representation-ring relation `(1+R)^N=1` and the vanishing of the
degree-five anomaly of `R^4`; Appendix K gives the unimodular physical
basis change and Smith calculation. The complete **cochain-to-physical
relation comparison** covers the orders actually listed in the accepted
tables; it is not inferred for an uncomputed order.

External sources have distinct scopes. [Freed–Hopkins, Theorem 9.87 and
Table 9.88, v6](https://arxiv.org/abs/1604.06527v6) supplies the interacting
bordism framework and coefficient groups. [Bahri–Gilkey (1987),
Theorem 0.1(b) and its following Remark](https://doi.org/10.2140/pjm.1987.128.1)
gives a published cyclic **2-power** comparison for the accepted powers of two;
its Lemmas 2.2–2.3 give eta input. [Hsieh (2018), §2.3,
v1](https://arxiv.org/abs/1808.02881v1) provides related eta arithmetic
for a different finite charge symmetry. The all-`N` formula above is the
reviewed project derivation, not an all-`N` result attributed to either
paper. Exact source-specific targets are recorded in the
[bordism reference ledger](../4p1d/calibration/BORDISM_TARGETS.md) and its
[additional targets](../4p1d/calibration/BATCH2_TARGETS.md).

## Uniform intrinsic pair and its natural section

The extra 4+1D coefficient row is the pair `(n0I,n0J)`, separate from
`(e_2,n_2,n_4,nu_5)`. With `c=2f` the Spin-c determinant class, its
integral response basis is

```math
I=\frac{c^3-cp_1}{48},\qquad J=\frac{c^3}{2}.
```

For this direct-product symmetry, let `p:U(1)^f × C_N -> U(1)^f`
forget `C_N`, and let `i` insert its identity. Pullback gives
`i* p*=id`. Thus assigning trivial `C_N` action to either uniform root
defines a natural group section of the restriction map, and

```math
\mathcal C^{4+1}(U(1)^f\times C_N)
 \cong\ker i^*\oplus\mathbb Z\{I\}\oplus\mathbb Z\{J\}.
```

The all-intrinsic table uses exactly this section. Substitution into the
reviewed opened-sheet equations at `s=rho=omega=0` gives `B3=0` and
allows `e2=n2=n4=nu5=0` for either unit intrinsic root. This is a direct
zero-input check plus the physical section argument; it is not an
execution of a general opened-intrinsic cochain solver. The pair is not
the scalar uniform IQH coefficient used in 2+1D. No analogous canonical
section is assumed for charge-conjugating, time-reversing, projective,
or general crystalline backgrounds.

## Reproduction and scope

Run the [exact cyclic driver](../../scripts/classify_cyclic_4p1.py) on an
idle compute node with a new output directory:

```bash
python3 scripts/classify_cyclic_4p1.py --order 16 --order 32 --order 64 --jobs 3 --timeout 1800 --evidence-format json-gzip --output NEW_DIRECTORY
```

Repeated `--order N` options specify the exact orders for a new campaign;
the example above selects three powers of two. Omitting them selects the
runner's bounded default set. Compressed evidence retains every exact
cochain value and gauge witness. The runner saves computed cochain results before the independent
physical comparison, so a disagreement preserves the mathematical
evidence. Acceptance additionally verifies source/input/evidence hashes
and the integer presentation independently.

The implementation caches exact source, product, and gauge evaluations
with complete cochain and symmetry keys. The bounded reference comparison
checks literal equality of every retained classification and witness:

```bash
python3 scripts/benchmark_cyclic_4p1.py --order 3 --order 6 --output NEW_BENCHMARK.json
```

The cyclic engine uses the Python standard library and the repository's
exact operation arrays. GAP is needed only for the separate resolution
controls. Raw model records keep their universal physical-certification
flag false; `physicalComparison` records the stronger, **family-specific**
kernel certificate. That certificate does not construct a universal
terminal CI comparison or a general global 4+1D classifier.

The other accepted signed backgrounds are documented separately:
[unitary charge conjugation](../../results/current/4p1d/charge_conjugation.md)
and [AI/AII at zero intrinsic response](../../results/current/4p1d/time_reversal_intrinsic_zero.md).
Their complete gauge calculation and distinct physical comparison scope
are given in [Signed C2](../4p1d/calibration/SIGNED_C2.md).
The separate [abelian-product calculation](../4p1d/calibration/ABELIAN_PRODUCTS.md)
adds mixed cohomology and incoming classes, including independent coprime
product controls of cyclic groups. The [translation calculation](../4p1d/calibration/TRANSLATIONS.md)
treats infinite groups using their complete finite classifying spaces.
