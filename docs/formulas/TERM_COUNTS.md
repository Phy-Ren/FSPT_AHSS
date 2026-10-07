# Expanded term counts and exact reductions

This census expands the coefficient tables and finite polynomials in the
[formula reference](../FORMULA_GUIDE.md). A specified MS word counts once;
a summation sign, a completion polynomial, or a named finite packet does
not count once.

## Counting boundary

- Distribute sums in multilinear cup and MS arguments. Expand the displayed
  lower obstruction and stacking polynomials, finite coefficient sets, and
  nonstandard helper definitions.
- Keep standard differentials, Bocksteins, and the declared physical
  coordinates. A whole canonical binary lift or second digit is nonlinear:
  retain its boundary and record the terms inside it separately. Splitting
  that boundary would change the formula.
- A nested cup expression and its fully flattened ordinary-MS expansion
  have different term counts. The tables explicitly identify which is
  being counted. For example, a square of a five-term lower source has
  25 distributed nested-cup terms, but its strict MS expansion can have
  814 words before collection.
- Physical face products already printed as scalar polynomials are counted
  separately from cochain operations. A factored row is expanded; it is
  not counted as one term.
- Keep each physical contribution separate, in the order c, c gamma,
  c psi, gamma, gamma psi, psi. No cancellation across those contributions
  is used to improve a count.

