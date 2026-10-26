# Final decoration layers and stacking extensions

This note distinguishes the final decoration-layer quotients from the stacking group.
The four layers, from lowest to highest decoration, are the integer p+ip input n2, Majorana input n3, complex-fermion input n4, and bosonic phase nu5.
Each layer is taken after all obstruction conditions and incoming identifications.
Their product gives the order of the stacking group, but the layers need not split as groups under stacking.
The calculations below determine the layers from the cochain maps and exact filtration presentations, rather than assigning them from the final invariant factors.

## The split elementary family

For G_f=C2f x C2^r, the final p+ip, Majorana, and complex-fermion layers are all trivial.
The final bosonic layer is

    C2^(3 binom(r,3) + 3 binom(r,4) + binom(r,5)).

The stacking group is therefore this same elementary group.
There are no nontrivial extensions between decoration layers.

The stable splitting gives the following contributions for a support containing k cyclic factors:

| k | p+ip | Majorana | Complex fermion | Bosonic |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | 0 |
| 2 | 0 | 0 | 0 | 0 |
| 3 | 0 | 0 | 0 | C2^3 |
| 4 | 0 | 0 | 0 | C2^3 |
| 5 | 0 | 0 | 0 | C2 |

For these groups, H*(G_b,F2) is the polynomial ring on degree-one generators x_i.
The first p+ip obstruction sends each integral degree-two generator to its nonzero square, so no integer decoration survives.
Sq2 is injective on degree-three cohomology: monomials with exponent patterns (3), (2,1), and (1,1,1) have independent nonzero images.
Thus the Majorana layer is zero already at its primary obstruction.
The degree-four kernel of the complex-fermion phase obstruction is exactly the incoming Sq2 image from degree two.
This leaves no complex-fermion layer.
The integral tensor-resolution matrices verify this on supports of size at most four; higher supports cannot occur in degree four.

The raw bosonic H5(G_b,U1) has support multiplicities 1,2,4,3,1 for k=1,2,3,4,5.
The incoming complex-fermion obstruction has ranks 1,2,1,0,0 on these supports.
The degree-two Majorana primary map is injective, so it produces no additional incoming secondary identification.
This gives the final bosonic multiplicities 0,0,3,3,1 directly.
No claim about the final stacking group is needed for this calculation.

## The nonsplit elementary family

For G_f=C4f x C2^r, keep the distinguished C2 quotient factor and split only in the r spectator factors.
The contribution of a fixed spectator support is

| Spectator count | p+ip | Majorana | Complex fermion | Bosonic | Stacking group |
|---|---|---|---|---|---|
| 0 | C2 | C2 | C2 | C2 | C16 |
| 1 | 0 | C2 | C2 | C2 | C8 |
| 2 | 0 | 0 | C2 | C2^3 | C4 x C2^2 |
| 3 | 0 | 0 | 0 | C2^6 | C2^6 |
| 4 | 0 | 0 | 0 | C2^4 | C2^4 |
| 5 | 0 | 0 | 0 | C2 | C2 |

Summing over spectator subsets gives the final layer ranks

    p+ip:             1,
    Majorana:         1+r,
    complex fermion:  1+r+binom(r,2),
    bosonic:          1+r+3 binom(r,2)+6 binom(r,3)+4 binom(r,4)+binom(r,5).

All factors in these four quotients are C2.
The stacking group is

    C16 x C8^r x C4^binom(r,2)
        x C2^(2 binom(r,2)+6 binom(r,3)+4 binom(r,4)+binom(r,5)).

The powers have a direct decoration interpretation.
The p+ip root on the distinguished factor has a Majorana decoration after two copies, a complex-fermion decoration after four copies, and a nontrivial bosonic phase after eight copies.
It has order sixteen.
Each one-spectator Majorana root has a complex-fermion decoration after two copies and a nontrivial bosonic phase after four copies, giving order eight.
Each two-spectator complex-fermion root squares to one of the three independent bosonic roots, giving C4 and leaving two independent order-two bosonic roots.
The other spectator supports are purely bosonic.
These statements concern final layer classes; a change of lifts may add a lower-decoration contribution without changing the chain.

For the two-spectator block, the exact tensor-resolution calculation gives six raw bosonic generators of order two.
The incoming identifications are e1+e4, e2+e4, and e4+e6.
Thus e3,e4,e5 form a basis of the final bosonic C2^3.
The complex-fermion representative is x1^2 x2^2.
Its doubling carry is e1+e2+e4, which becomes e4 after the incoming identifications.
This explicitly proves the C4 extension; it is not inferred from its total order.
The e_i are temporary coordinates of the verification matrix, not notation needed in the manuscript.

