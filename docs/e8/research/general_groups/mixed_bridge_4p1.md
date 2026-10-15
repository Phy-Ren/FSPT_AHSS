# 4+1D: an explicit relative E8–CI source, product, and gauge bridge

This note concerns the closed-sheet four-tuple
`(e_2,n_2,n_4,nu_5)`. It introduces no extra coefficient row and no
additional differential page. The results below are **relative to the
pure-CI comparison map**. They do not construct the still-missing universal
pure-CI terminal rephasing or certify that the retained CI model is the
entire physical kernel.

Let `a,b` denote closed integral degree-two sheets in the parity
presentation before adding E8; in the electronic lower map they are
`a=2n_2`, `b=2n'_2`. Let `e,f` denote the added neutral sheets `e_2,e'_2`.
All four have coefficient sign `s`. The parity sheets after addition are
`a+16e`, `b+16f`. Majorana and localized parity-charge coordinates are held
fixed by this addition. This is the same-symmetry comparison retaining the
charge circle, not an operation that discards charge conservation.

All reference-evaluator statements concern the generic publication path.
For direct runtime comparisons use `Backend(use_specializations=False)`.
A sixteen-sheet shift can leave the optional both-sheets-zero optimizer;
the certificate does not assume that optimizer's separate equivalence.

Write the explicit neutral product, associator, and commutator as

\[
P(e,f)=\frac{(e\cup_1 f)\cup(e-f)-(e-f)\cup(e\cup_1 f)}{3},
\]
\[
A(e,f,g)=\frac{(e\cup_1 f)\cup_1 g}{3},\qquad
C(e,f)=\frac{(e\cup_2 f)\cup(e-f)-(e-f)\cup(e\cup_2 f)}{3}.
\]

Their signed identities, modulo integral cochains, are

\[
\delta_s A(e,f,g)=P(e,f)+P(e+f,g)-P(f,g)-P(e,f+g),
\]
\[
\delta_s C(e,f)=P(e,f)-P(f,e).
\]

## 1. The mixed source rephasing

The fixed parity source has cubic term `a^3/12`. Its complete dyadic part
is unchanged when `a` is shifted by `16e`, with unchanged lower binary
coordinates. This requires the arbitrary-base periodicity check described
below; it does not follow from the special evaluation at `a=0`.

Expand the cubic as ordered products. The three terms with one `e` have
coefficient `16/12`, and the three terms with two `e` have coefficient
`256/12`. Both coefficients equal `1/3` modulo integers. The pure neutral
coefficient is `4096/12=1/3 mod Z`. Thus

\[
O^{\rm SC}(a+16e)-O^{\rm SC}(a)
=e^3/3+\delta_s R^{\rm mix}_5(a,e)\pmod1,
\qquad R^{\rm mix}_5(a,e)=P(a,e).              \tag{1}
\]

No graded commutation of the ordered cochains is needed. Equation (1)
is a concrete source-coordinate transformation. It is stronger than an
argument that neutral and charged phases have independent tensor factors.

## 2. The paired mixed product primitive

The third-primary part of the fixed parity product is `P(a,b)`. Once the
full dyadic product is known to be invariant under the sixteen-sheet
shifts, its change is

`P(a+e,b+f)-P(a,b) mod 1`,

because `16=1 mod 3`. With the source rephasing (1), the residual between
stacking the separate tensor factors and stacking the mapped states is

\[
D_5=P(a,b)+P(e,f)+P(a+b,e+f)
      -P(a,e)-P(b,f)-P(a+e,b+f).               \tag{2}
\]

An explicit primitive is

\[
\boxed{K^{\rm mix}_4(a,b;e,f)=
C(b,e)+A(a,b,e)-A(a,e,b)
-A(a+b,e,f)+A(a+e,b,f).}                       \tag{3}
\]

Then `delta_s K_mix=D_5 mod 1` for every flat sign background. To prove
it, reassociate `((a b)(e f))` into a left-associated product, interchange
the middle factors `b,e`, and reassociate to `((a e)(b f))`. Substituting
the two displayed identities for `delta A` and `delta C` cancels every
intermediate `P` term and leaves exactly (2). This is a universal formal
identity, not a claim inferred from testing finitely many groups.

The lower-coordinate product path inherited from the pure-CI bridge is
still required. The sixteen-sheet shift does not alter its binary lower
endpoints. For the canonical source-prism path that holds the integer
sheet fixed, its terminal gauge is unchanged as well: the dyadic source
is periodic, and the cubic difference is a horizontal pullback with zero
interval integral. Thus (3) needs no additional mixed correction from
that path. The path itself must not be silently omitted from the pure-CI
comparison equation. A separately chosen native gauge still requires its
coordinate transport.

## 3. Gauge transport is paired with the same rephasing

For degree-one integral gauge parameters `u,v`, use the closed cylinders

`a^I=a+delta_s(theta u)`, `e^I=e+delta_s(theta v)`.

Define the degree-four operation

\[
H^{\rm mix}_4(a,e;u,v)=\int_I P(a^I,e^I).      \tag{4}
\]

