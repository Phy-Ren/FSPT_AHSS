# 4+1D: E8, CI, charge, and the shared phase

The ordered fields are `(e_2,n_2,n_4,nu_5)`: neutral E8, CI sheet,
localized charge, and **one shared phase**. This page concerns that
four-tuple. Its AHSS operations are `d2`, `d3`, and `d4`; a subscript such
as `O6` specifies a cochain's degree, not an additional differential page.
The extra uniform pair `(n0I,n0J)` is recorded separately below; it is
not part of this tuple.

The operations and coefficient conventions are fixed in
[Operations](OPERATIONS.md). The two finite binary kernels are defined
by their [exact coefficient arrays](COEFFICIENTS.md). All formulas below
belong to one calibrated convention and use the actual lower outputs.

<a id="obstructions-4d"></a>

## Obstruction functions

Let `s` be the chirality sign, `rho` the charge sign, and
`B3=d_(rho+s)(omega_real-s1^2/2)` in the retained convention. Then

```math
d_s e_2=d_s n_2=0,\qquad
d_\rho n_4=-B_3\cup n_2-\rho_1\cup n_2\cup n_2,
```
```math
d_s\nu_5=e_2\cup e_2\cup e_2/3+\widehat O_6^{\rm CI}(n_2,n_4).
```

The neutral contribution is displayed first. To specify the CI term,
write `A2=check omega_R` and define the binary charge-conjugation block

```math
\begin{aligned}
\mathcal J_6(n_2)={}&\zeta_{1,4}(\rho,\bar n_2^2)
 +\rho^2\widetilde{(n_2^2)}
 +\rho\zeta^{\mathbb Z}_{2,2}(n_2,n_2)\\
&+[(\rho\cup_1s)\rho+(s^2\cup_1\rho)]\bar n_2^2.
\end{aligned}
```

The square inside the tilde is the actual signed integer cup square.
With `O5=-B3 n2-rho n2^2`, the complete terminal contribution is

```math
\begin{aligned}
\widehat O_6^{\rm CI}={}&\widehat O^c_6(n_4)
 +\frac12\mathcal P_{\rho+s}(A_2)n_2
 -\frac12 A_2\cup(n_2^2)_\rho\\
&+\frac14(\rho^2n_2^2)_s
 +\frac14(s)_{\rho+s}\cup\mathcal O_5
 +\frac16n_2^3\\
&+\frac12\left[
 \zeta^{\mathbb Z}_{3,2}(B_3,n_2)+\mathcal J_6(n_2)
 +(\bar B_3\bar n_2)\cup_4(\rho\bar n_2^2)
 +\rho\bar B_3\bar n_2\right].
\end{aligned}
```

The final bracket is binary before its half-valued embedding. The other
terms retain their displayed integer or real lifts and coefficient
retypings. In particular, charge is open by the entire `O5`, and the
last half-valued term is the fixed sheet-linear calibration.

The charge `d2` block remains part of the full CI terminal source;
the sheet-to-charge equation is `d3`, and the completed terminal obstruction,
including the neutral cubic, is `d4`. All lower completions and incoming
relations must be retained before testing the terminal class.

For `1 -> Z^r -> G -> P -> 1` with finite `P` and `r<=4`,
`H6(G,R_s)=0`. Every integral neutral `e_2` therefore admits a rational
phase completion, even when its class has a free part. A projective
rational resolution supplies an explicit construction; see the
[space-group proof](../e8/research/general_groups/general_groups.md).
Existence does not imply a canonical completion or a split stacking group.

<a id="stacking-4d"></a>

## Stacking twisters

For two states, set

```math
e_2^{\rm out}=e_2+e'_2,\qquad n_2^{\rm out}=n_2+n'_2,
```
```math
n_4^{\rm out}=n_4+n'_4+\mathcal E_4(n_2,n'_2),
\qquad\mathcal E_4=(n_2\cup n'_2)_\rho
                  +\rho_1\cup(n_2\cup_1n'_2).
```

The first cup in `E4` is formed in the sheet coefficient systems and then
retyped to the charge system. The common phase is

```math
\nu_5^{\rm out}=\nu_5+\nu'_5
 +P_5^{E8}(e_2,e'_2)+\widehat E_5^{\rm CI}(n_2,n_4;n'_2,n'_4),
```

```math
P_5^{E8}(e,f)=\frac13[(e\cup_1f)\cup(e-f)-(e-f)\cup(e\cup_1f)].
```

For the CI twister define the integral ordered cubic polarizer

```math
\mathcal C_5(n_2,n'_2)=(2n_2+n'_2)\cup(n_2\cup_1n'_2)
 +(n_2\cup_1n'_2)\cup(n_2+2n'_2).
```

Using the charge block from [Operations](OPERATIONS.md), the full formula is