The support-zero and support-one filtrations were independently extracted from the full archived integer relation matrices by taking the saturated kernel of their higher-layer columns.
Their nontrivial doubling chains follow from those same presentations.
For supports two through five, the exact cochain matrices independently give bosonic ranks 3,6,4,1 and complex-fermion ranks 1,0,0,0.
The degree-three Majorana primary kernel is zero on every support with at least two spectators.
The higher-support results therefore need no secondary Majorana assumption.

## General nonsplit 2-primary layers

Let G_f=C_(2m)^f x product C_Ni, with m and all N_i powers of two at least two.
Use g=min N_i on a nonempty spectator support.
The final p+ip and Majorana layers vanish for supports with at least two spectators.
The complete rules are:

| Spectators | Condition | p+ip | Majorana | Complex fermion | Bosonic |
|---|---|---|---|---|---|
| 0 | — | C_m | C2 | C2 | C_m |
| 1 | order N | C_(N/2) | C2 | C2 | C_(N/2) x C_gcd(m,N) x C_gcd(m/2,N) |
| 2 | g=N2<=m | 0 | 0 | C2 | C_(g/2)^3 x C_g^3 |
| 2 | g<N2, g<m | 0 | 0 | C2^2 | C_(g/2)^2 x C_g^4 |
| 2 | g<N2, g=m | 0 | 0 | C2 | C_(g/2)^2 x C_g^4 |
| 2 | m<g=N2 | 0 | 0 | C2 | C_(m/2) x C_m^3 x C_(g/2)^2 |
| 2 | m<g<N2 | 0 | 0 | C2 | C_(m/2) x C_m^3 x C_(g/2) x C_g |
| 3 | g<=m | 0 | 0 | C2 if g is unique; otherwise 0 | C_(g/2) x C_g^6 |
| 3 | g>m | 0 | 0 | C2 if g is unique; otherwise 0 | C_m^3 x C_g^4 |
| 4 | — | 0 | 0 | C2 if g>=2m; otherwise 0 | C_g^3 x C_min(m,g) |
| 5 | — | 0 | 0 | 0 | C_g |

Factors C1 are omitted.
The stable splitting makes the contribution of the whole group the product over spectator subsets in each individual layer.

### Why the low-support layers are final

The integer layer is fixed by its first obstruction: the distinguished generator survives, and each spectator generator survives precisely when doubled.
Naturality from cyclic integer-decoration roots proves their higher obstruction classes vanish.
The incoming integer-decoration source H1(G_b,Z) is zero, so it cannot introduce further identifications in the higher layers.

For one spectator, the degree-two Majorana map Sq2+omega2 is injective.
The bosonic quotient therefore receives only the incoming complex-fermion image, which is calculated directly by the tensor-resolution matrices.
They give the bosonic factors in the table and one complex-fermion class.
The degree-three Majorana primary kernel is one-dimensional, generated by y0 x1.
To verify that its secondary obstruction vanishes, compare these independently determined layers with the complete two-circle Gysin calculation.
The product of the integer, complex-fermion, and bosonic layer orders is

    (N/2) x 2 x (N/2) gcd(m,N) gcd(m/2,N),

which is exactly one half of the independently proved Gysin stacking-group order.
The only remaining primary candidate is that single Majorana class, so it must survive.
This is an order-completeness argument after computing the other three layers and the primary kernel, not an assignment of decoration layers from total invariant factors alone.

On support zero, the cyclic calculation gives the same conclusion.
The raw upper bound from the four layers has order m x 2 x 2 x m=4m^2, and the complete cyclic stacking group has exactly this order.
Thus no outgoing Majorana obstruction or incoming secondary identification can reduce these layers.
This cyclic completeness input is already proved by the independent eta/Gysin calculation.

### Arbitrary-exponent certificates

For one through three spectators, the bosonic quotient and complex-fermion kernel are computed directly from the integral Koszul-normalized cochain matrices.
There are 6,16,40 exhaustive order patterns, respectively.
The supplied certificates perform an exact Smith reduction over Z or Z[t], with g/m=2t in the unequal-order cases.
Their unimodular identities hold for arbitrary t, so this calculation does not extrapolate a finite exponent grid.
The four- and five-spectator layers follow directly from their bottom cochains, as detailed in the higher-support proof.

## Checks and presentation advice

The layer API matches all 25 archived nonsplit final filtrations and all 21 archived nonsplit support filtrations.
For the main elementary formulas it also matches the independently recomputed higher-support matrices and ranks zero through eight.
The archive comparison uses the final filtration after incoming identifications, not raw surviving representatives.

The main text should show the four layer results before stating the stacking group and explain the three kinds of nontrivial doubling chain.
The introduction can use one compact row for each of the two elementary families, with four decoration columns and a stacking-group column.
The general appendix should include the support-layer table above adjacent to the support stacking groups, or combine the two into a single table if the layout remains readable.
The matrix coordinates and symbolic certificates belong in the reproducibility package.
Calling the final object the stacking group consistently avoids confusing it with either the bosonic symmetry group or the product of its associated-graded decoration layers.
