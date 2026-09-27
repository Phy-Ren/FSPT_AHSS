# Generic p+ip O5 execution

`scripts/compile_pip_o5_straight.py` translates the existing scalar-operation
graph into `gap/pip_o5_general.g`. It performs no symbolic simplification or
change of formulas. The corrected graph has 7,239 nodes and SHA-256
`10e607ca43e32f0d343bb54e83dab248b1c4ea379a68f3cce2c479b5f6e7dd2f`.

The generated program retains normalization of every field call, exact
division with divisibility checks, floor division and bit extraction for
negative integers, and final reduction modulo 16. The specialized `n=s`
program has dispatch priority. Set `AFSUseGeneralPipO5 := false` to run the
original scalar interpreter for the general branch. The program exports its
source hash, operation count and call counter.

The independent fixture generator checks the graph directly against the
unchanged supplied `evaluate_simplex` oracle. Its 84 cases comprise the
original 12 tests, 64 signed integer-potential tests with negative edges,
and eight tests with integer potentials as large as ±2^45. All are legal
lower towers. The GAP regression compares every compiled result against
the interpreter and the oracle-derived fixtures, and also tests normalized
internal faces and specialized dispatch priority.

In the completed frozen worker test, 420 uncached evaluations took 2.074
CPU seconds compiled and 9.406 seconds interpreted, with exactly equal
results. This 4.53-fold speedup concerns scalar formula execution, not the
entire space-group pipeline. The task, source hashes, full output and timing
are preserved in [pip_o5_straight.json](validation_runs/pip_o5_straight.json).

Two additional signed fixtures exposed a transport error in the earlier
graph. They remain in `tests/pip_general_oracle_discrepancies.json` as
historical counterexamples. The correction and required phase-coordinate
changes are documented separately in
[AW_TRANSPORT_CORRECTION.md](AW_TRANSPORT_CORRECTION.md). Execution equivalence
does not replace those mathematical checks.
