# Computed calibration certificates

These files retain exact computed cochains, detector cycles, pairings, and
geometric periods. Original result hashes are included in each file. Their
scope complements the finite-group classifications in the parent directory.

| Certificate | Input and computed result |
| --- | --- |
| [Q8 d3 detectors](q8_d3_detectors.json) | For each nonzero character chi, 3+1D `(s=chi, omega=0, n1=chi)` and 4+1D `(s=0, omega=0, n2=beta chi)` have nonzero final d3. All eighteen legal Majorana lifts retain the detected class. |
| [V4 Euler input](v4_euler.json) | With `s=x`, `omega=x²+xy+y²`, and `n2=-beta_s(y)`, all four legal Majorana choices give zero normalized O6 pairings. The Theta6 detector pairs as `(0,1/2,1/2,0)`. |
| [D8 d4 detectors](d8_reflection_square_d4.json) | For the order-eight dihedral group, reflection `x`, rotation parity `y`, `s=0`, `omega=x²`, and `n2=beta(y)`, the final obstruction is `v2³/2`. The six cycle pairings are `(1/2,1/2,0,1/2,1/2,0)`; no legal lower adjustment cancels them. |
| [C2 exact-phase control](c2_exact_phase.json) | The antiunitary 3+1D control has O5 equal to zero. In the unitary 4+1D control, O6 has value `7/16` on the unique nondegenerate six-tuple but equals `d(7 x⁵/32)`, so its class is zero. |
| [Spin-c period](spinc_t2_cp2.json) | On `T² × CP²`, all ninety signed six-simplices give total phase `1/8`. The Pi6 period is `1/2`, so adding it changes the result to `5/8`; the Theta6 period is zero. |

The Spin-c input is `n2=2A`, `omega=rho2(B)`, `s=0`, `n3=0`, with the CF
cochain specified in the certificate. The stored gauge and gravitational
integrals are each `1/8`; the index subtracts the gravitational term, so their
signed contributions are `+1/8 - 1/8 = 0`. The ordinary cochain
period is a normalization test against that index, not a claim of an
obstruction to a continuous-symmetry field theory.

The group-bar certificates preserve their **zero-based** convention: identity
is 0 and multiplication entries are element labels. This differs from the
one-based finite-runner catalog. Flat cochain arrays are ordered lexicographically
over nonidentity increments. A Q8 `detector_cycle_indices` entry is a zero-based
index into the corresponding O4 or O5 array; its coefficients are modulo two.
Other cycles list `[word, integer coefficient]` pairs. Values ending in `mod16`,
including `phase_values`, are numerators over sixteen. The geometric file
retains all ninety signed simplex contributions and their term decomposition.

Only the final obstruction modulo all legal lower adjustments determines
whether a p+ip input survives. A nonzero phase cochain can be exact, as in the
C2 control. Q8 d4 is undefined for the listed inputs because their final d3
already obstructs a lift.

The general `scripts/run_finite_example.py` command reproduces finite-group
classifications and 3+1D stacking from the public catalog. These calibration
files are retained computed evidence; the command does not replay the
geometric Spin-c triangulation or reconstruct every recorded bar detector.
The public Q8 4+1D full-group square certificate has its own `--q8-square`
replay option, documented in the parent README.
