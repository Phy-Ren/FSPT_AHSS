# Ordinary-word table for the 3+1D complex-fermion exchange

**Phase convention:** physical, as fixed in the [formula guide](../FORMULA_GUIDE.md#phase-convention): the forward F move carries $`\nu`$, the consistency loop runs forward along $`D`$ and back along $`N`$, the insertions are $`X=P\Gamma`$ and $`\bar X=\bar P\Gamma^\dagger`$, and coefficients are signed minimal representatives.

The 132 words below are the normalized MS-word form of the complex-fermion
exchange in the [complex-fermion–p+ip stacking contribution](THREE_DIMENSIONAL.md#eq-t3b).
The [thirteen-product identity](THREE_DIMENSIONAL_CF_EXCHANGE_REDUCTION.md)
writes the same sum with the lower obstruction. Here
$`B_3=n_2\cup_1n_2`$ on each state.

Every row is the standard normalized MS operation on its displayed physical arguments. Binary arithmetic applies throughout. The source and its primed counterpart are the full lower obstruction, including both Majorana and integer contributions.

## The actual open-Majorana correction

The 132 rows below omit 54 degree-impossible words whose normalized
interval-cut tables are empty. This is an exact cochain identity.

| Word | Inputs |
|---|---|
| 1,2,1,2,3,1,2 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,n'_2)`$ |
| 1,2,1,3,1,2,1 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,n'_2)`$ |
| 1,2,1,3,1,4,1,3,4 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n_3+B_3,n_2)`$ |
| 1,2,1,3,1,4,1,3,4 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n'_3+B'_3,n_2)`$ |
| 1,2,1,3,2,3,1 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,n'_2)`$ |
| 1,2,1,3,2,3,1 | $`(n_2,n_3+B_3,\widetilde{\omega}_2[n'_1]_2)`$ |
| 1,2,1,3,4,1,3,1,4 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n_3+B_3)`$ |
| 1,2,1,3,4,1,3,1,4 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n'_3+B'_3)`$ |
| 1,2,1,3,4,1,3,1,4 | $`(n_3+B_3,s_1,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,1,3,4,1,3,1,4 | $`(n'_3+B'_3,s_1,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,1,3,4,2,4,3,4 | $`(s_1,n_3+B_3,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,1,3,4,2,4,3,4 | $`(s_1,n_3+B_3,n_2,\widetilde{\omega}_2[n'_1]_2)`$ |
| 1,2,1,3,4,2,4,3,4 | $`(s_1,n'_3+B'_3,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,1,3,4,2,4,3,4 | $`(s_1,n'_3+B'_3,n_2,\widetilde{\omega}_2[n'_1]_2)`$ |
| 1,2,1,3,4,3,1,3,4 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n_3+B_3,n_2)`$ |
| 1,2,1,3,4,3,1,3,4 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n'_3+B'_3,n_2)`$ |
| 1,2,1,3,4,3,1,3,4 | $`(n_3+B_3,s_1,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,1,3,4,3,1,3,4 | $`(n'_3+B'_3,s_1,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,1,3,4,3,4,1,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,1,3,4,3,4,1,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n_2)`$ |
| 1,2,1,3,4,3,4,1,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n'_2)`$ |
| 1,2,1,3,4,3,4,1,3 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n_3+B_3,n_2)`$ |
| 1,2,1,3,4,3,4,1,3 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,1,3,4,3,4,1,3 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n'_3+B'_3,n_2)`$ |
| 1,2,1,3,4,3,4,2,4 | $`(s_1,n_3+B_3,n_2,\widetilde{\omega}_2[n'_1]_2)`$ |
| 1,2,1,3,4,3,4,2,4 | $`(s_1,n'_3+B'_3,n_2,\widetilde{\omega}_2[n'_1]_2)`$ |
| 1,2,3,1,2,1,2 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,n'_2)`$ |
| 1,2,3,1,2,1,2 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,n'_2)`$ |
| 1,2,3,1,2,1,4,1,2 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,1,2,1,4,1,2 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n'_2)`$ |
| 1,2,3,1,2,1,4,1,2 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n_2)`$ |
| 1,2,3,1,2,1,4,1,2 | $`(\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,1,2,4,1,2,1 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,1,2,4,1,2,1 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,1,2,4,1,3,4 | $`(n_3+B_3,s_1,n'_2,\widetilde{\omega}_2[n_1]_2)`$ |
| 1,2,3,1,2,4,1,3,4 | $`(n'_3+B'_3,s_1,n'_2,\widetilde{\omega}_2[n_1]_2)`$ |
| 1,2,3,1,2,4,1,4,2 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,1,2,4,1,4,2 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n'_2)`$ |
| 1,2,3,1,2,4,1,4,2 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n_2)`$ |
| 1,2,3,1,2,4,1,4,2 | $`(\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,1,2,4,1,4,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n_3+B_3)`$ |
| 1,2,3,1,2,4,1,4,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n'_3+B'_3)`$ |
| 1,2,3,1,2,4,1,4,3 | $`(n_3+B_3,s_1,n'_2,\widetilde{\omega}_2[n_1]_2)`$ |
| 1,2,3,1,2,4,1,4,3 | $`(n'_3+B'_3,s_1,n'_2,\widetilde{\omega}_2[n_1]_2)`$ |
| 1,2,3,1,2,4,2,1,4 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n_2)`$ |
| 1,2,3,1,2,4,2,1,4 | $`(\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,1,2,4,2,4,1 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n_2)`$ |
| 1,2,3,1,2,4,2,4,1 | $`(\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,1,3,2,1 | $`(n_3+B_3,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,3,1,3,2,1 | $`(n_3+B_3,n_2,\widetilde{\omega}_2[n'_1]_2)`$ |
| 1,2,3,1,4,1,2,1,4 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,1,4,1,2,1,4 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n'_2)`$ |
| 1,2,3,1,4,1,2,1,4 | $`(n_3+B_3,n'_2,s_1,\widetilde{\omega}_2[n_1]_2)`$ |
| 1,2,3,1,4,1,2,1,4 | $`(n'_3+B'_3,n'_2,s_1,\widetilde{\omega}_2[n_1]_2)`$ |
| 1,2,3,1,4,1,3,1,4 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,3,1,4,1,3,1,4 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n'_2)`$ |
| 1,2,3,1,4,1,3,1,4 | $`(n_3+B_3,s_1,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,3,1,4,1,3,1,4 | $`(n_3+B_3,s_1,\widetilde{\omega}_2[n'_1]_2,n_2)`$ |
| 1,2,3,1,4,1,3,1,4 | $`(n'_3+B'_3,s_1,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,3,1,4,1,3,1,4 | $`(n'_3+B'_3,s_1,\widetilde{\omega}_2[n'_1]_2,n_2)`$ |
| 1,2,3,1,4,2,1,2,4 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,1,4,2,1,2,4 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n'_2)`$ |
| 1,2,3,1,4,2,1,4,1 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,1,4,2,1,4,1 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n'_2)`$ |
| 1,2,3,1,4,2,1,4,1 | $`(\widetilde{\omega}_2[n_1]_2,n'_2,s_1,n_3+B_3)`$ |
| 1,2,3,1,4,2,1,4,1 | $`(\widetilde{\omega}_2[n_1]_2,n'_2,s_1,n'_3+B'_3)`$ |
| 1,2,3,1,4,2,1,4,2 | $`(n_3+B_3,n'_2,s_1,\widetilde{\omega}_2[n_1]_2)`$ |
| 1,2,3,1,4,2,1,4,2 | $`(n'_3+B'_3,n'_2,s_1,\widetilde{\omega}_2[n_1]_2)`$ |
| 1,2,3,1,4,2,4,1,4 | $`(\widetilde{\omega}_2[n_1]_2,n'_2,s_1,n_3+B_3)`$ |
| 1,2,3,1,4,2,4,1,4 | $`(\widetilde{\omega}_2[n_1]_2,n'_2,s_1,n'_3+B'_3)`$ |
| 1,2,3,2,1,3,1 | $`(\widetilde{\omega}_2[n_1]_2,n'_2,n_3+B_3)`$ |
| 1,2,3,2,1,3,1 | $`(\widetilde{\omega}_2[n_1]_2,n'_2,n'_3+B'_3)`$ |
| 1,2,3,2,1,3,1 | $`(n_2,\widetilde{\omega}_2[n'_1]_2,n_3+B_3)`$ |
| 1,2,3,2,1,3,1 | $`(n_2,\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3)`$ |
| 1,2,3,2,1,4,1,4,2 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,2,1,4,1,4,2 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,2,1,4,1,4,2 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n'_2)`$ |
| 1,2,3,2,1,4,1,4,2 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n_2)`$ |
| 1,2,3,2,1,4,1,4,2 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,2,1,4,1,4,2 | $`(\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,2,3,1,2 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,n'_2)`$ |
| 1,2,3,2,3,1,2 | $`(n_2,n'_3+B'_3,\widetilde{\omega}_2[n'_1]_2)`$ |
| 1,2,3,2,3,2,1 | $`(n_2,\widetilde{\omega}_2[n'_1]_2,n_3+B_3)`$ |
| 1,2,3,2,3,2,1 | $`(n_2,\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3)`$ |
| 1,2,3,2,4,1,2,1,4 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n_2)`$ |
| 1,2,3,2,4,1,2,1,4 | $`(\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,2,4,1,2,4,1 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n_2)`$ |
| 1,2,3,2,4,1,2,4,1 | $`(\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,2,4,1,4,1,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n_3+B_3)`$ |
| 1,2,3,2,4,1,4,1,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n'_3+B'_3)`$ |
| 1,2,3,2,4,1,4,2,1 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n_2)`$ |
| 1,2,3,2,4,1,4,2,1 | $`(\widetilde{\omega}_2[n'_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,2,4,2,3,2,4 | $`(s_1,\widetilde{\omega}_2[n_1]_2,n_3+B_3,n'_2)`$ |
| 1,2,3,2,4,2,3,2,4 | $`(s_1,\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,n'_2)`$ |
| 1,2,3,2,4,3,1,4,1 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n_3+B_3)`$ |
| 1,2,3,2,4,3,1,4,1 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n'_3+B'_3)`$ |
| 1,2,3,4,1,3,1,3,4 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,3,4,1,3,1,3,4 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n'_2)`$ |
| 1,2,3,4,1,3,1,3,4 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n_3+B_3,n_2)`$ |
| 1,2,3,4,1,3,1,3,4 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n'_3+B'_3,n_2)`$ |
| 1,2,3,4,1,3,1,4,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,3,4,1,3,1,4,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n'_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n_3+B_3)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_2,n'_3+B'_3)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n_3+B_3,n_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n'_3+B'_3,n_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(n_3+B_3,s_1,\widetilde{\omega}_2[n'_1]_2,n_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(n_3+B_3,s_1,\widetilde{\omega}_2[n'_1]_2,n'_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(n'_3+B'_3,s_1,\widetilde{\omega}_2[n_1]_2,n_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(n'_3+B'_3,s_1,\widetilde{\omega}_2[n'_1]_2,n_2)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(n'_2,s_1,\widetilde{\omega}_2[n_1]_2,n_3+B_3)`$ |
| 1,2,3,4,1,3,4,1,3 | $`(n'_2,s_1,\widetilde{\omega}_2[n_1]_2,n'_3+B'_3)`$ |
| 1,2,3,4,1,3,4,3,1 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,3,4,1,3,4,3,1 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n_2)`$ |
| 1,2,3,4,1,3,4,3,1 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n'_2)`$ |
| 1,2,3,4,1,3,4,3,1 | $`(\widetilde{\omega}_2[n'_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,3,4,1,3,4,3,1 | $`(n_3+B_3,s_1,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,3,4,1,3,4,3,1 | $`(n_3+B_3,s_1,\widetilde{\omega}_2[n'_1]_2,n'_2)`$ |
| 1,2,3,4,1,3,4,3,1 | $`(n'_3+B'_3,s_1,\widetilde{\omega}_2[n_1]_2,n_2)`$ |
| 1,2,3,4,1,3,4,3,1 | $`(n'_3+B'_3,s_1,\widetilde{\omega}_2[n_1]_2,n'_2)`$ |
| 1,2,3,4,2,1,2,4,1 | $`(\widetilde{\omega}_2[n_1]_2,n_3+B_3,s_1,n'_2)`$ |
| 1,2,3,4,2,1,2,4,1 | $`(\widetilde{\omega}_2[n_1]_2,n'_3+B'_3,s_1,n'_2)`$ |
| 1,2,3,4,3,1,4,3,1 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n_3+B_3,n'_2)`$ |
| 1,2,3,4,3,1,4,3,1 | $`(\widetilde{\omega}_2[n_1]_2,s_1,n'_3+B'_3,n'_2)`$ |
| 1,2,3,4,3,2,3,4,3 | $`(s_1,n_2,\widetilde{\omega}_2[n'_1]_2,n_3+B_3)`$ |
| 1,2,3,4,3,2,3,4,3 | $`(s_1,n_2,\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3)`$ |
| 1,2,3,4,3,2,4,2,3 | $`(s_1,\widetilde{\omega}_2[n_1]_2,n'_2,n_3+B_3)`$ |
| 1,2,3,4,3,2,4,2,3 | $`(s_1,\widetilde{\omega}_2[n_1]_2,n'_2,n'_3+B'_3)`$ |
| 1,2,3,4,3,2,4,2,3 | $`(s_1,n_2,\widetilde{\omega}_2[n'_1]_2,n_3+B_3)`$ |
| 1,2,3,4,3,2,4,2,3 | $`(s_1,n_2,\widetilde{\omega}_2[n'_1]_2,n'_3+B'_3)`$ |

## The retained lower-fermion correction

The 22 rows below omit 36 further words with empty normalized
interval-cut tables at their displayed physical degrees.


| Word | Inputs |
|---|---|
| 1,2,1,2,3,1,3 | $`(\mathcal{𝒪}_4[n_1,n_2],n_2,n'_2)`$ |
| 1,2,1,2,3,1,3 | $`(\mathcal{𝒪}_4[n_1,n_2],n'_2,n_2)`$ |
| 1,2,1,2,3,1,3 | $`(\mathcal{𝒪}_4[n_1,n_2],\omega_2,n'_2)`$ |
| 1,2,1,2,3,1,3 | $`(\mathcal{𝒪}_4[n'_1,n'_2],n'_2,n_2)`$ |
| 1,2,1,2,3,1,3 | $`(\mathcal{𝒪}_4[n'_1,n'_2],\omega_2,n_2)`$ |
| 1,2,1,3,1,4,1,3,4 | $`(\mathcal{𝒪}_4[n_1,n_2],s_1,n'_2,n'_2)`$ |
| 1,2,1,3,1,4,1,3,4 | $`(\mathcal{𝒪}_4[n'_1,n'_2],s_1,n_2,n_2)`$ |
| 1,2,1,3,2,3,1 | $`(n_2,\mathcal{𝒪}_4[n_1,n_2],n'_2)`$ |
| 1,2,1,3,4,1,3,1,4 | $`(\mathcal{𝒪}_4[n_1,n_2],s_1,n'_2,n'_2)`$ |
| 1,2,1,3,4,1,3,1,4 | $`(\mathcal{𝒪}_4[n'_1,n'_2],s_1,n_2,n_2)`$ |
| 1,2,1,3,4,1,3,4,1 | $`(\mathcal{𝒪}_4[n_1,n_2],s_1,n_2,n'_2)`$ |
| 1,2,1,3,4,1,3,4,1 | $`(\mathcal{𝒪}_4[n_1,n_2],s_1,n'_2,n'_2)`$ |
| 1,2,1,3,4,1,3,4,1 | $`(\mathcal{𝒪}_4[n'_1,n'_2],s_1,n_2,n_2)`$ |
| 1,2,1,3,4,1,3,4,1 | $`(\mathcal{𝒪}_4[n'_1,n'_2],s_1,n_2,n'_2)`$ |
| 1,2,1,3,4,1,4,3,1 | $`(\mathcal{𝒪}_4[n_1,n_2],s_1,n_2,n'_2)`$ |
| 1,2,1,3,4,1,4,3,1 | $`(\mathcal{𝒪}_4[n'_1,n'_2],s_1,n_2,n'_2)`$ |
| 1,2,1,3,4,3,1,3,4 | $`(\mathcal{𝒪}_4[n_1,n_2],s_1,n_2,n'_2)`$ |
| 1,2,1,3,4,3,1,3,4 | $`(\mathcal{𝒪}_4[n'_1,n'_2],s_1,n_2,n'_2)`$ |
| 1,2,3,1,3,2,1 | $`(\mathcal{𝒪}_4[n_1,n_2],n_2,n'_2)`$ |
| 1,2,3,2,1,3,1 | $`(n_2,n'_2,\mathcal{𝒪}_4[n_1,n_2])`$ |
| 1,2,3,2,1,3,1 | $`(n_2,n'_2,\mathcal{𝒪}_4[n'_1,n'_2])`$ |
| 1,2,3,2,3,1,2 | $`(n_2,\mathcal{𝒪}_4[n'_1,n'_2],n'_2)`$ |

## Stacking-carry insertion

The third correction is exactly the two explicitly displayed $`P_4`$ terms, differing by the physical carry $`[n_1]_2[n'_1]_2`$. The eight-row $`P_4`$ table is printed in [the stacking formulas](THREE_DIMENSIONAL.md#eq-t3b). Ordinary multilinearity and the overlapping-word composition rule give its 56 rows; each choice contains the displayed p+ip stacking carry.
