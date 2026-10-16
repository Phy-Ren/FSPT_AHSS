# Complete 3+1D space-group catalogue

**All 230 space groups, in both spin conventions: 460 accepted four-data results.**
Each result includes $(e_1,n_1,n_3,\nu_4)$, complete stacking relations and the
neutral E8 decoration. The full rank-three translation subgroup is retained.

| Physical spin | Readable results | Download |
|---|---|---|
| Spinless | [230-row table](../current/3p1d/spinless/space_groups.md) | [CSV](../current/3p1d/spinless/space_groups.csv) · [JSON](../current/3p1d/spinless/space_groups.json) |
| Spin-1/2 | [230-row table](../current/3p1d/spin_half/space_groups.md) | [CSV](../current/3p1d/spin_half/space_groups.csv) · [JSON](../current/3p1d/spin_half/space_groups.json) |

See the [3+1D formula guide](../../docs/formulas/THREE_DIMENSIONAL.md) for
obstructions, stacking, gauge identifications and the selected model's exact
neutral-section factorization. The tables put E8 first and keep literature
sources separate. Their Song–Xiong–Huang comparison concerns the **neutral E8
layer only**; it is not a match claim for the full interacting electronic group.

The [accepted collection](collection.json) binds the unchanged
[full results](3p1d/space_groups/results.json),
[CI parents](3p1d/space_groups/ci_results.json),
[validation](3p1d/space_groups/validation.json) and
[parent provenance](3p1d/space_groups/provenance.json).
The original execution statuses are **389 ordinary complete and 71 recovered
complete** CI records; all 460 E8 records are complete. Recovery retains completed
native output and its explicit acceptance certificate without asserting an
unobserved process exit. The saved [assembly proof](provenance/assembly/assembly.json)
selects each background exactly once from 15 accepted parent pairs. Original
campaign selections and historical paths are retained as provenance.

The final tail is documented by the
[SG226 spinless evidence](../spacegroup_campaign_20261015/completed_h_226_spinless/README.md),
[SG230 spinless evidence](../spacegroup_campaign_20261015/preserved_h_230_spinless/README.md)
and [spin-1/2 tail evidence](../spacegroup_campaign_20261015/completed_h_tail_highmem/README.md).
Other campaign evidence remains in the
[campaign archive](../spacegroup_campaign_20261015/).

Run the portable offline audit with Python, SymPy and this checkout:

```sh
python3 results/spacegroup_full_20261015/verify.py
```

For a relocated package, pass `--repository /path/to/checkout`. The verifier
requires the five helper files pinned by the assembly proof and the exact 460
catalogue inputs; it does not contact the cluster or read historical absolute
paths. It checks all saved hashes, original result serialization and CI/E8 parent
bindings, disjoint selection, native root/witness structure and saved completion
certificates. It recomputes integer Smith groups, filling relations, all three CI
filtration groups and the complete signed affine E8 $H^1$ cocycles and gauge
witnesses. It does **not** rerun nonlinear CI cochains or the external recovery
ledgers; their original acceptance remains explicitly recorded.

These are accepted computations of the supplied four-data model. The records
retain `physicalClassificationCertified: false`: the physical CI-kernel
identification remains a separate question.
