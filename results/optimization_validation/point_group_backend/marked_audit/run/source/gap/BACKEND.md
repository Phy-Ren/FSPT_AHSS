# Native cochain backend

`backend.g` loads HAP and local `backend_resolution.g` and `backend_bar.g`.
It does not load SptSet, its tables, its objects, or its spectral sequence.
`backend_diagonal.g` is optional and must be loaded after `backend.g`.

## Coefficient and row conventions

`AFSBackend(number)` retains the full infinite affine space group. `ctx.G` is
its Pcp presentation; `ctx.iso` identifies the affine matrices with it.
`ctx.sign(g)` is the exact determinant of the affine linear action, and
`ctx.s(g)=(1-sign(g))/2`. For orientation-preserving groups, `ctx.s=AFSZero`.
Physical spin-half convention uses effective internal omega_2=0 in the formula
layer; the backend itself does not assume a fermionic obstruction or survivor.

Native cochains are row vectors. `AFSDifferential(ctx,k,coeff)` is the matrix
C^k -> C^(k+1), so the coboundary of a row v is v*D. Coefficients are `F2`,
`Z` (untwisted), `Zs` (determinant-twisted), and `U1s` (twisted R/Z).
`AFSCohomology(ctx,k,coeff)` returns `.generators`, `.orders`, and
`.coordinates(native_vector)`; order 0 denotes an infinite cyclic factor.
A failed cocycle/class conversion returns `fail`.

Integral cohomology uses exact Smith transformations of D_k to obtain the
integer kernel lattice; D_(k-1) is expressed in that lattice and a second
Smith form gives the quotient. F2 cohomology uses an echelon boundary span
completed to the cocycle span. Every native representative is retained.

For k>=4, H^k(G,U1_s) is identified with torsion H^(k+1)(G,Z_s). Crystallographic
G has a finite-index Z^3 subgroup, so its real cohomology vanishes above degree
3. The torsion of coker D_k is already the torsion of H^(k+1): the following
coboundary maps to a torsion-free group. This avoids constructing degree 7.
If U D_k V = diag(d_i), a U1 representative is U_i/d_i for |d_i|>1. For a
closed phase row a, its coordinates are the corresponding entries of
(a D_k)V modulo |d_i|. Native U1 vectors contain exact rational phases reduced to [0,1). This reduction
is equality in R/Z, not an approximation, and prevents large irrelevant
integer parts from entering later polynomial formulas.

## Comparison and primitives

`AFSBar(ctx,k,coeff,v)` produces a memoized normalized bar callback
`f(g1,...,gk)` on actual Pcp elements. `AFSNative(ctx,k,coeff,f)` evaluates it
on native cells. `AFSSolveNative(ctx,k,coeff,v)` returns a native primitive
of degree k-1, or `fail`; both Smith and F2 elimination factors are cached.

A native primitive alone is insufficient on bar cochains. For a closed input
cochain (a precondition supplied by each obstruction identity), `AFSSolve` retains
the exact comparison homotopy: F:C->B, G:B->C and h satisfy
FG-id = d h+h d. Its returned bar primitive is G^*(b)-h^*(f). Thus the
primitive satisfies the original bar equation (modulo 2 or 1 as appropriate),
not merely the transferred native equation. Tests use boundaries of arbitrary
bar cochains, rather than only callbacks arising from native representatives.

The comparison maps are constructed independently from contracting homotopies
by F=s_B F d_C, G=s_C G d_B and h=s_B(FG-id-h d_B). Their terms, contractions,
and tuple evaluations are cached. Reduced translated-cell contractions are
cached once; callers treat these cached words as immutable.

On a normalized bar basis, F and h always have leading group one. Consequently
all but the first face of h(d_bar) vanish under the bar contraction. The
implementation discards these terms before recursing. `AFSHomotopyPullback`
evaluates the resulting alternating suffix sum directly on a cochain, while
`AFSChainHomotopy` retains the full chain witness. Native contractions of
identity-leading G faces are separately cached without assuming h squared is
zero. Chain-word equality and arbitrary F2/U1 boundary primitives test these
optimizations.

`AFSChainToBarCombination(bar,k,z)` constructs F(z)=s_bar F(dz) after combining
the group-ring boundary of a scalar native chain. Closed-phase torsion periods
use it on the integral Smith dual cycles, avoiding individual top-degree bar
maps whose terms would subsequently cancel.

## Resolution and native cup operations

The affine resolution is HAP's twisted tensor product of a finite holonomy
resolution and the translation-lattice resolution. The section is centered in
a lattice fundamental parallelepiped. A synchronized element registry replaces
linear searches without changing group elements. Standard finite presentations
are transported to the actual holonomy group by verified isomorphisms.
Factor boundaries and contractions are cached with fresh returned words to
protect against mutation within HAP.

An independent explicit rank-three Koszul resolution is available with
`AFS_USE_KOSZUL:=true`. It is validated by the signed contraction identity on
positive and negative lattice translations. It remains optional: current
measurements do not show a material cubic-construction speed advantage.

