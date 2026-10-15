# 3+1D: signed H1 presentation examples

These are neutral-decoration and integer-lattice diagnostics, not complete
electronic classification tables. The fields are `(e_1,n_1,n_3,nu_4)`.
The sign in the following examples is the chirality character.

| Group and sign | H1(G,Z_s) | Integer feature |
|---|---|---|
| Three translations, trivial sign | Z^3 | Three weak E8 integers |
| Mirror `Pm`, chirality-reversing mirror | Z x Z2 | Normal weak layer and reversing root |
| Glide `Pc`, `g^2=t_y`, sign(g)=-1 | Z x Z2 | The glide relation is retained integrally |
| Inversion `Pbar1`, sign(i)=-1 | Z^3 x Z2 | Three weak integers remain |
| Screw `P2_1`, `g^2=t_z`, trivial sign | Z | Primitive e_1(g)=1 has e_1(t_z)=2 |
| Z^3 x C2^T, central time reversal | Z2 | No translation integer survives |
| Z^3 with an antiunitary primitive translation | Z2 | Unit translations form an index-two sublattice |

All seven cases are specified by generators, sign assignments, and
relators in [check_examples.py](check_examples.py). The exact saturated
cocycle kernels and principal-coboundary coordinates are preserved in
[examples.json](examples.json). All passed. Real ranks alone would miss
the screw's primitive translation multiplicity.

The general cohomology proof and the separate hypotheses needed for a
physical neutral section are in [general_groups.md](general_groups.md).
The table does not identify the inherited CI sector with the full physical
kernel, and makes no spin-dependent classification claim.
