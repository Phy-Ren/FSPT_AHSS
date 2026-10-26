# Complete two-factor nonsplit classification from circle Gysin sequences

Derivation, 2026-10-26.
Let m and N be positive powers of two, both at least two.
The symmetry is C_(2m)^f x C_N.
This argument proves completeness of the rank-two cubic lattice; it does not extrapolate free-fermion completeness to additional factors.

## Geometric model and low coefficient groups

A Spin--C_(2m) structure is a Spin^c structure with a trivialization of L0^m, where L0 is the Spin^c determinant line.
An independent C_N gauge field is a line L1 with a trivialization of L1^N.
Thus the required bordism spectrum is the iterated circle-fiber construction for L0^m and L1^N over Spin^c bordism with one extra BU(1) factor.
Both powers have canonical spin orientations because m and N are even.

In dimensions at most seven, Spin^c bordism has zero odd groups and free even groups, with ranks 1,1,2,2 in degrees 0,2,4,6.
The BU(1) Atiyah--Hirzebruch sequence therefore has no differentials or torsion extensions in this range.
The ranks of Omega_2, Omega_4, Omega_6 of Spin^c(BU(1)) are respectively 2,4,6.

The two circle Gysin sequences give the Koszul complex in total degree five:

    Omega_6 --(e0,e1)--> Omega_4 + Omega_4 --(e1,-e0)--> Omega_2.

The desired finite group is its middle homology.
There is only one nonzero filtration term in total degree five: the cube has length two and all base odd groups vanish.
Hence there is no later differential or hidden extension to add.
Rationally, the Euler complex is exact, as the two finite-group trivializations leave no rational degree-five bordism.
The first map is consequently injective and the middle homology is the torsion subgroup of its cokernel.
Since the image of the second map is free, taking the torsion subgroup introduces no further extension.

## Integral index bases

For an odd Spin^c charge q0 and an integer extra charge q1, use the six degree-six index polynomials

    v1=q0,
    v2=(q0^3-q0)/24,
    v3=q1,
    v4=(q1^3-q1)/6,
    v5=(q0^2-1)q1/8,
    v6=(q0 q1^2-q1)/2.

All are integer-valued on this charge lattice.
They form a primitive geometric basis, rather than merely a rational basis:

- CP^3 with determinant 2H and trivial extra line has index 4v2.
- CP^2 x S^2 with determinant H+2K and trivial extra line has index 3v2.
  Their difference realizes v2.
- The same product with determinant 3H+2K has index 27v2+v1, realizing v1 after subtraction.
- The product with determinant H and extra line K realizes v5.
- Determinant 3H and extra line K give 9v5+v3, realizing v3.
- CP^3 with trivial determinant and extra line H realizes v4.
- CP^2 x S^2 with determinant H+2K and extra line H has index 3v2+4v5+v6+v3, realizing v6.

Here H and K are the standard integral degree-two classes on CP^2 and S^2.
These geometric indices and the rank-six computation prove that this is the full integral index lattice.
Evaluation on odd q0 and integer q1 also spans its full dual: successive choices q0=1,3 and q1=0,1,-1,2 isolate the six coordinates.

In degree four, a primitive geometric index basis is

    1, (q0^2-1)/8, q0 q1, (q0 q1+q1^2)/2.

It is realized by CP^2 and S^2 x S^2 with suitable determinant and extra line bundles.
Evaluation at (1,0),(3,0),(1,1),(1,-1) spans its full dual.
In degree two the index basis is q0,q1.

## Euler maps and the exact finite presentation

The spin Euler characters are

    L0^(m/2)-L0^(-m/2),  L1^(N/2)-L1^(-N/2).

Accordingly the Euler maps act on index polynomials by the central differences

    P(q0+m,q1)-P(q0-m,q1),
    P(q0,q1+N/2)-P(q0,q1-N/2).

Dualizing the first map in the Koszul complex gives the finite charge-lattice presentation with six generators and relation rows

    v(q0+2m,q1)-v(q0,q1),
    v(q0,q1+N)-v(q0,q1).

The centers of the first differences remain odd because m is even.
The centers of the second differences remain integral because N is even.
Each row is an integer-valued polynomial of total degree at most two in t=(q0-1)/2 and q1.
Finite-difference interpolation therefore proves that t,q1 in {0,1,2} generate all relations over the integers.
This is the fixed 18-by-6 presentation implemented in two_factor_cubic_lattice.py.
Its Smith factors are the full classification group, with no undetected bosonic summand in this rank-two case.

## Why this does not assert free-fermion completeness in general

With three or more circle constraints, additional odd Koszul filtration degrees can contribute in total degree five.
These are precisely the extra contributions that the cubic charge presentation can miss.
The general theorem therefore treats supports with at least two extra cyclic factors using the separately derived cochain/Smith calculation, not this rank-two argument.
