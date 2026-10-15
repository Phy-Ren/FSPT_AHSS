# Read-only review of the new local E8 interface

Reviewed 2026-10-15. Files read:

- `insulator/e8.py`
- `insulator/_engine/e8_4p1.py`
- `insulator/e8_h1.py`
- `tests/test_e8.py`
- `docs/e8/notation.md`, `2p1.md`, `3p1.md`, and `4p1.md`

**No substantive valid-input defect was found.** The review did not modify
production files or repeat the full test suite.

The state and operation order is consistently
`(e_p,n_p,n_{p+2},nu_{p+3})`. The common source adds the neutral cubic only
in 4+1D. Stack and gauge add the corresponding neutral phase correction to
the inherited CI correction, with one shared phase. Both input and output
states are validated. The inverse subtracts the complete twister; the
neutral coordinate is negated while the CI integer-product correction is
retained. Background transport changes only the CI background and retains
the neutral coordinate, which is correct because that transport preserves
the chirality character. No group multiplication table, finite-group
averaging, or global sheet primitive is assumed by these local routines.

The neutral engine is the reviewed v0.9 engine with local package imports,
stricter cochain validation, and the additional gauge-composition primitive.
The latter has the correct sign: writing `b=e+dv`, `c=b+dw`, Leibniz's
rule gives

`d(v w c + v b w + e v w)/3 = G(e;v)+G(b;w)-G(e;v+w)`.

The signed H1 implementation retains a saturated integer kernel and
quotients by the one principal-coboundary column. It does not silently
replace translations by finite cyclic groups. Its restriction to a
nonempty generator list is an explicit input contract; a presentation of
the trivial group can use one generator and its killing relator.

The dimensional documentation keeps the necessary scope distinctions:
uniform neutral tensor layers in 2+1D; a selected physical neutral section
in 3+1D; and the completed, shared-phase closed-sheet extension in 4+1D.
It does not claim the current global classifier includes E8 or the
intrinsic row. The space-group real-cohomology statement is correct and
can be strengthened by the constructive rational-resolution proof in
[general_groups.md](general_groups.md).

The targeted additional check addresses a gap not filled by merely
completing arbitrary local simplex cocycles: it starts with a **global
free** E8 two-cocycle on `Z^4` and its explicit global bar-cochain phase,
then restricts them to translated simplices. It tests the production API
on that data, including negative coordinates and nonzero integer gauges.

```sh
PYTHONDONTWRITEBYTECODE=1 python check_runtime_free_sheet.py
```

All six source validations, six integer gauges, six exact inverse-state
checks, and six self-stacks passed. The script and output are
[check_runtime_free_sheet.py](check_runtime_free_sheet.py) and
[check_runtime_free_sheet.json](check_runtime_free_sheet.json). This is a
local interface check, not a new global classification or a physical
identification of the retained CI kernel.
