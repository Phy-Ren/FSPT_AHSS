# The four-data theory: equations, equivalence, and stacking

This is the active theory specification. The fields are always
`(e_p,n_p,n_{p+2},nu_{p+3})`, E8 first, with `p=d-2` for spatial dimension
`d`. The separate dimensional references are [2+1D](2p1.md),
[3+1D](3p1.md), and [4+1D](4p1.md). They give obstruction equations before
stacking and gauge equations. Additional intrinsic higher-dimensional
coefficient sectors are deferred and do not enter this specification.

## 1. Symmetry and coefficients

Fix the actual fermionic extension by `U(1)^f`, not just a point-group
name. Its quotient `G` is discrete and fits `1 -> Z^r -> G -> P -> 1`,
with finite `P` and `r<=d<=4`. The independent signs are `s,rho:G -> Z2`;
the circle extension has sign `rho+s`. For its real cocycle lift `omega_R`,

\[
\check\omega_R=\omega_R-\tfrac12s\cup s,
\qquad B=d_{\rho+s}\check\omega_R.
\]

The uniform 2+1D endpoint uses the **unshifted** connecting cochain
`d_(rho+s) omega_R`, as its dimensional equation states. The field types are

\[
e_p,n_p\in C^p(G,\mathbb Z_s),\quad
n_{p+2}\in C^{p+2}(G,\mathbb Z_\rho),\quad
\nu_{p+3}\in C^{p+3}(G,\mathbb R/\mathbb Z_s).
\]

There is one shared phase. Integer lifts, local-system transport, ordered
cups, and negative carries follow [the cochain definitions](../../formulas/02_operations.tex).
For an open binary cochain `x_k`, use

\[
\operatorname{Sq}^j x_k=x_k\cup_{k-j}x_k+x_k\cup_{k-j+1}dx_k.
\]

The second term is retained when charge is opened by a sheet source.
Integer charge is not reduced to parity before its extension coupling.

## 2. Exactly which AHSS differentials occur

Distinguish the cochain differential `d_chi` from the page differential
`d_r:(a,q)->(a+r,q-r+1)`. The nonempty coefficient rows here are `q=3`
(E8 and IQH), `q=1` (charge), and `q=0` (phase). The relevant operations
are **d2, d3, d4**. This tower has no higher outgoing differential.

For a closed integer charge `z_k`,

\[
d_2[z_k]=\left[\omega_R\cup z_k+\tfrac12\operatorname{Sq}^2\bar z_k\right].
\]

The sheet-to-charge `d3` is the class of the integer source in
`d_rho n_{p+2}=O_{p+3}`. Its neutral E8 component is zero in the selected
model. After solving that equation, the completed terminal source
`Ohat_{p+4}` represents the sheet-to-phase `d4`.

The latter has its higher-page target: changes of permissible charge
completion and incoming identifications are part of its definition.
Testing a raw phase without these quotients is not the AHSS obstruction
test. A nonzero cochain may be exact and therefore unobstructed.

## 3. The common charge block

Use these operations on the actual, possibly open, charge inputs.
Half-valued expressions are formed over `F2` before phase embedding:

\[
\widehat O^c_{k+2}(z)=\omega_R\cup z+\tfrac12\operatorname{Sq}^2\bar z,
\]
\[
\widehat E^c_{k+1}(z,z')=\tfrac12
 [\bar z\cup_{k-1}\bar z'+d\bar z\cup_k\bar z'],
\]
\[
\widehat G^c_{k+1}(u;z)=\omega_R\cup u+\tfrac12\operatorname{Sq}^2\bar u
 +\widehat E^c_{k+1}(z,d_\rho u).
\]

For closed `u`, the gauge may induce a nonzero incoming phase even though
the charge endpoint does not change. Such relations are retained.

## 4. What specifies the complete group law

A complete state solves every lower equation and the terminal equation.
Its product uses the actual lower output

\[
e''=e+e',\quad n''=n+n',\quad
z''=z+z'+\mathcal E_{p+2}(n,n'),
\]
\[
\nu''=\nu+\nu'+\widehat E_{p+3}((e,n,z),(e',n',z')).
\]

