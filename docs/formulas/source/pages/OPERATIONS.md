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

For an $`r`$-cochain $`x`$ of coefficient type $`\mathbb Z_{e s_1}`$, $`e\in\{0,1\}`$,

<a id="eq-o1"></a>

**(O1)**

{{equation:operations--differential-and-local-coefficients--1}}

For additive phases use the same rule modulo one. For binary cochains the
signs disappear. With the usual local trivialization,
$`d_{s_1}=d-2s_1\cup`$ on integer or phase cochains. A product of coefficient types
$`e,f`$ has type $`e+f`$ modulo two. The coefficient line is trivialized at the
first vertex of the entire evaluated simplex.

## Arithmetic and carries

$`\bar x`$ is pointwise reduction modulo two. A named binary cochain is
represented by its values $`0,1`$ whenever it occurs in integer arithmetic;
no extra symbol is needed for this canonical representative. Operations
are then performed in the indicated coefficient ring, with the signed
differential and cups in integer expressions.

In particular, an integer sum $`x+y`$ of binary inputs can have value two,
whereas $`\overline{x+y}`$ has values zero or one. The latter means reduce
the **entire sum** first, then use its canonical representative. The same
distinction applies to a differential or a higher cup: $`dx`$ and
$`x\cup_i y`$ in integer arithmetic are not automatically reduced modulo
two; $`\overline{dx}`$ and $`\overline{x\cup_i y}`$ are. A binary cochain
defined by an earlier equation is evaluated in its own binary arithmetic
before its named value is used in an integer expression.

The half-valued binary brackets in the phase formulas are reduced modulo
two before division by two. Quarter- and eighth-valued expressions instead
use integer arithmetic and the explicit bars shown in them. This retains
the distinction between an integer product of binary representatives and
the binary value of an entire product.

For an integer $`x`$, a tilde denotes its second binary digit:
$`\widetilde x=\overline{\lfloor x/2\rfloor}`$.
It always has this meaning; canonical integer lifts remain implicit as
stated above. Floors are mathematical floors also for negative integers.
If a higher digit is needed, its floor and reduction are written explicitly.
The Bockstein and second carry of a **closed** binary cochain are

<a id="eq-o2"></a>

**(O2)**

{{equation:operations--arithmetic-and-carries--2}}

Both are integer cochains; the differential in (O2) is ordinary, not twisted.
For an open binary cochain use the separately named integer carry

<a id="eq-o3"></a>

**(O3)**

{{equation:operations--arithmetic-and-carries--3}}

The twisted lift carry is
$`\beta_{s_1}\check\omega_2=d_{s_1}\check\omega_2/2`$; this integer
background carry has coefficient type $`\mathbb Z_{s_1}`$. Ordinary
Majorana Bocksteins above have untwisted integer coefficients.
Whenever a formula divides by $`2`$ or $`8`$, first form its **entire integer
numerator**, then perform the exact division, then reduce modulo two if
indicated. Generalized binomials use
$`\binom{x}{j}=x(x-1)\cdots(x-j+1)/j!`$ for every integer $`x`$, including
negative $`x`$, and $`\binom{x}{0}=1`$.

<a id="interval-cuts"></a>
## Interval cuts and May--Steenrod words

Let $`v=v_1\cdots v_L`$ be a word on $`1,\ldots,k`$, containing every label and
with no equal adjacent letters. For inputs $`x_j`$ of degrees $`q_j`$, the output
degree is $`q=\sum_jq_j-L+k`$. If $`q\lt 0`$ the result is zero. Otherwise enumerate
the weak cuts

<a id="eq-o4"></a>

**(O4)**

{{equation:operations--interval-cuts-and-may-steenrod-words--4}}

Interval $`\ell`$ is the vertex string $`[i_{\ell-1},\ldots,i_\ell]`$.
For each label $`j`$, concatenate the intervals with $`v_\ell=j`$ in their
original order. Keep the cut only if this concatenation consists of exactly
$`q_j+1`$ vertices with no repeated vertex. Evaluate $`x_j`$ on this face,
multiply over $`j`$, and sum over the retained cuts. Over $`\mathbb Z_2`$ this is
$`\mathop{\mathrm{MS}}\nolimits_v(x_1,\ldots,x_k)`$.

The alternating word beginning with $`1`$ and of length $`i+2`$ is $`\cup_i`$;
thus $`\cup=\mathop{\mathrm{MS}}\nolimits_{12}`$ and $`\cup_1=\mathop{\mathrm{MS}}\nolimits_{121}`$.
Negative cup indices give zero. The binary identity is

