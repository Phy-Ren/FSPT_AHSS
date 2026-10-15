# Physical meaning of the optional intrinsic coefficient in 4+1D

Date: 2026-10-15 UTC. This note is saved separately at the user's request. Work on this optional enlargement is suspended while the original four-coordinate theory $(e_2,n_2,n_4,\nu_5)$ is completed. Nothing here changes that theory or the runtime.

The extra $r_0=(r_0^I,r_0^J)$ would specify **uniform intrinsic 4+1D invertible phases**. Degree zero means that the coefficient is constant over connected group-cochain data. It does not mean a zero-dimensional physical phase. These responses are present already for $G=1$, where all four positive-degree decoration fields vanish.

For a Spin-c determinant class $c$, put $a=c/2$, the physical charge-one curvature class. The integral response basis is

$$I=a^3/6-a p_1/24,\qquad J=4a^3.$$

Its rank-two interacting coefficient group and primitive integral normalization are established in [intrinsic_response.md](intrinsic_response.md), using the interacting column of Freed–Hopkins rather than the fixed-charge-one free-band column.

A charge-$q$ complex fermion in a 4+1D Chern-insulator band has index polynomial

$$I_q=q^3a^3/6-q a p_1/24
=qI+\frac{q^3-q}{24}J\qquad(q\text{ odd}).$$

In particular,

$$I_3-3I_1=J.$$

At an oriented 3+1D boundary this combination has Weyl-anomaly coefficients $(\sum q^3,\sum q)=(27-3,3-3)=(24,0)$. This identifies an independent pure cubic charge response. It does not assert a second generator in a free-band problem whose elementary fermions all have fixed charge one.

There is an explicit local electron realization of the charge-three ingredient. For each effective orbital, take three microscopic charge-one fermion orbitals, with number operators $n_1,n_2,n_3$, and define

$$P=(1-n_1)(1-n_2)(1-n_3)+n_1n_2n_3,
\qquad f^\dagger=c_1^\dagger c_2^\dagger c_3^\dagger.$$

Add a large positive energy $\Delta(1-P)$. The retained local subspace is exactly $\{|000\rangle,|111\rangle\}$. On it, $f,f^\dagger$ obey the canonical fermion algebra and carry charge three. On distinct orbitals these composites anticommute because they contain an odd number of microscopic fermion operators.

Choose a finite-range four-dimensional Chern-insulator hopping matrix $t_{ij}$ with occupied-band second Chern number one, and use

$$H=\Delta\sum_i(1-P_i)+\sum_{ij}t_{ij}f_i^\dagger f_j.$$

The hopping term is a local charge-conserving six-fermion electron interaction. It preserves the constrained subspace; a sufficiently large $\Delta$ keeps all excluded local sectors gapped. Within that subspace the model is precisely the charge-three Chern insulator. The composites are local operators, with no emergent gauge constraint or fractionalization. Stacking this model with three inverse ordinary charge-one Chern insulators realizes the response $J$.

This is a constructive argument for the intrinsic $G=1$ coefficient. It does not assert that the same construction respects an arbitrary additional projective or antiunitary symmetry; extending it to such a symmetry is the separate equivariance problem. It also does not impose an externally fixed particle density. The construction is included to explain the physical meaning of the response basis, not to enlarge the current four-coordinate implementation.
