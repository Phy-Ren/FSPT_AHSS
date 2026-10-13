# Insulator calculation summary

Only saved results and saved comparison statuses are displayed. Spin labels are physical crystalline conventions.
Two-dimensional groups are the computed n0=0 subgroup. IQH multiplicity m means the full calculation permits n0 in mZ; 0 means forbidden. The full groups are retained in the CSV.
Three-dimensional groups cover the CI, charge and group-cohomological phase sector. Where available, the displayed reference is the quotient by the source's named neutral E8 root; this is an abstract comparison, not an implemented E8 cochain map.

## 2+1D point groups

| Group | Spinless, n0=0 | Spin-half, n0=0 | IQH m, spinless / spin-half | Comparison, spinless / spin-half |
| --- | --- | --- | --- | --- |
| C1 | 0 | 0 | 1 / 1 | both: stacking: match; rotation control: match |
| C2 | Z4 | Z4 | 1 / 1 | both: stacking: printed discrepancy; rotation control: match |
| Cs | 0 | 0 | 0 (forbidden) / 0 (forbidden) | both: stacking: match |
| C2v | Z4 | Z2^2 | 0 (forbidden) / 0 (forbidden) | both: stacking: match |
| C4 | Z2 x Z8 | Z2 x Z8 | 1 / 1 | both: stacking: printed discrepancy; rotation control: match |
| C4v | Z8 | Z2^3 | 0 (forbidden) / 0 (forbidden) | both: stacking: match |
| C3 | Z3^2 | Z3^2 | 1 / 1 | both: stacking: match; rotation control: match |
| C3v | Z3 | Z3 | 0 (forbidden) / 0 (forbidden) | both: stacking: match |
| C6 | Z3 x Z12 | Z3 x Z12 | 1 / 1 | both: stacking: printed discrepancy; rotation control: match |
| C6v | Z12 | Z2 x Z6 | 0 (forbidden) / 0 (forbidden) | both: stacking: match |

## 2+1D wallpaper groups

| Group | Spinless, n0=0 | Spin-half, n0=0 | IQH m, spinless / spin-half | Comparison, spinless / spin-half |
| --- | --- | --- | --- | --- |
| p1 | Z | Z | 1 / 1 | both: charge/phase/stacking: match; filling: normalization unmapped |
| p2 | Z x Z2 x Z4^3 | Z x Z2 x Z4^3 | 1 / 1 | both: charge/phase/stacking: match; filling: normalization unmapped |
| pm | Z x Z2 x Z4 | Z x Z2 x Z4 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| pg | Z | Z | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| cm | Z x Z2 | Z x Z2 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| pmm | Z x Z2^4 x Z4^3 | Z x Z2^8 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| pmg | Z x Z2 x Z4^2 | Z x Z2 x Z4^2 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| pgg | Z x Z2 x Z4 | Z x Z2 x Z4 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| cmm | Z x Z2^2 x Z4^2 | Z x Z2^4 x Z4 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| p4 | Z x Z2 x Z4^2 x Z8 | Z x Z2 x Z4^2 x Z8 | 1 / 1 | both: charge/phase/stacking: match; filling: normalization unmapped |
| p4m | Z x Z2^3 x Z4 x Z8 | Z x Z2^7 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| p4g | Z x Z2^2 x Z8 | Z x Z2^3 x Z4 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| p3 | Z x Z3^5 | Z x Z3^5 | 1 / 1 | both: charge/phase/stacking: match; filling: normalization unmapped |
| p3m1 | Z x Z3 x Z6 | Z x Z3 x Z6 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| p31m | Z x Z3 x Z6 | Z x Z3 x Z6 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |
| p6 | Z x Z3 x Z6 x Z12 | Z x Z3 x Z6 x Z12 | 1 / 1 | both: charge/phase/stacking: match; filling: normalization unmapped |
| p6m | Z x Z2^2 x Z12 | Z x Z2^3 x Z6 | 0 (forbidden) / 0 (forbidden) | both: charge/phase/stacking: match; filling: normalization unmapped |

## 3+1D point groups

