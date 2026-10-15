# Exact compiled 3+1D source and stacking phase

This optional execution layer evaluates the **same current U(1)^f formulas** as
`_engine/calibrated.py`. It changes scalar evaluation, not obstruction classes,
root completion, gauge, or stacking conventions. Generated expressions contain
no superconducting kernels and require no other checkout at runtime.

The offline compiler traces the generic calibrated 3+1D source and the generic
3+1D stacking phase through the original ordered simplex cup plans. Its rational
scalar is an integer DAG numerator divided by a fixed positive denominator.
Both final phases have denominator 8 in the admitted half-integral-background
domain; this is a result of the generated expressions, not an assumed period
or a reduction of input decorations modulo 8. Negative integers and arbitrarily
large integers retain their exact values throughout evaluation.

## Dispatch and validation

The public API performs its original validation first. The worker performs its
original field decoding and `Symmetry` construction, including checking that
`delta omega` is integral, before invoking the public API. `validate=False`
continues to support partial simplices and does not assert lower-tower closure.
The accelerated domains are:

- Source: spatial dimension 3, a 5-simplex, integer sheet and charge, half-integral
  omega, and a literally nonzero sheet.
- Product phase: spatial dimension 3, a 4-simplex, integer fields for both inputs,
  half-integral omega, and at least one literally nonzero sheet.

These guards select precisely the corresponding generic branches in
`calibrated.py`. Every zero-sheet specialization stays in the reference engine,
including cases where the charge is not closed. Other simplex dimensions,
non-half-integral backgrounds, and noninteger partial fields also retain the
reference evaluation. The product's lower sheet/charge correction is unchanged.
All gauge operations and all 2+1D/4+1D operations remain in the reference engine.

The compiler permits no symbolic truth-value branch. Its cup implementation
reuses the reference geometry and omits only structurally constant zero terms;
it never assumes an unknown expression vanishes. All coefficient signs remain
runtime inputs and `s` and `rho` are independent. Scalar common-subexpression
elimination does not interchange ordered cochain factors or group arguments.

## Arithmetic and execution

For a symbolic scalar `a/d`, addition uses a common constant denominator,
multiplication multiplies denominators, `(a/d) mod m = (a mod (m*d))/d`, and
`floor((a/d)/k) = floor(a/(d*k))`. Sign powers are `(-1)^b = 1-2*(b mod 2)` for
integer `b`. These identities hold for negative inputs as well. The final DAG
returns its numerator divided by its recorded denominator.

The default `U1_DAG_MODE=auto` uses the optional native integer VM if available;
otherwise it executes the same DAG with Python integers. Native addition and
multiplication check signed 64-bit overflow. Overflow, or an input outside the
64-bit range, restarts the whole DAG with unbounded Python integers. Exact
integer division rejects a nonzero remainder; it is never rounded. The native
VM has no floating-point operations.

- `U1_DAG_MODE=python`: use Python integer DAGs without loading the native VM.
- `U1_DAG_MODE=reference`: use the original cochain evaluator for every operation.
- `U1_DAG_LIBRARY=/absolute/path/library.so`: select the native library; otherwise
  the path is `insulator/_compiled/u1_dag_vm.so` in this checkout.

A missing native library is harmless. Compiler source and binary hashes belong
in the run's provenance. The generated DAGs also record their five source-file
hashes; a mismatch disables acceleration and retains the reference evaluator.
No value or background is cached in a program: each call supplies all fields.

Build the optional native VM explicitly, without changing formula data:

```sh
python scripts/build_formula_vm.py --metadata /tmp/u1_vm_build.json
```

Regenerate the reviewable JSON expressions from this checkout:

```sh
python -m insulator._compiled.compiler source --out insulator/_compiled/source3.json
python -m insulator._compiled.compiler product --out insulator/_compiled/product3.json
```

Compilation temporarily installs symbolic cup evaluation and is intended as an
offline command, not as a concurrent operation inside a running worker. Runtime
loading does not compile or alter the reference cochain engine.

## Provenance and checks

The generic integer builder/VM architecture comes from the separate
`FSPT_AHSS` main commit `0864495`, especially `fspt/formulas_pip_compile.py` and
`fspt/full_formula/native.cpp`. Only generic exact arithmetic infrastructure was
adapted. Every generated expression comes from the insulator engine adopted
from the consolidated v0.7 archive recorded in `AGENTS.md`.

`tests/test_compiled_source3.py` regenerates both DAGs and compares native,
Python-DAG, and reference results on independent signed backgrounds, negative
values, completed lower towers, huge integers, intermediate overflow, arbitrary
rational backgrounds, invalid requests, missing native libraries, and repeated
calls with different contexts. The full SG14 audit additionally compares every
captured response and the complete native classification record; its evidence
is archived separately from this implementation.