The reference before this iteration is commit
[`e5aa4bc`](https://github.com/Phy-Ren/FSPT_AHSS/tree/e5aa4bc3d12cb5e615bdd176dd935c68196db73c).
Raw occurrences can include zero and repeated terms. They measure the
size of a particular expansion, not the number of independent operations,
the smallest possible formula, or the cost of the production calculation.

## 2+1D and lower layers

One specified nested cup/MS composition or explicit physical-face product counts as one atom. Expand sums, outputs, named finite polynomials, lower correction symbols and Delta. The physical fields and their fixed modifiers are the primitive coordinate names. Ordinary differentials and Bocksteins retain their stated scopes. A named derivative carry is expanded using its displayed law. Degree-impossible and closed-input zero terms are removed. Collect literal duplicate binary terms modulo two.

The tower-expanded column additionally substitutes the displayed lower laws for derivatives of physical inputs. Protected integer-lift boundaries remain intact. Delta notation is expanded for both counts.

| Dimension | Law and physical part | Primitive atoms, baseline → adopted | Tower-expanded atoms, baseline → adopted |
|---|---|---:|---:|
| 2+1D | O2 gamma | 0 → 0 | 0 → 0 |
| 2+1D | O3 gamma | 2 → 2 | 2 → 2 |
| 2+1D | O4 c | 3 → 3 | 4 → 4 |
| 2+1D | O4 c-gamma | 1 → 1 | 4 → 4 |
| 2+1D | O4 gamma (half) | 5 → 5 | 5 → 5 |
| 2+1D | O4 gamma (quarter) | 2 → 2 | 2 → 2 |
| 2+1D | E1 gamma | 0 → 0 | 0 → 0 |
| 2+1D | E2 gamma | 2 → 2 | 2 → 2 |
| 2+1D | E3 c (half) | 5 → 5 | 5 → 5 |
| 2+1D | E3 c-gamma (half) | 15 → 15 | 22 → 22 |
| 2+1D | E3 gamma (half) | 19 → 13 | 19 → 13 |
| 2+1D | E3 gamma (quarter) | 8 → 8 | 8 → 8 |
| 2+1D | E3 gamma (eighth) | 3 → 3 | 3 → 3 |
| 3+1D | O2 psi | 0 → 0 | 0 → 0 |
| 3+1D | O3 psi | 2 → 2 | 2 → 2 |
| 3+1D | O4 gamma | 3 → 3 | 3 → 3 |
| 3+1D | O4 gamma-psi | 2 → 2 | 2 → 2 |
| 3+1D | O4 psi | 5 → 5 | 5 → 5 |
| 3+1D | E1 psi | 0 → 0 | 0 → 0 |
| 3+1D | E2 psi | 2 → 2 | 2 → 2 |
| 3+1D | E3 gamma | 2 → 2 | 2 → 2 |
| 3+1D | E3 gamma-psi | 5 → 5 | 5 → 5 |
| 3+1D | E3 psi | 18 → 18 | 20 → 20 |
| 4+1D | O3 psi | 0 → 0 | 0 → 0 |
| 4+1D | O4 psi | 3 → 3 | 3 → 3 |
| 4+1D | O5 gamma | 3 → 3 | 3 → 3 |
| 4+1D | O5 gamma-psi | 2 → 2 | 4 → 4 |
| 4+1D | O5 psi | 13 → 13 | 14 → 14 |
| 4+1D | E2 psi | 0 → 0 | 0 → 0 |
| 4+1D | E3 psi | 2 → 2 | 2 → 2 |
| 4+1D | E4 gamma | 2 → 2 | 2 → 2 |
| 4+1D | E4 gamma-psi | 6 → 5 | 8 → 6 |
| 4+1D | E4 psi | 29 → 27 | 31 → 29 |

Protected whole-lift interiors are listed separately in
[the lower-layer census data](term_census/LOWER_TERM_COUNTS.json).
For example, the cubic Delta has three outer lift occurrences and
ten interior binary monomials; it is not assigned a one-term cost.

## 3+1D terminal obstruction and stacking

This table uses a **fully flattened ordinary-MS form for the half-valued
cochain blocks**. All finite packets and actual lower stacked outputs are
substituted. Exact collection removes typed zero words and groups words
that define identical binary cochains. The normalization rule in the
coefficient appendices now includes this collection. Concise nested cup
expressions in the principal formulas remain available.

| Law | Contribution | Raw half MS words | After exact collection | Additional integer-cup terms | Explicit scalar face terms |
|---|---|---:|---:|---:|---:|
| O5 | c | 50 | 35 | 0 | 0 |
| O5 | c gamma | 814 | 168 | 0 | 0 |
| O5 | c psi | 2,974 | 841 | 0 | 0 |
| O5 | gamma | 26 | 12 | 4 | 0 |
| O5 | gamma psi | 6,241 | 2,276 | 7 | 0 |
| O5 | psi | 1,493 | 583 | 12 | 10,827 |
| E4 | c | 267 | 139 | 0 | 0 |
| E4 | c gamma | 26,720 | 2,916 | 0 | 0 |
| E4 | c psi | 10,501 | 1,422 | 0 | 0 |
| E4 | gamma | 365 | 67 | 6 | 0 |
| E4 | gamma psi | 76,485 | 16,015 | 59 | 0 |
| E4 | psi | 25,535 | 6,479 | 26 | 4,094 |

The half-valued MS blocks total **11,598 → 3,915** for O5 and
**139,873 → 27,038** for E4. These totals exclude the separately listed
integer-cup and scalar-face columns. In particular, the pure p+ip source
completion contains 10,825 scalar face monomials, and the product completion
contains 4,094. They are not counted as a single y term or as the smaller
number of factored rows. O5 also contains two explicitly signed integer
face products, included in its scalar-face column.

The integer-cup column substitutes each auxiliary exact-quotient numerator;
whole lifts stay intact, with their interior expressions recorded in the
term data. Thus that column is not an invitation to distribute a binary
lift over an integer sum.

The full term lists, with physical input expressions, are in
[the census data](term_census/README.md). Every removal is an equality of
normalized cochains; no cohomology quotient or change of phase is used.

## 4+1D terminal obstruction and stacking

The counts below measure **raw additive occurrences after the specified
formula definitions and finite indices have been expanded**. They do not
count a source-completion symbol or a finite path as one term. They are
not the number of independent terms, the size of a shortest formula, or
an estimate of the running time of an implementation that reuses results.

One specified ordinary cup, MS, or differential monomial counts once.
A nested product with no additive choice is one monomial. Declared
physical input/output fields, their decorations, and standard Bockstein
operations remain legitimate inputs. Steenrod squares and every named
polynomial are expanded. Canonical lifts and floor digits keep their
scope: their displayed interior summands are counted separately, without
applying an invalid linear expansion to the lift. Repeated subexpressions
are counted each time they occur. Physical face-binomial monomials form a
separate column in the JSON.

The complete source completion contains 1,086 indexed residual brackets.
Expanding each bracket at this boundary gives 7,673 ordinary-operation
occurrences. Its numerical term has 5,602 physical face-binomial
occurrences after expanding the coordinate differences. Thus its complete
raw count is

```math
1086\times7673+5602=8\,338\,480.
```

This large number precedes cancellations between pulled-back cochains.
For comparison, the numerical term alone has 1,784 collected physical
binary-digit monomials after also expanding its signed generalized
binomials. That is only one part of the source completion; it is not a
count or a lower bound for the complete source.

### Complete terminal contributions

The exact integers in the following table use the current reduced word
table, the lower-layer identities, the strict-root path cancellation,
and the Majorana-only branch cancellation. The JSON also records the
larger expansion of the previous unpruned definitions.

| Contribution | Bosonic obstruction, degree six | Bosonic stacking, degree five |
|---|---:|---:|
| Complex fermions | 3 | 69 |
| Complex fermions–Majorana | 25 | 20 |
| Complex fermions–p+ip | 299 | 52 |
| Majorana | 91 | 535,219 |
| Majorana–p+ip | 1,100 | 79,005,396,933,194,467 |
| p+ip | 8,338,535 | 18,584,875,760,063,481 |

These are exact **occurrence counts for this expansion procedure**.
The collected scalar normal forms of the full mixed and p+ip stacking
terms have not been materialized. In particular, the large raw numbers
do not assert that this many nonzero or indispensable terms remain.

### Reproducing the finite count

The [counting data](term_census/four_dimensional/FOUR_DIMENSIONAL_COUNT_DATA.json) specifies the count of each fully expanded kernel and
tensor coefficient for each possible number of nonzero branch bits.
The supplied standard-library scripts independently derive these weights
from the literal formula expressions and all fixed coefficient rows,
then recompute the path multiplicities and the table. Run the following
commands in `docs/formulas/term_census/four_dimensional/`:

```text
python derive_four_dimensional_weights.py
python derive_four_dimensional_weights.py --current
python replay_four_dimensional_census.py
```

All inputs are supplied beside the scripts. No private source, network
access, external package, or project checkout is needed. The weight
derivation includes all 970 numerical rows, the 453 source words, the
original and reduced Majorana tables, and the 226 tensor rows. The first
two commands compare their independently derived weights with the JSON;
the third recomputes the aggregate table.

For a multilinear operation with argument counts $`m_1,\ldots,m_q`$,
the outer occurrence count is $`\prod_i m_i`$. Interior counts propagate
with the same product of the other argument counts. Addition adds counts.
A canonical-lift or floor boundary has one outer value but retains the
complete interior count. This last rule is bookkeeping of a nonlinear
expression, not a mathematical claim that the nonlinear operation is
additive.

For a path with $`h`$ branch bits equal to one, the decoded p+ip part of
each input Majorana face contains $`2+2h`$ raw physical-factor terms.
The surviving unbranched grid-path multiplicities at lengths zero through
five are

```math
1,\quad116,\quad4176,\quad41760,\quad83520,\quad0.
```

Multiply each length-$`J`$ contribution with $`h`$ nonzero bits by
$`\binom Jh`$. A kernel coefficient additionally has 358 final-grid
choices; a tensor coefficient does not. This gives the recurrence

```math
\sum_{J=0}^{4} a_J
 \sum_{h=0}^{J}\binom Jh
 \bigl[358\,r(2+2h)+t(2+2h)\bigr],
```

where $`r`$ and $`t`$ denote the numerical occurrence counts in the
linked counting data, separately for each physical contribution. They are
counting functions, not added symbols in the physical formulas. For the
Majorana contribution only $`J=0`$ survives and the tensor count is zero.
Its remaining binary kernel has $`358\times1495=535210`$ raw occurrences;
the explicitly expanded quarter numerator contributes nine more.

Every residual bracket, standard-operation word, tensor row, lower
polynomial and lift interior is included in these weights. The path count
alone is never used as the formula-term count.

### Exact reductions already checked

The ordinary source table decreases from 1,176 to 1,090 rows: 101 to 85
Majorana rows, and 1,075 to 1,005 mixed rows. The Majorana reduction uses
only the already required closed backgrounds; the selected mixed rows
agree for fully independent binary Majorana and differential inputs.
Their colored use therefore preserves the stated factor ancestry.

Separately, the archived zero-background Majorana-source part of the
terminal product decreases from 179,225 to 106,147 ordinary words by exact
typed cochain identities. Its collected scalar expansion has 209,477
monomials. This component is not the complete stacking formula.

No phase convention or numerical classification changes in these
identities. Further reduction should first remove zero and equal terms
inside the indexed mixed and p+ip coefficients, rather than printing the
raw expansion or introducing another name for it.

## What changed in the formulas

The explicit 3+1D relative complex-fermion tables also lose their
degree-impossible rows: 186 → 132 open-Majorana rows and 58 → 22
lower-fermion rows. Every removed word has an empty normalized cut table.

The two output-minus-input combinations in the 2+1D bosonic twister now
use the already defined Delta. Its cubic term is

```math
-\frac18\Delta\!\left[\overline{n_1^3}\right].
```

This saves notation without claiming a reduction in expanded terms.
The canonical bar remains inside Delta. The antiunitary polynomial in
the same contribution is reduced from 12 cup summands to six explicit
physical face products, with exact equality on all closed degree-one
inputs. The impossible closed-input Sq-squared term is removed.

In 4+1D the empty degree-(4,3) cup-4 term is removed from the mixed
complex-fermion twister, and two identical diagonal products cancel in
its pure p+ip contribution. The ordinary Majorana source coefficient
table is reduced from 1,176 to 1,090 words (85 Majorana and 1,005 mixed),
using only the already stated closed backgrounds.

The 4+1D physical path sums omit equal binary branch pairs. Their proof
and strict index condition are in
[Physical face indices](FOUR_DIMENSIONAL_PHYSICAL_PATHS.md#exact-removal-of-zero-path-pairs).
This reduces path occurrences from 675,018,894,633 to 1,687,337 and removes
length five entirely. A path still contains many formula terms: these
numbers are never substituted for a term count. The pure Majorana part
simplifies further: every positive-length path cancels, so its binary
coefficient requires only the length-zero contribution.

## Next simplification targets

1. The 4+1D terminal coefficient construction: collect normalized physical
   face contributions before expanding its repeated finite paths. The raw
   expansion is very redundant; the reduced path count is only a first step.
2. The 3+1D mixed Majorana–p+ip half twister: its strict MS form still has
   16,015 words after identical-operation collection. Search for short cup
   identities and coupled changes of representative, rather than introduce
   another name for the same long polynomial.
3. The pure p+ip face polynomials and the 4+1D source completion: retain
   useful factorization while reducing the number of actual monomials.

All adopted changes in this iteration are exact cochain identities or
literal regroupings. The existing paired source/product phase maps and
numerical classification results are unchanged. No claim of a globally
minimal formula is made.
