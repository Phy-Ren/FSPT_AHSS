# Validation of the independent formulas and marked stacking calculation

This record describes checks completed on 26--27 September 2026. It
separates identities verified in this project from certificates supplied with
the mathematical inputs. No comparison with the collaborator's space-group
answer tables is included here. The recorded cluster runs and their log
hashes are in [validation_runs.json](validation_runs.json).

The calculation concerns three spatial dimensions, the complete infinite
affine space group, `omega2=0`, and the determinant orientation character
`s1`. The state has degrees `(n1,B2,C3,nu4)`. The integer layer has signed
coefficients, binary layers have F2 coefficients, and phases lie in
`R/Z_s`. Integer carries and signed cup products are exact. The closed
Majorana sector uses the manuscript CA coordinate. The integer-sector
terminal phase uses the root normalized p+ip manuscript, with the coordinate
comparisons below. Higher spatial dimensions are outside this calculation.

The current formula convention is `normalized-pip-aw-edge-transport-v2`.
[AW_TRANSPORT_CORRECTION.md](AW_TRANSPORT_CORRECTION.md) records the corrected
per-edge transport, the original failing fixtures, exact coordinate changes,
and direct unchanged-oracle regressions. Earlier affine phase witnesses in
this historical log used the preceding coordinate unless explicitly marked
as rerun. Closed-Majorana and even-integer results are unaffected pointwise.

## Formula and language checks

| Check | Completed evidence | Reproduction |
|---|---|---|
| Closed-Majorana source, O4/O5 and U3/U4 | Exact local lower-tower closure/product identities and comparison to the supplied analytic evaluator; incoming Majorana and CF gauge phases retained | `tests/test_formulas.py` |
| Python/GAP expression agreement | 26 exact fixtures, including generic graph and straight-line evaluation | `tests/test_formulas.g`, `tests/formula_cases.g`; cluster task `20260926T222652-formulas-fast-70871c9d` |
| Complete integer-layer O5 | 84 legal towers agree with the unchanged supplied public API, including negative integers, two retained regressions and magnitudes up to `2^45`; another 64 legal sign towers are checked independently | `tests/test_formulas_pip.py`, `tests/generate_pip_general_cases.py`, `tests/test_aw_transport_correction.py` |
| Real affine-group lower primitives | 48 actual bar-cochain tuples across SG 29, 41, 45, 110, 120 and 219 agree with the supplied parity evaluator; their Majorana equation is checked on all lower faces | `tests/test_pip_spacegroup_samples.g` and `.py`; `runs/pip_samples_sg*.json` |
| Secondary additivity probe | One nontrivial doubling test in SG35 passed. SG47 had empty relevant kernel, so this run is **not** evidence for distinct-pair additivity | `tests/test_formulas_secondary.g`; task `20260926T221214-secondary-additivity-ec7ccc6b` |

The corrected general O5 runtime is a 7,239-instruction compilation of the supplied
complete analytic specification, including its fixed Y5 coefficients. It
imports neither SptSet nor collaborator Python modules at runtime. The
compiled expression retains the open Bockstein, integer carries, mixed
terms and the full sixteenth-valued pure phase.

For `n1=s1`, the exact restriction is

```
O5(s1,B,C) = S^2(C)/2 + gamma_open(B) + 9 s1^5/16.
```

Here the pure parity vanishes on all 16 local sign four-simplices, and the
complete pure phase equals `9 s1^5/16` on all 32 sign five-simplices, checked
directly against the unchanged supplied evaluator. The corrected
935-instruction straight-line evaluator agrees with the general expression
on 512 cases: 256 legal towers and 256 unrestricted binary B/C inputs.
Another 32 exact Python/GAP/generic fixtures are regenerated for the corrected
coordinate. The earlier task `20260926T225946-pip-sign-fast-de0ea843` used the
superseded AW coordinate. These are arithmetic instruction
counts, not a claim of a particular end-to-end speedup. Reproduction:
`tests/test_pip_sign.py` and `.g`; generated code `gap/pip_o5_sign.g`.
The generic evaluator remains available and the specialization is selected
only for the actual canonical sign callback.

