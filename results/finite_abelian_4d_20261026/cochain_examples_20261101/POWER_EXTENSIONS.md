# Commuting fermion-parity extensions

These calculations support the cyclic and two-factor examples with a nontrivial fermion-parity power extension.
All groups considered here have unitary Abelian full symmetry.
The programs do not include noncommuting extensions.

## Symmetry and cochain primitives

Use `G_f=Z_(2M)^f x Z_N`, with `M` even, and the coordinate/carry cochains defined in [README.md](README.md).
The background is `omega2=[m2]_2` and `s1=0`.
Here `m1,m2` refer to the quotient factor of order `M`, and primes refer to the factor of order `N`.
The carry represents the extension even when four divides `M`, for which the square of the parity one-cocycle is cohomologically zero.

For the cyclic complex-fermion root, a pointwise phase primitive is

```math
n_2=n_3=0,\qquad n_4=[m_2^2]_2,\qquad
\nu_5=\frac{m_1m_2^2}{2M}
+\frac12\zeta_{2,2}([m_2]_2,[m_2]_2)\mod1.
```

The diagonal Cartan correction is essential: `Sq2[m2^2]_2` need not vanish pointwise for these bar representatives.
The differential of `zeta_{2,2}([m2]_2,[m2]_2)` is `Sq2[m2^2]_2` modulo two, while the rational term differentiates to the extension contribution `m2^3/2`.

For the mixed complex-fermion root, the analogous solution is

```math
n_2=n_3=0,\qquad n_4=[m_2m_2']_2,\qquad
\nu_5=\frac{m_2m_1'm_2'}{2N}
+\frac12\zeta_{2,2}([m_2]_2,[m_2']_2)\mod1.
```

Here the extension term cancels `m2^2 m2'/2` in the Cartan expansion, leaving `m2 (m2')^2/2`.
All displayed fractions use rational lifts before reduction modulo one.
The corrections become integral on doubling, so the cyclic and mixed roots double to the corresponding bosonic cocycles.

## Range of the abstract-group conclusion

The exhaustive two-primary extension tests cover

| `(M,N)` | Bosonic changes of integer-root power relations | Group for every change |
|---|---:|---|
| `(2,1)` | 2 | `Z16` |
| `(4,1)` | 4 | `Z2 x Z32` |
| `(2,2)` | 4 | `Z8 x Z16` |
| `(2,4)` | 64 | `Z2^2 x Z8 x Z16` |
| `(4,2)` | 16 | `Z2^2 x Z8 x Z32` |
| `(4,4)` | 4096 | `Z2^4 x Z16 x Z32` |

`N=1` means that the second factor is absent.
The cyclic odd-prime extension is trivial at primes other than three, and mixed odd-prime contributions are purely bosonic.
Prime decomposition therefore extends these results to `2 | M`, `8` not dividing `M` or `N`, and `3` not dividing `MN`.
This conclusion concerns the abstract stacking group, not the pointwise vanishing of a terminal cochain.
It applies to the nontrivial commuting power extensions above; split fermion parity with a quotient factor of order four has a nontrivial terminal extension and is not covered by this statement.
The higher-order counterexamples in the saved report limit the scope of the test and do not assert an exhaustive criterion at other orders.

## Run

Run from this directory:

```sh
python check_power_extension_cochains.py --output power_extension_cochain_results.json
python check_power_extension_terminal.py --output power_extension_terminal_results.json
python check_power_extension_formulas.py --output power_extension_formula_results.json
```

The scripts discover this checkout and parent formula package from their own paths, and also work when invoked by full path from another directory.
The cochain and terminal checks accept `--formula-repo` to select another checkout; the formula comparison accepts `--verification-dir` to select another copy of the finite-Abelian formula package.
The cochain check evaluates the cyclic and mixed complex-fermion phase primitives with their Cartan corrections, using exact rational arithmetic.
It exhausts cyclic orders two and four, and the pair of orders two and two.
It also checks reproducible samples for the other small cases and further even orders, including ten.
The proof for arbitrary orders is the Cartan identity and the pointwise vanishing of Sq1 on normalized cyclic carry cochains.
The sampled checks replay that identity; they do not replace it.
The cyclic first and second p+ip parity constraints and the incoming Majorana secondary obstruction are also evaluated.
The p+ip parity check uses the native formula coordinate and is not a claim that the physical upper-cochain representative is identically zero.

The terminal check starts with the archived exact relation matrices.
It extracts the subgroup with zero integer decoration and its embedded final bosonic subgroup by a Smith transformation.
It then varies every integer-root power relation by every bosonic element.
The six small nonsplit two-primary cases have unchanged invariant factors for all such choices.
This is an exhaustive test of every bosonic change compatible with the retained lower relations, not just a comparison with the archived final invariant factors.
The program also checks that the fourth obstruction vanishes on the integer-layer generators in the recorded cohomology quotient.
The saved JSON contains the source hashes, transported bosonic generators, reduced presentations, and every resulting group.
The higher-order counterexamples in that JSON illustrate the limits of the proved domain; they are not additional main-text examples.

The formula check compares the compact arbitrary-order layer and group expressions with the retained primary formulas.
Its default range contains 3200 layer calculations and 1458 group calculations with orders coprime to three.
These checks validate the simplification and assembly of established formulas.
They do not infer terminal independence from a known final group.
