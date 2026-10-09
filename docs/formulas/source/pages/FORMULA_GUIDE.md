# FSPT obstruction functions and stacking twisters

Each dimension has its own formula reference. Obstructions, general twisters,
and self-stacking twisters are linked together below; the self-stacking
formulas live in separate files. The notation is shared, while physical
fields are defined separately in each dimension.

| Dimension | Obstruction functions | Stacking twisters | Self-stacking twisters |
|---|---|---|---|
| 2+1D | [Obstructions](formulas/TWO_DIMENSIONAL.md#obstructions-2d) | [Twisters](formulas/TWO_DIMENSIONAL.md#stacking-2d) | [Self-stacking](formulas/TWO_DIMENSIONAL_SELF_STACKING.md) |
| 3+1D | [Obstructions](formulas/THREE_DIMENSIONAL.md#obstructions-3d) | [Twisters](formulas/THREE_DIMENSIONAL.md#stacking-3d) | [Self-stacking](formulas/THREE_DIMENSIONAL_SELF_STACKING.md) |
| 4+1D | [Obstructions](formulas/FOUR_DIMENSIONAL.md#obstructions-4d) | [Twisters](formulas/FOUR_DIMENSIONAL.md#stacking-4d) | [Self-stacking](formulas/FOUR_DIMENSIONAL_SELF_STACKING.md) |

[How self-stacking determines the group](formulas/ROOT_POWER_PRESENTATIONS.md)
explains the hypotheses, complete root relations, and gauge reductions.
[The simplification record](formulas/SIMPLIFICATION_PROGRESS.md) distinguishes
reductions already incorporated in these formulas from remaining targets.

## Notation

The backgrounds are $`\omega_2\in Z^2(G_b,\mathbb Z_2)`$ and
$`s_1\in Z^1(G_b,\mathbb Z_2)`$, held fixed during stacking.
A subscript gives the cochain degree. Each dimension defines its own
fields; their physical roles are not inferred from another section.
The physical labels $`c,\gamma,\psi`$ mean, respectively,
complex fermion, Majorana, and p+ip. The fixed order for resolved
contributions is $`c,c\gamma,c\psi,\gamma,\gamma\psi,\psi`$;
absent contributions are omitted. The mixed labels refer to signs from fermionic
anticommutation between the indicated microscopic origins. They are not
labels for the variables appearing after lower equations are substituted.
In particular, a c-gamma factor may depend on a Majorana differential;
expanding that differential does not by itself change the exchange origin. A mixed superscript identifies an interaction between the indicated physical layers. The pieces are parts of the full
cochain equation; they need not be separately closed. In the p+ip sections they refer to the
displayed shifted Majorana field; rewriting it in native fields redistributes
some mixed terms.

<a id="conventions-and-coordinates"></a>

### Arithmetic and modifiers

A prime denotes the second stacking input. On an individual field it is
placed outside the modifier: $`\bar n'_j,\widetilde n'_j,\check n'_j`$. The outputs are $`N_j`$ and
$`\mathcal V_j`$. A hat denotes the additive phase:
$`\nu_j=\exp(2\pi i\widehat\nu_j)`$ and
$`\mathcal V_j=\exp(2\pi i\widehat{\mathcal V}_j)`$, with
both hatted phases in $`\mathbb R/\mathbb Z`$. The same convention applies to
phase obstructions $`\widehat{\mathcal{𝒪}}`$ and corrections
$`\widehat{\mathcal{ℰ}}`$.

A bar means reduction modulo two; a tilde means the second binary digit:

{{equation:formula-guide--arithmetic-and-modifiers--1}}

Floors are mathematical floors, including for negative integers. Integer
lifts are implicit, so tilde always has the meaning above. A check denotes
an explicitly defined shift. The background shift is

<a id="eq-c1"></a>

**(C1)**

{{equation:formula-guide--arithmetic-and-modifiers--2}}

### Integer lifts are implicit in integer arithmetic

A named binary cochain in an integer expression means its canonical
$`0,1`$ lift. No lift symbol is needed. Sums, differences, differentials, and
higher cups in such an expression use integer arithmetic and its stated
coefficient transport. If an entire compound expression must first be
reduced, its bar stays explicit. For binary values, for example,

{{equation:formula-guide--integer-lifts-are-implicit-in-integer-arithmetic--3}}

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

{{equation:formula-guide--integer-lifts-are-implicit-in-integer-arithmetic--4}}

The second term is retained for a nonclosed cochain. Negative or
otherwise degree-impossible higher cups are zero in the explicit
[interval-cut definition](formulas/OPERATIONS.md#interval-cuts).

Each layer defines its differential and stacking twister completely before the higher layers
use them. In a higher formula, each defined operation is a mathematical
input: its lower-layer polynomial need not be expanded again. Its
coefficient system and chosen cochain representative remain those of its
definition. This is particularly useful for the final bosonic formulas.
The purpose is to make the structure reusable, not to remove the
complexity of evaluating it. Definitions and identities belong at the
layer where the structure first appears.
The source and stacking identities explain how successive layers fit
together, so later formulas can use established structures without
repeating their derivations. The cochain differential $`d`$ is distinct from an AHSS differential
$`d_r`$ and its specified cochain representative.

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

The [term census](formulas/TERM_COUNTS.md) keeps these defined differentials and twisters
in the primary count and distinguishes supplementary counts obtained by
substituting lower equations. An arbitrary named polynomial or finite sum
still contributes its actual number of terms.

<a id="integral-quadratic-cochain"></a>

### The repeated integer quadratic cochain

For an untwisted integer cochain $`x`$ of degree $`r\ge2`$, define

{{equation:formula-guide--the-repeated-integer-quadratic-cochain--5}}

It has three terms and degree $`r+2`$. Its parity is
$`\mathrm{Sq}^2\bar x+\omega_2\bar x`$; its integer value retains the
information required by a quarter-valued phase. The
[exact addition and stacking identities](formulas/QUADRATIC_REFINEMENTS.md)
explain its reuse in the obstruction and twister. It is a specified
cochain operation, with integer lifts retained, rather than an additional
physical field. In counts that retain this structure, its three defining
cups are recorded once and their full substitutions are reported separately.

## Finite definitions and coordinate maps

- 3+1D: [obstruction word coefficients](formulas/THREE_DIMENSIONAL_WORD_INDICES.md), [stacking word coefficients](formulas/THREE_DIMENSIONAL_PRODUCT_WORD_INDICES.md), [complex-fermion stacking coefficients](formulas/THREE_DIMENSIONAL_PRODUCT_CF_WORDS.md).
- 3+1D pure p+ip face coefficients: [obstruction](formulas/THREE_DIMENSIONAL_INTEGER_SOURCE_FACES.md), [stacking](formulas/THREE_DIMENSIONAL_INTEGER_PRODUCT_FACES.md).
- 4+1D: [obstruction word coefficients](formulas/FOUR_DIMENSIONAL_MAJORANA_WORD_COEFFICIENTS.md), [Majorana stacking MS terms](formulas/FOUR_DIMENSIONAL_MAJORANA_STACKING_WORDS.md), [Majorana canonical lifts](formulas/FOUR_DIMENSIONAL_MAJORANA_STACKING_LIFTS.md), [mixed and p+ip stacking coefficients](formulas/FOUR_DIMENSIONAL_STACKING_COEFFICIENTS.md).
- 4+1D construction data: [binary coefficients](formulas/FOUR_DIMENSIONAL_BINARY_COEFFICIENTS.md), [physical face indices](formulas/FOUR_DIMENSIONAL_PHYSICAL_PATHS.md), [tensor coefficients](formulas/FOUR_DIMENSIONAL_TENSOR_COEFFICIENTS.md).
- [4+1D pure-source construction](formulas/SOURCE_OPERATIONS.md#source-completion).
- [4+1D pure-source physical face coefficients](formulas/FOUR_DIMENSIONAL_Y6_FACES.md).
- [Root powers and the abelian stacking group](formulas/ROOT_POWER_PRESENTATIONS.md)
- [Transported 3+1D zero-p+ip self-twister](formulas/THREE_DIMENSIONAL_MAJORANA_SELF_STACKING.md)
- [Closed-Majorana formulas](formulas/MAJORANA_AND_ENDPOINTS.md), [4+1D zero-p+ip self-stacking](formulas/FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md)
- [Exact Majorana carry reduction](formulas/FOUR_DIMENSIONAL_MAJORANA_CARRY_REDUCTION.md)
- [Higher cups and finite sums](formulas/OPERATIONS.md), [fixed coefficients](formulas/COEFFICIENTS.md)
- [Changes of representative](formulas/REPRESENTATIVES.md)
- [Fermionic coboundary and stacking](formulas/COBOUNDARY_STACKING_COMPATIBILITY.md)
- [Integer quadratic cochains and their polarization](formulas/QUADRATIC_REFINEMENTS.md)
- [Further simplification targets](formulas/NEXT_SIMPLIFICATION_TARGETS.md)
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

[Complete 3+1D formulas](formulas/THREE_DIMENSIONAL.md). The current geometric pairing coordinate and its full phase transport are fixed in [the paired comparison](formulas/THREE_DIMENSIONAL_GEOMETRIC_REFERENCE.md).

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

## Maintaining this reference

The [maintained source](formulas/source/README.md) generates these reader pages
and their programmer translation. Shared display equations are stored once;
this guide and its generated pages are published together. Frozen coefficient
archives remain verification evidence, with their coordinate conventions
stated explicitly.
