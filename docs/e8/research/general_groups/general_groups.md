# E8 closure for finite-holonomy discrete groups

Independent review, 2026-10-15. This report concerns the formal domain
`1 -> Z^r -> G -> F -> 1`, with finite `F` and translation rank no greater
than the physical spatial dimension, at most four. It does not modify the
production classifier. All state coordinates have the order
`(e_p,n_p,n_{p+2},nu_{p+3})`, where `p=d-2`: neutral E8 first, then CI,
localized charge, and one shared phase. The chirality character is
`s:G -> {+1,-1}`; `Z_s`, `Q_s`, and `R_s` denote its coefficient modules.

**Result.** Infinite translations do not obstruct completion of the supplied
neutral cubic in this domain. There is an exact rational construction of
the phase completion, even for a free E8 decoration. The three-dimensional
neutral invariant has free summands and, when `s` is nontrivial, exactly
one `Z2` summand. Its selected physical section extends under explicit
symmetry-pullback and crystalline-equivalence assumptions. Neither result
proves that the inherited CI algorithm is the entire physical kernel, or
removes the intrinsic coefficient row in 4+1D.

## 1. Real and rational cohomology: a dimension bound, not finite averaging of e2

Replace the normal translation subgroup `T` by
`T'=T intersect ker(s)` if necessary. This is still normal, has rank `r`,
and has finite index in `G`; it acts trivially on the coefficient module.
Put `F'=G/T'`. The Lyndon–Hochschild–Serre sequence over a characteristic-zero
field `K` has

\[
E_2^{a,b}=H^a(F',\Lambda^b\operatorname{Hom}(T',K)\otimes K_s).
\]

Finite-group averaging kills all columns with `a>0`. Thus

