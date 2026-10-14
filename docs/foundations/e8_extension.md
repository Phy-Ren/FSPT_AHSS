# E8 extension notes (deferred)

Status: deferred, 2026-10-14. These notes preserve the mathematical input
for future work. E8 decoration is not implemented, and full E8-inclusive
classification tables are deferred until a separate implementation and
review. The previous reference-only full tables have been withdrawn from
the active comparison set; their source fixtures remain available.
The definition and validation status of the present model are on the separate
[CI-sector page](ci_sector.md).

**The coefficient to add.**

A two-dimensional neutral E8 layer is bosonic and invertible, with electric
Hall conductivity zero and chiral central charge eight. With electron
charge one, the full charge-conserving 2+1D coefficient lattice is

\[
 L=\{(\sigma_{xy},c_-)\in\mathbb Z^2:c_- -\sigma_{xy}\in8\mathbb Z\}
   =\mathbb Z I\oplus\mathbb Z E,
 \qquad I=(1,1),\quad E=(0,8).
\]

Thus a local layer `(n,e)` has `sigma_xy=n` and `c_-=n+8e`. This coefficient
classification is derived by Barkeshli, Chen, Hsin, and Manjunath (2022),
[Classification of (2+1)D invertible fermionic topological phases with symmetry](https://arxiv.org/abs/2109.11039),
in its `U(1)^f` and class-A examples.

The minimal BIQH state of charge-two bosons is `(sigma_xy,c_-)=(8,0)`, so
`BIQH_2=8I-E`. Neutral E8 and eight electronic CI layers are distinct.
This relation also prevents identifying “omit E8” with “quotient by all
bosonic phases.” Even at the coefficient level these give different
groups: `L/<E>=Z` but `L/<E,BIQH_2>=Z8`. The
[2D sector page](two_dimensional_sectors.md) treats uniform-response choices.

**Where E8 enters the decoration data.**

In spatial dimension `d`, a 2D layer occupies codimension `d-2`. Its group
cochain therefore has degree `d-2`:

| Spacetime | E8 cochain | Geometric support of its decoration |
|---|---|---|
| 2+1D | `e0` in `C^0(G,Z_s1)` | Uniform two-dimensional layer |
| 3+1D | `e1` in `C^1(G,Z_s1)` | Two-dimensional domain walls, dual to one-cochains |
| 4+1D | `e2` in `C^2(G,Z_s1)` | Two-dimensional junctions, dual to two-cochains |

Both CI and E8 chirality reverse under `s1`. Charge conjugation alone does
not reverse their Hall/thermal chirality. In 3+1D the two-dimensional
coefficient row is consequently the pair `(n1,e1)` with coefficient module
`Z_s1 I + Z_s1 E`. At the initial cohomology stage it contributes
`H^1(G,Z_s1 I + Z_s1 E)`. These are two coordinates of one coefficient row,
not two independently completed classifications.

In particular, `e1` is an **integer** twisted one-cocycle. In normalized
inhomogeneous notation its leading condition is

\[
 e_1(gh)=e_1(g)+(-1)^{s_1(g)}e_1(h).
\]

The leading coboundary change is `e1 -> e1+d_s1 u0`. This says nothing yet
about the necessary simultaneous changes of lower charge and phase fields.
It must not be used as a complete new gauge formula. For `C2^T`, the
representative `e1(T)=1` generates `H^1(C2,Z_s)=Z2`; the coefficient itself
is still integral, and the order two comes from the coboundary quotient.

Chen, Lu, and Vishwanath (2014) explicitly place chiral E8 states on
oriented time-reversal walls, with chirality reversed together with wall
orientation; see the three-dimensional time-reversal section of
[Symmetry protected topological phases from decorated domain walls](https://arxiv.org/abs/1303.4301).
Song, Xiong, and Huang (2020) give the corresponding twisted one-cocycle
and cellular interpretation for crystalline E8 configurations; see
[Bosonic crystalline phases beyond group cohomology](https://arxiv.org/abs/1811.06558).
Their construction and splitting theorem concern bosonic phases. They do
not supply the electronic mixed cochain operations required here.

The degree-two entry in 4+1D is also discussed explicitly by Gaiotto and
Johnson-Freyd in the subsection “Time reversal and E8” of
[Symmetry Protected Topological phases and Generalized Cohomology](https://arxiv.org/abs/1712.07950):
E8 layers can occur at symmetry-wall junctions. The coefficient degrees
alone do not determine the spectrum's higher operations.

**A bounded 3+1D conclusion about incoming classes.**

The missing E8 row could contribute incoming identifications to the
3+1D lower filtration from degree-zero E8 data. In the usual full AHSS,
this particular source is controlled without inventing a local operation:

1. If `s1=0`, a neutral E8 phase with trivial action of the entire internal
   group is a symmetric 2+1D phase. It ignores the charge extension and
   charge conjugation. Its edge image is the generator of `H^0(G,Z)=Z`.
   Existence of this lift makes that generator a permanent cycle, so all
   its obstruction differentials vanish as cohomology classes.
2. If `s1` is nontrivial, `H^0(G,Z_s1)=0`, because an invariant integer must
   equal its negative. There is no degree-zero incoming E8 class.

For a finite proper point group, `s1=0` and
`H^1(G,Z)=Hom(G,Z)=0` as well. Thus there is no nonzero E8 decoration class
on this 3+1D row, and its `H^0` source does not introduce an incoming
identification. Checking `H^1=0` alone would not establish the second
statement; the symmetric-layer lift is the missing argument.

For a finite group with nontrivial sign, the initial E8 group is
`H^1(G,Z_s1)=Z2`. To see this, restrict a twisted cocycle to the finite
kernel of the sign, where it is a homomorphism to `Z` and hence zero. It is
then determined by one integer on the reversing coset; a coboundary changes
that integer by two. This is a coefficient-row calculation, not the final
electronic classification.

Applying the incoming result to the program requires identifying the
retained tower with the full theory's corresponding filtration. The
argument does not perform that identification. It nevertheless gives no
basis for blaming the current proper-group discrepancies on E8. It also
does not cover all incoming sources in 4+1D, where degree-one E8 data can
enter. Infinite space groups can have nonzero `H^1(G,Z)` even when proper,
so the finite-group vanishing statement must not be reused there.

**Independence and splitting need their own evidence.**

The lattice decomposition `L=Z I + Z E` fixes a coefficient basis. It does
not imply a product decomposition of the complete symmetry-protected
classification. Nor does a bosonic phase necessarily remain independent
after embedding into an electronic system.

There are verified distinctions. For charge-preserving mirror symmetry,
Song, Huang, Fu, and Hermele (2017) construct the `Z8 x Z2` roots, including
an independent neutral E8 paramagnet. Its surface has thermal chirality
without electric Hall response; their Section IV rules out reproducing it
with a trivial two-dimensional electronic surface. Their Section IV A does
not itself exclude additional interacting internal 2D SPT roots, so that
construction alone should not be cited as a completeness proof. See
[Topological phases protected by point group symmetry](https://arxiv.org/abs/1604.08151).

Ning, Mao, Li, and Wang (2021) provide a more explicit root dictionary in
[Section III B 1 of their anomaly-indicator study](https://arxiv.org/abs/2105.02682).
Their mirror-plane roots `(mu1,mu2,mu3)` count neutral E8, IQH, and the
relative `Z4` SPT. After adjoining layers, the independent indicators are
`eta1f=exp[i pi (mu2-2mu3)/4]` and `eta2f=(-1)^mu1`. Thus their E8 generator
has `(eta1f,eta2f)=(1,-1)`, while the IQH generator has
`(exp(i pi/4),1)`. This supplies symmetry-specific evidence for the
independent E8 factor and a concrete target for a future program-root map.

In contrast, a different
bosonic phase, eTmT, equals four copies of the AIII electronic root and
becomes trivial for charged non-Kramers fermions in AI; see
[Metlitski, Section VI](https://arxiv.org/pdf/1510.05663) and the
[Wang–Senthil erratum](https://arxiv.org/abs/1401.1142v3).
Those examples concern the bosonic embedding and do not demonstrate an
E8 incoming differential in our 3+1D calculation.

The full 3+1D groups for AIII, AII, and AI are respectively `Z8 x Z2`,
`Z2^3`, and `Z2`, by Freed–Hopkins Corollaries 9.91, 9.93, and 9.95 of
[Reflection positivity and invertible topological phases](https://arxiv.org/pdf/1604.06527).
They are useful complete-theory benchmarks. Adding a factor to reproduce
these group orders would not construct the missing cochain theory.

**Mathematical input required before implementation.**

The extension needs a specified full electronic coefficient spectrum or an
equivalent physical construction, together with the embedding of its CI,
neutral E8, and charge-two BIQH generators. Within that model one must
determine the E8 obstruction operations and their allowed completions in
each dimension; the leading cocycle condition is only the first step.
One must then give the full gauge transgressions and incoming images,
including changes of the retained coordinates, and the stacking law for
two complete states with nonzero E8 data, including mixed terms and closed
corrections. Vanishing operations must be justified in their applicable
dimension and symmetry class.

A comparison map to bordism characters or explicit physical states must
finally identify the roots and their relations. It should reproduce the
3+1D permanent-cycle constraint above and the independent mirror E8
detector. None of these missing operations is represented in the runtime
by a placeholder zero.
