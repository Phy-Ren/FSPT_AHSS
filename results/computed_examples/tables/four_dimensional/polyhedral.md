# 4+1D: Tetrahedral and octahedral groups

11 distinct computed symmetry backgrounds. Every background appears in exactly one family table.

[All families](../internal_4d.md) · [Background definitions](../../FOUR_DIMENSIONAL_BACKGROUNDS.md) · [CSV](polyhedral.csv)

Each heading specifies the bosonic quotient and its order. The full fermionic symmetry has twice that order; the final column is the stacking group of phases.
The layer columns are final filtration quotients in the order p+ip, Majorana, complex fermion and bosonic.
Historical names and section choices are attached to each background in the [coverage ledger](../../COVERAGE_4D.json).

## $G_b=A_4$, order 12

| Background | $s_1$ | $\omega_2$ | Extension | p+ip | Majorana | CF | Bosonic | Stacking group |
|---|---|---|---|---|---|---|---|---|
| [A4_orbit_000](../../inputs/d4_A4_w0_s0.json) | $0$ | $0$ | split | $\mathbb Z_{3}$ | $0$ | $0$ | $\mathbb Z_{3}$ | $\mathbb Z_{9}$ |
| [A4_orbit_001](../../inputs/d4_A4_orbit_001.json) | $0$ | $\omega_{\rm tet}$ | nonsplit | $\mathbb Z_{3}$ | $\mathbb Z_{2}$ | $0$ | $\mathbb Z_{6}$ | $\mathbb Z_{2}\times\mathbb Z_{18}$ |

## $G_b=S_4$, order 24

| Background | $s_1$ | $\omega_2$ | Extension | p+ip | Majorana | CF | Bosonic | Stacking group |
|---|---|---|---|---|---|---|---|---|
| [S4_orbit_000](../../inputs/d4_S4_orbit_000.json) | $0$ | $0$ | split | $0$ | $0$ | $0$ | $0$ | $0$ |
| [S4_orbit_001](../../inputs/d4_S4_orbit_001.json) | $0$ | $\omega_{10}$ | nonsplit | $\mathbb Z_{2}$ | $\mathbb Z_{2}$ | $\mathbb Z_{2}^{2}$ | $\mathbb Z_{2}$ | $\mathbb Z_{2}\times\mathbb Z_{16}$ |
| [S4_orbit_002](../../inputs/d4_S4_orbit_002.json) | $0$ | $\omega_{11}$ | nonsplit | $0$ | $\mathbb Z_{2}^{2}$ | $0$ | $\mathbb Z_{2}^{3}$ | $\mathbb Z_{2}^{3}\times\mathbb Z_{4}$ |
| [S4_orbit_003](../../inputs/d4_S4_orbit_003.json) | $0$ | $\omega_{01}$ | nonsplit | $0$ | $\mathbb Z_{2}$ | $0$ | $\mathbb Z_{2}^{2}$ | $\mathbb Z_{2}\times\mathbb Z_{4}$ |
| [S4_orbit_004](../../inputs/d4_S4_orbit_004.json) | $x$ | $0$ | split | $\mathbb Z_{3}$ | $0$ | $0$ | $\mathbb Z_{3}$ | $\mathbb Z_{9}$ |
| [S4_orbit_005](../../inputs/d4_S4_orbit_005.json) | $x$ | $\omega_{10}$ | nonsplit | $\mathbb Z_{3}$ | $0$ | $0$ | $\mathbb Z_{6}$ | $\mathbb Z_{18}$ |
| [S4_orbit_006](../../inputs/d4_S4_orbit_006.json) | $x$ | $\omega_{11}$ | nonsplit | $\mathbb Z_{3}$ | $\mathbb Z_{2}$ | $0$ | $\mathbb Z_{3}$ | $\mathbb Z_{18}$ |
| [S4_orbit_007](../../inputs/d4_S4_orbit_007.json) | $x$ | $\omega_{01}$ | nonsplit | $\mathbb Z_{3}$ | $0$ | $0$ | $\mathbb Z_{6}$ | $\mathbb Z_{18}$ |

## $G_b=\mathrm{SL}(2,\mathbb F_3)$, order 24

| Background | $s_1$ | $\omega_2$ | Extension | p+ip | Majorana | CF | Bosonic | Stacking group |
|---|---|---|---|---|---|---|---|---|
| [SL23_orbit_000](../../inputs/d4_SL23_w0_s0.json) | $0$ | $0$ | split | $\mathbb Z_{3}$ | $\mathbb Z_{2}$ | $\mathbb Z_{2}$ | $\mathbb Z_{3}$ | $\mathbb Z_{2}\times\mathbb Z_{18}$ |
