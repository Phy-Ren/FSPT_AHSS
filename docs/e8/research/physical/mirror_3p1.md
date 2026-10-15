# 3+1D interacting mirror E8 control

Date: 2026-10-15 UTC. This physical-calibration review track changed no production code or supplied bundle.

State notation: **E8 first**, `(e_1,n_1,n_3,nu_4)`, with `p=d-2=1`.


For **physical 3+1D unitary mirror symmetry commuting with `U(1)^f`**, Ning, Mao, Li and Wang derive an interacting classification by dimensional reduction and adjoining operations. The mirror-plane symmetry is `U(1)^f x Z2`; fermion parity is `exp(i pi Q)`. Both choices `M^2=1` and `M^2=(-1)^F` describe the same group after charge rephasing, as their Sec. II.C states. This is a charge-conserving mirror insulator control, not an arbitrary assignment of antiunitary or Pin data. [Ning–Mao–Li–Wang, arXiv:2105.02682v1, Secs. II.C and III.B.1; *Phys. Rev. B* 104, 075111 (2021)](https://arxiv.org/abs/2105.02682v1)

Use the source's root coordinates in E8-first order: `mu_1` counts neutral E8 layers, `mu_2` counts electronic IQH layers, and `mu_3` counts the nonchiral order-four root. These are source root multiplicities, not an assertion that `mu_3` equals the AHSS cochain `n_3`. The source gives

\[
 c=8\mu_1+\mu_2,\qquad\sigma_H=\mu_2,
 \quad\eta_{2f}=(-1)^{\mu_1},\qquad
 \eta_{1f}=\exp\left[\frac{i\pi}{4}(\mu_2-2\mu_3)\right].
\]

Adjoining imposes `2 E8=0` and `2 IQH=-nonchiral`, while the nonchiral root has order four. The two detectors distinguish all 16 elements of `Z2 x Z8`; in particular the neutral E8 root has `(eta_2f,eta_1f)=(-1,+1)`. This identifies a physical neutral generator, rather than deleting an arbitrary factor of two from a group order. The exact script checks the source's relations and distinct detector pairs. It does not claim to have computed these surface observables from the new cochain implementation.

The executable source-relation checks are in `lens_calibration.py`, with a separate dimension-pinned output `mirror_3p1_checks.json`. Source bytes, metadata and exact locations are pinned in `source_manifest.json` (NMLW source lines 290–300 and 489–538).

This control does not establish the classification for arbitrary infinite space groups. For other dimensions see [the 4+1D lens calibration](eta_dictionary.md) and [the 2+1D coefficient dictionary](coefficient_2p1.md).
