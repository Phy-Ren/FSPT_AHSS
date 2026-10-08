# 4+1D cochain and geometric controls

These tests retain a chosen decoration, explicit cochain values, detector
cycles or geometric periods. They are not extra symmetry-classification rows.
Their associated finite backgrounds already appear in the
[classification tables](tables/internal_4d.md), where applicable.

| Control | Scope | Saved evidence |
|---|---|---|
| $G_b=Q_8$, split unitary symmetry | Tests the final p+ip $d_3$ class for each nonzero character and its legal Majorana lifts. | [Detector cycles](../finite_examples/calibrations/q8_d3_detectors.json) |
| $G_b=\mathbb Z_2^2$, $s_1=x$, $\omega_2=x^2+xy+y^2$ | Tests the normalized terminal obstruction and a separate cocycle detector on the Euler input. | [Cochains and pairings](../finite_examples/calibrations/v4_euler.json) |
| $G_b=D_4$ of order eight, $s_1=0$, $\omega_2=y^2$ | Tests the final p+ip $d_4$ class against six cycles after legal lower adjustments. Here $y(t)=1$ is the reflection character. | [Detector pairings](../finite_examples/calibrations/d8_reflection_square_d4.json) |
| $G_f=\mathbb Z_4^f$, unitary | Checks the complete local representatives and the phase change to the current formulas. | [Current cochains](../calibrations/Z4f_current_cochains.md); [earlier coordinate](../finite_examples/calibrations/c2_exact_phase.json) |
| Spin-c decoration on $T^2\times\mathbb {CP}^2$ | Tests the signed six-simplex period and gravitational normalization. | [Geometric certificate](../finite_examples/calibrations/spinc_t2_cp2.json) |

A nonzero obstruction cochain can still be exact. Only a nontrivial final
class after the allowed lower adjustments obstructs a decoration. The
[certificate conventions](../finite_examples/calibrations/README.md)
specify the cochain indexing, coefficient denominators and the scope of each
saved check. Historical witnesses remain in their recorded phase coordinate.
The dihedral certificate calls the reflection character $x$; it is $y$ in
the common rotation/reflection convention used here. The certificate itself
is preserved unchanged.
