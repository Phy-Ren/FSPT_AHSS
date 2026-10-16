# Audit of the remaining 3+1D point-group discrepancies

Date: 2026-10-16. Scope: U(1)^f, interacting insulators, the current E8-inclusive
catalogue. No production result or formula was changed. The numerical four-data
model and its identification with the full physical spectrum remain distinct.

## Main finding

The normal-C3 cases now have substantially stronger evidence than repeated
agreement between implementations of the same cochain formulas. Their full
bordism classifications reduce to smaller groups by an actual map of twisted
Thom spectra. This controls stacking extensions as well as graded layers.
The physical conclusion uses the phase-homology/bordism ansatz, just as the
Debray comparison does; it is not a theorem about all microscopic Hamiltonians.

For C3i, D3d, C6h and D3h, the fresh audit verifies the geometric and symmetry
data needed for that reduction. The resulting groups agree with our current
catalogue. The discrepant entries of Zhang--Ning--Qi--Gu are consequently
incompatible with these bordism reductions. This statement is about specific
entries and proofs, not about the reliability of an author as a person.

S4 and D2d now also have independent full bordism checks. The new
[S4 Gysin computation](S4_gysin.md) derives its nontrivial extension from the
actual subgroup map BC2 -> BC4, independently of the cochain formulas. The
separately reviewed D2d Adams/Koszul calculation, recorded in
`d2d_ext_audit.json` and `d2d_peer_oh.json`, agrees with the current answer for
both spins. D2d still has a specific possible missing real-space bubble relation;
the corresponding physical adjoining path has not been established, even
though the independent group computation no longer depends on that path.

## Source versions and corrections