This is the fixed signed prism sum already implemented by the neutral
`pair_gauge` operation. Stokes's identity and (1) give the paired source-
cylinder gauge comparison. For the cubic representatives themselves,

\[
\delta_s H^{\rm mix}_4
=G(a;u)+G(e;v)+P(a+\delta u,e+\delta v)-P(a,e)
-G(a+e;u+v).                                  \tag{5}
\]

Applying the same prism to the full parity source identity gives its
relative mixed gauge transport, including the changes in `R_mix` at both
endpoints. This statement uses the specified source-cylinder gauge;
another native gauge requires its own known coordinate transport.

## 4. Exact certificates and their scope

[check_middle_four_4p1.py](check_middle_four_4p1.py) expands (3) into formal
`P(x,y)` symbols and proves the cancellation exactly. It also evaluates
the signed local formulas for every one of the 64 vertex-sign assignments
on a five-simplex, with negative integer inputs: all 64 product checks
and all 64 gauge-prism checks passed. Output:
[check_middle_four_4p1.json](check_middle_four_4p1.json).

[probe_mixed_sixteen_periodicity.py](probe_mixed_sixteen_periodicity.py)
independently reads the immutable parity arithmetic DAGs. It tracks
valuations of both a base expression and the difference after a sheet
shift. Addition takes the minimum difference bound. Multiplication uses
`delta(xy)=x delta y+y delta x+delta x delta y`, with the exact extra
factor of two for a square. Division lowers the bound by the denominator's
two-adic valuation on the legal integral domain. Floors by powers of two,
bits, and modular reductions use their exact congruence rules. Unknown
opcodes fail; an inconclusive bound remains unknown.

Four scenarios were certified: arbitrary first-sheet shift, arbitrary
shifts of both sheets, and adding a sixteen-sheet neutral factor on the
right or left of an arbitrary state. In every scenario:

- All four lower source/product packets are unchanged.
- `y6`, `h6`, all 36 `rho4` outputs, and `tensor4` are unchanged.
- The dyadic `high6` output is unchanged.
- The `/48` numerator in `nonbinary4` changes by a multiple of sixteen;
  only its third-primary part can remain.

The source hashes, node counts, and counts of exact divisions whose
integrality is supplied by the legal lower-tower domain are recorded in
[probe_mixed_sixteen_periodicity.json](probe_mixed_sixteen_periodicity.json).
There are 264,431 interpreted nodes in each scenario. The certificate
does not round an unproved exact division into a stronger assertion.

The normalized-chain argument for the full `binary4` recurrence has also
been verified, independently of the packet-periodicity certificate. Its
exact-degeneracy guard can change after a sixteen-sheet shift; identical
control flow is not assumed. The exact symbolic certificate
[probe_parity_normalization.py](../physical/probe_parity_normalization.py)
substitutes every adjacent degeneracy into the immutable raw packets.
`y6`, `h6`, both `high6` top outputs, the raw `rho4` residual, and `tensor4`
vanish identically. Zero-factor substitutions vanish as well, with `rho4`'s
lower output equal to the other factor. Unresolved division, floor, bit,
and modular expressions are retained as formal atoms; no sampling or
unproved numerical simplification is used.

The same certificate composes all 291 degree-five Eilenberg–Zilber cuts
with each of the five input degeneracies, cancels equal projections over
`F2`, and discards only repeated-vertex or zero-fiber projections. The
remaining chain is empty in every case. Thus the transfer homotopy
preserves the degenerate ideal. The background perturbation preserves it
as well: for the first degeneracy the first background edge is zero;
the other degeneracies remain degenerate. Consequently the full normalized
recurrence descends to the chart with sheets reduced modulo sixteen,
even when the two exact input paths encounter different guards.

Combining these certificates proves the full dyadic periodicity used in
(1)–(3), on the legal parity lower-tower domain. The source, relative
mixed twister, and specified gauge bridge are therefore established for
the immutable evaluator. This conclusion is stronger than the pure
sixteen-sheet zero test, and remains distinct from the missing pure-CI
universal comparison.

## 5. What tensoring proves physically

Bosonic inclusion alone fixes the pure neutral restriction. It does not,
by itself, prove that the displayed CI cochain model is the entire
physical zero-E8 kernel or that its phase coordinates agree with another
Postnikov presentation. Pure restrictions can miss mixed operations.

There is a precise sufficient framework for tensor coordinates. Let the
physical positive-filtration theory have the leading neutral-sheet map,
let its fiber be the actual physical zero-E8 theory, and let the completed
neutral theory map into it over that leading coordinate. The neutral
theory and the fiber combine by tensor product, identifying the common
phase map and any kernel of that map. This yields the shared-phase
pushout, rather than a direct product. In the space-group domain, the
neutral completion proof supplies surjectivity onto neutral sheets. The
remaining physical identification of the retained CI presentation with
the fiber is a separate hypothesis.

Equations (1), (3), and (4) provide the concrete mixed source, twister, and
gauge conversion relative to a pure-CI comparison. Completing that pure-CI
comparison still requires its own natural universal terminal `R_5` and
paired `K_4`, including the circle-dependent carry terms and lower product
path. Neither an abstract rank argument nor a primitive on each
contractible simplex supplies those maps.