## Complete coordinate dictionaries

At zero integer input, the open-Majorana continuation and the CA phase are
not pointwise identical. On `dB=0`, `dC=Sq^2 B+s1 Sq^1 B`, we independently
constructed the exact dictionary

```
O_pip(0,B,C)-O_CA(B,C)
    = d_s[D0(s1,B) + lift(Sq^2 B)/4 + s1 cup C/2].
```

The quarter-valued D0 solves all 32,768 local closed-B equations; 128 further
complete legal towers verify the identity. Its coefficients are recorded in
`fspt/data/pip_zero_mc_coordinate.json`, and
`tests/derive_pip_zero_mc_coordinate.py` reproduces the solve and checks.
This certifies equality of the secondary cohomology classes used by the
two layers, without identifying their raw phase callbacks.

For the torsion family `n1=s1`, the reference CF coordinate is `C+Lambda1`,
where

```
Lambda1(0123) = B013 + B012 B013 + B012 B023 + B013 B023.
T1 = D1(s1,B) + s1^4/4 + [C cup_2 Lambda1 + Lambda1 cup_3 Q_native]/2.
O_reference(s1,B,C+Lambda1)-O_native(s1,B,C) = d_s T1.
```

The CF dictionary was checked exhaustively for the four integer multiples
`k*s1`, `k=0,1,2,3`, on 1,024 local states each
(`tests/derive_pip_coordinate.py`). The stored D1 is the historical base
table in `fspt/data/pip_upper_coordinate.json`. The complete corrected
dictionary `D1+s1^4/4` passes all 32,768 legal local lower-face equations.
Use `tests/derive_pip_upper_coordinate.py --verify-current`; its reference input
is the mathematical source checkout pinned at
`c2961a2d6ee9465a7b634a31b6c095e607972966`.

For the doubled output, **restricted to `n1=2s1,B=0`**,

```
Lambda2=s1^3,
T2(C)=-3 s1^4/16 + C cup_2 s1^3/2.
```

The two upper dictionaries pass 64 additional complete-tower comparisons
to the unchanged scalar reference phase evaluator. Their GAP callbacks and
the integer gauge below pass 96 exact cross-language fixtures
(`tests/test_pip_coordinates.py` and `.g`). The earlier task
`20260926T224052-pip-coordinates-fixed-deeabfff` used the superseded coordinate;
the Python fixtures have now been regenerated and passed. No unrestricted closed-B
claim is made for the displayed T2 formula.

## Integer gauge and calibrated torsion product

The integer gauge is derived directly from the normalized O5. On the
cylinder, with height zero-cochain `t` and bottom prism contraction `K`, set

```
n_I=2s1+d_s t,   B_I=s1 cup t cup dt,
C_I=pull(C)+K Q_native(n_I,B_I).
```

The endpoints are `(2s1,0,C)` and `(0,0,C+s1^3)`. The O5 prism integral is
an explicit local phase `g4`; its transport identity is

```
d_s g4 = O5(0,0,C+s1^3)-O5(2s1,0,C).
```

All 32,768 legal local five-simplex states verify this identity, together
with the cylinder's lower equations. `g4=13s1^4/16+P(s1,C)/2`, with the
complete polynomial P in `fspt/pip_coordinates.py`. Reproduction:
`tests/derive_pip_integer_gauge.py`.

The additional reference diagonal product is evaluated from its calibrated
mathematical construction, including the fixed closed terms. All 16,384
legal local four-simplex inputs were evaluated and compiled to a universal
cochain (also represented by 579 multilinear terms modulo 16). The exact
CF identity `beta_reference=S^1(B)+s1 B+s1^3` passes 1,024 checks. Artifacts:
`runs/formula_audit/pip_diagonal.json`, `gap/pip_diagonal_data.g`;
reproduction: `tests/derive_pip_diagonal.py` and
`tests/assemble_pip_diagonal.py`. These are local cochain coefficients,
not space-group classifications or an enumeration of physical phases.

