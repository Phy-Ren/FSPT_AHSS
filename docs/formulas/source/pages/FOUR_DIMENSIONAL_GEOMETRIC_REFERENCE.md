# Physical pairings and the 4+1D formulas

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

The single-layer construction retains the original ordinary Majorana pairings.
Its five positions, in cyclic order, are
`0123 B, 0134 B, 1234 B, 0124 A, 0234 A`.
Use the actual surviving ordinary or induced endpoint at each occupied position.
The central modes are ordered intrinsic array first, then projective array,
each in row-major order.

Pair an even central list consecutively. For an odd list reserve its first
mode, pair the rest, and attach the reserved mode to the last occupied B
position (B to centre), or the first occupied A position if there is no B
(centre to A). Pair the remaining face ends by the original resolved graph.
For four remaining ends, start after the unique empty position in the cyclic
list and pair consecutive positions. Every ordinary arrow follows the
written linear order, including `0123 B` to `0234 A` on the closing edge.
Both inputs and the output use this same one-layer rule.

## Obstruction and its reference

The complete directed F-move count, including all reference dimers, gives

```math
\Delta P_f=\mathcal O_5+dR_4\mod2.
```

Here $`\mathcal O_5`$ is the complete function in
[the 4+1D formula page](FOUR_DIMENSIONAL.md#eq-l4).
The occupation $`n_4`$ of the point fermions in this physical pairing
reference therefore obeys $`dn_4=\mathcal O_5+dR_4`$, and the shifted
occupation $`\widetilde{n}_4=n_4+R_4`$ obeys $`d\widetilde{n}_4=\mathcal O_5`$.
The terminal layer of the 4+1D formulas uses $`\widetilde{n}_4`$.
The fixed binary four-cochain is explicitly

<a id="eq-r4"></a>

{{equation:four-dimensional-geometric-reference--single-state--1}}

The added first term is the inversion parity of the three B positions and
the two A positions relative to the archived consecutive-list convention.
It is the usual higher cup, not an additional operation. Its local identity
holds for every length of the central list. The common symmetry signs do
not change that comparison. The other terms are the signed array reference
already required for intrinsic and projective modes.

## Stacking and its paired comparison

The actual P graph includes the two complete input states, the cross-copy
channels, the three-copy contacts, and the output state with the same
single-layer pairing rule. Its count is displayed below. Besides the twister
and $`\Delta R_4`$, it contains the coboundary of an explicit two-input
reference, written out as its alternating face sum.

$`\mathcal E_4`$ is the complete twister in
[the same formula page](FOUR_DIMENSIONAL.md#eq-p4). The output used in
$`\Delta R_4`$ is the actual lower product:

```math
N_2=n_2+n'_2,\qquad
N_3=n_3+n'_3+[n_2]_2\cup_1[n'_2]_2
             +s_1([n_2]_2\cup_2[n'_2]_2).
```

Equivalently $`\widetilde{N}_3=\widetilde{n}_3+\widetilde{n}'_3+\widetilde{\mathcal E}_3`$,
with $`\widetilde{\mathcal E}_3=[n_2]_2\cup_1[n'_2]_2`$. The complete count is

{{equation:four-dimensional-geometric-reference--pair--2}}

The summed term is a coboundary, not a decoration: the stacking law on the
formula page composes the P move with the complex-fermion gauge
transformation that removes it, and records the corresponding phase.

The paired identities imply, pointwise,

```math
d(\Delta P_f\text{ for }P)=\Delta(\Delta P_f\text{ for }F).
```

No term is discarded merely because the discrepancy is closed.
The lower formulas use the physical occupation $`n_4`$; the terminal
formulas, self-products and examples use the shifted occupation
$`\widetilde{n}_4=n_4+R_4`$. The two displayed witnesses relate the physical
matching convention to these formulas.

## Parity and output cleanup

Contacts act on effective modes and the already present point fermion in
one even unitary. Each continuous generator is quadratic and commutes with
total parity. The Majorana-subsystem parity is never changed in an isolated
physical step. Pure-gamma components retain their original move. Within a
component containing psi, the new rotations use a psi pivot; pure-gamma
pairs are only the prescribed initial or final pairs.

Complete face channels are then cancelled or transferred with even two-end
rotations, retaining every reference pair. The inverse reset is evaluated
on the native signed output $`N_2`$. The centre is indexed by the single
row-major $`N_2`$ array after the already executed contacts. Index enumeration
moves no operator and performs no further permutation of a fermion word.

The [verification bundle](verification/geometric_4d/README.md) contains the
independent matching constructor, exact symbolic comparisons, local circuits,
complete cleanup graphs and regenerated manuscript examples. The exact
product comparison has 42 free Boolean inputs; the paired identity has 75.
These are coefficient identities, not a claim to enumerate $`2^{75}`$
Hamiltonians. Arbitrary copy counts are covered by the integer shuffle and
local matching identities; explicit finite graphs check those constructions
independently. The model is the specified effective seam resolution with
retained partners; a unique microscopic chiral parent is not assumed.
