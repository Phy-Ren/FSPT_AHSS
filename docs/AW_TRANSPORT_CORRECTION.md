# Corrected per-edge AW transport

The runtime convention is `normalized-pip-aw-edge-transport-v2`. This corrects
our transcription of the supplied formula; no supplied source or classification
answer was changed. The full expression has 7,239 operations and its `n=s`
specialization has 935. The corrected JSON SHA256 is
`10e607ca43e32f0d343bb54e83dab248b1c4ea379a68f3cce2c479b5f6e7dd2f`.

The unchanged `polynomial_tables.py:28` defines each transported integer
edge as `M(ij)=(-1)^s(0i) n(ij)`. Our initial compiler transported every
middle-block edge from the first vertex of that block. Expanding regression
tests found two legal signed-integer towers on which its result differed from
the supplied scalar evaluator by `1/2`. The exact original fixtures remain in
`tests/pip_general_oracle_discrepancies.json`.

For effective `omega=0`, let `bit1(x)=(x>>1)&1`, using mathematical floor for
negative integers. The corrected minus previous O5 is exactly

```text
Delta O5(012345) = (1/2) s01 s12 s23 s34
                  bit1((-1)^s03 n34) (n45 mod2)  mod1.
```

Only the `(i,j,k)=(3,2,0)` AW monomial with integer word `0x22` changes.
The elementary identity `bit1(-x)+bit1(x)=x mod2` proves the displayed
difference. It vanishes pointwise for **every even integer cochain n** and
for `s=0`. Consequently the zero-integer CA dictionary, the universal doubled
dihedral tower, the unitary free towers, and the `n=2s,B=0` dictionary T2 are
unchanged. General signed odd free towers must use the corrected evaluator.

For the canonical torsion input `n=s`, the difference is `s^5/2`. Thus

```text
O5(s,B,C) = Sq_cochain^2(C)/2 + gamma_open(B) + 9 s^5/16.
nu_new = nu_previous - s^4/4,
T1_new = T1_previous + s^4/4.
```

Indeed `d_s(s^4/4)=-s^5/2`. The stored local D1 table is retained as a base;
the runtime adds the explicit `s^4/4`. The reference CF dictionary and its
calibrated diagonal Gamma remain unchanged. Re-evaluating the canonical
integer cylinder gives `g_new=g_previous+s^4/2`, or
`g_new=13s^4/16+P(s,C)/2` with the same binary polynomial P. This change occurs
inside the cylinder, whose integer cochain has odd vertical edges, despite
its two even endpoints.

In the complete square `2nu+2T1+Gamma-T2+g`, the first two rephasings cancel.
The remaining change is the explicit lower phase gauge

```text
square_new - square_previous = s^4/2 = d_s(s cup B /2),  dB=s^3.
```

This proves equality of the marked torsion relation classes after matching
the input lifts. It does not say that saved old phase cochains already satisfy
the corrected lift equations. The universal C4 primitive must be rephased by
`-s^4/4`, and current result witnesses must be regenerated. Frozen earlier
snapshots remain historical evidence.

Completed checks include:

- 84 fully legal towers against the unchanged supplied scalar oracle,
  including the two original failures, negative edges and integers up to `2^45`;
  independent GAP interpreter and straight-line evaluations agree on all 84.
- Every one of the 32 sign simplices against that scalar oracle, plus 64 legal
  sign towers and 512 generic/specialized comparisons.
- 256 old/new exact-difference checks, including 128 arbitrary even-character
  towers; 384 direct checks of the square's exact phase gauge.
- All 32,768 corrected unary dictionary equations, all 256 canonical cylinder
  states, and all 32,768 resulting cylinder transport equations.
- 256 full square closure tests and normalization on 471 degenerate legal
  towers; 96 regenerated unary Python/GAP fixtures.

Reproduction: `tests/test_aw_transport_correction.py`,
`tests/generate_pip_general_cases.py`, `tests/test_pip_sign.py`,
`tests/derive_pip_upper_coordinate.py --verify-current`,
`tests/derive_pip_integer_gauge.py`, and `tests/test_pip_stacking_review.py`.
The historical graph is an optional audit-only input to the first script;
it is never imported by production. Machine-readable evidence is in
`docs/validation_runs/aw_transport_correction.json` and the corresponding
compiler/C4 records. [COMPILED_PIP_O5.md](COMPILED_PIP_O5.md) and
`docs/validation_runs/pip_o5_straight.json` record the separate straight-line
compiler tests and source/log hashes. Fresh affine support checks and the uniform rerun use
this named convention.