Writing `K=S^1(B)+s1 B`, the native lower-sector square is

```
CF_square=K+s1^3,
nu_square=2nu+2T1+Gamma_reference-T2(K)+g4(K).
```

The full lower reduction then removes incoming CF classes with their
actual Majorana boundary phases and product cross terms. It does not drop
`s1^3` while forgetting its phase. The complete composed square and this
incoming-gauge phase passed 256 independent random legal five-simplex
closure tests; the diagonal is normalized on all 471 degenerate local
legal towers. Reproduction: `tests/test_pip_stacking_review.py`.

## Actual affine-group marked relations

The full audit checks every lift equation and relation gauge on the bar
simplices supporting the native comparison maps. The backend's explicit
chain homotopy is what corrects native primitives to actual bar primitives;
projection to a cohomology coordinate alone is not treated as a primitive.
The following historical completed runs used the earlier AW coordinate
and enabled
`AFS_STACK_AUDIT=true`:

| Space group | Computed abstract stacking group | Boson/CF coordinates of the chosen torsion generator's square |
|---|---|---|
| 7 | `Z + (Z2)^5` | `[0]` |
| 29 | `(Z2)^5` | `[0]` |
| 41 | `(Z2)^3 + Z4` | `[0,0]` |

Their task IDs are recorded in `validation_runs.json`; all three logs end
with `PASS_MARKED_PIP_REVIEW`. These are independently calculated outcomes,
not comparisons to external answers. The zero square coordinates are
measured results. The flat-lift code can use all Majorana-secondary and CF
incoming images, re-evaluating its nonlinear source after lower changes;
it does not infer that the initial AHSS defining tower is already flat.
These three particular runs needed no nonzero indeterminacy adjustment.
Their saved phase witnesses are old-coordinate evidence. Corrected-source
affine runs replace them for current-coordinate witness claims; the
explicit AW rephasing establishes equivalence of the torsion relation classes.

A further acceleration constructs a full universal C4 tower and pulls it
back only after proving an actual homomorphism from the affine group to
C4 lifting its orientation. Its finite checks include 256 CF equations,
4,096 top-closure equations and 1,024 phase-primitive equations, with
normalized and degenerate tuples included. See
`tests/derive_c4_pip_lift.py`, `runs/formula_audit/c4_pip_lift.json`,
`runs/formula_audit/c4_pip_phase.json`, and `gap/pip_c4_data.g`.
This constructs a flat affine-group representative; the classification
still uses the complete infinite affine group. The degree-one native
character proof and code were independently reviewed.
Flatness alone does not establish that replacing an upper lift preserves
its square modulo twice the lower group. A separate same-object,
same-marked-basis check, `tests/test_pip_lift_choice.g` with `AFS_TEST_SG=112`,
passed in task `20260926T231318-pip-lift-choice-sg112-c89d690b`.
The C4 and generic lifts have exactly the same measured lower square
coordinates `[0,1,0,0,0,1,0,1,1,0]`. The lower group in this case has exponent
two, so equality is required even if the lifts differ by a lower phase.
This verifies the actual relation and its nonzero bosonic carry in a common
basis. An earlier comparison between different runtime versions showed
different named coordinates because the backend had changed its Smith
basis; those separate coordinates were not a valid lift-choice test.
The C4 homomorphism and complete pulled-back tower also pass all comparison
support checks in SG7 (`20260926T231035-pip-c4-hom-flat-36422028`).

