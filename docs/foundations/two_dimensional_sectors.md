# Which 2+1D sector is being classified?

Status: 2026-10-14. This page distinguishes the response sectors and their
stacking structures. The current cochain model's general validation status
is on the [CI-sector page](ci_sector.md). Constructing the additional
neutral coefficient is the deferred [E8 extension](e8_extension.md).

The active tables have separate files for `n0=0` and all allowed `n0`,
and separate files for spinless and spin-half results within each choice.
All these files use `e0=0`. The separate
[e0-inclusive status file](../../results/foundation_review_20261014/2p1d/e0_included.md)
contains no classification table: those results are deferred.

The current 2+1D state is `(n0,n2,nu3)`, where `n0` counts uniform
electronic CI layers. In the full electronic coefficient lattice there is
also a neutral integer `e0`, with responses

\[
 C=\sigma_{xy}=n_0,\qquad c_-=n_0+8e_0.
\]

The present implementation has no independent `e0`. Accordingly, “all
`n0`” means the supplied model along the response condition `C=c_-`; it
does not mean the full physical 2+1D invertible classification.

| Choice | Uniform responses | Stacking structure |
|---|---|---|
| Relative sector: `n0=e0=0` | `C=c_-=0` | A group of relative states |
| Fixed admissible `n0=N`, with `e0=0` | `C=c_-=N` | A fiber; for `N!=0` it is not a group under physical stacking |
| All admissible `n0`, with `e0=0` | All allowed `C=c_-` | The larger group computed by the supplied convention |
| Full physical theory | Both response integers, subject to the symmetry and obstruction conditions | Requires the additional coefficient and its physical operations |

If the retained model has stacking group `T` and response map `n0:T->Z`,
its zero fiber is a subgroup. A nonempty fiber `T_N` is a torsor for that
subgroup: choosing a reference state identifies it with the zero fiber,
but the identification is not canonical. Stacking sends
`T_N x T_M -> T_(N+M)`, and inversion sends `T_N -> T_(-N)`.
A fixed nonzero IQH fiber must therefore not be advertised as a separate
stacking group. A symmetry obstruction can make a requested fiber empty;
one must not assume every integer is admissible for an arbitrary `G_f`.

If `s1` is nontrivial, an invariant uniform integer obeys `n0=-n0`, so
`n0=0`. The same sign argument forces `e0=0` in the full coefficient
lattice. This excludes uniform chirality, not higher-dimensional layer
decorations.

**Obstruction tests precede the product.**

In the supplied endpoint convention the lower equations are

\[
 d_{s_1}n_0=0,\qquad
 d_{r_1}n_2=-n_0d_{\rho_1}\omega_2^{\mathbb R}.
\]

After an allowed charge completion is chosen, the phase satisfies the
terminal source equation in
[the 2+1D formula section](../../formulas/03_two_dimensional.tex).
Changes of completion and incoming charge gauges are part of the
classification. A nonzero exact source is not an obstruction.

Stacking adds the two uniform integers and uses the specified charge
product plus a uniform-IQH correction. In the relative sector both charge
inputs are closed and that uniform correction vanishes. Thus the two
sectors share a formula family but have different physical calibration
status.

**What the physical comparison establishes.**

For `n0=e0=0`, the charge-conserving lattice construction of Wang, Qi, Fang,
Cheng, and Gu (2023) fixes the relative convention; see
[Exactly solvable lattice models for interacting electronic insulators in two dimensions](https://arxiv.org/abs/2112.15533).
The supplied relative cyclic roots also include their full phase and gauge
reductions. For example the `U(1)^f x C2` root has order four, with a
nontrivial bosonic square.

For nonzero `n0`, the archive supplies an explicit source comparison to
the parity theory and a consistent full product, but it explicitly leaves
the universal physical P-move matching of that product unresolved. This
is stated in both
[the dimensional section](../../formulas/03_two_dimensional.tex) and
[the scope table](../../formulas/11_reproducibility.tex). Exact source
polarization checks determine a derivative; a closed correction can still
change the physically relevant stacking relation. Relative-sector success
does not settle that comparison.

**A precise orientation-preserving wallpaper comparison.**

Manjunath, Calvera, and Barkeshli (2024) describe the complete response
classification using three independent integers `c_-`, `k1`, and `kappa`,
with `C=c_-+8k1`, and additional finite invariants. Here `kappa` is the
filling at zero magnetic flux. Their paper gives these independent
coordinates after the defect-relabeling equivalences, rather than only a
count of phases; see Table I and Section III of
[Characterization and classification of interacting (2+1)D topological crystalline insulators](https://arxiv.org/abs/2309.12389).

In these coordinates the response dictionary is

\[
 C=n_0,\qquad c_-=n_0+8e_0,\qquad k_1=-e_0.
\]

Thus `n0=e0=0` corresponds to `C=c_-=0`, whereas all `n0` with `e0=0`
corresponds to `k1=0`. Since the reference integers and finite invariants
are independent, the first restriction retains one free integer and the
second retains two, with the same finite subgroup. This is a restriction
to response-defined subgroups, not a quotient by all bosonic phases.

For `p1,p2,p3,p4,p6`, the reference rotation operators satisfy
`R_minus=exp(i pi Q/M) R_plus`, changing `R^M=1` to `R^M=(-1)^F`.
Because charge is central and all these spatial generators preserve
orientation, this redefinition leaves the translation relations intact
and identifies the abstract symmetry groups for the two spin conventions.
It preserves `C,c_-,kappa` but changes some rotation response coordinates.

The saved
[wallpaper response audit](../../results/calibration_20261014/wallpaper_2024_response_comparison.json)
matches the abstract subgroup types in all ten spin-labelled cases, both
for the relative sector and for the `k1=0` restriction. It does not map the
stored roots to all response invariants, and explicitly records that the
nonzero-`n0` physical product calibration is pending. Those two statements
must remain visible together.

To finish that comparison, choose the same physical rotation operators,
identify complete program roots through their response invariants, and
check that their products and gauge reductions reproduce the independent
physical stacking law. The response dictionary alone does not provide
these root-level maps.
