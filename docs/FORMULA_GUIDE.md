# FSPT obstruction and stacking formulas

This guide specifies the cochains evaluated by `FSPT_AHSS`. The physical input
is a bosonic symmetry group, its fermion-extension cocycle $`\omega_2`$, and its
antiunitary cocycle $`s_1`$. We write every source and stacking correction in one
coordinate convention at a time. An obstruction is a cochain first: a nonzero
value does not imply that a decoration is obstructed. The obstruction must
remain nontrivial in cohomology after the allowed lower-layer adjustments.

The complete integer-layer source and product below apply in $`3+1`$D and
$`4+1`$D. The [lower-dimensional endpoints](formulas/MAJORANA_AND_ENDPOINTS.md)
state separately the implemented $`1+1`$D and $`2+1`$D domains. These are formulas
and evaluation rules, not a claim that every group has been computed.

The organization follows the dependency order of an evaluation:

1. [Conventions and coordinates](#conventions-and-coordinates).
2. [Lower sources](#lower-sources) and [lower stacking](#lower-stacking).
3. [One shared terminal source](#shared-terminal-source).
4. [The $`3+1`$D pair](#three-dimensional-pair) or [the $`4+1`$D pair](#four-dimensional-pair).

Long, fixed operations appear once in the appendices:
[cochain operations](formulas/OPERATIONS.md),
[source operations](formulas/SOURCE_OPERATIONS.md),
[finite terminal transfer](formulas/TERMINAL_TRANSFER.md), and
[all fixed coefficients](formulas/COEFFICIENTS.md).
Every symbol used below is defined there or before its first use here.
The [formula registry](../formulas/FORMULA_REGISTRY.json) maps these equations
to executable sources. [The implementation guide](../formulas/README.md)
describes the API and file layout.

<a id="conventions-and-coordinates"></a>
## Conventions and coordinates

Let $`d`$ denote **spatial** dimension. In this section $`d=3,4`$ and $`p=d-2`$.
A decoration consists of

```math
(n_{d-2},n_{d-1},n_d,\nu_{d+1})
\in C^{d-2}(G_b,\mathbb Z_{s_1})\times
C^{d-1}(G_b,\mathbb Z_2)\times C^d(G_b,\mathbb Z_2)
\times C^{d+1}(G_b,U(1)_{s_1}).
```

The paper's $`\nu_{d+1}`$ is multiplicative. For the formulas below define its
additive phase by $`\nu_{d+1}=\exp(2\pi i\widehat\nu_{d+1})`$, with
$`\widehat\nu_{d+1}\in C^{d+1}(G_b,(\mathbb R/\mathbb Z)_{s_1})`$.
The equations for the first three layers and the additive phase are

```math
d_{s_1}n_{d-2}=0,\qquad dn_{d-1}=O_d,\qquad
dn_d=O_{d+1},\qquad d_{s_1}\widehat\nu_{d+1}=\widehat O_{d+2}.
```

Here $`d_{s_1}`$ is the twisted differential. Ordinary $`d`$ always means the
untwisted differential. Binary arithmetic is over $`\mathbb Z_2`$; a tilde is
the pointwise canonical integer lift after the entire indicated binary
expression has been formed. A phase lies in $`\mathbb R/\mathbb Z`$.

For the formulas, introduce this dictionary **once**:

| Paper field | Abbreviation | Runtime field |
|---|---|---|
| $`n_{d-2}`$ | $`n`$ | `n`, signed integer |
| $`n_{d-1}`$ | $`n_M`$ | `a`, binary, unshifted |
| $`n_d`$ | $`c`$ | `c`, binary |
| $`\omega_2`$ | $`w`$ | `w`, binary cocycle |
| $`s_1`$ | $`s`$ | `s`, binary cocycle |

Set

<a id="eq-c1"></a>

**(C1)**

```math
a=[n]_2,\qquad h=[\lfloor n/2\rfloor]_2,\qquad
W=w+s\cup s,\qquad u=n_M+s\cup h.
```

Thus the temporary letter $`a`$ below is the **parity of the integer layer**;
it is not the runtime field named `a`. A second input uses
$`(m,n'_M,c')`$, with $`b=[m]_2`$, $`k=[\lfloor m/2\rfloor]_2`$,
and $`v=n'_M+s\cup k`$. The API takes unshifted inputs and applies (C1) once.

Juxtaposition means the ordered cup $`\cup_0`$, never a commutative product of
cochains. Throughout the integer-layer formulas, every occurrence of the
canonical lift $`\widetilde W`$ has coefficient type $`\mathbb Z_s`$, whereas
$`\widetilde w`$ has untwisted integer coefficients. This includes the lifts
inside $`\Pi_5`$ and $`\widetilde W(n\cup_1m)`$ in the terminal product. Binary
$`W,w`$ have no sign local system. The coefficient type is part of each
integral cup operation, even though both lifts take values $`0,1`$.
For a degree-$`r`$ binary cochain, closed or open, define

<a id="eq-c2"></a>

**(C2)**

```math
S^j x=x\cup_{r-j}x+x\cup_{r-j+1}dx.
```

Negative cup indices and degree-impossible operations are zero. All binary
brackets multiplying $`1/2`$ are formed before their canonical lift. Integral
and fractional expressions retain the signed cups, local coefficient types,
and exact divisions specified in [Operations](formulas/OPERATIONS.md).
For example, $`\lfloor-1/2\rfloor=-1`$; a negative integer layer is not replaced
by its parity before evaluating carries.

<a id="lower-sources"></a>
## Lower sources

In native coordinates the Majorana source is

<a id="eq-l1"></a>

**(L1)**

```math
dn_M=S^2a+w a+s S^1a.
```

The shifted coordinate makes the two cases short:

| Dimension | $`du`$ | $`dh`$ |
|---|---|---|
| $`3+1`$D ($`p=1`$) | $`Wa`$ | $`a^2+sa`$ |
| $`4+1`$D ($`p=2`$) | $`a^2+Wa`$ | $`a\cup_1a+sa`$ |

The complex-fermion equation is

<a id="eq-l2"></a>

**(L2)**

```math
dc=F_{p+3}(n,u)=S^2u+sS^1u+wu+\Xi_{p+3}(n).
```

In $`3+1`$D,

<a id="eq-l3"></a>

**(L3)**

```math
\begin{aligned}
\Xi_4={}&\zeta_{2,1}(W,a)+(W\cup_1W+sW)h\\
&+\big[(W\cup_1W)\cup_1s+s(s\cup_1W)\big]a,\\
\zeta_{2,1}(W,a)(01234)={}&W(012)W(023)a(23)a(34).
\end{aligned}
```

In $`4+1`$D, put $`b_a=a\cup_1a`$. Then

<a id="eq-l4"></a>

**(L4)**

```math
\begin{aligned}
\Xi_5={}&\zeta_{2,2}(a,a)+\zeta_{2,2}(W,a)
 +a^2\cup_3(Wa)+h\,dh+b_a\cup_1(sa)\\
&+s\big[a^2\cup_4(Wa)+(a\cup_1s)a+a\cup_1b_a+a^2\big]\\
&+(W\cup_1W+sW)h
 +\big[(W\cup_1W)\cup_1s+s(s\cup_1W)\big]a,\\
\zeta_{2,2}(x,y)={}&\mathop{\mathrm{MS}}\nolimits_{1231343}(x,x,y,y).
\end{aligned}
```

$`\mathop{\mathrm{MS}}\nolimits`$ is the finite interval-cut operation defined in
[Operations](formulas/OPERATIONS.md#interval-cuts). No primitive is selected
by solving a cochain equation in (L3) or (L4).

<a id="lower-stacking"></a>
## Lower stacking

For two complete inputs, set

<a id="eq-p1"></a>

**(P1)**

```math
t=a\cup_{p-1}b,\qquad q=a\cup_p b,\qquad
N=n+m,\qquad U=u+v+t.
```

The native Majorana output and the complex-fermion output are

<a id="eq-p2"></a>

**(P2)**

```math
N_M=n_M+n'_M+t+s q=U+s(h+k+q),\qquad
C=c+c'+e_{p+2}.
```

The digit identity $`[\lfloor N/2\rfloor]_2=h+k+q`$ explains the shift in (P2).

### The 3+1D complex-fermion carry

Here $`p=1`$, $`t=ab`$, and $`q=a\cup_1b`$. Define
$`\epsilon(x)=(x^2\cup_1s)x`$ and
$`\Delta\epsilon=\epsilon(a+b)+\epsilon(a)+\epsilon(b)`$. Then

<a id="eq-p3"></a>

**(P3)**

```math
\begin{aligned}
e_3={}&u\cup_1v+du\cup_2v+(u+v)\cup_1t
 +s\big[u\cup_2v+(u+v)\cup_2t\big]\\
&+z^\psi_3(a,b)+[W(a+b)]\cup_2t+(dh)k\\
&+(sa)\cup_1b^2+a s b+q s(a+b)\\
&+s\big[sq+a\cup_1dk+q(a+b)\big]+\Delta\epsilon,\\
z^\psi_3(a,b)={}&\mathop{\mathrm{MS}}\nolimits_{12314}(a,a,b,b)
 =[a\cup_1(ab)]b.
\end{aligned}
```

### The 4+1D complex-fermion carry

Here $`p=2`$, $`t=a\cup_1b`$, $`q=a\cup_2b`$, and $`dt=ab+ba`$:

<a id="eq-p4"></a>

**(P4)**

```math
\begin{aligned}
e_4={}&u\cup_2v+du\cup_3v+(u+v)\cup_2t\\
&+s\big[u\cup_3v+du\cup_4v+(u+v)\cup_3t\big]\\
&+z^\psi_4(a,b)+[W(a+b)]\cup_3t
 +b^2\cup_4(Wa)+dt\cup_4[W(a+b)]\\
&+h(k+b)+ak+dh\cup_1k+(h+k)q\\
&+(sa)\cup_2(b\cup_1b)+a\cup_1(sb)+q\cup_1[s(a+b)]\\
&+s\big[sq+a\cup_2dk+q\cup_1(a+b)+\ell_3(a,b)\big].
\end{aligned}
```

The short operations in the last formula are fully explicit:

<a id="eq-p5"></a>

**(P5)**

```math
\begin{aligned}
z^\psi_4(a,b)={}&\mathop{\mathrm{MS}}\nolimits_{12413423}(a,a,a,b)\\
&+(\mathop{\mathrm{MS}}\nolimits_{12314132}+\mathop{\mathrm{MS}}\nolimits_{12314324}
 +\mathop{\mathrm{MS}}\nolimits_{12341321})(a,a,b,b)\\
&+(\mathop{\mathrm{MS}}\nolimits_{12132413}+\mathop{\mathrm{MS}}\nolimits_{12324214})(a,b,b,b),\\
\ell_3(a,b)(0123)={}&a(023)b(012)[1+a(013)b(123)].
\end{aligned}
```

The digit term $`h(k+b)+ak`$ already incorporates the closed $`ab`$ correction
required by the terminal product. Do not add a second $`ab`$.

<a id="shared-terminal-source"></a>
## Shared terminal source

The following block has inputs of degrees $`(|n|,|u|,|c|)=(2,3,4)`$.
They are the actual fields in $`4+1`$D and explicit virtual fields in the
$`3+1`$D transgression below. Thus this block needs to be specified only once.

Define the background quantities and the integer carry:

<a id="eq-s1"></a>

**(S1)**

```math
\begin{aligned}
v_3&=\frac{d_s\widetilde W}{2},&
\alpha_3&=[v_3]_2,&
h_\omega&=\left[\frac{v_3-\widetilde\alpha_3}{2}\right]_2,\\
\ell^\omega_3&=[\beta w]_2+sw,&
\mathcal P_s(W)&=\widetilde W\,\widetilde W
 +\widetilde W\cup_1d_s\widetilde W,\\
A_4&=a^2+Wa=du,&
j_4&=\frac{d\widetilde u-\widetilde{du}}2,&
K_4&=\frac{\widetilde A_4-n^2-\widetilde W n}{2},\\
B_4&=j_4+K_4=\frac{d\widetilde u-n^2-\widetilde W n}{2},&
dB_4&=-v_3n.
\end{aligned}
```

Using the coefficient types fixed above, $`j_4,K_4,B_4`$ and
$`\mathcal P_s(W)`$ are untwisted integers, while $`n,v_3`$ are twisted integers.
In particular, $`B_4`$ is generally **not closed**. The minus carry
$`h_\omega`$ differs from the plus carry $`\beta^+`$ used elsewhere.

Collect all the repeated binary terms in $`\mathcal H_6`$:

<a id="eq-s2"></a>

**(S2)**

```math
\begin{aligned}
\mathcal C_6={}&\mathop{\mathrm{MS}}\nolimits_{12132434}(\alpha_3,\alpha_3,a,a)
 +h_\omega(a\cup_1a)+(s\alpha_3)h+s(\alpha_3\cup_1s)a,\\
\mathcal H_6(n,u)={}&T_6(u;w,s)+u\ell^\omega_3
 +(S^2u+sS^1u+wu)\cup_4\Xi_5+y_6(n;w,s)\\
&+[j_4]_2\cup_2[K_4]_2+s\big([j_4]_2\cup_3[K_4]_2\big),\\
\mathcal A_6(n,u,c)={}&S^2c+wc+\mathcal H_6(n,u),\\
\mathcal Q_6(n,u)={}&B_4\cup_2B_4+B_4\cup_3dB_4
 +\widetilde w B_4-\widetilde{\mathcal C_6}.
\end{aligned}
```

$`T_6`$ and $`y_6`$ are the fixed finite operations in
[Source operations](formulas/SOURCE_OPERATIONS.md). That appendix gives their
prism sums, grid recursion, integer quotients, and complete coefficient
table; they are not unspecified solutions of differential equations.

The shared high source is

<a id="eq-s3"></a>

**(S3)**

```math
\widehat O^B_6(n,u,c)=\frac12\mathcal A_6
 +\frac14\mathcal Q_6
 +\frac1{16}\mathcal P_s(W)n+\frac18\widetilde W n^2
 \pmod1.
```

<a id="three-dimensional-pair"></a>
## The 3+1D terminal pair

Return here to physical degrees $`(|n|,|u|,|c|)=(1,2,3)`$.
The full source and stacking correction are

<a id="eq-t3"></a>

**(T3)**

```math
\boxed{\begin{aligned}
\widehat O_5(n,u,c)&=\frac12\tau_I\mathcal A_6
 +\frac14\tau_I\mathcal Q_6+\frac1{16}\mathcal P_s(W)n,\\
\widehat E_4(n,u,c;m,v,c')&=\frac12\tau_\triangle\mathcal A_6
 +\frac14\tau_\triangle\mathcal Q_6-\frac18\widetilde W n m.
\end{aligned}}
```

$`\tau_I`$ evaluates on six interval/base paths; $`\tau_\triangle`$ on fifteen
triangle/base paths. Both are signed finite sums, defined in
[Operations](formulas/OPERATIONS.md#parameter-integration). The virtual
fields supplied to (S2) are specified below, including the fermion fill.
The output additive phase is $`\widehat\nu_4+\widehat\nu'_4+\widehat E_4`$;
equivalently the paper's phase is $`\nu_4\nu'_4\exp(2\pi i\widehat E_4)`$.
The lower output is (P2),(P3).

First form, in physical degrees,

<a id="eq-t3a"></a>

**(T3a)**

```math
\begin{aligned}
D_3(n,u)&=Wh+u\cup_2du+(s\cup_1w)a,\\
g_2&=hb+(a+h)k+t\cup_2(u+v)+t
 +(s\cup_1a)q+(s\cup_1q)(a+b).
\end{aligned}
```

On the oriented triangle $`012`$, let the integer one-cocycles
$`\theta,\phi`$ have edge values $`(01,12,02)=(1,0,1),(0,1,1)`$.
Let the binary cochain $`\chi`$ have $`(0,0,1)`$, so
$`d\chi=\theta\phi`$. Backgrounds and physical fields are pulled from the
base, and parameter cochains from the parameter simplex. Set

<a id="eq-t3b"></a>

**(T3b)**

```math
\begin{aligned}
\mathfrak n&=\theta n+\phi m,\\
\mathfrak u&=\theta u+\phi v+(W\cup_1\theta)a
 +(W\cup_1\phi)b+\chi t+\theta(a\cup_1\phi)b,\\
J_5&=F_5(\mathfrak n,\mathfrak u),\\
\mathfrak c&=\mathcal H_4J_5+\theta(c+D_3(n,u))
 +\phi(c'+D_3(m,v))\\
&\quad+\chi\big(e_3+D_3(N,U)+D_3(n,u)+D_3(m,v)\big)
 +(d\chi)g_2.
\end{aligned}
```

For the interval, take $`\theta(01)=1`$ and omit all primed terms:

<a id="eq-t3c"></a>

**(T3c)**

```math
\mathfrak n=\theta n,\qquad
\mathfrak u=\theta u+(W\cup_1\theta)a,\qquad
\mathfrak c=\mathcal H_4F_5(\mathfrak n,\mathfrak u)
 +\theta(c+D_3(n,u)).
```

The binary parameter/base homotopy $`\mathcal H_4`$ is the explicit grid sum
in [Operations](formulas/OPERATIONS.md#parameter-base-fill). These formulas
require no group-dependent fill solve. Evaluate all integral products with
their coefficient transports before integrating.

The current fermion coordinate is related to the older direct coordinate by

<a id="eq-t3d"></a>

**(T3d)**

```math
c_{\rm old}=c+\kappa_3(n,u),\qquad
\kappa_3=(a+s)u+Wh+[W\cup_1(a+s)]a.
```

When using this dictionary the product must also be transported:
$`e_{3,\rm old}=e_3+\kappa_3(N,U)+\kappa_3(n,u)+\kappa_3(m,v)`$.
In particular, $`n=0`$ alone does not erase this coordinate change for $`s\ne0`$.

<a id="four-dimensional-pair"></a>
## The 4+1D terminal pair

All fields now have the actual degrees $`(2,3,4)`$. The source is

<a id="eq-t4"></a>

**(T4)**

```math
\boxed{\widehat O_6(n,u,c)=\widehat O^B_6(n,u,c)+\frac1{12}n^3\pmod1.}
```

The cubic term vanishes on the interval and triangle lifts above; it is
retained here. To give the product, continue using $`t=a\cup_1b`$,
$`q=a\cup_2b`$, and set $`z=ab`$, $`F=dc`$, $`F'=dc'`$, $`C=c+c'+e_4`$.
For any one-input expression $`X`$, write
$`\Delta X=X(N,U)-X(n,u)-X(m,v)`$, including $`c,C`$ when $`X`$ uses them.
This notation preserves integer signs; only binary expressions turn minus
into plus.

For the following shared carries abbreviate $`B=B_4(n,u)`$,
$`B'=B_4(m,v)`$, and $`B_N=B_4(N,U)`$, using (S1):

<a id="eq-t4a"></a>

**(T4a)**

```math
\begin{aligned}
\lambda&=\frac{\widetilde U-\widetilde u-\widetilde v+n\cup_1m}{2},
&R&=mn,&D&=d\lambda-R,\\
B_N&=B+B'+D,&r&=[B]_2,&r'&=[B']_2,\\
l&=[\lambda]_2,&\bar D&=dl+ba.
\end{aligned}
```

Every division is exact. Here $`n,m,N,v_3`$ have coefficient type
$`\mathbb Z_s`$, while $`\widetilde u,\widetilde v,\widetilde U,\lambda,R,D,
B,B',B_N`$ have untwisted integer coefficients. Together with the global
types of $`\widetilde W`$ and $`\widetilde w`$, this fixes the transports in
every integral product below. Define the binary five-cochains

<a id="eq-t4b"></a>

**(T4b)**

```math
\begin{aligned}
J_5={}&\zeta_{2,2}(b,a)+va+bu+(W\cup_1b)a
 +k(a\cup_1a)+sbh+s(b\cup_1s)a,\\
\mathcal V_5={}&r\cup_3r'+dr\cup_4r'+(r+r')\cup_3\bar D
 +(dr+dr')\cup_4\bar D\\
&+S^2l+(ba)\cup_3dl+wl+(h_\omega+\alpha_3)q+J_5,\\
\Phi_5={}&\zeta_{2,2}(a,b)+a\cup_1dv+h(b\cup_1b)
 +(W\cup_1a)b+sak+s(a\cup_1s)b+t(a+b)+Wt,\\
\varepsilon_5={}&c\cup_3c'+dc\cup_4c'+(c+c')\cup_3e_4
 +(e_4+z)\cup_3z+dC\cup_4z,
\end{aligned}
```

and the signed integral five-cochain

<a id="eq-t4c"></a>

**(T4c)**

```math
\Pi_5=N\widetilde U-n\widetilde u-m\widetilde v
 +(n\cup_1\widetilde W)m+(m\cup_1\widetilde W)n.
```

The terminal product is

<a id="eq-t4d"></a>

**(T4d)**

```math
\boxed{\begin{aligned}
\widehat E_5={}&\frac12[\varepsilon_5+\Phi_5+Z_5]
 +\frac14[\widetilde{\mathcal V_5}+\Pi_5]
 +\frac18\widetilde W(n\cup_1m)\\
&+\frac13\big[(m-n)(n\cup_1m)-(n\cup_1m)(m-n)\big]\pmod1.
\end{aligned}}
```

The output in the paper's multiplicative convention is
$`(N,N_M,C,\nu_5\nu'_5\exp(2\pi i\widehat E_5))`$ with (P2),(P4).
$`Z_5`$ is the six-slot finite transfer in
[Terminal transfer](formulas/TERMINAL_TRANSFER.md): its kernel $`\rho_6`$,
first-face rule, tensor coefficient, and eight small coefficient polynomials
are all specified there. The ordered $`1/3`$ term is part of this formula;
it is not removed by treating cup products as commutative.

The source coordinate used in (S3),(T4) differs from the raw supplied source
by the paired convention change

<a id="eq-t4e"></a>

**(T4e)**

```math
\widehat O_6=\widehat O_{6,\rm raw}+d_s\Lambda_5+\frac1{12}n^3,
\qquad \Lambda_5=\frac14j_4\cup_3K_4.
```

Sources and products are transported together. No term in this guide is an
instruction to combine the old source with the new product in isolation.

## Reading the calculation as a classification

For fixed lower decorations, solve each displayed cochain equation modulo
the allowed gauge and lower-layer adjustments. A source can be nonzero yet
exact, or become exact after those adjustments. A rejected decoration is
one with a nontrivial **final** obstruction class. Stacking applies the full
product to accepted representatives, then reduces the result by the same
equivalences; the resulting carries determine extensions between layers.
The abstract stacking group is obtained from those relations, rather than
from a direct product of the surviving layer counts.

The displayed representatives fix an executable convention. Structural
cochain identities, agreement between implementations, and comparisons with
independent physical calculations are distinct kinds of validation. The
example catalog records the actual computed groups and their input data.
