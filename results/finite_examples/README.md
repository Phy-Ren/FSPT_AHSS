# Finite internal-symmetry examples

This is a historical archive. See the [current complete-formula results](../complete_formulas/README.md) for the full updated classification and stacking calculations.

This release contains exact symmetry inputs and independently computed results
for 53 finite backgrounds: **16 full 3+1D stacking groups** and **53 4+1D
associated-graded classifications**. The collections retain the original 43
four-dimensional table entries, sixteen backgrounds in both dimensions, and
eight p+ip calibration controls. Identical multiplication/sign/extension arrays
are stored once; their original names and character conventions remain aliases.

- [3+1D layers and full groups](tables/classification_3d.md), [CSV](tables/classification_3d.csv).
- [4+1D graded layers](tables/classification_4d.md), [CSV](tables/classification_4d.csv).
- [Exact model catalog](models.json), [collection membership](collections/finite_16.json),
  [original 43 entries](collections/four_dimensional_43.json), [p+ip controls](collections/pip_controls.json).
- [Numerical provenance](provenance.json), [file and production-source hashes](manifest.json).
- [Computed cochain and geometric calibrations](calibrations/README.md):
  Q8 d3 detectors, V4 Euler, D8 d4, C2 exact phases, and the Spin-c period on T2 x CP2.

The full group is generally an extension of the surviving layers. All sixteen
3+1D full groups use the complete known Majorana/CF/bosonic U4 product. Every
possible remaining p+ip-to-CF and p+ip-to-bosonic carry is retained; the abstract
group is unchanged throughout that family. A unique group can have a nontrivial
extension, such as the C16 result for antiunitary C2 with nonzero omega.

The 4+1D table states the graded layers, without assuming their direct sum is
the full stacking group. For Q8 with zero sign and omega, the additional
[square certificate](certificates/Q8_w0_s0_square.json) proves the full group
is C2 x C2: its Majorana square has zero CF class, and no bosonic layer remains.

## Exact conventions

Each model fixes the **finite internal** symmetry data `(G_b, s1, omega2)`;
no crystalline embedding or physical spin convention is implied. The
`order` field is the order of G_b, not its fermion-parity central extension.
The full group law is explicit, so differing historical dihedral names are
unambiguous. Q8, Q16, D8 and D16 in the main sixteen-model collection have
orders 8, 16, 8 and 16 respectively.

`productTable`, `generatorIndices`, and the identity element use **one-based**
indexing, with identity 1. The entry `s1[g-1]=1` means an antiunitary element;
`omega2[g-1][h-1]` is the normalized binary fermion-parity extension cocycle.
Aliases retain formulas for these characters and the enumeration convention.
An exact-input SHA256 is computed from canonical JSON containing `order`,
`productTable`, `s1`, and `omega2`.

Group arrays are invariant factors: `[]` is trivial and `[2,4]` means C2 x C4.
Result files retain operation matrices, native cohomology data, lower stacking
presentations and witnesses, and p+ip page evaluations. A nonzero original
cohomology class need not be an obstruction: the allowed lower adjustments must
first be quotiented out. Only a nonzero final quotient class kills a candidate.
In particular, `d3Raw` and `d4Raw` contain original cohomology coordinates,
not pointwise cochain values; `d3` and `d4` are the final quotient coordinates.
When `phaseSkipped` or a zero-target certificate records skipped evaluation,
the stored placeholder zero is not evidence that the original cochain vanished.

## Reproduce one result

Use Python 3.8 or newer and GAP with HAP, Polycyclic and the JSON package. The
tested environment is GAP 4.13.1, HAP 1.62 and Polycyclic 2.16. The production
cochain programs are included; no formula ZIP, private reference, external answer
table, or SptSet package is required.

Run these commands from the repository root. Set `AFS_GAP=/path/to/gap` if GAP
is not on PATH, or pass `--gap /path/to/gap`.

```sh
python3 scripts/run_finite_example.py --list
python3 scripts/run_finite_example.py --model Q16_wref2_srot \
  --dimension 3 --output runs/finite/Q16_3d.json --check
python3 scripts/run_finite_example.py --model D16_wref2_srot \
  --dimension 3 --output runs/finite/D16_3d.json --check
python3 scripts/run_finite_example.py --model Q8_w0_s0 \
  --dimension 4 --output runs/finite/Q8_4d.json --check
python3 scripts/run_finite_example.py --model C2_w1_s0 \
  --dimension 4 --output runs/finite/C2_4d.json --check
python3 scripts/run_finite_example.py --model Q8_w0_s0 --dimension 4 \
  --q8-square --output runs/finite/Q8_square.json --check
```

`--dimension 3` means 3+1D; `--dimension 4` means 4+1D. The 3+1D calculation
computes classification and then stacking in the same GAP process. `--check`
compares the resulting graded/full groups with the published case. Native
bases and cochain representatives can change with GAP/HAP versions; comparison
of abstract groups is independent of those choices.

The Python launcher locates `results/finite_examples/models.json` by default.
An explicit `--catalog /path/to/models.json` also works. It checks GAP's positive
completion marker and reports failures instead of accepting a bare zero exit
code. Every invocation writes only the requested output and temporary drivers.
The CLI accepts the canonical IDs printed by `--list`. Historical names and
character conventions, including D4 for a dihedral group of order eight, are
preserved in each model's aliases rather than treated as additional CLI IDs.

## Reproduce the collection

Independent model/dimension pairs can run in parallel. Set the worker count to
the number of CPUs allocated to the computation; do not run a batch on a cluster
login node. The largest current single case, 4+1D D16 with reflection-square
omega and rotation sign, took about 18 minutes on the tested compute node.

```python
import concurrent.futures
import json
from pathlib import Path
import subprocess
import sys

models = json.loads(Path('results/finite_examples/models.json').read_text())['models']
jobs = [(m['id'], d) for m in models for d in m['verified_dimensions']]
def run(job):
    name, dimension = job
    subprocess.run([sys.executable, 'scripts/run_finite_example.py',
                    '--model', name, '--dimension', str(dimension),
                    '--output', f'runs/finite/d{dimension}_{name}.json', '--check'], check=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=8) as pool:
    list(pool.map(run, jobs))
```

For data and publication-policy checks without GAP, run
`PYTHONPATH=tests python3 -m unittest test_finite_examples test_publish_snapshot`.
The published model arrays and saved answers are separate from the numerical
engine; only the explicit symmetry input enters the calculation.
