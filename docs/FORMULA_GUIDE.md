# U(1)^f obstruction functions and stacking twisters

This is the current formula reference for the original four-data insulator
theory. Every state is ordered **E8, CI, charge, shared phase**:
`(e_p,n_p,n_{p+2},nu_{p+3})`, with `p=d-2` in spatial dimension `d`.
Each dimensional page specifies its own physical fields, obstruction
equations, stacking twisters, and complete gauges.

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
completed roots, coupled powers, and an independent bar-cycle audit.

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
Intrinsic higher-response coordinates are outside this four-data scope.

The [source provenance](../formulas/provenance.json),
[E8 provenance](../formulas/e8_provenance.json), and
[research record](e8/research/README.md) retain the exact inputs and proofs.
The preserved TeX files are source evidence and coefficient appendices;
the dimensional pages linked above are the current narrative.