| Group | Spinless | Spin-half | Reference, spinless / spin-half | Comparison, spinless / spin-half |
| --- | --- | --- | --- | --- |
| C1 | 0 | 0 | 0 / 0 | both: stacking: match |
| Ci | Z8 | Z8 | Z8 / Z8 | both: named-E8 quotient: match |
| C2 | 0 | 0 | 0 / 0 | both: stacking: match |
| Cs | Z8 | Z8 | Z8 / Z8 | both: named-E8 quotient: match |
| C2h | Z4 x Z8 | Z4 x Z8 | Z4 x Z8 / Z4 x Z8 | both: named-E8 quotient: match |
| D2 | 0 | Z2^2 | 0 / Z2^3 | stacking: match / stacking: mismatch |
| C2v | Z2^3 | Z4 x Z8 | Z2^3 / Z4 x Z8 | both: named-E8 quotient: match |
| D2h | Z2^6 x Z4 | Z2^4 x Z4^2 x Z8 | Z2^6 x Z4 / Z2^4 x Z4^2 x Z8 | both: named-E8 quotient: match |
| C4 | 0 | 0 | 0 / 0 | both: stacking: match |
| S4 | Z2 x Z4 | Z2 x Z4 | Z2^3 / Z2^3 | both: named-E8 quotient: mismatch |
| C4h | Z2 x Z4 x Z8 | Z2 x Z4 x Z8 | Z2 x Z4 x Z8 / Z2 x Z4 x Z8 | both: named-E8 quotient: match |
| D4 | 0 | Z2^2 | 0 / Z2^2 | both: stacking: match |
| C4v | Z2^3 | Z4 x Z8 | Z2^3 / Z4 x Z8 | both: named-E8 quotient: match |
| D2d | Z2^3 | Z2^2 x Z8 | Z2^2 x Z4 / Z2^4 x Z8 | both: named-E8 quotient: mismatch |
| D4h | Z2^6 x Z4 | Z2^4 x Z4^2 x Z8 | Z2^6 x Z4 / Z2^4 x Z4^2 x Z8 | both: named-E8 quotient: match |
| C3 | 0 | 0 | 0 / 0 | both: stacking: match |
| C3i | Z8 | Z8 | Z2 x Z4 / Z2 x Z4 | both: named-E8 quotient: mismatch |
| D3 | 0 | 0 | 0 / 0 | both: stacking: match |
| C3v | Z8 | Z8 | Z8 / Z8 | both: named-E8 quotient: match |
| D3d | Z4 x Z8 | Z4 x Z8 | Z2 x Z4 / Z2^2 x Z8 | both: named-E8 quotient: mismatch |
| C6 | 0 | 0 | 0 / 0 | both: stacking: match |
| C3h | Z8 | Z8 | Z8 / Z8 | both: named-E8 quotient: match |
| C6h | Z4 x Z8 | Z4 x Z8 | Z4 x Z8 / Z4 x Z8 | both: named-E8 quotient: match |
| D6 | 0 | Z2^2 | 0 / Z2^3 | stacking: match / stacking: mismatch |
| C6v | Z2^3 | Z4 x Z8 | Z2^3 / Z4 x Z8 | both: named-E8 quotient: match |
| D3h | Z2^3 | Z4 x Z8 | Z2^4 / Z2^2 x Z4 x Z8 | both: named-E8 quotient: mismatch |
| D6h | Z2^6 x Z4 | Z2^4 x Z4^2 x Z8 | Z2^6 x Z4 / Z2^4 x Z4^2 x Z8 | both: named-E8 quotient: match |
| T | 0 | 0 | 0 / 0 | both: stacking: match |
| Th | Z2^2 x Z4 | Z2^2 x Z8 | Z2^2 x Z4 / Z2^2 x Z8 | both: named-E8 quotient: match |
| O | 0 | Z2 | 0 / Z2 | both: stacking: match |
| Td | Z2^3 | Z2 x Z8 | Z2^3 / Z2 x Z8 | both: named-E8 quotient: match |
| Oh | Z2^4 x Z4 | Z2^3 x Z4 x Z8 | Z2^3 x Z4 / Z2^3 x Z4 x Z8 | named-E8 quotient: mismatch / named-E8 quotient: match |

A printed discrepancy remains a discrepancy even when the independent rotation control matches. That control concerns the interacting reduction of band-generated phases and does not prove absence of interaction-only roots.
Filling normalization remains unmapped until the source's decoration coordinates are matched to primitive-cell charge. Missing results and missing comparisons are never converted into agreement.

Source reports: `results/two_dimensional_20261013`, `results/three_dimensional_20261013`.
