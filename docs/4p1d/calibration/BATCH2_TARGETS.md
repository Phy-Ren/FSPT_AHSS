# Second-batch 4+1D interacting calibration targets

This is an independent reference ledger, not a list of completed classifier runs.
[batch2_targets.json](batch2_targets.json) records the exact backgrounds, groups,
source versions, and the small integer calculations used below. The targets are
for interacting electronic invertible phases with commuting internal symmetry,
`s=rho=omega=0`. The lower tuple is `(e2,n2,n4,nu5)`, with E8 included; the
uniform pair `(n0I,n0J)` is recorded separately. Internal groups have no
crystalline spinless/spin-half label.

The finite-group targets are **derived from primary bordism and homology
results**, rather than copied from a crystalline classification table. The use
of connective complex K-homology is justified as a low-degree Spin-c bordism
calculation below; it is not a free-fermion classification. Equality with these
groups tests additive extensions, but does not by itself identify every labelled
cochain root with a physical bordism character.

The reference arithmetic can be replayed with
`python scripts/verify_bordism_batch2.py`. Its
[saved replay](batch2_reference_replay.json) verifies all 55 targets, including
the finite Tor kernels and their prime-power annihilator counts. It uses only
the standard library and this reference ledger: no classifier modules or
computed campaign results. The report pins both input and verifier hashes and
states the theorem assumptions and prospective scope explicitly.

## Finite commuting groups

The full classification adds two free generators to every finite-group row.
They have a section obtained by making the finite symmetry act trivially.
The table displays only the zero-uniform finite group. Factors of order one
are omitted.

| Group | Zero-uniform interacting target | Calibration value |
|---|---|---|
| C2 × C2 | Z2² × Z4 × Z8² | First mixed incoming and stacking relations |
| C2 × C3 | Z3 × Z6 × Z72 | Independent presentation of the cyclic C6 control |
| C2 × C4 | Z2⁴ × Z4² × Z8 × Z16 | Unequal even orders; a different mixed kernel from C2 × C2 |
| C3 × C4 | Z2 × Z6 × Z12 × Z144 | Independent presentation of the cyclic C12 control |
| C2 × C10 | Z2 × Z10 × Z20 × Z40² | Independent 2- and 5-primary combination |
| C3 × C3 | Z3⁷ × Z9² | Odd-primary mixed extensions |
| C2 × C6 | Z2² × Z12 × Z24 × Z72 | Simultaneous 2- and 3-primary structure |
| C2 × C8 | Z2² × Z4³ × Z8² × Z32 | Unequal 2-primary exponents |
| C3 × C6 | Z3⁷ × Z18 × Z72 | Independent Sylow and mixed-order check |
| C4 × C4 | Z2⁶ × Z4² × Z8 × Z16² | Two non-elementary 2-primary factors |
| C3 × C9 | Z3⁶ × Z9³ × Z27 | Unequal 3-primary exponents |
| C4 × C8 | Z2³ × Z4⁴ × Z8² × Z16 × Z32 | Mixed kernel with three distinct exponents |
| C5 × C5 | Z5¹¹ | Odd-prime control without exceptional 2/3-primary extensions |
| C2 × C12 | Z2⁴ × Z4 × Z12 × Z24 × Z144 | Larger mixed-prime control |
| C2³ | Z2⁷ × Z4³ × Z8³ | Triple mixed terms invisible in the cyclic factors |
| C2⁴ | Z2²³ × Z4⁶ × Z8⁴ | Higher mixed terms and a large incoming quotient |

### The reduced degree-five Spin-c bridge, including odd primes