`AFSNativeCup(ctx,i,p,a,q,b)` evaluates the mod-two cup-i on native vectors.
The higher diagonals obey d D_i+D_i d=(1+tau)D_(i-1), with D_0 a diagonal
chain map. They are built using the tensor contraction
K=h tensor id + eta*epsilon tensor h. Only bidegrees that can contribute to
(p,q) are constructed; discarded components cannot return because K only
raises a tensor-factor degree. The group-valued tensors are then compiled to
sparse mod-two basis-index pairs and reused for every input vector.

Native and bar cup representatives need not agree as cochains. Their induced
cohomology operations are compared before use, including F2 classes before
the map x -> x/2 to U1. Native primitives for secondary formulas are still
corrected by the exact comparison homotopy.

`AFSNativeSq2U1Coordinates(ctx,p,a,target)` evaluates j Sq^2 directly in the
Smith coordinates of `target=AFSCohomology(ctx,p+2,"U1s")`. If
U D_(p+2) V = diag(d), the coordinate at an even torsion index j is
(d_j/2) times the mod-two pairing of Sq^2(a) with column j of U^-1;
odd-order factors receive zero. For p=2, scalar native chains are combined
before tensor contraction. For p=3 the projected cup_1 evaluator supplies the
native vector because its compressed intermediate chains are faster. The
operation is compared to the full native square, including sums of generators.

The finite-factor constructors explicitly request HAP's `"extendible"` mode.
HAP's default final resolution term omits the complete top contracting table;
at length six it provides boundaries through degree six but does not support
all h_5 evaluations. Keeping that table certifies signed contractions through
h_5 without changing lower-degree cochain operations. Tests check the entire
group-ring d^2 through degree six and translated-cell contraction identities,
including negative products, through degree five.

`AFSNativeCup1Projected(ctx,p,a,q,b)` is an additional exact cup_1 evaluator.
It computes each bidegree separately and forgets right group labels once
only left-factor contractions remain. Both augmented D_0 components are the
same map T_n=h T_(n-1) d with T_0=id. Their sum vanishes over F2, so the
left-degree-zero D_1 seed vanishes inductively. D_0 marginals retain the full
T seed; the implementation does not assume h(e,1)=0 or h squared is zero.
Equality with full native vectors, rather than only cohomology classes, is
tested.

Large differential Smith forms first eliminate unit pivots with exact integer
row and column operations. Both transformations and both inverse transformations
are updated at every pivot. GAP's Smith form handles the residual block; this
preserves the complete integral presentation, including odd torsion and free
parts. Random rectangular matrices are compared with GAP's standard Smith
invariants, and cubic differentials certify U D V=diagonal, U Ui=I and V Vi=I.
For SG230, degree-four and degree-five Smith data took 1.2 and 5.4 CPU seconds,
compared with approximately 19.5 and 108 seconds before this preconditioning.

## Mod-two contraction and optional performance experiments

`backend_mod2_contraction.g` reconstructs the twisted tensor product's
contracting homotopy modulo two, cancelling terms after every linear stage.
It uses only the recorded point/lattice factors and the native boundary.
Setting `AFS_USE_MOD2_CONTRACTION:=true` and reading this module before
`backend_diagonal.g` selects it for mod-two diagonals. The integral comparison
maps and exact bar primitives retain the integral contraction. The main `run_one.g` driver enables this option by default; setting the flag
to false before reading the driver restores the integral contraction. The
startup line reports the actual selected function, and JSON records
`native_mod2_contraction` plus `native_mod2_cache_degrees` (zero if the
perturbation cache was not needed). Other stand-alone callers retain the
integral default unless they explicitly load and select this module.

The change is an equality of native chains modulo two, not merely an equality
of cohomology operations. Write the extension boundary as the vertical part
plus the sum of terms lowering point-group degree. The original perturbation
contraction consists of finite linear sums, vertical and finite-factor
contractions, horizontal boundaries, and translates of group-ring basis
elements. Reduction modulo two commutes with every one of these operations.
Cancelling equal terms after each stage therefore gives exactly the reduction
of the integral contraction. The recursive correction terminates because its
point-group degree decreases. Induction in the higher-diagonal recurrence
then gives equality of the entire native diagonal modulo two. In particular,
the CF-only stacking shortcut consumes the same native phase seed, not just
a cohomologous seed. Integral comparison maps and exact bar primitives do not
use this replacement. Resolutions without recorded extension factors fall
back to reducing the original integral contraction.

Controls compare translated native-cell words through degree four for SG104,
219 and 226, including inverse products. All 38 H3-generator native squares
of SG47 agree exactly with an independently run integral-contraction source.
For SG219 and SG226, all native square coordinates agree with a separate
projected-cycle computation using the original integral contraction; these
include the order-six target coordinate in SG219. Complete integral native-vector comparisons also pass: 4 vectors of length
102 for SG219 and 9 vectors of length 231 for SG226 agree entry by entry.
Primary native Sq2 took 462.456 and 411.270 CPU seconds on those two groups;
the corresponding integral probe took 1009.767 and 912.855 seconds. The
loaded source-file hashes, complete vectors, raw logs and timings are in
`docs/validation_runs/backend_mod2.json`.

`backend_cup_slant.g` offers `AFSNativeCup1Slant`: it evaluates a fixed right
cochain during the recursion rather than retaining all right basis indices.
It is tested on arbitrary mixed native cochains against the full tensor
evaluator, but is not loaded by production drivers.
