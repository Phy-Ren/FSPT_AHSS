# Finite construction of the 3+1D terminal phase

This file records the finite construction in the supplied terminal phase coordinate. The [current physical formulas](THREE_DIMENSIONAL.md#three-dimensional) use the explicit [paired phase change](THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md). Throughout this construction, the unqualified obstruction and stacking symbols refer to the supplied coordinate; apply that map and its output coboundary to compare with the guide.
All parameter fields below are auxiliary mathematical cochains. Their degrees
do not change the physical roles of the fields in that section.

<a id="three-dimensional-pair"></a>

## Bosonic obstruction

The physical phase equation is

{{equation:three-dimensional-terminal--bosonic-obstruction--1}}

Its obstruction is the following fixed finite sum, with the
[integration rule specified in Operations](OPERATIONS.md#parameter-integration):

<a id="eq-t3"></a>

**(T3)**

{{equation:three-dimensional-terminal--bosonic-obstruction--2}}

## Bosonic stacking correction

The physical phase stacks as

{{equation:three-dimensional-terminal--bosonic-stacking-correction--3}}

The correction evaluates the same polynomial on the triangle fields:

<a id="eq-t3-product"></a>

**(T3 product)**

{{equation:three-dimensional-terminal--bosonic-stacking-correction--4}}

## Polynomial evaluated in both formulas

The same degree-six polynomial is evaluated on the interval fields for
the obstruction and on the triangle fields for stacking:

<a id="eq-aux-terminal-source"></a>

**(Auxiliary phase source)**

{{equation:three-dimensional-terminal--polynomial-evaluated-in-both-formulas--5}}

Its fields, residuals, and finite constituent formulas are specified below.

<a id="physical-field-evaluation"></a>
## Evaluation notation in the retained construction

The retained construction can denote its two fixed sums as
$`\mathop{\mathrm{ev}}\nolimits_5=\tau_I`$ for the obstruction and
$`\mathop{\mathrm{ev}}\nolimits_4=\tau_\triangle`$ for stacking. Both act on
a degree-six cochain. The subscript gives the output degree: the first
uses the six signed paths on an interval times a five-simplex; the second
uses the fifteen signed paths on a triangle times a four-simplex. Their
orientations and coefficient transports are exactly (O8).

The upward marks identify components of the **fixed lift of the complete
physical input**. The obstruction lift uses one input, whereas the stacking
lift uses both inputs and their displayed lower stacking corrections:

| Symbol in this construction | Obstruction evaluation | Stacking evaluation |
|---|---|---|
| $`\uparrow n_1`$ | $`n_2^I`$ | $`n_2^\triangle`$ |
| $`\uparrow\check n_2`$ | $`\check n_3^I`$ | $`\check n_3^\triangle`$ |
| $`\uparrow n_3`$ | $`n_4^I`$ | $`n_4^\triangle`$ |
| $`B_4^\uparrow`$ | $`B_4^I`$ | $`B_4^\triangle`$ |
| $`B_4^{\psi,\uparrow}`$ | $`B_4^{\psi,I}`$ | $`B_4^{\psi,\triangle}`$ |
| $`\mathcal{𝒪}_5^\psi[\uparrow n_1]`$ | $`\mathcal{𝒪}_5^{\psi,I}`$ | $`\mathcal{𝒪}_5^{\psi,\triangle}`$ |

Every entry on the right is defined explicitly below. In particular,
$`\uparrow\check n_2`$ and $`\uparrow n_3`$ include the mixed terms and
fixed cochain fills in those definitions. They are not independently
chosen linear suspensions of the individual fields. Backgrounds are pulled
from the physical base throughout.

This notation changes neither the cochains nor their representative. It
introduces no physical decoration or integer-lift convention. The arrow
components have degrees two, three, and four, with coefficients
$`\mathbb Z_{s_1},\mathbb Z_2,\mathbb Z_2`$, respectively. Products,
Bocksteins, and reductions inside the evaluation are formed before the
signed sum, using the arithmetic of the shared degree-six polynomial.
The fractional terms written outside these construction brackets
are precisely the signed identities in the final section below.

## Auxiliary integer residuals

The following residuals are untwisted integer cochains on the parameter
space. The definitions are local to the auxiliary fields:

<a id="eq-aux-residual"></a>

**(Auxiliary integer residuals)**

{{equation:three-dimensional-terminal--auxiliary-integer-residuals--6}}

## Auxiliary parameter fields

This construction uses cochains on an interval or triangle times the
physical base. They are **auxiliary**, not additional physical decorations.
A superscript $`J\in\{I,\triangle\}`$ always marks them: $`n_2^J`$ is
integer, while $`\check n_3^J,n_4^J`$ are binary. The physical $`n_2`$ in
this section remains Majorana decoration.

On the oriented triangle $`012`$, the integer one-cocycles
$`\theta_1,\theta'_1`$ have edge values $`(01,12,02)=(1,0,1),(0,1,1)`$.
The binary $`\chi_1`$ has values $`(0,0,1)`$ and satisfies
$`d\chi_1=\bar\theta_1\bar\theta'_1`$. Backgrounds and physical
fields are pulled from the base; parameter cochains are pulled from the
triangle. Integer parameter cochains act through their reductions inside
binary expressions.

<a id="eq-t3b"></a>

**(T3B)**

{{equation:three-dimensional-terminal--auxiliary-parameter-fields--7}}

For the interval, $`\theta_1(01)=1`$ and the second input is absent:

{{equation:three-dimensional-terminal--auxiliary-parameter-fields--8}}

The following binary degree-five source is evaluated on these auxiliary
fields. Its superscript keeps it separate from the physical terminal
phase obstruction $`\widehat{\mathcal{𝒪}}_5`$:

<a id="eq-aux-o5"></a>

**(Auxiliary source)**

{{equation:three-dimensional-terminal--auxiliary-parameter-fields--9}}

<a id="eq-aux-pip5"></a>

**(Auxiliary p+ip source)**

{{equation:three-dimensional-terminal--auxiliary-parameter-fields--10}}

The auxiliary complex-fermion fields now follow. Their complete
corrections are written directly, without additional named sum wrappers.

<a id="eq-t3a"></a>

**(T3A)**

{{equation:three-dimensional-terminal--auxiliary-parameter-fields--11}}

<a id="eq-t3c"></a>

**(T3C)**

{{equation:three-dimensional-terminal--auxiliary-parameter-fields--12}}

All brackets defining these binary fields are evaluated modulo two.
The interval and triangle sums and their coefficient transports are fixed
in [Operations](OPERATIONS.md#parameter-integration).

## Signed fractional terms

The extra integer terms have the exact signed transgressions

| Auxiliary term | $`\tau_I`$ | $`\tau_\triangle`$ |
|---|---|---|
| $`\mathcal P_{s_1}(\check\omega_2)n_2^J`$ | $`\mathcal P_{s_1}(\check\omega_2)n_1`$ | $`0`$ |
| $`\check\omega_2(n_2^J)^2`$ | $`0`$ | $`-\check\omega_2 n_1n'_1`$ |
| $`(n_2^J)^3`$ | $`0`$ | $`0`$ |

These identities use the displayed interval/triangle fields and the fixed
coefficient transport, so the compact pair includes all fractional terms.

The operations $`T_6,y_6`$ are the finite operations of
[Finite cochain formulas for the bosonic obstruction](SOURCE_OPERATIONS.md), applied to the displayed
auxiliary fields. Each $`1/2`$ bracket is binary. Each $`1/4`$ bracket is
integer, with the barred polynomial reduced as a whole before its
implicit lift. The parameter integration then gives phases modulo one.
