# S4: an independent full class-A bordism computation

This calculation uses the **crystallographic rotoinversion group S4 = C4**,
not the permutation group on four letters. It is independent of the supplied
cochain differential and stacking formulas. For both physical spins it gives

```
G(3+1D,S4,U(1)^f) = Z2 x Z2 x Z4
```

within the phase-homology/Spin-c-bordism framework. This agrees with the current
four-data answer and disagrees with the journal's Z2^4. The argument determines
the group, including extensions; it does not give a microscopic identification
of every cochain generator.

## Spatial representation and the physical spin dictionary

The current matrix generator is explicitly conjugated in `S4_gysin.py` to a
real sign line sigma plus a real plane L carrying a complex quarter-turn.
Thus V = sigma + L, and Det(V)=sigma.

For physical spinless class A, the crystalline Thom twist is
`3-V = (1-sigma)+(2-L)`. The virtual complex line `2-L` is Spin-c oriented and
has real rank zero; its Thom isomorphism introduces no shift. For physical
spin-half, the determinant twist is `sigma-1`. If one uses the split-extension
version of the shearing theorem, it gives the equivalent `3-V` expression.
The difference `(1-sigma)-(sigma-1)=2-2sigma` is itself a rank-zero virtual
complex line, so both spins reduce to

```
MTSpin-c smash X,             X=(BC4)^(sigma-1).
```

This is the class-A dictionary of
[Debray v3, Theorem 2.24](https://arxiv.org/abs/2102.02941v3), together with the
Spin-c Thom isomorphism. It is not a Pin-minus superconductor computation.
All vector-bundle operations above have their ranks subtracted explicitly.

The rank-zero Thom spectrum X is connective: the Thom space of sigma begins
in cell degree one, and the subsequent desuspension is by one. The 7-connected
map `MTSpin-c -> ku wedge Sigma^4 ku` therefore gives

```
Omega_4^Spin-c(X) = ku_4(X) + ku_0(X).
```

Both summands must be retained. Debray's section 3.2 states this natural
low-degree comparison, attributing it to Anderson--Brown--Peterson.

## The sign-line cofiber is an actual subgroup map

The unit sphere bundle of sigma over BC4 is
`EC4 x_C4 {+1,-1} = BC2`, where C2 is the kernel of the sign character.
The disk bundle retracts to BC4. Hence the Thom cofiber sequence is

```
BC2_+ --i--> BC4_+ --> (BC4)^sigma = Sigma X.
```

The first arrow is the ordinary subgroup inclusion, not a transfer or the
quotient C4->C2. The `ku` long exact sequence shows

```
ku_4(X) = coker[ku_5(BC2) --i_*--> ku_5(BC4)],
```

because `ku_4(BC2)->ku_4(BC4)` is the identity on the sole free basepoint Z.
The corresponding positive reduced even cyclic `ku` groups vanish. The same
argument in degree zero gives
`ku_0(X)=coker[ku_1(BC2)->ku_1(BC4)]`.

## Natural inclusion map from the Gysin sequence

Use the complex orientation convention of Shin Hashimoto,
[*On the connective K-homology groups of the classifying spaces BZ/p^r*,
Publ. RIMS **19** (1983), 765--771](https://doi.org/10.2977/prims/1195182451).
The [publisher PDF](https://ems.press/content/serial-article-files/42160)
was downloaded and ingested to the canonical cache. Section 2, especially
Proposition 2.1 and Lemmas 2.5--2.6, gives the Gysin presentation below.

Let eta be the universal complex line on CP-infinity, x its `ku` Euler class,
and u the Bott coefficient. Then

```
[m]_F(x) = ((1+ux)^m-1)/u.
```

Model BCm as the unit circle bundle of eta^m. The subgroup inclusion BC2->BC4
is the map on these circle bundles induced by fiber squaring
`eta^2 -> eta^4`; its base map on CP-infinity is the identity. The maps on
disk/sphere bundles induce a natural map of Gysin cofiber sequences.

Under the complex Thom identifications, the induced map on Thom spaces is
multiplication by

```
Q = [4]_F(x)/[2]_F(x) = 2 + 2ux + u^2 x^2.
```

One can verify this without choosing a finite-group self-duality: pull back
the Thom class along fiber squaring, then restrict to the zero section.
Its coefficient q must satisfy `q [2]_F(x)=[4]_F(x)`. The Euler series
`[2]_F(x)` is not a zero divisor in the coefficient power-series ring, so q
is exactly Q. The dual map in homology is cap product by Q.

In degree five the Gysin target is `ku_4(CP-infinity)`, with its three
connective basis elements `u^2 beta_0, u beta_1, beta_2`. Higher powers of x
cap into negative connective degree and vanish, so the quadratic truncation
is exact in this degree.

Hashimoto's Gysin generators B0,B1,B2 in degree five satisfy

```
m B0 = 0,
binom(m,2) B0 + m B1 = 0,
binom(m,3) B0 + binom(m,2) B1 + m B2 = 0.
```

Using columns for relations and for generator images, the matrices are

```
A2 = [2 1 0]       A4 = [4 6 4]       Q = [2 2 1]
     [0 2 1]            [0 4 6]           [0 2 2]
     [0 0 2]            [0 0 4]           [0 0 2].
```

They obey `A4 = Q A2`. Consequently the inclusion sends `[v]` to `[Qv]`
between `Z^3/A2 Z^3` and `Z^3/A4 Z^3`. Its cokernel is exactly
`Z^3/Q Z^3`. This is a natural geometric map computed from the Gysin sequence.
Hashimoto explicitly warns in section 1 that the abstract finite abelian
self-duality used there is not natural; none is used here.

The exact Smith forms are

```
SNF(A2) = (1,1,8),
SNF(A4) = (2,2,16),
SNF(Q)  = (1,2,4).
```

Thus `ku_4(X)=Z2 x Z4`. In degree one the map is multiplication by 2 from
Z2 to Z4, so `ku_0(X)=Z2`.

The inclusion in odd cyclic `ku` degree five is injective: if `Qv` lies in
`A4 Z^3=Q A2 Z^3`, then `v` lies in `A2 Z^3` because Q is nonsingular over Q.
The same is true in degree one. The cofiber long exact sequence therefore also
gives `ku_5(X)=ku_1(X)=0`. There is no degree-five free Hom contribution in the
Anderson-dual phase classification. All possible torsion primes here are 2.

It follows that the full finite class-A group is `Z2^2 x Z4`, for both spins.
The exact script additionally binds this to both current spatial inputs by
their hashes and their actual representation decomposition.

## Reproduce

```
python S4_gysin.py
```

Output: `S4_gysin.json`. This small integer computation tests the derived
presentation and input geometry; it is not a replacement for the geometric
Gysin-map proof above.