```math
\begin{aligned}
\widehat E_5^{\rm CI}={}&
 \widehat E^c_5(n_4,n'_4)
 +\widehat E^c_5(n_4+n'_4,\mathcal E_4)\\
&-\frac12 A_2\cup(n_2\cup_1n'_2)_\rho
 +\frac14[\rho^2(n_2\cup_1n'_2)]_s
 +\frac16\mathcal C_5(n_2,n'_2)
 -\frac14(s)_{\rho+s}\cup\mathcal E_4\\
&+\frac12\left[
 \zeta^{\mathbb Z}_{2,2}(n_2,n'_2)
 +\mathcal P^{\rm Cartan}_5(\bar B_3;\bar n_2,\bar n'_2)
 +\widetilde B_3(\bar n_2\cup_2\bar n'_2)\right.\\
&\hspace{23mm}\left.
 +(\rho\bar n_2^2)\cup_5(\bar B_3\bar n'_2)
 +\mathcal R_5(\rho,s;n_2,n'_2)\right].
\end{aligned}
```

The second charge-block evaluation includes the newly generated integer
charge `E4`; omitting it changes the source/product identity. The two
finite binary kernels have 814 and 3,117 fixed terms, respectively. Their
input order and complete arrays are in [Coefficients](COEFFICIENTS.md).

Below, `P5` abbreviates the neutral `P5^E8`; it never denotes the Cartan
kernel in the preceding CI expression.

The source/product identity is
`d_s P5=((e+f)^3-e^3-f^3)/3 mod 1`, so the output solves the full source.
The self-twister `P5(e,e)` is zero. The extension can still be nonsplit:
for `C3`, complete powers followed by the sheet-removing gauge give
`3X=b`, `3b=0`, hence `Z9`. The shared phase and its incoming kernel
must be identified, rather than multiplying graded groups.

<a id="gauges-4d"></a>

## Gauges and inverse

Use E8-first gauge parameters `v_1,u_1,lambda_3,lambda_4`, with the first
two signed by `s`, charge by `rho`, and phase by `s`. The lower endpoint is

```math
e_2^{\rm g}=e_2+d_sv_1,\qquad n_2^{\rm g}=n_2+d_su_1,
```
```math
n_4^{\rm g}=n_4+B_3\cup u_1
 +\rho_1\cup[n_2\cup u_1+u_1\cup n_2+u_1\cup d_su_1]
 +d_\rho\lambda_3.
```

The phase transforms by

```math
\nu_5^{\rm g}=\nu_5+\widehat G_5^{\rm CI}
 +G_5^{E8}(e_2;v_1)+d_s\lambda_4.
```

For `e_out=e+d_s v`, the additional phase correction is

```math
G_5^{E8}(e;v)=\frac13[v\cup e_{\rm out}^2+e\cup v\cup e_{\rm out}+e^2\cup v].
```

The CI phase gauge is the finite signed cylinder sum

```math
\widehat G_5^{\rm CI}(v_0\ldots v_5)=
\sum_{j=0}^{5}(-1)^j\widehat O_6^{\rm CI}
 (v_0^-,\ldots,v_j^-,v_j^+,\ldots,v_5^+;n_2^I,n_4^I).
```

Here the lower cylinder is the displayed lower gauge with `u1,lambda3`
replaced by `eta u1,eta lambda3`; all backgrounds and initial fields are
pulled back first. This is exactly six source evaluations. It is not
replaced by a partial charge gauge when the CI sheet changes.

An exact right inverse has `e_inv=-e`, `n_inv=-n`,
`n4_inv=-n4+E4(n,n)`, and phase
`-nu5-E5_CI(state, inverse_lower)-P5(e,-e)`.
`E8State.inverse` implements this formula and validates its source.
Arbitrary integer powers retain these corrections.

## Neutral coherence data

The explicit associator and commutator are

```math
A_4(e,f,g)=\frac13(e\cup_1f)\cup_1g,
\qquad C_4(e,f)=\frac13[(e\cup_2f)\cup(e-f)-(e-f)\cup(e\cup_2f)].
```

They obey `d_s A4=P5(e,f)+P5(e+f,g)-P5(f,g)-P5(e,f+g)` and
`d_s C4=P5(e,f)-P5(f,e)` modulo integers. For gauge composition, put
`b=e+dv`, `c=b+dw`. Then

```math
K_4(e;v,w)=\frac13(v\cup w\cup c+v\cup b\cup w+e\cup v\cup w),
```

and `G(e;v)+G(b;w)-G(e;v+w)=d_s K4` over rational lifts. The product/gauge
compatibility witness is the signed prism `integral_I P5(e^I,f^I)`.
Both explicit hexagon witnesses and these operations are retained in
[e8_4p1.py](../../insulator/_engine/e8_4p1.py); no independent phase field
is introduced for them.

## Explicit mixed conversion relative to the CI comparison

Let `a=2n_2`, `b=2n'_2` be parity sheets before adding neutral E8,
and `e=e_2`, `f=e'_2`. The generic publication parity formula is invariant in its
dyadic part under `a -> a+16e`, `b -> b+16f`, including its normalized
binary transfer recurrence. Ordered expansion of the parity cubic source
with coefficient `1/12` gives the additional source rephasing

```math
R_5^{\rm mix}(a,e)=P_5(a,e).
```

The paired mixed product primitive is

```math
K_4^{\rm mix}(a,b;e,f)=C_4(b,e)+A_4(a,b,e)-A_4(a,e,b)
 -A_4(a+b,e,f)+A_4(a+e,b,f).
```