\[
H^k(G,K_s)\cong
\bigl(\Lambda^k\operatorname{Hom}(T',K)\otimes K_s\bigr)^{F'},
\qquad H^k(G,K_s)=0\quad(k>r).                 \tag{1}
\]

This proof includes nonsymmorphic groups, finite ineffective internal
symmetries, and antiunitary translations. It does not assume that the group
extension splits. In particular `H5(G,R_s)=H6(G,R_s)=0` for `r<=4`.

For 4+1D, take any closed integral `e_2`. The rational source
`alpha/3`, where `alpha=e_2 cup e_2 cup e_2`, is closed and has sign `s`.
Equation (1) gives a rational `nu_5` with

\[
\delta_s\nu_5=e_2\cup e_2\cup e_2/3.          \tag{2}
\]

Reduction modulo integers supplies the neutral phase completion. This
does **not** require `e_2=delta_s a_1` over the reals. That stronger condition
is available for finite groups but fails for many translation decorations.
It is the degree-six cohomology, rather than degree two, that matters.

The coefficient long exact sequence also gives

\[
H^5(G,\mathbb R/\mathbb Z_s)\xrightarrow[\cong]{\beta}
H^6(G,\mathbb Z_s),                            \tag{3}
\]

and, for `r<=3`, the analogous isomorphism
`H4(G,R/Z_s) -> H5(G,Z_s)`. These statements concern these degrees in the
specified domain; they are not the general identification of flat phases
with integral response theory for arbitrary infinite or continuous groups.

### A constructive rational completion

Choose a proper cocompact affine action of `G` on `R^r`. Such an action
exists even with a finite ineffective kernel: the extension cocycle of the
finite group `F` becomes a coboundary in `R^r`, so a real choice of lifts
defines the affine action. Its kernel is finite. After an admissible
equivariant subdivision, the augmented cellular complex `P_*` of `R^r`
is an exact complex of `Q[G]`-modules of length `r`. Each module is a sum
of modules induced from trivial modules of finite cell stabilizers. Those
are projective over `Q`, by finite-stabilizer averaging. Thus `P_*` is a
projective resolution of the trivial module.

Let `B_*` be the rational bar resolution. Construct comparison maps
`f:B_* -> P_*`, `g:P_* -> B_*` and an equivariant chain homotopy

\[
1-gf=\partial H+H\partial.
\]

For `alpha=e_2^3` as a `Q[G]`-linear map `B_6 -> Q_s`, define

\[
\nu_5=\tfrac13\alpha H_5.                     \tag{4}
\]

Because `P_6=0`, `f_6=0`; because `alpha` is closed,
`alpha partial_7=0`. Therefore

\[
\delta_s(\alpha H_5)=\alpha H_5\partial_6
=\alpha(1-g_6f_6-\partial_7H_6)=\alpha.
\]

This proves (2) with exact rational arithmetic and is an algorithm once
the cellular resolution and comparison homotopy are supplied. It is not a
claim that those comparison maps have already been implemented for every
space group. In particular, it never requests a nonexistent primitive of
the free class `e_2` itself.

## 2. The exact completion criterion and the remaining extension

For any discrete group define the flat-model obstruction

\[
Q([e_2])=[e_2^3/3\bmod\mathbb Z]
\in H^6(G,\mathbb R/\mathbb Z_s).
\]

The coefficient exact sequence proves the exact criterion

\[
Q([e_2])=0\quad\Longleftrightarrow\quad
\tfrac13[e_{2,\mathbb R}^{\,3}]
\in\operatorname{im}\{H^6(G,\mathbb Z_s)\to H^6(G,\mathbb R_s)\}.
                                                               \tag{5}
\]

Consequently a real primitive of the cubic is sufficient, while a real
primitive of `e_2` is unnecessary. The supplied cubic polarizer makes `Q`
additive: the cubic cross terms are multiples of three in cohomology, and
the noncommuting cochain representatives differ by its explicit coboundary.

For the pure-neutral closed-sheet cochain model, its completed state group
has the exact sequence

\[
0\longrightarrow H^5(G,\mathbb R/\mathbb Z_s)
\longrightarrow N_{\rm flat}(G)
\longrightarrow\ker Q\longrightarrow0.        \tag{6}
\]

At zero E8 sheet the residual closed E8 gauge contributes no phase, which
identifies the left-hand kernel. Equation (1) makes the final term all of
`H2(G,Z_s)` in the space-group domain. **Surjectivity is not splitting.**
The completed `C3` example is `Z9`, not `Z3 x Z3`.

The CI and neutral models share the same phase, so their combination must
identify the common phase map, including any kernel produced by incoming
CI relations. Multiplication of graded groups discards this information.
In the present domain every neutral sheet separately completes; subtracting
such a completed neutral state from a completed joint state leaves a
completed CI state. This is the existence input needed for the shared-phase
pushout description. The assertion need not hold outside this domain if
two individually obstructed sources cancel only in the joint model.

## 3. H1, free layers, and the selected 3+1D section

For a finitely generated group the crossed-homomorphism group
`Z1(G,Z_s)` is a subgroup of a finite-rank free abelian group. If `s` is
trivial, `H1(G,Z)=Hom(G,Z)` is free. If `s` is nontrivial, choose `g0`
with `s(g0)=-1` and set

\[
\sigma(g)=(1-s(g))/2,\qquad
K=\{e_1\in Z^1(G,\mathbb Z_s):e_1(g_0)=0\}.
\]

Evaluation at `g0` gives
`Z1=Z sigma direct-sum K`, and the principal coboundaries are
`2Z sigma`, up to the conventional overall minus sign. Therefore

\[
H^1(G,\mathbb Z_s)\cong
\begin{cases}
\mathbb Z^k,&s=1,\\
\mathbb Z^k\oplus\mathbb Z_2,&s\ne1.
\end{cases}                                      \tag{7}
\]

For finite-holonomy groups, `k` is the invariant real dimension in (1).
The integral lattice still has to be computed: real ranks do not fix
primitive translation multiplicities, as the screw example below shows.

Song–Xiong–Huang construct a bosonic section and a left inverse for
ordinary three-dimensional space groups in Section V.C. Their Appendix
A.3 separately establishes the signed `H1` calculation for magnetic space
groups. These are different claims: the latter cohomology theorem alone
is not a new explicit construction of every magnetic phase. Their physical
classification uses the stated short-correlation-length/cellular setting.
[Song–Xiong–Huang, 2020](https://arxiv.org/abs/1811.06558).

A useful conditional extension makes the physical input explicit. Every
crossed homomorphism determines a genuine group homomorphism

\[
\phi_{e_1}:G\to\mathbb Z\rtimes C_2=D_\infty,
\qquad g\mapsto(e_1(g),s(g)).                   \tag{8}
\]

The weak neutral E8 root for the one-axis translation/reflection group
has a unit translation invariant. Under symmetry-pullback naturality and
the crystalline/internal-equivalence convention, its pullback along (8)
completes any `e_1`. Choose lifts of a free basis in (7), and choose for
the `Z2` generator the pullback along `s` of the order-two time-reversal
E8 root. These choices produce a homomorphic section. This construction
is noncanonical; it does not assert that a particular section is natural
under every change of group or every cochain convention. The order-two
neutral construction has a primary decorated-wall realization in
[Chen–Lu–Vishwanath, 2014](https://arxiv.org/abs/1303.4301).

Thus finite generation plus these physical pullback assumptions suffices;
finiteness of `G` is unnecessary. All groups in the formal domain are
finitely generated. If one declines those physical assumptions, the
unconditional result is (7), together with the directly constructed
ordinary-space-group section, rather than a theorem about arbitrary
abstract symmetry groups.

Finite internal extensions do not introduce a hidden free neutral sector.
If a finite normal internal subgroup has trivial `s`, its `H1(-,Z)`
vanishes and inflation identifies the quotient's signed `H1` with that of
the full group. If the finite internal kernel contains an element with
negative `s`, it commutes with a normal unitary translation subgroup:
their commutator lies in the trivial intersection of that finite kernel
with the torsion-free translations. The crossed-homomorphism equation
then forces every translation value to vanish. The neutral `H1` reduces
to the finite quotient's `Z2`, realized by the time-reversal pullback.

### Electronic survival and the dimension-specific incoming argument

The two-dimensional electronic coefficient has E8-first coordinates
`(e,n)` with electrical and thermal responses `(sigma,c)=(n,n+8e)`.
The neutral coefficient inclusion `e -> (e,0)` has an equivariant left
inverse. Given the physical bosonic section and electronic AHSS
naturality, its image is a completed physical class. At filtration one,
an incoming differential `d_r`, `r>=2`, would have negative source
filtration. Thus this neutral class cannot be killed by an incoming map.
Its additive leading coordinate and the chosen section give a split
neutral summand in 3+1D, under these hypotheses.

This does **not** identify the remaining physical kernel with the retained
CI algorithm. The internal AIII/AII/AI totals and the mirror indicators
support the selected neutral dictionary, but are not that identification
for every group; see the preceding
[three-dimensional review](../../3p1.md).

The possible uniform E8 incoming row can be dealt with specifically here.
For nontrivial `s`, `H0(G,Z_s)=0`. For trivial `s`, a uniform neutral E8
layer with trivial internal action is a symmetric physical lift of its
generator, so that generator is a permanent cycle and its obstruction
maps vanish. This is stronger than arguing only that `H1` vanishes for
proper point groups.

An intrinsic 4+1D coefficient cannot become an incoming correction to a
3+1D group. In the indexing where a coefficient's spacetime degree is `q`
and a decoration has filtration `p`, total degree is `p+q`; an incoming
differential to total degree four starts in total degree three. A source
coefficient of degree five would require `p=-2`. This degree argument
does not depend on whether `BG` has infinitely many cells. In 4+1D the
intrinsic row itself is present and must instead be kept explicitly.

## 4. Reproducible examples, separated by dimension

`check_examples.py` preserves the supplied extraction and writes
`examples.json`. Its presentation calculations use the pinned v0.9
integer-kernel implementation, whose SHA-256 is recorded in the output.
The independent bar-cochain calculations and tables are in separate files:

- [3+1D signed H1 presentation examples](examples_3p1.md): translations,
  mirror, glide, inversion, screw, and antiunitary extensions.
- [4+1D free-sheet completions](examples_4p1.md): `Z^4`, a four-dimensional
  glide, and exact bar-cochain primitives.

These are algebraic diagnostics, not full global classification tables.

Executed command:

```sh
PYTHONDONTWRITEBYTECODE=1 python check_examples.py
```

Result: all nine presentation cases passed; 3,000 exact square-primitive
checks, 3,000 exact single-free-sheet completions, and 3,000 two-free-sheet
stacking completions passed. These verify the examples and the local
identities, not a new global physical classification table.

The separate [2+1D uniform-response argument](uniform_2p1.md) explains the
free-quotient splitting and its physical scope. It contains no new global
classification table.

## Appendix: why unrestricted discrete and continuous groups remain separate

The exact criterion (5), rather than `e_2` being torsion, is the right
criterion for the flat model on any discrete group. It can fail outside
the formal space-group domain. Leary's metric Kan–Thurston theorem gives,
from a finite triangulation of `CP3`, a finite aspherical cubical complex
`B G` and a map to `CP3` inducing integral homology isomorphisms. Pull back
the degree-two generator. Its cube has period one on an integral
six-cycle, so `e_2^3/3` has period `1/3` and cannot have a flat phase
primitive. This gives a finitely presented, torsion-free discrete example;
it is not virtually abelian of translation rank at most four.
[Leary, Theorem A, 2013](https://arxiv.org/abs/1009.1540).

Such failure is not automatically a physical obstruction. The class `Q`
has a closed real lift, so its integral connecting Bockstein is always
zero. Replacing a generalized integral response theory by ordinary flat
`R/Z` cochains can lose characteristic responses. For continuous `U1`,
for example, the unit class on `BU1` gives `1/3` on `CP3`, while the mixed
characteristic response `(e_2 p1-e_2^3)/3` has the required integral
periods in the oriented response theory. The source's generalized
cohomology and physical normalizations must be retained; this observation
does not provide a completed continuous-group implementation.
[Saito–Tachikawa–Zhang, Section 3.2 and Appendix C, 2026](https://arxiv.org/abs/2607.14662v2).
Gaiotto–Johnson-Freyd also explicitly distinguish finite-group flat-phase
formulas from general realization/response data.
[Gaiotto–Johnson-Freyd, 2019](https://arxiv.org/abs/1712.07950).

## Primary-source locations read for this review

- Song–Xiong–Huang, *Bosonic Crystalline Symmetry Protected Topological
  Phases beyond the Group Cohomology Proposal*, PRB 101, 165129 (2020),
  arXiv:1811.06558. Cached `cSRE_arXiv_v1.tex:1559–1665` constructs the
  section; `1730–1780` gives weak-layer constructions; `2171–2250` treats
  magnetic signed H1. The surrounding scope discussion is at `1892–1916`.
- Chen–Lu–Vishwanath, *Symmetry protected topological phases from decorated
  domain walls*, Nature Communications 5, 3507 (2014), arXiv:1303.4301.
  Cached `ddwSPT.tex:546–556` treats E8-decorated time-reversal walls.
- Leary, *A metric Kan–Thurston theorem*, Journal of Topology 6, 251–284
  (2013), arXiv:1009.1540. Cached `mktjtar.tex:248–290`, Theorem A;
  `210–223` recalls asphericity of locally CAT(0) complexes.
- Gaiotto–Johnson-Freyd, *Symmetry Protected Topological phases and
  Generalized Cohomology*, JHEP 05 (2019) 007, arXiv:1712.07950.
  Cached `SuperCohomology.tex:746–752` distinguishes finite-group
  coefficients; `1029–1044` discusses the E8/time-reversal prediction.
- Saito–Tachikawa–Zhang, *Bosonic SPT and invertible phases and its relation
  to Steenrod's problem*, arXiv:2607.14662v2 (2026). Cached
  `oriented-paper-arXiv-version2.tex:1060–1090` defines the characteristic
  generator; Appendix C, `2540–2645`, supplies its Postnikov setting.
  The separate physical review resolves lens-space generator normalization;
  no eta value is inferred here from the bare group-cochain phase.

All cited fulltexts were retrieved and their relevant passages read.
