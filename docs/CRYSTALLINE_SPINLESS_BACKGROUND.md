# The crystalline spinless background

The convention is fixed by the supplied manuscript, preserved in
`reference/legacy_stacking_context/06_examples.tex:47–68`:

```
s_eff = s_crys + w1(V)
omega_eff = omega_crys + w2(V) + w1(V)(s_crys+w1(V)).
```

For spinless crystalline fermions, `s_crys=omega_crys=0`. Thus the new
calculation requires `s=w1(V)` and `omega=w2(V)+w1(V)^2`. This differs from
the accepted spin-half crystalline calculation, whose effective omega is
zero. The representation V is the actual linear representation of the
space group; translations remain in the group used for cohomology.

## An exact representative

`gap/crystalline_background.g` constructs the background without importing
SptSet. Given the actual rational point-group matrices R, set
`J(R)=det(R) R`. This is an oriented three-dimensional representation.
The splitting principle gives

```
w2(V tensor det(V)) = w2(V) + w1(V)^2.
```

Consequently the Spin double cover of J supplies the required Pin-minus
extension. In particular, a mirror and a proper twofold rotation square to
the central minus sign; spatial inversion squares to plus one.

The code forms the positive rational invariant metric `sum_R R^T R`,
diagonalizes it by rational Gram–Schmidt, and works in its exact
three-dimensional negative Clifford algebra. For each J(R), the equations
`q e_i = J(R)(e_i) q` determine a one-dimensional space in the even algebra.
The representative q has first nonzero coefficient one. Its Clifford norm
is strictly positive. Normalization by a positive square root would produce
a Spin element, but is unnecessary: the sign of the exact rational scalar
relating `q(R)q(S)` and `q(RS)` already gives omega(R,S).

Every pair is checked for scalar proportionality, every triple for the
cocycle identity, and all identity arguments for normalization. The finite
table is pulled back through the actual Pcp-to-point homomorphism. Table
lookups and memoized point indices are the only subsequent background cost.
This uses a finite point group to construct a background, not as a replacement
for the infinite affine symmetry in classification.

The interface is:

```
AFSInstallCrystallineBackground(ctx)  # installs raw ctx.omega2(g,h)
AFSCrystallineOmegaNative(ctx)        # optional cached F2 native vector
```

`ctx.crystallineBackground` retains the metric, rational spin representatives,
point multiplication and omega tables, and the projection. The installer
does not decide whether the pulled-back class is trivial on the full space
group. If that class is exact, a separately retained actual affine
trivializing one-cochain permits choosing the cohomologous zero extension
representative before any state construction. Tests in `tests/test_crystalline_background.g` passed on the allocated
compute node: every point group for SG1–230, all point-group pairs and
triples, all tested affine-generator projections, and native cocycle
closure for SG1, 2, 3, 6, 19 and 146. The task completed in 193.514 seconds;
this is a background-construction control, not a classification benchmark.
Exact source and log hashes are recorded in
`docs/validation_runs/crystalline_background.json`.

## A universal finite search bound for free integer decorations

The omega-zero unitary and infinite-dihedral free generators cannot simply
be reused at nonzero omega. There is, however, an exact universal bound.
The supplied normalized manuscript, `p_ip_d4_normalized.tex:833–850`, proves
the fixed-upper-layer identity

```
O5(n+8m,B,C) - O5(n,B,C) = (W cup W) cup [m]_2 / 2  mod 1,
W = omega + s^2,
```

for a signed integer cocycle m. At `n=16m`, both `[n]_2` and
`[floor(n/2)]_2` vanish. The first source and the complete native parity
source therefore vanish with `B=C=0`. Applying the displayed shift identity
twice gives `O5(16m,0,0)=O5(0,0,0)=0` pointwise. Thus

```
(16m, 0, 0, 0)
```

