# 4+1D finite symmetry backgrounds

An example is specified by $(G_b,s_1,[\omega_2])$. Here $G_b$ is the
bosonic quotient, $s_1$ identifies its antiunitary elements, and
$\omega_2$ defines the central extension by fermion parity $f$.
In every presentation below, $f^2=1$ and $f$ is central and unitary.
The order of $G_f$ is twice the order of $G_b$; neither order is the
stacking group printed in the last column.

The [seven family tables](tables/internal_4d.md) contain each background
once. Distinct names for an isomorphic graded central extension are
provenance aliases. The exact input arrays, group isomorphism, and section
one-cochain for every retained calculation are in the
[coverage ledger](COVERAGE_4D.json) and [symbolic table](tables/internal_4d_symbolic.json).
Changing section means $\omega_2\mapsto\omega_2+d\lambda$; it does not
create another physical example. The split column is determined by solving
this equation, rather than by asking whether the saved cocycle array is zero.

## Cyclic and noncyclic abelian groups

Use ordered generators $r_i$ of orders $m_i$, and write
$g=\prod_i r_i^{u_i}$ with $0\leq u_i\lt m_i$. Put

$$
\eta_i(g,h)=\left\lfloor\frac{u_i+v_i}{m_i}\right\rfloor\bmod2,
\qquad x_i(g)=u_i\bmod2.
$$

Only even-order factors carry a nonzero binary character. For $m_i=2$,
$\eta_i=x_i^2$. The two-generator tables abbreviate $x_1,x_2$ as $x,y$;
one-generator tables use $x$. The index on $\eta_i$ always refers to the
ordered factors printed in $G_b$.

Every displayed cocycle has the form

$$
\omega_2=\sum_i\epsilon_i\eta_i+
\sum_{i\lt j}\kappa_{ij}x_j\cup x_i.
$$

It specifies $R_i^{m_i}=f^{\epsilon_i}$ and
$R_jR_i=f^{\kappa_{ij}}R_iR_j$. The generator grading determines
$s_1=\sum_i s_1(r_i)x_i$. The saved section witnesses verify the displayed
cocycle on every ordered pair of elements.

## Dihedral, quaternion and other metacyclic groups

In these tables **$D_m$ has order $2m$**, while $Q_N$ has order $N$.
Use

$$
G_b=\langle r,t\mid r^m=1,\ t^n=r^k,\ trt^{-1}=r^a\rangle.
$$

| Group | $(m,n,k,a)$ |
|---|---|
| $D_m$ | $(m,2,0,-1)$ |
| $Q_N$ | $(N/2,2,N/4,-1)$ |
| $\mathrm{SD}_{16}$ | $(8,2,0,3)$ |
| $\mathrm{SD}_{32}$ | $(16,2,0,7)$ |
| $M_{16}$ | $(8,2,0,5)$ |
| $\mathbb Z_4\rtimes_{-1}\mathbb Z_4$ | $(4,4,0,-1)$ |

The subscript in $\omega_{\alpha\beta\gamma}$ gives the three signs in

$$
R^m=f^\alpha,\qquad T^n=R^k f^\beta,\qquad
TRT^{-1}=R^a f^\gamma.
$$

This also gives an explicit cocycle. For $g=r^it^j$ and
$g'=r^{i'}t^{j'}$ with $0\leq i,i'\lt m$, $0\leq j,j'\lt n$, it is

$$
\omega_{\alpha\beta\gamma}(g,g')
=\alpha\left\lfloor\frac{i+a^j i'+k\lfloor(j+j')/n\rfloor}{m}\right\rfloor
+\beta\left\lfloor\frac{j+j'}{n}\right\rfloor
+\gamma i'\sum_{q=0}^{j-1}a^q\pmod2.
$$

The sum is zero for $j=0$. Characters satisfy $x(r)=1,x(t)=0$ and
$y(r)=0,y(t)=1$ whenever allowed by the relations. For odd $m$, only
$y$ is used. The table's $s_1$ is the corresponding combination.

## Products with a cyclic factor

For $D_4\times\mathbb Z_2$ and $Q_8\times\mathbb Z_2$, use $r,t,z$,
with $r^4=z^2=1$, $t^2=r^k$, $trt^{-1}=r^{-1}$ and $z$ central;
$k=0$ for $D_4$ and $k=2$ for $Q_8$.
The six bits in $\omega_{\alpha\beta\gamma\delta\epsilon\zeta}$ mean

$$
\begin{aligned}
R^4&=f^\alpha,&T^2&=R^k f^\beta,&TRT^{-1}&=R^{-1}f^\gamma,\\
Z^2&=f^\delta,&ZR&=f^\epsilon RZ,&ZT&=f^\zeta TZ.
\end{aligned}
$$

For $g=r^it^jz^q$ and $g'=r^{i'}t^{j'}z^{q'}$, the cocycle is

$$
\omega_2(g,g')=
\alpha\left\lfloor\frac{i+(-1)^ji'+kjj'}{4}\right\rfloor
+\beta jj'+\gamma ji'+\delta qq'+\epsilon qi'+\zeta qj'\pmod2.
$$

The characters $x,y,z$ in the grading column evaluate on $r,t,z$,
respectively. The character $z$ and generator $z$ are distinguished by
whether an element or a cochain is required.

## Tetrahedral and octahedral groups

For $A_4$, choose $r^3=t^3=(rt)^2=1$. The nonzero background
$\omega_{\rm tet}$ is specified by $R^3=T^3=1$, $(RT)^2=f$;
its full fermionic extension is the binary tetrahedral group.
The split background on $G_b=\mathrm{SL}(2,\mathbb F_3)$ is a different
example: its fermionic group is $\mathbb Z_2^f\times\mathrm{SL}(2,\mathbb F_3)$.

For $S_4$, choose $r^2=t^4=(rt)^3=1$. The two signs in
$\omega_{\alpha\beta}$ specify

$$
R^2=f^\alpha,\qquad T^4=f^\beta,\qquad (RT)^3=1.
$$

The character $x$ is the permutation sign, with $x(r)=x(t)=1$.
The complete short presentations, including the chosen generator lifts,
are checked directly against the finite multiplication tables.

## Coverage and distinctness

Historical relabelings and section changes are checked on every ordered
pair. The additional Bott-family identifications are constructed from
their graded central extensions and verified by the same pairwise test.
Within each normalized group family, the verifier enumerates every group
automorphism and compares the complete defining-relator signs and grading,
allowing changes of generator lifts. No two retained rows have the same
graded extension orbit. Historical raw result bytes remain unchanged.

The [cochain and geometric controls](CALIBRATIONS_4D.md) have a different
scope and are listed separately from these classification examples.
