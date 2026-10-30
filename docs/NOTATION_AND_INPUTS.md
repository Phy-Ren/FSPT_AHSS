# Fixed symmetry notation and current inputs

The same definitions apply to the manuscript, current mathematical guides, Python APIs, GAP contexts, and generated symmetry inputs.
They are not interchangeable names for a single sign.

| Symbol | JSON/GAP field | Meaning |
| --- | --- | --- |
| `rho1` | `rho` | Action on the charge circle: `g U(theta) g^-1 = U((-1)^rho1(g) theta)` |
| `s1` | `s` | Antiunitarity: `g i g^-1 = (-1)^s1(g) i` |
| `r1=rho1+s1 mod 2` | `r` | Charge reversal: `g Q g^-1 = (-1)^r1(g) Q` |

Only two characters are independent.
Writing `U(theta)=exp(i theta Q)` gives the displayed relation because conjugation acts on both `i` and `Q`.
Sheets and additive phases carry sign `s1`, integral charge carries sign `r1`, and the real extension lift carries sign `rho1`.
Thus charge differentials use `d_r`, while the extension Bockstein uses `d_rho`.

| Operation | `s1` | `rho1` | `r1` |
| --- | --- | --- | --- |
| Unitary charge-preserving operation | 0 | 0 | 0 |
| Unitary charge conjugation | 0 | 1 | 1 |
| Ordinary charge-preserving time reversal | 1 | 1 | 0 |
| Antiunitary charge reversal | 1 | 0 | 1 |

For the initially unitary, charge-preserving spatial symmetries in the crystalline catalogue, effective internal symmetry has `s1=r1=w1` and `rho1=0`, where `w1` records orientation reversal.
Physical spin labels and the fermionic extension representatives are unchanged by this notation migration.
In particular, a mirror's effective internal operation is not ordinary charge-preserving time reversal.

## Current schema

Current local-evaluation requests and generated group backgrounds use schema version 2.
An unversioned input with explicit `s,r` is unambiguously current and defaults to version 2; generated backgrounds still write the explicit `schema_version:2` tag.
The fields `s` and `r` are required.
If `rho` is supplied, it must equal `r XOR s` at every entry; otherwise the evaluator derives it.
Generated catalogue records emit all three fields.
The retained catalogue metadata `circle_action` is a redundant copy of `rho` and must agree with it.
All character entries are integer bits, with equal array lengths and the additional character and normalization checks appropriate to the input domain.

The [JSON schema](../schemas/background_v2.schema.json) records the common field types.
Pointwise XOR, equal lengths, and group-character identities are semantic checks performed by the executable validators.
Local worker arrays have one entry per simplex vertex; catalogue arrays have one entry per finite-holonomy element, in the recorded element order.
For wallpaper and space groups these arrays do not replace the full affine group used in cohomology.

A current two-vertex example of ordinary time reversal is:

```json
{"schema_version":2,"s":[0,1],"r":[0,0],"rho":[0,1]}
```

The corresponding antiunitary charge-reversing example is:

```json
{"schema_version":2,"s":[0,1],"r":[0,1],"rho":[0,0]}
```

These are background fragments; a local evaluation additionally supplies its operation, dimension, simplex dimension, and cochains.
See the [executable-interface guide](formulas/IMPLEMENTATION.md) for a complete request.

## Historical inputs

The adopted v0.7/v0.9/v0.15 source packages, old run inputs, and frozen reference fixtures used `rho` for charge reversal.
Their explicit translation is:

| Historical field or formula | Current field or formula |
| --- | --- |
| `s_old` | `s` |
| `rho_old` | `r` |
| `rho_old+s_old` | `rho` |
| `d_(rho_old)` on charge | `d_r` |
| `d_(rho_old+s_old)` on the extension | `d_rho` |

An old `rho`-only request without `r` is ambiguous and is rejected by the current worker.
Omitting the version tag does not make an explicit `s,r` input historical.
Code deliberately reading an old record must call the explicit `migrate_legacy_request` adapter, or mark a request with both `schema_version:1` and `notation:"legacy-charge-rho"` at the documented legacy boundary.
The migration copies `rho_old` to `r`, computes `rho=r XOR s`, and validates any historical `circle_action` against that result.
The direct `Symmetry` interface uses `r1`; `Symmetry.from_legacy` is the explicit boundary for historical charge-`rho` arguments.
Never change an archived record in place merely to satisfy a current interface.

For a historical file, the conversion command writes a separate new file and refuses to replace an existing output:

```sh
python scripts/migrate_symmetry_input.py historical_input.json new_input_v2.json
```

The current `insulator_catalog/generated` JSON/GAP files are schema-v2 inputs.
Their migration preserves every geometric matrix, multiplication table, affine relation, extension value, and physical spin label.
The [catalogue migration record](../insulator_catalog/notation_migration.json) records the original and current hashes and the inverse-renaming check for all 578 backgrounds.
By contrast, versioned formula-source files and regression vectors under `formulas`, dated calculation records under `results`, reference runs under `benchmarks`, and dated research campaigns retain their original bytes and notation.
The current result tables keep their original response-sector scope and classification values; this naming change does not recompute or reinterpret them.
Undated active guides use the current notation, while a cited paper's unrelated representation symbol remains that paper's notation.

## Maintaining the convention

Any new formula or input must state which of the three actions it uses and satisfy `r1=rho1+s1` modulo two.
Source, product, gauge, and coefficient-transport expressions must be migrated together.
Tests must distinguish ordinary time reversal from antiunitary charge reversal, reject inconsistent supplied characters, and retain the old exact outputs through explicit legacy adaptation.
No future compatibility shortcut may make current `rho` silently mean charge reversal again.
