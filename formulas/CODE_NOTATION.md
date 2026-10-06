# Formula-to-code translation

This is the programmer's companion to the
[formula guide](../docs/FORMULA_GUIDE.md). The mathematical notation is defined
there; this page translates it into existing API keys, local source variables,
and compiled program names. These identifiers are scoped to their functions.
They do not introduce additional fields into the formulas. The numerical code
and its field names are unchanged by the notation refactor.

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
\check n_{d-1}=n_{d-1}+s_1\cup\bar n_{d-2}^{[1]}.
```

`Backend` accepts the native Majorana field and performs the required shift.
In contrast, readable functions with arguments `n,u,c,w,s` take the already
shifted Majorana field `u`. Apply the conversion once, according to the entry
point; do not pass a shifted field as the native API input.

Integer values retain their signs. `carry(n)` means
$`\bar n_{d-2}^{[1]}=\overline{\lfloor n_{d-2}/2\rfloor}`$.
Floors, canonical binary lifts, and exact divisions follow the mathematical
definitions. A required nonintegral quotient raises an error.

## Local names in the readable integer-layer definitions

This table applies to local variables in functions such as
`full3/lower.py`, `full3/source.py`, and `full4/product_full.py`, and to former
formula-guide abbreviations. It does not redefine the public API keys.

| Local or former name | Current mathematical notation |
|---|---|
| `n`, `m` | $`n_{d-2},n'_{d-2}`$ |
| `a=n.reduce(2)`, `b=m.reduce(2)` | $`\bar n_{d-2},\overline{n'_{d-2}}`$ |
| `h=carry(n)`, `k=carry(m)` | $`\bar n_{d-2}^{[1]},\overline{n'_{d-2}}^{[1]}`$ |
| `W` | $`\check\omega_2`$ |
| `u`, `v` | $`\check n_{d-1},\check n'_{d-1}`$ |
| `c`, `cp` | $`n_d,n'_d`$ |
| `N`, `U`, `C` or `Cnew` | $`N_{d-2},\check N_{d-1},N_d`$ |
| `t` | $`\check{\mathcal E}_{d-1}=\bar n_{d-2}\cup_{d-3}\overline{n'_{d-2}}`$ |
| `q` in lower-product local variables | $`\bar n_{d-2}\cup_{d-2}\overline{n'_{d-2}}`$ |
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
product. Their current definitions are [S1–S3](../docs/FORMULA_GUIDE.md#eq-s1)
and [T4a–T4e](../docs/FORMULA_GUIDE.md#eq-t4a).

| Readable-source name or former formula label | Current mathematical expression |
|---|---|
| `B`, former $`B_4`$ | $`B_4`$ |
| `K`, former $`K_4`$ | $`B_4^\psi`$ |
| `beta_open(u)`, local `b` in `full3/source.py:blocks`, former $`j_4`$ | $`\beta^\circ\check n_3`$ |
| Former $`A_4`$ | $`\check{\mathcal O}_4=d\check n_3`$ |
| Background integer carry, former $`v_3`$ | $`\beta_{s_1}\check\omega_2`$ |
| `alpha`, former $`\alpha_3`$ | $`\overline{\beta_{s_1}\check\omega_2}`$ |
| `hw`, former $`h_\omega`$ | $`\overline{\beta_{s_1}\check\omega_2}^{[1]}`$ |
| `ell(w,s)`, former $`\ell^\omega_3`$ | $`\overline{\beta\omega_2}+s_1\omega_2`$ |
| Background `P`, former $`\mathcal P_s(W)`$ | $`\mathcal P_{s_1}(\check\omega_2)`$ |
| `Bp`, former $`B'`$ | $`B'_4=B_4(n'_2,\check n'_3)`$ |
| `la`, dictionary key `lambda`, former $`\lambda`$ | $`\lambda_3`$ |
| `r`, `rp` in `collected_blocks` | $`\bar B_4,\overline{B'_4}`$ |
| `l` in `collected_blocks` | $`\bar\lambda_3`$ |
| Former $`R`$ | Ordered integer product $`n'_2n_2`$ |
| Former $`D`$ | $`\Delta B_4=d\lambda_3-n'_2n_2`$ |
| `Db` | $`\overline{\Delta B_4}`$ |
| `V5`, `Phi5`, `Pi5`, `epsilon5` | $`\mathcal V_5,\Phi_5,\Pi_5,\varepsilon_5`$ |
| `Zvalue`, `binary_phase` | Evaluation of $`Z_5`$ |

The variable `H` returned by `full3/source.py:blocks` is the **complete binary
source block** $`\mathcal A_6`$, including its complex-fermion terms. It is not
just $`\mathcal H_6`$. The other returned entries `Q,Pn,Wnn` are
$`\mathcal Q_6`$, $`\mathcal P_{s_1}(\check\omega_2)n_2`$, and
$`\widetilde{\check\omega_2}n_2^2`$, respectively, with the coefficient
transports specified in the formulas. `high_source16` returns their weighted
integer numerator with weights `8,4,1,2`; divide that value by sixteen to
obtain the phase. The $`4+1`$D terminal
source additionally retains the ordered cubic term $`n_2^3/12`$.

## 3+1D parameter fields

The physical $`3+1`$D fields are $`n_1,\check n_2,n_3`$. The shared source
instead consumes the constructed fields in
[T3b–T3c](../docs/FORMULA_GUIDE.md#eq-t3b):

| Earlier notation or construction | Current notation |
|---|---|
| $`\mathfrak n,\mathfrak u,\mathfrak c`$ on the triangle; output of `fields_on_triangle` | $`n_2^\triangle,\check n_3^\triangle,n_4^\triangle`$ |
| $`\mathfrak n,\mathfrak u,\mathfrak c`$ on the interval; output of `fields_on_interval` | $`n_2^I,\check n_3^I,n_4^I`$ |
| $`\theta,\phi,\chi`$ | $`\theta_1,\theta'_1,\chi_1`$ |
| Former $`J_5=F_5(\mathfrak n,\mathfrak u)`$ | $`\mathcal O_5[n_2^\triangle,\check n_3^\triangle]`$ |
| Former $`\mathcal H_4`$ acting on that source | $`(\mathsf h_4^{(2)})^*`$ |

The parameterized arguments `NN,UU,CC` of `high_blocks` have degrees two,
three, and four. `lift3_source` and `lift3_product` construct the respective
interval and triangle fields; the runtime then evaluates `high6` and performs
the signed integration. The correction $`D_3`$, the triangle term $`g_2`$,
and the older fermion-coordinate change $`\kappa_3`$ keep their names.
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

The coordinate string `ca` selects the default representative defined by
[M3–M11](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#eq-m3). The string `operator`
selects the paired source and product after the explicit change in
[M12](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#eq-m12).
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

## Equation-to-program index

| Formula family | API stage or readable entry point | Compiled targets |
|---|---|---|
| $`\mathcal O_d`$; [L1](../docs/FORMULA_GUIDE.md#eq-l1) | `source`, stage `majorana` | `source_3_majorana`, `source_4_majorana` |
| $`\mathcal O_{d+1}`$; [L2–L4](../docs/FORMULA_GUIDE.md#eq-l2) | `source`, stage `fermion` | `source_3_fermion`, `source_4_fermion` |
| $`\mathcal E_{d-1}`$; [P1–P2](../docs/FORMULA_GUIDE.md#eq-p1) | `product`, stage `majorana` | `product_3_majorana`, `product_4_majorana` |
| $`\mathcal E_d`$; [P3–P5](../docs/FORMULA_GUIDE.md#eq-p3) | `product`, stage `fermion` | `product_3_fermion`, `product_4_fermion` |
| $`\widehat{\mathcal O}_5,\widehat{\mathcal E}_4`$; [T3](../docs/FORMULA_GUIDE.md#eq-t3) | `full3/source.py:source16,product16` | `lift3_source`, `lift3_product`, `high6` |
| $`\widehat{\mathcal O}_6`$; [T4](../docs/FORMULA_GUIDE.md#eq-t4) | `full4/product_full.py:full_source48` and runtime assembly | `high6` |
| $`\widehat{\mathcal E}_5`$; [T4a–T4d](../docs/FORMULA_GUIDE.md#eq-t4a) | `full4/product_full.py:phase48` | `nonbinary4`, `rho4`, `tensor4` |
| Closed-Majorana $`\mathcal O,\mathcal E`$; [M1–M12](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#eq-m1) | `ClosedMajoranaBackend`, `majorana_complete.py` | `majorana_{q}_{operation}_{coordinate}` |
| fMPS source and product; [M13–M14](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#eq-m13) | `FMPS1Backend.source`, `FMPS1Backend.product` | Direct exact endpoint evaluation |

The [registry](FORMULA_REGISTRY.json) expands each family into concrete
dimensions, equation anchors, pinned source files, and actual target names.
For closed Majorana, `operation` is `majorana_source`, `majorana_product`,
`obstruction`, or `stacking`; binary operations use the `ca` target, while
phase operations retain the requested coordinate. This index describes
correspondence; the equation definitions remain in the formula guide and
its appendices.
