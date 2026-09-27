# Formula convention used by the independent calculation

The native engine computes cochains and their quotient classes. It never reads
the boss's or collaborator's space-group answer tables. GAP/HAP supplies the
space group and a free resolution; the comparison maps, exact linear algebra,
obstruction evaluation, and stacking reduction belong to this project.

## Physical layers and arithmetic

For a three-dimensional spatial problem the state is
`(n1, n2, n3, nu4)`: integer p+ip, binary Majorana chain, binary complex fermion,
and an additive phase in R/Z. The background is `(omega2, s1)`. The present
230-space-group calculation uses `omega2=0` and the binary orientation
character `s1`, defined by `(-1)^s1(g)=det(g)`.

The parameter `p` in the Majorana formulas is the degree of the **Majorana**
cochain (1 or 2). The parameter in the p+ip formulas is the degree of the
**integer** cochain (1 for the three-dimensional spatial problem). These are
different degree conventions.

All binary sums are reduced before a canonical integer lift is taken. Signed
integer cup products retain their interval-cut signs. Exact integer divisions
are checked. The obstruction and product formulas use integer numerators
modulo 8 or 16; solved phase primitives are general exact rational cochains
modulo one and need not have those denominators. A negative integer carry
uses floor division. Floating-point phase arithmetic is absent.

For a possibly nonclosed cochain define

`S^j(u) = u cup_(deg(u)-j) u + u cup_(deg(u)-j+1) du`.

Negative cup indices mean zero. The second summand is essential for nonclosed
upper decorations. The twisted phase differential is `d_s = d - 2 s cup`.

## Closed Majorana sector

The parity equation is

`dc = Sq^2(a) + omega2 cup a + s1 cup Sq^1(a)`.

The total obstruction is expressed in the CA coordinate:

`O(a,c) = 1/2 [S^2(c) + omega2 cup c] + gamma(a)`.

The full `gamma` and the full products `U3,U4`, including all antiunitary and
extension terms, are independently transcribed in `fspt/formulas.py`.
`majorana_product(a,b,s)` is

`m = a cup_(p-1) b + s cup (a cup_p b)`.

Stacking gives `N=a+b`, `C=c+cprime+m`, and
`nu_new=nu+nuprime+U(a,c,b,cprime)`. The supplied six-block decomposition
(`GW`, Bockstein, Adem, omega, s, omega-s) is retained in the algebraic code.
Neither analytic phase evaluates a microscopic phase lookup table.

The physical operator coordinate differs by
`Gamma(c)=1/2 c cup_(p+1) dc`. Both obstruction and product must be changed:
`O_op=O_CA+d_s Gamma`, `U_op=U_CA+Delta Gamma`. Comparing just an obstruction
representative is insufficient to compare a stacking law.

The supplied source-matching certificate also contains a closed unary phase
`Z`: `E_repo-U_CA=Delta B+Delta Z+d_s C`. It must not be silently dropped.
The earlier `s P(a)/4` coordinate correction is already accounted for in the
current manuscript normalization and is not appended a second time.

## Integer p+ip layer

In 3+1 dimensions the lower equations are

```
d_s n1 = 0                    over Z
dn2 = omega2 n1 + s1 n1^2      over F2
dn3 = O4(n1,n2)                over F2.
```

Set `h=floor(n1/2) mod 2`, `u=n2+s1 h`, and `W=omega2+s1^2`. The native short
source used in both Python and GAP is

```
O4 = S^2(u) + omega2 u + s1 S^1(u)
   + zeta_(2,1)(W,n1)
   + (W cup_1 W + s1 W) h
   + [(W cup_1 W) cup_1 s1 + s1 (s1 cup_1 W)] n1.
```

Binary occurrences of `n1` mean its parity. The four-factor operation is the
literal word `123134` with inputs `(W,W,n1,n1)`. This is the native short
representative, not the uniform higher-dimensional expression differing by an
unrecorded coboundary.

