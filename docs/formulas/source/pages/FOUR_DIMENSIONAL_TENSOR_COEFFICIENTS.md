# 4+1D finite tensor coefficients

The coefficient formula contains the following two binary sums on
$`(012345)`$:

```math
\begin{aligned}
&\sum_{(i,j,k,l,e)\in\mathcal C_{2,3}}
 \overline{\binom{n_2(012)}i}
 \overline{\binom{(-1)^{s_1(02)}n'_2(234)}j}
 \overline{\binom{(-1)^{s_1(02)}[n'_2(235)-n'_2(234)]}k}\\
&\qquad\times
 \overline{\binom{(-1)^{s_1(03)}n'_2(345)}l}
 [\check n'_3(2345)+\check\omega_2(023)\bar n'_2(345)]^e\\
&+\sum_{(i,j,k,l,e)\in\mathcal C_{3,2}}
 \overline{\binom{(-1)^{s_1(03)}n'_2(345)}i}
 \overline{\binom{n_2(012)}j}
 \overline{\binom{n_2(013)-n_2(012)}k}\\
&\qquad\times
 \overline{\binom{(-1)^{s_1(01)}n_2(123)}l}
 [\check n_3(0123)]^e.
\end{aligned}
```

Every coefficient in the two tables below is one. Binomials use integer
arithmetic, including negative arguments, before binary reduction. A
zeroth power is one. These are finite numerical coefficients; no auxiliary
physical field is assigned to a table column.

The additional background contribution is the ordinary cochain polynomial

```math
\begin{aligned}
s_1\Big[&\bar n_2\widetilde n'_2
 +(\widetilde n_2+\bar n_2)
                  \overline{\lfloor n'_2/4\rfloor}\\
&+(\overline{\lfloor n_2/4\rfloor}+\widetilde n_2
                         +\bar n_2\cup_2\widetilde n_2)
                      (\bar n'_2\cup_2\widetilde n'_2)\\
&+[s_1\cup_1(\widetilde n_2+\bar n_2)]
                     (\widetilde n'_2+\bar n'_2\cup_2\widetilde n'_2)\\
&+[s_1\cup_1(\overline{\lfloor n_2/4\rfloor}
                         +\bar n_2\cup_2\widetilde n_2)]\bar n'_2\Big].
\end{aligned}
```

For each index of the [physical face formula](FOUR_DIMENSIONAL_PHYSICAL_PATHS.md),
substitute its explicit physical factors into these two polynomials.
Use the decoded factors throughout: the signs and background correction
already printed here perform the conversion needed by these coefficients.
Thus the same face rule applies to both the kernel and these tensor terms.

The rows with $`e=0`$ contribute to $`\psi`$. For $`e=1`$, expand the
bracket before assigning origins: a physical Majorana value contributes
$`\gamma\psi`$, and its displayed integer-layer correction contributes
$`\psi`$. Apply the same rule to any additional background correction
in the physical path. The five-cup polynomial is entirely $`\psi`$.

## The 120 rows of $`\mathcal C_{2,3}`$