is an explicit flat tower for every background, and `16 H1(Z_s)` is contained
in the surviving subgroup. The corresponding assertion for `8m` does not
follow: its phase is `(W cup W) cup [m]_2 / 2`, which may be nonzero.
A finite search in the joint free/torsion quotient modulo sixteen is
therefore sufficient. A free candidate's terminal obstruction need not
have order two; the old order-two assertion must not be used for this search.

### Stronger existence bound for the actual tangent background

For the actual crystalline spinless background, eight times every signed
integer character already survives, although its phase need not vanish
pointwise. Let V be the real three-dimensional linear representation of
the affine group. Its action factors through the finite point group and

```
[W] = [omega+s^2] = w2(V).
```

The standard integral characteristic-class identity
`rho2(p1(V))=w2(V)^2` supplies an integral lift of `[W]^2`. Moreover
`p1(V)` is torsion: it is pulled back from positive-degree integral
cohomology of a finite group, which is annihilated by the group's order.
For any `m in H1(G,Z_s)`, the class

```
gamma = p1(V) cup m  in H5(G,Z_s)
```

is therefore torsion, and its mod-two reduction is `[W]^2 [m]_2`.
The cup product here includes the usual transport for local coefficients.
The shift-eight identity, with `B=C=0`, gives the closed terminal source

```
O5(8m,0,0) = (W cup W cup [m]_2)/2  mod 1.
```

To make exactness explicit, choose an integral twisted cocycle Gamma
representing gamma and a binary four-cochain lambda with
`d lambda = W cup W cup [m]_2 + rho2(Gamma)`.
Because gamma is torsion, choose a rational twisted four-cochain Q with
`d_s Q=Gamma`. For any integer lift of lambda,

```
nu = (Q + lift(lambda))/2  mod 1
```

satisfies `d_s nu=O5(8m,0,0)`. The possible sign changes in the lifted
lambda differential disappear modulo one after division by two. The
lower sources already vanish at `n=8m,B=C=0`, so this is an actual
existence proof of a complete flat tower and of
`8 H1(G,Z_s)` being contained in the surviving subgroup.

This improves the bound for the finite-holonomy tangent representation;
it is not a theorem for arbitrary unrelated omega. It does not justify
using `nu=0`, nor remove the need to construct a phase primitive when
exporting a marked generator. The current generic search keeps its
universally valid sixteen-period bound and tests the eight candidate
before that fallback. In this physical background a final index sixteen
would contradict the stronger theorem and must be investigated. We do
not assert a four-period theorem: the displayed shift-eight identity
alone gives no control of the additional lower-bit and Pontryagin
carries at `n=4m`.

There is also a representation-theoretic reason that the nonzero
background search only needs free rank one. Over the rationals,
`H1(G,Q_s)` is the multiplicity of the determinant representation in
`V*`. If that multiplicity is at least two, every proper point operation
fixes two independent vectors and therefore all three. Every improper
operation acts as minus one on those two vectors and, by its determinant,
also on the third. Thus the point group is contained in `{I,-I}` and the
multiplicity is three. For both those representations `w2(V)+w1(V)^2=0`;
the implementation selects the zero-background branch. Hence a genuinely
nonzero tangent background with a free integer layer has rank one.

## Incoming integer gauges and the first torsion square

For `s=0`, `H0(G,Z)=Z` contributes incoming integer-layer operations.
The first sends k to `k omega` in the Majorana layer. Quotienting by this
image alone can miss the CF and bosonic images of its kernel.
The supplied `latex/01_low.tex` is a degree-one-input O5 formula, despite
its filename; it does not directly print the required degree-zero tower.
Existing full formulas can instead construct the gauge by an interval
cylinder. With height t, take `n_I=-d_s(t k)` and successively apply the
contraction to the bottom to its primary, parity and phase sources. Each
bottom value is zero. The endpoint has zero integer component for `s=0`,
and Majorana component `k omega`. Lower endpoint gauges must be retained
when extracting the subsequent incoming images. Their phase coordinates
must agree with the CA convention of the lower stacking model. The
construction below obtains this full incoming subgroup directly in CA
coordinates, without evaluating that cylinder at runtime.

