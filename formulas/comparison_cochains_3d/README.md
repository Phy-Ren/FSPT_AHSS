# Comparison three-cochains

These two finite polynomials compare representative conventions; they do not
replace the canonical physical obstruction or stacking formulas.
They are archived here so that the manuscript can state the comparison
identities without printing their coefficient lists.

The [JSON data](coefficients.json) contains the 104 monomials of the lift
comparison and the 84 monomials of the suspension comparison. The
[original LaTeX lists](manuscript_coefficients.tex) are retained unchanged.
The JSON records their provenance and SHA-256 digest. The suspension list
agrees exactly with `G3_MASKS` in
[`suspension.py`](../publication_source/reference/d4_input/code/suspension.py).

## Evaluation

On the ordered tetrahedron (0123), construct the fifteen bits in `input_order`.
In the 3+1D notation used here, n1 is the integer p+ip decoration and n2 is the
binary Majorana decoration. Integer division is mathematical floor division,
also for negative n1. For a listed subset J, multiply the bits with indices in J.
Add the products modulo two. The JSON indices start at zero; each listed
monomial has coefficient one and all unlisted monomials have coefficient zero.

The resulting polynomials are respectively B3^L + Bcal3 and B3^S + Bcal3.
To obtain B3^L or B3^S, add the common cochain
Bcal3 = check(n2) cup_1 check(n2), where
check(n2) = n2 + s1 cup (floor(n1/2) mod 2).
All operations in this paragraph are modulo two. The check modifies n2 before
taking the higher cup product; it is not a relabeling of the input bits.
To take a coboundary, evaluate the same cochain on every ordered boundary face.

The admissible lower fields satisfy d s1 = d omega2 = 0, d_s1 n1 = 0,
and d n2 = omega2 cup n1 + s1 cup n1 cup n1 modulo two.
The identities are O4^L - O4 = d B3^L and
tau O5 - O4 = d B3^S, with the lift and suspension conventions defined in
the manuscript's integer-source comparison appendix and the retained source.
The data archive preserves the existing comparison polynomials. It makes no
new claim about a physical construction of the terminal p+ip phase.