An independent non-C4 check in SG41 changes a genuine surviving CF defining
choice in the upper tower, then solves its full O5 primitive again. Both
lift equations are checked on the comparison support. With the same
classification object and marked lower basis, the original square has
coordinates `[0,0]`, while the changed lift has `[1,0]`. Their nonzero
difference lies in twice the lower group, with exact lattice witness
`[-1,-1,0,0,1,1,0,0]` against the matrix formed by the lower relations
followed by `2I`. This is the required invariance modulo `2H`; literal
coordinate equality would be incorrect for this example. Task
`20260926T233044-pip-cf-lift-choice-sg41-f55f1aff` used the immutable v04
source and passed in 256 seconds. Reproduction:
`tests/test_pip_cf_lift_choice.g` with `AFS_TEST_SG=41`.

The native pure-CF shortcut was compared to literal full bar-cochain
stacking using one classification object in each of SG11, SG15 and SG87.
The entire marked relation matrices agree, not only their Smith invariants.
The resulting lower groups are `Z2+Z4`, `(Z2)^2+Z4`, and
`(Z2)^3+Z4+Z8`, respectively; the last example checks a bosonic Z4 subgroup
and a nontrivial carry producing Z8. In SG11 both chosen CF generators
double to the same bosonic generator. Separate SG11 support checks verify
the exact same-lift doubling identity and reconstruction of an actual flat
bar lift from the native primitive. Their completed logs and hashes are
also recorded in `validation_runs.json`.

The exact CF lift includes a separate operation-comparison correction; it
does not assume equality of the native and transferred bar obstruction
vectors. With `C` closed and `nu0` the bar image of the native phase seed,
`AFSReconstructNativeCFLift` forms
`rho=[2(O_bar(0,C)-d_s nu0)] mod2`, solves `dh=rho` over F2, and returns
`nu=nu0+h/2`. The code checks half-integrality and exact solvability. Thus
`d_s nu=O_bar(0,C)` and `2nu=2nu0` modulo one; the correction is required for
the defining equation even though it cancels in the doubling relation.

The implementation preserves exact zero callbacks and cancels identical
F2 summands. Its identity and pure-bosonic product simplifications pass
comparisons to the unchanged CA polynomial. The pure-CF product uses the
literal restriction `[c cup_2 c' + dc cup_3 c']/2`; retaining the second
term makes the restriction valid even for nonclosed inputs. Comparisons on
SG11 include arbitrary native C cochains as well as flat lifts, and the
full SG1 Majorana/CF audit passes after these simplifications.

## Corrected-convention affine controls

The following controls all use the immutable corrected source
`da5c49414d02076cb1f261b5008abd491f7c1bcfa0f43c2416082df8b4e802a1`,
with `normalized-pip-aw-edge-transport-v2`. Full task IDs, log hashes,
source IDs and artifacts are in
[validation_runs/corrected_pip_transport.json](validation_runs/corrected_pip_transport.json).

| Control | Completed result | Elapsed seconds |
|---|---|---:|
| SG7 generic torsion plus primitive signed free lift | All comparison-support equations pass; free basis `[1]`; 48 additional compiled/interpreted full free-tower values agree | 59.22 |
| SG81 complete marked relation | All support and unchanged CA-product checks pass; `Z + Z2^2 + Z4 + Z8^3` | 95.98 |
| SG82 complete marked relation | All support and unchanged CA-product checks pass; `Z + Z2^2 + Z4 + Z8^2` | 199.50 |
| Finite C4 and affine retractions | Full corrected tower and stacking pass; `2P=C` gives `Z4`; both SG81/82 retractions remain exact | 22.08 |

The corrected universal C4 phase is the preserved previous primitive minus
`s^4/4`. It passes all 256 CF equations, 4,096 top-closure equations and
1,024 phase-primitive equations. Every one of the 1,024 O5 tuples also agrees
directly with the unchanged supplied scalar evaluator, including degenerate
inputs. These are corrected-coordinate checks, not reuse of the historical
phase certificates. The runtime primitive and its source hashes are retained
with `runs/formula_audit/corrected_transport/c4_pip_lift.json`.

