# Current geometric pairing coordinate

The accompanying archive preserves the completed 2026-10-09 local census
verbatim. Its preliminary candidate-status text is historical: this reference
is now the canonical 3+1D coordinate. No archived arithmetic, graph constructor,
input, formula polynomial or receipt has been altered. The original six gamma
projection cases remain the fixed physical module.

The census independently constructs all 2^24 P graphs and all 2^24 F graphs,
with omega2 and s1, and compares directed-loop and matching-word parities.
It has zero formula mismatches. The included README specifies reproduction
and the modulo-four reduction for arbitrary signed copy counts.

From the repository root, run `python scripts/check_geometric_reference_3d.py`.
This extracts the frozen bundle to a temporary directory and compares the
maintained current API with 512 P and 512 F graphs in all four background
sectors. It also checks the explicit map to the retained coefficient kernels.

The phase transport is proved separately, with no microscopic-phase claim:

```sh
python docs/formulas/coefficients/verify_three_dimensional_geometric_phase_transport.py
python docs/formulas/coefficients/verify_three_dimensional_geometric_self_stacking.py
python scripts/check_z4ft_current_cochains.py
```

The first identity is exact in 45 independent bits; deleting omega2 B2 is a
negative control. The second compares all six current self-stacking phase
contributions, including the coordinate conversion, in twenty independent
valid-tower bits. The last checks every bar simplex for all four handwritten
time-reversal roots. These checks have distinct domains; no sampled check
is described as an exhaustive enumeration.
