# U(1)^f obstruction functions and stacking twisters

This is the current formula reference for the original four-data insulator
theory. Every state is ordered **E8, CI, charge, shared phase**:
`(e_p,n_p,n_{p+2},nu_{p+3})`, with `p=d-2` in spatial dimension `d`.
Each dimensional page specifies its own physical fields, obstruction
equations, stacking twisters, and complete gauges.

[Computed examples](../results/current/README.md) use the same notation and
keep dimensions, physical spins, and response sectors in separate tables.

| Dimension | Obstruction functions | Stacking twisters | Gauges |
| --- | --- | --- | --- |
| 2+1D | [Obstructions](formulas/TWO_DIMENSIONAL.md#obstructions-2d) | [Twisters](formulas/TWO_DIMENSIONAL.md#stacking-2d) | [Gauges](formulas/TWO_DIMENSIONAL.md#gauges-2d) |
| 3+1D | [Obstructions](formulas/THREE_DIMENSIONAL.md#obstructions-3d) | [Twisters](formulas/THREE_DIMENSIONAL.md#stacking-3d) | [Gauges](formulas/THREE_DIMENSIONAL.md#gauges-3d) |
| 4+1D | [Obstructions](formulas/FOUR_DIMENSIONAL.md#obstructions-4d) | [Twisters](formulas/FOUR_DIMENSIONAL.md#stacking-4d) | [Gauges](formulas/FOUR_DIMENSIONAL.md#gauges-4d) |

[Operations](formulas/OPERATIONS.md) defines all coefficient transport,
integer carries, higher cups, Cartan operations, and finite prism sums.
[Coefficients](formulas/COEFFICIENTS.md) fixes the two large binary kernels.
[Root-power presentations](formulas/ROOT_POWER_PRESENTATIONS.md) explains
how the full twister and gauges determine the final stacking group.
[Executable interfaces](formulas/IMPLEMENTATION.md) maps the equations to
the exact local API and persistent worker. The
[4+1D cyclic examples](formulas/FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md) retain
completed roots, coupled powers, full bar-cycle gauge reductions, and an
independent physical eta-kernel comparison.

The [3+1D factorization proof](formulas/THREE_DIMENSIONAL.md#why-the-global-calculation-can-be-factored)
explains why the supplied model permits an exact neutral E8 calculation
followed by assembly with the CI, charge, and shared-phase presentation.
The public classifier accepts the result only after both parts and the final
presentation pass validation. The coupled 4+1D formulas do not use this
factorization.

## Conventions and coordinates

The independent characters are `s,rho:G -> Z2`. The first reverses
chirality and the additive phase; the second reverses integer charge.
The charge-circle automorphism has character `rho+s`. The input is the
actual normalized extension lift
`omega_R in C2(G,R_(rho+s))`, with integral differential. Set

```math
\check\omega_R=\omega_R-\frac12s\cup s,
\qquad B_3=d_{\rho+s}\check\omega_R.
```

Both sheets have coefficients `Z_s`; charge has coefficients `Z_rho`;
the one phase has coefficients `R/Z_s`. The 2+1D endpoint uses the
unshifted connecting cochain `d_(rho+s) omega_R`, as stated on its page.
All phases in this reference are additive. A prime denotes the second
input. Juxtaposition denotes an ordered cup product, never a pointwise
product or a product of arbitrary `R/Z` representatives.

```math
\bar x=x\bmod2,\qquad
\widetilde x=\left\lfloor x/2\right\rfloor\bmod2.
```

Floors include negative integers. Half-valued brackets are evaluated over
`F2` before their canonical integer lift. Other rational coefficients
retain the displayed integral or real numerator until final reduction
modulo one. Retyping `(x)_chi` retains values and changes the coefficient
system explicitly; it is not an identification of local systems.

## AHSS pages and the fixed convention

The coefficient rows of this four-data tower are `q=3,1,0`, with both
E8 and IQH in `q=3`. For
`d_r:(a,q)->(a+r,q-r+1)`, the relevant operations are **d2, d3, d4**.
A source subscript, such as `O6`, denotes cochain degree. All obstruction
tests include the preceding lower completions and their incoming images.

The operative CI convention is fixed: sheet-linear calibration, cubic
coefficient `1/6`, and additional product coefficient `epsilon=0`.
The neutral contribution is the selected shared-phase E8 model. These
pages give one source/product/gauge convention; archive variants are not
alternative runtime choices.

## Computation and physical identification

`insulator.E8State` evaluates the four-data source, product, gauges,
inverse, arbitrary integer powers, and background transport exactly.
The global routines must additionally solve cohomology, include incoming
identifications, and calculate actual root powers. Local identities alone
do not constitute a global classification.

The explicit operations determine the adopted cochain model. Its universal
identification with the complete physical CI kernel still requires the
nonzero-CI terminal map and paired product comparison. The physical
nonzero-uniform-IQH product-coordinate comparison is also separate.
Published group agreement does not by itself prove these identifications.
The accepted cyclic cases have a stronger certificate: equality of the
full cochain relation lattice with the independently computed physical
character kernel, together with a bordism order bound. This is a
family-specific identification, not a universal terminal-map theorem.

## 4+1D examples and intrinsic response scope

The [accepted evidence](../results/four_dimensional_20261016/accepted.json)
contains fourteen commuting internal cyclic groups,
`N=1,2,3,4,5,6,7,8,9,10,12,15,16,18`, and four signed `C2` backgrounds.
Internal groups do not carry crystalline spinless/spin-half labels.

- [Cyclic groups: zero intrinsic response](../results/current/4p1d/internal_cyclic/intrinsic_zero.md).
- [Cyclic groups: all intrinsic responses](../results/current/4p1d/internal_cyclic/intrinsic_all.md).
- [Unitary charge conjugation](../results/current/4p1d/charge_conjugation.md), where symmetry forces the intrinsic row to zero.
- [AI/AII: zero intrinsic response](../results/current/4p1d/time_reversal_intrinsic_zero.md).

The extra 4+1D response pair `(n0I,n0J)` is separate from the four-data
tuple and from the scalar 2+1D IQH coefficient. For `U(1)^f × C_N`,
trivial `C_N` action gives an explicit natural section for both uniform
roots. Thus the all-intrinsic cyclic group is its computed and physically
calibrated intrinsic-zero group times `Z²`. The
[section proof](formulas/FOUR_DIMENSIONAL_CYCLIC_EXAMPLES.md#uniform-intrinsic-pair-and-its-natural-section)
also records the zero-lower-data substitution and its scope. A general
opened-intrinsic cochain solver is not inferred from this section.

The [signed C2 calculation](4p1d/calibration/SIGNED_C2.md) retains complete
products and all incoming gauges. Its reference comparison uses the
specified [interacting bordism targets](4p1d/calibration/BORDISM_TARGETS.md).
AI/AII are restricted to intrinsic zero; their full uniform-response
lattices are not outputs of that solver. A general global 4+1D classifier
is not supplied by these finite families.

The [even charge-root identity](formulas/CHARGE_ROOT_RELATIONS.md) is a
derived cohomology-class simplification. It is recorded separately from the
implemented full cochain and gauge witnesses; it does not replace them.

The [source provenance](../formulas/provenance.json),
[E8 provenance](../formulas/e8_provenance.json), and
[v0.15 intrinsic/calibration provenance](../formulas/v015_provenance.json)
pin the reviewed formula inputs. The
[research record](e8/research/README.md) retains the supporting proofs.
The preserved TeX files are source evidence and coefficient appendices;
the dimensional pages linked above are the current narrative.