The same cylinder explains a diagnostic for signed torsion, conditional on
the supplied first product. The source
`reference/legacy_stacking_context/05b_pip.tex:107–137` explicitly calls

```
E2(n,n') = [n]_2 cup [n']_2 + s cup([n]_2 cup1 [n']_2)
```

a proposed product: its closed cup-product term is not determined by the
obstruction identity. We use it as mathematical input. Closure checks do
not independently prove its unique physical normalization.

Here is the resulting leading-square calculation at the cochain level.
For the canonical torsion input `n=n'=s`, the degree-one cup-one product is
pointwise multiplication, so `s cup1 s=s` and `E2(s,s)=0`. The doubled
state therefore has integer component `2s` and zero Majorana component
before removing its integer gauge. On an interval cylinder, let t be the
integer vertex height, zero at the bottom and one at the top, with s and
omega pulled back from the group. Set

```
n_I = -d_s t,
a_I = [n_I]_2 = dt,
B_I = omega cup t + s cup (t cup dt).
```

On an edge, `n_I(ij)=t_i-(-1)^s_ij t_j`; thus its bottom restriction is
zero and its top restriction is `2s`. All terms in the following identity
are binary cochains. Since `ds=domega=d(dt)=0`, the ordinary cup-product
Leibniz rule gives

```
dB_I = omega cup dt + s cup(dt cup dt) = primary(n_I).
```

The bottom Majorana restriction is zero; the top restriction is omega
because `t=1` and `dt=0` there. Subtracting this integer-gauge cylinder
removes `2s` from the doubled state and changes its binary Majorana
component to omega. There is no additional first-product correction in
this subtraction, since both integer cochains being added are even.
Consequently

```
Majorana projection of 2P = [omega].
```

The equality is in the final Majorana quotient, and does not assert the
vanishing of the lower CF or phase coordinates. Changing the chosen full
lift P by a lower state L changes its square by `2L`, whose Majorana
projection is zero. For nontrivial s, `H0(G,Z_s)=0`, so the unitary integer
incoming subgroup discussed below is absent. The cylinder's higher
coordinates are genuine gauge data; the leading calculation does not
supply those coordinates or an actual full upper witness.

A nonzero projection often determines the abstract extension, but does
not universally do so. The remaining CF and bosonic coordinates are
irrelevant to the abstract group only when every allowed class in the
corresponding fiber of `H_lower/2H_lower` gives the same Smith invariant
factors. A complete marked upper witness still needs the actual cochain
relation even in that algebraically unambiguous case.

### What naturality can fix, and what still needs an input

There is just one cohomological closed-term ambiguity in a normalized
natural first product depending on the two signed integer cocycles and
s. To see this, use their universal group
`U=Z^2 semidirect C2`, where the involution reverses both integer
coordinates. Let a and a' be the two coordinates modulo two. The
Lyndon–Hochschild–Serre filtration bounds the dimension of
`H2(U,F2)` by `1+2+1=4`. The four classes

```
s^2, s a, s a', a a'
```

are independent: restrict to the four order-two subgroups generated by
`(u,v,1)`, for `u,v in {0,1}`. Their restrictions are the four functions
`1,u,v,uv` times the generator of `H2(C2,F2)`. Hence those classes form a
basis without assuming a spectral-sequence collapse. Requiring the
difference between two products to vanish when either integer input is
zero removes the first three classes. Only `a a'` remains. Allowing an
independent background omega uses the universal space
`BU x K(F2,2)`. Since `H1(K(F2,2),F2)=0` and its degree-two cohomology
is generated by omega, the Künneth formula adds exactly the omega class
and no mixed degree-two term. Restricting either integer input to zero
leaves omega unchanged, so identity normalization excludes that
input-independent term. This argument concerns natural first products
on the stated input data, up to a Majorana coboundary; it does not
classify arbitrary higher cochain products or prove their coherence.

