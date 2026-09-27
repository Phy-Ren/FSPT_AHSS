# Finite crystallographic point groups: physical and mathematical scope

The completed calculation has 32 finite matrix groups in dimension three, each in
two crystalline spin conventions. Its group is the finite point group `P`
itself. It is neither an affine space group nor the symmorphic infinite group
`Z^3 semidirect P`. No translation subgroup or weak translation decorations
are introduced. The 64 computations were frozen before comparison to reference
classification or stacking answers; the accepted data are in `results/point_groups`.

## Faithful matrix representation and backgrounds

The input is the actual faithful three-dimensional real representation `V`.
Groups with isomorphic abstract multiplication tables must remain distinct
when their representations differ. A proper twofold rotation, a mirror and
inversion are all abstract `C2`, but have different `V`, orientation and/or
fermion-extension background.

| Crystalline convention | Effective internal sign | Effective internal extension |
|---|---|---|
| Spin-half | `s=w1(V)` | `omega=0` |
| Spinless | `s=w1(V)` | `omega=w2(V)+w1(V)^2` |

The second background is represented by the exact Pin-minus double cover of
the finite matrix group. For a mirror, `w2=0` and `omega=s^2`; for a proper
twofold rotation, `s=0` and `omega` is its nontrivial square class; for inversion
on three axes, `w2=w1^2` and the effective extension is zero. These are
background identities, not classification answers.

An affine-group trivialization of a pulled-back Pin-minus cocycle cannot be
reused automatically on `P`. A nonsymmorphic extension or a translation
cochain can kill an inflated class on the infinite group even when its finite
point-group class is nonzero. Any zero-background gauge reduction in the new
calculation must be certified on the finite group anew.

## Geometry catalogue

`MatGroupZClass(3, representative_it_number)` is used only as a public CrystCat
matrix catalogue. The representative IT number below selects a geometric
matrix class; it does not identify the finite calculation with that infinite
space group or import a space-group result. Cohomology is computed on a Pcp
copy of the finite matrix group, using a finite-group resolution.

| HM | Schoenflies | Order | Matrix catalogue key |
|---|---|---:|---:|
| 1 | C1 | 1 | 1 |
| −1 | Ci | 2 | 2 |
| 2 | C2 | 2 | 3 |
| m | Cs | 2 | 6 |
| 2/m | C2h | 4 | 10 |
| 222 | D2 | 4 | 16 |
| mm2 | C2v | 4 | 25 |
| mmm | D2h | 8 | 47 |
| 4 | C4 | 4 | 75 |
| −4 | S4 | 4 | 81 |
| 4/m | C4h | 8 | 83 |
| 422 | D4 | 8 | 89 |
| 4mm | C4v | 8 | 99 |
| −42m | D2d | 8 | 111 |
| 4/mmm | D4h | 16 | 123 |
| 3 | C3 | 3 | 143 |
| −3 | C3i | 6 | 147 |
| 32 | D3 | 6 | 149 |
| 3m | C3v | 6 | 156 |
| −3m | D3d | 12 | 162 |
| 6 | C6 | 6 | 168 |
| −6 | C3h | 6 | 174 |
| 6/m | C6h | 12 | 175 |
| 622 | D6 | 12 | 177 |
| 6mm | C6v | 12 | 183 |
| −6m2 | D3h | 12 | 187 |
| 6/mmm | D6h | 24 | 191 |
| 23 | T | 12 | 195 |
| m−3 | Th | 24 | 200 |
| 432 | O | 24 | 207 |
| −43m | Td | 24 | 215 |
| m−3m | Oh | 48 | 221 |

There are 11 orientation-preserving and 21 orientation-reversing types. The
implementation checks exact order, matrix/Pcp correspondence and the
determinant character on the whole finite group. The independent
[`point_group_geometry.py`](../../fspt/point_group_geometry.py) constructs
all 32 types from explicit Cartesian or hexagonal-lattice rotations and
reflections. Its element order/trace/determinant spectra bind each HM label
to its faithful real representation; self-consistency of an exported matrix
set alone would not exclude swapping two labels. All 64 archived spectra
match these independently generated fingerprints. Names are compared by
HM and representation, not row numbers in supplied tables: their `O`/`Td`
ordering is not uniform.

## Integer layers and incoming quotients

For a finite group, `H^1(P,Z_s)` has no free part. If `s=0`, an integer
one-cocycle is a homomorphism from a finite group to `Z`, hence vanishes.
If `s` is nontrivial, its restriction to `ker(s)` vanishes for the same reason;
it is constant, with integer value `m`, on the odd coset. Coboundaries change
`m` by an even integer. Thus `H^1(P,Z_s)=Z2`, represented by `n=s`.
This is only the input integer cohomology: its torsion class must still pass
the actual outgoing obstructions. It is not a claimed surviving p+ip answer.

In degree zero, `H^0(P,Z_s)=Z` for `s=0` and is zero for nontrivial sign. The
unitary `H0` p+ip incoming quotient must therefore be retained. In a nonzero
background, its canonical full lower state is `X=(omega,0,F)` in the supplied
unary normalization. Quotient the complete lower stacking group by `<X>` and
recover graded factors from the filtered relation lattice. It is insufficient
to remove only the leading MC class. For nonunitary groups, the nonclosed
integer gauge that removes `2s` can still affect the torsion upper square;
vanishing closed `H0` does not remove that gauge step.

## Atomic parity and comparison scope

The requested unreduced physical convention retains the atomic fermion-parity
sector wherever the full decoration theory places it. Therefore the new
finite computation retains the CF layer and all its actual relations; it
does not discard that layer merely as an atomic contribution. Nor does it
append an independent universal `Z2` by hand. Adding a separate odd state at
a selected spatial origin, or quotienting by all such states, would require
a separately specified relative/reduced classification problem.

Finite point-group answers are not obtained from an affine-space-group table
by deleting free `Z` factors. Translation-dependent lower layers and gauges
also differ. Reference comparisons must match the faithful representation,
effective extension, dimension and atomic convention.

The general upper p+ip product has the same input limitation as in the affine
calculation. A computed witness under a selected calibrated product verifies
that model, not uniqueness of the physical product. An abstract extension
family may determine a group independently of unspecified higher carries;
where it does not, retain the ambiguity. Independent finite physical
benchmarks can calibrate a candidate product only after the independent
calculations are frozen, and must not be replaced by the same product's own
output as its justification.
