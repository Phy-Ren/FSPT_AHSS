# Changes of cochain representative

All changes here act on the source and stacking correction together.

## 3+1D: earlier complex-fermion coordinate



<a id="eq-t3d"></a>

**(T3D)**

```math
{n_3^{\mathrm{old}}}={n_{3}}+\kappa_3({n_{1}},{\check n_{2}}),\qquad
\kappa_3=({\bar n_{1}}+{s_1}){\check n_{2}}+{\check\omega_2}{\widetilde n_{1}}+[{\check\omega_2}\cup_1({\bar n_{1}}+{s_1})]{\bar n_{1}}.
```

Its stacking correction changes at the same time:

```math
\mathcal E_{3,\mathrm{old}}=\mathcal E_3+\Delta\kappa_3.
```

The obstruction is transported by the same substitution and $`d\kappa_3`$.
In particular, $`n_1=0`$ alone does not remove this coordinate change when
$`s_1\ne0`$.

## 4+1D: earlier bosonic obstruction



Write $`\widehat{\mathcal O}_{6,\mathrm{raw}}`$ for the earlier source.
The displayed change is paired with the product change in the same
coordinates:

<a id="eq-t4e"></a>

**(T4E)**

```math
{\widehat{\mathcal O}}_6=\widehat{\mathcal O}_{6,\mathrm{raw}}+d_{s_1}\Lambda_5+\frac1{12}{n_{2}}^3,
\qquad \Lambda_5=\frac14{\beta^\circ\check n_3}\cup_3{B_4^\psi}.
```

The corresponding terminal redefinition contributes
$`\Delta\Lambda_5`$ to the stacking correction. The separate cubic term
shown in (T4e) is retained in (T4); it is not being called a coboundary.

## Terminal phase changes



For fixed lower decorations, solve each obstruction modulo the permitted
gauge and lower-layer changes. A nonzero cochain may be exact; only a
nontrivial final obstruction class rules out the decoration. Stack accepted
representatives using the paired product and reduce by the same equivalences.

For a terminal phase change $`\widehat\nu\mapsto\widehat\nu+f`$, with
lower fields and their product fixed, the source and correction transform
together:

```math
\widehat{\mathcal O}\longmapsto\widehat{\mathcal O}+d_{s_1}f,\qquad
\widehat{\mathcal E}\longmapsto\widehat{\mathcal E}+\Delta f.
```

A change of a lower decoration must also be substituted into every higher
source and product. These coordinate rules concern the full equations,
not only the abstract group obtained in an example.

The separate [programmer translation](../../formulas/CODE_NOTATION.md) records
how the formulas correspond to existing variables and compiled operations.