Both corrections are specified in the dimensional references. They obey

\[
d_s\widehat E=\widehat O(e'',n'',z'')
 -\widehat O(e,n,z)-\widehat O(e',n',z').
\]

This identity preserves solutions but does not alone fix closed
two-input corrections. The operative CI convention is calibrated v0.7:
cubic coefficient `1/6`, the specified sheet-linear source term, and
additional product coefficient `epsilon=0`. These are fixed data, not
classifier options. A phase redefinition `nu -> nu+F` transports all data:

\[
\widehat O\mapsto\widehat O+d_sF,\qquad
\widehat E\mapsto\widehat E+F(a*b)-F(a)-F(b)+d_sH,
\]
\[
\widehat G(a\to a^g)\mapsto\widehat G(a\to a^g)+F(a^g)-F(a).
\]

Gauge compatibility, associativity, and commutativity on classes for the
adopted CI model are proved in
[the equivalence reference](../../formulas/06_equivalence.tex). The neutral
block supplies its own witnesses. `E8State.inverse` and `E8State.power`
retain complete phases; root orders need not be powers of two.

## 5. Gauge equivalence and incoming relations

Independent E8 and CI sheet gauges exist when `p>=1`. Changing a CI sheet
also changes charge by the dimensional correction. The phase receives
the full joint source-cylinder gauge, including the E8 part. A shorter
charge-only gauge is also defined and need not agree pointwise with the
joint gauge; every root calculation must retain the gauge actually used.

A closed parameter can have zero leading endpoint change and nonzero
induced charge or phase. These incoming relations are not optional
quotients. Removing an exact sheet or charge retains its induced phase.
Background lift and section changes are coordinate transports, treated
with the same finite source-cylinder rule.

## 6. Recovering the final stacking group

1. Compute signed integral and phase cohomology of the actual group,
   retaining its infinite translations and nonsymmorphic relations.
2. Test integer obstructions and construct charge completions; then test
   the terminal source modulo all permitted completion changes.
3. Choose completed roots, including their terminal phases.
4. Stack actual roots with the full twister. Remove exact accumulated
   fields with the full gauges and record the lower-root relations.
5. Include incoming relations, form the integer presentation, and compute
   its Smith normal form, retaining finite factors and free rank.

Surviving decorations or the associated graded group alone do not give
the final group. Two order-three layers can extend to `Z9` rather than
`Z3 x Z3`; the neutral 4+1D example records the completed root relation.
An exact obstruction does not imply a trivial twister or a split extension.

## 7. Current boundary of the proof

The local API implements this fixed model's source, product, gauge,
inverse, powers, and background transport. The preserved TeX coefficient
tables specify the full CI kernels; no unspecified primitive is fitted.
The neutral formulas are explicit in the dimensional references.

The universal nonzero-CI physical/parity terminal comparison still needs
its single-state map and paired two-input primitive. The nonzero uniform
IQH physical product comparison also remains open. These are physical
identification problems, not unnamed higher differentials or an
unselected coefficient in the operative twister. They remain required;
abstract-group splitting does not replace them.

The global CLI remains CI-only. E8-inclusive campaigns still require
the shared-phase presentation and incoming/root computations above.
A local identity test is not a completed global classification campaign.

These boundaries have different consequences for the final stacking group:

| Item | Consequence |
| --- | --- |
| Fixed source, product, and gauge convention | Within the adopted four-data model, these specify a group without an adjustable terminal twister. Its associated graded group alone still does not specify it. |
| Universal pure-CI physical comparison | Needed to identify that model with the intended physical theory. Until it is proved, physical completeness and agreement of all extension relations remain conditional; matching selected examples cannot remove this condition. |
| E8-inclusive global solver | A remaining computation and implementation task, not a new coefficient to choose. It must evaluate complete root powers and incoming relations in the shared phase. |
| Separate intrinsic response sector | Deferred by scope. It is not an unresolved operation inside this four-data model. |

Accordingly, “the formulas are specified” and “the complete physical
classification is proved” are distinct claims. This reference establishes
the former for the retained convention and states the remaining proof
obligations for the latter. It does not label those obligations harmless.
