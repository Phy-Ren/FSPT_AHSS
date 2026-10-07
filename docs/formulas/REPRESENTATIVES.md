# Changes of cochain representative

All changes here act on the source and stacking correction together.

## 3+1D: physical terminal formulas

The current guide uses the complete [paired terminal phase map](THREE_DIMENSIONAL_PAIRED_REPRESENTATIVE.md). That appendix gives the map, inverse, and output coboundary explicitly. The lower physical fields and their stacking laws are unchanged.

## 3+1D: earlier complex-fermion coordinate



<a id="eq-t3d"></a>

**(T3D)**

```math
{n_3^{\mathrm{old}}}={n_{3}}+\kappa_3({n_{1}},{\check n_{2}}),\qquad
\kappa_3=({\bar n_{1}}+{s_1}){\check n_{2}}+{\check\omega_2}{\widetilde n_{1}}+[{\check\omega_2}\cup_1({\bar n_{1}}+{s_1})]{\bar n_{1}}.
```

Its stacking correction changes at the same time:

```math
\mathcal{ℰ}_{3,\mathrm{old}}=\mathcal{ℰ}_3+\Delta\kappa_3.
```

The obstruction is transported by the same substitution and $`d\kappa_3`$.
In particular, $`n_1=0`$ alone does not remove this coordinate change when
$`s_1\ne0`$.

## 4+1D: historical source convention



Write $`\widehat{\mathcal{𝒪}}_{6,\mathrm{raw}}`$ for the earlier source.
This earlier change precedes the operator reordering below. Its source and product use the same coordinates:

<a id="eq-t4e"></a>

**(T4E)**

```math
{\widehat{\mathcal{𝒪}}}_6=\widehat{\mathcal{𝒪}}_{6,\mathrm{raw}}+d_{s_1}\Lambda_5+\frac1{12}{n_{2}}^3,
\qquad \Lambda_5=\frac14{\beta^\circ\check n_3}\cup_3{B_4^\psi}.
```

The corresponding terminal redefinition contributes
$`\Delta\Lambda_5`$ to the stacking correction. The separate cubic term
shown in (T4e) is retained in (T4); it is not being called a coboundary.

<a id="operator-phase-4d"></a>

## 4+1D: operator phase in the current guide

Relative to the supplied full terminal formula, the guide uses

```math
\widehat\nu_5^{\rm op}
 =\widehat\nu_5^{\rm supplied}+\frac12 n_4\cup_4dn_4.
```

The inverse subtracts the same half-valued cochain. The paired formulas are

```math
\begin{aligned}
\widehat{\mathcal{𝒪}}_6^{\rm op}
 &=\widehat{\mathcal{𝒪}}_6^{\rm supplied}
   +d_{s_1}\left(\frac12n_4\cup_4dn_4\right),\\
\widehat{\mathcal{ℰ}}_5^{\rm op}
 &=\widehat{\mathcal{ℰ}}_5^{\rm supplied}
   +\frac12\left[N_4\cup_4dN_4-n_4\cup_4dn_4
                                  -n'_4\cup_4dn'_4\right].
\end{aligned}
```

The actual stacked output is used in the last line. This yields the displayed c, c-gamma, and c-psi operator factors. The other terms are regrouped with all integer carries retained. There is no additional output coboundary in this 4+1D map.

## Terminal phase changes



For fixed lower decorations, solve each obstruction modulo the permitted
gauge and lower-layer changes. A nonzero cochain may be exact; only a
nontrivial final obstruction class rules out the decoration. Stack accepted
representatives using the paired product and reduce by the same equivalences.

For a terminal phase change $`\widehat\nu\mapsto\widehat\nu+f`$, with
lower fields and their product fixed, the source and correction transform
together:

```math
\widehat{\mathcal{𝒪}}\longmapsto\widehat{\mathcal{𝒪}}+d_{s_1}f,\qquad
\widehat{\mathcal{ℰ}}\longmapsto\widehat{\mathcal{ℰ}}+\Delta f.
```

A change of a lower decoration must also be substituted into every higher
source and product. These coordinate rules concern the full equations,
not only the abstract group obtained in an example.

The separate [programmer translation](../../formulas/CODE_NOTATION.md) records
how the formulas correspond to existing variables and compiled operations.

The terminal 4+1D Majorana contribution additionally uses the
[explicit output coboundary](FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md).
It changes the output cochain by an exact phase and leaves the obstruction
and every other designated contribution unchanged. Its inverse adds the
same displayed coboundary.
