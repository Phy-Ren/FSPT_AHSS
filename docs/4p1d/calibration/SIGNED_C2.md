# Signed C2: complete 4+1D four-data calculations

The exact global solver computes the following intrinsic-zero groups, including
the neutral E8 decoration and the common phase. All four agree with the
independently derived interacting [bordism targets](BORDISM_TARGETS.md).
These are internal symmetries; a crystalline spinless/spin-half label does not
apply.

Write `alpha(c)=1` and `omega=k alpha²/2`. The ordered data are
`(e2,n2,n4,nu5)`.

| Symmetry | (s,rho,k) | E8 e2 | CI n2 | Charge n4 | Phase nu5 | Computed stacking | Independent target | Comparison |
|---|---|---|---|---|---|---|---|---|
| Unitary C²=1, H+ | (0,alpha,0) | Z2 | 0 | 0 | 0 | Z2 | Z2 | **✓** |
| Unitary C²=(-1)^F, H− | (0,alpha,1) | Z2 | Z2 | 0 | Z2 | Z2³ | Z2³ | **✓** |
| Antiunitary T²=1, AI; intrinsic zero | (alpha,0,0) | 0 | 0 | 0 | 0 | 0 | 0 | **✓** |
| Antiunitary T²=(-1)^F, AII; intrinsic zero | (alpha,0,1) | 0 | 0 | 0 | 0 | 0 | 0 | **✓** |

The decoration columns are the **final filtration quotients**, after incoming
identifications. Stacking is computed from complete roots and relations, not
inferred by multiplying these columns.

## Global differential and all incoming gauges

The normalized C2 bar complex has exactly one nondegenerate generator in every
degree. Every normalized cochain is a scalar on `(c,...,c)`, with

$$
d_\chi(\alpha^p)_\chi
=\bigl[(-1)^{\chi(c)}+(-1)^{p+1}\bigr](\alpha^{p+1})_\chi.
$$

The solver pulls these entire cochains onto a six-simplex and evaluates the
adopted source, product and joint gauge. It verifies all output faces against
the global normalized cochain, including degenerate faces.

For H±, both integer sheets have trivial coefficients, while charge has the
nontrivial sign. The full integer obstruction is

$$
\mathcal O_5(n\alpha^2)=-n(n-k)\alpha^5,
\qquad n_4=\frac{n(n-k)}2\alpha^4.
$$

Thus an odd CI sheet is obstructed for H+, but allowed for H−. Charge completion
is unique. The equation `d nu5=O6` has two solutions modulo exact phase gauges;
both are retained. Sheet gauges reduce e and n modulo two. Between canonical
representatives the remaining gauge is the closed charge parameter
`u3=m alpha³`, whose phase shift is

$$
\Delta\nu_5=\frac{(k+1)m}{2}\alpha^5\pmod1.
$$

It kills the bosonic half-phase for H+ and vanishes for H−. There is no incoming
sheet class in `H¹(C2;Z)`.

For AI/AII, closed signed integer sheets vanish exactly: `e2=n2=0`. Charge has
trivial coefficients and its terminal source is `k q alpha⁶/2`. Since the
signed phase differential in degree five is zero, AII obstructs odd q; AI
allows it. A closed CI gauge `u1=u alpha` and a charge gauge `u3=w alpha³` give

$$
\Delta q=(k-1)u+2w.
$$

For AI this removes every integer charge; for AII it removes every allowed
even charge. All remaining phases are exact because the degree-four signed
U(1) differential is multiplication by −2, which is surjective. The closed
E8 parameter introduces no additional class. These scalar formulas exhaust
arbitrary integer parameters, not just a bounded set of tested gauges.

## Complete stacking witnesses

The neutral root for H± is
`E=(alpha²,0,0,alpha⁵/6)`. Its source is `alpha⁶/3`. Its raw square has phase
`alpha⁵/3`; the actual E8 gauge `v1=-alpha` removes the doubled sheet and
adds `2 alpha⁵/3`, proving `2E=0`.

For H− the CI root and bosonic root are

$$
X=(0,\alpha^2,0,7\alpha^5/48),
\qquad b=(0,0,0,\alpha^5/2).
$$

The exact CI source is `7 alpha⁶/24`. The raw square of X has
`n2=2 alpha²`, `n4=alpha⁴`, and phase `19 alpha⁵/24`. The full CI gauge
`u1=-alpha` removes both integer decorations and adds `5 alpha⁵/24`.
Consequently `2X=0`; the shared boson is retained and has `2b=0`.

The presentations are therefore:

* H+, roots `(E,b)`: `2E=0, 2b=0, b=0`.
* H−, roots `(E,X,b)`: `2E=2X=2b=0`.
* AI at intrinsic zero, charge root Q: `2Q=0, Q=0`.
* AII at intrinsic zero: no surviving root.

The solver enumerates respectively 4, 8, 2 and 1 completed canonical states
before incoming identifications. It computes every ordered product and every
incoming action, checks that the product descends to the quotient, checks
associativity, commutativity and inverses, and verifies the presentation order
against that exhaustive quotient. Outputs retain phase completions, raw
products, integer and phase gauge parameters, root relations, complete product
tables, and exact source hashes.

## Physical scope and reproducibility

For H± the intrinsic pair `(n0I,n0J)` is forced to zero. Their full interacting
targets follow from the specified Smith twists and Freed–Hopkins Theorem 9.87;
the [reference derivation](BORDISM_TARGETS.md#the-two-unitary-charge-conjugation-targets)
states the tangential conventions and primary citations.

AI/AII here are **restricted to intrinsic zero**. Their full interacting groups
are Z²: AI has embedded uniform image `2Z{I}⊕2Z{J}`, AII has `Z{I}⊕Z{J}`.
Those are separate physical inputs, not outputs of this four-data solver.
Freed–Hopkins Corollaries 9.95 and 9.93 supply the full groups, as recorded in
the reference ledger. Agreement of abstract groups is recorded as a comparison;
the solver does not assert a universal physical-spectrum identification or a
complete character dictionary for its signed roots.

Run [the isolated driver](../../../scripts/signed_charge_conjugation_4p1.py):

```bash
python3 scripts/signed_charge_conjugation_4p1.py --output NEW_DIRECTORY
python3 -m unittest discover -s tests -p test_signed_charge_conjugation_4p1.py -v
```

The [implementation](../../../insulator/signed_charge_conjugation_4p1.py) imports
no expected classification. Five substantive tests cover the rational CI square,
obstruction and incoming mechanisms, complete presentations, noncanonical
integer sheets, and signed gauge periods. An independent review also checked
all 64 six-words, including degeneracies, with a mixed integer/rational gauge
in each background. This is a complete calculation of these four fixed
four-data models; it is not a general signed-group or intrinsic classifier.
