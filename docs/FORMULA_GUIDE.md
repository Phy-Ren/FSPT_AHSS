# FSPT obstruction functions and stacking twisters

Each dimension has a complete formula page. Within each page, obstruction functions come first, followed by stacking twisters. The notation below is shared; physical fields are defined separately in each dimension.

| Dimension | Obstruction functions | Stacking twisters |
|---|---|---|
| 2+1D | [Obstructions](formulas/TWO_DIMENSIONAL.md#obstructions-2d) | [Stacking](formulas/TWO_DIMENSIONAL.md#stacking-2d) |
| 3+1D | [Obstructions](formulas/THREE_DIMENSIONAL.md#obstructions-3d) | [Stacking](formulas/THREE_DIMENSIONAL.md#stacking-3d) |
| 4+1D | [Obstructions](formulas/FOUR_DIMENSIONAL.md#obstructions-4d) | [Stacking](formulas/FOUR_DIMENSIONAL.md#stacking-4d) |

## Notation

The backgrounds are $`\omega_2\in Z^2(G_b,\mathbb Z_2)`$ and
$`s_1\in Z^1(G_b,\mathbb Z_2)`$, held fixed during stacking.
A subscript gives the cochain degree. Each dimension defines its own
fields; their physical roles are not inferred from another section.
The physical labels $`c,\gamma,\psi`$ mean, respectively,
complex fermion, Majorana, and p+ip. The fixed order for resolved
contributions is $`c,c\gamma,c\psi,\gamma,\gamma\psi,\psi`$;
absent contributions are omitted. A mixed superscript identifies an interaction between the indicated physical layers. The pieces are parts of the full
cochain equation; they need not be separately closed. In the p+ip sections they refer to the
displayed shifted Majorana field; rewriting it in native fields redistributes
some mixed terms.

<a id="conventions-and-coordinates"></a>

### Arithmetic and modifiers

A prime denotes the second stacking input. On an individual field it is
placed outside the modifier: $`\bar n'_j,\widetilde n'_j,\check n'_j`$. The outputs are $`N_j`$ and
$`\nu_j^{\mathrm{out}}`$. A hat denotes the additive phase,
$`\nu_j=\exp(2\pi i\widehat\nu_j)`$, with
$`\widehat\nu_j\in\mathbb R/\mathbb Z`$. The same convention applies to
phase obstructions $`\widehat{\mathcal{𝒪}}`$ and corrections
$`\widehat{\mathcal{ℰ}}`$.

A bar means reduction modulo two; a tilde means the second binary digit:

```math
\bar x=x\pmod2,\qquad
\widetilde x=\overline{\lfloor x/2\rfloor}.
```

Floors are mathematical floors, including for negative integers. Integer
lifts are implicit, so tilde always has the meaning above. A check denotes
an explicitly defined shift. The background shift is

<a id="eq-c1"></a>

**(C1)**

```math
\check\omega_2=\omega_2+s_1\cup s_1.
```

### Integer lifts are implicit in integer arithmetic

A named binary cochain in an integer expression means its canonical
$`0,1`$ lift. No lift symbol is needed. Sums, differences, differentials, and
higher cups in such an expression use integer arithmetic and its stated
coefficient transport. If an entire compound expression must first be
reduced, its bar stays explicit. For binary values, for example,

```math
\overline{x+y}=x+y-2xy\quad\text{in }\mathbb Z.
```

Thus $`(x+y)/4`$ and $`\overline{x+y}/4`$ need not be the same phase. A
previously defined binary polynomial is first evaluated as that binary
polynomial, then lifted when used in an integer expression. Integer
numerators are assembled completely before exact division.
A phase bracket with coefficient $`1/2`$ is binary before its implicit
lift; the integral $`1/4,1/8,1/16`$ terms state their arithmetic separately.

All products are ordered: juxtaposition means $`\cup=\cup_0`$. Powers are
ordered cup powers. Ordinary $`d`$ and $`d_{s_1}`$ are the untwisted and
sign-twisted differentials. Their coefficient domain follows the equation.
In particular, the differential inside an integer Bockstein is taken
before reduction.

For a binary cochain $`x`$ of degree $`r`$, use the standard Steenrod symbol:

<a id="eq-c2"></a>

**(C2)**

```math
\mathrm{Sq}^j x=x\cup_{r-j}x+x\cup_{r-j+1}dx.
```

The second term is retained for a nonclosed cochain. Negative or
otherwise degree-impossible higher cups are zero in the explicit
[interval-cut definition](formulas/OPERATIONS.md#interval-cuts).

| Operation | Definition and domain |
|---|---|
| $`\beta x=dx/2`$ | Integer Bockstein, for binary $`dx=0`$; numerator is the **integer** differential |
| $`\beta^\circ x=(dx-\overline{dx})/2`$ | Integer carry for a possibly open binary cochain |
| $`\beta^+x=(\beta x+\overline{\beta x})/2`$ | The plus carry of a closed binary cochain |
| $`\beta_{s_1}\check\omega_2=d_{s_1}\check\omega_2/2`$ | Twisted integer background carry |
| $`\Delta f=f(N)-f(n)-f(n')`$ | Full change under the displayed lower stacking law, with fixed backgrounds |

The integer lifts of $`\check\omega_2`$ and the p+ip field have coefficients
$`\mathbb Z_{s_1}`$; those of $`\omega_2`$ and the Majorana field have ordinary
integer coefficients. [Operations](formulas/OPERATIONS.md#eq-o7) specifies
all coefficient transports. A check is never an instruction to change
those coefficient systems.

Finite definitions of higher cups and ordered word operations are in
[Operations](formulas/OPERATIONS.md). The terminal formulas below use physical cochains. Long numerical coefficient lists and proofs of the paired representative changes are kept in separate appendices.

## Finite definitions and coordinate maps

- 3+1D: [obstruction word coefficients](formulas/THREE_DIMENSIONAL_WORD_INDICES.md), [stacking word coefficients](formulas/THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md), [complex-fermion stacking coefficients](formulas/THREE_DIMENSIONAL_PRODUCT_CF_WORDS.md).
- 3+1D pure p+ip face coefficients: [obstruction](formulas/THREE_DIMENSIONAL_INTEGER_SOURCE_FACES.md), [stacking](formulas/THREE_DIMENSIONAL_INTEGER_PRODUCT_FACES.md).
- 4+1D: [Majorana word coefficients](formulas/FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md), [stacking coefficients](formulas/FOUR_DIMENSIONAL_BINARY_COEFFICIENTS.md), [physical face indices](formulas/FOUR_DIMENSIONAL_PHYSICAL_PATHS.md), [tensor coefficients](formulas/FOUR_DIMENSIONAL_TENSOR_COEFFICIENTS.md).
- [4+1D pure-source construction](formulas/SOURCE_OPERATIONS.md#source-completion).
- [Closed-Majorana formulas](formulas/MAJORANA_AND_ENDPOINTS.md)
- [Higher cups and finite sums](formulas/OPERATIONS.md), [fixed coefficients](formulas/COEFFICIENTS.md)
- [Changes of representative](formulas/REPRESENTATIVES.md)
- [Formula-to-code translation](../formulas/CODE_NOTATION.md)

A nonzero obstruction cochain may be a coboundary. Only its nontrivial
class after the permitted lower-layer changes obstructs the decoration.

## Dimensional formula pages

<a id="two-dimensional"></a>
<a id="obstructions-2d"></a>
<a id="stacking-2d"></a>

[Complete 2+1D formulas](formulas/TWO_DIMENSIONAL.md).

<a id="three-dimensional"></a>
<a id="eq-c1-3d"></a>
<a id="obstructions-3d"></a>
<a id="lower-sources"></a>
<a id="eq-integer-3d"></a>
<a id="eq-l1"></a>
<a id="eq-l2"></a>
<a id="eq-l3"></a>
<a id="eq-t3"></a>
<a id="three-dimensional-pip-source"></a>
<a id="stacking-3d"></a>
<a id="lower-stacking"></a>
<a id="eq-p1"></a>
<a id="eq-p2"></a>
<a id="eq-p3"></a>
<a id="eq-t3b"></a>

[Complete 3+1D formulas](formulas/THREE_DIMENSIONAL.md).

<a id="four-dimensional"></a>
<a id="eq-c1-4d"></a>
<a id="obstructions-4d"></a>
<a id="eq-integer-4d"></a>
<a id="eq-l1-4d"></a>
<a id="eq-l2-4d"></a>
<a id="eq-l4"></a>
<a id="eq-t4"></a>
<a id="shared-terminal-source"></a>
<a id="four-dimensional-pair"></a>
<a id="eq-s1"></a>
<a id="eq-s2"></a>
<a id="eq-s3"></a>
<a id="stacking-4d"></a>
<a id="eq-p1-4d"></a>
<a id="eq-p2-4d"></a>
<a id="eq-p4"></a>
<a id="eq-p5"></a>
<a id="eq-t4c"></a>
<a id="eq-t4d"></a>
<a id="eq-t4a"></a>
<a id="eq-t4b"></a>

[Complete 4+1D formulas](formulas/FOUR_DIMENSIONAL.md).