The terminal O5 is the **complete** phase, comprising the CF square, the
nonclosed Majorana continuation, p+ip--Majorana mixing, and the pure integer
phase. The continuation uses
`beta_open(u)=(d lift(u)-lift(du))/2`; the closed-cochain Bockstein is invalid
for this input. The pure term includes its fixed `y5`, the Cartan carry lifted
as one bracket, and the sixteenth-valued twisted Pontryagin contribution.

`fspt/formulas_pip_compile.py` compiles the supplied explicit cochain
specification into a finite scalar program. It specializes **only omega2=0**;
it does not specialize `n1=s1`, choose one Majorana primitive, discard integer
carries, or replace a higher obstruction with an `s1^2` survival criterion.
The compilation retains the EZ completion and all relevant coefficients of
the fixed 55-coefficient Y5 polynomial. The generated program has 7,239 scalar
operations. Runtime evaluation imports no vendor Python code and performs no
new primitive solve for Y5.

For the canonical torsion representative `n1=s1`, the complete formula also
has an exact faster specialization:

`O5(s1,B,C) = S^2(C)/2 + gamma_open(B) + 9 s1^5/16`.

Here `h=0`, the pure parity `Xi(s1)` vanishes, and the pure integer phase is
the pullback `9 s1^5/16`. Both pullback statements have been checked on every
local sign simplex against the unchanged supplied evaluator. `gap/pip_o5_sign.g` evaluates the resulting 935 scalar
instructions directly; `AFSPipO5` dispatches there only when its actual integer
callback is `ctx.s`. The general formula remains available. The generic and
specialized expressions agree on 512 independent local towers, including
256 legal towers and 256 unrestricted binary Majorana/CF inputs.

The mathematical source is the root `p_ip_d4_normalized.tex` in the supplied
bundle, especially the low-dimensional complete assembly and Sections 8--9.
The `latex/` fragments are historical provenance. The final physical
normalization theorem has a stated relative finite-group scope; numerical
closure and formula agreement do not broaden that theorem by themselves.

## Obstruction quotients and gauge witnesses

A nonzero value for one lower primitive does not establish a nonzero AHSS
differential. The classification driver adjusts the Majorana primitive by the
full relevant cohomology space when solving d3, and projects d4 into the
quotient by the CF and Majorana-secondary images. This is performed on the
complete source, not separately on its displayed summands.

The incoming lower-dimensional Majorana gauge has state
`(a2=0, c3=P(a1), nu4=O4(a1,0))`; its twisted phase boundary equals
`O5(0,P(a1))`. If `dc2=P(a1)`, composing it with the CF gauge gives a phase
differing from `O4(a1,c2)` by `1/2 P cup_2 P`. This difference is the explicit
boundary `d_s[1/2 S^1(c2)]`. Both the cohomology comparison and the cochain
witness are therefore retained in the stacking reduction.

The full p+ip formula at zero integer input uses an open-Majorana continuation
whose raw phase is not identical to the closed-Majorana CA phase. Their exact
complete-tower dictionary is

`O_pip(0,B,C)-O_CA(B,C) = d_s[D0(s,B)+lift(Sq^2 B)/4+s cup C/2]`.

Here `dB=0` and `dC=Sq^2 B+s Sq^1 B`. The quarter-valued local cochain `D0` is recorded in
`fspt/data/pip_zero_mc_coordinate.json` and independently constructed by `tests/derive_pip_zero_mc_coordinate.py`,
which solves all 32,768 local closed-B equations and checks 128 complete
legal towers. This justifies comparing their secondary cohomology classes
while keeping their raw phase cochains separate.

The native pure-CF construction also retains its comparison correction.
Let `C` be closed, with zero Majorana and extension inputs, and let `nu0`
be the bar image of the phase seed obtained from the native higher diagonal.
Agreement of native and bar Steenrod operations in cohomology does not mean
their raw vectors agree. The reconstruction in `AFSReconstructNativeCFLift`
therefore solves

```
rho5 = [2 (O_bar(0,C) - d_s nu0)] mod 2,
dh4 = rho5,                 over F2,
nu4 = nu0 + h4/2,          modulo one.
```

