# 4+1D stacking verification

Direct checks of the displayed 4+1D bosonic stacking corrections: the
[general law](../../FOUR_DIMENSIONAL.md#eq-t4c), the
[self-stacking law](../../FOUR_DIMENSIONAL_SELF_STACKING.md), the
[closed-Majorana law (M3E)](../../MAJORANA_AND_ENDPOINTS.md#eq-m3-stacking-4d)
and the [zero-p+ip self-stacking law](../../FOUR_DIMENSIONAL_MAJORANA_DIAGONAL.md).
All arithmetic is exact. Run from this directory:

```sh
python check_stacking.py 40 12   # samples per check, worker processes; about 20 minutes on 12 cores
```

The receipt is written to [`results/STACKING_CHECK.json`](results/STACKING_CHECK.json).

## Modules

| File | Content |
|---|---|
| [`stacking.py`](stacking.py) | The displayed formulas, transcribed display by display: the lower layers $`\mathcal O_4,\mathcal O_5,\mathcal E_4`$, the Majorana contribution with its 455 MS words, four lifts, $`\Theta_5`$ and the P-move phase with the 129 products of $`b_4`$, the quarter numerators, the explicit terms of the Majorana–p+ip and p+ip contributions, and the closed and diagonal laws. The coefficient sums are read from the published coefficient files and evaluated with the lower operations of the formula pages. |
| [`check_stacking.py`](check_stacking.py) | Random exact lower towers and the comparisons below. |

## Checks

The states are random exact solutions of $`d_{s_1}n_2=0`$, $`dn_3=\mathcal O_4`$,
$`dn_4=\mathcal O_5`$ with signed integer $`n_2`$, open $`n_3`$, and closed
backgrounds in the four sectors ($`\omega_2`$ and $`s_1`$ zero or not).

- **general**: on a five-simplex the displayed $`\mathcal E_5`$ equals the stacking
  correction of the code (`product_4_bosonic` plus the transfer $`Z_5`$).
- **cocycle**: on a six-simplex,
  $`d_{s_1}\mathcal E_5=\mathcal O_6[N]-\mathcal O_6[n]-\mathcal O_6[n']`$ with the
  displayed $`\mathcal E_5`$ on each of the seven five-faces and the obstruction of the
  code (the displayed obstruction).
- **self**: for equal upper and lower states the displayed self-stacking
  correction equals the code.
- **closed**: at $`n_2=n'_2=0`$ the law (M3E) equals the code, the Majorana
  contribution of the general law equals (M7), and the contributions with p+ip
  decoration vanish.
- **diagonal**: at $`n_2=0`$ and equal states the zero-p+ip self-stacking law equals
  the code and the displayed self-stacking correction.
