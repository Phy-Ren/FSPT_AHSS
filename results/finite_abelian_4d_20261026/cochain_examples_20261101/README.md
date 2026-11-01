# Explicit cochains for cyclic and two-factor examples

These calculations complement the complete group and layer formulas in the parent directory.
They evaluate the obstruction functions and stacking twisters on explicit normalized cochains.
The two mixed examples use no terminal p+ip phase.
All phases below are additive elements of `R/Z`; products are cup products.

## Cyclic generators

For `G_b = Z_(N1) x Z_(N2)`, choose coordinates `0 <= a_i < N_i` and use

```math
\begin{aligned}
m_1(a)&=a_1,&m_2(a,b)&=\left\lfloor\frac{a_1+b_1}{N_1}\right\rfloor,\\
m_1'(a)&=a_2,&m_2'(a,b)&=\left\lfloor\frac{a_2+b_2}{N_2}\right\rfloor.
\end{aligned}
```

A prime denotes the second cyclic factor, not a second state being stacked.
The subscript is the cochain degree.
Their integer differentials are `dm1=N1 m2`, `dm1'=N2 m2'`, and `dm2=dm2'=0`.
Both carry cocycles take values zero or one.
The carry identity gives `Sq1[m2]_2=Sq1[m2']_2=0` pointwise.

## Split mixed complex-fermion phase

For `G_f = Z2f x Z_(N1) x Z_(N2)`, define the rational lifts

```math
C_5^{(1)}=\frac{m_1m_2m_2'}{N_1},\qquad
C_5^{(2)}=\frac{m_2m_1'm_2'}{N_2}.
```

Their derivatives are `m2^2 m2'` and `m2 (m2')^2`.
An explicit solution is

```math
n_2=n_3=0,\qquad n_4=[m_2m_2']_2,\qquad
\nu_5=\frac12\left[C_5^{(1)}+C_5^{(2)}
+\zeta_{2,2}([m_2]_2,[m_2']_2)\right]\mod1.
```

The fractions displayed for `C5` are taken before division by two.
The Cartan identity verifies `d nu5 = O6^c` pointwise.
Its correction becomes integral on doubling, while the diagonal complex-fermion twister is a `U(1)` coboundary.
The complete phase therefore obeys `2g_c=C5^(1)+C5^(2)` in the surviving bosonic quotient.
The candidate is incoming-trivial at `(N1,N2)=(2,2)`.

`check_split_pair_cochains.py` tests the Cartan identity, the carry identity, and the rational phase equation.
It exhausts all 4,096 six-simplices of `Z2 x Z2` with the first vertex fixed, and uses 1,000 reproducible random simplices for each of seven further pairs.
The universal Cartan and carry identities establish the arbitrary-order statement; these finite tests replay their explicit cochain convention.

For the exceptional incoming Majorana calculation on `Z2 x Z4`, use

```math
C_2=[m_1m_1']_2,\qquad
B_3=\left[m_1^2\left\lfloor\frac{m_1'}2\right\rfloor
+m_1(m_1'\cup_1m_1)m_1'\right]_2,\qquad dB_3=C_2^2.
```

`check_split_pair_secondary.py` checks this trivialization on all 4,096 four-simplices.
It constructs the two mixed degree-five bar cycles by signed shuffles of the cyclic-resolution chains, checks their boundaries, and evaluates the secondary obstruction.
Its two periods agree with those of `C5^(1)`, proving the incoming identification used in the pair calculation.
The obstruction uses the Cartan--Adem coordinate in `fspt.formulas.obstruction`; the coboundary relating it to the physical coordinate leaves these periods unchanged.

## The additional Majorana phase of Z4f x Z2

Here `G_b=Z2 x Z2`, `omega2=m1^2`, and both degree-one cochains are binary.
The additional Majorana root has

```math
n_2=n_4=0,\qquad n_3=m_1^2m_1',\qquad
\nu_5=\frac14m_1^3(m_1')^2+\frac38m_1(m_1')^4.
```

The canonical Majorana obstruction is

```math
\mathcal O_6^\gamma=\frac12m_1^4(m_1')^2
+\frac34m_1^2(m_1')^4=d\nu_5\mod1.
```

Self-stacking gives `E4^gamma=m1^2(m1')^2` and `E5^gamma=m1^4 m1'/2`.
Consequently,

```math
2\nu_5+\mathcal E_5^\gamma
=\frac34m_1(m_1')^4+d\left[\frac14m_1^3m_1'\right]\mod1.
```

After dropping this coboundary, two copies give the complex-fermion root with `n4=m1^2(m1')^2` and phase `3m1(m1')^4/4`.
Its self-stacking twister vanishes pointwise.
Four copies give the surviving bosonic root `m1(m1')^4/2`, and eight copies are trivial.
Together with the independent cyclic `Z16` contribution, this gives the full stacking group `Z16 x Z8`.
The surviving layer quotients and nontriviality of the bosonic root are given by the parent package's layer calculation.
`verify_abelian_z4f_z2.py` exhaustively checks the displayed obstruction equations, coboundary, and doubling chain using the published closed-Majorana formulas.

## General commuting power extensions

[POWER_EXTENSIONS.md](POWER_EXTENSIONS.md) gives the cyclic and mixed complex-fermion primitives for `G_f=Z_(2M)^f x Z_N`, including the necessary Cartan corrections.
It also documents an exact audit of every bosonic change to the integer-root power relations in six small nonsplit two-primary cases.
Together with prime decomposition, these cases establish abstract terminal-phase independence for arbitrary odd factors coprime to three when the two-primary quotient orders are at most four.
The nontrivial power extension is required for this statement; split fermion parity has different cyclic extensions.
The saved power-extension reports contain the pointwise checks, transported bosonic subgroups, and compact-formula comparisons.

## Run

From the repository root:

```sh
python results/finite_abelian_4d_20261026/cochain_examples_20261101/check_split_pair_cochains.py
python results/finite_abelian_4d_20261026/cochain_examples_20261101/check_split_pair_secondary.py
python results/finite_abelian_4d_20261026/cochain_examples_20261101/verify_abelian_z4f_z2.py
python results/finite_abelian_4d_20261026/cochain_examples_20261101/check_split_lowrank_groups.py
python results/finite_abelian_4d_20261026/cochain_examples_20261101/check_power_extension_cochains.py
python results/finite_abelian_4d_20261026/cochain_examples_20261101/check_power_extension_terminal.py
python results/finite_abelian_4d_20261026/cochain_examples_20261101/check_power_extension_formulas.py
```

The cochain commands discover this checkout automatically and accept `--formula-repo /path/to/FSPT_AHSS` to use another checkout.
They require only the Python standard library and this repository's formula implementation.
The formula-comparison commands and the terminal-extension audit use the parent package's exact-arithmetic dependencies.
The split comparison checks 500 cyclic orders and 820 pairs against the retained prime-power formulas.
The power-extension comparison checks 3200 layer results and 1458 group results.
That comparison checks assembly of the known groups and layers; it does not rerun the full AHSS.
`verification_report.json` records the actual checks and hashes the scripts and formula implementation used for the run.
`power_extension_report.json` records the added power-extension checks and their implementation hashes.
