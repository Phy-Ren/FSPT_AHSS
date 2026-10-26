# Four-factor split block from the bottom Moore spectra

Derivation, 2026-10-26. Pending independent review of the indicated standard stable-homotopy facts.

Let N_i=2^{a_i}, a_i>=1, g=min_i N_i, and let t be the number of N_i equal to 2.
The proposed exact answer for the four-factor smash block in dimension five is

    t=0:  C_2 x C_g^3;
    t=1:  C_2^4;
    t=2:  C_4 x C_2^2;
    t>=3: C_2^3.

The existing exact tensor-resolution calculation independently gives a bosonic layer C_g^3 and a CF layer C_2 precisely when t<=2.
The issue here is to determine the full extension, especially t=2.

## Reduction to Moore spectra

Write M_N for the cofiber of N:S^0 -> S^0, with bottom inclusion i and top quotient q.
The reduced 2-skeleton of BC_N is Sigma M_N.
Its degree-three cell has zero cellular boundary.
Its stable attachment is in pi_1(M_N)=C_2 and, if nonzero, is detected by Sq^2 on the degree-one class.
The instability identity Sq^2 H^1=0 therefore makes this attachment stably zero.
Consequently the reduced 3-skeleton stably splits as Sigma M_N wedge S^3.

In the smash of four BC_N factors, cells of degree four or higher in a single factor first contribute in degree seven.
The S^3 summands first contribute cells in degree six, with zero attachment to the Moore smash summand.
They cannot affect pi_5.
Since the unit S -> MSpin is an isomorphism in stems zero and one, connectivity gives

    reduced Omega_5^Spin(smash_i BC_Ni) = pi_1(smash_i M_Ni).

## Moore identities used

For even N,

    pi_0(M_N)=C_N,  pi_1(M_N)=C_2.

The standard stable Moore relation is

    N id_(M_N) = (N/2 mod 2) i eta q.

Thus N id is null when 4 divides N, while 2 id_(M_2)=i eta q and 4 id_(M_2)=0.
Also pi_1(M_2 smash M_2)=C_4; its twice-generator is the image of eta on the bottom cell.
These facts can be proved from the cofiber exact sequences with the Hopf map and its standard Moore coextension.
They are the only low stable-homotopy inputs that still need an independent source/proof audit before publication.

## Computation

If t=0, take the smallest factor M_g.
Every remaining multiplication N_i on M_g is null, so each successive Moore smash splits as the preceding spectrum wedge its suspension.
The fourfold smash therefore has, in stems at most one, one M_g and three Sigma M_g summands.
Its pi_1 is C_2 x C_g^3.

If t=1, the same argument applies because every other N_i is divisible by four and 4 id_(M_2)=0.
The answer is C_2^4.

If t=2, begin with M_2 smash M_2.
The other two multiplications are null because they are divisible by four.
The stem-one group is pi_1(M_2 smash M_2) plus two copies of pi_0(M_2 smash M_2), namely C_4 x C_2^2.

If t=3, the third factor is the cofiber of multiplication by two on M_2 smash M_2.
That multiplication kills the bottom eta class by quotienting the C_4 in stem one by its double.
The Hurewicz map is then an isomorphism in stem one: the answer for three M_2 factors is C_2^2.
One further factor, whether M_2 or M_N with 4|N, gives C_2^3 in stem one.
There is no remaining bottom eta class to support a hidden extension.

This gives the stated four-factor group, including its order-four factor when exactly two cyclic factors have order two.
