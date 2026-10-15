# Cochain operations

Use the [formula guide](../FORMULA_GUIDE.md) for symmetry data and the
E8-first physical fields. This page defines reusable operations; a generic
`x_p` or `y_q` is not a new physical decoration.

## Differential and coefficient transport

For a normalized inhomogeneous cochain `f_p` of sign `chi`,

```math
\begin{aligned}
(d_\chi f)(g_1,\ldots,g_{p+1})={}&
(-1)^{\chi(g_1)}f(g_2,\ldots,g_{p+1})\\
&+\sum_{j=1}^{p}(-1)^j f(g_1,\ldots,g_jg_{j+1},\ldots,g_{p+1})
 +(-1)^{p+1}f(g_1,\ldots,g_p).
\end{aligned}
```

The sign of a product is the sum of input signs. Transport each factor
from its own first vertex using its own local system. A normalized input
vanishes on a face with repeated vertices. A differential formed after
pullback is evaluated on the full product simplex before applying any
degeneracy simplification.

## Interval cuts and higher cups

For a word `w` of length `L` on `k` labels and input degrees `q_j`, put
`D=sum(q_j)-L+k`. On an ordered `D`-simplex sum over cuts
`0=i_0<=...<=i_L=D`. The interval `(i_(l-1),...,i_l)` is assigned to input
`w_l`; concatenate each input's intervals in order. Keep a cut only when
input `j` receives exactly `q_j+1` distinct increasing vertices. The binary
May–Steenrod word operation is the sum of these face products modulo two.

For `cup_i`, use the alternating two-label word of length `i+2`, starting
with label 1. An interval is inner when its label occurs again later.
Set `lambda_l=i_l-i_(l-1)+1` for inner intervals and
`lambda_l=i_l-i_(l-1)` otherwise. For degrees `p,q`, the integral sign is

```math
(-1)^{i(p+q)+\binom i2+
\sum_{l\ {m inner}}i_l+
\sum_{l<m,\ w_l>w_m}\lambda_l\lambda_m}.
```

Apply the input coefficient transports after this sign. In particular,
`(x2 cup_1 y2)(0123)=x2(023)y2(012)-x2(013)y2(123)` for trivial signs.
Negative or degree-impossible cups vanish. The identity is

```math
\begin{aligned}
d(x_p\cup_i y_q)={}&dx_p\cup_i y_q+(-1)^p x_p\cup_i dy_q\\
&+(-1)^{p+q-i}x_p\cup_{i-1}y_q
 +(-1)^{pq+p+q}y_q\cup_{i-1}x_p.
\end{aligned}
```

Every differential has its argument's coefficient system. The open square is

```math
\mathrm{Sq}^{j}x_p=x_p\cup_{p-j}x_p+x_p\cup_{p-j+1}dx_p.
```

The derivative term remains present when a sheet opens the charge equation.

## Charge source, twister, and gauge

For integer `z_k` of sign `rho`, define

```math
\widehat O^c_{k+2}(z)=\omega_R\cup z+\frac12\mathrm{Sq}^2\bar z,
```

```math
\widehat E^c_{k+1}(z,z')=\frac12
 [\bar z\cup_{k-1}\bar z'+d\bar z\cup_k\bar z'],
```

```math
\widehat G^c_{k+1}(u;z)=\omega_R\cup u+
 \frac12\mathrm{Sq}^2\bar u+\widehat E^c_{k+1}(z,d_\rho u).
```

Their outputs have phase sign `s`. On closed charge, the class of `O^c`
represents `d2`. Closed gauge parameters can produce nonzero incoming
phases; they are included in the global quotient.

For a closed pure charge in 3+1D (`n1=0`, `d_rho n3=0`) and no sheet
gauge, the canonical source-cylinder representative obeys the exact
identity

```math
G^{\rm cylinder}_4(v_2;n_3)=\widehat G^c_4(v_2;n_3)
 +d_s\left[\frac12\bar n_3\cup_2\bar v_2\right]\pmod1.
```

