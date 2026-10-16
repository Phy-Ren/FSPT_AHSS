# Independent review of the final 3D campaign

Reviewed `results/three_dimensional_20261013`: 64 distinct completed cases,
32 of each physical spin, no failures. Fresh comparisons reproduce every saved
comparison exactly. Source and calculation inputs remain separate.

One meaningful sector comparison per case gives **51 matches and 13
mismatches**. The 22 proper-rotation cases give 20 matches and 2 mismatches.
The 42 improper cases give 31 matches and 11 mismatches against the reference's
quotient by its explicitly named neutral E8 root. Their additional 42 full-group
`scope_mismatch` records are not calculation failures. Spinless totals are
26 matches / 6 mismatches; spin-half totals are 25 / 7.

| Case | Physical spin | Computed CI/charge/phase group | Reference for matching sector |
| --- | --- | --- | --- |
| D2 | Spin-half | Z2^2 | Z2^3 |
| S4 | Spinless | Z2 x Z4 | Z2^3 |
| S4 | Spin-half | Z2 x Z4 | Z2^3 |
| D2d | Spinless | Z2^3 | Z2^2 x Z4 |
| D2d | Spin-half | Z2^2 x Z8 | Z2^4 x Z8 |
| C3i = S6 | Spinless | Z8 | Z2 x Z4 |
| C3i = S6 | Spin-half | Z8 | Z2 x Z4 |
| D3d | Spinless | Z4 x Z8 | Z2 x Z4 |
| D3d | Spin-half | Z4 x Z8 | Z2^2 x Z8 |
| D6 | Spin-half | Z2^2 | Z2^3 |
| D3h | Spinless | Z2^3 | Z2^4 |
| D3h | Spin-half | Z4 x Z8 | Z2^2 x Z4 x Z8 |
| Oh | Spinless | Z2^4 x Z4 | Z2^3 x Z4 |

For D2 and D6 the reference column is the full published group; for the other
rows it is the named-E8 quotient. This is an abstract group comparison. The
implementation does not provide a full neutral-E8 cochain map or a physical
identification of every computed generator with a real-space root.

Interpretation limits:

- D2 spin-half has a source-named odd-charge center root incompatible with
  the source's SU(2) double-group convention; the independent obstruction
  calculation supports the computed result.
- S4 and C3i/S6 have independently certified nontrivial root extensions.
  Equal orders or equal graded factors do not establish group equality.
- Exact normal-C3 controls relate the supplied-sector D3d, D6 and D3h problems
  to C2h, D2 and C2v, respectively. They are independent consistency checks
  on the computed sector, not assumptions that all possible physical sectors
  were implemented.
- D2d has independent charge-obstruction and root-square checks. Its separate
  atomic-orbit induction quotient remains conditional until an explicit
  allowed inverse-paired bubble/adjoining path realizes the proposed rows.
- The independent full spinless Oh bordism calculation gives
  `ku4(X)=Z4 x Z2^4` and `ku0(X)=Z2` for `X=(BOh)^(3-V)`.
  Their Spin-c sum is the full E8-inclusive group `Z4 x Z2^5`, with the
  relevant differentials and extensions resolved. See the
  [bordism derivation](point3_mismatch_audit_20261016/oh_audit.md).
- None of the 13 discrepancies has been converted into a match by editing
  the primary table or fitting the backend. Numerical agreement elsewhere
  establishes the stated sector comparison, not completeness of every
  interacting insulator sector.

See [the source discrepancy audit](point3_discrepancies.md) and
[the direct cyclic-root certificate](../docs/cyclic_root_audits.md).

Reviewed file SHA-256 values:

```
results.json     31c7739b39e9634e46a76ddca97f55741bff6990aa2780b36d90eea319e4622a
comparisons.json d5499bfc165e6cdcf04d8787d7406aa775dd826c25e6a1c78d3288b6ac4d235b
```
