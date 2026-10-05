# Finite binary transfer in the 4+1D product

This appendix defines the single term $Z_5$ in (T4d) of the
[formula guide](../FORMULA_GUIDE.md#four-dimensional-pair). The definitions
are in evaluation order: kernel, coordinates, tensor coefficient, and final
finite sum. They use the guide's $B,B',B_N,\lambda,R,D,r,r',l,\bar D$,
$\mathcal H_6,\mathcal C_6,\mathcal V_5$, and lower product $e_4$.

## The binary kernel

Define

<a id="eq-k1"></a>

$$
Q(B)=B\cup_2B+B\cup_3dB,\qquad
\mathcal J_6(n,u)=\mathcal H_6(n,u)+a[B]_2+(a\cup_1\alpha_3)a,
\qquad T=-n\cup_1m.
\tag{K1}
$$

First form the entire integer expression

<a id="eq-k2"></a>

$$
\begin{aligned}
I_6={}&Q(B_N)-Q(B)-Q(B')+\widetilde w(d\lambda-R)\\
&-\widetilde{\mathcal C_6(N)}+\widetilde{\mathcal C_6(n)}
 +\widetilde{\mathcal C_6(m)}
 +\widetilde W R-v_3T-d_s\widetilde{\mathcal V_5}.
\end{aligned}
\tag{K2}
$$

It is pointwise even. With $F=F_5(n,u)$, $F'=F_5(m,v)$, and $z=ab$, set

<a id="eq-k3"></a>

$$
\begin{aligned}
\rho_6={}&S^2(e_4+z)+w(e_4+z)+F\cup_4F'\\
&+(F+F')\cup_3(e_4+z)+(e_4+z)\cup_3(F+F')\\
&+\mathcal J_6(N,U)+\mathcal J_6(n,u)+\mathcal J_6(m,v)
 +[I_6/2]_2+W\,dt+\alpha_3t.
\end{aligned}
\tag{K3}
$$

Every derivative in (K1)--(K3) differentiates a previously specified
expression; for instance, $dr=\alpha_3a$ and $dt=ab+ba$.
The free complex-fermion solutions $c,c'$ do not enter this kernel.

## Shared-background coordinates

A degree-$d$ graded simplex is

$$
S=(s,w;n_0,u_0;m_0,v_0),\qquad
dn_0=dm_0=0,\quad du_0=[n_0]_2^2,\quad dv_0=[m_0]_2^2.
$$

Here the integer cochains are untwisted. Decode to the physical fields by

<a id="eq-k4"></a>

$$
\begin{aligned}
n(i j k)&=(-1)^{s(0i)}n_0(i j k),&
m(i j k)&=(-1)^{s(0i)}m_0(i j k),\\
q_W(n)(i j k l)&=\begin{cases}0,&i=0,\\W(0ij)[n]_2(jkl),&i>0,
\end{cases}&
u&=u_0+q_W(n),\quad v=v_0+q_W(m).
\end{aligned}
\tag{K4}
$$

Take $s(00)=0$. Encoding is the inverse of (K4). Positive faces and
degeneracies are factorwise. The actual zeroth face is obtained by decoding,
restricting to $[1,\ldots,d]$, and re-encoding with vertex $1$ as root.
Relative to the factorwise zeroth face its changes are

<a id="eq-k5"></a>

$$
n_0\longmapsto(-1)^{s(01)}n_0,\qquad
u_0(ijkl)\longmapsto u_0(ijkl)+[W(01i)+W(01j)]a(jkl),
\tag{K5}
$$

for $1\le i<j<k<l\le d$, and the same for the second input.
Let $\delta S$ be the binary sum of the actual and factorwise zeroth faces.
Extend this operation linearly to binary chains. The root in (K4) is a
coordinate choice on each simplex, not a global trivialization of either
background; its failure on the zeroth face is precisely (K5).

## The tensor coefficient

The coefficient is $L=L_\star+L_s$. For integer values $x,y$, write
$x_i=[\lfloor x/2^i\rfloor]_2$ and $y_i=[\lfloor y/2^i\rfloor]_2$,
$i=0,1,2$. The antiunitary term is

<a id="eq-k6"></a>

$$
\begin{aligned}
f(x,y)&=(x_0+x_1)y_1(1+y_0)+x_1(y_0+y_2)+x_2y_0(1+y_1),\\
L_s(S)&=s(01)f(n_0(123),m_0(345)).
\end{aligned}
\tag{K6}
$$

These are **graded** integer values. An equivalent separated-variable form,
useful for evaluating the polynomial, is

<a id="eq-k7"></a>

$$
f=(\gamma_1+\gamma_2)\otimes(\gamma_2+\gamma_3)
 +\gamma_2\otimes(\gamma_1+\gamma_4)
 +\gamma_4\otimes(\gamma_1+\gamma_3),\qquad
\gamma_i(x)=\binom xi\pmod2.
\tag{K7}
$$

The first tensor factor acts on $x$, the second on $y$.

### Eight tetrahedral polynomials

For a single zero-background input $(n,u)$ on $0123$, first form the actual
integer differences

$$
p=n(012),\qquad q=n(013)-n(012),\qquad r=n(123).
$$

In this paragraph only, write their first bits as $(x,y,z)$, second bits as
$(X,Y,Z)$, set $\epsilon=u(0123)$, $S=x+y+z$, and $Q=X+Y+Z$. The following
products are ordinary products of bits on this tetrahedron:

<a id="eq-k8"></a>

$$
\begin{aligned}
P^L_1&=(x+y)(z+Z)+\epsilon[1+S+yz(1+x)+(x+y)Q+zZ],\\
P^L_2&=(y+Y)(x+z)+y[X(1+z)+Z(1+x)],\\
P^L_3&=P^L_2+Y(X+Z)+\epsilon[S+z(x+y)+(x+y)Q+zZ],\\
P^L_4&=Y(X+Z)+y[x(1+z+X+Y)+z(Y+Z)],\\
P^R_4&=yz(1+x),\\
P^R_2&=P^R_4+Y(X+Z),\\
P^R_3&=Y(X+Z)+xz(Y+Z)+y(xY+Xz)+\epsilon[S+SQ+xyz],\\
P^R_1&=P^R_3+xz(1+y)+\epsilon[1+S+xz(1+y)].
\end{aligned}
\tag{K8}
$$

Rows referenced on the right use the same input and face. In particular,
$Y$ is the second bit of the integer **difference** $q$, not the sum of the
second bits of $n(013)$ and $n(012)$. Define the ordered-cup polynomial

<a id="eq-k9"></a>

$$
L_0(n,u;m,v)=\sum_{i=1}^4
\big[\gamma_i(n)P^L_i(m,v)+P^R_i(n,u)\gamma_i(m)\big].
\tag{K9}
$$

### The balanced integer carry

Only in the following formulas set $w=s=0$; thus $dn=dm=0$,
$du=a^2$, $dv=b^2$. Use the definitions of $B,B',D,\lambda,R$ at these
zero backgrounds and let $q_{\mathbb Z}=n\cup_1m$. Form

<a id="eq-k10"></a>

$$
\begin{aligned}
\mathcal Q^{\rm int}_5={}&B\cup_3B'+(B+B')\cup_3D
 +\lambda\cup_1\lambda+\lambda\cup_2d\lambda+R\cup_3d\lambda\\
&+\zeta^{\mathbb Z}_{2,2}(m,n)-\binom m2(n\cup_1n),\\
K^-_5={}&(n+2m)q_{\mathbb Z}+q_{\mathbb Z}(2n+m),\\
A^{\rm pair}_4={}&v\cup_1a+b\cup_1t+\operatorname{MS}_{23123}(a,b,b),\\
G^0_5(n,u)={}&\frac12ua+\frac14n\widetilde u,\\
D^0_5={}&\left[\frac{\mathcal Q^{\rm int}_5-3K^-_5
 -\widetilde{\mathcal V}_{5,0}-d\widetilde A^{\rm pair}_4
 -4\Delta G^0_5}{2}\right]_2.
\end{aligned}
\tag{K10}
$$

The integer face polynomial is

$$
\zeta^{\mathbb Z}_{2,2}(m,n)(012345)=m(012)m(023)n(235)n(345).
$$

$\mathcal V_{5,0}$ means (T4b) evaluated at $w=s=0$;
$\Delta G^0_5=G^0_5(N,U)-G^0_5(n,u)-G^0_5(m,v)$.
The whole numerator defining $D^0_5$ is even. The first term of $G^0_5$ is
the canonical lift of the binary product $ua$ divided by two; retaining this
lift during $4\Delta G^0_5$ fixes the integer carry.

Now define

<a id="eq-k11"></a>

$$
L_\star=L_0+\operatorname{AW}^*
\big[(\operatorname{sh}^*D^0_5)_{2,3}
 +(\operatorname{sh}^*D^0_5)_{3,2}\big].
\tag{K11}
$$

This notation is a finite rule: for $(p,q)=(2,3)$ and $(3,2)$, use the
front $p$-face and back $q$-face of a five-simplex, sharing vertex $p$.
Enumerate the ten paths from $(0,p)$ to $(p,5)$. Pull the two **complete**
zero-background inputs along coordinates one and two, evaluate $D^0_5$,
and sum modulo two. Add the two sums to $L_0$. On a graded simplex,
$L_\star$ uses its two graded inputs at background degree zero, while (K6)
uses the background-degree-one component. These prescriptions define $L$
on every simplex appearing below.

<a id="transfer"></a>
## The six-slot formula

Use the grid operation $h$ in (O11), with factors ordered
$(\text{common background},\text{first input},\text{second input})$.
For grid vertices $(r_i,t_i,v_i)$, pull both $s,w$ along $r$, the complete
graded pair $(n_0,u_0)$ along $t$, and $(m_0,v_0)$ along $v$. After pulling
back, decode (K4) before evaluating $\rho_6$.

Encode the physical input as a graded five-simplex $S$. The required term is

<a id="eq-k12"></a>

$$
\boxed{Z_5(S)=\sum_{j=0}^{5}
\left[\rho_6\big(h(\delta h)^jS\big)
 +L\big((\delta h)^jS\big)\right]\pmod2.}
\tag{K12}
$$

Evaluation on a binary chain means the sum of the values on its normalized
simplices. Cancel equal simplices before evaluating the source. The bound
$j\le5$ is finite: each nonzero $\delta h$ lowers the background skeletal
filtration, whose degree here is at most five. All face rules, grids,
polynomials, and division operations used in (K12) have been specified
above; it does not call a group-dependent primitive solver.