The half-integrality and solvability of this comparison source are checked.
The resulting lift obeys the actual bar equation `d_s nu4=O_bar(0,C)`.
Its correction cancels pointwise under doubling, since `2nu4=2nu0` modulo
one. The native seed alone is not identified with the corrected bar phase.

## Primitive free integer generators

For a unitary character the complete tower `(n1,0,0,0)` is flat. For a signed
character, pullback of the universal infinite-dihedral tower proves survival
of `2n1`. The surviving free lattice is therefore determined by the joint
free/torsion parity classes in `H^1(G,Z_s)/2H^1(G,Z_s)`. A reduced echelon
basis of their surviving free projection, together with `2e_j` in nonpivot
columns, gives an integral lattice basis. Each chosen row retains its actual
torsion shift and a full flat tower. The proof and implementation scope are
in [FREE_PIP_LATTICE.md](FREE_PIP_LATTICE.md).

The corrected v07 campaign has completed all 230 classification checkpoints;
all 44 groups with nonzero free p+ip rank export these actual bases and towers
under `pip.free_lattice`. This is stronger than the abstract free rank in
earlier development files. It does not assert completion of all stacking
calculations or a full comparison-support audit of all 230 groups.

## Runtime API

Load `gap/formula_data.g`, `gap/pip_o5_program.g`, and `gap/formulas.g`.
Loading `gap/formula_fast.g` and `gap/pip_o5_sign.g` enables the exact
straight-line specializations.
The factory is `AFSFormula(name, ctx, inputs)`, where `ctx.G` is the actual GAP
group and `ctx.s` its binary character. It returns a variadic normalized bar
cochain; `AFSMemo` is used when the independent backend is loaded.

| name | inputs, besides `p` | output |
|---|---|---|
| `majorana_source` | `a` | binary degree p+2 |
| `majorana_product` | `a,b` | binary degree p+1 |
| `obstruction` | `a,c` | rational degree p+3, denominator 8 |
| `stacking` | `a,c,b,cp` | rational degree p+2, denominator 8 |
| `pip_majorana` | integer `n` | binary degree p+2 |
| `pip_parity` | integer `n`, Majorana `b` | binary degree p+3 |
| `pip_obstruction` | `p=1`, integer `n`, `b` of degree 2, `c` of degree 3 | rational degree 5, denominator 16 |

Except for the compiled `pip_obstruction`, an explicit `w` callback can supply
nonzero omega2. An omitted `w` means zero. `pip_obstruction` currently accepts
only the omega2=0 specialization. `AFSCup(i,p,a,q,b)` provides a mod-two higher
cup for stacking gauge manipulations. Callers must supply valid lower towers.

## Checks and their limits

`tests/test_formulas.py` checks the twisted closure and stacking identities on
independently generated local lower towers, compares to the supplied analytic
oracle, and checks the incoming gauge dictionary. `tests/test_formulas_pip.py`
compares native parity and the compiled complete O5 to the unchanged supplied
public evaluator on signed integer and `n1=s1` inputs. `tests/test_formulas.g`
checks the GAP runtime against 26 exact Python fixtures, including both the
straight-line and expression-graph evaluators. Real native-resolution
lower primitives for the six disputed space groups are separately exported
by `tests/test_pip_spacegroup_samples.g` and replayed through the supplied
oracle by its Python companion.

These are new arithmetic and integration checks. Universal coefficient and
physical normalization certificates supplied in the archives remain separate
evidence; their presence is not described as a fresh independent proof.

The supplied manuscript-aligned stacking formulas set p+ip to zero. The
torsion p+ip extension uses the collaborator's calibrated mathematical product
as an additional formula input, independently evaluated in the universal local
cochain coordinates described below. Final space-group tables remain
comparison data, never runtime inputs.

## Torsion p+ip coordinate dictionary and integer gauge

These formulas use `normalized-pip-aw-edge-transport-v2`, the exact per-edge
transport in the supplied scalar formula. The correction and its phase-gauge
witness are recorded in [AW_TRANSPORT_CORRECTION.md](AW_TRANSPORT_CORRECTION.md).

