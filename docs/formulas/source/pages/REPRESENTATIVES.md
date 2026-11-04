# Changes of cochain representative

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

All changes here act on the source and stacking correction together.

## 3+1D: physical terminal formulas

The current guide uses the [geometric pairing coordinate](THREE_DIMENSIONAL_GEOMETRIC_REFERENCE.md), including its lower-field map, inverse, and finite output-face phase. The earlier [paired terminal phase map](THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md) is a retained construction step evaluated on the shifted complex-fermion inputs. Both conversions are required; the current lower product is the compact geometric formula.

## 3+1D: earlier complex-fermion coordinate



<a id="eq-t3d"></a>

**(T3D)**

{{equation:representatives--3-1d-earlier-complex-fermion-coordinate--1}}

Its stacking correction changes at the same time:

{{equation:representatives--3-1d-earlier-complex-fermion-coordinate--2}}

The obstruction is transported by the same substitution and $`d\mathcal B_3^{\mathrm{ref}}`$.
In particular, $`n_1=0`$ alone does not remove this coordinate change when
$`s_1\ne0`$.

## 4+1D: historical source convention



Before the operator reordering below, the earlier obstruction function is related to the displayed $`\mathcal O_6`$ by


<a id="eq-t4e"></a>

**(T4E)**

{{equation:representatives--4-1d-historical-source-convention--3}}

The right-hand side is evaluated in the current convention; the subtraction recovers the earlier obstruction function without an additional symbol for it.
The corresponding terminal redefinition contributes $`\Delta B_5^{\mathrm{ref}}`$ to the stacking correction.
The cubic term in (T4E) is retained separately in the later formulas; it is not a coboundary.

<a id="operator-phase-4d"></a>

## 4+1D: preceding operator phase

The first step from the supplied full terminal formula is the operator-ordering change

{{equation:representatives--4-1d-operator-phase-in-the-current-guide--4}}

The inverse subtracts the same half-valued cochain.
The obstruction function and stacking twister change together:

{{equation:representatives--4-1d-operator-phase-in-the-current-guide--5}}

The actual stacked output is used in the last line. This yields the displayed c, c-gamma, and c-psi operator factors. The other terms are regrouped with all integer carries retained. This operator-ordering step introduces no additional output coboundary.

<a id="compact-majorana-phase-4d"></a>

## 4+1D: current compact Majorana phase

The guide then applies the single [explicit phase change](FOUR_DIMENSIONAL_MAJORANA_PHASE.md)
$`\nu_5\mapsto\nu_5-B_5[\widetilde{n}_3,n_4]`$.
Its source changes by $`-d_{s_1}B_5`$ and its product by $`-\Delta B_5`$,
evaluated on the same actual lower stacking output. The inverse adds
$`B_5`$; every lower decoration and lower product is fixed.

The [general](FOUR_DIMENSIONAL.md#stacking-4d) and
[self-stacking](FOUR_DIMENSIONAL_SELF_STACKING.md) formulas include this
change in each of the three lower physical contributions. The source,
product, and their zero-p+ip restrictions therefore use one phase
coordinate. The output coboundary already documented below precedes this
step and remains included; no new output gauge is imposed here.

## Terminal phase changes



For fixed lower decorations, solve each obstruction modulo the permitted
gauge and lower-layer changes. A nonzero cochain may be exact; only a
nontrivial final obstruction class rules out the decoration. Stack accepted
representatives using the paired product and reduce by the same equivalences.

For a terminal phase change $`\nu\mapsto\nu+B`$, with
lower fields and their product fixed, the source and correction transform
together:

{{equation:representatives--terminal-phase-changes--6}}

A change of a lower decoration must also be substituted into every higher
source and product. These coordinate rules concern the full equations,
not only the abstract group obtained in an example.

The separate [programmer translation](../../formulas/CODE_NOTATION.md) records
how the formulas correspond to existing variables and compiled operations.

Before the compact-Majorana coordinate change, the terminal 4+1D Majorana contribution uses the
[explicit output coboundary](FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md).
It changes the output cochain by an exact phase and leaves the obstruction
and every other designated contribution unchanged. Its inverse adds the
same displayed coboundary.
