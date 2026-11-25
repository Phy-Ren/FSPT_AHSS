# Changelog

## 2026-11-25: 4+1D stacking law printed in the physical occupation n_4

The general 4+1D stacking correction $`\mathcal E_5`$, its coefficient sums,
the self-stacking law, the closed sector, the zero-p+ip self-stacking page,
the group-inverse identity and the transfer appendix now use only the
physical occupation $`n_4`$ and the lower operations of the formula pages.
The printed $`\mathcal E_5`$ equals the stacking correction of the code term by
term. Every stored classification and stacking group, layer filtration and
example is unchanged.

- Correction: the general $`\mathcal E_5`$ printed since the change of
  2026-11-25 (parity count of the F move) was incorrect for $`n_2\neq0`$. Its
  coefficient sums $`\mathcal I_5^{\gamma\psi},\mathcal I_5^\psi`$ and the
  explicit terms of $`\mathcal E_5^{\gamma\psi},\mathcal E_5^\psi`$ had been derived
  with the compact lower operations of the transfer construction
  ($`\mathcal O_5^\psi`$ plus the differential of the polynomial in the last
  bracket of $`\mathcal E_4^\psi`$; $`n_3\cup_2dn_3`$ in $`\mathcal O_5^{\gamma\psi}`$;
  $`\mathcal E_4`$ plus $`\Delta(n_3\cup_2n_3+\text{that polynomial})+d(n_3\cup_3n'_3)`$),
  while that change defined $`\mathcal O_5^\psi`$, $`\mathcal O_5^{\gamma\psi}`$,
  $`\mathcal E_4^{\gamma\psi}`$ and $`\mathcal E_4^\psi`$ as the physical counts. Read
  with the page definitions, the printed law violated
  $`d_{s_1}\mathcal E_5=\Delta\mathcal O_6`$ by $`\tfrac12`$ on 18 of 36
  random states with $`n_2\neq0`$ (and on 6 of 10 against its own displayed
  $`\mathcal O_6`$); it was correct for $`n_2=n'_2=0`$.
  Read with the compact operations it still failed on 3 of 10 such states
  against its own obstruction: its occupation bracket did not complete the
  change of the complex-fermion coordinate. The law below is derived from
  the code directly and does not reuse that bracket.
- $`\mathcal E_5^{c\gamma}`$ is the exchange term
  $`\tfrac12[(\mathcal O_5^\gamma+\mathcal O_5^{\gamma\psi})\cup_4n'_4+\Delta(n_4\cup_4(\mathcal O_5^\gamma+\mathcal O_5^{\gamma\psi}))]`$;
  the occupation bracket written with the shifted coordinate is removed.
  The complex-fermion contributions contain every term that depends on
  $`n_4,n'_4`$.