This holds for arbitrary `v2`, including closed incoming parameters,
and independent signs and extension backgrounds. The prism square gives
`Sq2(v)+n cup_1 v+v cup_1 n`; the higher-cup identity compares this with
`Sq2(v)+n cup_2 dv` in the short gauge. The extension term integrates to
`omega_R cup v`. The closed-charge hypothesis is essential to this
particular formula; it is not an open-charge or nonzero-sheet shortcut.

For a real two-cochain `x` of sign `chi` with integral differential,

```math
\mathcal P_\chi(x)=x\cup x+x\cup_1d_\chi x.
```

This is a real cochain with ordinary coefficients, with the stated lift
retained. It is not an unspecified Pontryagin-square representative.

## Cartan operations and integer carries

The native binary words on `(x_p,x_p,y_q,y_q)` are fixed as follows.

| Operation | Word |
| --- | --- |
| `zeta_(2,1)` | `123134` |
| `zeta_(1,3)` | `1231434` |
| `zeta_(1,4)` | `12314343` |
| `zeta_(2,2)` | `1231343` |
| `zeta_(2,3)` | `12313434` |

The two reversed words used here are

```math
\begin{aligned}
\zeta_{3,1}(x,y)={}&\zeta_{1,3}(y,x)+\mathrm{Sq}^2(x\cup_1y)
 +(yx)\cup_3d(x\cup_1y)\\
&+(\mathrm{Sq}^1y)\cup_1(\mathrm{Sq}^1x)+y\cup_1\mathrm{Sq}^2x,\\
\zeta_{3,2}(x,y)={}&\zeta_{2,3}(y,x)+\mathrm{Sq}^2(y\cup_1x)
 +(xy)\cup_4d(y\cup_1x)\\
&+x\cup_1\mathrm{Sq}^2y+y\cup_1\mathrm{Sq}^2x
 +(\mathrm{Sq}^1x)\cup_1(\mathrm{Sq}^1y).
\end{aligned}
```

For integral cocycles `x_p` and `y_q` of signs `chi,psi`, and only the
degree pairs `(3,1),(3,2),(2,2)`, define the binary operation

```math
\zeta^{\mathbb Z}_{p,q}(x,y)=\zeta_{p,q}(\bar x,\bar y)
 +\widetilde x\,\mathrm{Sq}^1\bar y
 +(\chi\bar x)\widetilde y
 +\chi(\bar x\cup_1\psi)\bar y.
```

It has degree `p+q+1`. The tilde is the second digit of the actual signed
integer input. In particular, form an integer cup square before taking
its second digit. Its differential is

```math
d\zeta^{\mathbb Z}_{p,q}(x,y)=
\mathrm{Sq}^2(\bar x\bar y)+(\mathrm{Sq}^2\bar x)\bar y
 +\bar x\mathrm{Sq}^2\bar y+(\chi\psi)\bar x\bar y.
```

## Finite parameter-simplex integration

`I_m` is the parameter-first signed shuffle sum on `Delta^m x X`.
On a base `q`-simplex enumerate paths from `(0,0)` to `(m,q)` with unit
steps. The sign is `(-1)^epsilon`, where `epsilon` counts base steps
preceding parameter steps. Pull back every input with its own sign, and
evaluate on each resulting ordered `(m+q)`-simplex.

```math
d\mathcal I_mF=(-1)^m\mathcal I_m dF+
(-1)^{m+1}\sum_{j=0}^{m}(-1)^j
 \mathcal I_{m-1}(F|_{\partial_j\Delta^m}).
```

The dimensional pages specify all parameter fields. An integration symbol
never stands for an unknown primitive chosen by a cohomology solve.

## Paired representative transport

A rephasing `nu -> nu+F` must change the whole source/product/gauge triple:

```math
\widehat O\mapsto\widehat O+d_sF,\qquad
\widehat E\mapsto\widehat E+F(a*b)-F(a)-F(b)+d_sH,
\qquad
\widehat G\mapsto\widehat G+F(a^g)-F(a).
```

Here `a*b` is the actual lower product, including its generated charge.
Integral extension-lift changes use
`omega_R -> omega_R+z2`, `n_(p+2) -> n_(p+2)-z2 cup n_p`;
real section changes use `omega_R -> omega_R+d_(rho+s)alpha1` and leave
charge fixed. The phase is the dimensional source evaluated on the
specified height cylinder. Neutral E8 remains unchanged.
