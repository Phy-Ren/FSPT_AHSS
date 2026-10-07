# Recovering the stacking group from root powers

An abelian stacking group can be reconstructed from the power of each
cyclic filtration generator, provided the result is known as a complete
element of the lower group. A generator's order alone is insufficient.
For an order-two quotient generator, the required power is its self-stack.

## The presentation theorem

Choose full lifts $`g_i`$ of cyclic generators of a certified filtration,
ordered from lower to higher layers. If the quotient order is $`q_i`$,
determine the marked lower-group relation

```math
q_i g_i=\sum_{j\lt i}a_{ij}g_j.
```

Together with the lower relations, the integer rows

```math
q_i e_i-\sum_{j\lt i}a_{ij}e_j
```

present the abelian group. Smith normal form gives its invariant factors.
A free quotient generator contributes no finite power relation.

To prove this, map the presented group to the stacking group using the
chosen full lifts. They generate by the filtration. For any element in
the kernel, its coefficient in the highest cyclic quotient is a multiple
of that quotient's order, or zero for a free quotient. Subtract its known
power relation and repeat in lower layers. The certified bottom-layer
relations remove the remaining kernel.

If the chosen layers describe outward survivors before the incoming
gauge quotient, append every complete incoming relation vector as well.
Gauge transformations must retain their upper-layer corrections. A rank
or order assigned to an incoming image does not specify that vector.

For example, with lower group $`\mathbb Z_2\langle a\rangle\oplus\mathbb Z_2\langle b\rangle`$ and two order-two quotient
generators, the relations $`2x=a,\ 2y=b`$ give $`\mathbb Z_4\oplus\mathbb Z_4`$, whereas
$`2x=a,\ 2y=a`$ give $`\mathbb Z_4\oplus\mathbb Z_2\oplus\mathbb Z_2`$. Both lifted roots have order four.
Their marked doubling images contain the missing information.

## 3+1D: choose the basis around the one distinguished target

The complex-fermion and Majorana graded factors have exponent two.
The p+ip layer is a surviving subgroup of
$`H^1(G,\mathbb Z_{s_1})`$. Its only possible torsion factor is a single $`\mathbb Z_2`$.

Indeed, if a signed integer cocycle $`n_1`$ represents a torsion class,
then $`m n_1=d_{s_1} k`$ for an integer zero-cochain $`k`$. Since

```math
d_{s_1} k(g)=\big((-1)^{s_1(g)}-1\big)k=-2k s_1(g),
```

trivial $`s_1`$ forces $`n_1=0`$. For nontrivial $`s_1`$, this equation forces
$`n_1=r s_1`$ with integer $`r`$. Even $`r`$ is exact; odd $`r`$ has the same
class as $`s_1`$. Thus a surviving torsion root can be chosen with

```math
n_1=s_1.
```

Any change to this representative includes the full accompanying gauge
transformation of its upper fields.

Meanwhile the closed integer gauge parameters are

```math
H^0(G,\mathbb Z_{s_1})=
\begin{cases}
\mathbb Z,&s_1=0,\\
0,&s_1\ne0.
\end{cases}
```

Therefore there is at most one distinguished full target to incorporate
into the Majorana basis:

- If $`s_1=0`$, take $`Y`$ to be the complete vacuum gauge endpoint of the
  integer parameter $`1`$. Its incoming relation is $`Y=0`$.
- If $`s_1`$ is nontrivial and the torsion p+ip root $`P`$ survives, first
  form $`P+P`$. Apply the full integer gauge with parameter $`1`$ to remove
  its integer field, since $`2s_1+d_{s_1}1=0`$. Call the resulting full state
  $`Y`$; its power relation is $`2P=Y`$.

These alternatives cannot occur together. If the Majorana class of $`Y`$
is nonzero, include that class in a basis of the outward-surviving
Majorana space and choose the **entire state $`Y`$** as its lift. Flatness
of $`Y`$ already proves that this class survives every outgoing
obstruction. There is no need to reconstruct $`Y`$ by multiplying old
Majorana roots, or to guess its CF and bosonic components.

If the Majorana class is zero, remove its exact Majorana field by a
complete gauge transformation and reduce it in the CF/bosonic subgroup.

Every Majorana-root square has zero p+ip and Majorana output. The
remaining incoming Majorana/CF gauges do too. Their reductions therefore
need only the CF/bosonic product laws. The distinguished root's own
square relation is retained: imposing $`Y=0`$ must also preserve any
lower relation implied by $`2Y`$.

This gives a constructive presentation strategy using full self-stacking
specializations for the Majorana and p+ip roots, ordinary CF/bosonic
reduction, and complete source/gauge transport. Surviving free integer
quotients split abstractly and contribute their certified free rank.
The strategy does not require arbitrary pairs of Majorana or p+ip roots.

The [closed-Majorana self-stacking formula](THREE_DIMENSIONAL_MAJORANA_SELF_STACKING.md)
supplies the zero-p+ip specialization. A torsion p+ip root instead needs
the full specialization at $`n_1=s_1`$, including its potentially open
Majorana field and all physical contributions.

### Exact replay of the basis change

This reorganization has been checked on all **602 saved 3+1D
presentations**. Of these, 105 have a nonzero distinguished Majorana
target: 74 incoming images and 31 p+ip squares. Seventy require a
nonidentity integer basis matrix; in the other 35 the target already
has the marked coordinate of one root.

For every case the replay retains the target's full lower coordinates,
uses an explicit determinant-one basis map and its inverse, and keeps
the new root's square relation. Reversing all basis changes and row
additions recovers the original integer presentation exactly. There
are 566 full witness records and 36 accepted summaries, the latter
checked using their declared relation order and explicit sign input.
Eighty-eight cases retain free p+ip roots.

The [replay certificate](coefficients/ADAPTIVE_THREE_DIMENSIONAL_REPLAY.json)
records every reversible map; its
[standalone verifier](coefficients/verify_root_power_presentations.py)
uses only the published presentations and standard integer arithmetic.

This establishes the presentation reorganization. It does not claim
that an optimized cochain backend has already been implemented or timed.

## 4+1D: cyclic powers remain sufficient, but doubling is not universal

The CF and Majorana graded factors again have exponent two. The p+ip
layer now comes from $`H^2(G,\mathbb Z_{s_1})`$, which can have general cyclic orders.
For a quotient of order $`2^k`$, repeated self-stacking constructs its
required power. For other orders one needs the corresponding cyclic
power or a separate certified method of recovering it.

This distinction occurs in the saved examples. With trivial background
for $`G=C_3`$, the marked relations are

```math
3D=0,\qquad 3P=D,
```

giving $`\mathbb Z_9`$. For $`G=C_5`$, they are $`5D=0,\ 5P=0`$, giving $`\mathbb Z_5\oplus\mathbb Z_5`$.
Odd extensions cannot therefore be assumed to split.

Once a root's cyclic power has been formed, its integer class is zero.
Remove that field by its full integer gauge before reducing the lower
state. Subsequent products lie in the zero-p+ip subgroup. This avoids
products of different p+ip roots in a power-presentation construction,
although lower mixed products can remain necessary in a fixed basis.

The [closed-Majorana diagonal](FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md)
is useful for self-stacking in that subgroup, with its stated output
gauge. It does not by itself give every lower-coordinate comparison,
the full p+ip square, or the odd cyclic power relations. A corresponding
general adaptive-basis construction in 4+1D is a separate problem.

Keep the general stacking law alongside these specializations. It
supports arbitrary marked cochain products and independent coherence
checks. After a presentation is certified, abstract group operations
use its integer coordinates and need no further twister evaluations.