| $`i`$ | Tuples $`(j,k,l,e)`$ |
|---|---|
| 1 | (0,0,0,1), (0,0,1,0), (0,0,1,1), (0,0,3,0), (0,0,3,1), (0,1,0,1) |
| 1 | (0,1,1,0), (0,1,1,1), (0,1,2,0), (0,1,2,1), (0,1,3,0), (0,1,5,0) |
| 1 | (0,2,1,1), (0,2,2,0), (0,2,2,1), (0,2,3,0), (0,2,3,1), (0,2,4,0) |
| 1 | (0,3,0,1), (0,3,3,0), (0,4,2,0), (0,5,1,0), (1,0,0,1), (1,0,1,0) |
| 1 | (1,0,2,0), (1,1,0,0), (1,1,1,0), (1,1,1,1), (1,1,2,0), (1,1,2,1) |
| 1 | (1,3,3,0), (1,5,0,0), (2,0,1,0), (2,0,1,1), (2,0,2,1), (2,0,3,0) |
| 1 | (2,0,3,1), (2,1,1,1), (2,1,3,0), (2,2,0,0), (2,2,1,1), (2,2,3,0) |
| 1 | (2,3,0,0), (2,3,2,0), (2,4,0,0), (3,0,0,1), (3,0,1,0), (3,0,2,0) |
| 1 | (3,1,0,0), (3,1,1,1), (3,1,2,0), (3,1,3,0), (3,2,0,0), (3,2,1,0) |
| 1 | (3,3,0,0), (3,3,1,0), (4,2,0,0), (5,1,0,0) |
| 2 | (0,0,0,1), (0,0,1,0), (0,0,2,0), (0,0,3,0), (1,1,2,0), (2,1,1,0) |
| 3 | (0,0,1,1), (0,0,2,0), (0,0,3,1), (0,1,0,1), (0,1,3,0), (0,1,3,1) |
| 3 | (0,1,4,0), (0,2,1,0), (0,2,2,0), (0,2,3,0), (0,3,0,1), (0,3,2,0) |
| 3 | (0,4,1,0), (1,0,0,1), (1,0,1,1), (1,0,2,0), (1,0,3,0), (1,0,3,1) |
| 3 | (1,1,0,0), (1,1,1,0), (1,1,2,0), (1,2,0,0), (1,2,0,1), (1,2,1,1) |
| 3 | (1,2,3,0), (1,3,0,0), (1,3,1,0), (1,3,2,0), (1,4,0,0), (2,0,1,0) |
| 3 | (2,1,0,0), (2,1,0,1), (2,1,1,1), (2,1,2,0), (2,1,3,0), (2,2,0,0) |
| 3 | (2,2,1,0), (2,3,0,0), (2,3,1,0), (3,0,0,1), (3,0,1,0), (3,1,0,0) |
| 3 | (3,2,0,0), (4,1,0,0) |
| 4 | (0,1,3,0), (0,2,2,0), (0,3,1,0), (1,1,0,0), (1,1,1,0), (1,3,0,0) |
| 4 | (2,2,0,0), (3,1,0,0) |
| 5 | (0,1,2,0), (0,2,1,0), (1,2,0,0), (2,1,0,0) |

## The 106 rows of $`\mathcal C_{3,2}`$

| $`i`$ | Tuples $`(j,k,l,e)`$ |
|---|---|
| 1 | (0,0,0,1), (0,0,3,1), (0,1,1,0), (0,1,1,1), (0,1,3,1), (0,1,4,0) |
| 1 | (0,1,5,0), (0,2,1,0), (0,2,1,1), (0,2,4,0), (0,3,0,1), (0,3,1,1) |
| 1 | (0,3,3,0), (0,4,2,0), (0,5,1,0), (1,0,1,1), (1,0,2,0), (1,0,3,0) |
| 1 | (1,0,4,0), (1,1,0,0), (1,1,0,1), (1,1,1,0), (1,1,3,0), (1,1,3,1) |
| 1 | (1,2,0,0), (1,2,0,1), (1,2,1,0), (1,3,1,0), (1,3,1,1), (1,5,0,0) |
| 1 | (2,0,1,0), (2,0,2,0), (2,1,0,0), (2,1,2,1), (2,1,3,1), (2,2,0,0) |
| 1 | (2,3,0,0), (2,3,0,1), (2,3,1,0), (2,3,1,1), (2,4,0,0), (3,0,0,1) |
| 1 | (3,0,1,1), (3,0,2,1), (3,0,3,0), (3,0,3,1), (3,1,0,0), (3,1,1,1) |
| 1 | (3,1,2,0), (3,1,3,0), (3,2,0,1), (3,2,1,1), (3,3,0,0), (3,3,1,0) |
| 1 | (4,0,1,0), (4,1,0,0), (4,2,0,0), (5,1,0,0) |
| 2 | (0,0,0,1), (0,2,2,0), (1,0,1,0), (1,1,0,0), (2,2,0,0) |
| 3 | (0,0,1,1), (0,0,3,1), (0,1,0,1), (0,1,2,1), (0,1,4,0), (0,2,1,0) |
| 3 | (0,2,1,1), (0,2,2,0), (0,2,3,0), (0,3,0,1), (0,3,2,0), (0,4,1,0) |
| 3 | (1,0,0,1), (1,0,1,0), (1,0,1,1), (1,0,3,0), (1,0,3,1), (1,1,0,0) |
| 3 | (1,1,2,0), (1,1,2,1), (1,1,3,1), (1,2,1,0), (1,2,1,1), (1,3,0,1) |
| 3 | (1,3,1,1), (1,4,0,0), (2,0,1,1), (2,1,1,1), (2,2,0,0), (2,3,0,0) |
| 3 | (3,0,0,1), (3,1,0,1), (3,1,1,1), (3,2,0,0), (4,1,0,0) |
| 4 | (1,1,0,0), (1,1,1,0) |
| 5 | (0,1,1,0), (0,1,2,0), (0,2,1,0), (1,1,0,0), (1,2,0,0), (2,1,0,0) |
