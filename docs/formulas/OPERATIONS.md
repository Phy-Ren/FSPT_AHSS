# Cochain operations

This appendix fixes the operations used in the [formula guide](../FORMULA_GUIDE.md).
All simplices have ordered vertices. A repeated ordered **simplex index**
produced by an interval cut or projection gives a degenerate pullback, whose
normalized cochain value is zero. Such indices are never deleted to create
a different face. This rule concerns simplex indices, not equality of group
labels: on homogeneous group vertices, a normalized bar cochain is evaluated
on the successive group increments and vanishes if one of those increments
is the identity. Equal group labels at nonadjacent vertices alone do not
make a bar simplex degenerate.

## Differential and local coefficients

For an $`r`$-cochain $`x`$ of coefficient type $`\mathbb Z_{es}`$, $`e\in\{0,1\}`$,

<a id="eq-o1"></a>

**(O1)**

```math
(d_{es}x)(v_0\ldots v_{r+1})=
(-1)^{e s(v_0v_1)}x(v_1\ldots v_{r+1})
 +\sum_{j=1}^{r+1}(-1)^j x(v_0\ldots\widehat v_j\ldots v_{r+1}).
```

For additive phases use the same rule modulo one. For binary cochains the
signs disappear. With the usual local trivialization,
$`d_s=d-2s\cup`$ on integer or phase cochains. A product of coefficient types
$`e,f`$ has type $`e+f`$ modulo two. The coefficient line is trivialized at the
first vertex of the entire evaluated simplex.

## Lifts and carries

$`[x]_2`$ is reduction modulo two and $`\widetilde a`$ is the canonical lift of a
binary cochain $`a`$ to values $`0,1`$. These operations are pointwise.
In particular, $`\widetilde{a+b}`$ is not $`\widetilde a+\widetilde b`$.
The Bockstein and second carry of a **closed** binary cochain are

<a id="eq-o2"></a>

**(O2)**

```math
\beta a=\frac{d\widetilde a}{2},\qquad
\beta^+a=\frac{\beta a+\widetilde{[\beta a]_2}}2.
```

Both are integer cochains; the differential in (O2) is ordinary, not twisted.
For an open binary cochain use the separately named integer carry

<a id="eq-o3"></a>

**(O3)**

```math
\beta^\circ a=\frac{d\widetilde a-\widetilde{da}}2.
```

The twisted lift carry $`\beta_sW=d_s\widetilde W/2`$ is defined separately.
Whenever a formula divides by $`2`$ or $`8`$, first form its **entire integer
numerator**, then perform the exact division, then reduce modulo two if
indicated. Generalized binomials use
$`\binom{x}{j}=x(x-1)\cdots(x-j+1)/j!`$ for every integer $`x`$, including
negative $`x`$, and $`\binom{x}{0}=1`$.

<a id="interval-cuts"></a>
## Interval cuts and May--Steenrod words

Let $`v=v_1\cdots v_L`$ be a word on $`1,\ldots,k`$, containing every label and
with no equal adjacent letters. For inputs $`a_j`$ of degrees $`q_j`$, the output
degree is $`q=\sum_jq_j-L+k`$. If $`q\lt 0`$ the result is zero. Otherwise enumerate
the weak cuts

<a id="eq-o4"></a>

**(O4)**

```math
0=i_0\le i_1\le\cdots\le i_L=q.
```

Interval $`\ell`$ is the vertex string $`[i_{\ell-1},\ldots,i_\ell]`$.
For each label $`j`$, concatenate the intervals with $`v_\ell=j`$ in their
original order. Keep the cut only if this concatenation consists of exactly
$`q_j+1`$ vertices with no repeated vertex. Evaluate $`a_j`$ on this face,
multiply over $`j`$, and sum over the retained cuts. Over $`\mathbb Z_2`$ this is
$`\mathop{\mathrm{MS}}\nolimits_v(a_1,\ldots,a_k)`$.

The alternating word beginning with $`1`$ and of length $`i+2`$ is $`\cup_i`$;
thus $`\cup=\mathop{\mathrm{MS}}\nolimits_{12}`$ and $`\cup_1=\mathop{\mathrm{MS}}\nolimits_{121}`$.
Negative cup indices give zero. The binary identity is

<a id="eq-o5"></a>

**(O5)**

```math
d(x\cup_i y)=dx\cup_i y+x\cup_i dy+x\cup_{i-1}y+y\cup_{i-1}x.
```

For a general word, its binary boundary is obtained by deleting each letter
in turn. A deletion contributes zero if an input label disappears or equal
adjacent labels appear. Input differentials supply the remaining terms.

## Signed higher cups

Use the same cuts for integer $`x,y`$, now with signs. Call interval $`\ell`$
*inner* when its label appears again later. Put

```math
\lambda_\ell=i_\ell-i_{\ell-1}
 +\begin{cases}1,&\ell\text{ is inner},\\0,&\text{otherwise}.
\end{cases}
```

