# 2+1D E8 and IQH coefficient dictionary

Date: 2026-10-15 UTC. This physical-calibration review track changed no production code or supplied bundle.

State notation: **E8 first**, `(e_0,n_0,n_2,nu_3)`, with `p=d-2=0`. The two uniform invertible coefficients are ordered `(e_0,n_0)`.

Ning, Mao, Li and Wang supply the following charge-conserving coefficient control: the neutral E8 state has `(c,sigma_H)=(8,0)` and the electronic IQH state has `(1,1)`, so the symmetry-free charge-conserving invertible coefficient lattice is detected by `(e_0,n_0)=((c-sigma_H)/8,sigma_H)`. This fixes independent E8 and IQH responses; it is not a new classification of all wallpaper groups with those coefficients.

The primary source is Shang-Qiang Ning, Bin-Bin Mao, Zhengqiao Li and Chenjie Wang, *Anomaly indicators and bulk-boundary correspondences for 3D interacting topological crystalline phases with mirror and continuous symmetries*, arXiv:2105.02682v1, Sec. III.B.1, roots (i)–(ii); *Phys. Rev. B* 104, 075111 (2021), DOI 10.1103/PhysRevB.104.075111. Its dimensional-reduction construction explicitly uses these strictly 2D invertible phases. [Primary full text](https://arxiv.org/abs/2105.02682v1)

The source locations are lines 494–502 of `sources/NMLW_2105.02682v1.tex`; metadata and SHA-256 are in `source_manifest.json`. The machine-readable source dictionary is `coefficient_2p1_reference.json`. It is a source-defined coefficient dictionary, not a new solver result or a completeness proof for wallpaper groups.

For other dimensions see [the 3+1D mirror control](mirror_3p1.md) and [the 4+1D lens calibration](eta_dictionary.md).