- $`\mathcal E_5^\gamma`$ gains $`\tfrac12\Theta_5[n_3,n'_3]`$ (56 terms, open
  $`n_3`$) and the P-move phase $`d_{s_1}(\tfrac12b_4+\tfrac14n_3\cup_2n'_3)`$ with the
  129 face products of $`b_4`$ ([P-move rephasing](docs/formulas/FOUR_DIMENSIONAL_MAJORANA_STACKING_GAUGE.md#p-move-rephasing)).
  At $`n_2=n'_2=0`$ the complete law equals the closed-Majorana law of the thesis.
- The coefficient sums are rewritten: every factor of the compact operations
  is the page operation plus a polynomial factor (their difference on the same
  arguments; 1,335 and 765 factors), and the half-valued terms that depend on
  $`n_2`$ of the change of complex-fermion coordinate, of the P-move phase and
  of the polarization of the rephasing between the source completion $`y_6`$
  and the completion of the transfer construction are added as physical-face
  monomials. $`\mathcal I_5^{\gamma\psi}`$: 7,053,734 terms (was 5,684,189);
  $`\mathcal I_5^\psi`$: 3,265,871 (was 2,869,198). The self-stacking sums are their
  specializations: 3,661,063 and 824,945 terms.
- (M3E) and the zero-p+ip self-stacking page print the closed-Majorana laws of
  the thesis; the general law reduces to them as cochains. The group-inverse
  identity no longer carries an occupation bracket; its boxed result is unchanged.
- [Transfer appendix](docs/formulas/TERMINAL_TRANSFER.md#transfer-lower-data):
  the kernel (K1–K3) is written with the explicit compact lower data of the
  transfer construction ($`\mathcal O_5^{\rm tr},\mathcal E_4^{\rm tr},\mathcal O_5^{\psi,\rm tr},y_6^{\rm tr}`$).
- Code: `full4/physical.py:product48` evaluates the same values without a
  transfer at a shifted occupation (complex-fermion contributions, the
  occupation-free transfer part, and the explicit occupation, completion and
  P-move terms); `product_4_bosonic` was recompiled and
  `majorana4_product_composed` recomposed, with identical values.
- Verification ([4+1D stacking checks](docs/formulas/verification/four_dimensional/README.md)):
  on random exact towers with signed $`n_2`$ and all four background sectors, the
  printed general law equals the code on 40 of 40 states (32 with $`n_2\neq0`$),
  $`d_{s_1}\mathcal E_5=\Delta\mathcal O_6`$ holds on 40 of 40 six-simplices (32 with
  $`n_2\neq0`$), the printed self-stacking law equals the code on 40 of 40, (M3E)
  equals the code and the general Majorana contribution equals (M7) on 40 of 40
  closed states, and the zero-p+ip self-stacking law equals the code and the
  self-stacking law on 40 of 40. The factor differences were checked on four
  random states per table (23,824 factor evaluations, including open Majorana
  cochains); $`\Theta_5`$, its self specialization and $`b_4`$ were checked as exact
  polynomial identities; and the
  [4+1D verifier](docs/formulas/coefficients/verify_four_dimensional_bare_formulas.py)
  checks for arbitrary cochains that the complex-fermion contributions carry
  the complete dependence on $`n_4,n'_4`$.

## 2026-11-25: 4+1D code in the physical occupation n_4

The 4+1D programs now take the physical point-fermion occupation $`n_4`$,
with $`dn_4=\mathcal O_5`$ the complete F-move count. Every stored
classification and stacking group and every layer filtration is unchanged.

- `source_4_fermion` and `product_4_fermion` evaluate $`\mathcal O_5`$ and
  $`\mathcal E_4`$ of the formula pages (`full4/physical.py:parity,lower_product`).
- `source_4_bosonic` evaluates the displayed $`\mathcal O_6`$ in $`n_4`$
  (`full4/physical.py:source48`); it replaces the shared `high6` in 4+1D, which
  the 3+1D construction keeps.
- $`y_6`$ is the completion of the F-move parity $`\mathcal O_5^\psi`$: the
  residual (S6) uses $`\mathcal O_5^\psi`$, and two tridegrees of the numerical
  polynomial change. The pure p+ip obstruction is
  $`\tfrac12[y_6+s_1\mathcal O_5^\psi]`$ plus its fractional terms; the
  completion has 458,647 physical-face monomials. The relation to the earlier
  representative is the twisted differential of the Eilenberg–Zilber
  pullback of the change of the completion, a local five-cochain of
  $`n_2,\omega_2,s_1`$. The 3+1D auxiliary source keeps the completion of its
  auxiliary p+ip source (`y6_auxiliary`).
- `product_4_bosonic` replaces `nonbinary4`. At $`n_2=n'_2=0`$ the stacking
  correction equals the closed-Majorana law of the thesis and of
  `majorana_3_stacking_operator`; for $`n_2\neq0`$ it differs from the previous
  correction by the polarization of the source rephasing and by explicit
  P-move rephasings.
- The gauge cylinders, `majorana4_product_composed` and the GAP
  character-Majorana lift table were recompiled from these programs.
- Every compiled 4+1D program was checked against its readable source; the
  displayed $`\mathcal O_6`$, evaluated directly with the 1,897-word table and
  the new $`y_6`$, is closed on random on-shell data; the stacking correction
  satisfies $`d_{s_1}\mathcal E_5=\mathcal O_6[N]-\mathcal O_6[n]-\mathcal O_6[n']`$
  on random data with and without p+ip decoration.

## 2026-11-25: 4+1D formulas in the parity count of the F move

The 4+1D formula pages now write the complex-fermion layer with
$`dn_4=\mathcal O_5`$, where $`\mathcal O_5`$ is the complete directed
F-move count; the former four-cochain $`B_4`$ is absorbed and no longer
appears. The runtime, the compiled programs, the coefficient tables and every
stored classification and stacking result are unchanged; the code still
evaluates its own argument, and the [code notation](formulas/CODE_NOTATION.md#from-the-code-to-the-formulas)
states the map.

- $`\mathcal O_5^{\gamma\psi}=dn_3\cup_2n_3+s_1(n_3\cup_3dn_3)`$, and
  $`\mathcal O_5^\psi`$ has ten terms: intrinsic zero modes, projective zero
  modes, and their pairs. The new $`\mathcal O_5`$ equals the earlier one plus
  the earlier coboundary and matches the F-move graphs of the
  [geometric bundle](docs/formulas/verification/geometric_4d/README.md) as an
  exact polynomial identity in 75 local bits.
- Stacking: $`N_4=n_4+n'_4+\mathcal E_4`$ with
  $`\mathcal E_4^{\gamma\psi}=n_3\cup_3dn'_3+\mathcal E_3\cup_2(n_3+n'_3)+s_1[(n_3+n'_3)\cup_3\mathcal E_3]`$;
  $`\mathcal E_4^\psi`$ gains $`\mathcal E_3\cup_2\mathcal E_3`$ and an explicit
  $`\Delta[\cdots]`$ of a one-state $`s_1`$ polynomial. The three-cochain of the
  P-move count loses its term $`n_3\cup_3n'_3`$, and the closed sector has
  $`N_4=n_4+n'_4+\mathcal E_4^\gamma`$.
- Bosonic obstruction: $`\mathcal O_6^c+\mathcal O_6^{c\gamma}`$ and the three
  exchange cups of $`\mathcal O_6^{c\psi}`$ add up to
  $`\tfrac12[\omega_2n_4+n_4\cup_2n_4+dn_4\cup_3n_4+dn_4\cup_4dn_4]`$; the other
  terms of $`\mathcal O_6^{c\psi}`$ depend only on $`n_3`$, and
  $`\mathcal O_6^\psi`$ gains $`\tfrac12[\mathcal Q_{\omega_2}[x]+\mathcal O_5^\psi\cup_4dx]`$.
  Correction: the earlier $`\mathcal O_6^{c\psi}`$ used $`n_3\cup_2n_3`$ in the two
  terms that compensate the sign of the Majorana quarter bracket, where that
  sign change produces $`[\beta^-n_3]_2`$. Their difference is not closed for
  $`dn_3\neq0`$, so the earlier displayed obstruction was not closed; this is
  the 4+1D counterpart of the 3+1D correction of 2026-11-15.
- Bosonic stacking: the complex-fermion contributions are written in $`n_4`$
  and $`N_4`$ of the new law; $`\mathcal E_5^{c\gamma}`$ contains the explicit
  occupation bracket, which depends only on the lower decorations. The closed
  sector, the self-stacking pages and the group-inverse identity are their exact
  specializations.
- The [4+1D verifier](docs/formulas/coefficients/verify_four_dimensional_bare_formulas.py)
  checks the obstruction conversion and the stacking identity for arbitrary
  cochains. The term census is updated.

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
- The face formula of $`\zeta_{2,1}`$ moved from the $`\mathcal O_4^\psi`$
  display to the sentence below it, written for general arguments
  $`\zeta_{2,1}(x,y)(01234)=x(012)\,x(023)\,y(23)\,y(34)`$.

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