The primary real-space source is Jian-Hao Zhang, Shang-Qiang Ning, Yang Qi and
Zheng-Cheng Gu, *Construction and Classification of Crystalline Topological
Superconductor and Insulators in Three-Dimensional Interacting Fermion Systems*,
[Phys. Rev. X **15**, 031029 (2025)](https://doi.org/10.1103/PhysRevX.15.031029),
published July 28, 2025. The current published Table II is read separately from
[arXiv:2204.13558v2](https://arxiv.org/abs/2204.13558v2), June 18, 2024.
The journal [supplement](https://journals.aps.org/prx/supplemental/10.1103/PhysRevX.15.031029/3DpointCombine__supp.pdf)
is dated July 8, 2025. It was reread through the publisher PDF web view; direct
local download returned HTTP 403, so no local supplement hash is claimed.

A targeted publisher/arXiv search on this date found no separately published
erratum for PRX 15, 031029. This is a search result, not proof that no correction
exists. The four changed full-group cells between v2 and the journal are
D2d spin-half, C6h spin-half, and both D3h spins. These are version changes;
do not call them a separately published erratum.

The known PRB **103**, 099902 (2021) erratum belongs to the different 2D paper
PRB **101**, 100501(R) (2020), as linked on its
[publisher page](https://journals.aps.org/prb/abstract/10.1103/PhysRevB.101.100501).
It is not a correction to the 2025 3D U(1)^f table. The fulltext tool and direct
publisher PDF access for that erratum were blocked; no assertion about its
detailed correction is made here.

The independent mathematical source is Arun Debray,
[*Invertible phases for mixed spatial symmetries and the fermionic crystalline
equivalence principle*, arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3),
February 3, 2026. Theorem 2.24 supplies the class-A Thom-spectrum dictionary;
Theorem 4.57, p.49, supplies the Pin-c bordism anchor used below. Lemma 5.99,
p.87, explicitly uses the same mod-2 Thom-isomorphism/Whitehead strategy as our
subgroup argument. Our reduction to these particular groups is an inference,
not a separately printed classification table in that paper.

## Fresh exact background checks

`check_odd_c3_maps.py` imports no classifier. It reads the current catalogue's
finite multiplication tables, matrices, signs, effective extensions and geometric
Pin-minus cocycles. It independently exhausts subgroups and normalized binary
gauge cochains, and solves exact rational intertwining equations.

All eight spin-specific cases pass. The maps are:

- C3i -> Ci: kernel C3, complement C2.
- D3d -> C2h: kernel C3, complement C2 x C2.
- C6h -> C2h: kernel C3, complement C2 x C2.
- D3h -> C2v: kernel C3, complement C2 x C2.

The saved `odd_c3_current_witnesses.json` includes every quotient and section
index, a nonsingular rational matrix X satisfying
`V_source(j(h)) X = X V_target(h)`, the full-source gauge between omega and the
inflated target omega, and a full-source coboundary witness for the geometric
Pin-minus extension. This checks the physical spin convention as well as the
effective cochain background. In particular, isomorphism of abstract groups
alone is not used to identify two spatial actions.

E8 is included. Its finite improper-group generator is the integer cocycle
`e(g)=s(g)`; `2e=d_s(-1)`. It pulls back exactly under all displayed quotient
maps. It is nontrivial because any constant integer coboundary is even at an
orientation-reversing element. Thus there is no reference-side deletion of a
Z2 factor in this audit.

## Why the subgroup result is stronger than a four-data test

Let `1 -> C3 -> G -> H -> 1` split by the verified complement `j:H->G`.
The Lyndon--Hochschild--Serre spectral sequence with F2 coefficients collapses
because positive cohomology of C3 with F2 coefficients vanishes. Inflation is
an isomorphism; `j*` is its inverse. This statement needs the normal odd kernel,
not merely an odd subgroup index.

The actual rank-three spatial representation V restricts along j to the target
representation, as certified by X. The full spin extension also restricts
correctly. Consequently the natural map on the class-A Thom spectra induces
an F2-homology isomorphism, by the Thom isomorphism. These are bounded-below
spectra of finite type in each degree. Mod-2 Whitehead/Adams completion gives
an equivalence after 2-completion. Smashing with MTSpin-c preserves it.
The 2-primary torsion in the relevant bordism groups, and hence in their
Anderson-dual phase groups, is identical, including all extensions. This is
the same reasoning pattern used in Debray's Lemma 5.99.

This proof does not install any omitted differential as zero. A missing term
in the supplied four-data theory cannot evade a full bordism equivalence.

## Independent C2h anchor and rank conventions

In the current C2h matrices,

```
chi = (1,-1, 1,-1),       psi = (1,-1,-1, 1),
V = psi + chi + psi,     Det(V) = chi.
```

The two nontrivial real characters chi and psi are independent. For physical
spinless fermions, the class-A crystalline spectrum uses the rank-zero twist

```
3 - V = (1 - chi) + (2 - 2 psi).
```

The second summand is a rank-zero virtual complex line: two copies of a real
sign character are the underlying real plane of a complex character. It is
Spin-c oriented, so its Thom isomorphism removes that summand without a degree
shift. For physical spin-half fermions, the shearing formula gives the
determinant twist `chi - 1`; where the symmetry extension splits, the alternative
`3-V` formula is equivalent by the same orientation argument. Finally,
`(1-chi)-(chi-1)=2-2chi` is also a rank-zero virtual complex line. Both spins
therefore give

```
MTSpin-c smash (B(C2 x C2))^(chi-1)
  = MTSpin-c smash (BC2)^(sigma-1) smash (BC2)_+
  = MTPin-c smash (BC2)_+.
```

The two Pin-c conventions obtained by extending Pin+ or Pin- by the charge
circle are equivalent here; their rank-zero Thom twists differ by the
Spin-c-oriented doubled line just displayed. This is the Pin-c, not the
Pin- or Pin+ superconductor, calculation.

Debray Theorem 4.57 identifies
`Omega_4^Pin-c(BC2) = Z8 + Z4 + Z2` and states that the degree-five group is
torsion. The Anderson-dual exact sequence therefore gives the finite phase
group `Z2 x Z4 x Z8`. No shifted degree has been substituted: Ext uses degree
four and Hom uses degree five. This establishes the lower anchor independently
of the supplied AHSS implementation and independently of R3's C2h row.

## Ci and C2v anchors: exact locators and degree checks

For **Ci with either physical spin**, Debray section 4.2.3, printed p.32,
reduces `3-3sigma` to `1-sigma` by the Spin-c Thom isomorphism; section 4.1.3,
p.30, identifies the result with Pin-c bordism (also equation 2.10c, p.17).
This anchor can additionally be checked with the same fresh Gysin matrices
used in [the S4 audit](S4_gysin.md): the sign-line cofiber for C2 has sphere
bundle B1, so `(BC2)^(sigma-1)=Sigma^-1 reduced(BC2)` stably. Consequently
`ku_4=ku_5(BC2)=Z8` from `SNF(A2)=(1,1,8)`, and
`ku_0=ku_1(BC2)=Z2`. The degree-five Spin-c group has no free part. This gives
the full `Z8 x Z2` independently of a printed classification table.

For **C2v with physical spin-half**, the spatial representation is two
independent reflection characters plus a trivial line. Theorem 2.24 gives
the determinant twist over B(C2 x C2), which is the same
`MTPin-c smash (BC2)_+` as the C2h anchor. Debray Theorem 4.57, printed p.49,
gives `Z8 x Z4 x Z2`. Its proof's actual ku-spectrum splitting was reread:
the two ku summands are `ku smash Sigma^-1 BC2` and
`ku smash Sigma BC2`; the additional Eilenberg--Mac Lane generators have odd
degree. Thus degree four is `Z8 x Z4`, and degree zero is `Z2`.
These low-degree cyclic values also follow directly from Hashimoto's Gysin
matrices. The published Ossa spectrum splitting is used here, not re-proved
from scratch in this audit.

For **C2v with physical spinless fermions**, the twist is `2-V_plane`.
Debray Theorem **4.45**, printed p.45 (not Theorem 4.44, which is the odd-n
case), gives the full `Z2^4`. We reread its supporting equation (4.46) and
Figure 5, p.46: there are three free E(1)-module generators in degree four,
each yielding a filtration-zero ku class, and one in degree zero. The other
displayed summand contributes in odd stems. No incoming Adams differential
can reach filtration zero; there are no outgoing targets at the requisite
filtration, and the degree-four classes have no higher filtration for a
hidden 2-extension. Hence `ku_4=Z2^3`, with the separate shifted `ku_0=Z2`.
This checks the printed proof's degree count and extension claim; we have
not independently regenerated its entire E(1)-module from matrices in this
subtask. The current exact subgroup/matrix checks do independently identify
the physical background to which the anchor applies.

## Odd-prime and free contributions

The only possible odd prime for the groups above is 3. Restriction to their
Sylow C3 has index 2 or 4, invertible at 3. The finite-cover transfer composite
induces multiplication by that index on ordinary F3 homology; bounded-below
finite-type mod-3 Whitehead therefore makes the composite a 3-complete
equivalence, which supplies a retract and detects 3-primary contributions.
The generalized-transfer composite itself is not assumed to be the scalar
index map. On C3 the spatial representation is a
rotation plane plus a fixed real axis, so the plane is complex and the
class-A twist is Spin-c oriented; the spin extension introduces no odd-primary
obstruction. Debray Theorem 4.14 gives
`Omega_4^Spin-c(BC3)=Z^2` and degree-five torsion. Hence the 3+1D phase group
on that Sylow subgroup has no 3-primary torsion. Equivalently, the ordinary
homological AHSS has no positive even-degree homology of BC3 that could add
degree-four torsion to the even Spin-c coefficient groups.

There is also a direct twisted homological-AHSS check, avoiding any assumption
that a generalized-cohomology transfer composite is literally multiplication
by the index. Localize at 3. In the normal-C3 extension, the quotient has
order 2 or 4, so its positive homology vanishes over Z_(3). The three E2
positions of total bordism degree four use `p=4,2,0` and Spin-c coefficient
degrees `q=0,2,4`. Positive even-degree C3 homology is zero. At p=0, the
nontrivial orientation character on the quotient has zero coinvariants
because 2 is invertible. Thus every E2 entry of total degree four vanishes;
there can be no 3-primary bordism torsion or hidden extension there.

There is no rational/free phase contribution in these improper-group cases:
the Thom orientation character is nontrivial, and finite-group rational
homology with that sign module vanishes. Thus the full finite bordism phase
groups, rather than only their 2-primary summands, follow from the reductions.
The common basepoint/free coefficients are treated before this twisted-group
statement; no free root is silently dropped.

## Spinless conclusions

- **C3i:** current `Z2 x Z8`; journal `Z2^2 x Z4`. The exact reduction to Ci,
  whose full Pin-c answer is independently known, supports our group and
  rules out the printed group in the bordism framework. This is an extension
  disagreement, not an E8 count.
- **D3d:** current `Z2 x Z4 x Z8`; journal `Z2^2 x Z4`. Reduction to the
  independently established C2h anchor supports our answer. Both the size
  and the exponent of the printed group disagree.
- **S4:** current `Z2^2 x Z4`; journal `Z2^4`. The fresh direct normalized-bar
  audit reproduces a CI-root square with residual phase period 1/2, three
  gauge paths agreeing. Independently, the full [Gysin/bordism calculation](S4_gysin.md)
  gives `ku_4=Z2 x Z4` and the additional `ku_0=Z2`, confirming the full group.
- **D2d:** current `Z2^4`; journal `Z2^3 x Z4`. The freshly replayed atomic
  induction audit conditionally reduces the center group from Z4 to Z2.
  If its orbit is physically removable by an allowed adjoining path, this
  supplies exactly the factor needed for agreement. That path remains open.
  The separate Adams/Koszul audit gives `ku_4=Z2^3`, `ku_0=Z2`, independently
  confirming the current full bordism group without assuming that path.
- **D3h:** the journal `Z2^4` agrees with the current calculation and the
  independent reduction to C2v. Only the older v2 value `Z2^5` disagrees.

## Spin-half conclusions

- **C3i:** current `Z2 x Z8`; journal `Z2^2 x Z4`. Same full Pin-c/Ci
  reduction as above, with the spin extension separately verified.
- **D3d:** current `Z2 x Z4 x Z8`; journal `Z2^3 x Z8`. The independent C2h
  anchor fixes the nontrivial Z4 extension; identical total order is not enough.
- **C6h:** current `Z2 x Z4 x Z8`; journal `Z2^3 x Z8`. The same C2h anchor
  applies. The older v2 table agreed; the journal change introduced this
  disagreement, so a newer version cannot simply be assumed more accurate.
- **D3h:** current `Z2 x Z4 x Z8`; journal `Z2^2 x Z4 x Z8`. Reduction to
  the independently computed spin-half C2v result rules out the extra Z2 in
  the bordism framework. The journal reduced, but did not remove, the old
  discrepancy.
- **S4:** current `Z2^2 x Z4`; journal `Z2^4`. Same model-only extension
  certificate as for spinless, now independently confirmed by the full
  [Gysin/bordism computation](S4_gysin.md).
- **D2d:** current `Z2^3 x Z8`; journal `Z2^4 x Z8`. The journal has already
  removed one extra preprint 2D factor. Thus the existing conditional center
  quotient `Z2^3 -> Z2^2` would now remove exactly the remaining factor, not
  merely one of two discrepancies. This remains conditional on a physical
  bubble path and a root-by-root correspondence. The independent Adams/Koszul
  calculation gives `ku_4=Z2^2 x Z8`, `ku_0=Z2`, confirming the full group
  without using that candidate bubble relation.

The journal locations for the root checks are main IV.B.3 p.38 (S4), and
supplement III.K p.15 (D2d), III.N p.18 (C3i/S6), III.Q p.22 (D3d), III.T p.25
(C6h), III.W pp.28--29 (D3h). These contain the named neutral E8 roots. Their
explicit availability is why none of the discrepancies above can be explained
by accidentally omitting E8 in the comparison.

## Rechecks and remaining physical boundary

Fresh files in this directory:

- `odd_c3_current_witnesses.json`: eight complete subgroup/background checks.
- `cyclic_current_backgrounds.json`: current S4/C3i inputs rephased to the
  standard cyclic `s=rho=parity, omega=0` symmetry extension. S4 spinless
  uses an eighth-valued cochain; its omega is not literally zero in the
  catalogue. Rephasing a background also requires transporting its completed
  state coordinates; one may not change omega alone in a saved solution.
- `cyclic_roots_rechecked.json`: direct bar/periodic complete S4 root-square
  calculation, independent of GAP. The three dedicated tests passed.
- `D2d_spinless_orbit_rechecked.json` and
  `D2d_spin_half_orbit_rechecked.json`: fresh exact character induction and
  conditional Smith quotients, with all full center representation identities.
- `S4_gysin.md`, `S4_gysin.py` and `S4_gysin.json`: natural Gysin-map proof,
  actual spatial representation decomposition and exact Smith forms for the
  independent full class-A S4 computation.

The normal-C3 reductions, S4 Gysin calculation and separate D2d Adams calculation
independently support the full groups in these particular cases within the
bordism framework. The S4 cochain certificate and D2d atomic quotient have
narrower scopes and are supplemental evidence. These finitely many successful
physical-spectrum calibrations do not prove the universal identification of
the supplied nonzero-CI kernel with the full physical spectrum.
