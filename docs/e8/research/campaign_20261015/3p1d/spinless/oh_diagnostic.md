# Spinless Oh: saved-root diagnostic

Date: 2026-10-15 UTC. This note audits the immutable 2026-10-13 CI result
while the fresh campaign runs. It does not replace that rerun or identify an
unproved physical relation.

The saved CI group is $\mathbb Z_4\oplus\mathbb Z_2^4$. The selected 3+1D
neutral section contributes an independently calculated $H^1(O_h,\mathbb
Z_s)=\mathbb Z_2$, so its extension is
$\mathbb Z_4\oplus\mathbb Z_2^5$. Debray's pinned v3 states the **full**
interacting group $\mathbb Z_4\oplus\mathbb Z_2^4$. The discrepancy is a
factor of two after aligning sectors. Equality of the old CI answer with
the full source answer was not a valid sector comparison.

## Exact filtration and roots

The saved classification and its independent
[native-equation/restriction audit](../../../../../../results/audits/Oh_spinless_saved_witnesses.json)
give:

| Data | Before obstruction/incoming quotient | Surviving data |
|---|---|---|
| CI sheet $n_1$ | $H^1(O_h,\mathbb Z_s)=\mathbb Z_2$ | Zero: its integer `d3` class is nonzero, coordinates `(0,0,0,1)` in the audit basis |
| Charge $n_3$ | Three order-two cohomology generators | One order-two charge quotient; the saved `d2` map has rank two over $\mathbb F_2$ |
| Phase $\nu_4$ | Six order-two generators | Five order-two phase generators after one incoming charge-gauge relation |
| Independent neutral $e_1$ | $H^1(O_h,\mathbb Z_s)=\mathbb Z_2$ | One order-two root in the selected neutral section |

The phase and charge rows are filtration pieces, not a direct-product
stacking answer. In the saved nine-generator presentation name the six
phase roots $p_1,\ldots,p_6$ and the three completed charge lifts
$c_1,c_2,c_3$. The relations are exactly

\[
2p_i=0,\quad c_1=0,\quad
c_2-c_3=p_2+p_4,\quad
2c_2=p_4+p_5+p_6,\quad
p_1+p_2+p_4+p_5+p_6=0.
\]

Signs in the last two expressions are immaterial because the $p_i$ have
order two. The last relation is the actual incoming charge-gauge image
`(1,1,0,1,1,1)`, recomputed independently from its cochain gauge, not a
discarded raw cohomology generator. There is no closed incoming CI
parameter here; $H^0(O_h,\mathbb Z_s)=0$.

Set $q=c_2$. Eliminating $c_1,c_3,p_1,p_6$ gives the explicit basis

\[
q\;(\mathrm{order}\ 4),\qquad
p_2,p_3,p_4,p_5\;(\mathrm{order}\ 2),
\]

with $p_6=2q+p_4+p_5$, $p_1=p_2+2q$, and
$c_3=q-p_2-p_4$. In particular, the order-four extension is supported by
the nonzero square of a **completed** charge root. It cannot be inferred
by multiplying the graded layer orders alone. Independent Smith reduction
of the saved matrix gives `(1,1,1,1,2,2,2,2,4)`.

The neutral root can be taken globally as $e_1(g)=s(g)\in\{0,1\}$,
with $n_1=n_3=\nu_4=0$. It obeys the signed crossed-homomorphism equation,
and $2e_1+d_s(1)=0$. Neutral source, twister, and phase gauge vanish in the
[specified 3+1D section](../../../../3p1.md). Thus this root has its own
order-two relation and no mixed presentation relation. The obstructed CI
sheet does not obstruct this neutral root.

## Existing cochain and input checks

The saved-witness audit checked six native phase closures, three native
charge closures, three source closures, and three phase-completion
equations. It recomputed the incoming phase vector above. These are checks
of the selected model, not a physical-spectrum identification.

Its literal subgroup maps preserve both sign characters and the chosen
extension cocycle. The final phase-subgroup restriction ranks are:

| Subgroup | Image rank | Kernel rank |
|---|---:|---:|
| $D_{4h}$ | 5 | 0 |
| $T_h$ | 3 | 2 |
| $O$ | 0 | 5 |
| $T_d$ | 2 | 3 |

