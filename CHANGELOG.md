# Changelog

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
