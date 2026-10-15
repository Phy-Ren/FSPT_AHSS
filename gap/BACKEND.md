# Exact insulator classification backend

`load.g` loads only generic resolution infrastructure and U(1)^f insulator
operations. The infrastructure was adapted from the public main branch's HAP
native/bar comparison and Smith reduction code; no theory engine or result is
loaded from that branch.

```gap
U1_ROOT := "/absolute/path/to/insulator";;
Read(Concatenation(U1_ROOT,"/gap/load.g"));
Read(Concatenation(U1_ROOT,"/insulator_catalog/generated/point2_03_spinless.g"));
c := U1CatalogContext(U1_INPUT,6);;
r := U1Classify(c,U1_INPUT.dimension);;
```

Default 2+1D calculations fix the uniform IQH decoration n0=0. To calculate its
allowed free generator as well, pass `rec(uniformIQH:=true)` as a third argument.
The latter solves both the integer obstruction and terminal obstruction modulo
charge completions. Its witnesses record the actual allowed sheet multiple and
complete phase. It uses the package's stated nonzero-IQH product convention;
the package's qualification about its universal physical P-move matching still
applies. The output does not construct the neutral E8 or intrinsic higher
response sectors.

The global driver supports spatial dimension two for finite point groups and
full infinite wallpaper groups, and dimension three for finite point groups.
Local source/product/gauge operations also support spatial dimension four, via
the formula worker. A global dimension-four campaign is rejected explicitly.

## Integer and phase coordinates

Each context has immutable, independent `s`, `rho` and `omega` functions.
Coefficient keys `Zs`, `Zr`, `Zt`, `U1s` mean respectively Z_s, Z_rho,
Z_(rho+s), (R/Z)_s; every differential/Smith/cohomology cache includes that key.
The phase cohomology adapter is used only above the group's virtual
cohomological dimension, so there are no omitted continuous phase summands.
Integer charge groups retain arbitrary torsion orders and free summands.

The initial charge obstruction class uses the generic Smith dual-cycle
projection adapted from main commit `0864495b90297d3e1a0747b77aae17980f6d1f3f`,
`gap/class_coordinates.g`. This evaluates the closed phase on the exact
signed cycles needed for its class, instead of expanding every target cell.
The source adapter verifies the native integer charge is closed and requires
a validated, function-bound extension certificate; arbitrary contexts retain
the full native cocycle check. `c.phaseClassMode := "native"` selects that
reference route, and `"compare"` checks both. The period API rejects absent or
mismatched closure certificates. It is restricted to phase degrees above the
virtual cohomological dimension. Full primitives, completed roots and gauge
witnesses still use the original native/bar transfer and homotopy correction.

For the initial charge obstruction with zero CI sheet, a certified
half-integral extension also permits native binary operations. Write
`qbar = q mod 2` and `w = 2 omega mod 2`. The exact integral equation
`delta_rho q = 0` and the validated twisted extension equation imply that both
are binary cocycles. The coefficient map `j: F2 -> (Q/Z)_s`, `j(1)=1/2`,
is equivariant for every `s`. Consequently
`[omega cup q + Sq2(q)/2] = j([w cup qbar + Sq2(qbar)])`.
The native higher diagonal computes the same cohomology operations as the bar
resolution. Its half-valued result is projected using the actual signed
phase cohomology object; the map induced by `j` is not assumed injective.
Only this primary obstruction class uses binary data. Integral charge
lattices, free CI sheets, full bar sources, primitives, stacking and incoming
gauge relations retain their original exact data.

`gap/charge_primary.g` verifies the actual native integral charge, its signed
closure and the canonical target cohomology. Its background certificate is
bound to the context's action and extension callbacks. General rational
extensions and uncertified contexts fall back to the phase-class route above.
`c.chargePrimaryMode` accepts `"native"`, `"bar"` or `"compare"`; the last
compares the native primary class to the selected `c.phaseClassMode` route.
An explicit charge mode takes precedence. If only a phase mode is supplied,
the bar route remains selected for existing reference audits. The command-line
defaults are `--charge-primary native --phase-class cycles`.

The reusable diagonal and mod-two contraction modules come from main commit
`0864495b90297d3e1a0747b77aae17980f6d1f3f`, with only the public symbol prefix
changed. They contain generic resolution operations and load no other theory
engine. `tests/test_charge_primary.py` checks nonzero obstructions in the full
affine groups SG16 and SG25, all four independent sign choices, the general
rational-extension fallback and rejection of invalid charge/target inputs.

For charge cohomology generators, the code evaluates d2 in terminal cohomology,
constructs its exact integer kernel lattice, and solves the full phase for each
kernel generator. Torsion powers are evaluated by the supplied product and
reduced using the full charge gauge; their surviving phase gives a relation,
not a guessed direct product. For finite 3D groups, H1(Z_s) is zero or Z2. The
CI source is solved integrally; the terminal source is then tested modulo the
whole charge d2 image. A surviving CI root is completed, powered and reduced
by its integer sheet gauge before its charge/phase relation is recorded.

Incoming closed charge gauges and closed CI gauges are evaluated as actual
states and incorporated in the same presentation. The three final filtration
subquotients use integer elimination of later columns of the complete relation
lattice. They must not be inferred from `chargeOrders` or `phaseOrders`, which
are raw cohomology groups. `torsion` and `freeRank` describe the Smith reduction
of the complete stacking presentation.

All primitives include the native/bar comparison homotopy correction. Storing
only a native solution and applying the reverse chain map would not solve the
original bar obstruction. Witnesses and generators retain exact native seeds,
obstruction vectors, charge corrections, incoming images and root relations.
Finite exact phases are encoded as rational strings by `U1JSON`.

