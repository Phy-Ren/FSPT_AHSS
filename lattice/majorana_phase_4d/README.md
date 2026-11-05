# Lattice Majorana phases of 4+1D FSPT phases

This directory computes, from the fixed-point lattice construction, the two Majorana
Berry phases of 4+1D fermionic SPT phases with Majorana-chain decoration $n_3$:

* the **heptagon phase** $\mathcal O_6^\gamma$ (obstruction of the bosonic layer), and
* the **stacking phase** $\mathcal E_5^\gamma$ (stacking twister of the bosonic layer),

for every local configuration, with general fermionic symmetry data
$(\omega_2,s_1)$. The phases are evaluated exactly. All $2^{25}$ heptagon and $2^{23}$
stacking configurations take a few minutes on a workstation. The scripts verify the
stacking compatibility on every row and compare both phases with the cochain
formulas of this repository.

The results are in the [phase convention](../../docs/FORMULA_GUIDE.md#phase-convention).

- [1. The lattice construction](#1-the-lattice-construction)
- [2. Evaluation](#2-evaluation)
- [3. Results and checks](#3-results-and-checks)
- [4. Reproduction](#4-reproduction)
- [5. Files and formats](#5-files-and-formats)

## 1. The lattice construction

### Majoranas and dimer states

Every 3-simplex $\langle ijkl\rangle$ carries two Majoranas $\gamma_{ijkl,A}$,
$\gamma_{ijkl,B}$, one on each side. In a 4-simplex with local vertices
$0,\dots,4$, the face opposite to the local vertex $j$ contributes its B Majorana for
even $j$ and its A Majorana for odd $j$. A face with $n_3=0$ carries the vacuum pair
$-i\gamma_A\gamma_B=1$. The faces with $n_3=1$ of one 4-simplex (two or four of them)
are paired inside the 4-simplex. Label the faces by the opposite local vertex. The
arrows $a\to b$ (meaning $-i\gamma_a\gamma_b=1$) are

| faces | arrow | | faces | arrow |
|---|---|---|---|---|
| 0,1 | $0\to1$ $(\omega)$ | | 1,3 | $3\to1$ $(s)$ |
| 0,2 | $2\to0$ $(\omega+s)$ | | 1,4 | $4\to1$ |
| 0,3 | $0\to3$ $(\omega)$ | | 2,3 | $2\to3$ |
| 0,4 | $4\to0$ $(\omega+s)$ | | 2,4 | $4\to2$ $(s)$ |
| 1,2 | $2\to1$ | | 3,4 | $4\to3$ |

With four faces $p_0<p_1<p_2<p_3$ the two chains pair $(p_0,p_2)$ and $(p_1,p_3)$.
An arrow marked $(x)$ is reversed when $x=1$. In a 4-simplex obtained from the
standard one by $U(g)$, $\omega=\omega_2(g,g^{-1}g')$ and $s=s_1(g)$ come from the
non-standard pairing rule. A projector is written $\tfrac12(1+i^{p}\gamma_a\gamma_b)$.
Here $p=3$ is the arrow $a\to b$.

### Moves and inserted Majoranas

A move maps one dimer state to another by a product of projectors. If a transition
loop of the two states changes the fermion parity (non-Kasteleyn), one Majorana of
that loop is inserted before the projection. **One rule fixes all insertions:**

> On every parity-changing transition loop, insert the first Majorana of the move's
> priority list that lies on the loop. In a forward move the selected Majoranas act in
> priority order; the inverse move inserts $\Gamma^\dagger$.

| move | priority list | forward insertion |
|---|---|---|
| $F(012345)$ | $\gamma_{2345B},\gamma_{1234B},\gamma_{0123B},\gamma_{1235A}$ | $\Gamma=\gamma_{1235A}^d\gamma_{0123B}^c\gamma_{1234B}^b\gamma_{2345B}^a$ |
| $\mathcal P(01234)$ | $\gamma'_{1234B},\gamma'_{0134B},\gamma'_{0124A}$ | $\Gamma=\gamma'^{\,c}_{0124A}\gamma'^{\,b}_{0134B}\gamma'^{\,a}_{1234B}$ |

Every move uses these lists in its own local labels. Every parity-changing loop of
every configuration contains a candidate. A non-standard move $U(g)XU(g)^\dagger$
transports its inserted Majoranas, so a B Majorana gains $(-1)^{\omega_2(g,\sigma)+s_1(g)}$.

### Heptagon loop ($\mathcal O_6^\gamma$, six-simplex $0123456$, one layer)

The seven dimer states are the seven triangulations of the heptagon
([`include/heptagon_states.hpp`](include/heptagon_states.hpp), stages 0–6):

| stage | 4-simplices |
|---|---|
| 6 | 02345 03456 02356 01245 01256 01234 |
| 5 | 01245 02456 01256 23456 02346 01234 |
| 4 | 01234 02346 01246 23456 12456 01456 |
| 3 | 12346 12456 23456 01236 01346 01456 |
| 2 | 01346 01456 13456 01236 12356 12345 |
| 1 | 01236 01356 12356 03456 01345 12345 |
| 0 | 01235 01345 12345 01256 02356 03456 |

Faces shared by two 4-simplices of a stage carry the vacuum pair unless $n_3=1$
there. The ancillary faces of the other stages also carry it. With $|\psi\rangle$ the
state of stage 6,

$$
\mathcal O_6^\gamma=\langle\psi|\,\bar X_{012345}\,\bar X_{012356}\,\bar X_{013456}\,
{}^{01}\!\bar X_{123456}\,X_{012346}\,X_{012456}\,X_{023456}\,|\psi\rangle ,
$$

i.e. forward along the moves with odd omitted vertex, then back along those with even
omitted vertex.

### Stacking loop ($\mathcal E_5^\gamma$, five-simplex $012345$, two layers $n_3,n'_3$)

The $\mathcal P$ move maps the two layers on a 4-simplex to one layer carrying
$N_3=n_3+n'_3$ ([`include/stacking_states.hpp`](include/stacking_states.hpp)). The stages are:

| stage | dimer state |
|---|---|
| 7 | $\lvert\psi\rangle$: one layer $N_3$ on 01234, 01245, 02345; lower layer vacuum |
| 0, 1 | intermediate states of $\bar{\mathcal P}$ on 01234, 01245, 02345 |
| 2 | two layers $n_3,n'_3$ on 01234, 01245, 02345 |
| 3 | two layers on 01235, 01345, 12345 (after $F$, $F'$) |
| 4, 5 | intermediate states of $\mathcal P$ on 01235, 01345, 12345 |
| 6 | one layer $N_3$ on 01235, 01345, 12345 |

$$
\mathcal E_5^\gamma=\langle\psi|\,\bar X^{\rm tot}_{012345}\,X_{01235}\,X_{01345}\,
{}^{01}\!X_{12345}\,X_{012345}\,X'_{012345}\,\bar X_{01234}\,\bar X_{01245}\,
\bar X_{02345}\,|\psi\rangle .
$$

A $\mathcal P$ move is $X=P_3P_2P_1\Gamma$. Its inverse is
$\bar X=\bar P_1\Gamma^\dagger\bar P_2\bar P_3$, where $\bar P_i$ projects onto the state
before step $i$. The steps of the projection scheme on one 4-simplex are listed
below. A face is *dangling* if $n_3+n'_3=1$ there.

* A face with $n_3=n'_3=1$ gets a vertical bridge on the side inside the 4-simplex
  ($\gamma_A\to\gamma'_A$, $\gamma'_B\to\gamma_B$, sign $(-1)^{s_1}$ of the face) in
  step 1. The parity may change only in this step.
* Dangling faces get inclined bridges $\gamma_i$–$\gamma'_j$ with the arrow of the
  in-layer pair $(i,j)$. They follow the crossing convention of two chains. Two lower
  dangling faces in the same plane are moved to the upper layer in step 2.
* Pairs that a step leaves implicit are determined by the reference state (the final
  state for $\mathcal P$, the two-layer state for $\bar{\mathcal P}$). These are the
  lower vacuum pair across a dangling face, and the leftover upper pair when the upper
  layer has two chains. Their projectors are redundant; the tracker includes them.
* The last step produces $N_3$ with the two-chain convention.

## 2. Evaluation

**Operator word.** [`include/loop_word.hpp`](include/loop_word.hpp) follows the dimer
state through the loop. It finds the transition loops of every projection and selects
the insertions by the rule above. It also checks with the Kasteleyn rule that every
projection is nonzero. The loop becomes one word of projectors and Majoranas. Each
projector is $\tfrac12(1+i^{p}\gamma_a\gamma_b)$. For the projector onto
$|\psi\rangle$, the expectation value equals the trace of the word up to a positive
factor.

**Exact trace.** [`include/gauss.hpp`](include/gauss.hpp) expands every projector. A
term selects bilinears $x\in\mathbb F_2^m$, and its trace is nonzero iff every
Majorana occurs an even number of times. This is a linear condition on $x$. The term
is then $i^{\Phi(x)}$, where $\Phi$ is the sum of the phases plus twice the number of
inversions of the word. The inversion number is additive over pairs of factors, so
$\Phi$ is a $\mathbb Z_4$-valued quadratic form. The constrained sum of $i^{\Phi}$ is
a quadratic Gauss sum. It is evaluated exactly in $O(m^3)$ by eliminating one
variable at a time. The result is $0$ or $2^{k/2}e^{2\pi i\theta}$ with
$\theta\in\tfrac18\mathbb Z$. [`src/test_gauss.cpp`](src/test_gauss.cpp) compares it
with the brute-force expansion on 200,000 random words. It also checks the
four-Majorana example of the paper ($\theta=1/8$).

## 3. Results and checks

All phases are total phases in units of $1/8$.

**Stacking compatibility.** With the complex-fermion parts of the lattice
construction ([`scripts/cochains.py`](scripts/cochains.py)),

$$
d_{s_1}(\mathcal E^c+\mathcal E^{c\gamma}+\mathcal E_5^\gamma)
=\mathcal O_6[N]-\mathcal O_6[n]-\mathcal O_6[n'],\qquad
\mathcal O_6=\mathcal O_6^\gamma+\mathcal O^c+\mathcal O^{c\gamma}.
$$

This holds on every one of the 8,388,608 rows of $\mathcal E_5^\gamma$. Each row is
checked on its own six-simplex with random remaining data.

**Comparison with the formulas.** Let $\gamma$ and $\mathcal E$ be the closed-Majorana
source and stacking law of [`fspt/majorana_complete.py`](../../fspt/majorana_complete.py)
($q=3$, operator coordinate). Then

$$
\mathcal O_6^\gamma=\gamma[n_3]+d_{s_1}B_5^\gamma,\qquad
\mathcal E_5^\gamma+\mathcal E^c+\mathcal E^{c\gamma}
=\mathcal E+B_5^\gamma[N]-B_5^\gamma[n]-B_5^\gamma[n']+d_{s_1}\sigma_4 .
$$

$B_5^\gamma$ is a local table on the 5-simplex ([`data/B5gamma_15bit.bin`](data)).
$\sigma_4$ is a local table on the 4-face; it depends on
$n_3,n'_3,n_4,n'_4,\omega_2(012),s_1(01),s_1(02)$ ([`data/sigma4_13bit.bin`](data)). The
complex-fermion parts of the lattice equal the operator coordinate identically:
$\tfrac12[dn_4\cup_3n_4+dn_4\cup_4dn_4]=\tfrac12n_4\cup_3dn_4+d(\tfrac12n_4\cup_4dn_4)$.
The second identity holds on all 8,388,608 rows. $\sigma_4$ must depend on $n_4,n'_4$:
without them no local solution exists.

| check | script | scope | result |
|---|---|---|---|
| exact evaluator | `bin/test_gauss` | 200,000 random words | 0 mismatches |
| nonzero projections, covered loops | `bin/o6_heptagon`, `bin/e5_stacking` | all rows | 0 / 0 |
| stacking compatibility | `scripts/check_stacking.py` | all $2^{23}$ rows | 0 bad |
| $\mathcal O_6^\gamma$ vs formula | `scripts/check_o6_formula.py` | 30,000 random six-simplices | 0 bad |
| $\sigma_4$ exists | `scripts/fit_sigma4.py` | 20,000 equations, 20,000 fresh samples | 0 bad |
| $\mathcal E_5^\gamma$ vs formula | `scripts/check_e5_formula.py` | all $2^{23}$ rows | 0 bad |

## 4. Reproduction

Requirements: a C++17 compiler, Python 3 with NumPy, and this repository.

```sh
cd lattice/majorana_phase_4d
make                      # bin/e5_stacking bin/o6_heptagon bin/test_gauss bin/z8solve
make tables JOBS=16       # out/E5gamma_23bit.bin, out/O6gamma_25bit.bin (+ SHA-256 check)
make check JOBS=16        # evaluator, reference slices, short runs of the checks

# complete checks
python3 scripts/check_stacking.py   out/E5gamma_23bit.bin out/O6gamma_25bit.bin --jobs 16
python3 scripts/check_o6_formula.py out/O6gamma_25bit.bin --samples 30000 --jobs 16
python3 scripts/fit_sigma4.py       out/E5gamma_23bit.bin out/sigma4.bin --jobs 16
python3 scripts/check_e5_formula.py out/E5gamma_23bit.bin --jobs 16
```

Single configurations: `bin/e5_stacking first last out.bin` and
`bin/o6_heptagon first last out.bin` write one int8 per configuration. They print
the tracker diagnostics. Timing on 30 cores: tables 4 min; full stacking check 11 min;
full formula check 6 min. One core evaluates of the order of $10^4$ configurations per
second.

The full tables are not stored here; `make tables` regenerates them and compares their
SHA-256 sums with [`data/SHA256.json`](data/SHA256.json).
[`tests/`](tests) holds 4,096-row reference slices for the quick check.

## 5. Files and formats

| file | content |
|---|---|
| `include/gauss.hpp` | exact trace of a Majorana word |
| `include/tracker.hpp` | dimer state, transition loops, Kasteleyn rule |
| `include/loop_word.hpp` | loop assembly and insertion rule |
| `include/heptagon_states.hpp` | dimer states of the heptagon stages |
| `include/stacking_states.hpp` | dimer states and projection scheme of the stacking loop |
| `src/o6_heptagon.cpp`, `src/e5_stacking.cpp` | the two loops |
| `src/z8solve.cpp` | linear systems over $\mathbb Z/8$ (for $\sigma_4$) |
| `scripts/cochains.py` | cochain data, lattice complex-fermion parts, table keys |

Tables are int8 numerators of $1/8$. Bits are listed from least significant; "cone"
means the faces containing the first vertex, in lexicographic order.

| table | entries | index bits |
|---|---|---|
| $\mathcal O_6^\gamma$ | $2^{25}$ | $n_3$ cone of 0123456 (20), $\omega_2(012),(013),(023)$, $s_1(01),(02)$ |
| $\mathcal E_5^\gamma$ | $2^{23}$ | $n_3$ cone of 012345 (10), $n'_3$ (10), $\omega_2(012)$, $s_1(01)$, $s_1(02)$ |
| $B_5^\gamma$ | $2^{15}$ | $n_3$ cone of the five-face (10), $\omega_2(012),(013),(023)$, $s_1(01),(02)$ |
| $\sigma_4$ | $2^{13}$ | $n_3$, $n'_3$ cone of the four-face (4+4), $n_4$, $n'_4$, $\omega_2(012)$, $s_1(01)$, $s_1(02)$ |

The symmetry data enter only through these values. The construction uses standard
moves with first group element $e$. Only species of the first few vertices appear in
their non-standard pairings.
