# Point-group discrepancy evidence

These audits explain specific disagreements with
[arXiv:2204.13558v2](https://arxiv.org/abs/2204.13558v2). They do not change
the primary-source tables or supply expected groups to the AHSS backend.
The full physical source includes neutral E8; comparison to the present sector
uses the separately identified neutral generator only when the source supplies
one. The original comparison failures remain visible.

## D2 with physical spin-half fermions

Table II gives Z2^3, all in its real-space 0D layer. The root list at
`main.tex:4758-4763` identifies an odd-charge center state and the two D2
rotation characters. The same claim appears in the published
[PRX supplementary material](https://journals.aps.org/prx/supplemental/10.1103/PhysRevX.15.031029/3DpointCombine__supp.pdf),
page 6, subsection D. Thus the extra printed factor has an explicit charged
0D interpretation; it cannot be explained simply by an omitted neutral E8
decoration.

There is a direct obstruction to that named root under the paper's own
physical spin convention. Section II A (`main.tex:149-158`) defines spin-half
through the SU(2) double group. Orthogonal pi-rotation lifts obey

```
Rx Ry = (-1)^F Ry Rx.
```

On a one-dimensional center state their scalar eigenvalues commute, so
`(-1)^q=1`. Odd center charge is forbidden. Redefining either generator by a
U(1) phase leaves this commutator unchanged. The paper itself requires
one-dimensional center representations and excludes higher-dimensional
degenerate irreducible representations (`main.tex:580`). This is a physical
representation argument independent of the cochain implementation.

The independent atomic-orbit computation in `audit_center_orbits.py` further
finds that a two-site odd-electron orbit can remove charge 2 with trivial
center characters. The resulting center quotient is Z2^2. The saved evidence
is `point3_D2_spin_half_center_orbit_audit.json`, including actual site
characters and induced center characters. This agrees with the computed
cochain result. We have not located an author-confirmed correction, so the
printed Z2^3 remains a source discrepancy rather than a silently fixed datum.

## D2d center-state atomic orbits

The source root lists are at `main.tex:5778-5807`:

| Physical spin | Source 0D roots | Other named non-E8 roots |
| --- | --- | --- |
| Spinless | Center charge modulo 4, Z4 | A bosonic 2D SPT pattern, Z2; an axial Haldane-chain pattern, Z2 |
| Spin-half | Charge 2 modulo 4, Z2; two center characters, Z2^2 | CI and paired fSPT patterns extending to Z8; another bosonic 2D SPT pattern, Z2 |

For spin-half, the source explicitly imposes even center charge at line 5796.
The forbidden odd-charge error of its D2 paragraph therefore does not directly
explain D2d. Its neutral E8 root is separately named at lines 5780 and 5803;
the reference-side removal of that root is faithful to the printed list.

We independently induced every one-dimensional physical site representation
over every possible nonzero point-stabilizer stratum. The strata are obtained
from the exact arrangement of intersections of `Fix(g)`, using the catalog's
actual 3D matrices. The physical double group comes from the spin lifts; odd
fermion charge selects its parity-odd characters. For a filled fermionic orbit
the center character is a determinant, including permutation signs. For a
bosonic orbit it is a product. Every resulting full-group projective character
identity is checked. Smith reduction is done only after those orbit relations
are assembled.

Already before any CI bubble, this gives:

| Physical spin | Center quotient by mobile atomic orbits | Source center layer |
| --- | --- | --- |
| Spinless | Z2 | Z4 |
| Spin-half | Z2^2 | Z2^3 |

The saved files are `point3_D2d_spinless_center_orbit_audit.json` and
`point3_D2d_spin_half_center_orbit_audit.json`. A concrete relation common to
both cases comes from a charge-zero two-site orbit at `(0,0,1)`. In catalog
indexing its stabilizer is `[0,3,4,6]`; a site character with values
`[1,-1,1,-1]` induces center values `[1,1,-1,1,-1,1,-1,-1]` and removes one
center character. The exact double-group character and orbit permutations are
retained in the JSON witness. This is an ordinary neutral atomic orbit, not an
E8 quotient or a deletion of an arbitrary finite factor.

For spinless D2d, combining the reduced center group with the two other named
non-E8 Z2 roots has the same abstract group as the current solver's Z2^3.
That observation is not a constructed root-by-root map. For spin-half D2d,
the center audit removes one of the two excess Z2 factors in the source-side
comparison; the remaining difference requires an audit of the 2D pattern
relations and incoming bubbles. This file does not claim that audit completed.

## S4 rotoinversion

The source (`main.tex:5250-5265`, Table II line 269) names a CI sheet, a
neutral E8 sheet, odd center charge and a center rotation character, all of
order two, and asserts Z2^4 for both spins. Removing its named E8 root gives
Z2^3. The computed CI/charge/phase sector instead has Z2 x Z4. This is an
extension disagreement of equal group orders, not a difference in the number
of associated-graded states.

The source describes one removable charge-two orbit carrying rotation
eigenvalue -1. That relation alone is not enough to infer the center quotient:
axis sites have residual C2 representations and their other allowed characters
must also be included. The independent formula audit therefore checks the CI
root square and its full gauge completion. No conclusion about a missing
source extension is inferred solely from a truncated orbit relation.

## Reproduce the independent center audit

```bash
python benchmarks/audit_center_orbits.py insulator_catalog/generated/point3_06_spin_half.json
python benchmarks/audit_center_orbits.py insulator_catalog/generated/point3_14_spinless.json
python benchmarks/audit_center_orbits.py insulator_catalog/generated/point3_14_spin_half.json
```

This audit covers center states and mobile atomic orbits in D2 and D2d only.
It does not compute CI decorations, Haldane chains, higher differentials,
neutral E8, or the full 3D classification. Its physical-space character
coordinates are not automatically the onsite AHSS filtration coordinates.
