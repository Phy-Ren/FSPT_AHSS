# Formula-to-code translation

**Phase convention:** the formulas use the [physical convention](../docs/FORMULA_GUIDE.md#phase-convention); the runtime paths relate to it as stated [below](#phase-convention-of-the-runtime).

This is the programmer's companion to the
[formula guide](../docs/FORMULA_GUIDE.md). The mathematical notation is defined
there; this page translates it into existing API keys, local source variables,
and compiled program names. These identifiers are scoped to their functions.
They do not introduce additional fields into the formulas. The numerical kernels keep their own representatives and arguments. To compare a runtime value with a displayed formula, apply the maps in [From the code to the formulas](#from-the-code-to-the-formulas); the abstract classification and stacking groups do not depend on them.

The explicit $`4+1`$D Majorana stacking expression additionally uses the
[displayed output coboundary](../docs/formulas/FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md):
subtract $`d_{s_1}B_4^{\mathrm{out}}`$ from the runtime terminal product cochain, and add
it for the inverse comparison. The obstruction is unchanged since
$`d_{s_1}^2=0`$. This is a documented representative conversion; it does not
change any runtime algorithm or stored classification/stacking result.

See the [runtime interface](README.md#runtime-interface) for calling conventions
and the [operation registry](FORMULA_REGISTRY.json) for exact source hashes and
compiled targets.

<a id="phase-convention-of-the-runtime"></a>

## Phase convention of the runtime

The reader formulas and every executable path use the
[unified physical convention](../docs/FORMULA_GUIDE.md#phase-convention).
Their representatives and coordinates are related as follows.

| Path | Relation to the displayed formulas |
|---|---|
| Closed-Majorana programs `majorana_1_*` (2+1D, `fspt/majorana_complete.py`, `fspt/formulas.py`) | Equal. The stacking law contains the lattice term $`-\tfrac14[s_1n_1n'_1]_2`$. |
| Closed-Majorana programs `majorana_2_*` (3+1D) | Equal; the CF field `c` is the physical occupation $`n_3`$. |
| Closed-Majorana programs `majorana_3_*` (4+1D) | The obstruction is equal; the CF field `c` is the physical occupation $`n_4`$, and the product uses the displayed complex-fermion law $`N_4=n_4+n'_4+\mathcal E_4^\gamma`$. Its phase differs from the displayed closed law by the P-move rephasing $`\tfrac12(n_3\cup_2n_3)\cup_4n'_4`$, the explicit [output coboundary](../docs/formulas/FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md) and the [phase convention](../docs/formulas/FOUR_DIMENSIONAL_MAJORANA_PHASE.md). |
| Publication programs, 4+1D (`fspt/data/full_formula`, compiled from `formulas/publication_source`) | Equal after the [maps below](#from-the-code-to-the-formulas); the CF slot `c` holds $`n_4+y`$, with $`y`$ given below. |
| Publication programs, 3+1D | Equal after the [maps below](#from-the-code-to-the-formulas); the CF slot `c` holds $`n_3+B_3`$, $`B_3=n_2\cup_1n_2`$. The source and product are the parameter integrals of the [finite construction](../docs/formulas/THREE_DIMENSIONAL_TERMINAL.md), with the orientation of [(O8)](../docs/formulas/OPERATIONS.md#eq-o8) recorded in the call signs of `lift3_source` and `lift3_product`. |

No routine of the complete GAP engine computes a 3+1D phase of
denominator four, eight or sixteen itself: every such value reaches the
group engine through the backend. The native GAP shortcuts with quarter- or
finer-valued phases (`AFSFullCubePrimitive`, `AFSFullBinaryPrimitive`,
`AFSFullCFSquareLift`, `AFSFullCharacterMCLift`) act only in 4+1D, and the
native 3+1D shortcut `AFSFullClosedCFSource3` is half-valued. The separate
campaign engine (`gap/classification.g` with the generated formula data and
the p+ip O5 programs `gap/pip_o5_*.g`) is not used by the complete engine; it
is kept only to replay archived campaigns.

## Exact simplifications in the reader formulas

The source exchange identity in 3+1D uses the complete differential of the
code's complex-fermion input, not only its pure-Majorana part. Its standalone verifier checks that a 25-word
MS sum equals the seven displayed words.
The ordinary source cups also use that same complete lower differential.

The open-Majorana self-stacking reductions in 3+1D and 4+1D preserve the
phase representative exactly. The 3+1D whole binary lift is evaluated
before conversion to the integer phase coefficient. The 4+1D coefficient
normalization identifies `B4(n,0)` with its already defined integer-only
part `B4psi(n)`; it does not distribute a protected lift or change its
arguments. The public coefficient receipts record these identities.
These algebraic reductions do not change a representative; the maps of the next section are applied separately when comparing a reader formula with the numerical kernels.

<a id="from-the-code-to-the-formulas"></a>

## From the code to the formulas

The publication kernels evaluate the bosonic layer with the complex-fermion
argument $`n_3+B_3`$ in 3+1D and $`n_4+y`$ in 4+1D, where
$`B_3=n_2\cup_1n_2`$ and

```math
y=n_3\cup_2n_3+x,\qquad x=(s_1\cup_1[\lfloor n_2/2\rfloor]_2)[n_2]_2+s_1(([n_2]_2\cup_1[n_2]_2)\cup_2[n_2]_2)+\mathop{\mathrm{MS}}\nolimits_{12131}([n_2]_2\cup_1[n_2]_2,s_1,[n_2]_2).
```

The kernels use the parity polynomial $`\\mathcal O_5+dy`$ of their compact
form; its difference from the complete F-move count $`\\mathcal O_5`$ is $`dy`$.
The formula pages use the occupations $`n_3,n_4`$ themselves.

**3+1D.** The complete map is stated in
[From the code to the 3+1D formulas](../docs/formulas/THREE_DIMENSIONAL_GEOMETRIC_REFERENCE.md),
together with the [native phase representative](../docs/formulas/THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md)
of the code. The displayed lower fields $`\mathcal O_4`$ and $`\mathcal E_3`$ are
evaluated by [`formulas.py`](../docs/formulas/verification/three_dimensional/formulas.py).
For the product, compute $`\mathcal B_2`$ on the actual signed fields of the
separate states; the code output is $`N_3+B_3[N_2]+d\mathcal B_2`$. The code phases in
[`code_phases`](../docs/formulas/verification/three_dimensional/code_phases)
name the code argument `n_3+B_3`, and
[`check_code.py`](../docs/formulas/verification/three_dimensional/check_code.py)
checks the complete map pointwise.

<a id="eq-t3d"></a>

The parameter construction of the code evaluates its complex-fermion argument
after the further map

{{equation:representatives--3-1d-earlier-complex-fermion-coordinate--1}}

and its stacking correction changes at the same time:

{{equation:representatives--3-1d-earlier-complex-fermion-coordinate--2}}

The obstruction is transported by the same substitution and $`d\mathcal B_3^{\mathrm{ref}}`$.

**4+1D.** In this paragraph, write $`c=n_4+y`$ for the code argument; its
differential is $`\mathcal O_5+dy`$. The source of the code construction is

<a id="eq-t4e"></a>

{{equation:representatives--4-1d-historical-source-convention--3}}

in terms of the obstruction $`\mathcal O_6`$ written with the argument $`c`$
before the three changes below; the cubic term is retained separately and is
not a coboundary. The changes are applied in order:

1. the operator ordering $`\nu_5\mapsto\nu_5+\tfrac12c\cup_4dc`$;
2. the [phase convention](../docs/formulas/FOUR_DIMENSIONAL_MAJORANA_PHASE.md)
   with the code argument, $`\nu_5\mapsto\nu_5-B_5[n_3]-\tfrac12s_1c`$;
3. the occupation change

```math
\begin{aligned}
\nu_5\mapsto\nu_5-\tfrac12\big[&n_4\cup_3y+n_4\cup_4dy+(n_3\cup_2n_3)\cup_3x+(n_3\cup_2n_3)\cup_4dx
 +(n_3\cup_2n_3)\cup_4d(n_3\cup_2n_3)\\
 &+x\cup_4dx+dx\cup_5\big(\mathcal O_5+d(n_3\cup_2n_3)\big)+s_1x\big].
\end{aligned}
```

The result is the displayed obstruction; the three changes together contain
the displayed phase convention $`-B_5[n_3]-\tfrac12s_1n_4`$.
For the product, the stacked code argument is $`N_4+y_N+d(n_3\cup_3n'_3)`$,
with $`N_4`$ of the displayed law. The formula pages remove
$`d(n_3\cup_3n'_3)`$ by the complex-fermion gauge transformation of the
bosonic stacking law and use the P-move rephasing $`\tfrac12y\cup_4n'_4`$;
together with $`\Delta`$ of the three changes this gives the displayed twister.

The [4+1D verifier](../docs/formulas/coefficients/verify_four_dimensional_bare_formulas.py)
checks the identities behind the third change for arbitrary cochains.

Each change $`\nu\mapsto\nu+B`$ adds $`d_{s_1}B`$ to the obstruction and
$`\Delta B`$ to the stacking correction, evaluated on the actual lower fields of the stacked state.
The explicit $`4+1`$D Majorana stacking expression additionally uses the
[displayed output coboundary](../docs/formulas/FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md).

## Public integer-layer API

For spatial dimension $`d=3,4`$, the source call accepts the following entries
in `fields`. Product calls take the same decoration keys in `left` and `right`,
with `w,s` in `background`.

| Mathematical field | API key | Degree and coefficients |
|---|---|---|
| $`n_{d-2}`$ | `n` | Degree $`d-2`$, signed integers with twist $`s_1`$ |
| $`c_{d-1}=n_{d-1}+s_1\cup[\lfloor n_{d-2}/2\rfloor]_2`$ | `a` | Degree $`d-1`$, binary Majorana input |
| $`n_3+B_3`$ in 3+1D; $`n_4+y`$ in 4+1D | `c` | Degree $`d`$, binary CF argument of the code |
| $`\omega_2`$ | `w` | Degree two, binary extension cocycle |
| $`s_1`$ | `s` | Degree one, binary antiunitary cocycle |

For a product, `right['n']`, `right['a']`, `right['c']` represent
$`n'_{d-2},c'_{d-1}`$ and the same CF convention. The runtime packs them into compiled fields
`m,b,cp`. Thus **compiled input `b` is the Majorana field $`c'_{d-1}`$ of the lower state**;
it is not the parity variable called `b` inside some readable definitions.
The returned product value is a correction, not the entire stacked field $`N_j`$.
The sums of the lower fields and the phase sum are added by the caller.

The additive phase $`\nu_{d+1}`$ is not one of the five lower source
inputs. A terminal source or product call returns a `Fraction` modulo one,
representing $`\mathcal O_{d+2}`$ or
$`\mathcal E_{d+1}`$.
The same symbol $`\nu_{d+1}`$ denotes the multiplicative phase; exponentiating the additive value gives its $`U(1)`$ value.
The readable reference functions
ending in `16` or `48` instead return integer numerators with the indicated
denominator; their raw values must be divided accordingly.

The API key `a` holds the binary cochain $`c_{d-1}`$, not the Majorana
decoration $`n_{d-1}`$ itself. The internal conversion uses the background
[C1](../docs/FORMULA_GUIDE.md#eq-c1) and

{{equation:code-notation--public-integer-layer-api--1}}

`Backend` accepts $`c_{d-1}`$ and forms $`n_{d-1}`$.
In contrast, readable functions with arguments `n,u,c,w,s` take the
decoration $`n_{d-1}`$ itself as `u`. Apply the conversion once, according to the entry
point; do not pass $`n_{d-1}`$ as the API input `a`.

Integer values retain their signs. `carry(n)` means
$`[\lfloor n_{d-2}/2\rfloor]_2`$.
Floors, canonical binary representatives, and exact divisions follow the
mathematical definitions. A required nonintegral quotient raises an error.

The formulas leave a named binary field's zero-or-one integer
representative implicit. The source code performs these lift operations
explicitly:

| Source-code expression | Mathematical expression in integer arithmetic |
|---|---|
| `x.lift()` for a named binary cochain | $`x`$ |
| `(x+y).lift()` after binary addition | $`[x+y]_2`$ |
| `cup(x,y,i).lift()` with binary inputs and binary cup | $`[x\cup_i y]_2`$ |
| `cup(x.lift(),y.lift(),i)` with signed integer cup | $`x\cup_i y`$ |
| `x.d().lift()` with binary differential | $`[dx]_2`$ |
| `x.lift().d()` with integer differential | $`dx`$ |
| `x.reduce(2)` for an integer cochain | $`[x]_2`$ |

This convention removes notation from the formulas, not arithmetic from
the evaluator. In particular, the two cup expressions and the two
differentials in this table are distinct operations. In particular,
$`[\cdot]_2`$ on a whole integer numerator fixes the same reduction boundary
that the reference evaluator expresses with explicit `reduce(2)` and
`lift()` calls.

## Local names in the readable integer-layer definitions

This table applies to local variables in functions such as
`full3/lower.py`, `full3/source.py`, and `full4/product_full.py`. It does
not redefine the public API keys.

| Local name | Mathematical notation |
|---|---|
| `n`, `m` | $`n_{d-2},n'_{d-2}`$ |
| `a=n.reduce(2)`, `b=m.reduce(2)` | $`[n_{d-2}]_2,[n'_{d-2}]_2`$ |
| `h=carry(n)`, `k=carry(m)` | $`[\lfloor n_{d-2}/2\rfloor]_2,[\lfloor n'_{d-2}/2\rfloor]_2`$ |
| `W` | $`\widetilde{\omega}_2`$ |
| `u`, `v` | $`n_{d-1},n'_{d-1}`$ |
| `c`, `cp` | $`n_d,n'_d`$ |
| `N`, `U`, `C` or `Cnew` | $`N_{d-2},N_{d-1},N_d`$ |
| `t` | $`\mathcal E_{d-1}=[n_{d-2}]_2\cup_{d-3}[n'_{d-2}]_2`$ |
| `q` in lower-product local variables | $`[n_{d-2}]_2\cup_{d-2}[n'_{d-2}]_2`$ |
| `e` | $`\mathcal E_d`$ |

The local product variable `q` is a cochain. It is unrelated to the degree
index $`q`$ in the closed-Majorana appendix. Source-function arguments are
also scoped: `full3/source.py:blocks` receives fields of degrees two, three,
and four, even when constructed from a physical $`3+1`$D input.

## Shared source and 4+1D residuals

The following names belong to the shared six-cochain source or the $`4+1`$D
product. Their current definitions are [S1–S3](../docs/formulas/FOUR_DIMENSIONAL.md#eq-s1)
and [T4a–T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4a); the
[source of the code construction](#eq-t4e) is related to them above.

| Readable-source name | Mathematical expression |
|---|---|
| `B` | $`\beta_4`$ |
| `K` | $`\beta_4^\psi`$ |
| `beta_open(u)`, local `b` in `full3/source.py:blocks` | $`\beta^-n_3`$ |
| `alpha` | $`[\beta_{s_1}\widetilde{\omega}_2]_2`$ |
| `hw` | $`[\lfloor \beta_{s_1}\widetilde{\omega}_2/2\rfloor]_2`$ |
| `ell(w,s)` | $`[\beta\omega_2]_2+s_1\omega_2`$ |
| Background `P` | $`\mathfrak P_{s_1}(\widetilde{\omega}_2)`$ |
| `Bp` | $`\beta'_4=\beta_4(n'_2,n'_3)`$ |
| `la`, dictionary key `lambda` | $`\lambda_3`$ |
| `r`, `rp` in `collected_blocks` | $`[\beta_4]_2,[\beta'_4]_2`$ |
| `l` in `collected_blocks` | $`[\lambda_3]_2`$ |
| `Db` | $`[\Delta \beta_4]_2`$ |
| `V5` | $`V_5`$, the binary quarter numerator; $`\mathcal V_5`$ denotes the stacked bosonic phase |
| `Phi5` | The expanded lower-field portion of the half-valued bracket in [T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4d) |
| `Pi5` | The expanded integer terms accompanying $`V_5`$ in the quarter-valued bracket of [T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4d) |
| `epsilon5` | The expanded complex-fermion terms in the half-valued bracket of [T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4d) |
| `Zvalue`, `binary_phase` | Evaluation of $`Z_5`$ |

Frozen coefficient files and runtime identifiers keep their own spellings.
In serialized field labels, `B_3` and `B_4` mean the carries $`\beta_3`$ and
$`\beta_4`$, not the cochain $`B_3`$ of the 3+1D formulas; bars, digits, primes, and physical superscripts are preserved.
In particular, `B_4^psi` and `barB4gamma` denote
$`\beta_4^\psi`$ and $`[\beta_4^\gamma]_2`$. The runtime function
`R5` evaluates the phase primitive $`B_5`$.

The following local names refer to parts of the expanded
[4+1D source](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4):

| Local name | Location in the expanded formula |
|---|---|
| Local `H` | The sum of the half-valued physical contributions, including $`\mathrm{Sq}^2c+\omega_2c`$ for the code argument $`c=n_4+y`$ |
| Local `Q` | All quarter-valued source terms, including the separately displayed subtraction |
| `cartan_word` | The complete reduced background-and-digit polynomial in that subtraction |

In particular, the source variable `H` includes the complex-fermion terms.
The other entries `Pn,Wnn`
returned by `blocks` are $`\mathfrak P_{s_1}(\widetilde{\omega}_2)n_2`$ and
$`\widetilde{\omega}_2n_2^2`$, with the stated coefficient transports.
`high_source16` returns the weighted integer numerator for `H,Q,Pn,Wnn`
with weights `8,4,1,2`; divide it by sixteen to obtain the phase. The 4+1D
source additionally retains $`n_2^3/12`$.

## 3+1D parameter fields

The physical $`3+1`$D fields are $`n_1,n_2,n_3`$.
The code parameter construction takes $`n_3+B_3`$
in its CF slot and the stacked argument $`N_3+B_3[N_2]+d\mathcal B_2`$.
Its raised fields are defined in
[T3a–T3c](../docs/formulas/THREE_DIMENSIONAL_TERMINAL.md#eq-t3b):

| Construction or local name | Notation |
|---|---|
| Output of `fields_on_triangle` | $`n_2^\triangle,n_3^\triangle,n_4^\triangle`$ |
| Output of `fields_on_interval` | $`n_2^I,n_3^I,n_4^I`$ |
| `theta()`, `phi()`, `chi()` in `prism.py` | $`\theta_1,\theta'_1,\chi_1`$ |

The parameterized arguments `NN,UU,CC` of `high_blocks` have degrees two,
three, and four. `lift3_source` and `lift3_product` construct the respective
interval and triangle fields; the runtime then evaluates `high6` and performs
the signed integration. The reader guide prints the entire finite expression for both terminal
operations. Its upward marks denote these same constructed components,
not independent lifts of the three fields. The notation-to-runtime map is:

| Reader evaluation | Existing construction and integration |
|---|---|
| $`\mathop{\mathrm{ev}}\nolimits_5`$ | `lift3_source`, then the signed six-simplex interval sum |
| $`\mathop{\mathrm{ev}}\nolimits_4`$ | `lift3_product`, then the signed fifteen-simplex triangle sum |
| $`\uparrow n_1,\uparrow n_2,\uparrow n_3`$ | The three components `n,u,c` returned by the relevant lift |
| $`\beta_4^\uparrow,\beta_4^{\psi,\uparrow}`$ | The same integer residuals `B,K` on those components |

The full six-cochain's cubic term has zero transgression on both parameter
spaces, so the runtime may omit it without changing either phase. The
linear and quadratic fractional terms are already collapsed into the
explicit sixteenth-valued source and negative eighth-valued product in
the reader guide; they are not omitted.
The [maps above](#from-the-code-to-the-formulas) must also be applied, including
[the complex-fermion map](#eq-t3d) with $`\mathcal B_3^{\mathrm{ref}}`$ (computed by
`kappa3`), to the source and product together.

## Closed-Majorana and fMPS backends

The closed-Majorana formulas use a different, explicitly named phase
representative. In `fspt/majorana_complete.py` and `ClosedMajoranaBackend`,
$`q=1,2,3`$ denotes the Majorana degree and spatial dimension is $`q+1`$.

| Backend or local field | Closed-Majorana notation |
|---|---|
| `a`, `b` | $`n_q,n'_q`$ |
| `c`, `cp` | $`n_{q+1},n'_{q+1}`$ |
| `w`, `s` | $`\omega_2,s_1`$ |
| `p=a.beta()`, `r=p.reduce()` | $`\beta n_q,[\beta n_q]_2`$ |
| `second_carry(a)` | $`\beta^+n_q`$ |
| `n=a+b` in `intrinsic` | $`N_q`$ |
| `u=cup(a,b,q)` in `intrinsic` | $`n_q\cup_qn'_q`$ |
| `t=cup(a,b,q-1)` in `intrinsic` | $`n_q\cup_{q-1}n'_q`$ |
| `gamma(a,w,s)` | Pure Majorana source $`\mathcal O^\gamma_{q+3}`$ |
| `operator_gauge(c)` | $`\tfrac12n_{q+1}\cup_{q+1}dn_{q+1}`$ |

The coordinate string `operator` evaluates the displayed phase source and
product in the [2+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-2d) and
[3+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-3d) sections, and the displayed
source in the [4+1D](../docs/formulas/MAJORANA_AND_ENDPOINTS.md#majorana-4d) section;
the 4+1D product is related as stated in the table above. The `ca` targets
evaluate the same laws without the operator ordering of the complex fermions,
which is the single-state term `operator_gauge(c)`. The binary lower laws
agree in both. The documentation's reader default does not change the
runtime's default argument.
`ClosedMajoranaBackend` divides the compiled terminal numerator by eight.
Its output is not silently substituted into the separate integer-layer
publication coordinate.

The degree-zero fMPS endpoint in `fspt/full_formula/fmps1.py` uses:

| fMPS field name | Endpoint notation |
|---|---|
| `gamma=a` | $`n_0`$ |
| `beta=c` | $`n_1`$ |
| `alpha=v` | $`\nu_2`$ |

Here `beta` names a **field**, whereas $`\beta`$ elsewhere in the formulas
denotes the Bockstein operation. The coordinate identifier remains
`fmps1-turzillo-you-eq44`. Renaming its mathematical fields does not change
the fMPS representative or assert a dictionary to a different manuscript
phase coordinate. Its residual parity quotient remains part of classification.
Similarly, the keys `beta` and `gamma` in specialized gauge calls denote gauge
parameters, not automatically a Bockstein or a pure Majorana phase source.

## Expanded transfer polynomials

The reader appendices write out the polynomial that this source function
evaluates.

| Source function | Location of the expanded expression |
|---|---|
| `Lstar` | The shuffle contribution written directly in $`L_5`$, [K11](../docs/formulas/TERMINAL_TRANSFER.md#eq-k11) |

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
| $`\mathcal O_5,\mathcal E_4`$; [T3](../docs/formulas/THREE_DIMENSIONAL.md#eq-t3) | `full3/source.py:source16,product16` | `lift3_source`, `lift3_product`, `high6` |
| $`\mathcal O_6`$; [T4](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4) | `full4/product_full.py:full_source48` and runtime assembly | `high6` |
| $`\mathcal E_5`$; [T4a–T4d](../docs/formulas/FOUR_DIMENSIONAL.md#eq-t4a) | `full4/product_full.py:phase48` | `nonbinary4`, `rho4`, `tensor4` |
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

The full integer-layer runtime returns the entire obstruction or
product in its existing publication coordinate. The guide's gamma / psi /
gamma-psi split of the lower formulas expands the same open-cochain
Steenrod operation and partitions the existing product terms. For the
terminal 4+1D source, substitute `B = beta_open(u) + K` and expand the
ordered bilinear integer cups. Sum the displayed six physical blocks to
recover the preceding `high6` coordinate plus its existing cubic term.
The [maps above](#from-the-code-to-the-formulas) then give the displayed source
and product; `R5(n3,x)` evaluates the phase-convention cochain
$`B_5[n_3]+\tfrac12s_1x`$ on the code arguments, and the product uses its value
on the actual stacked state minus the values on the upper and lower states. Using componentwise
sums is incorrect. The source and general/self product are converted together.

The 4+1D terminal product separates all freely variable complex-fermion
terms. In its remaining term `dCnew` equals the lower fermion source at
the displayed stacked state. The c-free Majorana/p+ip transfer is retained as
a combined expression; `Zvalue` is not a pure-p+ip twister. The 3+1D
terminal operations are expanded in the main guide, with the finite lift
and summation rules in the [technical file](../docs/formulas/THREE_DIMENSIONAL_TERMINAL.md).
No compiled program or coefficient table changes in this regrouping.

## Reader notation and frozen field labels

The reader formulas use $`\beta^-x=(dx-[dx]_2)/2`$ for the integer carry of a possibly nonclosed binary cochain.
Binary reduction is $`[x]_2`$, and the second binary digit is $`[\lfloor x/2\rfloor]_2`$.
The 3+1D term lists use the printed expressions as field names.
The 4+1D coefficient files retain their original field labels so their checksums and recorded calculations remain reproducible.
The formulas use the same symbol for a phase and its additive value; a phase hat in those files denotes the additive value.
In those files `\check n_2` is the Majorana decoration $`n_2`$, `\check\omega_2` is $`\widetilde{\omega}_2`$, `beta_open` denotes $`\beta^-`$, and a `tilde` field denotes the explicit second binary digit.
These are translations of labels, with no change to the cochains, coefficients, or numerical API.

## GitHub script-glyph encoding

The reader Markdown writes `\mathcal{ℰ}` and `\mathcal{𝒪}` for the same
stacking correction and obstruction denoted by `\mathcal{E}` and
`\mathcal{O}` in TeX. GitHub's native MathML display can ignore the script
font on an ASCII letter; the explicit Unicode script glyph preserves its
visible shape, including under a tilde. This is a rendering fallback,
not a different mathematical symbol or program variable.

For manuscript TeX export, replace `\mathcal{ℰ}` with `\mathcal{E}` and
`\mathcal{𝒪}` with `\mathcal{O}` before passing the formulas to LaTeX.
The replacement is literal, including inside `\widetilde{...}`.
Formula token comparisons apply the same normalization.

## Exact formula reductions and term counting

The reader formulas also apply exact normalized-cochain cancellations.
The Delta regroupings, the six-face antiunitary polynomial in 2+1D,
the empty degree-(4,3) cup-4 term, and the diagonal product cancellation
in 4+1D preserve the existing phase coordinate. The ordinary Majorana
coefficient table is reduced with its stated closed backgrounds; the
physical path sums omit identical binary branch pairs. These changes
do not require a new source/product coordinate map.

The numerical kernels evaluate checked equivalent expressions.
The [term census](../docs/formulas/TERM_COUNTS.md) distinguishes expanded
formula size, exact cochain cancellation, and raw construction occurrences;
none of these counts is a runtime estimate. Finite sums and completion
polynomials are expanded in that census rather than assigned unit cost.


## Signed carry reduction and reusable quadratic cochain

The [complete Majorana product](../docs/formulas/FOUR_DIMENSIONAL.md)
is pointwise equal to the
[face expansion](../docs/formulas/FOUR_DIMENSIONAL_MAJORANA_STACKING_FACES.md),
with the same output gauge. Its carry at degree four is the same
canonical binary-addition carry used at degree three, applied to
the binary differentials of the separate states. It is not an integer differential
of a lifted binary cochain. The four nonlinear lift boundaries must survive
translation to code.

The public [carry replay](../docs/formulas/coefficients/verify_majorana_carry_reduction.py)
uses only the face polynomial and the four explicit lift tables.
The [signed-transfer certificate](../docs/formulas/coefficients/verify_majorana_signed_transfer.py)
checks the integer chain identity and normalization. The numerical runtime
evaluates an equivalent frozen expression; the reader form does not
change computed examples.

The [quadratic cochain](../docs/formulas/QUADRATIC_REFINEMENTS.md) is the
integer sum of its three printed cups. The source substitutions and
terminal-kernel regrouping are literal identities. The optional quarter-lift
transport in that appendix is a separate, fully stated output gauge; it is
not silently applied to the runtime or to the principal formula.


## Root-power formulas and reconstruction

The [relative-power presentation](../docs/formulas/ROOT_POWER_PRESENTATIONS.md)
proves that complete marked cyclic-power relations determine the abelian
group. Its 3+1D adapted-basis construction has a reversible replay on all
602 published presentations. The replay reorganizes existing certified
integer relations; it does not re-evaluate cochains or benchmark a new
runtime. The production reconstruction uses its general reduction
backend.

The [ten-term 3+1D zero-p+ip self-stack](../docs/formulas/THREE_DIMENSIONAL_MAJORANA_SELF_STACKING.md)
is exactly equal to the general reader formula in the same
coordinates. Its standard-library verifier keeps integer Bocksteins
modulo four by lifting modulo eight before exact division. It preserves
the whole binary value of the lower obstruction in the quarter bracket.
Translations from older runtime coordinates still use the previously
specified paired maps.

The separate 4+1D closed diagonal retains its explicit output gauge
relative to the reader formula. Restricted counts never replace
the general counts for arbitrary upper and lower states, and neither zero-p+ip formula supplies a
self-stack for a state with nonzero integer decoration.

## Maintained source and complete self-stacking references

The sole editable reader source is [docs/formulas/source](../docs/formulas/source/README.md).
The builder generates the guide, dimensional pages, and this translation;
shared display equations have one maintained definition. Frozen supplier
sources and numerical regression fixtures use their own coordinates.

Complete restricted formulas are on separate pages for
[2+1D](../docs/formulas/TWO_DIMENSIONAL_SELF_STACKING.md),
[3+1D](../docs/formulas/THREE_DIMENSIONAL_SELF_STACKING.md), and
[4+1D](../docs/formulas/FOUR_DIMENSIONAL_SELF_STACKING.md). The latter two
include p+ip decoration in their stated domains. The zero-p+ip pages are
proofs or additional closed-input simplifications, not the full nonzero-p+ip law.

The 4+1D adapted-root presentation has 320 reversible two-primary replays
and 35 marked odd-extension checks. The odd check retains the factor 4t
from two additional doublings after integer-gauge alignment. This is
algebra on saved presentations, not a new execution of an optimized cochain
backend. Production reconstruction uses the general backend.

The general 3+1D exchange reduction and 4+1D mixed-quarter
polarization preserve the reader representative exactly. They do not
authorize mixing reader cochains with older numerical phase coordinates;
the same existing paired maps remain required. Exact term counts are in
the [term census](../docs/formulas/TERM_COUNTS.md).
