# Changelog

## 2026-11-15: 3+1D bosonic formulas corrected and verified

The displayed 3+1D bosonic formulas are now checked directly: closure,
stacking compatibility, exact reduction to the closed sector, both
self-stacking branches, the time-reversal example, and the relation to the
publication code ([3+1D verification](docs/formulas/verification/three_dimensional/README.md)).
This found and corrected three errors in the displayed formulas. Every stored
classification and stacking group is unchanged: the runtime evaluates the
phases of the code, which the new check confirms, and apart from a rephasing
of the stacking move the corrected terms vanish when $`dn_2=dn'_2=0`$.

- $`\mathcal O_5^{\gamma\psi}`$ gains the four terms
  $`\frac12[\omega_2c+B_3\cup_1c+c\cup_1B_3+c\cup_1c]`$, $`c=n_2\cup_2dn_2`$.
  Without them $`d_{s_1}\mathcal O_5\neq0`$ when $`dn_2\neq0`$.
- $`\mathcal E_4^{c\psi}`$ gains $`B_3\cup_2B'_3+[\beta^-n_2]_2\cup_2[\beta^-n'_2]_2`$,
  uses $`[\beta^-n_2]_2`$ instead of $`B_3`$ in the terms with $`\lambda_2^\gamma`$,
  and has a corrected stacking-move rephasing. The leftover symbol $`R'_3`$ is
  now $`B'_3`$.
- The torsion self-stacking contributions $`\mathcal E_4^{c\psi}`$ and
  $`\mathcal E_4^\gamma`$ are rewritten from the general law. Both face tables
  were regenerated from the general law on all $`2^{16}`$ inputs and are unchanged.
- The lattice parity of the F and P moves is enumerated on all $`2^{24}`$
  inputs of each move, with the order of effective Majorana zero modes used in
  the 3+1D stacking paper; it equals $`\mathcal O_4`$ and $`\mathcal E_3`$.
- Removed: the earlier census archive and the scripts of the earlier 3+1D
  coordinate (`fspt/geometric_reference_3d.py`, `scripts/check_geometric_reference_3d.py`,
  `scripts/check_z4ft_current_cochains.py`, and five coefficient verifiers with
  their certificates). The 3+1D term manifests use the printed expressions as
  field names; the complex-fermion and Majorana phases of the code moved to
  `docs/formulas/verification/three_dimensional/code_phases`.

## 2026-11-04: phase convention unified with the published lattice papers

All formula pages, manuscript exports and evaluators use one phase convention,
the one of the published fixed-point lattice constructions. It is stated once
in the [formula guide](docs/FORMULA_GUIDE.md#phase-convention), and every
formula page names it in its header.

- Convention: the forward F move carries $\nu$; the consistency loop runs
  forward along the odd-omitted-vertex path and back along the
  even-omitted-vertex path, so $d_{s_1}\nu=\mathcal O$; Majorana insertions
  are $X=P\Gamma$ and $\bar X=\bar P\Gamma^\dagger$; stacking is
  $\mathcal V=\nu+\nu'+\mathcal E$ with
  $d_{s_1}\mathcal E=\mathcal O[N]-\mathcal O[n]-\mathcal O[n']$;
  coefficients are signed minimal representatives.
- 2+1D: the Majorana stacking twister is the lattice result, with
  antiunitary quarter term $-\tfrac14[s_1n_1n'_1]_2$; the self-stacking
  twister has seven terms.
- 3+1D: the closed-Majorana sector is written in the physical occupation
  $n_3$; the terminal p+ip layer is written in
  $\widetilde n_3=n_3+\widetilde n_2\cup_1\widetilde n_2$. The bridging identity
  relates the two forms.
- 4+1D: the closed-Majorana sector is written in the physical occupation
  $n_4$, lower p+ip layers obey $dn_4=\mathcal O_5+dR_4$, and the terminal
  p+ip layer is written in $\widetilde n_4=n_4+R_4$. The two-input pairing
  reference of the physical P move is written out explicitly.
- Code: the closed-Majorana evaluators, the generated GAP data and the
  complete runtime evaluate the same convention. The 3+1D parameter
  integration uses the orientation fixed in the formula guide's operations.
  Earlier revisions used the opposite orientation; archived results keep the
  frozen sources recorded with them.
- Calibration cochains, printed example values and coefficient verifiers were
  updated and re-verified with their scripts. All stored classification and
  stacking groups and layer filtrations are unchanged, and every example
  rerun for this change reproduces them.
