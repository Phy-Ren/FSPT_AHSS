# Explicit finite internal backgrounds in 3+1D

The [symbolic table](tables/internal_3d_symbolic.csv) lists **72 distinct
backgrounds** from the 78 named finite 3+1D records. The
[JSON version](tables/internal_3d_symbolic.json) retains the exact selected
input, all aliases, final filtration and stacking group, and the section
change to each short cocycle below. The [unique example index](unique_examples.json)
provides the explicit group and section maps identifying equivalent saved
backgrounds, including automorphism-related gradings. One row is the
hand-calculated $\mathbb Z_4^{f,T}$ example; the other 71 are additional
backgrounds. Different literal arrays or historical names do not create new rows.

The notation specifies the bosonic quotient $G_b$, its antiunitary character
$s_1$, and the central fermion-parity extension $\omega_2$. Group subscripts
refer to group order. Each row's generator ordering is part of its input.
The layer columns are final filtration quotients, ordered p+ip, Majorana,
complex fermion, bosonic; their direct product need not equal the stacking
group.

## Abelian backgrounds

For $G_b=\prod_i\mathbb Z_{m_i}$ write $g=(u_i)$ and $h=(v_i)$, with
$0\leq u_i,v_i<m_i$. Define the cyclic carry and, when $m_i$ is even,
the binary character by

$$
\eta_i(g,h)=\left\lfloor\frac{u_i+v_i}{m_i}\right\rfloor\pmod2,
\qquad x_i(g)=u_i\pmod2.
$$

For two factors the table writes $x,y$; for a single even cyclic factor it
writes $x$. For $m_i=2$, $\eta_i=x_i^2$. The table's displayed representative is

$$
\omega_2(g,h)=\sum_i\epsilon_i\eta_i(g,h)
 +\sum_{i<j}\kappa_{ij}x_j(g)x_i(h).
$$

Here $R_i^{m_i}=f^{\epsilon_i}$ and
$R_jR_i=f^{\kappa_{ij}}R_iR_j$ for lifts of the specified generators,
with $f$ central and $f^2=1$. Each nonzero term is printed in the CSV;
the JSON also retains all bits. For the odd cyclic control $\mathbb Z_3$,
the grading and extension are both zero.

## Dihedral, quaternion, semidihedral and modular backgrounds

Use the following presentation and coordinates:

$$
G_b=\langle r,t\mid r^m=1,\ t^2=r^k,\ trt^{-1}=r^a\rangle,
\qquad g=r^it^j,\quad 0\leq i<m,\quad j\in\{0,1\}.
$$

| $G_b$ | $m$ | $k$ | $a$ |
|---|---:|---:|---:|
| $D_8$ | 4 | 0 | -1 |
| $D_{16}$ | 8 | 0 | -1 |
| $Q_8$ | 4 | 2 | -1 |
| $Q_{16}$ | 8 | 4 | -1 |
| $M_{16}$ | 8 | 0 | 5 |
| $\mathrm{SD}_{16}$ | 8 | 0 | 3 |

The characters are $x(r^it^j)=i\bmod2$ and $y(r^it^j)=j$.
The three binary extension labels in $\omega_{\alpha\beta\gamma}$ mean

$$
R^m=f^\alpha,\qquad T^2=R^kf^\beta,\qquad
TRT^{-1}=R^af^\gamma,\qquad f^2=1,
$$

with $f$ central. They define the explicit normalized cocycle, for
$h=r^{i'}t^{j'}$,

$$
\omega_{\alpha\beta\gamma}(g,h)
=\alpha\left\lfloor\frac{i+a^ji'+kjj'}{m}\right\rfloor
 +\beta jj'+\gamma ji'\pmod2.
$$

The zero triple is printed as $0$. In particular $\omega_{010}=y^2$
and $\omega_{001}=y\cup x$. Negative numerators use the ordinary floor,
so the formula applies with $a=-1$. The table uses only triples obtained
from the accepted central extensions; no arbitrary triple is asserted to
define a consistent extension for every presentation.

## Other quotient groups

For the tetrahedral group, $\omega_{\mathrm{tet}}$ denotes the binary
tetrahedral extension

$$
1\longrightarrow\mathbb Z_2^f\longrightarrow
\mathrm{SL}(2,\mathbb F_3)\longrightarrow A_4\longrightarrow1.
$$

The stored generators satisfy $r^3=t^3=(rt)^2=1$ in $A_4$; their lifts
satisfy $R^3=T^3=1$ and $(RT)^2=f$ in the nontrivial extension.
The separate $G_b=\mathrm{SL}(2,\mathbb F_3)$ control has $s_1=\omega_2=0$.

The order-32 quotient $G_{32}$ in the table is

$$
G_{32}=\langle r,t\mid r^8=1,\ t^4=r^4,\ trt^{-1}=r^3\rangle.
$$

Its two rows have $\omega_2=0$ and $s_1=x$ or $y$, where $x(r)=1,x(t)=0$
and $y(r)=0,y(t)=1$.

The central product $\mathbb Z_8\circ Q_8$ has order 32 and presentation

$$
\langle r,u,v\mid r\text{ central},\ r^8=1,\
u^2=v^2=r^4,\ vu=r^4uv\rangle.
$$

Here $\omega_2=0$ and $s_1(r)=1$, $s_1(u)=s_1(v)=0$.

## Exact representative checks

The displayed short cocycles use sections built from ordered powers of the
listed generator lifts. The saved numerical input uses its original section.
For every abelian or two-generator metacyclic row the JSON supplies a binary
one-cochain $\lambda$ and checks, for every ordered pair,

$$
\omega_{\mathrm{display}}(g,h)=\omega_{\mathrm{saved}}(g,h)
 +\lambda(g)+\lambda(h)+\lambda(gh)\pmod2.
$$

The generator verifies 14,549 pair identities in total, all generator orders
and defining relations used above, and the binary gradings. This is a
translation of saved exact backgrounds, not a new classification calculation.
No original numerical result or literal input is changed. Rebuild or verify:

```sh
python3 results/computed_examples/rebuild_symbolic_3d.py
python3 results/computed_examples/rebuild_symbolic_3d.py --check
```