An optional optimization for a **closed** pure-CF input follows
from the literal identity `O5(0,C,0,s)=[C cup1 C+C cup2 dC]/2`. For `dC=0`
it requires only the three products in `C cup1 C`. The independent test
`tests/test_closed_cf_phase.py` exhausts 1,024 closed local C cochains and
all 32 sign simplices, and includes a nonclosed negative-domain fixture.
This does not authorize applying the shortcut to the nonclosed CF primitive
inside a Majorana lift. It is separate from the frozen corrected campaign.

The lazy cup-one evaluator and exact half-valued transfer also pass a
complete same-basis marked-lift comparison on SG87. For each of two CF
generators, the native phase seed, full obstruction comparison support, and
all 2,690 phase comparison-support values agree with the general solver.
Task `20260927T011014-closed-cf-half-marked-sg87-458d9ae3` completed in
209.975 seconds with mod-two classification contractions enabled; evidence
is in `docs/validation_runs/closed_cf_half_phase.json`. The test runs both
paths sequentially in one context, so its timings are not an independent
production benchmark. A separate SG228 control compares all 231 entries of
the native obstruction vector exactly; its evidence, together with the
half-phase transfer and primitive controls, is in
`docs/validation_runs/cf_backend_optimizations.json`.

An earlier SG228 complete marked-lift comparison timed out after 1,800
seconds and remains inconclusive; it is not counted as a passing check.
The accepted v09 configuration enables the closed-CF branch
(`closed_cf_obstruction=true`) and retains the integral bar comparison map
(`binary_bar_mod2=false`). The separate native mod-two contraction remains
enabled (`native_mod2_contraction=true`). The earlier v08 candidate enabled
both the mod-two bar map and closed-CF branch; it is not the accepted archive.
The frozen accepted configuration is in `results/space_groups/source/`. See
`docs/CLOSED_CF_OPTIMIZATION.md` for the exact domain and preserved
comparison-homotopy correction.

## Scope of the conclusions

The checks above establish the implemented cochain identities, coordinate
changes and marked torsion square reductions. The reference product's
calibrated closed terms remain mathematical input. These calculations are
not a new proof of all of its associativity, commutativity or higher
coherence identities. The supplied normalized manuscript's physical
uniqueness statement has its stated relative and finite-group hypotheses;
local arithmetic tests do not enlarge those hypotheses.

The initial v04 files handle free p+ip factors at the abstract group level.
The separate `gap/pip_free.g` adapter now constructs explicit primitive free
lattice bases and full flat generators. It proves universal survival of
twice a signed integer character by an actual infinite-dihedral tower,
tests the complete joint free/torsion parity quotient, checks that the
projected survivors form their full F2 span, and retains directly solved
RREF rows plus doubled nonpivot vectors. Every chosen generator is exported
with its integer H1 coordinates, torsion shift, native defining tower and
phase primitive. This does not change the finite joint presentation.

The accepted v09 archive, `results/space_groups/`, contains all 230 complete
classification and stacking results, with source ID
`9c16c0714da16a1ed5dc23b7830701afc01e6d7a37ee6d243f536ee4dc9ecd96`
and convention `normalized-pip-aw-edge-transport-v2` throughout. Every one
of its 44 groups with nonzero free p+ip rank has
`pip.free_lattice.fullFreePhaseWitness=true`, with the actual primitive
basis and full generator towers exported. The lattice indices are one for
29 groups, two for 14 groups, and eight for SG2. All 32 surviving torsion
p+ip cases have `stacking.fullUpperPhaseWitness=true`. SG219 has invariants
`[2,2,4]` and the actual marked relation `2P=C1`.

Strict archive checks verify the complete stored witnesses, exact Smith
identities and reported invariant factors, source hashes and formula
convention. The complete mathematical fields agree literally with the
same-source v07 baseline of 229 original results plus its SG219 retry;
that assembled baseline is not a single-campaign performance record.
Constructing and exporting these witnesses is distinct from the separate
comparison-support audits: no full-support audit of all 230 groups is
claimed. The accepted archive retains the actual frozen source, campaign,
task and extension evidence, and strict performance report in
`results/space_groups/archive.json` and `performance.json`.