The subgroup with `u=v=1` detects the remaining bit. For `C2` with
nontrivial sign and `omega=s^2`, the independently evaluated lower CA
model has `H_lower=Z8`, with its Majorana class represented by an odd
generator. The supplied first product gives an odd square of P and
therefore `Z16`. Adding the alternative closed term `a a'` makes that
square even; no such extension can have an element of order sixteen.
Thus an **independent physical or mathematical input** that this theory
has strong `Z16` fixes the first product's cohomology class and its
leading-square rule. This is a conditional uniqueness argument, not a
derivation of that physical input from the obstruction. In particular,
the finite control below uses the supplied first product and cannot
circularly serve as an independent calibration of it.

Such a separately stated normalization is already present in the supplied
materials: `reference/legacy_stacking_context/tables_point_groups.tex:57`
gives the spinless crystalline mirror `Cs=C1h` four `Z2` layers and total
`Z16`. The caption at line 89 identifies the table with the left panel of
Table III of `Zhang25_PRX_point`, and `06_examples.tex:75` describes that
source as a real-space block-state construction. We record this as a
provided reference input; we have not rederived that construction here.
The collaborator checkout also reports `(s,omega)=([1],[1])`, package
degree four, as `Z16` in `doc/extension-paper-comparisons.md:112–119`,
with explicit measured relations at lines 137–153. The latter is a
separate implementation comparison, not by itself an independent
physical derivation. Neither reference group was used as an input to
the finite-control calculation.

## The complete unitary incoming cyclic subgroup

`gap/pip_incoming_background.g` exports
`AFSBackgroundIncomingState(ctx) -> rec(a,c,v)` and rejects nonunitary
groups. Its generator is the actual flat CA state

```
X = (omega, 0, F(omega)).
```

The choice of its CF component is a supplied unary normalization, not a
consequence of solving the phase equation with that component fixed. For
the positive integer gauge generator and its nonnegative multiples, the
provided `source/lib/ss_fermion.gi:66–76` in the stacking bundle specifies
the MC component `n0 omega` and the CF component
`floor(n0/2) (omega cup1 omega)`. In particular `n0=1` has CF component
zero. The supplied repo-to-CA dictionary changes only the top phase and
keeps the lower `(a,c)` coordinates fixed; see
`note/stacking_note.tex:94–120` and `README.md:27–54` in that bundle.
Thus this normalization still gives `C=0` in the CA coordinate. We use
these as mathematical inputs; the independent runtime loads no old
SptSet implementation. The old callback's literal `Int` agrees with floor
for the nonnegative inputs cited here; its negative-input behavior is
not used to define inverses in the independent calculation.

The normalized universal four-cochain F is determined by exact equations
on the closed background:

```
dF = O_CA(B=omega,C=0; background omega,s=0)
2F + U_CA(omega,0;omega,0) = -P(omega)/8,
P(omega) = lift(omega) cup lift(omega)
           + lift(omega) cup1 d lift(omega).
```

The even-input calibration is the literal `R0(A=2,b=0)` in the supplied
collaborator checkout's `python/low_phases.py`, with its stated Pontryagin
sign convention. This is an explicit mathematical input, not an external
space-group answer. Closure alone would not fix the incoming subgroup.
The independently transcribed full-background CA obstruction and product
are used to derive F. `tests/derive_pip_incoming_background.py` solves and
checks every one of the 1,024 local closed-omega five-simplices, all 64
four-simplex square equations, and all 23 degenerate four-simplex states.
The resulting 64 rational coefficients are a universal cochain formula.

The remaining phase ambiguity in this fixed-CF normalization is also checked. After fixing the square,
any two F differ by a normalized half-valued closed four-cochain. In this
universal local cochain model that space
has dimension four over F2: three exact directions and the class
`omega^2/2`. The latter is exactly `8X` as a phase class. Thus all solutions
give the same cyclic incoming subgroup: changing X by `8X` replaces its
generator by `9X`, and exact changes are gauges.
This does not assert that closure or the square calibration alone uniquely
fixes every possible natural CF component. For example, the actual state
`3X` has CF component `Sq1(omega)` and generates the same cyclic subgroup;
we do not infer a statement about that CF component combined with an
arbitrary uncalibrated phase.