Its signed differential is
`P5(a,b)+P5(e,f)+P5(a+b,e+f)-P5(a,e)-P5(b,f)-P5(a+e,b+f)`.
The gauge transport is `integral_I P5(a^I,e^I)`. The mixed source
conversion is thus accompanied by a product and gauge conversion;
source equality alone is not used to guess a twister.

Direct reference-runtime comparisons must use
`Backend(use_specializations=False)`. The certificate covers the generic
publication path; equivalence of its optional zero-sheet optimizer is a
separate assertion and is not assumed here.

The E8-first runtime helpers in `insulator.parity_bridge` are
`e8_ci_source_bridge_4p1`, `e8_ci_product_bridge_4p1`, and
`e8_ci_gauge_bridge_4p1`. They implement exactly these relative corrections;
they do not silently supply the missing pure-CI map.

The proof, immutable evaluator certificates, and universal cancellation
are in the [mixed bridge review](../e8/research/general_groups/mixed_bridge_4p1.md).
This is a **relative** bridge: the remaining universal pure-CI terminal
map, its circle carries, and its lower product path are still required
to identify both complete physical presentations. The E8 result does
not prove that the retained CI model is the entire physical kernel.

## Complete examples and physical calibration

The accepted [4+1D campaign](../../results/four_dimensional_20261016/accepted.json)
contains fourteen commuting cyclic backgrounds and four signed `C2`
backgrounds. Each calculation includes the full `(e2,n2,n4,nu5)` source,
stacking, joint gauges, incoming identifications, and completed root powers.
The results are organized by symmetry and response sector:

- [Internal cyclic groups, zero intrinsic response](../../results/current/4p1d/internal_cyclic/intrinsic_zero.md).
- [Internal cyclic groups, all intrinsic responses](../../results/current/4p1d/internal_cyclic/intrinsic_all.md).
- [Unitary charge conjugation](../../results/current/4p1d/charge_conjugation.md).
- [AI/AII, zero intrinsic response](../../results/current/4p1d/time_reversal_intrinsic_zero.md).

For `U(1)^f × C_N`, `s=rho=omega=0`, the
[cyclic calculation](FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md) covers
`N=1,2,3,4,5,6,7,8,9,10,12,15,16,18`. Complete powers and actual
gauges are evaluated on the full cyclic five-cycle. An independent
Spin-c eta calculation then identifies the **entire relation lattice**
in the reviewed electronic-root dictionary. An independent bordism order
bound proves completeness of that physical character group. This certifies
these specified cyclic presentations without supplying a universal
terminal CI comparison.

For the signed cases, write `alpha(c)=1` and `omega=k alpha²/2`.
The [complete normalized-bar calculation](../4p1d/calibration/SIGNED_C2.md)
uses the scalar differential
`d_chi(alpha^p)=[(-1)^chi(c)+(-1)^(p+1)]alpha^(p+1)` and evaluates
every completed product and incoming action.

- Unitary charge conjugation has `s=0,rho=alpha`. For `k=0`,
  `C²=1` and the result is `Z2`; for `k=1`, `C²=(-1)^F` and the
  result is `Z2³`. Symmetry forces the intrinsic pair to vanish, so
  these tables cover the full response sector.
- Time reversal has `s=alpha,rho=0`. For `k=0` (AI) and `k=1` (AII),
  the computed **intrinsic-zero** group is zero. Their full groups and
  allowed uniform lattices are separate physical inputs.

These signed groups agree with the independently derived
[bordism targets](../4p1d/calibration/BORDISM_TARGETS.md), with each source
and tangent structure specified there. This is a group comparison for
these backgrounds; a full signed-root character dictionary is not asserted.

## Additional uniform response pair

The reviewed [v0.15 supplement](../../formulas/v015_provenance.json)
has two intrinsic 4+1D integer coordinates `(n0I,n0J)`. With `c=2f`
the Spin-c determinant class, their response polynomials are

```math
I=\frac{c^3-cp_1}{48},\qquad J=\frac{c^3}{2}.
```

These are additional bulk responses, separate from the E8-first tuple
and from the scalar 2+1D IQH coefficient. Their possible outgoing
`d3,d5,d6` belong to this additional coefficient row; they do not change
the `d2,d3,d4` scope of the original four-data equations above.

For the direct product `U(1)^f × C_N`, forgetting `C_N` has the identity
inclusion as a section. Pulling a uniform phase back with trivial `C_N`
action therefore gives a natural group splitting into the intrinsic-zero
kernel and `Z{I} ⊕ Z{J}`. At `s=rho=omega=0`, direct substitution into
the reviewed intrinsic equations permits zero lower data for both unit
roots. The [cyclic section proof](FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md#uniform-intrinsic-pair-and-its-natural-section)
justifies the all-intrinsic table. It is not an implementation of a
general opened-intrinsic solver or a section for arbitrary signed backgrounds.

The exact closed-sheet operations, the accepted global examples, and the
independent physical identifications have these stated scopes. A general
global 4+1D classifier and a universal pure-CI terminal source/product
comparison remain separate requirements; no missing operation is set to zero.