For the alternating word of $`x\cup_i y`$, the cut sign is $`(-1)^\eta`$, where

<a id="eq-o6"></a>

**(O6)**

```math
\eta=i(|x|+|y|)+\binom i2
 +\sum_{\ell\text{ inner}}i_\ell
 +\sum_{\ell\lt m,\ v_\ell\gt v_m}\lambda_\ell\lambda_m
 \pmod2.
```

If $`x,y`$ have types $`\mathbb Z_{es},\mathbb Z_{fs}`$, and their cut faces are
$`F,G`$ inside a simplex rooted at $`v_0`$, multiply this sign further by

<a id="eq-o7"></a>

**(O7)**

```math
(-1)^{e s(v_0,F_0)+f s(v_0,G_0)}.
```

For example, untwisted integral two-cochains satisfy

```math
(x\cup_1 y)(0123)=x(023)y(012)-x(013)y(123).
```

Every integral cup in the guide uses (O6),(O7). Higher-arity May words in the
guide are binary; the explicitly displayed $`\zeta^{\mathbb Z}_{2,2}`$ in the
terminal-transfer appendix is defined by its own face polynomial.

<a id="parameter-integration"></a>
## Parameter integration

For an oriented parameter $`r`$-simplex $`T`$ and base $`q`$-simplex $`f`$, enumerate
all paths from $`(0,0)`$ to $`(r,q)`$ with one-coordinate unit steps. If the
parameter steps occupy $`P\subset\{1,\ldots,r+q\}`$, let
$`\mathop{\mathrm{inv}}\nolimits(P)`$ count base steps preceding parameter steps. Then

<a id="eq-o8"></a>

**(O8)**

```math
(\tau_T Q)(f)=\sum_{|P|=r}(-1)^{\mathop{\mathrm{inv}}\nolimits(P)}
 Q(\sigma_P(T,f)).
```

Pull each cochain along its own projection, retaining coefficient
transports in each operation. All summands begin over the same base vertex,
so no additional transport is inserted between summands. The $`3+1`$D source
uses $`(r,q)=(1,5)`$, hence six paths; its product uses $`(2,4)`$, hence fifteen.
The height operation $`T_6`$ uses $`(1,6)`$, hence seven paths. For binary values
the orientation signs disappear.

<a id="parameter-base-fill"></a>
## Parameter/base fill

The binary operation $`\mathcal H_d`$ takes a degree-$`(d+1)`$ cochain $`Q`$ on a
parameter/base product to a degree-$`d`$ cochain. On the product simplex
$`f_i=(t_i,x_i)`$, enumerate

```math
0\le j\lt d,\quad 1\le r\le d-j,\quad
I\subset\{1,\ldots,d-j\},\quad |I|=r,
\qquad h_\ell=|I\cap\{1,\ldots,\ell\}|.
```

For each choice, form the ordered grid

<a id="eq-o9"></a>

**(O9)**

```math
G_{j,r,I}=((0,0),\ldots,(j,j),
 (j+h_0,j+r-h_0),\ldots,(j+h_{d-j},d+r-h_{d-j})).
```

The point indexed by $`\ell`$ in the second segment of (O9) is explicitly
$`(j+h_\ell,j+r+\ell-h_\ell)`$ for $`0\le\ell\le d-j`$.
If the vertices of the complete grid are $`(\alpha_i,\beta_i)`$, set

<a id="eq-o10"></a>

**(O10)**

```math
(\mathcal H_dQ)(f)=\sum_{j,r,I}
Q((t_{\alpha_0},x_{\beta_0}),\ldots,
  (t_{\alpha_{d+1}},x_{\beta_{d+1}}))\pmod2.
```

The guide uses $`d=4`$. This is a fixed finite sum; no group-dependent linear
system is part of the definition.

<a id="three-factor-grid"></a>
## Three-factor grid

The source and terminal transfer use the same binary grid recursion, with
different explicitly stated assignments of inputs to its coordinates.
For $`0\le r_1\le r_2\le d`$, take every lattice path from $`(0,r_1,r_2)`$ to
$`(r_1,r_2,d)`$ with $`r_1,r_2-r_1,d-r_2`$ steps in coordinates $`1,2,3`$.
Let $`G_d`$ be their sum over $`\mathbb Z_2`$. With $`\mathbf0=(0,0,0)`$, define

<a id="eq-o11"></a>

**(O11)**

```math
h_0=0,\qquad
h_d=\sum_{g\in G_d,\ g_0\ne\mathbf0}[\mathbf0,g]
 +\sum_{g\in h_{d-1}}[\mathbf0,g+(1,1,1)].
```

The notation $`[\mathbf0,g]`$ prepends one vertex. Equal grids cancel modulo
two. Pull input cochains along the assigned grid coordinates, evaluating
normalized degeneracies as zero, and sum the resulting simplex values.
The two applications specify their assignments separately:
[source completion](SOURCE_OPERATIONS.md#source-completion) and
[terminal transfer](TERMINAL_TRANSFER.md#transfer).