Writing `r=(d lift(omega)/2) mod 2`, the retained literal powers are

```
2X = (0, r, -P/8)
4X = (0, 0, -P/4 + (r cup2 r)/2)
8X = (0, 0, -P/2)
16X = 0.
```

The fourth-power correction has an explicit phase gauge:
`r cup2 r = d eta`, where on `[0123]`
`eta=(1-omega012) omega013 (1-omega023)` modulo two. Its 64 local equations
are checked separately. `AFSBackgroundIncomingPowers` retains all five
states, the Pontryagin cochain and `eta/2`. Quotienting the full marked lower
group by this single actual state X therefore includes the incoming d2,
d3 and d4 together; the graded layers must be extracted from the resulting
filtered presentation. This does not justify quotienting only by `[omega]`
and leaving the old CF and bosonic quotients unchanged.

### A geometric order bound, not a vanishing theorem for incoming d4

For a unitary three-dimensional crystalline group, the actual representation
V is oriented and has rank three. The characteristic-class identity is
`P(w2(V))=rho4(p1(V))`. The rank-three condition matters: the corresponding
general higher-rank identity can have a `2 w4` term. As above, finite
point-group holonomy makes `p1(V)` torsion.

Choose an integral four-cocycle Gamma representing `p1(V)`, a mod-four
three-cochain lambda with `d lambda=P(omega)-Gamma mod4`, and a rational
three-cochain Q with `dQ=Gamma`. The fourth power in the retained CA
coordinate has the explicit primitive

```
4X phase = -P(omega)/4 + d eta/2
         = d[-(Q+lift(lambda))/4 + eta/2] mod1.
```

Thus the actual incoming element has order dividing four in this physical
background, before imposing the cyclic incoming quotient. This explains why
orders two and four have a geometric basis, rather than being merely a
sixteenth-valued formula cutoff. It is not an assertion about arbitrary
unrelated omega.

The order bound does **not** imply that incoming d4 vanishes. If `2X` has
trivial CF class after the allowed CF and MC-incoming gauges, its remaining
bosonic class could still have order two; `4X=0` only kills its double.
Triviality in that filtered CF quotient is also weaker than ordinary
cochain exactness of the raw `Sq1(omega)`. Accordingly, any statement that
incoming d4 vanishes for all 230 computed groups must cite the actual
cyclic-quotient filtration certificates, not this structural bound alone.


## Finite controls at nonzero background

`tests/compute_finite_c2_nonzero_background.g` runs the same independent
resolution, classification and CA stacking machinery on actual finite
`C2`, with `omega=chi^2` for its binary character chi. No expected group
invariant is passed to the calculation. The compute-node run completed in
19.058 seconds and checked its explicit success sentinel; hashes and
exact source snapshots are retained in
`docs/validation_runs/finite_c2_nonzero_background.json`.

| Sign action | Before integer incoming | Integer incoming | Final result |
|---|---|---|---|
| Unitary | The lower group is `Z2`, entirely Majorana | The actual state X generates that `Z2` | Trivial; all four graded layers vanish |
| Nontrivial | Each of bosonic, CF, Majorana and p+ip is `Z2` | `H0(Z_s)=0` | Lower group `Z8`; the full permitted upper Ext fiber has the unique abstract type `Z16` |

In the signed control the measured lower relations are
`2D=0`, `2C=D`, and `2B=C`. Thus the known leading square of P is an odd
multiple of the `Z8` generator, whatever its remaining CF/bosonic carry.
This explains the unique abstract `Z16` without choosing an uncomputed
upper phase. The export explicitly records `fullUpperPhaseWitness=false`.
The lower lifts and relations were checked on the backend comparison
supports. These two controls do not assert full affine classification,
a new proof of product coherence, or a complete marked upper cochain.
