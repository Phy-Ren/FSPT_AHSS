# Two-dimensional sectors: supplied-model audit, 2026-10-14

All 54 independently computed zero-IQH groups equal the exact n0 kernels of their full runs: generator cochains are identical, relation lattices agree by integer HNF, and independent SNF reproduces every listed group. The 20 nonzero-IQH-capable cases have actual image n0=Z; the other 34 have image zero.

R means the relative charge construction. I means the explicit full-IQH model whose universal physical product normalization remains open in the supplied note. All rows omit the independent E8 coordinate. A fixed allowed nonzero n0 is a torsor for A0, not the group in either group column. Zm^r denotes r copies of Zm.

| Family / group | A0 spinless | A0 spin-half | Full model spinless | Full model spin-half | n0 image | Status | Cell charge step (spinless / half) |
| --- | --- | --- | --- | --- | --- | --- | --- |
| point2 / C1 | 0 | 0 | Z | Z | Z | I | — |
| point2 / C2 | Z4 | Z4 | Z x Z4 | Z x Z4 | Z | I | — |
| point2 / Cs | 0 | 0 | 0 | 0 | 0 | R | — |
| point2 / C2v | Z4 | Z2^2 | Z4 | Z2^2 | 0 | R | — |
| point2 / C4 | Z2 x Z8 | Z2 x Z8 | Z x Z2 x Z8 | Z x Z2 x Z8 | Z | I | — |
| point2 / C4v | Z8 | Z2^3 | Z8 | Z2^3 | 0 | R | — |
| point2 / C3 | Z3^2 | Z3^2 | Z x Z3^2 | Z x Z3^2 | Z | I | — |
| point2 / C3v | Z3 | Z3 | Z3 | Z3 | 0 | R | — |
| point2 / C6 | Z3 x Z12 | Z3 x Z12 | Z x Z3 x Z12 | Z x Z3 x Z12 | Z | I | — |
| point2 / C6v | Z12 | Z2 x Z6 | Z12 | Z2 x Z6 | 0 | R | — |
| wallpaper / p1 | Z | Z | Z^2 | Z^2 | Z | I | 1 / 1 |
| wallpaper / p2 | Z x Z2 x Z4^3 | Z x Z2 x Z4^3 | Z^2 x Z2 x Z4^3 | Z^2 x Z2 x Z4^3 | Z | I | 1 / 1 |
| wallpaper / pm | Z x Z2 x Z4 | Z x Z2 x Z4 | Z x Z2 x Z4 | Z x Z2 x Z4 | 0 | R | 1 / 1 |
| wallpaper / pg | Z | Z | Z | Z | 0 | R | 2 / 2 |
| wallpaper / cm | Z x Z2 | Z x Z2 | Z x Z2 | Z x Z2 | 0 | R | 1 / 1 |
| wallpaper / pmm | Z x Z2^4 x Z4^3 | Z x Z2^8 | Z x Z2^4 x Z4^3 | Z x Z2^8 | 0 | R | 1 / 2 |
| wallpaper / pmg | Z x Z2 x Z4^2 | Z x Z2 x Z4^2 | Z x Z2 x Z4^2 | Z x Z2 x Z4^2 | 0 | R | 2 / 2 |
| wallpaper / pgg | Z x Z2 x Z4 | Z x Z2 x Z4 | Z x Z2 x Z4 | Z x Z2 x Z4 | 0 | R | 2 / 2 |
| wallpaper / cmm | Z x Z2^2 x Z4^2 | Z x Z2^4 x Z4 | Z x Z2^2 x Z4^2 | Z x Z2^4 x Z4 | 0 | R | 1 / 2 |
| wallpaper / p4 | Z x Z2 x Z4^2 x Z8 | Z x Z2 x Z4^2 x Z8 | Z^2 x Z2 x Z4^2 x Z8 | Z^2 x Z2 x Z4^2 x Z8 | Z | I | 1 / 1 |
| wallpaper / p4m | Z x Z2^3 x Z4 x Z8 | Z x Z2^7 | Z x Z2^3 x Z4 x Z8 | Z x Z2^7 | 0 | R | 1 / 2 |
| wallpaper / p4g | Z x Z2^2 x Z8 | Z x Z2^3 x Z4 | Z x Z2^2 x Z8 | Z x Z2^3 x Z4 | 0 | R | 2 / 2 |
| wallpaper / p3 | Z x Z3^5 | Z x Z3^5 | Z^2 x Z3^5 | Z^2 x Z3^5 | Z | I | 1 / 1 |
| wallpaper / p3m1 | Z x Z3 x Z6 | Z x Z3 x Z6 | Z x Z3 x Z6 | Z x Z3 x Z6 | 0 | R | 1 / 1 |
| wallpaper / p31m | Z x Z3 x Z6 | Z x Z3 x Z6 | Z x Z3 x Z6 | Z x Z3 x Z6 | 0 | R | 1 / 1 |
| wallpaper / p6 | Z x Z3 x Z6 x Z12 | Z x Z3 x Z6 x Z12 | Z^2 x Z3 x Z6 x Z12 | Z^2 x Z3 x Z6 x Z12 | Z | I | 1 / 1 |
| wallpaper / p6m | Z x Z2^2 x Z12 | Z x Z2^3 x Z6 | Z x Z2^2 x Z12 | Z x Z2^3 x Z6 | 0 | R | 1 / 2 |

Cell charge steps use completed charge roots and the actual primitive translation lattice. All ten wallpaper CI lifts chosen by the solver have zero additional cell charge, but a different IQH lift may be shifted by an A0 state. A printed literature free factor Z or 2Z is not a primitive-cell normalization without a separate coordinate map.

Reproduce with `python results/calibration_20261014/audit_2d_sectors.py`. This reads the immutable evidence archive and does not change the original runs or reports.