Completed full-generator checks give the following surviving lattices in
the respective native free H1 bases: SG1 has `I3` (index1), SG2 has `2I3`
(index8), SG6 has `[2]` (index2), and SG7 has `[1]` (index1). For every
chosen generator these tests verify the integer cocycle, both lower
equations and the full phase equation on all comparison-support faces,
and confirm that the original classification torsion tower is unchanged.
The universal infinite-dihedral construction also passes independent bar
tests with negative translations and degenerate tuples. Scripts are
`tests/test_free_pip_lattice.g`, `tests/test_dihedral_pip_lift.g`, and
`tests/test_dihedral_pip_extra.g`; exact logs and hashes are recorded.

Only result files containing `pip.free_lattice.fullFreePhaseWitness=true`
claim these actual primitive free generators. The replay interface labels
older files `abstract-free-splitting` and supplemented files
`explicit-primitive-free-lifts`. A free quotient splits after choosing its
actual lifts because `Ext^1_Z(Z^r,H)=0`; this algebraic splitting does not
justify replacing a required doubled generator by an unsolved primitive
integer character.

External answer comparisons are documented separately in
[PROJECT_REPORT_ZH.md](PROJECT_REPORT_ZH.md) and
[COMPARISON_WEICHENG.md](COMPARISON_WEICHENG.md). They do not replace the
cochain and saved-certificate checks described here.

## Exact native contraction and performance checks

The production driver selects a native contraction evaluated modulo two
after each linear stage of the extension perturbation. Reduction commutes
with the finite-factor and lattice contractions, horizontal boundary,
group-ring translates and sums. Induction on decreasing point-group degree
therefore identifies this map with the reduction of the original integral
contraction. Induction in the higher-diagonal recurrence gives equality of
the complete native diagonal modulo two. This is stronger than agreement
of the induced cohomology operation: the CF-only stacking calculation also
receives the same native phase seed. Integer comparison maps, bar homotopy
corrections and phase primitives retain their integral implementation.

Independent frozen runs compare every entry of the native square of every
H3 generator. They agree for SG47 (38 vectors), SG219 (4 vectors of length
102) and SG226 (9 vectors of length 231). Complete vectors, raw logs and
their hashes, loaded source-file hashes, task commands, machine identities
and timings are retained in
[backend_mod2.json](validation_runs/backend_mod2.json).

| Space group | Integral native operation, CPU seconds | Modular native operation, CPU seconds |
|---|---:|---:|
| 219 | 1009.767 | 462.456 |
| 226 | 912.855 | 411.270 |

These timings exclude resolution construction and concern these frozen
probes, not a full classification/stacking campaign. The integral reference
uses exact-key hash tables for tensor cancellation; that separate experiment
did not improve performance and is absent from production. The complete
output equality is unaffected by the dictionary representation.

Additional controls compare signed/inverse translated-cell contractions
through degree four in SG104, SG219 and SG226. A separate projected-cycle
calculation using the original integral contraction agrees with all modular
H5 coordinates in both cubic groups, including the order-six target factor
of SG219. The native/bar square and Majorana Bockstein cohomology-coordinate
checks also pass in SG2, SG7, SG29 and SG47; they do not assert equality of
the raw native and transferred bar cochains. The evidence file records only completed checks with
explicit success markers.

The driver prints the actual contraction mode at startup and exports
`native_mod2_contraction` and `native_mod2_cache_degrees`. Resolutions without
extension factors use the original contraction reduced modulo two. Known
zero callbacks and zero native representatives return the exact canonical
zero without constructing comparison maps; the arbitrary-bar-primitive
regression on SG1, SG2 and SG7 passes after this change.
