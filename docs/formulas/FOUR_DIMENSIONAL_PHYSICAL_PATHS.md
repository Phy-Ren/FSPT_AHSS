# Physical face indices in the 4+1D stacking coefficients

This appendix specifies the finite integer indices of the coefficient
sum. Every factor is a value of the original physical fields on the
original simplex $`(012345)`$. The maps below act on vertex numbers.

## Finite index lists

For $`D=4,5`$, choose

```math
0\le k<D,\qquad
\sigma\in\{0,1,2\}^{D-k},\qquad \sigma\ne2^{D-k}.
```

Make a list of $`D+2`$ triples by first writing

```math
(0,0,0),\ldots,(k,k,k),
\quad(k,k+|\sigma|_0,k+|\sigma|_0+|\sigma|_1),
```

then successively incrementing the coordinate named by each letter of
$`\sigma`$. Here $`|\sigma|_a`$ counts occurrences of the letter $`a`$.
The three coordinate lists are $`g^0,g^1,g^2`$. Denote this finite set by
$`\mathcal G_D`$, and its subset with $`k\ge1`$ by $`\mathcal G_D^+`$.

Choose a length $`0\le J\le4`$, lists
$`g_1,\ldots,g_J\in\mathcal G_5^+`$, and bits
$`\epsilon_1,\ldots,\epsilon_J`$. For every such list put

```math
p_\ell^a(i)=g_\ell^a(i+1),\qquad 0\le i\le5,
\qquad a=0,1,2.
```

For the degree-six coefficient also choose a final list
$`g_*\in\mathcal G_5`$ and set $`p_*^a(i)=g_*^a(i)`$ for
$`0\le i\le6`$. For the degree-five tensor coefficient take
$`p_*^a=\mathrm{id}`$ on $`0,\ldots,5`$ instead. These are the two
parts of the complete finite index set; both are included.

## Vertex maps in each factor

Compose the integer maps in their displayed order:

```math
\begin{aligned}
P_\ell^a&=p_1^a\circ\cdots\circ p_\ell^a,
 &P_0^a&=\mathrm{id},\\
P^a&=P_J^a\circ p_*^a,
 &Q_\ell^a&=p_{\ell+1}^a\circ\cdots\circ p_J^a\circ p_*^a,\\
r_\ell&=P_{\ell-1}^0(0),
 &t_\ell&=P_{\ell-1}^0(1),\\
A_\ell^a(i)&=P_{\ell-1}^0
             \big(g_\ell^0(1+Q_\ell^a(i))\big),
 &e&=\sum_{\ell=1}^{J}\epsilon_\ell s_1(r_\ell,t_\ell)\pmod2.
\end{aligned}
```

Empty compositions are identity maps. A normalized cochain on a face
with repeated vertices is zero. Background factors become

```math
s_1(ij)\longmapsto s_1(P^0(i),P^0(j)),\qquad
\omega_2(ijk)\longmapsto\omega_2(P^0(i),P^0(j),P^0(k)).
```

For either physical integer input, the face factor is

```math
n_2^{(a)}(ijk)\longmapsto
(-1)^{e+s_1(0,P^a(i))+s_1(P^0(0),P^0(i))}
n_2^{(a)}(P^a(i),P^a(j),P^a(k)),\qquad a=1,2.
```

Here the two input labels mean $`n_2^{(1)}=n_2`$ and
$`n_2^{(2)}=n'_2`$; they do not introduce other physical decorations.
Every Majorana face factor becomes the following explicit sum:

```math
\begin{aligned}
\check n_3^{(a)}(ijkl)\longmapsto{}&
 \check n_3^{(a)}(P^a(i),P^a(j),P^a(k),P^a(l))\\
&+\Big[\check\omega_2(0,P^a(i),P^a(j))
 +\check\omega_2(P^0(0),P^0(i),P^0(j))\\
&\qquad+\sum_{\ell=1}^{J}\epsilon_\ell
  \big\{\check\omega_2(r_\ell,t_\ell,A_\ell^a(i))
       +\check\omega_2(r_\ell,t_\ell,A_\ell^a(j))\big\}\Big]\\
&\hspace{20mm}\times
 \bar n_2^{(a)}(P^a(j),P^a(k),P^a(l)).
\end{aligned}
```

The first term has Majorana origin. Every term in the square bracket
times the parity of the integer face has p+ip origin. Expand this sum
before collecting the physical contributions in the
[binary coefficient formula](FOUR_DIMENSIONAL_BINARY_COEFFICIENTS.md).
The formula uses $`\check n_3^{(1)}=\check n_3`$ and
$`\check n_3^{(2)}=\check n'_3`$.

Every cup or MS operation in the coefficient definition supplies its
ordinary finite list of faces. Substituting the factors above therefore
gives a finite sum of products of original physical cochain values. No
operation on an auxiliary physical field remains in that sum. Integer
signs are retained until the indicated divisions have been completed.

Use these same rules for the
[tensor coefficients](FOUR_DIMENSIONAL_TENSOR_COEFFICIENTS.md).
Their printed transport signs and background corrections already account
for their coefficient convention. No extra change of input is needed.

## Exact removal of zero path pairs

In the finite index list it is enough to keep

```math
0\le J\le4,\qquad
P_{\ell-1}^0(0)<P_{\ell-1}^0(1)
\quad(1\le\ell\le J).
```

All vertex maps and physical face factors remain as defined above. If the
inequality fails, write the coincident vertex as $`r`$. The two choices
of $`\epsilon_\ell`$ then give identical inputs: normalization gives
$`s_1(r,r)=0`$ and $`\check\omega_2(r,r,x)=0`$. Their binary contributions
cancel exactly, including their integer transports before the indicated
divisions. Every length-five path contains such a pair. No cochain
representative or phase convention is changed by omitting these pairs.

The retained path occurrences, including the binary branch choices, are
$`1,232,16704,334080,1336320`$ at lengths zero through four. These are
counts of construction indices, not counts of final nonzero formula terms.

For the pure Majorana coefficient, only length zero is needed. All
Majorana-origin factors and backgrounds are independent of the branch
bits: those bits affect only the integer-input sign and the displayed
p+ip correction. This remains true inside each Bockstein, canonical lift,
and integer digit. Every positive-length Majorana contribution thus
cancels with the identical term obtained by flipping one branch bit.
Its tensor contribution is zero.
