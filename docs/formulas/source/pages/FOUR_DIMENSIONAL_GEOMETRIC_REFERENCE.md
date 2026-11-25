# Physical pairings and the 4+1D formulas

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

At the dual vertex of a four-simplex the Majorana modes of the decorated
chains on its five faces are paired together with the effective Majorana zero
modes of the p+ip layers. The face positions, in cyclic order, are
`0123 B, 0134 B, 1234 B, 0124 A, 0234 A`; a position is occupied when the
chain on that face is present. The effective Majorana zero modes form one
list, intrinsic modes first and then projective modes, each in row-major order.

Pair an even list of effective Majorana zero modes consecutively. For an odd
list keep its first mode aside, pair the rest, and pair the kept mode with the
last occupied B position (B to the mode), or with the first occupied A position
if no B position is occupied (the mode to A). Pair the remaining faces as
without p+ip decoration: for four faces, start after the unique empty position
in the cyclic list and pair consecutive positions. Every arrow follows the
written linear order, including `0123 B` to `0234 A` on the closing edge.
The separate states and the stacked state use this same rule.

<a id="obstruction"></a>

## Obstruction

The complete directed F-move count, including all vacuum and interval pairs, gives

```math
\Delta P_f=\mathcal O_5\mod2.
```

Here $`\mathcal O_5`$ is the complete function in
[the 4+1D formula page](FOUR_DIMENSIONAL.md#eq-l4).
The occupation $`n_4`$ of the point fermions therefore obeys
$`dn_4=\mathcal O_5`$. The chain ends give $`n_3\cup_1n_3+dn_3\cup_2n_3`$
together with their species and anti-unitary signs; the order $`dn_3\cup_2n_3`$
comes from the inversion parity $`n_3\cup_2n_3`$ of the three B positions and
the two A positions, whose local identity holds for every length of the list
of effective Majorana zero modes. The intrinsic zero modes, the projective
zero modes and their mixed pairs give the three lines of
$`\mathcal O_5^\psi`$. A different convention for steps that only order the
effective Majorana zero modes changes the count of every F move by a
coboundary and leaves the class of $`\mathcal O_5`$ unchanged.

## Stacking

The P graph includes the complete upper and lower states, the three-copy
contacts, and the stacked state with the same pairing rule. Besides the twister,
its count contains the coboundary of an explicit three-cochain $`B_3`$ that
depends on both separate states, written out as its alternating face sum.
$`\mathcal E_4`$ is the complete twister in
[the same formula page](FOUR_DIMENSIONAL.md#eq-p4), evaluated with the
actual lower fields of the stacked state

```math
N_2=n_2+n'_2,\qquad
N_3=n_3+n'_3+[n_2]_2\cup_1[n'_2]_2.
```

The complete count is

{{equation:four-dimensional-geometric-reference--pair--2}}

The summed term is a coboundary, not a decoration: the stacking law on the
formula page composes the P move with the complex-fermion gauge
transformation that removes it, and records the corresponding phase.
The two counts obey, pointwise,

```math
d(\Delta P_f\text{ for }P)=\Delta(\Delta P_f\text{ for }F).
```

Contacts act on effective modes and the already present point fermion in
one even unitary, so the total parity is never changed in an isolated step.

The [verification bundle](verification/geometric_4d/README.md) contains the
matching constructor, exact symbolic comparisons, local circuits and the two
worked examples of the manuscript. The exact product comparison has 42 free
Boolean inputs and the paired identity has 75; these are coefficient
identities over the complete local domain. Arbitrary layer numbers are covered by
the integer shuffle and local matching identities, which the finite graphs
check independently.
