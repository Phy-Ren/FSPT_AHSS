# Classification and stacking groups

Complete tables for 230 space groups and 32 crystallographic point groups in each crystalline spin convention. The four decoration layers and final abstract stacking group are listed separately.

| Crystalline convention | Equivalent internal convention | Effective background |
| --- | --- | --- |
| spin-1/2 | spinless | `s=w1, omega=0` |
| spinless | spin-1/2 | `s=w1, omega=w2+w1^2` |

- Space groups, crystalline spin-1/2: [230-row table](space_groups_spin_half_230.md), [CSV](space_groups_spin_half_230.csv).
- Space groups, crystalline spinless: [230-row table](space_groups_spinless_230.md), [CSV](space_groups_spinless_230.csv).
- Finite point groups, both conventions: [64-row table](point_groups_64.md), [CSV](point_groups_64.csv).
- [32-row point-group summary with both full groups](point_groups_full_32.md).

The space groups include translations, weak phases and atomic fermion parity. The point groups are finite matrix groups without translations.

CSV group cells contain invariant-factor arrays: `[]` is trivial, each `0` contributes `Z`, and each positive entry n contributes `Zn`. Source IDs and result SHA-256 hashes are included per row. [manifest.json](manifest.json) records all 524 input digests, frozen sources and generated table hashes. All 2,620 group-valued cells in each of the CSV and Markdown representations are parsed back and compared with the original result JSON. The 32-row summary is checked separately.