<a id="eq-o5"></a>

**(O5)**

{{equation:operations--interval-cuts-and-may-steenrod-words--5}}

For a general word, its binary boundary is obtained by deleting each letter
in turn. A deletion contributes zero if an input label disappears or equal
adjacent labels appear. Input differentials supply the remaining terms.

## Signed higher cups

Use the same cuts for integer $`x,y`$, now with signs. Call interval $`\ell`$
*inner* when its label appears again later. The indicator
$`\mathbf1_{\ell\,\mathrm{inner}}`$ is one for such an interval and zero otherwise.

For the alternating word of $`x\cup_i y`$, the cut sign is $`(-1)^\eta`$, where

<a id="eq-o6"></a>

**(O6)**

{{equation:operations--signed-higher-cups--6}}

If $`x,y`$ have types $`\mathbb Z_{e s_1},\mathbb Z_{f s_1}`$, and their cut faces are
$`F,G`$ inside a simplex rooted at $`v_0`$, multiply this sign further by

<a id="eq-o7"></a>

**(O7)**

{{equation:operations--signed-higher-cups--7}}

For example, untwisted integral two-cochains satisfy

{{equation:operations--signed-higher-cups--8}}

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

{{equation:operations--parameter-integration--9}}

Pull each cochain along its own projection, retaining coefficient
transports in each operation. All summands begin over the same base vertex,
so no additional transport is inserted between summands. The $`3+1`$D source
uses $`(r,q)=(1,5)`$, hence six paths; its product uses $`(2,4)`$, hence fifteen.
The height operation $`T_6`$ uses $`(1,6)`$, hence seven paths. For binary values
the orientation signs disappear.

<a id="parameter-base-fill"></a>
## Parameter/base fill

The chain homotopy $`\mathsf h_D^{(2)}`$ sends a degree-$`D`$ simplex on a
parameter/base product to a binary sum of degree-$`(D+1)`$ simplices.
Its dual $`(\mathsf h_D^{(2)})^*`$ evaluates a degree-$`(D+1)`$ cochain on
that sum, giving a degree-$`D`$ cochain. The superscript counts the two
factors, parameter and base. On the product simplex
$`f=(f_0,\ldots,f_D)`$ with $`f_i=(t_i,x_i)`$, enumerate

{{equation:operations--parameter-base-fill--10}}

For each choice, form the ordered grid

<a id="eq-o9"></a>

**(O9)**

{{equation:operations--parameter-base-fill--11}}

The point indexed by $`\ell`$ in the second segment of (O9) is explicitly
$`(j+h_\ell,j+r+\ell-h_\ell)`$ for $`0\le\ell\le D-j`$.
If the vertices of the complete grid are $`(\alpha_i,\beta_i)`$, set

<a id="eq-o10"></a>

**(O10)**

{{equation:operations--parameter-base-fill--12}}

Extend $`Q`$ linearly to binary chains. The guide uses $`D=4`$.
This is a fixed finite sum; no group-dependent linear system is part of the definition.

<a id="three-factor-grid"></a>
## Three-factor grid

The source and terminal transfer use the same binary grid recursion, with
different explicitly stated assignments of inputs to its coordinates.
For $`0\le r_1\le r_2\le D`$, take every lattice path from $`(0,r_1,r_2)`$ to
$`(r_1,r_2,D)`$ with $`r_1,r_2-r_1,D-r_2`$ steps in coordinates $`1,2,3`$.
Let $`G_D`$ be their sum over $`\mathbb Z_2`$. With $`\mathbf0=(0,0,0)`$, define

<a id="eq-o11"></a>

**(O11)**

{{equation:operations--three-factor-grid--13}}

The notation $`[\mathbf0,g]`$ prepends one vertex. Equal grids cancel modulo
two. The superscript now counts the three grid factors. Pull input cochains
along the assigned grid coordinates, evaluating normalized degeneracies as
zero. The dual $`(\mathsf h_D^{(3)})^*`$ sums a degree-$`(D+1)`$ cochain
over these pulled-back grids and produces a degree-$`D`$ cochain.
The two applications specify their assignments separately:
[integer-layer contribution to the bosonic obstruction](SOURCE_OPERATIONS.md#source-completion) and
[terminal transfer](TERMINAL_TRANSFER.md#transfer).
