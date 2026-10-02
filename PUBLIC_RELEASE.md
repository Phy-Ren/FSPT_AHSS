# Complete-formula release and reproduction

This release continues the existing public history of
[Phy-Ren/FSPT_AHSS](https://github.com/Phy-Ren/FSPT_AHSS). Its source pin and public
packaging overlays are recorded in [COMPLETE_RELEASE_MANIFEST.json](COMPLETE_RELEASE_MANIFEST.json).
It includes executable definitions, coefficient tables, the independent group
engine, exact inputs and completed examples. No source ZIP is required at runtime
or to recompile the core formulas.

## Current results

[results/complete_formulas/index.json](results/complete_formulas/index.json) is the
machine-readable inventory. Every record names its exported result, SHA-256,
calculation input, dimension, formula coordinate, group, collection memberships
and independent-target status. An empty invariant list means the trivial group;
`0` denotes an infinite cyclic factor; `n>1` denotes `Z/n`.

The separately dated [2026-10-02 supplement](results/complete_formulas_20261002_supplement/README.md)
adds five accepted finite inputs, S4 and four bosonic Q24 backgrounds. Pass its index with `--index`
to the reproduction and verification commands. The original 832 records remain
unchanged.

The archived JSON records preserve all scientific fields, including the full
integer presentation, generators, incoming gauge witnesses, obstruction records,
source hashes and timing metadata. Export removes only the top-level
`source_snapshot` field, which named a machine-local directory. It then serializes
JSON with sorted keys. Both the original raw-byte hash and exported-byte hash are
recorded. Archived source IDs identify the original computation versions; a new
run freezes the current public runtime and receives a new source ID.

The final decoration filtration follows the complete incoming gauge quotient.
`rawSurvivingLayers` is an intermediate classification result and must not be
substituted for that final filtration. A nonzero obstruction cochain may be exact:
only a nontrivial cohomology class obstructs a candidate.

## Exact finite inputs

Each finite record has a one-model input catalog. Its `productTable` is one-based,
with the identity first; `s1` is a binary homomorphism and `omega2` is a normalized
binary central-extension cocycle. `generatorIndices` uses the same one-based
indexing. These specify the bosonic quotient, antiunitary grading and fermionic
extension completely. The canonical catalog and historical section/isomorphism
certificates are also included.

For crystalline records, the input is the space-group number or crystallographic
point-group index plus the physical crystalline spin convention. The production
GAP constructors and background routines are included. The point-group JSON also
records its finite matrix realization.

```sh
python3 scripts/run_complete_example.py --case d4_D8_orbit_005 \
  --output runs/spin_q16_4d.json --dry-run
```

Remove `--dry-run` to compute. The wrapper reads only the exact input and retained
performance settings before solving. Afterward it independently checks integer
arithmetic and compares the resulting group to the saved answer. Expected groups
are never inputs to classification or stacking. `--audit` additionally checks all generator inverses and the recorded selection
of commutators and triples. The result's `coherenceAudit.allGeneratorTriples`
flag states whether every generator triple was tested. This can be much more
expensive than the basic calculation.

## Optional finite resolutions

The finite runner accepts one alternate resolution at a time:

| Option | Scope |
|---|---|
| `--tensor-abelian` | Tensor products of cyclic resolutions for finite abelian groups |
| `--dihedral-resolution` | Standard permutation presentation of a dihedral group |
| `--input-generators-resolution` | The exact generators listed in the input catalog, before PC conversion |
| `--direct-product-resolution D8xC2` | Standard D8 and C2 factor resolutions |
| `--direct-product-resolution Q8xC2` | Explicit two-generator Q8 and C2 factor resolutions |

D8 and Q8 both have order eight. The new strategies transport all integral
boundary and contraction coefficients back to the original input group. The
grading, extension cocycle, and formulas remain attached to that original group.
A mismatched family or a generator list that fails to generate the input is an
error. No alternate strategy is selected automatically.

For a published finite input, the reproduction wrapper retains
`finiteResolutionStrategy` when present (otherwise the default), or accepts an
explicit override:

```sh
python3 scripts/run_complete_example.py --case d4_Q8_w0_s0 \
  --resolution input-generators --output runs/q8_marked.json --dry-run
```

Remove `--dry-run` to compute on an allocated node. Strategies can change the
resolution basis and the displayed representative coordinates; compare the
exact input, final group and filtration rather than untransported vector entries.
The chosen strategy is saved in every new finite result.

[Resolution certificates](results/resolution_certificates/README.md) include
complete integral boundaries, contractions and transport tables for both direct
products, with a standalone Python replay checker. Their recorded profile times
measure resolution construction and verification, not a full FSPT calculation.
The original [complete release manifest](COMPLETE_RELEASE_MANIFEST.json) remains
the inventory at commit `78d83512`; subsequent option changes are recorded in
[RESOLUTION_UPDATE.json](RESOLUTION_UPDATE.json).

## Self-contained checks

Use a fresh output directory on an allocated compute node:

```sh
python3 scripts/check_complete_release.py --gap "$AFS_GAP" \
  --output runs/release_check --recompile-formulas
```

This checks the saved inventory and integer arithmetic, recompiles every retained
core DAG from the readable formula source and compares its instructions and
outputs exactly, then runs small complete 1D, 2D, 3D, 4D, point-group and space-group
examples with coherence checks. The compiler's source-file inventory naturally
changes under public packaging; mathematical programs must agree exactly.

To compile one formula into a separate directory:

```sh
python3 -m fspt.full_formula.compiler \
  --source formulas/publication_source --target high6 \
  --out runs/recompiled/high6.json
```

The production runtime supports Python 3.8. Recompiling the supplied readable
source requires Python 3.9 or newer; pass `--compiler-python /path/to/python3.11`
when the runtime interpreter is older.

The optional exact cylinder and specialization compilers are in `scripts/`.
They compose existing mathematical programs without dropping terms. Use a
separate data directory when rebuilding them; do not overwrite retained results.

The older `scripts/publish_snapshot.py` reproduces the earlier archive layout.
It does not build this new complete-formula release and should not be used to
replace its result inventory.
