# Formula-to-code translation

This is the programmer's companion to the
[formula guide](../docs/FORMULA_GUIDE.md). The mathematical notation is defined
there; this page translates it into existing API keys, local source variables,
and compiled program names. These identifiers are scoped to their functions.
They do not introduce additional fields into the formulas. The numerical kernels and their field names retain the supplied representative. The guide now also uses an explicitly transported terminal phase. Compare cochains only after the [3+1D paired map](../docs/formulas/THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md) or the [4+1D operator map](../docs/formulas/REPRESENTATIVES.md#operator-phase-4d), as appropriate. These maps leave the lower decoration fields and abstract stacking groups unchanged.

The explicit $`4+1`$D Majorana stacking expression additionally uses the
[displayed output coboundary](../docs/formulas/FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md):
subtract $`d_{s_1}G_4`$ from the previous terminal product cochain, and add
it for the inverse comparison. The obstruction is unchanged since
$`d_{s_1}^2=0`$. This is a documented representative conversion; no runtime
algorithm or stored classification/stacking result was modified.

See the [runtime interface](README.md#runtime-interface) for calling conventions
and the [operation registry](FORMULA_REGISTRY.json) for exact source hashes and
compiled targets.

## Public integer-layer API

For spatial dimension $`d=3,4`$, the source call accepts the following entries
in `fields`. Product calls take the same decoration keys in `left` and `right`,
with `w,s` in `background`.

| Mathematical field | API key | Degree and coefficients |
|---|---|---|
| $`n_{d-2}`$ | `n` | Degree $`d-2`$, signed integers with twist $`s_1`$ |
| $`n_{d-1}`$ | `a` | Degree $`d-1`$, native binary Majorana field |
| $`n_d`$ | `c` | Degree $`d`$, binary complex-fermion field |
| $`\omega_2`$ | `w` | Degree two, binary extension cocycle |
| $`s_1`$ | `s` | Degree one, binary antiunitary cocycle |

For a product, `right['n']`, `right['a']`, `right['c']` represent
$`n'_{d-2},n'_{d-1},n'_d`$. The runtime packs them into compiled fields
`m,b,cp`. Thus **compiled input `b` is the second native Majorana field**;
it is not the parity variable called `b` inside some readable definitions.
The returned product value is a correction, not the entire output $`N_j`$.
The lower input sums and the phase sum are added by the caller.

The additive phase $`\widehat\nu_{d+1}`$ is not one of the five lower source
inputs. A terminal source or product call returns a `Fraction` modulo one,
representing $`\widehat{\mathcal O}_{d+2}`$ or
$`\widehat{\mathcal E}_{d+1}`$. The multiplicative phase is always
$`\nu_{d+1}=\exp(2\pi i\widehat\nu_{d+1})`$. The readable reference functions
ending in `16` or `48` instead return integer numerators with the indicated
denominator; their raw values must be divided accordingly.

The internal conversion uses [C1](../docs/FORMULA_GUIDE.md#eq-c1):

```math
\check\omega_2=\omega_2+s_1\cup s_1,\qquad
\check n_{d-1}=n_{d-1}+s_1\cup\widetilde n_{d-2}.
```

`Backend` accepts the native Majorana field and performs the required shift.
In contrast, readable functions with arguments `n,u,c,w,s` take the already
shifted Majorana field `u`. Apply the conversion once, according to the entry
point; do not pass a shifted field as the native API input.

Integer values retain their signs. `carry(n)` means
$`\widetilde n_{d-2}=\overline{\lfloor n_{d-2}/2\rfloor}`$.
Floors, canonical binary representatives, and exact divisions follow the
mathematical definitions. A required nonintegral quotient raises an error.

The formulas now leave a named binary field's zero-or-one integer
representative implicit. The source code still performs exactly the same
lift operations:

| Source-code expression | Mathematical expression in integer arithmetic |
|---|---|
| `x.lift()` for a named binary cochain | $`x`$ |
| `(x+y).lift()` after binary addition | $`\overline{x+y}`$ |
| `cup(x,y,i).lift()` with binary inputs and binary cup | $`\overline{x\cup_i y}`$ |
| `cup(x.lift(),y.lift(),i)` with signed integer cup | $`x\cup_i y`$ |
| `x.d().lift()` with binary differential | $`\overline{dx}`$ |
| `x.lift().d()` with integer differential | $`dx`$ |
| `x.reduce(2)` for an integer cochain | $`\bar x`$ |

This convention removes notation from the formulas, not arithmetic from
the evaluator. In particular, the two cup expressions and the two
differentials in this table are distinct operations.

## Local names in the readable integer-layer definitions

This table applies to local variables in functions such as
`full3/lower.py`, `full3/source.py`, and `full4/product_full.py`, and to former
formula-guide abbreviations. It does not redefine the public API keys.

| Local or former name | Current mathematical notation |
|---|---|
| `n`, `m` | $`n_{d-2},n'_{d-2}`$ |
| `a=n.reduce(2)`, `b=m.reduce(2)` | $`\bar n_{d-2},\bar n'_{d-2}`$ |
| `h=carry(n)`, `k=carry(m)` | $`\widetilde n_{d-2},\widetilde n'_{d-2}`$ |
| `W` | $`\check\omega_2`$ |
| `u`, `v` | $`\check n_{d-1},\check n'_{d-1}`$ |
| `c`, `cp` | $`n_d,n'_d`$ |
| `N`, `U`, `C` or `Cnew` | $`N_{d-2},\check N_{d-1},N_d`$ |
| `t` | $`\check{\mathcal E}_{d-1}=\bar n_{d-2}\cup_{d-3}\bar n'_{d-2}`$ |
| `q` in lower-product local variables | $`\bar n_{d-2}\cup_{d-2}\bar n'_{d-2}`$ |
| `e`, former $`e_d`$ | $`\mathcal E_d`$ |
| Former $`F_{d+1}`$ | $`\mathcal O_{d+1}`$ |
| Former $`\Xi_{d+1}`$ | $`\mathcal O^\psi_{d+1}`$ |
| Former $`S^j`$ | $`\mathrm{Sq}^j`$ |

The local product variable `q` is a cochain. It is unrelated to the degree
index $`q`$ in the closed-Majorana appendix. Source-function arguments are
also scoped: `full3/source.py:blocks` receives fields of degrees two, three,
and four, even when constructed from a physical $`3+1`$D input.

## Shared source and 4+1D residuals

The following names belong to the shared six-cochain source or the $`4+1`$D
product. Their current definitions are [S1–S3](../docs/formulas/FOUR_DIMENSIONAL.md#eq-s1)
and [T4a–T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4a), with the
[earlier coordinate map](../docs/formulas/REPRESENTATIVES.md#eq-t4e) kept separately.

| Readable-source name or former formula label | Current mathematical expression |
|---|---|
| `B`, former $`B_4`$ | $`B_4`$ |
| `K`, former $`K_4`$ | $`B_4^\psi`$ |
| `beta_open(u)`, local `b` in `full3/source.py:blocks`, former $`j_4`$ | $`\beta^\circ\check n_3`$ |
| Former $`A_4`$ | $`\check{\mathcal O}_4=d\check n_3`$ |
| Background integer carry, former $`v_3`$ | $`\beta_{s_1}\check\omega_2`$ |
| `alpha`, former $`\alpha_3`$ | $`\overline{\beta_{s_1}\check\omega_2}`$ |
| `hw`, former $`h_\omega`$ | $`\widetilde{\beta_{s_1}\check\omega_2}`$ |
| `ell(w,s)`, former $`\ell^\omega_3`$ | $`\overline{\beta\omega_2}+s_1\omega_2`$ |
| Background `P`, former $`\mathcal P_s(W)`$ | $`\mathcal P_{s_1}(\check\omega_2)`$ |
| `Bp`, former $`B'`$ | $`B'_4=B_4(n'_2,\check n'_3)`$ |
| `la`, dictionary key `lambda`, former $`\lambda`$ | $`\lambda_3`$ |
| `r`, `rp` in `collected_blocks` | $`\bar B_4,\bar B'_4`$ |
| `l` in `collected_blocks` | $`\bar\lambda_3`$ |
| Former $`R`$ | Ordered integer product $`n'_2n_2`$ |
| Former $`D`$ | $`\Delta B_4=d\lambda_3-n'_2n_2`$ |
| `Db` | $`\overline{\Delta B_4}`$ |
| `V5` | $`\mathcal V_5`$, the binary value used in the quarter-valued product |
| `Phi5` | The expanded lower-field portion of the half-valued bracket in [T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4d) |
| `Pi5` | The expanded integer terms accompanying $`\mathcal V_5`$ in the quarter-valued bracket of [T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4d) |
| `epsilon5` | The expanded complex-fermion terms in the half-valued bracket of [T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4d) |
| `Zvalue`, `binary_phase` | Evaluation of $`Z_5`$ |

The former source-sum names are now expanded in the
[4+1D source](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4):

| Existing local or former formula name | Location in the expanded formula |
|---|---|
| Local `H`, former $`\mathcal A_6`$ | The sum of the half-valued physical contributions, including $`\mathrm{Sq}^2n_4+\omega_2n_4`$ |
| Former $`\mathcal H_6`$ | The half-valued Majorana, p+ip, and mixed contributions after subtracting those complex-fermion terms |
| Local `Q`, former $`\mathcal Q_6`$ | All quarter-valued source terms, including the separately displayed subtraction |
| `cartan_word`, former $`\mathcal C_6`$ | The complete reduced background-and-digit polynomial in that subtraction |
| Former $`\widehat{\mathcal O}^{\mathrm{base}}_6`$ | The complete source before the final ordered cubic term |

In particular, the source variable `H` includes the complex-fermion terms;
it was never just the former $`\mathcal H_6`$. The other entries `Pn,Wnn`
returned by `blocks` are $`\mathcal P_{s_1}(\check\omega_2)n_2`$ and
$`\check\omega_2n_2^2`$, with the stated coefficient transports.
`high_source16` returns the weighted integer numerator for `H,Q,Pn,Wnn`
with weights `8,4,1,2`; divide it by sixteen to obtain the phase. The 4+1D
source additionally retains $`n_2^3/12`$.

## 3+1D parameter fields

The physical $`3+1`$D fields are $`n_1,\check n_2,n_3`$. The shared source
instead consumes the constructed fields in
[T3a–T3c](../docs/formulas/THREE_DIMENSIONAL_TERMINAL.md#eq-t3b):

| Earlier notation or construction | Current notation |
|---|---|
| $`\mathfrak n,\mathfrak u,\mathfrak c`$ on the triangle; output of `fields_on_triangle` | $`n_2^\triangle,\check n_3^\triangle,n_4^\triangle`$ |
| $`\mathfrak n,\mathfrak u,\mathfrak c`$ on the interval; output of `fields_on_interval` | $`n_2^I,\check n_3^I,n_4^I`$ |
| $`\theta,\phi,\chi`$ | $`\theta_1,\theta'_1,\chi_1`$ |
| Former $`J_5=F_5(\mathfrak n,\mathfrak u)`$ | $`\mathcal O_5^\triangle`$ |
| Former $`\mathcal H_4`$ acting on that source | $`(\mathsf h_4^{(2)})^*`$ |

The parameterized arguments `NN,UU,CC` of `high_blocks` have degrees two,
three, and four. `lift3_source` and `lift3_product` construct the respective
interval and triangle fields; the runtime then evaluates `high6` and performs
the signed integration. The reader guide now prints the entire finite expression for both terminal
operations. Its upward marks denote these same constructed components,
not independent lifts of the three fields. The notation-to-runtime map is:

| Reader evaluation | Existing construction and integration |
|---|---|
| $`\mathop{\mathrm{ev}}\nolimits_5`$ | `lift3_source`, then the signed six-simplex interval sum |
| $`\mathop{\mathrm{ev}}\nolimits_4`$ | `lift3_product`, then the signed fifteen-simplex triangle sum |
| $`\uparrow n_1,\uparrow\check n_2,\uparrow n_3`$ | The three components `n,u,c` returned by the relevant lift |
| $`B_4^\uparrow,B_4^{\psi,\uparrow}`$ | The same integer residuals `B,K` on those components |

The full six-cochain's cubic term has zero transgression on both parameter
spaces, so the runtime may omit it without changing either phase. The
linear and quadratic fractional terms are already collapsed into the
explicit sixteenth-valued source and negative eighth-valued product in
the reader guide; they are not omitted.
The former $`D_3`$ and $`g_2`$ are expanded directly
in those parameter fields, with no change of the native physical $`n_3`$
coordinate. The older fermion-coordinate change $`\kappa_3`$ keeps its name.
The older coordinate change must be applied to its source and product
together; it is not implied by renaming `c` to $`n_3`$.

## Closed-Majorana and fMPS backends

The closed-Majorana formulas use a different, explicitly named phase
representative. In `fspt/majorana_complete.py` and `ClosedMajoranaBackend`,
$`q=1,2,3`$ denotes the Majorana degree and spatial dimension is $`q+1`$.

| Backend or local field | Current closed-Majorana notation |
|---|---|
| `a`, `b` | $`n_q,n'_q`$ |
| `c`, `cp` | $`n_{q+1},n'_{q+1}`$ |
| `w`, `s` | $`\omega_2,s_1`$ |
| `p=a.beta()`, `r=p.reduce()` | $`\beta n_q,\overline{\beta n_q}`$ |
| `second_carry(a)` | $`\beta^+n_q`$ |
| `n=a+b` in `intrinsic` | $`N_q`$ |
| `u=cup(a,b,q)` in `intrinsic` | $`n_q\cup_qn'_q`$ |
| `t=cup(a,b,q-1)` in `intrinsic` | $`n_q\cup_{q-1}n'_q`$ |
| `gamma(a,w,s)` | Pure Majorana source $`\widehat{\mathcal O}^\gamma_{q+3}`$ |
| `operator_gauge(c)` | $`\tfrac12n_{q+1}\cup_{q+1}dn_{q+1}`$ |

The coordinate string `operator` selects the reader's displayed phase
source and product in the [2+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-2d),
[3+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-3d), and
[4+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-4d) sections.
The existing `ca` target remains unchanged and is the coordinate denoted
by the superscript `old` there. Recover it by subtracting the displayed
single-state rephase from the source and its full stacking change from
the product: [2+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#eq-m12-2d),
[3+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#eq-m12), and
[4+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#eq-m12-4d).
The binary lower laws agree in both coordinates. The documentation's
reader default does not change the runtime's default argument.
`ClosedMajoranaBackend` divides the compiled terminal numerator by eight.
Its output is not silently substituted into the separate integer-layer
publication coordinate.

The degree-zero fMPS endpoint in `fspt/full_formula/fmps1.py` uses:

| Existing fMPS field name | Current endpoint notation |
|---|---|
| `gamma=a` | $`n_0`$ |
| `beta=c` | $`n_1`$ |
| `alpha=v` | $`\widehat\nu_2`$ |

Here `beta` names a **field**, whereas $`\beta`$ elsewhere in the formulas
denotes the Bockstein operation. The coordinate identifier remains
`fmps1-turzillo-you-eq44`. Renaming its mathematical fields does not change
the fMPS representative or assert a dictionary to a different manuscript
phase coordinate. Its residual parity quotient remains part of classification.
Similarly, the keys `beta` and `gamma` in specialized gauge calls denote gauge
parameters, not automatically a Bockstein or a pure Majorana phase source.

## Expanded source and transfer polynomials

The following single-use formula names were removed from the reader's
appendices. Their polynomial terms remain in the stated expression; the
source functions and coefficient lists retain their existing identifiers.

| Former formula label | Present location of the expanded expression |
|---|---|
| $`\mathcal X_7`$ | The explicit $`\mathcal W_4`$ word sum in $`M_7`$, [S4](../docs/formulas/SOURCE_OPERATIONS.md#eq-s4); [all 453 words](../docs/formulas/COEFFICIENTS.md#eq-y2) |
| $`V_6,\Theta_6`$ | The two complete terms multiplied by sixteen inside the twisted differential in the numerator of $`R_7`$, [S6](../docs/formulas/SOURCE_OPERATIONS.md#eq-s6) |
| $`B^{\mathrm{par}}_7`$ | The complete reduced binary polynomial with coefficient eight in that same numerator |
| $`\widehat M_7`$ | The $`8M_7`$ term and the explicit integer Bockstein bracket with coefficient four in that numerator |
| $`I_6`$ | The final even integer numerator, multiplied by one half, in $`\rho_6`$, [K1–K3](../docs/formulas/TERMINAL_TRANSFER.md#eq-k1) |
| $`J_6`$ | The entire binary $`\Delta[\cdots]`$ bracket in that same kernel |
| $`Q^{\mathrm{int}}_5,K^-_5,A^{\mathrm{pair}}_4,G^0_5`$ | Their full terms in the numerator defining $`D^0_5`$, [K10](../docs/formulas/TERMINAL_TRANSFER.md#eq-k10) |
| $`L^\star_5`$ | The shuffle contribution written directly in $`L_5`$, [K11](../docs/formulas/TERMINAL_TRANSFER.md#eq-k11) |

No retained numerical coefficient, word, quotient, or signed transport is
changed by expanding these names. In particular, a bar on a whole integer
numerator fixes the same reduction boundary that the reference evaluator
expresses with explicit `reduce(2)` and `lift()` calls.

## Equation-to-program index

| Formula family | API stage or readable entry point | Compiled targets |
|---|---|---|
| 3+1D $`\mathcal O_3`$; [L1](../docs/formulas/THREE_DIMENSIONAL.md#eq-l1) | `source`, stage `majorana` | `source_3_majorana` |
| 4+1D $`\mathcal O_4`$; [L1](../docs/formulas/FOUR_DIMENSIONAL.md#eq-l1-4d) | `source`, stage `majorana` | `source_4_majorana` |
| 3+1D $`\mathcal O_4`$; [L2–L3](../docs/formulas/THREE_DIMENSIONAL.md#eq-l2) | `source`, stage `fermion` | `source_3_fermion` |
| 4+1D $`\mathcal O_5`$; [L2–L4](../docs/formulas/FOUR_DIMENSIONAL.md#eq-l2-4d) | `source`, stage `fermion` | `source_4_fermion` |
| 3+1D $`\mathcal E_2`$; [P1–P2](../docs/formulas/THREE_DIMENSIONAL.md#eq-p1) | `product`, stage `majorana` | `product_3_majorana` |
| 4+1D $`\mathcal E_3`$; [P1–P2](../docs/formulas/FOUR_DIMENSIONAL.md#eq-p1-4d) | `product`, stage `majorana` | `product_4_majorana` |
| 3+1D $`\mathcal E_3`$; [P3](../docs/formulas/THREE_DIMENSIONAL.md#eq-p3) | `product`, stage `fermion` | `product_3_fermion` |
| 4+1D $`\mathcal E_4`$; [P4–P5](../docs/formulas/FOUR_DIMENSIONAL.md#eq-p4) | `product`, stage `fermion` | `product_4_fermion` |
| $`\widehat{\mathcal O}_5,\widehat{\mathcal E}_4`$; [T3](../docs/formulas/THREE_DIMENSIONAL.md#eq-t3) | `full3/source.py:source16,product16` | `lift3_source`, `lift3_product`, `high6` |
| $`\widehat{\mathcal O}_6`$; [T4](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4) | `full4/product_full.py:full_source48` and runtime assembly | `high6` |
| $`\widehat{\mathcal E}_5`$; [T4a–T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4a) | `full4/product_full.py:phase48` | `nonbinary4`, `rho4`, `tensor4` |
| Closed-Majorana source/product; [3+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-3d), [4+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-4d), [2+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-2d) | `ClosedMajoranaBackend`, `majorana_complete.py` | `majorana_{q}_{operation}_{coordinate}` |
| fMPS source and product; [M13–M14](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#eq-m13) | `FMPS1Backend.source`, `FMPS1Backend.product` | Direct exact endpoint evaluation |

The [registry](FORMULA_REGISTRY.json) expands each family into concrete
dimensions, equation anchors, pinned source files, and actual target names.
For closed Majorana, `operation` is `majorana_source`, `majorana_product`,
`obstruction`, or `stacking`; binary operations use the `ca` target, while
phase operations retain the requested coordinate. This index describes
correspondence; the equation definitions remain in the formula guide and
its appendices.

## Physical contribution regrouping

The full integer-layer runtime still returns the entire obstruction or
product in its existing publication coordinate. The guide's gamma / psi /
gamma-psi split of the lower formulas expands the same open-cochain
Steenrod operation and partitions the existing product terms. For the
terminal 4+1D source, substitute `B = beta_open(u) + K` and expand the
ordered bilinear integer cups. Sum the displayed six physical blocks to
recover `high6` plus its existing cubic term.

The 4+1D terminal product separates all freely variable complex-fermion
terms. In its remaining term `dCnew` equals the lower fermion source at
the displayed output. The c-free Majorana/p+ip transfer is retained as
a combined expression; `Zvalue` is not a pure-p+ip twister. The 3+1D
terminal operations are expanded in the main guide, with the finite lift
and summation rules in the [technical file](../docs/formulas/THREE_DIMENSIONAL_TERMINAL.md).
No compiled program or coefficient table changes in this regrouping.

## GitHub script-glyph encoding

The reader Markdown writes `\mathcal{ℰ}` and `\mathcal{𝒪}` for the same
stacking correction and obstruction denoted by `\mathcal{E}` and
`\mathcal{O}` in TeX. GitHub's native MathML display can ignore the script
font on an ASCII letter; the explicit Unicode script glyph preserves its
visible shape, including under a hat or check. This is a rendering fallback,
not a different mathematical symbol or program variable.

For manuscript TeX export, replace `\mathcal{ℰ}` with `\mathcal{E}` and
`\mathcal{𝒪}` with `\mathcal{O}` before passing the formulas to LaTeX.
The replacement is literal, including inside `\widehat{...}` and
`\check{...}`. Formula token comparisons apply the same normalization.

## Exact formula reductions and term counting

The reader formulas also apply exact normalized-cochain cancellations.
The Delta regroupings, the six-face antiunitary polynomial in 2+1D,
the empty degree-(4,3) cup-4 term, and the diagonal product cancellation
in 4+1D preserve the existing phase coordinate. The ordinary Majorana
coefficient table is reduced with its stated closed backgrounds; the
physical path sums omit identical binary branch pairs. These changes
do not require a new source/product coordinate map.

The numerical kernels retain the previously checked equivalent expressions.
The [term census](../docs/formulas/TERM_COUNTS.md) distinguishes expanded
formula size, exact cochain cancellation, and raw construction occurrences;
none of these counts is a runtime estimate. Finite sums and completion
polynomials are expanded in that census rather than assigned unit cost.