All completed charge restrictions pass the target obstruction. In
particular, every surviving phase direction is detected on $D_{4h}$ in
this model. This rules out a phase direction that appears solely from an
inconsistent saved $O_h$ restriction, but does not prove its physical
survival.

The input contains all 48 distinct signed permutation matrices, with 24
proper elements. Its $s=\rho$ equals the determinant character,
`circle_action=0`, and its spinless extension is exactly half the stored
Pin-minus cocycle. Central inversion is element 1, with $s=\rho=1$ and
`omega(1,1)=0`. These checks distinguish this case from $O$, $T_d$, or the
spin-half input. Debray uses the same standard spatial representation of
$S_4\times C_2$; no group-name or physical-spin exchange explains the
discrepancy. An explicit universal cochain-to-bordism root map is still
not supplied by these input checks.

## Full interacting bordism result

[Debray, arXiv:2102.02941v3](https://arxiv.org/abs/2102.02941v3), Table 6
(p.60), is unambiguous. Its `full_octahedral.tex`, lines 583–599, identifies
the spinless Class-A problem with
$\widetilde\Omega^{\mathrm{Spin}^c}_4((BO_h)^{3-V_\lambda})$ and states
$\mathbb Z_4\oplus\mathbb Z_2^4$. Lines 601–710 give an Adams
$\mathcal E(1)$-module calculation and claim no relevant differentials or
hidden extensions. This is interacting bordism under the phase-homology
ansatz, not a free-band result or an E8-removed table.

The journal [PRX 15, 031029 (2025)](https://doi.org/10.1103/PhysRevX.15.031029),
Table II, prints the same full group for this cell.

The [independent Steenrod/Koszul reconstruction](../../../../../../benchmarks/point3_mismatch_audit_20261016/oh_audit.md)
computes $ku_4(X)=\mathbb Z_4\oplus\mathbb Z_2^4$ for
$X=(BO_h)^{3-V_\lambda}$. The low-degree Spin-c splitting additionally
requires $ku_0(X)=\mathbb Z_2$. Thus

$$
\widetilde\Omega_4^{\mathrm{Spin}^c}(X)
\cong ku_4(X)\oplus ku_0(X)
\cong\mathbb Z_4\oplus\mathbb Z_2^5.
$$

The relevant differentials and extensions are resolved, and there is no
degree-five free contribution to the Anderson-dual phase group. This gives
the full E8-inclusive interacting group, agreeing with the current result.
Debray's displayed calculation omits the shifted $ku_0$ contribution.

This determines the group within the crystalline/bordism framework. A
microscopic identification of every cochain generator and a universal map
from the four-data formulas to the physical spectrum remain separate
questions. In particular, the added spectral summand is not automatically
a canonical E8 generator in the coordinates above.

## Immutable evidence

- Saved case: `/home/xingyu/insulator-campaign-download/23f9d9c-point3/point3_32_spinless/result.json`; SHA256 `f687a8fea95ac60111e11a205f6c4e061cea78fca33de1c805043432300a3bde`.
- Saved CI source digest: `46c38566e635bf4e93a7e9e2168efd44f8b5910a068947a371de0c85a06be171`; input digest: `a52500d844681368e71e3317a5b4b1d8865907688e26d4c9a1bd6e7b01ad63dd`.
- Saved native/restriction audit: `results/audits/Oh_spinless_saved_witnesses.json`; SHA256 `7e04d9df94a9197049e8f5886fd346993e0651402b856a8baf64b3b08fc2f397`.
- Explicitly downloaded v3 source archive: SHA256 `0e015df95d1b6fb9ac405446ed4edc7f9e843999c551ed81b15a9126412eb9ad`; `full_octahedral.tex` SHA256 `223b5c061bbae1a16cf60101a709a25fd248be859147b85db1cafaaebb7cfed9`; `tet_oct_icos_generalities.tex` SHA256 `2f53ce2fb93f4c8176062b8c6a44fdb8c7ef5aced1f89e140afe6094d54d71df`.

This audit changed no runtime formula, frozen result, or reference value.