For `n=s`, the normalized CF cochain and the collaborator's reference CF
cochain obey `C_ref=C+Lambda`, where on an ordered tetrahedron

`Lambda = B013 + B012 B013 + B012 B023 + B013 B023`.

This satisfies `dLambda=Q_native+Q_ref`. The upper phases differ by the
explicit unary rephasing

`T1 = D4(s,B) + s^4/4 + 1/2 [C cup_2 Lambda + Lambda cup_3 Q_native]`,

with `O_ref(s,B,C+Lambda)-O_native(s,B,C)=d_s T1`. The universal local
cochain `D4` is stored in `fspt/data/pip_upper_coordinate.json`: its index
consists of four sign cone edges and six Majorana cone faces. These 1,024
entries are exact fractions modulo 16. This retained base table was solved
before the per-edge AW transport correction; the explicit `s^4/4` term
converts it to the supplied coordinate. The complete corrected dictionary
passes all 32,768 legal local five-simplex equations. Its entries are
coefficients of a cochain, with no target-group classifications involved.
`tests/derive_pip_upper_coordinate.py --verify-current` verifies this stored
base plus its correction against the mathematical oracle. Without that flag
the script solves a new table directly in the corrected coordinate; such a
table must replace the complete `D4+s^4/4`, not only `D4`. Additional tests compare complete
legal towers to the unchanged scalar reference evaluator.

The doubled output has `n=2s,B=0`. In precisely this sector,
`Lambda2=s^3` and

`T2(C) = -3/16 s^4 + 1/2 C cup_2 s^3`.

It obeys the analogous upper-phase dictionary. This statement is deliberately
restricted to `B=0`; the unrestricted closed-B formula has not been used.

The integer gauge removing `2s` is constructed directly from the supplied
normalized O5. Let `t` be the cylinder height zero-cochain and let `K` be
the standard prism contraction to the bottom face. Choose

```
n_I = 2s + d_s t,   B_I = s cup t cup dt,
C_I = pull(C) + K Q_native(n_I,B_I).
```

The two endpoints have `(n,B)=(2s,0)` and `(0,0)`. The top CF cochain is
`C+s^3`, and the prism integral of the full O5 is a fixed phase `g4(s,C)`.
Thus `(2s,0,C,V)` and `(0,0,C+s^3,V+g4)` represent the same state. The
phase is `13/16 s^4+1/2 P`, where `P` is the binary polynomial recorded as
`INTEGER_GAUGE_ANF` in `fspt/pip_coordinates.py`. The cylinder lower equations
and the resulting phase identity have been checked on all 32,768 legal
five-simplex states by `tests/derive_pip_integer_gauge.py`.

For a diagonal reference product with output CF cochain `beta` and phase
correction `Gamma_ref`, its exact normalized lower-sector square is therefore

```
CF_square = beta,
V_square = 2V + 2T1 + Gamma_ref - T2(beta+s^3) + g4(beta+s^3).
```

This formula retains the closed phase of the chosen reference product; it
does not select an extension by solving an arbitrary target-group residual.
The runtime callbacks are in `gap/pip_coordinates.g`, with its universal
data in `gap/pip_coordinate_data.g`. `tests/test_pip_coordinates.py` also
checks the doubled-sector bridge against 32 unchanged scalar reference
evaluations and exports 96 exact cross-language callback fixtures.

The reference diagonal has now been independently evaluated on all 16,384
legal local four-simplex states and compiled as a universal degree-four
operation, also represented by 579 exact multilinear terms modulo 16.
`tests/test_pip_stacking_review.py` checks the complete composed square on
256 random legal five-simplices, including the incoming Majorana gauge's
phase, and verifies normalization on all 471 degenerate local towers.
The full marked-group driver in `gap/pip_stacking.g` uses all Majorana
secondary images to obtain a flat upper lift, re-evaluates its nonlinear
obstruction after changing lower cochains, and reduces the resulting square
against the same marked lower generators used in their own relations.

These checks establish the implemented diagonal identities and gauge
transport. The reference product's chosen closed terms remain a calibrated
mathematical input; these calculations are not a separate proof of all of
its higher coherence identities.