The published Anderson–Brown–Peterson spectrum splitting, stated in
[Buchanan–McKean, Theorem 3.6](https://doi.org/10.2140/agt.2026.26.485), is
**2-local**. It must not be used at odd primes without another argument.
The following low-degree argument is sufficient for all the finite groups here.

Let `a:MSpinC -> ku` be the connective Atiyah–Bott–Shapiro orientation. The
Spin-c Thom orientation is [Atiyah–Bott–Shapiro (1964), Theorem 12.3(ii)](https://doi.org/10.1016/0040-9383(64)90003-5).
For the determinant line `L`, let `x(L) in ku²(BSpinC)` be the complex-oriented
Euler class. Multiplying the Thom class by `x(L)²` defines a second map
`b:MSpinC -> Sigma⁴ku`. This construction supplies the map to the connective
cover directly. It is stronger than merely observing that a periodic K-theory
map is zero on two low homotopy groups.

On a four-manifold, the coefficient homomorphism `(a,b)` is

```
(index D_L, integral c1(L)^2).
```

For the canonical Spin-c structures on CP² and CP¹ × CP¹ the two pairs are
`(1,9)` and `(1,8)`, whose determinant is −1. These are therefore a primitive
basis of the degree-four coefficient group. In degrees zero and two the first
orientation is an isomorphism, with CP¹ of determinant degree two having index
one. The odd coefficient groups through degree five vanish; the coefficient
ranks are given in [Freed–Hopkins v6, Theorem 9.87](https://arxiv.org/abs/1604.06527v6).
Consequently the cofiber of `(a,b)` has no homotopy below degree six.

For a connected based space `X`, its reduced suspension spectrum starts in
positive degree. Smashing the cofiber with it therefore cannot change homotopy
in degree five. Thus the resulting natural map gives

```
reduced Omega5^SpinC(X) = reduced ku5(X) + reduced ku1(X).
```

The sign of the Euler-class convention changes neither `x(L)²` nor the
primitive-basis test. This is a reduced degree-five statement. It does not
assert an integral equivalence through degree seven or a universal
identification of the project's full cochain model with a physical spectrum.
For finite G, the character group of Omega5 has the same invariant factors;
the rational degree-six part supplies precisely the two uniform responses.

### Rank-two targets from an exact Tor kernel

[Bruner–Greenlees (2003), Proposition 3.4.3(1), pp.69–70](https://doi.org/10.1090/memo/0785)
gives the cyclic ku-homology module from the representation ring. Equivalently,
write `|u|=2`, `|z_j|=2j+1`, and choose signs of generators so its relations are

```
sum_{k=0}^j binom(N,k+1) u^k z_(j-k) = 0.
```

The degree-five cyclic term is the cokernel of the three-row matrix

```
[N,          0,          0]
[binom(N,2), N,          0]
[binom(N,3), binom(N,2), N].
```

The degree-one term is Z_N. This keeps the extensions already present in each
cyclic factor, before taking a product.

The free ku-module resolution of a cyclic classifying space is obtained from
the Thom/Gysin sequence of the Nth tensor power of the universal line. See
[Bruner–Greenlees, Section 2.2, pp.32–33](https://doi.org/10.1090/memo/0785), and
[BMSS v1, Sections 2.1–2.8](https://arxiv.org/abs/1008.0166v1) for the resulting
length-one resolution and Kunneth sequence. BMSS formulates its calculation
for prime order. The same free resolution for general N follows directly
from that Gysin sequence: its diagonal coefficient is the nonzero integer N,
so the map between the free modules remains injective. No claim that a
prime-only theorem was printed for arbitrary N is needed.

In the odd degree five of a two-factor smash product, the tensor term vanishes
by parity. Thus there is **no unresolved Kunneth extension**: the answer is
exactly the degree-four Tor kernel. Put

```
A_N = <x,y,z | N*x=0, binom(N,2)*x+N*y=0, N*z=0>,
D_M(x,y,z) = (M*x+binom(M,2)*z, M*y, M*z).
```

Then

```
ku5(BC_N smash BC_M) = ker(D_M:A_N -> A_N).
Omega5^SpinC(B(C_N x C_M))
  = ku5(BC_N) + ku5(BC_M) + ker(D_M) + Z_N + Z_M.
```

These equations, not a guessed AHSS collapse, determine each target. The JSON
contains `A_N`, `D_M`, and the numbers of kernel elements annihilated by each
prime power. In the recorded cases the domain has at most 125 elements. Those
counts determine every elementary divisor, independently of the classifier's
cochain arithmetic and Smith-normal-form calculation.

For example, for N=2 and M=4, `A_2=Z4+Z2`, and `D_4=0` because `4A_2=0`
and `6x=0`. The mixed term is therefore `Z4+Z2`. In contrast, for N=M=2,
`D_2` has an order-two image and its kernel is Z4. This explains why simply
copying the mixed C2 × C2 relation to C2 × C4 would fail.

For N=M=p, [BMSS, Theorem 2.12](https://arxiv.org/abs/1008.0166v1) independently
gives the odd-degree smash group as
`sum_(i=1)^(p-1) ku_(5-2i)(BC_p)`. It yields Z4 at p=2, Z3³ at p=3,
and Z_p³ at p≥5, agreeing with the explicit Tor kernel. Products with coprime
orders give a zero mixed kernel and recover the cyclic product control.

### Higher elementary abelian 2-groups

Use the **spectrum** decomposition in
[Bruner–Greenlees, Proposition 4.2.3, p.83](https://doi.org/10.1090/memo/0785),
together with the Eilenberg–Mac Lane multiplicities in
[BMSS, Theorem 2.12](https://arxiv.org/abs/1008.0166v1). For `P=BC2` it is

```
ku smash P smash P
  = Sigma²(ku smash P) wedge Sigma² H(F2[u,v]), |u|=|v|=2.
```

Because this is a spectrum equivalence it may be smashed with further copies
of P. An abstract graded-group isomorphism alone would not justify that step.
The degree-five reduced ku groups of `P`, `P^smash2`, `P^smash3`, and
`P^smash4` are respectively Z8, Z4, Z2⁴, and Z2³. For the triple smash,
the last two contributions are `H3(P;F2)` and two copies of `H1(P;F2)`;
for the quadruple smash the ordinary-homology contribution is
`H3(P smash P;F2)=F2²`, in addition to the suspended triple-smash term.

Splitting the cartesian product into all nonempty smash products gives, for
r=1,...,4,

```
ku5(B(C2)^r) = Z8^r + Z4^binom(r,2)
              + Z2^(4*binom(r,3)+3*binom(r,4)),
ku1(B(C2)^r) = Z2^r.
```

This proves the C2³ and C2⁴ rows, including the extra mixed order-two terms.
Their absence in a representation-only calculation would be a real failure
of completeness, even if all cyclic restrictions matched.

## Translation benchmarks

For `G=Z^r`, r=1,...,4, the linear action and all twists are trivial. The stable
splitting `T^r_+ = wedge_k binom(r,k) S^k` gives the following exact groups.
The crystalline interpretation uses the same generalized-cohomology framework
as [Thorngren–Else v6, Section III.C](https://arxiv.org/abs/1612.00846v6).

| Translation rank | e2 rank | n2 rank | n4 rank | nu5 rank | Zero-uniform group | Full group |
|---|---:|---:|---:|---:|---|---|
| 1 | 0 | 0 | 0 | 0 | 0 | Z² |
| 2 | 1 | 1 | 0 | 0 | Z² | Z⁴ |
| 3 | 3 | 3 | 0 | 0 | Z⁶ | Z⁸ |
| 4 | 6 | 6 | 1 | 0 | Z¹³ | Z¹⁵ |

The ranks are `2*binom(r,2)+binom(r,4)`, plus two in the full sector. This uses
the interacting coefficient groups `TP5=Z²`, `TP3=Z²`, `TP1=Z`, and
`TP4=TP2=0` from [Freed–Hopkins v6](https://arxiv.org/abs/1604.06527v6).
The n4 generator at rank four is charge per unit cell and is retained. Removing
atomic filling would change the classification problem. These examples test
free groups and cannot be justified by finite-group averaging.

For later mixed batches the same splitting gives an entire family of targets
for `G=Z^r x C_N`. Define `A5(N)` to be the accepted cyclic zero-uniform target
and `A3(N)=Z_(N/g2)+Z_(g2*N)`, where `g2=gcd(N,2)`. Then

```
TP5(Z^r x C_N) = A5(N)
  + A3(N)^binom(r,2) + (Z_N)^binom(r,4)
  + Z^(2+2*binom(r,2)+binom(r,4)).
```

Here `TP4(C_N)=TP2(C_N)=0`, `TP3(C_N)=Z²+A3(N)`, and
`TP1(C_N)=Z+Z_N`; the cyclic lower bordism inputs follow from the same
Gysin presentation. The zero-uniform group removes only the displayed uniform
Z². Twelve targets with r=1,...,4 and N=2,3,4 are recorded as prospective
examples. This is a derivation from stable splitting, not a claim that these
mixed translation backgrounds have already been computed by our formulas.

## Expanded cyclic controls and source provenance

The second ledger also records the 23 cyclic orders
`11,13,14,17,19,20,21,22,23,24,25,26,27,28,29,30,31,32,36,40,48,54,64`.
Their physical targets use the reviewed v0.15 all-N eta-kernel and bordism-order
proof, with `g2=gcd(N,2)` and `g3=gcd(N,3)`:

```
A5(N) = Z_(N/(g2*g3)) + Z_(N/g2) + Z_N + Z_(g2*g2*g3*N).
```

The cases C32 and C64 have a separate directly published
[Bahri–Gilkey (1987), Theorem 0.1(b) and following Remark](https://doi.org/10.2140/pjm.1987.128.1)
comparison: respectively `Z16²+Z32+Z128` and `Z32²+Z64+Z256`.
Their theorem is not credited with the general all-N formula.

The source ledger pins the same versions as the first batch, adding:

- M. F. Atiyah, R. Bott and A. Shapiro, *Clifford modules*, Topology 3,
  Supplement 1 (1964), 3–38, Theorem 12.3(ii),
  DOI [10.1016/0040-9383(64)90003-5](https://doi.org/10.1016/0040-9383(64)90003-5).
- R. R. Bruner and J. P. C. Greenlees, *The connective K-theory of finite
  groups*, Memoirs of the AMS 165, no.785 (2003), Sections 2.2, 3.4 and 4.2,
  DOI [10.1090/memo/0785](https://doi.org/10.1090/memo/0785).
  The [author's accepted manuscript](https://digitalcommons.wayne.edu/mathfrp/84/)
  was read in full at the required theorem locations.

All finite and translation entries retain the exact direct-product background.
A nontrivial charge conjugation, time reversal, projective extension, rotation
representation, or nonsymmorphic action requires a different comparison.
