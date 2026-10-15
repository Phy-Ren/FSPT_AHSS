# 4+1D: free E8 decorations and exact completions

These are algebraic diagnostics, not complete electronic classification
tables. The fields are `(e_2,n_2,n_4,nu_5)`; the relevant neutral
decoration is a closed integral two-cochain.

Two rank-four presentation checks verify the cohomological dimension
argument and its integer implementation:

| Group and sign | Signed real H2 rank | Signed real H5 and H6 |
|---|---|---|
| Z^4, trivial sign | 6 | Both zero |
| Klein-bottle group x Z^2, chirality sign | 3 | Both zero |

The same script checks their H1 presentation lattices as implementation
diagnostics (`Z^4` and `Z x Z2`, respectively). Those auxiliary H1
calculations are not the 4+1D classification: the E8 sheet here is `e_2`.

For an explicit free completion on `Z^4`, let `x,y` be integer
one-cocycles and `e_2=x cup y`. Write
`k_1(g)=x(g)y(g)` and `q_1(g)=x(g)(x(g)-1)/2`. Then

\[
\delta k_1=-(x\cup y+y\cup x),\qquad
\delta q_1=-x\cup x,
\]
\[
h_3=x\cup k_1\cup y+q_1\cup y\cup y,
\qquad\delta h_3=e_2^2,
\qquad\nu_5=h_3\cup e_2/3.
\]

This solves `delta nu_5=e_2^3/3` exactly, although `[e_2]` is a nonzero
free real cohomology class. An averaging construction requesting
`e_2=delta a_1` would fail on this example.

The script also combines `e_2=x1 cup x2+x3 cup x4` using the supplied
neutral twister and checks the resulting source modulo integers. It uses
negative integer inputs. All 3,000 square-primitive checks, 3,000 exact
single-free-sheet completions, and 3,000 two-free-sheet stacking
completions passed. The reproducible script is
[check_examples.py](check_examples.py), with output in
[examples.json](examples.json).

The general rational-resolution construction is proved in
[general_groups.md](general_groups.md). Existence of these completions
does not split the stacking extension or remove the intrinsic 4+1D row.
