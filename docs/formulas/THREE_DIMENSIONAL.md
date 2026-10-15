# 3+1D: the complete four-data domain-wall theory

The ordered fields are `(e_1,n_1,n_3,nu_4)`, with coefficient actions
`(s,s,rho,s)`. Use the cochains and charge blocks in
[the four-data reference](OPERATIONS.md). This file concerns 3+1D.

<a id="obstructions-3d"></a>

## Obstruction functions

```math
d_s e_1=d_s n_1=0,\qquad d_\rho n_3=-B_3\cup n_1,
\qquad d_s\nu_4=\widehat O_5^{\rm CI}(n_1,n_3),
```
```math
B_3=d_{\rho+s}(\omega_R-s\cup s/2).
```

The integer source represents the CI component of `d3`; the neutral
component is zero in the selected section. The completed terminal source
represents `d4`. Its closed-charge restriction gives `d2`. The E8 field
is an integer signed cocycle: reducing it modulo two loses free weak layers.

## A finite formula for source and terminal twister

The following parameter construction fixes the source and product
together. Its parent is the calibrated CI expression `Ohat_6` in
[the complete 4+1D source](FOUR_DIMENSIONAL.md#obstructions-4d),
including its finite Cartan kernels. No group-dependent primitive is fitted.

On `Delta^m x X`, let `eta_i(j)=0` for `j<i` and `1` otherwise, and let
`theta_i=d eta_i`. All backgrounds and input fields are pulled back from
`X` with their actual local systems. Define

```math
k_2=\sum_i\theta_i n_1^{(i)},
```
```math
\ell_3=\sum_{i<j}\big[(\theta_i\cup_1\theta_j)
 (n_1^{(i)}n_1^{(j)})+
 \theta_i(n_1^{(i)}\cup_1\theta_j)n_1^{(j)}\big],
```
```math
z_4=\sum_i[\theta_i n_3^{(i)}+(B_3\cup_1\theta_i)n_1^{(i)}]
 +\rho\ell_3
 +d_\rho\left\{\sum_{i<j}[\rho\cup_1(\theta_i\cup_1\theta_j)]
 (n_1^{(i)}n_1^{(j)})\right\}.
```

These fields satisfy the parent lower equations on the entire parameter
product, with the correct grouped lower data on its faces. Let `I_m`
be the parameter-first signed shuffle sum defined in
[Operations](OPERATIONS.md). Then

```math
\widehat O_5^{\rm CI}=\mathcal I_1\widehat O_6(k_2,z_4),
\qquad \widehat E_4^{\rm CI}=\mathcal I_2\widehat O_6(k_2,z_4).
```

This requires six evaluations for the source and fifteen for the twister
on their respective base simplices. A complete associator witness is
`A_3=-I_3 Ohat_6`. These are finite formulas with specified inputs.
Signed Stokes proves closure, the source/product identity, and the
associator identity; the detailed face proof is in
[the dimensional baseline](../../formulas/04_three_dimensional.tex).

<a id="stacking-3d"></a>

## Stacking twisters

```math
E_1=e_1+e'_1,\qquad N_1=n_1+n'_1,
```
```math
N_3=n_3+n'_3-\rho\cup(n_1\cup n'_1),
\qquad \Nu_4=\nu_4+\nu'_4+\widehat E_4^{\rm CI}.
```

The integer charge twister is retained even though the integer source is
linear. The selected neutral section contributes zero additional phase
source and twister. This is a coordinate choice supported by the physical
section argument below, not a statement that E8 has no gravitational response.

<a id="gauges-3d"></a>

## Gauges and incoming identifications

For independent `v_0,u_0 in C0(G,Z_s)` and `w_2 in C2(G,Z_rho)`,

```math
e_1^g=e_1+d_s v_0,\qquad n_1^g=n_1+d_s u_0,
\qquad n_3^g=n_3+B_3u_0+d_\rho w_2.
```

For height `eta` on `I`, take the same expressions with `u_0,w_2`
replaced by `eta u_0,eta w_2`, giving `n_1^I,n_3^I`. The phase gauge is

```math
G_4=\mathcal I_1\widehat O_5^{\rm CI}(n_1^I,n_3^I),
\qquad \nu_4^g=\nu_4+G_4+d_s\lambda_3.
```

The neutral gauge has no additional phase in this section. The joint CI
gauge uses five prism paths, each with the specified six-evaluation source.
For closed `u_0`, the induced charge `B_3 u_0` and its phase are still an
incoming relation. Closed charge parameters produce the incoming phase
from the common charge block. None of these phases are dropped during
sheet removal or root-power calculations.

Integral background lift changes use
`omega_R -> omega_R+z_2`, `n_3 -> n_3-z_2 cup n_1`; real section changes
use `omega_R -> omega_R+d_(rho+s)alpha_1` with charge unchanged. The phase
is the same source-cylinder evaluation, and E8 is unchanged.

## Why the global calculation can be factored

The supplied E8 supplement fixes these **3+1D tensor coordinates** in
Section 3, “Operative three-dimensional fields and equations”
(`note.tex:151–164`; source and product labels `eq:3d-source` and
`eq:3d-product`). Its additional neutral source, neutral and mixed
twisters, and neutral gauge phase are zero **as cochains in these
coordinates**, rather than terms discarded after a cohomology test.
The archive is `E8_AHSS_v0_9_complete.zip`, SHA256
`da3ad9368390e8d075f27e0039e8486f14890fefb3ccbf0aea4d85a5ba0685cd`;
see [the retained provenance](../../formulas/e8_provenance.json).

Let `C_CI` denote the completed CI states modulo their full joint gauges,
phase coboundaries and incoming identifications. The equations above give
an explicit isomorphism of stacking groups:

```math
\begin{aligned}
\Phi:\mathcal C_{\mathrm{four\ data}}^{3+1}
&\longrightarrow H^1(G,\mathbb Z_s)\oplus\mathcal C_{\rm CI},\\
[e_1,n_1,n_3,\nu_4]&\longmapsto
([e_1],[n_1,n_3,\nu_4]).
\end{aligned}
```

To prove it, choose an integer cocycle representing `[e_1]` and a completed
CI representative. Their four-tuple satisfies every displayed equation,
which defines the inverse map. Changing the neutral representative by
`d_s v_0` leaves all CI fields and the phase unchanged; changing the CI
representative uses the same full CI gauge with `v_0=0`. Thus the inverse
is independent of both choices. Conversely, projecting any joint gauge
gives a principal neutral gauge and an allowed CI gauge. Thus `Phi` is
well-defined, and the two maps are mutually inverse.
Stacking adds the neutral cocycles and applies exactly the CI product to
the other three fields, proving that the maps preserve the group law.
There is only **one** phase coordinate: it is already part of `C_CI`.

This proof also includes the incoming relations. A closed neutral gauge
has `d_s v_0=0` and no charge or phase action, even on a nonzero CI state.
Closed CI sheet and charge gauges retain their complete existing actions,
independently of `e_1`. A neutral root-power relation therefore introduces
no CI correction. If `P_E8` presents the integral cocycle lattice modulo
principal gauges and `P_CI` is the full computed CI relation matrix, the
four-data relation matrix is `diag(P_E8,P_CI)`.

Consequently `extend_e8_3p1.py` computes the same group as a simultaneous
solver of these equations: it computes the actual signed integer `H1`,
retains its gauge witnesses, combines the presentations and takes Smith
form. This factorization is an exact theorem of the supplied model, not
an independent derivation of its physical coordinate convention. In
4+1D the neutral cubic source and sheet-removal phase are nonzero; this
argument does not apply there (see [4+1D](FOUR_DIMENSIONAL.md)).

The public `scripts/classify_3p1d.py` entrypoint runs both factors and final
acceptance in one workflow. It reports completion only after the full
four-data results, exact selected inputs and source provenance pass the
collector and terminal checks. The internal CI stage alone is not a
completed four-data classification.

## Neutral section, infinite groups, and remaining comparison

For ordinary three-dimensional space groups with their orientation
character, the physical neutral section is constructed by Song, Xiong,
and Huang, [PRB 101, 165129 (2020)](https://doi.org/10.1103/PhysRevB.101.165129).
The generalized section argument and its naturality/crystalline-equivalence
assumptions are recorded in
[the space-group proof](../e8/research/general_groups/general_groups.md).
Electronic survival uses coefficient inclusion and AHSS naturality.

Within this selected model the group is the CI group times `H1(G,Z_s)`;
the physical statement additionally requires identifying the CI model
with the physical kernel. The universal nonzero-CI terminal comparison
remains separate required work.

`insulator.e8_h1.twisted_h1` computes `H1(G,Z_s)` from a finite presentation
with a saturated integer kernel and principal-coboundary quotient. It
retains free rank and torsion for infinite groups. The finite-group
shortcut `0` or `Z2` is not used for space groups with translations.

The executable `scripts/extend_e8_3p1.py` consumes actual completed CI
results. For a finite point group it derives a Cayley presentation from
the multiplication table and verifies every crossed-homomorphism identity.
For a rank-three space group it instead uses the certified full affine
presentation, checks its relators and primitive translation words, and
computes the saturated signed integer kernel. The latter calculation
retains translations and nonsymmorphic relations; it does not replace
the space group by its finite holonomy quotient.

In both cases the routine retains the principal gauge that removes the
neutral torsion relation, joins the neutral presentation to the actual
CI presentation, and computes Smith form. Saved CI roots and gauge
witnesses remain intact. This implements the selected section's global
group law for the supported inputs; it does not prove the outstanding
physical CI-kernel identification.
