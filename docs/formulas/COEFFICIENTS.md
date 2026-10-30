# Exact finite coefficients

The [4+1D formula](FOUR_DIMENSIONAL.md) uses two binary polynomial kernels.
Their complete coefficient arrays are runtime data, not fitted primitives.
The notation `P5^Cartan` distinguishes the first from the neutral E8
twister `P5^E8`.

| Kernel | Variables on `[012345]` | Terms | Exact array |
| --- | --- | --- | --- |
| `P5^Cartan(z3;x2,y2)` | `z(0ijk)`, then `x(0ij)`, then `y(0ij)`, each lexicographic | 814 | [cartan32_polarizer.json](../../insulator/_engine/cartan32_polarizer.json) |
| `R5(r,s;n2,n2')` | `r(0i)`, `s(0i)`, `bar n(0ij)`, `bar n'(0ij)`, `tilde n(0ij)`, `tilde n'(0ij)`, each lexicographic | 3,117 | [r_polarizer.json](../../insulator/_engine/r_polarizer.json) |

For `P5^Cartan`, each stored triple `(iz,ix,iy)` means
`product(z[j] for j in iz) * x[ix] * y[iy]`; sum modulo two.
For `R5`, a hexadecimal mask `q=sum q_i 2^i` denotes the squarefree
monomial `product(v_i for q_i=1)`. Every listed coefficient is one;
unlisted coefficients are zero. No extra quarter-valued correction is
enabled in the operative array.

Evaluate on any ordered five-simplex by induced vertex relabeling.
The `R5` variables retain the two actual integer-sheet digits, including
negative carries. Both kernels vanish with either sheet input zero and
on normalized degeneracies. `R5` vanishes for `r=0`.

The independent polynomial identities and degeneracy certificates are in
[universal_certificates.json](../../formulas/universal_certificates.json).
The [printed coefficient source](../../formulas/C_coefficients.tex)
contains the same masks, and [provenance.json](../../formulas/provenance.json)
pins the supplied archive. The executable definitions are `P32` and
`R5_table` in [product4d.py](../../insulator/_engine/product4d.py).
