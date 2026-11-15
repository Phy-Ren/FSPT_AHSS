# 3+1D geometric pairing census

The archive contains the local census of 2026-10-09. It builds all 2^24 P
graphs and all 2^24 F graphs, with omega2 and s1, and compares their
directed-loop and matching-word parities with the formulas. There are no
mismatches. Its own README describes the reproduction and the reduction
modulo four for arbitrary integer layer numbers.

From the repository root, run `python scripts/check_geometric_reference_3d.py`.
It extracts the archive into a temporary directory and compares the current
code with 512 P and 512 F graphs in each of the four background sectors. It
also checks the map [from the code to the formulas](../../THREE_DIMENSIONAL_GEOMETRIC_REFERENCE.md).

The phase identities of that map are checked by

```sh
python docs/formulas/coefficients/verify_three_dimensional_bare_formulas.py
python docs/formulas/coefficients/verify_three_dimensional_geometric_phase_transport.py
python docs/formulas/coefficients/verify_three_dimensional_geometric_self_stacking.py
python scripts/check_z4ft_current_cochains.py
```

The first checks the change from the code argument n3 + B3 to n3, the closed
sector and the self-stacking formulas. The second proves the change of the
output face reference exactly in 45 independent bits; deleting omega2 B2 is a
negative control. The third compares all six self-stacking contributions of
the code in twenty independent valid-tower bits. The last checks every bar
simplex for all four time-reversal roots.
