# Changelog

## 2026-11-04: phase convention unified with the published lattice papers

All formula pages, manuscript exports and the closed-Majorana evaluators now
use one physical phase convention, the one of the published fixed-point
lattice constructions. It is stated once in the
[formula guide](docs/FORMULA_GUIDE.md#phase-convention), and every formula
page names it in its header.

- Convention: the forward F move carries $\nu$; the consistency loop runs
  forward along the odd-omitted-vertex path and back along the
  even-omitted-vertex path, so $d_{s_1}\nu=\mathcal O$; Majorana insertions
  are $X=P\Gamma$ and $\bar X=\bar P\Gamma^\dagger$; stacking is
  $\mathcal V=\nu+\nu'+\mathcal E$ with
  $d_{s_1}\mathcal E=\mathcal O[N]-\mathcal O[n]-\mathcal O[n']$;
  coefficients are signed minimal representatives.
- 2+1D: the Majorana stacking twister is the lattice result. Its
  antiunitary quarter term is $-\tfrac14[s_1n_1n'_1]_2$, and the
  self-stacking twister has no separate $\tfrac12s_1\beta n_1$ term.
- 3+1D: the closed-Majorana sector is written in the physical occupation
  $n_3$ with the lattice-sign Majorana phase. The terminal p+ip layer is
  written in $\widetilde n_3=n_3+\widetilde n_2\cup_1\widetilde n_2$ with physical
  phases; every quarter-, eighth- and sixteenth-valued coefficient changed
  sign, and half-valued terms are unchanged. The bridging identity relates
  the two forms.
- 4+1D: the closed-Majorana sector is written in the physical occupation
  $n_4$ with the quarter bracket $-\tfrac14$; lower p+ip layers use $n_4$
  with $dn_4=\mathcal O_5+dR_4$; the terminal p+ip layer is written in
  $\widetilde n_4=n_4+R_4$, where the existing expressions were already
  physical. The two-input pairing reference of the physical P move is
  written out explicitly. The microscopic heptagon table is related by
  $\mathcal O^{\mathrm{phys}}=-\mathcal O^{\mathrm{table}}$.
- Code: the closed-Majorana transcriptions (`fspt/formulas.py`,
  `fspt/majorana_complete.py`) and their generated GAP data and compiled
  programs use the same convention: they evaluate the displayed formulas,
  except that the 4+1D closed product keeps its documented output
  coboundary and phase-coordinate change. The complete runtime evaluates the
  same convention in every dimension: the backend applies the orientation
  sign of the 3+1D parameter integration to all 3+1D phase outputs, and no
  routine of the complete GAP engine computes a 3+1D quarter-, eighth- or
  sixteenth-valued phase itself. The compiled programs are unchanged. Archived results keep the
  frozen sources recorded with them, which use the earlier orientation, and
  remain reproducible as historical records; see the
  [programmer translation](formulas/CODE_NOTATION.md#phase-convention-of-the-runtime).
- Calibration cochains and printed example values were converted and
  re-verified with their scripts.
- Results: in 3+1D and 4+1D the changes are a global complex conjugation
  and changes of cochain coordinates, which are group isomorphisms. In 2+1D
  the lattice twister differs from the previous one by the closed term
  $\tfrac12s_1n_1n'_1$; all catalogued 2+1D calculations were rerun with it.
  The stored classification and stacking groups and layer filtrations are
  unchanged, and every example rerun for this change reproduces them.
