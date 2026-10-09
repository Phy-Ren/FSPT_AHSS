# Fermionic coboundary and stacking

Fermionic coboundary and stacking constrain the formulas in adjacent
dimensions. In coordinates where the two constructions commute as
cochains, their phase identity is

{{equation:coboundary-stacking-compatibility--fermionic-coboundary-and-stacking--1}}

The stacking twister on the right belongs to the **bulk in one higher
spacetime dimension**. Its arguments are the actual bulk decoration
cochains obtained by fermionic coboundary. They are not the boundary
fields with different degree labels.

This appendix derives the phase identity under the stated compatibility
hypothesis and proves an exact simplification of the [4+1D stacking law](FOUR_DIMENSIONAL.md#4-bosonic-stacking)
when the two bulk inputs have the same closed Majorana decoration.
It keeps all cochain representatives, inverse carries, and coefficient
systems explicit.

## The compatibility identity

Let the boundary spacetime dimension be $`D`$. Write its decoration
data as $`X`$ and its additive phase as
$`\widehat\nu_D\in C^D((\mathbb R/\mathbb Z)_{s_1})`$.
The boundary product is

{{equation:coboundary-stacking-compatibility--the-compatibility-identity--2}}

Here $`X*Y`$ includes every lower stacking twister. Define
$`\Delta f(X,Y)=f(X*Y)-f(X)-f(Y)`$.
In the fermionic-coboundary convention used here, the top bulk phase is

{{equation:coboundary-stacking-compatibility--the-compatibility-identity--3}}

Suppose the chosen cochain representatives satisfy
$`\delta((X,\widehat\nu_D)*(Y,\widehat\nu_D')) =\delta(X,\widehat\nu_D)*\delta(Y,\widehat\nu_D')`$.
Comparison of their top components gives the displayed identity:
the left construction has phase
$`\widehat{\mathcal{𝒪}}_{D+1}(X*Y)-d_{s_1}\widehat\nu_D -d_{s_1}\widehat\nu_D'-d_{s_1}\widehat{\mathcal{ℰ}}_D`$;
the right construction has phase
$`\widehat{\mathcal{𝒪}}_{D+1}(X)+\widehat{\mathcal{𝒪}}_{D+1}(Y) -d_{s_1}\widehat\nu_D-d_{s_1}\widehat\nu_D' +\widehat{\mathcal{ℰ}}_{D+1}`$.

All terms have degree $`D+1`$ and coefficients
$`(\mathbb R/\mathbb Z)_{s_1}`$.
For inputs satisfying the lower boundary equations,
$`\delta_{\mathrm{lower}}X=\delta_{\mathrm{lower}}Y=0`$.
Normalization of the bulk product then reduces the identity to

{{equation:coboundary-stacking-compatibility--the-compatibility-identity--4}}

For more general boundary data the bulk term must be retained.
If the two constructions are identified by a lower gauge transformation,
apply that transformation before comparing phases. If their remaining
phase difference is $`d_{s_1}H_D`$, that specified term is also retained.
This distinguishes strict cochain compatibility from compatibility of
cohomology classes.

## An exact 4+1D product with a group inverse

Work entirely in the 4+1D context in this section. Let

{{equation:coboundary-stacking-compatibility--an-exact-4-1d-product-with-a-group-inverse--5}}

where the entries are the p+ip, Majorana, complex-fermion, and phase
cochains. The lower fields satisfy

{{equation:coboundary-stacking-compatibility--an-exact-4-1d-product-with-a-group-inverse--6}}

Thus $`u`$ has degree three, $`c,c'`$ have degree four, and
$`c+c'`$ is closed. All these lower fields are binary. The backgrounds
$`\omega_2,s_1`$ are closed and remain fixed.

The complete current product has the exact specialization

{{equation:coboundary-stacking-compatibility--an-exact-4-1d-product-with-a-group-inverse--7}}

After distributing $`c+c'`$, the correction contains **four specified
cup terms**. The already defined lower obstruction remains a structured
argument. The terminal Majorana coefficient sum has canceled. This
identity describes relative stacking at fixed Majorana decoration; the
self-stacking law remains specified separately.

### The inverse includes a lower stacking carry

The Majorana self-stacking correction is the known lower twister

{{equation:coboundary-stacking-compatibility--the-inverse-includes-a-lower-stacking-carry--8}}

Call this twister $`T`$ only in the following derivation, and put
$`k=\mathcal{𝒪}_5^\gamma(u)`$. The inverse of $`Y`$ has lower fields
$`(0,u,c'+T)`$. Its phase is

{{equation:coboundary-stacking-compatibility--the-inverse-includes-a-lower-stacking-carry--9}}

This expression has six half-valued cup terms after distributing the
two occurrences of $`c'+T`$. The Majorana diagonal is the same
fully specified operation as in the original stacking law.
This chooses the inverse representative for which $`Y*Y^{-1}`$ is the
zero cochain state. It includes the lower carry as well as the phase
correction.

For $`X*Y^{-1}`$, the direct product adds

{{equation:coboundary-stacking-compatibility--the-inverse-includes-a-lower-stacking-carry--10}}

The half-valued bracket contains ten cup terms after distributing its
displayed sums. Subtracting the inverse correction cancels the two
identical Majorana diagonals as whole phase cochains. Bilinearity
over $`\mathbb Z_2`$ cancels every $`T`$ term and leaves

{{equation:coboundary-stacking-compatibility--the-inverse-includes-a-lower-stacking-carry--11}}

This proves the boxed specialization. It uses the original c,
c-gamma, and gamma contributions in their stated operator ordering.
No contribution is reassigned by its dependence on decoration fields.

The cancellation is independent of the chosen representative of
$`\widehat{\mathcal{ℰ}}_5^\gamma(u,u)`$, provided that the same
representative is used in the inverse and the product. In particular,
its quarter-valued terms cancel before any lift is expanded.

## Applying the specialization to a 3+1D lower tower

Return now to the 3+1D degree convention. Its lower equations give

{{equation:coboundary-stacking-compatibility--applying-the-specialization-to-a-3-1d-lower-tower--12}}

The two Majorana bulk fields relevant to the pure-layer
fermionic-coboundary construction are the same closed three-cochain
$`d\check n_2=\check\omega_2\bar n_1`$. Their bulk p+ip coordinates vanish.
Once the pure-layer bulk maps are expressed in the same cochain
coordinates, the preceding exact identity applies with

{{equation:coboundary-stacking-compatibility--applying-the-specialization-to-a-3-1d-lower-tower--13}}

Its entire additional phase is consequently

{{equation:coboundary-stacking-compatibility--applying-the-specialization-to-a-3-1d-lower-tower--14}}

Here $`\mathcal{𝒪}_4^\psi`$ is the **3+1D** lower obstruction,
whereas $`\mathcal{𝒪}_5^\gamma`$ is the **4+1D** closed-Majorana
obstruction defined above. The expression contains two cup terms
of degree five. It is the bulk product correction for the stated
fields; the complete boundary obstruction also includes the phases
of the specified pure-layer bulk maps.

The complete phases of the pure-layer bulk maps are evaluated on their
stated domains before this additional product correction is applied.
Here `check n3 = n3 + check n2 cup1 check n2` is the explicit
[geometric-reference conversion](THREE_DIMENSIONAL_GEOMETRIC_REFERENCE.md).
Thus the bulk sum is `d check n3`, not the current point occupation `dn3`.
The boundary product also receives the face-reference phase on that page.

## Transporting representatives together

A terminal coordinate change
$`\widehat\nu_D^{\,\mathrm{new}}=\widehat\nu_D+f_D(X)`$
has the paired transport

{{equation:coboundary-stacking-compatibility--transporting-representatives-together--15}}

Both use the same complete lower product. A redefinition of a lower
decoration first requires substitution throughout the remaining
tower. An exact change in an obstruction therefore comes with its
corresponding change in the twister.

The signs can also be fixed geometrically. Let $`\tau_P`$ denote
parameter-first signed shuffle integration over an oriented
parameter simplex $`P`$, with $`s_1`$ pulled back from the physical
space. Then

{{equation:coboundary-stacking-compatibility--transporting-representatives-together--16}}

This is the cochain form of the boundary identity for the shuffle
cross product. For a closed high-dimensional cochain on a triangle,

{{equation:coboundary-stacking-compatibility--transporting-representatives-together--17}}

The triangle formula explains the common sign in
$`d_{s_1}\widehat{\mathcal{ℰ}}=\Delta\widehat{\mathcal{𝒪}}`$.
It also fixes the source and product signs when an explicit
parameter-dependent representative is changed.