The 2D fixed-sheet charge gauge is the supplied short CF gauge. Higher joint
sheet/charge gauges use the calibrated cylinder formula. Those two valid gauge
representatives can differ by closed phases; they are not assumed pointwise
equal. The worker has a bounded content cache, and native/bar cochains also
memoize exact evaluations.

## Validation

Run `python -m unittest discover -s tests -p 'test_backend*.py' -v` with GAP,
HAP and CrystCat installed. Regressions include full C2 charge Z4 with its
quarter-valued phase, odd-order C3 and order-four C4 roots, calibrated AIII Z8,
AII Z2^2 and AI=0 with its nontrivial incoming quotient, a nonzero-background
uniform IQH lift, and the full affine glide wallpaper group with its free
charge summand. These examples validate the declared CI/charge/phase sector;
they do not certify omitted physical sectors.

Before constructing a finite context, the backend exhaustively checks the
multiplication table, both independent characters, normalization and every
triple of the twisted U(1) extension equation. Completed generators, incoming
states and gauge reductions are checked against their exact native chain
equations, including source closure. The output records the check count and
integer gauge parameters. This is supplemented by 108 independent bar-tuple
checks with distinct s/rho characters, a half-valued extension, negative
integer gauges and comparison-homotopy primitives. Native identities and these
bar regressions are explicit verification levels, not an exhaustive bar
examination of every large campaign group.

For wallpaper groups, `wallpaperFilling` records the image of physical filling,
separately from abstract free rank. It uses a Pcp Smith basis of the full
translation kernel, checks that the basis generates that kernel, orders it by
positive affine determinant, and evaluates every completed generator on
`[tx|ty]-[ty|tx]`. The gcd of those integer periods is `fillingStep`; each full
presentation relation is verified to have zero filling. In particular, p1 has
step one while the glide group pg has step two, although both contain one
abstract free charge summand. No finite quotient replaces the wallpaper group.

A uniform-IQH run also returns `relativeUniformIQH0`, the n0=0 subgroup obtained
by exact integer elimination of the CI columns of the same certified complete
presentation. Its generators, finite factors, free rank and phase/charge
filtration are explicit. This supports direct comparison with a relative run
without asserting a free IQH generator in advance. Wallpaper witnesses
separately report `chargeRootSubgroupFillingStep` and `ciGeneratorFillings`; the
nested relative result uses only the former subgroup's actual periods.

## Independent discrepancy audits

`audit_d2.g` checks the spin-half D2 charge obstruction before comparison with
any external table. For G=C2 x C2 and zero effective extension, the integral
charge generator is q=beta(xy). Its mod-two reduction is x^2 y+x y^2 and the
Bockstein of the phase obstruction has reduction
Sq^1 Sq^2(q mod 2)=x^4 y^2+x^2 y^4, which is nonzero. Thus this charge root is
obstructed in the supplied theory. The script verifies the integral, mod-two
and explicit bar descriptions independently and retains the obstruction.

`audit_d2d.g` records every raw D2d charge obstruction, its restriction to the
proper D2 subgroup, the CI integer obstruction, and charge-root/incoming
phase classes computed with both supplied gauge representatives. In the
spin-half background the D2-nonzero charge restricts to the preceding D2
obstruction. In the spinless background the other charge is obstructed only
in the full D2d group. The audit does not identify an obstruction with a
particular physical center-state root without an additional physical map.

`audit_odd_kernel.g` verifies normal C3 kernels and Sylow-2 complements in
D3d, D6 and D3h. Their complements have the same real representation characters,
signs and extension classes as C2h, D2 and C2v respectively. The witness includes
all element maps and an explicit half-valued background coboundary. For
1 -> C3 -> G -> H -> 1, the Lyndon-Hochschild-Serre spectral sequence with
2-local coefficients collapses: positive-degree C3 cohomology vanishes because
three is invertible. Inflation is an isomorphism and restriction to the
displayed complement is its inverse. This holds for all supplied sign modules.
Restriction to Sylow C3 detects the remaining 3-primary groups, but
H1(C3,Z)=H3(C3,Z)=H4(C3,R/Z)=0, so none of the three retained 3D filtration
layers has a 3-primary part. Naturality of the differentials, products and
gauges therefore identifies the complete CI/charge/phase stacking groups for
each pair. This argument does not assert completeness of omitted sectors.

Load an audit after `load.g`. Optionally set `U1_D2_AUDIT_OUT`,
`U1_D2D_AUDIT_OUT` or `U1_ODD_KERNEL_AUDIT_OUT` to write its exact JSON witness.
The audits are covered by backend regression tests and never change
classification outputs to agree with a reference table.

`python gap/audit_oh_saved.py --output /tmp/oh-audit.json` audits the archived
spinless Oh result and its D4h, Th, O and Td restrictions, without rerunning
classification. It checks six native phase closures, three charge closures,
three phase-completion equations and three source closures. It also reproduces
the incoming charge-gauge phase `(1,1,0,1,1,1)` independently and confirms the
nonzero CI integer obstruction. The full surviving phase group Z2^5 injects
into the D4h phase quotient; its images in Th, O and Td have ranks 3, 0 and 2.
The surviving charge square restricts to the nonzero D4h/Th root phases and
the zero Td root phase. Every completed charge restriction passes the target
obstruction. The output records exact maps and hashes of the archived input,
current mathematical code and catalog backgrounds. These are consistency
checks within the supplied sector; identifying an individual native phase
with a physical center character requires an additional physical map.
