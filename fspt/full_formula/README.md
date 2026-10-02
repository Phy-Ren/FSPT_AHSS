# Exact complete-formula evaluator

The runtime implements the full matched obstruction and stacking laws in spatial
dimensions 3 and 4. Read [the formula guide](../../formulas/README.md) for fields,
coordinates, every operation's readable definition, the scalar instruction
format, and the separately calibrated lower-dimensional endpoints.

No external source package is imported by the runtime. All required DAGs are in
`fspt/data/full_formula/`. The readable compiler input is included in
`formulas/publication_source/`; the [reproduction guide](../../PUBLIC_RELEASE.md)
contains build and verification commands.

The optional native evaluator uses exact signed integers with checked overflow
and an arbitrary-precision Python fallback. Required nonintegral divisions fail
explicitly. Specialization kernels compose the same complete expressions and do
not discard physical source or stacking terms.
