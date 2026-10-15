# 4+1D computed examples: internal cyclic symmetry

These are global calculations of the original four-data model, ordered
`(e_2,n_2,n_4,nu_5)`, for a unitary internal `C_N` commuting with `U(1)^f`.
The backgrounds are exactly `s=rho=0` and `omega=0`. A cyclic label here
does not stand for a crystalline rotation or a spin convention.

The [current results](../../results/current/4p1d/internal_cyclic.md) and
[accepted records](../../results/expansion_20261015/4p1d/internal_cyclic/results.json)
contain the six actual cluster computations. The
[independent root audit](../../results/expansion_20261015/4p1d/cyclic_root_audit.json)
checks the complete root relations by a different evaluation path and
verifies every saved native phase-boundary witness.

## Cohomology, obstructions, and incoming completeness

For `N>1`,

```math
H^2(C_N,\mathbb Z)=H^4(C_N,\mathbb Z)
 =H^5(C_N,\mathbb R/\mathbb Z)=\mathbb Z_N,
\qquad H^6(C_N,\mathbb R/\mathbb Z)=0.
```

The integer source vanishes identically because `B3=rho=0`. The terminal
target vanishes, so both sheet roots and the charge root admit phase
completions. Closed incoming sheet and charge parameters are classified
by `H1(C_N,Z)=0` and `H3(C_N,Z)=0`; there is no additional incoming
cohomology class to quotient. Their exact representatives are already
covered by the full cochain gauges. The four filtration layers each
have order `N`, so the completed presentation must have order `N^4`.
This order check alone does not determine its extensions.

## Canonical completed roots

Write group elements as `g^j`, `0<=j<N`, and use

```math
a(g^j)=j,\qquad
x(g^i,g^j)=\left\lfloor\frac{i+j}{N}\right\rfloor,
\qquad da=Nx,\qquad dx=0.
```

In the order E8, CI, charge, phase, choose

```math
X=\left(x,0,0,\frac{a x^2}{3N}\right),\qquad
Y=\left(0,x,0,\frac{a x^2}{6N}\right),\qquad
b=\left(0,0,0,\frac{a x^2}{N}\right).
```

The charge root has `n4=x^2`. The global solver obtains its phase from
an exact resolution primitive. The independent Python audit instead uses
the explicit phase `zeta^Z_(2,2)(x,x)/2`. Its differential is the charge
source: the two `x^3` terms in the integral Cartan identity cancel over
`F2`. These are two specified completion procedures; their phases need
not be pointwise equal.

The canonical sheets solve the complete source equations. Each root is
checked on the native resolution and on explicit normalized bar
simplices. The pilot then forms every `N`th power with the full product,
removes its sheets with the complete joint gauge, extracts and removes
its charge root, and solves the final exact phase. No phase from sheet
or charge removal is discarded.

## Actual root relations and final groups

All rows below use the same generator names `X,Y,Q,b`. The last relation
is always `Nb=0`.

| Internal group | Neutral root | CI root | Charge root | Final stacking group |
| --- | --- | --- | --- | --- |
| `C1` | no positive-degree root | no positive-degree root | no positive-degree root | `0` |
| `C2` | `2X=0` | `2Y=Q+b` | `2Q=b` | `Z2 × Z8` |
| `C3` | `3X=b` | `3Y=2b` | `3Q=0` | `Z3² × Z9` |
| `C4` | `4X=0` | `4Y=2Q` | `4Q=2b` | `Z2² × Z4 × Z16` |
| `C5` | `5X=0` | `5Y=0` | `5Q=0` | `Z5⁴` |
| `C6` | `6X=2b` | `6Y=3Q+b` | `6Q=3b` | `Z3 × Z6 × Z72` |

For example, `C2` has `4Y=b`, hence an order-eight CI root, while the
neutral root supplies an independent order-two class. For `C3`, `X`
has order nine, `Y-2X` has order three, and `Q` has order three. The two
sheet relations share `b`; the result is not the product of independent
E8 and CI classifications. The `C6` group also has the same primary
decomposition as the product of the computed `C2` and `C3` groups.

## Independent checks

The standard normalized cyclic five-cycle is

```math
\tau_5=\sum_{i,j=0}^{N-1}[g\mid g^i\mid g\mid g^j\mid g].
```

Terms containing an identity vanish. Pairing with `tau5` detects
`H5(C_N,R/Z)`, and `b(tau5)=1/N`. The Python audit constructs the
canonical cochains directly on these simplices, computes full powers
with `insulator.E8State`, removes sheets using `v=-a` or `u=-a`, and
removes a remaining charge multiple `kN x^2` using `w=-k a x`.
It reproduces every displayed presentation for `N=2,...,6`, without the
GAP resolution, its completed charge root, or its primitive solver.

The neutral coefficient also has a closed analytic check. The carry
cocycle `x` is binary and `x cup_1 x=0` over integers: in
`x(023)x(012)-x(013)x(123)`, closure equates the sums of two binary pairs,
and therefore their products. Neutral stacking produces no twister for
multiples of `x`. After removing `Nx` with `v=-a`, the phase is

```math
\frac{a x^2-N^2x^2a}{3}.
```

Both ordered numerators pair to one with `tau5`, so

```math
NX=\left[\frac{N(1-N^2)}3\bmod N\right]b
 =\begin{cases}(N/3)b,&3\mid N,\\0,&3\nmid N.\end{cases}
```

A separate resolution-only audit verifies
`d(nativePhasePrimitive)=residualNativePhase mod1` for all twenty stored
nontrivial root relations. The `C6` charge relation has a nonzero exact
residual and a nonzero primitive; requiring the residual cochain itself
to vanish would incorrectly reject this valid relation.

## Reproduction and scope

The isolated implementation is
[cyclic_4p1.g](../../formulas/examples/cyclic_4p1.g). It is valid for a
positive cyclic order with these specified backgrounds and does not
relax the general classifier's dimension checks. Run a fresh case with

```bash
python scripts/pilot_cyclic_4p1.py --order 2 --order 3 --output /path/to/new-run
```

Run the independent audit on saved records with

```bash
python scripts/audit_cyclic_4p1.py --input /path/to/saved-run --output /path/to/new-audit.json
```

`tests/test_pilot_cyclic_4p1.py` checks the smallest complete presentations,
the neutral `C3` cube on every normalized bar five-simplex, and the
independent bar-cycle reduction. The actual campaign additionally retains
the frozen source hash, input hashes, runtime logs, roots, gauges,
primitive witnesses, and Smith presentations.

These are complete global results of the specified four-data cochain
model. The records explicitly set `physicalClassificationCertified=false`:
the universal physical CI-kernel identification is not proved by these
calculations or by a matching abstract group. No intrinsic uniform
4+1D response has been added to this scoped calculation.
