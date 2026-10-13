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
